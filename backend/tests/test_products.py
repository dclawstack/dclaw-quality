import pytest
from httpx import AsyncClient


# ── helpers ───────────────────────────────────────────────────────────────────

async def create_product(client: AsyncClient, name="Widget", sku="W-001", status="active", **kw):
    payload = {"name": name, "sku": sku, "status": status, **kw}
    resp = await client.post("/api/v1/products", json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()


# ── create ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_product_minimal(client: AsyncClient):
    resp = await client.post("/api/v1/products", json={"name": "A", "sku": "A-001", "status": "active"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "A"
    assert data["sku"] == "A-001"
    assert data["status"] == "active"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_product_full(client: AsyncClient):
    payload = {
        "name": "Widget Pro",
        "sku": "WP-001",
        "description": "A premium widget",
        "category": "widgets",
        "status": "active",
    }
    resp = await client.post("/api/v1/products", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["description"] == "A premium widget"
    assert data["category"] == "widgets"


@pytest.mark.asyncio
async def test_create_product_discontinued(client: AsyncClient):
    resp = await client.post("/api/v1/products", json={"name": "Old", "sku": "OLD-001", "status": "discontinued"})
    assert resp.status_code == 201
    assert resp.json()["status"] == "discontinued"


@pytest.mark.asyncio
async def test_create_product_duplicate_sku_returns_409(client: AsyncClient):
    await create_product(client, name="First", sku="DUP-001")
    resp = await client.post("/api/v1/products", json={"name": "Second", "sku": "DUP-001", "status": "active"})
    assert resp.status_code == 409
    assert "SKU" in resp.json()["detail"]


# ── read ──────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_product_by_id(client: AsyncClient):
    product = await create_product(client, name="B", sku="B-001")
    resp = await client.get(f"/api/v1/products/{product['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == product["id"]


@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient):
    resp = await client.get("/api/v1/products/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_list_products_empty(client: AsyncClient):
    resp = await client.get("/api/v1/products")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_list_products_returns_all(client: AsyncClient):
    await create_product(client, name="P1", sku="P1-001")
    await create_product(client, name="P2", sku="P2-001")
    resp = await client.get("/api/v1/products")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
async def test_list_products_pagination(client: AsyncClient):
    for i in range(5):
        await create_product(client, name=f"Prod{i}", sku=f"PR-{i:03d}")
    resp = await client.get("/api/v1/products?limit=2&skip=0")
    assert resp.status_code == 200
    assert len(resp.json()) == 2

    resp2 = await client.get("/api/v1/products?limit=2&skip=2")
    assert resp2.status_code == 200
    assert len(resp2.json()) == 2

    ids_page1 = {p["id"] for p in resp.json()}
    ids_page2 = {p["id"] for p in resp2.json()}
    assert ids_page1.isdisjoint(ids_page2)


@pytest.mark.asyncio
async def test_list_products_search(client: AsyncClient):
    await create_product(client, name="Alpha Sensor", sku="AS-001")
    await create_product(client, name="Beta Valve", sku="BV-001")
    resp = await client.get("/api/v1/products?search=alpha")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["name"] == "Alpha Sensor"


@pytest.mark.asyncio
async def test_list_products_search_no_match(client: AsyncClient):
    await create_product(client, name="Gamma", sku="G-001")
    resp = await client.get("/api/v1/products?search=zzz")
    assert resp.status_code == 200
    assert resp.json() == []


# ── update ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_product_name(client: AsyncClient):
    product = await create_product(client, name="OldName", sku="UP-001")
    resp = await client.put(f"/api/v1/products/{product['id']}", json={"name": "NewName"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "NewName"
    assert resp.json()["sku"] == "UP-001"  # unchanged


@pytest.mark.asyncio
async def test_update_product_status(client: AsyncClient):
    product = await create_product(client, name="Active", sku="ACT-001", status="active")
    resp = await client.put(f"/api/v1/products/{product['id']}", json={"status": "discontinued"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "discontinued"


@pytest.mark.asyncio
async def test_update_product_not_found(client: AsyncClient):
    resp = await client.put(
        "/api/v1/products/00000000-0000-0000-0000-000000000000",
        json={"name": "Ghost"},
    )
    assert resp.status_code == 404


# ── delete ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient):
    product = await create_product(client, name="ToDelete", sku="DEL-001")
    resp = await client.delete(f"/api/v1/products/{product['id']}")
    assert resp.status_code == 204

    get_resp = await client.get(f"/api/v1/products/{product['id']}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_product_not_found(client: AsyncClient):
    resp = await client.delete("/api/v1/products/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
