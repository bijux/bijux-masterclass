# Module 01 — Data Lifetimes, Durability, and Storage Responsibility

> **Governing question:** What must survive, who owns it, and which failure domain is allowed to destroy it?

## Why this module exists

An Atlas worker is rescheduled after a Node failure. The replacement Pod is healthy, but the queued job disappears and the result directory contains only half of an artifact. Every Kubernetes object looks normal. The failure began before Kubernetes storage APIs were even involved: no one had defined which bytes were disposable and which were authoritative.

This module does not begin with YAML. It begins by locating authority and the earliest missing transition. Kubernetes storage is a set of cooperating control loops around an external data system; the application still owns the meaning and correctness of the data.

## Learning outcomes

- separate container, Pod, Node, volume, zone, and regional lifetimes
- classify transactional state, artifacts, caches, scratch data, and recovery evidence
- distinguish persistence, durability, availability, consistency, and recoverability
- assign one authoritative writer and one deletion authority to each data class
- identify unsafe uses of emptyDir, hostPath, shared filesystems, and local volumes
- write a data-responsibility matrix for Atlas

## The unit of failure is not the Pod

A Pod is a scheduling and lifecycle unit. It is not a durability boundary. Data written into the container writable layer disappears when the container or Pod is replaced. Data in `emptyDir` survives container restart but is tied to the Pod and Node. A local persistent volume can survive Pod replacement yet remain trapped on one Node. A network or cloud volume may survive Node loss but still be lost through reclaim policy, operator deletion, backend failure, or account compromise. Object storage may survive cluster loss while still being corrupted by an application that overwrites the wrong key.

A production design therefore starts with a failure-domain table. For each data class, list the smallest event allowed to destroy it: process exit, Pod deletion, Node replacement, zone loss, cluster deletion, account loss, or deliberate retention expiry. If the design cannot answer that question, choosing a volume type is premature.
## Five meanings hidden behind “persistent”

Persistence means that bytes outlive some lifecycle boundary. Durability is a claim about acknowledged writes surviving specified faults. Availability concerns whether clients can reach a usable copy. Consistency defines which values concurrent clients may observe. Recoverability concerns whether an operator can reconstruct a valid service after damage. These properties are independent.

A single-zone block volume may be persistent across Pod replacement and durable against host failure, while unavailable during a zone outage. A replicated database may remain available yet return stale data under a chosen consistency model. A snapshot may be durable in the same storage account but useless after an account-wide credential compromise. A backup may exist yet fail restoration because the encryption key or schema version is missing. The course uses exact property names instead of the vague label “persistent storage.”
## Data classes need different contracts

Atlas separates transactional run state, immutable artifacts, scratch space, caches, logs, and recovery evidence. Transactional state requires ordered mutation and one application authority. Immutable artifacts need content identity, checksum verification, retention, and efficient read distribution. Scratch space may be disposable but still needs size bounds. Caches must tolerate complete loss and prevent stale authorization leakage. Logs and audit evidence have their own retention and integrity rules.

Putting all classes on one RWX filesystem appears convenient but erases these distinctions. It gives every process a filesystem-shaped interface, encourages hidden coordination through paths, and makes deletion or corruption blast radius difficult to bound. A more mature design selects storage after the data contract is written.
## Authority before access mode

Kubernetes access modes describe how a volume may be mounted by Nodes and Pods; they do not prove safe application concurrency. `ReadWriteOnce` historically means one Node, not one Pod. `ReadWriteOncePod` narrows the Kubernetes attachment/mount contract to one Pod when supported by CSI, but a stale process, storage-system split brain, or application-level lease failure can still violate single-writer assumptions. `ReadWriteMany` describes storage accessibility, not transaction isolation.

For every authoritative data set, define the writer identity, how that identity is elected, how it is revoked, how stale writers are fenced, and how readers know which generation they are observing. Storage access and application authority reinforce each other but are not interchangeable.
## Deletion is a privileged state transition

