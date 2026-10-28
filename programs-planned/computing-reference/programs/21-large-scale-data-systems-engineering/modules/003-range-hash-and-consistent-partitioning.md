---
module_id: LSDS-003
program: Large-Scale Data Systems Engineering
level: 1
module_number: 3
title: Range, Hash, and Consistent Partitioning
status: complete
last_verified: 2026-09-03
---

# Range, Hash, and Consistent Partitioning

## One-Page Review

### Governing question

How should an engineer choose and evolve a partition function when ordered access, balance, membership change, locality, and operational safety pull in different directions?

### Essential definitions

- **Range partitioning** assigns ordered key intervals to logical partitions.
- **Hash partitioning** hashes a canonical key and maps the result into a fixed logical bucket space.
- **Consistent hashing** is a family of hash-based mappings designed to limit reassignment when the destination set changes.
- A **token** is a position in a hash space; a **virtual node** gives one physical node several token positions or ranges.
- A **hash slot** is a stable logical bucket that can be placed independently of the hash computation.
- **Rendezvous hashing** selects the destination with the highest deterministic key-destination score.
- **Churn** is the fraction or weighted load of keys whose assignment changes across map versions.
- A **hot key** is an indivisible key whose work exceeds a destination's safe capacity.

### Central model, mechanism, or theorem

A partition design is the tuple `P=(K,C,F,L,O,R,M,W,E)`: key domain `K`; canonicalization `C`; versioned partition function `F`; stable logical units `L`; ownership/placement `O`; replica and failure-domain policy `R`; migration protocol `M`; workload model `W`; and retained evidence `E`.

For ordered boundaries `b_0 < ... < b_m`, range partition `i` owns `b_i <= k < b_(i+1)`. Fixed hash partitioning commonly uses `h(C(k)) mod m`. In an ideal equal-capacity consistent mapping, adding one of `n+1` destinations gives the newcomer about `1/(n+1)` of keys and leaves other assignments stable in expectation. That probabilistic movement property is not a guarantee of even load, locality, availability, or safe migration.

### Critical invariants

- Canonical key bytes and partition-function version are identical at every router and owner.
- Every valid key maps to exactly one primary logical unit for an active epoch.
- Range boundaries are ordered, adjacent under the declared domain, and have explicit endpoint semantics.
- Hash algorithms, seeds, integer widths, encoding, and bucket identities are durable protocol fields.
- Ownership and replica placement are separate from logical key assignment.
- An epoch transition has one defined authority for each key at every observable point.
- Churn and balance are weighted by bytes, rate, state, and cost, not key count alone.
- Hot-key and adversarial distributions are tested independently of average hash quality.

### Common failures

Frequent failures are choosing range partitioning solely for scans, treating a hash as proof of balance, binding modulo directly to machine count, using inconsistent hashes across languages, confusing a token with a node, assuming consistent hashing solves replication, moving bytes without an ownership epoch, ignoring stale routers, overusing virtual nodes, and measuring only record counts.

### Compact example

A nine-node store computes `hash(customer_id) mod 9`. Adding a tenth node changes the divisor, so most customers move. Keeping 4,096 logical slots instead lets the hash-to-slot function remain fixed while selected slots move to the new node. This reduces data movement, but one celebrity customer still occupies one slot and can remain hot.

### Connections

[LSDS-002](002-horizontal-partitioning.md) defines the logical partition contract. [LSDS-004](../ROADMAP.md) develops data locality. Range layouts connect to [Database Engineering](../../18-database-engineering/ROADMAP.md), key distribution to [Data Engineering](../../19-data-engineering/ROADMAP.md), and membership and replication to [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md).

## Governing Question

A partition function is a routing contract, not a cosmetic distribution choice. It determines which requests route directly, which scans prune, which keys share transactions or state, what moves during growth, and where skew becomes a bottleneck. Range, hash, and consistent methods optimize different properties; none dominates for all workloads.

The governing question is therefore not “which algorithm is best?” It is: which stable logical mapping fits the measured workload, and how will that mapping remain correct when keys, load, membership, software, and topology change? A defensible answer separates at least four layers:

1. canonical application key to a point in an ordered or hashed domain;
2. that point to a logical range, bucket, slot, or token interval;
3. the logical unit to a primary owner and replica set;
4. the owner to a physical node, zone, device, or process.

Collapsing these layers makes every node change look like a data-model change. Indirection allows a stable partition universe to outlive machines, while explicit epochs make reconfiguration observable and testable.

## Why This Matters

Range partitioning preserves order. An engine can route equality lookups by boundary search, prune interval predicates, stream adjacent keys in order, and split a large contiguous interval. These properties are valuable for time-series windows, ordered indexes, prefix scans, and storage engines that keep sorted data. The same order can concentrate new traffic at one edge when keys increase monotonically. A boundary plan that balances yesterday's bytes can also fail on tomorrow's writes.

