---
module_id: DE-091
program: Data Engineering
level: 2
module_number: 91
title: Warehouses, Query Engines, and Serving Stores
status: complete
last_verified: 2026-09-03
---

# Warehouses, Query Engines, and Serving Stores

## One-Page Review

### Governing question

How should a data organization map each analytical or operational workload to a warehouse, query engine, serving store, or deliberate combination, while making latency, freshness, correctness, concurrency, isolation, availability, cost, governance, and synchronization obligations explicit instead of choosing from product categories or benchmark headlines?

### Essential definitions

- A **data warehouse** is a managed analytical system that combines governed storage, metadata, SQL execution, transactions, optimization, workload management, and administration around durable analytical data.
- A **query engine** plans and executes queries over data it may not own, commonly through connectors, table formats, catalogs, and object or remote storage.
- A **serving store** is a persistence/query system shaped for a bounded access contract such as point lookup, key/range scan, low-latency aggregate, full-text search, vector retrieval, graph traversal, or time-series query.
- A **system of record** is the authoritative state for a defined fact and time; a **system of serving** is an access-optimized representation that may be derived.
- **Storage/compute separation** allows stored data and query compute to scale or fail independently, while introducing network, caching, and coordination trade-offs.
- **MPP** (massively parallel processing) partitions query work across workers and combines partial results.
- A **coordinator** parses, analyzes, optimizes, schedules, and tracks work; a **worker** scans, filters, joins, aggregates, sorts, or writes its assigned fragments.
- **Predicate/projection pushdown** moves filters or column selection toward the source to reduce transfer; correctness depends on compatible semantics.
- **Partition pruning** avoids irrelevant partitions; **data skipping** avoids blocks using metadata such as min/max statistics.
- A **shuffle** repartitions intermediate data across workers, often dominating network, spill, skew, and tail latency.
- **Workload isolation** prevents one workload class or tenant from consuming resources needed by another.
- **Freshness lag** is elapsed time between an authoritative change and visibility in the queried representation.
- **Read consistency** defines which writes a read may observe; **session/read-your-writes consistency** gives a client a scoped monotonic expectation.
- A **materialized serving projection** is a derived, access-shaped copy with explicit source version, transform, watermark, rebuild, and reconciliation.
- **Fan-out** sends one logical query to multiple partitions or systems; its tail depends on slow or unavailable components.
- A **workload contract** specifies query shapes, result sizes, percentiles, concurrency, freshness, consistency, availability, security, evolution, and budget.

### Central model, mechanism, or theorem

For workload $w$ and candidate system $s$, define measurable objectives and constraints rather than a universal score:

$$
Feasible(s,w)=LatencyOK\land FreshnessOK\land SemanticsOK\land CapacityOK\land GovernanceOK\land RecoveryOK.
$$

Among feasible designs, compare total lifecycle cost and operational risk. End-to-end response time can be decomposed as

$$
T=T_{queue}+T_{plan}+T_{scan}+T_{shuffle}+T_{compute}+T_{spill}+T_{return}.
$$

For a derived serving projection, observed answer state is bounded by source, capture, transport, materialization, replication, and cache progress. A low query latency does not imply fresh data. If one request fans out to all $n$ shards, then under independence

$$
P(T_{max}\le t)=\prod_{i=1}^{n}P(T_i\le t),
$$

so adding shards can worsen tail success even when median shard latency is unchanged. Independence rarely holds exactly; the formula is a reasoning aid, not a production guarantee.

### Critical invariants

- Select systems from workload contracts and failure consequences, not OLAP/OLTP labels, vendor categories, or one benchmark.
- Name the authoritative source for every fact and the exact semantics of every derived serving copy.
- Correctness includes types, nulls, collation, timezone, decimal/float behavior, filters, joins, duplicate handling, security predicates, and snapshot boundaries.
- Query identity binds subject, purpose, SQL/logical plan, catalog/schema, input versions, engine/version, configuration, policy, and output or error.
- Latency budgets cover queue, planning, data access, shuffle, compute, spill, result transfer, client, retries, and admission—not engine time alone.
- Freshness and query latency are separate SLOs with separate timestamps, watermarks, and error budgets.
- Capacity planning uses concurrency, service time, scan/shuffle bytes, skew, working set, result size, burst, maintenance, failure headroom, and noisy-neighbor behavior.
- Admission, quotas, queues, priorities, timeouts, cancellation, resource groups, and workload pools have explicit fairness and overload semantics.
- Partitioning, clustering, indexing, replicas, materializations, and caches are workload-specific physical designs with write, rebuild, and lifecycle costs.
- Pushdown is accepted only when source and engine semantics agree; otherwise correctness takes precedence over bytes saved.
- Federated queries treat remote limits, credentials, egress, source load, consistency, and partial failure as part of the query contract.
- Serving projections preserve stable keys, source offsets/versions, idempotency, deletion/tombstone behavior, late events, backfills, and reconciliation.
- Retries do not duplicate writes, double-count usage, or silently exceed deadline/cost budgets.
- Governance is enforced at all planes: catalog, plan, source, engine, intermediate/spill, result, cache, export, logs, and derived stores.
- Performance tests use representative distributions, concurrency, skew, cache state, failures, security rules, evolution, and result sizes.
- Cost attribution distinguishes reserved/idle capacity, scan and compute, storage, network/egress, index/materialization, operations, and downstream externalities.
- Architecture decisions record assumptions, rejected alternatives, reversible boundaries, migration triggers, and exit/rebuild paths.

### Common failures

Common failures include sending dashboard concurrency to an unbounded ad hoc warehouse; placing exploratory scans on an operational database; adding a low-latency store without owning synchronization; benchmarking warm-cache single queries only; partitioning by a low-selectivity or skewed field; assuming more shards always improve latency; ignoring result transfer; pushing filters across incompatible collations or timezones; joining live remote sources without consistency boundaries; treating successful dual writes as atomic; retrying timed-out mutations without idempotency; confusing replica lag with query latency; scaling compute while the bottleneck is queue, network, metadata, spill, or a hot key; and reporting per-query price while omitting materialization, egress, idle capacity, and operator cost.

