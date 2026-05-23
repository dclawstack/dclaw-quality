import pytest
from httpx import AsyncClient


# ── helpers ───────────────────────────────────────────────────────────────────

async def create_product(client, name="Prod", sku="P-INS01"):
    r = await client.post("/api/v1/products", json={"name": name, "sku": sku, "status": "active"})
    assert r.status_code == 201, r.text
    return r.json()


async def create_batch(client, product_id, batch_number="B-INS01", status="in_qa"):
    r = await client.post("/api/v1/batches", json={
        "product_id": product_id,
        "batch_number": batch_number,
        "quantity_produced": 10,
        "production_date": "2024-01-15T00:00:00",
        "status": status,
    })
    assert r.status_code == 201, r.text
    return r.json()


async def create_inspection(client, batch_id, inspector="Alice", result="pass",
                            inspection_type="visual", **kw):
    r = await client.post("/api/v1/inspections", json={
        "batch_id": batch_id,
        "inspector_name": inspector,
        "inspection_type": inspection_type,
        "result": result,
        "inspected_at": "2024-01-16T10:00:00",
        **kw,
    })
    assert r.status_code == 201, r.text
    return r.json()


# ── create ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_inspection_pass(client: AsyncClient):
    prod = await create_product(client, name="IP1", sku="IP1-001")
    batch = await create_batch(client, prod["id"], "BI-001")
    insp = await create_inspection(client, batch["id"], result="pass")
    assert insp["result"] == "pass"
    assert insp["inspector_name"] == "Alice"
    assert insp["batch_id"] == batch["id"]
    assert "id" in insp


@pytest.mark.asyncio
async def test_create_inspection_fail(client: AsyncClient):
    prod = await create_product(client, name="IP2", sku="IP2-001")
    batch = await create_batch(client, prod["id"], "BI-002")
    insp = await create_inspection(client, batch["id"], result="fail")
    assert insp["result"] == "fail"


@pytest.mark.asyncio
async def test_create_inspection_pending(client: AsyncClient):
    prod = await create_product(client, name="IP3", sku="IP3-001")
    batch = await create_batch(client, prod["id"], "BI-003")
    insp = await create_inspection(client, batch["id"], result="pending")
    assert insp["result"] == "pending"


@pytest.mark.asyncio
async def test_create_inspection_all_types(client: AsyncClient):
    prod = await create_product(client, name="IT", sku="IT-001")
    batch = await create_batch(client, prod["id"], "BI-TYPE")
    for i, itype in enumerate(["visual", "dimensional", "functional", "custom"]):
        insp = await create_inspection(client, batch["id"], inspector=f"Insp{i}",
                                       inspection_type=itype)
        assert insp["inspection_type"] == itype


@pytest.mark.asyncio
async def test_create_inspection_with_notes(client: AsyncClient):
    prod = await create_product(client, name="IN", sku="IN-001")
    batch = await create_batch(client, prod["id"], "BI-NOTE")
    insp = await create_inspection(client, batch["id"], notes="Checked under UV lamp")
    assert insp["notes"] == "Checked under UV lamp"


# ── read ──────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_inspection_by_id(client: AsyncClient):
    prod = await create_product(client, name="IG", sku="IG-001")
    batch = await create_batch(client, prod["id"], "BI-GET")
    insp = await create_inspection(client, batch["id"], inspector="Bob")
    resp = await client.get(f"/api/v1/inspections/{insp['id']}")
    assert resp.status_code == 200
    assert resp.json()["inspector_name"] == "Bob"


