from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.quality import Inspection
from app.schemas.quality import InspectionCreate, InspectionOut, InspectionUpdate, InspectionWithBatch
from app.repositories.quality import InspectionRepository

router = APIRouter(prefix="/inspections", tags=["inspections"])


@router.get("", response_model=list[InspectionWithBatch])
async def list_inspections(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    batch_id: UUID | None = Query(None),
    result: str | None = Query(None),
):
    repo = InspectionRepository(db)
    if batch_id or result:
        stmt = select(Inspection).offset(skip).limit(limit)
        if batch_id:
            stmt = stmt.where(Inspection.batch_id == batch_id)
        if result:
            stmt = stmt.where(Inspection.result == result)
        result_obj = await db.execute(stmt)
        return result_obj.scalars().all()
    items, _ = await repo.list_all(limit=limit, offset=skip)
    return items


@router.post("", response_model=InspectionOut, status_code=201)
async def create_inspection(data: InspectionCreate, db: AsyncSession = Depends(get_db)):
    repo = InspectionRepository(db)
    inspection = Inspection(**data.model_dump())
    return await repo.create(inspection)


@router.get("/{inspection_id}", response_model=InspectionWithBatch)
async def get_inspection(inspection_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = InspectionRepository(db)
    inspection = await repo.get_by_id(inspection_id)
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    return inspection


@router.put("/{inspection_id}", response_model=InspectionOut)
async def update_inspection(inspection_id: UUID, data: InspectionUpdate, db: AsyncSession = Depends(get_db)):
    repo = InspectionRepository(db)
    inspection = await repo.get_by_id(inspection_id)
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(inspection, field, value)
    await db.commit()
    await db.refresh(inspection)
    return inspection


@router.delete("/{inspection_id}", status_code=204)
async def delete_inspection(inspection_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = InspectionRepository(db)
    inspection = await repo.get_by_id(inspection_id)
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    await repo.delete(inspection)
    return None
