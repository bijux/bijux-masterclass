# Module 07 — Snapshots, Clones, Populators, and Consistency

> **Governing question:** What does a point-in-time copy actually contain, and what coordination is required before it can be trusted for recovery or testing?

## Why this module exists

A `VolumeSnapshot` reaches `readyToUse: true`. The restored database starts crash recovery, then reports a missing transaction-log segment because the data and log volumes were captured at different times. The snapshot API succeeded exactly as requested; the recovery design was wrong.

This module does not begin with YAML. It begins by locating authority and the earliest missing transition. Kubernetes storage is a set of cooperating control loops around an external data system; the application still owns the meaning and correctness of the data.

## Learning outcomes

- trace VolumeSnapshot, VolumeSnapshotContent, and VolumeSnapshotClass ownership
- distinguish pre-provisioned and dynamic snapshots
- compare snapshots, clones, and data populators
- separate crash-consistent, filesystem-consistent, and application-consistent states
- coordinate group snapshots and multi-volume restore
- verify snapshot lineage, readiness, deletion policy, and restore behavior

## Snapshot APIs coordinate references and controller work

A `VolumeSnapshot` is a namespaced request, comparable to a PVC. `VolumeSnapshotContent` is cluster-scoped supply, comparable to a PV. `VolumeSnapshotClass` selects the driver, parameters, and deletion policy. The snapshot controller binds requests to content, while the CSI snapshotter sidecar calls the driver. The resources are extension APIs installed by the distribution or cluster administrator.

A snapshot reaching `readyToUse` means the storage system and controllers report the copy usable according to their contract. It does not mean the application had flushed buffers, completed a checkpoint, or captured multiple volumes consistently.
## Crash consistency is a precise but limited guarantee

A crash-consistent snapshot should resemble the storage after abrupt power loss. Journaling filesystems and databases may recover correctly, lose recent acknowledged work depending on their durability settings, or require manual repair if invariants span devices. Filesystem freeze can improve metadata consistency but still does not coordinate application buffers or distributed transactions.

Application consistency requires an application-aware protocol: pause or redirect writes, flush buffers, create a database checkpoint or backup marker, capture all required volumes, record the logical recovery point, then resume. The protocol must have a maximum pause budget and a cleanup path when snapshot creation fails.
## Clones are provisioning tools, not retention policies

A CSI volume clone creates a new volume from an existing PVC, normally within driver and namespace constraints. It is useful for test environments, migrations, or rapid copy-on-write creation. The clone may share backend blocks and failure domains with the source. It is not automatically an independent backup.

Restoring a PVC from a VolumeSnapshot similarly creates a new volume whose initial content comes from the snapshot. The new volume’s class, size, topology, encryption, and performance profile must be compatible. Atlas records source identity and copy generation so test data cannot be mistaken for production authority.
## Data populators generalize initial content

`dataSource` supports PVC clones and VolumeSnapshots. `dataSourceRef` can reference custom data sources when the appropriate feature and populator controller are available. A populator may fill a new volume from an object-store backup, external dataset, or application-specific resource. This is a controller protocol with its own authorization, retry, and status requirements.

A PVC waiting for a missing populator should not be diagnosed as a generic provisioner failure. Atlas manifests use explicit data-source types and include the controller dependency in release evidence.
## Group snapshots coordinate storage, not applications

Volume group snapshots request a crash-consistent point across a selected set of PVCs when the CSI driver and snapshot stack support the feature. This is valuable for data and log volumes or sharded filesystems. It still captures storage-level consistency. A database may require pre-freeze or checkpoint hooks before the group operation and post-thaw behavior afterward.

The course uses a conservative implementation API profile because served CRD versions depend on the installed external-snapshotter release. The feature’s Kubernetes lifecycle status and the actual cluster API surface are verified separately.
## Deletion policy and restoration are part of snapshot design

A snapshot class with `Delete` may remove the snapshot content and backend copy when the namespaced request is deleted. `Retain` preserves the content, but operators must still maintain identity, encryption keys, ownership, and cleanup procedures. Snapshots can consume backend capacity through copy-on-write deltas and may degrade source performance.

Every Atlas snapshot has a purpose, owner, source generation, consistency level, retention, and tested restore path. Unowned snapshots are not free safety; they are ungoverned data copies.

## Snapshot freeze hooks must fail safely

If quiescing succeeds and snapshot creation fails, the application must resume within a bounded interval. If unquiesce fails, operators need an alert and a safe recovery action. A controller should record each phase durably so restart does not leave the application frozen indefinitely.

Atlas’s coordinator models prepare, quiesce, snapshot, verify, and resume as separate states. Cleanup is attempted on every failure path, and the application checkpoint is recorded only when the coordinated set is complete.


## Snapshot identity must survive API object deletion

