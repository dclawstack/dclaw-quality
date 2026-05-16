import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_get_defect(client: AsyncClient):
    prod = await client.post("/api/v1/products", json={"name": "Q", "sku": "Q-001", "status": "active"})
    product_id = prod.json()["id"]
    batch = await client.post("/api/v1/batches", json={
        "product_id": product_id,
        "batch_number": "B-005",
        "quantity_produced": 10,
        "production_date": "2024-01-15T00:00:00",
        "status": "in_qa",
    })
    batch_id = batch.json()["id"]
    insp = await client.post("/api/v1/inspections", json={
        "batch_id": batch_id,
        "inspector_name": "Charlie",
        "inspection_type": "visual",
        "result": "fail",
        "inspected_at": "2024-01-16T10:00:00",
    })
    inspection_id = insp.json()["id"]
    payload = {
        "inspection_id": inspection_id,
        "defect_type": "surface_scratch",
        "severity": "low",
        "description": "Minor scratch on housing",
        "quantity_affected": 2,
    }
    resp = await client.post("/api/v1/defects", json=payload)
    assert resp.status_code == 201
    defect_id = resp.json()["id"]

    get_resp = await client.get(f"/api/v1/defects/{defect_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["description"] == "Minor scratch on housing"


@pytest.mark.asyncio
async def test_list_defects_by_severity(client: AsyncClient):
    prod = await client.post("/api/v1/products", json={"name": "QQ", "sku": "QQ-001", "status": "active"})
    product_id = prod.json()["id"]
    batch = await client.post("/api/v1/batches", json={
        "product_id": product_id,
        "batch_number": "B-006",
        "quantity_produced": 10,
        "production_date": "2024-01-15T00:00:00",
        "status": "in_qa",
    })
    batch_id = batch.json()["id"]
    insp = await client.post("/api/v1/inspections", json={
        "batch_id": batch_id,
        "inspector_name": "Dana",
        "inspection_type": "visual",
        "result": "fail",
        "inspected_at": "2024-01-16T10:00:00",
    })
    inspection_id = insp.json()["id"]
    await client.post("/api/v1/defects", json={
        "inspection_id": inspection_id,
        "defect_type": "functional",
        "severity": "critical",
        "description": "Unit does not power on",
        "quantity_affected": 1,
    })
    resp = await client.get("/api/v1/defects?severity=critical")
    assert resp.status_code == 200
    data = resp.json()
    assert any(d["severity"] == "critical" for d in data)
