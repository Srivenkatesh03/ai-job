from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.workflow import WorkflowRun
from app.schemas.auth import APIResponse
from app.schemas.workflow import WorkflowRunRead, WorkflowCreate
from app.core.celery_app import celery_app

router = APIRouter()


@router.post("", response_model=APIResponse[WorkflowRunRead])
async def create_workflow(
    payload: WorkflowCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Register a new workflow pipeline run."""
    workflow_id = f"wf-{uuid.uuid4().hex[:8]}"
    run = WorkflowRun(
        id=workflow_id,
        user_id=current_user.id,
        status="pending",
        task_name=payload.task_name,
        queue=payload.queue,
    )
    db.add(run)
    await db.commit()
    await db.refresh(run)
    return APIResponse(success=True, data=WorkflowRunRead.model_validate(run))


@router.get("", response_model=APIResponse[List[WorkflowRunRead]])
async def list_workflows(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve all workflow runs for the current user, syncing statuses with Celery."""
    result = await db.execute(
        select(WorkflowRun)
        .where(WorkflowRun.user_id == current_user.id)
        .order_by(WorkflowRun.created_at.desc())
    )
    runs = result.scalars().all()

    # Sync active/pending runs with Celery Result backend in real-time
    from celery.result import AsyncResult
    changed = False
    for run in runs:
        if run.status in ["pending", "running"]:
            try:
                celery_res = AsyncResult(run.id, app=celery_app)
                if celery_res.ready():
                    if celery_res.successful():
                        run.status = "completed"
                        run.logs = str(celery_res.result)
                    else:
                        run.status = "failed"
                        run.logs = str(celery_res.result) or str(celery_res.info)
                    changed = True
            except Exception:
                pass

    if changed:
        await db.commit()

    return APIResponse(success=True, data=[WorkflowRunRead.model_validate(r) for r in runs])


@router.post("/{workflow_id}/run", response_model=APIResponse[dict])
async def trigger_workflow(
    workflow_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Dispatch Celery canvas execution trigger to designated broker queue."""
    result = await db.execute(select(WorkflowRun).where(WorkflowRun.id == workflow_id))
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "error": {"code": "NOT_FOUND", "message": "Workflow run not found"}}
        )

    # Trigger async Celery task
    # Exposes real-time canvas coordination pipelines
    task = celery_app.send_task(
        run.task_name,
        args=["Original Resume Data...", "Senior FastAPI Backend Developer", current_user.email],
        queue=run.queue
    )

    # Sync Celery Task ID
    run.status = "running"
    run.id = task.id
    await db.commit()

    return APIResponse(success=True, data={"task_id": task.id, "status": "running"})


@router.get("/{workflow_id}/status", response_model=APIResponse[WorkflowRunRead])
async def get_workflow_status(
    workflow_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve Celery background task status from Redis broker in real-time."""
    result = await db.execute(
        select(WorkflowRun).where(
            (WorkflowRun.id == workflow_id) &
            (WorkflowRun.user_id == current_user.id)
        )
    )
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "error": {"code": "NOT_FOUND", "message": "Workflow run not found"}}
        )

    # Pull active status from Celery Result backend
    from celery.result import AsyncResult
    celery_res = AsyncResult(run.id, app=celery_app)
    if celery_res.ready():
        if celery_res.successful():
            run.status = "completed"
            run.logs = str(celery_res.result)
        else:
            run.status = "failed"
            run.logs = str(celery_res.result) or str(celery_res.info)
        await db.commit()

    return APIResponse(success=True, data=WorkflowRunRead.model_validate(run))
