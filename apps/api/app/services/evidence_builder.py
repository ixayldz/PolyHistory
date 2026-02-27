"""
Evidence Builder Service
Builds evidence packs from retrieved sources.
"""

import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sentence_transformers import SentenceTransformer

from app import models
from app.core.config import get_settings
from app.schemas import PropositionParsed

settings = get_settings()


class EvidenceBuilder:
    """Build and score evidence packs for historical analysis."""
    
    # Source type weights for reliability scoring
    SOURCE_TYPE_WEIGHTS = {
        "primary": 1.0,
        "academic": 0.8,
        "secondary": 0.7,
        "memoir": 0.5,
        "press": 0.4,
    }
    
    # Institution reputation scores (simplified)
    INSTITUTION_REPUTATION = {
        "archives": 0.95,
        "university_press": 0.9,
        "peer_reviewed_journal": 0.9,
        "national_library": 0.85,
        "established_newspaper": 0.6,
        "unknown": 0.5,
    }
    
    def __init__(self, db: AsyncSession):
        self.db = db
        # Load embedding model for semantic similarity
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    async def build_evidence_pack(
        self,
        case_id: str,
        parsed_proposition: PropositionParsed
    ) -> List[models.EvidenceItem]:
        """
        Build a complete evidence pack for a case.
        
        Args:
            case_id: UUID of the case
            parsed_proposition: Parsed proposition data
            
        Returns:
            List of EvidenceItem objects
        """
        evidence_items = []
        
        # Collect from multiple sources in parallel
        retrieval_tasks = [
            self._collect_academic_sources(parsed_proposition),
            self._collect_archive_sources(parsed_proposition),
            self._collect_press_sources(parsed_proposition),
            self._collect_treaty_sources(parsed_proposition),
        ]
        
        results = await asyncio.gather(*retrieval_tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                evidence_items.extend(result)
        
        # Score and filter evidence
        scored_evidence = await self._score_evidence(evidence_items, parsed_proposition)
        
        # Sort by reliability score
        scored_evidence.sort(key=lambda x: x.reliability_score or 0, reverse=True)
        
        # Limit to maximum evidence per case
        limited_evidence = scored_evidence[:settings.MAX_EVIDENCE_PER_CASE]
        
        # Save to database
        for item in limited_evidence:
            item.case_id = case_id
            self.db.add(item)
            # Add snippets
            for snippet in item.snippets:
                snippet.evidence_id = item.id
                self.db.add(snippet)
        
        await self.db.commit()
        
        return limited_evidence
    
    async def _collect_academic_sources(
        self,
        parsed_proposition: PropositionParsed
    ) -> List[models.EvidenceItem]:
        """Collect sources from academic databases."""
        # Placeholder: Would integrate with Semantic Scholar, JSTOR, etc.
        # For MVP, return empty list or mock data
        return []
    
    async def _collect_archive_sources(
        self,
        parsed_proposition: PropositionParsed
    ) -> List[models.EvidenceItem]:
        """Collect sources from archives."""
        # Placeholder: Would integrate with archive APIs
        return []
    
    async def _collect_press_sources(
        self,
        parsed_proposition: PropositionParsed
    ) -> List[models.EvidenceItem]:
        """Collect sources from period press."""
        # Placeholder: Would integrate with newspaper archives
        return []
    
    async def _collect_treaty_sources(
        self,
        parsed_proposition: PropositionParsed
    ) -> List[models.EvidenceItem]:
        """Collect official texts and treaties."""
        # Placeholder: Would integrate with treaty databases
        return []
    
    async def _score_evidence(
        self,
        evidence_items: List[models.EvidenceItem],
        parsed_proposition: PropositionParsed
    ) -> List[models.EvidenceItem]:
        """Score evidence items based on multiple factors."""
        for item in evidence_items:
            # Calculate component scores
            type_weight = self.SOURCE_TYPE_WEIGHTS.get(item.source_type, 0.4)
            institution_score = self.INSTITUTION_REPUTATION.get(
                self._get_institution_type(item), 
                0.5
            )
            
            # Cross-source consistency (placeholder)
            consistency_score = await self._check_consistency(item, evidence_items)
            
            # Citation density (placeholder - would analyze text)
            citation_score = 0.5
            
            # Calculate final reliability score
            reliability = (
                type_weight * 0.4 +
                institution_score * 0.25 +
                consistency_score * 0.20 +
                citation_score * 0.15
            )
            
            item.reliability_score = min(reliability, 1.0)
            item.reliability_factors = {
                "type_weight": type_weight,
                "institution_score": institution_score,
                "consistency_score": consistency_score,
                "citation_score": citation_score,
            }
        
        return evidence_items
    
    def _get_institution_type(self, item: models.EvidenceItem) -> str:
        """Determine institution type from evidence metadata."""
        # Simplified logic - would be more sophisticated in production
        publisher = (item.publisher or "").lower()
        
        if "archive" in publisher or "devlet arşiv" in publisher:
            return "archives"
        elif "university" in publisher or "üniversite" in publisher:
            return "university_press"
        elif "journal" in publisher:
            return "peer_reviewed_journal"
        elif "library" in publisher:
            return "national_library"
        elif "gazete" in publisher or "newspaper" in publisher:
            return "established_newspaper"
        
        return "unknown"
    
    async def _check_consistency(
        self,
        item: models.EvidenceItem,
        all_items: List[models.EvidenceItem]
    ) -> float:
        """Check consistency with other sources."""
        # Placeholder: Would implement semantic similarity check
        # between different sources' claims
        return 0.7
    
    def create_snippet(
        self,
        text: str,
        page_location: Optional[str] = None,
        quality_score: Optional[float] = None
    ) -> models.Snippet:
        """Create a snippet with embedding."""
        # Generate embedding
        embedding = self.embedding_model.encode(text).tolist()
        
        return models.Snippet(
            text=text[:settings.SNIPPET_MAX_LENGTH],
            page_location=page_location,
            quality_score=quality_score or 0.5,
            embedding=embedding
        )
