# Installation

## Via Docker Compose (Recommended for Local Dev)

```bash
cd dclaw-quality
docker compose up -d --build
```

Services:
- **postgres** — PostgreSQL 16 with persistent volume
- **backend** — FastAPI on port `8047`
- **frontend** — Next.js on port `3047`

## Via DPanel / Kubernetes

1. Open DPanel at `https://panel.yourdomain.com`
2. Find **DClaw Quality** in the app grid
3. Click **Install**
4. The DClaw Operator will provision:
   - Namespace: `dclaw-quality`
   - Frontend deployment (Next.js)
   - Backend deployment (FastAPI)
   - PostgreSQL database (CloudNativePG)
   - Ingress with TLS

## Via kubectl

```bash
kubectl apply -f - <<EOF
apiVersion: platform.dclaw.io/v1
kind: DClawApp
metadata:
  name: quality
spec:
  appId: quality
  appName: DClaw Quality
  version: 1.3.0
  category: manufacturing
  enabled: true
  frontend:
    image: ghcr.io/dclawstack/dclaw-quality:latest
    replicas: 2
  backend:
    image: ghcr.io/dclawstack/dclaw-quality-backend:latest
    replicas: 2
  database:
    enabled: true
    storage: 10Gi
  ingress:
    enabled: true
    host: quality.yourdomain.com
    tls: true
EOF
```

## Verify

```bash
# Kubernetes
kubectl get pods -n dclaw-quality
kubectl get ingress -n dclaw-quality

# Docker Compose
docker compose ps
docker compose logs -f backend
```
