---
module_id: PLAT-045
program: Platform Engineering
level: 1
module_number: 45
title: Stateful Workload Standards
status: complete
last_verified: 2026-09-02
---

# Stateful Workload Standards

## One-Page Review

### Governing question

How should a platform decide which stateful workloads it will support and enforce identity, membership, replication, consistency, fencing, storage, topology, maintenance, upgrade, backup, recovery, security, observability, and retirement standards without implying that StatefulSet or persistent storage operates a correct database?

### Essential definitions

- **authoritative state** is data whose loss, divergence, stale acceptance, or unauthorized mutation changes the system’s promised truth.
- A **stateful workload standard** is a versioned admission and lifecycle contract for software whose correctness depends on persistent data, stable member identity, membership, ordering, or recovery.
- A **stable member identity** survives process/Pod replacement and names one logical replica; it is distinct from the disposable Pod UID and from the data volume.
- **membership** is the authoritative set and roles of replicas participating in a protocol; desired replica count is not automatically membership.
- **quorum** is the minimum agreeing subset required by a protocol for a specified operation; it is not merely “most Pods ready.”
- **fencing** makes stale actors unable to mutate authoritative state, commonly through monotonically increasing epochs/tokens enforced by the storage or protocol authority.
- A **failure domain** is a set of components likely to fail together, such as one node, rack, zone, region, account, key authority, or control plane.
- A **crash-consistent snapshot** resembles storage after abrupt power loss; an **application-consistent backup** also respects the application’s transaction/protocol boundary.
- **RPO** bounds acceptable data loss measured backward from an incident; **RTO** bounds acceptable time to restore the service outcome.
- A **domain operator** is a controller encoding application-specific lifecycle knowledge such as membership, failover, backup, restore, and upgrade; a generic reconciler does not acquire that knowledge by naming itself an operator.

### Central model, mechanism, or theorem

Let stateful service contract $S=(A,C,M,R,F,V,T,U,B,O,L)$ contain authority $A$, consistency $C$, membership $M$, replication/quorum $R$, fencing $F$, storage $V$, topology $T$, upgrade/maintenance $U$, backup/recovery $B$, observability $O$, and lifecycle $L$. A runtime mapping is admissible only when every mandatory property has an owner, mechanism, evidence, and tested failure response. For a majority protocol with $n$ voting members, quorum $q=\lfloor n/2\rfloor+1$ and tolerable member failures $f=n-q=\lfloor(n-1)/2\rfloor$ only under the protocol’s timing, independence, durability, and membership assumptions. Kubernetes identity or storage objects do not establish those assumptions.

### Critical invariants

- Authoritative state, consistency, data-loss tolerance, and recovery outcome are declared before controller or storage selection.
- StatefulSet supplies stable ordinals/network names and optional stable claim association; the application/operator owns replication, quorum, membership, leadership, fencing, repair, backup, and data compatibility.
- A logical member never runs concurrently in two unfenced incarnations; force deletion and ambiguous node state require proven node/storage/protocol fencing.
- Desired replicas, protocol membership, ready Pods, healthy replicas, voting members, and recoverable copies remain distinct and observable.
- Replicas and backups are placed across independent failure domains consistent with the stated fault model; equal Pod counts do not prove independence.
- Storage class, topology, access mode, performance, encryption, reclaim/retention, expansion, snapshot, attachment, and failure behavior match the application contract.
- Persistent storage is not replication, backup, immutability, or recovery; every restore path is regularly tested to a clean environment and validated at the application layer.
- Readiness, liveness, startup, disruption, scaling, maintenance, and rollout are role- and protocol-aware; generic uniform defaults cannot establish quorum safety.
- Schema/data-format, application, operator, Kubernetes, storage, and backup-version compatibility are checked across upgrade, rollback, and restore.
- Scaling changes membership through application-aware procedures; deleting or creating Pods/PVCs does not safely add or remove members by itself.
- Operators and managed services are privileged lifecycle dependencies with version, authority, status, backup, recovery, migration, and retirement obligations.
- Deletion inventories final data, replicas, snapshots, backups, keys, credentials, DNS, volumes, external resources, audit evidence, and legal retention before revoking recovery.

### Common failures

Calling every workload with a volume stateful; using StatefulSet as a database operator; equating `Ready` with quorum health; putting three replicas and volumes in one zone; using a PDB as protection from zone failure or rollout; force-deleting an uncertain member; assuming `ReadWriteOnce` universally prevents a second Pod; binding before topology is known; snapshotting without application coordination; keeping replicas but no backup; taking backups without restore tests; autoscaling voters on CPU; scaling down by deleting the highest ordinal before membership removal; rolling incompatible binaries through a quorum; making liveness restart a slow recovering member; treating a managed service as responsibility-free; and deleting a custom resource while finalizers, volumes, snapshots, keys, or remote data remain.

### Compact example

A three-voter store promises one-zone failure tolerance and RPO five minutes/RTO one hour. Its operator owns membership, fenced leadership, role-aware health, ordered upgrades, application-consistent backup, and restore. StatefulSet supplies ordinals and claim association; a headless Service supplies discovery. Voters and zonal volumes spread one per zone, while backup copies and keys cross a separate failure boundary. `maxUnavailable: 1` is allowed for voluntary maintenance only when application quorum is healthy; rollout pauses on replication lag. A node in unknown state is fenced at compute and storage layers before ordinal replacement. Nightly recovery creates a clean isolated cluster, restores, validates checksums and domain queries, records achieved RPO/RTO, and destroys the exercise environment. Scale-down first transfers leadership and removes membership, then deletes the ordinal and handles its claim by policy.

### Connections

This module specializes the identity-bearing stateful archetype from [PLAT-041](041-workload-archetypes.md), applies the maintained template contract from [PLAT-042](042-service-templates.md), and reuses controller, storage, connectivity, configuration, security, telemetry, and data-access capabilities from [PLAT-023](023-kubernetes-declarative-resources.md) through [PLAT-039](039-database-and-data-service-access.md). It prepares the runtime, health, security, and lifecycle standards in the following modules.

## Governing Question

What evidence-backed platform standard determines whether a stateful service belongs on a managed offering, a supported domain operator, a constrained generic runtime, or outside the platform—and keeps its data correct and recoverable throughout operation and retirement?

Statefulness is not synonymous with mounting a disk. A stateless process may depend on authoritative external sessions or leases; a cache may use a volume while remaining disposable; a replicated database may need stable identity, membership, consensus, and fencing even when its storage is remote.

The platform must start from the data and protocol promise. It then decides which lifecycle owner can satisfy it. Kubernetes resources provide useful building blocks, but a declarative Pod controller cannot infer transaction boundaries, choose a new leader safely, repair a divergent replica, or prove a restored database is usable.

