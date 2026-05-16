# Troubleshooting

Common issues and solutions for DClaw Quality.

## Quick Diagnostics

```bash
# Docker Compose
docker compose ps
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres

# Kubernetes
kubectl get pods -n dclaw-quality
kubectl logs -n dclaw-quality deployment/dclaw-quality-backend
kubectl get clusters -n dclaw-quality
```

## Sections

- [Common Issues](./common-issues)
- [FAQ](./faq)
