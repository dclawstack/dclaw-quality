# DClaw Quality — Strategic Plan v1.3

> **Authored:** 2026-05-16  
> **Based on audit of:** scaffold-based DClaw Quality app (backend port 8047, frontend port 3047)  
> **Repository:** `dclawstack/dclaw-quality`

---

## 1. Current State Inventory

### What's Working
- ✅ FastAPI skeleton with `lifespan`, CORS, healthcheck
- ✅ SQLAlchemy 2.0 + `DeclarativeBase` from `app.models.base`
- ✅ `BaseRepository` generic CRUD pattern
- ✅ `get_db` dependency injection + async sessions
- ✅ Next.js 14 frontend with Tailwind + pre-built UI components
- ✅ Docker Compose with PostgreSQL, backend, frontend
- ✅ pytest test harness with `pytest-asyncio==0.24.0`
- ✅ Alembic scaffold configured
- ✅ GitHub Actions CI present

### What's Broken / Missing
- ❌ **MOCK DATA** — `quality.py` generates random `pass_rate` / `defect_count` via `random.randint()`
- ❌ **NO REAL MODELS** — `app/models/` only contains `base.py`; zero domain entities
- ❌ **NO REAL SCHEMAS** — `app/schemas/__init__.py` is empty
- ❌ **NO REAL REPOSITORIES** — `app/repositories/__init__.py` is empty
- ❌ **NO ALEMBIC MIGRATIONS** — `versions/` directory has only `.gitkeep`
- ❌ **NO BACKEND TESTS** — only `test_health.py` exists; zero domain tests
- ❌ **PORT MISMATCH** — `docker-compose.yml` uses `8135:8135` / `3049:3049` but `AGENTS.md` specifies `8047` / `3047`
- ❌ **Frontend only mocks** — `dashboard/page.tsx` calls `/reports` and `/reports/{id}/trends` which are random-number endpoints
- ❌ **No navigation shell** — single-page app with no routing structure
- ❌ `.env.example` uses `localhost:8135` but should be `localhost:8047`

---

## 2. Y Combinator Gap Analysis

### 2.1 What YC Looks For
YC evaluates startups on: **(a)** hair-on-fire problem, **(b)** rapid execution, **(c)** defensibility, **(d)** market size, **(e)** team velocity.

### 2.2 Competitive Landscape
| Competitor | Pricing | Weakness |
|-----------|---------|----------|
| **MasterControl** | $$$$ (enterprise) | Bloated, 6-month implementation |
| **EtQ Reliance** | $$$$ | On-prem legacy, poor UX |
| **Qualio** | $$$ (life-science only) | Narrow vertical, limited flexibility |
| **Intellect** | $$ | Weak reporting, no AI features |
| **Spreadsheets / SharePoint** | $ | Zero traceability, manual everything |

### 2.3 Hair-on-Fire Problem Statement
> *"Quality teams in mid-market manufacturers (100–2,000 employees) are stuck between expensive enterprise QMS suites ($50K+/year, 6-month onboarding) and fragile spreadsheet workflows. They need a modern, affordable quality platform that works in days, not quarters — with AI-assisted defect analysis and real-time SPC dashboards."*

### 2.4 Gaps vs. YC Standard

| Dimension | Current State | YC Standard | Gap |
|-----------|--------------|-------------|-----|
| **Product** | Empty scaffold with random mock data | Working MVP with real CRUD + 2+ screens | 🔴 Massive |
| **AI Differentiation** | None | AI-powered defect classification, win-probability | 🔴 Massive |
| **UX Polish** | Single dashboard page with raw inputs | Kanban, tables, modals, search, filters | 🔴 Large |
| **Domain Depth** | Zero entities defined | Product → Batch → Inspection → Defect → CAPA chain | 🔴 Large |
| **Data Integrity** | Random numbers | Audit trails, traceability, version history | 🔴 Large |
| **Scalability** | Single-table design | Normalized schema, indexed search, pagination | 🟡 Medium |
| **Dev Velocity** | Scaffold only | 70%+ test coverage, CI green, Docker ready | 🟡 Medium |
| **Go-to-Market** | None | In-app onboarding, demo data, public API docs | 🟡 Medium |

### 2.5 What Will Make This Stand Out to YC
1. **AI Defect Copilot** — Upload an inspection photo or description; AI suggests defect classification, severity, and corrective action.
2. **Real-Time SPC Charts** — Statistical Process Control with control limits, Cpk calculations, trend alerts (auto-generated on the frontend).
3. **Supplier Quality Scorecards** — Aggregate defect rates, on-time delivery, and PPM (parts per million) by supplier.
4. **CAPA Workflow Engine** — Corrective / Preventive Action with approval routing, due dates, and effectiveness verification.
5. **Zero-to-Value in 48 Hours** — Self-serve onboarding with demo templates so a quality manager can go from signup to first inspection report in under 5 minutes.

