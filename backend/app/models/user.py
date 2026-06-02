import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, String, Uuid, func

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, nullable=False, default="user", index=True)
    is_active = Column(Boolean, nullable=False, default=True)
    
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
