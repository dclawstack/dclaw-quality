import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check_status_ok(client: AsyncClient):
    resp = await client.get("/health/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_health_check_content_type_json(client: AsyncClient):
    resp = await client.get("/health/")
    assert "application/json" in resp.headers["content-type"]


@pytest.mark.asyncio
async def test_health_check_returns_quickly(client: AsyncClient):
    import time
    start = time.monotonic()
    resp = await client.get("/health/")
    elapsed = time.monotonic() - start
    assert resp.status_code == 200
    assert elapsed < 2.0, f"Health check too slow: {elapsed:.2f}s"
