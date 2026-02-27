import pytest
from datetime import date
from app.schemas import (
    CaseCreate, TimeWindow, CaseOptions, UserCreate,
    EvidenceItemResponse, ClaimResponse
)


class TestSchemas:
    """Test Pydantic schemas."""
    
    def test_case_create_valid(self):
        """Test valid case creation schema."""
        case = CaseCreate(
            proposition="Test historical proposition?",
            time_window=TimeWindow(start=date(1919, 1, 1), end=date(1923, 12, 31)),
            geography=["Turkey", "UK"],
            options=CaseOptions()
        )
        
        assert case.proposition == "Test historical proposition?"
        assert case.options.require_steel_man is True
    
    def test_case_create_minimal(self):
        """Test case creation with minimal data."""
        case = CaseCreate(proposition="This is a valid historical question?")
        
        assert case.proposition == "This is a valid historical question?"
        assert case.time_window is None
        assert case.options.require_steel_man is True
    
    def test_case_create_invalid_short_proposition(self):
        """Test case creation with too short proposition."""
        with pytest.raises(ValueError):
            CaseCreate(proposition="Short")
    
    def test_user_create_valid(self):
        """Test valid user creation schema."""
        user = UserCreate(email="test@example.com", password="password123")
        
        assert user.email == "test@example.com"
        assert user.password == "password123"
    
    def test_user_create_invalid_email(self):
        """Test user creation with invalid email."""
        with pytest.raises(ValueError):
            UserCreate(email="invalid-email", password="password123")
    
    def test_user_create_short_password(self):
        """Test user creation with short password."""
        with pytest.raises(ValueError):
            UserCreate(email="test@example.com", password="short")
    
    def test_evidence_response(self):
        """Test evidence response schema."""
        from uuid import uuid4
        
        evidence = EvidenceItemResponse(
            id=uuid4(),
            title="Test Evidence",
            source_type="primary",
            country="TR",
            language="tr",
            reliability_score=0.95
        )
        
        assert evidence.title == "Test Evidence"
        assert evidence.reliability_score == 0.95
    
    def test_claim_response(self):
        """Test claim response schema."""
        from uuid import uuid4
        
        claim = ClaimResponse(
            id=uuid4(),
            normalized_text="Test claim",
            category="diplomatic",
            stance="support",
            confidence_label="high",
            final_score=0.85,
            is_core_consensus=True,
            is_disputed=False
        )
        
        assert claim.normalized_text == "Test claim"
        assert claim.confidence_label == "high"
        assert claim.is_core_consensus is True
