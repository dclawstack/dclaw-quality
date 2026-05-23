import pytest
from httpx import AsyncClient


# ── helpers ───────────────────────────────────────────────────────────────────

async def setup_inspection(client, prod_sku="DEF-P01", batch_num="DEF-B01"):
    prod = await client.post("/api/v1/products", json={"name": prod_sku, "sku": prod_sku, "status": "active"})
    assert prod.status_code == 201, prod.text
    product_id = prod.json()["id"]

    batch = await client.post("/api/v1/batches", json={
        "product_id": product_id,
        "batch_number": batch_num,
        "quantity_produced": 10,
        "production_date": "2024-01-15T00:00:00",
        "status": "in_qa",
    })
    assert batch.status_code == 201, batch.text
    batch_id = batch.json()["id"]

    insp = await client.post("/api/v1/inspections", json={
        "batch_id": batch_id,
        "inspector_name": "Tester",
        "inspection_type": "visual",
        "result": "fail",
        "inspected_at": "2024-01-16T10:00:00",
    })
    assert insp.status_code == 201, insp.text
    return insp.json()["id"]


async def create_defect(client, inspection_id, defect_type="surface_scratch",
                        severity="low", description="Minor scratch", quantity=1, **kw):
    r = await client.post("/api/v1/defects", json={
        "inspection_id": inspection_id,
        "defect_type": defect_type,
        "severity": severity,
        "description": description,
        "quantity_affected": quantity,
        **kw,
    })
    assert r.status_code == 201, r.text
    return r.json()


# ── create ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_defect_surface_scratch(client: AsyncClient):
    insp_id = await setup_inspection(client, "DF1-P", "DF1-B")
    defect = await create_defect(client, insp_id, defect_type="surface_scratch", severity="low")
    assert defect["defect_type"] == "surface_scratch"
    assert defect["severity"] == "low"
    assert "id" in defect


@pytest.mark.asyncio
async def test_create_defect_all_types(client: AsyncClient):
    insp_id = await setup_inspection(client, "DFT-P", "DFT-B")
    defect_types = ["surface_scratch", "dimensional", "contamination",
                    "assembly", "cosmetic", "functional", "other"]
    for i, dt in enumerate(defect_types):
        defect = await create_defect(client, insp_id, defect_type=dt,
                                     description=f"Defect of type {dt}", quantity=i + 1)
        assert defect["defect_type"] == dt


@pytest.mark.asyncio
async def test_create_defect_all_severities(client: AsyncClient):
    insp_id = await setup_inspection(client, "DFS-P", "DFS-B")
    for i, sev in enumerate(["low", "medium", "high", "critical"]):
        defect = await create_defect(client, insp_id, defect_type="other",
                                     severity=sev, description=f"Severity test {sev}")
        assert defect["severity"] == sev


@pytest.mark.asyncio
async def test_create_defect_ai_suggested(client: AsyncClient):
    insp_id = await setup_inspection(client, "DFAI-P", "DFAI-B")
    defect = await create_defect(client, insp_id, ai_suggested=True,
                                 ai_confidence=0.92,
                                 recommended_action="Check tooling wear")
    assert defect["ai_suggested"] is True
    assert defect["ai_confidence"] == pytest.approx(0.92, abs=0.01)
    assert defect["recommended_action"] == "Check tooling wear"


@pytest.mark.asyncio
async def test_create_defect_quantity_affected(client: AsyncClient):
    insp_id = await setup_inspection(client, "DFQ-P", "DFQ-B")
    defect = await create_defect(client, insp_id, quantity=25)
    assert defect["quantity_affected"] == 25


# ── read ──────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_defect_by_id(client: AsyncClient):
    insp_id = await setup_inspection(client, "DFG-P", "DFG-B")
    defect = await create_defect(client, insp_id, description="Unique description")
    resp = await client.get(f"/api/v1/defects/{defect['id']}")
    assert resp.status_code == 200
    assert resp.json()["description"] == "Unique description"


