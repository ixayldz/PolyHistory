"""
AI Source Classifier
Classifies web research results into historical source categories using AI models.
"""

import logging
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from app.core.config import get_settings
from app.services.deep_research import ResearchResult

settings = get_settings()
logger = logging.getLogger(__name__)


@dataclass
class ClassifiedSource:
    """A research result classified into historical source categories."""
    title: str
    url: str
    content: str
    source_type: str  # primary, academic, secondary, press, memoir
    stance: str  # pro, contra, neutral
    country: str  # ISO country code
    language: str  # ISO language code
    publisher: str
    publication_date: Optional[str] = None
    relevance_score: float = 0.0


# Domain-to-country mapping for common institutional domains
DOMAIN_COUNTRY_MAP = {
    "devletarsivleri.gov.tr": "TR",
    "mfa.gov.tr": "TR",
    "dergipark.org.tr": "TR",
    "nationalarchives.gov.uk": "UK",
    "fco.gov.uk": "UK",
    "archives.gov": "US",
    "loc.gov": "US",
    "gallica.bnf.fr": "FR",
    "persee.fr": "FR",
    "europeana.eu": "EU",
    "treaties.un.org": "INT",
}

# Domain-to-source-type mapping
DOMAIN_SOURCE_TYPE = {
    "devletarsivleri.gov.tr": "primary",
    "nationalarchives.gov.uk": "primary",
    "archives.gov": "primary",
    "loc.gov": "primary",
    "gallica.bnf.fr": "primary",
    "scholar.google.com": "academic",
    "jstor.org": "academic",
    "academia.edu": "academic",
    "researchgate.net": "academic",
    "dergipark.org.tr": "academic",
    "cambridge.org": "academic",
    "oxford.ac.uk": "academic",
    "persee.fr": "academic",
    "arxiv.org": "academic",
    "treaties.un.org": "primary",
    "avalon.law.yale.edu": "primary",
}


