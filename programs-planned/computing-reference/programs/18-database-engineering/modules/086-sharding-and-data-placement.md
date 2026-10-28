---
module_id: DBE-086
program: Database Engineering
level: 2
module_number: 86
title: Sharding and Data Placement
status: complete
last_verified: 2026-09-05
---

# Sharding and Data Placement

## One-Page Review

### Governing question

How can a database divide one logical data model into independently served units and place their replicas so capacity, locality, failure survival, transactions, queries, and movement remain correct as workload and topology change?

### Essential definitions

**Sharding** horizontally partitions logical rows or keys into disjoint authoritative units. A **shard**, **range**, **tablet**, or **partition** is a placement and routing unit; product meanings differ. A **partition function** maps a logical key to one unit. **Range sharding** uses ordered intervals; **hash sharding** maps key hashes to buckets; **directory sharding** uses explicit metadata. **Placement** assigns each unit's replicas and leader/lease to nodes and failure domains. A **routing directory** maps key spans or shard IDs to owners under a metadata epoch. A **hotspot** is a unit or resource whose load exceeds useful capacity even when total cluster capacity is sufficient. **Split**, **merge**, and **move** change unit boundaries or owners. **Resharding** changes the partition function or shard set while preserving data and request correctness. A **scatter/gather** operation contacts several shards and combines results. **Colocation** places related data in one shard or nearby units to reduce distributed work.

### Central model, mechanism, or theorem

For keyspace $K$ and active shard intervals $I_1,\ldots,I_m$, correctness requires

$$
\bigcup_{i=1}^{m}I_i=K,\qquad I_i\cap I_j=\varnothing\quad(i\ne j),
$$

plus one current metadata epoch that assigns each interval exactly one authoritative replication group. Replica placement must satisfy per-shard constraints such as count, distinct zones, residency, storage compatibility, and leader locality. During movement, a snapshot plus complete ordered delta is installed at the destination, then one epoch-fenced cutover transfers authority. Hash balance over keys does not imply balance over requests, bytes, or transaction cost.

### Critical invariants

- Every routable key maps to exactly one authoritative shard in the current partition epoch.
- Routing metadata is versioned; stale routers are redirected or rejected rather than accepted by two owners.
- Every replica set satisfies distinct identity, history, replication factor, failure-domain, residency, and compatibility constraints.
- A split/merge preserves coverage without overlap or holes at the authority cut.
- A move transfers a consistent snapshot and complete post-snapshot delta before epoch-fenced ownership changes.
- Secondary indexes, uniqueness, foreign keys, transactions, and change streams declare local versus cross-shard semantics.
- Rebalancing accounts for state-transfer bandwidth, write amplification, quorum health, and retained history.
- Hot-key mitigation preserves deterministic read/write routing and semantic identity.
- Capacity reserves tolerate the declared node/zone failure while repair and movement occur.

### Common failures

Failures include choosing a monotonically increasing leading range key for a high insert rate; assuming random hashes balance tenant workload; changing a modulo shard count and remapping nearly every key; caching directory entries without epoch checks; dual-writing old and new shards without atomicity or idempotence; deleting the source before destination catch-up/verification; placing three replicas on one rack or storage system; moving too many replicas simultaneously and losing quorum; scattering every query because indexes ignore the shard key; enforcing “global” uniqueness only per shard; splitting a single hot key that cannot be subdivided; violating residency during repair; and measuring only bytes while CPU, QPS, indexes, or transaction coordination saturate.

### Compact example

Ranges `[0,100)`, `[100,250)`, and `[250,1000)` cover integer keyspace `[0,1000)` without overlap. Key 99 routes to the first, key 100 to the second, and key 999 to the third. Splitting `[250,1000)` at 600 creates `[250,600)` and `[600,1000)` under a new epoch; only the upper 400-key interval changes owner if the lower child retains the old group. A replica set in zones z1/z2/z3 survives one zone loss under the assumed independent zones; three nodes in z1 do not.

### Connections

Retrieve [Physical Replication](081-physical-replication.md), [Logical Replication](082-logical-replication.md), [Replication Lag and Stale Reads](084-replication-lag-and-stale-reads.md), and [Leader Election and Failover](085-leader-election-and-failover.md). Continue through [the program roadmap](../ROADMAP.md) to distributed transactions, consensus-backed replication, global transactions, and consistency/latency/availability evaluation.

## Governing Question

A single database server can be too small because data, read/write rate, CPU, memory, I/O, connections, or maintenance work exceed one machine. Sharding creates parallel ownership units. The key choice determines which operations remain local, where hotspots form, how much metadata clients need, and how expensive it is to move or join data.

