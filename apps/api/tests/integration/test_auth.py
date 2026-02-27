import pytest
from httpx import AsyncClient


class TestAuth:
    """Test authentication endpoints."""
    
    async def test_register_success(self, client: AsyncClient):
        """Test successful user registration."""
        response = await client.post("/api/v1/auth/register", json={
            "email": "newuser@example.com",
            "password": "password123"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert "tier" in data
        assert data["tier"] == "free"
    
    async def test_register_duplicate_email(self, client: AsyncClient, test_user):
        """Test registration with duplicate email."""
        user_data, _ = test_user
        response = await client.post("/api/v1/auth/register", json={
            "email": user_data["email"],
            "password": "password123"
        })
        
        assert response.status_code == 422
        assert "already registered" in response.json()["error"].lower()
    
    async def test_register_invalid_email(self, client: AsyncClient):
        """Test registration with invalid email."""
        response = await client.post("/api/v1/auth/register", json={
            "email": "invalid-email",
            "password": "password123"
        })
        
        assert response.status_code == 422
    
    async def test_register_short_password(self, client: AsyncClient):
        """Test registration with short password."""
        response = await client.post("/api/v1/auth/register", json={
            "email": "test2@example.com",
            "password": "short"
        })
        
        assert response.status_code == 422
    
    async def test_login_success(self, client: AsyncClient, test_user):
        """Test successful login."""
        user_data, _ = test_user
        response = await client.post("/api/v1/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    async def test_login_invalid_credentials(self, client: AsyncClient):
        """Test login with invalid credentials."""
        response = await client.post("/api/v1/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        })
        
        assert response.status_code == 401
    
    async def test_get_current_user(self, client: AsyncClient, auth_headers):
        """Test getting current user info."""
        response = await client.get("/api/v1/auth/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert "id" in data
        assert "tier" in data
    
    async def test_get_current_user_no_auth(self, client: AsyncClient):
        """Test getting current user without authentication."""
        response = await client.get("/api/v1/auth/me")
        
        assert response.status_code == 401
    
    async def test_get_current_user_invalid_token(self, client: AsyncClient):
        """Test getting current user with invalid token."""
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid-token"}
        )
        
        assert response.status_code == 401
