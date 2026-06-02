import uuid
from typing import Optional, Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.auth import UserRegister


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: Union[str, uuid.UUID]) -> Optional[User]:
        """Fetch user by primary key (UUID)."""
        if isinstance(user_id, str):
            try:
                user_id = uuid.UUID(user_id)
            except ValueError:
                return None
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Fetch user by unique email."""
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def create(self, user_in: UserRegister, hashed_password: str) -> User:
        """Create a new user in the database."""
        db_user = User(
            email=user_in.email,
            password_hash=hashed_password,
            full_name=user_in.full_name,
            role="user",  # Default role for self-registered users
            is_active=True,
        )
        self.db.add(db_user)
        await self.db.flush()  # Populates db_user.id
        return db_user
