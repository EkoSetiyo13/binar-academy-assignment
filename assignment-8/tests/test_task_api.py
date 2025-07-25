import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta
import uuid

client = TestClient(app)

class TestTaskAPI:
    def setup_method(self):
        # Create a test list for tasks
        list_data = {"name": "Task Test List"}
        response = client.post("/api/lists", json=list_data)
        self.list_id = response.json()["id"]
    
    def teardown_method(self):
        # Delete the test list
        client.delete(f"/api/lists/{self.list_id}")
    
    def test_add_task(self):
        # Add a task to the list
        task_data = {
            "title": "Test Task",
            "description": "A test task",
            "deadline": (datetime.now() + timedelta(days=1)).isoformat()
        }
        response = client.post(f"/api/lists/{self.list_id}/tasks", json=task_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert "id" in data
        assert data["completed"] == False
        
        # Clean up
        task_id = data["id"]
        client.delete(f"/api/lists/{self.list_id}/tasks/{task_id}")
    
    def test_get_tasks(self):
        # Add a task
        task_data = {"title": "Task for Getting"}
        response = client.post(f"/api/lists/{self.list_id}/tasks", json=task_data)
        task_id = response.json()["id"]
        
        # Get all tasks in the list
        response = client.get(f"/api/lists/{self.list_id}/tasks")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        
        # Clean up
        client.delete(f"/api/lists/{self.list_id}/tasks/{task_id}")
    
    def test_update_task(self):
        # Add a task
        task_data = {"title": "Original Task"}
        response = client.post(f"/api/lists/{self.list_id}/tasks", json=task_data)
        task_id = response.json()["id"]
        
        # Update the task
        update_data = {
            "title": "Updated Task",
            "description": "Updated description"
        }
        response = client.put(f"/api/lists/{self.list_id}/tasks/{task_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]
        
        # Clean up
        client.delete(f"/api/lists/{self.list_id}/tasks/{task_id}")
    
    def test_complete_task(self):
        # Add a task
        task_data = {"title": "Task to Complete"}
        response = client.post(f"/api/lists/{self.list_id}/tasks", json=task_data)
        task_id = response.json()["id"]
        
        # Toggle completion
        response = client.patch(f"/api/lists/{self.list_id}/tasks/{task_id}/complete")
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] == True
        
        # Toggle back
        response = client.patch(f"/api/lists/{self.list_id}/tasks/{task_id}/complete")
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] == False
        
        # Clean up
        client.delete(f"/api/lists/{self.list_id}/tasks/{task_id}")
    
    def test_delete_task(self):
        # Add a task
        task_data = {"title": "Task to Delete"}
        response = client.post(f"/api/lists/{self.list_id}/tasks", json=task_data)
        task_id = response.json()["id"]
        
        # Delete the task
        response = client.delete(f"/api/lists/{self.list_id}/tasks/{task_id}")
        assert response.status_code == 204
        
        # Confirm it's deleted
        response = client.get(f"/api/lists/{self.list_id}/tasks/{task_id}")
        assert response.status_code == 404
    
    def test_get_tasks_due_this_week(self):
        # Add a task due this week
        task_data = {
            "title": "Due This Week",
            "deadline": (datetime.now() + timedelta(days=2)).isoformat()
        }
        response = client.post(f"/api/lists/{self.list_id}/tasks", json=task_data)
        this_week_task_id = response.json()["id"]
        
        # Add a task due next month
        task_data = {
            "title": "Due Next Month",
            "deadline": (datetime.now() + timedelta(days=30)).isoformat()
        }
        response = client.post(f"/api/lists/{self.list_id}/tasks", json=task_data)
        next_month_task_id = response.json()["id"]
        
        # Get tasks due this week
        response = client.get("/api/tasks/due-this-week")
        assert response.status_code == 200
        tasks = response.json()
        assert isinstance(tasks, list)
        
        # Check that our task is in the results
        due_this_week_titles = [task["title"] for task in tasks]
        assert "Due This Week" in due_this_week_titles
        
        # Clean up
        client.delete(f"/api/lists/{self.list_id}/tasks/{this_week_task_id}")
        client.delete(f"/api/lists/{self.list_id}/tasks/{next_month_task_id}")
    
    def test_get_tasks_ordered(self):
        # Add tasks with different deadlines
        task1_data = {
            "title": "Task Due Later",
            "deadline": (datetime.now() + timedelta(days=5)).isoformat()
        }
        response = client.post(f"/api/lists/{self.list_id}/tasks", json=task1_data)
        task1_id = response.json()["id"]
        
        task2_data = {
            "title": "Task Due Soon",
            "deadline": (datetime.now() + timedelta(days=1)).isoformat()
        }
        response = client.post(f"/api/lists/{self.list_id}/tasks", json=task2_data)
        task2_id = response.json()["id"]
        
        # Get ordered tasks
        response = client.get(f"/api/lists/{self.list_id}/tasks/ordered")
        assert response.status_code == 200
        tasks = response.json()
        
        # Check order (first task should be the one due sooner)
        assert tasks[0]["title"] == "Task Due Soon"
        assert tasks[1]["title"] == "Task Due Later"
        
        # Clean up
        client.delete(f"/api/lists/{self.list_id}/tasks/{task1_id}")
        client.delete(f"/api/lists/{self.list_id}/tasks/{task2_id}")
