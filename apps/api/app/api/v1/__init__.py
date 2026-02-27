from fastapi import APIRouter
from app.api.v1.endpoints import auth, cases, evidence, timeline, consensus, export

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["authentication"])
router.include_router(cases.router, prefix="/cases", tags=["cases"])
router.include_router(evidence.router, prefix="/cases/{case_id}/evidence", tags=["evidence"])
router.include_router(timeline.router, prefix="/cases/{case_id}/timeline", tags=["timeline"])
router.include_router(consensus.router, prefix="/cases/{case_id}/consensus", tags=["consensus"])
router.include_router(export.router, prefix="/cases", tags=["export"])
