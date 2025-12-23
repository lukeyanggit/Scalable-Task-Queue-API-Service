"""Task business logic service"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.repository import TaskRepository
from app.models.task import Task, TaskStatus, TaskPriority
from app.core.logging import logger


class TaskService:
    """Service for task business logic"""
    
    def __init__(self, db: Session):
        self.repository = TaskRepository(db)
        self.db = db
    
    def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        priority: TaskPriority = TaskPriority.MEDIUM
    ) -> Task:
        """Create a new task"""
        task = Task(
            title=title,
            description=description,
            priority=priority,
            status=TaskStatus.PENDING
        )
        logger.info(f"Creating task: {title} with priority {priority}")
        return self.repository.create(task)
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID"""
        return self.repository.get_by_id(task_id)
    
    def list_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None
    ) -> List[Task]:
        """List tasks with optional filtering"""
        return self.repository.get_all(skip=skip, limit=limit, status=status, priority=priority)
    
    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[TaskPriority] = None,
        status: Optional[TaskStatus] = None
    ) -> Optional[Task]:
        """Update a task"""
        task = self.repository.get_by_id(task_id)
        if not task:
            return None
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None:
            task.priority = priority
        if status is not None:
            task.status = status
            if status == TaskStatus.COMPLETED:
                task.completed_at = datetime.utcnow()
            elif status != TaskStatus.COMPLETED:
                task.completed_at = None
        
        logger.info(f"Updating task {task_id}: status={status}, priority={priority}")
        return self.repository.update(task)
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        logger.info(f"Deleting task {task_id}")
        return self.repository.delete(task_id)
    
    def process_task(self, task_id: int) -> Optional[Task]:
        """Mark a task as in progress (called by worker)"""
        task = self.repository.get_by_id(task_id)
        if not task:
            return None
        
        if task.status != TaskStatus.PENDING:
            logger.warning(f"Task {task_id} is not pending, cannot process")
            return None
        
        task.status = TaskStatus.IN_PROGRESS
        logger.info(f"Processing task {task_id}: {task.title}")
        return self.repository.update(task)
    
    def complete_task(self, task_id: int, result: Optional[str] = None) -> Optional[Task]:
        """Mark a task as completed"""
        task = self.repository.get_by_id(task_id)
        if not task:
            return None
        
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.utcnow()
        if result:
            task.result = result
        
        logger.info(f"Completed task {task_id}: {task.title}")
        return self.repository.update(task)
    
    def fail_task(self, task_id: int, error_message: str) -> Optional[Task]:
        """Mark a task as failed"""
        task = self.repository.get_by_id(task_id)
        if not task:
            return None
        
        task.status = TaskStatus.FAILED
        task.error_message = error_message
        logger.error(f"Task {task_id} failed: {error_message}")
        return self.repository.update(task)
    
    def get_pending_tasks(self, limit: int = 10) -> List[Task]:
        """Get pending tasks for processing"""
        return self.repository.get_pending_tasks(limit=limit)
    
    def get_stats(self) -> dict:
        """Get task statistics"""
        return {
            "pending": self.repository.count_by_status(TaskStatus.PENDING),
            "in_progress": self.repository.count_by_status(TaskStatus.IN_PROGRESS),
            "completed": self.repository.count_by_status(TaskStatus.COMPLETED),
            "failed": self.repository.count_by_status(TaskStatus.FAILED),
            "cancelled": self.repository.count_by_status(TaskStatus.CANCELLED),
        }

