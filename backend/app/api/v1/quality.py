import random
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class CreateReportRequest(BaseModel):
    batch_id: str
    product_spec: str


class QualityReport(BaseModel):
    id: str
    batch_id: str
    product_spec: str
    pass_rate: int
    defect_count: int
    defect_types: list[str]
    recommended_action: str
    created_at: str


class TrendScore(BaseModel):
    batch_id: str
    score: int


@router.post("/reports")
async def create_report(req: CreateReportRequest) -> QualityReport:
    return QualityReport(
        id=str(uuid.uuid4()),
        batch_id=req.batch_id,
        product_spec=req.product_spec,
        pass_rate=random.randint(85, 99),
        defect_count=random.randint(0, 12),
        defect_types=["Surface scratch"],
        recommended_action="Adjust conveyor speed",
        created_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    )


@router.get("/reports/{report_id}/trends")
async def get_report_trends(report_id: str) -> list[TrendScore]:
    return [
        TrendScore(batch_id=f"BATCH-{i+1:03d}", score=random.randint(82, 98))
        for i in range(5)
    ]