---

## 3. Strategic Feature Roadmap — Plan v1.3

### Complexity Legend
- **0** — Low complexity / Core foundational (Quick wins: 1–2 hours each)
- **1** — Medium complexity / Core differentiators (4–8 hours each)
- **2** — High complexity / Advanced features (12–24 hours each)

### P0 — Must Have (Foundational)

#### [0] Fix Infrastructure Mismatch
- Fix ports in `docker-compose.yml`: `8135` → `8047`, `3049` → `3047`
- Fix `.env.example`: `localhost:8135` → `localhost:8047`
- Fix `frontend/package.json` dev port: `3049` → `3047`
- Fix backend `Dockerfile` env `PORT=8135` → `8047` and expose `8047`
- Fix `AGENTS.md` / `README.md` references if any

#### [0] Bootstrap Domain Models (SQLAlchemy)
Create real entities that replace the mock:
- `Product` — id, name, sku, description, category, active, created_at, updated_at
- `Batch` — id, product_id (FK), batch_number, quantity_produced, production_date, status, created_at, updated_at
- `Inspection` — id, batch_id (FK), inspector_name, inspection_type, result, notes, inspected_at, created_at, updated_at
- `Defect` — id, inspection_id (FK), defect_type, severity, description, quantity_affected, created_at, updated_at
- `QualityStandard` — id, name, version, description, acceptable_ppm, created_at, updated_at

#### [0] Create Pydantic v2 Schemas
- `ProductCreate`, `ProductUpdate`, `ProductOut`, `ProductList`
- `BatchCreate`, `BatchUpdate`, `BatchOut`, `BatchList`
- `InspectionCreate`, `InspectionUpdate`, `InspectionOut`, `InspectionList`
- `DefectCreate`, `DefectUpdate`, `DefectOut`, `DefectList`

#### [0] Create Repositories
- `ProductRepository(BaseRepository[Product])`
- `BatchRepository(BaseRepository[Batch])`
- `InspectionRepository(BaseRepository[Inspection])`
- `DefectRepository(BaseRepository[Defect])`

#### [0] Create API Routers (Full CRUD)
- `GET/POST /api/v1/products` + `GET/PUT/DELETE /api/v1/products/{id}`
- `GET/POST /api/v1/batches` + `GET/PUT/DELETE /api/v1/batches/{id}`
- `GET/POST /api/v1/inspections` + `GET/PUT/DELETE /api/v1/inspections/{id}`
- `GET/POST /api/v1/defects` + `GET/PUT/DELETE /api/v1/defects/{id}`
- Wire all routers in `app/api/main.py`

#### [1] Generate Alembic Migration
- `alembic revision --autogenerate -m "bootstrap quality domain"`

#### [0] Write Backend Tests
- Tests for all 4 entity routers (list, create, get, update, delete)
- Test for relationships (e.g., batch linked to product, defects linked to inspection)
- Minimum 70%+ coverage target

### P1 — Should Have (Core Differentiators)

#### [1] Dashboard API Endpoint
- `GET /api/v1/dashboard` — aggregate stats:
  - Total inspections this month
  - Pass rate %
  - Total defects by severity
  - Batches by status
  - Top defect types
  - Trending pass/fail over last 30 days

#### [1] Frontend Dashboard (Real Data)
- Replace mock dashboard with real data from `/api/v1/dashboard`
- Summary stat cards (inspections, pass rate, defects, batches)
- Recent inspections table
- Defects by severity chart (simple bar/horizontal bars)
- Quick action buttons (Add Inspection, Add Batch, Log Defect)

#### [1] Frontend Pages (App Shell + Navigation)
- Responsive sidebar navigation: Dashboard, Products, Batches, Inspections, Defects
- `/batches` — table with search, status filter, pagination
- `/inspections` — table with result filter, date range, pagination
- `/defects` — table with severity/type filter, pagination
- `/products` — CRUD table with edit modal

#### [1] Frontend API Client (`src/lib/api.ts`)
- Typed functions for all backend endpoints
- Full domain types: `Product`, `Batch`, `Inspection`, `Defect`

#### [1] Defect Classification AI Endpoint (Phase 1)
- `POST /api/v1/ai/classify-defect` — accepts `{ description: string }`
- Returns `{ defect_type, severity, recommended_action, confidence }`
- Uses a simple rules-based engine for v1.3 (no external AI dependency yet)
- Frontend: "AI Suggest" button on defect form