### Compact example

An executive dashboard needs p95 under two seconds, 200 concurrent viewers, data no older than five minutes, stable metric semantics, tenant isolation, and bounded cost. Ad hoc queries scan billions of events and take seconds to minutes. The team keeps governed history in a warehouse/query layer, incrementally materializes approved aggregates into a serving store keyed by tenant and time bucket, propagates corrections and tombstones, exposes source and materialization watermarks, and reconciles totals. Dashboard latency is measured separately from freshness; analysts still use the warehouse for investigations. The derived store is a product with ownership and recovery, not a transparent cache.

### Connections

[DE-063](063-table-metadata-and-snapshots.md) provides versioned table state, [DE-066](066-time-travel-and-reproducible-reads.md) defines reproducible input snapshots, [DE-067](067-compaction-and-small-file-management.md) and [DE-068](068-clustering-and-data-skipping.md) shape scan work, [DE-069](069-catalog-integration.md) connects engines to governed metadata, [DE-071](071-completeness-validity-accuracy-and-consistency.md), [DE-073](073-reconciliation-tests.md), and [DE-074](074-freshness-and-timeliness.md) define serving correctness and freshness, [DE-086](086-access-control-for-analytical-data.md) governs access, and [DE-090](090-making-data-discoverable-without-losing-control.md) defines safe discovery. [DE-092](../ROADMAP.md) next deepens materialized views and derived tables.

## Governing Question

Architecture discussions often begin with a category: warehouse, lakehouse, federated engine, column store, key-value database, document store, search engine, or time-series database. That reverses the decision. Begin with access and change contracts: which questions, over what data, with what result shape, at which latency percentile and concurrency, under which freshness and consistency, during which failures, with which governance and budget?

A warehouse can serve interactive dashboards, and a serving store can support aggregation. A query engine can provide SQL over object storage, remote databases, or streaming tables. These overlaps do not make the systems equivalent. Ownership of storage and metadata, transaction model, optimizer statistics, physical layout, cache behavior, isolation, availability, and operational boundary differ.

One workload can need multiple paths. An analyst explores history through a warehouse; an API reads a precomputed customer projection; an investigator federates a bounded lookup; a model retrieves features from online and offline stores. The challenge is not to eliminate every copy but to make authority, derivation, freshness, correction, deletion, recovery, and cost explicit for each copy.

The governing question is therefore a proof obligation: demonstrate that the selected path meets its workload contract under representative concurrency, distribution, failure, evolution, and governance conditions, and that every derived path remains consistent enough with its authoritative source for the promise being made.

## Why This Matters

The wrong execution surface creates systemic failure. Large scans on a transactional source contend with customer writes. Thousands of dashboard requests overwhelm a warehouse queue. A key-value store cannot answer changing ad hoc groupings without precomputed access paths. A federated engine can transfer huge remote tables or apply subtly different SQL semantics. A serving copy can be fast and wrong.

Performance is multidimensional. Median latency can improve while p99 deteriorates under fan-out. A query can execute quickly after waiting minutes in a queue. A cache can meet latency while serving yesterday's state. A benchmark can exclude authentication, policy evaluation, network, serialization, and client rendering. Architecture must measure the experience and correctness the consumer receives.

Economics are similarly coupled. Separating storage and compute can allow independent scaling, but remote reads, object requests, egress, cache warming, compaction, indexes, and materialized projections cost money. Dedicated capacity reduces queue variance but creates idle cost. Operational complexity and incident load belong in the comparison.

The selection also affects governance. Query engines may move data through workers and spill; serving stores create new retention and access scope; federation crosses credential and jurisdiction boundaries; caches outlive policy or deletion changes. A fast design that cannot explain which version, policy, and tenant produced an answer is not production-ready.

## Prerequisites and Retrieval

Retrieve workload evidence: query fingerprints and logical shapes, point/range/scan/search/vector/graph operations, predicates, joins, aggregations, result sizes, read/write ratio, update pattern, late corrections, backfills, concurrency, burst, priority, tenants, schedules, cacheability, interactive/batch/API consumers, and growth.

Retrieve objectives: p50/p95/p99 and deadline, throughput, freshness by fact, event versus processing time, read consistency, read-your-writes, atomicity, correctness tolerance, approximation error, availability, recovery point/time, regional constraints, degradation, and maximum cost.

Retrieve data properties: volume, row width, cardinality, distributions, skew, selectivity, temporal locality, mutable keys, duplication, schema evolution, file sizes, partitions, clustering, compression, statistics, indexes, snapshots, deletion, and retention.

Retrieve system semantics: storage ownership, compute topology, coordinator/workers, connector capabilities, transaction/isolation model, read snapshot, optimizer, vectorization, pushdown, join algorithms, shuffle, spill, result cache, autoscaling, workload manager, admission, cancellation, quotas, replication, failover, backup, and restore.

Retrieve security and governance: identity propagation, tenant boundaries, row/column/masking policy, catalog authorization, source credentials, delegated access, intermediate/spill encryption, result/export control, audit logs, lineage, purpose, geography, keys, deletion/tombstones, and evidence retention.

Retrieve operational and cost evidence: query profiles, queue and execution time, scanned/pruned/shuffled/spilled/returned bytes, CPU/memory/network/storage, cache hit, hot partitions/keys, retries, cancellations, errors, remote-source load, replication/materialization lag, reconciliation, capacity reservations, per-unit prices, egress, labor, and incidents.

Distinguish warehouse from engine; engine from connector; system of record from system of serving; source state from cache state; execution latency from queue and end-to-end latency; query freshness from ingestion/materialization/replica lag; consistency from availability; concurrency from throughput; partition pruning from filtering after scan; index selectivity from existence; logical SQL equivalence from physical execution; retry from replay-safe retry; and benchmark performance from production fitness.

Create a workload decision record:

