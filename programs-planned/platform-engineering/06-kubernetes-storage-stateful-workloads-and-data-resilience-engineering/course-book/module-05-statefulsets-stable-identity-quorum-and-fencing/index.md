# Module 05 — StatefulSets, Stable Identity, Quorum, and Fencing

> **Governing question:** When does stable ordinal identity help, and what additional mechanisms prevent two replicas from believing they own the same data?

## Why this module exists

A Node loses network connectivity but continues running a database process. Kubernetes eventually schedules a replacement Pod and the storage backend force-detaches the volume. The original process regains connectivity and attempts another write. Stable Pod names and a successful attach do not prevent two logical writers.

This module does not begin with YAML. It begins by locating authority and the earliest missing transition. Kubernetes storage is a set of cooperating control loops around an external data system; the application still owns the meaning and correctness of the data.

## Learning outcomes

- explain StatefulSet Pod, DNS, and PVC identity
- evaluate OrderedReady and Parallel management policies
- reason about update partitions and claim retention
- separate stable identity from leader election, quorum, and replication
- implement monotonic fencing generations
- diagnose split brain during Node loss and force detach

## What StatefulSet actually guarantees

A StatefulSet assigns stable ordinal names, stable network identities through a governing Service, and deterministic PVC names from claim templates. It can order creation, deletion, scaling, and updates. These are orchestration guarantees. The controller does not replicate data, elect a leader, form quorum, repair logs, or decide which replica is authoritative after a partition.

The right question is not “is the application stateful?” but “does it require stable per-member identity or ordered lifecycle?” A single-writer database may use a StatefulSet for stable claim identity. A stateless worker with a durable queue usually should remain a Deployment.
## Ordinal identity connects several resources

For a StatefulSet named `atlas-db`, Pod `atlas-db-0` receives a DNS identity and a claim such as `data-atlas-db-0`. Deleting and recreating the Pod preserves that ordinal and claim. Scaling down normally retains or deletes claims according to the configured PVC retention policy. Deleting the StatefulSet does not necessarily delete the claims.

This stability helps recovery only if the application and operator understand it. Reusing ordinal 0 with stale data after a restore can be dangerous. Atlas records data generation separately from Pod ordinal so identity does not imply freshness.
## Ordering is not correctness by itself

`OrderedReady` waits for lower ordinals to become ready before progressing. This can be useful when bootstrap order matters, but it can also deadlock if readiness depends on a higher ordinal. `Parallel` relaxes Pod management ordering but does not change update strategy semantics or application replication rules.

An ordered rollout can still corrupt data if the schema is incompatible. A parallel rollout can be safe when the application protocol supports mixed versions. Course 7 will automate promotion; Course 6 defines the data-safe order and evidence.
## Fencing closes the stale-writer gap

Leader election tells participants who should write. Fencing prevents a participant with an old decision from writing after leadership changes. Atlas issues a monotonically increasing generation when authority transfers. Every authoritative mutation includes the generation. The data store rejects a generation lower than the current one.

Storage attachment can contribute a physical fence, but it is not sufficient for every backend or failure. Network partitions, cached handles, delayed requests, and shared storage can preserve stale write paths. Application or storage-system fencing must be explicit.
## Quorum and data replication remain application concerns

A three-replica StatefulSet does not create a three-replica database. Replication topology, commit quorum, read consistency, lag, membership changes, and failure recovery belong to the database or operator. Pod anti-affinity can spread replicas while still leaving them in one storage failure domain. Persistent volumes can be individually durable while the database loses quorum.

Atlas uses a deliberately simple single-writer ledger in the mandatory lane. It makes fencing and restoration observable without pretending to teach a production database operator. The course compares this with managed and operator-based choices in Module 6.
## Readiness after recovery

A replacement stateful Pod may start quickly while recovery, log replay, checksum validation, membership reconciliation, or snapshot restoration is still running. Readiness must remain false until the process can serve the workload contract. Liveness should not kill slow but progressing recovery. Startup probes can protect long initialization, while application-specific conditions report phase and progress.

The Atlas stateful workload publishes `Recovering`, `Fenced`, and `Ready` states. Only `Ready` endpoints enter ordinary service traffic. Course 5’s endpoint eligibility contract therefore depends on Course 6’s data-recovery truth.

## Pod identity, data generation, and membership generation

Three generations may coexist: Kubernetes Pod incarnation, StatefulSet revision, and application data or membership generation. A recreated `atlas-db-0` has the same name but a new UID. It may mount the same PVC but join a newer database generation. Logs and metrics that use only the ordinal can merge incompatible histories.

Atlas records Pod UID, fencing generation, data generation, and schema version separately. This makes recovery and incident timelines intelligible.


## Force detach is a distributed-systems decision

When a Node is unreachable, the control plane cannot know whether the process and storage path are truly dead. Force detaching can restore availability but may violate single-writer safety. Waiting protects data but extends outage. The correct policy depends on storage fencing, workload behavior, failure detection, and business priorities.

The runbook names who may accept the risk, what evidence is required, and how the old writer is fenced. An automated timeout without a fencing guarantee is not a safe policy.


