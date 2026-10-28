---
module_id: SARCH-053
program: Software Engineering: Software Architecture
level: 2
module_number: 53
title: Partitioning and Data Placement
status: complete
last_verified: 2026-09-06
---

# Partitioning and Data Placement

## One-Page Review

### Governing question

How should architects divide data and work into independently owned units, place those units across failure and jurisdiction boundaries, and change the mapping without turning skew, cross-partition coordination, or movement into hidden correctness and availability failures?

### Essential definitions

- A **partition** or **shard** is a subset of a logical dataset or workload assigned as one placement, routing, scaling, or failure unit.
- A **partition key** maps a record or operation to a partition; a **placement policy** maps each partition and replica to resources and locations.
- **range partitioning** assigns ordered key intervals; **hash partitioning** assigns hash-space intervals or buckets; **directory partitioning** uses explicit metadata.
- A **logical partition** is a stable routing unit; a **physical placement** is its current machine, process, disk, zone, or region assignment.
- **skew** is unequal distribution of records, bytes, requests, computation, or growth. A **hot key** concentrates load that adding ordinary partitions may not divide.
- **affinity** is a reason to colocate data or work; **anti-affinity** is a reason to separate replicas or correlated risks.
- **residency** constrains where governed data may be stored or processed; **sovereignty** may add legal or administrative control constraints.
- **rebalancing** changes placement to restore capacity, balance, or fault isolation; **resharding** changes logical partition boundaries.
- A **routing epoch** identifies one version of the key-to-partition and partition-to-placement mapping.
- **split brain** means incompatible actors simultaneously believe they own writes for the same partition.

### Central model, mechanism, or theorem

Let item or request $i$ have weight $w_i$ and map to partition $p(i)$. Partition load is

$$
L_j=\sum_{i:p(i)=j}w_i,
$$

and normalized utilization on capacity $C_j$ is $U_j=L_j/C_j$. A design fails at the most constrained resource, so records alone are a poor balance metric: weights may represent bytes, requests, CPU, memory, storage bandwidth, network egress, locks, or growth.

For $m$ partitions with mean load $\bar L$, one descriptive skew measure is coefficient of variation

$$
CV=\frac{\sqrt{\frac{1}{m}\sum_{j=1}^{m}(L_j-\bar L)^2}}{\bar L}.
$$

It summarizes dispersion but does not reveal a single harmful tenant, tail latency, correlated failure, or an overloaded capacity class. Architecture therefore joins quantitative signals to key semantics, access paths, placement constraints, and failure experiments.

### Critical invariants

- one authoritative owner or safely coordinated owner set exists for every writable key at every routing epoch;
- routing and storage agree on key boundaries, epochs, and cutover state;
- old clients cannot write through stale ownership after a move or split;
- replicas of one partition satisfy declared failure-domain and residency constraints;
- partition keys preserve required domain boundaries and do not expose sensitive information unnecessarily;
- uniqueness, referential integrity, ordering, transactions, and authorization state their partition scope;
- cross-partition operations have explicit coordination, saga, approximation, or rejection semantics;
- capacity models include requests, bytes, compute, state, growth, fan-out, repair, and movement;
- hot keys receive semantic treatment rather than blind partition-count increases;
- movement is rate-limited, checksummed, observable, reversible where possible, and fenced at cutover;
- deleted or expired data does not reappear from a moving or lagging replica;
- partition loss, unavailability, and relocation have bounded blast radius and owned recovery;
- placement constraints are verified continuously, including during repair and emergency operation;
- logical identity remains stable when physical placement changes.

### Common failures

Common failures include choosing a monotonically increasing key that sends all writes to one range; hashing away locality needed by range scans; assuming even record counts imply even work; partitioning by tenant while one tenant dominates; scattering a transaction across shards accidentally; embedding current host names in durable IDs; placing replicas in labels called “zones” that share one power or network dependency; violating residency during backup or repair; dual-writing old and new owners without fencing; moving data faster than foreground traffic permits; letting caches retain an obsolete routing map; splitting a hot range without splitting its hot key; and declaring a rebalance complete before indexes, change streams, tombstones, and external effects agree.

### Compact example

