"""
Query Expansion Service
AI-powered multi-lingual query expansion for comprehensive historical retrieval.
Uses Gemini for intelligent query generation with historical context.
Falls back to dictionary-based expansion if AI is unavailable.
"""

import logging
from typing import List, Dict, Optional
from dataclasses import dataclass

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


@dataclass
class ExpandedQuery:
    """Expanded query for a specific language."""
    language: str
    original: str
    variants: List[str]
    keywords: List[str]


# ─── AI-Powered Query Generation ─────────────────────────────────

AI_EXPANSION_PROMPT = """You are a historical research query specialist.
Given a historical proposition, generate optimized search queries in {language_name} ({lang_code}).

Proposition: {proposition}
Time period: {time_start} to {time_end}
Entities: {entities}

Generate exactly 5 search queries in {language_name} that would find:
1. Official diplomatic documents and correspondence from this period
2. Academic research papers analyzing this topic
3. Period newspaper coverage and press reports
4. Treaty texts, agreements, or official protocols
5. Memoirs, diaries, or personal accounts

Rules:
- Use period-accurate terminology (e.g. "Angora" not "Ankara" for pre-1923 English sources)
- Include relevant person names, place names, and event names in {language_name}
- Each query should be optimized for web search engines
- Include date ranges or year references where helpful

Respond ONLY with a JSON array of 5 query strings, no explanation:
["query1", "query2", "query3", "query4", "query5"]"""


LANGUAGE_NAMES = {
    "tr": "Turkish",
    "en": "English",
    "fr": "French",
    "el": "Greek",
}


class QueryExpansionEngine:
    """Multi-lingual query expansion for historical source retrieval."""

    # ─── Fallback period terminology (used when AI is unavailable) ───
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

    DOC_TYPE_KEYWORDS = {
        "tr": ["anlaşma", "antlaşma", "tutanak", "görüşme", "yazışma", "rapor", "belge"],
        "en": ["treaty", "agreement", "correspondence", "dispatch", "memorandum", "report", "document"],
        "fr": ["traité", "accord", "correspondance", "dépêche", "mémorandum", "rapport", "document"],
        "el": ["συνθήκη", "συμφωνία", "αλληλογραφία", "έκθεση", "έγγραφο"],
    }

    SOURCE_KEYWORDS = {
        "tr": ["arşiv", "gazete", "dergi", "belge", "anı"],
        "en": ["archive", "newspaper", "press", "document", "memoir"],
        "fr": ["archive", "journal", "presse", "document", "mémoire"],
        "el": ["αρχείο", "εφημερίδα", "τύπος", "έγγραφο", "απομνημόνευμα"],
    }

    def __init__(self):
        """Initialize with optional AI model for intelligent expansion."""
        self._gemini_model = None

        if settings.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self._gemini_model = genai.GenerativeModel("gemini-2.0-flash")
                logger.info("AI query expansion enabled (Gemini)")
            except Exception as e:
                logger.warning(f"Gemini init failed for query expansion: {e}")

    def expand(
        self,
        proposition: str,
        entities: List[str],
        time_window: tuple,
        languages: List[str] = None
    ) -> Dict[str, ExpandedQuery]:
        """
        Expand a proposition into multi-lingual search queries.
        Uses AI when available, falls back to dictionary matching.
        """
        if languages is None:
            languages = ["tr", "en"]

        expanded = {}

        for lang in languages:
            # Try AI expansion first
            if self._gemini_model:
                ai_queries = self._ai_expand(proposition, entities, time_window, lang)
                if ai_queries:
                    expanded[lang] = ExpandedQuery(
                        language=lang,
                        original=proposition,
                        variants=ai_queries,
                        keywords=self._generate_keywords(lang)
                    )
                    continue

            # Fallback to dictionary-based expansion
            variants = self._generate_variants(proposition, entities, lang)
            keywords = self._generate_keywords(lang)

            expanded[lang] = ExpandedQuery(
                language=lang,
                original=proposition,
                variants=variants,
                keywords=keywords
            )

        return expanded

    def _ai_expand(
        self,
        proposition: str,
        entities: List[str],
        time_window: tuple,
        lang: str
    ) -> Optional[List[str]]:
        """Generate queries using AI model."""
        try:
            time_start = str(time_window[0]) if time_window[0] else "unknown"
            time_end = str(time_window[1]) if time_window[1] else "unknown"

            prompt = AI_EXPANSION_PROMPT.format(
                proposition=proposition,
                language_name=LANGUAGE_NAMES.get(lang, lang),
                lang_code=lang,
                time_start=time_start,
                time_end=time_end,
                entities=", ".join(entities) if entities else "none specified",
            )

            response = self._gemini_model.generate_content(prompt)
            text = response.text.strip()

            # Parse JSON array from response
            import json
            import re

            # Try extracting JSON array
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                queries = json.loads(match.group())
                if isinstance(queries, list) and len(queries) > 0:
                    return [str(q) for q in queries[:5]]

        except Exception as e:
            logger.warning(f"AI query expansion failed for {lang}: {e}")

        return None

    def _generate_variants(
        self,
        proposition: str,
        entities: List[str],
        lang: str
    ) -> List[str]:
        """Fallback: Generate query variants using dictionary matching."""
        variants = []
        period_terms = self.PERIOD_TERMS.get(lang, {})

        for entity in entities:
            entity_lower = entity.lower()
            if entity_lower in period_terms:
                for variant in period_terms[entity_lower]:
                    new_variant = proposition.lower().replace(entity_lower, variant)
                    if new_variant != proposition.lower():
                        variants.append(new_variant)

        for entity in entities:
            variants.append(entity)

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
        Generate concrete search queries for the deep research engine.

        Returns:
            List of {"query": str, "language": str, "type": str} dicts
        """
        queries = []

        for lang, query in expanded.items():
            # Add each variant as a standalone query
            for variant in query.variants:
                queries.append({
                    "language": lang,
                    "query": variant,
                    "type": "ai_generated" if self._gemini_model else "dictionary_variant",
                })

            # For dictionary fallback, also combine with keywords
            if not self._gemini_model:
                for variant in query.variants[:3]:
                    for keyword in query.keywords[:3]:
                        queries.append({
                            "language": lang,
                            "query": f"{variant} {keyword}",
                            "type": "variant_keyword"
                        })

        return queries