Hash partitioning removes useful correlation between key order and destination. With a suitable deterministic hash and sufficiently varied keys, it often spreads distinct keys more evenly than range partitioning. Equality routing is direct. Ordered scans, prefix access, and adjacent-key locality are lost unless another structure provides them. A repeated hot key is not divided: every occurrence hashes to the same result. Hashing distributes key identities, not necessarily requests, bytes, state, or computation.

Direct modulo by the number of machines is operationally brittle. Changing `m` changes the remainder for most hash values, coupling scale-out to broad reassignment. Production systems commonly keep many logical buckets or slots and move their ownership, or use a consistent mapping whose assignment changes minimally with membership. Both introduce metadata and transition obligations absent from a one-line modulo expression.

Consistent hashing is often summarized as a ring. Hash keys and destination tokens into one circular space, then choose the first eligible token clockwise. Adding a token takes a neighboring interval instead of changing every assignment. The 1997 Karger et al. paper introduced consistency properties for distributed caching; later systems adapted the mechanism to partitioned storage. The ring is one implementation family, not the definition of every low-churn mapping.

Operational correctness dominates elegant steady-state diagrams. A new owner needs data, concurrent changes, replica placement, an authoritative epoch, and a failure-safe cutover. Routers can remain stale. A node may rejoin after isolation and claim an old range. Movement consumes the same disk and network capacity needed for foreground work and recovery. An algorithm's remapping bound says which keys should change destinations; it does not perform or validate the migration.

## Prerequisites and Retrieval

Recall from [LSDS-001](001-workloads-that-require-multiple-machines.md) that distribution is justified by measured constraints, and from [LSDS-002](002-horizontal-partitioning.md) that a primary partitioning requires total assignment, coverage, exclusivity, and version-compatible routing. You should also understand total order, modular arithmetic, deterministic hashing, probability, binary search, replication, and failure domains.

Retrieve three distinctions before continuing. First, a partition key need not uniquely identify a record. Second, a logical partition is not a physical machine. Third, balance has several dimensions: records, bytes, requests, state, CPU, storage operations, and tail latency can disagree.

## Learning Objectives

After completing this module, you should be able to:

- derive routing and pruning for nonoverlapping range boundaries;
- explain why monotonic and concentrated keys create range hotspots;
- specify a portable, versioned hash partition contract;
- quantify balance and churn across two mapping epochs;
- derive why direct modulo changes broadly when its modulus changes;
- explain ring tokens, virtual nodes, hash slots, and stable logical buckets;
- compare ring, rendezvous, jump, directory, and composite approaches;
- separate logical assignment, primary ownership, replica placement, and routing;
- design split, merge, transfer, cutover, rollback, and stale-router behavior;
- test representative, adversarial, growth, failure, and recovery scenarios;
- identify when high-consequence repartitioning requires domain and independent review.

## Core Exposition

### Range partitioning

Let canonical keys belong to a totally ordered domain. Boundaries `b_0 < b_1 < ... < b_m` define logical interval `L_i=[b_i,b_(i+1))`. The half-open convention assigns a boundary value to exactly one interval. Unbounded sentinels can cover the domain below the first or above the last finite boundary. The contract must also define nulls, invalid encodings, collation, composite-key comparison, timezone normalization, and schema evolution.

Routing one key uses predecessor or upper-bound search over the boundary index. A predicate `low <= k < high` can identify intersecting partitions without examining unrelated intervals. This makes range partitioning fit ordered scans, min/max access, merge operations, and storage formats whose statistics describe ordered key domains. Partition pruning is correct only when the query predicate and comparison semantics match the boundary contract.

Order also preserves correlations. If the leading key is an increasing timestamp or sequence, current writes target the highest interval. If one lexicographic prefix is popular, its neighborhood can become hot. Pre-splitting future intervals, reversing or hashing a leading component, using time buckets with secondary distribution, and adaptive split placement can help, but each changes routing or locality.

A range split replaces one logical interval with two or more child intervals. A safe split records parent and child identities, exact boundaries, source snapshot, concurrent-change handling, ownership epochs, validation, and rollback. Retaining the lower child under the parent's identifier can reduce movement, but that identity rule must be explicit. A merge has the inverse concerns and can recreate a hotspot if undertaken solely to reduce metadata.

Balanced bytes do not imply balanced operations. One narrow interval may receive expensive point updates; a large cold historical interval may dominate bytes but consume little CPU. Boundary selection should use weighted samples or sketches of the relevant workload, then be tested against growth and adversarial concentrations. Adaptive systems require hysteresis and movement budgets to avoid split-merge oscillation.

### Fixed hash partitioning

A fixed hash scheme computes canonical bytes `C(k)`, applies a specified hash `h`, and maps the result to a logical bucket. The familiar expression is `f(k)=h(C(k)) mod m`. Correctness depends on details frequently omitted from diagrams: text encoding, Unicode normalization, serialization, field order, type tags, hash algorithm, seed, signedness, width, overflow, endianness, and modulo semantics for negative values.