Reclaim policy, PVC deletion, StatefulSet claim retention, snapshot deletion policy, object lifecycle rules, backup retention, and application cleanup can each destroy data. The platform must name the deletion authority for every layer. A claim owner should not accidentally possess authority to delete a retained backup. A namespace deletion should not silently erase a regulated archive. A dynamically provisioned volume with `Delete` may be correct for disposable environments and unacceptable for a production database.

Deletion design includes evidence: who requested deletion, which logical data was affected, which physical copies remained, whether restore was still possible, and when cryptographic or lifecycle expiry made deletion irreversible.
## Atlas responsibility matrix

Atlas Data Plane 1.0 declares transactional state as database-owned, artifacts as content-addressed and immutable after publication, scratch data as Pod-scoped, and recovery evidence as separately retained. The cluster owns claims and workload placement. The CSI implementation owns provisioning and node preparation. The application owns consistency and write ordering. The backup system owns copy inventory and restoration metadata. The platform team owns storage classes and policy; service owners own schema and recovery procedures.

This matrix prevents a common organizational failure in which the platform team is expected to recover a database it cannot interpret, while the service team assumes the existence of a PVC means backups are handled elsewhere.

## Durability begins at acknowledgement

An application’s durability claim begins when it tells a caller that a mutation succeeded. If the process returns success before data and required metadata reach a durable boundary, a later crash can violate the contract even though a PVC exists. Database settings such as synchronous commit, filesystem semantics, controller caches, and storage-system replication all influence the actual acknowledgement point. The platform cannot infer this from Kubernetes.

For Atlas, the transactional ledger records a commit generation only after the write, file synchronization, and directory synchronization required by the local evidence lane. In a real database, the engine’s commit protocol owns that rule. The platform team must ask which failures are covered: process crash, Node power loss, storage-controller restart, zone loss, or regional loss. “The volume is replicated” is incomplete without the replication boundary and acknowledgement semantics.


## Why local storage is neither bad nor automatically safe

Local persistent volumes can provide predictable latency and avoid network dependencies. They also tie data to a Node and make replacement, maintenance, and disaster recovery an explicit application concern. For systems with native replication and repair, local disks can be appropriate. For a singleton database without replication, a failed Node may turn a routine Pod restart into a manual data-recovery event.

The design should compare local and remote storage against workload semantics, not fashion. Ask whether the application can replicate, whether Node identity is durable enough, how failed media is replaced, how backups leave the Node, and how the scheduler avoids stranding the workload. Atlas uses local directories only in the dependency-light lane and labels them as local mechanism evidence.


## Data classification changes platform APIs

A platform that asks developers only for “size” and “fast or standard” hides important requirements. A stronger claim includes authority, access pattern, consistency, retention, recovery objective, residency, encryption, deletion, and expected growth. Those fields can map to StorageClasses, data services, backup policies, quotas, and review gates.

Course 10 will eventually expose a higher-level platform API. Course 6 provides its vocabulary. The API should not let a developer request “highly available storage” without choosing or inheriting a data-service profile that defines replication, failure domains, fencing, backup, and restore evidence.


## A practical responsibility review

Run the responsibility review before selecting technology. The service owner defines data meaning, legal retention, schema, consistency, and acceptable loss. The platform owner defines supported storage classes, CSI drivers, snapshot stack, backup capability, monitoring, and cluster-level policy. The storage provider owns documented backend behavior. Security owners define key and access boundaries. Incident owners define authority during recovery.

If any cell is empty, the design is not ready. Responsibility matrices are useful only when they name actions and decisions rather than vague labels such as “consulted.” Who can delete a retained snapshot? Who can rotate the key? Who can accept data loss to meet RTO? Those are executable authorities.

## Worked semantic example

