from datetime import timedelta
from typing import Optional, Tuple
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.core.config import settings
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import UserLogin, UserRegister


class UserAlreadyExistsError(Exception):
    """Exception raised when a user email is already registered."""
    pass


class InvalidCredentialsError(Exception):
    """Exception raised when user login fails."""
    pass


class TokenError(Exception):
    """Exception raised when token decoding or verification fails."""
    pass


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def register_user(self, user_in: UserRegister) -> User:
        """Register a new user after verifying email uniqueness."""
        existing_user = await self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise UserAlreadyExistsError("A user with this email already exists.")
        
        hashed_password = security.get_password_hash(user_in.password)
        db_user = await self.user_repo.create(user_in, hashed_password)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def authenticate_user(self, login_in: UserLogin) -> Tuple[str, str, int]:
        """Authenticate a user by email and password.
        
        Returns:
            Tuple of (access_token, refresh_token, expires_in)
        """
        user = await self.user_repo.get_by_email(login_in.email)
        if not user:
            raise InvalidCredentialsError("Incorrect email or password.")
        
        if not security.verify_password(login_in.password, user.password_hash):
            raise InvalidCredentialsError("Incorrect email or password.")
            
        if not user.is_active:
            raise InvalidCredentialsError("User account is inactive.")

        access_token = security.create_access_token(user.id, user.role)
        refresh_token = security.create_refresh_token(user.id)
        
        expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        return access_token, refresh_token, expires_in

    async def refresh_access_token(self, refresh_token: str) -> Tuple[str, str, int]:
        """Verify refresh token and issue a new access/refresh token pair (token rotation)."""
        try:
            payload = security.decode_token(refresh_token)
            token_type = payload.get("type")
            if token_type != "refresh":
                raise TokenError("Invalid token type. Refresh token required.")
            
            user_id = payload.get("sub")
            if not user_id:
                raise TokenError("Subject missing from token claims.")
        except JWTError as e:
            raise TokenError("Could not validate refresh token.") from e

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise TokenError("User not found.")
            
        if not user.is_active:
            raise TokenError("User account is inactive.")

        # Issue rotated tokens
        new_access_token = security.create_access_token(user.id, user.role)
        new_refresh_token = security.create_refresh_token(user.id)
        expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        
        return new_access_token, new_refresh_token, expires_in
