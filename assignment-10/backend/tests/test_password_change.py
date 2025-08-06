import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

# Fix TestClient initialization
client = TestClient(app)

class TestPasswordChange:
    """Test suite for password change functionality"""
    
    def setup_method(self):
        """Setup method to reset test data before each test"""
        with patch('app.models.user_model.UserModel._load_users') as mock_load:
            mock_load.return_value = {}
    
    def test_change_password_success(self):
        """Test successful password change"""
        # Register user
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "oldpassword123"
        }
        client.post("/api/auth/register", json=user_data)
        
        # Login to get token
        login_data = {
            "username": "testuser",
            "password": "oldpassword123"
        }
        login_response = client.post("/api/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Change password
        change_data = {
            "current_password": "oldpassword123",
            "new_password": "newpassword123"
        }
        
        response = client.put("/api/auth/change-password", json=change_data, headers=headers)
        assert response.status_code == 200
        assert "Password changed successfully" in response.json()["message"]
        
        # Verify old password no longer works
        old_login_response = client.post("/api/auth/login", json=login_data)
        assert old_login_response.status_code == 401
        
        # Verify new password works
        new_login_data = {
            "username": "testuser",
            "password": "newpassword123"
        }
        new_login_response = client.post("/api/auth/login", json=new_login_data)
        assert new_login_response.status_code == 200
    
    def test_change_password_wrong_current_password(self):
        """Test password change with wrong current password"""
        # Register and login
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "oldpassword123"
        }
        client.post("/api/auth/register", json=user_data)
        
        login_data = {
            "username": "testuser",
            "password": "oldpassword123"
        }
        login_response = client.post("/api/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Try to change password with wrong current password
        change_data = {
            "current_password": "wrongpassword",
            "new_password": "newpassword123"
        }
        
        response = client.put("/api/auth/change-password", json=change_data, headers=headers)
        assert response.status_code == 400
        assert "Current password is incorrect" in response.json()["detail"]
    
    def test_change_password_weak_new_password(self):
        """Test password change with weak new password"""
        # Register and login
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "oldpassword123"
        }
        client.post("/api/auth/register", json=user_data)
        
        login_data = {
            "username": "testuser",
            "password": "oldpassword123"
        }
        login_response = client.post("/api/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Try to change to weak password
        change_data = {
            "current_password": "oldpassword123",
            "new_password": "123"
        }
        
        response = client.put("/api/auth/change-password", json=change_data, headers=headers)
        assert response.status_code == 422
    
    def test_change_password_without_authentication(self):
        """Test password change without authentication"""
        change_data = {
            "current_password": "oldpassword123",
            "new_password": "newpassword123"
        }
        
        response = client.put("/api/auth/change-password", json=change_data)
        assert response.status_code == 403
    
    def test_change_password_missing_fields(self):
        """Test password change with missing fields"""
        # Register and login
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "oldpassword123"
        }
        client.post("/api/auth/register", json=user_data)
        
        login_data = {
            "username": "testuser",
            "password": "oldpassword123"
        }
        login_response = client.post("/api/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Missing current_password
        change_data = {
            "new_password": "newpassword123"
        }
        
        response = client.put("/api/auth/change-password", json=change_data, headers=headers)
        assert response.status_code == 422
        
        # Missing new_password
        change_data = {
            "current_password": "oldpassword123"
        }
        
        response = client.put("/api/auth/change-password", json=change_data, headers=headers)
        assert response.status_code == 422
    
    def test_change_password_same_password(self):
        """Test password change with same password"""
        # Register and login
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "oldpassword123"
        }
        client.post("/api/auth/register", json=user_data)
        
        login_data = {
            "username": "testuser",
            "password": "oldpassword123"
        }
        login_response = client.post("/api/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Try to change to same password
        change_data = {
            "current_password": "oldpassword123",
            "new_password": "oldpassword123"
        }
        
        response = client.put("/api/auth/change-password", json=change_data, headers=headers)
        assert response.status_code == 400
        assert "New password must be different" in response.json()["detail"] 