"""API endpoint tests"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import Base, get_db
from app.models.task import TaskStatus, TaskPriority

# Test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def test_db():
    """Create test database tables"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create test client"""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_create_task(client):
    """Test task creation"""
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high"
        },
        headers={"X-API-Key": "test-key"} if False else {}  # API key optional in dev
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "pending"
    assert data["priority"] == "high"
    assert "id" in data


def test_get_task(client):
    """Test getting a task"""
    # Create a task first
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Get Test Task", "priority": "medium"}
    )
    task_id = create_response.json()["id"]
    
    # Get the task
    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Get Test Task"


def test_get_task_not_found(client):
    """Test getting non-existent task"""
    response = client.get("/api/v1/tasks/99999")
    assert response.status_code == 404


def test_list_tasks(client):
    """Test listing tasks"""
    # Create multiple tasks
    for i in range(3):
        client.post(
            "/api/v1/tasks",
            json={"title": f"Task {i}", "priority": "low"}
        )
    
    # List tasks
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_update_task(client):
    """Test updating a task"""
    # Create a task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Original Title", "priority": "low"}
    )
    task_id = create_response.json()["id"]
    
    # Update the task
    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Updated Title", "priority": "high", "status": "in_progress"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["priority"] == "high"
    assert data["status"] == "in_progress"


def test_delete_task(client):
    """Test deleting a task"""
    # Create a task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "To Be Deleted", "priority": "medium"}
    )
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/tasks/{task_id}")
    assert get_response.status_code == 404


def test_get_task_stats(client):
    """Test getting task statistics"""
    # Create tasks with different statuses
    client.post("/api/v1/tasks", json={"title": "Task 1", "priority": "low"})
    client.post("/api/v1/tasks", json={"title": "Task 2", "priority": "medium"})
    
    response = client.get("/api/v1/tasks/stats/summary")
    assert response.status_code == 200
    data = response.json()
    assert "pending" in data
    assert "in_progress" in data
    assert "completed" in data
    assert "failed" in data
    assert "cancelled" in data

