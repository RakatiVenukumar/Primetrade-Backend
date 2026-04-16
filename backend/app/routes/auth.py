"""
Authentication routes for user registration and login.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from app.utils import hash_password, verify_password, create_access_token
from app.core.dependencies import get_current_user

# ============================================================================
# Router Setup
# ============================================================================

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
    responses={
        400: {"description": "Bad Request"},
        409: {"description": "Conflict (email already exists)"},
        401: {"description": "Unauthorized (invalid credentials)"},
        500: {"description": "Internal Server Error"},
    }
)


# ============================================================================
# Registration Route
# ============================================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password"
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Register a new user.
    
    - **email**: Must be a valid, unique email address
    - **password**: Minimum 8 characters
    
    Returns:
    - User object with id, email, role, and created_at
    - Password hash is never returned
    """
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{user_data.email}' is already registered"
        )
    
    try:
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Create new user
        new_user = User(
            email=user_data.email,
            password=hashed_password,
            role="user"  # Default role
        )
        
        # Save to database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
        
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{user_data.email}' is already registered"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user"
        )


# ============================================================================
# Login Route
# ============================================================================

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="User login",
    description="Authenticate user and return JWT access token"
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """
    Login with email and password.
    
    - **email**: Registered email address
    - **password**: User password
    
    Returns:
    - JWT access token
    - Token type (bearer)
    - User information
    """
    
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    # Verify user exists and password is correct
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Create JWT token
    try:
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": user.role
            }
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.from_orm(user)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate authentication token"
        )


# ============================================================================
# Protected Routes (require authentication)
# ============================================================================

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="Get the authenticated user's profile using JWT token"
)
def get_profile(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """
    Get the current authenticated user's profile.

    Requires valid JWT token in Authorization header.

    Returns:
    - Current user information
    """
    return current_user