Hashing helps only when the hash input has enough distinct values and the function spreads them suitably. Ten million events for one account remain one hashed key. Low-cardinality countries cannot fill thousands of useful partitions. Large values, expensive operations, and uneven request popularity can produce resource skew even with uniform record counts. An adversary may deliberately choose collisions or concentrate a public key unless the threat model and hash choice address that risk.

Hash partitioning provides direct equality routing when the complete partition key is available. It normally destroys order: a key range can touch every bucket, adjacent values are not colocated, and global order requires a merge after distributed work. A compound design can hash a tenant while range-ordering time within the tenant's partition, or time-bucket first and hash within each bucket. Such designs preserve selected locality while accepting fan-out across the other dimension.

Direct modulo is stable while `m` is fixed. When `m` changes from 8 to 9, equality `h mod 8 = h mod 9` holds for only a minority of hash values. The exact fraction depends on the finite key set and hash outputs; broad remapping is the normal outcome. This is a placement problem when bucket identities equal machines. Decouple them by keeping `m` logical slots stable and maintaining a separate slot-to-node map.

### Consistent hashing and low-churn mappings

In a basic ring, hash-space positions wrap around. Each key position is assigned to the first destination token clockwise. Adding one token changes ownership only for the interval between its predecessor and itself; removing it transfers its interval to its successor. With ideal independent placements and equal capacity, adding one new destination to `n` existing destinations moves about `1/(n+1)` of keys to the newcomer in expectation.

A single token per physical node produces high variance because random arc lengths differ. Virtual nodes place many tokens per node, averaging several intervals and allowing capacity-weighted ownership. They also enlarge routing metadata, recovery fan-out, streaming concurrency, and the number of pieces involved in topology changes. More virtual nodes are not free and do not split an individual hot key.

Ring traversal must skip duplicate physical nodes when choosing replicas. A replication factor of three means three eligible distinct owners under a placement policy, not the next three tokens regardless of host. Rack, zone, region, device, and correlated-failure constraints belong to replica placement. The partition function proposes a primary logical location; it does not prove durability or availability.

Some systems use a fixed slot universe rather than exposing a token ring. Redis Cluster, for example, documents 16,384 hash slots and maps slots separately to nodes. Moving selected slots changes placement without changing `CRC16(key) mod 16384`. This is conceptually different from `hash(key) mod node_count`: the divisor names stable logical units, not current machines.

Rendezvous or highest-random-weight hashing computes a deterministic score for the key with each eligible destination and selects the greatest score. It provides low churn and simple weighted or ranked variants without ordered ring metadata, at the cost of evaluating destinations or using acceleration structures. Its protocol must specify the destination identity set and score hash exactly.

Jump consistent hash maps a 64-bit key to numbered buckets with small state and expected low movement when buckets are appended. The original algorithm requires bucket identities `0,...,n-1`; arbitrary removals or reordered identities need another layer or remap. Its compactness does not supply replica selection, heterogeneous weights, membership consensus, or migration.

Directory partitioning stores an explicit key/range/slot-to-owner map in a control plane. It can express capacity, topology, exceptions, splits, draining, and tenant isolation directly. The cost is authoritative metadata, caching, lookup, epoch distribution, and recovery. In practice, consistent hash calculations and directories are often combined: the algorithm selects a stable logical unit, and metadata places it.

### Choosing from the workload

Choose range partitioning when order, interval pruning, prefix locality, or range splits are central and edge or prefix hotspots can be controlled. Choose fixed hash slots when equality routing and stable, explicitly placeable units matter more than order. Choose a consistent mapping when membership changes frequently enough that low churn justifies its metadata and operational complexity. Use rendezvous when keyed ranking over a modest destination set is useful; use jump when compact ordered-bucket assignment fits the membership model.

The decision unit is not algorithm name but the whole tuple `P`. State key semantics, logical partition identity, placement, replication, migration, workload, and evidence. Two systems can both claim “consistent hashing” while differing in tokens, virtual-node count, replica walk, topology constraints, weights, epochs, routing behavior, and safety.

### Hot keys and composite strategies

A hot key sets a lower bound on maximum load under any exclusive one-key-to-one-primary mapping. Adding nodes, slots, tokens, or a better hash cannot divide it. Options include caching reads; aggregating or rate-limiting writes; splitting the key with deterministic salts; isolating the tenant; decomposing state; changing the transaction boundary; or giving the owner more capacity.

Salting transforms `k` into `(k,s)` for several subkeys. It distributes writes but requires reads or aggregates over all salts unless the caller can derive one. Random salt spreads load but makes point lookup fan out; a salt derived from record identity preserves direct item routing. Neither preserves a single serial transaction over the unsalted key without another coordination mechanism.

