# Common Issues

## App won't start

**Symptoms:** Backend container exits or `Connection refused` on port 8047.

**Solutions:**

```bash
# Check backend logs
docker compose logs -f backend

# Verify database is healthy
docker compose logs -f postgres
docker compose exec postgres pg_isready -U postgres

# Run migrations manually
cd backend
alembic upgrade head
```

## Database connection errors

**Symptoms:** Backend logs show `connection refused` or `timeout`.

**Solutions:**

1. Verify PostgreSQL is running:
   ```bash
   docker compose ps
   ```

2. Check the connection string:
   ```bash
   echo $DATABASE_URL
   # Expected: postgresql+asyncpg://postgres:postgres@localhost:5432/dclaw_quality
   ```

3. For Kubernetes:
   ```bash
   kubectl get clusters -n dclaw-quality
   kubectl get secret dclaw-quality-db-credentials -n dclaw-quality
   ```

## Frontend can't reach backend

**Symptoms:** Browser console shows CORS errors or empty dashboard.

**Solutions:**

1. Verify backend is running on `localhost:8047`
2. Check `NEXT_PUBLIC_API_URL` is set to `http://localhost:8047`
3. If using Docker, rebuild the frontend image after changing `NEXT_PUBLIC_API_URL`:
   ```bash
   docker compose up -d --build frontend
   ```

## Tests fail with database error

**Symptoms:** `pytest` fails with connection refused.

**Solutions:**

1. Ensure PostgreSQL is running on `localhost:5432`
2. Create the test database:
   ```bash
   psql -h localhost -U postgres -c "CREATE DATABASE dclaw_app_test;"
   ```
3. Check `DATABASE_URL` in `conftest.py` points to `localhost:5432`

## AI Suggest returns no results

**Symptoms:** AI classification button does nothing.

**Solutions:**

1. The rules engine runs entirely in the backend — no external API key is needed for Phase 1
2. Ensure the backend is reachable from the frontend (`NEXT_PUBLIC_API_URL`)
3. Check browser network tab for `POST /api/v1/ai/classify-defect`
