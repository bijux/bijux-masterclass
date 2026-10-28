---
module_id: PLAT-027
program: Platform Engineering
level: 1
module_number: 27
title: Storage and Stateful Workloads
status: complete
last_verified: 2026-09-02
---

# Storage and Stateful Workloads

## One-Page Review

### Governing question

How should a platform bind stateful workloads to storage so that identity, placement, durability, consistency, performance, recovery, retention, security, cost, and destructive lifecycle behavior remain explicit?

### Essential definitions

- A **volume** presents filesystem or block storage to containers; its medium and lifetime depend on volume type.
- A **PersistentVolume (PV)** is a cluster-scoped storage resource with a lifecycle independent of any individual pod.
- A **PersistentVolumeClaim (PVC)** is a namespaced request and binding identity through which a workload consumes a PV.
- A **StorageClass** is an operator-owned provisioning profile that selects a provisioner and parameters such as reclaim policy, binding mode, expansion, topology, filesystem, encryption, or performance.
- **Container Storage Interface (CSI)** is the standard through which external drivers provision, attach, mount, resize, snapshot, and report capabilities for storage systems.
- An **access mode** participates in PV/PVC matching and, depending on driver, attachment constraints; it is not a general application-level concurrency or write-safety protocol.
- **volume mode** selects a mounted filesystem or raw block device presentation.
- A **StatefulSet** manages pods with stable ordinal, network, and storage identities plus ordered or parallel lifecycle behavior.
- A **snapshot** is a storage-system point-in-time representation; crash consistency, application consistency, isolation, retention, and recoverability are separate properties.
- **reclaim policy** controls what happens to a PV/backing volume after its claim is released; **PVC retention policy** controls selected StatefulSet-created PVC deletion during scale-down or StatefulSet deletion.
- **recovery point objective (RPO)** bounds acceptable lost data; **recovery time objective (RTO)** bounds acceptable restoration time.

### Central model, mechanism, or theorem

Model a stateful binding as $S=(D,C,A,P,T,Q,B,R,E,L,O,X)$: data semantics $D$, consistency/availability contract $C$, access and volume modes $A$, provisioning profile $P$, topology/placement $T$, capacity/performance $Q$, backup/snapshot/replication $B$, restore/recovery $R$, encryption and authorization $E$, lifecycle/retention $L$, observations $O$, and declared exceptions $X$. A running pod with a Bound PVC proves neither data durability nor recoverability. The usable-state predicate requires correct binding, reachable attachment, successful mount, filesystem/block integrity, application ownership, sufficient capacity/performance, valid data, and successful application recovery.

### Critical invariants

- Every byte is classified as ephemeral, reproducible, cached, durable, authoritative, replicated, backed up, archived, or regulated before a storage class is selected.
- A PVC name is the workload's stable storage binding; provider volume IDs and pod names are implementation/lifecycle details, never reconstructed casually.
- StorageClass name and parameters are a versioned platform contract with measured durability, availability, performance, topology, encryption, expansion, snapshot, restore, retention, and cost behavior.
- `ReadWriteOnce` is never interpreted as single-pod exclusion; use `ReadWriteOncePod` where supported and still retain application fencing and data-format safety.
- Topology-constrained provisioning preserves scheduler knowledge through `WaitForFirstConsumer`; pod placement, volume topology, failure domains, and replica placement are solved together.
- StatefulSet ordinals and PVCs preserve member identity but do not create application replication, quorum, leader election, backup, or safe failover.
- Snapshot success is not backup success; application consistency, independent failure domain, retention, immutability, integrity, restore, and RPO/RTO evidence are verified separately.
- Expansion is grow-only at the Kubernetes claim layer and is complete only after provider, PV/PVC, filesystem or block consumer, and application capacity agree.
- Scale-down, workload deletion, PVC deletion, reclaim, snapshot deletion, backup expiry, and provider cleanup are distinct destructive transitions with explicit owners and protection.
- Recovery is exercised from documented artifacts into an isolated target and validated at the application/business level, not inferred from object status.

### Common failures

Writing durable data to the container layer or `emptyDir`; treating a PV as replicated storage; using `Immediate` binding for zonal volumes; setting `nodeName` with delayed binding; assuming RWO means one pod; running two database writers without fencing; using StatefulSet as a database operator; sharing one PVC across identities accidentally; deleting PVCs to repair attach failures; relying on default `Delete` reclaim behavior; taking crash-consistent snapshots during multi-volume transactions; storing backups in the same failure domain and credentials; expanding beyond provider quota; expecting shrink; ignoring inode, latency, queue, and attach limits; and declaring recovery from a green snapshot without a restore test.

### Compact example

A three-member database uses a versioned `database-zonal-retain` StorageClass with CSI provisioning, encrypted volumes, `WaitForFirstConsumer`, expansion, snapshots, and `Retain`. A StatefulSet gives ordinals and one `ReadWriteOncePod` claim per member; the database protocol supplies quorum, replication, leader election, fencing, and repair. Anti-affinity and topology spread place members across three zones, while each zonal volume follows its member. Application-aware backup coordinates a database checkpoint, records log position, snapshots each member as required, exports backups and metadata to a separate account/region, and regularly restores into isolation. Status distinguishes database health, PVC binding, attachment, mount, filesystem, capacity, snapshot, export, and restore evidence. Scale-down retains claims until an approved data-retirement workflow erases them.

### Connections

