"""
Authentication router
"""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.middleware.rate_limit import rate_limit_auth_login, rate_limit_auth_register, rate_limit_get_endpoints
from app.middleware.validation import sanitize_string_input
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@rate_limit_auth_register()
async def register_user(
    request_data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
    request: Request = None,
):
    """
    Register a new user account.
    
    Args:
        request: User registration data
        db: Database session
        
    Returns:
        UserResponse: Created user information
        
    Raises:
        409: Email already registered
    """
    # Sanitize string inputs
    request_data.full_name = sanitize_string_input(request_data.full_name)
    request_data.organisation = sanitize_string_input(request_data.organisation)
    
    user = await AuthService.register_user(db, request_data)
    return UserResponse.from_orm(user)


@router.post("/login", response_model=TokenResponse)
@rate_limit_auth_login()
async def login_user(
    request_data: LoginRequest,
    db: AsyncSession = Depends(get_db),
    request: Request = None,
):
    """
    Authenticate user with email and password.
    
    Args:
        request: Login credentials
        db: Database session
        
    Returns:
        TokenResponse: Access token, refresh token, and user info
        
    Raises:
        401: Invalid credentials or inactive user
    """
    return await AuthService.login_user(db, request_data.email, request_data.password)


@router.post("/token", response_model=TokenResponse, include_in_schema=False)
@rate_limit_auth_login()
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    request: Request = None
):
    """
    OAuth2 compatible login endpoint for FastAPI docs.
    
    Args:
        form_data: OAuth2 form data (username=email, password)
        db: Database session
        
    Returns:
        TokenResponse: Access token, refresh token, and user info
    """
    return await AuthService.login_user(db, form_data.username, form_data.password)


@router.post("/refresh")
async def refresh_token(
    request: RefreshRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate new access token from refresh token.
    
    Args:
        request: Refresh token
        db: Database session
        
    Returns:
        dict: New access token
        
    Raises:
        401: Invalid or expired refresh token
    """
    return await AuthService.refresh_access_token(db, request.refresh_token)


@router.post("/logout")
async def logout_user(
    current_user: User = Depends(get_current_user)
):
    """
    Logout current user.
    
    Note: JWT tokens are stateless, so logout is handled client-side
    by removing the tokens. This endpoint exists for consistency.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        dict: Logout confirmation message
    """
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
@rate_limit_get_endpoints()
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    request: Request = None,
):
    """
    Get current user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserResponse: Current user information
    """
    return UserResponse.from_orm(current_user)
