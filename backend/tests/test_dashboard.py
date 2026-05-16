import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_dashboard(client: AsyncClient):
    # seed data
    prod = await client.post("/api/v1/products", json={"name": "Dash", "sku": "D-001", "status": "active"})
    product_id = prod.json()["id"]
    batch = await client.post("/api/v1/batches", json={
        "product_id": product_id,
        "batch_number": "B-DASH",
        "quantity_produced": 10,
        "production_date": "2024-01-15T00:00:00",
        "status": "in_qa",
    })
    batch_id = batch.json()["id"]
    insp = await client.post("/api/v1/inspections", json={
        "batch_id": batch_id,
        "inspector_name": "Eve",
        "inspection_type": "visual",
        "result": "pass",
        "inspected_at": "2024-01-16T10:00:00",
    })
    inspection_id = insp.json()["id"]
    await client.post("/api/v1/defects", json={
        "inspection_id": inspection_id,
        "defect_type": "surface_scratch",
        "severity": "low",
        "description": "Tiny scratch",
        "quantity_affected": 1,
    })

    resp = await client.get("/api/v1/dashboard")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_inspections" in data
    assert "pass_rate" in data
    assert "total_defects" in data
    assert "defects_by_severity" in data
    assert "batches_by_status" in data
    assert "recent_inspections" in data
