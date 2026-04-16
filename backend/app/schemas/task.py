"""
Pydantic schemas for Task validation and API responses.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ============================================================================
# Task Request Schemas
# ============================================================================

class TaskCreate(BaseModel):
    """
    Schema for task creation request.
    
    Validates:
    - title: Required, 1-255 characters
    - description: Optional task description
    """
    
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Task title (required, 1-255 chars)"
    )
    
    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Optional task description (max 5000 chars)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete project proposal",
                "description": "Write and submit project proposal to management"
            }
        }


class TaskUpdate(BaseModel):
    """
    Schema for task update request.
    
    Validates:
    - title: Optional task title
    - description: Optional task description
    - completed: Optional completion status
    """
    
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Updated task title (optional)"
    )
    
    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Updated task description (optional)"
    )
    
    completed: Optional[bool] = Field(
        default=None,
        description="Task completion status (optional)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete project proposal",
                "description": "Write and submit project proposal to management",
                "completed": False
            }
        }


# ============================================================================
# Task Response Schema
# ============================================================================

class TaskResponse(BaseModel):
    """
    Schema for task data in API responses.
    Includes task details and timestamps.
    """
    
    id: int = Field(..., description="Task ID")
    user_id: int = Field(..., description="Owner's user ID")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(..., description="Task description")
    completed: bool = Field(..., description="Task completion status")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True  # Pydantic v2 ORM mode
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "title": "Complete project proposal",
                "description": "Write and submit project proposal to management",
                "completed": False,
                "created_at": "2026-04-16T10:30:00",
                "updated_at": "2026-04-16T10:30:00"
            }
        }


# ============================================================================
# Task List Response (with pagination info)
# ============================================================================

class TaskListResponse(BaseModel):
    """
    Schema for task list responses with pagination.
    """
    
    tasks: list[TaskResponse] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks")
    limit: int = Field(..., description="Items per page")
    offset: int = Field(..., description="Current offset")
    
    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": 1,
                        "user_id": 1,
                        "title": "Complete project proposal",
                        "description": "Write and submit project proposal to management",
                        "completed": False,
                        "created_at": "2026-04-16T10:30:00",
                        "updated_at": "2026-04-16T10:30:00"
                    }
                ],
                "total": 1,
                "limit": 10,
                "offset": 0
            }
        }