A retained snapshot content may outlive the namespaced VolumeSnapshot. Operators need a durable mapping from logical recovery point to VolumeSnapshotContent and backend snapshot handle. Otherwise retained copies become anonymous and dangerous to delete.

The Atlas snapshot catalogue records source PVC UID, PV identity, backend handle, class, consistency, checkpoint, encryption context, creation generation, and retention owner.


## Cross-namespace data sources are an authority change

Allowing a PVC to populate from a source in another namespace crosses an ownership boundary. Reference authorization, source immutability, tenant isolation, and audit evidence become necessary. A clone or restore can copy sensitive data even when the destination workload cannot reach the source service over the network.

Course 6 denies cross-namespace sources by default and requires an explicit platform policy for approved cases.


## Copies need lineage and freshness labels

A restored or cloned database may be correct but stale. If it is exposed through production names, clients can mistake it for authority. Atlas assigns a new instance identity and records source recovery point. Promotion to authoritative state requires a separate cutover and fencing decision.

This prevents test clones, disaster-recovery drills, and forensic copies from joining normal service discovery accidentally.

## Worked semantic example

```python
from atlas_data.snapshots import SnapshotCoordinator

coordinator = SnapshotCoordinator()
record = coordinator.application_snapshot(
    group="atlas-db",
    volumes=["data", "wal"],
    quiesce=lambda: "checkpoint-8842",
)
assert record.consistency == "application"
assert record.recovery_point == "checkpoint-8842"
```

The example is intentionally small enough to inspect. It establishes one invariant in the dependency-light lane; it does not claim native Kubernetes or storage-system conformance.

## Production-intent API fragment

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: atlas-db-data-2026-08-09
  namespace: atlas-system
spec:
  volumeSnapshotClassName: atlas-retained
  source:
    persistentVolumeClaimName: data-atlas-db-0
