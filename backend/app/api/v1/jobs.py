from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.job import Job, SavedJob
from app.schemas.auth import APIResponse
from app.schemas.job import JobRead, JobSaveRequest

router = APIRouter()


async def ensure_default_jobs(db: AsyncSession):
    """Seed default jobs for visual demonstration if database is blank."""
    result = await db.execute(select(Job))
    existing = result.scalars().all()
    if not existing:
        default_jobs = [
            Job(
                id="job-1",
                title="Senior FastAPI Backend Developer",
                company="Scalable Solutions Inc.",
                location="San Francisco, CA",
                description="Looking for an experienced engineer to build high-performance async APIs, manage Redis task brokers, and scale databases.",
                relevance_score=96,
                skills_matched=["FastAPI", "Python", "Redis", "PostgreSQL"],
                skills_gaps=["Kubernetes", "AWS EKS"],
            ),
            Job(
                id="job-2",
                title="DevOps / Infrastructure Engineer",
                company="CloudVisions Systems",
                location="Austin, TX",
                description="Manage container deployments, configure Celery worker structures, orchestrate PostgreSQL clusters, and set up Docker pipelines.",
                relevance_score=87,
                skills_matched=["Docker", "Celery", "PostgreSQL", "Redis"],
                skills_gaps=["Terraform", "Prometheus"],
            ),
            Job(
                id="job-3",
                title="Frontend React Developer",
                company="Creative Designs Studio",
                location="Remote",
                description="Construct responsive UI pages using Next.js App Router, manage application stores using Zustand, and integrate Axios API layers.",
                relevance_score=72,
                skills_matched=["Next.js", "Zustand", "TypeScript", "Tailwind CSS"],
                skills_gaps=["React Query", "Jest Component Testing"],
            ),
        ]
        db.add_all(default_jobs)
        await db.commit()


@router.get("/search", response_model=APIResponse[List[JobRead]])
async def search_jobs(
    keyword: Optional[str] = None,
    location: Optional[str] = None,
    remote: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search registered job index with dynamic matching filters."""
    await ensure_default_jobs(db)

    query = select(Job)
    if keyword:
        query = query.where(
            (Job.title.ilike(f"%{keyword}%")) |
            (Job.description.ilike(f"%{keyword}%"))
        )
    if location:
        query = query.where(Job.location.ilike(f"%{location}%"))
    if remote:
        query = query.where(Job.location.ilike("%remote%"))

    result = await db.execute(query)
    jobs = result.scalars().all()

    return APIResponse(success=True, data=[JobRead.model_validate(j) for j in jobs])


@router.post("/save", response_model=APIResponse[bool])
async def save_job(
    payload: JobSaveRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Save a job posting to user's dashboard index."""
    job_result = await db.execute(select(Job).where(Job.id == payload.job_id))
    job = job_result.scalar_one_or_none()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "error": {"code": "NOT_FOUND", "message": "Job not found"}}
        )

    # Check already saved
    existing_result = await db.execute(
        select(SavedJob).where(
            (SavedJob.user_id == current_user.id) &
            (SavedJob.job_id == payload.job_id)
        )
    )
    existing = existing_result.scalar_one_or_none()
    if not existing:
        saved = SavedJob(user_id=current_user.id, job_id=payload.job_id)
        db.add(saved)
        await db.commit()

    return APIResponse(success=True, data=True)


@router.get("/saved", response_model=APIResponse[List[JobRead]])
async def get_saved_jobs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve user's saved jobs index."""
    query = select(Job).join(SavedJob, SavedJob.job_id == Job.id).where(SavedJob.user_id == current_user.id)
    result = await db.execute(query)
    saved_jobs = result.scalars().all()

    return APIResponse(success=True, data=[JobRead.model_validate(j) for j in saved_jobs])
