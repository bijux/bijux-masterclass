---
module_id: LSDS-002
program: Large-Scale Data Systems Engineering
level: 1
module_number: 2
title: Horizontal Partitioning
status: complete
last_verified: 2026-08-29
---

# Horizontal Partitioning

## One-Page Review

### Governing question

How can a logical dataset be divided into independently placeable horizontal partitions while preserving coverage, identity, routing, correctness, and operability?

### Essential definitions

- **Horizontal partitioning** assigns whole records or keyed state units to logical subsets with the same schema.
- A **partition key** supplies values used by a partition function; it need not be a unique record key.
- A **partition function** maps an eligible record or key to one or more logical partition identifiers.
- A **logical partition** is a stable data/work unit; a **placement** maps it to workers or storage nodes.
- **Partition pruning** avoids partitions proven unable to contain relevant records.
- **Co-location** places data frequently processed together in the same partition or placement boundary.
- **Skew** is uneven data volume or work; a **hot partition** exceeds a resource or service objective.
- **Repartitioning** changes assignment while preserving data and request semantics through a declared transition.

### Central model, mechanism, or theorem

Let dataset `D` be partitioned into `P_0,...,P_{n-1}` by assignment `a(x)`. For an exclusive primary partitioning:

`union_i P_i = D` and `P_i intersect P_j = empty` for `i != j`.

If replication is present, distinguish one primary logical assignment from physical copies. Correctness additionally requires deterministic routing for the active map version, stable record identity, defined handling of invalid/missing keys, and an atomic or versioned ownership transition during movement.

### Critical invariants

- Every eligible record belongs to the declared partition universe.
- A record has exactly one primary logical owner unless overlap is explicitly modeled.
- Routing and storage use the same partition-map version.
- Partition identity is separate from current machine placement.
- Co-located operations use compatible keys and identical canonicalization.
- Global operations name their shuffle, broadcast, coordination, or merge cost.
- Repartitioning prevents lost, duplicated, or multiply applied writes.
- Balance is measured by work, bytes, rate, state, and tails—not partition count alone.

### Common failures

Frequent failures are partitioning before defining access patterns, confusing a partition with a server, assuming even keys mean even work, ignoring null or malformed keys, using mutable attributes as keys, co-locating one workflow while scattering another, creating too few or too many partitions, pruning without proof, changing maps without versioned routing, and treating replicas as extra logical records.

### Compact example

Orders are partitioned by `customer_id` so one customer's history is local. Coverage and exclusivity hold, but a wholesale customer creates a hot partition and queries by warehouse scatter. The key improves one access pattern while harming others; secondary organization, salting, hierarchical keys, or a different boundary may be required.

### Connections

[LSDS-001](001-workloads-that-require-multiple-machines.md) establishes when distribution is justified. [LSDS-003](../ROADMAP.md) compares range, hash, and consistent mechanisms. Partition semantics connect to [Database Engineering](../../18-database-engineering/ROADMAP.md) and failure/ownership transitions to [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md).

## Governing Question

Adding machines provides aggregate resources only when data and work can be divided. Horizontal partitioning is the foundational division: retain a common logical schema and assign different records, keys, or state units to logical partitions. Each partition can then be stored, scanned, scheduled, recovered, or moved with bounded independence.

The hard part is not computing `hash(key) mod n`. It is choosing the unit whose identity, access, transactions, locality, growth, skew, and movement can be governed. A partition function that distributes rows evenly can scatter every important join. A key that co-locates transactions can concentrate a large tenant. A correct static mapping can fail during reconfiguration if routers and owners disagree.

DeWitt and Gray's [parallel database survey](https://www.microsoft.com/en-us/research/publication/parallel-database-systems-the-future-of-database-processing-or-a-passing-fad/) describes shared-nothing systems whose relation tuples are declustered across processors for parallel scans and dataflow. Modern systems add elastic placement, replication, online movement, and heterogeneous workloads, but the core obligation remains: define a logical decomposition whose parallel benefit exceeds its movement and coordination cost.