## StatefulSet updates and data compatibility

A StatefulSet rolling update proceeds by ordinal and can use partitions for staged rollout. The controller observes Pod readiness, not schema compatibility or replication health unless readiness exposes those facts. An operator can pause at one ordinal, validate replication and data format, then continue.

Atlas release evidence links each Pod revision to the data schema it can read and write. The update partition is a deployment tool; the compatibility matrix is the safety proof.


## PVC retention and environment lifecycle

Retaining claims protects data during accidental StatefulSet deletion or scale-down, but it also leaves resources and cost after ephemeral environments disappear. Deleting claims automatically simplifies cleanup but can erase evidence or recovery points. The platform should select retention by data class and environment, not one global preference.

Atlas production-intent claims retain by default. Disposable test data may delete automatically only when generated from a recoverable source and clearly labelled.

## Worked semantic example

```python
from atlas_data.fencing import FenceRegistry

fences = FenceRegistry()
first = fences.acquire("atlas-db")
second = fences.acquire("atlas-db")
fences.write("atlas-db", second, "run-42", "completed")
try:
    fences.write("atlas-db", first, "run-43", "completed")
except PermissionError:
    pass
else:
    raise AssertionError("stale writer was not fenced")
```

The example is intentionally small enough to inspect. It establishes one invariant in the dependency-light lane; it does not claim native Kubernetes or storage-system conformance.

## Production-intent API fragment

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: atlas-db
spec:
  serviceName: atlas-db
  replicas: 1
  podManagementPolicy: OrderedReady
  persistentVolumeClaimRetentionPolicy:
    whenDeleted: Retain
    whenScaled: Retain
