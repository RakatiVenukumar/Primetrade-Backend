"""
User model for authentication and role-based access control.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.core import Base


class User(Base):
    """
    User table for PrimeTrade.
    
    Fields:
    - id: Primary key
    - email: Unique email address for login
    - password: Hashed password (bcrypt)
    - role: User role (user/admin)
    - created_at: Account creation timestamp
    """
    
    __tablename__ = "users"
    
    # ========================================================================
    # Columns
    # ========================================================================
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique email address for user login"
    )
    
    password = Column(
        String(255),
        nullable=False,
        comment="Bcrypt-hashed password"
    )
    
    role = Column(
        String(50),
        nullable=False,
        default="user",
        index=True,
        comment="User role: 'user' or 'admin'"
    )
    
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
        comment="Account creation timestamp"
    )
    
    # ========================================================================
    # Methods
    # ========================================================================
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
