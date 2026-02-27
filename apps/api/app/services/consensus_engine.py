"""
Consensus Engine
Computes weighted consensus from multiple model outputs.
"""

from typing import List, Dict, Any, Set, Tuple
from dataclasses import dataclass, field

from app.core.config import get_settings
from app.services.judge.base import JudgeOutput

settings = get_settings()


@dataclass
class ConsensusClaim:
    """A claim in the consensus."""
    id: str
    normalized_text: str
    category: str
    stance: str
    evidence_refs: List[Dict[str, Any]] = field(default_factory=list)
    evidence_strength: float = 0.0
    agreement_ratio: float = 0.0
    final_score: float = 0.0
    confidence_label: str = "low"
    is_core_consensus: bool = False
    is_disputed: bool = False
    dispute_reasons: List[str] = field(default_factory=list)
    supporting_models: List[str] = field(default_factory=list)


@dataclass
class ConsensusResult:
    """Result of consensus computation."""
    core_claims: List[ConsensusClaim] = field(default_factory=list)
    medium_claims: List[ConsensusClaim] = field(default_factory=list)
    disputed_claims: List[ConsensusClaim] = field(default_factory=list)
    overall_confidence: float = 0.0
    summary: str = ""
    agreement_matrix: Dict[str, Any] = field(default_factory=dict)
    
    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "core_claims": [self._claim_to_dict(c) for c in self.core_claims],
            "medium_claims": [self._claim_to_dict(c) for c in self.medium_claims],
            "disputed_claims": [self._claim_to_dict(c) for c in self.disputed_claims],
            "overall_confidence": self.overall_confidence,
            "summary": self.summary,
            "agreement_matrix": self.agreement_matrix
        }
    
    def _claim_to_dict(self, claim: ConsensusClaim) -> Dict[str, Any]:
        return {
            "id": claim.id,
            "normalized_text": claim.normalized_text,
            "category": claim.category,
            "stance": claim.stance,
            "evidence_refs": claim.evidence_refs,
            "evidence_strength": claim.evidence_strength,
            "agreement_ratio": claim.agreement_ratio,
            "final_score": claim.final_score,
            "confidence_label": claim.confidence_label,
            "is_core_consensus": claim.is_core_consensus,
            "is_disputed": claim.is_disputed,
            "dispute_reasons": claim.dispute_reasons,
            "supporting_models": claim.supporting_models
        }


