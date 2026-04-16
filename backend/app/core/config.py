"""
Database configuration and connection management.
Defaults to SQLite for local development and supports PostgreSQL when configured.
"""

import os
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# ============================================================================
# Environment Variables
# ============================================================================

DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
USE_SQLITE: bool = os.getenv("USE_SQLITE", "true").lower() in ["true", "1", "yes"]

# ============================================================================
# Default Credentials (for development only; use .env in production)
# ============================================================================

if not DATABASE_URL:
    if USE_SQLITE:
        # SQLite: file-based database for development/testing
        DATABASE_URL = "sqlite:///./primetrade.db"
    else:
        # PostgreSQL: default connection (requires local postgres server)
        PG_USER = os.getenv("PG_USER", "postgres")
        PG_PASSWORD = os.getenv("PG_PASSWORD", "password")
        PG_HOST = os.getenv("PG_HOST", "localhost")
        PG_PORT = os.getenv("PG_PORT", "5432")
        PG_DB = os.getenv("PG_DB", "primetrade")
        
        DATABASE_URL = (
            f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
        )

# ============================================================================
# SQLAlchemy Setup
# ============================================================================

# Determine if using SQLite for engine configuration
is_sqlite = "sqlite" in DATABASE_URL.lower()

# Create engine with appropriate kwargs for SQLite or PostgreSQL
if is_sqlite:
    # SQLite: use check_same_thread=False for threading compatibility
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=os.getenv("SQL_ECHO", "false").lower() in ["true", "1"],
    )
else:
    # PostgreSQL: standard connection pool
    engine = create_engine(
        DATABASE_URL,
        echo=os.getenv("SQL_ECHO", "false").lower() in ["true", "1"],
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()


# ============================================================================
# Dependency: Get DB Session
# ============================================================================

def get_db() -> Session:
    """
    Dependency injection function for FastAPI routes.
    Returns a database session for a single request, then closes it.
    
    Usage in routes:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# Database URL Info (for debugging/logging)
# ============================================================================

def get_db_info() -> dict:
    """Return database connection information for logging/debugging."""
    return {
        "engine": "SQLite" if is_sqlite else "PostgreSQL",
        "url": DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else DATABASE_URL,
    }
