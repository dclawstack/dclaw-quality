"""Tests for the dashboard stats endpoint (/api/v1/dashboard)."""

import pytest
from httpx import AsyncClient


# ── helpers ───────────────────────────────────────────────────────────────────

async def seed_chain(client, prod_sku, batch_num, inspector, result,
                     defect_type=None, severity=None):
    """Create product → batch → inspection → optional defect and return IDs."""
    prod = await client.post("/api/v1/products", json={"name": prod_sku, "sku": prod_sku, "status": "active"})
    assert prod.status_code == 201
    product_id = prod.json()["id"]

    batch = await client.post("/api/v1/batches", json={
        "product_id": product_id,
        "batch_number": batch_num,
        "quantity_produced": 10,
        "production_date": "2024-01-15T00:00:00",
        "status": "in_qa",
    })
    assert batch.status_code == 201
    batch_id = batch.json()["id"]

    insp = await client.post("/api/v1/inspections", json={
        "batch_id": batch_id,
        "inspector_name": inspector,
        "inspection_type": "visual",
        "result": result,
        "inspected_at": "2024-01-16T10:00:00",
    })
    assert insp.status_code == 201
    inspection_id = insp.json()["id"]

    if defect_type:
        defect = await client.post("/api/v1/defects", json={
            "inspection_id": inspection_id,
            "defect_type": defect_type,
            "severity": severity or "medium",
            "description": f"Defect for {batch_num}",
            "quantity_affected": 1,
        })
        assert defect.status_code == 201

    return product_id, batch_id, inspection_id


# ── empty state ───────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_dashboard_empty_database(client: AsyncClient):
    resp = await client.get("/api/v1/dashboard")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_inspections"] == 0
    assert data["total_defects"] == 0
    assert data["pass_rate"] == 0.0
    assert data["defects_by_severity"] == {}
    assert data["batches_by_status"] == {}
    assert data["top_defect_types"] == []
    assert data["recent_inspections"] == []


# ── response schema ───────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_dashboard_response_shape(client: AsyncClient):
    await seed_chain(client, "DS-P1", "DS-B1", "Eve", "pass")
    resp = await client.get("/api/v1/dashboard")
    assert resp.status_code == 200
    data = resp.json()
    required = [
        "total_inspections", "inspections_this_month", "pass_rate",
        "total_defects", "defects_by_severity", "batches_by_status",
        "top_defect_types", "recent_inspections",
    ]
    for field in required:
        assert field in data, f"Missing field: {field}"


# ── total_inspections ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_dashboard_total_inspections_count(client: AsyncClient):
    await seed_chain(client, "TI-P1", "TI-B1", "Insp1", "pass")
    await seed_chain(client, "TI-P2", "TI-B2", "Insp2", "fail")
    await seed_chain(client, "TI-P3", "TI-B3", "Insp3", "pending")

    resp = await client.get("/api/v1/dashboard")
    assert resp.json()["total_inspections"] == 3


# ── pass_rate ─────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_dashboard_pass_rate_all_pass(client: AsyncClient):
    await seed_chain(client, "PR-P1", "PR-B1", "I1", "pass")
    await seed_chain(client, "PR-P2", "PR-B2", "I2", "pass")
    data = (await client.get("/api/v1/dashboard")).json()
    assert data["pass_rate"] == pytest.approx(100.0, abs=0.1)


@pytest.mark.asyncio
async def test_dashboard_pass_rate_none_pass(client: AsyncClient):
    await seed_chain(client, "PR2-P1", "PR2-B1", "I1", "fail")
    await seed_chain(client, "PR2-P2", "PR2-B2", "I2", "fail")
    data = (await client.get("/api/v1/dashboard")).json()
    assert data["pass_rate"] == pytest.approx(0.0, abs=0.1)


@pytest.mark.asyncio
async def test_dashboard_pass_rate_mixed(client: AsyncClient):
    # 2 pass, 2 fail → 50%
    await seed_chain(client, "PR3-P1", "PR3-B1", "I1", "pass")
    await seed_chain(client, "PR3-P2", "PR3-B2", "I2", "pass")
    await seed_chain(client, "PR3-P3", "PR3-B3", "I3", "fail")
    await seed_chain(client, "PR3-P4", "PR3-B4", "I4", "fail")
    data = (await client.get("/api/v1/dashboard")).json()
    assert data["pass_rate"] == pytest.approx(50.0, abs=0.1)


# ── total_defects ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_dashboard_total_defects(client: AsyncClient):
    await seed_chain(client, "TD-P1", "TD-B1", "I1", "fail",
                     defect_type="surface_scratch", severity="low")
    await seed_chain(client, "TD-P2", "TD-B2", "I2", "fail",
                     defect_type="functional", severity="critical")
    data = (await client.get("/api/v1/dashboard")).json()
    assert data["total_defects"] == 2


# ── defects_by_severity ───────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_dashboard_defects_by_severity_breakdown(client: AsyncClient):
    await seed_chain(client, "DS1-P", "DS1-B", "I1", "fail",
                     defect_type="surface_scratch", severity="low")
    await seed_chain(client, "DS2-P", "DS2-B", "I2", "fail",
                     defect_type="contamination", severity="high")
    await seed_chain(client, "DS3-P", "DS3-B", "I3", "fail",
                     defect_type="functional", severity="critical")
    data = (await client.get("/api/v1/dashboard")).json()
    sev = data["defects_by_severity"]
    assert sev.get("low") == 1
    assert sev.get("high") == 1
    assert sev.get("critical") == 1


# ── batches_by_status ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_dashboard_batches_by_status(client: AsyncClient):
    prod = await client.post("/api/v1/products", json={"name": "BST", "sku": "BST-001", "status": "active"})
    pid = prod.json()["id"]
    for i, status in enumerate(["in_production", "passed", "passed"]):
        await client.post("/api/v1/batches", json={
            "product_id": pid,
            "batch_number": f"BST-B{i}",
            "quantity_produced": 10,
            "production_date": "2024-01-15T00:00:00",
            "status": status,
        })
    data = (await client.get("/api/v1/dashboard")).json()
    bbs = data["batches_by_status"]
    assert bbs.get("in_production") == 1
    assert bbs.get("passed") == 2


# ── top_defect_types ──────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_dashboard_top_defect_types_ordering(client: AsyncClient):
    # Create 3 functional defects and 1 cosmetic — functional should rank first
    insp_ids = []
    for i in range(4):
        _, _, iid = await seed_chain(client, f"TDT-P{i}", f"TDT-B{i}", f"I{i}", "fail")
        insp_ids.append(iid)

    for iid in insp_ids[:3]:
        await client.post("/api/v1/defects", json={
            "inspection_id": iid,
            "defect_type": "functional",
            "severity": "critical",
            "description": "Functional failure",
            "quantity_affected": 1,
        })
    await client.post("/api/v1/defects", json={
        "inspection_id": insp_ids[3],
        "defect_type": "cosmetic",
        "severity": "low",
        "description": "Cosmetic issue",
        "quantity_affected": 1,
    })

    data = (await client.get("/api/v1/dashboard")).json()
    types = data["top_defect_types"]
    assert len(types) >= 1
    assert types[0]["type"] == "functional"
    assert types[0]["count"] == 3


# ── recent_inspections ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_dashboard_recent_inspections_present(client: AsyncClient):
    await seed_chain(client, "RI-P1", "RI-B1", "Inspector X", "pass")
    data = (await client.get("/api/v1/dashboard")).json()
    assert len(data["recent_inspections"]) >= 1
    assert data["recent_inspections"][0]["inspector_name"] == "Inspector X"
