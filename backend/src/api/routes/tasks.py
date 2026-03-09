"""
Task API routes.
Provides CRUD endpoints for task management.
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlmodel import Session, create_engine
from src.models.task import Task
from src.services.task_service import (
    get_user_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
    toggle_task_completion,
)
from src.services.auth_service import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.core.config import get_settings
from datetime import datetime

settings = get_settings()

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

security = HTTPBearer(auto_error=False)


def get_db_session() -> Session:
    """Get database session."""
    connect_args = {}
    if settings.database_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    engine = create_engine(settings.database_url, connect_args=connect_args)
    return Session(engine)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    """
    Get current user ID from JWT token.
    
    Args:
        credentials: Bearer token from Authorization header
        
    Returns:
        int: User ID
        
    Raises:
        HTTPException: 401 if token is missing or invalid
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload["user_id"]


# Request/Response schemas
class TaskCreate(BaseModel):
    """Request schema for creating a task."""
    title: str = Field(min_length=1, max_length=500, description="Task title")
    description: Optional[str] = Field(default=None, max_length=2000, description="Task description")


class TaskUpdate(BaseModel):
    """Request schema for updating a task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: Optional[bool] = Field(default=None)


class TaskResponse(BaseModel):
    """Response schema for a task."""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Response schema for task list."""
    tasks: List[TaskResponse]
    total: int
    filters: dict


class ErrorResponse(BaseModel):
    """Generic error response."""
    status_code: int
    error_type: str
    message: str


@router.get(
    "",
    response_model=TaskListResponse,
    responses={401: {"model": ErrorResponse, "description": "Unauthorized"}},
)
async def list_tasks(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db_session),
    status_filter: Optional[str] = Query(default=None, alias="status", description="Filter by status: pending, completed, or all"),
    sort: str = Query(default="created_at", description="Sort field: created_at or title"),
    order: str = Query(default="desc", description="Sort order: asc or desc"),
):
    """
    List all tasks for the authenticated user.
    
    - **status**: Filter by task status (pending, completed, or all)
    - **sort**: Sort field (created_at or title)
    - **order**: Sort order (asc or desc)
    """
    # Validate status filter
    if status_filter and status_filter not in ["pending", "completed", "all"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status filter. Must be 'pending', 'completed', or 'all'",
        )
    
    # Validate sort field
    if sort not in ["created_at", "title"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid sort field. Must be 'created_at' or 'title'",
        )
    
    # Validate order
    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid sort order. Must be 'asc' or 'desc'",
        )
    
    # Get tasks from service
    tasks = get_user_tasks(
        session=session,
        user_id=user_id,
        status=status_filter if status_filter != "all" else None,
        sort=sort,
        order=order,
    )
    
    return TaskListResponse(
        tasks=tasks,
        total=len(tasks),
        filters={
            "status": status_filter or "all",
            "sort": sort,
            "order": order,
        },
    )


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    },
)
async def create_new_task(
    task_data: TaskCreate,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db_session),
):
    """
    Create a new task.
    
    - **title**: Task title (required, 1-500 characters)
    - **description**: Optional task description (max 2000 characters)
    """
    task = create_task(
        session=session,
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
    )
    return task


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Task not found"},
    },
)
async def get_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db_session),
):
    """
    Get a specific task by ID.
    
    Returns 404 if task doesn't exist or belongs to another user.
    """
    task = get_task_by_id(session=session, task_id=task_id, user_id=user_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Task not found"},
    },
)
async def update_existing_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db_session),
):
    """
    Update a task (full replace).
    
    - **title**: New task title (optional)
    - **description**: New task description (optional)
    - **completed**: New completion status (optional)
    """
    # Build updates dict
    updates = {}
    if task_data.title is not None:
        updates["title"] = task_data.title
    if task_data.description is not None:
        updates["description"] = task_data.description
    if task_data.completed is not None:
        updates["completed"] = task_data.completed
    
    task = update_task(session=session, task_id=task_id, user_id=user_id, updates=updates)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Task not found"},
    },
)
async def patch_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db_session),
):
    """
    Partially update a task.
    
    Same as PUT but only updates provided fields.
    """
    updates = {}
    if task_data.title is not None:
        updates["title"] = task_data.title
    if task_data.description is not None:
        updates["description"] = task_data.description
    if task_data.completed is not None:
        updates["completed"] = task_data.completed
    
    task = update_task(session=session, task_id=task_id, user_id=user_id, updates=updates)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Task not found"},
    },
)
async def delete_existing_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db_session),
):
    """
    Delete a task.
    
    Returns 204 No Content on success.
    """
    success = delete_task(session=session, task_id=task_id, user_id=user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )


@router.post(
    "/{task_id}/toggle",
    response_model=TaskResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Task not found"},
    },
)
async def toggle_task(
    task_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db_session),
):
    """
    Toggle task completion status.
    
    Switches completed from true to false or vice versa.
    """
    task = toggle_task_completion(session=session, task_id=task_id, user_id=user_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    return task
