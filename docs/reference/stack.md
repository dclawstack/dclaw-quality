# Stack

## Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Frontend | Next.js | 14.2+ |
| Frontend | React | 18.3+ |
| Frontend | Tailwind CSS | 3.4+ |
| Frontend | TypeScript | 5.4+ |
| Frontend | lucide-react | 0.400+ |
| Backend | Python | 3.11+ |
| Backend | FastAPI | 0.110+ |
| Backend | Pydantic | 2.5+ |
| Backend | SQLAlchemy | 2.0+ |
| Backend | asyncpg | 0.29+ |
| Backend | pytest-asyncio | 0.24.0 |
| Database | PostgreSQL | 16 |
| Migrations | Alembic | 1.13+ |
| Packaging | Helm | 3 |
| Build | Hatchling | latest |

## Ports

| Service | Port |
|---------|------|
| Frontend | `3047` |
| Backend | `8047` |
| Database | `5432` |

## Key Constraints

- **pytest-asyncio** is pinned to `0.24.0`. Do not upgrade.
- **Tailwind v3** is used. Do not install shadcn CLI v4 or `@base-ui/react`.
- **SQLAlchemy 2.0** uses `DeclarativeBase` from `app.models.base`. Never use `declarative_base()` separately.
- **Pydantic v2** schemas use `ConfigDict(from_attributes=True)`.
