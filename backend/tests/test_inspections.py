import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_get_inspection(client: AsyncClient):
    prod = await client.post("/api/v1/products", json={"name": "Z", "sku": "Z-001", "status": "active"})
    product_id = prod.json()["id"]
    batch = await client.post("/api/v1/batches", json={
        "product_id": product_id,
        "batch_number": "B-003",
        "quantity_produced": 10,
        "production_date": "2024-01-15T00:00:00",
        "status": "in_qa",
    })
    batch_id = batch.json()["id"]
    payload = {
        "batch_id": batch_id,
        "inspector_name": "Alice",
        "inspection_type": "visual",
        "result": "pass",
        "inspected_at": "2024-01-16T10:00:00",
    }
    resp = await client.post("/api/v1/inspections", json=payload)
    assert resp.status_code == 201
    insp_id = resp.json()["id"]

    get_resp = await client.get(f"/api/v1/inspections/{insp_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["inspector_name"] == "Alice"


@pytest.mark.asyncio
async def test_list_inspections_by_result(client: AsyncClient):
    prod = await client.post("/api/v1/products", json={"name": "ZZ", "sku": "ZZ-001", "status": "active"})
    product_id = prod.json()["id"]
    batch = await client.post("/api/v1/batches", json={
        "product_id": product_id,
        "batch_number": "B-004",
        "quantity_produced": 10,
        "production_date": "2024-01-15T00:00:00",
        "status": "in_qa",
    })
    batch_id = batch.json()["id"]
    await client.post("/api/v1/inspections", json={
        "batch_id": batch_id,
        "inspector_name": "Bob",
        "inspection_type": "visual",
        "result": "fail",
        "inspected_at": "2024-01-16T10:00:00",
    })
    resp = await client.get("/api/v1/inspections?result=fail")
    assert resp.status_code == 200
    data = resp.json()
    assert any(i["result"] == "fail" for i in data)
