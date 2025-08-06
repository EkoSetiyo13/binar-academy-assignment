import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

# Fix TestClient initialization
client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Todo List API"}

class TestListAPI:
    """Test suite for List API endpoints"""
    
    def setup_method(self):
        """Setup method to reset test data before each test"""
        # Clear any existing test data
        import os
        if os.path.exists("app/db/users.json"):
            os.remove("app/db/users.json")
        if os.path.exists("app/db/lists.json"):
            os.remove("app/db/lists.json")
        if os.path.exists("app/db/tasks.json"):
            os.remove("app/db/tasks.json")
        
        # Register and login a user for authentication
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        client.post("/api/auth/register", json=user_data)
        
        login_data = {
            "username": "testuser",
            "password": "password123"
        }
        login_response = client.post("/api/auth/login", json=login_data)
        self.token = login_response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    def test_create_list(self):
        """Test creating a list"""
        # Create a test list
        list_data = {
            "name": "Test List",
            "description": "A test list"
        }
        response = client.post("/api/lists", json=list_data, headers=self.headers)
        assert response.status_code == 201
        
        data = response.json()
        assert "id" in data
        assert data["name"] == "Test List"
        assert data["description"] == "A test list"
    
    def test_get_lists(self):
        """Test getting all lists"""
        # Create a test list
        list_data = {"name": "Test List For Getting"}
        response = client.post("/api/lists", json=list_data, headers=self.headers)
        list_id = response.json()["id"]
        
        # Get all lists
        response = client.get("/api/lists", headers=self.headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Find our created list
        created_list = None
        for lst in data:
            if lst["id"] == list_id:
                created_list = lst
                break
        
        assert created_list is not None
        assert created_list["name"] == "Test List For Getting"
    
    def test_get_list(self):
        """Test getting a specific list"""
        # Create a test list
        list_data = {"name": "Test List For Getting Single"}
        response = client.post("/api/lists", json=list_data, headers=self.headers)
        list_id = response.json()["id"]
        
        # Get the specific list
        response = client.get(f"/api/lists/{list_id}", headers=self.headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == list_id
        assert data["name"] == "Test List For Getting Single"
    
    def test_update_list(self):
        """Test updating a list"""
        # Create a test list
        list_data = {"name": "Original List Name"}
        response = client.post("/api/lists", json=list_data, headers=self.headers)
        list_id = response.json()["id"]
        
        # Update the list
        update_data = {
            "name": "Updated List Name",
            "description": "Updated description"
        }
        response = client.put(f"/api/lists/{list_id}", json=update_data, headers=self.headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Updated List Name"
        assert data["description"] == "Updated description"
    
    def test_delete_list(self):
        """Test deleting a list"""
        # Create a test list
        list_data = {"name": "List to Delete"}
        response = client.post("/api/lists", json=list_data, headers=self.headers)
        list_id = response.json()["id"]
        
        # Delete the list
        response = client.delete(f"/api/lists/{list_id}", headers=self.headers)
        assert response.status_code == 204
        
        # Verify the list is deleted
        response = client.get(f"/api/lists/{list_id}", headers=self.headers)
        assert response.status_code == 404
