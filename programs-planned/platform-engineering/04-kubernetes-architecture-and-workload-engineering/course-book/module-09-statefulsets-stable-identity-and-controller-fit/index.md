# Module 9 — StatefulSets, stable identity, and controller fit

A StatefulSet is often described as “the controller for databases.” That description is too broad and encourages false confidence. StatefulSet provides stable Pod identity, ordered or parallel management, and stable association with volume claims. It does not implement replication, consensus, backup, failover correctness, or data repair.

The design question is:

> Which identity or ordering must survive Pod replacement, and which data-system guarantees remain the application's responsibility?

## Stable ordinal identity

StatefulSet Pods have predictable names:

```text
atlas-sentinel-0
atlas-sentinel-1
atlas-sentinel-2
```

A replacement for ordinal 1 reuses `atlas-sentinel-1`, though it receives a new Pod UID. The stable ordinal can support membership, partition identity, or storage association.

A Deployment intentionally treats replicas as interchangeable. If the application does not need a stable ordinal, StatefulSet adds constraints without value.

## Network identity depends on a governing Service

A StatefulSet names a governing Service, normally a headless Service, to establish stable DNS identities. Course 4 records the object relationship; Course 5 explains DNS and service networking. Stable DNS naming still depends on control-plane and network components and does not make the process available.

## Stable storage association

`volumeClaimTemplates` can create one PVC per ordinal. A replacement Pod for the ordinal reuses its claim. That association is valuable, but the PVC only represents a storage request/binding. The storage system's durability, topology, snapshots, replication, restore, and failure behavior belong to Course 6.

A StatefulSet with an `emptyDir` has stable Pod names and ephemeral data. A StatefulSet with one local volume per Node can lose access after Node failure. The controller name does not change those facts.

## PVC retention is deliberate

By default, StatefulSet-created PVCs are retained when Pods are scaled down or the StatefulSet is deleted. This protects data from casual controller deletion but leaves lifecycle work for operators. Modern retention policy fields can change behavior, but deletion must be supported by application and backup evidence.

Course 4 never auto-deletes Atlas state claims merely because the workload object is deleted.

## OrderedReady and Parallel management

Default `OrderedReady` behavior creates or updates Pods in ordinal order and waits for predecessors to be Ready. This is useful when order is an application invariant. It can also deadlock a rollout if one lower ordinal cannot become Ready.

`Parallel` permits concurrent creation/deletion and is appropriate when replicas do not need ordered startup. Choosing Parallel while relying on implicit order is a bug; choosing OrderedReady without need increases recovery time.

## Rolling updates and partitions

A StatefulSet RollingUpdate replaces Pods in reverse ordinal order. A partition can update only ordinals at or above a threshold, enabling canary or staged rollout.

OnDelete strategy requires operators or another workflow to delete Pods to adopt the new template. It can support careful systems but moves rollout responsibility elsewhere. Course 7 would need to govern that choreography.

## Identity is not leadership

Ordinal 0 is not automatically a safe leader. Leadership requires consensus, leases, fencing, or another algorithm. Assuming `pod-0` is always leader can produce split brain during network partition or delayed termination.

Kubernetes Lease objects can support coordination, but the application still needs a correct protocol. Course 4's sentinel lab uses ordinal identity only; it does not claim consensus.

## Identity is not data correctness

Suppose `atlas-db-0` restarts and reattaches its volume. This preserves a data copy, but several questions remain:

- was the last write durable?
- is the volume accessible in the new zone?
- is the data logically consistent?
- is another replica ahead?
- can the application recover its journal?
- is the backup restorable?

StatefulSet does not answer them.

## Headless service does not load-balance

A headless Service commonly returns individual Pod addresses. Clients may implement their own discovery and routing. Course 5 will examine DNS records, readiness, and client behavior. Course 4 only records the stable identity requirement.

## When Atlas should not use a StatefulSet

### Atlas API

Replicas are interchangeable, stateless at the Pod level, and should roll independently. Deployment is correct.

### Atlas worker

The worker consumes durable queue state and writes durable results, but the process itself does not require stable ordinal identity. A Deployment remains correct. Course 6 will determine how multiple workers coordinate storage/queue access.

### Atlas stable-identity sentinel

A lab-only component demonstrates ordinal identity and partitioned rollout. It stores no production data and is excluded from the accepted Atlas workload release.

This explicit rejection is important. Learning a controller includes learning when not to use it.

## Stateful application operator boundary

Complex databases often need domain-specific orchestration for membership, backup, failover, and upgrade. An operator can encode that knowledge, but it must be evaluated as software with authority and failure modes. A StatefulSet may be one child object; it is not the entire operator.