A telemetry service hashes `device_id` into 256 logical buckets, then places buckets across nodes. One fleet gateway uses one device identity for 35% of writes. Adding nodes moves buckets but cannot divide that key. The design changes the semantic key to `(gateway_id, time_bucket, subshard)`, keeps an index for device history, bounds query fan-out, and records the routing epoch. The remedy changes write distribution and read cost; it is not merely a larger cluster.

### Connections

[SARCH-041](041-system-of-record-boundaries.md) supplies authority, [SARCH-051](051-partial-failure-as-an-architectural-constraint.md) supplies failure models, and [SARCH-052](052-consistency-and-availability-trade-offs.md) supplies consistency choices. [SARCH-054](../ROADMAP.md) next evaluates multi-region topologies. Database Engineering owns engine-specific sharding and query execution; this module owns architectural boundaries, placement policy, evolution, and consequences.

## Governing Question

Partitioning promises horizontal scale by replacing one large ownership and resource unit with many smaller ones. Yet the mapping itself becomes architecture: it determines which operations are local, which failures correlate, which users interfere, where data crosses borders, and how much state must move when capacity changes.

The governing question is not simply “which shard key?” It is which logical boundaries remain stable, which physical placements may change, what must be colocated or separated, how skew is detected, and which protocol preserves authority while the map evolves.

## Why This Matters

A poor partition key can make a hundred-node system behave like one overloaded node. A technically balanced placement can still violate residency, concentrate replicas behind one network dependency, or make every important query fan out to the entire fleet. Rebalancing intended to restore capacity can consume the storage and network headroom needed to survive.

Placement is also a correctness concern. Routing during a split, merge, migration, or failover decides whether writes are lost, duplicated, reordered, or accepted by two owners. Treating it as an infrastructure afterthought hides business invariants inside caches and operational scripts.

## Prerequisites and Retrieval

Retrieve domain identity, aggregate, authority, transaction, index, query, hash function, ordered range, replica, quorum, consistency model, failure domain, availability zone, region, latency, throughput, tail latency, working set, capacity, backpressure, idempotency, tombstone, change stream, data residency, and reconciliation.

From SARCH-025 retrieve deployment structure; SARCH-041 and SARCH-042 provide system-of-record and store-selection reasoning; SARCH-048 and SARCH-049 provide release and environment topology; SARCH-051 provides partial failure; and SARCH-052 provides consistency and quorum limits.

## Learning Objectives

After completing this module, you should be able to:

1. separate logical partitioning, routing, replica placement, and physical allocation;
2. compare range, hash, directory, geographic, tenant, and composite partitioning;
3. quantify imbalance across several resource dimensions without mistaking one metric for a guarantee;
4. detect hot keys, hot ranges, noisy tenants, and fan-out amplification;
5. choose affinity and anti-affinity from transactions, queries, failure domains, and governance;
6. define authority and fencing across split, merge, move, and failover epochs;
7. design online migration with copy, catch-up, validation, cutover, and rollback evidence;
8. evaluate replication placement against correlated failure and residency constraints;
9. reason about operational headroom, repair traffic, and movement debt;
10. review partitioning evidence from workload traces and adversarial tests without inferring universal balance.

## Core Exposition

**Separate the maps.** A useful design distinguishes at least four mappings: domain entity to logical partition, logical partition to replica set, replica to physical resource, and request to current authority. Combining them makes routine movement change durable identity and forces clients to know hosts.

Keep logical partitions more stable than machines. A partition identifier may survive disk replacement, zone evacuation, or process restart. Routing metadata resolves the current placement and authority epoch. Caches accelerate the lookup but cannot become independent truth.

**Begin with access and invariant boundaries.** List writes, reads, joins, scans, ordering requirements, uniqueness, transactions, retention, authorization, and recovery. Estimate current and projected distributions. A key that distributes writes but forces every critical read across all shards has moved cost rather than removed it.

Prefer locality for operations that must be atomic or ordered. A customer aggregate may colocate account settings and commands, while global email uniqueness remains a separate coordinated index. Do not enlarge one shard until every relationship is local; oversized partitions lose the independence sought.

**Use range partitioning for order deliberately.** Ordered ranges support prefix lookup, bounded scans, time traversal, and boundary-aware split. They expose skew when inserts concentrate at the end, when one lexical prefix dominates, or when a hot interval receives most queries.

