---
module_id: SEPAT-096
program: Software Engineering: Patterns
level: 2
module_number: 96
title: Materialized View
status: complete
last_verified: 2026-08-29
---

# Materialized View

## One-Page Review

### Governing question

When should a system persist a query result, and how can it keep that derived state fresh, transactionally meaningful, rebuildable, secure and demonstrably equal to its defining computation?

### Essential definitions

- A **view** is a named query whose result is computed when read; a **materialized view** persists the result and maintains or refreshes it.
- The **defining query** (Q) maps authoritative base state (B) to intended derived relation (V=Q(B)).
- **full recomputation/refresh** reevaluates (Q) over the relevant base state and replaces the materialization.
- **incremental view maintenance (IVM)** derives a view delta (Delta V) from base deltas (Delta B) rather than recomputing everything.
- A **refresh boundary/watermark** names the source snapshot, transaction or stream position incorporated in the view.
- **freshness lag** is distance in time/positions between source authority and materialization.
- A **projection** is an application-maintained read model; a database materialized view is one implementation of persisted derivation.
- A **monotone query** only adds results as inputs grow; deletion, negation, top-k, distinct and many aggregates require retractions/support state.
- **reconciliation** independently compares materialized output with the defining query at the same boundary.
- **build-and-swap** creates a new version/target, validates and catches it up, then atomically redirects readers.

### Central model, mechanism, or theorem

Correct materialization at source boundary (p) requires (V_p=Q(B_p)). Under base transition $B' = B\oplus\Delta B$, incremental maintenance seeks

$$
Q(B\oplus\Delta B)=Q(B)\oplus\Delta Q(B,\Delta B).
$$

The delta generally depends on old state and auxiliary counts/indexes. For a sum, insert (x) adds (x), delete (x) subtracts (x); for minimum, deleting the current minimum requires finding the next candidate; for joins, one base change joins against the other current input. “Consume each change once” is insufficient unless snapshot, ordering, duplicate, delete and transaction semantics preserve the equation.

### Critical invariants

- Each view has one defining query/semantics, authority set, owner, audience, schema/version and refresh boundary.
- Readers know the view's freshness and whether it represents one consistent source boundary.
- Incremental changes are gap-free, duplicate-safe and applied in a valid ordering/transaction scope.
- Inserts, updates, deletes, key changes, nulls, duplicates and late/corrected facts preserve bag/set semantics deliberately.
- Auxiliary state for joins, aggregates, distinct and top-k is sufficient to process retractions.
- Refresh/rebuild never exposes a partial mixture unless that weaker state is explicitly acceptable.
- Indexes and physical layout support actual query workload without making refresh cost unbounded.
- The view is not command authority when staleness can violate invariants or authorization.
- Security/privacy policy applies independently to the denormalized persisted copy.
- Full recomputation/reconciliation and a versioned swap can repair drift within stated RTO.

### Common failures

Common failures are materializing without measured query cost; no freshness contract; timestamp polling; forgetting deletes; double-counting duplicate deltas; wrong bag/set semantics; `COUNT`/`SUM` errors on updates; deleting a minimum without candidate state; incomplete join changes; source transactions visible partially; refresh blocking readers/writers; “concurrent” refresh assumptions not checked against engine prerequisites; refreshing in place; no indexes; too many specialized views; using stale authorization/inventory; schema changes breaking refresh; manual repair without reproducibility; zero lag treated as equality; and sensitive cross-domain data copied into broadly accessible views.

### Compact example

An order-total view starts customer A at 30 from orders 10 and 20. Update order 10→15 is represented as delete old 10 plus insert new 15, producing 35—not adding 15 to 30. A duplicate delivery is suppressed by change identity. The view records source boundary 42. A query requiring boundary 44 must wait, fall back or report stale; it cannot infer readiness from wall time.

### Connections

[CQRS](095-command-query-responsibility-segregation.md) often uses materialized views as read models but does not require them. [Observer](037-observer.md), [CDC](093-change-data-capture-pattern.md) and [Idempotent Consumer](089-idempotent-consumer.md) supply change propagation concerns. [Repository](091-repository.md) must not mistake a stale view for aggregate authority. The successor [Strangler Fig](../ROADMAP.md) often builds comparison/read projections during migration.

## Governing Question

