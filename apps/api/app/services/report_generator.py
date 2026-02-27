import json
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import models


class ReportGenerator:
    """Generate exportable reports from case data."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _load_case(self, case_id: UUID) -> models.Case | None:
        result = await self.db.execute(
            select(models.Case)
            .where(models.Case.id == case_id)
            .options(
                selectinload(models.Case.evidence_items).selectinload(models.EvidenceItem.snippets),
                selectinload(models.Case.claims),
                selectinload(models.Case.model_outputs),
            )
        )
        return result.scalar_one_or_none()

    async def generate_markdown(self, case_id: UUID, citation_style: str = "chicago") -> str:
        """Generate a Markdown report from persisted case data."""
        case = await self._load_case(case_id)
        if not case:
            return "# Report\n\nCase not found."

        lines = [
            "# Historical Analysis Report",
            "",
            f"**Case ID:** {case.id}",
            f"**Citation Style:** {citation_style}",
            f"**Status:** {case.status}",
            f"**Confidence:** {case.confidence_score if case.confidence_score is not None else 'n/a'}",
            "",
            "## Proposition",
            "",
            case.proposition,
            "",
            "## Verdict",
            "",
            case.verdict_short or "No verdict generated.",
            "",
            "## Claims",
            "",
        ]

        if case.claims:
            for claim in sorted(case.claims, key=lambda c: (c.final_score or 0), reverse=True):
                lines.extend(
                    [
                        f"- **{claim.normalized_text}**",
                        f"  - stance: {claim.stance or 'unknown'}",
                        f"  - confidence: {claim.confidence_label or 'unknown'}",
                        f"  - score: {claim.final_score if claim.final_score is not None else 'n/a'}",
                    ]
                )
        else:
            lines.append("- No claims generated.")

        lines.extend(["", "## Evidence"])
        if case.evidence_items:
            for item in sorted(case.evidence_items, key=lambda e: (e.reliability_score or 0), reverse=True):
                lines.extend(
                    [
                        "",
                        f"### {item.title or 'Untitled Source'}",
                        f"- type: {item.source_type or 'unknown'}",
                        f"- country: {item.country or 'unknown'}",
                        f"- reliability: {item.reliability_score if item.reliability_score is not None else 'n/a'}",
                    ]
                )
                for snippet in item.snippets[:2]:
                    lines.append(f"  - snippet: {snippet.text[:200]}")
        else:
            lines.extend(["", "- No evidence available."])

        return "\n".join(lines) + "\n"

    async def generate_json(self, case_id: UUID) -> str:
        """Generate JSON export from persisted case data."""
        case = await self._load_case(case_id)
        if not case:
            return json.dumps({"error": "case_not_found", "case_id": str(case_id)}, indent=2)

        data = {
            "case": {
                "id": str(case.id),
                "proposition": case.proposition,
                "status": case.status,
                "confidence_score": case.confidence_score,
                "mbr_compliant": case.mbr_compliant,
                "mbr_missing_clusters": case.mbr_missing_clusters,
                "verdict_short": case.verdict_short,
                "consensus_output": case.consensus_output,
                "created_at": case.created_at,
                "completed_at": case.completed_at,
            },
            "claims": [
                {
                    "id": str(claim.id),
                    "claim_id_in_case": claim.claim_id_in_case,
                    "normalized_text": claim.normalized_text,
                    "category": claim.category,
                    "stance": claim.stance,
                    "evidence_strength": claim.evidence_strength,
                    "agreement_ratio": claim.agreement_ratio,
                    "final_score": claim.final_score,
                    "confidence_label": claim.confidence_label,
                    "is_core_consensus": claim.is_core_consensus,
                    "is_disputed": claim.is_disputed,
                    "dispute_reasons": claim.dispute_reasons,
                }
                for claim in case.claims
            ],
            "evidence": [
                {
                    "id": str(item.id),
                    "title": item.title,
                    "country": item.country,
                    "language": item.language,
                    "source_type": item.source_type,
                    "stance": item.stance,
                    "reliability_score": item.reliability_score,
                    "url": item.url,
                    "snippets": [
                        {
                            "id": str(snippet.id),
                            "text": snippet.text,
                            "page_location": snippet.page_location,
                            "quality_score": snippet.quality_score,
                        }
                        for snippet in item.snippets
                    ],
                }
                for item in case.evidence_items
            ],
            "model_outputs": [
                {
                    "id": str(output.id),
                    "model_name": output.model_name,
                    "status": output.status,
                    "latency_ms": output.latency_ms,
                    "error_message": output.error_message,
                    "output_json": output.output_json,
                }
                for output in case.model_outputs
            ],
        }
        return json.dumps(data, indent=2, default=str)