Mitigations include salting, reverse-time or composite keys, adaptive range splits, and separate write/read representations. Each affects scan order and fan-out. Range boundaries should be metadata, not embedded forever in clients.

**Use hashing for distribution deliberately.** Hashing removes ordinary key order and often spreads independent keys more evenly. Modulo by a changing node count causes broad remapping; stable logical buckets, consistent hashing, or rendezvous hashing can limit movement when membership changes.

Hash balance is probabilistic and workload-dependent. Many keys do not help if one key dominates. Hash quality does not solve heterogeneous node capacity, transaction locality, residency, or a shared downstream bottleneck. Measure weighted load after mapping.

**Use directory partitioning when policy outweighs arithmetic.** An explicit directory can place tenant A in Sweden, a regulated account in an isolated cell, and a large tenant across dedicated resources. It supports exceptions, heterogeneous capacity, and gradual migration.

The directory becomes critical metadata. It needs durable authority, caching rules, versioning, bootstrap, recovery, and protection from unavailable control planes. A stale directory must not grant stale write authority.

**Compose keys cautiously.** Composite keys such as `(tenant, account)` or `(region, day, hash suffix)` encode both locality and distribution. Put stable semantic scope first when queries use prefixes; add bounded subshards where a scope is too hot.

Every suffix creates read amplification for queries that omit it. Maintain a routing index, query only known subshards, or accept bounded scatter. Do not use a random suffix without an aggregation and deletion plan.

**Measure several kinds of skew.** Record count, bytes, request rate, CPU time, memory residency, storage operations, network egress, lock contention, queue delay, and growth rate. Normalize by each placement's capacity. Inspect maxima and tails, not only mean or coefficient of variation.

Skew changes with time. Midnight jobs, market open, viral tenants, rolling retention, and a new query can shift the constraint. Use per-key or heavy-hitter sketches where cardinality prevents complete labels, while protecting customer privacy and metric capacity.

**Treat hot keys semantically.** A hot key is not divided by adding nodes if it remains one ownership unit. Read replication and caching help read heat. Commutative counters can shard updates and aggregate. A strict single-object order may require one authority, batching, admission, or a redesigned domain.

Splitting identity can weaken semantics. Ten independent inventory counters do not preserve a global bound unless rights are allocated and conserved. State explicitly which guarantee changes.

**Control fan-out.** Scatter-gather can recover queries not aligned with the partition key, but its cost grows with partitions. Even if each shard has independent 99th-percentile latency, the slowest of many replies dominates the aggregate. Partial responses also need semantics.

Use secondary routing indexes, materialized views, hierarchical aggregation, bounded time windows, or asynchronous analytics. Cap concurrency and total work. A timeout does not prove missing shards have no matching data.

**Choose partition granularity.** Too few partitions constrain parallelism, isolate poorly, and make movement large. Too many increase metadata, files, connections, scheduling, replication, compaction, and recovery overhead. Logical partitions should be small enough to move within the recovery budget but large enough to amortize fixed costs.

Estimate movement duration from transferable bytes divided by safe residual bandwidth, then include ongoing writes, verification, retries, and throttling. Nominal link bandwidth is not a safe migration rate.

**Place replicas against real failure domains.** Anti-affinity should follow power, rack, network, zone, region, provider, administrative, software, and operational dependencies relevant to the claim. Labels are evidence inputs, not proof of independence.

Replica placement also affects latency, quorum reachability, egress, and repair. Three replicas across three regions may survive a regional loss yet make quorum writes slow. Three replicas in one building may be fast but not region resilient. State the fault set and operation contract.

**Honor jurisdiction and lifecycle.** Residency applies to primary replicas, backups, logs, indexes, caches, queues, support exports, training copies, and repair paths as policy requires. Processing location and administrative access can matter separately from storage location.

Deletion must follow movement. Tombstones or deletion epochs need retention long enough to cover disconnected replicas and backups under the governing policy. A restored snapshot must reapply later deletion and policy records before serving.

**Colocate selectively.** Colocation reduces latency and coordination for transactions, joins, and ordered streams. It can also create noisy-neighbor coupling and a large failure unit. Anti-affinity improves isolation but adds network cost and distributed coordination.

Use domain aggregate and transaction evidence, not object-reference convenience. Cross-partition operations may use a distributed transaction, workflow with compensation, reserved rights, immutable event plus projection, approximation, or rejection. Each has different failure and user-visible semantics.

