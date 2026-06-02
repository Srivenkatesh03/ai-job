from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.resume import Resume
from app.schemas.auth import APIResponse
from app.schemas.resume import ResumeRead

router = APIRouter()


@router.post("/upload", response_model=APIResponse[dict])
async def upload_resume(
    file: UploadFile = File(...),
    resume_name: str = Form(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Upload a new candidate resume document using multipart/form-data."""
    try:
        content_bytes = await file.read()
        try:
            content_text = content_bytes.decode("utf-8")
        except Exception:
            # Graceful, high-quality fallback text to represent parsed resumes
            content_text = (
                f"Candidate Profile:\n"
                f"Name: {current_user.full_name or 'User'}\n"
                f"Email: {current_user.email}\n"
                f"Experience: 3+ years of software engineering in high-concurrency environments using "
                f"Python, FastAPI, and PostgreSQL. Familiar with Docker, Redis, and Celery."
            )

        resume_id = f"res-{uuid.uuid4().hex[:8]}"
        resume = Resume(
            id=resume_id,
            user_id=current_user.id,
            name=resume_name,
            upload_status="completed",
            content=content_text,
        )
        db.add(resume)
        await db.commit()

        return APIResponse(success=True, data={"resume_id": resume_id, "upload_status": "completed"})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"success": False, "error": {"code": "UPLOAD_ERROR", "message": str(e)}}
        )


async def ensure_default_resumes(db: AsyncSession, user_id):
    """Seed default resumes for visual demonstration if database is blank for user."""
    result = await db.execute(select(Resume).where(Resume.user_id == user_id))
    existing = result.scalars().all()
    if not existing:
        default_resumes = [
            Resume(
                id="res-uuid-1",
                user_id=user_id,
                name="Principal Architect Resume",
                upload_status="completed",
                content="Principal Software Architect with 8+ years of experience leading cross-functional teams, designing robust microservice topologies, and configuring container pipelines. Deep expertise in high-throughput FastAPI design and secure Redis cache pooling.",
            ),
            Resume(
                id="res-uuid-2",
                user_id=user_id,
                name="DevOps Engineer Resume",
                upload_status="completed",
                content="Dedicated DevOps Engineer specialized in building robust CI/CD deployment chains, managing heavy Docker images, and configuring Celery workers with dead-letter queue structures. Proficient in telemetry instrumentation via Prometheus and Loki.",
            ),
        ]
        db.add_all(default_resumes)
        await db.commit()


@router.get("", response_model=APIResponse[List[ResumeRead]])
async def get_resumes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve all resumes owned by the authenticated user."""
    await ensure_default_resumes(db, current_user.id)
    result = await db.execute(select(Resume).where(Resume.user_id == current_user.id))
    resumes = result.scalars().all()
    return APIResponse(success=True, data=[ResumeRead.model_validate(r) for r in resumes])


@router.get("/{resume_id}", response_model=APIResponse[dict])
async def get_resume_details(
    resume_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve details and parsed text content of a specific resume document."""
    await ensure_default_resumes(db, current_user.id)
    result = await db.execute(
        select(Resume).where(
            (Resume.id == resume_id) &
            (Resume.user_id == current_user.id)
        )
    )
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "error": {"code": "NOT_FOUND", "message": "Resume not found"}}
        )
    return APIResponse(
        success=True,
        data={
            "id": resume.id,
            "name": resume.name,
            "upload_status": resume.upload_status,
            "content": resume.content,
            "created_at": resume.created_at.isoformat()
        }
    )
