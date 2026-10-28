---
module_id: SARCH-093
program: Software Engineering: Software Architecture
level: 2
module_number: 93
title: Architecture for Extreme Read or Write Scale
status: complete
last_verified: 2026-09-06
---

# Architecture for Extreme Read or Write Scale

## One-Page Review

### Governing question

How should architects design a system when read demand, write demand, data volume, fan-out, skew, or growth makes a single ordinary serving path inadequate—without trading away meaning, correctness, bounded latency, recovery, operability, and affordable evolution?

### Essential definitions

- **scale** is workload magnitude relative to a stated resource, topology, objective, and time window;
- **throughput** is completed useful work per unit time, while **goodput** excludes rejected, duplicated, expired, or otherwise useless work;
- **latency** is completion time for a named operation; a percentile such as p99 is a distribution statistic, not a maximum;
- **read amplification** is physical work performed per logical read, including fan-out, index probes, decompression, and filtering;
- **write amplification** is physical bytes or operations caused by one logical write, including replication, indexes, logs, compaction, and derived views;
- **skew** is unequal demand across keys, tenants, ranges, time, regions, or operations;
- a **hot key** or **hot partition** receives enough concentrated demand to limit the system despite spare aggregate capacity;
- **sharding** maps work or state into partitions that can be placed and operated independently;
- **fan-out** sends one logical request to multiple partitions or services; **fan-in** combines their results;
- a **materialized view** stores derived state optimized for a read question;
- **backpressure** communicates that a downstream stage cannot accept more work at the offered rate;
- **load shedding** rejects or degrades selected work before it destroys useful service;
- **resharding** changes the logical-to-physical mapping while the system remains in service;
- **headroom** is capacity reserved for bursts, failures, maintenance, recovery, and estimation error.

### Central model, mechanism, or theorem

Describe a workload envelope as

$$
W=(\lambda_r,\lambda_w,B_r,B_w,K,F,G,D),
$$

where $\lambda_r$ and $\lambda_w$ are read and write arrival rates, $B_r$ and $B_w$ are logical bytes per operation, $K$ is the key/tenant distribution, $F$ is fan-out, $G$ is growth and burst behavior, and $D$ contains durability, consistency, latency, freshness, jurisdiction, and availability demands. For every constrained resource $i$, require offered demand $d_i$ to remain inside an evidenced operating envelope $C_i$ with recovery headroom: $\rho_i=d_i/C_i<1$ is necessary but not sufficient. The architecture must also bound skew, amplification, queues, failure redistribution, and transition states.

### Critical invariants

- count useful completed outcomes, not merely accepted requests or internal operations;
- state workload assumptions by operation, key distribution, payload, time window, locality, and growth;
- preserve domain identity, ordering, uniqueness, authorization, and audit semantics across replicas and shards;
- keep ownership and routing epochs explicit while partitions move;
- bound read and write amplification, fan-out, retries, queue age, and derived-state staleness;
- treat a hot key as a semantic distribution problem, not proof that the whole fleet is small;
- make caches and materialized views derived, repairable, and observably fresh enough for their questions;
- admit, prioritize, defer, or shed overload before queues make all work expire;
- reserve capacity for failure, resharding, compaction, repair, replay, and regional evacuation;
- test mixed-version and mixed-placement states, not only the final topology;
- reconcile uncertain and duplicated effects under stable operation identities;
- measure cost, human operability, recovery time, and migration risk with throughput and latency.

### Common failures

Common failures include saying “millions of users” instead of specifying operations; sizing from averages; multiplying nodes while one key remains hot; caching without an invalidation or staleness contract; broadcasting every read; adding secondary indexes to a write path without counting their cost; dual-writing without one authority or reconciliation; using a queue as infinite capacity; retrying overload; reading all replicas for confidence; treating p99 as worst case; ignoring compaction and repair traffic; assuming uniform hashes imply uniform work; resharding only after saturation; measuring internal throughput rather than goodput; and choosing a hyperscale topology before a single-node design has an evidenced limit.

### Compact example

A sports score service receives 2 million reads/s during a final, but one match produces 70% of demand and authoritative updates arrive at 20/s. Hashing by match ID sends 1.4 million reads/s to one partition. More ordinary shards do not divide that key. The architecture keeps one ordered score stream, publishes versioned immutable snapshots, serves them from replicated regional caches, coalesces refreshes, and permits bounded staleness for spectators. Betting settlement uses the authoritative stream rather than the cache. Admission and stale-on-error behavior protect reads while repair catches up. Scale comes from separating one correctness path from many derived read paths, not from weakening the score's identity.

### Connections

[SARCH-053](053-partitioning-and-data-placement.md) owns partition mechanics, [SARCH-057](057-queue-based-load-leveling.md) owns queue behavior, and [SARCH-066](066-performance-and-capacity-models.md) owns basic capacity models. This module composes those mechanisms into workload-specific architectural judgment. [SARCH-094](../ROADMAP.md) next addresses machine-learning-enabled products.

