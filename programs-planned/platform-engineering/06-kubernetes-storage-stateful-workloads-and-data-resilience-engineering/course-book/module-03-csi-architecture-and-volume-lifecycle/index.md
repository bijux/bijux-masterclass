# Module 03 — CSI Architecture and Volume Lifecycle

> **Governing question:** Which component owns each provision, attach, stage, publish, unpublish, expand, snapshot, and deletion transition?

## Why this module exists

The PVC is Bound and the Pod is assigned to a Node, but the container never starts. Kubernetes reports a mount timeout. The storage console shows the disk attached. An engineer retries attachment manually and creates a second backend operation. The missing transition was NodeStage, not ControllerPublish.

This module does not begin with YAML. It begins by locating authority and the earliest missing transition. Kubernetes storage is a set of cooperating control loops around an external data system; the application still owns the meaning and correctness of the data.

## Learning outcomes

- separate Kubernetes sidecars, CSI controller service, and CSI node service
- trace CreateVolume through ControllerPublish, NodeStage, and NodePublish
- design idempotent RPC behavior and stable volume identity
- distinguish attachment, device preparation, filesystem mount, and container publication
- diagnose partial failure and stale VolumeAttachment state
- evaluate driver capabilities before relying on an API feature

## CSI is an interface boundary, not one daemon

Kubernetes storage support is distributed across built-in controllers, external sidecars, a CSI controller plugin, node plugins, kubelet, and the backend. The external provisioner observes PVCs and calls `CreateVolume`. The attach/detach controller and external attacher coordinate `VolumeAttachment` objects and controller publish operations. Kubelet interacts with the node plugin to stage and publish. Snapshot and resize controllers add further loops.

A diagnosis that says “CSI is broken” is as imprecise as saying “the network is broken.” Identify the object, controller, RPC, backend state, Node path, and expected next transition.
## Identity and idempotency are the center of CSI

Controller operations may be retried after timeouts when the caller does not know whether the backend completed the request. A correct plugin must make requests idempotent according to the CSI contract. `CreateVolume` repeated with the same name and compatible parameters should return the same logical volume. Reusing the name with incompatible capacity or capabilities must fail rather than silently returning a different object.

Stable `volume_id` values connect Kubernetes objects to backend state. Losing that mapping can create orphaned volumes, duplicate provisioning, or deletion of the wrong data. Atlas stores request fingerprints and backend handles in its semantic driver so retry behavior is observable.
## Attach is not mount

ControllerPublish typically attaches a volume to a Node or grants Node access. NodeStage prepares the device or filesystem at a node-global staging path. NodePublish exposes the prepared volume at a target path for a specific Pod. Some drivers skip staging; some storage is network-mounted and does not require controller attachment. Capability discovery determines which calls are valid.

The phases fail differently. An attach failure points to backend attachment, credentials, topology, or limits. A stage failure can indicate device discovery, filesystem checks, encryption, or mount options. A publish failure can indicate target paths, bind mounts, permissions, or access-mode conflicts. The course records these phases separately.
## The reverse lifecycle matters

Pod termination should trigger NodeUnpublish, then NodeUnstage when no consumers remain, then ControllerUnpublish when attachment is no longer needed. Volume deletion must not race an active attachment or snapshot. Node loss complicates the sequence because kubelet may never complete unpublish. The control plane and storage system need a force-detach or timeout policy, but force can expose a live volume to a second Node while the first writer still exists.

Safe recovery therefore links detach policy to fencing. Storage detach is necessary for many backends; application-level writer revocation is still required before a replacement becomes authoritative.
## Capability discovery prevents fantasy manifests

CSI plugins report controller, node, and volume capabilities. Kubernetes sidecars also have version and feature requirements. A StorageClass with `allowVolumeExpansion: true` does not make expansion work if the driver lacks controller or node expansion. A VolumeSnapshot object cannot create a backend snapshot if the driver lacks snapshot support. `ReadWriteOncePod`, raw block, multi-node access, volume condition reporting, and modify-volume behavior all depend on implementation support.

