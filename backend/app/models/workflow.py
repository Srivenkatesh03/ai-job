import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String, Uuid, ForeignKey, func, Text

from app.db.session import Base


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id = Column(String, primary_key=True, index=True) # Celery task ID or custom ID
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String, nullable=False, default="pending", index=True) # pending, running, completed, failed
    task_name = Column(String, nullable=False, index=True)
    queue = Column(String, nullable=False, default="workflows", index=True)
    logs = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),
    )