## Governing Question

“Extreme” has no fixed request count. Ten writes per second can be extreme when each synchronously updates a terabyte-scale structure across an intermittent link; a million reads per second can be routine when they request the same immutable object from nearby caches. The relevant question is whether a named workload, including bursts and failures, fits within an evidenced operating and recovery envelope while preserving its required semantics.

Read scale and write scale pull architecture in different directions. Read optimization duplicates and derives state, moving work before requests arrive. Write optimization reduces synchronous work, distributes authority, batches sequentially, or relaxes freshness. Every optimization relocates cost: caches create coherence work; indexes accelerate reads by adding writes and storage; denormalization reduces joins by multiplying update paths; partitions add routing and rebalancing; replication adds bandwidth and consistency decisions. Architecture must expose that conservation of work rather than hide it behind product names.

## Why This Matters

The original Bigtable design describes a data model and storage architecture shaped by petabyte-scale data, thousands of servers, and applications with different latency and data demands [2]. Dynamo documents a different target: highly available key-value operations under an explicit service-level objective, using techniques including partitioning, replication, and object versioning [3]. Spanner describes globally distributed synchronous replication and external consistency, accepting mechanisms and latency consequences appropriate to that contract [4]. These systems are evidence that workload and guarantees shape designs; they are not interchangeable recipes.

At large fan-out, rare component delay becomes common request delay. Dean and Barroso analyze this tail-at-scale effect and mitigation families [6]. At high utilization, bursts, retries, garbage collection, repair, and dependency slowdown can amplify one another. The OSDI 2022 metastability study identifies recurring severe incidents in which systems remain in low-goodput overload after a trigger [10]. These findings motivate headroom, admission, bounded queues, and recovery experiments. They do not supply a universal utilization threshold.

## Prerequisites and Retrieval

Retrieve arrival and service rate, utilization, Little's Law, percentile, distribution, burst, queue, backpressure, goodput, idempotency, partition, replica, quorum, consistency, linearizability, cache, index, log, compaction, batch, stream, fan-out, skew, hot key, materialized view, change-data capture, routing epoch, failure domain, region, admission control, load shedding, recovery point, recovery time, and unit economics.

SARCH-051 through SARCH-060 establish partial failure, consistency, placement, multi-region topology, control planes, cells, queues, event-native processing, edge operation, and failure evaluation. SARCH-061 through SARCH-070 establish trade-off, scenario, sensitivity, fitness, coupling, capacity, reliability, threat, cost, and evidence review. This chapter applies those foundations to a system dominated by asymmetric read or write demand.

## Learning Objectives

After completing this module, you should be able to:

1. specify a workload envelope rather than use scale adjectives;
2. distinguish throughput, goodput, latency, freshness, volume, and growth;
3. derive first-order capacity, queue, fan-out, and amplification implications;
4. diagnose skew and hot keys that aggregate capacity hides;
5. design read paths with caches, replicas, indexes, and materialized views;
6. design write paths with partitioned authority, logs, batching, and backpressure;
7. preserve semantics during dual operation, replication, and resharding;
8. bound overload, retries, tail latency, repair, and metastable failure risk;
9. evaluate evidence, cost, security, privacy, operability, and recovery; and
10. reject unnecessary distribution when a simpler design fits the envelope.

## Core Exposition

**Start with operations, not users.** Name reads and writes separately: point lookup, range scan, search, append, conditional update, counter, transaction, bulk ingest, repair, and replay. Record rate distributions over seconds, minutes, and seasons; payloads before and after compression; key and tenant histograms; locality; concurrency; and fan-out. Include internal work and failure traffic. “One billion records” does not state whether the system performs one lookup a day or scans them every second.

**State the consequence contract.** For each operation, name latency distribution, freshness, ordering, consistency, durability, availability, privacy, residency, and cost objectives. A cached product description and an account balance can have equal read rates and incompatible correctness paths. A telemetry write may tolerate delayed query visibility but not silent loss. An advertisement view count may be approximate; a legal limit may not. Scale cannot decide semantics.

**Find the limiting resource.** Translate the envelope into CPU, memory, storage capacity and IOPS, network bandwidth, connections, locks, log bandwidth, metadata operations, downstream calls, and human operational work. Compute per-operation demand and the dominant resource. Measure service time distributions under realistic data, concurrency, background maintenance, and failure. Aggregate capacity is misleading if one serial coordinator, lock, index range, tenant, network link, or control-plane object limits progress.

**Use queueing bounds carefully.** In a stable interval, Little's Law gives $N=\lambda T$: average in-system work $N$ equals average arrival/completion rate $\lambda$ times average time $T$. At 80,000 completed operations/s and mean time 0.025 s, about 2,000 operations are in the system. The identity does not predict a percentile or prove stability. If sustained arrivals exceed sustainable completions, backlog grows; finite deadlines mean much of that work becomes useless before service.