How do engineers decide what to precompute and choose full, incremental or streaming maintenance while keeping the persisted result semantically equivalent to a named query at a named source boundary?

A materialized view trades work at read time for work and storage before reads. It can turn repeated joins/aggregations into low-latency lookups, isolate source load, serve disconnected systems and tailor data to an audience. The cost is a new copy that can be stale, corrupt, exposed or expensive to maintain.

The pattern is not “cache some JSON.” Its defining feature is derivation from authoritative data under a reproducible query. If the view disappears, the system should know how to reconstruct it. If business staff edit it directly, authority has split and the object is no longer merely a materialized view. Design begins with the equality (V_p=Q(B_p)), its allowable delay and evidence.

## Why This Matters

Suppose an API repeatedly joins orders, customers and shipments and groups totals. Computing from authority on each request may be slow and disruptive. Persisting the result makes reads predictable. Yet the view might reflect orders through 10:00, customers through 10:03 and shipments through 09:58. A number can be internally well-formed and still lack a coherent business boundary.

Incremental maintenance is especially deceptive. Inserts are easy; deletes, updates, duplicates, null semantics, late records, joins and non-monotone aggregates are not. A current minimum cannot be repaired after deletion without other candidates. `COUNT(DISTINCT)` needs reference counts. An outer join changes when the first/last match appears. A source transaction changing several rows may be observed in pieces.

Database-native materialized views can simplify ownership and consistent refresh. Application/streaming projections provide different stores and lower latency but add distributed failure. Periodic full rebuild is often more trustworthy for small/medium data than complex IVM. Choose from query workload, change rate, freshness, consistency, recomputation cost and operational capability.

## Prerequisites and Retrieval

Learners should retrieve:

- relational algebra, selection, projection, join, grouping, bag/set and null semantics;
- database transactions, isolation, snapshots, indexes and query plans;
- CDC/log offsets, idempotency, ordering, checkpoints and deletes;
- aggregates such as count, sum, average, minimum, maximum and distinct;
- CQRS/read models, cache invalidation and source authority;
- schema migration, backfill, versioned deployment and atomic aliases;
- data classification, tenant isolation and retention;
- checksums, invariants, differential testing and reconciliation.

Before continuing, derive why an average cannot be incrementally maintained from the previous average alone after an insert or delete. Name sufficient auxiliary state.

## Learning Objectives

After this module, learners can:

1. distinguish virtual views, materialized views, caches, replicas and CQRS projections;
2. specify defining query, source boundary, freshness and authority;
3. derive delta rules for filters, joins and common aggregates;
4. identify non-monotone operations and required support state/retractions;
5. choose synchronous, scheduled full, incremental or streaming refresh;
6. preserve source transaction/order semantics and duplicate safety;
7. design indexes/layout from query and refresh workload;
8. rebuild and atomically promote a versioned view;
9. secure and independently reconcile derived copies;
10. reject materialization when direct query/cache/replica is simpler.

## Core Exposition

### Define the relation before its storage

Write the authoritative inputs, relational/query expression, filters, grouping, time and null semantics, output key, duplicates, ordering/pagination and consumer contract. Record whether data is valid-time or transaction-time and what corrections mean. Then choose persistence.

For customer spend, specify whether cancelled/refunded orders count, currency conversion date/rate/version, late corrections and decimal rounding. `customer.total` without these is not a durable view definition. The output key must be stable; otherwise incremental updates cannot locate the row. If several sources contribute, define a consistent snapshot or watermark vector rather than a fictional global timestamp.

### Choose maintenance topology

**Synchronous transaction maintenance** updates base and view in one transaction. It offers immediate consistency within the database but increases write latency/contention and couples schema. Database indexes are a familiar example of synchronously maintained derived structures.

**Scheduled full refresh** evaluates the entire query every interval. It is simple and self-healing: old errors disappear when the defining query recomputes correctly. Cost/locking and coarse freshness can be high.

**Incremental scheduled refresh** processes changes since a durable boundary. It lowers work but requires gap-free change identity, deletes and state.

**Continuous/streaming maintenance** applies deltas with low latency. It requires checkpoints, ordering, backpressure, schema history and recovery.

**On-demand/lazy refresh** recomputes after invalidation or expiry. It fits low-frequency views but produces cold-request latency/stampedes.