| Concern | Evidence and decision |
|---|---|
| Contract | Query shapes, percentile/deadline, concurrency, freshness, consistency, availability |
| Authority | Source of truth, exact versions, correction/deletion and derived-copy semantics |
| Physical work | Scan, prune, index, join, shuffle, spill, result and fan-out expectations |
| Isolation | Admission, queues, pools, quotas, priority, fairness and overload degradation |
| Governance | Identity/purpose, source/intermediate/result controls, audit and geography |
| Lifecycle | Schema, backfill, rebuild, reconciliation, failover, backup, restore and decommission |
| Economics | Compute, scan, storage, egress, idle capacity, copies, operations and incident cost |

Write a falsifiable claim: “Dashboard workload W uses projection P sourced from warehouse snapshot sequence S and capture offset O; materializer M applies versioned logic V with idempotent keys and tombstones; serving store K supports tenant/time access at p95 below two seconds for 200 concurrent requests, five-minute source-to-answer freshness, stated read consistency and 99.9% availability; admission Q protects capacity; reconciliation R checks counts/digests; policy A applies at source, materializer, store and result; tests cover skew, cold cache, failover, late corrections and rebuild; cost C includes all retained copies and operations.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish warehouses, query engines, connectors, serving stores, authoritative systems, and derived serving projections;
2. translate consumer needs into explicit query-shape, latency, concurrency, freshness, consistency, availability, governance, and cost contracts;
3. decompose query time across admission, planning, scan, shuffle, compute, spill, return, retries, and clients;
4. reason about columnar scans, pruning, skipping, indexing, vectorization, join strategy, data movement, skew, and fan-out tails;
5. design workload isolation, admission, quotas, priorities, cancellation, capacity, autoscaling, and overload degradation;
6. evaluate federation and pushdown against source load, remote semantics, credentials, egress, snapshots, and partial failure;
7. build low-latency serving projections with authority, version, idempotency, watermarks, corrections, tombstones, rebuilds, and reconciliation;
8. protect catalogs, sources, plans, workers, spills, results, caches, exports, and derived stores consistently;
9. benchmark representative data, concurrency, cache states, failures, security rules, evolution, and end-to-end costs; and
10. record a reversible architecture decision with assumptions, rejected alternatives, migration triggers, and verification.

## Core Exposition

### Characterize execution surfaces by responsibility

A warehouse usually owns or tightly integrates managed analytical storage, transaction/catalog semantics, optimizer, execution, workload management, security, and administration. Separation of storage and compute can permit independent scaling and multiple compute pools, but it does not remove network or metadata coordination.

A query engine can be embedded, clustered, or serverless and operate over data through connectors. Its value is flexible execution and federation without always moving data first. Its correctness and performance depend on table format, catalog, source, connector, statistics, file layout, credentials, and pushdown. The engine cannot optimize facts it cannot observe.

A serving store specializes around known access patterns. A key-value or wide-column store favors keyed operations; a column-oriented OLAP store favors filtered aggregates; search favors inverted indexes; vector stores favor approximate similarity; time-series stores optimize time-keyed retention and aggregation. Specialized paths trade ad hoc flexibility for predictable work. Call the contract, not the brand, the architectural boundary.

### Follow a query through the system

A request authenticates and authorizes, parses, resolves catalog objects and functions, binds types, rewrites a logical plan, estimates cardinalities/cost, chooses physical operators and distribution, waits for admission, schedules stages/tasks, reads data, exchanges intermediate blocks, spills if necessary, combines results, serializes them, and returns them through a client. Cancellation and retry can occur at several layers.

Instrument these phases separately. A slow query may be queued behind another tenant, waiting for source metadata, scanning unpruned files, suffering a skewed join, spilling because memory estimates were wrong, blocked by a remote source, or returning too many rows. Adding workers helps only some bottlenecks and can increase shuffle or coordination.

Bind the plan to evidence: normalized fingerprint and safe query reference, subject/purpose, catalog/schema snapshots, input versions, statistics/version, engine/configuration, logical and physical plan, admission pool, resources, scanned/shuffled/spilled/returned bytes, output or error, and timestamps. Avoid logging sensitive literals or results unnecessarily.

### Match physical design to access paths

Columnar formats reduce analytical I/O when queries select subsets of columns and vectorized operators amortize interpretation overhead. Partitioning can eliminate large regions when predicates align with partition transforms. Clustering or sorting can improve locality and data skipping. Good file/block sizes balance parallelism, metadata overhead, range reads, and update/compaction behavior.

An index is worthwhile when its lookup plus fetch cost beats scanning and when write/storage/rebuild costs fit. Composite index order should match equality, range, ordering, and covering needs. High fan-out across partitions can defeat point-lookup latency. A materialized aggregate or view is an index-like derived result with stronger semantic and freshness responsibilities.

Measure selectivity and distributions, not intuition. Tenant sizes, popular keys, recent time windows, nulls, and correlated predicates create skew. Salting, adaptive repartition, broadcast, pre-aggregation, or different partition keys can help, but each alters write paths or query semantics. Preserve a way to repartition/rebuild as workloads evolve.

### Control joins and data movement

Distributed joins move data or replicate one side. Broadcast is efficient when one input is truly bounded; repartition/hash joins scale larger inputs but shuffle; merge joins exploit compatible ordering; nested-loop/index lookup can fit selective outer inputs. Cardinality estimation errors cascade into bad choices.

Skew creates stragglers: one key or partition owns disproportionate work. Report task distributions and p95/p99, not stage averages. Detect hot values, isolate them, pre-aggregate, split heavy keys, or select an alternate plan. Ensure special-case logic preserves null and duplicate semantics.

Federated joins add remote rate limits, latency, egress, credentials, source concurrency, and inconsistent snapshots. Prefer moving a bounded side, taking governed snapshots, or materializing repeated cross-system joins. If live federation is required, define partial failure, timeout, cancellation, and source protection; do not let analytical scans destabilize production databases.

### Treat pushdown as semantic delegation