Atlas maintains a capability matrix as release evidence. Unsupported features are rejected before workload rollout rather than discovered during an incident.
## Partial failure and reconciliation

A timeout after backend success can leave the API object behind the physical state. A driver restart can lose transient work while durable backend operations continue. A Node can disappear with mounts still active. Controllers reconcile by reading current state, retrying idempotently, and updating API objects. Operators reconcile by comparing three planes: Kubernetes objects, CSI plugin state, and backend state.

Manual backend changes should be treated as migrations with evidence. Deleting a VolumeAttachment object to make an alert disappear can cause a new attach while the old Node still writes. The correct intervention starts from the authoritative state and preserves the ability to prove exclusivity.

## Sidecars are controllers with independent releases

External provisioner, attacher, resizer, snapshotter, health monitor, and registrar components are separate binaries with compatibility requirements. Upgrading the CSI driver while leaving sidecars unchanged can produce unsupported RPC assumptions or missing API features. Conversely, a new sidecar cannot create a capability the driver lacks.

A driver release dossier should list CSI spec support, sidecar versions, Kubernetes compatibility, feature gates, CRDs, required RBAC, sockets, leader election, and upgrade order. Atlas records these as evidence rather than assuming that a DaemonSet image tag fully identifies the storage stack.


## Controller and node security boundaries

The controller plugin often holds credentials to create, delete, attach, and snapshot storage. Node plugins run with privileged host access, mount propagation, device paths, and a Unix socket used by kubelet. Compromise can affect data far beyond one Pod. Namespaces and ordinary Pod security settings do not contain the host-level authority of a CSI node plugin.

Course 8 will harden the platform, but Course 6 already records the required privileges and narrows network access. Driver credentials, socket paths, host mounts, and service accounts are part of the data-plane threat model.


## Filesystem creation is a policy decision

When Kubernetes or a CSI plugin formats a new volume, filesystem type and mount options influence durability, performance, permissions, and recoverability. Invalid mount options can make a volume unusable; unsafe options can weaken write ordering or integrity. Raw block volumes move even more responsibility to the application.

The platform should expose only reviewed combinations. Atlas manifests treat filesystem and volume mode as part of the storage class contract, and the native lane records the actual mount rather than assuming the requested option took effect.


## Observing reconciliation without causing it

Operators need a read-only sequence before intervention: inspect PVC, PV, StorageClass, Pod scheduling, VolumeAttachment, CSINode, driver Pods, kubelet events, node-plugin logs, and backend state. Each object narrows the missing transition. Manually attaching a volume or deleting controller objects changes the evidence and can create a second writer.

A safe runbook collects state first, identifies the owner, and performs the smallest reversible repair. Atlas runbooks encode this order.

## Worked semantic example

```python
from atlas_data.csi import SemanticCSI

driver = SemanticCSI(driver_name="csi.atlas.example.invalid")
volume = driver.create_volume("pvc-123", 20, zone="zone-a")
driver.controller_publish(volume.id, node_id="node-a")
driver.node_stage(volume.id, node_id="node-a")
driver.node_publish(volume.id, node_id="node-a", target="pod/db")
assert driver.volume(volume.id).published_targets == {"pod/db"}
```

The example is intentionally small enough to inspect. It establishes one invariant in the dependency-light lane; it does not claim native Kubernetes or storage-system conformance.

## Production-intent API fragment

```yaml
apiVersion: storage.k8s.io/v1
kind: CSIDriver
metadata:
  name: csi.atlas.example.invalid
spec:
  attachRequired: true
  podInfoOnMount: true
  storageCapacity: true
  volumeLifecycleModes: [Persistent]
```

The manifest is a contract candidate. Its effect depends on admission, installed controllers, CSI capabilities, backend behavior, and application compatibility.

## Failure signatures

| Observation | Likely missing guarantee | Decisive evidence |
|---|---|---|
| attach timeout | controller/backend state diverges | VolumeAttachment plus backend handle |
| stage failure | device or filesystem preparation failed | node plugin and kubelet evidence |
| stale detach | second writer risk | fencing before replacement |

