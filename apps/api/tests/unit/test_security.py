import pytest
from datetime import datetime
from app.core.security import (
    verify_password, get_password_hash, create_access_token, 
    create_refresh_token, decode_token
)


class TestSecurity:
    """Test security utilities."""
    
    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        # Hash should be different from password
        assert hashed != password
        
        # Verification should succeed
        assert verify_password(password, hashed) is True
        
        # Wrong password should fail
        assert verify_password("wrongpassword", hashed) is False
    
    def test_access_token_creation(self):
        """Test JWT access token creation."""
        data = {"sub": "user-123"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_refresh_token_creation(self):
        """Test JWT refresh token creation."""
        data = {"sub": "user-123"}
        token = create_refresh_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_token_decode(self):
        """Test token decoding."""
        data = {"sub": "user-123"}
        token = create_access_token(data)
        decoded = decode_token(token)
        
        assert decoded is not None
        assert decoded["sub"] == "user-123"
        assert decoded["type"] == "access"
        assert "exp" in decoded
    
    def test_invalid_token_decode(self):
        """Test decoding invalid token."""
        decoded = decode_token("invalid.token.here")
        assert decoded is None
    
    def test_expired_token(self):
        """Test expired token handling."""
        from datetime import timedelta
        
        # Create token that expires immediately
        data = {"sub": "user-123"}
        token = create_access_token(data, expires_delta=timedelta(seconds=-1))
        decoded = decode_token(token)
        
        assert decoded is None