Retrieve pod identity, controllers, rollout, disruption, and termination from [PLAT-024](024-pods-workloads-and-controllers.md), declarative resources from [PLAT-023](023-kubernetes-declarative-resources.md), runtime and local-resource limits from [PLAT-022](022-runtime-isolation-and-resource-controls.md), configuration and credentials from [PLAT-026](026-configuration-and-secrets.md), and service/headless discovery from [PLAT-025](025-services-and-ingress.md). Database, distributed-systems, reliability, security, and data-governance programs supply the domain protocols Kubernetes does not.

## Governing Question

Which state must survive which failures, where may it reside, who may read or destroy it, how is one workload identity bound to it, and what measured mechanism satisfies consistency, durability, recovery, retention, security, performance, and cost requirements?

Kubernetes reconciles resource objects and calls storage drivers. It does not infer whether bytes are authoritative, whether simultaneous writers are safe, whether a snapshot captures a valid transaction boundary, whether replicas share a hidden failure domain, or whether restored data meets business rules.

The platform must make the full data lifecycle visible. A claim can be Bound while a volume cannot attach in the selected zone. A volume can mount while its filesystem is corrupt. A database can start while replaying hours of logs. A snapshot can be ReadyToUse while it contains a crash-consistent image that the application cannot recover. Storage status is layered evidence, not a single green light.

## Why This Matters

Compute replacement is routine; state loss is often permanent. The most dangerous storage errors occur at lifecycle boundaries: provisioning in the wrong zone, attaching one writer twice, deleting a claim under a default reclaim policy, restoring an incomplete snapshot, retaining regulated copies beyond policy, or discovering during an incident that provider credentials and backups share the same compromised account.

Stateful services also constrain scheduling and rollout. A pod can move only where its volume is attachable. Detach and attach operations take time and may be blocked by an unreachable node. Quorum members require failure-domain separation and controlled disruption. Capacity and latency changes can turn a nominally healthy service into a queueing collapse.

A platform therefore offers storage as an evidence-backed product, not a menu of provider flags. Consumers should choose from understandable classes whose measured properties, unsupported uses, cost, recovery, and deletion behavior are explicit.

## Prerequisites and Retrieval

Retrieve filesystems, blocks, pages, caches, flush and `fsync`, write ordering, journaling, corruption, latency, throughput, IOPS, queues, capacity, inodes, encryption, checksums, snapshots, replication, quorum, consensus, transactions, logs, backup, restore, retention, deletion, identity, authorization, topology, scheduling, pods, controllers, Services, and eventual consistency.

You should distinguish persistence from durability, redundancy from backup, crash consistency from application consistency, availability from recoverability, logical deletion from physical erasure, filesystem capacity from provider allocation, and Kubernetes object state from storage-system and application state.

## Learning Objectives

After completing this module, you should be able to:

1. classify workload data and derive persistence, durability, consistency, RPO, RTO, retention, security, and performance requirements;
2. explain volume, PV, PVC, StorageClass, CSI, binding, attachment, mount, and reclaim lifecycles;
3. select access mode, volume mode, topology, binding mode, expansion, snapshot, encryption, and reclaim behavior;
4. design StatefulSet identity, storage, update, scale, and deletion contracts without attributing database semantics to the controller;
5. combine storage topology with scheduler constraints, failure domains, replication, fencing, and disruption safety;
6. design application-consistent snapshot, backup, export, restore, and disaster-recovery workflows;
7. govern capacity, latency, throughput, quotas, health, security, cost, retention, and data destruction; and
8. diagnose provisioning, scheduling, attachment, mount, filesystem, performance, and recovery failures by layer.

## Core Exposition

### Begin with data semantics and failure scope

Inventory every write path: container writable layer, logs, `emptyDir`, cache, uploaded objects, queue state, database files, transaction logs, indexes, model artifacts, audit records, and derived outputs. Classify what can be discarded, regenerated, replayed, or restored and from which source.

State the failures each dataset must survive: process restart, container restart, pod replacement, node loss, zone loss, region loss, operator error, credential compromise, ransomware, application corruption, and provider/account loss. “Persistent” usually means independent of a pod, not safe from all of these.

Define consistency, maximum acknowledged-data loss, maximum outage, retention, legal hold, residency, encryption, tenant isolation, size, growth, read/write shape, latency percentiles, throughput, IOPS, burst, inode count, queue depth, and concurrency. These requirements determine architecture before a PVC appears.

### Separate ephemeral and persistent storage

The container writable layer follows container lifecycle and is unsuitable for authoritative data. `emptyDir` follows a pod: it survives container restarts inside that pod but is deleted when the pod is removed from the node. Node disk pressure can evict workloads, and memory-backed `emptyDir` consumes memory resources. Use them for bounded scratch, caches, staging, or inter-container exchange whose loss is acceptable.

Generic ephemeral volumes create a PVC owned by the pod and can use ordinary dynamic provisioning, capacity, snapshot, or clone capabilities. Their ownership normally deletes the claim with the pod; reclaim policy then affects the backing volume. Pod creation can indirectly create claims, so admission and quota must include this path.

Persistent volumes have a lifecycle independent of one pod, but applications must still write to the mounted path. A stray path in the image layer can appear to work until replacement. Readiness and backup checks should verify the intended filesystem/device identity, not merely a directory's existence.

### Understand PV and PVC binding

A PV is cluster-scoped supply; a PVC is namespaced demand. The control plane matches storage class, requested capacity, access modes, volume mode, selector where used, and availability. Binding is one-to-one and exclusive between one PV and one PVC, even when the underlying storage supports many clients.

The claim name is the workload contract. A pod references the PVC, not the provider disk. The bound PV records a claim reference and provider/CSI identity. Do not manually swap claim references or provider IDs except through a documented recovery procedure with the workload stopped and data identity verified.