A standard therefore combines admission, implementation profiles, operational evidence, and retirement. It narrows supported combinations rather than offering arbitrary YAML. The platform’s strongest service may be a managed database binding; self-operation is justified only when ownership and evidence exceed the risk.

## Why This Matters

Stateful failures survive process restart. A corrupt page, stale leader, lost key, inconsistent snapshot, or mistaken scale-down can persist through every healthy green Pod. Automatic replacement can amplify damage by restarting a bad member, attaching the wrong data, or accepting two incarnations of one identity.

Replication and backup solve different problems. Replication improves availability and may copy corruption or deletion immediately. Backup preserves historical recovery points but does not serve traffic and may be unreadable, incomplete, or too slow. Both need independent failure domains and validation.

Maintenance changes the fault budget. A three-member majority system tolerates one unavailable member only while the other two are correct and connected. Draining a second member during a zone impairment removes quorum. A generic disruption budget sees Pods; it may not understand roles, lag, witnesses, learners, or an ongoing membership change.

Storage choices become architectural commitments. Topology binding determines where a Pod can move. Access modes constrain attachment but may not fence an old process. Reclaim policies decide whether deletion destroys or retains capacity. Snapshot facilities expose storage images, not necessarily transactionally coherent application state.

State also expands security and compliance obligations. Volumes, snapshots, backups, replicas, logs, exports, keys, and recovery environments can all contain sensitive records. Deleting the primary does not prove erasure; losing encryption keys without recovery planning can make valid backups useless.

## Prerequisites and Retrieval

Retrieve filesystems and crash recovery, write-ahead logging, transactions, isolation and consistency, replication, consensus, leader election, leases and fencing, quorum, membership changes, split brain, failure detectors, network partitions, CAP trade-offs, checksums, corruption, storage attachment, access modes, topology, latency/IOPS/throughput, caches, backups, snapshots, incremental logs, restore, RPO/RTO, failover/failback, schema migration, rolling upgrades, compatibility, graceful shutdown, disruption budgets, Kubernetes StatefulSet/PersistentVolume/StorageClass/VolumeSnapshot/operator concepts, security identity, encryption/key management, telemetry, incident response, cost, data retention, and deletion.

You should distinguish stateful process from stateful system; persistent data from authoritative state; Pod identity from member identity; member identity from volume identity; desired replicas from protocol membership; leader from writable authority; lease from fencing; replica from backup; snapshot from application-consistent backup; backup completion from restore validation; readiness from data health; liveness from recoverability; voluntary from involuntary disruption; storage access mode from application exclusivity; high availability from disaster recovery; failover from failback; deletion from verified erasure; and provider automation from retained accountability.

## Learning Objectives

After completing this module, you should be able to:

1. derive a stateful workload contract from authority, consistency, failure, and recovery requirements;
2. choose managed service, domain operator, or constrained self-operation through an evidence-based admission decision;
3. distinguish StatefulSet identity/storage mechanics from application replication and membership protocols;
4. calculate basic majority fault tolerance and test its failure-domain assumptions;
5. specify storage topology, access, performance, encryption, expansion, snapshot, retention, and deletion;
6. design fencing, role-aware health, disruption, scaling, and maintenance procedures;
7. govern compatible rollout, schema migration, rollback, backup, restore, failover, and failback;
8. secure and observe data, members, operators, storage, backups, and recovery environments; and
9. migrate, deprecate, and retire stateful services with complete residual-data evidence.

## Core Exposition

### Define authoritative state and the promise

Inventory every state location: memory, local ephemeral disk, persistent volume, remote database, object store, log, cache, replica, snapshot, backup, client, and downstream projection. Mark which is authoritative, derived, rebuildable, temporary, or evidence.

Specify consistency and availability at named operations. “Strong consistency” is too broad. Define whether acknowledged writes survive which failures, whether reads can be stale, how monotonic/session behavior works, what conflicts mean, and when the service refuses operation.

State the fault model: process crash, node loss, zone loss, region loss, storage corruption, credential/key loss, network partition, operator defect, malicious deletion, software regression, and correlated provider failure. Name what is tolerated and what requires restoration.

Define RPO and RTO per outcome and incident class. Zero RPO or near-zero RTO has major architectural and testing cost; do not select it as a default checkbox. Include detection, decision, provisioning, data transfer, validation, traffic cutover, and communication in RTO.

Identify data owner, service owner, operator/provider owner, storage owner, backup owner, security/key owner, incident authority, and deletion approver. Automation coordinates responsibility; it does not eliminate it.

### Use an admission hierarchy

First ask whether an existing managed data service meets consistency, data class, residency, performance, connectivity, identity, recovery, portability, and cost requirements. A managed service can reduce undifferentiated operations while introducing provider limits, shared-control responsibilities, egress, and migration obligations.

Second consider a mature domain operator whose reconciliation includes membership, failover, backup, restore, upgrade, and status for the exact application. Review its maintainers, releases, CVEs, permissions, compatibility matrix, failure behavior, recovery procedures, conformance, and support.

Use a generic StatefulSet profile only when the application itself supplies and the owning team can operate the missing domain protocol. Examples can include independent ordinal workers or applications with simple stable identity, not an implicitly supported arbitrary database.

Reject or route to specialist review when requirements include untested multi-region consensus, unusual hardware/local storage, global writes, unsupported kernel/network privileges, unbounded datasets, bespoke replication, or recovery the platform cannot exercise.

Admission is revisited. A successful prototype does not prove production recovery, and a once-supported operator can become abandoned or incompatible.

### Write the stateful service specification

Record service/data identities, authority, owners, criticality, classification, tenants, consistency, read/write paths, data size/growth, throughput/latency, member roles, replication/quorum, membership protocol, leader/fencing, storage classes and topology, network discovery, resource profile, placement, health, disruption, bootstrap, scaling, upgrade, schema migration, backup, restore, DR, security, telemetry, support, cost, retention, deletion, compatibility, exceptions, and retirement.

Separate intent from provider detail. A user may request “zonal majority store, medium throughput, five-minute RPO” from supported profiles. They should not select arbitrary reclaim policies, finalizers, privileged sidecars, or unreviewed operators.

State guarantees and non-guarantees. The platform might guarantee tested provisioning, identity, backup schedules, and restore workflow. It does not guarantee application transactions if the application bypasses the protocol, recovery from unmodeled corruption, or unlimited capacity.

Version the specification, operator, application image, data/schema format, storage driver/class, backup format/tool, and recovery procedure independently. Compatibility is a relation among them, not one version string.