**Version routing and authority.** Every placement change has an epoch or generation. Requests carry or resolve it; owners reject writes for epochs they no longer own. Fencing prevents an isolated former owner from accepting after cutover.

Reads during migration require a rule: old owner, new owner after caught-up watermark, merge of versioned results, or bounded stale response. Dual reads and dual writes are mechanisms with failure modes, not a complete migration protocol.

**Split and move through explicit states.** A robust online move commonly records intent, establishes target, copies a snapshot, streams changes, verifies state, quiesces or fences authority, advances routing atomically at its authority, drains old traffic, validates outcomes, and retires old state after rollback and retention windows.

The order depends on the storage and consistency model. Copying without a change boundary misses writes. Dual writing without identity and ordering can diverge. Deleting the source immediately removes rollback evidence. Make each state restartable and idempotent.

**Budget rebalancing as production traffic.** Copy, compaction, checksum, index build, repair, and cache warm-up consume the same resources as foreground work. Rate-limit by resource and tenant, preserve failure reserve, and pause automatically when latency or error budgets deteriorate.

Avoid oscillation: a short spike should not repeatedly move a large partition. Use hysteresis, minimum residence time, benefit threshold, and movement budget. Sometimes admission or dedicated capacity is safer than immediate relocation.

**Plan membership and metadata failure.** Routing metadata needs a bootstrap path and a consistency contract. If the directory is unavailable, existing cached routes might continue for reads or fenced writes within lease, while new partitions and moves stop. Say which behavior is safe.

Reconfiguration must preserve overlap or transfer authority explicitly. A membership list assembled from eventually consistent health gossip is not sufficient evidence to grant write ownership. Separate suspicion, placement desire, and authority decision.

**Design tenant isolation.** Tenant-based partitioning simplifies deletion, export, billing, and blast-radius attribution. Large tenants may need multiple subpartitions; small tenants may share. Maintain a stable tenant directory so growth changes placement without changing public identity.

Protect against noisy neighbors with per-tenant admission, quotas, scheduling, and resource accounting. A dedicated shard can improve isolation but may waste capacity and create a unique recovery path that receives less testing.

**Observe the mapping and its consequences.** Record logical partition, key class without leaking raw secrets, routing epoch, owner, replica placements, placement constraints, request cost, queue and latency, bytes, growth, split/move state, verification watermark, stale-route rejection, and recovery status.

Dashboards showing equal bytes do not prove balanced latency or safe placement. Audit constraints independently. Sample user journeys spanning joins, indexes, asynchronous projections, and deletions.

**Test adversarial evolution.** Test a split during heavy writes, target crash after copy, lost cutover response, stale client, duplicate change record, delayed tombstone, rollback, simultaneous node loss, false zone label, saturated repair link, and policy change mid-move.

Verify invariants and terminal outcomes. Measure foreground impact and recovery time. Tests demonstrate observed histories in a recorded environment; proofs and design arguments remain necessary for unobserved schedules.

## Definitions and Notation

Let:

- $K$ be the key space and $P=\{p_1,\ldots,p_m\}$ the logical partition set;
- $h:K\rightarrow P$ be the current key-to-partition mapping;
- $g_e:P\rightarrow 2^R$ map a partition to replica resources under routing epoch $e$;
- $w_i^{(d)}$ be item or request $i$'s weight in resource dimension $d$;
- $L_j^{(d)}=\sum_{i:h(i)=p_j}w_i^{(d)}$ be load of partition $j$ in dimension $d$;
- $C_r^{(d)}$ be safe capacity of resource $r$ in dimension $d$;
- $U_r^{(d)}=L_r^{(d)}/C_r^{(d)}$ be normalized utilization;
- $F$ be the declared fault set the placement is intended to tolerate;
- $B$ be bytes to move, $b$ safe residual transfer rate, and $T\ge B/b$ the optimistic transfer lower bound before write catch-up and verification;
- **routing epoch** mean an ordered mapping version used to reject stale authority;
- **heavy hitter** mean a key or key class contributing a disproportionate share of a resource;
- **scatter-gather** mean dispatching one logical query to multiple partitions and combining results;
- **movement debt** mean placement work deferred while imbalance or policy exposure remains.

