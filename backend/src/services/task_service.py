"""
Task service layer for business logic.
"""

from sqlmodel import Session, select
from typing import List, Optional
from src.models.task import Task
from src.models.user import User
from datetime import datetime


def get_user_tasks(session: Session, user_id: int, status: Optional[str] = None, sort: str = "created_at", order: str = "desc") -> List[Task]:
    """
    Get all tasks for a user with optional filtering and sorting.
    
    Args:
        session: Database session
        user_id: User ID to filter tasks
        status: Filter by status ('pending', 'completed', or None for all)
        sort: Sort field ('created_at' or 'title')
        order: Sort order ('asc' or 'desc')
    
    Returns:
        List of tasks
    """
    query = select(Task).where(Task.user_id == user_id)
    
    # Apply status filter
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)
    
    # Apply sorting
    if sort == "title":
        if order == "asc":
            query = query.order_by(Task.title.asc())
        else:
            query = query.order_by(Task.title.desc())
    else:  # default to created_at
        if order == "asc":
            query = query.order_by(Task.created_at.asc())
        else:
            query = query.order_by(Task.created_at.desc())
    
    results = session.exec(query)
    return list(results.all())


def get_task_by_id(session: Session, task_id: int, user_id: int) -> Optional[Task]:
    """
    Get a task by ID, ensuring it belongs to the user.
    
    Args:
        session: Database session
        task_id: Task ID
        user_id: User ID for ownership validation
    
    Returns:
        Task if found and belongs to user, None otherwise
    """
    task = session.get(Task, task_id)
    if task and task.user_id == user_id:
        return task
    return None


def create_task(session: Session, user_id: int, title: str, description: Optional[str] = None) -> Task:
    """
    Create a new task.
    
    Args:
        session: Database session
        user_id: User ID to associate with task
        title: Task title
        description: Optional task description
    
    Returns:
        Created task
    """
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        created_at=datetime.utcnow(),
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def update_task(session: Session, task_id: int, user_id: int, updates: dict) -> Optional[Task]:
    """
    Update a task.
    
    Args:
        session: Database session
        task_id: Task ID
        user_id: User ID for ownership validation
        updates: Dictionary of fields to update
    
    Returns:
        Updated task if successful, None if task not found
    """
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return None
    
    # Update allowed fields
    for field, value in updates.items():
        if field in ["title", "description", "completed"]:
            setattr(task, field, value)
    
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task_id: int, user_id: int) -> bool:
    """
    Delete a task.
    
    Args:
        session: Database session
        task_id: Task ID
        user_id: User ID for ownership validation
    
    Returns:
        True if deleted, False if task not found
    """
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return False
    
    session.delete(task)
    session.commit()
    return True


def toggle_task_completion(session: Session, task_id: int, user_id: int) -> Optional[Task]:
    """
    Toggle task completion status.
    
    Args:
        session: Database session
        task_id: Task ID
        user_id: User ID for ownership validation
    
    Returns:
        Updated task if successful, None if task not found
    """
    task = get_task_by_id(session, task_id, user_id)
    if not task:
        return None
    
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
