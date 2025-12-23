"""Background task worker"""

import asyncio
import time
from typing import Optional
from app.db.session import SessionLocal
from app.services.task_service import TaskService
from app.models.task import Task, TaskStatus
from app.core.config import settings
from app.core.logging import logger


class TaskWorker:
    """Background worker for processing tasks"""
    
    def __init__(self):
        self.running = False
        self.concurrency = settings.worker_concurrency
        self.poll_interval = settings.worker_poll_interval
    
    async def process_task(self, task: Task):
        """Process a single task"""
        db = SessionLocal()
        try:
            service = TaskService(db)
            
            # Mark task as in progress
            service.process_task(task.id)
            
            # Simulate task processing
            logger.info(f"Processing task {task.id}: {task.title}")
            
            # Simulate work based on priority
            processing_time = {
                "low": 2,
                "medium": 3,
                "high": 1,
                "urgent": 0.5
            }.get(task.priority.value, 2)
            
            await asyncio.sleep(processing_time)
            
            # Simulate random failures (5% chance)
            import random
            if random.random() < 0.05:
                service.fail_task(task.id, "Simulated processing error")
            else:
                result = f"Task {task.id} completed successfully"
                service.complete_task(task.id, result)
            
            logger.info(f"Completed processing task {task.id}")
        except Exception as e:
            logger.error(f"Error processing task {task.id}: {str(e)}")
            try:
                # Create new service for error handling
                error_service = TaskService(db)
                error_service.fail_task(task.id, str(e))
            except Exception as error_error:
                logger.error(f"Failed to mark task {task.id} as failed: {str(error_error)}")
        finally:
            db.close()
    
    async def worker_loop(self):
        """Main worker loop"""
        logger.info(f"Worker started with concurrency={self.concurrency}")
        
        while self.running:
            try:
                db = SessionLocal()
                service = TaskService(db)
                
                # Get pending tasks
                pending_tasks = service.get_pending_tasks(limit=self.concurrency)
                
                if pending_tasks:
                    # Process tasks concurrently
                    tasks = [self.process_task(task) for task in pending_tasks]
                    await asyncio.gather(*tasks, return_exceptions=True)
                else:
                    # No tasks to process, wait before polling again
                    await asyncio.sleep(self.poll_interval)
                
                db.close()
            except Exception as e:
                logger.error(f"Error in worker loop: {str(e)}")
                await asyncio.sleep(self.poll_interval)
    
    def start(self):
        """Start the worker"""
        if self.running:
            logger.warning("Worker is already running")
            return
        
        self.running = True
        logger.info("Starting task worker...")
        
        try:
            asyncio.run(self.worker_loop())
        except KeyboardInterrupt:
            logger.info("Worker stopped by user")
            self.running = False
        except Exception as e:
            logger.error(f"Worker crashed: {str(e)}")
            self.running = False
    
    def stop(self):
        """Stop the worker"""
        self.running = False
        logger.info("Stopping worker...")


# Global worker instance
worker = TaskWorker()

