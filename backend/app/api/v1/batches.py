from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.quality import Batch
from app.schemas.quality import BatchCreate, BatchOut, BatchUpdate, BatchWithProduct
from app.repositories.quality import BatchRepository

router = APIRouter(prefix="/batches", tags=["batches"])


@router.get("", response_model=list[BatchWithProduct])
async def list_batches(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    product_id: UUID | None = Query(None),
    status: str | None = Query(None),
):
    repo = BatchRepository(db)
    if product_id or status:
        stmt = select(Batch).offset(skip).limit(limit)
        if product_id:
            stmt = stmt.where(Batch.product_id == product_id)
        if status:
            stmt = stmt.where(Batch.status == status)
        result = await db.execute(stmt)
        return result.scalars().all()
    items, _ = await repo.list_all(limit=limit, offset=skip)
    return items


@router.post("", response_model=BatchOut, status_code=201)
async def create_batch(data: BatchCreate, db: AsyncSession = Depends(get_db)):
    repo = BatchRepository(db)
    batch = Batch(**data.model_dump())
    return await repo.create(batch)


@router.get("/{batch_id}", response_model=BatchWithProduct)
async def get_batch(batch_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = BatchRepository(db)
    batch = await repo.get_by_id(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch


@router.put("/{batch_id}", response_model=BatchOut)
async def update_batch(batch_id: UUID, data: BatchUpdate, db: AsyncSession = Depends(get_db)):
    repo = BatchRepository(db)
    batch = await repo.get_by_id(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(batch, field, value)
    await db.commit()
    await db.refresh(batch)
    return batch


@router.delete("/{batch_id}", status_code=204)
async def delete_batch(batch_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = BatchRepository(db)
    batch = await repo.get_by_id(batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    await repo.delete(batch)
    return None
