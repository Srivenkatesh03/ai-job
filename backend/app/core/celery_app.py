import json
import logging
import traceback
from datetime import datetime
from celery import Celery, Task
from kombu import Queue
from app.core.config import settings

logger = logging.getLogger(__name__)

# Set custom Task base class
class BaseWorkflowTask(Task):
    """
    Custom Celery Task base class implementing automatic dead-letter queue
    routing on final failure after exhausting all retries.
    """
    abstract = True

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Called when task fails. Sends final failures to the dead-letter queue (DLQ)."""
        logger.error(f"Task {self.name}[{task_id}] failed: {exc}")

        max_retries = self.max_retries if self.max_retries is not None else 3
        current_retries = self.request.retries

        if current_retries >= max_retries:
            logger.warning(f"Task {self.name}[{task_id}] exceeded max retries ({max_retries}). Routing to DLQ.")
            
            # Send task payload and error info to the dead-letter queue
            dlq_payload = {
                "task_id": task_id,
                "task_name": self.name,
                "args": args,
                "kwargs": kwargs,
                "error": str(exc),
                "stack_trace": traceback.format_exc() if einfo else "No stack trace available",
                "retry_history": current_retries,
                "failed_at": datetime.utcnow().isoformat(),
            }

            try:
                # Direct publish to Redis dead_letter queue
                from app.core.redis import redis_manager
                redis_client = redis_manager.get_client()
                
                # Push into the dead_letter_queue list
                redis_client.lpush("dead_letter_queue", json.dumps(dlq_payload))
                logger.info(f"Task {task_id} successfully pushed to DLQ.")
            except Exception as dlq_err:
                logger.critical(f"Failed to push task {task_id} to DLQ: {dlq_err}")

        super().on_failure(exc, task_id, args, kwargs, einfo)


# Initialize Celery app
celery_app = Celery(
    "ai_job_automation",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    task_cls=BaseWorkflowTask,
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,  # Acknowledge after run completes
    task_reject_on_worker_lost=True,
    
    # Configure named queues
    task_queues=[
        Queue("ai_tasks"),
        Queue("notifications"),
        Queue("scraping"),
        Queue("workflows"),
        Queue("analytics"),
    ],
    
    # Route tasks dynamically based on their names
    task_routes={
        "app.tasks.ai.*": {"queue": "ai_tasks"},
        "app.tasks.notifications.*": {"queue": "notifications"},
        "app.tasks.scraping.*": {"queue": "scraping"},
        "app.tasks.workflows.*": {"queue": "workflows"},
        "app.tasks.analytics.*": {"queue": "analytics"},
    },
    
    # Timeouts per task category
    task_annotations={
        "app.tasks.ai.*": {"time_limit": 60, "soft_time_limit": 55},
        "app.tasks.notifications.*": {"time_limit": 15, "soft_time_limit": 12},
        "app.tasks.scraping.*": {"time_limit": 120, "soft_time_limit": 110},
        "app.tasks.analytics.*": {"time_limit": 300, "soft_time_limit": 280},
    },
    
    # Registered task modules for worker autodiscovery
    imports=[
        "app.tasks.ai",
        "app.tasks.notifications",
        "app.tasks.scraping",
        "app.tasks.workflows",
    ],
)

# Register base task class
celery_app.Task = BaseWorkflowTask