Object protection delays deletion while resources are in use, and modern CSI deletion protection coordinates PV removal with backing-volume deletion. These mechanisms reduce races; they do not make an approved PVC deletion harmless. Finalizers stuck during provider failure require diagnosis, not blind removal.

A PVC requesting more capacity may bind a larger PV; the request is a minimum. Quotas must account for claims, provisioned capacity, snapshots, backups, and provider allocation rather than only application-visible bytes.

### Treat StorageClass as a product contract

A StorageClass names a provisioner and provider-specific parameters. It also sets `reclaimPolicy`, `volumeBindingMode`, `allowVolumeExpansion`, mount options, and allowed topologies. Its name is a durable consumer API, so changing the meaning under an existing name silently changes future volumes while old volumes retain prior properties.

Offer classes by stable intent, such as `database-zonal-retain`, `shared-filesystem-delete`, or `scratch-zonal-delete`, only when the names match measured behavior. Document media/backend, topology, durability, availability, encryption and key ownership, access and volume modes, size range, performance envelope, burst/throttle, expansion, snapshot/clone, reclaim, backup integration, restore, cost, quotas, and support.

The default class should be safe for the broadest ordinary use, but high-risk state should request a class explicitly. Multiple defaults or a changing default create surprises for claims that omit `storageClassName`. Admission can require explicit classes for namespaces or workloads with durable data.

Mount options and opaque parameters are driver-specific and may not be validated until provisioning or mount. Version classes or policies when semantics change; test driver and sidecar compatibility with cluster upgrades.

### Preserve topology through delayed binding

`Immediate` provisioning occurs when the claim is created, before the scheduler selects a consumer node. For zonal or node-local storage, the resulting volume may be inaccessible from nodes that satisfy CPU, architecture, affinity, taints, or replica constraints.

`WaitForFirstConsumer` delays selection/provisioning until a pod is considered for scheduling. The scheduler can combine pod constraints with available storage topology. This is normally the safe choice for topology-constrained CSI and local volumes.

Do not set `nodeName` for a pod using delayed binding because it bypasses scheduler participation and can leave the claim pending. Use node selectors or affinity when placement must be constrained. Preserve topology labels consistently and test zone removal, capacity exhaustion, and autoscaler interaction.

Storage locality becomes part of recovery. A zonal disk cannot make one data copy survive zone loss. An application or storage system must replicate across independent failure domains, and the scheduler must place those replicas accordingly.

### Interpret access and volume modes correctly

`ReadWriteOnce` (RWO) means read-write mount by a single node; multiple pods on that node may still access it. `ReadOnlyMany` permits read-only mounts by many nodes. `ReadWriteMany` permits read-write mounts by many nodes where the driver/backend supports it. `ReadWriteOncePod` (RWOP), for supported CSI stacks, restricts read-write use to one pod cluster-wide.

Access modes primarily describe matching and attach/mount capability. They do not implement file locking, transactions, cache coherence, leader election, or writer fencing. A split-brain database can corrupt an RWO filesystem if two processes share the same node or stale attachment authority. Use application consensus, leases with fencing tokens, storage reservations where available, and safe recovery.

Filesystem mode asks kubelet/driver to prepare and mount a filesystem. Raw block mode exposes a device path and shifts formatting, allocation, integrity, and tooling responsibility to the application. Choose raw block only for software explicitly designed and operated for it.

Mounting read-only in a pod is an additional consumer setting, not a replacement for provider permissions or application authorization. Shared filesystems also need tenant boundaries, UID/GID and permission design, locking semantics, quotas, noisy-neighbor controls, and failure testing.

### Inventory binding and lifecycle decisions

Storage intent should be reviewable before provisioning. The following synthetic inventory separates persistence, binding, reclaim, access, backup, and topology choices.

