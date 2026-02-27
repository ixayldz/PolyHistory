from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_active_user
from app.core.exceptions import NotFoundException
from app import schemas, models

router = APIRouter()


@router.get("", response_model=schemas.ConsensusAnalysisResponse)
async def get_consensus(
    case_id: UUID,
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get consensus analysis for a case."""
    # Verify case ownership
    case_result = await db.execute(
        select(models.Case).where(
            models.Case.id == case_id,
            models.Case.user_id == current_user.id
        )
    )
    case = case_result.scalar_one_or_none()
    if not case:
        raise NotFoundException("Case", str(case_id))
    
    # Get all claims for this case
    result = await db.execute(
        select(models.Claim).where(models.Claim.case_id == case_id)
    )
    claims = result.scalars().all()
    
    # Categorize claims
    core_claims = []
    medium_claims = []
    disputed_claims = []
    
    for claim in claims:
        claim_data = schemas.ClaimResponse(
            id=claim.id,
            claim_id_in_case=claim.claim_id_in_case,
            normalized_text=claim.normalized_text,
            category=claim.category,
            stance=claim.stance,
            evidence_strength=claim.evidence_strength,
            agreement_ratio=claim.agreement_ratio,
            final_score=claim.final_score,
            confidence_label=claim.confidence_label,
            is_core_consensus=claim.is_core_consensus,
            is_disputed=claim.is_disputed,
            dispute_reasons=claim.dispute_reasons,
            evidence_refs=[]  # Would be populated from claim_evidence table
        )
        
        if claim.is_disputed:
            disputed_claims.append(claim_data)
        elif claim.confidence_label == "high":
            core_claims.append(claim_data)
        elif claim.confidence_label == "medium":
            medium_claims.append(claim_data)
    
    # Get model outputs for agreement matrix
    models_result = await db.execute(
        select(models.ModelOutput.model_name).where(
            models.ModelOutput.case_id == case_id,
            models.ModelOutput.status == "success"
        )
    )
    model_names = [m for m in models_result.scalars().all()]
    
    # Build agreement matrix (simplified)
    agreement_matrix = schemas.AgreementMatrix(
        models=model_names,
        claims=[c.normalized_text[:50] for c in claims],
        agreement_scores=[[c.agreement_ratio or 0 for c in claims]]
    )
    
    # Calculate overall confidence
    overall_confidence = case.confidence_score or 0.0
    
    return schemas.ConsensusAnalysisResponse(
        core_claims=core_claims,
        medium_claims=medium_claims,
        disputed_claims=disputed_claims,
        agreement_matrix=agreement_matrix,
        overall_confidence=overall_confidence
    )
