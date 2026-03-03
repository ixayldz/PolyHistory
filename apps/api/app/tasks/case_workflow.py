"""
Case workflow task orchestration.

Provides:
- A Celery task entrypoint for worker execution.
- A local fallback path for environments without Redis/Celery workers.
"""

import asyncio
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import delete, select

from app import models
from app.core.database import AsyncSessionLocal
from app.services.balance_protocol import BalanceProtocol
from app.services.consensus_engine import ConsensusEngine, ConsensusClaim
from app.services.evidence_builder import EvidenceBuilder
from app.services.judge.base import JudgeOutput
from app.services.judge.orchestrator import JudgeOrchestrator, DegradationLevel
from app.services.proposition_parser import PropositionParser
from app.tasks import celery_app


def _pick_evidence_refs(evidence_pack: List[Dict[str, Any]], limit: int = 2) -> List[Dict[str, Any]]:
    refs: List[Dict[str, Any]] = []
    for item in evidence_pack[:limit]:
        snippet_id = None
        if item.get("snippets"):
            snippet_id = item["snippets"][0].get("id")
        refs.append(
            {
                "evidence_id": item.get("id", "unknown"),
                "snippet_id": snippet_id or "unknown",
                "source_type": item.get("source_type", "press"),
                "reliability": item.get("reliability_score") or 0.5,
            }
        )
    return refs


def _build_fallback_judge_outputs(
    proposition: str,
    claim_type: Optional[str],
    evidence_pack: List[Dict[str, Any]],
) -> Dict[str, JudgeOutput]:
    """Deterministic local fallback when external model APIs are unavailable."""
    refs = _pick_evidence_refs(evidence_pack, limit=2)
    category = claim_type or "diplomatic"
    normalized = proposition.strip().rstrip("?")
    confidence = 0.72 if any(e.get("source_type") == "primary" for e in evidence_pack) else 0.55

    output_a = JudgeOutput(
        definitions_review=["Fallback mode: deterministic local analysis was used."],
        claims=[
            {
                "claim_id": "fallback-1",
                "normalized_text": normalized or "Insufficient proposition detail.",
                "category": category,
                "stance": "support",
                "evidence_refs": refs,
                "evidence_strength_score": confidence,
            }
        ],
        strongest_evidence=[{"evidence_id": ref["evidence_id"], "reasoning": "High reliability local source."} for ref in refs[:1]],
        strongest_counter_evidence=[{"evidence_id": ref["evidence_id"], "reasoning": "Alternative interpretation present."} for ref in refs[1:2]],
        uncertainties=["Fallback mode does not use external LLM APIs."],
        bias_risk_notes=["Local fallback output may under-represent nuanced disagreement."],
        verdict={
            "short_statement": "Fallback consensus indicates partial support under limited model availability.",
            "confidence_score": int(confidence * 100),
        },
    )

    output_b = JudgeOutput(
        definitions_review=["Fallback mode: deterministic local analysis was used."],
        claims=[
            {
                "claim_id": "fallback-1",
                "normalized_text": normalized or "Insufficient proposition detail.",
                "category": category,
                "stance": "support",
                "evidence_refs": refs,
                "evidence_strength_score": confidence - 0.05,
            }
        ],
        strongest_evidence=[{"evidence_id": ref["evidence_id"], "reasoning": "Consistent across local source set."} for ref in refs[:1]],
        strongest_counter_evidence=[{"evidence_id": ref["evidence_id"], "reasoning": "Counter-evidence remains inconclusive."} for ref in refs[1:2]],
        uncertainties=["Fallback mode used due to missing model credentials or dependencies."],
        bias_risk_notes=["Agreement is generated from deterministic fallback logic."],
        verdict={
            "short_statement": "Fallback secondary judge aligns with the primary fallback interpretation.",
            "confidence_score": int((confidence - 0.05) * 100),
        },
    )

    return {
        "fallback_judge_a": output_a,
        "fallback_judge_b": output_b,
    }


