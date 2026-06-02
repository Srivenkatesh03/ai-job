import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_optimize_resume_success(client: AsyncClient, db_session: AsyncSession):
    """Test successful resume optimization using default seeded resumes."""
    # 1. Register User & Login to get token
    user_payload = {
        "email": "ai_test@example.com",
        "password": "strongpassword123",
        "full_name": "AI User",
    }
    await client.post("/api/v1/auth/register", json=user_payload)
    
    login_response = await client.post("/api/v1/auth/login", json=user_payload)
    access_token = login_response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # 2. Get resumes to trigger auto-seeding
    get_res_response = await client.get("/api/v1/resumes", headers=headers)
    assert get_res_response.status_code == 200
    res_data = get_res_response.json()
    assert res_data["success"] is True
    assert len(res_data["data"]) == 2
    resume_id = res_data["data"][0]["id"]

    # 3. Call the optimize endpoint
    opt_payload = {
        "resume_id": resume_id,
        "target_role": "Senior Staff FastAPI Architect"
    }
    opt_response = await client.post("/api/v1/ai/resume/optimize", json=opt_payload, headers=headers)
    assert opt_response.status_code == 200
    opt_data = opt_response.json()
    assert opt_data["success"] is True
    assert opt_data["data"]["optimized_resume"] is not None
    assert opt_data["data"]["ats_score"] > 0
    assert len(opt_data["data"]["suggestions"]) > 0
