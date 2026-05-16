from datetime import datetime
from enum import Enum as PyEnum

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.core.utils import utc_now


class ProductStatus(str, PyEnum):
    active = "active"
    discontinued = "discontinued"


class BatchStatus(str, PyEnum):
    in_production = "in_production"
    in_qa = "in_qa"
    passed = "passed"
    failed = "failed"
    shipped = "shipped"


class InspectionResult(str, PyEnum):
    pass_ = "pass"
    fail = "fail"
    pending = "pending"


class DefectSeverity(str, PyEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class DefectType(str, PyEnum):
    surface_scratch = "surface_scratch"
    dimensional = "dimensional"
    contamination = "contamination"
    assembly = "assembly"
    cosmetic = "cosmetic"
    functional = "functional"
    other = "other"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[sa.UUID] = mapped_column(sa.UUID(as_uuid=True), primary_key=True, default=sa.func.gen_random_uuid())
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    sku: Mapped[str] = mapped_column(sa.String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    category: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)
    status: Mapped[str] = mapped_column(sa.String(20), nullable=False, default=ProductStatus.active.value)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False, default=utc_now, onupdate=utc_now)

    batches: Mapped[list["Batch"]] = relationship("Batch", back_populates="product", lazy="selectin")


class Batch(Base):
    __tablename__ = "batches"

    id: Mapped[sa.UUID] = mapped_column(sa.UUID(as_uuid=True), primary_key=True, default=sa.func.gen_random_uuid())
    product_id: Mapped[sa.UUID] = mapped_column(sa.UUID(as_uuid=True), sa.ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    batch_number: Mapped[str] = mapped_column(sa.String(100), nullable=False, unique=True)
    quantity_produced: Mapped[int] = mapped_column(sa.Integer, nullable=False, default=0)
    production_date: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False, default=utc_now)
    status: Mapped[str] = mapped_column(sa.String(20), nullable=False, default=BatchStatus.in_production.value)
    notes: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False, default=utc_now, onupdate=utc_now)

    product: Mapped["Product"] = relationship("Product", back_populates="batches", lazy="selectin")
    inspections: Mapped[list["Inspection"]] = relationship("Inspection", back_populates="batch", lazy="selectin")


class Inspection(Base):
    __tablename__ = "inspections"

    id: Mapped[sa.UUID] = mapped_column(sa.UUID(as_uuid=True), primary_key=True, default=sa.func.gen_random_uuid())
    batch_id: Mapped[sa.UUID] = mapped_column(sa.UUID(as_uuid=True), sa.ForeignKey("batches.id", ondelete="CASCADE"), nullable=False)
    inspector_name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    inspection_type: Mapped[str] = mapped_column(sa.String(100), nullable=False, default="visual")
    result: Mapped[str] = mapped_column(sa.String(20), nullable=False, default=InspectionResult.pending.value)
    notes: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    inspected_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False, default=utc_now)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False, default=utc_now, onupdate=utc_now)

    batch: Mapped["Batch"] = relationship("Batch", back_populates="inspections", lazy="selectin")
    defects: Mapped[list["Defect"]] = relationship("Defect", back_populates="inspection", lazy="selectin")


class Defect(Base):
    __tablename__ = "defects"

    id: Mapped[sa.UUID] = mapped_column(sa.UUID(as_uuid=True), primary_key=True, default=sa.func.gen_random_uuid())
    inspection_id: Mapped[sa.UUID] = mapped_column(sa.UUID(as_uuid=True), sa.ForeignKey("inspections.id", ondelete="CASCADE"), nullable=False)
    defect_type: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    severity: Mapped[str] = mapped_column(sa.String(20), nullable=False, default=DefectSeverity.medium.value)
    description: Mapped[str] = mapped_column(sa.Text, nullable=False)
    quantity_affected: Mapped[int] = mapped_column(sa.Integer, nullable=False, default=1)
    ai_suggested: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=False)
    ai_confidence: Mapped[float | None] = mapped_column(sa.Float, nullable=True)
    recommended_action: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False, default=utc_now, onupdate=utc_now)

    inspection: Mapped["Inspection"] = relationship("Inspection", back_populates="defects", lazy="selectin")