**Budget amplification.** Let logical read bytes be $L_r$ and total physical read bytes $P_r$; $A_r=P_r/L_r$. Define write amplification similarly as $A_w=P_w/L_w$. A 1-KiB logical write replicated three ways, written to a log and table, copied into two indexes, and rewritten during compaction can consume far more than 3 KiB. Exact accounting depends on implementation, compression, batching, cache, and time window. Measure bytes, IOPS, CPU, and network separately rather than claiming one universal amplification number.

**Partition by a useful semantic distribution.** Hashing can spread many independent keys; ranges support ordered scans and locality; directory or lookup placement supports explicit tenant, jurisdiction, or cell assignment. Composite and time-bucketed keys can divide a naturally hot source, but they increase read fan-out and lifecycle work. Partition count should exceed immediate machine count where movement granularity benefits, without making metadata, fan-out, or tiny partitions dominant. Store a routing epoch or equivalent version so stale clients and movers can detect disagreement.

**Treat skew as primary data.** Measure hottest-key share, top-tenant share, partition percentiles, temporal correlation, and correlated payload cost. Uniform hashing distributes keys, not requests or bytes. A single globally authoritative counter cannot be scaled by merely hashing its name. Options include hierarchical or escrowed counters, sharded partials with defined merge semantics, request coalescing, write combining, caching, semantic subdivision, or admitting that one ordered authority bounds throughput.

**Build read scale from derived state.** Replicas multiply read capacity only if routing, lag, consistency, failure redistribution, and update bandwidth fit. Caches need keys, freshness or invalidation, stampede control, eviction behavior, negative entries, authorization boundaries, and stale-on-error policy. Materialized views precompute specific questions; they need source authority, derivation version, watermark, replay, correction, and rebuild. Search and analytical indexes are derived state unless the domain explicitly makes them authoritative.

**Bound fan-out.** If a request waits for the slowest of $k$ statistically independent partitions with per-partition latency CDF $F(t)$, then

$$
P(\max X_i>t)=1-F(t)^k.
$$

If each partition exceeds $t$ with probability 0.01 and a request fans to 50, the illustrative probability is $1-0.99^{50}\approx0.395$: about 39.5%. Real delays are often correlated, so the formula is a sensitivity illustration, not a production forecast. Reduce unnecessary fan-out, prune partitions, precompute, use deadlines, return partial results only when semantics permit, and observe result quality as well as speed.

**Design a narrow write authority.** Each invariant needs a place where concurrent writes are serialized, commuted, escrowed, or otherwise reconciled under a proved rule. Partitioning works when cross-partition invariants are rare or intentionally coordinated. A durable log can establish order and feed derived views, but a log does not by itself enforce uniqueness, authorize commands, or make consumers exactly once. Use stable operation identity, conditional writes, deduplication windows, and reconciliation for uncertain effects.

**Move noncritical work off the commit path.** Index updates, notifications, analytics, enrichment, and search refresh can often derive asynchronously from an authoritative commit. Record enough source identity, version, and causality to replay and repair. State the staleness contract. Synchronous work remains appropriate when the operation cannot honestly succeed without it. “Eventual” must name what converges, under which continued conditions, and how violations are observed.

**Choose storage layout from dominant work.** B-trees and log-structured designs expose different write, read, space, compaction, and range-scan trade-offs. The LSM-tree paper formalizes a hierarchy that batches and merges changes [5]. Bigtable uses sorted storage and compaction-related mechanisms within its design [2]. High ingest can benefit from sequential buffered writes, but compaction consumes bandwidth and can damage tail latency. Index and retention policy are architectural workload choices, not free database options.

**Control overload before it controls the system.** Admission should consider tenant, priority, cost, deadline, current queue age, and downstream health. Backpressure must propagate toward the source or a durable bounded buffer; otherwise an upstream stage keeps creating doomed work. Retries consume the same constrained capacity unless delayed, budgeted, deduplicated, and stopped. Shed optional enrichment before authoritative writes; reject new work explicitly before accepted work loses its guarantee. Recovery may require traffic below ordinary sustainable load while queues, caches, replicas, and repairs normalize.

**Reshard as a correctness transition.** A move has source and destination identity, placement epoch, snapshot boundary, change capture, verification, cutover, rollback or roll-forward rule, and cleanup. Avoid two silent authorities. Reads during movement must have a defined routing and merge rule. Throttle copy and repair against foreground headroom. Slicer's published design separates a reliable forwarding data plane from load-balancing decisions and reports production skew even with active sharding [7]; the lesson is to measure movement and imbalance, not to expect perfect uniformity.

**Separate regional read scale from global write semantics.** Immutable and bounded-stale views can serve near readers. Globally ordered writes incur coordination dictated by their protocol and geography. Spanner's design uses synchronous replication and a time API for its stated external-consistency features [4]. Other domains may assign a home region, partition authority by jurisdiction, use commutative operations, or accept weaker freshness. Label failover authority, session behavior, conflict policy, and evacuation capacity.

