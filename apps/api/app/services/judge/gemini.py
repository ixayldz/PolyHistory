"""
Gemini Judge Adapter
Google Gemini 3.1 Pro Preview model integration.
"""

import json
import asyncio
from typing import Dict, Any, List

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - optional dependency in local/offline mode
    genai = None

from app.services.judge.base import BaseJudge, JudgeOutput, JudgeTimeoutError, JudgeParseError
from app.core.config import get_settings

settings = get_settings()

SYSTEM_PROMPT = """You are a historical analysis judge specializing in evidence-based historical research.

Your task is to analyze historical propositions using ONLY the provided Evidence Pack.

RULES:
1. Use ONLY the provided Evidence Pack - do not use external knowledge
2. Every claim MUST have at least one evidence reference
3. Distinguish between discourse evidence (press, propaganda) and event evidence (official documents)
4. Explicitly list all uncertainties and data gaps
5. Do not speculate beyond the evidence
6. Present the strongest counter-argument (steel-man principle)

OUTPUT FORMAT - Valid JSON only:
{
  "definitions_review": ["List any definitional issues or clarifications"],
  "claims": [
    {
      "claim_id": "unique-id",
      "normalized_text": "Clear statement of claim",
      "category": "diplomatic|economic|military|intelligence|propaganda",
      "stance": "support|oppose|neutral",
      "evidence_refs": [{"evidence_id": "id", "snippet_id": "id"}],
      "evidence_strength_score": 0.0-1.0
    }
  ],
  "strongest_evidence": [{"evidence_id": "id", "reasoning": "why strong"}],
  "strongest_counter_evidence": [{"evidence_id": "id", "reasoning": "why counters"}],
  "uncertainties": ["List uncertainties"],
  "bias_risk_notes": ["Potential bias issues"],
  "verdict": {
    "short_statement": "2-6 sentence summary",
    "confidence_score": 0-100
  }
}

CONFIDENCE SCORING:
- 70-100: Strong primary evidence supporting
- 40-69: Mixed or secondary evidence
- 0-39: Weak or insufficient evidence

If no primary evidence exists, confidence MUST NOT exceed 70."""


class GeminiJudge(BaseJudge):
    """Google Gemini 3.1 Pro Preview judge implementation.
    
    Model: gemini-3.1-pro-preview
    - Advanced reasoning capabilities
    - 2M token context window
    - Native JSON output support
    - Optimized for complex analysis tasks
    """
    
    def __init__(self, api_key: str = None):
        api_key = api_key or settings.GEMINI_API_KEY
        super().__init__(api_key, timeout=settings.MODEL_TIMEOUT_SECONDS)
        if genai is None:
            raise RuntimeError("google-generativeai package is not installed")

        genai.configure(api_key=api_key)
        # Gemini 3.1 Pro Preview - Latest model with enhanced capabilities
        self.model = genai.GenerativeModel(
            model_name="gemini-3.1-pro-preview",
            system_instruction=SYSTEM_PROMPT,
            generation_config={
                "temperature": 0.1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "application/json"
            }
        )
    
    async def analyze(
        self,
        case_id: str,
        proposition: str,
        definitions: Dict[str, Any],
        evidence_pack: List[Dict[str, Any]]
    ) -> JudgeOutput:
        """Analyze using Gemini 3.1 Pro Preview."""
        prompt = self._build_prompt(proposition, definitions, evidence_pack)
        
        try:
            # Run in executor to make async
            loop = asyncio.get_event_loop()
            response = await asyncio.wait_for(
                loop.run_in_executor(
                    None, 
                    lambda: self.model.generate_content(prompt)
                ),
                timeout=self.timeout
            )
            
            # Parse JSON response
            try:
                output = json.loads(response.text)
            except json.JSONDecodeError as e:
                # Try to extract JSON from markdown code block
                text = response.text
                if "```json" in text:
                    json_str = text.split("```json")[1].split("```")[0]
                    output = json.loads(json_str)
                elif "```" in text:
                    json_str = text.split("```")[1].split("```")[0]
                    output = json.loads(json_str)
                else:
                    raise JudgeParseError(f"Invalid JSON from Gemini: {e}")
            
            return self._validate_output(output)
            
        except asyncio.TimeoutError:
            raise JudgeTimeoutError(f"Gemini 3.1 Pro Preview timeout for case {case_id}")
        except Exception as e:
            raise JudgeParseError(f"Gemini 3.1 Pro Preview analysis failed: {e}")
    
    def _build_prompt(
        self,
        proposition: str,
        definitions: Dict[str, Any],
        evidence_pack: List[Dict[str, Any]]
    ) -> str:
        """Build prompt for Gemini 3.1 Pro Preview."""
        evidence_text = self._format_evidence_pack(evidence_pack)
        
        return f"""Analyze the following historical proposition using ONLY the provided evidence.

PROPOSITION: {proposition}

OPERATIONAL DEFINITIONS: {json.dumps(definitions, indent=2)}

{evidence_text}

Provide your analysis in the required JSON format."""