## Why This Matters

Partitioning determines the natural unit of parallelism. A scan can run one task per partition. A keyed aggregation can be local when all equal keys meet in one partition. Failure recovery can reconstruct or reassign bounded units. Capacity can grow by adding placements. These benefits arise from the partition contract, not merely from multiple files.

The same boundary determines distributed cost. A join on the partition key can be local; another join may require moving an entire input. A transaction within one partition can use a local protocol; a cross-partition transaction needs coordination or different semantics. A point lookup can route directly only when the request contains derivable key information.

Skew makes averages deceptive. One partition may contain more bytes, receive a celebrity key's traffic, retain a long window of state, or execute expensive values. Stage completion and p99 service follow the busiest required partition. Balance must be evaluated for each workload dimension and over time.

Partitioning also creates a durable compatibility surface. Producers and consumers may encode keys differently, changing case, Unicode normalization, timezone, sign, or missing-value treatment. If their partition calculations diverge, related records separate or requests route incorrectly. Canonicalization is part of the schema contract.

Finally, partitions move. Nodes fail, capacity grows, hot units split, tenants migrate, and placement policies change. A design that explains only the steady-state map is incomplete. Movement must define read and write authority, map versions, transfer snapshot, concurrent changes, validation, cutover, rollback, and cleanup.

## Prerequisites and Retrieval

You should understand sets, functions, keys, records, joins, aggregation, concurrency, replication, and basic distributed failure. Recall from [LSDS-001](001-workloads-that-require-multiple-machines.md) that multiple machines are justified by measured constraints and that skew and movement reduce ideal scale.

Distinguish horizontal partitioning from vertical partitioning. Horizontal partitioning divides records under a common schema. Vertical partitioning divides fields or components and requires an identity to reconstruct them. This chapter also distinguishes logical ownership from replica placement; replication is developed elsewhere.

## Learning Objectives

After completing this module, you should be able to:

- define horizontal partitioning with coverage and exclusivity invariants;
- distinguish record identity, partition key, logical partition, replica, and node;
- derive routing and pruning behavior from a partition map;
- choose keys from access, transaction, locality, and growth evidence;
- quantify data, request, state, and computational skew;
- identify local, broadcast, and repartitioned operations;
- design missing-key, oversize-key, and mutable-key policies;
- explain versioned online repartitioning and its failure boundaries;
- validate a partitioner independently over representative/adversarial data;
- scope human review for high-consequence partition transitions.

## Core Exposition

Let `D` be a logical dataset of records sharing schema `S`. Horizontal partitioning defines a finite logical partition set `L` and assignment `a : D -> L` for exclusive primary ownership. Partition `P_l = {x in D | a(x)=l}`. Coverage follows because `a` is total; exclusivity follows because it returns one primary identifier.

Totality is a design obligation. The key may be missing, malformed, outside a declared domain, or unavailable at ingest. Policies include rejecting/quarantining the record, assigning a governed fallback partition, or deriving another key. Silently using a runtime-dependent hash or random worker makes replay and routing unstable.

The **record key** identifies a record or entity under a namespace. The **partition key** chooses locality and may be shared by many records. The **partition identifier** names a logical unit. The **node identifier** names current placement. Conflating them makes movement appear to change data identity and binds clients to infrastructure.

Partition maps add indirection: `a(x)` selects a logical partition, while placement map `m_v(l)` under version `v` selects owners or replicas. This allows partitions to move without changing record keys. Routers need an authoritative map version, refresh protocol, stale-route behavior, and bounded redirects or retries.

The best key depends on dominant operations. A customer key co-locates history, customer-scoped aggregates, and perhaps transactions. A time key prunes temporal scans but concentrates current writes. A tenant key simplifies isolation and movement but makes a very large tenant indivisible. Composite or hierarchical keys can express several dimensions, with corresponding routing and balance consequences.

Co-partitioned datasets use compatible key domains, canonicalization, partition functions, and map boundaries so matching records meet locally. Same partition count is insufficient. If one input lowercases account IDs and another does not, or their range boundaries differ, a join still needs correction or shuffle.

