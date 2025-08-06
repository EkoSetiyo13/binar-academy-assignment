from fastapi import APIRouter, Depends, HTTPException, status
from app.services.auth_service import AuthService
from app.schemas.auth_schema import UserCreate, UserLogin, UserResponse, Token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Initialize auth service
auth_service = AuthService()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user
    
    - **username**: Unique username for the account
    - **email**: Valid email address
    - **password**: Secure password (minimum 6 characters)
    """
    try:
        user = auth_service.register_user(user_data)
        return UserResponse(
            id=user["id"],
            username=user["username"],
            email=user["email"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """
    Login user and get access token
    
    - **username**: Username for authentication
    - **password**: User password
    """
    try:
        result = auth_service.login_user(user_data)
        return Token(
            access_token=result["access_token"],
            token_type=result["token_type"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(auth_service.get_current_user)):
    """
    Get current user information
    
    Requires authentication via Bearer token
    """
    return UserResponse(
        id=current_user["id"],
        username=current_user["username"],
        email=current_user["email"]
    ) 