import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_product(client: AsyncClient):
    payload = {
        "name": "Widget Pro",
        "sku": "WP-001",
        "description": "A premium widget",
        "category": "widgets",
        "status": "active",
    }
    response = await client.post("/api/v1/products", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Widget Pro"
    assert data["sku"] == "WP-001"


@pytest.mark.asyncio
async def test_list_products(client: AsyncClient):
    # create first
    await client.post("/api/v1/products", json={"name": "A", "sku": "A-001", "status": "active"})
    response = await client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_get_product(client: AsyncClient):
    create_resp = await client.post("/api/v1/products", json={"name": "B", "sku": "B-001", "status": "active"})
    product_id = create_resp.json()["id"]
    response = await client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["id"] == product_id


@pytest.mark.asyncio
async def test_update_product(client: AsyncClient):
    create_resp = await client.post("/api/v1/products", json={"name": "C", "sku": "C-001", "status": "active"})
    product_id = create_resp.json()["id"]
    response = await client.put(f"/api/v1/products/{product_id}", json={"name": "C Updated"})
    assert response.status_code == 200
    assert response.json()["name"] == "C Updated"


@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient):
    create_resp = await client.post("/api/v1/products", json={"name": "D", "sku": "D-001", "status": "active"})
    product_id = create_resp.json()["id"]
    response = await client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == 204
    get_resp = await client.get(f"/api/v1/products/{product_id}")
    assert get_resp.status_code == 404
