"""Data access layer (Repository pattern)"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.task import Task, TaskStatus, TaskPriority


class TaskRepository:
    """Repository for task data access operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, task: Task) -> Task:
        """Create a new task"""
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        return self.db.query(Task).filter(Task.id == task_id).first()
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None
    ) -> List[Task]:
        """Get all tasks with optional filtering"""
        query = self.db.query(Task)
        
        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == priority)
        
        return query.order_by(desc(Task.created_at)).offset(skip).limit(limit).all()
    
    def update(self, task: Task) -> Task:
        """Update an existing task"""
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def delete(self, task_id: int) -> bool:
        """Delete a task by ID"""
        task = self.get_by_id(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
            return True
        return False
    
    def get_pending_tasks(self, limit: int = 10) -> List[Task]:
        """Get pending tasks for processing"""
        return self.db.query(Task).filter(
            Task.status == TaskStatus.PENDING
        ).order_by(
            desc(Task.created_at)
        ).limit(limit).all()
    
    def count_by_status(self, status: TaskStatus) -> int:
        """Count tasks by status"""
        return self.db.query(Task).filter(Task.status == status).count()