<!-- bijux-verify: {"id":"stateful-storage-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"claims=8\npersistent=6\nephemeral=2\nwait_consumer=5\nretain=3\nrwop=2\nsnapshot_required=5\nzones=3\n","stderr":""}} -->
```python
claims = [
    {"name": "orders-data", "persistent": True, "wait": True, "reclaim": "Retain", "access": "RWOP", "snapshot": True, "zone": "a"},
    {"name": "orders-wal", "persistent": True, "wait": True, "reclaim": "Retain", "access": "RWO", "snapshot": True, "zone": "a"},
    {"name": "analytics-shared", "persistent": True, "wait": True, "reclaim": "Delete", "access": "RWX", "snapshot": True, "zone": "b"},
    {"name": "cache-scratch", "persistent": False, "wait": False, "reclaim": "Delete", "access": "RWO", "snapshot": False, "zone": "b"},
    {"name": "batch-work", "persistent": False, "wait": True, "reclaim": "Delete", "access": "RWO", "snapshot": False, "zone": "c"},
    {"name": "media", "persistent": True, "wait": True, "reclaim": "Delete", "access": "RWX", "snapshot": True, "zone": "c"},
    {"name": "registry", "persistent": True, "wait": False, "reclaim": "Retain", "access": "RWOP", "snapshot": True, "zone": "b"},
    {"name": "audit", "persistent": True, "wait": False, "reclaim": "Delete", "access": "ROX", "snapshot": False, "zone": "c"},
]
print(f"claims={len(claims)}")
print(f"persistent={sum(item['persistent'] for item in claims)}")
print(f"ephemeral={sum(not item['persistent'] for item in claims)}")
print(f"wait_consumer={sum(item['wait'] for item in claims)}")
print(f"retain={sum(item['reclaim'] == 'Retain' for item in claims)}")
print(f"rwop={sum(item['access'] == 'RWOP' for item in claims)}")
print(f"snapshot_required={sum(item['snapshot'] for item in claims)}")
print(f"zones={len({item['zone'] for item in claims})}")
```

The fixture is a design inventory, not proof of driver capability, persistence, application consistency, backup success, topology independence, performance, security, or recoverability.

### Use StatefulSet for stable member identity

A StatefulSet gives each pod a stable ordinal and name, stable DNS identity through a governing headless Service, and stable storage through `volumeClaimTemplates`. Recreated pod `database-2` can reattach the PVC created for ordinal 2. This is valuable when application membership maps state to a stable member identity.

It does not make arbitrary software stateful-safe. The application must define replication, quorum, leader election, member replacement, bootstrap, fencing, resynchronization, schema migration, and backup. A Deployment with one PVC may be correct for a single-instance service; an application-specific operator may be safer for a complex distributed database.

Default ordered pod management creates/scales lower ordinals first and deletes higher ordinals first, waiting on readiness. `Parallel` management removes ordering for scale operations where members are independent. Rolling updates proceed in reverse ordinal order under the StatefulSet strategy. Partitioning can stage updates, but readiness alone must represent application membership and data safety.

A broken rolling configuration can require manual pod deletion after reverting the template because the controller may wait on a pod that never becomes ready. Test forced rollback and maintain revision evidence; ControllerRevisions are rollout history, not data backup.

### Govern claim retention across StatefulSet lifecycle

Each `volumeClaimTemplate` normally creates one PVC per ordinal. By default, deleting or scaling the StatefulSet retains those claims, preserving data and requiring intentional cleanup. The optional PVC retention policy can set `whenDeleted` and `whenScaled` independently to `Retain` or `Delete` under supported cluster versions.

Choose from data semantics, not convenience. Retain is safer for authoritative state but can accumulate cost and regulated data. Delete is suitable for reproducible members only when replication/backup and ordinal removal workflows prove the copy is disposable.

The StatefulSet PVC-retention choice controls PVC deletion; the PV reclaim policy then controls the PV/backing volume. A `Delete`/`Delete` path can destroy storage after scale-down. A `Delete` PVC with `Retain` PV leaves provider data for manual recovery/erasure. Map the entire chain before approval.

Scale-down is a data operation. Confirm quorum and replica health, move leadership/partitions, drain clients, remove the member from application membership, verify backup, then change replicas. Scaling back up with a retained ordinal claim may revive stale membership or data; the application recovery procedure must decide whether to reuse, wipe, or resynchronize it.

### Design replication and fencing outside the volume API

Storage redundancy may protect media or infrastructure failure while remaining one logical copy vulnerable to deletion, corruption, bad writes, or compromised credentials. Application replication can provide availability and consistency, but only with correct quorum, failure-domain placement, lag bounds, and repair.

For a consensus group of $n$ voting members tolerating $f$ crash failures,

$$
n \ge 2f+1
$$

under the protocol's assumptions. Three PVCs in one zone do not tolerate zone loss, and three mounts of one shared filesystem are not three replicas. Record physical provider/account/zone dependencies.

Fencing prevents an old leader or node from continuing writes after authority moves. Attachment state alone may be delayed during partitions or node failure. Use protocol epochs, leases with monotonically increasing fencing tokens, storage reservations, or provider guarantees appropriate to the system. Never force-detach and attach a suspected live writer merely to reduce recovery time.

### Build application-consistent snapshot and backup workflows

Kubernetes VolumeSnapshot APIs represent namespaced requests, cluster-scoped contents, and classes; the CRDs, snapshot controller, CSI sidecar, and capable driver must be installed. `ReadyToUse` reports storage-system readiness, not application consistency or independent backup.

A crash-consistent snapshot resembles sudden power loss: it preserves a point-in-time storage image according to backend semantics. A database with a correct write-ahead log may recover; a multi-volume or distributed transaction may not. Application-consistent capture coordinates flush, checkpoint, freeze, database-native backup, log position, or group snapshot as supported, while bounding pause and write latency.

Snapshot locality can share provider account, region, control plane, encryption keys, and deletion authority with the source. Export or copy backups into an independent failure and administrative domain according to RPO, retention, immutability, residency, and cost. Protect catalogs, manifests, transaction logs, schemas, keys, and restore instructions together.

Backups need integrity verification, completeness, encryption, access separation, legal hold, expiry, and monitored deletion. A successful job without a restorable artifact and known data position is not success.

### Make restore the acceptance test

Restore into an isolated namespace, account, network, and identity so validation cannot overwrite production or call live dependencies. Select an artifact by time and application position, provision compatible storage, restore bytes, perform filesystem/database recovery, apply logs to the desired point, validate schema and invariants, run representative read/write tasks, and record duration and data loss.

Test empty bootstrap, recent and old backups, regional loss, missing log segment, corrupted artifact, lost key, changed driver/class, larger dataset, and dependency version changes. Recovery documentation should identify who can authorize data replacement and how client traffic is switched.

RPO and RTO are measurements from repeated exercises. Snapshot schedule is not RPO if capture, export, or log continuity can fail. Provider restore completion is not RTO if application replay, validation, DNS, credentials, and traffic activation take longer.

### Expand storage through every layer

Expansion requires a class with `allowVolumeExpansion`, driver support, provider capacity/quota, and a larger PVC request. Kubernetes supports growth, not shrink. The controller may expand the backing volume before the node expands the filesystem; raw-block applications have their own capacity discovery and allocation behavior.

Track requested PVC size, PV capacity, allocated-resource status, provider size, filesystem/block visible size, application allocation, and remaining headroom. In-use filesystem expansion depends on driver, filesystem, and node support. A request beyond provider limits may retry until corrected.

Do not edit PV capacity to simulate expansion; that can prevent the controller from performing required work. Shrink by creating a smaller target, copying and validating data, switching consumers, and retaining the old source until rollback expires.

Capacity planning includes bytes, inodes, IOPS, throughput, queue depth, snapshot delta growth, replica amplification, backup staging, rebuild traffic, and provider attach/volume limits. Alert early enough for provisioning, rebalance, and expansion latency.

### Engineer performance as an end-to-end contract

Measure application operation latency, filesystem latency, block latency, queueing, IOPS, throughput, cache hit/miss, flush latency, throttling, CPU, network, and provider metrics. Average latency hides tail stalls that trigger timeouts and failovers.

Performance depends on request size, read/write ratio, sequentiality, concurrency, sync writes, filesystem, mount options, encryption, volume size, provisioned limits, shared backend load, node bandwidth, zone path, snapshot activity, and application compaction. Benchmark representative workloads on supported classes, including steady state, burst, rebuild, snapshot, restore, and failure.

Do not promise IOPS from provider marketing alone. State measured envelope, test conditions, noisy-neighbor policy, and saturation behavior. Admission and quota should prevent workloads from requesting unsupported combinations or exhausting node attach limits.

### Secure every copy and control path

Encrypt data in transit to network storage and at rest at provider/storage layer where required; application-level encryption may be needed for stronger tenant or administrator boundaries. Define key ownership, rotation, backup, revocation, and recovery. Encryption without available keys destroys recoverability; shared keys preserve broad blast radius.

PVC namespace boundaries and pod references are control-plane controls. CSI controller/node components, service accounts, sockets, host mounts, provider credentials, snapshots, clones, backups, exports, and support tooling need least privilege. A subject able to create pods may be able to mount accessible claims or generic ephemeral volumes under policy.

Filesystem ownership and permission changes can be expensive on large volumes and behave differently across drivers. Define UID/GID, `fsGroup` support, root behavior, SELinux/AppArmor context where relevant, and shared-filesystem tenant isolation. Read-only mounts do not sanitize malicious content.

Data deletion must cover workload records, snapshots, clones, retained PVs, provider volumes, backups, replicas, caches, search indexes, and keys. Cryptographic erasure only works when keys are unique enough, protected, and actually destroyed across copies.

### Observe the storage state machine

Observe PVC phase and conditions, PV phase and claim, StorageClass, provisioner/controller health, CSI driver/node registration, scheduler events, topology, VolumeAttachment, provider operation, mount events, volume health where supported, filesystem errors, capacity/inodes, latency/throughput/queue, snapshot status, backup export, restore exercises, retention, and orphan inventory.

Use safe identities: namespace/PVC, PV, driver, class, zone, application member, provider volume alias, snapshot/backup ID, and restore exercise. Avoid secrets and sensitive paths in events or labels.

Correlate lifecycle time: claim creation to binding, scheduled pod to attach, attach to mount, mount to application readiness, snapshot request to ready/export, restore request to validated service, and deletion request to confirmed provider erasure. Long-tail operations determine rollout and recovery objectives.

### Diagnose without destructive guessing

For a Pending PVC, inspect class existence/defaults, requested modes and size, selector, quota, provisioner, capacity, binding mode, pod scheduling constraints, topology, and events. With `WaitForFirstConsumer`, a claim can legitimately wait for a schedulable pod; solve scheduling and storage jointly.

For an unscheduled pod, inspect CPU/memory and policy plus PVC binding, allowed topology, node affinity, taints, attach limits, and zone capacity. For attach failure, inspect VolumeAttachment, current/previous node, driver controller, provider state, fencing, and node reachability. Do not force detach until the former writer is proved fenced.

For mount failure, inspect node plugin, device/filesystem mode, filesystem type, mount options, permissions, corruption, encryption/key access, and node logs/events. For performance, correlate application and provider layers before moving data or changing classes.

For recovery, preserve source objects and provider data. Snapshot or clone where safe, set Retain before an approved PVC recreation procedure, record IDs, and validate claims before traffic. Never delete PVC/PV, remove finalizers, format a device, repair a filesystem, or reuse an ordinal based solely on a generic attach/mount error.

### Offer governed stateful platform products

Publish a small class catalog and conformance matrix across supported cluster, CSI driver, sidecar, provider, filesystem, and workload versions. Test provisioning, topology, attach/detach, node failure, expansion, snapshots, clone, reclaim, encryption, permissions, performance, upgrade, and cleanup.

Offer backup/restore workflows with inventories, independent copies, immutable retention, isolated exercises, and RPO/RTO reports. Provide StatefulSet patterns only for applications whose membership and recovery semantics are known; prefer managed services or mature operators when they reduce risk.

Chargeback should expose provisioned capacity, performance tier, replicas, snapshots, backups, transfer, idle retained volumes, and orphaned resources. Cost controls must never delete unknown authoritative data automatically; they route ownership and retirement decisions.

## Definitions and Notation

Let $P$ be a PV, $C$ a PVC, $W$ a workload member, $Z$ a topology domain, and $D(t)$ application data at time $t$. A binding is written

$$
C \leftrightarrow P \rightarrow Z,
$$

while the workload mounts $C$ and should not depend on the provider identity of $P$.

Let $a(t)$ be latest acknowledged application position and $r(t)$ latest independently recoverable position. Observed data exposure is

$$
RPO_{observed}(t)=a(t)-r(t),
$$

expressed in time or logical log position. Let $t_f$ be failure declaration and $t_v$ validated service restoration; then

$$
RTO_{observed}=t_v-t_f.
$$

Define usable state for member $w$:

$$
U_w=Bound\land Scheduled\land Attached\land Mounted\land Intact\land Owned\land CapacityOK\land PerformanceOK\land DataValid.
$$

A green `Bound`, `Attached`, or `ReadyToUse` condition proves only one conjunct or storage-layer state.

For replicas $i$ and $j$, $zone(i)\ne zone(j)$ is useful only when those zones and their storage/control dependencies are operationally independent under the declared failure model.

## Mechanisms, Invariants, or Proof Structure

The mechanism is a coupled reconciliation chain. A claim requests a governed class; provisioning or selection creates/binds a PV; scheduling chooses reachable topology; CSI controller and node components attach and mount; the application establishes data ownership and recovery; backup controllers capture/export artifacts; restore workflows validate recoverability; lifecycle controllers eventually retain or delete objects and provider resources.

The **identity invariant** keeps claim/member identity stable across pod replacement. The **topology invariant** makes storage reachable from the scheduled member and separates replicas across real failure domains. The **single-writer invariant** combines attach constraints with application fencing rather than trusting access-mode names.

The **durability invariant** maps every acknowledged state to replication and independently recoverable artifacts meeting the RPO. The **recovery invariant** proves artifacts through isolated restore and application validation within RTO. The **lifecycle invariant** maps StatefulSet retention, PVC deletion, PV reclaim, snapshot/backup retention, and provider erasure without implicit gaps.

The **capacity/performance invariant** maintains bounded headroom and latency under steady, burst, rebuild, and backup load. The **security invariant** covers every live and retained copy plus CSI/provider authority and encryption keys.

These invariants form an assurance structure, not a proof that a storage system is durable. Provider guarantees, driver correctness, application protocols, physical failure independence, backup integrity, keys, and operational execution remain assumptions requiring evidence.

## Alternatives and Trade-Offs

Ephemeral storage is fast and simple for discardable data but couples loss to pod/node lifecycle. Network persistent storage supports movement and managed durability at added latency, provider dependency, and cost. Local persistent storage offers locality and performance but couples recovery to a node and requires explicit replication/replacement.

Filesystem volumes provide familiar paths and shared-file semantics; raw block gives specialized applications control but transfers formatting and integrity responsibility. RWO is widely supported but is not pod exclusion; RWOP narrows attachment for one pod but needs CSI support. RWX enables multiple nodes but adds cache, locking, tenant, and noisy-neighbor concerns.

Immediate binding reduces claim latency and fits topology-independent storage. Delayed binding preserves placement choices for constrained volumes but means claim readiness depends on a schedulable consumer. Retain reduces accidental loss and aids forensic recovery while accumulating cost and erasure work; Delete automates cleanup but magnifies mistaken PVC deletion.

StatefulSet provides stable identities with generic lifecycle controls. An application operator can encode membership, backup, failover, and upgrades, but adds controller authority and complexity. A managed state service may offer stronger operations and regional recovery while introducing vendor, network, compliance, and cost trade-offs.

Synchronous replication can reduce acknowledged loss but adds latency and quorum availability constraints. Asynchronous replication preserves latency/availability over distance with nonzero RPO. Snapshots are efficient point-in-time copies but may share failure domains; exported logical/physical backups improve independence at time, bandwidth, and restore cost.

## Failure Modes and Misconceptions

- **“PersistentVolume means durable.”** It means lifecycle independence from a pod; provider, topology, replication, corruption, deletion, and backup determine durability.
- **“Bound means ready for the application.”** Scheduling, attach, mount, filesystem, ownership, capacity, performance, recovery, and data validity remain.
- **“RWO prevents two pods from writing.”** It restricts read-write mount to one node; co-located pods may share it. RWOP and application fencing address different layers.
- **“Three StatefulSet pods are three replicas.”** Only the application/storage protocol creates and verifies copies; placement may still share one failure domain.
- **“StatefulSet deletion deletes—or preserves—all data.”** PVC retention and PV reclaim policies combine, and snapshots/backups have independent lifecycle.
- **“A ReadyToUse snapshot is a backup.”** It may be crash-consistent, incomplete across volumes, locally dependent, mutable/deletable by the same authority, or never restored.
- **“Immediate binding is faster and therefore safer.”** It can preselect an inaccessible zone and make the consumer unschedulable.
- **“Expansion gives the application space immediately.”** Provider, PV/PVC, node filesystem or block layer, and application allocation converge separately; shrink is unsupported.
- **“Force detach repairs failover.”** Without proving the previous writer fenced, it can create split brain and corruption.
- **“Retain is enough protection.”** It preserves a released backing volume but not catalog knowledge, keys, backup, replication, access, or tested recovery.
- **“Encryption solves deletion and tenancy.”** Copies, shared keys, authorized readers, live plaintext, snapshots, backups, and metadata remain.
- **“Deleting and recreating the PVC is ordinary troubleshooting.”** It is a data-lifecycle operation whose effect depends on reclaim, binding identity, and provider state.

## Worked Examples

### Example 1

A cache writes to `emptyDir` with a size limit and accepts eviction loss; authoritative objects live in object storage. Readiness warms gradually instead of pretending the cache is durable.

### Example 2

A zonal PVC bound immediately in zone A while the pod required a GPU in zone B. A topology-aware class with `WaitForFirstConsumer` lets the scheduler solve both constraints.

### Example 3

Two database pods on one node mount an RWO claim and corrupt files. The design changes to RWOP where supported plus protocol fencing, distinct identities, and recovery tests.

### Example 4

A StatefulSet scales from five to three with retained PVCs. The database first removes members and partitions; owners later approve backup, retention expiry, and erasure of ordinals four and three.

### Example 5

A crash-consistent snapshot of data and log volumes captures different transaction points. The backup workflow uses database checkpoint/log position and coordinated capture, then restores and validates both.

### Example 6

PVC expansion reaches the provider but not the filesystem. Status separates requested, allocated, PV, node-visible, filesystem, and application sizes and completes the supported filesystem resize.

### Example 7

A node is unreachable and a volume appears attached. Operators fence the node at infrastructure and application layers before detach/reattach, preventing a stale writer from returning.

### Example 8

Snapshots and volumes share one provider account compromised by an attacker. Immutable exported backups in a separately administered account and region enable isolated recovery.

### Example 9

A shared RWX filesystem meets throughput but metadata latency and inode exhaustion cause tail failures. The platform adds inode, operation-latency, queue, and tenant quota objectives rather than watching bytes alone.

### Example 10

A retained PV lacks an owner after namespace deletion. Inventory connects provider ID, former claim, classification, backup, legal hold, cost, and approver so recovery or erasure is intentional.

## Cross-Program Connections

Operating systems contributes filesystems, blocks, caching, flush, permissions, devices, and corruption. Distributed systems contributes replication, quorum, consensus, fencing, partitions, and consistency. Databases contributes logs, checkpoints, transactions, backup, point-in-time recovery, and membership.

Reliability engineering contributes RPO/RTO, failure-domain analysis, capacity, objectives, drills, and incident recovery. Security contributes encryption, keys, authorization, isolation, audit, ransomware resistance, and erasure. Data engineering and governance contribute lineage, residency, retention, legal hold, quality validation, and authoritative-copy ownership.

Performance engineering contributes latency distributions, IOPS, throughput, queues, caching, and representative benchmarks. Finance contributes provisioned capacity, tiers, replicas, snapshots, transfer, backup, and orphan cost. Platform product engineering turns provider/CSI capabilities into measured, versioned classes and safe workflows.

## References

- Kubernetes Project, [*Volumes*](https://kubernetes.io/docs/concepts/storage/volumes/), current documentation retrieved September 2, 2026. Container filesystems, pod volume mounting, ephemeral versus persistent lifetime, shared data, CSI volume forms, and volume types.
- Kubernetes Project, [*Persistent Volumes*](https://kubernetes.io/docs/concepts/storage/persistent-volumes/), current documentation retrieved September 2, 2026. PV/PVC lifecycle and binding, protection, reclaim, access/volume modes, node affinity, raw block, expansion, snapshots, cloning, and portability.
- Kubernetes Project, [*Storage Classes*](https://kubernetes.io/docs/concepts/storage/storage-classes/), current documentation retrieved September 2, 2026. Provisioners, parameters, defaults, reclaim, expansion, mount options, immediate/delayed binding, allowed topology, and local volumes.
- Kubernetes Project, [*Dynamic Volume Provisioning*](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/), current documentation retrieved September 2, 2026. StorageClass selection, defaulting, dynamic PV creation, and provisioning lifecycle.
- Kubernetes Project, [*StatefulSets*](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/), current documentation retrieved September 2, 2026. Stable ordinal/network/storage identity, volume claim templates, ordered/parallel management, rolling updates, revisions, forced rollback, and PVC retention.
- Kubernetes Project, [*Volume Snapshots*](https://kubernetes.io/docs/concepts/storage/volume-snapshots/), current documentation retrieved September 2, 2026. Snapshot, content, and class resources; CSI/controller/CRD dependencies; deletion policy; readiness; topology; and restore data sources.
- Kubernetes Project, [*Ephemeral Volumes*](https://kubernetes.io/docs/concepts/storage/ephemeral-volumes/), current documentation retrieved September 2, 2026. `emptyDir`, CSI and generic ephemeral lifecycles, generated PVC ownership, delayed binding, quotas, naming, admission, and cleanup.
- Kubernetes Project, [*Local Ephemeral Storage*](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#local-ephemeral-storage), current documentation retrieved September 2, 2026. Requests, limits, accounting scope, node allocation, eviction, writable layers, logs, and `emptyDir` consumption.
- Kubernetes Project, [*Storage Capacity*](https://kubernetes.io/docs/concepts/storage/storage-capacity/), current documentation retrieved September 2, 2026. CSI capacity reporting, scheduler decisions, delayed binding, topology, and stale-capacity behavior.
- Kubernetes Project, [*Volume Health Monitoring*](https://kubernetes.io/docs/concepts/storage/volume-health-monitoring/), current documentation retrieved September 2, 2026. CSI health capability, controller/node detection, PVC events/conditions, and driver dependency.
- Kubernetes CSI, [*Snapshot & Restore Feature*](https://kubernetes-csi.github.io/docs/snapshot-restore-feature), current developer documentation retrieved September 2, 2026. Snapshot controller and external-snapshotter architecture, CRDs, sidecars, driver capabilities, lifecycle, and restoration.
- Kubernetes CSI, [*CSI Sidecar Containers*](https://kubernetes-csi.github.io/docs/sidecar-containers.html), current developer documentation retrieved September 2, 2026. External provisioner, attacher, snapshotter, resizer, health monitor, compatibility, and CSI controller responsibilities.

## Exercises

### Exercise 1

Design storage classes and workload bindings for a discardable build cache, single-writer transactional database, shared media filesystem, append-only audit archive, and three-zone replicated message service. Include topology, modes, performance, encryption, reclaim, backup, restore, and cost.

### Exercise 2

Audit a StatefulSet with three pods, one RWX claim shared by all members, all pods in one zone, no application quorum, `Delete` reclaim, automated PVC deletion on scale-down, daily snapshots in the same account, and no restore exercises.

### Exercise 3

Design an application-consistent backup and point-in-time recovery workflow for a database with separate data and WAL volumes, continuous writes, a 5-minute RPO, 60-minute RTO, regional-loss requirement, encryption, and 35-day retention.

### Exercise 4

Diagnose a pod stuck Pending after a node pool migration: its PVC is Pending, StorageClass uses `WaitForFirstConsumer`, the pod sets `nodeName` to an old node, the class permits two zones, and provider capacity is available. Then explain a safe response if the old bound volume instead appears attached to an unreachable node.

### Exercise 5

Transfer the storage-binding model to scientific instruments at remote observatories that collect irreplaceable data with intermittent networks. Address local media, identity, integrity, capacity, replication, transfer, catalog, retention, encryption, recovery, erasure, and human authority.

## Answers to the Exercises

### Answer 1

The build cache uses bounded `emptyDir` or generic ephemeral zonal storage with Delete, quotas, and no backup because source inputs reproduce it. The database uses a measured encrypted zonal class, delayed binding, filesystem or block mode required by the engine, RWOP where supported plus application fencing, Retain, expansion, latency/flush objectives, application-consistent backup, exported copies, and tested point-in-time recovery. Shared media uses an RWX class with explicit locking, UID/GID, inode, throughput, tenant quota, encryption, snapshots plus independent backup, and deletion tied to object lifecycle. The audit archive is preferably immutable object/archive storage rather than a mutable PVC; if staged on a volume, use encrypted Retain, narrow writers, checksums, export, legal retention, and erasure approval. The message service uses one zonal claim per member across three independent zones, protocol replication/quorum/fencing, delayed binding, controlled disruption, Retain until member retirement, and restore/replay evidence. Cost covers provisioned tiers, replicas, snapshots, exports, transfer, retained volumes, and exercises.

### Answer 2

Three pods and one shared filesystem are one storage copy and do not establish replication, quorum, or safe concurrent writes. Co-location loses all members to one zone event. Define the application's membership and consistency protocol first, normally with a distinct claim per member, single-writer fencing where applicable, and topology spread across real failure domains. Change destructive policies before testing: retain PVCs and PVs while data authority is unknown, require an application member-removal workflow before scale-down, and prevent generic autoscaling from deleting state. Same-account daily snapshots can be deleted or lost with the source, may be crash-consistent, and give up to a day of nominal loss. Create application-aware captures/log continuity, export immutable encrypted backups to a separately administered region/account, inventory keys and positions, and perform isolated restore/business validation. Only after replication, backup, recovery, ownership, and erasure are proved should retention/reclaim automation be narrowed.

### Answer 3

The database periodically coordinates a checkpoint and records a consistent WAL position while snapshotting data/WAL coherently or uses a database-native physical backup. Continuous WAL is segmented, checksummed, encrypted, and exported with manifests and schema/version metadata to a separate regional/account failure domain. Monitoring proves the gap between latest acknowledged and independently recoverable log position stays under five minutes; snapshot schedule alone is insufficient. Retain daily/weekly artifacts according to the 35-day policy with immutable protection, catalog integrity, key availability, legal exceptions, and confirmed expiry. Restore automation provisions compatible isolated storage, restores the base, replays an unbroken WAL chain to a requested timestamp, performs recovery, validates schema/invariants and representative writes, and measures failure declaration through safe traffic readiness under 60 minutes. Exercises cover corrupt base, missing segment, regional loss, lost key, changed driver/class, and full-size data. Production replacement requires named authorization and retains the old source for a bounded rollback window.

### Answer 4

The scheduler must participate in delayed binding, but `nodeName` bypasses it; the claim can remain Pending even with provider capacity. Remove direct `nodeName`, express any valid requirement with node affinity/selector across supported zones, and inspect pod scheduling plus PVC/provisioner events together. The scheduler can then choose a node and the provisioner can create/bind storage in matching topology. If an existing volume is attached to an unreachable old node, preserve the PVC/PV and data identity. Determine node and provider state, application leadership, outstanding writes, attachment, fencing capability, and recovery objective. Fence the old node from power/network/storage and advance application epoch or lease before requesting detach/reattach. Confirm the provider no longer permits the old writer, then schedule in reachable topology, attach, mount, recover filesystem/application, and validate data before traffic. Never delete claims, remove finalizers, or force-detach solely to clear status.

### Answer 5

Each instrument and acquisition session receives stable identities; local writes use redundant, monitored media with append-only segments, checksums, monotonic sequence, timestamps, calibration/configuration version, and a durable catalog. Capacity reserves cover the longest plausible disconnection plus margin, and acquisition sheds only reproducible secondary products before raw observations. When connectivity returns, resumable encrypted transfer sends content-addressed chunks to two independent regional repositories, verifies completeness and integrity, and records custody before local deletion becomes eligible. Device-unique hardware-backed keys protect data and authenticate transfer; key backup/recovery does not collapse every instrument into one credential. Retention distinguishes raw science, derived products, calibration, personal/environmental restrictions, and legal commitments. Recovery exercises rebuild a session from local replica, regional archive, catalog, and keys. Erasure covers media, staging, replicas, backups, and retired keys under approved policy. Observatory operators can halt deletion, replace failing media, and prioritize transmission during hazards; central automation reports capacity and integrity but cannot silently discard irreplaceable observations.
