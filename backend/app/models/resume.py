import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String, Uuid, ForeignKey, func, Text
from sqlalchemy.orm import relationship

from app.db.session import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    upload_status = Column(String, nullable=False, default="completed", index=True) # completed, processing, failed
    content = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )
