# Module 04 — Topology, Scheduling, Capacity, Expansion, and Storage QoS

> **Governing question:** How can compute placement and storage placement converge without deadlock, false capacity, or unsafe in-place mutation?

## Why this module exists

Atlas needs two 100 GiB claims and three replicas spread across two zones. Capacity objects report enough storage overall. The scheduler selects a Node, one claim provisions, and the second fails. The first bound volume pins the Pod to a topology segment that can no longer satisfy the second claim.

This module does not begin with YAML. It begins by locating authority and the earliest missing transition. Kubernetes storage is a set of cooperating control loops around an external data system; the application still owns the meaning and correctness of the data.

## Learning outcomes

- combine Pod constraints with PV node affinity and CSI topology
- explain WaitForFirstConsumer selected-node behavior
- use capacity information without treating it as a reservation
- reason about attach limits and multi-volume scheduling
- separate controller expansion, node expansion, and filesystem growth
- govern VolumeAttributesClass changes as service-level mutations

## Scheduling now has two resource graphs

A Pod without persistent storage is scheduled against CPU, memory, devices, taints, affinity, topology spread, and other Node predicates. A Pod with unbound or bound volumes adds storage class, provisioner, topology, capacity, access, and attachment constraints. These graphs interact. A Node that fits compute may not access the PV. A zone with storage capacity may not have a Node satisfying Pod affinity.

Course 6 models scheduling as an explanation problem. For every rejected Node, preserve the failed predicates. “No nodes available” is insufficient; the operator needs to know whether the blocker is compute, topology, capacity, claim state, or attachment limits.
## WaitForFirstConsumer is a coordination protocol

Delayed binding lets the scheduler tentatively select a Node and annotate the PVC so the provisioner can create storage in an accessible topology. The selection is not final until provisioning and binding complete. If the backend rejects creation, scheduling can be retried. This is coordination across controllers, not a single atomic transaction.

The selected-node annotation should not be edited casually. Repeated failures can reflect stale capacity, class restrictions, unavailable zones, provider quotas, or incompatible multiple claims. Atlas records the scheduling attempt and provisioning result together.
## Capacity advertisements are observations

`CSIStorageCapacity` can help the scheduler avoid Nodes whose accessible segments lack requested capacity. The values may be stale and are not reservations. Concurrent claims, backend allocation granularity, quotas, and fragmentation can invalidate them. A successful scheduling filter improves probability; it does not guarantee provisioning.

Capacity decisions therefore include safety margins and retry behavior. For critical state, the platform also monitors backend capacity directly and tests claim creation before an emergency requires it.
## Node attachment limits are real capacity

Many cloud and CSI backends limit the number of volumes attachable to a Node. The scheduler considers driver-reported limits, but stale state or mixed drivers can complicate placement. A Node can have ample CPU and storage bytes yet be unable to attach another volume. Large StatefulSets with one PVC per Pod frequently encounter this boundary.

Atlas capacity reports count attachment slots per Node and per driver, not only GiB. Scaling a workload or moving it during maintenance must fit both storage topology and attachment capacity.
## Expansion is a multi-stage migration

PVC expansion updates the requested size. The external resizer may call controller expansion. The backend grows the volume. If a filesystem is present, node expansion and filesystem growth may occur when the volume is mounted. Status conditions reveal whether controller or filesystem resize remains pending. Shrinking is generally not supported through the same flow.

An expanded volume does not automatically mean the database or application uses the new capacity correctly. Filesystem, tablespace, quota, alert, backup, and restore assumptions may require updates. Atlas treats expansion as a reviewed change with before/after evidence.
## Mutable service tiers with VolumeAttributesClass

VolumeAttributesClass allows a PVC to reference a mutable storage service profile when the driver supports modify-volume behavior. This can change provisioned IOPS or throughput without replacing the volume. The API object is stable, but parameters are driver-specific and the actual transition can be asynchronous.

The platform must define permitted transitions, cost effects, rollback behavior, and status interpretation. Moving from `silver` to `gold` is not just metadata; it is a change to performance and cost assumptions. Atlas blocks a release until the volume reports the requested class and measured behavior meets the workload budget.

## Multiple claims turn scheduling into a packing problem

A Pod using several unbound claims may need all volumes provisioned in one accessible topology. The scheduler and provisioner coordinate each claim, but the backend may allocate them sequentially. If capacity becomes insufficient partway through, already-created volumes can constrain future attempts. This is not a simple sum-of-capacity problem because classes, zones, attach limits, and allowed topologies differ.

For critical multi-volume workloads, preflight capacity, reserve headroom, or use a backend feature designed for coordinated allocation. Atlas keeps the first failed allocation visible and requires explicit cleanup before retry.


## Topology labels are part of a driver API

CSI drivers advertise topology keys and Node values. StorageClasses can restrict allowed topologies, and PVs record node affinity. Renaming or changing topology labels during driver migration can strand existing volumes. The labels are not merely scheduling metadata; they connect Kubernetes to backend accessibility.

A driver upgrade or cloud-region change must verify old PV affinity and new CSINode topology. Course 6’s migration ledger records this compatibility boundary.


## Expansion failure needs a safe retry path

If controller expansion succeeds but node expansion fails, the backend is larger while the filesystem remains smaller. Repeating the operation should not create another volume or shrink anything. The status condition and requested capacity must remain available for reconciliation. Operators should not edit PV capacity to hide the mismatch.

Atlas injects this partial state and verifies that the resizer resumes from the correct phase. The application remains usable when the old filesystem size is safe, but capacity alerts must use the effective filesystem size until growth completes.


## Performance tiers are not labels alone

A VolumeAttributesClass or provider parameter can request IOPS or throughput. Actual performance depends on volume size, backend limits, Node path, network, filesystem, queueing, and workload. The platform must measure the declared workload after the transition. If the driver reports success but the workload budget is not met, the release remains review-required.

Cost and quota changes are also part of the decision. A tier upgrade that exhausts account-level IOPS quota can harm unrelated workloads.

## Worked semantic example

```python
from atlas_data.topology import Scheduler, Node, CapacitySegment

scheduler = Scheduler(
    nodes=[Node("node-a", "zone-a", attach_limit=8)],
    capacities=[CapacitySegment("zone-a", "atlas-rwo-durable", 500)],
)
decision = scheduler.place(pod="atlas-db-0", claims=[("db", 20)])
assert decision.node == "node-a"
assert decision.explanations["node-a"] == []
```

The example is intentionally small enough to inspect. It establishes one invariant in the dependency-light lane; it does not claim native Kubernetes or storage-system conformance.

## Production-intent API fragment

```yaml
apiVersion: storage.k8s.io/v1
kind: VolumeAttributesClass
metadata:
  name: atlas-throughput
driverName: csi.atlas.example.invalid
parameters:
  provisioned-iops: "5000"
  provisioned-throughput-mibps: "250"
```

The manifest is a contract candidate. Its effect depends on admission, installed controllers, CSI capabilities, backend behavior, and application compatibility.

## Failure signatures

| Observation | Likely missing guarantee | Decisive evidence |
|---|---|---|
| capacity stale | scheduling succeeds then provisioning fails | retry plus capacity observation |
| attach limit | Node fits compute but not volumes | driver-specific slot accounting |
| resize pending | backend grew but filesystem did not | phase-specific conditions |

## Atlas capstone increment

The scheduler, capacity catalogue, expansion controller, and attributes-class policy explain every placement or mutation decision and preserve unresolved states.

## Evidence boundary

The module’s Python and filesystem tests can falsify logical invariants and local durability mechanisms. Cluster controller behavior, CSI RPC behavior, snapshot semantics, cloud durability, and operated recovery require the corresponding native evidence lane. Record unavailable evidence as `not-executed`.

## Transition

Module 5 adds workload identity, ordered lifecycle, quorum, and fencing on top of the storage placement model.

## Advanced design review — capacity must be schedulable

Storage capacity is only useful when it is accessible in the same topology as a feasible workload and within the same operational constraints. Aggregate dashboards hide zone imbalance, per-Node attachment limits, class quotas, maximum volume sizes, snapshot delta pools, and recovery headroom. Capacity planning should therefore model placement transactions rather than one number.

For a workload with multiple claims, calculate a feasible tuple: Node, zone, class, capacities, attachment slots, access modes, and application placement constraints. If no tuple exists, do not create partial external effects merely because one claim could succeed. A higher-level admission control can preflight this tuple and reserve scarce resources, but it still needs reconciliation for races and backend failure.

## QoS without accidental data-policy drift

Performance tiers are data-plane releases. A change in IOPS, filesystem, mount options, topology, or backend type can change acknowledgement latency, snapshot compatibility, cost, and failure behavior. Keep durability, reclaim, encryption, and restore gates categorical. An optimization is accepted only after those gates pass and the workload evidence demonstrates an application benefit.

## Scheduling and storage are one admission problem

Kubernetes often exposes scheduling and provisioning as cooperating controllers, but a platform product should present one understandable admission decision. A developer should learn before a rollout whether the requested replicas, claims, zones, attachment counts, and capacity can coexist. This does not eliminate races, but it moves predictable failure earlier and makes quotas and cost visible.

A useful preflight result is not simply `allowed: false`. It lists every candidate topology and the failed predicates: insufficient class capacity in zone A, attachment limit on node pool B, no node matching the workload architecture in zone C, or a volume mode unsupported by the driver. This evidence also helps capacity planning because repeated rejections reveal which dimension—not global free bytes—is constraining growth.

## Expansion is a release with no shrink button

Storage expansion is commonly described as safe because Kubernetes rejects shrink. That same fact makes poor expansion decisions expensive and difficult to reverse. A larger volume can change billing, snapshot size, backup duration, restore time, and migration requirements. Some backends change performance with size; others require a separate QoS profile. The platform should require a growth forecast and verify recovery capacity before expansion.

If the filesystem phase fails, do not treat a newly larger backend as rollbackable. The correct recovery is to complete the supported node/filesystem transition or migrate to another volume. For destructive test cases, use a disposable claim and preserve the exact phase evidence so the runbook distinguishes backend, device, filesystem, and application capacity.
## Storage-aware scheduling is a joint constraint problem

