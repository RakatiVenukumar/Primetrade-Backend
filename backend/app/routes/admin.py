"""
Admin-only routes for user management and role-based access control.
Requires authenticated user with 'admin' role.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core import get_db
from app.core.dependencies import get_current_admin
from app.models import User
from app.schemas import UserResponse

# ============================================================================
# Router Setup
# ============================================================================

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["Admin"],
    responses={
        401: {"description": "Unauthorized (invalid or missing token)"},
        403: {"description": "Forbidden (user is not admin)"},
        404: {"description": "Not Found (user does not exist)"},
        500: {"description": "Internal Server Error"},
    }
)


# ============================================================================
# Admin Routes (requires admin role)
# ============================================================================

@router.get(
    "/users",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="List all users (admin only)",
    description="Retrieve list of all users. Requires admin role."
)
def list_users(
    current_admin: UserResponse = Depends(get_current_admin),
    db: Session = Depends(get_db)
) -> List[UserResponse]:
    """
    Get all users in the system.
    
    Only accessible to users with admin role.
    
    Returns:
    - List of all users with their id, email, role, and created_at
    """
    users = db.query(User).all()
    return users


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID (admin only)",
    description="Retrieve a specific user by ID. Requires admin role."
)
def get_user_by_id(
    user_id: int,
    current_admin: UserResponse = Depends(get_current_admin),
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Get a specific user by their ID.
    
    Only accessible to users with admin role.
    
    Parameters:
    - user_id: The ID of the user to retrieve
    
    Returns:
    - User object if found
    - 404 Not Found if user doesn't exist
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    return user


@router.put(
    "/users/{user_id}/role",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update user role (admin only)",
    description="Change a user's role (promote or demote). Requires admin role."
)
def update_user_role(
    user_id: int,
    new_role: str,
    current_admin: UserResponse = Depends(get_current_admin),
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Update a user's role.
    
    Only accessible to users with admin role.
    Only allows roles: 'user' or 'admin'
    
    Parameters:
    - user_id: The ID of the user to update
    - new_role: The new role ('user' or 'admin')
    
    Returns:
    - Updated user object
    - 400 Bad Request if invalid role
    - 404 Not Found if user doesn't exist
    """
    
    # Validate role
    if new_role not in ["user", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Must be 'user' or 'admin'"
        )
    
    # Find user
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # Prevent self-demotion (optional: can be removed if desired)
    if user.id == current_admin.id and new_role == "user":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot demote yourself from admin role"
        )
    
    # Update role
    user.role = new_role
    db.commit()
    db.refresh(user)
    
    return user


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user account (admin only)",
    description="Delete a user account permanently. Requires admin role."
)
def delete_user(
    user_id: int,
    current_admin: UserResponse = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Delete a user account.
    
    Only accessible to users with admin role.
    
    Parameters:
    - user_id: The ID of the user to delete
    
    Returns:
    - 204 No Content on success
    - 404 Not Found if user doesn't exist
    """
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # Prevent self-deletion
    if user.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    db.delete(user)
    db.commit()
    
    return None
