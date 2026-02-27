"""
Claude Judge Adapter
Anthropic Claude Opus 4.6 model integration.
"""

import json
import asyncio
from typing import Dict, Any, List

from anthropic import AsyncAnthropic

from app.services.judge.base import BaseJudge, JudgeOutput, JudgeTimeoutError, JudgeParseError
from app.core.config import get_settings

settings = get_settings()

SYSTEM_PROMPT = """You are a historical analysis judge specializing in nuanced historical interpretation and steel-man argumentation.

Your task is to analyze historical propositions using ONLY the provided Evidence Pack. Focus on:
1. Nuanced historical interpretation
2. Steel-man counter-arguments (strongest version of opposing view)
3. Language and translation quality
4. Contextual understanding

RULES:
1. Use ONLY the provided Evidence Pack - do not use external knowledge
2. Every claim MUST have at least one evidence reference
3. Present the strongest counter-argument before your conclusion
4. Consider translation and terminology nuances
5. Explicitly list all uncertainties
6. Do not speculate beyond the evidence

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

STEEL-MAN PRINCIPLE:
Before presenting your conclusion, you MUST present the strongest possible version of the counter-argument, with full evidence support.

CONFIDENCE SCORING:
- 70-100: Strong primary evidence supporting
- 40-69: Mixed or secondary evidence
- 0-39: Weak or insufficient evidence

If no primary evidence exists, confidence MUST NOT exceed 70."""


class ClaudeJudge(BaseJudge):
    """Anthropic Claude Opus 4.6 judge implementation.
    
    Model: claude-opus-4-6
    - Most intelligent model for complex analysis
    - Adaptive thinking mode for dynamic reasoning depth
    - Effort parameter: low, medium, high, max
    - 200K context window (1M in beta)
    - 128K max output tokens
    - Steel-man argumentation specialization
    """
    
    def __init__(self, api_key: str = None):
        api_key = api_key or settings.ANTHROPIC_API_KEY
        super().__init__(api_key, timeout=settings.MODEL_TIMEOUT_SECONDS)
        self.client = AsyncAnthropic(api_key=api_key)
    
    async def analyze(
        self,
        case_id: str,
        proposition: str,
        definitions: Dict[str, Any],
        evidence_pack: List[Dict[str, Any]]
    ) -> JudgeOutput:
        """Analyze using Claude Opus 4.6 with adaptive thinking."""
        prompt = self._build_prompt(proposition, definitions, evidence_pack)
        
        try:
            # Claude Opus 4.6 with adaptive thinking and high effort
            response = await asyncio.wait_for(
                self.client.messages.create(
                    model="claude-opus-4-6",
                    max_tokens=8000,  # 128K available, using 8K for balance
                    system=SYSTEM_PROMPT,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    # Adaptive thinking for dynamic reasoning depth
                    thinking={
                        "type": "adaptive"
                    },
                    # High effort for maximum analysis quality
                    effort="high"
                ),
                timeout=self.timeout
            )
            
            # Parse JSON response
            content = response.content[0].text
            
            # Try to extract JSON if wrapped in markdown
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0]
                output = json.loads(json_str)
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0]
                output = json.loads(json_str)
            else:
                output = json.loads(content)
            
            return self._validate_output(output)
            
        except asyncio.TimeoutError:
            raise JudgeTimeoutError(f"Claude Opus 4.6 timeout for case {case_id}")
        except json.JSONDecodeError as e:
            raise JudgeParseError(f"Invalid JSON from Claude Opus 4.6: {e}")
        except Exception as e:
            raise JudgeParseError(f"Claude Opus 4.6 analysis failed: {e}")
    
    def _build_prompt(
        self,
        proposition: str,
        definitions: Dict[str, Any],
        evidence_pack: List[Dict[str, Any]]
    ) -> str:
        """Build prompt for Claude Opus 4.6."""
        evidence_text = self._format_evidence_pack(evidence_pack)
        
        return f"""Analyze the following historical proposition using ONLY the provided evidence.

PROPOSITION: {proposition}

OPERATIONAL DEFINITIONS: {json.dumps(definitions, indent=2)}

{evidence_text}

Provide your analysis in the required JSON format. Remember to apply the steel-man principle - present the strongest counter-argument before your conclusion."""