```

The manifest is a contract candidate. Its effect depends on admission, installed controllers, CSI capabilities, backend behavior, and application compatibility.

## Failure signatures

| Observation | Likely missing guarantee | Decisive evidence |
|---|---|---|
| split brain | two members accept writes | monotonic fence |
| readiness too early | traffic reaches recovering replica | data-aware readiness |
| scale-down deletion | claim removed with ordinal | retention policy |

## Atlas capstone increment

A StatefulSet planner creates deterministic identities, while a fencing registry—not the Pod name—authorizes the current writer and delays readiness until recovery completes.

## Evidence boundary

The module’s Python and filesystem tests can falsify logical invariants and local durability mechanisms. Cluster controller behavior, CSI RPC behavior, snapshot semantics, cloud durability, and operated recovery require the corresponding native evidence lane. Record unavailable evidence as `not-executed`.

## Transition

Module 6 decides which data services belong in-cluster, which should be managed, and which responsibilities an operator may own.

## Advanced design review — stable identity amplifies both safety and error

Stable ordinals and claims make it possible for a database member to recognize its history. They also make stale history easy to reintroduce. Scaling back up can attach an old claim whose membership was removed months ago; a stable DNS name can direct traffic to a member that is mounted but not current. Bootstrap must validate generation, cluster identity, and membership before reusing state.

Fencing should be designed so the stale actor cannot bypass it. A Kubernetes Lease observed only by the new Pod is insufficient if the old process can keep writing to the backend. Stronger mechanisms include storage reservation, VM power fencing, database term/epoch validation, or a transaction path that rejects old generations. Availability procedures must state when force-detach or promotion is allowed and what data-loss risk is accepted.

## Availability math belongs to the database protocol

StatefulSet ordering, replica count, PDB, anti-affinity, and topology spread are useful inputs. None defines quorum. Review the engine’s membership and commit rules, then map Kubernetes controls to them. A PDB that preserves two Pods is harmful if the database requires three voters to make progress; three zones are irrelevant if all durable logs share one backend failure domain.

## Membership changes are data migrations

Adding or removing a database member changes replicated history, quorum, and failure tolerance. It should be treated with the same discipline as a schema migration. The operation has a stable identity, prerequisites, phases, verification, abort conditions, and retained evidence. Scaling the StatefulSet is only one implementation step and may be the wrong first step.

For addition, create storage and process identity, join the member through the engine protocol, transfer or replay data, verify catch-up, then count it in quorum or route reads. For removal, move or drain leadership, remove the member from the consensus configuration, confirm remaining quorum, fence the old generation, and only then retire the Pod and eventually its claim. Reversing those steps can leave stale voters, unreplicated data, or a claim that later rejoins incorrectly.

## Recovery must distinguish replacement from resurrection

A replacement member receives a new process and possibly a new Node but can preserve the same logical ordinal and claim. A resurrected old machine or process may reappear with stale credentials and storage access. The platform should assign a new attempt or fence generation to replacement and reject the resurrected actor. This rule applies beyond databases: job workers, controllers, and storage attachments all need a way to distinguish current authority from historical identity.

During a partition, resist the temptation to choose the newest Pod or fastest side. Authority comes from the protocol’s committed term, quorum, and fencing evidence. Recovery that selects a winner without that evidence is a data-loss decision and must be labelled as such.
## Stable identity is not writer authority

A StatefulSet gives Pods stable ordinals, DNS identities, and per-ordinal claims. These properties are useful for membership and storage association. They do not elect a leader, prove quorum, or revoke a process that continues writing after a partition. The distinction is foundational:

```text
stateful identity: db-0, db-1, db-2
writer authority: generation 47 accepted by the data service
```

A replacement `db-0` may have the same Kubernetes identity as the previous Pod while representing a new process incarnation. If the old process can still reach storage or peers, identity reuse without generation fencing can produce two writers claiming the same logical role.

### Quorum protects decisions, not every operational action

Consensus systems typically require a majority to commit a new value. For three voting members, two must agree; for five, three. Quorum can preserve a single committed history during partitions, but only when membership, transport, storage, and clock assumptions match the implementation. Kubernetes does not add quorum by creating three Pods.

The platform must understand:

- voter versus learner or replica roles;
- membership-change protocol;
- bootstrap rules;
- quorum loss behavior;
- leader election and lease duration;
- write acknowledgement policy;
- snapshot and log retention;
- recovery from a lost majority;
- whether a member’s persistent identity may be reused.

A PodDisruptionBudget reduces voluntary simultaneous disruption; it cannot prevent hardware loss, operator force deletion, or application-level quorum mistakes.

### Fencing closes the stale-writer window

Fencing is a monotonic authority check. A new leader or worker receives a higher generation, epoch, term, or token. Every state-changing operation carries that value, and the authoritative store rejects values older than the current generation. Merely acquiring a lease is insufficient if the stale holder can continue writing without presenting the lease generation.

Atlas demonstrates durable fencing with a ledger:

```text
writer A receives generation 12
writer B takes over and receives generation 13
late write from A with generation 12 → rejected
write from B with generation 13 → accepted
```

The generation must be stored at the same authority boundary as the protected mutation. An in-memory counter in the controller cannot fence a writer after controller restart. A ConfigMap-based lease may coordinate actors, but the data store still needs to enforce the resulting generation when stale access is possible.

### StatefulSet update ordering and data compatibility

Ordered Pod replacement can help applications that require one member at a time, but it can also stall indefinitely when the highest ordinal is unhealthy. Parallel management can speed bootstrap or recovery while violating assumptions of systems that depend on ordered membership.

Application compatibility must be considered independently of Pod readiness. During a rolling update, old and new binaries may share a database, replication protocol, or on-disk format. The release must answer:

- Can old and new members communicate?
- Can either version read data written by the other?
- Is the schema expanded before new writers start?
- Can the binary roll back after the on-disk format advances?
- Does leadership need to move before upgrade?
- Which member is safe to update first?

A successful StatefulSet rollout only proves the Kubernetes controller reached its desired Pod template; it does not prove data compatibility.

### Claim retention and ordinal reuse

StatefulSet claim templates usually create one PVC per ordinal. Retention policy determines whether claims remain when replicas scale down or the StatefulSet is deleted. Retaining claims protects data from accidental workload deletion but can surprise operators during scale-up: a reused ordinal may attach old data that no longer belongs in the current membership.

Before reusing an ordinal, validate:

- the data generation;
- cluster or system identity;
- membership status;
- encryption keys;
- schema version;
- snapshot or restore lineage;
- whether the member was cleanly removed;
- whether a newer authoritative copy exists elsewhere.

Deletion is not the only risk. Silent reuse of stale but valid-looking data can be worse than an obvious missing volume.

### Bootstrap and disaster recovery are different workflows

Initial bootstrap assumes no authoritative history. Disaster recovery assumes a history existed and must be selected correctly. Reusing bootstrap scripts during recovery can initialize a new empty cluster beside retained volumes, reset membership identifiers, or overwrite recovery metadata.

Atlas separates:

```text
bootstrap: create first authoritative generation
join: add a member to an existing generation
replace: substitute a failed member without changing history
restore: create a new runtime from a selected recovery point
```

Each operation has distinct preconditions and evidence. A controller or operator should reject ambiguous state rather than guess.

### Readiness for quorum systems

A stateful member can be process-alive but unsafe for traffic. Readiness may require:

- membership in the intended cluster;
- current term or generation;
- sufficient replication progress;
- valid local storage;
- no recovery or replay still in progress;
- ability to serve the requested consistency level;
- accepted fencing token;
- no pending schema or format transition.

Using a simple TCP probe can route clients to a member that is listening but stale. Conversely, making liveness depend on peer quorum can trigger restart storms during a network partition. Liveness asks whether the local process can make progress; readiness asks whether it can safely serve.

### Final StatefulSet design review

Approve a StatefulSet only when stable identity is a real application requirement. Then require evidence for:

1. identity-to-storage mapping;
2. bootstrap, join, replace, and restore paths;
3. quorum and membership changes;
4. durable fencing;
5. upgrade and rollback compatibility;
6. claim retention and ordinal reuse;
7. readiness semantics;
8. disruption policy;
9. snapshot and backup consistency;
10. recovery after one member and one Node loss at the claimed tier.

A stateless worker with durable jobs may be better represented by a Deployment. StatefulSet is a lifecycle tool, not a badge of data seriousness.
