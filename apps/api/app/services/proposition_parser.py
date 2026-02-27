"""
Proposition Parser Service
Parses and normalizes user historical propositions.
"""

import re
from typing import List, Dict, Any, Optional
from datetime import date

from langdetect import detect

from app.schemas import PropositionParsed, TimeWindow

try:
    import spacy as _spacy
except ImportError:  # pragma: no cover - optional dependency in lightweight setups
    class _SpaCyStub:
        @staticmethod
        def load(*_args, **_kwargs):
            raise OSError("spaCy is not installed")

    _spacy = _SpaCyStub()

spacy = _spacy


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
        """Initialize the parser with an NLP model when available."""
        self.nlp = None
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception:
            # Fallback mode keeps service operational without runtime model download.
            self.nlp = None

    async def parse(self, proposition: str) -> PropositionParsed:
        """
        Parse a historical proposition into structured data.

        Args:
            proposition: Raw user proposition text

        Returns:
            PropositionParsed: Structured proposition data
        """
        try:
            lang = detect(proposition)
        except Exception:
            lang = "tr"

        entities = self._extract_entities(proposition)
        time_window = self._infer_time_window(proposition)
        geography = self._extract_geography(proposition, entities)
        claim_type = self._determine_claim_type(proposition)
        ambiguity_terms = self._find_ambiguous_terms(proposition, lang)
        normalized_definitions = self._create_definitions(ambiguity_terms)

        return PropositionParsed(
            entities=entities,
            time_window=time_window,
            geography=geography,
            claim_type=claim_type,
            ambiguity_terms=ambiguity_terms,
            normalized_definitions=normalized_definitions,
        )

    def _extract_entities(self, text: str) -> List[str]:
        """Extract named entities from text using NLP when available."""
        entities: List[str] = []

        if self.nlp is not None:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in ["PERSON", "ORG", "GPE", "NORP"]:
                    entities.append(ent.text)

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

        seen = set()
        unique_entities = []
        for entity in entities:
            key = entity.lower()
            if key not in seen:
                seen.add(key)
                unique_entities.append(entity)

        return unique_entities

    def _infer_time_window(self, text: str) -> TimeWindow:
        """Infer time window from historical references in text."""
        text_lower = text.lower()

        year_pattern = r"(\d{4})\s*[-–]\s*(\d{4})"
        matches = re.findall(year_pattern, text)
        if matches:
            start_year, end_year = matches[0]
            return TimeWindow(start=date(int(start_year), 1, 1), end=date(int(end_year), 12, 31))

        between_pattern = r"(?:between|arasında)\s+(\d{4})\s+(?:and|ile)\s+(\d{4})"
        between_matches = re.findall(between_pattern, text_lower)
        if between_matches:
            start_year, end_year = between_matches[0]
            return TimeWindow(start=date(int(start_year), 1, 1), end=date(int(end_year), 12, 31))

        single_year_pattern = r"(\d{4})'(?:te|de|ta|da)"
        matches = re.findall(single_year_pattern, text)
        if matches:
            year = int(matches[0])
            return TimeWindow(start=date(year, 1, 1), end=date(year, 12, 31))

        for period, (start, end) in self.HISTORICAL_PERIODS.items():
            if period in text_lower:
                return TimeWindow(start=start, end=end)

        return TimeWindow(start=None, end=None)

    def _extract_geography(self, text: str, _entities: List[str]) -> List[str]:
        """Extract geographic locations from text."""
        geography = []

        if self.nlp is not None:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ == "GPE":
                    geography.append(ent.text)

        country_patterns = {
            "Turkey": ["türkiye", "turkey", "osmanlı", "ottoman"],
            "UK": ["ingiltere", "britain", "england", "uk", "birleşik krallık"],
            "France": ["fransa", "france"],
            "Greece": ["yunanistan", "greece", "yunan"],
            "Germany": ["almanya", "germany"],
            "Russia": ["rusya", "russia", "soviet"],
        }

        text_lower = text.lower()
        for country, patterns in country_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                geography.append(country)

        return list(set(geography)) if geography else ["Turkey"]

    def _determine_claim_type(self, text: str) -> Optional[str]:
        """Determine the type of historical claim."""
        text_lower = text.lower()
        type_scores: Dict[str, int] = {}

        for claim_type, patterns in self.CLAIM_TYPE_PATTERNS.items():
            score = sum(1 for pattern in patterns if pattern in text_lower)
            if score > 0:
                type_scores[claim_type] = score

        return max(type_scores, key=type_scores.get) if type_scores else None

    def _find_ambiguous_terms(self, text: str, _lang: str) -> List[str]:
        """Find ambiguous terms that need operational definitions."""
        text_lower = text.lower()
        found = [term for term in self.AMBIGUOUS_TERMS if term in text_lower]
        if "iş yap" in text_lower and "iş yapmak" not in found:
            found.append("iş yapmak")
        return found

    def _create_definitions(self, ambiguity_terms: List[str]) -> Dict[str, List[str]]:
        """Create operational definitions for ambiguous terms."""
        return {term: self.AMBIGUOUS_TERMS[term] for term in ambiguity_terms if term in self.AMBIGUOUS_TERMS}
