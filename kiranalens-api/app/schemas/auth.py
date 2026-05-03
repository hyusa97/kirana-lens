"""
Authentication Pydantic schemas
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole


class RegisterRequest(BaseModel):
    """User registration request schema"""
    name: str = Field(..., min_length=2, max_length=200, description="Full name")
    email: EmailStr = Field(..., description="Email address")
    organisation: Optional[str] = Field(None, max_length=200, description="Organisation name")
    password: str = Field(..., min_length=8, max_length=100, description="Password (min 8 characters)")
    role: UserRole = Field(UserRole.CREDIT_OFFICER, description="User role")


class LoginRequest(BaseModel):
    """User login request schema"""
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password")


class UserResponse(BaseModel):
    """User response schema"""
    id: UUID
    email: str
    name: str
    organisation: Optional[str]
    role: UserRole
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshRequest(BaseModel):
    """Token refresh request schema"""
    refresh_token: str = Field(..., description="Refresh token")


class TokenData(BaseModel):
    """Token data schema for JWT payload"""
    user_id: Optional[str] = None
    email: Optional[str] = None