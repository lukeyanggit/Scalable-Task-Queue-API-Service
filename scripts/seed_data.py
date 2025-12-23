"""Script to seed database with sample data"""

from app.db.session import SessionLocal, init_db
from app.services.task_service import TaskService
from app.models.task import TaskPriority
from app.core.logging import logger


def seed_data():
    """Populate database with sample tasks"""
    # Initialize database
    init_db()
    
    db = SessionLocal()
    try:
        service = TaskService(db)
        
        # Create sample tasks
        sample_tasks = [
            {
                "title": "Implement user authentication",
                "description": "Add JWT-based authentication to the API",
                "priority": TaskPriority.HIGH
            },
            {
                "title": "Write API documentation",
                "description": "Create comprehensive API documentation with examples",
                "priority": TaskPriority.MEDIUM
            },
            {
                "title": "Add rate limiting",
                "description": "Implement rate limiting middleware for API endpoints",
                "priority": TaskPriority.MEDIUM
            },
            {
                "title": "Optimize database queries",
                "description": "Review and optimize slow database queries",
                "priority": TaskPriority.LOW
            },
            {
                "title": "Set up CI/CD pipeline",
                "description": "Configure GitHub Actions for automated testing and deployment",
                "priority": TaskPriority.HIGH
            },
            {
                "title": "Add caching layer",
                "description": "Implement Redis caching for frequently accessed data",
                "priority": TaskPriority.MEDIUM
            },
            {
                "title": "Write unit tests",
                "description": "Increase test coverage to 90%+",
                "priority": TaskPriority.HIGH
            },
            {
                "title": "Update README",
                "description": "Add installation and usage instructions to README",
                "priority": TaskPriority.LOW
            }
        ]
        
        created_count = 0
        for task_data in sample_tasks:
            task = service.create_task(
                title=task_data["title"],
                description=task_data["description"],
                priority=task_data["priority"]
            )
            created_count += 1
            logger.info(f"Created task: {task.title} (ID: {task.id})")
        
        logger.info(f"Successfully seeded {created_count} tasks")
        
        # Display statistics
        stats = service.get_stats()
        logger.info(f"Task statistics: {stats}")
        
    except Exception as e:
        logger.error(f"Error seeding data: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()

