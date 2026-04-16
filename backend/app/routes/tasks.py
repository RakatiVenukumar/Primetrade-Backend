"""
Task CRUD routes for authenticated users.
Each user can only access their own tasks.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.core import get_db
from app.core.dependencies import get_current_user
from app.models import Task
from app.schemas import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate, UserResponse


router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"],
    responses={
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
        404: {"description": "Task not found"},
        500: {"description": "Internal Server Error"},
    },
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
    description="Create a new task for the authenticated user",
)
def create_task(
    payload: TaskCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TaskResponse:
    task = Task(
        user_id=current_user.id,
        title=payload.title,
        description=payload.description,
        completed=False,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get(
    "",
    response_model=TaskListResponse,
    status_code=status.HTTP_200_OK,
    summary="List tasks",
    description="List tasks for the authenticated user with pagination",
)
def list_tasks(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    completed: Optional[bool] = Query(default=None),
) -> TaskListResponse:
    base_query = db.query(Task).filter(Task.user_id == current_user.id)
    if completed is not None:
        base_query = base_query.filter(Task.completed == completed)

    total = base_query.count()
    tasks = base_query.order_by(Task.created_at.desc()).offset(offset).limit(limit).all()

    return TaskListResponse(tasks=tasks, total=total, limit=limit, offset=offset)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get task by ID",
    description="Get a single task by ID for the authenticated user",
)
def get_task(
    task_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TaskResponse:
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update task",
    description="Update a task owned by the authenticated user",
)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TaskResponse:
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update",
        )

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Delete a task owned by the authenticated user",
)
def delete_task(
    task_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
