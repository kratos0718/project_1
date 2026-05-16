import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    response = await async_client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_submit_complaint_invalid_payload(async_client: AsyncClient):
    # Testing with missing required fields
    response = await async_client.post("/api/complaints", json={"locality": "Downtown"})
    assert response.status_code == 422