### Understand StatefulSet’s actual contract

StatefulSet manages Pods with stable ordinal identities, stable network names through a governing Service, optional per-ordinal volume claims, and ordered or parallel creation/deletion plus rolling or on-delete update behavior. A replacement Pod has a new UID but retains its ordinal identity.

The controller does not form database membership, replicate data, elect a leader, enforce write fencing, choose quorum, validate lag, repair corruption, coordinate schema, back up data, or prove recovery. These belong to the application/operator and standard.

Ordered readiness can support simple bootstrap dependencies but can also wedge the set behind one broken member. Parallel management improves independence but is safe only when the application handles simultaneous creation/removal.

Rolling update order and partitions provide rollout mechanics. An application-aware operator should gate progress on protocol health and compatibility. Controller success is not proof every replica has applied schema, caught up, or retained quorum.

PersistentVolumeClaims created from templates can outlive Pods and, depending on retention configuration/policy, StatefulSet scale-down or deletion. That protects data and creates cost, privacy, and reuse obligations.

### Separate every identity

Track service identity, cluster identity, logical member ID, role, ordinal, Pod name/UID, node, volume/PV/PVC ID, storage attachment, certificate identity, fencing epoch, data generation, backup ID, and restore-cluster ID.

Do not derive durable membership solely from Pod IP or UID. Use stable logical identity and an authoritative membership store/protocol. DNS may lag changes and is discovery, not proof a member is safe.

A volume belongs to a data generation and member under explicit rules. Reattaching the wrong historical volume to a recycled member name can reintroduce stale state. Store cluster/member/generation metadata and validate it before serving.

Certificates and credentials should bind intended member/service identity with narrow permissions and rotation. Copying one cluster-wide credential to all Pods expands lateral movement and complicates member removal.

Catalog the mapping so incidents can answer: which process is serving which member generation from which volume under which epoch and software/data revision?

### Define membership before replica count

Desired controller replicas express desired Pods. Protocol membership decides voters, learners, replicas, witnesses, shards, and roles. Changing one without the other can create abandoned members, lost quorum, or multiple identities.

Bootstrap through an explicit initial membership and cluster identity. Prevent a restarted member from forming a new cluster accidentally when discovery is unavailable. Record bootstrap completion as an irreversible or carefully controlled state transition.

Add a member by allocating identity/storage, joining as non-voting/learner where the protocol supports it, transferring state, verifying catch-up and fault-domain placement, then promoting. Remove by transferring leadership, demoting/removing from membership, confirming the remaining quorum, then deleting runtime and data according to policy.

Scale-down order by ordinal is not sufficient. The highest ordinal may be leader, sole healthy copy of a shard, or behind a membership operation. Operator status must make safe candidates explicit.

Serialize membership changes unless the protocol proves joint/reconfiguration behavior for concurrent changes. A controller reconciliation loop must persist intent and recover idempotently after interruption.

### Reason about quorum and failure domains

For majority voting with $n$ members, $q=\lfloor n/2\rfloor+1$. With $n=3$, $q=2$ and one member failure is tolerated. With $n=4$, $q=3$ and still only one; an extra voter does not always increase tolerance. With $n=5$, $q=3$ and two are tolerated.

This arithmetic proves only set intersection, not service safety by itself. Members need correct protocol implementation, durable accepted state, compatible versions, valid membership, sufficiently independent failures, and network paths.

Place voters so the stated failure domain cannot remove quorum. Three Pods on different nodes but one zone do not tolerate zone loss. Three zones in one region do not tolerate region/control-plane/key-authority failure.

Storage topology matters alongside compute. Pods spread across zones with all backing volumes or snapshots dependent on one system retain correlated failure. Include DNS, load balancers, certificate authorities, identity providers, and operator/control-plane dependencies in the availability graph.

Quorum availability and data durability are different. A quorum can be online with latent corruption; several replicas may contain the same bad write. Checksums, scrubbing, backups, and recovery points address other hazards.

### Fence stale and duplicate actors

Leader election or lease acquisition says who currently believes it has authority. A paused old leader can resume after its lease expired. Fencing requires the authoritative write target to reject stale epochs/tokens.

Use monotonically increasing term/epoch, storage reservation, compare-and-swap generation, provider fencing API, or protocol-native authority. Every protected write includes the epoch or occurs through a connection invalidated on loss.

Killing a Pod is not fencing. A node can be partitioned from the control plane while the process and storage path remain active. Force-deleting the Pod object tells Kubernetes not to wait for confirmation and can permit another Pod with the same StatefulSet identity.

Before forced replacement, prove the node/process cannot act through power-off, hypervisor/provider fencing, storage detach/reservation, network isolation, or protocol membership/epoch enforcement. Record authority and evidence.

Read paths can also require fencing when stale reads violate the contract. Readiness must reflect leadership/lease and replication state rather than process responsiveness alone.

### Specify storage behavior

Choose capacity, IOPS, throughput, latency distribution, durability, topology, access mode, filesystem/block mode, encryption, key ownership, expansion, snapshot/clone, attach/detach time, multi-attach handling, health monitoring, reclaim, retention, cost, and deletion.

Kubernetes access modes describe matching/mount constraints, not universal application locks. `ReadWriteOnce` allows read-write mounting by a single node and can still permit multiple Pods on that node. `ReadWriteOncePod`, for supported CSI paths, is the mode intended to constrain one Pod cluster-wide. Neither fences an already running process outside the observed attachment path.

Use delayed binding such as `WaitForFirstConsumer` when topology-aware provisioning must follow scheduling; immediate binding can allocate a volume in a zone that makes the Pod unschedulable. Test rescheduling and capacity shortage.

Reclaim policy `Delete` may destroy underlying storage after claim release; `Retain` preserves it for manual handling. Neither substitutes for a data lifecycle workflow. Protect critical claims and volumes from accidental deletion while still enabling verified retirement.

Expansion needs application/filesystem support, capacity headroom, monitoring, rollback/recovery, and quotas. Storage resize does not rebalance shards or improve per-volume performance automatically.

### Treat snapshots and backups as distinct mechanisms

A storage snapshot captures one volume at a provider-defined point. It may be crash-consistent. Multi-volume or distributed state can require coordinated quiescence, transaction markers, log positions, and application metadata.

An application-consistent backup records a recoverable transaction/protocol boundary, cluster identity rules, schema/version, encryption/key reference, checksums, completeness, source, timestamps, retention, and restoration instructions.

Replicas are online copies, not backups: user deletion, logical corruption, compromised credentials, and bad software can propagate. Snapshots in the same account/region/key boundary may not satisfy disaster or malicious-deletion recovery.

