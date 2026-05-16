import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_get_batch(client: AsyncClient):
    # need a product first
    prod = await client.post("/api/v1/products", json={"name": "X", "sku": "X-001", "status": "active"})
    product_id = prod.json()["id"]
    payload = {
        "product_id": product_id,
        "batch_number": "B-001",
        "quantity_produced": 100,
        "production_date": "2024-01-15T00:00:00",
        "status": "in_production",
    }
    resp = await client.post("/api/v1/batches", json=payload)
    assert resp.status_code == 201
    batch_id = resp.json()["id"]

    get_resp = await client.get(f"/api/v1/batches/{batch_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["batch_number"] == "B-001"


@pytest.mark.asyncio
async def test_list_batches_with_filter(client: AsyncClient):
    prod = await client.post("/api/v1/products", json={"name": "Y", "sku": "Y-001", "status": "active"})
    product_id = prod.json()["id"]
    await client.post("/api/v1/batches", json={
        "product_id": product_id,
        "batch_number": "B-002",
        "quantity_produced": 50,
        "production_date": "2024-01-15T00:00:00",
        "status": "passed",
    })
    resp = await client.get("/api/v1/batches?status=passed")
    assert resp.status_code == 200
    data = resp.json()
    assert any(b["status"] == "passed" for b in data)
