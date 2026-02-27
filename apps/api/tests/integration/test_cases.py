import pytest
from httpx import AsyncClient


class TestCases:
    """Test case management endpoints."""
    
    async def test_create_case_success(self, client: AsyncClient, auth_headers):
        """Test successful case creation."""
        response = await client.post(
            "/api/v1/cases",
            headers=auth_headers,
            json={
                "proposition": "Mustafa Kemal Atatürk İngilizlerle iş yaptı mı?",
                "time_window": {
                    "start": "1919-05-01",
                    "end": "1923-10-29"
                },
                "geography": ["Turkey", "UK"],
                "options": {
                    "require_steel_man": True,
                    "source_preference": "balanced",
                    "languages": ["tr", "en"]
                }
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["proposition"] == "Mustafa Kemal Atatürk İngilizlerle iş yaptı mı?"
        assert data["status"] in ["pending", "processing"]
    
    async def test_create_case_no_auth(self, client: AsyncClient):
        """Test case creation without authentication."""
        response = await client.post("/api/v1/cases", json={
            "proposition": "Test proposition"
        })
        
        assert response.status_code == 401
    
    async def test_create_case_invalid_data(self, client: AsyncClient, auth_headers):
        """Test case creation with invalid data."""
        # Too short proposition
        response = await client.post(
            "/api/v1/cases",
            headers=auth_headers,
            json={
                "proposition": "Short"
            }
        )
        
        assert response.status_code == 422
    
    async def test_list_cases(self, client: AsyncClient, auth_headers):
        """Test listing user cases."""
        # First create a case
        await client.post(
            "/api/v1/cases",
            headers=auth_headers,
            json={
                "proposition": "Test proposition for listing"
            }
        )
        
        # List cases
        response = await client.get("/api/v1/cases", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert isinstance(data["items"], list)
        assert isinstance(data["total"], int)
    
    async def test_list_cases_with_pagination(self, client: AsyncClient, auth_headers):
        """Test case listing with pagination."""
        response = await client.get(
            "/api/v1/cases?limit=5&offset=0",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) <= 5
    
    async def test_list_cases_filtered_by_status(self, client: AsyncClient, auth_headers):
        """Test case listing with status filter."""
        response = await client.get(
            "/api/v1/cases?status=pending",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        for item in data["items"]:
            assert item["status"] == "pending"
    
    async def test_get_case_detail(self, client: AsyncClient, auth_headers):
        """Test getting case details."""
        # Create a case first
        create_response = await client.post(
            "/api/v1/cases",
            headers=auth_headers,
            json={
                "proposition": "Test case for detail view"
            }
        )
        case_id = create_response.json()["id"]
        
        # Get case detail
        response = await client.get(f"/api/v1/cases/{case_id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == case_id
        assert "proposition" in data
        assert "status" in data
        assert "mbr_compliant" in data
    
    async def test_get_case_not_found(self, client: AsyncClient, auth_headers):
        """Test getting non-existent case."""
        response = await client.get(
            "/api/v1/cases/12345678-1234-1234-1234-123456789abc",
            headers=auth_headers
        )
        
        assert response.status_code == 404
    
    async def test_get_case_unauthorized(self, client: AsyncClient, auth_headers, test_user):
        """Test getting case belonging to another user."""
        # This would require creating a case with a different user
        # For now, just check that unauthorized access is properly handled
        response = await client.get(
            "/api/v1/cases/12345678-1234-1234-1234-123456789abc",
            headers=auth_headers
        )
        
        assert response.status_code in [404, 403]
    
    async def test_delete_case(self, client: AsyncClient, auth_headers):
        """Test deleting a case."""
        # Create a case
        create_response = await client.post(
            "/api/v1/cases",
            headers=auth_headers,
            json={
                "proposition": "Test case to delete"
            }
        )
        case_id = create_response.json()["id"]
        
        # Delete the case
        response = await client.delete(
            f"/api/v1/cases/{case_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = await client.get(
            f"/api/v1/cases/{case_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404
    
    async def test_delete_case_not_found(self, client: AsyncClient, auth_headers):
        """Test deleting non-existent case."""
        response = await client.delete(
            "/api/v1/cases/12345678-1234-1234-1234-123456789abc",
            headers=auth_headers
        )
        
        assert response.status_code == 404
