# Course 6 — Kubernetes Storage, Stateful Workloads, and Data Resilience Engineering

This course teaches how Kubernetes coordinates storage without pretending that Kubernetes itself provides data durability, database correctness, backup integrity, or disaster recovery.

The learner builds **Atlas Data Plane 1.0** from the exact Course 5 connectivity handoff. The result distinguishes transactional state, immutable artifacts, snapshots, backups, and recovery evidence. It includes a semantic CSI lifecycle, topology-aware binding, StatefulSet and fencing models, application-consistent snapshot coordination, content-verified backups, empty-destination restores, storage performance reasoning, production-intent manifests, and an exact handoff to Course 7.

Start at [`course-book/start-here.md`](course-book/start-here.md).

```bash
make help
make doctor
make predecessor-proof
make core-proof
make capstone-tour
make manifest-proof
```
