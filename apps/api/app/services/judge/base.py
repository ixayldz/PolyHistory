"""
Base Judge Adapter
Abstract base class for AI model judges.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class JudgeOutput:
    """Structured output from a model judge."""
    definitions_review: List[str]
    claims: List[Dict[str, Any]]
    strongest_evidence: List[Dict[str, Any]]
    strongest_counter_evidence: List[Dict[str, Any]]
    uncertainties: List[str]
    bias_risk_notes: List[str]
    verdict: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "definitions_review": self.definitions_review,
            "claims": self.claims,
            "strongest_evidence": self.strongest_evidence,
            "strongest_counter_evidence": self.strongest_counter_evidence,
            "uncertainties": self.uncertainties,
            "bias_risk_notes": self.bias_risk_notes,
            "verdict": self.verdict
        }


class BaseJudge(ABC):
    """Abstract base class for model judges."""
    
    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.timeout = timeout
        self.model_name = self.__class__.__name__.replace('Judge', '').lower()
    
    @abstractmethod
    async def analyze(
        self,
        case_id: str,
        proposition: str,
        definitions: Dict[str, Any],
        evidence_pack: List[Dict[str, Any]]
    ) -> JudgeOutput:
        """Analyze evidence pack and return structured output."""
        pass
    
    @abstractmethod
    def _build_prompt(
        self,
        proposition: str,
        definitions: Dict[str, Any],
        evidence_pack: List[Dict[str, Any]]
    ) -> str:
        """Build model-specific prompt."""
        pass
    
    def _validate_output(self, output: Dict[str, Any]) -> JudgeOutput:
        """Validate and parse model output."""
        # Validate required fields
        required_fields = ["definitions_review", "claims", "strongest_evidence", 
                          "strongest_counter_evidence", "uncertainties", 
                          "bias_risk_notes", "verdict"]
        
        for field in required_fields:
            if field not in output:
                output[field] = [] if field != "verdict" else {"short_statement": "", "confidence_score": 0}
        
        # Validate verdict structure
        if "verdict" in output:
            if "short_statement" not in output["verdict"]:
                output["verdict"]["short_statement"] = ""
            if "confidence_score" not in output["verdict"]:
                output["verdict"]["confidence_score"] = 0
        
        return JudgeOutput(**output)
    
    def _format_evidence_pack(self, evidence_pack: List[Dict[str, Any]]) -> str:
        """Format evidence pack for prompt."""
        formatted = []
        for i, item in enumerate(evidence_pack, 1):
            formatted.append(f"""
EVIDENCE [{i}]:
- ID: {item.get('id', 'unknown')}
- Type: {item.get('source_type', 'unknown')}
- Country: {item.get('country', 'unknown')}
- Language: {item.get('language', 'unknown')}
- Reliability: {item.get('reliability_score', 'unknown')}
- Text: {item.get('text', 'No text')[:500]}...
""")
        return "\n".join(formatted)


class JudgeTimeoutError(Exception):
    """Raised when a judge times out."""
    pass


class JudgeParseError(Exception):
    """Raised when judge output cannot be parsed."""
    pass
