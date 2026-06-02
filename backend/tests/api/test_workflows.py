import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.workflow import WorkflowRun


@pytest.mark.asyncio
async def test_workflow_lifecycle_success(client: AsyncClient, db_session: AsyncSession):
    """Test full workflow run lifecycle: register, list, trigger, and status check."""
    # 1. Register User & Login to get token
    user_payload = {
        "email": "workflow_test@example.com",
        "password": "strongpassword123",
        "full_name": "Workflow User",
    }
    await client.post("/api/v1/auth/register", json=user_payload)
    
    login_response = await client.post("/api/v1/auth/login", json=user_payload)
    access_token = login_response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # 2. Register a new workflow
    wf_payload = {
        "task_name": "app.tasks.workflows.run_resume_optimization_pipeline",
        "queue": "workflows"
    }
    create_response = await client.post("/api/v1/workflows", json=wf_payload, headers=headers)
    assert create_response.status_code == 200
    create_data = create_response.json()
    assert create_data["success"] is True
    wf_id = create_data["data"]["id"]
    assert wf_id is not None
    assert create_data["data"]["status"] == "pending"

    # 3. List workflows
    list_response = await client.get("/api/v1/workflows", headers=headers)
    assert list_response.status_code == 200
    list_data = list_response.json()
    assert list_data["success"] is True
    assert len(list_data["data"]) == 1
    assert list_data["data"][0]["id"] == wf_id

    # 4. Trigger the workflow (Mock Celery send_task)
    mock_task = MagicMock()
    mock_task.id = "mock-celery-task-id-123"
    
    with patch("app.api.v1.workflows.celery_app.send_task", return_value=mock_task) as mock_send:
        run_response = await client.post(f"/api/v1/workflows/{wf_id}/run", headers=headers)
        assert run_response.status_code == 200
        run_data = run_response.json()
        assert run_data["success"] is True
        assert run_data["data"]["task_id"] == "mock-celery-task-id-123"
        assert run_data["data"]["status"] == "running"
        mock_send.assert_called_once()

    # 5. Check status (Mock Celery AsyncResult)
    mock_async_result = MagicMock()
    mock_async_result.ready.return_value = True
    mock_async_result.successful.return_value = True
    mock_async_result.result = "Success! Optimization and Email completed."

    with patch("celery.result.AsyncResult", return_value=mock_async_result) as mock_result:
        # Note: Since run.id was updated to mock-celery-task-id-123 in the previous step,
        # we check status on the mock-celery-task-id-123 (which replaced the old wf_id in DB)
        status_response = await client.get(f"/api/v1/workflows/mock-celery-task-id-123/status", headers=headers)
        assert status_response.status_code == 200
        status_data = status_response.json()
        assert status_data["success"] is True
        assert status_data["data"]["status"] == "completed"
        assert status_data["data"]["logs"] == "Success! Optimization and Email completed."
        mock_result.assert_called_once()
