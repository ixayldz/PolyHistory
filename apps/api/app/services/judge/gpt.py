"""
GPT Judge Adapter
OpenAI GPT-5.2 model integration.
"""

import json
import asyncio
from typing import Dict, Any, List

from openai import AsyncOpenAI

from app.services.judge.base import BaseJudge, JudgeOutput, JudgeTimeoutError, JudgeParseError
from app.core.config import get_settings

settings = get_settings()

SYSTEM_PROMPT = """You are a historical analysis judge specializing in evidence-based historical research and claim decomposition.

Your task is to analyze historical propositions using ONLY the provided Evidence Pack. Focus on:
1. Precise claim decomposition
2. Consistency checking across sources
3. Structured reasoning

RULES:
1. Use ONLY the provided Evidence Pack - do not use external knowledge
2. Every claim MUST have at least one evidence reference
3. Check for contradictions between sources
4. Explicitly list all uncertainties
5. Do not speculate beyond the evidence
6. Present the strongest counter-argument

OUTPUT FORMAT - Valid JSON only:
{
  "definitions_review": ["Any definitional clarifications needed"],
  "claims": [
    {
      "claim_id": "unique-id",
      "normalized_text": "Precise claim statement",
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


class GPTJudge(BaseJudge):
    """OpenAI GPT-5.2 judge implementation.
    
    Model: gpt-5.2
    - Latest flagship model with advanced reasoning
    - Supports reasoning effort: none, low, medium, high, xhigh
    - Supports verbosity control: low, medium, high
    - Responses API for chain-of-thought preservation
    - JSON mode support
    """
    
    def __init__(self, api_key: str = None):
        api_key = api_key or settings.OPENAI_API_KEY
        super().__init__(api_key, timeout=settings.MODEL_TIMEOUT_SECONDS)
        self.client = AsyncOpenAI(api_key=api_key)
    
    async def analyze(
        self,
        case_id: str,
        proposition: str,
        definitions: Dict[str, Any],
        evidence_pack: List[Dict[str, Any]]
    ) -> JudgeOutput:
        """Analyze using GPT-5.2 with advanced reasoning capabilities."""
        prompt = self._build_prompt(proposition, definitions, evidence_pack)
        
        try:
            # GPT-5.2 with Responses API for optimal chain-of-thought handling
            response = await asyncio.wait_for(
                self.client.responses.create(
                    model="gpt-5.2",
                    input=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    reasoning={
                        "effort": "high"  # Use high reasoning for complex historical analysis
                    },
                    text={
                        "verbosity": "medium"  # Balanced output length
                    },
                    max_output_tokens=4000
                ),
                timeout=self.timeout
            )
            
            # Parse JSON response from output text
            output_text = response.output_text
            try:
                output = json.loads(output_text)
            except json.JSONDecodeError:
                # Try to extract JSON from markdown code block
                if "```json" in output_text:
                    json_str = output_text.split("```json")[1].split("```")[0]
                    output = json.loads(json_str)
                elif "```" in output_text:
                    json_str = output_text.split("```")[1].split("```")[0]
                    output = json.loads(json_str)
                else:
                    raise JudgeParseError(f"Invalid JSON from GPT-5.2")
            
            return self._validate_output(output)
            
        except asyncio.TimeoutError:
            raise JudgeTimeoutError(f"GPT-5.2 timeout for case {case_id}")
        except json.JSONDecodeError as e:
            raise JudgeParseError(f"Invalid JSON from GPT-5.2: {e}")
        except Exception as e:
            raise JudgeParseError(f"GPT-5.2 analysis failed: {e}")
    
    def _build_prompt(
        self,
        proposition: str,
        definitions: Dict[str, Any],
        evidence_pack: List[Dict[str, Any]]
    ) -> str:
        """Build prompt for GPT-5.2."""
        evidence_text = self._format_evidence_pack(evidence_pack)
        
        return f"""Analyze the following historical proposition using ONLY the provided evidence.

PROPOSITION: {proposition}

OPERATIONAL DEFINITIONS: {json.dumps(definitions, indent=2)}

{evidence_text}

Provide your analysis in the required JSON format."""