## Atlas capstone increment

A semantic CSI plugin records idempotent requests, controller attachments, node staging, Pod publication, capability checks, and safe reverse transitions.

## Evidence boundary

The module’s Python and filesystem tests can falsify logical invariants and local durability mechanisms. Cluster controller behavior, CSI RPC behavior, snapshot semantics, cloud durability, and operated recovery require the corresponding native evidence lane. Record unavailable evidence as `not-executed`.

## Transition

Module 4 connects CSI operations to scheduling topology, capacity, expansion, and service-level mutation.

## Advanced design review — CSI is a distributed state machine

CSI calls cross process, Node, network, and storage-system boundaries. Timeouts therefore create ambiguous outcomes: the caller may not know whether an effect occurred. Idempotency is not an optional optimization; it is the mechanism that turns an ambiguous timeout into a recoverable state. Every create, attach, stage, publish, expand, snapshot, and delete operation needs stable identity and compatible replay semantics.

The node half of CSI also crosses privilege boundaries. A node plugin can manipulate devices, mounts, and host paths. Its failure can affect every workload on the Node, and its compromise can exceed the authority of ordinary Pods. Treat node-plugin rollout, security context, host access, and observability as platform-critical changes.

## Diagnose by phase, not by product name

When a volume is unusable, classify the earliest failed phase: schedule/bind, provision, attach, stage, publish, runtime mount, filesystem recovery, or application readiness. Each phase has a different owner and evidence source. This prevents broad interventions such as restarting every CSI Pod, deleting claims, or force-detaching volumes before the writer state is known.

## Sidecars are protocol participants, not invisible plumbing

The external provisioner, attacher, resizer, snapshotter, registrar, and health monitor are separate controllers or helpers with their own versions, leader election, queues, retry behavior, and permissions. A CSI driver profile therefore includes the sidecar matrix, not only the driver container tag. An API feature can be unavailable because the driver implements it but the installed sidecar or CRD does not, or because a sidecar supports a newer behavior than the backend safely handles.

Upgrades should test mixed versions and in-flight operations. Replacing the provisioner while requests are pending must not allocate twice. Updating node plugins must preserve staged and published mounts. Changing registrar or socket paths can make a healthy binary undiscoverable. Controller and node rollout strategies have different blast radii: a bad controller can stall new operations cluster-wide, while a bad node plugin can disrupt every volume on selected Nodes.

## Status is a projection of several truths

Kubernetes status usually reflects the controller’s latest observation. The backend may be ahead after a timeout, or the object may be ahead after an external rollback. A VolumeAttachment marked attached can coexist briefly with a backend detachment; a PVC can retain expanded capacity while a filesystem remains smaller. Reconciliation should compare stable identities and current generations, not assume one status is perfect truth.

For incident analysis, preserve timestamps and operation IDs across API events, sidecar logs, driver logs, node logs, and backend audit records. The objective is to reconstruct one lifecycle. Restarting components before collecting that evidence often destroys the only explanation for an ambiguous outcome.
## CSI operations under ambiguous failure

The most important CSI design fact is that a timeout does not mean “nothing happened.” The caller may lose the response after the storage provider created a volume, attached it, or expanded it. Retrying with a new identity can duplicate resources or split authority; refusing to retry can strand a successful backend operation. CSI therefore relies on stable request identities and idempotent semantics.

For every mutating operation, record:

- the stable request or resource identity;
- the compatible parameters for replay;
- the externally observable effect;
- the state that survives a controller or node-plugin restart;
- the response when the same identity is replayed with different parameters;
- the reconciliation path when Kubernetes and backend state disagree.

Atlas’s semantic driver returns the same volume for a compatible `CreateVolume` replay and rejects a replay that changes capacity or topology. That is the minimum behavior required to recover from an ambiguous timeout without inventing a second resource.

### Controller-side and node-side authority differ

Controller operations usually manage backend lifecycle: create, delete, attach, detach, snapshot, and expand. Node operations prepare and expose storage on a particular machine: stage, publish, unpublish, unstage, and sometimes expand the mounted filesystem. A failure can therefore be localized by phase.