def _serialize_evidence_for_judges(evidence_items: List[models.EvidenceItem]) -> List[Dict[str, Any]]:
    evidence_pack: List[Dict[str, Any]] = []
    for item in evidence_items:
        snippets = []
        for snippet in item.snippets:
            snippets.append(
                {
                    "id": str(snippet.id),
                    "text": snippet.text,
                    "quality_score": snippet.quality_score,
                    "page_location": snippet.page_location,
                }
            )
        evidence_pack.append(
            {
                "id": str(item.id),
                "title": item.title,
                "source_type": item.source_type,
                "country": item.country,
                "language": item.language,
                "stance": item.stance,
                "reliability_score": item.reliability_score,
                "text": snippets[0]["text"] if snippets else (item.title or ""),
                "snippets": snippets,
            }
        )
    return evidence_pack


async def _persist_consensus_claims(
    case_id: UUID,
    claims: List[ConsensusClaim],
) -> List[models.Claim]:
    persisted: List[models.Claim] = []
    async with AsyncSessionLocal() as db:
        await db.execute(delete(models.Claim).where(models.Claim.case_id == case_id))
        for claim in claims:
            persisted.append(
                models.Claim(
                    case_id=case_id,
                    claim_id_in_case=claim.id,
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
                )
            )
        db.add_all(persisted)
        await db.commit()
    return persisted


