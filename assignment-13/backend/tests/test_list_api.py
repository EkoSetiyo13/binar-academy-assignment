import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Todo List API is running" in response.json()["message"]

class TestListAPI:
    def test_create_list(self):
        # Create a test list
        list_data = {
            "name": "Test List",
            "description": "A test list"
        }
        response = client.post("/api/lists", json=list_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == list_data["name"]
        assert data["description"] == list_data["description"]
        assert "id" in data
        
        # Clean up - delete the created list
        list_id = data["id"]
        client.delete(f"/api/lists/{list_id}")

    def test_get_lists(self):
        # Create a test list
        list_data = {"name": "Test List For Getting"}
        response = client.post("/api/lists", json=list_data)
        list_id = response.json()["id"]
        
        # Get all lists
        response = client.get("/api/lists")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        
        # Clean up
        client.delete(f"/api/lists/{list_id}")

    def test_get_list(self):
        # Create a test list
        list_data = {"name": "Test List For Getting Single"}
        response = client.post("/api/lists", json=list_data)
        list_id = response.json()["id"]
        
        # Get the specific list
        response = client.get(f"/api/lists/{list_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == list_id
        assert data["name"] == list_data["name"]
        
        # Clean up
        client.delete(f"/api/lists/{list_id}")

    def test_update_list(self):
        # Create a test list
        list_data = {"name": "Original List Name"}
        response = client.post("/api/lists", json=list_data)
        list_id = response.json()["id"]
        
        # Update the list
        update_data = {"name": "Updated List Name"}
        response = client.put(f"/api/lists/{list_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        
        # Clean up
        client.delete(f"/api/lists/{list_id}")

    def test_delete_list(self):
        # Create a test list
        list_data = {"name": "List to Delete"}
        response = client.post("/api/lists", json=list_data)
        list_id = response.json()["id"]
        
        # Delete the list
        response = client.delete(f"/api/lists/{list_id}")
        assert response.status_code == 204
        
        # Confirm it's deleted
        response = client.get(f"/api/lists/{list_id}")
        assert response.status_code == 404
