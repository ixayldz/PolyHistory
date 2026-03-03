"""
Test suite for Sprint 3: AI Integration (Model Judges, Orchestrator, Consensus Engine).
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import json

from app.services.judge.base import BaseJudge, JudgeOutput, JudgeTimeoutError, JudgeParseError
from app.services.judge.gemini import GeminiJudge
from app.services.judge.gpt import GPTJudge
from app.services.judge.claude import ClaudeJudge
from app.services.judge.orchestrator import JudgeOrchestrator, ModelResult, AnalysisResult, DegradationLevel
from app.services.consensus_engine import ConsensusEngine, ConsensusClaim, ConsensusResult


class TestBaseJudge:
    """Test base judge functionality."""
    
    def test_validate_output_complete(self):
        """Test output validation with complete data."""
        judge = Mock(spec=BaseJudge)
        judge._validate_output = BaseJudge._validate_output.__get__(judge, Mock)
        
        output = {
            "definitions_review": ["test"],
            "claims": [],
            "strongest_evidence": [],
            "strongest_counter_evidence": [],
            "uncertainties": [],
            "bias_risk_notes": [],
            "verdict": {"short_statement": "test", "confidence_score": 50}
        }
        
        result = judge._validate_output(output)
        
        assert isinstance(result, JudgeOutput)
        assert result.verdict["confidence_score"] == 50
    
    def test_validate_output_missing_fields(self):
        """Test output validation with missing fields."""
        judge = Mock(spec=BaseJudge)
        judge._validate_output = BaseJudge._validate_output.__get__(judge, Mock)
        
        output = {
            "verdict": {"short_statement": "test"}  # Missing confidence_score
        }
        
        result = judge._validate_output(output)
        
        assert result.verdict["confidence_score"] == 0  # Should default to 0
        assert result.claims == []  # Should default to empty list
    
    def test_format_evidence_pack(self):
        """Test evidence pack formatting."""
        judge = Mock(spec=BaseJudge)
        judge._format_evidence_pack = BaseJudge._format_evidence_pack.__get__(judge, Mock)
        
        evidence = [
            {"id": "1", "source_type": "primary", "country": "TR", "text": "Test evidence"}
        ]
        
        result = judge._format_evidence_pack(evidence)
        
        assert "EVIDENCE [1]" in result
        assert "primary" in result
        assert "TR" in result


class TestJudgeOrchestrator:
    """Test judge orchestrator."""
    
    @pytest.fixture
    def mock_judges(self):
        """Create mock judges."""
        gemini = Mock(spec=GeminiJudge)
        gemini.analyze = AsyncMock(return_value=JudgeOutput(
            definitions_review=[],
            claims=[{"claim_id": "1", "normalized_text": "Claim A"}],
            strongest_evidence=[],
            strongest_counter_evidence=[],
            uncertainties=[],
            bias_risk_notes=[],
            verdict={"short_statement": "Test", "confidence_score": 70}
        ))
        
        gpt = Mock(spec=GPTJudge)
        gpt.analyze = AsyncMock(return_value=JudgeOutput(
            definitions_review=[],
            claims=[{"claim_id": "1", "normalized_text": "Claim A"}],
            strongest_evidence=[],
            strongest_counter_evidence=[],
            uncertainties=[],
            bias_risk_notes=[],
            verdict={"short_statement": "Test", "confidence_score": 75}
        ))
        
        claude = Mock(spec=ClaudeJudge)
        claude.analyze = AsyncMock(return_value=JudgeOutput(
            definitions_review=[],
            claims=[{"claim_id": "2", "normalized_text": "Claim B"}],
            strongest_evidence=[],
            strongest_counter_evidence=[],
            uncertainties=[],
            bias_risk_notes=[],
            verdict={"short_statement": "Test", "confidence_score": 65}
        ))
        
        return {"gemini": gemini, "gpt": gpt, "claude": claude}
    
    @pytest.mark.asyncio
    async def test_run_parallel_analysis_success(self, mock_judges):
        """Test successful parallel analysis."""
        orchestrator = JudgeOrchestrator()
        orchestrator.judges = mock_judges
        
        result = await orchestrator.run_parallel_analysis(
            case_id="test-123",
            proposition="Test proposition",
            definitions={},
            evidence_pack=[]
        )
        
        assert isinstance(result, AnalysisResult)
        assert len(result.outputs) == 3
        assert "gemini" in result.outputs
        assert "gpt" in result.outputs
        assert "claude" in result.outputs
        assert result.degradation_level == DegradationLevel.FULL
    
    @pytest.mark.asyncio
    async def test_run_parallel_analysis_partial_failure(self, mock_judges):
        """Test parallel analysis with one failure."""
        orchestrator = JudgeOrchestrator()
        orchestrator.judges = mock_judges
        
        # Make one judge fail
        mock_judges["claude"].analyze = AsyncMock(side_effect=Exception("Claude error"))
        
        result = await orchestrator.run_parallel_analysis(
            case_id="test-123",
            proposition="Test proposition",
            definitions={},
            evidence_pack=[]
        )
        
        assert isinstance(result, AnalysisResult)
        assert len(result.outputs) == 3
        assert result.outputs["gemini"] is not None
        assert result.outputs["gpt"] is not None
        assert result.outputs["claude"] is None  # Failed
        assert result.degradation_level == DegradationLevel.PARTIAL
    
    @pytest.mark.asyncio
    async def test_run_parallel_analysis_insufficient_judges(self, mock_judges):
        """Test with too many failures — should return REDUCED degradation, not raise."""
        orchestrator = JudgeOrchestrator()
        orchestrator.judges = mock_judges
        
        # Make two judges fail
        mock_judges["gpt"].analyze = AsyncMock(side_effect=Exception("GPT error"))
        mock_judges["claude"].analyze = AsyncMock(side_effect=Exception("Claude error"))
        
        # Graceful degradation: should NOT raise, but return REDUCED level
        result = await orchestrator.run_parallel_analysis(
            case_id="test-123",
            proposition="Test proposition",
            definitions={},
            evidence_pack=[]
        )
        assert result.degradation_level == DegradationLevel.REDUCED
        assert result.confidence_cap == 0.50
        assert result.successful_count == 1
    
    def test_get_available_judges(self, mock_judges):
        """Test getting available judges."""
        orchestrator = JudgeOrchestrator()
        orchestrator.judges = mock_judges
        
        available = orchestrator.get_available_judges()
        
        assert len(available) == 3
        assert "gemini" in available
        assert "gpt" in available
        assert "claude" in available
    
    def test_is_ready(self, mock_judges):
        """Test readiness check."""
        orchestrator = JudgeOrchestrator()
        orchestrator.judges = mock_judges
        
        assert orchestrator.is_ready() is True
    
    def test_is_not_ready(self):
        """Test not ready when no judges."""
        orchestrator = JudgeOrchestrator()
        orchestrator.judges = {}
        
        assert orchestrator.is_ready() is False


class TestConsensusEngine:
    """Test consensus engine."""
    
    @pytest.fixture
    def engine(self):
        return ConsensusEngine()
    
    @pytest.fixture
    def sample_model_outputs(self):
        """Create sample model outputs for testing."""
        return {
            "gemini": JudgeOutput(
                definitions_review=[],
                claims=[{
                    "claim_id": "1",
                    "normalized_text": "Mustafa Kemal had diplomatic contact with British officials",
                    "category": "diplomatic",
                    "stance": "support",
                    "evidence_refs": [{"evidence_id": "e1", "source_type": "primary", "reliability": 0.9}]
                }],
                strongest_evidence=[],
                strongest_counter_evidence=[],
                uncertainties=[],
                bias_risk_notes=[],
                verdict={"short_statement": "Evidence supports diplomatic contact", "confidence_score": 70}
            ),
            "gpt": JudgeOutput(
                definitions_review=[],
                claims=[{
                    "claim_id": "1",
                    "normalized_text": "Mustafa Kemal had diplomatic contact with British officials",
                    "category": "diplomatic",
                    "stance": "support",
                    "evidence_refs": [{"evidence_id": "e2", "source_type": "primary", "reliability": 0.85}]
                }],
                strongest_evidence=[],
                strongest_counter_evidence=[],
                uncertainties=[],
                bias_risk_notes=[],
                verdict={"short_statement": "Diplomatic contact confirmed", "confidence_score": 75}
            ),
            "claude": JudgeOutput(
                definitions_review=[],
                claims=[{
                    "claim_id": "2",
                    "normalized_text": "No evidence of secret collaboration",
                    "category": "intelligence",
                    "stance": "oppose",
                    "evidence_refs": [{"evidence_id": "e3", "source_type": "secondary", "reliability": 0.6}]
                }],
                strongest_evidence=[],
                strongest_counter_evidence=[],
                uncertainties=[],
                bias_risk_notes=[],
                verdict={"short_statement": "No secret collaboration found", "confidence_score": 60}
            )
        }
    
    @pytest.mark.asyncio
    async def test_compute_consensus(self, engine, sample_model_outputs):
        """Test consensus computation."""
        result = await engine.compute_consensus(sample_model_outputs)
        
        assert isinstance(result, ConsensusResult)
        assert result.overall_confidence > 0
        assert len(result.summary) > 0
    
    @pytest.mark.asyncio
    async def test_consensus_core_claims(self, engine, sample_model_outputs):
        """Test that core claims are identified correctly."""
        result = await engine.compute_consensus(sample_model_outputs)
        
        # Should have at least one core or medium claim
        assert len(result.core_claims) > 0 or len(result.medium_claims) > 0
    
    @pytest.mark.asyncio
    async def test_consensus_disputed_claims(self, engine):
        """Test disputed claims detection."""
        # Create outputs with conflicting stances
        conflicting_outputs = {
            "gemini": JudgeOutput(
                definitions_review=[],
                claims=[{
                    "claim_id": "1",
                    "normalized_text": "Claim A",
                    "stance": "support"
                }],
                strongest_evidence=[],
                strongest_counter_evidence=[],
                uncertainties=[],
                bias_risk_notes=[],
                verdict={"short_statement": "", "confidence_score": 50}
            ),
            "gpt": JudgeOutput(
                definitions_review=[],
                claims=[{
                    "claim_id": "1",
                    "normalized_text": "Claim A",
                    "stance": "oppose"
                }],
                strongest_evidence=[],
                strongest_counter_evidence=[],
                uncertainties=[],
                bias_risk_notes=[],
                verdict={"short_statement": "", "confidence_score": 50}
            ),
            "claude": JudgeOutput(
                definitions_review=[],
                claims=[{
                    "claim_id": "1",
                    "normalized_text": "Claim A",
                    "stance": "support"
                }],
                strongest_evidence=[],
                strongest_counter_evidence=[],
                uncertainties=[],
                bias_risk_notes=[],
                verdict={"short_statement": "", "confidence_score": 50}
            )
        }
        
        result = await engine.compute_consensus(conflicting_outputs)
        
        # Should detect dispute
        assert len(result.disputed_claims) > 0
    
    def test_text_similarity(self, engine):
        """Test text similarity calculation."""
        text1 = "Mustafa Kemal had diplomatic contact"
        text2 = "Mustafa Kemal had diplomatic contact with British"
        text3 = "Completely different claim"
        
        sim1 = engine._text_similarity(text1, text2)
        sim2 = engine._text_similarity(text1, text3)
        
        assert sim1 > sim2  # Similar texts should have higher score
        assert sim1 > 0.5
        assert sim2 < 0.5
    
    def test_compute_evidence_strength(self, engine):
        """Test evidence strength calculation."""
        evidence_refs = [
            {"source_type": "primary", "reliability": 0.9},
            {"source_type": "primary", "reliability": 0.8},
        ]
        
        strength = engine._compute_evidence_strength(evidence_refs)
        
        assert strength > 0
        assert strength <= 1.0
    
    def test_compute_evidence_strength_empty(self, engine):
        """Test evidence strength with empty refs."""
        strength = engine._compute_evidence_strength([])
        
        assert strength == 0.0
    
    def test_majority_stance(self, engine):
        """Test majority stance determination."""
        group = [
            {"claim": {"stance": "support"}},
            {"claim": {"stance": "support"}},
            {"claim": {"stance": "oppose"}}
        ]
        
        stance = engine._majority_stance(group)
        
        assert stance == "support"
    
    def test_majority_stance_neutral(self, engine):
        """Test majority stance with no clear majority."""
        group = [
            {"claim": {"stance": "support"}},
            {"claim": {"stance": "oppose"}}
        ]
        
        stance = engine._majority_stance(group)
        
        # Should return one of them
        assert stance in ["support", "oppose"]
    
    def test_build_agreement_matrix(self, engine):
        """Test agreement matrix construction."""
        model_outputs = {"gemini": Mock(), "gpt": Mock()}
        claim_groups = [
            [{"model": "gemini"}, {"model": "gpt"}]
        ]
        
        matrix = engine._build_agreement_matrix(model_outputs, claim_groups)
        
        assert "models" in matrix
        assert "claims" in matrix
        assert "agreement_scores" in matrix
        assert len(matrix["models"]) == 2
    
    def test_generate_summary(self, engine):
        """Test summary generation."""
        core_claims = [ConsensusClaim(id="1", normalized_text="Claim A", category="test", stance="support")]
        disputed_claims = []
        confidence = 0.75
        
        summary = engine._generate_summary(core_claims, disputed_claims, confidence)
        
        assert "1 core consensus" in summary or "1 core" in summary.lower()
        assert "75%" in summary or "confidence" in summary.lower()
    
    def test_evidence_weights(self, engine):
        """Test evidence type weights."""
        assert engine.EVIDENCE_WEIGHTS["primary"] == 1.0
        assert engine.EVIDENCE_WEIGHTS["academic"] == 0.8
        assert engine.EVIDENCE_WEIGHTS["secondary"] == 0.7
        assert engine.EVIDENCE_WEIGHTS["memoir"] == 0.5
        assert engine.EVIDENCE_WEIGHTS["press"] == 0.4