No scalar load score preserves all resource constraints. Placement is feasible only if every required dimension, failure rule, jurisdiction rule, and operational reserve is satisfied.

## Mechanisms, Invariants, or Proof Structure

### Partition-design procedure

1. Enumerate operations, access paths, invariants, ordering, and transaction scope.
2. Describe key distributions and weighted workloads, including growth and adversarial concentration.
3. Select stable logical partition identity and candidate range, hash, directory, geography, tenant, or composite mapping.
4. Quantify local work, scatter, secondary indexes, and cross-partition coordination.
5. Define replica count, authority, consistency, failure domains, residency, and capacity reserve.
6. Define hot-key treatment and tenant isolation without silently weakening invariants.
7. Version routing and specify stale-client, control-plane-loss, and split-brain behavior.
8. Specify split, merge, move, copy, catch-up, validation, cutover, rollback, and retirement states.
9. Observe every mapping and constraint; test skew, failure, policy change, and restoration.

### Balance calculation

For loads $[40,20,20,20]$, mean load is $25$. The population standard deviation is

$$
\sqrt{((40-25)^2+3(20-25)^2)/4}=\sqrt{75}\approx8.66,
$$

so $CV\approx8.66/25=0.346$. This signals dispersion but not whether load 40 exceeds capacity, which keys cause it, or whether the light partitions occupy smaller nodes.

### Architectural invariants

- every key resolves to one valid logical partition under each published map;
- every writable partition has one valid authority protocol at cutover;
- every replica set satisfies the declared placement policy, including during repair;
- every cross-partition operation exposes its consistency and partial-failure semantics;
- every migration can identify copied state, subsequent changes, cutover epoch, validation result, and remaining old state;
- no balance claim depends on record count alone.

## Alternatives and Trade-Offs

| Choice | Strength | Cost or risk | Evidence needed |
|---|---|---|---|
| ordered ranges | scans and adaptive boundaries | end hotspots and uneven ranges | range heat and split history |
| hash buckets | ordinary key distribution | no natural range locality | weighted bucket distribution |
| consistent/rendezvous hash | limited remapping | probabilistic balance and policy complexity | movement and load simulation |
| explicit directory | tenant, capacity, and policy control | metadata authority and cache failure | epoch and recovery tests |
| tenant partition | isolation and lifecycle locality | whale tenants and shared-small-tenant skew | per-tenant multidimensional cost |
| geographic partition | locality and residency | cross-region operations and mobility | jurisdiction and latency audit |
| colocated aggregate | local transaction and order | larger blast radius and hotspot | invariant and workload trace |
| scatter-gather | flexible reads | fan-out work and tail latency | shard count, partial results, deadline |
| online split/move | continuity during change | dual-state protocol complexity | copy, catch-up, fencing, reconciliation |
| overpartitioning | flexible placement and parallelism | metadata and fixed overhead | control-plane and recovery capacity |

## Failure Modes and Misconceptions

1. **“More shards always mean more capacity.”** A hot key, shared dependency, or coordination point can remain serial.
2. **“Hashing guarantees balance.”** Distribution is probabilistic and weights are rarely uniform.
3. **“Equal row counts mean balance.”** bytes, CPU, requests, locks, growth, and egress may differ.
4. **“Range partitioning always hotspots.”** it depends on key and workload; adaptive splits can help.
5. **“Consistent hashing solves sharding.”** it addresses remapping, not domain locality, authority, or governance.
6. **“Cross-shard transactions are impossible.”** they are possible but impose coordination and failure costs.
7. **“Replica count proves resilience.”** correlated placement can defeat every replica.
8. **“Zone labels prove independence.”** actual power, network, software, and administrative dependencies matter.
9. **“Residency concerns only primary storage.”** backups, logs, caches, repair, and support paths may be governed.
10. **“Dual write makes migration safe.”** ordering, identity, fencing, and partial failure remain.
11. **“A copied snapshot is current.”** concurrent writes require a change boundary and catch-up.
12. **“Adding a random suffix fixes heat.”** it creates read, deletion, and aggregation fan-out.
13. **“Rebalancing is background and free.”** it consumes production headroom and can amplify failure.
14. **“Routing caches may fail open.”** stale write routes can create dual authority.
15. **“Physical host is a durable partition ID.”** replacement and movement then break identity.
16. **“Replica equality completes migration.”** indexes, streams, tombstones, external effects, and policy evidence may still diverge.

