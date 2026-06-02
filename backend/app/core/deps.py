from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.db.session import get_db
from app.models.user import User
from app.repositories.user import UserRepository

# OAuth2 scheme for authorization header injection
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"/api/v1/auth/login",
    auto_error=False,  # We can handle errors customly to match error format requirement
)


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """Dependency to retrieve and validate the authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "success": False,
            "error": {
                "code": "UNAUTHORIZED",
                "message": "Could not validate credentials",
            }
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception

    try:
        payload = security.decode_token(token)
        token_type = payload.get("type")
        if token_type != "access":
            raise credentials_exception
            
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise credentials_exception
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "success": False,
                "error": {
                    "code": "FORBIDDEN",
                    "message": "Inactive user account",
                }
            },
        )
        
    return user


class RoleRequired:
    """RBAC dependency to enforce list of allowed roles on an endpoint."""

    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "error": {
                        "code": "FORBIDDEN",
                        "message": "Permission denied. Elevate permissions to perform this action.",
                    }
                },
            )
        return current_user
