from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    email: str = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="User password (minimum 6 characters)")

class UserLogin(BaseModel):
    username: str = Field(..., description="Username for login")
    password: str = Field(..., description="User password")

class UserInDB(UserBase):
    id: str
    hashed_password: str

class UserResponse(UserBase):
    id: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=6, description="New password (minimum 6 characters)")

class PasswordChangeResponse(BaseModel):
    message: str