## Worked Examples

### Example 1

**Situation.** Orders are range-partitioned by increasing numeric ID, and all new writes reach the final range.

**Reasoning.** Historical ranges remain cold while one owner handles inserts and current-order reads. Splitting the final range repeatedly moves the edge but does not remove a single monotonic frontier. A composite key such as `(customer_region, hash(customer_id), order_id)` spreads writes; a separate time index supports recent-order scans with explicit fan-out.

**Conclusion.** Preserve query locality through indexes while removing the write frontier from the primary placement key.

### Example 2

**Situation.** Four partitions receive weighted loads $[40,20,20,20]$ on equal-capacity nodes.

**Reasoning.** Mean is 25, standard deviation is $\sqrt{75}\approx8.66$, and $CV\approx0.346$. If safe capacity is 35, only the first partition violates it despite a moderate aggregate average. Per-key data shows one tenant contributes 28 units, so moving unrelated cold keys cannot solve the overload.

**Conclusion.** Distribution metrics must be joined to capacity and heavy-hitter attribution.

### Example 3

**Situation.** A social feed hashes user IDs evenly, but celebrity reads overload one partition.

**Reasoning.** The write keys are balanced; read popularity is not. Replicate or cache immutable feed segments, apply request admission, and build fan-out-on-write or fan-out-on-read according to follower distribution. Splitting the celebrity's mutable ordered feed may change ordering and publication semantics.

**Conclusion.** Treat read heat with workload-specific replication or model change, not a blind node-count increase.

### Example 4

**Situation.** An account transfer debits one customer partition and credits another.

**Reasoning.** If atomic transfer is required, use a distributed transaction or colocate both accounts under a stable aggregate where feasible. A workflow may instead expose pending transfer, reserve debit, idempotently credit, and compensate under explicit rules. Two independent best-effort writes can lose or create value.

**Conclusion.** Cross-partition semantics must be selected from the monetary invariant, not hidden in client retries.

### Example 5

**Situation.** A tenant shard grows from 600 GB to 1.2 TB, and safe residual copy bandwidth is 40 MB/s.

**Reasoning.** Ignoring decimal/binary differences, the optimistic lower bound for 1.2 TB is $1{,}200{,}000/40=30{,}000$ seconds, about 8.33 hours. Ongoing writes, checksum, index build, retries, and throttling make reality longer. Split earlier so each movement unit fits recovery and maintenance windows.

**Conclusion.** Partition size is constrained by safe movement time, not storage capacity alone.

### Example 6

**Situation.** Three replicas are labeled as separate zones but share one building network edge.

**Reasoning.** The declared fault set includes a network-edge failure, so all replicas are correlated against that claim. Placement must use verified independent paths or narrow the promise. Adding a fourth replica behind the same edge changes count, not the failure boundary.

**Conclusion.** Anti-affinity follows causal dependencies rather than labels or replica totals.

### Example 7

**Situation.** A Swedish health tenant's primary is local, but repair temporarily copies a replica through an unconstrained region.

**Reasoning.** If policy covers storage and processing location, the repair violates placement even though final state returns. Constrain targets, transit and keys; include backups, logs, support export, and emergency replacement; block unsafe repair and surface reduced redundancy.

**Conclusion.** Residency is a continuous lifecycle invariant, including degraded and recovery paths.

### Example 8

**Situation.** During a shard move, an isolated old owner and the new owner both accept writes.

**Reasoning.** Copy correctness cannot prevent split brain. The authority service advances from epoch 18 to 19; the new owner accepts epoch 19, and storage rejects epoch 18 even if an old router sends it. The move preserves change identity and reconciles the cutover watermark before retirement.

**Conclusion.** Movement requires fencing and ordered authority, not only data transfer.

### Example 9

**Situation.** A query for the latest 100 events fans out to 2,000 partitions.

**Reasoning.** Each shard performs work and the coordinator waits on a large tail or defines partial results. Partition-local top 100 yields up to 200,000 candidates before merge. A time/tenant routing index, hierarchical top-k, and bounded window reduce fan-out; the API states completeness and cutoff.

**Conclusion.** A write-balanced key can be architecturally poor when dominant reads scatter globally.

