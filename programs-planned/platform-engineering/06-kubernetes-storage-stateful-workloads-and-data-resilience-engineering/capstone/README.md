# Atlas Data Plane 1.0 — executable course capstone

The capstone is an executable explanation of the course book. Its semantic
models expose state transitions that are normally spread across the Kubernetes
API server, scheduler, CSI sidecars, node plugin, storage backend, application,
backup repository, and operator runbooks.

The dependency-light lane proves logic and local mechanisms. It cannot prove a
particular CSI driver, cloud volume service, database engine, or regional
recovery system. Those claims require the native lanes described in the labs.

Run:

```bash
make capstone-tour
make core-proof
```
