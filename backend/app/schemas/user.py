"""
Pydantic schemas for User validation and API responses.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# ============================================================================
# User Request Schemas
# ============================================================================

class UserCreate(BaseModel):
    """
    Schema for user registration request.
    
    Validates:
    - Email: Must be a valid email address
    - Password: Minimum 8 characters, maximum 100 characters
    """
    
    email: EmailStr = Field(..., description="User email address (must be unique)")
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password (min 8 chars, max 100 chars)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepass123"
            }
        }


class UserLogin(BaseModel):
    """
    Schema for user login request.
    
    Validates:
    - Email: Must be a valid email address
    - Password: Any non-empty string (actual validation on login)
    """
    
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=1, description="User password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepass123"
            }
        }


# ============================================================================
# User Response Schemas
# ============================================================================

class UserResponse(BaseModel):
    """
    Schema for user data in API responses.
    
    Excludes sensitive fields like password.
    """
    
    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email address")
    role: str = Field(..., description="User role (user or admin)")
    created_at: datetime = Field(..., description="Account creation timestamp")
    
    class Config:
        from_attributes = True  # Pydantic v2 ORM mode
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "role": "user",
                "created_at": "2026-04-16T10:30:00"
            }
        }


class TokenResponse(BaseModel):
    """
    Schema for JWT authentication response.
    """
    
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer')")
    user: UserResponse = Field(..., description="Authenticated user information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": 1,
                    "email": "user@example.com",
                    "role": "user",
                    "created_at": "2026-04-16T10:30:00"
                }
            }
        }
