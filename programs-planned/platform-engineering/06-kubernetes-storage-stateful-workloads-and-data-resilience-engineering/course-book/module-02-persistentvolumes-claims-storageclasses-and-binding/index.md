# Module 02 — PersistentVolumes, Claims, StorageClasses, and Binding

> **Governing question:** How does a storage request become one specific volume without creating an unschedulable or destructively managed workload?

## Why this module exists

A new Atlas database Pod remains Pending. The PVC is also Pending. The storage backend has free capacity, and the scheduler reports no suitable Node. An operator creates a volume manually in zone A; the Pod requires zone B. The intervention converts a recoverable scheduling problem into a hard topology conflict.

This module does not begin with YAML. It begins by locating authority and the earliest missing transition. Kubernetes storage is a set of cooperating control loops around an external data system; the application still owns the meaning and correctness of the data.

## Learning outcomes

- explain PV and PVC identity, phases, binding, and protection finalizers
- design StorageClasses as platform service contracts rather than vendor parameter dumps
- evaluate static and dynamic provisioning
- reason about Immediate and WaitForFirstConsumer binding
- apply reclaim policy and claim-retention rules deliberately
- diagnose a Pending claim from events, class, capacity, selectors, topology, and provisioner state

## PV and PVC are a two-sided contract

A PVC is a namespaced request: capacity, access modes, volume mode, storage class, selector, data source, and optional mutable attributes. A PV is cluster-scoped supply: capacity, access modes, volume mode, class, reclaim policy, source handle, and topology. Binding creates a one-to-one relationship. The claim does not become the volume, and the volume does not inherit namespace ownership.

The binder must match more than size. A filesystem claim cannot safely bind a raw-block PV. A claim requesting a class must not bind an unrelated class. Access modes must be compatible. A selector can intentionally restrict supply but also prevent dynamic provisioning. Prebinding through `volumeName` or `claimRef` is a strong override and must be treated as an ownership decision.
## StorageClass is a product interface

A StorageClass should describe a supported service tier: provisioner, binding mode, reclaim policy, expansion capability, allowed topologies, mount options, and driver-specific parameters. The class name becomes a platform API. Renaming or changing semantics underneath it can alter durability, cost, encryption, topology, and performance for every new claim.

A class named `fast` is weak because its meaning cannot be reviewed. Atlas uses names such as `atlas-rwo-durable` and records what “durable” means in the current environment. The class does not promise a universal IOPS number unless the implementation and evidence support it.
## Immediate binding can pre-decide topology

With `Immediate`, provisioning can occur when the PVC is created, before a Pod is considered. That can be suitable for topology-independent storage. It is dangerous for zonal volumes because the chosen zone may conflict with Pod affinity, resource availability, or other bound volumes. `WaitForFirstConsumer` delays binding or provisioning until the scheduler has a candidate Node and can pass an allowed topology to the provisioner.

Delayed binding does not guarantee success. Capacity data can be stale; a multi-volume Pod can consume capacity for one claim and fail another; attach limits may change; provider APIs may reject provisioning. The correct response is to examine each transition rather than repeatedly deleting the claim.
## Default classes and omission are policy

A PVC with no `storageClassName` can be defaulted by admission. A PVC with `storageClassName: ""` explicitly requests no class and behaves differently. Multiple default classes are tolerated to support migration, but the most recently created default can affect new claims. That is a platform release concern, not a harmless annotation change.

Course 6 requires every production-intent claim to name a class. Omission is permitted only in exercises that study defaulting. This keeps the workload contract independent of cluster-wide default changes.
## Reclaim and retention are different layers

The PV reclaim policy controls what happens to the backing volume after its claim is released: retain or delete in normal CSI practice. StatefulSet PVC retention policy controls whether claims created from templates are retained or deleted when the StatefulSet is deleted or scaled down. Snapshot classes have their own deletion policy. Object stores and backups have independent lifecycle rules.

A safe production deletion path evaluates all layers. Retaining a PV while deleting the snapshot encryption key is not recoverability. Deleting a PVC while retaining the backend volume may preserve bytes but lose the metadata needed to identify and restore them. Atlas records logical identity, physical handle, data class, checksum, encryption context, and recovery owner before any destructive transition.
## Diagnosing Pending and Released states

A Pending PVC is an outcome, not a diagnosis. Inspect StorageClass existence, provisioner identity, binding mode, events, selectors, requested size, access modes, volume mode, topology, capacity objects, and controller logs. For delayed binding, inspect the Pod’s scheduling constraints and selected-node annotation. For bound claims whose Pods remain Pending, inspect PV node affinity, attach limits, multi-attach conflicts, and Node availability.

A Released PV still carries old data and a former claim reference. Reusing it safely may require backend sanitation, claimRef removal, and a documented adoption procedure. Automated rebinding of arbitrary released volumes is a data-leak risk.

## Binding protection and object deletion

Kubernetes uses protection finalizers to delay deletion of PVs and PVCs that are still in use or participating in protected relationships. These finalizers reduce accidental data loss, but they do not make deletion safe in every failure. An operator who removes finalizers without understanding the active references can bypass the protection and create orphaned or concurrently used storage.

The correct diagnostic starts from the finalizer’s reason: which Pod, claim, snapshot, or controller still references the object? If the referenced object is stale, repair or reconcile that state. Finalizer removal is a last-resort migration action with backend verification and an audit record, not a routine way to unblock a pipeline.


## Static provisioning and adoption

Static PVs are appropriate when storage already exists, when an administrator must control exact backend identity, or when migration adopts an existing volume. The PV must accurately describe capacity, access modes, volume mode, class, node affinity, reclaim policy, and source handle. A prebound claim should verify that the intended logical data matches the physical volume.

Adopting an old volume without an identity manifest can expose another tenant’s data or attach an incompatible filesystem. Atlas adoption requires a checksum or database identity, former claim record, encryption context, and explicit release from the previous owner.


## Class evolution without surprise

Changing a StorageClass object does not normally mutate existing PVs; it changes how future provisioning requests are handled. This can produce hidden heterogeneity: two claims with the same class name may have been created under different parameter versions. The platform should version class semantics or record a provisioned profile on each volume.

Atlas treats class definitions as released platform APIs. A new backend, encryption default, topology, or reclaim policy is introduced as a new class or a controlled migration, not an invisible edit to the meaning of an existing name.


## Binding state as incident evidence

Preserve the PVC events, selected-node annotation, PV node affinity, class version, provisioner logs, and backend request identifier during incidents. Recreating the PVC can erase the evidence needed to distinguish scheduler, provisioner, quota, and backend failure.

The dependency-light binder produces a transition ledger for this reason. In a real cluster, collect object YAML and events before attempting repair. This discipline shortens diagnosis and prevents a “delete and retry” habit that may leak or duplicate data.

## Worked semantic example

```python
from atlas_data.binding import Binder
from atlas_data.models import Claim, StorageClass

claim = Claim(
    namespace="atlas-system", name="db-atlas-db-0",
    requested_gib=20, access_modes=("ReadWriteOncePod",),
    storage_class="atlas-rwo-durable",
)
result = Binder(classes=[StorageClass.atlas_default()]).bind(
    claim, selected_zone="zone-a"
)
assert result.volume.zone == "zone-a"
```

The example is intentionally small enough to inspect. It establishes one invariant in the dependency-light lane; it does not claim native Kubernetes or storage-system conformance.

## Production-intent API fragment

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: atlas-rwo-durable
provisioner: csi.atlas.example.invalid
reclaimPolicy: Retain
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

The manifest is a contract candidate. Its effect depends on admission, installed controllers, CSI capabilities, backend behavior, and application compatibility.

## Failure signatures

| Observation | Likely missing guarantee | Decisive evidence |
|---|---|---|
| PVC Pending | no matching supply or provisioning transition | events, class, selector, capacity, topology |
| PV Released | old data remains with former claim identity | controlled reclamation |
| wrong zone | bound volume and Pod constraints conflict | delayed binding and topology evidence |

## Atlas capstone increment

A deterministic binder creates topology-compatible PVs, preserves one-to-one claim identity, and refuses unsafe rebinding or destructive reclaim.

## Evidence boundary

The module’s Python and filesystem tests can falsify logical invariants and local durability mechanisms. Cluster controller behavior, CSI RPC behavior, snapshot semantics, cloud durability, and operated recovery require the corresponding native evidence lane. Record unavailable evidence as `not-executed`.

## Transition

Module 3 follows the bound volume into CSI controller and node operations.

## Advanced design review — binding is an allocation transaction

Binding is often taught as a status change, but it is a cross-system allocation transaction. Kubernetes records demand and identity; a CSI component creates or discovers an external object; topology and scheduler decisions constrain where it is usable; reclaim policy determines what happens after logical release. There is no universal atomic transaction across these systems, so reconciliation and stable identity are essential.

An allocation can be in at least five meaningful states: no request, request without feasible topology, backend effect without PV, PV without usable attachment, and bound claim with valid application data. Operators should be able to inventory each state and know whether retry, adoption, retention, or cleanup is safe. Deleting and recreating the PVC erases evidence and can produce a second physical effect.

## A strong StorageClass review

Review the class as if it were a public platform API. Confirm its name does not overclaim durability or performance; document every mutable and immutable parameter; test delayed binding; define reclaim and expansion behavior; publish allowed topologies and capacity; declare supported filesystems and modes; identify the provisioner and sidecar versions; and state native evidence status. If consumers must understand provider parameter names to use it safely, the platform abstraction is incomplete.

## Worked boundary example — imported data versus newly provisioned data

Consider two claims with identical size and access mode. The first requests a new empty volume for a disposable integration environment. The second must adopt a retained production volume after a cluster rebuild. Their YAML can look similar, but their safety models are opposite.

For the disposable claim, dynamic provisioning with `Delete` may be correct. The stable request name prevents duplicate effects, and cleanup can remove the backend after the environment expires. For the retained volume, automatic provisioning is dangerous: a newly created empty volume can satisfy the claim while silently abandoning the real data. The recovery workflow must identify the exact backend handle, use `Retain`, verify topology and encryption, bind intentionally, and prevent formatting or initialization.

This example demonstrates why a PVC is a request rather than a complete data identity. Platform APIs should distinguish `new`, `clone`, `restore`, and `adopt` operations. Each has different authority, replay, cleanup, and evidence. Treating them as one generic claim invites destructive defaulting.

## Review the binder under failure

A robust binder must survive its own restart and concurrent reconciliation. It should never bind two claims to one PV or create two PVs for one backend handle. It should preserve claim and volume protection, reject incompatible modes, and record the chosen topology. If a backend effect exists without a PV, the repair path should adopt it through stable request identity rather than allocate again. If a claim disappears mid-operation, cleanup waits until the backend effect is classified as disposable or retained.

The course’s deterministic binder is intentionally small, which makes these invariants visible. Native Kubernetes and CSI controllers are more complex but face the same ambiguity. Use the model to formulate tests, not to claim conformance.
## Binding as a distributed agreement

A PVC–PV binding is not a filesystem mount. It is an agreement among several control-plane actors about identity, capacity, access mode, class, volume mode, and—when topology matters—placement. The claim expresses workload demand. The volume object represents a provisioned resource. A StorageClass describes an administrative provisioning policy. The binder and external provisioner coordinate these objects. The scheduler may participate when `WaitForFirstConsumer` delays provisioning until Pod placement is known.

Treat the binding as a state machine:

```text
PVC Pending
  ├─ no matching class or capacity → remains Pending
  ├─ immediate provisioning → backend allocation → PV creation → Bound
  └─ WaitForFirstConsumer → selected consumer topology
                           → backend allocation in compatible zone
                           → PV creation → Bound
```

The first useful diagnostic question is therefore not “why did the mount fail?” It is “which transition has not happened?” A Pending claim, a Bound claim with an unschedulable Pod, and a scheduled Pod with a failed mount belong to different owners and require different evidence.

### Bidirectional identity prevents accidental rebinding

