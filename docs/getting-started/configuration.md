# Configuration

## Environment Variables

### Backend

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://postgres:postgres@localhost:5432/dclaw_quality` |
| `APP_ENV` | Runtime environment (`dev` / `production`) | `dev` |
| `DEBUG` | Enable debug logging | `true` |
| `SECRET_KEY` | JWT / session signing key | `change-me-in-production` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Auth token lifetime | `60` |
| `OLLAMA_URL` | Local LLM endpoint (optional) | `http://localhost:11434` |
| `OLLAMA_MODEL` | Default local model | `llama3.1` |
| `OPENROUTER_API_KEY` | External LLM API key (optional) | — |
| `OPENROUTER_MODEL` | External model slug | `meta-llama/llama-3.1-8b-instruct` |

### Frontend

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8047` |

> **Important:** `NEXT_PUBLIC_API_URL` is baked at build time. If you change it in Docker, rebuild the image or set it via the `ARG` in `frontend/Dockerfile`.

## Kubernetes Resources

Adjust resource limits in the DClawApp CRD:

```yaml
spec:
  resources:
    limits:
      cpu: 1000m
      memory: 2Gi
    requests:
      cpu: 250m
      memory: 512Mi
```
