import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.models.user import User


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient, db_session: AsyncSession):
    """Test successful user registration."""
    payload = {
        "email": "register_test@example.com",
        "password": "strongpassword123",
        "full_name": "Test User",
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "User registered successfully"
    assert "user_id" in data["data"]
    
    # Confirm user exists in the database
    result = await db_session.execute(
        select(User).filter(User.email == "register_test@example.com")
    )
    user = result.scalars().first()
    assert user is not None
    assert user.full_name == "Test User"
    assert user.role == "user"
    assert user.is_active is True


@pytest.mark.asyncio
async def test_register_user_duplicate_email(client: AsyncClient):
    """Test registering a user with an already existing email."""
    payload = {
        "email": "duplicate@example.com",
        "password": "strongpassword123",
        "full_name": "Original User",
    }
    # Register first user
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201

    # Attempt to register second user with same email
    payload["full_name"] = "Duplicate User"
    response2 = await client.post("/api/v1/auth/register", json=payload)
    assert response2.status_code == 409
    
    data2 = response2.json()
    assert data2["success"] is False
    assert data2["error"]["code"] == "USER_ALREADY_EXISTS"


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Test successful login returns access and refresh tokens."""
    # Register first
    payload = {
        "email": "login_test@example.com",
        "password": "strongpassword123",
        "full_name": "Login User",
    }
    await client.post("/api/v1/auth/register", json=payload)

    # Perform login
    login_payload = {
        "email": "login_test@example.com",
        "password": "strongpassword123",
    }
    response = await client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]
    assert data["data"]["expires_in"] == 900


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test login with incorrect password or unregistered email."""
    # Register first
    payload = {
        "email": "login_fail@example.com",
        "password": "strongpassword123",
    }
    await client.post("/api/v1/auth/register", json=payload)

    # Incorrect password
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "login_fail@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["success"] is False
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"

    # Unregistered email
    response2 = await client.post(
        "/api/v1/auth/login",
        json={"email": "nonexistent@example.com", "password": "somepassword"},
    )
    assert response2.status_code == 401
    assert response2.json()["success"] is False


@pytest.mark.asyncio
async def test_refresh_token_success(client: AsyncClient):
    """Test rotating tokens via refresh endpoint."""
    # Register & Login to get tokens
    payload = {
        "email": "refresh_test@example.com",
        "password": "strongpassword123",
    }
    await client.post("/api/v1/auth/register", json=payload)
    
    login_response = await client.post("/api/v1/auth/login", json=payload)
    refresh_token = login_response.json()["data"]["refresh_token"]

    # Exchange refresh token
    response = await client.post(
        "/api/v1/auth/refresh", json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]


@pytest.mark.asyncio
async def test_refresh_token_invalid(client: AsyncClient):
    """Test refresh endpoint with malformed or expired refresh token."""
    response = await client.post(
        "/api/v1/auth/refresh", json={"refresh_token": "invalid_token_signature"}
    )
    assert response.status_code == 401
    assert response.json()["success"] is False
    assert response.json()["error"]["code"] == "INVALID_TOKEN"


@pytest.mark.asyncio
async def test_get_current_user_profile(client: AsyncClient):
    """Test retrieval of authenticated profile details using bearer access token."""
    payload = {
        "email": "profile_test@example.com",
        "password": "strongpassword123",
        "full_name": "Profile User",
    }
    await client.post("/api/v1/auth/register", json=payload)
    
    login_response = await client.post("/api/v1/auth/login", json=payload)
    access_token = login_response.json()["data"]["access_token"]

    # Access /me route
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "profile_test@example.com"
    assert data["data"]["full_name"] == "Profile User"
    assert data["data"]["role"] == "user"


@pytest.mark.asyncio
async def test_rbac_middleware_user_denied_admin(client: AsyncClient):
    """Test standard user is denied access to admin-only endpoints."""
    payload = {
        "email": "user_role_test@example.com",
        "password": "strongpassword123",
    }
    await client.post("/api/v1/auth/register", json=payload)
    
    login_response = await client.post("/api/v1/auth/login", json=payload)
    access_token = login_response.json()["data"]["access_token"]

    # Try admin endpoint
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.get("/api/v1/auth/admin-only", headers=headers)
    assert response.status_code == 403
    
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "FORBIDDEN"
    assert "Permission denied" in data["error"]["message"]


@pytest.mark.asyncio
async def test_rbac_middleware_admin_allowed(client: AsyncClient, db_session: AsyncSession):
    """Test user with admin role is allowed access to admin-only endpoints."""
    # Register standard user
    payload = {
        "email": "admin_role_test@example.com",
        "password": "strongpassword123",
    }
    await client.post("/api/v1/auth/register", json=payload)
    
    # Manually promote user to admin role in database
    result = await db_session.execute(
        select(User).filter(User.email == "admin_role_test@example.com")
    )
    user = result.scalars().first()
    user.role = "admin"
    await db_session.commit()

    # Login to get new JWT token containing the admin role claim
    login_response = await client.post("/api/v1/auth/login", json=payload)
    access_token = login_response.json()["data"]["access_token"]

    # Try admin endpoint with admin token
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.get("/api/v1/auth/admin-only", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert data["data"]["role"] == "admin"
    assert data["message"] == "Hello Admin!"