Partitioning enables pruning only when a predicate proves which partitions may match. An equality predicate with the full partition key may route to one partition. A range predicate can prune range-partitioned data when boundaries are known. A predicate on an unrelated attribute usually fans out. Incorrect pruning loses results and is a correctness defect, not a performance approximation.

Operations fall into communication shapes. A **local/narrow** operation consumes each input partition independently. A **broadcast** operation copies a small input to relevant partitions. A **shuffle/repartition** operation moves records so a new key groups them. A global order, exact distinct, non-aligned join, or repartitioned aggregation can require wide movement and merge stages.

Partition count controls granularity. Too few partitions cap parallelism and make movement/coarse failures expensive. Too many create metadata, scheduling, open-file, small-object, and coordination overhead. Logical partitions can outnumber workers so placement changes without rewriting the partition function, but the chosen count must fit metadata and task economics.

Balance is vector-valued. For partition `l` measure bytes `B_l`, record count `N_l`, request rate `R_l`, state `S_l`, computation `C_l`, and observed latency. Useful diagnostics include maximum-to-mean ratio, percentiles across partitions, coefficient of variation, and contribution of the heaviest keys. A single “balanced” label is meaningless without dimension and window.

Key popularity often has a long tail. Salting a hot key spreads work by adding a bucket component, but later aggregation must combine buckets and key-scoped transactions lose single-partition locality. Splitting an oversize tenant may be necessary; design the secondary boundary and consumer semantics rather than hiding it inside an undocumented exception.

Changing a partition key is a data migration and compatibility change. Historical records must be reassigned, downstream layouts and state stores may need rebuild, consumers may retain old assumptions, and checkpoints may encode partition identity. An apparently internal repartition can change ordering, transaction boundaries, and recovery cost.

Online movement separates data copy from authority. One safe family of protocols records a source snapshot, copies it, captures concurrent changes, validates destination state, changes versioned routing/ownership, drains stale requests, then retires the source. Other protocols use dual reads/writes or forwarding. Each must define duplicate, conflict, retry, failure, and rollback behavior.

Replication modifies physical membership but should not obscure primary logical assignment. A record with three copies is still one logical record. Reads can choose a replica under consistency policy; writes and repairs follow ownership/replication protocols. This chapter uses one primary logical partition to reason about coverage, while later modules own replica correctness.

The word **shard** is often used for a horizontally partitioned unit, but product documentation varies: it may mean a logical key range, a replication group, a physical database, or a tenant boundary. Architecture and incident records should use the system's exact definition and separately record logical partition, replica group, and placement. Otherwise “move a shard” cannot say whether ownership, replicas, routing, or only bytes changed.

Partition metadata is control-plane state. It can contain boundaries, map epochs, leaders/owners, replica locations, lifecycle status, and split ancestry. Losing or inconsistently updating that metadata can make intact data unreachable or multiply writable. Protect it with durability and consistency appropriate to its authority, cache it with explicit epochs, and test bootstrap/recovery. A data-plane scan is not always sufficient to reconstruct intent: overlapping transition copies may be indistinguishable without their map versions.

Statistics should also be partition-aware. Global averages can hide a saturated unit; per-partition statistics can become stale after movement or rapid growth. Query and scheduler decisions need cardinality, byte, key-frequency, and cost estimates with collection time and uncertainty. Adaptive decisions must avoid oscillation: repeatedly splitting, moving, or merging around a threshold can consume more capacity than the original imbalance. Hysteresis, minimum residence time, and movement budgets are policy mechanisms, not proofs that a new placement is better.

Partition boundaries interact with transactions and uniqueness. A uniqueness constraint scoped to the partition key can be checked locally. A global unique email address across tenant partitions requires a global index, reservation service, coordination, or relaxed semantics. Referential relationships may be local when child and parent keys co-locate; otherwise validation and deletion cross partitions. The architecture should not silently downgrade a global invariant because its enforcement is expensive.