```

The manifest is a contract candidate. Its effect depends on admission, installed controllers, CSI capabilities, backend behavior, and application compatibility.

## Failure signatures

| Observation | Likely missing guarantee | Decisive evidence |
|---|---|---|
| ready snapshot | copy is crash-consistent only | application checkpoint evidence |
| group mismatch | volumes captured at different points | group snapshot plus app coordination |
| clone mistaken for backup | same failure domain destroys both | independent retention |

## Atlas capstone increment

A snapshot coordinator records consistency level, application checkpoint, source generation, grouped volumes, retention, and restore verification.

## Evidence boundary

The module’s Python and filesystem tests can falsify logical invariants and local durability mechanisms. Cluster controller behavior, CSI RPC behavior, snapshot semantics, cloud durability, and operated recovery require the corresponding native evidence lane. Record unavailable evidence as `not-executed`.

## Transition

Module 8 exports protected copies beyond the source failure domain and proves restoration against explicit RPO and RTO.

## Advanced design review — snapshots create a dependency graph

A snapshot can be a full copy, thin copy, redirect-on-write tree, or provider-defined construct. Clones and later snapshots may depend on it. Deletion and performance behavior therefore require a graph, not a flat list. Track source, parent, dependents, backend handle, consistency, recovery point, key, and deletion policy.

Group snapshots solve only storage-side coordination. Application consistency still requires a protocol with bounded freeze time and guaranteed resume. The controller must be able to reconcile a timeout after the backend created some or all snapshots. Leaving the database frozen to preserve a backup attempt is an availability defect.

## Restore is the specification test

The most useful snapshot test creates new claims, starts compatible software with side effects disabled, and validates the recorded recovery point. This test reveals missing keys, unsupported topology, stale classes, filesystem incompatibility, and application inconsistency. Snapshot creation without restore evidence remains an inventory claim, not a recovery guarantee.

## Snapshot portability is narrower than backup portability

Kubernetes snapshot objects make creation and restoration portable at the API level, but snapshot content remains tied to a driver, backend, region, account, and implementation. A VolumeSnapshot from one driver generally cannot be restored by another, and exported metadata alone is not the data. This matters during cluster migration and provider exit.

If portability is a requirement, add an export or backup path whose format and keys can be consumed independently. Keep snapshots for fast local recovery, but do not let their convenient API hide the backend dependency. Test restoration after upgrading the driver and snapshot controllers because retained content can outlive the components that created it.

## Consistency labels are contracts

Use a small vocabulary—crash-consistent, filesystem-consistent, application-consistent, and transactionally coordinated—and define the procedure and oracle behind each. Do not infer consistency from the name of a snapshot class or backup product. The same backend can produce different guarantees depending on quiesce, logs, and group coordination.

A recovery catalogue should let an operator filter copies by usable consistency and target. If only crash-consistent copies exist, the runbook must state which engines and versions can recover them. Honest labels are more valuable than optimistic ones because they guide safe decisions during an incident.
## A snapshot captures storage state, not necessarily application truth

A storage snapshot can be perfectly valid while containing an application state that requires recovery or is unusable. The storage layer usually sees blocks or filesystem contents; it does not understand transaction boundaries, distributed membership, object indexes, or application invariants. The first question is therefore: **what consistency level does this recovery point claim?**

- A **crash-consistent** snapshot approximates sudden power loss at the captured instant.
- A **filesystem-consistent** snapshot includes filesystem coordination but may still interrupt application transactions.
- An **application-consistent** snapshot coordinates the application so its on-disk representation is a documented recovery point.
- A **distributed-consistent** snapshot also coordinates related volumes or services sufficiently to preserve cross-component invariants.

These terms should be recorded in metadata and validated by restore, not inferred from a `readyToUse` status.

### Snapshot workflow with application coordination

A defensible application-consistent workflow may be:

1. acquire a backup or checkpoint lease;
2. stop or redirect writes;
3. flush application buffers and database logs;
4. record the exact logical generation or log position;
5. request the snapshot or group snapshot;
6. wait for the storage-system recovery point;
7. record snapshot content identity and topology;
8. release the application checkpoint;
9. restore into an isolated destination;
10. run application-level validation.

The quiesce window should be bounded. If snapshot creation is asynchronous, the application needs to know when the storage point was actually captured, not merely when the API request was accepted.

### VolumeSnapshot objects and backend contents

The snapshot API separates user intent, cluster representation, and backend snapshot identity. A `VolumeSnapshot` is the namespaced request. A `VolumeSnapshotContent` represents the cluster-level snapshot content and references the backend handle. A `VolumeSnapshotClass` defines driver and deletion policy. The external snapshotter and CSI driver reconcile these objects.

Deletion policy matters. Removing a namespaced snapshot can delete or retain the backend recovery point depending on class policy and content lifecycle. Backup systems must not assume that a Kubernetes object and the backend copy have identical retention.

### Group snapshots and cross-volume boundaries

A group snapshot can coordinate a crash-consistent point across several PVCs when the installed implementation supports it. This is valuable for applications that split data across multiple volumes. It does not automatically coordinate external services, object storage, message brokers, or application metadata outside the selected group.

The group definition must be stable and auditable. If a new volume is added to the application but omitted from the selector, the snapshot can report success while the recovery set is incomplete. Atlas records the member PVC identities and application checkpoint generation in the evidence dossier.

### Clones and data sources preserve lineage

PVC cloning and snapshot restore create new writable volumes from existing data. Custom populators can prepare a new claim from another source. These mechanisms are powerful for testing, migration, and recovery, but every derived volume needs lineage:

```text
source identity
source generation
copy mechanism
creation time
consistency class
encryption/key context
validation result
intended environment
```

Without lineage, a clone can be mistaken for the authoritative primary or can introduce sensitive production data into an unsafe environment. Admission and automation should enforce destination policy.

### Restore is the real compatibility test

Snapshot creation tests only part of the path. A complete proof restores to a new claim and verifies:

- expected filesystem or block layout;
- application startup;
- logical schema and version;
- transaction or log consistency;
- membership and fencing metadata;
- object counts or checksums;
- secrets and keys;
- absence of writes to the original source;
- ability to continue normal operation.

Restoring over the primary destination hides errors and risks corruption. Atlas requires an empty destination and treats the restored environment as untrusted until validation succeeds.

### Snapshot retention and cost

Snapshots often share blocks with their source and later consume more space as data changes. Retention cost is therefore workload-dependent. Long chains can increase recovery complexity and backend coupling. Deleting the original volume may change snapshot storage accounting or behavior depending on the provider.

A snapshot policy specifies:

- schedule and trigger;
- consistency class;
- retention count and duration;
- cross-account or cross-region requirements;
- encryption-key ownership;
- deletion policy;
- restore frequency;
- maximum acceptable restore-chain depth;
- monitoring for stalled or orphaned contents.

### Populator trust boundary

A custom volume populator is a controller that writes data into a new claim. It may read external sources, use credentials, and create large data copies. Treat it as a privileged data-migration component. Validate source identity, tenant scope, checksum, destination emptiness, retry behavior, cancellation, and cleanup. A populator should publish completion only after the target is verifiably usable.

### Snapshot release gate

A release may claim snapshot support only when it has evidence for:

1. installed CRDs and controller versions;
2. driver snapshot capability;
3. class and deletion policy;
4. consistency procedure;
5. content identity and retention;
6. empty-destination restore;
7. application-level validation;
8. failure and cancellation cleanup;
9. key availability;
10. a tested ownership and escalation path.

This gate prevents “snapshot exists” from being promoted into “service is recoverable.”
