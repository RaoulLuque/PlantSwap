import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(base_url="http://plantswap-app:8000") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"message": "Healthy!"}
