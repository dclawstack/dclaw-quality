# Architecture

## Overview

DClaw Quality follows the standard DClaw app architecture with a real domain layer:

```
┌─────────────┐     ┌──────────────────────────────┐     ┌─────────────┐
│  Frontend   │────▶│           Backend              │────▶│  Database   │
│  (Next.js)  │     │  FastAPI → Services → Repos  │     │ (PostgreSQL)│
└─────────────┘     └──────────────────────────────┘     └─────────────┘
                              │
                              ▼
                        ┌─────────────┐
                        │  AI Engine  │
                        │(rules-based)│
                        └─────────────┘
```

## Domain Model

```
Product (1) ────► Batch (N)
  │                   │
  │              Inspection (N)
  │                   │
  └──────────── Defect (N)
```

### Entities

| Entity | Key Fields | Relationships |
|--------|-----------|---------------|
| **Product** | `id`, `name`, `sku`, `category`, `status` | `batches` (1→N) |
| **Batch** | `id`, `batch_number`, `quantity_produced`, `production_date`, `status` | `product` (N→1), `inspections` (1→N) |
| **Inspection** | `id`, `inspector_name`, `inspection_type`, `result`, `inspected_at` | `batch` (N→1), `defects` (1→N) |
| **Defect** | `id`, `defect_type`, `severity`, `description`, `quantity_affected`, `ai_suggested`, `ai_confidence`, `recommended_action` | `inspection` (N→1) |

## Components

### Frontend

- **Framework:** Next.js 14 (App Router)
- **Styling:** Tailwind CSS
- **UI Components:** Pre-built custom design system (Button, Card, Dialog, Table, Badge, Tabs, etc.)
- **State:** React hooks (`useState`, `useEffect`)
- **API Client:** Typed fetch wrapper in `src/lib/api.ts`

### Backend

- **Framework:** FastAPI with `lifespan` handler
- **ORM:** SQLAlchemy 2.0 (DeclarativeBase from `app.models.base`)
- **Schemas:** Pydantic v2 with `ConfigDict(from_attributes=True)`
- **Database:** PostgreSQL + asyncpg + AsyncSession
- **Pattern:** Repository layer (`app/repositories/`) + Dependency Injection (`Depends(get_db)`)
- **Migrations:** Alembic

### AI Engine

- **Phase 1 (Current):** Rules-based keyword classifier
  - Maps descriptions to defect type, severity, and recommended action
  - Zero external API dependency — works offline
- **Phase 2 (Future):** LLM integration via Ollama / OpenRouter for natural-language inspection summaries

## Infrastructure

- **Container:** Docker + Docker Compose
- **Orchestration:** Kubernetes via DClaw Operator
- **Database:** CloudNativePG (K8s) or standard PostgreSQL image (Compose)
- **Ingress:** nginx-ingress + cert-manager
