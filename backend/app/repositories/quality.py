from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quality import Product, Batch, Inspection, Defect
from app.repositories.base_repo import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Product)


class BatchRepository(BaseRepository[Batch]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Batch)


class InspectionRepository(BaseRepository[Inspection]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Inspection)


class DefectRepository(BaseRepository[Defect]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Defect)