Use full, incremental, and log/point-in-time mechanisms according to RPO, restore complexity, bandwidth, and retention. A chain with a missing or corrupt increment is not recoverable merely because every scheduled job reported success.

Encrypt backup data and metadata, isolate write/delete authority, use immutability where required, rotate keys without orphaning historical backups, and test key recovery. Limit recovery operators from production mutation where separation of duties matters.

### Prove restore, not backup activity

Backup success proves an artifact was produced, not that it is complete, decryptable, compatible, timely, or useful. Recovery tests create a clean isolated environment with no hidden dependency on production state.

Select a declared point, provision compatible runtime/storage/operator, obtain keys under controlled authority, restore full/incremental/log data, validate checksums and protocol health, run domain queries and invariants, measure achieved RPO/RTO, and record evidence.

Test empty bootstrap, single-member loss, total cluster loss, corrupt latest backup, missing key, incompatible version, regional dependency outage, and large real-world data scale. Tabletop exercises do not replace technical restoration.

Restore must not connect accidentally to production peers, clients, outbound integrations, or credentials. Use new cluster identity and isolated network, then follow an explicit promotion/cutover process.

Regular tests should sample backup ages and formats across the retention window. An old legally required backup is useless if current tooling cannot read it and no compatible recovery environment exists.

### Design health as protocol evidence

Startup means the member has initialized storage, validated identity/generation, joined or intentionally bootstrapped, and reached a state from which health checks are meaningful. Slow recovery belongs behind startup, not repeated liveness kills.

Liveness detects a locally unrecoverable process condition where restart improves the situation. It must not restart on ordinary replication lag, absent leader during election, unavailable optional dependency, or a state requiring operator repair.

Readiness indicates whether this endpoint may serve its advertised read/write role consistently. A follower may be ready for stale reads but not writes; a leader without quorum or with an expired fence is not write-ready.

Cluster health includes membership, quorum, leader/term, replication lag, durable commit, shard coverage, under-replication, corruption, storage health/capacity, backup freshness, restore evidence, certificate/key expiry, and operator reconciliation.

Do not make every member’s readiness depend on every peer in a way that removes all endpoints during a partial failure. Model service outcome and role-specific routing.

### Govern disruption and maintenance

PodDisruptionBudget limits certain voluntary evictions. It does not prevent node crash, zone loss, direct Pod deletion, controller rollout behavior in every path, or application loss of quorum. Calculate it from current protocol health and roles.

Before node drain, verify no existing failure consumes the budget, transfer leadership, catch up replicas, ensure storage can attach in target topology, and observe one change at a time where required. Pause if lag, quorum, backup, or capacity violates thresholds.

Graceful node shutdown can help kubelet terminate Pods according to configured priorities and grace periods, but abrupt power loss remains in the fault model. Application logs and recovery protocols must handle both.

Maintenance runbooks name stop conditions, rollback, fencing, provider/storage dependencies, on-call roles, and escalation. An automated drain should not override a domain operator that reports unsafe disruption.

Plan simultaneous maintenance and involuntary failure. “One unavailable allowed” assumes the other members and their domains are healthy; live evidence must confirm it.

### Scale state through data-aware operations

Vertical scale changes resources and restarts/reschedules members. Validate memory representation, cache warmup, storage throughput, scheduling feasibility, QoS, eviction, and rollback. More memory can lengthen restart or make placement scarce.

Horizontal scale changes membership, replication traffic, partitions/shards, recovery duration, and cost. It may decrease availability temporarily while transferring data. CPU utilization alone cannot choose voters or shard movement safely.

Capacity planning includes data growth, write amplification, compaction, indexes, replication factor, backup/snapshot space, temporary repair/migration headroom, network, restore bandwidth, and failure-mode capacity.

Preserve spare capacity to rebuild one failure without exhausting remaining members. A cluster at 80% disk may cross critical thresholds when a replica rebuilds or compaction doubles temporary usage.

Scale-in requires proof that no unique data remains, quorum survives, clients no longer address the member, snapshots/backups remain governed, and its volume/identity are retired or retained intentionally.

### Upgrade binaries, data, and operators coherently

Maintain a compatibility matrix across application versions, wire protocols, data formats, schemas, operators/CRDs, Kubernetes releases, CSI drivers/storage, backup agents/formats, and observability/security integrations.

Use expand-and-contract for schema/protocol changes: introduce readers/writers compatible with old and new, migrate/backfill, verify, switch authority, then remove old support after rollback and retained-backup requirements expire.

Canary or rolling member upgrades respect leadership, quorum, lag, role, and version-skew limits. Pause after each fault domain/member and validate domain operations, not only Pod readiness.

Rollback is often asymmetric. Once data format or schema changes, the old binary may not read it. State whether rollback means binary downgrade, forward fix, restore to a prior point with data loss, or failover to an untouched environment.

Upgrade the operator itself with CRD storage/conversion, reconciliation, leader election, permissions, webhooks, and in-flight operation compatibility. Removing a CRD or finalizer incorrectly can orphan or delete managed data.

### Select and govern operators

An operator is executable domain knowledge with broad authority. Review source and release provenance, supported application/Kubernetes matrix, CRD versioning/conversion, reconciliation idempotency, status/conditions, finalizers, leader election, failure behavior, permissions, network access, backup/restore, upgrade, telemetry, and support.

Prefer explicit desired state and durable operations over imperative hidden scripts. Status should expose observed generation, phase, membership, health, current/target revision, backup, recovery, blocking conditions, and safe next action without secrets.

Controller reconciliation must tolerate restart and duplicate observation. External effects use stable operation identity, idempotency, and reconciliation. Finalizers delay deletion only while a named owner can complete or escalate cleanup; a dead operator must not strand resources indefinitely without a break-glass procedure.

Separate platform installation/upgrade authority from tenant workload requests. Constrain which custom resources and fields users may set; a flexible CR can expose privileged images, storage classes, backups, or network paths.

Canary operator releases against representative data sizes and failure operations. A successful create/delete smoke test is insufficient for membership, recovery, and upgrade safety.

### Bind security to data lifecycle

Authenticate client, member, operator, backup, restore, monitoring, and administrative identities separately. Authorize reads, writes, membership, failover, backup creation/deletion, restore, key use, schema changes, and final deletion.

Use encryption in transit between clients and members and among members. Encrypt volumes, snapshots, backups, and exports at rest under documented key boundaries. Test certificate and key rotation during degraded states.

Minimize privileged containers, host access, kernel capabilities, host networking, and broad API permissions. Some storage/database agents require privilege; isolate, inventory, sign, scan, and audit them rather than declaring a general exception.

