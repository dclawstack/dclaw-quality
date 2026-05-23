import pytest
from httpx import AsyncClient


# ── helpers ───────────────────────────────────────────────────────────────────

async def create_product(client: AsyncClient, name="Prod", sku="P-001"):
    resp = await client.post("/api/v1/products", json={"name": name, "sku": sku, "status": "active"})
    assert resp.status_code == 201, resp.text
    return resp.json()


async def create_batch(client: AsyncClient, product_id: str, batch_number="B-001",
                       status="in_production", quantity=100, **kw):
    payload = {
        "product_id": product_id,
        "batch_number": batch_number,
        "quantity_produced": quantity,
        "production_date": "2024-01-15T00:00:00",
        "status": status,
        **kw,
    }
    resp = await client.post("/api/v1/batches", json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()


# ── create ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_batch(client: AsyncClient):
    prod = await create_product(client, name="X", sku="X-001")
    batch = await create_batch(client, prod["id"], batch_number="B-001", status="in_production")
    assert batch["batch_number"] == "B-001"
    assert batch["status"] == "in_production"
    assert batch["product_id"] == prod["id"]
    assert "id" in batch


@pytest.mark.asyncio
async def test_create_batch_with_notes(client: AsyncClient):
    prod = await create_product(client, name="N", sku="N-001")
    batch = await create_batch(client, prod["id"], batch_number="B-N01", notes="Rush order")
    assert batch["notes"] == "Rush order"


@pytest.mark.asyncio
async def test_create_batch_all_statuses(client: AsyncClient):
    prod = await create_product(client, name="S", sku="S-001")
    for i, status in enumerate(["in_production", "in_qa", "passed", "failed", "shipped"]):
        batch = await create_batch(client, prod["id"], batch_number=f"BS-{i:03d}", status=status)
        assert batch["status"] == status


# ── read ──────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_batch_by_id(client: AsyncClient):
    prod = await create_product(client, name="G", sku="G-001")
    batch = await create_batch(client, prod["id"], batch_number="B-GET")
    resp = await client.get(f"/api/v1/batches/{batch['id']}")
    assert resp.status_code == 200
    assert resp.json()["batch_number"] == "B-GET"


@pytest.mark.asyncio
async def test_get_batch_includes_product(client: AsyncClient):
    prod = await create_product(client, name="WithProd", sku="WP-B01")
    batch = await create_batch(client, prod["id"], batch_number="B-WP")
    resp = await client.get(f"/api/v1/batches/{batch['id']}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["product"] is not None
    assert data["product"]["id"] == prod["id"]
    assert data["product"]["name"] == "WithProd"


@pytest.mark.asyncio
async def test_get_batch_not_found(client: AsyncClient):
    resp = await client.get("/api/v1/batches/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_list_batches_empty(client: AsyncClient):
    resp = await client.get("/api/v1/batches")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_list_batches_pagination(client: AsyncClient):
    prod = await create_product(client, name="Pag", sku="PAG-001")
    for i in range(5):
        await create_batch(client, prod["id"], batch_number=f"BP-{i:03d}")
    resp = await client.get("/api/v1/batches?limit=3&skip=0")
    assert len(resp.json()) == 3
    resp2 = await client.get("/api/v1/batches?limit=3&skip=3")
    assert len(resp2.json()) == 2


@pytest.mark.asyncio
async def test_list_batches_filter_by_status(client: AsyncClient):
    prod = await create_product(client, name="FS", sku="FS-001")
    await create_batch(client, prod["id"], batch_number="FS-PASS", status="passed")
    await create_batch(client, prod["id"], batch_number="FS-FAIL", status="failed")

    resp = await client.get("/api/v1/batches?status=passed")
    assert resp.status_code == 200
    data = resp.json()
    assert all(b["status"] == "passed" for b in data)
    assert any(b["batch_number"] == "FS-PASS" for b in data)


@pytest.mark.asyncio
async def test_list_batches_filter_by_product_id(client: AsyncClient):
    prod1 = await create_product(client, name="FP1", sku="FP1-001")
    prod2 = await create_product(client, name="FP2", sku="FP2-001")
    await create_batch(client, prod1["id"], batch_number="FP1-B")
    await create_batch(client, prod2["id"], batch_number="FP2-B")

    resp = await client.get(f"/api/v1/batches?product_id={prod1['id']}")
    assert resp.status_code == 200
    data = resp.json()
    assert all(b["product_id"] == prod1["id"] for b in data)
    assert len(data) == 1


# ── update ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_batch_status(client: AsyncClient):
    prod = await create_product(client, name="UB", sku="UB-001")
    batch = await create_batch(client, prod["id"], batch_number="UB-B", status="in_production")
    resp = await client.put(f"/api/v1/batches/{batch['id']}", json={"status": "in_qa"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "in_qa"


@pytest.mark.asyncio
async def test_update_batch_quantity(client: AsyncClient):
    prod = await create_product(client, name="UQ", sku="UQ-001")
    batch = await create_batch(client, prod["id"], batch_number="UQ-B", quantity=50)
    resp = await client.put(f"/api/v1/batches/{batch['id']}", json={"quantity_produced": 200})
    assert resp.status_code == 200
    assert resp.json()["quantity_produced"] == 200


@pytest.mark.asyncio
async def test_update_batch_not_found(client: AsyncClient):
    resp = await client.put(
        "/api/v1/batches/00000000-0000-0000-0000-000000000000",
        json={"status": "passed"},
    )
    assert resp.status_code == 404


# ── delete ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_delete_batch(client: AsyncClient):
    prod = await create_product(client, name="DB", sku="DB-001")
    batch = await create_batch(client, prod["id"], batch_number="DB-B")
    resp = await client.delete(f"/api/v1/batches/{batch['id']}")
    assert resp.status_code == 204

    get_resp = await client.get(f"/api/v1/batches/{batch['id']}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_batch_not_found(client: AsyncClient):
    resp = await client.delete("/api/v1/batches/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
