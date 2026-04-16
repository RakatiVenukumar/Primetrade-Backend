from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core import Base, engine, get_db_info
from app.routes import auth_router, admin_router, tasks_router

openapi_tags = [
    {
        "name": "Health",
        "description": "Service health and readiness endpoints.",
    },
    {
        "name": "Authentication",
        "description": "User registration, login, and current user profile endpoints.",
    },
    {
        "name": "Admin",
        "description": "Admin-only user management and role control endpoints.",
    },
    {
        "name": "Tasks",
        "description": "Authenticated task CRUD endpoints with per-user ownership isolation.",
    },
]

# Initialize FastAPI app
app = FastAPI(
    title="PrimeTrade Backend API",
    description=(
        "Scalable backend with JWT authentication, role-based access control, "
        "task CRUD operations, and standardized error responses."
    ),
    version="1.0.0",
    openapi_tags=openapi_tags,
    contact={
        "name": "PrimeTrade API Support",
    },
)

# ============================================================================
# Include Routers
# ============================================================================

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(tasks_router)


# ============================================================================
# Global Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Return a standardized payload for expected HTTP errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "type": "http_error",
                "message": exc.detail,
                "status_code": exc.status_code,
                "path": str(request.url.path),
            },
        },
        headers=getattr(exc, "headers", None),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Return a standardized payload for request validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "type": "validation_error",
                "message": "Request validation failed",
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "path": str(request.url.path),
                "details": exc.errors(),
            },
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Return a standardized payload for unexpected server errors."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "type": "internal_server_error",
                "message": "An unexpected error occurred",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "path": str(request.url.path),
            },
        },
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
    print(f"[OK] Database initialized: {db_info}")


# ============================================================================
# Versioned Health Routes
# ============================================================================

@app.get(
    "/api/v1",
    tags=["Health"],
    summary="API root",
    description="Versioned API root endpoint used for quick service checks.",
)
def read_root() -> dict:
    """Versioned root endpoint for health check."""
    return {"message": "PrimeTrade backend is running"}


@app.get(
    "/api/v1/health",
    tags=["Health"],
    summary="Health check",
    description="Returns backend health status and active database configuration.",
)
def health_check() -> dict:
    """Versioned health check endpoint with database info."""
    return {
        "status": "healthy",
        "database": get_db_info(),
    }