Predicate, projection, aggregation, limit, join, or function pushdown can drastically reduce transfer. But delegation is correct only when source semantics match the engine: nulls, collation, case, timezone, decimal overflow, floating point, coercion, pattern matching, and security rules can differ. Connector claims should be verified for versions and expressions actually used.

Record pushed and residual operations in the plan. Compare results against non-pushed execution on adversarial values. A pushed `LIMIT` without compatible ordering can change results; a filter evaluated under different timezone can move boundary records; remote row policies may see a service identity rather than the user.

When pushdown is unavailable, estimate transferred bytes and source load before execution. Admission should reject or route queries that exceed governance, deadline, or budget rather than discovering the problem after a remote table scan.

### Isolate and admit workloads

Interactive exploration, scheduled transformation, dashboard, export, maintenance, and incident queries have different service goals. Assign workload pools or resource groups with concurrency, memory/CPU, scan, spill, runtime, result, and cost limits. Define priorities and fairness so “high priority” is not a permanent starvation mechanism.

Admission protects the system before overload. Queues should be bounded and observable; deadlines include time already queued. Cancellation must reach workers and remote sources and clean up spill or locks. Retries need remaining deadline, idempotency, attempt identity, and retry budgets. Retrying an expensive query during overload can amplify collapse.

Autoscaling reacts after signals and has provisioning/warm-up delay. Keep headroom for bursts, node failure, maintenance, compaction, and metadata operations. Little's Law, $L=\lambda W$, connects average concurrency $L$, arrival rate $\lambda$, and time in system $W$ for stable conditions; it does not substitute for tail or burst analysis.

### Separate latency, freshness, and consistency

Query latency begins when the consumer sends the request and ends when the required result is usable. Measure queue, service, network, retries, serialization, and client consumption. First-byte and full-result latency differ. A two-second engine plan followed by a 500 MB download is not a two-second user result.

Freshness compares the answer's authoritative event/source version with time or required progress. Expose source watermark, materialization offset, replica applied position, cache generation, and query snapshot. Processing-time “last refreshed” can look recent while old source events remain missing.

Consistency defines allowed observations. A warehouse snapshot may provide a stable multi-table read; a replica may lag; a serving store may provide eventual, session, or strongly consistent reads for certain operations. State requirements such as read-your-writes, monotonic reads, atomic publication of a version, or bounded staleness. “Real time” is not a consistency model.

### Engineer serving projections as data products

Create a serving projection only when repeated bounded access or isolation justifies another stateful system. Define authoritative inputs, keys, schema, transform/version, ordering, duplicate handling, late events, corrections, deletion/tombstones, freshness, consistency, rebuild, reconciliation, owner, on-call, capacity, and retirement.

Prefer one source log/outbox or CDC stream over uncoordinated application dual writes. Consumers apply stable event IDs and source versions idempotently. Per-key ordering or version comparisons prevent late old updates from overwriting new state. Tombstones must survive long enough to prevent replay resurrection.

Backfills and live updates need a cutover protocol: snapshot at a known source position, build, catch up changes, validate, atomically switch reads, and retain rollback bounds. Rebuilds apply current policies and deletions. Reconciliation compares source and projection populations, counts, key/version samples or digests, and semantic queries; repair is explicit and observable.

### Design for overload and failure

State what happens when the warehouse is saturated, one query worker dies, a coordinator fails, object storage slows, a remote connector times out, a replica lags, or the serving materializer stops. Some engines retry tasks; others restart queries. Some stores favor availability under partition; others reject. Documentation and fault tests determine actual behavior.

Degrade by workload contract: serve a marked older cache within freshness budget, reduce optional dimensions, queue batch work, reject expensive exploration with retry guidance, or switch to a verified replica. Never silently return partial aggregates as complete. Approximation must expose method, error/bias, and eligibility.

Hedging or duplicate reads can reduce tails but increases load and cost; use only for idempotent reads with bounded budgets and cancel losers. Circuit breakers and admission protect dependencies. Avoid synchronized retries and failovers that send every client to one recovering system.

### Govern every data-bearing plane

Propagate identity and purpose rather than using one omnipotent connector where source policy requires end-user context. Apply catalog, row, column, masking, tenant, query, result, export, and network controls consistently. Verify that pushdown and caches do not bypass them.

Intermediate exchanges, local disks, spill, temporary tables, result caches, query histories, plans, error messages, and profiles can contain sensitive values. Encrypt, isolate, minimize, expire, and audit them. Serving stores inherit classification and retention; derived keys or aggregates can still reveal protected facts.

Bind decisions to policy and resource versions as in [DE-089](089-auditability-and-provenance.md). Test authorization after schema change, failover, restore, cache hit, federation, and backfill. A secure source plus an ungoverned result export is not end-to-end control.

### Benchmark decisions, not marketing claims

Build representative fixtures from distributions and query fingerprints without exposing production secrets. Include cold and warm caches, expected and peak concurrency, mixed workload classes, skew, small and large results, late data, schema changes, security predicates, compaction/maintenance, worker loss, source throttling, and failover.

Measure correctness first, then p50/p95/p99 end-to-end latency, queue and execution, throughput, errors/timeouts, freshness, scanned/pruned/shuffled/spilled/returned bytes, resource utilization, cache state, scale-up/down, recovery, and total cost. Repeat enough to show variance and report exclusions.

Use production shadows or replays only with authorization, minimization, load bounds, and no unsafe writes. Synthetic benchmarks are evidence for their tested envelope, not universal rankings. Re-evaluate when data, workload, prices, versions, policies, or objectives change.

### Preserve economics and reversibility

Total cost includes stored bytes and versions, compute, scans, object requests, network/egress, cache, indexes, materializations, replicas, streaming/CDC, backups, idle reserved capacity, support, engineering, on-call, migrations, and incidents. Attribute shared cost by understandable drivers without incentivizing unsafe behavior.

Prefer reversible boundaries: open file/table formats where appropriate, portable contracts, isolated connectors, reproducible projections, export paths, dual-read validation, and documented cutover. Portability is not free; common SQL syntax does not equal identical semantics, optimization, security, or operations.

