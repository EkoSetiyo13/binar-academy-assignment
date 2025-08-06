from fastapi import APIRouter, Depends, HTTPException, status
from app.services.auth_service import AuthService
from app.schemas.auth_schema import UserCreate, UserLogin, UserResponse, Token, PasswordChange, PasswordChangeResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user"""
    return auth_service.register_user(user_data)

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """Login user and return access token"""
    return auth_service.login_user(user_data)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(auth_service.get_current_user)):
    """Get current user information"""
    return {
        "id": current_user["id"],
        "username": current_user["username"],
        "email": current_user["email"]
    }

@router.put("/change-password", response_model=PasswordChangeResponse)
async def change_password(
    password_data: PasswordChange,
    current_user: dict = Depends(auth_service.get_current_user)
):
    """Change user password"""
    return auth_service.change_password(current_user["username"], password_data) 