class SourceClassifier:
    """
    Classify research results into historical source categories.
    
    Uses a two-pass approach:
    1. Rule-based: Domain matching for known institutional sources
    2. AI-based: Gemini/GPT classification for ambiguous sources
    """

    CLASSIFICATION_PROMPT = """You are a historical source classifier. Given a web research result,
classify it into the following categories. Respond ONLY with valid JSON.

Source types: primary, academic, secondary, press, memoir
Stance values: pro, contra, neutral (relative to the main proposition)
Country: ISO 2-letter code of the source's origin country

Research result:
Title: {title}
URL: {url}
Domain: {domain}
Content snippet: {content}

Proposition being analyzed: {proposition}

Respond with this exact JSON format:
{{"source_type": "...", "stance": "...", "country": "...", "publisher": "..."}}"""

    def __init__(self):
        self._gemini_model = None
        self._openai_client = None
        self._init_ai()

    def _init_ai(self):
        """Initialize AI client for classification (prefer Gemini for speed)."""
        if settings.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self._gemini_model = genai.GenerativeModel("gemini-2.0-flash")
            except Exception as e:
                logger.warning(f"Gemini init failed for classifier: {e}")

        if not self._gemini_model and settings.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self._openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception as e:
                logger.warning(f"OpenAI init failed for classifier: {e}")

    async def classify_results(
        self,
        results: List[ResearchResult],
        proposition: str,
    ) -> List[ClassifiedSource]:
        """
        Classify a list of research results into historical source categories.

        Args:
            results: Raw research results from DeepResearchEngine
            proposition: The original proposition being analyzed

        Returns:
            List of ClassifiedSource objects
        """
        classified = []

        for result in results:
            source = await self._classify_single(result, proposition)
            if source:
                classified.append(source)

        return classified

    async def _classify_single(
        self,
        result: ResearchResult,
        proposition: str,
    ) -> Optional[ClassifiedSource]:
        """Classify a single research result."""
        domain = result.source_domain

        # Pass 1: Rule-based classification from known domains
        source_type = DOMAIN_SOURCE_TYPE.get(domain)
        country = DOMAIN_COUNTRY_MAP.get(domain)

        if source_type and country:
            # Known institutional domain — use rule-based classification
            return ClassifiedSource(
                title=result.title,
                url=result.url,
                content=result.content[:1000],
                source_type=source_type,
                stance="neutral",  # Default for rule-based
                country=country,
                language=result.language,
                publisher=domain,
                publication_date=result.published_date,
                relevance_score=result.score,
            )

        # Pass 2: AI-based classification for unknown domains
        ai_classification = await self._classify_with_ai(result, proposition)

        return ClassifiedSource(
            title=result.title,
            url=result.url,
            content=result.content[:1000],
            source_type=ai_classification.get("source_type", "secondary"),
            stance=ai_classification.get("stance", "neutral"),
            country=ai_classification.get("country", self._guess_country(result)),
            language=result.language,
            publisher=ai_classification.get("publisher", domain),
            publication_date=result.published_date,
            relevance_score=result.score,
        )

    async def _classify_with_ai(
        self,
        result: ResearchResult,
        proposition: str,
    ) -> Dict[str, str]:
        """Use AI model to classify an ambiguous source."""
        prompt = self.CLASSIFICATION_PROMPT.format(
            title=result.title,
            url=result.url,
            domain=result.source_domain,
            content=result.content[:500],
            proposition=proposition,
        )

        # Try Gemini first (faster, cheaper)
        if self._gemini_model:
            try:
                response = self._gemini_model.generate_content(prompt)
                return self._parse_json_response(response.text)
            except Exception as e:
                logger.warning(f"Gemini classification failed: {e}")

        # Fallback to OpenAI
        if self._openai_client:
            try:
                response = self._openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=200,
                )
                return self._parse_json_response(response.choices[0].message.content)
            except Exception as e:
                logger.warning(f"OpenAI classification failed: {e}")

        # Final fallback: heuristic classification
        return self._heuristic_classify(result)

    def _parse_json_response(self, text: str) -> Dict[str, str]:
        """Extract JSON from AI response text."""
        try:
            # Try direct parse
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try extracting JSON from markdown code block
        try:
            import re
            match = re.search(r'\{[^}]+\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except (json.JSONDecodeError, AttributeError):
            pass

        return {}

    def _heuristic_classify(self, result: ResearchResult) -> Dict[str, str]:
        """Fallback heuristic classification based on URL and content patterns."""
        domain = result.source_domain.lower()
        content = (result.title + " " + result.content).lower()

        # Source type heuristics
        source_type = "secondary"
        if any(kw in domain for kw in ["archive", "arsiv", "gov"]):
            source_type = "primary"
        elif any(kw in domain for kw in ["scholar", "jstor", "academic", "university", "edu"]):
            source_type = "academic"
        elif any(kw in domain for kw in ["news", "press", "gazette", "times", "post"]):
            source_type = "press"
        elif any(kw in content for kw in ["memoir", "anı", "hatıra", "diary"]):
            source_type = "memoir"

        # Country heuristics
        country = self._guess_country(result)

        return {
            "source_type": source_type,
            "stance": "neutral",
            "country": country,
            "publisher": result.source_domain,
        }

    def _guess_country(self, result: ResearchResult) -> str:
        """Guess country from domain TLD or language."""
        domain = result.source_domain.lower()
        if domain.endswith(".tr"):
            return "TR"
        elif domain.endswith(".uk"):
            return "UK"
        elif domain.endswith(".fr"):
            return "FR"
        elif domain.endswith(".gr"):
            return "GR"
        elif domain.endswith(".de"):
            return "DE"
        elif domain.endswith(".ru"):
            return "RU"

        # Fallback by search language
        lang_map = {"tr": "TR", "en": "US", "fr": "FR", "el": "GR"}
        return lang_map.get(result.language, "INT")