Record why the design is fit, assumptions, evidence, known limits, rejected alternatives, and triggers such as concurrency, tail, freshness, cost, region, feature, or operational burden. A durable decision can be revisited without treating migration as failure.

## Definitions and Notation

For workload $w$, let arrival rate be $\lambda_w$, concurrent in-system requests $N_w$, mean response time $W_w$, scan bytes $B_s$, shuffled bytes $B_x$, returned bytes $B_r$, freshness lag $F$, and availability $A$. Under a stable long-run system, Little's Law gives $N_w=\lambda_wW_w$; bursts, time-varying rates, and percentile objectives require richer queue analysis.

Let a source expose monotonically comparable position $p_s(t)$ and serving projection expose applied position $p_m(t)$. Position lag is $\Delta_p=p_s-p_m$ when the position supports subtraction; time freshness requires mapping positions to authoritative event/source time. Never subtract unrelated offsets.

Let requested deadline $D$ and elapsed queue time $Q$. Remaining execution budget is $D-Q$ minus required return/client margin. A retry at attempt $j$ is admissible only if its predicted completion and cost fit remaining budgets and the operation is replay safe.

For $n$ independent shard response distributions $F_i(t)=P(T_i\le t)$, all-shard completion has $F_{max}(t)=\prod_iF_i(t)$. Correlation, quorum reads, early termination, replication, hedging, and partial-result contracts alter this model; validate with observed traces.

For serving keys $K$, source version $v_s(k)$ and projection version $v_m(k)$, one reconciliation condition is $v_m(k)=v_s(k)$ for all in-scope keys at a pinned comparison boundary. Missing, extra, stale, tombstoned, and unknown keys remain separate outcomes.

## Mechanisms, Invariants, or Proof Structure

### Workload-to-system mechanism

1. Inventory consumers, query shapes, data distributions, concurrency, change patterns, dependencies, governance, failures, and costs.
2. Define workload contracts with percentile/deadline, throughput, freshness, consistency, availability, result, security, recovery, and budget.
3. Name authoritative facts and versions; specify any derived projection's keys, logic, progress, correction, deletion, rebuild, reconciliation, and owner.
4. Generate warehouse, external-engine, federation, and serving alternatives; reject candidates that cannot meet semantic, governance, or recovery constraints.
5. Design physical layout, indexes/materializations, joins, pushdown, pools, admission, capacity, cancellation, retry, and degradation.
6. Instrument end-to-end query phases, freshness/watermarks, effective security, propagation, resource use, cost, and reconciliation.
7. Benchmark representative mixes under cold/warm state, skew, burst, failure, maintenance, policy, evolution, and large results.
8. Pilot with shadow/dual reads where safe; compare result semantics, latency, freshness, availability and cost at pinned versions.
9. Cut over with rollback bounds, alerts, runbooks, capacity headroom, ownership, evidence, and downstream communication.
10. Revisit on observed trigger thresholds; rebuild, repartition, reroute, or retire without abandoning authority and lifecycle invariants.

### Conditional claims and proof sketches

**Serving correctness claim.** If source versions are totally ordered per key, the materializer applies every in-scope source change exactly once in version order or idempotently to the same effect, late lower versions cannot overwrite higher versions, tombstones are retained across replay, and reconciliation at boundary $b$ shows each projection key/version equals the pinned source, then the projection represents the specified transform at $b$.

**Proof sketch.** Induct on per-key source version. The base build applies the pinned initial version. For each next version, idempotency makes duplicates neutral, the version guard rejects reordering regressions, and the transform advances state. Tombstones represent deletion. Complete delivery and reconciliation remove missing/extra/stale cases at $b$. Cross-key atomic semantics require an additional publication protocol and are not implied.

**Isolation claim.** If every workload enters through enforceable admission, each class has bounded concurrency/resources, shared dependencies have protected capacity, and cancellation releases resources within a bound, then one class cannot consume more than its allocation at modeled enforcement points.

**Proof sketch.** Admission caps admitted work; per-class resource limits cap its local consumption; protected shared capacity prevents indirect exhaustion; cancellation bounds abandoned work. Bugs, unmodeled dependencies, control-plane saturation, priority inversion, and correlated failures weaken the claim and must be fault-tested.

### Executable routing illustration

This deterministic fixture routes five simplified workload contracts by query shape, latency, and freshness. It demonstrates explicit rules, not a benchmark or product recommendation.