Protect administrative and recovery interfaces from normal application credentials. Break-glass access is time-bounded, strongly authenticated, audited, rehearsed, and reviewed.

Data deletion follows all copies and cryptographic dependencies: primary, replicas, removed volumes, snapshots, backups, logs, recovery tests, caches, exports, and support artifacts. Legal retention and deletion exceptions remain explicit.

### Observe correctness, capacity, and recovery

Correlate service/cluster/member IDs, roles, terms/epochs, Pods, nodes, volumes, zones, application/operator revisions, backups, restores, and operations. Avoid sensitive keys/queries or high-cardinality identities in broad labels.

Metrics cover availability by operation, read/write latency/error, quorum/leader changes, membership, replication lag, commit/apply positions, under-replication, conflicts, corruption/checksum, disk capacity/latency/errors, network, compaction, resource pressure, backup age/duration/failure, restore recency/result, certificate/key expiry, and operator reconciliation.

Alert on outcomes: no safe write quorum, stale/expired fence, unavailable shard, data integrity failure, recovery point beyond RPO, projected restore beyond RTO, storage nearly full, rebuild threatening capacity, backup chain/key loss, or retirement blocked.

Controller and CSI metrics explain infrastructure, while application telemetry proves protocol state. A bound PVC and running Pod can coexist with an unreadable filesystem or divergent database.

Record evidence for every maintenance, membership, failover, restore, upgrade, and deletion operation. Logs alone are insufficient durable workflow state.

### Test hazards, not just provisioning

Test bootstrap, restart, duplicate/stale member, node loss, zone loss, network partition, storage detach delay, multi-attach rejection, forced deletion safeguards, corrupt data, disk full, slow IO, certificate expiry, key unavailability, operator crash, control-plane outage, and dependency failure.

Test member add/remove, leadership transfer, scale-out/in, drain, simultaneous fault plus maintenance, rolling upgrade, incompatible version stop, schema migration, rollback boundary, backup, point-in-time restore, total loss, failover, and failback.

Use realistic data scale and workload. A one-gigabyte restore does not validate a ten-terabyte RTO. Include write load during backup, compaction, rebuild, and upgrade.

Verify negative admission: unsupported operators, storage classes, topologies, access modes, versions, privileges, recovery tiers, and deletion policies are rejected with an actionable path.

Conformance is current evidence over application, membership, data, operator, Kubernetes, storage, backup, security, and recovery. Template ancestry and green Pods are insufficient.

### Plan disaster recovery and failback

Define incident declaration authority, data source of truth, recovery region/account, infrastructure dependencies, keys/identity, DNS/traffic, capacity, backup/log transport, consistency check, cutover, communication, and data-loss approval.

Failover can be active-passive, restore-based, or protocol-native multi-site. Each has split-brain risks. Fence the old write authority before promoting the new, or use a protocol that enforces one accepted epoch across sites.

Record the exact recovery point and missing/ambiguous operations. Reconcile downstream effects and communicate data loss rather than hiding it behind service availability.

Failback is another migration. Replicate or export the new authority, validate compatibility and completeness, fence, cut traffic, observe, and retain rollback. Automatically switching back when a region returns can create a second outage or split brain.

Exercise people and technical paths together, including unavailable personnel, provider API limits, key access, and communications. Measure achieved outcomes against RPO/RTO.

### Migrate and retire without orphaning state

Migration inventories source authority, target, schema, identity, data range, replication/copy path, change capture, validation, cutover, dual-write risks, rollback, freeze window, security, cost, and cleanup.

Prefer one authoritative writer at each moment. If dual writes are unavoidable, define conflict resolution, idempotency, ordering, observation, and termination; “keep both in sync” is not a mechanism.

Validate row/object counts, checksums, aggregates, constraints, representative domain queries, access, performance, backup, and recovery on the target before cutover. Continue post-cutover reconciliation through the evidence window.

Retirement stops writes, drains clients/replication, captures required final backup, resolves legal retention, removes membership, fences old instances, revokes credentials and network paths, handles volumes/snapshots/backups/keys, deletes operator custom resources safely, verifies external provider deletion, and removes telemetry last.

Retain a tombstone containing identity, owner, deletion evidence, retained artifacts/policy, final backup disposition, and restoration prohibition or route. Resource absence alone does not prove data erasure.

### Operate standards as a platform portfolio

Catalog supported managed services, operators, application/version profiles, storage classes, topology/recovery tiers, consumers, owners, exceptions, conformance, incidents, costs, and deprecation.

Measure time to safe provisioning, availability and integrity outcomes, backup/restore success, achieved RPO/RTO, maintenance/upgrade reliability, capacity forecast accuracy, operator toil, security exceptions, user effort, and retirement completeness.

Canary standard revisions against platform-owned representative clusters and data. Preserve old operator/runtime/recovery compatibility until consumer migration and retained-backup windows permit removal.

The following executable inventory is synthetic review evidence. It counts declared controls and does not prove consensus safety, failure independence, data integrity, storage durability, backup recoverability, operator correctness, RPO/RTO attainment, security, or production reliability.

