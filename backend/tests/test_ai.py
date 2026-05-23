"""Tests for the AI defect classification endpoint (/api/v1/classify-defect)."""

import pytest
from httpx import AsyncClient


async def classify(client: AsyncClient, description: str):
    resp = await client.post(f"/api/v1/ai/classify-defect?description={description}")
    assert resp.status_code == 200, resp.text
    return resp.json()


# ── classification rules ──────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_classify_surface_scratch_by_scratch(client: AsyncClient):
    data = await classify(client, "There is a scratch on the surface")
    assert data["defect_type"] == "surface_scratch"
    assert data["severity"] == "low"
    assert data["ai_suggested"] is True
    assert data["ai_confidence"] == pytest.approx(0.85, abs=0.01)


@pytest.mark.asyncio
async def test_classify_surface_scratch_by_dent(client: AsyncClient):
    data = await classify(client, "Small dent found on the panel")
    assert data["defect_type"] == "surface_scratch"
    assert data["severity"] == "low"


@pytest.mark.asyncio
async def test_classify_surface_scratch_by_scuff(client: AsyncClient):
    data = await classify(client, "Scuff mark on outer casing")
    assert data["defect_type"] == "surface_scratch"


@pytest.mark.asyncio
async def test_classify_dimensional_by_dimension(client: AsyncClient):
    data = await classify(client, "Dimension is out of tolerance")
    assert data["defect_type"] == "dimensional"
    assert data["severity"] == "high"
    assert data["ai_confidence"] == pytest.approx(0.92, abs=0.01)


@pytest.mark.asyncio
async def test_classify_dimensional_by_off_spec(client: AsyncClient):
    data = await classify(client, "Part is off-spec by 0.2mm")
    assert data["defect_type"] == "dimensional"
    assert data["severity"] == "high"


@pytest.mark.asyncio
async def test_classify_dimensional_by_length(client: AsyncClient):
    data = await classify(client, "Length exceeds the limit")
    assert data["defect_type"] == "dimensional"


@pytest.mark.asyncio
async def test_classify_contamination_by_oil(client: AsyncClient):
    data = await classify(client, "Oil contamination found on the part")
    assert data["defect_type"] == "contamination"
    assert data["severity"] == "high"
    assert data["ai_confidence"] == pytest.approx(0.88, abs=0.01)


@pytest.mark.asyncio
async def test_classify_contamination_by_dirt(client: AsyncClient):
    data = await classify(client, "Dirt particles embedded in the surface")
    assert data["defect_type"] == "contamination"


@pytest.mark.asyncio
async def test_classify_contamination_by_grease(client: AsyncClient):
    data = await classify(client, "Grease residue detected")
    assert data["defect_type"] == "contamination"


@pytest.mark.asyncio
async def test_classify_assembly_by_loose(client: AsyncClient):
    data = await classify(client, "Connector is loose and not seated")
    assert data["defect_type"] == "assembly"
    assert data["severity"] == "medium"
    assert data["ai_confidence"] == pytest.approx(0.80, abs=0.01)


@pytest.mark.asyncio
async def test_classify_assembly_by_missing(client: AsyncClient):
    data = await classify(client, "Screw is missing from the assembly")
    assert data["defect_type"] == "assembly"


@pytest.mark.asyncio
async def test_classify_cosmetic_by_paint(client: AsyncClient):
    data = await classify(client, "Paint drip on the coating")
    assert data["defect_type"] == "cosmetic"
    assert data["severity"] == "low"
    assert data["ai_confidence"] == pytest.approx(0.83, abs=0.01)


@pytest.mark.asyncio
async def test_classify_cosmetic_by_color(client: AsyncClient):
    data = await classify(client, "Color mismatch on the finish")
    assert data["defect_type"] == "cosmetic"


@pytest.mark.asyncio
async def test_classify_functional_by_broken(client: AsyncClient):
    data = await classify(client, "Unit is broken and does not respond")
    assert data["defect_type"] == "functional"
    assert data["severity"] == "critical"
    assert data["ai_confidence"] == pytest.approx(0.95, abs=0.01)


@pytest.mark.asyncio
async def test_classify_functional_by_power(client: AsyncClient):
    data = await classify(client, "No power signal detected")
    assert data["defect_type"] == "functional"
    assert data["severity"] == "critical"


@pytest.mark.asyncio
async def test_classify_functional_by_failure(client: AsyncClient):
    data = await classify(client, "Performance failure under load")
    assert data["defect_type"] == "functional"


@pytest.mark.asyncio
async def test_classify_other_unknown_description(client: AsyncClient):
    data = await classify(client, "Something unusual happened during production")
    assert data["defect_type"] == "other"
    assert data["severity"] == "medium"
    assert data["ai_confidence"] == pytest.approx(0.50, abs=0.01)


# ── response shape ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_classify_response_has_required_fields(client: AsyncClient):
    data = await classify(client, "scratch on part")
    required_fields = [
        "id", "inspection_id", "defect_type", "severity",
        "description", "quantity_affected", "ai_suggested",
        "ai_confidence", "recommended_action", "created_at", "updated_at",
    ]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"


@pytest.mark.asyncio
async def test_classify_description_preserved_in_response(client: AsyncClient):
    description = "The part has a visible scratch on the top face"
    data = await classify(client, description)
    assert data["description"] == description


@pytest.mark.asyncio
async def test_classify_recommended_action_present(client: AsyncClient):
    data = await classify(client, "dimensional issue with width")
    assert data["recommended_action"] is not None
    assert len(data["recommended_action"]) > 0


@pytest.mark.asyncio
async def test_classify_ai_suggested_always_true(client: AsyncClient):
    for desc in ["scratch", "dimension", "contamination", "assembly", "paint", "broken", "unknown xyz"]:
        data = await classify(client, desc)
        assert data["ai_suggested"] is True, f"ai_suggested should be True for: {desc}"
