# Changelog

## v1.3.0 — Quality Domain MVP

### Added

- **Real domain models** — `Product`, `Batch`, `Inspection`, `Defect` with full SQLAlchemy 2.0 relationships
- **Full CRUD REST API** for all four entities with Pydantic v2 schemas
- **Typed repositories** (`ProductRepository`, `BatchRepository`, `InspectionRepository`, `DefectRepository`)
- **Alembic migration** `bootstrap_quality_domain` with proper foreign keys and cascades
- **Dashboard API** (`GET /api/v1/dashboard`) returning real aggregated stats:
  - Total inspections, pass rate %, total defects
  - Defects by severity, batches by status, top defect types
  - Recent inspections with related batch data
- **Frontend Dashboard** — real data cards, severity bars, defect type ranking, recent inspections table
- **Frontend App Shell** — responsive sidebar navigation (Dashboard, Products, Batches, Inspections, Defects)
- **Products page** — CRUD table with search, add/edit modal, status badges
- **Batches page** — create linked to product, status-colored badges, delete
- **Inspections page** — create linked to batch, result badges, delete
- **Defects page** — log defects with severity/type filters, AI Suggest integration
- **AI Defect Classification** (`POST /api/v1/ai/classify-defect`) — rules-based engine mapping keywords to type, severity, and recommended action
- **Backend tests** covering all routers (create, list, get, update, delete) plus dashboard aggregation
- **Docker Compose** with healthchecks and correct ports (`8047` backend, `3047` frontend)

### Removed

- All random mock data endpoints (`/reports`, `/reports/{id}/trends`) replaced by real database-backed APIs

### Infrastructure

- Fixed frontend `Dockerfile` port mismatch (`3049` → `3047`)
- `.env.example` updated with real environment variables (AI, auth, database)

## v0.1.0 — Initial Scaffold

### Added
- Empty Next.js frontend and FastAPI backend scaffold
- Helm chart for Kubernetes deployment
- Basic documentation structure
- Mock dashboard endpoints (now superseded)
