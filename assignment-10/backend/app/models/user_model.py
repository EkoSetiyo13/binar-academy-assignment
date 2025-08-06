import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__default_rounds=12)

class UserModel:
    def __init__(self):
        self.users_file = "app/db/users.json"
        self.users = self._load_users()
        self._create_default_admin()

    def _load_users(self) -> Dict[str, Any]:
        """Load users from JSON file"""
        import json
        import os
        
        if not os.path.exists(self.users_file):
            # Create default admin user
            default_users = {
                "admin": {
                    "id": "admin",
                    "username": "admin",
                    "email": "admin@example.com",
                    "hashed_password": pwd_context.hash("admin123"),
                    "created_at": datetime.now().isoformat()
                }
            }
            self._save_users(default_users)
            return default_users
        
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_users(self, users: Dict[str, Any]) -> None:
        """Save users to JSON file"""
        import json
        import os
        
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)

    def _create_default_admin(self):
        """Create default admin user if no users exist"""
        if not self.users:
            admin_user = {
                "id": str(uuid.uuid4()),
                "username": "admin",
                "email": "admin@example.com",
                "hashed_password": self.get_password_hash("admin123"),
                "created_at": datetime.utcnow().isoformat()
            }
            self.users[admin_user["username"]] = admin_user
            self._save_users(self.users)

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        return self.users.get(username)
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        for user in self.users.values():
            if user.get("email") == email:
                return user
        return None
    
    def create_user(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Create a new user"""
        hashed_password = self.get_password_hash(password)
        user = {
            "id": str(uuid.uuid4()),
            "username": username,
            "email": email,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.users[username] = user
        self._save_users(self.users)
        return user
    
    def update_user_password(self, username: str, new_hashed_password: str):
        """Update user password"""
        if username in self.users:
            self.users[username]["hashed_password"] = new_hashed_password
            self.users[username]["updated_at"] = datetime.utcnow().isoformat()
            self._save_users(self.users)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password) 