```python
from atlas_data.models import DataClass, FailureDomain

transactional = DataClass(
    name="run-state",
    authoritative=True,
    maximum_loss=FailureDomain.REGION,
    allowed_rpo_seconds=60,
    allowed_rto_seconds=900,
    writers=1,
)
transactional.validate()
```

The example is intentionally small enough to inspect. It establishes one invariant in the dependency-light lane; it does not claim native Kubernetes or storage-system conformance.

## Production-intent API fragment

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: atlas-transactional-state
spec:
  accessModes: [ReadWriteOncePod]
  storageClassName: atlas-rwo-durable
  resources:
    requests:
      storage: 20Gi
```

The manifest is a contract candidate. Its effect depends on admission, installed controllers, CSI capabilities, backend behavior, and application compatibility.

## Failure signatures

| Observation | Likely missing guarantee | Decisive evidence |
|---|---|---|
| Pod replacement | container-layer data vanishes | data-class catalogue and lifetime contract |
| Namespace deletion | claims or snapshots disappear unexpectedly | retention and deletion authority |
| Node loss | local data becomes inaccessible | failure-domain and recovery plan |

## Atlas capstone increment

A machine-readable data catalogue assigns lifetime, authority, RPO, RTO, writer count, retention, and deletion ownership to every Atlas data class.

## Evidence boundary

The module’s Python and filesystem tests can falsify logical invariants and local durability mechanisms. Cluster controller behavior, CSI RPC behavior, snapshot semantics, cloud durability, and operated recovery require the corresponding native evidence lane. Record unavailable evidence as `not-executed`.

## Transition

Module 2 turns those data requirements into concrete PV, PVC, StorageClass, binding, and reclaim behavior.

## Advanced design review — failure domains form a lattice

Failure domains are not a single ordered list in every system. A zonal storage service may survive Node failure but share an account-level control plane with its cross-zone replica. An off-cluster backup can survive cluster deletion yet remain vulnerable to the same KMS key, organization administrator, or ransomware identity. Model both physical and administrative domains. For each copy, ask which hardware, region, account, credentials, keys, catalogue, and operator can destroy or make it unusable.

This changes the meaning of “three copies.” Three replicas behind one compromised identity are one administrative copy. A snapshot and its source in one thin-provisioned pool are not independent capacity copies. A backup without its manifest or key is incomplete. The data catalogue should therefore include dependency edges, not just locations.

## Design review questions

- Can the service identify the exact commit or generation represented by every recovery copy?
- Can a namespace deletion, GitOps prune, or compromised workload delete all copies?
- Does the writer authority survive process restart and reject an old generation?
- Can recovery be performed without the source cluster, account session, or DNS?
- Which data is intentionally disposable, and is its resource consumption still bounded?

A platform team should be able to reject a request whose requirements are contradictory—for example, zero data loss across regional failure with one asynchronous single-region database—rather than translating it into a misleading storage-class name.
## Design clinic — write a durability contract before choosing storage

A useful durability contract is short enough to review and precise enough to falsify. For each data set, state the authoritative copy, acknowledgement point, tolerated failures, maximum acceptable loss, maximum restoration time, and deletion authority. Do not begin with a product name. Begin with the result the service must preserve.

| Data set | Authoritative owner | Success may be acknowledged after | Failure the design must survive | Recovery target |
|---|---|---|---|---|
| analysis-run state | database transaction owner | durable commit and required replication acknowledgement | API restart and Node loss | no acknowledged mutation lost |
| immutable artifact | artifact publisher | content digest, object publication, and metadata commit | worker restart and duplicate publication | same bytes under the same identity |
| worker scratch | current worker attempt | never part of a client-visible success | container or Pod replacement | complete recomputation is acceptable |
| backup catalogue | recovery system | manifest and referenced objects are durable | cluster deletion | restore into an empty destination |
| cache entry | cache owner | not authoritative | complete cache loss | refill from owner without semantic drift |

The table is not merely documentation. It determines architecture. If transactional state and artifacts have different owners and recovery semantics, placing both on one shared filesystem does not simplify the system; it hides two contracts behind one mount. If a cache cannot be discarded, it is not a cache. If an audit record is required to explain a recovery decision, it belongs to the recovery evidence plane rather than to the application’s temporary logs.

### Separate the data plane, control plane, and recovery plane

Three kinds of state are often confused:

- **Data-plane state** is the business or workload data whose correctness users care about.
- **Control-plane state** describes how the platform intends to provision, attach, schedule, and protect that data.
- **Recovery-plane state** contains the independent manifests, keys, catalogues, runbooks, and evidence required to rebuild or validate the data plane.

A PVC is control-plane state. The bytes behind the bound volume are data-plane state. A backup manifest and its encryption-key reference are recovery-plane state. Restoring only the Kubernetes objects does not restore the data. Restoring only a disk image may not restore a usable service if membership, keys, schema, or generation metadata are missing. A complete recovery design names all three planes and ensures that a single failure cannot silently destroy them together.

### Durability claims need an acknowledgement boundary

Suppose an API stores a mutation in a buffered file and immediately returns `201 Created`. The Pod then loses power before the buffer reaches stable media. The presence of a PVC did not protect the contract; the application acknowledged too early. Conversely, forcing every byte through a globally synchronous replication path can satisfy a strong durability target while making latency and availability unacceptable. The engineering task is to choose the acknowledgement boundary that matches the service objective and to expose its cost honestly.

For a database, the acknowledgement boundary may include a write-ahead log flush, quorum replication, or a storage-system durability guarantee. For a content-addressed artifact, it may include writing a temporary object, synchronizing it, atomically publishing the final name, and committing metadata that refers to the digest. For an event, it may include the authoritative state change and outbox record in one transaction. Kubernetes can mount the storage, but it cannot decide where application success begins.

### Model destructive authority explicitly

Most storage incidents are not media failures. They are authorized operations performed with the wrong scope: deleting a namespace, changing a reclaim policy, pruning a claim from Git, expiring an object lifecycle rule, rotating away the only decryption key, or restoring into a non-empty destination. The data contract should list destructive actions and the principal allowed to perform each one.

A mature deletion workflow often has stages:

1. mark the logical data set for retirement;
2. stop new writers and record the final generation;
3. verify retention and legal constraints;
4. preserve or expire recovery copies deliberately;
5. remove platform bindings;
6. delete physical copies;
7. record evidence that the requested scope—and only that scope—was removed.

This is slower than `kubectl delete pvc`, because deletion is a business transition rather than a cleanup command.

### Failure-domain reasoning exercise

For every Atlas data class, walk through this sequence:

```text
process crash
→ container restart
→ Pod replacement
→ Node loss
→ zone loss
→ cluster loss
→ cloud-account compromise
→ operator deletion
```

At each arrow, answer four questions:

1. Is the authoritative copy still present?
2. Can the service reach it?
3. Is its latest acknowledged generation intact?
4. Does the recovery team still possess the evidence and keys needed to use it?

A “yes” to the first question is not enough. Data can exist but be unreachable, stale, encrypted with a lost key, or inconsistent with the application’s membership state. This four-question test prevents storage presence from being mistaken for service recovery.

## Decision record for Atlas

Atlas adopts the following hard boundaries for the remainder of the course:

- Kubernetes objects never constitute the only backup of business data.
- A mounted volume never proves application consistency.
- Single-writer data requires a generation or fencing mechanism in addition to attachment policy.
- Recovery evidence is retained separately from the primary cluster.
- Every destructive operation names an owner, scope, precondition, and audit record.
- A release cannot strengthen its durability claim without an executed failure or restore proof at the corresponding evidence level.

These rules are intentionally inconvenient. They prevent later modules from “solving” data safety with a StorageClass name, a StatefulSet, or a snapshot status field.