Course 10 introduces custom controllers generally. Course 6 later studies storage/data resilience before the program claims any stateful production capability.

## Worked failure: stable name, lost data

A sentinel Pod writes to `emptyDir`, is deleted, and returns with the same ordinal name. The file is gone. An operator says StatefulSet failed to preserve state.

The controller preserved the identity it promised: ordinal and governing relationship. The volume class was ephemeral. The design failed by assigning a durability expectation to the wrong mechanism.

## Worked failure: OrderedReady deadlock

A three-replica StatefulSet updates. Pod 2 is replaced and becomes Ready, then Pod 1 fails readiness due to corrupted configuration. Pod 0 remains old because ordered rollout cannot proceed. The controller is preserving order.

The repair is to correct Pod 1 or make an explicit partition/rollback decision. Deleting Pod 0 to “speed up” rollout can violate application ordering.

## Stable identity evidence

A useful report records:

- StatefulSet UID and generation;
- Pod ordinal, name, and UID before/after replacement;
- governing Service reference;
- PVC names and retention policy;
- update strategy and partition;
- readiness order;
- application membership/leadership protocol, if any;
- data durability owner and evidence boundary.

## Capstone increment

`atlas_kube/stateful.py` models ordinal identity, ordered/parallel creation, partitions, and claim retention. The manifest laboratory deploys `atlas-sentinel` without production data. The final architecture decision explicitly rejects StatefulSet for Atlas API and worker.

## Further reading

- StatefulSets: <https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/>
- Persistent volumes: <https://kubernetes.io/docs/concepts/storage/persistent-volumes/>
- Leases: <https://kubernetes.io/docs/concepts/architecture/leases/>

## Transition

Built-in controllers cover many workload invariants. Module 10 asks when Atlas needs a new API and reconciler, then builds a small controller that follows Kubernetes ownership, status, finalizer, and idempotency conventions.

## Worked decision — does Atlas worker need a StatefulSet?

The Atlas worker consumes a durable queue and publishes results to durable storage. A proposal argues that it should become a StatefulSet because it “handles state.” This confuses application state with Pod identity.

Ask whether each replica needs:

- a stable ordinal identity;
- stable per-replica network naming;
- stable per-replica storage association;
- ordered creation, update, or termination;
- application semantics that map work ownership to that identity.

The baseline worker needs none of these. Queue state is external, effects are idempotent, and any replica can process any eligible item. A Deployment remains the better controller. Adding stable identity would create coupling without solving durability.

Now consider a partitioned processor where ordinal 0 owns partitions 0–9 and ordinal 1 owns 10–19, with local durable checkpoints. Stable identity may be meaningful. The design must still handle rescheduling, fencing, storage attachment, partition reassignment, backup, and restore. StatefulSet supplies identity mechanics; it does not supply consensus or data safety.

### PVC retention is a lifecycle policy

A StatefulSet can create per-Pod claims through volume claim templates. Deleting or scaling the StatefulSet does not necessarily delete those claims. This safety can also create orphaned cost and stale data. Retention behavior must be explicit and tested. A replacement Pod reusing a claim may observe data produced by an older software version.

### Headless service is an identity mechanism

Stable network identity is commonly exposed through a headless Service. That does not make the protocol safe or the endpoint healthy. Clients still need discovery, readiness, retry, and membership rules. Course 5 owns the network data plane; Course 4 records only the identity requirement.

## Controller-fit test

Choose StatefulSet only when removing stable identity would break a documented invariant. Choose Deployment for replaceable replicas. Choose Job for finite completion. Choose DaemonSet for node-derived cardinality. Choose a custom controller only when none of these control loops can express the desired relationship without hiding important state in application code.

## Common false conclusions

- **“Stateful application means StatefulSet.”** Controller choice follows identity and lifecycle invariants.
- **“Stable Pod name means stable process.”** Containers and Pods can still restart and be recreated.
- **“PVC means data is backed up.”** Persistence, backup, restore, and resilience are separate claims.
- **“Ordered rollout means safe distributed-system upgrade.”** Protocol and data compatibility remain application responsibilities.
- **“One replica avoids distributed-systems problems.”** It often converts them into availability and recovery problems.

## Failure case — stable identity amplifies a bad assumption

A three-replica StatefulSet maps each ordinal to an external partition. After restoring an old PVC snapshot for ordinal 1, the Pod resumes with stale checkpoint state and reprocesses effects. Kubernetes correctly preserved identity; the application incorrectly treated identity as proof of current ownership. Fencing generation, replay-safe effects, and restore coordination remain necessary.

This illustrates the governing rule: stable identity is a mechanism. Safety comes from the protocol that uses it.
