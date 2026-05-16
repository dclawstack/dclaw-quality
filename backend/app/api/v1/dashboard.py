from datetime import datetime, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.core.database import get_db
from app.models.quality import Inspection, Defect, Batch
from app.schemas.quality import DashboardStats, InspectionWithBatch

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardStats)
async def get_dashboard(db: AsyncSession = Depends(get_db)):
    # Total inspections
    total_inspections_result = await db.execute(select(func.count()).select_from(Inspection))
    total_inspections = total_inspections_result.scalar() or 0

    # Inspections this month
    now = datetime.now()
    first_of_month = datetime(now.year, now.month, 1)
    inspections_this_month_result = await db.execute(
        select(func.count()).select_from(Inspection).where(Inspection.created_at >= first_of_month)
    )
    inspections_this_month = inspections_this_month_result.scalar() or 0

    # Pass rate
    pass_count_result = await db.execute(
        select(func.count()).select_from(Inspection).where(Inspection.result == "pass")
    )
    pass_count = pass_count_result.scalar() or 0
    pass_rate = (pass_count / total_inspections * 100) if total_inspections > 0 else 0.0

    # Total defects
    total_defects_result = await db.execute(select(func.count()).select_from(Defect))
    total_defects = total_defects_result.scalar() or 0

    # Defects by severity
    severity_result = await db.execute(
        select(Defect.severity, func.count()).group_by(Defect.severity)
    )
    defects_by_severity = {severity: count for severity, count in severity_result.all()}

    # Batches by status
    batch_status_result = await db.execute(
        select(Batch.status, func.count()).group_by(Batch.status)
    )
    batches_by_status = {status: count for status, count in batch_status_result.all()}

    # Top defect types
    defect_type_result = await db.execute(
        select(Defect.defect_type, func.count())
        .group_by(Defect.defect_type)
        .order_by(func.count().desc())
        .limit(5)
    )
    top_defect_types = [{"type": dt, "count": c} for dt, c in defect_type_result.all()]

    # Recent inspections (last 30 days)
    recent_result = await db.execute(
        select(Inspection)
        .where(Inspection.created_at >= now - timedelta(days=30))
        .order_by(Inspection.created_at.desc())
        .limit(10)
    )
    recent_inspections = recent_result.scalars().all()

    return DashboardStats(
        total_inspections=total_inspections,
        inspections_this_month=inspections_this_month,
        pass_rate=round(pass_rate, 2),
        total_defects=total_defects,
        defects_by_severity=defects_by_severity,
        batches_by_status=batches_by_status,
        top_defect_types=top_defect_types,
        recent_inspections=recent_inspections,
    )