**Test the envelope and transitions.** Use recorded or justified distributions, including hot keys, large values, cache misses, background compaction, repair, failover, resharding, rolling versions, and downstream slowdown. Verify domain oracles: no duplicate charge, no missing accepted event, bounded staleness, stable pagination, authorized result, and recoverable derived state. Measure goodput, queue age, work discarded after deadlines, retry ratio, amplification, lag, imbalance, and time to recover—not just requests accepted during a short benchmark.

**Stop when simplicity wins.** Vertical scaling, efficient queries, correct indexes, batching, compression, a read replica, or a cache can extend a single authoritative system far enough. Distribution adds partial failure, movement, compatibility, security, and staffing cost. Adopt it where evidence identifies a bottleneck or isolation need and where an operational owner can rehearse recovery. Extreme ambition is not extreme workload.

## Definitions and Notation

Let $\lambda_o(t)$ denote arrival rate for operation class $o$ at time $t$, $s_o$ its resource service demand, and $C_i$ evidenced capacity for resource $i$ under a named configuration. Let $K(x)$ describe demand share for key or tenant $x$. Let $q_a$ be queue age, $d$ a request deadline, $F$ fan-out, $A_r$ read amplification, $A_w$ write amplification, $e$ routing epoch, and $h$ reserved headroom.

An architecture review should record at least:

$$
R=(W,S,P,Q,A,O,X),
$$

where $W$ is workload evidence, $S$ semantic guarantees, $P$ partition and placement, $Q$ queue/admission behavior, $A$ amplification and derived state, $O$ observability and operations, and $X$ transition, failure, and recovery evidence. This tuple organizes questions; it does not compute a design score.

## Mechanisms, Invariants, or Proof Structure

### Goodput invariant

Capacity claims count operations that complete within their semantic and deadline contract. Retries, duplicates, expired queue entries, corrupt results, and unrepairable partial effects do not increase goodput.

### Authority invariant

For each noncommutative invariant at an instant or governed transition, one authority or one explicit coordination/reconciliation rule decides accepted state. Replicas, caches, search indexes, movers, and replay consumers cannot silently become rival authorities.

### Placement-epoch invariant

A request and migration action can identify the mapping version under which it was routed. Stale and concurrent epochs produce explicit forwarding, retry, or merge behavior rather than loss or duplicate authority.

### Recovery-envelope invariant

At the admitted workload, the system retains evidenced resources and procedures for the selected failure, repair, rebalancing, replay, or evacuation scenario. Normal-load success without recovery capacity is not a sufficient scale claim.

### Executable skew diagnosis