A Pod with persistent storage is schedulable only when compute and storage constraints intersect. CPU and memory may fit on several Nodes, while the existing PV is accessible from one zone, the driver’s attach limit is exhausted on another, and policy forbids the remaining Node. Reporting only “0/3 nodes are available” hides the reasoning needed to repair the design.

A useful scheduler explanation preserves every rejected predicate per Node:

```text
node-a: insufficient memory
node-b: volume node affinity conflicts
node-c: CSI attach limit exhausted
```

This matters because the remedies differ. Increasing a claim does not fix memory. Moving a Pod does not fix a backend capacity shortage. Adding a Node in the wrong zone does not create a target for an already bound zonal volume.

### Topology is part of the data contract

Topology keys describe where a volume can be provisioned or accessed. They may represent regions, zones, racks, storage pools, or vendor-specific domains. Treat them as a versioned interface. If a driver changes key names or values during upgrade, existing PV node affinity and new provisioning decisions can diverge.

For each storage class, document:

- provisioning topologies;
- attachment topologies;
- replication boundary;
- failure domains the backend survives;
- zones where restore is supported;
- whether failover changes the volume identity;
- whether application replicas must be spread independently of storage replicas.

A volume replicated across devices in one zone does not provide zone resilience. A multi-zone data service may still require clients or quorum members in specific locations.

### Capacity is more than requested GiB

Storage capacity has at least four dimensions:

1. **Space** — allocatable bytes and inode or object limits.
2. **Attachment slots** — the number of volumes a Node or controller can attach.
3. **Performance** — IOPS, throughput, latency, queue depth, and burst credits.
4. **Operational headroom** — space and throughput needed for compaction, rebuild, snapshot, expansion, and recovery.

A claim can bind successfully while the workload remains operationally unsafe. A database at 92% capacity may have enough room for current rows but not for index rebuilds or write-ahead log bursts. A Node can have free disk space while its attach-slot limit prevents another volume. A backend can provide nominal capacity while throttling every tenant during a noisy-neighbor event.

### Mutable attach limits and stale scheduler knowledge

Modern CSI integrations can update reported node attach limits. This improves scheduling after capacity changes or `ResourceExhausted` responses, but the information still has propagation delay. The scheduler’s view, kubelet’s view, and backend’s actual limit can temporarily differ. The runbook should distinguish a stale advertised count from a real backend exhaustion and should avoid endless `ContainerCreating` loops.

The platform should alert on both persistent attach failures and significant drift between advertised and observed capacity. Increasing limits without validating kernel, device, or backend constraints can move the failure later into the lifecycle.

### Expansion is a capacity and availability event

Online expansion appears simple—raise a PVC request—but can increase backend allocation, trigger node operations, extend a filesystem, and alter performance or billing. Some filesystems expand online; others require remount or restart. Some backends allow growth but not shrink. A failed filesystem expansion can leave the API capacity larger than the usable filesystem.

Plan expansion as a change:

- verify backup or snapshot policy;
- confirm backend and driver capabilities;
- reserve capacity in the correct topology;
- set an application threshold before emergency exhaustion;
- observe controller and node phases;
- verify filesystem and application views;
- update capacity forecasts;
- record cost and quota impact.

Shrinking normally requires migration to a new volume. Editing capacity downward is not a safe reclaim mechanism.

### VolumeAttributesClass and mutable service levels

A stable VolumeAttributesClass API can represent mutable storage attributes such as service level, when the CSI driver supports modification. This does not make every QoS change instantaneous, reversible, or safe. A provider may perform a backend migration, throttle during transition, or reject a downgrade while snapshots exist.

Treat a class change as a release candidate with:

- old and new performance envelopes;
- driver capability evidence;
- expected transition time;
- application impact;
- rollback semantics;
- cost change;
- verification after completion.

A desired attribute in the API is not proof that the backend applied it.

### Storage QoS and noisy neighbours

Kubernetes requests and limits do not generally provide a universal portable storage-IO reservation model. StorageClass parameters, backend pools, filesystem behavior, and provider controls determine isolation. The platform should measure workload-visible latency and throughput rather than infer QoS from a name such as `premium`.

For Atlas, performance profiles include:

- request size distribution;
- read/write ratio;
- sync-write frequency;
- target p50 and p99 latency;
- sustained and burst throughput;
- concurrency;
- recovery and rebuild load;
- maximum acceptable queue time.

The same storage can behave very differently under random 4 KiB writes and sequential 8 MiB artifact reads. A class should describe the workload for which its evidence is valid.

### Scheduling review before release

A storage-aware release review should prove:

1. every PVC can be provisioned in at least one feasible topology;
2. every existing PV has at least one replacement Node candidate;
3. attach limits allow rollout surge and failure recovery;
4. topology spread does not conflict with volume affinity;
5. capacity includes recovery and maintenance headroom;
6. expansion has an observed completion oracle;
7. performance evidence matches the workload shape;
8. the design remains recoverable after one planned Node or zone outage at the claimed tier.

This review connects scheduler success to service resilience rather than treating initial placement as the final result.
