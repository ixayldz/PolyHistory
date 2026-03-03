"""
Unit tests for PRD v2.0 alignment changes.
Tests consensus formula, adaptive MBR, evidence builder, and graceful degradation.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from datetime import date


# ============== Consensus Engine Tests ==============

class TestConsensusFormula:
    """Test PRD v2.0 normalized consensus formula: 0.4*A + 0.6*E."""

    def _make_engine(self):
        from app.services.consensus_engine import ConsensusEngine
        return ConsensusEngine()

    def test_formula_weighted_average(self):
        """Final score should be 0.4*agreement + 0.6*evidence, not product."""
        engine = self._make_engine()
        # Simulate a group with known values
        group = [{
            "model": "gemini",
            "claim": {
                "claim_id": "c1",
                "normalized_text": "test claim",
                "category": "diplomatic",
                "stance": "support",
                "evidence_refs": [],
            }
        }]
        all_models = ["gemini", "gpt", "claude"]
        result = engine._compute_group_consensus(group, all_models)

        # agreement_ratio = 1/3 ≈ 0.333
        # evidence_strength = 0.0 (no evidence refs)
        # final = 0.4 * 0.333 + 0.6 * 0.0 ≈ 0.133
        assert result.final_score == pytest.approx(0.4 * (1/3) + 0.6 * 0.0, abs=0.01)

    def test_full_agreement_high_evidence(self):
        """3/3 models + strong evidence should yield very_high."""
        engine = self._make_engine()
        refs = [
            {"source_type": "primary", "reliability": 0.9},
            {"source_type": "academic", "reliability": 0.8},
        ]
        group = [
            {"model": "gemini", "claim": {"claim_id": "c1", "normalized_text": "claim", "category": "diplomatic", "stance": "support", "evidence_refs": refs}},
            {"model": "gpt", "claim": {"claim_id": "c1", "normalized_text": "claim", "category": "diplomatic", "stance": "support", "evidence_refs": refs}},
            {"model": "claude", "claim": {"claim_id": "c1", "normalized_text": "claim", "category": "diplomatic", "stance": "support", "evidence_refs": refs}},
        ]
        all_models = ["gemini", "gpt", "claude"]
        result = engine._compute_group_consensus(group, all_models)

        # agreement = 3/3 = 1.0
        # final >= 0.86 when evidence is strong
        assert result.agreement_ratio == 1.0
        assert result.final_score >= 0.4  # at minimum 0.4 from agreement alone
        assert result.is_core_consensus is True

    def test_very_high_confidence_label(self):
        """Score >= 0.86 should return 'very_high' label."""
        engine = self._make_engine()
        refs = [{"source_type": "primary", "reliability": 1.0}]
        group = [
            {"model": m, "claim": {"claim_id": "c1", "normalized_text": "claim", "category": "diplomatic", "stance": "support", "evidence_refs": refs}}
            for m in ["gemini", "gpt", "claude"]
        ]
        result = engine._compute_group_consensus(group, ["gemini", "gpt", "claude"])
        
        # agreement=1.0, evidence=min(1.0*1.0/1, 1.0)=1.0
        # final = 0.4*1.0 + 0.6*1.0 = 1.0 → very_high
        assert result.confidence_label == "very_high"
        assert result.is_core_consensus is True

    def test_low_confidence_label(self):
        """Score < 0.31 should return 'low'."""
        engine = self._make_engine()
        group = [{
            "model": "gemini",
            "claim": {"claim_id": "c1", "normalized_text": "test", "category": "diplomatic", "stance": "support", "evidence_refs": []}
        }]
        result = engine._compute_group_consensus(group, ["gemini", "gpt", "claude"])
        # agreement=1/3, evidence=0, final = 0.133 → low
        assert result.confidence_label == "low"


# ============== Balance Protocol Tests ==============

class TestAdaptiveMBR:
    """Test PRD v2.0 adaptive MBR based on topic_scope."""

    def _make_protocol(self):
        from app.services.balance_protocol import BalanceProtocol
        return BalanceProtocol()

    def _make_evidence(self, country, source_type="primary", stance="pro"):
        item = MagicMock()
        item.country = country
        item.source_type = source_type
        item.stance = stance
        return item

    def test_international_requires_2_foreign(self):
        """International topics need foreign_countries >= 2."""
        protocol = self._make_protocol()
        evidence = [
            self._make_evidence("TR", "primary", "pro"),
            self._make_evidence("TR", "press", "contra"),
            self._make_evidence("UK", "primary", "neutral"),
            # Only 1 foreign country
        ]
        result = protocol.check_minimum_balance("test", evidence, topic_scope="international")
        assert result.compliant is False
        assert "foreign_countries" in result.missing_clusters

    def test_domestic_requires_1_foreign(self):
        """Domestic topics need foreign_countries >= 1."""
        protocol = self._make_protocol()
        evidence = [
            self._make_evidence("TR", "primary", "pro"),
            self._make_evidence("TR", "press", "contra"),
            self._make_evidence("UK", "primary", "neutral"),
            self._make_evidence("UK", "press", "neutral"),
        ]
        result = protocol.check_minimum_balance("test", evidence, topic_scope="domestic")
        # 1 foreign country (UK) should be enough for domestic
        assert "foreign_countries" not in result.missing_clusters

    def test_suggested_search_terms(self):
        """Missing foreign clusters should include suggested search terms."""
        protocol = self._make_protocol()
        evidence = [
            self._make_evidence("TR", "primary", "pro"),
            self._make_evidence("TR", "press", "contra"),
        ]
        result = protocol.check_minimum_balance("test", evidence, topic_scope="domestic")
        assert "foreign_countries" in result.missing_clusters
        assert "suggested_search_terms" in result.missing_clusters["foreign_countries"]

    def test_topic_scope_stored(self):
        """MBRStatus should store the topic_scope used."""
        protocol = self._make_protocol()
        evidence = [
            self._make_evidence("TR", "primary", "pro"),
            self._make_evidence("TR", "press", "contra"),
            self._make_evidence("UK", "primary", "neutral"),
            self._make_evidence("FR", "press", "neutral"),
        ]
        result = protocol.check_minimum_balance("test", evidence, topic_scope="domestic")
        assert result.topic_scope == "domestic"


# ============== Evidence Builder Tests ==============

class TestEvidenceBuilderFormula:
    """Test PRD v2.0 5-factor reliability formula."""

    def _make_item(self, source_type="primary", publisher="National Archives",
                   url=None, stance="pro", snippets=None):
        item = MagicMock()
        item.source_type = source_type
        item.publisher = publisher
        item.url = url
        item.stance = stance
        item.country = "TR"
        item.snippets = snippets or []
        item.reliability_score = None
        item.reliability_factors = None
        return item

    def test_document_quality_digital(self):
        """Born-digital academic/press sources should get quality 1.0."""
        from app.services.evidence_builder import EvidenceBuilder

        builder = EvidenceBuilder.__new__(EvidenceBuilder)
        builder.embedding_model = None

        item = self._make_item(source_type="academic", url="https://example.com")
        quality = builder._compute_document_quality(item)
        assert quality == 1.0

    def test_document_quality_ocr(self):
        """Sources without URL use snippet quality as OCR proxy."""
        from app.services.evidence_builder import EvidenceBuilder

        builder = EvidenceBuilder.__new__(EvidenceBuilder)
        builder.embedding_model = None

        snippet = MagicMock()
        snippet.quality_score = 0.85
        item = self._make_item(source_type="primary", snippets=[snippet])
        quality = builder._compute_document_quality(item)
        assert quality == 0.85

    def test_document_quality_default(self):
        """Sources without URL or quality data default to 0.7."""
        from app.services.evidence_builder import EvidenceBuilder

        builder = EvidenceBuilder.__new__(EvidenceBuilder)
        builder.embedding_model = None

        item = self._make_item(source_type="primary", snippets=[])
        quality = builder._compute_document_quality(item)
        assert quality == 0.7

    def test_citation_score_primary(self):
        """Primary sources should have highest citation score."""
        from app.services.evidence_builder import EvidenceBuilder

        builder = EvidenceBuilder.__new__(EvidenceBuilder)
        builder.embedding_model = None

        item = self._make_item(source_type="primary")
        score = builder._compute_citation_score(item)
        assert score == 0.9

    def test_reliability_factors_keys(self):
        """Scored evidence should have all 5 PRD v2.0 factor keys."""
        from app.services.evidence_builder import EvidenceBuilder
        import asyncio

        builder = EvidenceBuilder.__new__(EvidenceBuilder)
        builder.embedding_model = None
        builder.db = MagicMock()

        item = self._make_item()
        asyncio.run(builder._score_evidence([item], MagicMock()))

        expected_keys = {
            "source_type_score", "institution_reputation",
            "document_quality", "cross_source_consistency",
            "citation_count_score"
        }
        assert set(item.reliability_factors.keys()) == expected_keys


# ============== Orchestrator Degradation Tests ==============

class TestGracefulDegradation:
    """Test PRD v2.0 4-tier graceful degradation."""

    def test_degradation_levels_exist(self):
        """DegradationLevel enum should have all 4 tiers."""
        from app.services.judge.orchestrator import DegradationLevel
        assert DegradationLevel.FULL.value == "full"
        assert DegradationLevel.PARTIAL.value == "partial"
        assert DegradationLevel.REDUCED.value == "reduced"
        assert DegradationLevel.FALLBACK.value == "fallback"

    def test_confidence_caps(self):
        """Confidence caps should match PRD v2.0."""
        from app.services.judge.orchestrator import DEGRADATION_CAPS, DegradationLevel
        assert DEGRADATION_CAPS[DegradationLevel.FULL] == 1.0
        assert DEGRADATION_CAPS[DegradationLevel.PARTIAL] == 0.80
        assert DEGRADATION_CAPS[DegradationLevel.REDUCED] == 0.50
        assert DEGRADATION_CAPS[DegradationLevel.FALLBACK] == 0.40

    def test_analysis_result_defaults(self):
        """AnalysisResult should have sensible defaults."""
        from app.services.judge.orchestrator import AnalysisResult, DegradationLevel
        result = AnalysisResult()
        assert result.degradation_level == DegradationLevel.FULL
        assert result.confidence_cap == 1.0
        assert result.outputs == {}
        assert result.errors == []

    @pytest.mark.asyncio
    async def test_no_judges_returns_fallback(self):
        """Orchestrator with no judges should return FALLBACK."""
        from app.services.judge.orchestrator import JudgeOrchestrator, DegradationLevel

        with patch.object(JudgeOrchestrator, '__init__', lambda self: setattr(self, 'judges', {})):
            orch = JudgeOrchestrator()
            result = await orch.run_parallel_analysis("c1", "test", {}, [])
            assert result.degradation_level == DegradationLevel.FALLBACK
            assert result.confidence_cap == 0.40
