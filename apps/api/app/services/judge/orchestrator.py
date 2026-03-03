"""
Judge Orchestrator
Manages parallel execution of multiple model judges with graceful degradation.
"""

import asyncio
from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

from app.core.config import get_settings
from app.core.exceptions import InsufficientConsensusException
from app.services.judge.base import BaseJudge, JudgeOutput, JudgeTimeoutError, JudgeParseError

settings = get_settings()


class DegradationLevel(str, Enum):
    """PRD v2.0: 4-tier graceful degradation."""
    FULL = "full"              # 3/3 models succeeded
    PARTIAL = "partial"        # 2/3 models succeeded
    REDUCED = "reduced"        # 1/3 models succeeded
    FALLBACK = "fallback"      # 0/3 models — use local deterministic


# Confidence caps per degradation level
DEGRADATION_CAPS = {
    DegradationLevel.FULL: 1.0,
    DegradationLevel.PARTIAL: 0.80,
    DegradationLevel.REDUCED: 0.50,
    DegradationLevel.FALLBACK: 0.40,
}


@dataclass
class ModelResult:
    """Result from a single model."""
    model_name: str
    output: JudgeOutput = None
    error: str = None
    latency_ms: int = 0


@dataclass
class AnalysisResult:
    """Result from the judge orchestrator with degradation metadata."""
    outputs: Dict[str, Optional[JudgeOutput]] = field(default_factory=dict)
    degradation_level: DegradationLevel = DegradationLevel.FULL
    confidence_cap: float = 1.0
    successful_count: int = 0
    total_count: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class JudgeOrchestrator:
    """Orchestrate parallel execution of multiple AI judges with graceful degradation."""
    
    def __init__(self):
        """Initialize judges."""
        self.judges: Dict[str, BaseJudge] = {}

        if settings.GEMINI_API_KEY:
            try:
                from app.services.judge.gemini import GeminiJudge
                self.judges["gemini"] = GeminiJudge()
            except Exception:
                pass

        if settings.OPENAI_API_KEY:
            try:
                from app.services.judge.gpt import GPTJudge
                self.judges["gpt"] = GPTJudge()
            except Exception:
                pass

        if settings.ANTHROPIC_API_KEY:
            try:
                from app.services.judge.claude import ClaudeJudge
                self.judges["claude"] = ClaudeJudge()
            except Exception:
                pass
    
    async def run_parallel_analysis(
        self,
        case_id: str,
        proposition: str,
        definitions: Dict[str, Any],
        evidence_pack: List[Dict[str, Any]],
        single_model_mode: bool = False,
    ) -> AnalysisResult:
        """
        Run all judges in parallel with graceful degradation.
        
        PRD v2.0 degradation tiers:
        - 3/3 → FULL consensus (no cap)
        - 2/3 → PARTIAL consensus (cap 0.80)  
        - 1/3 → REDUCED analysis (cap 0.50)
        - 0/3 → FALLBACK to local deterministic (cap 0.40)
        
        Args:
            case_id: Case UUID
            proposition: Original proposition
            definitions: Operational definitions
            evidence_pack: Evidence items
            single_model_mode: If True, only use first available judge (Free tier)
            
        Returns:
            AnalysisResult with outputs and degradation metadata
        """
        if not self.judges:
            return AnalysisResult(
                degradation_level=DegradationLevel.FALLBACK,
                confidence_cap=DEGRADATION_CAPS[DegradationLevel.FALLBACK],
                total_count=0,
                warnings=["No model judges configured. Using local fallback."],
            )
        
        # In single_model_mode (Free tier), use only the first available judge
        judges_to_use = self.judges
        if single_model_mode:
            first_name = next(iter(self.judges))
            judges_to_use = {first_name: self.judges[first_name]}
        
        # Create tasks for all judges
        tasks = {
            name: self._run_judge_with_timeout(
                judge, case_id, proposition, definitions, evidence_pack
            )
            for name, judge in judges_to_use.items()
        }
        
        # Execute all tasks concurrently
        results = await asyncio.gather(
            *tasks.values(),
            return_exceptions=True
        )
        
        # Process results
        outputs = {}
        errors = []
        
        for (name, _), result in zip(tasks.items(), results):
            if isinstance(result, Exception):
                errors.append(f"{name}: {str(result)}")
                outputs[name] = None
            else:
                outputs[name] = result
        
        # Count successful judges
        successful = sum(1 for o in outputs.values() if o is not None)
        total = len(judges_to_use)
        
        # Determine degradation level
        if single_model_mode:
            degradation = DegradationLevel.REDUCED if successful >= 1 else DegradationLevel.FALLBACK
        elif successful >= 3:
            degradation = DegradationLevel.FULL
        elif successful >= 2:
            degradation = DegradationLevel.PARTIAL
        elif successful >= 1:
            degradation = DegradationLevel.REDUCED
        else:
            degradation = DegradationLevel.FALLBACK
        
        cap = DEGRADATION_CAPS[degradation]
        warnings = []
        
        if degradation == DegradationLevel.PARTIAL:
            warnings.append(f"Only {successful}/{total} models responded. Confidence capped at {int(cap*100)}%.")
        elif degradation == DegradationLevel.REDUCED:
            warnings.append(f"Only {successful}/{total} models responded. Reduced analysis mode, confidence capped at {int(cap*100)}%.")
        elif degradation == DegradationLevel.FALLBACK:
            warnings.append("No models responded. Using local deterministic fallback.")
        
        return AnalysisResult(
            outputs=outputs,
            degradation_level=degradation,
            confidence_cap=cap,
            successful_count=successful,
            total_count=total,
            errors=errors,
            warnings=warnings,
        )
    
    async def _run_judge_with_timeout(
        self,
        judge: BaseJudge,
        case_id: str,
        proposition: str,
        definitions: Dict[str, Any],
        evidence_pack: List[Dict[str, Any]]
    ) -> JudgeOutput:
        """Run a single judge with timeout handling."""
        timeout = getattr(judge, "timeout", settings.MODEL_TIMEOUT_SECONDS)
        if not isinstance(timeout, (int, float)):
            timeout = settings.MODEL_TIMEOUT_SECONDS

        return await asyncio.wait_for(
            judge.analyze(case_id, proposition, definitions, evidence_pack),
            timeout=timeout
        )
    
    def get_available_judges(self) -> List[str]:
        """Get list of available judge names."""
        return list(self.judges.keys())
    
    def is_ready(self) -> bool:
        """Check if orchestrator has at least one judge configured."""
        return len(self.judges) >= 1
