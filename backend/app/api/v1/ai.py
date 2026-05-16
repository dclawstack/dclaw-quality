from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.quality import DefectOut

router = APIRouter(prefix="/ai", tags=["ai"])


def _classify_defect(description: str) -> dict:
    """Rules-based defect classification engine.
    
    Maps keywords in the description to defect type, severity, and action.
    """
    d = description.lower()
    if any(word in d for word in ["scratch", "dent", "mark", "scuff"]):
        return {
            "defect_type": "surface_scratch",
            "severity": "low",
            "recommended_action": "Review polishing process; check conveyor belt for debris.",
            "confidence": 0.85,
        }
    if any(word in d for word in ["dimension", "tolerance", "size", "length", "width", "off-spec"]):
        return {
            "defect_type": "dimensional",
            "severity": "high",
            "recommended_action": "Calibrate measurement equipment; inspect tooling wear.",
            "confidence": 0.92,
        }
    if any(word in d for word in ["contamination", "dirt", "oil", "grease", "foreign"]):
        return {
            "defect_type": "contamination",
            "severity": "high",
            "recommended_action": "Review cleaning protocol; check HVAC and personnel gowning.",
            "confidence": 0.88,
        }
    if any(word in d for word in ["assemble", "fit", "mount", "loose", "missing"]):
        return {
            "defect_type": "assembly",
            "severity": "medium",
            "recommended_action": "Retrain assembly operators; update work instructions.",
            "confidence": 0.80,
        }
    if any(word in d for word in ["cosmetic", "color", "finish", "paint", "coating"]):
        return {
            "defect_type": "cosmetic",
            "severity": "low",
            "recommended_action": "Adjust spray parameters; check paint viscosity.",
            "confidence": 0.83,
        }
    if any(word in d for word in ["function", "performance", "failure", "broken", "power", "signal"]):
        return {
            "defect_type": "functional",
            "severity": "critical",
            "recommended_action": "Halt production line; initiate root-cause analysis and CAPA.",
            "confidence": 0.95,
        }
    return {
        "defect_type": "other",
        "severity": "medium",
        "recommended_action": "Investigate further; document findings.",
        "confidence": 0.50,
    }


@router.post("/classify-defect", response_model=DefectOut)
async def classify_defect(
    description: str,
    db: AsyncSession = Depends(get_db),
):
    result = _classify_defect(description)
    return DefectOut(
        id=UUID("00000000-0000-0000-0000-000000000000"),
        inspection_id=UUID("00000000-0000-0000-0000-000000000000"),
        defect_type=result["defect_type"],
        severity=result["severity"],
        description=description,
        quantity_affected=1,
        ai_suggested=True,
        ai_confidence=result["confidence"],
        recommended_action=result["recommended_action"],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
