# Best Practices

## Data Integrity

- Always create a **Product** before creating a **Batch**
- Always create a **Batch** before creating an **Inspection**
- Always create an **Inspection** before logging a **Defect**
- Use the AI Suggest feature to keep defect types consistent across inspectors

## Security

- Rotate `SECRET_KEY` in production
- Use TLS termination at the ingress / reverse-proxy layer
- Never expose PostgreSQL port `5432` publicly in production

## Performance

- All list endpoints support `skip` and `limit` query parameters
- Use `search` on the Products list for large catalogs
- Filter inspections by `result` and batches by `status` to reduce payload size

## Testing

- Backend tests run against a real PostgreSQL database on `localhost:5432`
- Run `pytest` in the `backend/` directory before committing changes
- Target: 70%+ coverage for all routers and repositories

## Upgrades

- Run `alembic upgrade head` after every schema change before deploying
- Backup PostgreSQL volumes before major version bumps
- Read the [changelog](../releases/changelog) before upgrading
