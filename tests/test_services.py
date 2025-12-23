"""Service layer tests"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.services.task_service import TaskService
from app.models.task import TaskStatus, TaskPriority

# Test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_services.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create test database session"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_create_task(db_session):
    """Test task creation service"""
    service = TaskService(db_session)
    task = service.create_task(
        title="Test Task",
        description="Test Description",
        priority=TaskPriority.HIGH
    )
    
    assert task.id is not None
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.priority == TaskPriority.HIGH
    assert task.status == TaskStatus.PENDING


def test_get_task(db_session):
    """Test getting a task"""
    service = TaskService(db_session)
    created_task = service.create_task(title="Get Test", priority=TaskPriority.MEDIUM)
    
    retrieved_task = service.get_task(created_task.id)
    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.title == "Get Test"


def test_update_task(db_session):
    """Test updating a task"""
    service = TaskService(db_session)
    task = service.create_task(title="Original", priority=TaskPriority.LOW)
    
    updated_task = service.update_task(
        task_id=task.id,
        title="Updated",
        priority=TaskPriority.HIGH,
        status=TaskStatus.IN_PROGRESS
    )
    
    assert updated_task.title == "Updated"
    assert updated_task.priority == TaskPriority.HIGH
    assert updated_task.status == TaskStatus.IN_PROGRESS


def test_delete_task(db_session):
    """Test deleting a task"""
    service = TaskService(db_session)
    task = service.create_task(title="To Delete", priority=TaskPriority.MEDIUM)
    task_id = task.id
    
    success = service.delete_task(task_id)
    assert success is True
    
    deleted_task = service.get_task(task_id)
    assert deleted_task is None


def test_complete_task(db_session):
    """Test completing a task"""
    service = TaskService(db_session)
    task = service.create_task(title="Complete Test", priority=TaskPriority.MEDIUM)
    
    completed_task = service.complete_task(task.id, result="Task completed successfully")
    
    assert completed_task.status == TaskStatus.COMPLETED
    assert completed_task.result == "Task completed successfully"
    assert completed_task.completed_at is not None


def test_fail_task(db_session):
    """Test failing a task"""
    service = TaskService(db_session)
    task = service.create_task(title="Fail Test", priority=TaskPriority.MEDIUM)
    
    failed_task = service.fail_task(task.id, "Error occurred")
    
    assert failed_task.status == TaskStatus.FAILED
    assert failed_task.error_message == "Error occurred"


def test_get_pending_tasks(db_session):
    """Test getting pending tasks"""
    service = TaskService(db_session)
    
    # Create tasks with different statuses
    task1 = service.create_task(title="Pending 1", priority=TaskPriority.LOW)
    task2 = service.create_task(title="Pending 2", priority=TaskPriority.MEDIUM)
    task3 = service.create_task(title="In Progress", priority=TaskPriority.HIGH)
    
    service.update_task(task3.id, status=TaskStatus.IN_PROGRESS)
    
    pending_tasks = service.get_pending_tasks(limit=10)
    assert len(pending_tasks) == 2
    assert all(task.status == TaskStatus.PENDING for task in pending_tasks)


def test_get_stats(db_session):
    """Test getting task statistics"""
    service = TaskService(db_session)
    
    # Create tasks
    task1 = service.create_task(title="Task 1", priority=TaskPriority.LOW)
    task2 = service.create_task(title="Task 2", priority=TaskPriority.MEDIUM)
    service.complete_task(task1.id)
    
    stats = service.get_stats()
    assert stats["pending"] == 1
    assert stats["completed"] == 1
    assert stats["in_progress"] == 0
    assert stats["failed"] == 0
    assert stats["cancelled"] == 0