### Example 10

**Situation.** A rebalance starts at 75% disk utilization and raises foreground 99th-percentile latency beyond its objective.

**Reasoning.** Copy and compaction consume disk and network reserve. The controller throttles by latency and queue depth, prioritizes a partition at imminent capacity risk, and retains hysteresis so it does not reverse after a brief dip. Admission and temporary dedicated capacity may be safer than faster copying.

**Conclusion.** Rebalancing is governed production traffic with safety margins and stop conditions.

## Cross-Program Connections

- **Database Engineering:** owns access methods, distributed transactions, optimizer behavior, and engine-specific sharding.
- **Data Engineering:** owns stream partitions, batch distribution, shuffle, watermarking, and pipeline skew.
- **Data Architecture Engineering:** owns authoritative domains, residency, lifecycle, lineage, and cross-system placement governance.
- **Distributed Systems Engineering:** owns formal membership, replication, consensus, consistent hashing, and reconfiguration protocols.
- **Algorithm Engineering:** supplies hashing, load balancing, heavy-hitter detection, and approximation analysis.
- **Platform Engineering:** supplies schedulers, topology labels, capacity, routing, isolation, and placement enforcement.
- **Security Engineering:** owns sensitive-key exposure, authorization locality, encryption domains, and hostile-tenant isolation.
- **Software Delivery and Reliability Engineering:** owns safe rollout, migration operations, SLO protection, recovery, and incident evidence.

## References

1. David J. DeWitt and Jim Gray, “Parallel Database Systems: The Future of High Performance Database Systems,” *Communications of the ACM* 35(6), 1992. <https://doi.org/10.1145/129888.129894>
2. David Karger et al., “Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web,” *STOC 1997*. <https://doi.org/10.1145/258533.258660>
3. Giuseppe DeCandia et al., “Dynamo: Amazon's Highly Available Key-value Store,” *SOSP 2007*. <https://doi.org/10.1145/1294261.1294281>
4. James C. Corbett et al., “Spanner: Google's Globally-Distributed Database,” *OSDI 2012*. <https://www.usenix.org/conference/osdi12/technical-sessions/presentation/corbett>
5. Carlo Curino et al., “Schism: A Workload-Driven Approach to Database Replication and Partitioning,” *PVLDB* 3(1–2), 2010. <https://www.vldb.org/pvldb/vldb2010/pvldb_vol3/R19.pdf>
6. Atul Adya et al., “Slicer: Auto-Sharding for Datacenter Applications,” *OSDI 2016*. <https://www.usenix.org/conference/osdi16/technical-sessions/presentation/adya>
7. Marcos K. Aguilera et al., “Shard Manager: A Generic Shard Management Framework for Geo-Distributed Applications,” *SOSP 2021*. <https://doi.org/10.1145/3477132.3483546>
8. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.

## Exercises

### Exercise 1

Define logical partition, physical placement, partition key, range partitioning, hash partitioning, directory partitioning, skew, hot key, affinity, anti-affinity, routing epoch, residency, rebalancing, resharding, scatter-gather, and movement debt.

### Exercise 2

For equal-capacity partitions with request loads $[60,30,20,10]$, calculate mean, population standard deviation, coefficient of variation, and maximum-to-mean ratio. If safe capacity is 50, explain what each statistic does and does not establish.

### Exercise 3

Diagnose an online move that copies a snapshot, immediately changes DNS, dual-writes with no operation identity, allows cached old routes for an hour, deletes the source after five minutes, and checks only row count. Design a safe state machine and evidence set.

### Exercise 4

Compare range, hash, consistent/rendezvous hash, and explicit-directory partitioning for time-series ingestion, customer accounts, a global catalog, and regulated multi-tenant records. Address transactions, queries, skew, movement, failure domains, and governance.

### Exercise 5

Design partitioning and placement for an international emergency-supply network with national warehouses, mobile clinics, intermittent links, temperature telemetry, controlled medicines, recalls, patient privacy, uneven disasters, and physical inventory. Include keys, logical units, replicas, authority, residency, rights, hot-key treatment, queries, routing epochs, migration, recovery, evidence, and human control.

## Answers to the Exercises

### Answer 1

