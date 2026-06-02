import uuid
from typing import Any, Dict, Generic, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, EmailStr, Field

T = TypeVar("T")


# --- Success and Error Standard wrappers ---
class APIError(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None


class APIErrorResponse(BaseModel):
    success: bool = False
    error: APIError


# --- Auth Input/Output Schemas ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: Optional[str] = Field(None, max_length=100)


class RegisterResponseData(BaseModel):
    user_id: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponseData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 900  # 15 minutes in seconds


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
