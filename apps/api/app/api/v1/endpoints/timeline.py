from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_active_user
from app.core.exceptions import NotFoundException
from app import schemas, models

router = APIRouter()


@router.get("", response_model=List[schemas.TimelineEvent])
async def get_timeline(
    case_id: UUID,
    granularity: str = Query("month", description="Timeline granularity: day, week, month, year"),
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get timeline data for a case."""
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
    
    # Get evidence with dates
    result = await db.execute(
        select(models.EvidenceItem).where(
            models.EvidenceItem.case_id == case_id,
            models.EvidenceItem.publication_date.isnot(None)
        ).order_by(models.EvidenceItem.publication_date)
    )
    evidence_items = result.scalars().all()
    
    # Build timeline events
    events = []
    for item in evidence_items:
        track = f"{item.country}_{item.stance}" if item.stance else item.country or "unknown"
        
        events.append(schemas.TimelineEvent(
            id=str(item.id),
            date=item.publication_date,
            track=track,
            title=item.title or "Untitled",
            description=f"{item.source_type} source from {item.country}",
            source_id=item.id,
            evidence_type=item.source_type or "unknown"
        ))
    
    return events
