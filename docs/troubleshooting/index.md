# Troubleshooting

Common issues and solutions for DClaw Quality.

## Quick Diagnostics

```bash
# Check app pods
kubectl get pods -n dclaw-quality

# Check logs
kubectl logs -n dclaw-quality deployment/dclaw-quality-backend

# Check database
kubectl get clusters -n dclaw-quality
```

## Sections

- [Common Issues](./common-issues)
- [FAQ](./faq)
