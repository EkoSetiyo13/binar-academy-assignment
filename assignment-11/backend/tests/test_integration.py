import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

class TestIntegration:
    """Integration tests for end-to-end functionality"""
    
    def setup_method(self):
        """Setup method to reset test data before each test"""
        with patch('app.models.user_model.UserModel._load_users') as mock_load:
            mock_load.return_value = {}
    
    def test_full_application_flow(self):
        """Test complete application flow from registration to task management"""
        
        # 1. Register a new user
        user_data = {
            "username": "integrationuser",
            "email": "integration@example.com",
            "password": "password123"
        }
        
        register_response = client.post("/api/auth/register", json=user_data)
        assert register_response.status_code == 201
        
        # 2. Login and get token
        login_data = {
            "username": "integrationuser",
            "password": "password123"
        }
        
        login_response = client.post("/api/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Get current user info
        me_response = client.get("/api/auth/me", headers=headers)
        assert me_response.status_code == 200
        user_info = me_response.json()
        assert user_info["username"] == "integrationuser"
        
        # 4. Create a list
        list_data = {
            "name": "Integration Test List",
            "description": "A list for integration testing"
        }
        
        list_response = client.post("/api/lists/", json=list_data, headers=headers)
        assert list_response.status_code == 201
        
        list_id = list_response.json()["id"]
        
        # 5. Create a task in the list
        task_data = {
            "title": "Integration Test Task",
            "description": "A task for integration testing",
            "deadline": "2024-12-31T23:59:00"
        }
        
        task_response = client.post(f"/api/lists/{list_id}/tasks", json=task_data, headers=headers)
        assert task_response.status_code == 201
        
        task_id = task_response.json()["id"]
        
        # 6. Get all lists with tasks
        lists_response = client.get("/api/lists/", headers=headers)
        assert lists_response.status_code == 200
        
        lists = lists_response.json()
        assert len(lists) > 0
        
        # Find our created list
        created_list = None
        for lst in lists:
            if lst["id"] == list_id:
                created_list = lst
                break
        
        assert created_list is not None
        assert created_list["name"] == "Integration Test List"
        assert len(created_list["tasks"]) == 1
        
        # 7. Update the task
        update_task_data = {
            "title": "Updated Integration Test Task",
            "description": "Updated task description",
            "completed": True
        }
        
        update_response = client.put(f"/api/lists/{list_id}/tasks/{task_id}", json=update_task_data, headers=headers)
        assert update_response.status_code == 200
        
        # 8. Get the updated task
        get_task_response = client.get(f"/api/lists/{list_id}/tasks/{task_id}", headers=headers)
        assert get_task_response.status_code == 200
        
        updated_task = get_task_response.json()
        assert updated_task["title"] == "Updated Integration Test Task"
        assert updated_task["completed"] == True
        
        # 9. Delete the task
        delete_task_response = client.delete(f"/api/lists/{list_id}/tasks/{task_id}", headers=headers)
        assert delete_task_response.status_code == 204
        
        # 10. Verify task is deleted
        get_deleted_task_response = client.get(f"/api/lists/{list_id}/tasks/{task_id}", headers=headers)
        assert get_deleted_task_response.status_code == 404
        
        # 11. Delete the list
        delete_list_response = client.delete(f"/api/lists/{list_id}", headers=headers)
        assert delete_list_response.status_code == 204
        
        # 12. Verify list is deleted
        get_deleted_list_response = client.get(f"/api/lists/{list_id}", headers=headers)
        assert get_deleted_list_response.status_code == 404
    
    def test_authentication_flow_with_password_change(self):
        """Test authentication flow including password change"""
        
        # 1. Register user
        user_data = {
            "username": "passworduser",
            "email": "password@example.com",
            "password": "oldpassword123"
        }
        
        register_response = client.post("/api/auth/register", json=user_data)
        assert register_response.status_code == 201
        
        # 2. Login with old password
        login_data = {
            "username": "passworduser",
            "password": "oldpassword123"
        }
        
        login_response = client.post("/api/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Change password
        change_password_data = {
            "current_password": "oldpassword123",
            "new_password": "newpassword123"
        }
        
        change_response = client.put("/api/auth/change-password", json=change_password_data, headers=headers)
        assert change_response.status_code == 200
        
        # 4. Try to login with old password (should fail)
        old_login_response = client.post("/api/auth/login", json=login_data)
        assert old_login_response.status_code == 401
        
        # 5. Login with new password (should succeed)
        new_login_data = {
            "username": "passworduser",
            "password": "newpassword123"
        }
        
        new_login_response = client.post("/api/auth/login", json=new_login_data)
        assert new_login_response.status_code == 200
    
    def test_error_handling_integration(self):
        """Test error handling in integration scenarios"""
        
        # 1. Try to access protected endpoint without authentication
        lists_response = client.get("/api/lists/")
        assert lists_response.status_code == 403
        
        # 2. Try to access with invalid token
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        invalid_response = client.get("/api/lists/", headers=invalid_headers)
        assert invalid_response.status_code == 401
        
        # 3. Register user and test invalid operations
        user_data = {
            "username": "erroruser",
            "email": "error@example.com",
            "password": "password123"
        }
        
        client.post("/api/auth/register", json=user_data)
        
        login_data = {
            "username": "erroruser",
            "password": "password123"
        }
        
        login_response = client.post("/api/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 4. Try to access non-existent resource
        non_existent_response = client.get("/api/lists/non-existent-id", headers=headers)
        assert non_existent_response.status_code == 404
        
        # 5. Try to create task in non-existent list
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "deadline": "2024-12-31T23:59:00"
        }
        
        non_existent_task_response = client.post("/api/lists/non-existent-id/tasks", json=task_data, headers=headers)
        assert non_existent_task_response.status_code == 404
    
    def test_concurrent_operations(self):
        """Test concurrent operations on the same resources"""
        
        # 1. Register multiple users
        users = []
        for i in range(3):
            user_data = {
                "username": f"concurrentuser{i}",
                "email": f"concurrent{i}@example.com",
                "password": "password123"
            }
            
            register_response = client.post("/api/auth/register", json=user_data)
            assert register_response.status_code == 201
            
            login_data = {
                "username": f"concurrentuser{i}",
                "password": "password123"
            }
            
            login_response = client.post("/api/auth/login", json=login_data)
            assert login_response.status_code == 200
            
            users.append({
                "username": f"concurrentuser{i}",
                "token": login_response.json()["access_token"]
            })
        
        # 2. Each user creates a list simultaneously
        lists = []
        for user in users:
            headers = {"Authorization": f"Bearer {user['token']}"}
            list_data = {
                "name": f"List by {user['username']}",
                "description": f"List created by {user['username']}"
            }
            
            list_response = client.post("/api/lists/", json=list_data, headers=headers)
            assert list_response.status_code == 201
            lists.append(list_response.json()["id"])
        
        # 3. Each user creates tasks in their lists
        for i, user in enumerate(users):
            headers = {"Authorization": f"Bearer {user['token']}"}
            task_data = {
                "title": f"Task by {user['username']}",
                "description": f"Task created by {user['username']}",
                "deadline": "2024-12-31T23:59:00"
            }
            
            task_response = client.post(f"/api/lists/{lists[i]}/tasks", json=task_data, headers=headers)
            assert task_response.status_code == 201
        
        # 4. Verify each user can only see their own lists
        for i, user in enumerate(users):
            headers = {"Authorization": f"Bearer {user['token']}"}
            lists_response = client.get("/api/lists/", headers=headers)
            assert lists_response.status_code == 200
            
            user_lists = lists_response.json()
            assert len(user_lists) >= 1  # At least their own list
    
    def test_data_persistence(self):
        """Test that data persists across requests"""
        
        # 1. Register and login user
        user_data = {
            "username": "persistenceuser",
            "email": "persistence@example.com",
            "password": "password123"
        }
        
        client.post("/api/auth/register", json=user_data)
        
        login_data = {
            "username": "persistenceuser",
            "password": "password123"
        }
        
        login_response = client.post("/api/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Create a list
        list_data = {
            "name": "Persistence Test List",
            "description": "Testing data persistence"
        }
        
        list_response = client.post("/api/lists/", json=list_data, headers=headers)
        assert list_response.status_code == 201
        list_id = list_response.json()["id"]
        
        # 3. Create multiple tasks
        tasks = []
        for i in range(5):
            task_data = {
                "title": f"Task {i}",
                "description": f"Description for task {i}",
                "deadline": "2024-12-31T23:59:00"
            }
            
            task_response = client.post(f"/api/lists/{list_id}/tasks", json=task_data, headers=headers)
            assert task_response.status_code == 201
            tasks.append(task_response.json()["id"])
        
        # 4. Verify all tasks are persisted
        list_detail_response = client.get(f"/api/lists/{list_id}", headers=headers)
        assert list_detail_response.status_code == 200
        
        list_detail = list_detail_response.json()
        assert len(list_detail["tasks"]) == 5
        
        # 5. Update some tasks
        for i, task_id in enumerate(tasks[:3]):
            update_data = {
                "title": f"Updated Task {i}",
                "completed": True
            }
            
            update_response = client.put(f"/api/lists/{list_id}/tasks/{task_id}", json=update_data, headers=headers)
            assert update_response.status_code == 200
        
        # 6. Verify updates are persisted
        updated_list_response = client.get(f"/api/lists/{list_id}", headers=headers)
        assert updated_list_response.status_code == 200
        
        updated_list = updated_list_response.json()
        completed_tasks = [task for task in updated_list["tasks"] if task["completed"]]
        assert len(completed_tasks) == 3 