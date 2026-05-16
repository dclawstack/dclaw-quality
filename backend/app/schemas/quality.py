import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


# ── Enums ──

class ProductStatus(str, Enum):
    active = "active"
    discontinued = "discontinued"


class BatchStatus(str, Enum):
    in_production = "in_production"
    in_qa = "in_qa"
    passed = "passed"
    failed = "failed"
    shipped = "shipped"


class InspectionResult(str, Enum):
    pass_ = "pass"
    fail = "fail"
    pending = "pending"


class DefectSeverity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class DefectType(str, Enum):
    surface_scratch = "surface_scratch"
    dimensional = "dimensional"
    contamination = "contamination"
    assembly = "assembly"
    cosmetic = "cosmetic"
    functional = "functional"
    other = "other"


# ── Product ──

class ProductBase(BaseModel):
    name: str
    sku: str
    description: str | None = None
    category: str | None = None
    status: ProductStatus = ProductStatus.active


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    sku: str | None = None
    description: str | None = None
    category: str | None = None
    status: ProductStatus | None = None


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# ── Batch ──

class BatchBase(BaseModel):
    product_id: uuid.UUID
    batch_number: str
    quantity_produced: int = 0
    production_date: datetime
    status: BatchStatus = BatchStatus.in_production
    notes: str | None = None


class BatchCreate(BatchBase):
    pass


class BatchUpdate(BaseModel):
    product_id: uuid.UUID | None = None
    batch_number: str | None = None
    quantity_produced: int | None = None
    production_date: datetime | None = None
    status: BatchStatus | None = None
    notes: str | None = None


class BatchOut(BatchBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class BatchWithProduct(BatchOut):
    model_config = ConfigDict(from_attributes=True)
    product: ProductOut | None = None


# ── Inspection ──

class InspectionBase(BaseModel):
    batch_id: uuid.UUID
    inspector_name: str
    inspection_type: str = "visual"
    result: InspectionResult = InspectionResult.pending
    notes: str | None = None
    inspected_at: datetime


class InspectionCreate(InspectionBase):
    pass


class InspectionUpdate(BaseModel):
    batch_id: uuid.UUID | None = None
    inspector_name: str | None = None
    inspection_type: str | None = None
    result: InspectionResult | None = None
    notes: str | None = None
    inspected_at: datetime | None = None


class InspectionOut(InspectionBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class InspectionWithBatch(InspectionOut):
    model_config = ConfigDict(from_attributes=True)
    batch: BatchWithProduct | None = None


# ── Defect ──

class DefectBase(BaseModel):
    inspection_id: uuid.UUID
    defect_type: DefectType
    severity: DefectSeverity = DefectSeverity.medium
    description: str
    quantity_affected: int = 1
    ai_suggested: bool = False
    ai_confidence: float | None = None
    recommended_action: str | None = None


class DefectCreate(DefectBase):
    pass


class DefectUpdate(BaseModel):
    inspection_id: uuid.UUID | None = None
    defect_type: DefectType | None = None
    severity: DefectSeverity | None = None
    description: str | None = None
    quantity_affected: int | None = None
    ai_suggested: bool | None = None
    ai_confidence: float | None = None
    recommended_action: str | None = None


class DefectOut(DefectBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class DefectWithInspection(DefectOut):
    model_config = ConfigDict(from_attributes=True)
    inspection: InspectionWithBatch | None = None


# ── Dashboard ──

class DashboardStats(BaseModel):
    total_inspections: int
    inspections_this_month: int
    pass_rate: float
    total_defects: int
    defects_by_severity: dict[str, int]
    batches_by_status: dict[str, int]
    top_defect_types: list[dict[str, str | int]]
    recent_inspections: list[InspectionWithBatch]
