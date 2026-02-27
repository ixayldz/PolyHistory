from uuid import UUID
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_active_user
from app.core.exceptions import NotFoundException
from app import schemas, models
from app.services.report_generator import ReportGenerator

router = APIRouter()


@router.post("/{case_id}/export")
async def export_case(
    case_id: UUID,
    export_request: schemas.ExportRequest,
    current_user: models.User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Export case report in specified format."""
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
    
    # Generate report
    generator = ReportGenerator(db)
    
    if export_request.format == "markdown":
        content = await generator.generate_markdown(case_id, export_request.citation_style)
        media_type = "text/markdown"
        filename = f"case_{case_id}.md"
    elif export_request.format == "json":
        content = await generator.generate_json(case_id)
        media_type = "application/json"
        filename = f"case_{case_id}.json"
    else:
        # PDF would require additional library like reportlab or weasyprint
        content = "PDF export not yet implemented"
        media_type = "text/plain"
        filename = f"case_{case_id}.txt"
    
    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
