from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.api.deps import get_db, get_current_active_user
from app.core.exceptions import NotFoundException
from app import schemas, models

router = APIRouter()


@router.get("", response_model=List[schemas.EvidenceItemResponse])
async def get_evidence(
    case_id: UUID,
    source_type: Optional[str] = Query(None, description="Filter by source type"),
    country: Optional[str] = Query(None, description="Filter by country"),
    stance: Optional[str] = Query(None, description="Filter by stance"),
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get evidence pack for a case with optional filtering."""
    # Verify case ownership
    case_result = await db.execute(
        select(models.Case).where(
            models.Case.id == case_id,
            models.Case.user_id == current_user.id
        )
    )
    if not case_result.scalar_one_or_none():
        raise NotFoundException("Case", str(case_id))
    
    # Build query
    query = (
        select(models.EvidenceItem)
        .where(models.EvidenceItem.case_id == case_id)
        .options(selectinload(models.EvidenceItem.snippets))
    )
    
    if source_type:
        query = query.where(models.EvidenceItem.source_type == source_type)
    if country:
        query = query.where(models.EvidenceItem.country == country)
    if stance:
        query = query.where(models.EvidenceItem.stance == stance)
    
    query = query.order_by(models.EvidenceItem.reliability_score.desc())
    
    result = await db.execute(query)
    evidence_items = result.scalars().all()
    
    response_items = []
    for item in evidence_items:
        response_items.append(schemas.EvidenceItemResponse(
            id=item.id,
            title=item.title,
            author=item.author,
            publisher=item.publisher,
            publication_date=item.publication_date,
            country=item.country,
            language=item.language,
            source_type=item.source_type,
            stance=item.stance,
            reliability_score=item.reliability_score,
            reliability_factors=item.reliability_factors,
            url=item.url,
            biblio_reference=item.biblio_reference,
            snippets=[schemas.SnippetResponse.model_validate(s) for s in item.snippets]
        ))
    
    return response_items


@router.get("/{evidence_id}", response_model=schemas.EvidenceItemResponse)
async def get_evidence_item(
    case_id: UUID,
    evidence_id: UUID,
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific evidence item with snippets."""
    # Verify case ownership
    case_result = await db.execute(
        select(models.Case).where(
            models.Case.id == case_id,
            models.Case.user_id == current_user.id
        )
    )
    if not case_result.scalar_one_or_none():
        raise NotFoundException("Case", str(case_id))
    
    # Get evidence item
    result = await db.execute(
        select(models.EvidenceItem)
        .where(
            models.EvidenceItem.id == evidence_id,
            models.EvidenceItem.case_id == case_id
        )
        .options(selectinload(models.EvidenceItem.snippets))
    )
    item = result.scalar_one_or_none()
    
    if not item:
        raise NotFoundException("Evidence", str(evidence_id))
    
    return schemas.EvidenceItemResponse(
        id=item.id,
        title=item.title,
        author=item.author,
        publisher=item.publisher,
        publication_date=item.publication_date,
        country=item.country,
        language=item.language,
        source_type=item.source_type,
        stance=item.stance,
        reliability_score=item.reliability_score,
        reliability_factors=item.reliability_factors,
        url=item.url,
        biblio_reference=item.biblio_reference,
        snippets=[schemas.SnippetResponse.model_validate(s) for s in item.snippets]
    )
