"""
Test suite for Sprint 2: Retrieval & Evidence services.
"""

import pytest
from datetime import date
from unittest.mock import Mock, AsyncMock, patch
import numpy as np

from app.services.proposition_parser import PropositionParser
from app.services.query_expansion import QueryExpansionEngine, ExpandedQuery
from app.services.evidence_builder import EvidenceBuilder
from app.services.balance_protocol import BalanceProtocol, MBRStatus
from app import models
from app.schemas import PropositionParsed, TimeWindow


class TestPropositionParser:
    """Test proposition parsing service."""
    
    @pytest.fixture
    def parser(self):
        with patch('app.services.proposition_parser.spacy.load') as mock_load:
            mock_nlp = Mock()
            mock_nlp.return_value.ents = []
            mock_load.return_value = mock_nlp
            yield PropositionParser()
    
    @pytest.mark.asyncio
    async def test_parse_basic_proposition(self, parser):
        """Test parsing a basic historical proposition."""
        result = await parser.parse("Mustafa Kemal Atatürk İngilizlerle iş yaptı mı?")
        
        assert isinstance(result, PropositionParsed)
        assert len(result.entities) >= 0  # May or may not extract entities
        assert result.geography is not None
        assert "Turkey" in result.geography or "UK" in result.geography
    
    @pytest.mark.asyncio
    async def test_time_window_inference(self, parser):
        """Test time window inference from historical references."""
        # Test explicit year range
        result = await parser.parse("What happened between 1919 and 1923?")
        assert result.time_window.start == date(1919, 1, 1)
        assert result.time_window.end == date(1923, 12, 31)
    
    @pytest.mark.asyncio
    async def test_historical_period_detection(self, parser):
        """Test detection of historical periods."""
        result = await parser.parse("Kurtuluş Savaşı döneminde ne oldu?")
        assert result.time_window.start == date(1919, 5, 19)
        assert result.time_window.end == date(1923, 10, 29)
    
    def test_extract_entities(self, parser):
        """Test entity extraction."""
        # Mock NLP entities
        mock_ent = Mock()
        mock_ent.text = "Mustafa Kemal"
        mock_ent.label_ = "PERSON"
        parser.nlp = Mock()
        parser.nlp.return_value.ents = [mock_ent]
        
        entities = parser._extract_entities("Mustafa Kemal Atatürk was a leader.")
        assert "Mustafa Kemal" in entities
    
    def test_find_ambiguous_terms(self, parser):
        """Test detection of ambiguous terms."""
        result = parser._find_ambiguous_terms("Mustafa Kemal iş yaptı mı?", "tr")
        assert "iş yapmak" in result
    
    def test_create_definitions(self, parser):
        """Test creation of operational definitions."""
        terms = ["iş yapmak"]
        definitions = parser._create_definitions(terms)
        
        assert "iş yapmak" in definitions
        assert "diplomatic_contact" in definitions["iş yapmak"]
        assert "economic_agreement" in definitions["iş yapmak"]
    
    def test_determine_claim_type(self, parser):
        """Test claim type determination."""
        # Test diplomatic
        result = parser._determine_claim_type("Diplomasi görüşmeleri yapıldı mı?")
        assert result == "diplomatic"
        
        # Test economic
        result = parser._determine_claim_type("Ekonomik anlaşma yapıldı mı?")
        assert result == "economic"
        
        # Test military
        result = parser._determine_claim_type("Askeri destek sağlandı mı?")
        assert result == "military"


class TestQueryExpansion:
    """Test query expansion service."""
    
    @pytest.fixture
    def engine(self):
        return QueryExpansionEngine()
    
    def test_expand_basic(self, engine):
        """Test basic query expansion."""
        result = engine.expand(
            proposition="Mustafa Kemal Atatürk",
            entities=["Mustafa Kemal"],
            time_window=(date(1919, 1, 1), date(1923, 12, 31)),
            languages=["tr", "en"]
        )
        
        assert "tr" in result
        assert "en" in result
        assert isinstance(result["tr"], ExpandedQuery)
        assert isinstance(result["en"], ExpandedQuery)
    
    def test_generate_variants(self, engine):
        """Test variant generation for different languages."""
        variants = engine._generate_variants(
            "Mustafa Kemal Atatürk",
            ["Mustafa Kemal", "Atatürk"],
            "en"
        )
        
        assert len(variants) > 0
        # Should include name variants
        assert any("mustafa kemal" in v.lower() for v in variants) or \
               any("atatürk" in v.lower() for v in variants)
    
    def test_generate_keywords(self, engine):
        """Test keyword generation."""
        keywords = engine._generate_keywords("tr")
        
        assert len(keywords) > 0
        assert "anlaşma" in keywords or "antlaşma" in keywords
        assert "arşiv" in keywords
    
    def test_get_search_queries(self, engine):
        """Test search query generation."""
        expanded = {
            "tr": ExpandedQuery(
                language="tr",
                original="test",
                variants=["variant1", "variant2"],
                keywords=["keyword1", "keyword2"]
            )
        }
        
        queries = engine.get_search_queries(expanded)
        
        assert len(queries) > 0
        assert all("query" in q for q in queries)
        assert all("language" in q for q in queries)


