---
module_id: DARCH-039
program: Data Architecture Engineering
level: 1
module_number: 39
title: Replication and Synchronization
status: complete
last_verified: 2026-09-03
---

# Replication and Synchronization

## One-Page Review

### Governing question

When should an organization maintain copies of data across systems or locations, and how can it govern consistency, lag, conflict, authority, failover, correction, protection, and retirement without confusing availability of a copy with correctness for a consumer purpose?

### Essential definitions

- **Replication** creates and maintains one or more copies of source data through logs, changes, snapshots, operations, or state transfer.
- **Synchronization** reconciles changes between independently evolving copies according to declared authority, direction, conflict, and convergence rules.
- A **primary-replica** topology directs authoritative writes to one primary and propagates them to read or standby replicas.
- **Multi-primary** replication accepts writes at several authorities and must detect, prevent, serialize, or resolve concurrent conflicts.
- **Synchronous replication** waits for a declared replica acknowledgement before completing a write; **asynchronous replication** completes before remote application and therefore permits lag and loss on failover.
- **Physical replication** reproduces storage or log structures for a compatible engine; **logical replication** transmits logical operations, rows, or products that can be filtered or transformed.
- **Replication lag** is the distance between source commit and replica receipt or application, measured by time, positions, bytes, or transactions under declared boundaries.
- **recovery point objective (RPO)** bounds acceptable data loss in a recovery scenario; **recovery time objective (RTO)** bounds acceptable restoration time. Objectives are requirements, not achieved evidence.
- A **conflict** occurs when changes cannot all be applied while preserving declared invariants or authority.
- **convergence** means replicas eventually reach equivalent declared state after updates and communication stabilize; it does not imply they were always current or correct.
- A **tombstone** communicates deletion through a replicated history; premature removal can resurrect old state.
- **split brain** occurs when participants independently accept incompatible authority, commonly during partition or failed failover coordination.

### Central model, mechanism, or theorem

Represent a replicated product as:

`R = (authority, nodes, topology, scope, mechanism, position, consistency, conflict, service, protection, observability, failover, ownership, correction, lifecycle)`

Replication moves or maintains state; synchronization defines how independently changed state is reconciled. A copy can improve locality, read scale, availability, recovery, or migration, but introduces lag, common defects, conflict, extra attack surface, deletion propagation, and lifecycle cost. Correct design begins with authority and consumer invariants, then selects topology and consistency behavior that can be tested under partition, overload, failover, replay, and resynchronization.

### Critical invariants

- Every replicated assertion has declared source authority, write locations, consumers, purpose, keys, grain, time, schema, and effective interval.
- Acknowledgement semantics state whether data reached memory, durable log, applied state, quorum, region, backup, or consumer-visible service.
- Ordering and position are scoped to source lineage, partition, key, transaction, or replication channel; no global order is inferred casually.
- Reads disclose replica identity, applied position, age or staleness, consistency level, and behavior after a caller's own write where relevant.
- Multi-writer designs define invariants, conflict detection, causality or version evidence, deterministic resolution, audit, and correction.
- Deletes, tombstones, expiry, retention, erasure, schema changes, key changes, resnapshot, and replay cannot silently resurrect or misinterpret state.
- Admission, bandwidth, buffers, checkpoints, fan-out, backpressure, lag, retained logs, and resynchronization protect primary and replica service.
- Failover and failback establish one authorized writer set, fence old authority, validate lineage, reconcile divergence, and preserve rollback evidence.
- Credentials, network links, logs, copies, backups, caches, metadata, conflict records, and providers obey purpose, minimization, residency, retention, deletion, and incident rules.
- Retirement removes channels, slots, accounts, routes, copies, tombstones, alerts, failover procedures, contracts, and consumer dependencies after verification.

### Common failures

Common failures are calling asynchronous replicas strongly consistent; measuring transport receipt while application lags; routing read-after-write traffic to stale replicas; treating RPO and RTO objectives as tested outcomes; assuming replication is backup; accepting multi-primary writes without business conflict rules; resolving by wall-clock last write under unsynchronized clocks; deleting tombstones before offline replicas return; promoting a replica without fencing the former primary; resuming from positions belonging to another lineage; replicating every protected column by default; letting catch-up saturate the primary; comparing row counts without keys and content; and deleting a channel while live copies, credentials, consumers, and failover assumptions remain.

### Compact example

An Account product replicates asynchronously from Stockholm to a reporting region. The contract says the primary owns writes, the replica serves analysis only, ordinary applied lag is under sixty seconds, and read-after-write is not promised. Each response exposes source epoch and applied position. A reconciliation compares keys and canonical content digests, while lag and retained-log headroom protect the primary. Disaster failover requires fencing, promotion authorization, lineage change, consumer routing, and post-recovery reconciliation; the replica is not called a backup.

### Connections

