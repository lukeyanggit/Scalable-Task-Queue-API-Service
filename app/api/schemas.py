"""Request and response schemas"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.task import TaskStatus, TaskPriority


# Task Schemas
class TaskBase(BaseModel):
    """Base task schema"""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    priority: TaskPriority = Field(TaskPriority.MEDIUM, description="Task priority")


class TaskCreate(TaskBase):
    """Schema for creating a task"""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None


class TaskResponse(TaskBase):
    """Schema for task response"""
    id: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[str] = None
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True


class TaskStatsResponse(BaseModel):
    """Schema for task statistics response"""
    pending: int
    in_progress: int
    completed: int
    failed: int
    cancelled: int


class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str
    version: str
    timestamp: datetime

