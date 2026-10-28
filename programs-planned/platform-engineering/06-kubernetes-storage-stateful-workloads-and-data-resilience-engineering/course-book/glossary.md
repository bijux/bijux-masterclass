# Glossary

**application-consistent snapshot** — a point-in-time copy coordinated with the application so that its recovery invariants are satisfied, often by quiescing writes or creating a database checkpoint.

**attach** — a controller-side operation that makes a volume available to a Node. It is distinct from staging or mounting the volume into a Pod.

**backup** — an independently managed recovery copy with retention, inventory, verification, and restoration procedures. A snapshot may be one component of a backup.

**binding** — the one-to-one association between a PVC and a PV.

**claim** — a namespaced request for storage expressed by a PersistentVolumeClaim.

**crash-consistent** — equivalent to storage observed after an abrupt power loss. Filesystem or database recovery may still be required.

**CSI** — Container Storage Interface, the RPC contract between a container orchestrator and storage plugins.

**fencing** — preventing a stale or deposed writer from continuing to mutate authoritative data.

**high-water recovery point** — the newest durable point included in a backup or replication stream.

**mount** — exposing a staged or prepared filesystem at a container-visible path. A successful mount says nothing about application-level correctness.

**PV** — cluster-scoped PersistentVolume representing storage available for binding.

**PVC** — namespaced PersistentVolumeClaim requesting storage.

**RPO** — recovery point objective: the maximum acceptable loss measured as time or committed operations.

**RTO** — recovery time objective: the target duration to restore the service or capability.

**snapshot** — a point-in-time storage-system copy or reference, usually sharing some failure domain with the source unless exported.

**stage** — a node-side CSI operation that prepares a volume at a global node path before per-Pod publication.

**StatefulSet** — a workload controller providing stable ordinal identity, stable network identity, and persistent claim templates. It does not provide consensus or application replication.

**storage class** — a cluster-scoped policy and provisioner selection object used when dynamically provisioning volumes.

**topology segment** — a set of driver-defined key/value labels describing where storage can be provisioned or accessed.

**VolumeAttributesClass** — a storage API object describing a mutable volume service profile for drivers that support modify-volume behavior.
