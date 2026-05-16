# Quickstart

## Step 1: Clone & Start

```bash
cd dclaw-quality
docker compose up -d --build
```

This starts three services:

| Service | Port | Description |
|---------|------|-------------|
| PostgreSQL | `5432` | Database |
| Backend (FastAPI) | `8047` | REST API + OpenAPI docs |
| Frontend (Next.js) | `3047` | Web UI |

## Step 2: Verify

```bash
# Check health
curl http://localhost:8047/health/
# → {"status":"ok"}

# Check API docs
curl http://localhost:8047/docs

# Open the app
open http://localhost:3047/dashboard
```

## Step 3: First Data

1. Open **http://localhost:3047/products**
2. Click **Add Product** — create a product (e.g., "Widget Pro", SKU `WP-001`)
3. Go to **Batches** — create a batch linked to that product
4. Go to **Inspections** — record an inspection for the batch
5. Go to **Defects** — log a defect; try the **AI Suggest** button by typing a description like *"deep scratch found on polished surface"*
6. Return to **Dashboard** — watch real stats update instantly

## Next Steps

- Read the [Guides](../guides) for detailed use cases
- Check the [Reference](../reference) for API docs and architecture
