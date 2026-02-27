"""
Proposition Parser Service
Parses and normalizes user historical propositions.
"""

import re
from typing import List, Dict, Any, Optional
from datetime import date
import spacy
from langdetect import detect

from app.schemas import PropositionParsed, TimeWindow


class PropositionParser:
    """Parse and normalize user propositions for historical analysis."""
    
    # Historical keywords for time period inference
    HISTORICAL_PERIODS = {
        "kurtuluş savaşı": (date(1919, 5, 19), date(1923, 10, 29)),
        "independence war": (date(1919, 5, 19), date(1923, 10, 29)),
        "birinci dünya savaşı": (date(1914, 7, 28), date(1918, 11, 11)),
        "wwi": (date(1914, 7, 28), date(1918, 11, 11)),
        "world war i": (date(1914, 7, 28), date(1918, 11, 11)),
        "osmanlı": (date(1299, 1, 1), date(1922, 11, 1)),
        "ottoman": (date(1299, 1, 1), date(1922, 11, 1)),
        "tanzimat": (date(1839, 11, 3), date(1876, 2, 14)),
        "meşrutiyet": (date(1876, 12, 23), date(1918, 11, 11)),
    }
    
    # Ambiguous terms that need operational definitions
    AMBIGUOUS_TERMS = {
        "iş yapmak": ["diplomatic_contact", "economic_agreement", "intelligence_cooperation", "trade_relations"],
        "çalışmak": ["collaboration", "employment", "espionage"],
        "ilişki": ["diplomatic_relations", "personal_relationship", "trade_relations"],
        "work with": ["collaboration", "negotiation", "trade"],
        "relationship": ["diplomatic", "personal", "economic"],
    }
    
    # Claim type indicators
    CLAIM_TYPE_PATTERNS = {
        "diplomatic": ["diplomasi", "diplomatic", "müzakere", "negotiation", "görüşme", "meeting"],
        "economic": ["ekonomi", "economic", "ticaret", "trade", "para", "money", "sözleşme", "contract"],
        "military": ["askeri", "military", "savaş", "war", "ordu", "army", "silah", "weapon"],
        "intelligence": ["istihbarat", "intelligence", "casus", "spy", "gizli", "secret"],
        "propaganda": ["propaganda", "basın", "press", "yayın", "publication"],
    }
    
    def __init__(self):
        """Initialize the parser with NLP models."""
        # Load spaCy model for NER (would use tr_core_news_sm for Turkish if available)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback: download model if not present
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
    
    async def parse(self, proposition: str) -> PropositionParsed:
        """
        Parse a historical proposition into structured data.
        
        Args:
            proposition: Raw user proposition text
            
        Returns:
            PropositionParsed: Structured proposition data
        """
        # Detect language
        try:
            lang = detect(proposition)
        except:
            lang = "tr"  # Default to Turkish
        
        # Extract entities
        entities = self._extract_entities(proposition)
        
        # Infer time window
        time_window = self._infer_time_window(proposition)
        
        # Extract geography
        geography = self._extract_geography(proposition, entities)
        
        # Determine claim type
        claim_type = self._determine_claim_type(proposition)
        
        # Find ambiguous terms
        ambiguity_terms = self._find_ambiguous_terms(proposition, lang)
        
        # Create normalized definitions
        normalized_definitions = self._create_definitions(ambiguity_terms)
        
        return PropositionParsed(
            entities=entities,
            time_window=time_window,
            geography=geography,
            claim_type=claim_type,
            ambiguity_terms=ambiguity_terms,
            normalized_definitions=normalized_definitions
        )
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract named entities from text using NLP."""
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG", "GPE", "NORP"]:
                entities.append(ent.text)
        
        # Also add specific patterns for Turkish historical figures
        turkish_patterns = [
            r"Mustafa Kemal(?: Atatürk)?",
            r"Atatürk",
            r"İsmet İnönü",
            r"Enver Paşa",
            r"Talat Paşa",
            r"Cemal Paşa",
        ]
        
        for pattern in turkish_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities.extend(matches)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_entities = []
        for e in entities:
            if e.lower() not in seen:
                seen.add(e.lower())
                unique_entities.append(e)
        
        return unique_entities
    
    def _infer_time_window(self, text: str) -> TimeWindow:
        """Infer time window from historical references in text."""
        text_lower = text.lower()
        
        # Check for explicit year ranges
        year_pattern = r"(\d{4})\s*[-–]\s*(\d{4})"
        matches = re.findall(year_pattern, text)
        if matches:
            start_year, end_year = matches[0]
            return TimeWindow(
                start=date(int(start_year), 1, 1),
                end=date(int(end_year), 12, 31)
            )
        
        # Check for single year with context
        single_year_pattern = r"(\d{4})'(?:te|de|ta|da)"
        matches = re.findall(single_year_pattern, text)
        if matches:
            year = int(matches[0])
            return TimeWindow(
                start=date(year, 1, 1),
                end=date(year, 12, 31)
            )
        
        # Check for historical periods
        for period, (start, end) in self.HISTORICAL_PERIODS.items():
            if period in text_lower:
                return TimeWindow(start=start, end=end)
        
        # Default: return empty time window
        return TimeWindow(start=None, end=None)
    
    def _extract_geography(self, text: str, entities: List[str]) -> List[str]:
        """Extract geographic locations from text and entities."""
        geography = []
        
        # Check entities for locations
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "GPE":  # Geopolitical Entity
                geography.append(ent.text)
        
        # Check for specific country mentions
        country_patterns = {
            "turkey": ["türkiye", "turkey", "osmanlı", "ottoman"],
            "uk": ["ingiltere", "britain", "england", "uk", "birleşik krallık"],
            "france": ["fransa", "france"],
            "greece": ["yunanistan", "greece", "yunan"],
            "germany": ["almanya", "germany"],
            "russia": ["rusya", "russia", "soviet"],
        }
        
        text_lower = text.lower()
        for country, patterns in country_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    geography.append(country)
                    break
        
        # Remove duplicates
        return list(set(geography)) if geography else ["Turkey"]
    
    def _determine_claim_type(self, text: str) -> Optional[str]:
        """Determine the type of historical claim."""
        text_lower = text.lower()
        
        type_scores = {}
        for claim_type, patterns in self.CLAIM_TYPE_PATTERNS.items():
            score = sum(1 for pattern in patterns if pattern in text_lower)
            if score > 0:
                type_scores[claim_type] = score
        
        if type_scores:
            return max(type_scores, key=type_scores.get)
        
        return None
    
    def _find_ambiguous_terms(self, text: str, lang: str) -> List[str]:
        """Find ambiguous terms that need operational definitions."""
        text_lower = text.lower()
        found = []
        
        for term, definitions in self.AMBIGUOUS_TERMS.items():
            if term in text_lower:
                found.append(term)
        
        return found
    
    def _create_definitions(self, ambiguity_terms: List[str]) -> Dict[str, List[str]]:
        """Create operational definitions for ambiguous terms."""
        definitions = {}
        
        for term in ambiguity_terms:
            if term in self.AMBIGUOUS_TERMS:
                definitions[term] = self.AMBIGUOUS_TERMS[term]
        
        return definitions