#### [1] Batch → Inspection → Defect Detail Pages
- `/batches/{id}` — show batch info + related inspections + add inspection
- `/inspections/{id}` — show inspection info + related defects + add defect
- `/defects/{id}` — defect detail with AI suggestion replay

### P2 — Could Have (Advanced / AI)

#### [2] Statistical Process Control (SPC) Dashboard
- Backend: `GET /api/v1/analytics/spc` — calculate control limits (UCL, LCL, Cp, Cpk) for a product/batch over time
- Frontend: SPC line chart with upper/lower control limit bands
- Out-of-control rule detection (points outside 3σ, runs, trends)

#### [2] Supplier Quality Management Module
- `Supplier` model: name, contact_email, rating, ppm_target
- `SupplierShipment` model: supplier_id, batch_id, received_date, defects_found
- Supplier scorecard API
- Frontend: supplier table + scorecard view

#### [2] CAPA Workflow Engine
- `CAPA` model: title, description, root_cause, corrective_action, preventive_action, status, assigned_to, due_date, effectiveness_verified
- Status flow: `open` → `in_review` → `approved` → `implemented` → `verified` → `closed`
- `/capa` page with Kanban-style board

#### [2] AI-Powered Inspection Summary
- `POST /api/v1/ai/inspection-summary` — accepts inspection_id
- Analyzes linked defects, generates a natural-language summary
- Suggests next best action (e.g., "Escalate to CAPA — 3 critical defects found in Batch-X")
- Uses OpenRouter/Ollama integration (already scaffolded in `.env.example`)

#### [2] Document / Attachment Upload
- Upload inspection photos, certificates, SOPs
- Store file metadata in DB, serve via presigned URL pattern

---

## 4. Implementation Priority (Execution Order)

| # | Feature | Complexity | Est. Time | Status |
|---|---------|-----------|-----------|--------|
| 1 | Fix port/infrastructure mismatch | 0 | 30 min | 🔲 |
| 2 | Bootstrap domain models | 0 | 1 hr | 🔲 |
| 3 | Create Pydantic schemas | 0 | 45 min | 🔲 |
| 4 | Create repositories | 0 | 30 min | 🔲 |
| 5 | Create API routers + wire them | 0 | 1.5 hr | 🔲 |
| 6 | Generate alembic migration | 1 | 15 min | 🔲 |
| 7 | Write backend tests | 0 | 1.5 hr | 🔲 |
| 8 | Dashboard API endpoint | 1 | 1 hr | 🔲 |
| 9 | Frontend app shell + nav | 1 | 1 hr | 🔲 |
| 10 | Frontend API client (typed) | 1 | 30 min | 🔲 |
| 11 | Frontend Dashboard (real data) | 1 | 1.5 hr | 🔲 |
| 12 | Frontend list pages (Products/Batches/Inspections/Defects) | 1 | 3 hr | 🔲 |
| 13 | AI defect classification (rules engine) | 1 | 1 hr | 🔲 |
| 14 | Detail pages + relationship views | 1 | 2 hr | 🔲 |
| 15 | SPC Analytics | 2 | 4 hr | 🔲 |
| 16 | Supplier Quality Module | 2 | 6 hr | 🔲 |
| 17 | CAPA Workflow | 2 | 6 hr | 🔲 |
| 18 | AI Inspection Summary (LLM) | 2 | 4 hr | 🔲 |
| 19 | Document Upload | 2 | 4 hr | 🔲 |

**Phase 1 Target (This Session):** Items 1–14  
**Phase 2 Target:** Items 15–19

---

## 5. Anti-Patterns to Avoid (From AGENTS.md)

- NEVER use `declarative_base()` — always `from app.models.base import Base`
- NEVER use `default_factory=` in `mapped_column()` — use `default=`
- NEVER use in-memory `MOCK_*` dicts
- NEVER use `curl` in healthchecks
- NEVER install shadcn CLI or `@base-ui/react`
- NEVER upgrade `pytest-asyncio` past `0.24.0`
- NEVER use `localhost:PORT` hardcoded in frontend — use `process.env.NEXT_PUBLIC_API_URL`
- NEVER skip alembic migrations for new models
- ALWAYS use `lazy="selectin"` for relationships
- ALWAYS use `ondelete="CASCADE"` for child tables

---

## 6. Success Criteria for v1.3

- [ ] `docker compose up -d` starts all services cleanly
- [ ] Backend healthcheck returns `{"status":"ok"}`
- [ ] All 4 domain entities have full CRUD via REST API
- [ ] Frontend has working navigation + 5+ pages
- [ ] Dashboard shows real aggregated data (not random numbers)
- [ ] 70%+ backend test coverage
- [ ] Alembic migration is present and reversible
- [ ] No mock data anywhere in the codebase
- [ ] AI defect classification works via rules engine