<!-- bijux-verify: {"id":"scale-envelope-diagnosis","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"balanced: within-envelope\nhot key: hot-key-limit\nfleet: fleet-headroom-exhausted\nfailover: failover-headroom-exhausted\ninvalid: invalid-envelope\n","stderr":""}} -->
```python
def diagnose(arrivals, shard_capacity, shards, hottest_share,
             target_utilization=0.70, surviving_fraction=1.0):
    if min(arrivals, shard_capacity, shards, surviving_fraction) <= 0:
        return "invalid-envelope"
    if not 0 <= hottest_share <= 1 or not 0 < target_utilization < 1:
        return "invalid-envelope"
    usable_shards = shards * surviving_fraction
    if arrivals * hottest_share > shard_capacity * target_utilization:
        return "hot-key-limit"
    if arrivals > shard_capacity * usable_shards * target_utilization:
        return ("failover-headroom-exhausted" if surviving_fraction < 1
                else "fleet-headroom-exhausted")
    return "within-envelope"

cases = {
    "balanced": (4_000, 1_000, 10, 0.05, 0.70, 1.0),
    "hot key": (4_000, 1_000, 10, 0.20, 0.70, 1.0),
    "fleet": (8_000, 1_000, 10, 0.05, 0.70, 1.0),
    "failover": (6_000, 1_000, 10, 0.05, 0.70, 0.80),
    "invalid": (4_000, 1_000, 0, 0.05, 0.70, 1.0),
}
for name, facts in cases.items():
    print(f"{name}: {diagnose(*facts)}")
```

The finite model checks one conservative ordering: validate inputs, test a per-key limit, then aggregate surviving capacity. It assumes divisible shards and one service cost. Production evidence needs discrete placement, multiple resources, payload cost, correlated keys, background work, and measured service distributions.

### Proposition: aggregate spare capacity does not imply key capacity

Consider ten shards each able to serve 1,000 requests/s and total demand of 4,000 requests/s. Aggregate utilization is 40%. If one indivisible key receives 1,500 requests/s and maps to one shard, that shard is overloaded while 6,000 requests/s of aggregate capacity appears unused. Therefore aggregate spare capacity does not imply capacity for every key distribution.

### Proposition: asynchronous derivation does not imply loss of authority

Suppose an authoritative order transaction commits once, then a replayable identified event updates search and analytics views asynchronously. The views can lag while the order record remains the sole authority. Therefore asynchronous visibility does not by itself imply ambiguous authoritative state; ambiguity arises when contracts or write paths permit rival decisions.

## Alternatives and Trade-Offs

**Scale up versus scale out.** A larger machine preserves simple transactions and operations but has a ceiling and failure concentration. Distribution increases capacity and isolation while adding coordination, movement, and partial failure.

**Hash versus range versus directory placement.** Hashing spreads many keys but weakens locality. Ranges support scans but split moving hotspots. A directory expresses tenant, jurisdiction, or cell policy but becomes control state that must remain available and versioned.

**Cache versus read replica versus materialized view.** A cache reuses prior answers, a replica serves copied source state, and a materialized view derives a different question. They have different freshness, invalidation, authority, rebuild, and security obligations.

**Synchronous versus asynchronous derived writes.** Synchronous updates tighten visibility but multiply latency and availability dependencies. Asynchronous derivation protects the authoritative commit but requires lag contracts, replay, repair, and user-visible intermediate behavior.

**Exact versus approximate aggregation.** Sketches, samples, and partial aggregation reduce work where bounded error is acceptable. Financial, legal, inventory, and entitlement decisions may require exact or conservatively bounded semantics.

**Precompute versus fan out at read time.** Precomputation spends storage and write/refresh work to bound reads. Fan-out keeps writes simpler but multiplies latency and failure exposure. Workload asymmetry and freshness choose the balance.

**Automatic versus governed resharding.** Automation reacts quickly and repeatedly but can move the wrong thing or amplify instability. Human-governed moves are slower. Both need epochs, safety constraints, rate limits, observability, and recovery.

## Failure Modes and Misconceptions

1. **“Scale means user count.”** Users do not specify operations, concurrency, payloads, skew, or guarantees.
2. **“Average utilization is low, so capacity is safe.”** Bursts, tails, failures, maintenance, and hotspots can exhaust a component.
3. **“Consistent hashing fixes hot keys.”** It distributes identities, not demand for one identity.
4. **“A cache is just faster storage.”** It creates staleness, invalidation, stampede, security, eviction, and fallback behavior.
5. **“Read replicas give linear capacity.”** Lag, routing, update bandwidth, cache effects, and failure redistribution intervene.
6. **“A queue absorbs spikes.”** It stores delayed work; without a drain and deadline policy, it stores doomed work.
7. **“Retries improve availability.”** During overload they can lower goodput and delay recovery.
8. **“Adding an index only helps reads.”** It adds write, storage, cache, compaction, rebuild, and consistency work.
9. **“A log gives exactly-once business effects.”** Identity, conditional state changes, and reconciliation remain end-to-end concerns.
10. **“Async means eventually correct.”** Convergence requires continued delivery, valid derivation, repair, and a defined target.
11. **“p99 is the worst case.”** One percent of observations exceed it, and aggregation changes the distribution.
12. **“More fan-out always lowers latency.”** Redundant requests can help tails, but broad required fan-out exposes more stragglers and load.
13. **“Every write can be partition-local.”** Some invariants are truly cross-partition and require redesign or coordination.
14. **“Dual-write is migration.”** Without authority, ordering, verification, and reconciliation it is a divergence generator.
15. **“More replicas mean independent safety.”** Replicas can share software, corruption, control, power, or operator failure.
16. **“Compression is free capacity.”** It trades bytes for CPU, memory, latency, and operational complexity.
17. **“Compaction is background noise.”** It competes for the same storage and CPU resources and can dominate tails.
18. **“Autoscaling removes capacity planning.”** Detection delay, startup, state movement, quotas, and hot keys remain.
19. **“Benchmark throughput proves production scale.”** A result outside real distributions, failures, and correctness oracles has a narrow boundary.
20. **“Hyperscale architecture is future-proofing.”** Premature distribution can make product and operational change slower and riskier.

## Worked Examples

### Example 1

**Situation.** A catalog serves 500,000 description reads/s, while price changes 2,000 times/s and must not be stale at checkout.

**Reasoning.** One cache contract need not cover both meanings. Product descriptions are versioned, cacheable objects with long freshness and stale-on-error behavior. Price display uses short-lived derived regional views tagged with price version. Checkout performs an authoritative conditional price read or validates the submitted version. Cache invalidation messages accelerate freshness but periodic version comparison and rebuild repair missed messages. Authorization-sensitive fields never share a public cache key.

**Conclusion.** Read scale comes from derived views with separate semantic contracts; the purchase invariant remains on the narrow authoritative path.

### Example 2

**Situation.** Ten cache shards have 100,000 reads/s each. Total traffic is 400,000 reads/s, but one profile receives 180,000 reads/s.

**Reasoning.** Fleet utilization is 40%, yet the indivisible key exceeds one shard. Adding hash shards without changing the key does not help. Replicate the immutable versioned profile across shards or edge caches, coalesce misses, randomize replica choice, and cap refresh concurrency. Keep privacy and block-state decisions outside a broadly shared public object or version them into authorized variants. Measure hottest version and cache-miss concentration.

**Conclusion.** Replication and coalescing address concentrated reads; aggregate capacity was never the binding fact.

### Example 3

**Situation.** A search request waits for 50 independent partitions. Each has a 1% chance of exceeding 200 ms.

**Reasoning.** The illustrative chance that none exceeds 200 ms is $0.99^{50}\approx0.605$. Thus $1-0.99^{50}\approx0.395$, about 39.5%, waits for at least one slow partition. Correlation can make reality better or worse. Route only to partitions that can contain results, precompute common aggregates, set per-shard deadlines, and define whether partial results are honest. Hedging must be budgeted because duplicated work can create overload.

**Conclusion.** End-to-end latency depends on aggregation topology and semantics, not one shard's percentile.

### Example 4

**Situation.** One million devices emit one 300-byte observation every ten seconds; gateways batch bursts after reconnect.

**Reasoning.** Baseline is 100,000 writes/s and 30 MB/s before protocol, replication, indexes, and compaction. Device ID alone creates a long-lived partition and inconvenient retention; time alone creates a current-range hotspot. A composite `(time_bucket, hash(device_id))` spreads current writes and permits bucket expiry. Stable observation identity deduplicates reconnect batches. A durable admission tier reports accepted-versus-durable semantics, prioritizes safety events, and backpressures gateways. Query views by device derive asynchronously with a watermark and replay.

**Conclusion.** Key design, identity, admission, and derived reads jointly handle write scale; raw byte division is only the first bound.

### Example 5

**Situation.** A product asks for one exact, linearizable global counter supporting 5 million increments/s and local-region latency.

**Reasoning.** One ordered value has one serialization semantics even if its storage is replicated. First ask what decision needs exact immediacy. Display counts can use regional partials and monotonic approximate merges. A quota may use escrowed regional rights whose total never exceeds the limit. Ticket inventory can partition by inventory unit or use a reservation authority. If a truly exact total must be returned after every increment, coordination and distance impose a real bottleneck; architecture cannot wish it away.

**Conclusion.** Semantic decomposition can unlock scale; infrastructure cannot simultaneously erase a required global order.

### Example 6

**Situation.** Checkout synchronously writes order, search, recommendations, analytics, and email systems; one slow analytics store reduces checkout availability.

**Reasoning.** Only the authoritative order and required payment/inventory conditions belong to commit success. Commit one stable order identity and an atomic outbox or equivalent source record. Identified consumers derive search, recommendations, analytics, and email under idempotent state transitions. Each exposes lag, retry age, poison records, replay, and reconciliation. Email has an external-effect ledger so replay does not resend silently. User response states what is committed and which views can lag.

**Conclusion.** A narrow authority protects write goodput while replayable derivation preserves eventual products and repair.

### Example 7

**Situation.** Logical ingest is 200 MB/s, storage measurements show 4.5 times physical write amplification, and the device sustains 1 GB/s only under ideal sequential load.

**Reasoning.** Estimated physical writing is $200\times4.5=900$ MB/s before replication, repair, reads, and burst headroom. The design is already vulnerable near the advertised maximum. Reduce retained indexes, tune partition and compaction policy with measured data, batch appropriately, add devices or partitions, and isolate or rate-limit bulk work. Test steady state after compaction debt accumulates, not a short empty-store benchmark. Watch p99 latency, pending compaction bytes, device saturation, and recovery time.

**Conclusion.** High logical throughput can conceal maintenance debt; physical work and steady-state recovery determine the safe envelope.

### Example 8

**Situation.** Tenant range A–M is full and must split while clients and servers run mixed versions.

**Reasoning.** Create a new placement epoch and split boundary. Snapshot the source at a recorded position, stream later identified changes, and compare counts, hashes, and domain invariants. Until cutover, the old owner is authoritative and the destination shadows. At cutover, routing under the new epoch forwards stale clients safely; do not accept independent writes at both owners. Keep source data through a rollback decision window, throttle copying, test failure at every boundary, then remove old routing and data after reconciliation.

**Conclusion.** Resharding is an authority and compatibility transition, not just copying bytes.

### Example 9

**Situation.** A collaboration product needs low-latency document reads worldwide, but edit conflicts and residency rules differ by workspace.

**Reasoning.** Assign each workspace an explicit home and policy. Serve immutable document versions and bounded-stale summaries regionally. Route edits to the home authority unless the document model supplies a proved merge operation. Include version and home epoch so failover cannot create silent split authority. Evacuation changes authority through a governed state machine; it accounts for missing acknowledgements and residency. Regional caches retain only permitted data and revoke or expire access predictably.

**Conclusion.** Regional read scale can coexist with explicit write authority; locality, conflict, and jurisdiction are part of placement semantics.

### Example 10

**Situation.** An earthquake alert system faces a 200-fold read surge, damaged networks, duplicate publisher retries, multilingual content, and malicious false alerts.

**Reasoning.** Authenticated authorized publishers append one alert identity and version to a narrow durable authority. Immutable signed alert objects replicate before or alongside notification, then serve through regional and edge caches with request coalescing and stale-on-error rules. Channel-specific queues prioritize new life-safety updates over receipts and analytics, suppress duplicates, expose age, and shed optional personalization. Clients display issue time, area, language, supersession, and offline status. Capacity tests include regional loss, cache cold start, retry storms, revocation, accessibility, and correction of a false message. Public safety authorities decide release and correction policy.

**Conclusion.** Extreme read scale is only one constraint; authenticity, ordering, correction, degraded delivery, and legitimate authority define useful service.

## Cross-Program Connections

- [Algorithms Engineering](../../16-algorithm-engineering/ROADMAP.md) owns asymptotic and empirical algorithm selection for indexes, sketches, routing, and aggregation.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns storage engines, transactions, indexes, query processing, replication, and physical tuning.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns authority, lineage, semantic models, derived data, and lifecycle.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns consensus, clocks, replication, consistency, partitioning, and distributed protocols.
- [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns production capacity, overload, observability, incident response, and recovery practice.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns reusable self-service data, caching, queue, and workload capabilities for internal consumers.

## References

1. Martin Kleppmann and Chris Riccomini, [*Designing Data-Intensive Applications*](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/), 2nd ed., O'Reilly, February 2026; publisher record checked 2026-09-06.
2. Fay Chang et al., [“Bigtable: A Distributed Storage System for Structured Data”](https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/), OSDI 2006, pp. 205–218.
3. Giuseppe DeCandia et al., [“Dynamo: Amazon's Highly Available Key-value Store”](https://dl.acm.org/doi/10.1145/1294261.1294281), SOSP 2007, pp. 205–220.
4. James C. Corbett et al., [“Spanner: Google's Globally-Distributed Database”](https://research.google/pubs/spanner-googles-globally-distributed-database-2/), OSDI 2012.
5. Patrick O'Neil, Edward Cheng, Dieter Gawlick, and Elizabeth O'Neil, [“The Log-Structured Merge-Tree (LSM-Tree)”](https://doi.org/10.1007/s002360050048), *Acta Informatica* 33, 1996, pp. 351–385.
6. Jeffrey Dean and Luiz André Barroso, [“The Tail at Scale”](https://research.google/pubs/the-tail-at-scale/), *Communications of the ACM* 56(2), 2013, pp. 74–80.
7. Atul Adya et al., [“Slicer: Auto-Sharding for Datacenter Applications”](https://research.google/pubs/slicer-auto-sharding-for-datacenter-applications/), OSDI 2016.
8. Michael Stonebraker, [“The Case for Shared Nothing”](https://www.ics.uci.edu/~cs223/papers/csn.pdf), *Database Engineering* 9(1), 1986, pp. 4–9.
9. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1992. Concurrency, recovery, logging, and transaction-processing performance.
10. Lexiang Huang et al., [“Metastable Failures in the Wild”](https://www.usenix.org/conference/osdi22/presentation/huang-lexiang), OSDI 2022, pp. 73–90.
11. Avinash Lakshman and Prashant Malik, [“Cassandra: A Decentralized Structured Storage System”](https://doi.org/10.1145/1773912.1773922), *ACM SIGOPS Operating Systems Review* 44(2), 2010, pp. 35–40.
12. Sanjay Ghemawat, Howard Gobioff, and Shun-Tak Leung, [“The Google File System”](https://research.google/pubs/the-google-file-system/), SOSP 2003, pp. 29–43.

## Exercises

### Exercise 1

Define throughput, goodput, read amplification, write amplification, skew, fan-out, and headroom. Explain why high throughput alone cannot establish scale readiness.

### Exercise 2

A request fans out to 30 independent partitions, each with probability 0.02 of exceeding 100 ms. Compute the illustrative probability that at least one exceeds 100 ms. Then state five ways the model can mislead a production decision.

### Exercise 3

A write service receives 120,000 logical 1-KiB writes/s. It has three replicas, two synchronous secondary indexes, estimated compaction amplification of 2.5 over base table bytes, and a 10-Gbit/s storage network path. Produce a first-order byte-rate budget, identify ambiguities, and propose the next measurements and controls.

### Exercise 4

Design a live resharding protocol for a marketplace in which one seller accounts for 25% of writes and orders require unique identities. Include semantic key changes, epochs, authority, copying, change capture, verification, cutover, overload protection, rollback or roll forward, and cleanup.

### Exercise 5

A national election-results publication service must absorb extreme reads and regional write bursts while preserving source provenance, corrections, embargoes, accessibility, multilingual delivery, hostile traffic, regional outages, and public trust. Design the architecture and its evidence plan without claiming that the software decides or certifies the election.

## Answers to the Exercises

### Answer 1

Throughput is completed operations per unit time; goodput counts only useful operations completed within their semantic and deadline contract. Read and write amplification compare total physical work with one logical read or write. Skew is unequal demand across keys, tenants, ranges, time, regions, or operations. Fan-out sends one logical request to multiple participants. Headroom reserves capacity for bursts, failures, maintenance, repair, movement, and uncertainty. High throughput can include duplicates or expired work, hide unacceptable latency and errors, omit background maintenance, use uniform rather than skewed keys, violate correctness, have no failure margin, and cost too much. A scale claim needs workload, semantics, distributions, transitions, recovery, operations, and cost.

### Answer 2

Under independence, $P(\text{at least one slow})=1-(1-0.02)^{30}=1-0.98^{30}\approx1-0.5455=0.4545$, about 45.45%. Production delays may be correlated; shard probabilities can differ; the request may not wait for every shard; retries or hedges add load; “slow” may not violate the end-to-end deadline; routing and pruning change fan-out; the workload mix and cache state can differ; and the estimated 0.02 has uncertainty. The result is a sensitivity calculation, not a latency forecast.

### Answer 3

Logical rate is $120{,}000\times1$ KiB/s, about 122.88 MB/s using decimal MB. If each of three replicas writes the base and two same-sized indexes, pre-compaction physical data is approximately $122.88\times3\times3=1{,}105.92$ MB/s. Applying 2.5 to all those bytes gives 2,764.8 MB/s, already above 10 Gbit/s, whose theoretical decimal maximum is 1,250 MB/s. But “three replicas” may include the local copy or mean three remote copies; index entries differ in size; the 2.5 factor may apply only to base storage or already include indexes; network and device write paths differ; compression, batching, protocol, acknowledgements, repair, and read traffic are omitted.

Measure serialized base and index bytes, per-replica network, device bytes, CPU, compaction debt, steady-state latency, burst distribution, skew, and failure redistribution. Remove unnecessary synchronous indexes, derive eligible views asynchronously, partition load, batch where latency permits, compress when CPU permits, add independent paths, reserve headroom, backpressure sources, and shed nonauthoritative work. Preserve stable operation identities and do not weaken an invariant merely to fit the link.

### Answer 4

Hashing only by seller leaves the 25% seller hot. Split its writes by a domain-safe subkey such as order identity or bounded time plus order hash; maintain a separate seller query view. Preserve globally unique order identity through an authoritative allocator or collision-resistant domain-approved scheme and conditional acceptance. Introduce a routing epoch and explicit old/new key mapping. Snapshot each old range at a log position, copy with rate limits, stream identified later changes, and verify counts, hashes, uniqueness, money, and order-state invariants. Keep old owners authoritative until each governed cutover; stale clients forward or retry under the new epoch. Never allow uncoordinated dual authority.

Reserve capacity for copy, log retention, replay, and one-node or one-zone failure. Abort or roll forward from named thresholds for lag, queue age, error, or invariant violation. Retain the old path for a bounded reconciliation window, compare shadow reads, repair discrepancies under recorded authority, then remove forwarders, obsolete mappings, duplicated data, and migration telemetry. Test client and server mixed versions and failures before snapshot, during capture, at cutover, and during cleanup.

### Answer 5

Election officials and authorized regional systems remain the source authorities; the publication software records provenance and never infers, adjudicates, or certifies a winner. Each submitted result has jurisdiction, contest, source identity, signature or authenticated channel, sequence, issue time, status, embargo rule, and supersession link. A narrow append and validation path preserves immutable history; correction creates a new version. Regional bursts enter bounded durable queues with deduplication, backpressure, quarantine, and human escalation. Authority rules prevent one region from overwriting another.

Build signed immutable publication snapshots and derived jurisdiction, language, accessibility, and aggregate views with version and watermark. Replicate snapshots to regional and edge caches before broad release; coalesce misses, rate-limit abusive clients, and provide low-bandwidth accessible formats. Embargo release is a governed authoritative event with clock and operator controls, not merely a cache TTL. Stale-on-error responses show version and issue time; corrections propagate with priority and explicit supersession. Separate public data from protected contact, device, and operational metadata.

The evidence plan covers expected and adversarial key distributions, simultaneous regional bursts, cold caches, hostile traffic, source replay, duplicate and out-of-order submissions, invalid signatures, correction storms, embargo mistakes, accessibility and language completeness, network partition, region loss, control-plane loss, and recovery. Oracles check provenance, no silent overwrite, monotonic version history, authorized release, bounded publication lag, visible correction, reproducible aggregates, and rebuildable views. Report goodput, queue age, cache and origin load, staleness, failed verification, correction propagation, regional imbalance, recovery time, and operator burden. Election authorities, accessibility experts, security teams, regional officials, observers, and affected communities must review real policy and evidence; passing software tests does not certify the election.
