import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from celery.exceptions import Retry
from app.core.celery_app import celery_app
from app.tasks.ai import optimize_resume_task, compute_job_relevance_task
from app.tasks.notifications import send_email_task, send_webhook_task
from app.tasks.scraping import scrape_jobs_task
from app.tasks.workflows import run_resume_optimization_pipeline


@pytest.fixture(scope="module", autouse=True)
def configure_celery_eager():
    """Forces Celery to execute tasks synchronously in-process for test isolation."""
    celery_app.conf.update(
        task_always_eager=True,
        task_eager_propagates=True,
    )
    yield
    celery_app.conf.update(
        task_always_eager=False,
        task_eager_propagates=False,
    )


@patch("app.ai.providers.provider_factory.ai_factory.generate_with_fallback")
def test_optimize_resume_task_success(mock_generate):
    """Verifies that the resume optimization task executes and fetches AI outputs successfully."""
    # Mock AI response
    mock_response = MagicMock()
    mock_response.content = "Optimized Resume Content: 5+ years of experience with Python & FastAPI"
    mock_generate.return_value = mock_response

    # Execute eager task
    result = optimize_resume_task.delay("Original Resume Text", "FastAPI Engineer")
    
    assert result.successful()
    assert "Optimized Resume Content" in result.result
    mock_generate.assert_called_once()


@patch("app.ai.providers.provider_factory.ai_factory.generate_with_fallback")
def test_compute_job_relevance_task_success(mock_generate):
    """Verifies that the job relevance comparison task successfully calculates match details."""
    mock_response = MagicMock()
    mock_response.content = '{"score": 92.5, "skills": ["Python", "Docker"], "gaps": []}'
    mock_generate.return_value = mock_response

    result = compute_job_relevance_task.delay(
        "Python Developer",
        "Looking for a backend engineer proficient in Python.",
        "Experienced Python backend developer.",
    )

    assert result.successful()
    assert "score" in result.result
    mock_generate.assert_called_once()


def test_send_email_task_success():
    """Verifies that the simulated email delivery task successfully runs under normal conditions."""
    result = send_email_task.delay("user@example.com", "Welcome", "Hello World!")
    
    assert result.successful()
    assert result.result["status"] == "sent"
    assert result.result["recipient"] == "user@example.com"


@patch("app.tasks.notifications.send_email_task.retry")
def test_send_email_task_failure_and_retry(mock_retry):
    """Tests that sending an email to a recipient with 'fail' in their name triggers a retry."""
    # Set eager to false temporarily for mock retry validation
    celery_app.conf.update(task_always_eager=False)
    
    mock_retry.side_effect = Retry("Simulated Retry Exception")

    with pytest.raises(Retry):
        send_email_task(recipient="fail@example.com", subject="Test", body="Failed mail")

    mock_retry.assert_called_once()
    
    celery_app.conf.update(task_always_eager=True)


@patch("httpx.AsyncClient.post")
def test_send_webhook_task_success(mock_post):
    """Verifies that the webhook dispatch task succeeds when HTTP client receives a success status code."""
    # Mock HTTP response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    result = send_webhook_task.delay(
        "https://example.com/webhook",
        "resume.optimized",
        {"id": 1, "status": "done"},
    )

    assert result.successful()
    assert result.result["status"] == "success"
    assert result.result["code"] == 200


def test_scrape_jobs_task_success():
    """Verifies that the job scraping task successfully runs and parses matching job roles."""
    result = scrape_jobs_task.delay("FastAPI", "San Francisco")
    
    assert result.successful()
    assert result.result["status"] == "success"
    assert result.result["jobs_count"] == 2
    assert "FastAPI" in result.result["jobs"][0]["title"]


@patch("app.core.redis.redis_manager.get_client")
def test_dead_letter_queue_push_on_final_failure(mock_get_client):
    """Verifies that a task which exceeds its retry limit is routed to the Redis dead-letter queue."""
    # Mock Redis client and list push
    mock_redis = MagicMock()
    mock_get_client.return_value = mock_redis
    
    fake_exc = ConnectionError("SMTP Server down permanently")
    task_id = "test-task-123"
    args = ("fail@example.com", "Test", "DLQ test")
    kwargs = {}
    
    # Subclass BaseWorkflowTask to satisfy super() requirements and mock request
    from app.core.celery_app import BaseWorkflowTask
    
    class TestTask(BaseWorkflowTask):
        name = "app.tasks.notifications.send_email_task"
        max_retries = 3
        
        @property
        def request(self):
            mock_req = MagicMock()
            mock_req.retries = 3
            return mock_req

    mock_task = TestTask()
    
    # Invoke on_failure handler
    mock_task.on_failure(fake_exc, task_id, args, kwargs, None)
    
    # Verify it pushed the JSON trace to dead_letter_queue list in Redis
    mock_redis.lpush.assert_called_once()
    call_args = mock_redis.lpush.call_args[0]
    assert call_args[0] == "dead_letter_queue"
    
    dlq_data = json.loads(call_args[1])
    assert dlq_data["task_id"] == task_id
    assert dlq_data["task_name"] == "app.tasks.notifications.send_email_task"
    assert dlq_data["error"] == "SMTP Server down permanently"
    assert dlq_data["retry_history"] == 3


@patch("app.tasks.workflows.optimize_resume_task.run")
@patch("app.tasks.workflows.email_delivery_after_optimization_task.run")
def test_run_resume_optimization_pipeline(mock_email_run, mock_opt_run):
    """Tests the coordinating workflow pipeline triggers the execution chain successfully."""
    mock_opt_run.return_value = "Optimized resume text content"
    mock_email_run.return_value = {"status": "sent"}
    
    # Execute the workflow coordinator
    chain_id = run_resume_optimization_pipeline(
        resume_text="Original resume text.",
        target_role="Principal Architect",
        user_email="architect@example.com",
    )

    assert chain_id is not None
    mock_opt_run.assert_called_once_with("Original resume text.", "Principal Architect")
    mock_email_run.assert_called_once_with(
        "Optimized resume text content", 
        "architect@example.com", 
        "Optimized Resume: Principal Architect"
    )