@pytest.mark.asyncio
async def test_get_inspection_includes_batch(client: AsyncClient):
    prod = await create_product(client, name="IBatch", sku="IB-001")
    batch = await create_batch(client, prod["id"], "BI-NEST")
    insp = await create_inspection(client, batch["id"])
    resp = await client.get(f"/api/v1/inspections/{insp['id']}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["batch"] is not None
    assert data["batch"]["id"] == batch["id"]


@pytest.mark.asyncio
async def test_get_inspection_not_found(client: AsyncClient):
    resp = await client.get("/api/v1/inspections/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_list_inspections_empty(client: AsyncClient):
    resp = await client.get("/api/v1/inspections")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_list_inspections_pagination(client: AsyncClient):
    prod = await create_product(client, name="IPag", sku="IPAG-001")
    batch = await create_batch(client, prod["id"], "BI-PAG")
    for i in range(5):
        await create_inspection(client, batch["id"], inspector=f"Inspector{i}")
    resp = await client.get("/api/v1/inspections?limit=2&skip=0")
    assert len(resp.json()) == 2
    resp2 = await client.get("/api/v1/inspections?limit=2&skip=2")
    assert len(resp2.json()) == 2


@pytest.mark.asyncio
async def test_list_inspections_filter_by_result(client: AsyncClient):
    prod = await create_product(client, name="IR", sku="IR-001")
    batch = await create_batch(client, prod["id"], "BI-RES")
    await create_inspection(client, batch["id"], inspector="Pass1", result="pass")
    await create_inspection(client, batch["id"], inspector="Fail1", result="fail")
    await create_inspection(client, batch["id"], inspector="Pend1", result="pending")

    resp = await client.get("/api/v1/inspections?result=fail")
    assert resp.status_code == 200
    data = resp.json()
    assert all(i["result"] == "fail" for i in data)
    assert len(data) == 1


@pytest.mark.asyncio
async def test_list_inspections_filter_by_batch_id(client: AsyncClient):
    prod = await create_product(client, name="IBF", sku="IBF-001")
    batch1 = await create_batch(client, prod["id"], "BI-F1")
    batch2 = await create_batch(client, prod["id"], "BI-F2")
    await create_inspection(client, batch1["id"], inspector="For1")
    await create_inspection(client, batch2["id"], inspector="For2")

    resp = await client.get(f"/api/v1/inspections?batch_id={batch1['id']}")
    assert resp.status_code == 200
    data = resp.json()
    assert all(i["batch_id"] == batch1["id"] for i in data)
    assert len(data) == 1


# ── update ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_inspection_result(client: AsyncClient):
    prod = await create_product(client, name="IU", sku="IU-001")
    batch = await create_batch(client, prod["id"], "BI-UPD")
    insp = await create_inspection(client, batch["id"], result="pending")
    resp = await client.put(f"/api/v1/inspections/{insp['id']}", json={"result": "pass"})
    assert resp.status_code == 200
    assert resp.json()["result"] == "pass"


@pytest.mark.asyncio
async def test_update_inspection_notes(client: AsyncClient):
    prod = await create_product(client, name="IUN", sku="IUN-001")
    batch = await create_batch(client, prod["id"], "BI-UNOTE")
    insp = await create_inspection(client, batch["id"])
    resp = await client.put(f"/api/v1/inspections/{insp['id']}", json={"notes": "Re-checked"})
    assert resp.status_code == 200
    assert resp.json()["notes"] == "Re-checked"


@pytest.mark.asyncio
async def test_update_inspection_not_found(client: AsyncClient):
    resp = await client.put(
        "/api/v1/inspections/00000000-0000-0000-0000-000000000000",
        json={"result": "pass"},
    )
    assert resp.status_code == 404


# ── delete ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_delete_inspection(client: AsyncClient):
    prod = await create_product(client, name="ID", sku="ID-001")
    batch = await create_batch(client, prod["id"], "BI-DEL")
    insp = await create_inspection(client, batch["id"])
    resp = await client.delete(f"/api/v1/inspections/{insp['id']}")
    assert resp.status_code == 204

    get_resp = await client.get(f"/api/v1/inspections/{insp['id']}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_inspection_not_found(client: AsyncClient):
    resp = await client.delete("/api/v1/inspections/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
