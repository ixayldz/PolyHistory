"""
Query Expansion Service
Expands queries across multiple languages for comprehensive retrieval.
"""

from typing import List, Dict, Set
from dataclasses import dataclass


@dataclass
class ExpandedQuery:
    """Expanded query for a specific language."""
    language: str
    original: str
    variants: List[str]
    keywords: List[str]


class QueryExpansionEngine:
    """Multi-lingual query expansion for historical source retrieval."""
    
    # Period terminology mappings
    PERIOD_TERMS = {
        "tr": {
            "mustafa kemal": ["mustafa kemal", "kemal paşa", "atatürk"],
            "ankara government": ["ankara hükümeti", "anadolu hükümeti"],
            "istanbul government": ["istanbul hükümeti", "osmanlı hükümeti"],
            "national movement": ["milli mücadele", "milli hareket"],
        },
        "en": {
            "mustafa kemal": ["mustafa kemal", "kemal pasha", "atatürk", "ghazi"],
            "ankara government": ["angora government", "ankara government", "nationalist government"],
            "istanbul government": ["istanbul government", "ottoman government", "sultan's government"],
            "national movement": ["national movement", "turkish nationalists", "kemalists"],
        },
        "fr": {
            "mustafa kemal": ["mustafa kemal", "kemal pacha", "atatürk"],
            "ankara government": ["gouvernement d'angora", "gouvernement d'ankara"],
            "istanbul government": ["gouvernement d'istanbul", "gouvernement ottoman"],
            "national movement": ["mouvement national", "nationalistes turcs"],
        },
        "el": {
            "mustafa kemal": ["μουσταφά κεμάλ", "κεμάλ πασάς", "ατατούρκ"],
            "ankara government": ["κυβέρνηση της Άγκυρας"],
            "istanbul government": ["κυβέρνηση της Κωνσταντινούπολης"],
            "national movement": ["εθνικό κίνημα"],
        }
    }
    
    # Document type keywords by language
    DOC_TYPE_KEYWORDS = {
        "tr": ["anlaşma", "antlaşma", "muhtere", "tutanak", "görüşme", "yazışma", "rapor"],
        "en": ["treaty", "agreement", "convention", "protocol", "correspondence", "dispatch", "memorandum", "report"],
        "fr": ["traité", "accord", "convention", "protocole", "correspondance", "dépêche", "mémorandum", "rapport"],
        "el": ["συνθήκη", "συμφωνία", "σύμβαση", "πρωτόκολλο", "αλληλογραφία", "έκθεση"],
    }
    
    # Source type keywords
    SOURCE_KEYWORDS = {
        "tr": ["arşiv", "gazete", "dergi", "belge", "anı"],
        "en": ["archive", "newspaper", "press", "document", "memoir"],
        "fr": ["archive", "journal", "presse", "document", "mémoire"],
        "el": ["αρχείο", "εφημερίδα", "τύπος", "έγγραφο", "απομνημόνευμα"],
    }
    
    def __init__(self):
        """Initialize the query expansion engine."""
        pass
    
    def expand(
        self,
        proposition: str,
        entities: List[str],
        time_window: tuple,
        languages: List[str] = None
    ) -> Dict[str, ExpandedQuery]:
        """
        Expand a proposition into multi-lingual search queries.
        
        Args:
            proposition: Original proposition text
            entities: Extracted entities
            time_window: (start_date, end_date) tuple
            languages: List of target languages (default: ['tr', 'en'])
            
        Returns:
            Dict mapping language codes to ExpandedQuery objects
        """
        if languages is None:
            languages = ["tr", "en"]
        
        expanded = {}
        
        for lang in languages:
            variants = self._generate_variants(proposition, entities, lang)
            keywords = self._generate_keywords(lang)
            
            expanded[lang] = ExpandedQuery(
                language=lang,
                original=proposition,
                variants=variants,
                keywords=keywords
            )
        
        return expanded
    
    def _generate_variants(
        self,
        proposition: str,
        entities: List[str],
        lang: str
    ) -> List[str]:
        """Generate query variants for a specific language."""
        variants = []
        period_terms = self.PERIOD_TERMS.get(lang, {})
        
        # Replace entities with language-specific variants
        for entity in entities:
            entity_lower = entity.lower()
            if entity_lower in period_terms:
                for variant in period_terms[entity_lower]:
                    new_variant = proposition.lower().replace(entity_lower, variant)
                    if new_variant != proposition.lower():
                        variants.append(new_variant)
        
        # Add entity-only queries
        for entity in entities:
            variants.append(entity)
        
        # Remove duplicates
        return list(set(variants))
    
    def _generate_keywords(self, lang: str) -> List[str]:
        """Generate document type keywords for a language."""
        doc_keywords = self.DOC_TYPE_KEYWORDS.get(lang, [])
        source_keywords = self.SOURCE_KEYWORDS.get(lang, [])
        return doc_keywords + source_keywords
    
    def get_search_queries(
        self,
        expanded: Dict[str, ExpandedQuery],
        source_types: List[str] = None
    ) -> List[Dict]:
        """
        Generate concrete search queries for retrieval systems.
        
        Args:
            expanded: Output from expand()
            source_types: Filter by source types
            
        Returns:
            List of search query dictionaries
        """
        queries = []
        
        for lang, query in expanded.items():
            # Combine variants with keywords
            for variant in query.variants:
                for keyword in query.keywords:
                    queries.append({
                        "language": lang,
                        "query": f"{variant} {keyword}",
                        "type": "variant_keyword"
                    })
            
            # Add entity-focused queries
            for variant in query.variants[:3]:  # Limit to first 3 variants
                queries.append({
                    "language": lang,
                    "query": variant,
                    "type": "entity_focused"
                })
        
        return queries
