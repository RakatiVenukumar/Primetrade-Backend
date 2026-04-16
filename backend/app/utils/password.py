"""
Password hashing and verification utilities using bcrypt.
"""

import bcrypt

# ============================================================================
# Password Hashing Functions
# ============================================================================

def hash_password(plain_password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    
    Args:
        plain_password (str): The plain text password to hash.
    
    Returns:
        str: The bcrypt hashed password (format: $2b$12$...).
    
    Note:
        Bcrypt cost factor is set to 12 for optimal security/performance balance.
        Cost factor determines computational cost: higher = slower but more secure.
    
    Example:
        hashed = hash_password("my_secret_password")
        print(hashed)  # $2b$12$JNXeGz.MXzLEqJ...
    
    Raises:
        ValueError: If password is empty.
    """
    if not plain_password:
        raise ValueError("Password cannot be empty")
    
    # Encode password to bytes for bcrypt
    password_bytes = plain_password.encode('utf-8')
    
    # Bcrypt has a 72-byte limit. Truncate if longer.
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Generate salt and hash password in one step
    # Cost factor 12: good balance between security and performance
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a bcrypt hash.
    
    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The bcrypt hash to verify against.
    
    Returns:
        bool: True if password matches the hash, False otherwise.
    
    Example:
        hashed = hash_password("my_password")
        is_valid = verify_password("my_password", hashed)  # True
        is_valid = verify_password("wrong_password", hashed)  # False
    """
    if not plain_password or not hashed_password:
        return False
    
    try:
        # Encode inputs to bytes
        password_bytes = plain_password.encode('utf-8')
        hash_bytes = hashed_password.encode('utf-8')
        
        # Bcrypt truncates passwords at 72 bytes - apply same logic on verify
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        
        # Use bcrypt.checkpw for verification
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except Exception:
        # If verification fails due to invalid hash format or other error, return False
        return False
