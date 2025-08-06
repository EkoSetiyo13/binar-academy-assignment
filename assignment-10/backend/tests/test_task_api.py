import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from datetime import datetime, timedelta
import uuid

# Fix TestClient initialization
client = TestClient(app)

class TestTaskAPI:
    """Test suite for Task API endpoints"""
    
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
        
        # Create a test list for tasks
        list_data = {"name": "Task Test List"}
        response = client.post("/api/lists", json=list_data, headers=self.headers)
        self.list_id = response.json()["id"]
    
    def teardown_method(self):
        # Delete the test list
        client.delete(f"/api/lists/{self.list_id}", headers=self.headers)
    
    def test_add_task(self):
        """Test adding a task to a list"""
        task_data = {
            "title": "Test Task",
            "description": "A test task",
            "deadline": "2024-12-31T23:59:00"
        }
        
        response = client.post(f"/api/lists/{self.list_id}/tasks", json=task_data, headers=self.headers)
        assert response.status_code == 201
        
        data = response.json()
        assert "id" in data
        assert data["title"] == "Test Task"
        assert data["description"] == "A test task"
        assert data["completed"] == False
    
    def test_get_tasks(self):
        """Test getting all tasks from a list"""
        # Add a task first
        task_data = {
            "title": "Test Task for Getting",
            "description": "A test task for getting",
            "deadline": "2024-12-31T23:59:00"
        }
        client.post(f"/api/lists/{self.list_id}/tasks", json=task_data, headers=self.headers)
        
        # Get all tasks
        response = client.get(f"/api/lists/{self.list_id}/tasks", headers=self.headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_update_task(self):
        """Test updating a task"""
        # Add a task first
        task_data = {
            "title": "Original Task",
            "description": "Original description",
            "deadline": "2024-12-31T23:59:00"
        }
        response = client.post(f"/api/lists/{self.list_id}/tasks", json=task_data, headers=self.headers)
        task_id = response.json()["id"]
        
        # Update the task
        update_data = {
            "title": "Updated Task",
            "description": "Updated description",
            "completed": True
        }
        response = client.put(f"/api/lists/{self.list_id}/tasks/{task_id}", json=update_data, headers=self.headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == "Updated Task"
        assert data["description"] == "Updated description"
        assert data["completed"] == True
    
    def test_complete_task(self):
        """Test completing a task"""
        # Add a task first
        task_data = {
            "title": "Task to Complete",
            "description": "A task to complete",
            "deadline": "2024-12-31T23:59:00"
        }
        response = client.post(f"/api/lists/{self.list_id}/tasks", json=task_data, headers=self.headers)
        task_id = response.json()["id"]
        
        # Complete the task
        update_data = {"completed": True}
        response = client.put(f"/api/lists/{self.list_id}/tasks/{task_id}", json=update_data, headers=self.headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["completed"] == True
    
    def test_delete_task(self):
        """Test deleting a task"""
        # Add a task first
        task_data = {
            "title": "Task to Delete",
            "description": "A task to delete",
            "deadline": "2024-12-31T23:59:00"
        }
        response = client.post(f"/api/lists/{self.list_id}/tasks", json=task_data, headers=self.headers)
        task_id = response.json()["id"]
        
        # Delete the task
        response = client.delete(f"/api/lists/{self.list_id}/tasks/{task_id}", headers=self.headers)
        assert response.status_code == 204
        
        # Verify the task is deleted
        response = client.get(f"/api/lists/{self.list_id}/tasks/{task_id}", headers=self.headers)
        assert response.status_code == 404
    
    def test_get_tasks_due_this_week(self):
        """Test getting tasks due this week"""
        # Add a task with deadline this week
        from datetime import datetime, timedelta
        next_week = datetime.now() + timedelta(days=7)
        
        task_data = {
            "title": "Task Due This Week",
            "description": "A task due this week",
            "deadline": next_week.isoformat()
        }
        client.post(f"/api/lists/{self.list_id}/tasks", json=task_data, headers=self.headers)
        
        # Get tasks due this week
        response = client.get(f"/api/lists/{self.list_id}/tasks?due_this_week=true", headers=self.headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_tasks_ordered(self):
        """Test getting tasks ordered by deadline"""
        # Add multiple tasks with different deadlines
        task_data1 = {
            "title": "Task 1",
            "description": "First task",
            "deadline": "2024-12-31T23:59:00"
        }
        task_data2 = {
            "title": "Task 2",
            "description": "Second task",
            "deadline": "2024-12-30T23:59:00"
        }
        
        client.post(f"/api/lists/{self.list_id}/tasks", json=task_data1, headers=self.headers)
        client.post(f"/api/lists/{self.list_id}/tasks", json=task_data2, headers=self.headers)
        
        # Get tasks ordered by deadline
        response = client.get(f"/api/lists/{self.list_id}/tasks?ordered=true", headers=self.headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2