Partitioning and placement are separate. A tenant may map to shard 42, while shard 42 has replicas in three zones and a leader near its writers. Repartitioning changes which keys belong together; rebalancing changes where existing units live. Confusing them leads to migrations that solve storage balance but not a hot key, or spread data while violating transaction locality.

## Why This Matters

Good sharding allows incremental capacity, fault isolation, parallel queries, locality, and maintenance on bounded units. Bad sharding embeds permanent coordination into ordinary requests. A sequential key can direct all new writes to one range. A tenant-first key can colocate transactions but trap a very large tenant in one unit. Hashing can spread writes yet turn ordered scans into all-shard operations.

Movement is unavoidable: tenants grow, nodes fail, regions change, hardware ages, compliance policy evolves, and load shifts. Online resharding is a distributed state transition operating concurrently with writes. “Copy rows and update the router” is not sufficient; it needs a consistent cut, delta capture, authority epochs, rollback, and verification.

Current Google Spanner documentation describes range-based splits and warns that monotonically increasing leading keys can create insert hotspots; current CockroachDB documentation describes data ranges, replica/lease placement, locality, and load-aware movement. These are version-sensitive implementations checked on 2026-09-05. The durable principles come from range partitioning, consistent hashing, workload-aware partitioning, replication, and transaction theory.

## Prerequisites and Retrieval

Retrieve these ideas:

- a primary/partition key has identity, ordering, collation, encoding, and mutability semantics;
- B-tree/range indexes support ordered locality while hashing destroys order but can spread keys;
- replication creates several physical copies of one authoritative shard and requires leader/election/fencing rules;
- a transaction spanning shards needs a distributed atomicity/ordering protocol or weaker application semantics;
- query planning uses predicates to prune partitions and must know routing metadata;
- secondary indexes can be local to a shard or globally partitioned with maintenance cost;
- snapshots plus ordered logs can move a consistent state across concurrent updates;
- source and destination acknowledgements, apply, visibility, and deletion are different frontiers;
- failure domains and residency policies constrain candidate placements;
- capacity planning must preserve headroom for failure repair, compaction, checkpoints, and movement.

This module owns partition units, routing, placement, and movement. DBE-087 owns distributed transaction commit; DBE-088 owns consensus-backed replication inside/between shard groups.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish partitioning, replication, placement, routing, and rebalancing;
2. compare range, hash, consistent-hash, directory, and composite strategies;
3. choose keys from workload locality, cardinality, skew, growth, and query requirements;
4. express replica/leader placement as hard constraints plus optimization goals;
5. design epoch-safe online split, merge, and move protocols;
6. reason about local/global indexes, constraints, joins, transactions, and change streams;
7. diagnose hot ranges, hot keys, noisy tenants, and correlated placement failures;
8. validate coverage, ownership, migration, failure survival, performance, and residency.

## Core Exposition

**Define the unit and authority.** Choose a logical keyspace K and a deterministic mapping $P_e(k)$ for partition epoch e. The mapping may be computed (hash/modulo), interval-based, or looked up in a directory. Each result names an authoritative shard ID; a separate placement record maps that shard to a replication group and leader/lease epoch.

Keep stable logical shard identity apart from current node addresses. Clients route by shard/directory metadata, then the owner validates the epoch. A stale client receives a bounded redirect containing a newer epoch or refreshes from an authoritative directory. The old owner must reject mutations after cutover even if a cache still points to it.

**Range sharding.** Ordered, nonoverlapping intervals preserve locality for scans, prefix queries, and related composite keys. Splitting one hot/large range can move a bounded interval. Boundaries must follow the database's exact byte collation/encoding; human-looking order can differ from encoded order.

Sequential timestamps or increasing IDs concentrate inserts at the last range. Automatic splitting helps only if the hot interval contains enough distinct keys and movement reacts faster than growth. A single hot key or row remains indivisible without changing the data/operation model.

**Hash sharding.** A stable hash distributes sufficiently varied keys across buckets, reducing monotonic edge hotspots. It sacrifices ordered locality: a time-range query without the hash prefix may contact every bucket. Uniform key counts do not imply uniform load if a celebrity tenant/key dominates.

Simple `hash(key) mod N` remaps most keys when N changes. Consistent hashing and rendezvous/jump-style methods reduce expected movement under membership changes, especially with virtual partitions. They do not remove the need for one authoritative membership epoch, bounded load, replication placement, state transfer, or hot-key controls. In databases, fixed logical buckets mapped by a directory can separate key mapping stability from physical node count.

**Directory/list sharding.** An explicit map assigns tenants, countries, accounts, or ranges to shards. It supports residency, bespoke placement, and moving one tenant without changing a hash function. The directory is critical metadata: it needs consistency, availability, versioning, cache invalidation, backup, and recovery. A directory lookup on every request adds latency; cache it with epochs and owner-side validation.

Hybrid designs are common. Use tenant ID as a directory/range prefix for transaction locality, then hash or range by entity/time within large tenants. Keep small tenants grouped in shared shards and graduate large tenants to dedicated subshards. Define the transition so an entity cannot exist under two writable maps.

**Model the workload.** Inventory point reads/writes, range scans, tenant transactions, joins, aggregates, secondary lookups, bulk loads, retention deletes, change capture, and maintenance. For each, record key distribution, QPS, bytes, CPU/I/O cost, transaction conflicts, latency/locality, growth, and diurnal/regional pattern.

Optimize for the bottleneck that matters. Balance can be measured by bytes, rows, QPS, write bandwidth, CPU, memory, lock contention, index amplification, or tail latency. A vector objective with hard limits is better than one average. Preserve headroom for the loss of the largest allowed failure domain.

**Choose locality deliberately.** Put data accessed/updated together under a common leading key when doing so avoids distributed transactions and joins. Tenant-first placement makes tenant operations local and eases deletion/export, but a giant/noisy tenant needs subdivision. Time-first placement supports global recent scans but creates an insertion edge and scatters tenant history.

Composite-key order is an API to placement. `(tenant, order_time, order_id)` colocates a tenant and preserves its time scans; `(hash(order_id), order_time)` spreads writes but fans out tenant scans. Secondary indexes may restore access paths at storage and write/transaction cost.

**Design indexes and constraints.** A local secondary index includes the shard key and is maintained with the base row in one shard/transaction. A global secondary index has its own partitioning and can turn one row mutation into a cross-shard transaction or asynchronous index update. State its consistency and failure behavior.

Global uniqueness cannot be proven by independent per-shard unique indexes unless the unique value determines the shard. Options include shard by the unique key, a globally coordinated index, reservation service, probabilistic identifiers with collision handling, or scoped uniqueness. Foreign keys and materialized aggregates need equivalent ownership decisions.

**Place replicas under constraints.** For each shard specify replication factor, allowed/forbidden regions, minimum distinct zones/racks/hosts/storage systems, storage class, encryption/key boundary, version compatibility, and leader/lease preferences. Hard constraints determine legality; soft goals minimize latency, cost, imbalance, and movement.

Count failure domains, not process replicas. A placement `[n1:z1,n2:z2,n3:z3]` can survive one zone loss under independent-node/storage assumptions; three nodes in z1 cannot. The leader near writers reduces request latency, while quorum replicas must still satisfy survival/residency. Read replicas may have different roles and must not be counted for write quorum without protocol membership.

**Split and merge safely.** To split parent interval `[a,c)` at b, create children `[a,b)` and `[b,c)` with inherited consistent state and replication. Establish a cut position, copy/initialize both child states, route or buffer concurrent deltas, and commit one metadata epoch that replaces the parent. The authority layer rejects stale parent writes after cutover.

A merge reverses the boundary but can increase blast radius and create a hot unit. Ensure histories and schema are compatible, drain/coordinate operations, install combined state, atomically replace both children in the directory, and retain redirects/tombstones until stale routers expire safely.

**Move with snapshot plus delta.** Select a source snapshot at position p, transfer and verify it at destination, retain/capture all ordered changes after p, apply through cut frontier q, validate constraints/checksums/counts, install destination replicas and leader eligibility, then atomically update metadata/fence the source in epoch e+1. Forward/reject late stale requests with their idempotency identity.

Do not delete source data immediately. Retain it read-only for a bounded rollback/reconciliation interval, but make one authority explicit. If the destination fails before cutover, discard/restart it. After it accepts authoritative writes, rollback is a new reverse move or restore—not merely switching a pointer to stale source state.

**Avoid uncoordinated dual writes.** Writing old and new shards from the application creates partial-success ambiguity, ordering divergence, and retry duplication. Prefer source log capture plus idempotent destination apply, or a database protocol that atomically fences/cuts ownership. If dual writing is unavoidable, define transaction IDs, per-key ordering, conflict policy, durable repair log, and which copy is authoritative at every instant.

**Control movement.** Rebalancing consumes source reads, network, destination writes, log retention, compaction, cache warmup, and quorum changes. Limit concurrent moves per node, shard, zone, and link. Do not remove an old replica until the new one has caught up and entered the replication configuration through its safe membership protocol. Schedule around backups/checkpoints and reserve emergency repair bandwidth.

Movement can chase noise. Use hysteresis, minimum residence time, benefit-versus-cost thresholds, and forecasts. Separate urgent constraint repair from optional balance. A hot shard might need query/index/schema changes, rate limiting, caching, or key subdivision rather than another move.

**Handle hot keys and tenants.** Replication spreads reads but a single-writer key still serializes writes. Techniques include semantic decomposition (per-account subledgers with later aggregation), escrow/commutative counters, bucketing by time or salt, application rate limits, caching, or changing the invariant. Salting adds read fan-out and makes uniqueness/range operations harder. Preserve exactness requirements; do not shard a balance by adding sums if overdraft checks require coordination.

For noisy tenants, enforce per-tenant QPS/concurrency/storage quotas, isolate large tenants, and monitor skew percentiles. Migration should not let a large tenant monopolize movement bandwidth or retained log.

**Plan cross-shard operations.** The router/query planner prunes shards from predicates. Missing shard keys can require scatter/gather, with fan-out tail latency, partial failures, duplicated work, and memory limits. Push filters/aggregates down, bound fan-out, use top-k merge correctly, and define snapshot consistency across shards.

Transactions spanning shards require DBE-087's commit protocol; merely contacting both leaders does not provide atomicity. Resharding can turn formerly local transactions into distributed ones, so migration plans must measure coordination rate before cutover.

**Protect metadata and streams.** Routing directories, shard epochs, placement constraints, replica memberships, and movement state are critical data. Replicate, audit, back up, and recover them. A data shard must validate directory epochs even if control metadata is temporarily unavailable.

Change streams need stable logical identities across movement. Include shard/partition epoch and source transaction identity, suppress duplicates at cutover, and maintain an end-to-end watermark that accounts for old and new units. Consumers should not interpret a split as data deletion/reinsertion unless the contract says so.

**Validate adversarially.** Enumerate keys at every lower/upper boundary; use property tests for total coverage and no overlap; compare router and owner decisions across epochs. Generate skewed Zipf-like workloads, sequential inserts, hot tenants/keys, large rows, cross-shard transactions, scans, indexes, and deletes.

Cut source/destination/router/directory/network/storage before and after snapshot, delta capture, catch-up, metadata commit, fence, and source deletion. Lose a node/zone during movement. Inject stale directory caches, duplicate deltas, boundary key updates, insufficient disk, corrupted copies, incompatible schemas, residency constraints, and concurrent split/move. Oracles compare every key/value/version, uniqueness/foreign-key scope, transaction outcomes, stream identities, placement constraints, and one current owner.

The finite executable model below checks interval coverage/routing, splits one interval, and evaluates zone diversity for two replica sets. It models integer intervals only; it does not implement a directory, database, replication, consensus, movement, failure, or workload optimizer.