Time bucketing bounds state and retention units but current time can remain hot. A compound `(hash(entity), time_bucket)` key distributes entities while preserving bounded history within each entity-bucket. Reversing component order changes which predicates route directly. Explicitly trace every important read, write, join, transaction, retention action, and recovery operation through the chosen order.

### Reconfiguration and authority

Represent partition metadata with a monotonically ordered epoch or otherwise comparable configuration version. A routing decision should carry or imply the epoch used. Owners either serve, redirect with a newer epoch, or reject safely; they must not accept conflicting primary authority indefinitely. Cache refresh and retry behavior need bounds to avoid redirect loops and retry storms.

An online transfer commonly moves through states such as planned, copying, catching up, validating, cutover-ready, authoritative, draining, and retired. State names are system-specific, but the obligations persist. Capture a source snapshot or equivalent point, transfer it, replay concurrent writes and deletes in order compatible with application semantics, validate data and invariants, switch authoritative routing, drain stale work, prove recovery, and only then remove the old copy.

Dual writes are not automatically safe. One side can succeed while the other fails; retries can reorder; a delete can race a copy; readers can observe different sides; and rollback can resurrect stale state. If dual operations are used, define idempotency, sequence/version rules, reconciliation, read selection, failure recovery, and termination.

Movement should be capacity-governed. Measure bytes to stream, foreground bandwidth, compaction/write amplification, recovery reserve, replica risk, expected duration, and abort thresholds. Adding a node during an incident can worsen the incident if rebalance saturates disks or networks. Rate limiting and resumable progress are correctness-adjacent operational controls because overload can trigger further failures.

## Definitions and Notation

Let `K` be the canonical key domain and `C` the deterministic serialization. A versioned partition function `F_v:K->L_v` maps a key to one primary logical unit. Placement `O_e:L_v->N` maps that unit under ownership epoch `e` to a primary node, while replica placement `R_e(l)` yields an ordered set of eligible distinct physical nodes.

For range partitioning, ordered boundaries `B=(b_0,...,b_m)` define `F_B(k)=i` exactly when `b_i <= k < b_(i+1)`. Boundary coverage and endpoint policy must cover every eligible key exactly once.

For fixed hash partitioning, `F_m(k)=h(C(k)) mod m`, where `h`, seed, width, serialization, and modulo semantics are named protocol elements. If `m` is a stable logical slot count, changing physical ownership can change `O_e` without changing `F_m`.

For a ring with token set `T`, let `x=h(C(k))`. The primary token is the least `t in T` with `t >= x`, wrapping to the least token when none exists. A token ownership relation maps it to a physical node; replica selection walks or otherwise selects distinct topology-eligible owners.

For mapping versions `a` and `b` over observed keys `Q`, unweighted churn is `chi(a,b)=|{k in Q : F_a(k) != F_b(k)}| / |Q|`. For nonnegative workload weight `w(k)`, weighted churn divides moved weight by total weight. Balance for destination loads `W_i` can use maximum-to-mean `max(W_i)/mean(W_i)`, coefficient of variation, quantiles, and capacity-normalized utilization. Report the dimension and observation window.

The full design tuple `P=(K,C,F,L,O,R,M,W,E)` prevents a hash equation from standing in for the system. Evidence `E` includes source review, conformance vectors, distribution replays, transition simulations, fault tests, data reconciliation, performance measurements, and approvals appropriate to consequence.

## Mechanisms, Invariants, or Proof Structure

A defensible selection and transition has eight obligations.

**1. Key and comparison contract.** Define key extraction, types, canonical bytes or total ordering, invalid/null policy, stability, collation, and schema version. Cross-language implementations must pass shared conformance vectors.

**2. Assignment proof.** Show the function is total and single-valued for the declared logical universe. For ranges, prove ordered nonoverlapping coverage. For hashes, freeze algorithm, seed, width, and bucket identities.

**3. Workload fitness.** Trace equality and range reads, writes, joins, aggregates, transactions, retention, backup, and recovery. Quantify pruning, fan-out, shuffle, locality, and coordination.

**4. Distribution evidence.** Replay representative and adversarial keys. Measure records, bytes, requests, state, CPU, disk, network, and tails. Inspect heavy keys separately because aggregate histograms can hide them.

**5. Churn and capacity.** Compare current and proposed maps with both key-count and weighted churn. Estimate transfer, foreground interference, compaction, replica risk, and rollback reserve.

**6. Placement and replication.** Keep logical assignment distinct from node ownership. Verify distinct replicas, failure-domain constraints, weights, decommissioning behavior, and unavailable destinations.

**7. Epoch transition.** Specify copy/catch-up, concurrent updates, authority, stale routes, redirect/retry bounds, reconciliation, cutover, drain, rollback, cleanup, and crash recovery at every state.

**8. Retained evidence and review.** Store exact maps, versions, fixtures, measurements, decisions, and exceptions. High-consequence domains require named domain, safety, security/privacy, operations, and independent reviewers; local checks cannot substitute for them.

