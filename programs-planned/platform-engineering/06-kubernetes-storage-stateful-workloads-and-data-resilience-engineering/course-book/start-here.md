# Start here

Course 6 begins with a running and connected Kubernetes workload, not an empty cluster. Course 5 already established Services, DNS, Gateway routing, NetworkPolicy expectations, egress restrictions, and topology assumptions. The unresolved question is whether data survives the failures that Pods and Nodes are designed to tolerate.

A useful storage design starts by separating five things that are often collapsed:

1. **bytes** — the physical or logical data stored by a backend;
2. **volume identity** — the storage-system object represented through a CSI handle;
3. **claim identity** — the namespaced request and binding expressed through a PVC;
4. **workload identity** — the Pod or StatefulSet member permitted to use the data;
5. **application authority** — the process allowed to interpret and mutate the data.

The course never treats a mounted volume as proof of safe application ownership. It never treats a snapshot as a backup. It never treats a completed backup as proof of restoration. It never treats a StatefulSet as a database consensus system.

## Study lane

The mandatory lane uses Python, Go, YAML, JSON, local filesystems, and deterministic fixtures. It proves semantics that do not require a cluster. The optional cluster lane uses kind and a CSI-capable storage setup. The environment-backed lane uses a real storage system or managed Kubernetes service. Keep the evidence classes separate.

## What you build

Atlas Data Plane 1.0 introduces:

- an explicit storage-class catalogue;
- topology-aware PVC binding;
- a semantic CSI controller and node lifecycle;
- a single-writer transactional-state profile;
- immutable artifact storage and checksums;
- StatefulSet identity and fencing;
- application-consistent snapshots;
- group-snapshot reasoning;
- backup manifests and empty-destination restore drills;
- storage performance budgets and diagnostic runbooks;
- a Course 7 handoff that GitOps can promote without violating data safety.

Read the course book in order. Labs deliberately create failure. Do not run the optional destructive lanes against a shared or production cluster.