| Phase | Typical authority | Evidence |
|---|---|---|
| provision | external provisioner + controller plugin | PVC, PV, sidecar logs, backend resource |
| attach | external attacher + controller plugin | VolumeAttachment, controller logs, backend attachment |
| stage | kubelet + node plugin | kubelet events, node-plugin logs, device/mount state |
| publish | kubelet + node plugin | target path, bind mount, Pod events |
| application open | workload | permissions, filesystem, application logs and readiness |

Restarting the controller plugin cannot fix a filesystem permission error inside the Pod. Deleting a Pod cannot correct a leaked backend volume allocation. Phase ownership narrows intervention.

### Node loss and force detach

A Node may disappear before kubelet unpublishes or unstages a volume. The control plane eventually needs to decide whether a replacement can attach it elsewhere. Force-detach mechanisms are operationally necessary, but they are not proof that the previous writer stopped. Network partitions, hypervisor pauses, and delayed Node recovery can leave the old process alive.

The safe sequence for single-writer data is:

1. revoke or fence the old writer generation;
2. determine whether the old Node can still reach storage;
3. detach or invalidate the old attachment;
4. attach and stage on the replacement Node;
5. verify application-level recovery before admitting traffic.

Skipping step 1 creates a split-brain window. Storage attachment policy reduces risk; the application or data service must still reject stale generations.

### Capability matrices belong to releases

CSI is an interface, not a guarantee that every driver implements every optional behavior. A release dossier should record actual support for:

- controller publish/unpublish;
- node stage/unstage;
- expansion and whether node expansion is required;
- snapshots and clones;
- raw block;
- `ReadWriteOncePod` or multi-node modes;
- topology and capacity reporting;
- volume health;
- mutable volume attributes;
- group snapshots;
- ephemeral volumes;
- maximum attach counts and dynamic updates.

The matrix also records sidecar versions and API dependencies. The external provisioner, attacher, resizer, snapshotter, registrar, and health monitor are separate controllers with independent release behavior. “Driver version 3.2” is not enough to reproduce the stack.

### Upgrade order and mixed-version evidence

A storage-stack upgrade can affect control-plane sidecars, node plugins, CRDs, conversion webhooks, and backend firmware. The platform should define a supported mixed-version window and test in-flight operations. Questions include:

- Can an old node plugin serve a volume created by the new controller?
- Can a new snapshotter read existing snapshot objects and contents?
- Are CRDs upgraded before controllers that write new fields?
- What happens to a pending expansion during rollout?
- Can node-plugin replacement preserve staged and published volumes?
- Is rollback possible after the backend representation changes?

The upgrade is not complete when all Pods become Ready. It is complete when provisioning, attachment, expansion, snapshot, restore, and recovery operations still satisfy their contracts.

### Security review of CSI components

Controller plugins often hold cloud or storage credentials capable of creating, deleting, and snapshotting large amounts of data. Node plugins commonly require privileged host access, mount propagation, device paths, and a kubelet-facing Unix socket. These components are part of the platform’s trusted computing base.

Review:

- service-account and cloud permissions;
- hostPath mounts and socket ownership;
- privileged mode and capabilities;
- network reachability to storage APIs;
- secret rotation;
- image identity and provenance;
- log redaction;
- admission exceptions;
- upgrade and emergency rollback authority.

A namespace boundary alone does not contain a compromised node plugin.

### An evidence-preserving incident procedure

When attachment or mount operations fail, collect before changing:

```text
PVC and PV identity
StorageClass and VolumeAttributesClass
Pod scheduling decision
VolumeAttachment
CSINode and CSIDriver capabilities
sidecar and controller-plugin logs
kubelet and node-plugin logs
host device and mount state
backend resource and audit record
application generation and fencing state
```

Then identify the earliest inconsistent transition. Destructive actions such as deleting a VolumeAttachment, removing a finalizer, or force-detaching are last-resort migrations with explicit approval and a rollback limit. The goal is not merely to make the Pod start; it is to preserve one authoritative data history.