class ConsensusEngine:
    """
    Compute weighted consensus from multiple model judge outputs.
    
    Algorithm:
    1. Extract all claims from all models
    2. Group semantically similar claims (similarity >= threshold)
    3. Compute evidence strength for each group
    4. Compute agreement ratio across models
    5. Calculate final score = agreement_ratio * evidence_strength
    6. Categorize as core/medium/disputed based on scores
    """
    
    # Evidence type weights
    EVIDENCE_WEIGHTS = {
        "primary": 1.0,
        "academic": 0.8,
        "secondary": 0.7,
        "memoir": 0.5,
        "press": 0.4,
    }
    
    def __init__(self):
        """Initialize consensus engine."""
        self.similarity_threshold = settings.CONSENSUS_SIMILARITY_THRESHOLD
    
    async def compute_consensus(
        self,
        model_outputs: Dict[str, JudgeOutput]
    ) -> ConsensusResult:
        """
        Compute consensus from multiple model outputs.
        
        Args:
            model_outputs: Dict mapping model names to JudgeOutput
            
        Returns:
            ConsensusResult with categorized claims
        """
        # Step 1: Extract all claims from all models
        all_claims = []
        for model_name, output in model_outputs.items():
            if output and output.claims:
                for claim in output.claims:
                    all_claims.append({
                        "model": model_name,
                        "claim": claim
                    })
        
        # Step 2: Group semantically similar claims
        claim_groups = self._group_similar_claims(all_claims)
        
        # Step 3: Compute consensus for each group
        consensus_claims = []
        for group in claim_groups:
            consensus_claim = self._compute_group_consensus(group, list(model_outputs.keys()))
            consensus_claims.append(consensus_claim)
        
        # Step 4: Categorize by confidence
        core_claims = []
        medium_claims = []
        disputed_claims = []
        
        for claim in consensus_claims:
            if claim.is_disputed:
                disputed_claims.append(claim)
            elif claim.confidence_label == "high":
                core_claims.append(claim)
            elif claim.confidence_label == "medium":
                medium_claims.append(claim)
        
        # Step 5: Build agreement matrix
        agreement_matrix = self._build_agreement_matrix(model_outputs, claim_groups)
        
        # Step 6: Compute overall confidence
        overall_confidence = self._compute_overall_confidence(consensus_claims)
        
        # Step 7: Generate summary
        summary = self._generate_summary(core_claims, disputed_claims, overall_confidence)
        
        return ConsensusResult(
            core_claims=core_claims,
            medium_claims=medium_claims,
            disputed_claims=disputed_claims,
            overall_confidence=overall_confidence,
            summary=summary,
            agreement_matrix=agreement_matrix
        )
    
    def _group_similar_claims(
        self,
        all_claims: List[Dict[str, Any]]
    ) -> List[List[Dict[str, Any]]]:
        """Group claims by semantic similarity using simple text matching."""
        if not all_claims:
            return []
        
        groups = []
        used = set()
        
        for i, claim_data in enumerate(all_claims):
            if i in used:
                continue
            
            # Start new group
            group = [claim_data]
            used.add(i)
            
            claim_text = claim_data["claim"].get("normalized_text", "").lower()
            
            # Find similar claims
            for j, other_data in enumerate(all_claims[i+1:], start=i+1):
                if j in used:
                    continue
                
                other_text = other_data["claim"].get("normalized_text", "").lower()
                
                # Simple similarity: Jaccard similarity of word sets
                similarity = self._text_similarity(claim_text, other_text)
                
                if similarity >= self.similarity_threshold:
                    group.append(other_data)
                    used.add(j)
            
            groups.append(group)
        
        return groups
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate Jaccard similarity between two texts."""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _compute_group_consensus(
        self,
        group: List[Dict[str, Any]],
        all_model_names: List[str]
    ) -> ConsensusClaim:
        """Compute consensus for a group of similar claims."""
        # Get base claim (first in group)
        base_claim = group[0]["claim"]
        
        # Aggregate evidence refs
        all_evidence_refs = []
        for item in group:
            refs = item["claim"].get("evidence_refs", [])
            all_evidence_refs.extend(refs)
        
        # Compute evidence strength
        evidence_strength = self._compute_evidence_strength(all_evidence_refs)
        
        # Get supporting models
        supporting_models = list(set(item["model"] for item in group))
        
        # Compute agreement ratio
        agreement_ratio = len(supporting_models) / len(all_model_names) if all_model_names else 0
        
        # Calculate final score
        final_score = agreement_ratio * evidence_strength
        
        # Determine confidence label
        if final_score >= 0.61:
            confidence_label = "high"
        elif final_score >= 0.31:
            confidence_label = "medium"
        else:
            confidence_label = "low"
        
        # Check if disputed (different stances)
        stances = set(item["claim"].get("stance", "neutral") for item in group)
        is_disputed = len(stances) > 1
        
        # Generate dispute reasons if disputed
        dispute_reasons = []
        if is_disputed:
            dispute_reasons.append(f"Different stances: {', '.join(stances)}")
        
        return ConsensusClaim(
            id=base_claim.get("claim_id", "unknown"),
            normalized_text=base_claim.get("normalized_text", ""),
            category=base_claim.get("category", "unknown"),
            stance=self._majority_stance(group),
            evidence_refs=all_evidence_refs,
            evidence_strength=evidence_strength,
            agreement_ratio=agreement_ratio,
            final_score=final_score,
            confidence_label=confidence_label,
            is_core_consensus=(confidence_label == "high" and not is_disputed),
            is_disputed=is_disputed,
            dispute_reasons=dispute_reasons,
            supporting_models=supporting_models
        )
    
    def _compute_evidence_strength(
        self,
        evidence_refs: List[Dict[str, Any]]
    ) -> float:
        """Compute weighted evidence strength."""
        if not evidence_refs:
            return 0.0
        
        total_weight = 0.0
        for ref in evidence_refs:
            source_type = ref.get("source_type", "press")
            reliability = ref.get("reliability", 0.5)
            weight = self.EVIDENCE_WEIGHTS.get(source_type, 0.4) * reliability
            total_weight += weight
        
        # Normalize against average support in this claim cluster.
        return min(total_weight / len(evidence_refs), 1.0)
    
    def _majority_stance(self, group: List[Dict[str, Any]]) -> str:
        """Determine majority stance in claim group."""
        stance_counts = {}
        for item in group:
            stance = item["claim"].get("stance", "neutral")
            stance_counts[stance] = stance_counts.get(stance, 0) + 1
        
        if not stance_counts:
            return "neutral"
        
        return max(stance_counts, key=stance_counts.get)
    
    def _build_agreement_matrix(
        self,
        model_outputs: Dict[str, JudgeOutput],
        claim_groups: List[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Build agreement matrix between models."""
        model_names = list(model_outputs.keys())
        
        # Initialize matrix
        matrix = {
            "models": model_names,
            "claims": [f"Claim {i+1}" for i in range(len(claim_groups))],
            "agreement_scores": []
        }
        
        for group in claim_groups:
            row = []
            supporting = set(item["model"] for item in group)
            
            for model in model_names:
                if model in supporting:
                    row.append(1.0)
                else:
                    row.append(0.0)
            
            matrix["agreement_scores"].append(row)
        
        return matrix
    
    def _compute_overall_confidence(
        self,
        consensus_claims: List[ConsensusClaim]
    ) -> float:
        """Compute overall confidence score."""
        if not consensus_claims:
            return 0.0
        
        # Weight by evidence strength
        total_weight = sum(c.evidence_strength for c in consensus_claims)
        weighted_scores = sum(c.final_score * c.evidence_strength for c in consensus_claims)
        
        if total_weight == 0:
            return 0.0
        
        return weighted_scores / total_weight
    
    def _generate_summary(
        self,
        core_claims: List[ConsensusClaim],
        disputed_claims: List[ConsensusClaim],
        overall_confidence: float
    ) -> str:
        """Generate summary statement."""
        parts = []
        
        if core_claims:
            parts.append(f"Found {len(core_claims)} core consensus claims")
        
        if disputed_claims:
            parts.append(f"{len(disputed_claims)} disputed claims requiring further review")
        
        confidence_pct = int(overall_confidence * 100)
        parts.append(f"Overall confidence: {confidence_pct}%")
        
        return ". ".join(parts) + "."
