"""
Judge Orchestrator
Manages parallel execution of multiple model judges.
"""

import asyncio
from typing import Dict, List, Any
from dataclasses import dataclass

from app.core.config import get_settings
from app.core.exceptions import InsufficientConsensusException
from app.services.judge.base import BaseJudge, JudgeOutput, JudgeTimeoutError, JudgeParseError
from app.services.judge.gemini import GeminiJudge
from app.services.judge.gpt import GPTJudge
from app.services.judge.claude import ClaudeJudge

settings = get_settings()


@dataclass
class ModelResult:
    """Result from a single model."""
    model_name: str
    output: JudgeOutput = None
    error: str = None
    latency_ms: int = 0


class JudgeOrchestrator:
    """Orchestrate parallel execution of multiple AI judges."""
    
    def __init__(self):
        """Initialize judges."""
        self.judges: Dict[str, BaseJudge] = {}
        
        # Initialize available judges
        if settings.GEMINI_API_KEY:
            self.judges['gemini'] = GeminiJudge()
        if settings.OPENAI_API_KEY:
            self.judges['gpt'] = GPTJudge()
        if settings.ANTHROPIC_API_KEY:
            self.judges['claude'] = ClaudeJudge()
    
    async def run_parallel_analysis(
        self,
        case_id: str,
        proposition: str,
        definitions: Dict[str, Any],
        evidence_pack: List[Dict[str, Any]]
    ) -> Dict[str, JudgeOutput]:
        """
        Run all judges in parallel with timeout handling.
        
        Args:
            case_id: Case UUID
            proposition: Original proposition
            definitions: Operational definitions
            evidence_pack: Evidence items
            
        Returns:
            Dict mapping model names to JudgeOutput
            
        Raises:
            InsufficientConsensusException: If fewer than MIN_MODELS_FOR_CONSENSUS succeed
        """
        if not self.judges:
            raise InsufficientConsensusException(
                successful=0,
                required=settings.MIN_MODELS_FOR_CONSENSUS
            )
        
        # Create tasks for all judges
        tasks = {
            name: self._run_judge_with_timeout(
                judge, case_id, proposition, definitions, evidence_pack
            )
            for name, judge in self.judges.items()
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
                # Log error, continue with partial consensus
                errors.append(f"{name}: {str(result)}")
                outputs[name] = None
            else:
                outputs[name] = result
        
        # Count successful judges
        successful = sum(1 for o in outputs.values() if o is not None)
        
        # Check minimum requirement
        if successful < settings.MIN_MODELS_FOR_CONSENSUS:
            error_msg = f"Only {successful} judges succeeded, minimum {settings.MIN_MODELS_FOR_CONSENSUS} required"
            if errors:
                error_msg += f". Errors: {'; '.join(errors)}"
            raise InsufficientConsensusException(
                successful=successful,
                required=settings.MIN_MODELS_FOR_CONSENSUS
            )
        
        return outputs
    
    async def _run_judge_with_timeout(
        self,
        judge: BaseJudge,
        case_id: str,
        proposition: str,
        definitions: Dict[str, Any],
        evidence_pack: List[Dict[str, Any]]
    ) -> JudgeOutput:
        """Run a single judge with timeout handling."""
        return await asyncio.wait_for(
            judge.analyze(case_id, proposition, definitions, evidence_pack),
            timeout=judge.timeout
        )
    
    def get_available_judges(self) -> List[str]:
        """Get list of available judge names."""
        return list(self.judges.keys())
    
    def is_ready(self) -> bool:
        """Check if orchestrator has enough judges configured."""
        return len(self.judges) >= settings.MIN_MODELS_FOR_CONSENSUS