PostgreSQL's current built-in materialized view stores a table-like result and `REFRESH MATERIALIZED VIEW` replaces its contents. `CONCURRENTLY` allows concurrent selects but has prerequisites, including a qualifying unique index, and supports only one refresh at a time per view. These are engine/version-specific mechanics, not universal pattern guarantees.

### Derive incremental rules

For selection/projection, apply the same predicate/mapping to inserted/deleted rows. An update is logically delete-old plus insert-new, important when grouping key or predicate changes.

For group count and sum maintain `(count,sum)`. Insert (x): `count+1,sum+x`; delete: `count-1,sum-x`. Average is `sum/count` and handles empty group explicitly. For distinct, maintain occurrence counts so removing one duplicate does not remove the value prematurely.

For minimum/maximum, inserting compares one value; deleting the extremum needs an ordered multiset/index or recomputation of that group. Top-k similarly needs candidates beyond k to replace retractions. Median/quantiles require richer exact structures or declared approximation.

For join $R\bowtie S$, insertion $\Delta R^+$ adds $\Delta R^+\bowtie S$; deletion removes matches against the applicable $S$ snapshot. If both change in a transaction, delta expansion must avoid omitting/double-counting cross-terms and preserve desired atomic visibility. Outer joins require retractions/additions when match count crosses zero.

Incremental SQL engines automate some rules, but operators/functions may be unsupported or expensive. Validate actual plan/state/correctness; “incremental” does not imply bounded memory or cheap updates.

### Preserve transactions and order

A source transaction that inserts an invoice and lines should not leave a consumer-visible total without the lines if atomic visibility is required. Same-database synchronous refresh can inherit transaction semantics. Log/stream projection may need transaction markers and atomic sink apply, or it must document row-level eventual visibility.

Use stable change identity and source coordinate. A crash after apply but before checkpoint redelivers; atomically combine dedupe/version state with view mutation. Detect per-key gaps. A later full image with a larger source version can overwrite older state; deltas often do not commute and must remain ordered. Multiple source systems need source-specific watermarks and a rule for when a joined view is considered complete.

### Make freshness queryable

Publish `source_position`, `as_of`, `projector/definition_version`, last successful refresh, current lag and degraded/gap status. A scheduled view may promise “complete through the 02:00 consistent snapshot,” not “real time.” A streaming view can expose per-shard watermark.

Consumers choose behavior: accept stale for dashboard; wait for a command position; query authority; hide/mark incomplete; or fail closed for authorization/safety. Never use view generation time as source truth if processing was delayed. Do not serve a stale entitlement/medical alert merely because latency is low.

### Index for reads without destroying refresh

Materialization helps only if physical design matches queries. Choose output key, covering/filter/sort indexes, partitioning and clustering from workload. Every index increases build, refresh and storage cost. A unique index may also establish key/idempotency and enable engine concurrent refresh, but uniqueness must reflect semantics.

Measure read latency/throughput, refresh duration, write amplification, state/storage, lock/blocking, source load and catch-up. Partition refresh can limit blast radius if defining query permits independent partitions. Too many per-screen views create a maintenance portfolio; inventory owners/consumers and retire unused views.

### Evolve with build-and-swap

Changing definition/schema creates view version 2. Build into a new table/index/view, using a consistent starting boundary. Replay/apply changes to upper position (q), validate query fixtures and independently compare to direct (Q(B_q)). Continue catch-up, wait for freshness, switch a stable alias/router atomically and keep version 1 for rollback.

Do not refresh/migrate the only target in place if readers would see emptiness, partial load or mixed definitions. When the database supports atomic refresh semantics, verify version-specific behavior and locks. Schema evolution must coordinate base columns, change records, projector and readers; additive source change can still break `SELECT *` materializations.

### Reconcile as a first-class operation

Progress is not equality. At a common boundary, recompute full query or sampled/partitioned reference results and compare keys, canonical hashes, sums/counts and domain invariants. Use a separately implemented oracle where feasible so one bug is not shared. Inject missing/delete/double-count faults to prove detection.

Repair may rebuild a partition or full view, not manually edit rows. Persist discrepancy evidence, affected boundary/definition and resolution. For enormous views, stratified checks and algebraic invariants reduce cost but do not prove full equality; schedule periodic stronger evidence according to risk.

### Secure the denormalized copy