<!-- bijux-verify: {"id":"stateful-standard-control-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"profiles 10\nauthority_consistency 10\nmembership_fencing 9\nstorage_topology 9\nhealth_disruption 9\nupgrade_compatibility 8\nbackup_restore 9\nsecurity_observability 9\ndisaster_recovery 8\nretirement_owned 8\n","stderr":""}} -->
```python
profiles = [
    ("managed-relational", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("operator-relational", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("consensus-kv", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("streaming-log", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("search-cluster", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("object-metadata", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("identity-bearing-workers", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("single-volume-service", 1, 1, 1, 1, 1, 1, 1, 0, 1),
    ("legacy-statefulset", 1, 1, 1, 1, 0, 1, 1, 1, 0),
    ("experimental-store", 1, 0, 0, 0, 0, 0, 0, 0, 0),
]
fields = [
    "authority_consistency", "membership_fencing", "storage_topology",
    "health_disruption", "upgrade_compatibility", "backup_restore",
    "security_observability", "disaster_recovery", "retirement_owned",
]
print("profiles", len(profiles))
for index, field in enumerate(fields, start=1):
    print(field, sum(row[index] for row in profiles))
```

## Definitions and Notation

Let stateful contract $S=(A,C,M,R,F,V,T,U,B,O,L)$ contain authority $A$, consistency $C$, membership $M$, replication/quorum $R$, fencing $F$, storage $V$, topology $T$, upgrade/maintenance $U$, backup/recovery $B$, observability $O$, and lifecycle $L$.

For a majority protocol with $n$ voting members, quorum is $q=\lfloor n/2\rfloor+1$ and tolerated unavailable members under the simple model are $f=n-q=\lfloor(n-1)/2\rfloor$. This is a protocol-set result, not a Kubernetes availability guarantee.

Let failure domains $D_1,\ldots,D_k$ contain member sets. A required fault tolerance is feasible only if loss of each in-scope domain leaves a valid quorum and required data/authority dependencies. Pairwise Pod anti-affinity alone does not model storage, network, identity, or control-plane domains.

Let recovery point at incident time $t_i$ be $t_r$; achieved data loss window is $t_i-t_r$. Let service outcome restore at $t_o$ after incident declaration/detection origin $t_0$; achieved recovery time is $t_o-t_0$. Compare both to explicitly defined RPO and RTO origins.

Let incarnation $I=(m,g,e)$ bind logical member $m$, data generation $g$, and fencing epoch $e$. Authoritative writes accept only current valid epochs; Pod name or volume attachment alone cannot establish $e$.

## Mechanisms, Invariants, or Proof Structure

The stateful assurance chain is:

1. identify authoritative state, operation-specific consistency, fault model, RPO/RTO, data lifecycle, and accountable owners;
2. admit a managed service, domain operator, or constrained self-operated profile only when every mandatory contract property has a mechanism and evidence;
3. bind service, cluster, member, data-generation, volume, credential, and fencing identities without conflating Pod lifecycle;
4. establish application-aware bootstrap, membership, replication/quorum, leadership, fencing, placement, and capacity;
5. supply storage whose topology, access, performance, encryption, expansion, snapshot, reclaim, and failure behavior match the protocol;
6. expose role/protocol-aware startup, readiness, liveness, telemetry, disruption, maintenance, and scaling;
7. coordinate compatible application/schema/operator/storage upgrades with explicit asymmetric rollback boundaries;
8. produce isolated, protected recovery artifacts and repeatedly restore them to domain-validated outcomes within measured RPO/RTO;
9. test partial failures, partitions, stale members, corruption, capacity, maintenance, failover/failback, migration, and deletion at realistic scale; and
10. drain authority, remove membership, fence, revoke, retain/delete every data copy and key by policy, verify external cleanup, and preserve retirement evidence.

The majority intersection argument says any two quorums of size greater than $n/2$ overlap in at least one member. It does not prove that overlapping member is correct, durable, up-to-date, independently failed, or enforcing the same membership/term. The platform may use quorum arithmetic for feasibility only alongside protocol and failure evidence.

The invariants are authority-first design, bounded support, separation of controller and protocol, unique fenced incarnation, membership/replica distinction, independent placement, storage-contract fit, tested recovery, role-aware operation, compatibility-controlled change, privileged lifecycle governance, and complete deletion evidence.

## Alternatives and Trade-Offs

**Managed service versus self-operation:** managed offerings transfer much domain toil and may provide mature recovery, but add provider constraints, shared responsibility, cost, and migration risk. Self-operation offers control only with sustained expertise and evidence.

**Domain operator versus generic StatefulSet:** an operator can encode membership, backup, and upgrade while adding privileged code and version coupling. StatefulSet is simpler and portable but intentionally lacks domain lifecycle knowledge.

**Synchronous versus asynchronous replication:** synchronous quorum can reduce acknowledged data loss but increases write latency and partition unavailability. Asynchronous copies improve latency/geo-distance but allow lag and RPO loss.

**Three versus five voters:** three tolerate one failure with lower cost and coordination. Five tolerate two under assumptions but increase latency, operations, and correlated-failure exposure; four often adds cost without another majority failure.

**Network storage versus local storage:** network storage eases reattachment and provider durability but adds network/control dependencies. Local storage offers latency/control but binds recovery to nodes and requires application replication/rebuild.

**Immediate versus delayed volume binding:** immediate provisioning is simple but can choose incompatible topology. Delayed binding follows scheduling at the cost of later provisioning latency and capacity uncertainty.

**Delete versus retain reclaim:** deletion reduces orphan cost and supports erasure but raises accidental-loss risk. Retain protects data and recovery evidence but needs ownership, cost, and eventual deletion.

**Crash-consistent snapshot versus application backup:** snapshots are fast and storage-native but may not capture distributed transaction boundaries. Application backups understand protocols but consume compute and depend on application tooling.

**Frequent full versus incremental/log backup:** full copies simplify restore but cost bandwidth/time. Incremental/log chains improve RPO and efficiency but increase dependency and validation complexity.

**Automatic failover versus manual promotion:** automation reduces outage time but can split brain under ambiguous authority. Human approval can incorporate context but increases RTO and is error-prone unless rehearsed.

**Rolling upgrade versus replace/restore migration:** rolling preserves availability but requires version skew and data compatibility. A new cluster allows clean validation and rollback but duplicates capacity and needs data cutover.

**Strict disruption blocking versus maintenance progress:** conservative blocking protects quorum but can strand infrastructure/security work. Protocol-aware approvals preserve safety while exposing actionable conditions and break-glass authority.

## Failure Modes and Misconceptions

- **“A volume makes the application stateful.”** authority and recovery behavior, not mount presence, determine the archetype.
- **“StatefulSet operates a database.”** it supplies identity/lifecycle mechanics, not the data protocol.
- **“Three replicas tolerate one zone failure.”** only if member and dependency placement make zones independent.
- **“Ready Pods equal quorum.”** readiness may ignore membership, term, lag, shard coverage, or data health.
- **“One replica prevents two writers.”** old and new incarnations can overlap without fencing.
- **“Deleting an uncertain Pod is safe.”** API deletion does not prove the old process stopped.
- **“ReadWriteOnce is a distributed lock.”** its node-scoped mount behavior is not application fencing.
- **“PersistentVolume means durable.”** durability depends on provider, topology, configuration, corruption, and keys.
- **“Replication is backup.”** replicas copy valid and invalid changes and may share the incident domain.
- **“Snapshot means application-consistent.”** distributed and in-flight state may require coordination.
- **“Backup succeeded means recoverable.”** only isolated restore and domain validation establish recovery evidence.
- **“PDB protects availability.”** it covers bounded voluntary eviction behavior, not every failure or rollout.
- **“Ordered rollout is safe.”** order does not prove quorum, compatibility, or completed migration.
- **“Autoscaling voters on CPU is elasticity.”** membership and data transfer require protocol-aware operations.
- **“Scale-down is deleting the last ordinal.”** membership and unique data must be removed first.
- **“Rollback always means old image.”** data/schema changes can make downgrade impossible.
- **“The operator owns everything.”** platform, application, storage, security, backup, and data owners retain duties.
- **“Multi-region means disaster recovery.”** correlated authority, keys, data lag, and split-brain controls determine it.
- **“Deleting a PVC erases data.”** snapshots, backups, retained volumes, replicas, logs, and keys remain.
- **“Green template conformance lasts.”** current data, versions, recovery evidence, and lifecycle state change.

## Worked Examples

### Example 1

A team places three database Pods on three nodes in one zone and claims zone tolerance. Quorum is two, but zone loss removes all three and their zonal volumes. The standard requires one voter and compatible storage per zone plus independent backup/key recovery. Conclusion: node spread does not prove failure-domain independence.

### Example 2

A four-voter majority cluster is proposed to tolerate two failures. $q=\lfloor4/2\rfloor+1=3$, so $f=4-3=1$. Five voters give $q=3$ and $f=2$. Conclusion: even replica counts can add cost without increasing simple majority fault tolerance.

### Example 3

Node A becomes unreachable, but database-0 continues writing to network storage. An operator force-deletes the Pod and database-0 starts on node B, creating two writers. Provider power fencing and storage reservation are required before replacement, while epoch-aware writes reject the stale incarnation. Conclusion: Kubernetes object deletion is not fencing.

### Example 4

Two Pods on the same node mount one `ReadWriteOnce` volume and both start the application. The design assumed cluster-wide exclusivity. It adopts supported `ReadWriteOncePod` plus protocol fencing, because even attachment policy cannot prove a stale external process is harmless. Conclusion: access mode and write authority are separate controls.

### Example 5

A snapshot captures data volume after a transaction log advances but before a second volume receives corresponding pages. Restore fails consistency checks. The operator quiesces or uses application backup at a recorded log position, snapshots coordinated volumes, and validates restore. Conclusion: storage point-in-time does not automatically equal distributed application consistency.

### Example 6

Nightly backups report success for a year. During disaster, the encryption key from nine months ago is unavailable and current binary cannot read the format. Monthly isolated restores across retention would have detected both. Conclusion: backup activity without key/version-aware restore testing is weak evidence.

### Example 7

A PDB allows one unavailable Pod in a three-voter cluster. One zone is already down; a node drain requests another eviction. Static policy permits or blocks based on Pods, while the domain operator sees only two healthy voters and refuses maintenance. Conclusion: live protocol health must govern disruption.

### Example 8

CPU rises, so HPA changes a StatefulSet from three to six. New Pods exist but never join membership; replication saturates disks and leader latency worsens. An operator-driven scale plan adds learners sequentially, verifies topology/catch-up, promotes, and rebalances under capacity limits. Conclusion: replica elasticity is not state elasticity.

### Example 9

A rolling binary upgrade writes a new irreversible data format after the first member. The old version cannot rejoin, so image rollback reduces quorum. The compatibility plan uses dual-readable format, gates writes, validates one member, completes migration, and removes old support only after recovery windows. Conclusion: state makes rollback asymmetric.

### Example 10

Deleting a database custom resource removes Pods, but its finalizer controller is gone. Retained volumes, cloud snapshots, backup objects, DNS, certificates, and a replica in a second region remain. Retirement inventories and resolves every object/provider identity, preserves required recovery evidence, revokes authority, and verifies deletion. Conclusion: declarative parent deletion is not lifecycle completion.

## Cross-Program Connections

- **Distributed systems:** consensus, quorum intersection, membership, leases, fencing, partitions, consistency, replication, and failover define state safety.
- **Databases:** transactions, WAL, MVCC, schema migration, indexes, backup, point-in-time recovery, checksums, and repair supply domain mechanisms.
- **Operating systems:** filesystems, crash consistency, process identity, signals, memory, IO scheduling, and power loss shape recovery.
- **Data structures:** logs, trees, LSM compaction, indexes, Merkle/checksum structures, and sharding determine performance and repair behavior.
- **API engineering:** operation-specific consistency, long-running maintenance status, idempotency, compatibility, and deprecation expose lifecycle safely.
- **Security engineering:** workload/member identity, least privilege, encryption, key custody, backup isolation, audit, and deletion protect persistent data.
- **Reliability engineering:** SLOs, capacity, disruption, recovery tests, RPO/RTO, disaster exercises, and incident command turn infrastructure into outcomes.
- **Systems engineering:** hazard models, independent failure domains, interfaces, assurance cases, maintenance authority, and retirement inventory prevent local overclaims.
- **Data engineering:** change capture, replication lag, backfill, lineage, validation, and retention connect state stores to downstream systems.
- **Economics and governance:** storage growth, replica/backup cost, provider concentration, recovery tiers, residency, legal hold, and deletion allocate long-lived obligations.

## References

1. Kubernetes Authors, “StatefulSets,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
2. Kubernetes Authors, “Persistent Volumes,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/storage/persistent-volumes/
3. Kubernetes Authors, “Storage Classes,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/storage/storage-classes/
4. Kubernetes Authors, “Volume Snapshots,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/storage/volume-snapshots/
5. Kubernetes Authors, “Force Delete StatefulSet Pods,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/tasks/run-application/force-delete-stateful-set-pod/
6. Kubernetes Authors, “Disruptions,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/workloads/pods/disruptions/
7. Kubernetes Authors, “Operator Pattern,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/extend-kubernetes/operator/
8. Kubernetes Authors, “Node Shutdowns,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/cluster-administration/node-shutdown/
9. Diego Ongaro and John Ousterhout, “In Search of an Understandable Consensus Algorithm,” USENIX ATC 2014. https://raft.github.io/raft.pdf
10. Kubernetes SIG Storage, “Volume Snapshot,” CSI external-snapshotter documentation, retrieved 2026-09-02. https://kubernetes-csi.github.io/docs/snapshot-restore-feature.html
11. etcd Authors, “Disaster Recovery,” current documentation, retrieved 2026-09-02. https://etcd.io/docs/v3.6/op-guide/recovery/
12. NIST, “Contingency Planning Guide for Federal Information Systems,” SP 800-34 Revision 1, May 2010. https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
13. CNCF Platforms Working Group, “Platforms White Paper,” April 2023. https://tag-app-delivery.cncf.io/whitepapers/platforms/

## Exercises

### Exercise 1

Define authoritative state, stable member identity, membership, quorum, fencing, failure domain, crash-consistent snapshot, application-consistent backup, RPO, RTO, domain operator, and retirement tombstone. State one adjacent concept each must not be confused with.

### Exercise 2

For three, four, five, six, and seven majority voters, calculate quorum and tolerated member failures. Then place each across three zones and explain why arithmetic alone cannot prove one-zone tolerance, durable writes, or safe membership change.

### Exercise 3

A team runs a five-Pod database in one zone, uses one shared `ReadWriteOnce` volume, force-deletes unreachable Pods, probes a TCP port for health, autos-scales on CPU, snapshots hourly without coordination, never restores, rolls incompatible versions automatically, and deletes PVCs for retirement. Diagnose at least twenty defects and correct them.

### Exercise 4

Design platform admission profiles for managed relational storage, an operator-managed consensus store, independent identity-bearing workers, and an unsupported experimental database. Define contract fields, owners, provider resources, storage/topology, fencing, health, disruption, scale, upgrade, backup/recovery, security, evidence, and escape paths.

### Exercise 5

A region is partitioned during an operator upgrade; the old leader may still write, backup keys were rotated, the recovery region is one schema version behind, one replica is corrupt, and legal hold covers some records. Produce a safe incident, recovery, failover/failback, and eventual retirement sequence.

## Answers to the Exercises

### Answer 1

Authoritative state is the promised source of truth and differs from a derived cache. Stable member identity names a logical replica across process replacement and differs from Pod UID. Membership is the protocol’s accepted member/role set and differs from desired replicas. Quorum is the operation-specific agreeing subset and differs from ready-Pod count. Fencing makes stale actors’ writes reject and differs from merely holding a lease. A failure domain groups correlated failures and differs from a label that has not been validated operationally. A crash-consistent snapshot resembles abrupt-stop storage and differs from a transactionally coordinated backup. An application-consistent backup captures an application recovery boundary and differs from replica storage. RPO bounds acceptable historical data loss and differs from backup frequency alone. RTO bounds restored outcome time and differs from Pod startup. A domain operator encodes application lifecycle knowledge and differs from a generic controller. A retirement tombstone records final identity, evidence, retained obligations, and restoration policy and differs from resource absence.

### Answer 2

For $n=3$, $q=2$ and $f=1$. For $n=4$, $q=3$ and $f=1$. For $n=5$, $q=3$ and $f=2$. For $n=6$, $q=4$ and $f=2$. For $n=7$, $q=4$ and $f=3$. Across three zones, three voters can use 1/1/1 and lose one zone. Four might use 2/1/1; loss of the two-member zone leaves two, below quorum three. Five can use 2/2/1; loss of either two-member zone leaves quorum three. Six at 2/2/2 loses two and retains quorum four. Seven at 3/2/2 loses the three-member zone and retains quorum four. These placements concern voter counts only. Shared storage, network, region, identity, keys, control plane, correlated software, lag, corruption, invalid membership, or non-durable acknowledgements can violate the claimed outcome. Membership changes also require protocol rules such as joint consensus; static intersection arithmetic does not make arbitrary simultaneous reconfiguration safe.

### Answer 3

Five Pods do not prove protocol membership, replication, quorum, or correct roles. One zone defeats zone tolerance. One shared volume creates contention/single failure and may be incompatible with multi-member data layout. `ReadWriteOnce` is node-scoped rather than a universal distributed lock. No stable per-member/data-generation mapping exists. Force deletion does not stop the old process and can create duplicate identity/writers. There is no compute/storage/protocol fencing or epoch. TCP liveness proves only a listener, not startup recovery, membership, quorum, lag, write authority, corruption, or safe read role; aggressive liveness may restart recovery. CPU autoscaling changes Pods without membership/data movement and ignores storage/downstream capacity. Hourly snapshots do not define transaction/application consistency, multi-volume coordination, RPO, isolation, encryption, retention, or independent failure domain. No restore test means completeness, keys, format, scale, RPO, and RTO are unknown. Automatic incompatible rolling risks quorum/version/data-format failure; rollback may be impossible. PVC deletion is not application drain, membership removal, final backup, legal retention, snapshot/replica/key cleanup, or verified erasure. Corrections begin with authority/consistency/fault/recovery specification and admission to a managed service or mature operator. Spread members and storage by failure model; use per-member identity/data, protocol membership, fenced leadership, role-aware health, application-aware disruption/scale, compatible staged upgrades, coordinated protected backups, isolated restore tests, security/telemetry, and inventory-driven retirement with tombstone evidence.

### Answer 4

The common specification contains authority, operation consistency, fault model, RPO/RTO, identity/membership, replication/fencing, storage/topology, health/disruption, capacity/scale, upgrade/schema, backup/restore/DR, security, telemetry, data lifecycle, owner/support, and conformance. Managed relational storage maps to a provider binding: provider owns engine replication/patching under a shared-responsibility contract; platform owns identity/network/policy/telemetry, and data team owns schema/query/recovery acceptance. Operator consensus uses a reviewed pinned operator, CRD, StatefulSet/PVCs/headless discovery, zonal voters, fenced native protocol, role-aware maintenance, and tested backup/restore. Identity-bearing workers may use a generic StatefulSet only when ordinals/claims are independent, no hidden quorum exists, duplicate incarnation is fenced, and each ordinal has recovery/retirement. The experimental database is rejected from production or isolated in an explicitly non-production exception until owners demonstrate membership, corruption recovery, upgrade, security, realistic restore, and support. Each profile exposes supported storage/recovery tiers and prohibits arbitrary privileged fields. Conformance tests creation plus node/zone fault, duplicate identity, maintenance, scale, upgrade, restore, and deletion. Escape routes are managed-provider review, specialist platform, time-bounded experiment, or external ownership—not silent generic YAML.

### Answer 5

Declare an incident, freeze operator upgrade, membership changes, automatic failover, force deletion, and destructive cleanup. Inventory current membership/terms, possible writers, network reachability, storage attachments, data generations, schema/operator versions, corruption scope, backups/logs, key versions, recovery capacity, and legal-hold records. Fence the old region through protocol epoch plus provider compute/storage/network controls before authorizing another writer; if fencing cannot be proven, remain read-only or unavailable rather than create split brain. Isolate the corrupt replica and preserve forensic evidence; choose an authoritative recovery point from healthy quorum or validated backup/log chain. Recover needed historical keys through audited key authority and never rotate/delete the only decrypting version. Provision an isolated recovery cluster with a version combination that can read the backup; if the target region is behind, upgrade it compatibly or restore using the old reader and then migrate. Validate checksums, membership, domain queries, held-record completeness, RPO loss, and performance before promotion. Cut traffic under one new fencing epoch, record lost/ambiguous operations, and reconcile downstream effects. Resume operator migration only after stability and compatibility tests. Failback later as a separate fenced migration from the new authority, not an automatic switch. Apply legal hold to all required primary/backup/evidence copies while deleting non-held residuals by policy. Retirement of the old region removes membership, credentials, volumes, snapshots, operator resources, and keys only after holds, recovery evidence, and deletion approvals are satisfied; retain a tombstone and incident audit.