async def run_case_workflow(
    case_id: str,
    case_payload: Optional[Dict[str, Any]] = None,
    analysis_mode: str = "multi_model",
) -> Dict[str, Any]:
    """
    Execute full case workflow in async mode.

    This function is used by both Celery workers and local fallback execution.
    """
    started_at = time.perf_counter()
    case_uuid = UUID(case_id)

    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(models.Case).where(models.Case.id == case_uuid))
            case = result.scalar_one_or_none()
            if not case:
                return {"case_id": case_id, "status": "missing"}

            case.status = "processing"
            await db.commit()

            parser = PropositionParser()
            parsed = await parser.parse(case.proposition)

            case.normalized_proposition = parsed.model_dump(mode="json")
            case.claim_type = parsed.claim_type
            if not case.time_window_start:
                case.time_window_start = parsed.time_window.start
            if not case.time_window_end:
                case.time_window_end = parsed.time_window.end
            if not case.geography:
                case.geography = parsed.geography
            await db.commit()

            builder = EvidenceBuilder(db)
            evidence_items = await builder.build_evidence_pack(case_id, parsed)

            balance = BalanceProtocol()
            mbr_status = balance.check_minimum_balance(case_id, evidence_items)
            case.mbr_compliant = mbr_status.compliant
            case.mbr_missing_clusters = mbr_status.missing_clusters or None
            await db.commit()

            evidence_pack = _serialize_evidence_for_judges(evidence_items)
            definitions = parsed.normalized_definitions

            orchestrator = JudgeOrchestrator()
            single_model = analysis_mode == "single_model"
            if orchestrator.is_ready():
                analysis_result = await orchestrator.run_parallel_analysis(
                    case_id=case_id,
                    proposition=case.proposition,
                    definitions=definitions,
                    evidence_pack=evidence_pack,
                    single_model_mode=single_model,
                )
                model_outputs = analysis_result.outputs
                degradation_level = analysis_result.degradation_level
                confidence_cap = analysis_result.confidence_cap
                degradation_warnings = analysis_result.warnings

                # If FALLBACK degradation, use local deterministic
                if degradation_level == DegradationLevel.FALLBACK:
                    model_outputs = _build_fallback_judge_outputs(
                        proposition=case.proposition,
                        claim_type=parsed.claim_type,
                        evidence_pack=evidence_pack,
                    )
            else:
                model_outputs = _build_fallback_judge_outputs(
                    proposition=case.proposition,
                    claim_type=parsed.claim_type,
                    evidence_pack=evidence_pack,
                )
                degradation_level = DegradationLevel.FALLBACK
                confidence_cap = 0.40
                degradation_warnings = ["No model judges configured. Using local fallback."]

            await db.execute(delete(models.ModelOutput).where(models.ModelOutput.case_id == case_uuid))
            for model_name, output in model_outputs.items():
                status = "success" if output else "error"
                db.add(
                    models.ModelOutput(
                        case_id=case_uuid,
                        model_name=model_name,
                        output_json=output.to_dict() if output else {"error": "model output missing"},
                        status=status,
                    )
                )
            await db.commit()

            consensus_engine = ConsensusEngine()
            consensus_result = await consensus_engine.compute_consensus(model_outputs)
            all_consensus_claims = (
                consensus_result.core_claims +
                consensus_result.medium_claims +
                consensus_result.disputed_claims
            )

            await _persist_consensus_claims(case_uuid, all_consensus_claims)

            overall_confidence = consensus_result.overall_confidence

            # Apply degradation confidence cap (PRD v2.0)
            overall_confidence = min(overall_confidence, confidence_cap)

            if not mbr_status.compliant:
                overall_confidence = balance.apply_penalty(overall_confidence)

            has_primary = any(item.source_type == "primary" for item in evidence_items)
            risk_status = balance.check_high_risk_claim(case.proposition, has_primary)
            if risk_status["confidence_cap"] is not None:
                overall_confidence = min(overall_confidence, risk_status["confidence_cap"])

            case.confidence_score = max(0.0, min(1.0, round(overall_confidence, 4)))

            # Store consensus output with degradation metadata
            consensus_dict = consensus_result.dict()
            consensus_dict["degradation_level"] = degradation_level.value
            consensus_dict["analysis_mode"] = analysis_mode
            consensus_dict["degradation_warnings"] = degradation_warnings
            case.consensus_output = consensus_dict

            verdict = consensus_result.summary
            if risk_status["warning"]:
                verdict = f"{verdict} {risk_status['warning']}"
            if degradation_warnings:
                verdict = f"{verdict} [{'; '.join(degradation_warnings)}]"
            case.verdict_short = verdict

            case.status = "completed"
            case.completed_at = datetime.utcnow()
            case.processing_duration_ms = int((time.perf_counter() - started_at) * 1000)

            db.add(
                models.AuditLog(
                    case_id=case_uuid,
                    user_id=case.user_id,
                    action="case.workflow_completed",
                    details={
                        "mbr_compliant": case.mbr_compliant,
                        "models_used": list(model_outputs.keys()),
                        "claim_count": len(all_consensus_claims),
                        "degradation_level": degradation_level.value,
                        "analysis_mode": analysis_mode,
                    },
                )
            )
            await db.commit()

        return {"case_id": case_id, "status": "completed"}

    except Exception as exc:
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(models.Case).where(models.Case.id == case_uuid))
            case = result.scalar_one_or_none()
            if case:
                case.status = "failed"
                case.completed_at = datetime.utcnow()
                case.processing_duration_ms = int((time.perf_counter() - started_at) * 1000)
                db.add(
                    models.AuditLog(
                        case_id=case_uuid,
                        user_id=case.user_id,
                        action="case.workflow_failed",
                        details={"error": str(exc)},
                    )
                )
                await db.commit()
        return {"case_id": case_id, "status": "failed", "error": str(exc)}


@celery_app.task(name="app.tasks.case_workflow.process_case_workflow")
def process_case_workflow_task(
    case_id: str,
    case_payload: Optional[Dict[str, Any]] = None,
    analysis_mode: str = "multi_model",
) -> Dict[str, Any]:
    """Celery task entrypoint."""
    return asyncio.run(run_case_workflow(case_id, case_payload, analysis_mode))


def enqueue_case_workflow(
    case_id: str,
    case_payload: Optional[Dict[str, Any]] = None,
    analysis_mode: str = "multi_model",
) -> str:
    """
    Enqueue workflow via Celery, with safe local async fallback.
    """
    try:
        process_case_workflow_task.delay(case_id, case_payload, analysis_mode)
        return "celery"
    except Exception:
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(run_case_workflow(case_id, case_payload, analysis_mode))
        except RuntimeError:
            asyncio.run(run_case_workflow(case_id, case_payload, analysis_mode))
        return "local"