Views often join data into more sensitive combinations. Apply field minimization, row/tenant policy, encryption, access logging, retention/deletion and inference analysis. A materialized view can bypass new source authorization if its refresh account reads everything and its consumers have broad access. Treat refresh credentials and output store as production data authority dependencies, though output remains derived.

Define deletion propagation and backups. A removed source row may remain in snapshots, old view versions, caches and exports. Retaining rollback versions conflicts with erasure unless governed. Do not encode secrets into indexes/search tokens casually.

### A deterministic aggregate delta model

The executable model maintains per-customer sums/counts from insert/delete deltas, suppressing a duplicate change and representing an update as delete-old plus insert-new.

<!-- bijux-verify: {"id":"sepat-096-incremental-aggregate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"changes=1:insert-10,2:insert-20,3:delete-10,4:insert-15,duplicate-4\ncustomer=A count=2 sum=35 average=17.5\nposition=4\n","stderr":""}} -->
```python
totals = {}
seen = set()
trace = []
changes = [
    (1, "insert", "A", 10),
    (2, "insert", "A", 20),
    (3, "delete", "A", 10),
    (4, "insert", "A", 15),
    (4, "insert", "A", 15),
]
position = 0

for change_id, operation, customer, amount in changes:
    if change_id in seen:
        trace.append("duplicate-" + str(change_id))
        continue
    count, total = totals.get(customer, (0, 0))
    direction = 1 if operation == "insert" else -1
    totals[customer] = (count + direction, total + direction * amount)
    seen.add(change_id)
    position = change_id
    trace.append(str(change_id) + ":" + operation + "-" + str(amount))

count, total = totals["A"]
print("changes=" + ",".join(trace))
print("customer=A count=" + str(count) + " sum=" + str(total) + " average=" + str(total / count))
print("position=" + str(position))
```

The run proves only a sequential integer sum/count delta. It does not implement source snapshots, durable changes/checkpoints, concurrency, joins, null/bag SQL semantics, transactions, decimal/currency policy, persistence, refresh locks, security or reconciliation.

## Definitions and Notation

Let base relations at boundary (p) be $B_p=(R_{1,p},\ldots,R_{m,p})$, defining query be (Q), and materialization version (j) be (V_{j,p}). Correctness is (V_{j,p}=Q_j(B_p)) under declared bag/set, null, collation, time and numeric semantics.

Let $\Delta B_p^-$ and $\Delta B_p^+$ be deletions and insertions; an update can be modeled as one of each. Delta maintenance $D_Q(B,\Delta B)$ must satisfy $Q(B\oplus\Delta B)=Q(B)\oplus D_Q(B,\Delta B)$. The operator $\oplus$ includes multiplicity/retractions, not simple set union.

**Refresh consistency** means output corresponds to a declared source snapshot/boundary. **Freshness** measures distance from that boundary to current authority. **Availability during refresh** describes whether old complete, new complete, partial or blocked results are visible. These are independent properties.

For multiple independent sources, boundary may be vector $\mathbf p=(p_1,\ldots,p_m)$. A single “last refreshed at” does not prove each component reached equivalent business time.

## Mechanisms, Invariants, or Proof Structure

1. **Specify (Q).** Define base authority, relational/semantic rules, output key, audience and forbidden direct edits.
2. **Set consistency/freshness.** Name source boundary, lag objective, query behavior and decisions that require authority.
3. **Measure economics.** Compare direct-query cost/frequency with storage, refresh, write amplification and operations.
4. **Choose maintenance.** Synchronous, full scheduled, incremental, streaming or on-demand from risk and workload.
5. **Derive deltas.** Prove insert/delete/update rules including bags, nulls, joins, aggregates and non-monotone cases.
6. **Capture reliably.** Preserve transactions/order as required; detect gaps/duplicates and checkpoint atomically with mutation.
7. **Design physical state.** Keys, support tables/counts, indexes, partitions and bounded resource/backpressure.
8. **Expose metadata.** Definition/projector version, boundary, freshness, gap/degraded state and read-your-writes hooks.
9. **Rebuild safely.** New target, bounded build/catch-up, independent reconciliation, atomic promotion and rollback.
10. **Govern copies.** Security/privacy, retention/deletion, ownership, SLOs, recovery drills and retirement.

Delta correctness can be proven operator-by-operator under relational semantics. For `SUM`, addition/subtraction preserves equality if every multiplicity delta is applied exactly once logically; transport duplicates must be neutralized. For composition, valid delta rules compose if intermediate state/boundaries match. This conditional algebra does not prove an implementation's source capture, numeric precision, SQL null/collation or transaction behavior.

## Alternatives and Trade-Offs

**Direct query/virtual view** always uses current transaction-visible base state and avoids another copy, but can be expensive or tightly couple source availability.

**Indexes** materialize access structures automatically and may solve latency without duplicating semantic rows.

**Cache-aside** stores individual query results with TTL/invalidation; simpler for hot keys, weaker for comprehensive derived relations and repair.

**Read replica** copies base storage and offloads queries but retains similar schema and replica lag; complex queries still cost work.

**Periodic export/snapshot** replaces a whole small dataset and often gives simpler correctness/recovery than incremental streams.

**Application projection** permits different stores and event semantics; it adds delivery, schema, checkpoint and rebuild ownership.

**Data warehouse/lake transformation** fits analytical latency/history and broad joins; it may be excessive for operational millisecond reads.

**API composition/federated query** avoids copies and improves point freshness but adds runtime latency/availability fan-out.

Prefer the least complex option meeting measured latency, freshness, isolation and availability. Materialization is unnecessary when an indexed direct query is already cheap and safe.

## Failure Modes and Misconceptions

- **“Materialized means current.”** Persisted results have a boundary and lag.
- **“Refresh timestamp proves content.”** It may record process time, not consistent source position or successful completeness.
- **“Incremental means append.”** Deletes, updates and retractions are essential.
- **“Average needs only average.”** Count and sum (with numeric policy) are required.
- **“Distinct deletion removes the value.”** Only when its multiplicity reaches zero.
- **“Minimum deletion is subtractive.”** It requires next-candidate support/recomputation.
- **“Join each new row once.”** Join deltas depend on the other input state and concurrent cross-terms.
- **“At-least-once is fine.”** Only logical idempotency/dedupe prevents double counts.
- **“One watermark covers all sources.”** Independent sources need scoped/vector progress.
- **“Concurrent refresh is universal.”** Engine/version/index/locking prerequisites differ.
- **“Rebuild in place is simpler.”** It exposes partial/mixed state and weakens rollback.
- **“Zero lag proves correctness.”** Filters, mapping and delete bugs advance positions.
- **“Read-only copies are harmless.”** Denormalization increases privacy/inference and deletion surfaces.
- **“Manual row fixes solve drift.”** Without reproducible source logic, replay reintroduces it.
- **“More views always improve reads.”** Refresh/storage/ownership cost can exceed saved query work.

## Worked Examples

### Example 1

**Situation.** An indexed base query takes 8 ms at 20 requests/minute; proposed view refresh takes 40 seconds and adds on-call ownership.

**Reasoning.** Read savings are negligible and no isolation force exists. Keep direct query and monitor plan/latency.

**Conclusion.** Materialization requires measured benefit, not merely a complex-looking query.

### Example 2

**Situation.** A customer total is 30 from orders 10 and 20; order 10 updates to 15.

**Reasoning.** Treat update as deletion -10 and insertion +15, yielding 35. Adding after value alone yields incorrect 45. If grouping customer changed, retract old group and add new.

**Conclusion.** Correct incremental updates require before/after semantics, not blind accumulation.

### Example 3

**Situation.** Multiset contains values {5,5,8}; one 5 is deleted from a distinct view.

**Reasoning.** Maintain count(5)=2. Decrement to 1 and retain distinct 5. Delete only when count becomes zero.

**Conclusion.** Set-looking outputs often require bag multiplicity as auxiliary state.

### Example 4

**Situation.** Minimum response time is 12; its row is deleted.

**Reasoning.** `min-12` is meaningless. Keep an ordered multiset/candidate index or recompute the group to find next 15. Storage/write costs are the price of fast retraction.

**Conclusion.** Non-monotone aggregates require retained alternatives or recomputation.

### Example 5

**Situation.** Invoice header and three lines commit together, but projector publishes totals per received row.

**Reasoning.** Readers briefly see partial invoice. If prohibited, capture transaction boundary and apply atomically, stage until commit marker, or refresh from consistent database snapshot. If allowed, label incomplete state.

**Conclusion.** Source atomicity is not automatically preserved by row/event-wise maintenance.

### Example 6

**Situation.** A duplicate insert delta doubles a financial total while the checkpoint advances normally.

**Reasoning.** Atomically store stable change ID with aggregate mutation, or use source version compare. Reconcile sums/counts at same boundary. Exactly one transport delivery is not a safe assumption.

**Conclusion.** Logical effect-once behavior is a sink invariant, not a broker slogan.

### Example 7

**Situation.** View definition adds a filter while the team updates production rows in place.

**Reasoning.** Readers observe mixed old/new definition. Build v2 separately, reconcile against direct v2 query at q, catch up, atomically switch and retain v1 for rollback.

**Conclusion.** Definition versioning and build-and-swap make evolution coherent.

### Example 8

**Situation.** A permissions view is 30 seconds stale after revocation.

**Reasoning.** If revocation must be immediate, the view cannot authorize. Query authority, wait for revocation version or use bounded grants/fail closed. The same view may remain acceptable for displaying a member list.

**Conclusion.** Staleness acceptability belongs to the decision, not the dataset.

### Example 9

**Situation.** Positions show caught up, counts match, but tenant A and B each have one swapped row.

**Reasoning.** Global counts/lag pass. Tenant-keyed canonical digests and isolation invariants detect mismatch. Fix projector and rebuild; do not edit two rows manually.

**Conclusion.** Reconciliation must be granular enough to detect semantics/security errors.

### Example 10

**Situation.** A clinical-risk view joins diagnoses, medications and current alerts for emergency use.

**Reasoning.** Define source/version vector, maximum permissible lag by field, missing-source behavior, correction and authoritative fallback. Minimize access, protect inference, audit emergency reads and test rebuild during outage. Named human clinical-safety, privacy and security reviewers must approve stale/degraded semantics and reconciliation evidence.

**Conclusion.** High-stakes materialization requires explicit temporal provenance and human-reviewed failure behavior.

## Cross-Program Connections

- **Database Engineering:** relational algebra, query optimization, indexes, transactions and engine refresh behavior implement view semantics.
- **Data Structures/Algorithms:** auxiliary multisets, indexes, heaps and incremental algorithms determine update complexity.
- **Distributed Systems:** source boundaries, ordering, duplication, watermarks and convergence govern external projections.
- **Data Engineering:** incremental pipelines, late data, backfills, lineage and quality controls are view maintenance at scale.
- **Security Engineering:** denormalized persisted joins require independent authorization, minimization and deletion governance.
- **Architecture:** materialized views trade runtime coupling for derived-data coupling and explicit staleness.
- **Reliability Engineering:** refresh duration, lag, rebuild RTO, capacity and atomic cutover become service objectives.
- **Testing and Quality:** differential query comparison, fault injection and invariant checks establish semantic evidence.

## References

- PostgreSQL Global Development Group, [Materialized Views](https://www.postgresql.org/docs/current/rules-materializedviews.html), PostgreSQL 18 documentation, retrieved 2026-08-29. Defines PostgreSQL materialized-view persistence and refresh behavior.
- PostgreSQL Global Development Group, [REFRESH MATERIALIZED VIEW](https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html), PostgreSQL 18 documentation, retrieved 2026-08-29. Specifies replacement, locking, `CONCURRENTLY` prerequisites and restrictions.
- Microsoft Azure Architecture Center, [Materialized View Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/materialized-view), retrieved 2026-08-29. Current pattern guidance on prepopulated views, consistency and maintenance.
- Ashish Gupta and Inderpal Singh Mumick, editors, *Materialized Views: Techniques, Implementations, and Applications*, MIT Press, 1999. Foundational view-selection and maintenance treatment.
- Ashish Gupta, Inderpal Singh Mumick, and V. S. Subrahmanian, [Maintaining Views Incrementally](https://doi.org/10.1145/170035.170066), ACM SIGMOD 1993. Foundational algorithms for incremental view maintenance.
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017, chapters 11–12. Derived data, streams, recomputation and consistency foundations.
- Apache Flink Project, [Dynamic Tables](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/concepts/dynamic_tables/), stable documentation, retrieved 2026-08-29. Current streaming-table model, updates and changelog concepts.
- Materialize, [What Is Materialize?](https://materialize.com/docs/get-started/), documentation retrieved 2026-08-29. Current example of incrementally maintained SQL views; product claims are not generalized.

## Exercises

### Exercise 1

Define defining query, materialized view, refresh boundary, incremental maintenance and reconciliation. Explain how a cache and replica differ.

### Exercise 2

Derive insert/delete rules for per-department count, sum, average, minimum and distinct salary. Identify auxiliary state.

### Exercise 3

Diagnose a streaming view that is caught up but double-counts retries, retains deleted users and exposes partially committed orders.

### Exercise 4

Choose direct query, index, cache, read replica, scheduled full refresh or streaming materialized view for four workloads: product lookup, nightly tax report, live leaderboard and immediate authorization.

### Exercise 5

Design an unfamiliar multi-source disaster-response resource view. Cover temporal boundaries, joins, retractions, degradation, privacy, reconciliation, rebuild and human approval.

## Answers to the Exercises

### Answer 1

The defining query (Q) specifies intended derived relation from authoritative base state. A materialized view persists (Q(B_p)) at a named boundary (p). Refresh boundary identifies what source snapshot/positions are incorporated. Incremental maintenance computes output retractions/additions from base deltas and support state. Reconciliation independently compares stored output with direct/reference computation at the same boundary. A cache usually stores opaque request results with eviction/TTL and may lack comprehensive relational maintenance/rebuild lineage. A replica copies base data/engine representation rather than a query-specific derived relation. All can be stale, but their ownership and reconstruction contracts differ.

### Answer 2

Maintain count (n), sum (s), average (s/n) with empty-group policy. Insert salary x: `n+1,s+x`; delete: `n-1,s-x`. Average cannot use old average alone because different `(n,s)` pairs share it. For distinct salary, maintain a frequency map; insert first occurrence adds output, delete last removes it. For minimum, maintain an ordered multiset/frequency index of all group salaries or recompute the department when current minimum's last occurrence is deleted. Updates are delete-old plus insert-new, possibly across departments. Decimal/rounding/null and bag semantics must be specified; null salaries may be excluded by SQL aggregate rules but still affect row count if separately defined.

### Answer 3

Caught-up offsets do not prove correct effects. Double counts show missing atomic dedupe/source-version compare; retain stable change IDs and combine idempotency record with aggregate mutation. Deleted users indicate delete/tombstone filtering, expiry or key mismatch; test deletion and ensure recovery horizon/snapshots can reconstruct absence. Partial orders show transaction boundaries lost; buffer/stage by transaction and publish atomically, or explicitly expose incomplete status. Stop risky consumers, preserve evidence, fix a new projector version, build isolated target and reconcile keyed counts/digests plus order invariants against authority at q. Catch up and switch atomically. Add gap/duplicate/delete/transaction metrics and injected crash/reorder tests.

### Answer 4

Product lookup: indexed direct query first; cache hot immutable-ish entries if measured latency/load requires, with explicit invalidation. Nightly tax report: consistent scheduled full refresh/warehouse transformation at period boundary with financial reconciliation; streaming adds little. Live leaderboard: streaming materialized view may justify incremental top-k support and seconds-level freshness, with rebuild and anti-cheat authority elsewhere. Immediate authorization: authoritative query or synchronously maintained transaction state; a lagging view cannot safely grant after revocation. A read replica may offload product reads/reports where its lag is acceptable, but it does not eliminate query computation. Selection follows correctness and economics per workload.

### Answer 5

Name authorities for shelters, vehicles, supplies and incidents; define output keys and a vector boundary `(shelter_p,vehicle_p,supply_p,incident_p)` rather than one timestamp. Specify join rules, location validity time, reservation status, units and missing-source meaning. Maintain changes idempotently with per-source identity; represent moves/updates as retractions plus additions, retain join/match counts and transaction markers where atomic visibility matters. Mark stale/missing source components and fail closed for dispatch allocation while permitting clearly labeled situational display or authoritative fallback.

Build each definition version in an isolated target from consistent per-source snapshots plus deltas; bound replay, reconcile per agency/region keyed digests, capacity totals, no-double-assignment and privacy invariants, catch up and switch atomically. Protect precise locations/medical needs by role/agency, minimize fields, encrypt/log access and propagate deletion/retention. Test outages, late corrections, duplicate/reordered changes, source reset, regional failover and rebuild under emergency load. Named human emergency-operations, safety, privacy and security reviewers approve degradation and allocation rules; automated equality checks cannot decide their acceptable risk.
