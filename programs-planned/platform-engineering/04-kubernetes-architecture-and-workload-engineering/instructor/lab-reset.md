# Laboratory reset

Dependency-light labs should construct state in temporary directories or fresh `ApiStore` instances. `make clean` removes generated reports and caches.

The kind lane always uses the cluster name `atlas-course4`, an isolated kubeconfig under `capstone/reports`, a cleanup trap, and an explicit `ALLOW_KIND_PROOF=1` guard. If a run is interrupted:

```bash
kind delete cluster --name atlas-course4
rm -f capstone/reports/kind-kubeconfig
```

Never repoint the course scripts at a shared context.