For analytical jobs, the input partition is not necessarily the execution partition. File/object boundaries, table partitions, stream partitions, and operator state partitions can differ. A source task may read several small objects; a shuffle creates a new partitioning; a sink may coalesce output. Trace partition identity at each boundary so retry, checkpoint, locality, and small-file behavior are attributed to the correct layer.

## Definitions and Notation

Let `D` be a finite logical dataset, `K` a partition-key domain, `L={0,...,p-1}` logical partitions, `k:D->K` canonical key extraction, and `f_v:K->L` the partition function under map version `v`. Primary assignment is `a_v(x)=f_v(k(x))` and `P_l^v={x in D | a_v(x)=l}`.

Coverage requires `union_l P_l^v=D`. Exclusivity requires `P_i^v intersect P_j^v=empty` for `i != j`. A replicated placement relation `M_v(l)` maps one logical partition to one or more physical owners; it does not alter these set identities.

For load measure `w(x,t)`, partition load is `W_l(t)=sum_{x in P_l} w(x,t)`. Imbalance can be summarized by `max_l W_l / mean_l W_l` when the mean is nonzero, but tails and capacity constraints must also be inspected. A routing function is correct when every accepted request is evaluated by the owners of the same `a_v` used for the relevant stored data, or by a transition protocol that preserves equivalent observations.

## Mechanisms, Invariants, or Proof Structure

A partitioning argument has six obligations.

**1. Key contract.** Define extraction, canonicalization, domain, missing/invalid policy, stability, and authority. Prove that every eligible record produces exactly one canonical primary key value.

**2. Assignment correctness.** Show the partition function is total and deterministic for a declared version. Establish coverage and exclusivity independently by counting record identities and detecting duplicates across primary partitions.

**3. Workload fitness.** Map reads, writes, joins, aggregates, transactions, retention, and recovery to partitions. Quantify local operations, fan-out, shuffle bytes, large keys, and expected growth.

**4. Balance.** Replay representative and adversarial distributions. Measure bytes, events/requests, state, computation, spills, and tails per partition. Test hot keys and correlations rather than assuming uniformity.

**5. Routing and placement.** Verify that writers, readers, batch plans, stream state, and recovery use compatible map versions. Test stale routers, unavailable owners, duplicate retries, and node movement.

**6. Evolution.** Define split/merge/repartition state machines, ownership cutover, concurrent-write capture, validation, rollback, and cleanup. Recompute coverage, exclusivity, counts/digests, and application invariants before retiring the source.

The executable model uses a deliberately simple stable byte-sum partition function so its arithmetic is inspectable. It checks exact primary coverage/exclusivity and exposes skew. Module 003 develops production range, hash, and consistent algorithms.