A **logical partition** is a stable routing or ownership subset; **physical placement** is its current resource location. A **partition key** maps records or work to a partition. **Range**, **hash**, and **directory partitioning** use ordered intervals, hash-space allocation, and explicit metadata respectively. **Skew** is unequal weighted distribution; a **hot key** contributes disproportionate load. **Affinity** motivates colocation; **anti-affinity** separates correlated risk. A **routing epoch** versions mapping and authority. **Residency** constrains storage or processing location. **Rebalancing** changes placement; **resharding** changes logical boundaries. **Scatter-gather** queries multiple partitions and combines results. **Movement debt** is deferred relocation while imbalance or policy exposure persists.

### Answer 2

The mean is $(60+30+20+10)/4=30$. Squared deviations are $900,0,100,400$, so population variance is $1{,}400/4=350$ and standard deviation is $\sqrt{350}\approx18.71$. Thus $CV\approx18.71/30=0.624$, and maximum-to-mean is $60/30=2$. These describe request dispersion and show one partition exceeds safe capacity 50. They do not identify the hot keys, byte/CPU/lock cost, tail latency, node heterogeneity, correlated placement, time variation, or whether moving the partition is safe.

### Answer 3

The move lacks a concurrent-write boundary, durable identity, fencing, safe routing, rollback window, and content validation. Record a move intent and source epoch; provision the target; copy a versioned snapshot; stream idempotently identified changes after its watermark; build indexes; compare counts, checksums, sampled values, tombstones, constraints, and change position; then quiesce or fence source writes and atomically advance authoritative routing to a new epoch. New storage rejects old epochs. Observe stale-route rejections and drain reads according to an explicit rule. Keep the source read-only through a governed rollback and retention window. Reconcile change streams and external effects before retirement. DNS may distribute endpoints but is not the authority protocol.

### Answer 4

Time-series ingestion benefits from time ranges for retention and scans but needs a device/hash subkey to avoid a current-time hotspot. Customer accounts often use account or tenant directory placement to preserve local transactions and move large tenants independently. A global catalog can hash primary product identity while maintaining search and category indexes; popular products need read caching or replication. Regulated records favor an explicit tenant/jurisdiction directory with constrained replica sets and audited lifecycle paths.

Range partitioning preserves order and adaptive boundaries but can hotspot. Plain hash buckets distribute ordinary keys but lose order; stable buckets decouple node count. Consistent or rendezvous hashing limits remapping but remains probabilistic and needs capacity, replica, and policy logic. A directory expresses exceptions and heterogeneous constraints but creates authoritative metadata and stale-cache risks. Every design must state cross-partition transaction behavior, fan-out, heavy-hitter response, epoch fencing, repair placement, and migration evidence.

### Answer 5

Use stable jurisdiction and organization identities, then logical partitions such as `(country, warehouse)` and `(country, clinic, bounded_subshard)` rather than physical hosts. A governed directory maps them to residency-compliant replica sets and routing epochs. Controlled-medicine inventory has one warehouse authority or conserved transfer rights; physical dispatch and receipt use immutable identities and require reconciliation. Clinics receive bounded rights for offline dispensing. Recall authority publishes authenticated monotonic lot epochs and deletion-like tombstones that old devices cannot overwrite.

Temperature telemetry uses `(shipment, time_bucket, hash_suffix)` to spread ingestion, with an index for shipment history and explicit late-data rules. A disaster or mass recall can create hot countries and lots; preallocate subshards, cache signed read-only recall facts, admit work by safety priority, and dedicate capacity without splitting authoritative medicine counts unsafely. Patient records remain in permitted jurisdictions; logs, backups, support access, repair transit, and analytics follow the same policy. Cross-country aggregate planning uses minimized asynchronous projections rather than unrestricted patient copies.

Moves record snapshot and change watermarks, verify signatures, checksums, tombstones, rights, indexes, and physical counts, fence the old epoch, and retain a rollback window. During directory loss, existing bounded routes may continue only within explicit lease and policy; new authority changes stop. Recovery throttles copy traffic, restores recall and identity foundations first, and reconciles warehouse, vehicle, clinic, dispensing, and patient outcomes. Evidence includes partition and policy epoch, owner, replicas, rights, freshness, temperature gaps, move state, stale-route rejection, physical count, manual decision, and terminal resolution. Named national and clinical authorities control emergency overrides, which are scoped, authenticated, expiring, and audited.
