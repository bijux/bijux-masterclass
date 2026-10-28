# Capstone — Atlas Data Plane 1.0

Atlas uses different stores for different meanings:

```text
transactional run state
    strong application ownership and ordered mutation

immutable artifacts
    content identity, integrity, retention, and efficient transfer

recovery evidence
    snapshots, backups, manifests, restore logs, and verification
```

The API and worker remain ordinary Kubernetes workloads. Course 6 adds a single-writer transactional-state service for the dependency-light lane, production-intent StatefulSet and PVC contracts, a backup target, a snapshot catalogue, and a restoration controller. The course does not claim that a one-replica database is highly available. It uses that simple deployment to make storage and recovery semantics visible before later courses automate delivery and fleet operation.

The final defense must show that a new environment can be created from the Course 6 manifests and recovery package without relying on the original Pods, Nodes, or volume attachments.