A correct binding is represented on both sides: the PVC names the volume and the PV’s claim reference names the claim. That identity must survive controller retries. Static prebinding is especially dangerous when operators copy manifests between environments or reuse a volume name after deletion. A claim that requests an existing PV must still match class, mode, capacity, and access requirements; prebinding is not permission to violate the storage contract.

The Atlas semantic binder rejects several tempting shortcuts:

- binding a filesystem claim to a raw-block PV;
- shrinking the requested capacity to fit an existing volume;
- reusing a PV already claimed by another UID;
- binding a topology-constrained volume before the consumer’s zone is known;
- changing the meaning of a StorageClass while old claims still rely on the original contract.

### StorageClass is a platform API, not a vendor flag bag

A StorageClass name becomes part of a workload’s platform contract. Developers should be able to reason about `atlas-transactional` or `atlas-artifact-standard` without knowing provider-specific parameters. The class should document:

- intended data class and workload pattern;
- provisioning and binding mode;
- reclaim policy;
- expansion support;
- filesystem or block mode assumptions;
- topology and replication boundary;
- snapshot and clone support;
- performance envelope and variability;
- encryption and key ownership;
- backup integration;
- unsupported uses.

Changing any of these semantics under the same class name can be a breaking platform change even if the YAML remains valid. Create a new class or use a governed mutation mechanism when the contract changes materially.

### `WaitForFirstConsumer` solves one race, not every topology problem

Immediate binding can allocate a zonal volume before the scheduler chooses a Node, leaving the Pod and volume in incompatible zones. `WaitForFirstConsumer` lets scheduling constraints influence provisioning. It does not guarantee that sufficient storage capacity exists, that the chosen Node can attach another volume, or that later rescheduling will be possible.

A robust topology decision combines:

- Pod CPU, memory, affinity, taints, and topology constraints;
- StorageClass allowed topologies;
- CSI capacity information when available;
- node-specific attach limits;
- existing volume node affinity;
- failure-domain and availability policy.

The scheduler can satisfy today’s placement while creating tomorrow’s maintenance trap. For example, binding a singleton database to the only Node in a zone may make the initial Pod schedulable but leave no safe replacement target. Course 6 therefore reviews recovery topology before approving the claim.

### Reclaim policy and deletion protection

`Delete` makes the backend volume lifecycle follow the claim. `Retain` preserves the PV and backend resource for explicit recovery or reuse. Neither policy is universally correct. Disposable development environments benefit from automatic cleanup. Transactional production data usually needs a deliberate retirement workflow.

Protection finalizers reduce races while a claim or volume is in use, but they do not replace governance. A privileged operator can remove finalizers or delete the backend directly. A GitOps controller can prune a claim that was mistakenly removed from desired state. Release policy must therefore combine API-level protection, authorization, backup evidence, and recovery runbooks.

### Expansion has multiple completion points

Increasing a PVC request can trigger controller-side volume growth, node-side device recognition, and filesystem expansion. These phases may complete at different times. The PVC capacity, PV capacity, backend capacity, block-device size, and filesystem size can temporarily disagree. Readiness should remain truthful: a database that requires the larger capacity should not report the expansion complete merely because the API request was accepted.

The runbook records each boundary:

```text
requested capacity
→ controller expansion
→ backend capacity
→ node expansion
→ filesystem capacity
→ application validation
```

A failed expansion must not be “repaired” by editing status fields. Restore the missing transition or create a controlled migration.

### Binding review checklist

Before a workload release, verify:

1. The claim’s class name refers to a documented, versioned contract.
2. Volume mode and access modes match application behavior.
3. Binding mode matches topology requirements.
4. Reclaim policy matches deletion and recovery policy.
5. Expansion behavior is supported by the driver and application.
6. Snapshot, clone, and restore capabilities are verified rather than assumed.
7. The chosen capacity leaves operational headroom.
8. The claim cannot silently consume the wrong default class.
9. Static or imported volumes use immutable backend identity and claim UID checks.
10. A Bound state is followed by attach, mount, filesystem, and application-readiness evidence.

This checklist turns the PV subsystem from “storage YAML” into a governed resource-allocation API.
