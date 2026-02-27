import asyncio
from datetime import datetime
from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.core.config import get_settings
from app import models
from app.services.proposition_parser import PropositionParser
from app.services.evidence_builder import EvidenceBuilder
from app.services.judge.orchestrator import JudgeOrchestrator
from app.services.consensus_engine import ConsensusEngine
from app.services.balance_protocol import BalanceProtocol
from app.services.report_generator import ReportGenerator

settings = get_settings()


@shared_task(bind=True, max_retries=3)
def process_case_workflow(self, case_id: str):
    """Main workflow for processing a historical analysis case."""
    # Run async workflow in sync context
    asyncio.run(_process_case_async(case_id))
    return {"case_id": case_id, "status": "completed"}


async def _process_case_async(case_id: str):
    """Async implementation of case processing workflow."""
    async with AsyncSessionLocal() as db:
        try:
            # Get case
            from sqlalchemy import select
            result = await db.execute(
                select(models.Case).where(models.Case.id == case_id)
            )
            case = result.scalar_one_or_none()
            
            if not case:
                raise ValueError(f"Case {case_id} not found")
            
            # Update status
            case.status = "processing"
            await db.commit()
            
            start_time = datetime.utcnow()
            
            # Step 1: Parse proposition
            parser = PropositionParser()
            parsed = await parser.parse(case.proposition)
            case.normalized_proposition = parsed.dict()
            case.time_window_start = parsed.time_window.start
            case.time_window_end = parsed.time_window.end
            case.geography = parsed.geography
            case.claim_type = parsed.claim_type
            
            # Step 2: Build evidence pack
            evidence_builder = EvidenceBuilder(db)
            evidence_items = await evidence_builder.build_evidence_pack(
                case_id=case_id,
                parsed_proposition=parsed
            )
            
            # Step 3: Check balance protocol
            balance_protocol = BalanceProtocol()
            mbr_status = balance_protocol.check_minimum_balance(case_id, db)
            case.mbr_compliant = mbr_status.compliant
            case.mbr_missing_clusters = mbr_status.missing_clusters if not mbr_status.compliant else None
            
            # Step 4: Run multi-model judges
            orchestrator = JudgeOrchestrator()
            model_outputs = await orchestrator.run_parallel_analysis(
                case_id=case_id,
                proposition=case.proposition,
                definitions=parsed.normalized_definitions,
                evidence_pack=[{"id": str(e.id), "text": e.title} for e in evidence_items]
            )
            
            # Step 5: Compute consensus
            consensus_engine = ConsensusEngine()
            consensus_result = await consensus_engine.compute_consensus(model_outputs)
            
            # Step 6: Apply MBR penalties if needed
            if not case.mbr_compliant:
                consensus_result.overall_confidence *= (1 - settings.MBR_PENALTY_PERCENTAGE / 100)
            
            # Store results
            case.consensus_output = consensus_result.dict()
            case.confidence_score = consensus_result.overall_confidence
            case.verdict_short = consensus_result.summary
            
            # Create claim records
            for claim_data in consensus_result.core_claims + consensus_result.medium_claims + consensus_result.disputed_claims:
                claim = models.Claim(
                    case_id=case_id,
                    claim_id_in_case=claim_data.id,
                    normalized_text=claim_data.normalized_text,
                    category=claim_data.category,
                    stance=claim_data.stance,
                    evidence_strength=claim_data.evidence_strength,
                    agreement_ratio=claim_data.agreement_ratio,
                    final_score=claim_data.final_score,
                    confidence_label=claim_data.confidence_label,
                    is_core_consensus=claim_data.is_core_consensus,
                    is_disputed=claim_data.is_disputed,
                    dispute_reasons=claim_data.dispute_reasons
                )
                db.add(claim)
            
            # Finalize
            case.status = "completed"
            case.completed_at = datetime.utcnow()
            case.processing_duration_ms = int(
                (datetime.utcnow() - start_time).total_seconds() * 1000
            )
            
            await db.commit()
            
        except Exception as exc:
            case.status = "failed"
            await db.commit()
            # Retry with exponential backoff
            raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task
def reset_monthly_analysis_counts():
    """Reset monthly analysis counts for all users (run on 1st of month)."""
    async def _reset():
        async with AsyncSessionLocal() as db:
            from sqlalchemy import update
            await db.execute(
                update(models.User).values(monthly_analysis_count=0)
            )
            await db.commit()
    
    asyncio.run(_reset())
    return {"status": "monthly counts reset"}
