"""
Dependency injection functions for FastAPI routes.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from jose import JWTError
 
from app.models import User
from app.core.config import get_db
from app.schemas import UserResponse
from app.utils import verify_token

# ============================================================================
# Security Scheme
# ============================================================================

# HTTP Bearer token scheme for API documentation
security = HTTPBearer(description="JWT Bearer token")


# ============================================================================
# Current User Dependency
# ============================================================================

def get_current_user(
    credentials: Optional[dict] = Depends(security),
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Dependency injection function to get the current authenticated user.
    
    Extracts and validates the JWT token from the Authorization header,
    then loads and returns the corresponding User from the database.
    
    Usage in routes:
        @router.get("/me")
        def get_profile(current_user: UserResponse = Depends(get_current_user)):
            return current_user
    
    Args:
        credentials (HTTPAuthenticationCredentials): Bearer token from Authorization header
        db (Session): Database session
    
    Returns:
        UserResponse: The authenticated user
    
    Raises:
        HTTPException 401: If token is missing, invalid, or user not found
        HTTPException 403: If token is expired
    """
    
    # Check if credentials are provided
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = credentials.credentials
    
    # Verify JWT token
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Extract user ID from token
    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Load user from database
    try:
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return UserResponse.model_validate(user)
        
    except (ValueError, JWTError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )


def get_current_admin(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """
    Dependency injection function to verify the current user is an admin.
    
    Usage in routes (admin-only endpoints):
        @router.delete("/users/{user_id}")
        def delete_user(
            user_id: int,
            current_admin: UserResponse = Depends(get_current_admin)
        ):
            # Only admins can reach here
            return {"message": "User deleted"}
    
    Args:
        current_user (UserResponse): The current authenticated user (from get_current_user)
    
    Returns:
        UserResponse: The admin user
    
    Raises:
        HTTPException 403: If user is not an admin
    """
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user
