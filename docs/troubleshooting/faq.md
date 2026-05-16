# Frequently Asked Questions

## General

### How do I update DClaw Quality?

Pull latest changes and rebuild:

```bash
git pull origin main
docker compose up -d --build
```

For Kubernetes, patch the DClawApp CRD:

```bash
kubectl patch dclawapp quality --type merge -p '{"spec":{"version":"1.3.1"}}'
```

### How do I back up my data?

**Docker Compose:**

```bash
docker compose exec postgres pg_dump -U postgres dclaw_quality > backup.sql
```

**Kubernetes:**

```yaml
spec:
  database:
    backups:
      enabled: true
      schedule: "0 2 * * *"
```

### How do I scale the app?

**Docker Compose:** does not auto-scale; use Kubernetes for production scaling.

**Kubernetes:**

```yaml
spec:
  frontend:
    replicas: 3
  backend:
    replicas: 3
```

### Can I run DClaw Quality without Kubernetes?

Yes. Docker Compose is the recommended local path:

```bash
docker compose up -d --build
```

For native development:

```bash
# Terminal 1 — Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.api.main:app --host 0.0.0.0 --port 8047 --reload

# Terminal 2 — Frontend
cd frontend
npm install
export NEXT_PUBLIC_API_URL=http://localhost:8047
npm run dev
```

## Domain Model

### What happens if I delete a Product?

Deleting a Product will cascade-delete all linked **Batches**, **Inspections**, and **Defects** due to `ondelete="CASCADE"`.

### Can I change a Batch status after creation?

Yes — use `PUT /api/v1/batches/{id}` with the new status (`in_production`, `in_qa`, `passed`, `failed`, `shipped`).

### Does the AI engine require an internet connection?

**No.** Phase 1 uses a purely local rules-based classifier. Phase 2 (planned) will add optional LLM integration via Ollama or OpenRouter.

## Support

For issues not covered here, check the [DClaw Platform Troubleshooting Guide](../../ecosystem/troubleshooting).
