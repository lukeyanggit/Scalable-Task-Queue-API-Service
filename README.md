# Scalable Task Queue & API Service (TaskFlow)

A production-ready, scalable task queue API service built with FastAPI, demonstrating clean architecture, async processing, and best practices for backend development.

## 🚀 Features

- **RESTful API** - Full CRUD operations for task management
- **Async Background Processing** - Worker system for processing tasks asynchronously
- **Clean Architecture** - Separation of concerns with API, Service, and Repository layers
- **Comprehensive Testing** - Unit and integration tests with pytest
- **Configuration Management** - Environment-based configuration using Pydantic Settings
- **Security** - API key authentication support
- **Logging** - Structured logging throughout the application
- **Docker Ready** - Containerized deployment with Docker
- **Production Features** - Health checks, CORS, error handling

## 📁 Project Structure

```
taskflow/
│
├── app/
│   ├── __init__.py
│   │
│   ├── main.py                # Entry point (FastAPI app)
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py          # API endpoints
│   │   └── schemas.py         # Request / response models (Pydantic)
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Environment & settings
│   │   ├── logging.py         # Logging setup
│   │   └── security.py        # Auth / API keys
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py    # Business logic
│   │
│   ├── workers/
│   │   ├── __init__.py
│   │   └── worker.py          # Async background jobs
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py            # Data models (SQLAlchemy)
│   │
│   └── db/
│       ├── __init__.py
│       ├── session.py         # DB connection
│       └── repository.py      # Data access layer
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py           # API endpoint tests
│   └── test_services.py      # Service layer tests
│
├── scripts/
│   └── seed_data.py           # Populate sample data
│
├── .env                       # Environment variables (create from .env.example)
├── .gitignore
├── requirements.txt
├── pyproject.toml             # Tooling config
├── README.md
└── Dockerfile                 # Deployment-ready container
```

## 🏗️ Architecture

### Layer Separation

```
┌─────────────────────────────────────┐
│          API Layer (routes)         │  ← FastAPI endpoints
│         Request/Response            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Service Layer (business)       │  ← Business logic
│      Task orchestration             │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Repository Layer (data access)    │  ← Database operations
│      CRUD operations                │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│        Database (SQLAlchemy)        │  ← SQLite/PostgreSQL
└─────────────────────────────────────┘
```

### Key Design Patterns

- **Repository Pattern** - Data access abstraction
- **Service Layer** - Business logic separation
- **Dependency Injection** - FastAPI's dependency system
- **Async/Await** - Background worker processing

## 🛠️ Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **Pytest** - Testing framework
- **AsyncIO** - Asynchronous I/O support
- **Uvicorn** - ASGI server
- **Docker** - Containerization

## 📦 Installation

### Prerequisites

- Python 3.9+
- pip or poetry
- (Optional) Docker and Docker Compose

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Scalable-Task-Queue-API-Service
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy .env.example to .env and update values
   # For development, API_KEY can be left empty to disable auth
   ```

5. **Initialize the database**
   ```bash
   # The database will be created automatically on first run
   # Or seed with sample data:
   python scripts/seed_data.py
   ```

6. **Run the application**
   ```bash
   # Development mode
   uvicorn app.main:app --reload
   
   # Or use the main module
   python -m app.main
   ```

7. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🧪 Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

## 🐳 Docker Deployment

### Build and run with Docker

```bash
# Build the image
docker build -t taskflow-api .

# Run the container
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./taskflow.db \
  -e API_KEY=your-api-key \
  taskflow-api

# Or use docker-compose (create docker-compose.yml if needed)
docker-compose up
```

## 📡 API Endpoints

### Health Check

```http
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Create Task