<!-- bijux-verify: {"id":"workload-contract-routing","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"warehouse=2\nquery_engine=1\nserving_store=2\nall_routed=true\nlow_latency_served=true\n","stderr":""}} -->
```python
workloads = [
    {"shape": "ad_hoc", "latency_ms": 30000, "freshness_s": 3600},
    {"shape": "point", "latency_ms": 50, "freshness_s": 5},
    {"shape": "object_scan", "latency_ms": 120000, "freshness_s": 900},
    {"shape": "aggregate", "latency_ms": 400, "freshness_s": 60},
    {"shape": "governed_sql", "latency_ms": 10000, "freshness_s": 600},
]


def route(workload: dict[str, object]) -> str:
    if workload["shape"] in {"point", "aggregate"} and workload["latency_ms"] < 1000:
        return "serving_store"
    if workload["shape"] == "object_scan":
        return "query_engine"
    return "warehouse"


routes = [route(workload) for workload in workloads]
for target in ("warehouse", "query_engine", "serving_store"):
    print(f"{target}={routes.count(target)}")
print(f"all_routed={len(routes) == len(workloads)}".lower())
low_latency = [route(workload) for workload in workloads if workload["latency_ms"] < 1000]
print(f"low_latency_served={set(low_latency) == {'serving_store'}}".lower())
```

## Alternatives and Trade-Offs

1. **Integrated warehouse versus external query engine.** Integration strengthens transactions, statistics, governance, and operations; external engines preserve open storage and cross-source flexibility while adding connector and metadata dependencies.
2. **Coupled versus separated storage/compute.** Coupling can improve locality and simplicity; separation enables independent scaling and pools but depends on network, caches, metadata, and storage request behavior.
3. **Direct query versus serving projection.** Direct reads reduce copies and freshness paths; projections provide predictable low latency and isolation but require synchronization, reconciliation, recovery, and lifecycle ownership.
4. **Federation versus ingestion.** Federation avoids upfront copies and accesses live state; ingestion gives stable snapshots, source isolation, repeatability, and optimization at freshness/storage cost.
5. **Scan versus index.** Scans fit broad analytics and sequential columnar work; indexes fit selective stable access while increasing write, storage, compaction, and rebuild cost.
6. **Partition versus secondary index.** Partitioning defines placement/pruning and can create hot keys; secondary indexes add access paths without changing primary placement but have consistency and amplification costs.
7. **Precompute versus compute on demand.** Precompute stabilizes latency and cost for repeated questions; on-demand execution preserves flexibility and avoids unused derived state.
8. **Reserved versus elastic/on-demand capacity.** Reservations improve isolation and price predictability but can idle; elasticity absorbs variation but has quotas, cold starts, and variable cost.
9. **Strong versus eventual consistency.** Stronger guarantees simplify some consumers but may add coordination/availability/latency constraints; eventual paths need visible versions and stale-read handling.
10. **One global store versus polyglot serving.** Consolidation reduces operations and duplication; specialized stores fit access paths. Each added store needs durable ownership and evidence of value.
11. **Broadcast versus shuffle join.** Broadcast avoids repartition for a bounded side but risks memory failure when estimates are wrong; shuffle scales both sides but pays network/spill and skew costs.
12. **Fail closed versus stale-cache degradation.** Fail closed protects correctness/freshness; a bounded marked cache may preserve availability. The workload contract determines whether stale is safer than absent.
13. **Exact versus approximate result.** Approximation reduces resources/latency but requires explicit method, error/bias, reproducibility, and exclusion from decisions needing exactness.
14. **Portability versus deep platform optimization.** Portable formats/contracts preserve options; platform-specific indexes, functions, and workload controls may deliver material benefit. Record the exit cost deliberately.

## Failure Modes and Misconceptions

1. **“A warehouse is just a large database.”** Analytical storage, execution, optimization, workload and governance assumptions differ.
2. **“A query engine owns the data.”** It may depend entirely on external catalogs, formats, files, credentials, and sources.
3. **“A serving store is a cache.”** It may be a durable derived product with correction, recovery, deletion, and reconciliation duties.
4. **“One system avoids complexity.”** Misfit workloads create hidden queues, contention, workarounds, and exports.
5. **“Polyglot is automatically best-of-breed.”** Every added stateful system multiplies ownership and synchronization.
6. **“Fast query means fresh answer.”** Cached or lagged data can return instantly.
7. **“Last refresh time proves freshness.”** It may not reflect source event/version progress or missing partitions.
8. **“Engine time is user latency.”** Queue, network, serialization, retries, result transfer, and client work matter.
9. **“Average latency is enough.”** Percentiles, deadline success, fan-out, skew, and bursts drive experience.
10. **“More workers always help.”** Coordination, shuffle, source limits, skew, and small tasks can dominate.
11. **“More shards reduce tails.”** All-shard fan-out can amplify the slowest component.
12. **“Partitioning is indexing.”** A query touching many partitions can fan out broadly despite a key.
13. **“Columnar means every query is fast.”** Poor pruning, high result volume, joins, skew, and concurrency still dominate.
14. **“Pushdown is always correct.”** Source and engine types, collation, time, null, numeric, and policy semantics can differ.
15. **“Federation avoids data movement.”** Results, intermediate data, or whole remote inputs may cross networks.
16. **“Connector support means production fitness.”** Version coverage, transactions, cancellation, limits, security, and failure semantics vary.
17. **“Dual writes keep stores synchronized.”** Partial success and retries create divergence without an authoritative protocol.
18. **“At-least-once creates duplicate business state.”** Stable identity and idempotency can make duplicate delivery harmless; naive consumers cannot.
19. **“A retry is free.”** It consumes remaining deadline, capacity, source load, and money.
20. **“Autoscaling replaces admission.”** Scaling reacts after overload and cannot protect bounded dependencies instantly.
21. **“Priority prevents delay.”** Unlimited priority can starve other critical work and overload shared planes.
22. **“Replica availability means current data.”** Applied position and consistency determine what the read observes.
23. **“Successful backfill means safe cutover.”** Live catch-up, validation, tombstones, policies, and atomic reader switch remain.
24. **“Counts matching proves equality.”** Different keys or values can share counts; reconcile versions and semantic samples/digests.
25. **“Results inherit source security.”** intermediates, caches, exports, query history, and serving copies need their own controls.
26. **“Per-query cost is total cost.”** Copies, streaming, indexes, egress, idle capacity, operations and incidents remain.
27. **“A benchmark chooses the architecture.”** It proves behavior only for its data, query mix, configuration, concurrency, cache, and failures.
28. **“SQL makes systems interchangeable.”** Dialect, types, optimizer, transactions, security, availability, and operations differ.

## Worked Examples

### Example 1

**Situation.** A BI dashboard issues the same 12 group-bys for 600 viewers. **Reasoning.** Ad hoc warehouse concurrency queues badly; incremental aggregates in a serving store meet two-second latency and five-minute freshness, while the warehouse remains authoritative for drill-down. **Conclusion.** Repeated bounded shapes justify a governed projection.

### Example 2

**Situation.** A fraud analyst changes joins and predicates daily over two years of history. **Reasoning.** A warehouse/query engine supports flexible scans and joins; precomputing every question is impossible. Resource isolation keeps exploration away from dashboards. **Conclusion.** Access uncertainty favors general analytical execution.

### Example 3

**Situation.** A federated query joins warehouse customers to a production order table. **Reasoning.** The plan would scan the remote table, overload it, and mix snapshots. The team captures a versioned CDC projection and queries that instead; rare live lookup uses bounded keys. **Conclusion.** Convenient federation can externalize load and consistency risk.

### Example 4

**Situation.** A timestamp predicate pushed to a source returns different midnight rows. **Reasoning.** Engine and source interpret timezone conversion differently. The connector disables that pushdown, fetches a bounded partition, evaluates centrally, and adds adversarial conformance tests. **Conclusion.** Saved bytes never justify semantic drift.

### Example 5

**Situation.** A hash join's build side was estimated at 50 MB but is 12 GB. **Reasoning.** Broadcast exhausts workers. Current statistics, runtime guards, repartition fallback, memory admission, and spill limits address the fault; merely adding workers may replicate more data. **Conclusion.** Estimation error and fallback are part of plan reliability.

### Example 6

**Situation.** One tenant owns 45% of events on a tenant-keyed cluster. **Reasoning.** Its partition becomes the tail. The design subpartitions heavy tenants by time/hash while preserving tenant predicates, documents fan-out, and tests rebalancing. **Conclusion.** Logical tenancy and balanced physical placement are different goals.

### Example 7

**Situation.** A read times out after applying a serving-store mutation and the client retries. **Reasoning.** The command uses an idempotency key and source version; the store returns the prior outcome rather than incrementing twice. Deadline and attempt evidence remain linked. **Conclusion.** Timeout is uncertainty, not proof of failure.

### Example 8

**Situation.** A serving rebuild resurrects deleted customers. **Reasoning.** The snapshot predates tombstones and replay omitted them. The corrected protocol pins a source position, includes current deletion state, catches up, reconciles, and only then switches reads. **Conclusion.** Rebuild is a governed migration, not bulk copying.

### Example 9

**Situation.** A warehouse query finishes in one second after nine minutes in queue. **Reasoning.** End-to-end SLO fails. Separate pools, bounded admission, dashboard projection, deadlines, and capacity address the right phase. **Conclusion.** Execution profiles without queue time misdiagnose service quality.

### Example 10

**Situation.** A proof-of-concept engine is 30% cheaper on warm single queries. **Reasoning.** Mixed concurrency, cold metadata, row policy, large results, worker failure, source throttling, egress, and operator time erase the advantage. The team records conditions under which reevaluation is warranted. **Conclusion.** Architecture evidence must match the production envelope.

## Cross-Program Connections

- [DE-063](063-table-metadata-and-snapshots.md), [DE-066](066-time-travel-and-reproducible-reads.md), and [DE-067](067-compaction-and-small-file-management.md) supply snapshot, repeatability, file-size, metadata-overhead, and scan foundations.
- [DE-068](068-clustering-and-data-skipping.md) develops physical locality, predicate alignment, and skip effectiveness for analytical scans.
- [DE-069](069-catalog-integration.md) connects engines to stable names, table formats, versions, credentials, and governed catalog state.
- [DE-071](071-completeness-validity-accuracy-and-consistency.md), [DE-073](073-reconciliation-tests.md), and [DE-074](074-freshness-and-timeliness.md) supply quality, source/projection comparison, and source-to-answer freshness contracts.
- [DE-076](076-data-contracts.md) turns query, freshness, schema and access promises into producer-consumer interfaces.
- [DE-078](078-data-incident-detection-and-triage.md) and [DE-079](079-root-cause-analysis-with-lineage.md) use query/projection evidence during failure.
- [DE-086](086-access-control-for-analytical-data.md), [DE-088](088-retention-and-deletion.md), and [DE-089](089-auditability-and-provenance.md) govern every source, intermediate, result, cache and serving copy.
- [DE-090](090-making-data-discoverable-without-losing-control.md) lets consumers find fit-for-purpose products without granting data access implicitly.
- [API-071](../../28-api-and-service-engineering/modules/071-timeout-and-deadline-budgets.md), [API-072](../../28-api-and-service-engineering/modules/072-retries-and-backoff.md), and [API-077](../../28-api-and-service-engineering/modules/077-fan-out-and-tail-latency.md) connect deadlines, retries and fan-out to serving APIs.
- [PLAT-073](../../29-platform-engineering/modules/073-resource-quotas.md) and [PLAT-077](../../29-platform-engineering/modules/077-admission-control.md) connect pools, quotas and overload admission to platform operations.
- [DE-092](../ROADMAP.md) develops materialization selection, incremental maintenance, consistency and invalidation in depth.

## References

- Google Cloud, “BigQuery Overview,” current documentation. <https://cloud.google.com/bigquery/docs/introduction>
- Snowflake, “Snowflake Key Concepts and Architecture,” current documentation. <https://docs.snowflake.com/en/user-guide/intro-key-concepts>
- Trino Software Foundation, “Trino Concepts,” current documentation. <https://trino.io/docs/current/overview/concepts.html>
- DuckDB Foundation, “DuckDB Internals Overview,” current documentation. <https://duckdb.org/docs/stable/internals/overview>
- Apache Software Foundation, “Introduction to Apache Druid,” current documentation. <https://druid.apache.org/docs/latest/design/>
- ClickHouse, “Deployment and Scaling Terminology,” current documentation. <https://clickhouse.com/docs/guides/oss/deployment-and-scaling/terminology>
- Amazon Web Services, “Core Components of Amazon DynamoDB,” current documentation. <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html>
- Apache Software Foundation, “Apache Cassandra Architecture Overview,” current documentation. <https://cassandra.apache.org/doc/latest/cassandra/architecture/overview.html>
- PostgreSQL Global Development Group, “Using EXPLAIN,” PostgreSQL 18 current documentation. <https://www.postgresql.org/docs/current/using-explain.html>
- Apache Software Foundation, “Apache Parquet,” current documentation. <https://parquet.apache.org/docs/>

## Exercises

### Exercise 1

Distinguish warehouse, query engine, connector, serving store, system of record, system of serving, replica, cache, index, and materialized projection. For each, state the authority and freshness question an architect must answer.

### Exercise 2

A workload receives 120 requests/s with average end-to-end time 0.4 s in stable conditions. Use Little's Law to estimate mean in-system concurrency. At a burst of 300 requests/s with unchanged service behavior, estimate the corresponding concurrency, then explain why neither number proves p99 capacity or stability.

### Exercise 3

Three independent shards each complete within 100 ms with probability 0.99. Compute the probability that an all-shard request finishes within 100 ms. Repeat for 30 shards. Explain how correlation, quorum, hedging, replication, and early termination change the interpretation.

### Exercise 4

Design a serving projection for customer account summaries sourced from a warehouse/CDC stream. Include keys, ordering, idempotency, source and materialization versions, late corrections, deletion, backfill/cutover, consistency, freshness, reconciliation, failure, security, recovery, and retirement.

### Exercise 5

Choose an architecture for four workloads: nightly multi-terabyte transformation, unpredictable analyst SQL, a 500-concurrent dashboard needing p95 below one second and ten-minute freshness, and an API point lookup needing p99 below 40 ms and read-your-writes. Present alternatives, physical designs, isolation, failure behavior, total cost, tests, and triggers for revisiting the choice.

## Answers to the Exercises

### Answer 1

A **warehouse** integrates owned analytical storage and execution; ask which committed snapshot is authoritative. A **query engine** executes against owned or external data; ask which catalog/source snapshot and connector semantics the query observed. A **connector** translates metadata, plans, data and credentials; ask which operations were pushed and whether semantics match.

A **serving store** owns an access-shaped state; ask whether it is authoritative for that fact or derived and to which source position it is current. A **system of record** is authoritative for a defined fact/time; a **system of serving** optimizes access and needs derivation/reconciliation. A **replica** copies a primary's state under a consistency/lag contract. A **cache** reuses a prior result under invalidation/expiry. An **index** is a maintained access structure whose consistency follows its owner. A **materialized projection** persists transformed results and needs source versions, refresh/correction, tombstones and rebuild semantics. The words alone never answer authority or freshness; the explicit contract does.

### Answer 2

Under stable long-run averages, $N=\lambda W=120\times0.4=48$ concurrent requests. If 300 requests/s could sustain the same 0.4-second mean, $N=300\times0.4=120$. This is a conditional estimate, not a capacity guarantee.

The burst may increase queue time, service time, contention, spill, remote throttling, retries, and errors; then the assumed $W$ changes and queues may grow without bound. Means do not establish p99, deadline success, skew, fan-out, cache state, memory distribution, or failure headroom. Validate with arrival distributions, duration, service-time distributions, resource bottlenecks, bounded queues, overload behavior and representative load tests.

### Answer 3

For three independent shards, all complete by 100 ms with probability $0.99^3=0.970299$, about 97.03%. For 30, $0.99^{30}\approx0.7397$, about 73.97%. More all-required shards amplify tail failure even though each shard remains 99% likely to meet the threshold.

Real shard times share network, coordinator, load and storage causes, so independence may overstate or understate the result. A quorum needs only a threshold rather than all shards. Replicas and hedges can select an early successful response but add load and correlated failure paths; losers need cancellation. Early termination is valid only when result semantics permit it. Use traces and workload-specific order-statistic models rather than applying the simple product blindly.

### Answer 4

Use stable customer ID as logical key and subpartition heavy tenants if needed. Define fields and transform version, authoritative sources, source sequence/version per key, and atomic publication boundary. Consume CDC at least once with event IDs and compare source versions; duplicates are neutral and late lower versions cannot overwrite newer state. Model corrections as later versions and deletion as durable tombstones that outlive replay.

Build from a source snapshot pinned at offset $o$, record per-key versions, then replay changes after $o$ until lag meets the cutover bound. Reconcile missing, extra, stale, tombstoned and unknown keys using population counts, version samples/digests and semantic totals. Switch readers atomically by projection generation; preserve a bounded rollback path without serving two inconsistent generations.

Specify p99 lookup, throughput, five-minute source-event freshness, read consistency and session/read-your-writes mechanism. Expose applied watermark. Admit/rate-limit by tenant, isolate materialization from reads, alert lag/dead letters/hot keys, and define stale versus unavailable behavior. Encrypt and enforce tenant/field policy at source, stream, store, cache and result; audit access without payload leakage. Back up configuration and rebuildable state as required, test store/consumer failure and source restore, apply current tombstones on rebuild, and retire only after clients migrate and derived data, logs, backups and keys satisfy lifecycle policy.

### Answer 5

Use warehouse-managed scheduled compute for the nightly transformation, with pinned inputs, partition pruning, incremental boundaries where valid, workload pool, retry/idempotency and completion evidence. Route unpredictable analyst SQL to a warehouse or object-storage query engine in an exploratory pool with scan/runtime/result/cost limits, representative connectors, and no impact on serving dependencies.

Incrementally materialize the dashboard's stable metrics into a columnar serving store or warehouse acceleration layer designed for its filters. Partition/cluster by time and tenant, preaggregate approved grains, expose source/materialization watermarks, reconcile results, and preserve warehouse drill-down. For the API point lookup, use a keyed serving store with a source-of-truth write path, idempotent projection, session token or primary read for read-your-writes, tenant isolation, and bounded fan-out. Do not route arbitrary analyst queries to either serving path.

Reserve/protect capacity for API and dashboard; bound queues and fail with explicit retry/degradation. Batch work yields first. Define cold-cache, replica lag, materializer outage, worker loss, source/object slowdown, coordinator failure and regional recovery. Cost includes warehouse capacity/scans, object requests/egress, CDC, two serving projections, indexes, replicas, backups and operations. Test correctness across systems at pinned versions; p95/p99 under mixed peak concurrency; freshness and read-your-writes; skew/hot tenants; large results; policy filters; late corrections/deletes; rebuild/failover; and total cost. Revisit when query shapes, concurrency, tail, freshness, source load, region, cost or operational burden cross recorded thresholds.