class TestEvidenceBuilder:
    """Test evidence builder service."""
    
    @pytest.fixture
    def mock_db(self):
        return AsyncMock()
    
    @pytest.fixture
    def builder(self, mock_db):
        with patch('app.services.evidence_builder.SentenceTransformer') as mock_model:
            mock_model.return_value.encode.return_value = np.array([0.1, 0.2, 0.3])
            yield EvidenceBuilder(mock_db)
    
    @pytest.mark.asyncio
    async def test_score_evidence(self, builder):
        """Test evidence scoring."""
        # Create mock evidence items
        item1 = models.EvidenceItem(
            source_type="primary",
            publisher="National Archives"
        )
        item2 = models.EvidenceItem(
            source_type="press",
            publisher="Daily Newspaper"
        )
        
        items = [item1, item2]
        
        parsed = PropositionParsed(
            entities=[],
            time_window=TimeWindow(),
            geography=[],
            claim_type="diplomatic",
            ambiguity_terms=[],
            normalized_definitions={}
        )
        
        scored = await builder._score_evidence(items, parsed)
        
        # Primary source should have higher score
        assert scored[0].reliability_score > scored[1].reliability_score
        assert scored[0].reliability_factors["source_type_score"] == 1.0
        assert scored[1].reliability_factors["source_type_score"] == 0.4
    
    def test_get_institution_type(self, builder):
        """Test institution type detection."""
        # Test archive
        item = models.EvidenceItem(publisher="National Archives")
        assert builder._get_institution_type(item) == "archives"
        
        # Test university
        item = models.EvidenceItem(publisher="Oxford University Press")
        assert builder._get_institution_type(item) == "university_press"
        
        # Test unknown
        item = models.EvidenceItem(publisher="Unknown Publisher")
        assert builder._get_institution_type(item) == "unknown"
    
    def test_source_type_weights(self, builder):
        """Test source type weight constants."""
        assert builder.SOURCE_TYPE_WEIGHTS["primary"] == 1.0
        assert builder.SOURCE_TYPE_WEIGHTS["academic"] == 0.8
        assert builder.SOURCE_TYPE_WEIGHTS["secondary"] == 0.7
        assert builder.SOURCE_TYPE_WEIGHTS["memoir"] == 0.5
        assert builder.SOURCE_TYPE_WEIGHTS["press"] == 0.4


class TestBalanceProtocol:
    """Test balance protocol service."""
    
    @pytest.fixture
    def protocol(self):
        return BalanceProtocol()
    
    def test_check_minimum_balance_compliant(self, protocol):
        """Test MBR check with compliant evidence."""
        evidence = [
            models.EvidenceItem(country="TR", stance="pro", source_type="primary"),
            models.EvidenceItem(country="TR", stance="contra", source_type="press"),
            models.EvidenceItem(country="UK", stance="neutral", source_type="press"),
            models.EvidenceItem(country="FR", stance="neutral", source_type="academic"),
        ]
        
        result = protocol.check_minimum_balance("case-123", evidence)
        
        assert result.compliant is True
        assert len(result.missing_clusters) == 0
    
    def test_check_minimum_balance_non_compliant(self, protocol):
        """Test MBR check with non-compliant evidence."""
        evidence = [
            models.EvidenceItem(country="TR", stance="pro", source_type="primary"),
            # Missing TR press
            # Missing contra stance
            # Only 1 foreign country
        ]
        
        result = protocol.check_minimum_balance("case-123", evidence)
        
        assert result.compliant is False
        assert len(result.missing_clusters) > 0
    
    def test_check_minimum_balance_missing_tr_sources(self, protocol):
        """Test MBR check missing TR sources."""
        evidence = [
            models.EvidenceItem(country="UK", stance="pro", source_type="press"),
            models.EvidenceItem(country="FR", stance="contra", source_type="academic"),
        ]
        
        result = protocol.check_minimum_balance("case-123", evidence)
        
        assert result.compliant is False
        assert "tr_sources" in result.missing_clusters
    
    def test_apply_penalty(self, protocol):
        """Test confidence score penalty application."""
        original_score = 0.85
        penalized = protocol.apply_penalty(original_score)
        
        # Should reduce by MBR_PENALTY_PERCENTAGE (default 20%)
        expected = original_score * 0.8
        assert penalized == pytest.approx(expected, 0.01)
    
    def test_check_high_risk_claim_with_evidence(self, protocol):
        """Test high-risk claim check with primary evidence."""
        result = protocol.check_high_risk_claim(
            "Gizli işbirliği yapıldı",
            has_primary_evidence=True
        )
        
        assert result["is_high_risk"] is True
        assert result["confidence_cap"] is None  # No cap with evidence
    
    def test_check_high_risk_claim_without_evidence(self, protocol):
        """Test high-risk claim check without primary evidence."""
        result = protocol.check_high_risk_claim(
            "Gizli işbirliği yapıldı",
            has_primary_evidence=False
        )
        
        assert result["is_high_risk"] is True
        assert result["confidence_cap"] == 0.6  # 60% cap
        assert result["warning"] is not None
    
    def test_check_high_risk_claim_safe(self, protocol):
        """Test high-risk claim check with safe claim."""
        result = protocol.check_high_risk_claim(
            "Diplomatik görüşmeler yapıldı",
            has_primary_evidence=False
        )
        
        assert result["is_high_risk"] is False
        assert result["confidence_cap"] is None
    
    def test_classify_discourse_vs_event(self, protocol):
        """Test discourse vs event classification."""
        evidence = [
            models.EvidenceItem(source_type="press"),
            models.EvidenceItem(source_type="primary"),
            models.EvidenceItem(source_type="treaty"),
        ]
        
        result = protocol.classify_discourse_vs_event(evidence)
        
        assert len(result["discourse"]) == 1
        assert len(result["event"]) == 2
    
    def test_mbr_status_details(self, protocol):
        """Test MBR status details are populated correctly."""
        evidence = [
            models.EvidenceItem(country="TR", stance="pro", source_type="primary"),
            models.EvidenceItem(country="UK", stance="contra", source_type="press"),
        ]
        
        result = protocol.check_minimum_balance("case-123", evidence)
        
        assert "tr_count" in result.details
        assert "foreign_countries" in result.details
        assert "pro_count" in result.details
        assert "contra_count" in result.details
