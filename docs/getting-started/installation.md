# Installation

## Via DPanel

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
# Apply the DClawApp CRD
kubectl apply -f - <<EOF
apiVersion: platform.dclaw.io/v1
kind: DClawApp
metadata:
  name: quality
spec:
  appId: quality
  appName: DClaw Quality
  version: 0.1.0
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
kubectl get pods -n dclaw-quality
kubectl get ingress -n dclaw-quality
```