<!-- bijux-verify: {"id":"horizontal-partition-invariants","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"counts=((0, 1), (1, 0), (2, 3), (3, 1))\ncoverage=True exclusivity=True\nroute(alpha)=2\nmax_to_mean=2.40\n","stderr":""}} -->
```python
records = (
    {"record_id": "r1", "customer_id": "alpha"},
    {"record_id": "r2", "customer_id": "beta"},
    {"record_id": "r3", "customer_id": "gamma"},
    {"record_id": "r4", "customer_id": "alpha"},
    {"record_id": "r5", "customer_id": "alpha"},
)
partition_count = 4


def canonical_key(value):
    if not isinstance(value, str) or not value:
        raise ValueError("customer_id must be nonempty text")
    return value.encode("utf-8")


def partition_for(value):
    return sum(canonical_key(value)) % partition_count


partitions = {partition: [] for partition in range(partition_count)}
for record in records:
    partitions[partition_for(record["customer_id"])].append(record)

input_ids = {record["record_id"] for record in records}
output_ids = [
    record["record_id"]
    for partition in partitions.values()
    for record in partition
]
coverage = set(output_ids) == input_ids
exclusivity = len(output_ids) == len(set(output_ids)) == len(input_ids)
counts = tuple((partition, len(partitions[partition])) for partition in partitions)
mean = len(records) / partition_count
max_to_mean = max(count for _partition, count in counts) / mean

print(f"counts={counts}")
print(f"coverage={coverage} exclusivity={exclusivity}")
print(f"route(alpha)={partition_for('alpha')}")
print(f"max_to_mean={max_to_mean:.2f}")
```

The checker proves these fixture properties only. The byte-sum function has weak distribution and easy collisions and is unsuitable as a general production hash. Python memory, persistent storage, concurrent routing, replication, failures, and online movement are not modeled. Real validation must use the exact implementation and retained key distributions.

## Alternatives and Trade-Offs

**Partition at ingest versus at computation.** Early partitioning enables locality and reusable layout but commits consumers to a key. Repartitioning per job adapts to each operator but repeatedly moves bytes. Persist layouts for durable dominant access; shuffle only when benefit exceeds movement.

**Entity versus time partitioning.** Entity keys localize history and keyed state. Time partitions prune retention/range scans and bound files, but current-time hotspots and entity-spanning queries remain. Composite/hierarchical layouts trade routing simplicity for flexibility.

**Static versus adaptive boundaries.** Static maps are reproducible and cheap to route. Adaptive split/merge responds to growth and skew but needs metadata, movement, stable identities, and transition protocols.

**Fine versus coarse partitions.** Fine units improve balance, placement, and recovery granularity while adding metadata/tasks/files. Coarse units reduce overhead but cap parallelism and amplify hotspots and movement.

**Co-location versus even distribution.** Co-location reduces communication/coordination for aligned work. Splitting heavy keys improves balance but makes key-scoped operations distributed. Choose from weighted workload evidence.

**Primary-only versus overlapping layouts.** One primary partitioning simplifies ownership. Secondary indexes, materialized projections, or replicas accelerate other access patterns but add update, consistency, storage, and repair obligations.

## Failure Modes and Misconceptions

1. **A partition is a machine.** Logical partitions can move, share nodes, or have replicas.
2. **The primary key is automatically the partition key.** Uniqueness does not guarantee locality or balanced workload.
3. **Equal record counts mean equal load.** Values, requests, state, and computation vary.
4. **Hashing eliminates skew.** Repeated hot keys still map together.
5. **More partitions always improve scale.** Metadata, scheduling, files, and coordination can dominate.
6. **Pruning is optional optimization only.** Incorrect pruning changes results.
7. **Same partition count means co-partitioned.** Key semantics, canonicalization, function, and boundaries must match.
8. **Moving bytes moves authority automatically.** Routing/write ownership needs an explicit cutover protocol.
9. **Dual writes guarantee migration safety.** Partial failures, ordering, retries, and divergence require reconciliation.
10. **Replication violates exclusivity.** Primary logical assignment remains exclusive while placement intentionally overlaps.

## Worked Examples

### Example 1

**Question:** Distinguish record, partition, and node identity.

**Reasoning:** `order-17` remains one record, logical partition `p42` owns it under map `v`, and `p42` currently resides on nodes `n3,n8` as replicas. Moving `p42` changes placement, not record or partition identity.

**Conclusion:** Stable logical identity permits physical movement.

### Example 2

**Question:** What breaks if missing tenant keys route randomly?

**Reasoning:** Replays differ, point reads cannot derive location, related records separate, and retries can create duplicates. Quarantine/reject or use a deterministic governed fallback with explicit semantics.

**Conclusion:** Total assignment requires a durable missing-key policy.

### Example 3

**Question:** Two tables both have eight partitions. Is their customer join local?

**Reasoning:** Only if customer domains/canonicalization, functions, map versions, and boundaries align. Eight incompatible partitions still require shuffle.

**Conclusion:** Co-partitioning is semantic and algorithmic compatibility, not equal counts.

### Example 4

**Question:** Why can a tenant key create a hotspot?

**Reasoning:** One large tenant's bytes and rate remain indivisible even if other tenants balance. A secondary bucket may distribute it but makes tenant-wide work multi-partition.

**Conclusion:** Key frequency and per-key work bound achievable balance.

### Example 5

**Question:** Can an email-domain predicate prune customer-ID partitions?

**Reasoning:** Not generally. Customer ID assignment reveals no domain relation. An index/projection may route it; otherwise every partition must participate.

**Conclusion:** Pruning requires a proven predicate-to-boundary relationship.

### Example 6

**Question:** When should a small table be broadcast?

**Reasoning:** When copying its serialized representation to workers costs less than repartitioning both inputs and worker memory can safely hold it. Size, concurrency, retries, and change frequency matter.

**Conclusion:** Broadcast is a costed communication choice, not a semantic shortcut.

### Example 7

**Question:** Why partition event-time windows by entity rather than event date?

**Reasoning:** Entity partitioning keeps keyed state and per-entity ordering local; date partitioning prunes time scans but moves entity histories across boundaries. Dominant operation decides.

**Conclusion:** Partition keys encode locality priorities.

### Example 8

**Question:** A source copy and destination digest match during migration. Is cutover safe?

**Reasoning:** Only for the captured snapshot. Concurrent writes, deletes, ordering, map freshness, pending retries, replica state, and application invariants still require reconciliation and authority transfer.

**Conclusion:** Byte copy validation is one stage of online repartitioning.

### Example 9

**Question:** How should a heavy key be diagnosed?

**Reasoning:** Measure its record bytes, rate, state, compute, spill, and tail contribution; compare with partition capacity; trace dependent operations. Salting helps only if combine/transaction costs remain acceptable.

**Conclusion:** Diagnose the limiting dimension before applying a skew technique.

### Example 10

**Question:** A national emergency-dispatch system repartitions incident state across regions. Is invariant testing sufficient?

**Reasoning:** No. Incident identity, geographic authority, failover, cross-region incidents, late updates, dispatcher workflow, degraded networks, privacy, accessibility, and safe rollback require simulations and named emergency-domain, safety, operations, geographic-data, security/privacy, network, software, and independent assurance reviewers. No external review is claimed here.

**Conclusion:** High-consequence movement requires domain validation and operational exercises beyond partition arithmetic.

## Cross-Program Connections

[Database Engineering](../../18-database-engineering/ROADMAP.md) develops table partitioning, indexes, transactions, and query planning. [Data Engineering](../../19-data-engineering/ROADMAP.md) owns pipeline partition layouts and data contracts; this program owns their cluster execution mechanics.

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies maps, trees, rings, and sketches used by partition maps. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns replication, consensus, membership, consistency, and partial-failure theory.

The 2012 [Spanner paper](https://research.google/pubs/spanner-googles-globally-distributed-database-2/) illustrates automatic partitioning combined with synchronous replication and transactions; those additional guarantees do not follow from partitioning alone. Spark's current [RDD programming guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html), checked 2026-08-29, exposes partitioned collections, shuffles, repartitioning, and recovery through recomputation.

## References

- David J. DeWitt and Jim Gray, [*Parallel Database Systems: The Future of High Performance Database Processing*](https://www.microsoft.com/en-us/research/publication/parallel-database-systems-the-future-of-database-processing-or-a-passing-fad/), `Communications of the ACM` 35(6), 1992. Primary shared-nothing and partitioned-parallelism survey.
- James C. Corbett et al., [*Spanner: Google's Globally-Distributed Database*](https://research.google/pubs/spanner-googles-globally-distributed-database-2/), OSDI, 2012. Primary partitioned, replicated database architecture.
- David F. Bacon et al., [*Spanner: Becoming a SQL System*](https://research.google/pubs/spanner-becoming-a-sql-system/), SIGMOD, 2017. Primary query routing and distributed execution during resharding.
- Giuseppe DeCandia et al., [*Dynamo: Amazon's Highly Available Key-value Store*](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf), SOSP, 2007. Primary dynamic partitioning, replication, membership, and failure-handling design.
- Matei Zaharia et al., [*Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing*](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf), NSDI, 2012. Primary partitioned collection and lineage-recovery abstraction.
- Apache Spark Project, [*RDD Programming Guide, Spark 4.1.2*](https://spark.apache.org/docs/latest/rdd-programming-guide.html), checked 2026-08-29. Official current partition, repartition, shuffle, and recovery behavior.
- Martin Kleppmann and Chris Riccomini, [*Designing Data-Intensive Applications*, second edition](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/), O'Reilly Media, 2026. Current durable treatment of partitioning, skew, routing, and rebalancing.

## Exercises

### Exercise 1

State coverage and exclusivity for five records assigned to three primary partitions. Explain how two replicas per partition affect each invariant.

### Exercise 2

Given partition loads `[10,10,10,50]` requests/s, compute maximum-to-mean ratio and explain why adding empty partitions may not fix the hot key.

### Exercise 3

Diagnose a customer-key partitioner where ingestion trims whitespace but query routing does not. Give a contract and migration repair.

### Exercise 4

Compare tenant, time, and composite tenant-time partition keys for a multitenant event store. Address routing, pruning, hot tenants, transactions, retention, and movement.

### Exercise 5

A hospital migrates medication-order state from 32 to 64 logical partitions while writes continue. Specify invariants, transition evidence, failure tests, and named human-review roles required before cutover.

## Answers to the Exercises

### Answer 1

Let `D={r1,...,r5}` and primary sets `P0,P1,P2`. Coverage requires `P0 union P1 union P2=D`. Exclusivity requires every pairwise intersection empty, equivalently each record identity occurs once across primary sets. Two physical replicas mean placement `M(Pi)` has two nodes; they do not add logical records or change primary set membership. Replica content/consistency requires separate invariants, while logical coverage/exclusivity remain unchanged.

### Answer 2

Total load is 80 and mean is 20, so maximum-to-mean ratio is `50/20=2.5`. If 50 belongs to one indivisible key, increasing partition count assigns that key to exactly one primary partition and its load remains 50. Splitting/salting the key, isolating it, changing the model, or increasing per-partition capacity may help, but each changes locality or combine/transaction cost.

### Answer 3

`" customer-7 "` is stored under canonical `"customer-7"` but an untrimmed router computes another partition, causing false absence or scatter. Define one versioned canonicalization over encoding, Unicode, case, whitespace, and invalid values and share conformance fixtures across writers/readers. Inventory records and request logs under both functions, route old and new versions during repair, reassign mispartitioned records with validation, cut over authority, drain stale clients, and retire the old map only after coverage/exclusivity and lookup probes pass.

### Answer 4

Tenant partitioning directly routes tenant operations and localizes transactions/isolation, but a large/hot tenant is indivisible and time retention touches its partition. Time partitioning prunes range retention/scans and bounds old data, while current writes hotspot and tenant operations fan out. Tenant-time limits both dimensions and supports pruning with both keys, but tenant-wide transactions/queries span buckets and routing needs a time bound. Select from measured access and growth; oversized tenants may need a governed secondary bucket, and stable logical partitions should move independently of nodes.

### Answer 5

Require stable medication/order identity, total/exclusive primary assignment under each map, canonical keys, no lost/duplicated orders, preserved ordering and transaction semantics, compatible readers/writers, and one authoritative write path at every instant. Snapshot each old partition, copy to new assignments, capture concurrent writes/deletes, reconcile counts/digests and domain invariants, validate routed reads, version ownership cutover, drain old requests, and retain rollback until new recovery is proven. Test crash/restart at every transition, stale routers, duplicate/reordered retries, network partition, hot patients/wards, cancellation, replica lag, rollback, and backup restore. Named reviewers include pharmacists/medication-safety clinicians, clinical workflow owners, health-data governance/privacy, cybersecurity, database/distributed-systems engineers, operations and disaster recovery, test/quality, and the applicable independent clinical-safety authority. No local checker or this answer supplies external approval.
