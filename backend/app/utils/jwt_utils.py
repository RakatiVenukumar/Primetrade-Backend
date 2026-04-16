"""
JWT (JSON Web Token) utilities for authentication.
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt

# ============================================================================
# JWT Configuration
# ============================================================================

# Secret key for signing tokens (use environment variable in production)
# Generate secure key: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "your-secret-key-change-in-production-use-env-var"
)

# JWT algorithm
ALGORITHM = "HS256"

# Token expiry time (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Validation
if SECRET_KEY == "your-secret-key-change-in-production-use-env-var":
    import warnings
    warnings.warn(
        "WARNING: Using default SECRET_KEY. Set SECRET_KEY environment "
        "variable in production for security!"
    )


# ============================================================================
# Token Functions
# ============================================================================

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        data (Dict[str, Any]): The claims to encode in the token.
                               Typically: {"sub": user_id, "email": user_email}
        expires_delta (Optional[timedelta]): Custom token expiry. 
                                            If None, uses ACCESS_TOKEN_EXPIRE_MINUTES.
    
    Returns:
        str: Encoded JWT token as string.
    
    Example:
        token = create_access_token(
            data={"sub": "1", "email": "user@example.com"}
        )
        # Returns: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    """
    to_encode = data.copy()
    
    # Set token expiry
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Encode token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode a JWT token.
    
    Args:
        token (str): The JWT token string to verify.
    
    Returns:
        Optional[Dict[str, Any]]: Dictionary of token claims if valid, None if invalid.
    
    Example:
        payload = verify_token(token)
        if payload:
            user_id = payload.get("sub")
            email = payload.get("email")
        else:
            print("Invalid token")
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        # Token is invalid (expired, tampered, wrong signature, etc.)
        return None


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode a token and raise exception if invalid.
    Use this when you want to catch JWT errors explicitly.
    
    Args:
        token (str): The JWT token string to decode.
    
    Returns:
        Dict[str, Any]: Dictionary of token claims.
    
    Raises:
        JWTError: If token is invalid, expired, or tampered.
    
    Example:
        try:
            payload = decode_token(token)
            user_id = payload.get("sub")
        except JWTError:
            print("Invalid token")
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


# ============================================================================
# Info Functions
# ============================================================================

def get_jwt_config() -> Dict[str, Any]:
    """Return JWT configuration info (for debugging/logging)."""
    return {
        "algorithm": ALGORITHM,
        "expire_minutes": ACCESS_TOKEN_EXPIRE_MINUTES,
        "secret_key_set": bool(os.getenv("SECRET_KEY")),
    }