[DARCH-018](018-temporal-and-historical-modeling.md) supplies temporal truth, [DARCH-028](028-cross-domain-dependencies.md) supplies graph reasoning, and [DARCH-036](036-change-data-capture-architecture.md) supplies capture positions and snapshot handoffs. [DARCH-038](038-federation-and-virtualization.md) offers query-time access without a primary durable copy; this module prepares [DARCH-040](../ROADMAP.md) on integration-style choice.

## Governing Question

Replication is often proposed as an uncomplicated way to make data local, scalable, or available. The copy itself is easy to see; the semantics of when it is current, who may write, what happens during partition, and how it is retired are distributed across infrastructure and consumers.

The governing question is not “Can this platform replicate the data?” It is “Which purpose requires a copy, which authority and invariants must it preserve, what divergence is acceptable, and can lag, conflict, failure, protection, correction, and lifecycle be evidenced?”

## Why This Matters

Read replicas protect primaries from analytical load. Regional copies reduce latency. Standbys support recovery. Search indexes and caches provide specialized access. Migrations require old and new systems to coexist. Each benefit comes from a different product contract; calling all of them replication conceals crucial guarantees.

PostgreSQL's [Warm Standby and Streaming Replication](https://www.postgresql.org/docs/current/warm-standby.html) documentation describes log shipping, streaming, standby behavior, and synchronous options for that engine. MySQL's [Replication Implementation](https://dev.mysql.com/doc/refman/8.4/en/replication-implementation.html) describes source binary logging, replica relay logging, and application. Guarantees remain engine-, topology-, and configuration-specific.

Amazon's [Dynamo paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf) describes an always-writable key-value system using techniques including consistent hashing, object versioning, and reconciliation. Ongaro and Ousterhout's [Raft paper](https://raft.github.io/raft.pdf) describes a consensus algorithm for replicated logs. These solve different problems: leaderless availability and consensus replication are not interchangeable labels.

The [CAP result](https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer2.pdf) formalizes limits for consistency and availability under partition in an asynchronous network model. W3C [PROV-O](https://www.w3.org/TR/prov-o/) supplies derivation concepts. Google's [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) informs bounded catch-up and retry, and NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy lifecycle engineering.

## Prerequisites and Retrieval

You should understand transactions, logs, CDC, snapshots, consistency, distributed failure, partitions, quorums, clocks, identities, schemas, data products, service objectives, recovery, privacy, lineage, provenance, and lifecycle.

Retrieve primary, replica, leader, follower, multi-primary, leaderless, physical, logical, synchronous, asynchronous, acknowledgement, commit, position, epoch, lag, staleness, quorum, consistency, causality, conflict, merge, convergence, tombstone, fencing, failover, failback, RPO, RTO, resnapshot, reconciliation, and retirement.

As a retrieval test, inspect “The database is replicated across three regions with zero data loss.” Ask which writes and regions, acknowledgement boundary, quorum, failure scenario, partitions, applied state, source epoch, RPO evidence, write authority, conflict behavior, schema, failover, and consumer read consistency apply. The topology and slogan do not establish the claim.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish replication, synchronization, backup, caching, materialization, CDC, federation, and archival products;
2. model authority, nodes, topology, scope, mechanism, position, consistency, conflict, service, protection, failover, correction, and lifecycle;
3. compare primary-replica, synchronous, asynchronous, multi-primary, leaderless, quorum, physical, and logical designs;
4. define acknowledgement, commit, durability, visibility, read-after-write, monotonic-read, staleness, lag, and convergence boundaries;
5. design snapshot, incremental catch-up, positions, epochs, schema history, deletes, tombstones, and resynchronization;
6. specify conflict prevention, detection, causality, resolution, audit, consumer disclosure, and correction;
7. engineer bandwidth, buffers, fan-out, backpressure, retained logs, catch-up, overload isolation, and source protection;
8. test fencing, promotion, routing, lineage, failback, RPO, RTO, reconciliation, and disaster recovery;
9. protect replicated columns, metadata, links, copies, regions, providers, retention, deletion, and incident evidence;
10. choose replication or alternatives from consumer purpose, invariants, workload, failure, cost, and lifecycle evidence.

## Core Exposition

**Start with purpose.** Read scale, locality, availability, disaster recovery, migration, search, analytics, and partner exchange require different copies and guarantees.

Record consumers, assertions, workload, freshness, consistency, history, failure scenarios, protection, and lifetime. Do not let a platform's replication switch define the product.

**Declare authority.** State which node or domain may create and change each assertion. A primary-replica design has one write authority during an epoch. Multi-primary distributes authority and therefore needs conflict rules.

Authority can vary by field, region, tenant, or key range. Avoid two systems both claiming global ownership while synchronization attempts to guess winners.

**Define replication scope.** Name products, databases, tables, keys, columns, operations, schemas, consumers, filters, and effective interval. Wildcards can expose new protected fields automatically.

Physical replication often copies an engine-level unit. Logical replication can filter or transform but needs stable keys and schema semantics. Match mechanism to scope.

**Distinguish physical and logical copies.** Physical replication reproduces storage or log blocks for compatible engines and is strong for standby fidelity. It couples versions, layouts, and cluster behavior.

Logical replication publishes operations or rows and can support selective products or heterogeneous sinks. It must interpret schema, keys, transactions, and deletes explicitly.

**Define synchronous acknowledgement.** “Synchronous” can mean a remote node received bytes, wrote a log, flushed durable storage, applied state, or made it readable. State the required acknowledgers and timeout behavior.

Waiting reduces loss in covered failures but adds latency and availability dependence. Acknowledgement from one region does not prove all replicas or consumers are current.

**Define asynchronous behavior.** The primary acknowledges before remote durability or application. This improves latency and independence but permits lag and committed-write loss on failover.

Measure sent, received, durable, replayed, and applied positions separately. Communicate which state readers can see and how routing responds to lag.

**Model commit and visibility.** A write can be committed at the authority but not visible on a replica. A log can be durable remotely but not yet applied. Queries may lag behind transport.

Expose suitable applied position or age. Do not use network receipt as consumer freshness evidence. Test long transactions and apply bottlenecks.

**Scope ordering.** One primary log supplies an order for its lineage. Sharding, parallel apply, partitioned logical streams, and multiple writers weaken or divide it.

Promise order only per transaction, key, partition, or source where preserved. Business causality may require explicit versions or dependencies beyond log order.

**Use epochs.** A source or leadership epoch distinguishes one authoritative history from another. Positions are meaningful only with their lineage.

Promotion, restore, resnapshot, and topology change can create new epochs. Reject checkpoints from incompatible history and reconcile rather than resuming by numeric coincidence.

**Define consistency for reads.** Linearizable, serializable, snapshot, read-after-write, monotonic, bounded-staleness, eventual, and best-effort reads serve different needs.

Avoid promising a textbook label without mapping it to actual operations and failure modes. State how callers select consistency and how the system responds when it cannot meet it.

**Provide read-after-write deliberately.** Route a caller to the primary, wait for a replica to reach a returned position, attach a session token, or accept stale behavior under contract.

The consumer must carry enough context. A global load balancer cannot infer which prior write matters. Time delays are weak substitutes for position evidence.

**Provide monotonic reads.** A user moving between replicas can observe state go backward. Session routing or minimum-position tokens can prevent this within a declared scope.

Fail or route elsewhere when no replica meets the minimum. Silently ignoring the token makes the contract false during precisely the failures it was meant to address.

**Measure lag precisely.** Time lag uses clocks and commit timestamps; byte or position lag uses source mechanisms; transaction and record lag add other views.

Record transport and apply lag separately. A small byte gap may contain one critical transaction; a large byte gap may be harmless bulk maintenance. Connect lag to consumer consequence.

**Do not treat staleness as one scalar.** A replica can be current for one partition and stale for another. Derived indexes can apply fields at different times. Clock uncertainty affects age.

Expose source, epoch, applied position, observation time, and product limitations. Use per-key or partition evidence where high consequence requires it.

**Design initial synchronization.** Create a consistent snapshot tied to a log position, load it, then apply later changes without gaps. Large snapshots may require chunks and source protection.

If one snapshot is unavailable, overlap and reconcile explicitly. Validate keys, values, deletes, schema, counts, checksums, and high-risk populations before serving.

**Plan incremental catch-up.** A replica needs retained source history or another peer. Estimate change rate, bandwidth, apply capacity, log headroom, and time to catch up.

If apply capacity is not greater than sustained incoming work, lag cannot close. Rate-limit other workloads or resnapshot. Avoid endless degraded catch-up.

**Protect the primary.** Replication consumes log retention, disk, CPU, network, connections, locks, checkpoints, and operator attention. A stalled consumer can threaten source storage.

Use quotas, retention alarms, maximum-lag policy, isolation, and slot or channel authority. Decide when completeness yields to source survival before incidents.

**Plan fan-out.** Many replicas multiply egress, log retention relationships, credentials, monitoring, schema coordination, and failure recovery.

Use cascading replicas where appropriate, but recognize added lag and dependency. Model blast radius and recovery load. One hub replica can become a bottleneck.

**Bound catch-up and resynchronization.** After outage, replicas compete with live traffic. Backlogs, full copies, index builds, validation, and consumer queries can overload sources and networks.

Use workload classes, rate limits, windows, checkpoints, and reserved live capacity. Test realistic data volumes and skew, not empty replicas.

**Handle deletes.** Replicate hard deletes, soft-delete state, or tombstones with explicit semantics. Consumers need keys, order, retention, and correction.

In eventually connected systems, deleting tombstones too early allows an old replica to reintroduce state. Retention must exceed offline and synchronization assumptions or use stronger version evidence.

**Handle expiry.** Time-to-live can be evaluated at source, replica, or read time. Clock differences and offline nodes affect removal.

Define authoritative expiration time and whether late replicas delete immediately. Preserve records or holds where policy overrides ordinary expiry.

**Handle schema evolution.** Physical replicas often require tightly coordinated engine compatibility. Logical replicas need mappings for add, remove, rename, type, key, and default changes.

Maintain schema history for replay and offline return. Test mixed-version periods, rollback, and resnapshot. Structural success does not prove semantic compatibility.

**Define conflict.** Concurrent writes conflict when they cannot jointly satisfy the data product's invariants or authority. Byte differences are evidence, not the full definition.

Some operations commute; others need serialization or domain review. Declare keys, causal context, invariant scope, and intended outcomes before selecting an algorithm.

**Prevent conflicts where consequence demands it.** Partition authority by region or key, elect one leader, require quorum, or coordinate a transaction. Prevention trades availability, latency, and autonomy.

Do not deploy multi-primary merely for proximity if the domain cannot define merges. Local acceptance creates an obligation to reconcile.

**Detect concurrent versions.** Version vectors, causal metadata, transaction versions, or application tokens can distinguish concurrent from ordered updates under their assumptions.

Wall-clock timestamps alone can misorder changes when clocks skew. A higher timestamp is not proof of later business intent or legitimate authority.

**Resolve conflicts by domain rule.** Options include reject and escalate, authoritative region, field ownership, commutative operation, set union, maximum under invariant, or user choice.

Last-write-wins is a rule, not neutrality. Record lost alternatives, policy version, reason, actor, and correction path. Preserve audit where consequence warrants.

**Treat convergence as bounded.** Eventual convergence assumes updates and partitions stop long enough, messages remain available, replicas execute compatible merge rules, and tombstones persist.

State these conditions. Equivalent bytes can still be semantically wrong if a shared defect replicated everywhere.

**Separate replication from backup.** Online replicas rapidly copy accidental deletion, corruption, malicious changes, and schema mistakes. They may share credentials and failure domains.

Backups need independent retention, version history, restore evidence, protection, and recovery objectives. Replication can support availability but does not replace restore testing.

**Design reconciliation.** Compare population, keys, versions, canonical content digests, deletes, schema, counts, aggregates, and high-risk values. Use source authority and time boundaries.

Row counts alone hide missing, extra, and mismatched records. Sampled reconciliation has uncertainty. Define thresholds, complete checks where feasible, and correction ownership.

**Correct divergence.** Determine authoritative state, affected keys and intervals, cause, consumers, and downstream effects. Repair through versioned changes or resnapshot with evidence.

Do not silently overwrite if completed decisions or audit require both histories. Notify consumers and restate derived products.

**Design failover.** Detect failure, establish authorized decision, fence the old writer, select a sufficiently current replica, promote under a new epoch, route clients, validate service, and communicate data risk.

Automation reduces time but can automate split brain. Use leases, quorum, fencing tokens, or external coordination appropriate to the system. Test partitions, not only clean shutdown.

**Design failback.** The old primary's history may diverge. Rejoin it as a fresh replica, reconcile, or explicitly merge; never assume reverse replication is safe.

Validate schema, positions, epochs, credentials, routing, and consumer sessions. Failback is another migration with rollback and observation.

**Define RPO and RTO by scenario.** A regional loss, accidental deletion, logical corruption, credential compromise, and total provider outage have different recoverable states and times.

Objectives state acceptable bounds. Exercises and incidents provide achieved evidence. Report uncertainty and dependencies rather than claiming zero loss from configuration alone.

**Protect every copy.** Replication expands access, linkability, jurisdiction, providers, storage, backups, logs, caches, and incident scope. Apply purpose and minimization before copying.

Authorize publishers, channels, replicas, readers, and administration separately. Encrypt, segment, rotate identities, audit access, and govern support access.

**Govern residency.** Failover and follower reads can move data or processing across regions. Map normal, recovery, backup, and support paths.

A technically available replica may be impermissible for one product. Enforce route and storage policy by classification and purpose.

**Propagate deletion and legal exceptions.** Erasure requests need source authority, replica application evidence, derived-copy notifications, and conflict with records or holds resolved accountably.

Offline replicas and backups complicate deletion. Document restoration controls so expired data is not reintroduced without reapplying deletion history.

**Observe the topology.** Track source and replica epochs, roles, positions, transport and apply lag, retained logs, bandwidth, queue depth, conflicts, tombstones, schema versions, errors, retries, failovers, and reconciliation.

Connect infrastructure metrics to product freshness and consumer outcomes. Monitor missing telemetry and false healthy states caused by stalled positions.

**Maintain provenance.** Relate copies and derived products to source, epoch, position, snapshot, replication mechanism, transformations, schema, and executions.

Provenance supports correction and audit. It does not prove the source assertion or replicated copy is correct. Pair with quality and reconciliation evidence.

**Assign ownership.** Product owners define authority, consistency, conflict, correction, and consumer contract. Database or platform teams operate replication. Security, privacy, records, and recovery owners govern their controls.

Name promotion authority, fencing responsibility, maximum-lag decisions, conflict review, resnapshot, communication, and retirement. Shared ownership must not mean absent ownership.

**Choose replication for a purpose.** Use it for local reads, standby recovery, compatible search or analytical copies, migrations, and bounded partner distribution when copy semantics fit.

Avoid it when consumers need flexible federation without durable copies, business events rather than mutations, or derived facts that deserve a governed product.

**Plan migration.** Inventory authorities, writers, readers, copies, channels, schemas, positions, workloads, conflicts, protection, and unknown use. Establish snapshots, epochs, checkpoints, and reconciliation.

Run old and new paths with one named authority. Compare keys, values, deletes, order, time, lag, schema, protection, and consumer decisions. Test failover and rollback.

**Retire completely.** Stop channels and writes; drop slots safely; revoke identities and network rules; remove replicas, caches, logs, tombstones, backups under policy, alerts, routes, docs, and failover procedures.

Update catalogs and lineage. Preserve required evidence, holds, and correction capability. Verify consumers and source resource release.

**Measure value.** Track consumer latency and freshness, lag distribution, source load, read offload, conflicts, divergence, reconciliation, retained-log margin, failover RPO and RTO evidence, incidents, cost, protection exceptions, and closure.

Replica count is not value. Success means appropriate copies provide intended service while authority, divergence, risk, and lifecycle remain controlled.

## Definitions and Notation

Represent replicated product $R=(A,N,T,S,M,P,C,F,Q,Z,O,D,L)$, where $A$ is authority, $N$ nodes, $T$ topology, $S$ scope and schema, $M$ mechanism, $P$ positions and epochs, $C$ consistency, $F$ conflict and convergence, $Q$ service and capacity, $Z$ protection, $O$ observability and ownership, $D$ disaster recovery and correction, and $L$ lifecycle.

For one source epoch, let committed source position be $p_s$, replica durable position $p_d$, and applied position $p_a$, with $p_a\leq p_d\leq p_s$ under comparable order. The position gaps do not directly equal time, records, bytes, or business impact.

Let time-based applied lag be $L_a=t_{observe}-t_{commit(p_a)}$ under compatible clocks and available commit evidence. A small $L_a$ for the latest applied record does not prove every prior key is correct or all partitions are equally current.

For source and replica mappings $S(k)$ and $R(k)$ over a declared key population, reconciliation partitions keys into missing, unexpected, matching, and mismatched sets. Canonical comparison must define schema, normalization, time boundary, and digest collision assumptions.

Define `JustifiedReplication(R,t)` as a review predicate requiring a copy purpose, explicit authority and consistency, bounded lag and source risk, governed conflicts, tested failure and recovery, effective protection, observable consumer fitness, reconciled state, compared alternatives, and funded lifecycle at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for every material replicated product.

**1. Purpose gate.** Define consumers, copy purpose, assertions, workload, freshness, consistency, availability, recovery, protection, lifetime, and alternatives.

**2. Authority gate.** Assign writers, key or field ownership, epochs, fencing, conflicts, business invariants, consumer use, and correction.

**3. Mechanism gate.** Specify physical or logical scope, logs, snapshots, checkpoints, channels, keys, schemas, filters, positions, and compatibility.

**4. Consistency gate.** Define acknowledgement, durability, application, visibility, ordering, read-after-write, monotonic reads, staleness, lag, and convergence conditions.

**5. Conflict gate.** Establish prevention, causal evidence, detection, resolution, lost alternatives, audit, consumer disclosure, and correction.

**6. Capacity gate.** Model change rate, fan-out, bytes, bandwidth, buffers, retained logs, apply capacity, backpressure, catch-up, resnapshot, source protection, and cost.

**7. Protection gate.** Apply purpose, minimization, identity, access, encryption, regions, providers, copies, backups, retention, deletion, records, audit, and incidents.

**8. Recovery gate.** Test partitions, fencing, promotion, routing, new epochs, RPO, RTO, failback, divergence, reconciliation, rollback, and communication.

**9. Evidence gate.** Observe roles, epochs, positions, lag, retained logs, conflicts, tombstones, schemas, failures, consumer freshness, provenance, quality, and reconciliation.

**10. Lifecycle gate.** Discover, authorize, snapshot, replicate, reconcile, correct, fail over, resynchronize, migrate, revoke, remove, archive, retire, and verify closure.

The executable example reconciles keyed canonical content between a source and replica.

<!-- bijux-verify: {"id":"replica-keyed-reconciliation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"source_keys=3\nreplica_keys=3\nmatching_keys=101\nmissing_keys=103\nunexpected_keys=104\nmismatched_keys=102\nreplica_equivalent=false\n","stderr":""}} -->
```python
source = {101: "d-a1", 102: "d-b2", 103: "d-c3"}
replica = {101: "d-a1", 102: "d-old", 104: "d-d4"}

shared = source.keys() & replica.keys()
matching = sorted(key for key in shared if source[key] == replica[key])
mismatched = sorted(key for key in shared if source[key] != replica[key])
missing = sorted(source.keys() - replica.keys())
unexpected = sorted(replica.keys() - source.keys())

print(f"source_keys={len(source)}")
print(f"replica_keys={len(replica)}")
print(f"matching_keys={','.join(str(key) for key in matching) or 'none'}")
print(f"missing_keys={','.join(str(key) for key in missing) or 'none'}")
print(f"unexpected_keys={','.join(str(key) for key in unexpected) or 'none'}")
print(f"mismatched_keys={','.join(str(key) for key in mismatched) or 'none'}")
print(f"replica_equivalent={str(source == replica).lower()}")
```

The example proves only inequality between two small keyed digest maps: key 101 matches, 103 is missing, 104 is unexpected, and 102 differs. It does not prove source authority, digest correctness or collision resistance, schema and time equivalence, delete meaning, complete population, replication ordering, or safe repair. Production reconciliation needs governed canonicalization, source boundaries, protected evidence, and accountable correction.

## Alternatives and Trade-Offs

**Synchronous versus asynchronous replication.** Synchronous acknowledgement reduces covered failover loss but adds latency and dependency. Asynchronous replication improves write availability while permitting lag and loss.

**Physical versus logical replication.** Physical copies provide engine fidelity and standby behavior but couple technology. Logical copies enable filtering and heterogeneity while adding schema and key interpretation.

**Single-primary versus multi-primary.** Single authority simplifies ordering and conflict. Multiple writers improve locality or partition availability while demanding domain-aware reconciliation.

**Leader-based versus leaderless.** Leaders serialize writes within scope. Leaderless quorum approaches accept broader writes and reconcile versions, with different latency and availability trade-offs.

**Direct replicas versus cascading topology.** Direct connections reduce path lag but increase primary fan-out. Cascades offload the primary while adding dependency and recovery layers.

**Replica versus cache.** Replicas follow source state broadly and may expose query capability. Caches hold selected results with eviction and invalidation semantics.

**Replication versus federation.** Replication improves local service through copies and synchronization. Federation queries sources at runtime and avoids intended durable copies while adding dependencies and source load.

**Replication versus backup.** Replication supports continuity and locality; independent versioned backups support recovery from propagated corruption or deletion. Responsible systems often need both.

**Automatic conflict resolution versus manual review.** Deterministic rules scale for understood commutative or precedence cases. Material conflicts may require human authority and slower correction.

**Long tombstone retention versus compact history.** Long retention prevents resurrection from offline replicas but costs storage and exposure. Compact histories require bounded offline time or stronger version mechanisms.

## Failure Modes and Misconceptions

1. **A replica is just another copy.** It has authority, consistency, failure, protection, and lifecycle semantics.
2. **Synchronous means all replicas applied.** Acknowledgement scope must be named.
3. **Asynchronous replication is eventually consistent under any condition.** Convergence assumptions can fail.
4. **Transport lag equals query freshness.** Apply and consumer layers remain.
5. **One lag number describes all data.** Partitions and keys can differ.
6. **Positions compare across failover histories.** Epoch and lineage are required.
7. **Read replicas provide read-after-write.** Routing or minimum-position mechanisms are needed.
8. **Last timestamp wins is neutral.** Clocks, authority, and lost intent make it a business rule.
9. **Equal row counts prove equivalence.** Missing, extra, and mismatched keys can cancel.
10. **Convergence proves correctness.** All replicas can converge on a propagated error.
11. **Replication is backup.** Corruption and deletion replicate quickly.
12. **More replicas always improve availability.** Quorum, coordination, dependencies, and recovery load can worsen.
13. **Stopping a lagging replica protects the primary.** Retained logs may grow until the slot is resolved.
14. **Failover is only a routing change.** Fencing, lineage, loss, promotion, and reconciliation matter.
15. **Failback simply reverses the channel.** Histories may diverge.
16. **Source deletion removes every copy.** Offline replicas, backups, caches, and exports persist.
17. **Dropping the channel retires replication.** Copies, consumers, credentials, and recovery assumptions remain.

## Worked Examples

### Example 1

A synchronous standby acknowledges after durable log flush but applies changes five seconds later. Failover loss is bounded for acknowledged writes, yet standby queries can still be stale. **Conclusion:** durability acknowledgement and read visibility are distinct.

### Example 2

A user writes an address then reads from a random replica that has not applied the returned position. A session token routes the read to a sufficiently advanced node or primary. **Conclusion:** read-after-write requires context and enforcement.

### Example 3

Two replicas have three rows each. Reconciliation finds one match, one missing, one unexpected, and one mismatched shared key. **Conclusion:** equal row counts cannot establish equivalent state.

### Example 4

Two regions update credit status during partition. Wall clocks differ by ninety seconds, so last-write-wins selects the older business decision. A single credit authority or versioned domain review replaces timestamp arbitration. **Conclusion:** conflict resolution embodies business policy.

### Example 5

An offline replica returns after tombstones expired and reintroduces deleted profiles. A bounded offline period plus retained causal deletion evidence prevents resurrection. **Conclusion:** deletion retention participates in convergence correctness.

### Example 6

A replica applies 80 MB/s while the primary generates 100 MB/s. Lag grows even with perfect network throughput. The team isolates bulk writes or resnapshots after provisioning greater apply capacity. **Conclusion:** catch-up requires sustainable capacity above incoming work.

### Example 7

A region fails and automation promotes a replica, but the old primary still accepts writes through a network path. Fencing tokens and quorum-based promotion stop split brain. **Conclusion:** promotion without authority revocation is unsafe.

### Example 8

All live replicas immediately reproduce an accidental table deletion. A separately retained, access-isolated backup restores prior state and deletion history supports correction. **Conclusion:** replicated availability and recoverability from logical error are different capabilities.

### Example 9

A protected field is added to a wildcard logical publication and appears in another jurisdiction. Column allowlists and schema-protection review block it. **Conclusion:** schema evolution can silently expand replicated purpose and residency scope.

### Example 10

After migration, the channel is stopped but a reporting team still reads the old replica and disaster procedures assume it can be promoted. Retirement migrates the consumer, revokes access, removes the copy and failover path, and updates evidence. **Conclusion:** technical disconnection is not lifecycle closure.

## Cross-Program Connections

- **Distributed systems:** consensus, quorums, partitions, causality, clocks, consistency, convergence, split brain, and failure detectors shape replication.
- **Database engineering:** logs, transactions, snapshots, standbys, isolation, schemas, keys, recovery, and backups implement core mechanisms.
- **Data engineering:** CDC, streams, checkpoints, materialized views, reconciliation, backfills, lineage, and serving build logical replicas.
- **Platform engineering:** topology, identity, automation, observability, capacity, failover, providers, and self-service sustain shared capability.
- **Cybersecurity and privacy:** copy proliferation, residency, purpose, access, tombstones, backups, deletion, support, and incidents constrain topology.
- **Software architecture:** authority, aggregates, conflicts, ownership, bounded contexts, caches, migrations, and anti-corruption layers locate semantics.
- **Reliability engineering:** RPO, RTO, lag, fault injection, fencing, disaster exercises, reconciliation, and recovery evidence verify claims.
- **Systems engineering:** trade studies, interface contracts, fault trees, configuration, assurance, verification, and lifecycle govern the whole replicated system.

## References

1. PostgreSQL Global Development Group, *Warm Standby and Streaming Replication*, PostgreSQL Documentation. <https://www.postgresql.org/docs/current/warm-standby.html>
2. Oracle, *Replication Implementation*, MySQL 8.4 Reference Manual. <https://dev.mysql.com/doc/refman/8.4/en/replication-implementation.html>
3. DeCandia, G., et al., *Dynamo: Amazon's Highly Available Key-value Store*, SOSP, 2007. <https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf>
4. Ongaro, D., and Ousterhout, J., *In Search of an Understandable Consensus Algorithm*, USENIX ATC, 2014. <https://raft.github.io/raft.pdf>
5. Gilbert, S., and Lynch, N., *Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services*, 2002. <https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer2.pdf>
6. W3C, *PROV-O: The PROV Ontology*, W3C Recommendation, 2013. <https://www.w3.org/TR/prov-o/>
7. Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds., *Site Reliability Engineering: Addressing Cascading Failures*, Google, 2016. <https://sre.google/sre-book/addressing-cascading-failures/>
8. NIST, *Systems Security Engineering: Considerations for a Multidisciplinary Approach in the Engineering of Trustworthy Secure Systems*, SP 800-160 Volume 1 Revision 1, 2022. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Define a complete regional read-replica product, including authority, scope, acknowledgement, consistency, lag, service, protection, failover, ownership, and lifecycle.

### Exercise 2

Design keyed reconciliation for two replicas with millions of records. Include canonicalization, time boundary, digests, partitions, mismatches, confidence, and correction.

### Exercise 3

Design a safe failover and failback procedure for asynchronous primary-replica replication. Include fencing, RPO, epochs, routing, reconciliation, rollback, and communication.

### Exercise 4

Compare single-primary, synchronous regional standby, asynchronous read replicas, and multi-primary synchronization for an Account product with financial invariants.

### Exercise 5

Plan retirement of a replicated legacy database used by unknown reports, a search index, disaster recovery, and an external partner. Include discovery, migration, protection, and closure.

## Answers to the Exercises

### Answer 1

Name the source-aligned product, authoritative primary and epoch, permitted writers, replicated tables and columns, keys, grain, schemas, consumers, purposes, and regions. Define whether the replica is physical or logical, initial snapshot and position, transport, durability and apply acknowledgements, ordering scope, deletes, schema evolution, and resynchronization. State read consistency, read-after-write exclusion or token behavior, ordinary and maximum lag, stale response labeling, and source protection.

Service covers availability, latency, freshness, completeness, capacity, recovery, correction, support, and consumer-visible applied state. Protection covers minimization, identities, channel, encryption, storage, backups, region, providers, retention, deletion, audit, and incidents. Failover names detection, decision authority, fencing, eligible positions, promotion, new epoch, routing, RPO and RTO evidence, reconciliation, and failback. Product, database, platform, security, and consumer responsibilities are explicit. Lifecycle includes schema changes, consumer migration, channel and slot removal, access revocation, copy disposition, catalog and lineage updates, evidence retention, and verified closure.

### Answer 2

Choose one authoritative product boundary and comparison time or source position. Define stable key namespaces, included population, schema versions, nulls, types, units, normalization, field ordering, encoding, and excluded volatile metadata. Partition keys deterministically so each partition can be retried. Compare key sets first to find missing and unexpected records. Compute canonical content digests for shared keys, then inspect mismatches using protected field-level comparison. Compare delete or tombstone state separately.

Validate digest algorithm and collision assumption; a digest mismatch proves different canonical bytes, while a match gives bounded probabilistic evidence rather than semantic truth. Reconcile counts and aggregates as supporting evidence. Record source and replica epochs, positions, extraction times, schema, query, code version, and incomplete partitions. Use complete comparison for high-consequence populations or state sampling confidence and blind spots. Route discrepancies to source, replication, or semantic owners. Repair through versioned changes or resnapshot, re-run comparison, notify affected consumers, and preserve evidence under access and retention rules.

### Answer 3

Detect failure using several signals and obtain authorized promotion decision. Record primary epoch and last known committed, durable, and applied positions. Fence the old primary through quorum, lease, storage fencing, network isolation, or another tested mechanism before enabling writes elsewhere. Select an eligible replica based on position, integrity, protection, and service. Promote under a new epoch, update routing and identity, validate writes and reads, disclose potential loss from asynchronous lag, and monitor consumers.

Compare acknowledged source history with promoted state to establish achieved RPO; communicate affected intervals and correction. Preserve rollback only if it cannot recreate two writers. When the old site returns, treat its history as divergent. Rebuild it from the new authority or reconcile explicitly, then join it as a replica. Test schema, keys, tombstones, positions, consumer sessions, and protection. Failback repeats fenced promotion and new-epoch control; it is not channel reversal. Measure achieved RTO, preserve incident evidence, correct downstream products, and review automation gaps.

### Answer 4

Financial account invariants favor one write authority per account or transaction scope. A single primary gives clear ordering and conflict prevention but creates latency and availability dependency. A synchronous regional standby can reduce acknowledged-loss risk if acknowledgement means durable remote log, at the cost of write latency and regional dependency; applied reads may still lag. Asynchronous read replicas suit reporting and locality where staleness is disclosed and read-after-write is not assumed.

Unrestricted multi-primary is dangerous when concurrent debit, limit, or status changes cannot merge safely. If regional write availability is essential, partition authority by account or use a consensus/quorum design for invariant scope, with fencing and causal evidence. Do not use wall-clock last-write-wins for balances. Keep independent backups for logical corruption. Compare failure scenarios, latency, availability, RPO, RTO, capacity, conflict, consumer service, protection, operating maturity, and cost. Architecture can mix synchronous standby for recovery with asynchronous read replicas for analytics.

### Answer 5

Assign stable replica, channel, slot, account, consumer, report, index, partner, and failover identifiers. Discover use from query and access logs, grants, network records, schedulers, BI tools, code, partner contracts, catalogs, lineage, alerts, recovery plans, incidents, and interviews. Record purpose, fields, keys, workload, consistency, freshness, protection, retention, owner, and observed confidence. Monitor unknown reports and communicate before irreversible action.

Move reports to a governed analytical product or replacement replica, rebuild the search index from a source contract with comparison, establish a tested replacement disaster-recovery capability, and version the partner exchange with acknowledgement. Run parallel paths and compare keys, values, deletes, schemas, time, lag, service, protection, search behavior, reports, and partner outcomes. Define rollback and correction. After acceptance, stop writes and channels, drop slots safely, revoke identities and network rules, remove copies, caches, indexes, backups under policy, alerts, routing, docs, and promotion procedures, update catalogs and lineage, preserve required evidence and holds, and verify both access and source resource use have ceased.
