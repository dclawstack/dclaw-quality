from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.quality import Defect
from app.schemas.quality import DefectCreate, DefectOut, DefectUpdate, DefectWithInspection
from app.repositories.quality import DefectRepository

router = APIRouter(prefix="/defects", tags=["defects"])


@router.get("", response_model=list[DefectWithInspection])
async def list_defects(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    inspection_id: UUID | None = Query(None),
    severity: str | None = Query(None),
    defect_type: str | None = Query(None),
):
    repo = DefectRepository(db)
    if inspection_id or severity or defect_type:
        stmt = select(Defect).offset(skip).limit(limit)
        if inspection_id:
            stmt = stmt.where(Defect.inspection_id == inspection_id)
        if severity:
            stmt = stmt.where(Defect.severity == severity)
        if defect_type:
            stmt = stmt.where(Defect.defect_type == defect_type)
        result = await db.execute(stmt)
        return result.scalars().all()
    items, _ = await repo.list_all(limit=limit, offset=skip)
    return items


@router.post("", response_model=DefectOut, status_code=201)
async def create_defect(data: DefectCreate, db: AsyncSession = Depends(get_db)):
    repo = DefectRepository(db)
    defect = Defect(**data.model_dump())
    return await repo.create(defect)


@router.get("/{defect_id}", response_model=DefectWithInspection)
async def get_defect(defect_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = DefectRepository(db)
    defect = await repo.get_by_id(defect_id)
    if not defect:
        raise HTTPException(status_code=404, detail="Defect not found")
    return defect


@router.put("/{defect_id}", response_model=DefectOut)
async def update_defect(defect_id: UUID, data: DefectUpdate, db: AsyncSession = Depends(get_db)):
    repo = DefectRepository(db)
    defect = await repo.get_by_id(defect_id)
    if not defect:
        raise HTTPException(status_code=404, detail="Defect not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(defect, field, value)
    await db.commit()
    await db.refresh(defect)
    return defect


@router.delete("/{defect_id}", status_code=204)
async def delete_defect(defect_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = DefectRepository(db)
    defect = await repo.get_by_id(defect_id)
    if not defect:
        raise HTTPException(status_code=404, detail="Defect not found")
    await repo.delete(defect)
    return None
