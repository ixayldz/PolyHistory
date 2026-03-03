"""
Deep Research Engine
Performs real web research using Tavily Search API for historical source discovery.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import date

import httpx

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


@dataclass
class ResearchResult:
    """A single research result from web search."""
    title: str
    url: str
    content: str  # Extracted text snippet
    score: float  # Relevance score from Tavily (0-1)
    published_date: Optional[str] = None
    source_domain: str = ""
    language: str = "en"
    search_query: str = ""
    raw_content: Optional[str] = None  # Full page content if available


@dataclass
class ResearchReport:
    """Aggregated research report from multiple queries."""
    results: List[ResearchResult] = field(default_factory=list)
    queries_executed: int = 0
    total_results: int = 0
    languages_searched: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class DeepResearchEngine:
    """
    Performs deep web research using Tavily Search API.
    
    Tavily is an AI-optimized search engine designed for agent workflows,
    providing structured results with citations and extracted content.
    Falls back gracefully if API key is not configured.
    """

    TAVILY_SEARCH_URL = "https://api.tavily.com/search"

    # Search topic categories for different evidence types
    SEARCH_CATEGORIES = {
        "academic": {
            "topic": "general",
            "include_domains": [
                "scholar.google.com", "jstor.org", "academia.edu",
                "researchgate.net", "arxiv.org", "dergipark.org.tr",
                "cambridge.org", "oxford.ac.uk", "persee.fr",
            ],
            "search_suffix": "academic research paper",
        },
        "archive": {
            "topic": "general",
            "include_domains": [
                "catalog.archives.gov", "nationalarchives.gov.uk",
                "devletarsivleri.gov.tr", "gallica.bnf.fr",
                "europeana.eu", "loc.gov", "archives.gov",
            ],
            "search_suffix": "official archive document primary source",
        },
        "press": {
            "topic": "news",
            "include_domains": [],  # Wide search for press
            "search_suffix": "newspaper historical report",
        },
        "treaty": {
            "topic": "general",
            "include_domains": [
                "treaties.un.org", "avalon.law.yale.edu",
                "treaties.fco.gov.uk", "mfa.gov.tr",
            ],
            "search_suffix": "treaty agreement diplomatic document",
        },
    }

    def __init__(self):
        self.api_key = settings.TAVILY_API_KEY
        self.max_queries = getattr(settings, "DEEP_RESEARCH_MAX_QUERIES", 12)
        self.max_results = getattr(settings, "DEEP_RESEARCH_MAX_RESULTS", 20)

    def is_available(self) -> bool:
        """Check if Tavily API is configured."""
        return bool(self.api_key)

    async def research(
        self,
        queries: List[Dict[str, str]],
        category: str = "general",
        time_window: Optional[tuple] = None,
    ) -> ResearchReport:
        """
        Execute multiple search queries and aggregate results.

        Args:
            queries: List of {"query": str, "language": str} dicts
            category: One of academic/archive/press/treaty/general
            time_window: Optional (start_date, end_date) tuple

        Returns:
            ResearchReport with deduplicated results
        """
        if not self.is_available():
            logger.info("Tavily API not configured. Skipping deep research.")
            return ResearchReport(errors=["Tavily API key not configured"])

        report = ResearchReport()
        seen_urls = set()

        # Limit queries
        limited_queries = queries[: self.max_queries]

        # Execute queries concurrently in batches of 4
        batch_size = 4
        for i in range(0, len(limited_queries), batch_size):
            batch = limited_queries[i : i + batch_size]
            tasks = [
                self._search_single(
                    query=q["query"],
                    language=q.get("language", "en"),
                    category=category,
                    time_window=time_window,
                )
                for q in batch
            ]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)

            for q, result in zip(batch, batch_results):
                report.queries_executed += 1
                if isinstance(result, Exception):
                    report.errors.append(f"Query '{q['query']}': {str(result)}")
                    continue

                for r in result:
                    if r.url not in seen_urls:
                        seen_urls.add(r.url)
                        report.results.append(r)
                        lang = q.get("language", "en")
                        if lang not in report.languages_searched:
                            report.languages_searched.append(lang)

        # Sort by relevance score and limit
        report.results.sort(key=lambda x: x.score, reverse=True)
        report.results = report.results[: self.max_results]
        report.total_results = len(report.results)

        return report

    async def research_by_category(
        self,
        queries: List[Dict[str, str]],
        time_window: Optional[tuple] = None,
    ) -> Dict[str, ResearchReport]:
        """
        Execute research across all categories (academic, archive, press, treaty).

        Args:
            queries: Base queries to augment per category
            time_window: Optional time window

        Returns:
            Dict mapping category name to ResearchReport
        """
        if not self.is_available():
            return {}

        results = {}
        for cat_name in self.SEARCH_CATEGORIES:
            # Augment queries with category-specific suffix
            cat_config = self.SEARCH_CATEGORIES[cat_name]
            suffix = cat_config["search_suffix"]
            augmented = [
                {
                    "query": f"{q['query']} {suffix}",
                    "language": q.get("language", "en"),
                }
                for q in queries[:3]  # Limit per category
            ]
            results[cat_name] = await self.research(
                augmented, category=cat_name, time_window=time_window
            )

        return results

    async def _search_single(
        self,
        query: str,
        language: str = "en",
        category: str = "general",
        time_window: Optional[tuple] = None,
    ) -> List[ResearchResult]:
        """Execute a single Tavily search query."""
        cat_config = self.SEARCH_CATEGORIES.get(
            category,
            {"topic": "general", "include_domains": [], "search_suffix": ""},
        )

        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": 5,
            "include_answer": False,
            "include_raw_content": False,
            "topic": cat_config.get("topic", "general"),
        }

        # Add domain filters if specified
        domains = cat_config.get("include_domains", [])
        if domains:
            payload["include_domains"] = domains

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.TAVILY_SEARCH_URL, json=payload)
            response.raise_for_status()
            data = response.json()

        results = []
        for item in data.get("results", []):
            result = ResearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                content=item.get("content", ""),
                score=item.get("score", 0.0),
                published_date=item.get("published_date"),
                source_domain=self._extract_domain(item.get("url", "")),
                language=language,
                search_query=query,
                raw_content=item.get("raw_content"),
            )
            results.append(result)

        return results

    @staticmethod
    def _extract_domain(url: str) -> str:
        """Extract domain from URL."""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc.replace("www.", "")
        except Exception:
            return ""
