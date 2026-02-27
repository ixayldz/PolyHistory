from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from app.api.deps import get_db, get_current_active_user, check_analysis_limit
from app.core.exceptions import NotFoundException
from app import schemas, models
from app.tasks.case_workflow import enqueue_case_workflow

router = APIRouter()


@router.post("", response_model=schemas.CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(
    case_in: schemas.CaseCreate,
    current_user: models.User = Depends(check_analysis_limit),
    db: AsyncSession = Depends(get_db)
):
    """Create a new analysis case."""
    # Create case record
    case = models.Case(
        user_id=current_user.id,
        proposition=case_in.proposition,
        time_window_start=case_in.time_window.start if case_in.time_window else None,
        time_window_end=case_in.time_window.end if case_in.time_window else None,
        geography=case_in.geography,
        status="pending"
    )
    db.add(case)
    
    # Increment user's analysis count
    current_user.monthly_analysis_count += 1
    
    await db.commit()
    await db.refresh(case)
    
    # Trigger background processing
    enqueue_case_workflow(str(case.id), case_in.model_dump(mode="json"))
    
    return case


@router.get("", response_model=schemas.CaseListResponse)
async def list_cases(
    status: Optional[str] = Query(None, description="Filter by case status"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """List user's cases with pagination."""
    query = select(models.Case).where(models.Case.user_id == current_user.id)
    
    if status:
        query = query.where(models.Case.status == status)
    
    # Get total count
    count_result = await db.execute(
        select(func.count()).select_from(query.subquery())
    )
    total = count_result.scalar()
    
    # Get paginated results
    query = query.order_by(desc(models.Case.created_at)).offset(offset).limit(limit)
    result = await db.execute(query)
    cases = result.scalars().all()
    
    return schemas.CaseListResponse(
        items=[schemas.CaseResponse.model_validate(c) for c in cases],
        total=total
    )


@router.get("/{case_id}", response_model=schemas.CaseDetailResponse)
async def get_case(
    case_id: UUID,
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get case details by ID."""
    result = await db.execute(
        select(models.Case).where(
            models.Case.id == case_id,
            models.Case.user_id == current_user.id
        )
    )
    case = result.scalar_one_or_none()
    
    if not case:
        raise NotFoundException("Case", str(case_id))
    
    # Build response
    response = schemas.CaseDetailResponse(
        id=case.id,
        proposition=case.proposition,
        status=case.status,
        confidence_score=case.confidence_score,
        created_at=case.created_at,
        normalized_proposition=case.normalized_proposition,
        time_window=schemas.TimeWindow(
            start=case.time_window_start,
            end=case.time_window_end
        ) if case.time_window_start or case.time_window_end else None,
        mbr_compliant=case.mbr_compliant,
        mbr_missing_clusters=case.mbr_missing_clusters,
        verdict={"short_statement": case.verdict_short} if case.verdict_short else None,
        consensus=case.consensus_output
    )
    
    return response


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_case(
    case_id: UUID,
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a case."""
    result = await db.execute(
        select(models.Case).where(
            models.Case.id == case_id,
            models.Case.user_id == current_user.id
        )
    )
    case = result.scalar_one_or_none()
    
    if not case:
        raise NotFoundException("Case", str(case_id))
    
    await db.delete(case)
    await db.commit()
    
    return None
