from fastapi import FastAPI
from app.core import Base, engine, get_db_info

# Initialize FastAPI app
app = FastAPI(
    title="PrimeTrade Backend API",
    description="Scalable backend with authentication, role-based access, and CRUD APIs",
    version="1.0.0",
)


# ============================================================================
# Startup Event: Initialize Database
# ============================================================================

@app.on_event("startup")
def startup_event():
    """
    Initialize database tables on app startup.
    Creates all tables defined in models if they don't exist.
    """
    Base.metadata.create_all(bind=engine)
    db_info = get_db_info()
    print(f"✓ Database initialized: {db_info}")


# ============================================================================
# Health Check Route
# ============================================================================

@app.get("/", tags=["Health"])
def read_root() -> dict:
    """Root endpoint for health check."""
    return {"message": "PrimeTrade backend is running"}


@app.get("/health", tags=["Health"])
def health_check() -> dict:
    """Health check endpoint with database info."""
    return {
        "status": "healthy",
        "database": get_db_info(),
    }
