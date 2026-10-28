# Atlas data authority

- `atlas-db` owns transactional run state and the authoritative writer generation.
- `atlas-artifacts` owns immutable objects identified by SHA-256.
- `atlas-backup` owns recovery manifests and independently retained objects.
- Kubernetes owns desired workload and claim state.
- The CSI stack owns storage lifecycle operations, not application consistency.
- Course 7 may reconcile resources but may not infer data rollback safety.
