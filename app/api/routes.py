"""API routes"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.task_service import TaskService
from app.api.schemas import (
    TaskCreate, TaskUpdate, TaskResponse, TaskStatsResponse, HealthResponse
)
from app.models.task import TaskStatus, TaskPriority
from app.core.security import verify_api_key
from app.core.config import settings
from datetime import datetime

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.api_version,
        timestamp=datetime.utcnow()
    )


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_api_key)
):
    """Create a new task"""
    service = TaskService(db)
    created_task = service.create_task(
        title=task.title,
        description=task.description,
        priority=task.priority
    )
    return created_task


@router.get("/tasks", response_model=List[TaskResponse], tags=["Tasks"])
async def list_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority"),
    db: Session = Depends(get_db),
    _: bool = Depends(verify_api_key)
):
    """List all tasks with optional filtering"""
    service = TaskService(db)
    tasks = service.list_tasks(skip=skip, limit=limit, status=status, priority=priority)
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_api_key)
):
    """Get a specific task by ID"""
    service = TaskService(db)
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_api_key)
):
    """Update a task"""
    service = TaskService(db)
    updated_task = service.update_task(
        task_id=task_id,
        title=task_update.title,
        description=task_update.description,
        priority=task_update.priority,
        status=task_update.status
    )
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return updated_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_api_key)
):
    """Delete a task"""
    service = TaskService(db)
    success = service.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )


@router.get("/tasks/stats/summary", response_model=TaskStatsResponse, tags=["Tasks"])
async def get_task_stats(
    db: Session = Depends(get_db),
    _: bool = Depends(verify_api_key)
):
    """Get task statistics"""
    service = TaskService(db)
    stats = service.get_stats()
    return TaskStatsResponse(**stats)