@pytest.mark.asyncio
async def test_get_defect_includes_inspection(client: AsyncClient):
    insp_id = await setup_inspection(client, "DFN-P", "DFN-B")
    defect = await create_defect(client, insp_id)
    resp = await client.get(f"/api/v1/defects/{defect['id']}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["inspection"] is not None
    assert data["inspection"]["id"] == insp_id


@pytest.mark.asyncio
async def test_get_defect_not_found(client: AsyncClient):
    resp = await client.get("/api/v1/defects/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_list_defects_empty(client: AsyncClient):
    resp = await client.get("/api/v1/defects")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_list_defects_pagination(client: AsyncClient):
    insp_id = await setup_inspection(client, "DFPG-P", "DFPG-B")
    for i in range(5):
        await create_defect(client, insp_id, description=f"Defect {i}")
    resp = await client.get("/api/v1/defects?limit=2&skip=0")
    assert len(resp.json()) == 2
    resp2 = await client.get("/api/v1/defects?limit=2&skip=2")
    assert len(resp2.json()) == 2


@pytest.mark.asyncio
async def test_list_defects_filter_by_severity(client: AsyncClient):
    insp_id = await setup_inspection(client, "DFSEV-P", "DFSEV-B")
    await create_defect(client, insp_id, severity="low", description="Low defect")
    await create_defect(client, insp_id, severity="critical", description="Critical defect")

    resp = await client.get("/api/v1/defects?severity=critical")
    assert resp.status_code == 200
    data = resp.json()
    assert all(d["severity"] == "critical" for d in data)
    assert len(data) == 1


@pytest.mark.asyncio
async def test_list_defects_filter_by_defect_type(client: AsyncClient):
    insp_id = await setup_inspection(client, "DFTYPE-P", "DFTYPE-B")
    await create_defect(client, insp_id, defect_type="dimensional", description="Dim 1")
    await create_defect(client, insp_id, defect_type="cosmetic", description="Cos 1")

    resp = await client.get("/api/v1/defects?defect_type=dimensional")
    assert resp.status_code == 200
    data = resp.json()
    assert all(d["defect_type"] == "dimensional" for d in data)
    assert len(data) == 1


@pytest.mark.asyncio
async def test_list_defects_filter_by_inspection_id(client: AsyncClient):
    insp1 = await setup_inspection(client, "DFII1-P", "DFII1-B")
    insp2 = await setup_inspection(client, "DFII2-P", "DFII2-B")
    await create_defect(client, insp1, description="For inspection 1")
    await create_defect(client, insp2, description="For inspection 2")

    resp = await client.get(f"/api/v1/defects?inspection_id={insp1}")
    assert resp.status_code == 200
    data = resp.json()
    assert all(d["inspection_id"] == insp1 for d in data)
    assert len(data) == 1


# ── update ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_defect_severity(client: AsyncClient):
    insp_id = await setup_inspection(client, "DFU-P", "DFU-B")
    defect = await create_defect(client, insp_id, severity="low")
    resp = await client.put(f"/api/v1/defects/{defect['id']}", json={"severity": "high"})
    assert resp.status_code == 200
    assert resp.json()["severity"] == "high"


@pytest.mark.asyncio
async def test_update_defect_description(client: AsyncClient):
    insp_id = await setup_inspection(client, "DFUD-P", "DFUD-B")
    defect = await create_defect(client, insp_id, description="Original")
    resp = await client.put(f"/api/v1/defects/{defect['id']}", json={"description": "Updated"})
    assert resp.status_code == 200
    assert resp.json()["description"] == "Updated"


@pytest.mark.asyncio
async def test_update_defect_not_found(client: AsyncClient):
    resp = await client.put(
        "/api/v1/defects/00000000-0000-0000-0000-000000000000",
        json={"severity": "high"},
    )
    assert resp.status_code == 404


# ── delete ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_delete_defect(client: AsyncClient):
    insp_id = await setup_inspection(client, "DFDEL-P", "DFDEL-B")
    defect = await create_defect(client, insp_id, description="To be deleted")
    resp = await client.delete(f"/api/v1/defects/{defect['id']}")
    assert resp.status_code == 204

    get_resp = await client.get(f"/api/v1/defects/{defect['id']}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_defect_not_found(client: AsyncClient):
    resp = await client.delete("/api/v1/defects/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
