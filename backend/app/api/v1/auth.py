from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, get_current_user, RoleRequired
from app.models.user import User
from app.schemas.auth import (
    APIResponse,
    RegisterResponseData,
    TokenRefreshRequest,
    TokenResponseData,
    UserLogin,
    UserRead,
    UserRegister,
)
from app.services.auth_service import (
    AuthService,
    InvalidCredentialsError,
    TokenError,
    UserAlreadyExistsError,
)

router = APIRouter()


@router.post(
    "/register",
    response_model=APIResponse[RegisterResponseData],
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_in: UserRegister, db: AsyncSession = Depends(get_db)
) -> APIResponse[RegisterResponseData]:
    """Register a new user account."""
    auth_service = AuthService(db)
    try:
        user = await auth_service.register_user(user_in)
        return APIResponse(
            success=True,
            message="User registered successfully",
            data=RegisterResponseData(user_id=str(user.id)),
        )
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "success": False,
                "error": {
                    "code": "USER_ALREADY_EXISTS",
                    "message": str(e),
                }
            },
        )


@router.post("/login", response_model=APIResponse[TokenResponseData])
async def login(
    login_in: UserLogin, db: AsyncSession = Depends(get_db)
) -> APIResponse[TokenResponseData]:
    """Authenticate credentials and return session tokens."""
    auth_service = AuthService(db)
    try:
        access_token, refresh_token, expires_in = await auth_service.authenticate_user(
            login_in
        )
        return APIResponse(
            success=True,
            message="Login successful",
            data=TokenResponseData(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=expires_in,
            ),
        )
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": str(e),
                }
            },
        )


@router.post("/refresh", response_model=APIResponse[TokenResponseData])
async def refresh(
    refresh_in: TokenRefreshRequest, db: AsyncSession = Depends(get_db)
) -> APIResponse[TokenResponseData]:
    """Exchange a valid refresh token for a rotated access/refresh token pair."""
    auth_service = AuthService(db)
    try:
        access_token, refresh_token, expires_in = await auth_service.refresh_access_token(
            refresh_in.refresh_token
        )
        return APIResponse(
            success=True,
            message="Tokens refreshed successfully",
            data=TokenResponseData(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=expires_in,
            ),
        )
    except TokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": str(e),
                }
            },
        )


@router.get("/me", response_model=APIResponse[UserRead])
async def get_me(
    current_user: User = Depends(get_current_user),
) -> APIResponse[UserRead]:
    """Retrieve the current authenticated user profile details."""
    return APIResponse(
        success=True,
        message="Profile retrieved successfully",
        data=UserRead.model_validate(current_user),
    )


@router.get(
    "/admin-only",
    response_model=APIResponse[UserRead],
    dependencies=[Depends(RoleRequired(["admin"]))],
)
async def admin_only_endpoint(
    current_user: User = Depends(get_current_user),
) -> APIResponse[UserRead]:
    """Endpoint accessible only by users with the admin role."""
    return APIResponse(
        success=True,
        message="Hello Admin!",
        data=UserRead.model_validate(current_user),
    )