<!-- bijux-verify: {"id":"finite-shard-map-and-placement","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"coverage_before=true\nroute_0=s0\nroute_99=s0\nroute_100=s1\nroute_999=s2\ncoverage_after=true\nroute_599=s2a\nroute_600=s2b\nroute_700=s2b\nmoved_interval_width=400\ns0_distinct_zones=3\ns0_survives_one_zone=true\ns1_distinct_zones=1\ns1_survives_one_zone=false\nevidence=finite_shard_map_and_placement\n","stderr":""}} -->
```python
def complete_nonoverlapping(ranges, start, end):
    ordered = sorted(ranges)
    return (ordered[0][0] == start and ordered[-1][1] == end
            and all(ordered[i][1] == ordered[i + 1][0]
                    for i in range(len(ordered) - 1)))

def route(ranges, key):
    matches = [name for lower, upper, name in ranges if lower <= key < upper]
    if len(matches) != 1:
        raise ValueError("key must have exactly one owner")
    return matches[0]

before = [(0, 100, "s0"), (100, 250, "s1"), (250, 1000, "s2")]
after = [(0, 100, "s0"), (100, 250, "s1"),
         (250, 600, "s2a"), (600, 1000, "s2b")]
zones = {"s0": ["z1", "z2", "z3"], "s1": ["z1", "z1", "z1"]}

print(f"coverage_before={str(complete_nonoverlapping(before, 0, 1000)).lower()}")
for key in (0, 99, 100, 999):
    print(f"route_{key}={route(before, key)}")
print(f"coverage_after={str(complete_nonoverlapping(after, 0, 1000)).lower()}")
for key in (599, 600, 700):
    print(f"route_{key}={route(after, key)}")
print("moved_interval_width=400")
for shard in ("s0", "s1"):
    distinct = len(set(zones[shard]))
    print(f"{shard}_distinct_zones={distinct}")
    print(f"{shard}_survives_one_zone={str(distinct >= 2).lower()}")
print("evidence=finite_shard_map_and_placement")
```

## Definitions and Notation

- $K$: logical keyspace with a defined encoding and order where relevant.
- $P_e(k)$: partition function/directory mapping key k under metadata epoch e.
- $I_i=[a_i,b_i)$: half-open interval owned by range shard i.
- $R_i$: replica set for shard i.
- $L_i$: leader/leaseholder placement for shard i.
- **Partition epoch:** version of key-to-shard boundaries/mapping.
- **Placement epoch:** version of shard-to-replica/leader assignments.
- **Virtual partition:** stable logical bucket decoupling key mapping from physical nodes.
- **Hard constraint:** placement condition that may never be violated, such as residency.
- **Soft objective:** quantity optimized when legal placements exist, such as latency or movement cost.
- **Authority cut:** instant/epoch transition after which only the new owner accepts mutations.
- **Hot shard:** unit whose aggregate load exceeds capacity.
- **Hot key:** indivisible key whose load can exceed one shard's useful capacity.

## Mechanisms, Invariants, or Proof Structure

**Coverage invariant.** Sorted half-open intervals cover K exactly when the first lower bound equals K's start, each interval upper bound equals the next lower bound, and the last upper bound equals K's end. Half-open boundaries assign key b to the right interval exactly once. Encoded comparison semantics are part of the premise.

**Split preservation.** Replacing parent `[a,c)` by `[a,b)` and `[b,c)` for $a<b<c$ preserves union and disjointness. Data correctness additionally requires that every version/event be assigned by key and cut epoch, and that one authority accepts each mutation.

**Move safety.** Given a source-consistent snapshot at p, complete ordered idempotent delta `(p,q]`, verified destination state through q, and an atomic epoch/fence cut, destination state equals the source's declared projection through q and only destination accepts later writes. Missing delta, non-idempotent duplicate, or overlapping authority breaks the conclusion.

**Placement survival.** A replica set tolerates one failure domain D only if after removing every one D-domain it retains the protocol's required members/data and a promotable leader. Distinct process/node counts do not imply distinct domains or quorum survival.

**Balance counterexample.** Uniform hashing distributes keys in expectation, but if request probabilities are skewed, expected load per bucket depends on weighted key popularity. One hot key remains hot regardless of balanced key counts, so key uniformity cannot prove request/CPU balance.

## Alternatives and Trade-Offs

| Strategy | Strength | Cost or risk | Best fit |
| --- | --- | --- | --- |
| Ordered ranges | scans, locality, bounded splits | edge hotspots and skew | ordered access and adaptive ranges |
| Fixed hash buckets | write distribution, stable virtual units | scatter for ranges | point access with many keys |
| Modulo physical nodes | trivial computation | massive remap when N changes | rarely durable database design |
| Consistent/rendezvous hashing | reduced membership movement | probabilistic balance and metadata epoch | key-value placement |
| Directory by tenant/key | explicit moves and residency | critical lookup metadata | heterogeneous tenants/policy |
| Tenant-prefix range | transaction and export locality | giant/noisy tenant hotspot | mostly tenant-local workloads |
| Hash prefix + ordered suffix | spreads inserts | read fan-out across buckets | high-write time data |
| Local secondary index | atomic/local maintenance | requires shard-key access | shard-scoped queries |
| Global secondary index | alternate global lookup | cross-shard consistency/write cost | necessary global access paths |
| Automatic load split | adapts to observed ranges | reaction delay/thrashing | divisible range hotspots |
| Dedicated tenant shard | isolation and policy control | fragmentation/idle capacity | large or regulated tenants |

## Failure Modes and Misconceptions

- **“Sharding means replication.”** Partitioning divides authority; replication copies each authority unit.
- **“Uniform keys mean uniform load.”** Popularity, row size, indexes, and transaction cost can remain skewed.
- **“Hashing solves every hotspot.”** One hot key remains indivisible and ordered queries fan out.
- **“A sequential key is harmless because ranges auto-split.”** All new writes can chase the newest edge faster than splitting/movement.
- **“Modulo makes scaling easy.”** Changing N remaps most keys and creates a full migration.
- **“The router is authoritative.”** Owners must validate epochs because caches and retries are stale.
- **“Dual writing keeps copies synchronized.”** Partial success and ordering need an explicit protocol.
- **“Copied means movable.”** Snapshot, delta, integrity, readiness, authority cut, and source retention remain.
- **“Three replicas survive a zone.”** They may share one zone/storage/power domain.
- **“Global unique means a unique index on each shard.”** Independent local constraints allow cross-shard duplicates.
- **“Rebalancing is free background work.”** It consumes I/O, network, log retention, compaction, cache, and quorum budget.
- **“A split fixes a hot key.”** Both children cannot divide one logical key without semantic redesign.
- **“Scatter/gather scales with nodes.”** Fan-out increases tail and partial-failure exposure.
- **“Rollback is pointer reversal.”** Once the destination accepts writes, the old source is stale.

## Worked Examples

### Example 1

**Situation.** Intervals `[0,100)`, `[100,250)`, `[250,1000)` serve integer keys `[0,1000)`.

**Reasoning.** The first starts at 0, consecutive boundaries meet, and the last ends at 1000. Half-open semantics route 99 left, 100 to the second, and 999 to the third. Adding `[90,110)` creates overlap; changing the second lower bound to 101 creates a hole at 100.

**Conclusion.** Boundary convention plus adjacency checks prove structural coverage for the modeled keyspace.

### Example 2

**Situation.** A high-rate events table uses increasing timestamp as its leading range key.

**Reasoning.** Every new insert targets the rightmost interval. Splitting produces a new rightmost child that immediately receives subsequent writes, so old children cool while one remains hot. Add a stable hash/tenant prefix, pre-split a known key distribution, or change ingestion/aggregation—accepting that time scans now contact multiple prefixes.

**Conclusion.** Monotonic leading keys create a moving-edge hotspot despite total cluster capacity.

### Example 3

**Situation.** One million keys hash evenly across 100 buckets, but key `celebrity` produces 40% of writes.

**Reasoning.** Key-count balance says about 10,000 keys per bucket; the celebrity bucket still receives at least 40% of writes. Virtual nodes or more buckets cannot split one key. Semantic subkeys, commutative aggregation, caching, or rate limits are required.

**Conclusion.** Uniform hashing balances numerous independent keys, not indivisible hot-key demand.

### Example 4

**Situation.** A cluster changes routing from `hash(k) mod 4` to `hash(k) mod 5`.

**Reasoning.** A key remains only when its hash has equal residues modulo 4 and 5; for broadly distributed hashes, most keys change buckets. Use stable virtual buckets mapped to nodes or a consistent-hash/rendezvous scheme, then move only reassigned buckets under a controlled epoch.

**Conclusion.** Modulo physical node count couples scaling to near-global remapping.

### Example 5

**Situation.** Shard s has replicas n1/z1, n2/z1, n3/z1 with replication factor three.

**Reasoning.** Three process/node copies survive some individual node failures, but one zone failure removes all. A one-zone objective needs replicas placed across enough independent zones and a quorum/leader rule that remains satisfiable after removing any one.

**Conclusion.** Replica count without failure-domain diversity is a misleading availability measure.

### Example 6

**Situation.** Move shard `[250,1000)` using snapshot at position 80 while writes continue through 100.

**Reasoning.** Copy/verify snapshot 80, retain and apply every ordered delta 81–100 idempotently, then establish cut q=100. Commit destination ownership in epoch e+1 and make old owner reject/forward mutations bearing e. Keep old data read-only until validation/rollback window closes.

**Conclusion.** Snapshot plus complete delta and one epoch-fenced cut supports online movement.

### Example 7

**Situation.** Usernames must be globally unique, but rows are sharded by tenant.

**Reasoning.** Per-tenant indexes permit the same username in different shards. If global uniqueness is real, maintain a globally partitioned reservation/index keyed by normalized username in the same distributed transaction, shard users by username, or change the contract to tenant-scoped uniqueness. Normalize/collate identically.

**Conclusion.** Constraint scope must align with partition ownership or use coordination.

### Example 8

**Situation.** A query requests a tenant's orders by time, but data is hash-sharded only by order ID across 64 buckets.

**Reasoning.** Without an index keyed by tenant/time, the planner contacts all 64 shards, pays their tail/partial-failure cost, and merges/sorts results. A tenant-prefix range or global tenant/time index reduces fan-out at the cost of locality hotspot or cross-shard index maintenance.

**Conclusion.** Partition keys determine query fan-out; secondary access paths move rather than erase cost.

### Example 9

**Situation.** A stale router sends a write for key 700 to old shard s2 after epoch e+1 split it into s2a/s2b.

**Reasoning.** Old s2 checks epoch and rejects or forwards to s2b with the newer metadata version; it must not accept authority. The client refreshes and retries using the same transaction/idempotency identity. A time-only cache TTL cannot guarantee absence of stale requests.

**Conclusion.** Owner-side epoch enforcement makes stale routing safe.

### Example 10

**Situation.** The balancer schedules every replica of 20 shards away from node n1 simultaneously before replacement replicas catch up.

**Reasoning.** Network/disk/log retention spike, several groups can lose quorum on another failure, and source deletion can remove the only current copy. Limit concurrent transfers, add/catch up/verify one replica, change membership safely, then remove the old replica; reserve bandwidth and quorum capacity for an overlapping failure.

**Conclusion.** Rebalancing must preserve replication safety and failure headroom at each intermediate state.

## Cross-Program Connections

- Distributed Systems owns consistent hashing, membership, replication groups, consensus, partial failure, and distributed metadata foundations; this module applies them to database key/transaction/query semantics.
- Data Architecture Engineering owns domain boundaries, residency, tenant identity, lineage, and global/local semantic constraints that should shape shard keys.
- Data Engineering owns downstream partitioning, watermarks, and skew handling; database resharding must preserve stable change identities for those consumers.
- Algorithm Engineering owns partitioning, bin packing, graph cuts, load balancing, and optimization; practical placement combines hard constraints with heuristic objectives.
- Platform Engineering owns node/zone inventory, service discovery, resource quotas, and movement orchestration; the database remains authority for shard epochs and safe ownership.
- Security Engineering owns residency, isolation, encryption keys, privileged metadata, and tenant deletion/export requirements embedded in placement.

## References

1. David Karger, Eric Lehman, Tom Leighton, Matthew Levine, Daniel Lewin, and Rina Panigrahy. [Consistent Hashing and Random Trees](https://people.csail.mit.edu/karger/Papers/web.pdf). ACM STOC, 1997. Minimal-disruption distributed mapping foundations.
2. Giuseppe DeCandia et al. [Dynamo: Amazon's Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf). ACM SOSP, 2007. Consistent hashing, virtual nodes, replication, and operational partitioning.
3. Fay Chang et al. [Bigtable: A Distributed Storage System for Structured Data](https://research.google.com/archive/bigtable-osdi06.pdf). USENIX OSDI, 2006. Ordered row ranges/tablets, splitting, metadata, and assignment.
4. James C. Corbett et al. [Spanner: Google's Globally-Distributed Database](https://research.google.com/archive/spanner-osdi2012.pdf). USENIX OSDI, 2012. Directories, placement, replication groups, and data movement.
5. Carlo Curino et al. [Schism: A Workload-Driven Approach to Database Replication and Partitioning](https://www.vldb.org/pvldb/vol3/R04.pdf). PVLDB 3, 2010. Workload-aware graph partitioning and distributed-transaction minimization.
6. Google Cloud. [Spanner Schema Design Best Practices](https://cloud.google.com/spanner/docs/schema-design). Current range-split, monotonic-key hotspot, hash-prefix, and locality guidance checked 2026-09-05.
7. Google Cloud. [Spanner Schema and Data Model](https://cloud.google.com/spanner/docs/schema-and-data-model). Current split boundaries, load-based splitting, and key locality behavior checked 2026-09-05.
8. Cockroach Labs. [CockroachDB Stable: Architecture Overview](https://www.cockroachlabs.com/docs/stable/architecture/overview) and [Replication Layer](https://www.cockroachlabs.com/docs/stable/architecture/replication-layer). Current range, replica, leaseholder, and locality concepts checked 2026-09-05.
9. Alexander Thomson et al. “Calvin: Fast Distributed Transactions for Partitioned Database Systems.” ACM SIGMOD, 2012. Partitioned transaction scheduling and deterministic coordination perspective.
10. Martin Kleppmann. *Designing Data-Intensive Applications*. O'Reilly, 2017. Partitioning, hotspots, rebalancing, routing, and secondary-index foundations.

## Exercises

### Exercise 1

Distinguish partitioning, placement, replication, and routing. Explain why changing a shard's leader is not necessarily resharding.

### Exercise 2

Verify coverage for `[0,20)`, `[20,55)`, `[55,100)`. Split the middle interval at 40 and show the new mapping for keys 19, 20, 39, 40, 54, and 55. State the authority invariant during cutover.

### Exercise 3

A database is sharded by `timestamp mod 16`, uses application dual writes during movement, enforces email uniqueness locally, and places three replicas on nodes backed by one storage array. Diagnose at least six independent design defects and corrective directions.

### Exercise 4

Compare tenant-prefix range sharding with hash-by-entity sharding for a SaaS workload containing tenant-local transactions, a few huge tenants, global reporting, legal residency, and bursty event ingestion. Recommend a hybrid and state its costs.

### Exercise 5

Design an online move of a 2 TiB shard between regions while writes continue. Include eligibility/capacity, snapshot and delta positions, routing epochs, fencing, replication membership, residency, bandwidth controls, verification, client retries, change streams, rollback, source deletion, and failure injection.

## Answers to the Exercises

### Answer 1

**Partitioning** maps logical keys/rows to authoritative shard units. **Placement** maps a shard's replicas and leader/lease to physical nodes/failure domains. **Replication** maintains multiple copies of one shard's ordered state. **Routing** directs a request to the current shard/replica using versioned metadata. Moving leadership among existing replicas changes placement/authority but not which keys belong to the shard, so it is not resharding. Splitting, merging, or changing the key-to-shard mapping is resharding even if all resulting units initially stay on the same nodes.

### Answer 2

The intervals start at 0, adjacent upper/lower bounds match (20 and 55), end at 100, and are half-open, so they cover `[0,100)` once. Replace `[20,55)` with `[20,40)` and `[40,55)`. Key 19 maps to `[0,20)`; 20 and 39 to `[20,40)`; 40 and 54 to `[40,55)`; 55 to `[55,100)`. During cutover, every key has exactly one authoritative owner in the active epoch. Old-parent and new-child maps cannot both accept mutations; stale requests are rejected/redirected with stable retry identity.

### Answer 3

`timestamp mod 16` is not ordinary time-range locality and its exact language/time representation may be unstable; if it means hash/bucket by a small timestamp residue, it can skew periodically and forces range queries across buckets. Sixteen fixed buckets may cap parallelism or create expensive future remapping if confused with physical nodes. Application dual writes permit partial success, reordering, and ambiguous retries. Local email indexes allow cross-shard duplicates. Three nodes on one storage array do not survive array failure. The design also lacks routing epochs/owner fencing, snapshot-plus-delta movement, and declared global-index transaction semantics.

Use a stable canonical partition key, perhaps tenant/directory prefix plus hashed event subbucket and ordered time suffix. Keep virtual shards independent of node count. Move through one authoritative source snapshot/log and epoch-fenced cut. Implement global normalized-email reservation in a coordinated index or change uniqueness scope. Place replicas across independent storage/zone domains and validate quorum survival. Add versioned routing, idempotent transaction identities, workload/skew metrics, and explicit query fan-out.

### Answer 4

Tenant-prefix ranges colocate tenant transactions, simplify residency/export/deletion, and enable tenant time scans, but huge tenants and bursty sequential suffixes can hotspot; global reporting fans out. Hash-by-entity spreads many independent writes and accommodates uniform point access, but tenant transactions, scans, deletion, and residency need scatter/gather or a directory/global index.

A hybrid uses a directory mapping each tenant to a residency region and shard policy. Small tenants share range groups keyed `(tenant_id, entity/time)`. Large tenants graduate to multiple stable virtual subshards selected by a hash of entity ID, with time as a suffix; exceptionally hot entities need semantic subkeys/rate controls. Local indexes serve tenant operations; asynchronous analytical exports or a governed global index serve global reporting. Costs include directory consistency, migration state, extra buckets/fan-out for large-tenant scans, distributed transactions across subshards, index/change-stream coordination, and capacity reserved per region.

### Answer 5

First verify destination residency, encryption keys, schema/version, 2 TiB plus index/log headroom, failure-domain/quorum capacity, network budget, and source retention; throttle other moves. Add destination replicas without removing source quorum members. Establish source-consistent snapshot at p, stream/copy in chunks with manifests/checksums, and capture every ordered delta after p. Apply idempotently while tracking per-range/transaction gaps and an end-to-end change-stream identity.

When destination reaches cut candidate q, quiesce only if needed to close the final delta, verify row/key/value/version digests, indexes, constraints, samples, transaction frontiers, replica integrity, and read behavior. Commit a new partition/placement epoch through the authoritative directory and install a fence so old owners reject/forward all e-era writes; reset/redirect cached routers using stable request IDs. Change replication membership through its safe joint/add-catch-up-remove protocol and elect/place the destination leader only after eligibility.

Limit transfer bandwidth/concurrency and monitor application latency, retained log, disk, apply rate, and time to capacity. Preserve legal residency throughout temporary copies and erase unauthorized staging if aborted. Before cutover, rollback discards/restarts the destination. After authoritative destination writes, rollback is a new reverse move, not pointer reversal. Keep source read-only for a bounded audited recovery window, then delete only after stale-router bounds, backup/change-consumer watermarks, and verification pass.

Inject source/destination/node/zone/network/directory/router failures before and after p, catch-up, q, epoch commit, fence, membership changes, and deletion; test full disks, corruption, duplicate/gapped deltas, boundary-key writes, stale clients, and another replica loss. The oracle proves total nonoverlapping coverage, one writable owner, complete values/versions/transactions, valid replica placement, stable change IDs/no missing events, and documented client outcomes at every cut.
