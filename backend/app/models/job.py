import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String, Uuid, Integer, JSON, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False, index=True)
    location = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    relevance_score = Column(Integer, nullable=True)
    skills_matched = Column(JSON, nullable=True)  # array of strings
    skills_gaps = Column(JSON, nullable=True)     # array of strings

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )


class SavedJob(Base):
    __tablename__ = "saved_jobs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )

    # Relationships
    job = relationship("Job")
