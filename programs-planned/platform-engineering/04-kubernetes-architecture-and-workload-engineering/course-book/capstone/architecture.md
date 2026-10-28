# Atlas Kubernetes Runtime architecture

Atlas Kubernetes Runtime preserves the Course 3 workload release while introducing Kubernetes ownership.

```text
AtlasWorkload custom resource
├── API Deployment (3 replaceable replicas)
├── Worker Deployment (1 replica in Course 4)
├── ServiceAccounts
├── configuration references
├── PodDisruptionBudget
└── Course 5 Service handoff
```

The worker remains one replica because the durability and concurrency model for its queue/storage is not proven here. Scaling it before Course 6 could duplicate or corrupt effects.

Production-intent manifests use exact image digests, UID/GID 65532, read-only root filesystems, dropped capabilities, no privilege escalation, explicit requests/limits, and graceful termination.