```http
POST /api/v1/tasks
Content-Type: application/json
X-API-Key: your-api-key (optional if API_KEY not set)

{
  "title": "Implement feature X",
  "description": "Add new feature with tests",
  "priority": "high"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "title": "Implement feature X",
  "description": "Add new feature with tests",
  "priority": "high",
  "status": "pending",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### List Tasks

```http
GET /api/v1/tasks?skip=0&limit=100&status=pending&priority=high
```

**Query Parameters:**
- `skip` (int): Number of tasks to skip (default: 0)
- `limit` (int): Maximum number of tasks (default: 100, max: 1000)
- `status` (optional): Filter by status (pending, in_progress, completed, failed, cancelled)
- `priority` (optional): Filter by priority (low, medium, high, urgent)

### Get Task

```http
GET /api/v1/tasks/{task_id}
```

### Update Task

```http
PUT /api/v1/tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated title",
  "status": "in_progress",
  "priority": "urgent"
}
```

### Delete Task

```http
DELETE /api/v1/tasks/{task_id}
```

**Response:** `204 No Content`

### Get Task Statistics

```http
GET /api/v1/tasks/stats/summary
```

**Response:**
```json
{
  "pending": 5,
  "in_progress": 2,
  "completed": 10,
  "failed": 1,
  "cancelled": 0
}
```

## 🔄 Background Worker

The worker processes pending tasks asynchronously. To run the worker:

```bash
python -m app.workers.worker
```

Or integrate it into your application startup. The worker:
- Polls for pending tasks
- Processes tasks concurrently (configurable concurrency)
- Handles task failures gracefully
- Updates task status (pending → in_progress → completed/failed)

## 🔐 Security

- **API Key Authentication**: Set `API_KEY` in environment variables
- **CORS**: Configurable via `CORS_ORIGINS` setting
- **Input Validation**: Pydantic schemas validate all inputs
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## ⚙️ Configuration

Environment variables (set in `.env` file):

```env
# API Configuration
API_TITLE=TaskFlow API
API_VERSION=1.0.0

# Database
DATABASE_URL=sqlite:///./taskflow.db
# For PostgreSQL: postgresql://user:password@localhost:5432/taskflow

# Security
API_KEY=your-api-key-here  # Leave empty to disable auth
SECRET_KEY=change-in-production

# Worker
WORKER_ENABLED=true
WORKER_CONCURRENCY=4
WORKER_POLL_INTERVAL=5

# Logging
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=["*"]
```

## 📊 Example Usage

### Using cURL

```bash
# Create a task
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "title": "Deploy to production",
    "description": "Deploy latest version",
    "priority": "urgent"
  }'

# List all tasks
curl "http://localhost:8000/api/v1/tasks"

# Get task statistics
curl "http://localhost:8000/api/v1/tasks/stats/summary"
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {"X-API-Key": "your-api-key"}

# Create a task
response = requests.post(
    f"{BASE_URL}/tasks",
    json={
        "title": "Test Task",
        "description": "This is a test",
        "priority": "high"
    },
    headers=HEADERS
)
task = response.json()
print(f"Created task: {task['id']}")

# Get task
response = requests.get(f"{BASE_URL}/tasks/{task['id']}", headers=HEADERS)
print(response.json())
```

## 🔮 Future Improvements

- [ ] Redis integration for distributed task queue
- [ ] WebSocket support for real-time task updates
- [ ] Rate limiting middleware
- [ ] JWT authentication
- [ ] Task scheduling (cron-like functionality)
- [ ] Task retry mechanism with exponential backoff
- [ ] Metrics and monitoring (Prometheus)
- [ ] Database migrations (Alembic)
- [ ] Multi-tenancy support
- [ ] Task dependencies and workflows
- [ ] File upload/download for task attachments
- [ ] Email notifications for task completion

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🎯 Why This Project Stands Out

✅ **Production-Ready Architecture** - Clean separation of concerns that scales

✅ **Best Practices** - Testing, logging, configuration management, error handling

✅ **Modern Tech Stack** - FastAPI, async/await, type hints, Pydantic

✅ **Developer Experience** - Clear structure, documentation, easy to extend

✅ **Interview-Ready** - Demonstrates system design thinking and backend fundamentals

---

**Built with ❤️ using FastAPI**