The executable fixture compares three precisely defined transitions over 10,000 integer keys. It is deterministic and useful for recomputation, not a benchmark or production recommendation.

<!-- bijux-verify: {"id":"partition-movement-comparison","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"modulo_moved=8917 (89.17%)\njump_moved=1135 (11.35%)\nrange_split_moved=1250 (12.50%)\nmodulo_loads_9=(1102, 1079, 1127, 1084, 1125, 1150, 1132, 1063, 1138)\njump_loads_9=(1101, 1129, 1072, 1107, 1075, 1158, 1142, 1081, 1135)\nrange_lookup_6200=r2\nrange_lookup_6800=r4\n","stderr":""}} -->
```python
from bisect import bisect_right

MASK = (1 << 64) - 1


def mix64(value):
    value = (value + 0x9E3779B97F4A7C15) & MASK
    value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & MASK
    value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & MASK
    return value ^ (value >> 31)


def modulo_partition(key, buckets):
    return mix64(key) % buckets


def jump_partition(key, buckets):
    key = mix64(key)
    previous = -1
    candidate = 0
    while candidate < buckets:
        previous = candidate
        key = (key * 2862933555777941757 + 1) & MASK
        candidate = int(
            (previous + 1) * (1 << 31) / ((key >> 33) + 1)
        )
    return previous


def moved(partitioner, before, after):
    return sum(
        partitioner(key, before) != partitioner(key, after)
        for key in range(10_000)
    )


def loads(partitioner, buckets):
    result = [0] * buckets
    for key in range(10_000):
        result[partitioner(key, buckets)] += 1
    return tuple(result)


def range_partition(key, boundaries):
    return bisect_right(boundaries, key) - 1


old_bounds = (0, 2500, 5000, 7500, 10_000)
new_bounds = (0, 2500, 5000, 6250, 7500, 10_000)
old_ids = ("r0", "r1", "r2", "r3")
new_ids = ("r0", "r1", "r2", "r4", "r3")
range_moved = sum(
    old_ids[range_partition(key, old_bounds)]
    != new_ids[range_partition(key, new_bounds)]
    for key in range(10_000)
)
modulo_moved = moved(modulo_partition, 8, 9)
jump_moved = moved(jump_partition, 8, 9)

print(f"modulo_moved={modulo_moved} ({modulo_moved / 10_000:.2%})")
print(f"jump_moved={jump_moved} ({jump_moved / 10_000:.2%})")
print(f"range_split_moved={range_moved} ({range_moved / 10_000:.2%})")
print(f"modulo_loads_9={loads(modulo_partition, 9)}")
print(f"jump_loads_9={loads(jump_partition, 9)}")
print(f"range_lookup_6200={new_ids[range_partition(6200, new_bounds)]}")
print(f"range_lookup_6800={new_ids[range_partition(6800, new_bounds)]}")
```

The observed movement applies only to these consecutive integer keys, this mixing function, these bucket counts, and this range identity convention. Jump's 11.35% is near the ideal `1/9`, but finite samples vary. The range result assumes the parent's lower child retains `r2` and only `[6250,7500)` receives new identity `r4`. The fixture does not model bytes, popular keys, replicas, failure domains, concurrency, persistence, routing caches, or transfer safety.

## Alternatives and Trade-Offs

**Range boundaries versus hash buckets.** Ranges support order, interval pruning, and targeted splits but preserve skewing correlations. Hash buckets spread varied keys and route equality but discard order and make range access fan out.

**Direct modulo versus stable slots.** Modulo by node count has minimal metadata and broad membership churn. A stable slot universe adds a placement map but permits nodes to change without rehashing every key.

**Ring tokens versus rendezvous scoring.** Rings index ordered token positions and can locate owners efficiently; virtual nodes complicate metadata and movement. Rendezvous offers simple deterministic ranking and natural failover order but naively scores every eligible destination.

**Jump hashing versus arbitrary membership.** Jump uses constant auxiliary state and appended numbered buckets. It does not directly model arbitrary node removal, weights, topology, or replicas; indirection may restore those properties at the cost of metadata.

**Algorithmic mapping versus directory lookup.** Algorithms let routers derive destinations locally from shared membership. Directories represent exceptions, ranges, weights, and transitions flexibly, but require authoritative availability, cache coherence, and recovery.

**Virtual nodes versus fixed logical partitions.** Both create more movement granularity than physical nodes. Virtual nodes arise as token positions; fixed logical partitions have durable explicit identities. Either can overproduce metadata, files, tasks, or recovery streams.

**Salting versus key locality.** Salting divides a hot key's load but fans out unsalted-key reads and combines, and can break single-key ordering or transactions. Isolation preserves key semantics but consumes dedicated capacity.

**Static versus adaptive maps.** Static maps are easy to reproduce and audit. Adaptive splitting and placement respond to observed load but require stable control, hysteresis, movement budgets, and explanations for automatic decisions.

**Uniform versus capacity-weighted placement.** Uniform placement is simple for homogeneous nodes. Weighted tokens or scores can reflect capacity, but inaccurate weights, changing bottlenecks, and correlated failures can create hidden overload.

**Locality versus low churn.** Minimizing movement during membership change does not guarantee that related keys remain together. Preserving order or co-location can be more valuable than minimizing churn for scan-, join-, or transaction-heavy workloads.

## Failure Modes and Misconceptions

1. **Range partitioning is automatically balanced.** Ordered boundaries can be balanced for one sample and hot under future growth or correlated access.
2. **Hashing eliminates skew.** It spreads distinct hash inputs; it cannot divide one repeated or oversized key.
3. **A good cryptographic-looking hash proves workload balance.** Bytes, rate, CPU, state, and popularity can remain uneven.
4. **Modulo by machine count scales cleanly.** A divisor change usually remaps most keys.
5. **Consistent hashing means zero movement.** It reduces assignment churn; the new destination still needs its share and removals move owned keys.
6. **Every low-churn algorithm is a token ring.** Rendezvous and jump hashing provide consistency properties through different mechanisms.
7. **A token is a node.** One node can own many tokens; tokens and ranges remain logical positions.
8. **More virtual nodes are always better.** They reduce placement variance while increasing metadata, streaming, repair, and operational complexity.
9. **Consistent hashing provides replication.** Replica count, topology, consistency, repair, and failure handling are separate policies.
10. **The next tokens are valid replicas.** They may belong to one physical node or one failure domain unless selection filters them.
11. **Changing a hash library is an internal refactor.** Output changes can silently remap the entire dataset.
12. **All languages serialize keys identically.** Encoding, signedness, field order, and normalization routinely diverge.
13. **Hash slots remove the need for metadata.** Routers still need current slot ownership and transition behavior.
14. **A copy digest makes cutover safe.** Concurrent mutations, deletes, authority, stale routers, retries, and rollback remain.
15. **Dual writes prevent loss.** Partial success and reordering can create divergence without idempotency and reconciliation.
16. **Key-count churn measures migration cost.** A small number of very large or hot keys can dominate bytes and risk.
17. **Adding a node always relieves overload.** Rebalancing can consume scarce network, disk, and recovery headroom.
18. **Range splits can divide any hotspot.** A single hot row/key may be unsplittable without changing the key model.
19. **Hash tags are free co-location.** They concentrate related keys and can create a hot slot.
20. **A stale router will harmlessly retry.** Unbounded redirects and retries can amplify overload or reach conflicting owners.
21. **Placement weights encode every bottleneck.** CPU, disk, network, and data size may require different weights and change over time.
22. **Uniform synthetic keys are sufficient tests.** Production correlations, low cardinality, heavy hitters, and adversarial inputs must be replayed.
23. **One map supports every operation.** Range scans, equality reads, joins, and retention can prefer incompatible layouts.
24. **Partition movement is transparent to stateful computation.** Checkpoints, offsets, ordering, and task identity can depend on boundaries.
25. **Deleting the source immediately saves cost.** It removes rollback and recovery evidence before the new owner is proven.

## Worked Examples

### Example 1

**Question:** Which range owns key `5000` under boundaries `(0,2500,5000,7500,10000)`?

**Reasoning:** Half-open intervals make `[5000,7500)` the third interval; `5000` does not remain in `[2500,5000)`.

**Conclusion:** Endpoint semantics are part of correctness.

### Example 2

**Question:** Why does a timestamp-leading range key often hotspot?

**Reasoning:** New timestamps are near the maximum, so current inserts converge on the last active range even if historical bytes are balanced.

**Conclusion:** Ordered locality preserves workload correlations, including harmful ones.

### Example 3

**Question:** Does `hash(account_id) mod 128` split a celebrity account's 60,000 requests/s?

**Reasoning:** All requests use the same canonical input and bucket. More distinct accounts may balance, but the celebrity key remains indivisible.

**Conclusion:** Hot-key treatment requires changing caching, aggregation, key granularity, or capacity.

### Example 4

**Question:** Why is changing eight modulo buckets to nine disruptive?

**Reasoning:** The equality of remainders under different divisors is uncommon across varied hash outputs. The executable fixture moved 8,917 of 10,000 keys; that observation is fixture-specific, not a theorem for every dataset.

**Conclusion:** Do not bind durable data directly to a changing node-count modulus.

### Example 5

**Question:** How do fixed hash slots change scale-out?

**Reasoning:** Keep `hash(key) mod slot_count` fixed, add the node, and reassign selected slot owners. Only keys in moved slots change physical placement.

**Conclusion:** Stable logical indirection turns membership change into controlled placement change.

### Example 6

**Question:** Why can one token per node be badly imbalanced?

**Reasoning:** Random token gaps vary. A node can inherit a long arc and much more key-space mass. Multiple dispersed tokens average intervals but add operational pieces.

**Conclusion:** Low churn and balance are distinct properties.

### Example 7

**Question:** When is rendezvous hashing attractive?

**Reasoning:** A router with the same eligible destination set can score every destination for a key, obtain a deterministic winner and ranking, and avoid ring maintenance. Large destination sets may require acceleration.

**Conclusion:** Choose the low-churn mechanism whose membership and lookup costs fit the system.

### Example 8

**Question:** A router sends epoch 41 traffic to the old owner after epoch 42 cutover. What should happen?

**Reasoning:** The old owner should follow the declared transition rule—typically reject or redirect with epoch 42—while retries remain bounded and idempotent. Accepting writes as an independent primary risks divergence.

**Conclusion:** Epoch-aware authority is part of repartitioning correctness.

### Example 9

**Question:** A range is split and both children have matching record counts. Is migration validated?

**Reasoning:** Counts can match despite substituted records, missed deletes, duplicate identities, stale versions, or broken domain invariants. Compare identities/content, concurrent-change positions, routed reads, and application constraints.

**Conclusion:** Validation is multidimensional and tied to a capture point.

### Example 10

**Question:** Can an automated checker approve repartitioning national blood-product inventory?

**Reasoning:** It can verify fixtures and system invariants, but not clinical allocation rules, cold-chain operations, emergency overrides, regional authority, privacy, degraded-network workflow, or public-safety acceptability. Named transfusion-medicine, supply-chain, safety, security/privacy, operations, distributed-systems, disaster-recovery, accessibility, and independent assurance reviewers must evaluate representative exercises and rollback evidence. No such external review is claimed here.

**Conclusion:** High-consequence partition changes require human domain and independent assurance beyond algorithms.

## Cross-Program Connections

[LSDS-002](002-horizontal-partitioning.md) supplies coverage, exclusivity, key, placement, and migration foundations. [LSDS-004](../ROADMAP.md) examines data locality, which range and composite schemes preserve differently from hashes. Later shuffle and join modules revisit partition compatibility during distributed execution.

[Database Engineering](../../18-database-engineering/ROADMAP.md) develops ordered indexes, declarative table partitioning, query pruning, and transaction implications. PostgreSQL's current documentation provides concrete range and hash table-partition semantics without implying distributed node placement.

[Data Engineering](../../19-data-engineering/ROADMAP.md) owns pipeline keys, file layouts, contracts, and repartitioning decisions. [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns cross-domain placement principles and evolution governance.

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies binary search, ordered maps, heaps, and hashing foundations. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns membership, consensus, replication, failure detection, consistency, and partial-failure reasoning that partition placement relies upon but does not create.

Current system designs illustrate combinations rather than universal recipes. Cassandra documents token-ring consistent hashing, virtual nodes, and topology-aware replicas. Redis Cluster documents fixed hash slots and configuration epochs rather than consistent hashing. Spanner documents ordered key ranges, automatic splits, and the danger of monotonic leading keys. DynamoDB documents hash-based distribution and write sharding while warning that activity, not merely key count, must be distributed.

## References

- David Karger et al., [*Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web*](https://people.csail.mit.edu/karger/Papers/web.pdf), STOC, 1997. Primary introduction of consistent hashing properties and bounds.
- Giuseppe DeCandia et al., [*Dynamo: Amazon's Highly Available Key-value Store*](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf), SOSP, 2007. Primary token, virtual-node, replication, and membership design.
- John Lamping and Eric Veach, [*A Fast, Minimal Memory, Consistent Hash Algorithm*](https://arxiv.org/abs/1406.2294), 2014. Primary jump consistent hash algorithm and movement analysis.
- David G. Thaler and Chinya V. Ravishankar, [*Using Name-Based Mappings to Increase Hit Rates*](https://www.eecs.umich.edu/techreports/cse/96/CSE-TR-316-96.pdf), 1996. Primary highest-random-weight or rendezvous mapping report.
- Apache Cassandra Project, [*Dynamo Architecture*](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html), checked 2026-09-03. Official current token-ring, virtual-node, replica, and topology documentation.
- Redis Ltd., [*Redis Cluster Specification*](https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/), checked 2026-09-03. Official current hash-slot, hash-tag, configuration-epoch, and reconfiguration specification.
- PostgreSQL Global Development Group, [*Table Partitioning*](https://www.postgresql.org/docs/current/ddl-partitioning.html), checked 2026-09-03. Official current range, list, and hash table-partition semantics.
- Google Cloud, [*Schemas Overview for Spanner*](https://cloud.google.com/spanner/docs/schema-and-data-model), checked 2026-09-03. Official current ordered-key, split, locality, and hotspot behavior.
- Google Cloud, [*Schema Design Best Practices for Spanner*](https://cloud.google.com/spanner/docs/schema-design), checked 2026-09-03. Official current monotonic-key hotspot guidance.
- Amazon Web Services, [*Best Practices for Designing and Using Partition Keys Effectively in DynamoDB*](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html), checked 2026-09-03. Official current activity-distribution and hot-key guidance.
- Amazon Web Services, [*Using Write Sharding to Distribute Workloads Evenly in DynamoDB*](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-sharding.html), checked 2026-09-03. Official current calculated and random write-sharding trade-offs.
- Ceph Project, [*CRUSH Maps*](https://docs.ceph.com/en/latest/rados/operations/crush-map/), checked 2026-09-03. Official current algorithmic placement, hierarchy, weights, and failure-domain documentation.

## Exercises

### Exercise 1

For boundaries `(-infinity,100,200,500,+infinity)`, locate keys `99`, `100`, `499`, and `500` under half-open intervals. State the invariants needed to insert boundary `350`.

### Exercise 2

A service uses `h(k) mod 12` where bucket identities are physical nodes. Explain the impact of adding a thirteenth node and redesign the mapping with 1,024 stable logical slots.

### Exercise 3

Observed request loads across four hash buckets are `[110,90,100,700]` requests/s. Compute maximum-to-mean. If 650 requests/s in the last bucket belong to one key, explain why adding buckets is insufficient and compare two remedies.

### Exercise 4

Compare range partitioning, fixed hash slots, a token ring, rendezvous hashing, and jump hashing for a multitenant event service. It requires tenant point lookups, per-tenant time scans, zone-aware replicas, heterogeneous nodes, and arbitrary node removal.

### Exercise 5

A hospital moves medication-administration state from an old token map to a new one while devices can be offline. Specify partition, routing, migration, clinical, and review evidence required before retiring old ownership.

## Answers to the Exercises

### Answer 1

The keys route as `99 -> [-infinity,100)`, `100 -> [100,200)`, `499 -> [350,500)` after the proposed split (or `[200,500)` before it), and `500 -> [500,+infinity)`. Inserting `350` must preserve the same total comparison domain, strict boundary order, adjacency, no overlap or gap, and exactly one primary owner per key in each active epoch. The split must define child identities and owners, snapshot/catch-up, concurrent changes, validation, cutover, stale routes, rollback, and source retirement.

### Answer 2

Changing the modulus changes the assignment of most varied hash outputs; every affected key must move or become unreachable under new routing. Instead freeze `slot(k)=h(C(k)) mod 1024`, keep a versioned `owner_epoch(slot)` map, add node 13, and select roughly its capacity-weighted share of slots from existing owners. Stream and validate those slots, cut over their ownership by epoch, drain stale requests, and retain rollback. The redesign reduces placement churn but does not cure hot keys or provide replication by itself.

### Answer 3

Total load is 1,000, mean is 250, and maximum-to-mean is `700/250=2.8`. The heavy key alone contributes 650 requests/s and remains assigned to one primary under ordinary hashing, so additional buckets cannot reduce its requirement below 650. Read caching or replicated read serving can absorb repeated reads but adds freshness and invalidation concerns. Deterministic salting can divide writable substate, but reads/aggregates fan out and single-key ordering or transactions require redesign. Dedicated capacity is another option when semantics must remain local.

### Answer 4

Pure ranges support per-tenant time scans if keys order by tenant then time, but tenant size and current-time traffic can hotspot. Fixed hash slots route tenants directly and support arbitrary slot movement; time scans remain local only if events for a tenant share a slot, which makes a hot tenant indivisible. A token ring provides low-churn membership and capacity weighting through token allocation but needs topology-aware distinct replica selection and controlled arbitrary removal. Rendezvous naturally ranks an eligible, weighted destination set and can filter zones, at scoring cost. Jump is compact for appended numbered buckets but does not directly fit arbitrary removal, heterogeneous weights, or replica topology. A practical design may hash tenants to stable logical slots, range-order time within each tenant/slot, and use a versioned directory for weighted, zone-aware slot ownership and removal.

### Answer 5

Require identical canonical patient/encounter/medication keys, total exclusive primary assignment per epoch, distinct failure-domain replicas, one authoritative write path, preserved medication event identity/order/version, no loss or duplicate application, and bounded stale-device reconciliation. Capture old state, transfer by token interval, retain concurrent administrations/cancellations/corrections, compare identities and content plus clinical invariants, test routed reads and recovery, cut over with versioned redirects, support offline clients carrying old epochs, and retain rollback until backup/restore and new-owner failure are proven. Test crashes at every transition, network partitions, clock error, duplicate/reordered device submissions, urgent overrides, replica loss, and rollback. Named reviewers should include pharmacists and medication-safety clinicians, nursing/device workflow owners, clinical informatics, health-data governance/privacy, cybersecurity, distributed-storage engineers, operations/disaster recovery, quality/safety, accessibility, and the applicable independent clinical-safety authority. Local validation and this answer do not constitute external approval.
