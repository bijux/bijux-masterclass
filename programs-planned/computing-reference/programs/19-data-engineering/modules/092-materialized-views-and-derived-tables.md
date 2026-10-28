---
module_id: DE-092
program: Data Engineering
level: 2
module_number: 92
title: Materialized Views and Derived Tables
status: complete
last_verified: 2026-09-03
---

# Materialized Views and Derived Tables

## One-Page Review

### Governing question

How can a data organization persist the result of a transformation for lower latency, lower repeated cost, isolation, or a stable consumer contract while proving which definition and source boundary it represents, incrementally maintaining corrections and deletions, changing it safely, rebuilding it reproducibly, and retiring it without leaving contradictory derived truth?

### Essential definitions

- A **logical view** stores a query definition and evaluates it when read; a **materialized view** persists query results and maintains or refreshes them under system-defined rules.
- A **derived table** is any persisted dataset computed from other data, whether maintained by a database, transformation tool, stream processor, or application.
- A **materialization definition** is the versioned transformation, schema, parameters, policies, and semantic contract that determine the result.
- A **source boundary** identifies the exact source snapshot, commit, offset, watermark, or transaction set represented by a materialization.
- A **full refresh** recomputes the target from the complete in-scope source boundary.
- **Incremental view maintenance** updates a prior result using changes since its prior boundary rather than recomputing all source data.
- A **delta** contains insertions, deletions, or value changes expressed with enough before/after state to update the target correctly.
- A transformation is **incrementalizable** under a given change model when its new result can be derived from prior maintained state plus source changes within bounded work.
- **Self-maintainability** means maintenance can use the materialized state and changes without querying unchanged base data; it is relative to the auxiliary state retained.
- **Monotone** transformations only add conclusions as inputs grow; non-monotone operations such as deletion, negation, some minima/maxima, and distinctness require retractions or more state.
- A **refresh policy** defines trigger, schedule/event, target lag, mode, retry, overlap, cancellation, and failure behavior.
- **Atomic publication** makes one complete materialization generation visible as a unit instead of exposing partial writes.
- A **watermark or applied position** states how far source progress is reflected; it is not proof that no eligible change is missing.
- **Backfill** computes historical scope; **catch-up** applies changes after a pinned build boundary; **cutover** switches consumers to a validated generation.
- **Reconciliation** compares source-derived expectation with materialized state at a common boundary and classifies missing, extra, stale, duplicate, and unknown outcomes.
- A **query rewrite** substitutes a compatible materialization for some or all of a query while preserving semantics and freshness requirements.

### Central model, mechanism, or theorem

For source state $B_t$, definition version $f_v$, and stored materialization $M_{v,t}$, the fundamental correctness invariant is

$$
M_{v,t}=f_v(B_t)
$$

for an explicitly named boundary $t$. With source delta $\Delta B$ taking $B_t$ to $B_{t+1}$, valid incremental maintenance uses a delta function $\delta f_v$ such that

$$
f_v(B_t\oplus\Delta B)=f_v(B_t)\oplus\delta f_v(M_{v,t},\Delta B,A_t),
$$

where $A_t$ is declared auxiliary state and $\oplus$ applies insertions and retractions. The equation is an obligation, not an assumption: joins, distinct values, minima/maxima, averages, late corrections, and deletes require sufficient keys, before-images, multiplicities, or auxiliary indexes.

A safe replacement pins boundary $b$, builds $M_{v,b}$, catches up changes $(b,c]$, validates $M_{v,c}=f_v(B_c)$ within the declared comparison, then atomically publishes generation $(v,c)$. A successful job without boundary alignment does not establish equivalence.

### Critical invariants

- Every materialization names stable ID, owner, consumers, definition/schema/policy version, source versions, grain, keys, refresh mode, and lifecycle.
- The target's declared primary or unique key matches its semantic grain; merge keys never silently collapse distinct facts.
- Source boundary and target applied boundary are durable, monotonically guarded where comparable, and queryable by consumers.
- Inserts, updates, deletes, late data, duplicates, reordering, source rewrites, schema changes, and backfills have explicit semantics.
- Incremental filters derive from durable source progress or changed-key evidence, not target `max(timestamp)` unless its assumptions are proven.
- A retry is idempotent at batch/event and target-key/version boundaries; overlapping runs cannot publish out of order.
- `SUM`/`COUNT` maintenance tracks retractions; `AVG` retains sum and count; `MIN`/`MAX` and `DISTINCT` handle deletion with sufficient candidates/multiplicity or recomputation.
- Joins account for changes on every input and multiplicity; dimension corrections update already materialized facts when required by temporal semantics.
- Full and incremental execution are tested against the same definition and source boundary.
- Publication is atomic or readers receive an explicit partial/staging state that cannot masquerade as complete.
- Freshness distinguishes source event time, captured position, processed position, committed target, and client-visible cache.
- Query rewrite is allowed only when definition containment/equivalence, policy, source, snapshot, freshness, and type semantics are compatible.
- Materialized data receives its own classification, access, masking, lineage, audit, retention, deletion, backup, and residency controls.
- Rebuild includes current tombstones, corrections, policies, reference data, code, dependencies, and deterministic parameters.
- Reconciliation uses a common pinned boundary and more than row counts: keys, versions, aggregates, samples/digests, and business invariants.
- Definition changes create a new compatible version/generation unless in-place change is proven safe; consumers migrate deliberately.
- Materializations are observed for lag, failures, duration, cost, drift, unused state, and downstream incidents, then retired when value no longer exceeds ownership cost.

### Common failures

Common failures include calling any scheduled table a materialized view; filtering incrementally on a target maximum timestamp; ignoring source updates and deletes; merging on a nonunique business key; double-adding a retried batch; refreshing overlapping partitions out of order; treating averages as averages of averages; assuming `MIN` can be maintained after deleting its winner without other state; updating facts to today's dimension value when historical-as-of semantics were promised; publishing a table partition by partition to live readers; rebuilding from current sources while comparing with an old generation; equating matching counts with equality; changing logic in place while caches and consumers still use old semantics; and retaining unused derived copies indefinitely.

### Compact example

Orders are keyed by `order_id` and have monotonically increasing per-order versions. A daily regional revenue table stores both the current per-order contribution and group sums. When order `o1` changes from 100 to 125, maintenance subtracts the prior contribution and adds the new one; when `o2` is deleted, it retracts 50; a duplicate delivery of the same version is ignored. The target records its applied source position and definition version. A pinned full rebuild produces the same keys and totals before the new generation is published. Fast aggregation is earned by explicit retraction and reconciliation, not by appending changed rows.

### Connections

[DE-035](035-incremental-models.md) introduces changed-scope computation, [DE-046](046-backfill-planning.md) develops bounded historical repair, [DE-055](055-delivery-semantics-in-streaming-pipelines.md) and [DE-056](056-exactly-once-effects.md) govern retries/effects, [DE-057](057-event-time-and-processing-time.md) and [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) govern temporal change, [DE-063](063-table-metadata-and-snapshots.md) supplies atomic versions, [DE-066](066-time-travel-and-reproducible-reads.md) supplies pinned comparisons, [DE-073](073-reconciliation-tests.md) proves source/target agreement, [DE-074](074-freshness-and-timeliness.md) defines lag, and [DE-091](091-warehouses-query-engines-and-serving-stores.md) motivates serving projections. [DE-093](../ROADMAP.md) next applies derived data to operational activation.

## Governing Question

Materialization trades repeated read work for stored state and maintenance work. It can accelerate predictable queries, isolate source systems, stabilize a consumer schema, precompute expensive semantics, or place data near a serving workload. It also creates a second representation that can be stale, inconsistent, overexposed, expensive, or orphaned.

The phrase “incremental model” hides multiple change models. Append-only events are simpler than mutable records. An update may arrive as before/after images, only a new image, or a source snapshot rewrite. Deletes may be explicit tombstones, missing-from-snapshot signals, partition replacements, or retention expiration. The view may contain filters, joins, group-bys, distinct values, windows, nondeterministic functions, or external reference data. Each combination determines what state and recomputation are necessary.

Correctness must be indexed by definition and source boundary. Two identical row sets computed under different policies or time semantics are not necessarily interchangeable. Two generations computed from different boundaries cannot be compared naively. Consumers need to know whether reads are fresh, consistent across related tables, complete, and governed for their purpose.

The governing question is therefore lifecycle-wide: when is materialization justified, what mathematical and operational state makes it maintainable, how are changes applied and published, how is equivalence tested, how do definitions migrate, and when is the copy retired?

## Why This Matters

Repeated transformations can dominate analytical cost and latency. Precomputed results reduce scans, shuffles, remote reads, and concurrency pressure. They can make interactive dashboards or data APIs possible and protect operational sources from exploratory workloads.

But derived data compounds correctness risk. An incremental predicate can permanently skip a late record. A partial refresh can mix old and new dimensions. A retry can double revenue. A deletion can remain in an aggregate after the raw record disappears. A full rebuild can resurrect data if tombstones or current policies are not applied.

Materializations also harden semantics into shared infrastructure. A daily customer metric may feed dashboards, activation, billing, and models. Changing grain, join temporal semantics, currency conversion, or null handling then becomes a contract migration, not a private query edit.

Operationally, each copy needs compute, storage, orchestration, monitoring, access control, lineage, retention, recovery, and incident response. A materialization that saves query cost but requires constant manual repair may have negative total value. Its benefits and obligations must be measured together.

## Prerequisites and Retrieval

Retrieve consumer demand: query fingerprints, frequency, concurrency, predicates, groupings, joins, result shapes, latency percentiles, freshness, consistency, availability, access policy, purpose, downstream exports, and cost.

Retrieve source semantics: stable IDs and keys, snapshots/commits/offsets, event and processing time, insert/update/delete encoding, before-images, ordering scope, duplicate identity, late/correction windows, partition replacement, retention, schema evolution, reference-data history, and transaction boundaries across inputs.

Retrieve transformation semantics: definition/code/dependency/configuration/policy versions, grain, keys, filters, joins and cardinalities, aggregations, distinctness, windows, nondeterminism, timezones, decimals, nulls, slowly changing dimensions, UDFs, external services, and approximation.

Retrieve platform behavior: database-managed view support, incremental restrictions, refresh/merge/overwrite semantics, query rewrite, indexes, partitions, locking, concurrent refresh, snapshots, staging/swap, transactions, change capture, stream state, checkpointing, recovery, and cost.

Retrieve operations: triggers, schedules, source and target watermarks, job/run/attempt IDs, overlap, priority, admission, timeouts, retries, cancellation, batch sizes, checkpoints, dead letters, partial failure, lag, full refresh, repair, backfill, catch-up, cutover, rollback, reconciliation, and incidents.

Retrieve governance/lifecycle: resource/field classifications, owner/steward, row/column/masking policy, tenant/geography, audit, lineage, retention, deletion/tombstones, legal holds, backups, restore, consumers, deprecation, cost attribution, and retirement.

Distinguish logical view from materialized view; managed materialized view from pipeline-built derived table; source event time from capture and applied progress; append from update; update from delete+insert; full refresh from partition replacement; incremental read scope from correct change scope; processing exactly once from exactly-once effect; refreshed from published; source equivalence from count equality; query rewrite from explicit direct read; schema compatibility from semantic compatibility; and rebuild from replay without tombstones.

Create a materialization contract:

| Concern | Required evidence and decision |
|---|---|
| Identity | Stable target/generation, owner, consumers, grain, key and schema |
| Definition | Code/query, dependencies, parameters, policy and semantic version |
| Boundary | Input snapshots/offsets/watermarks and target applied/published position |
| Change | Insert/update/delete, before-image, order, duplicate, late/correction and backfill |
| Maintenance | Full/delta mode, auxiliary state, trigger, overlap, retry and atomic publication |
| Verification | Pinned rebuild, key/version/digest/aggregate reconciliation and invariants |
| Service | Latency, freshness, consistency, availability, cost and degradation |
| Governance | Classification, access/masking, audit, lineage, residency, retention and deletion |
| Evolution | Compatibility, parallel generation, migration, rollback and retirement |

Write a falsifiable claim: “Materialization M generation G implements definition V7 at grain `(tenant, day, product)` from fact snapshot S42 and dimension as-of history D18; CDC through offset O900 supplies keyed before/after changes; idempotent maintenance stores source version, sum and count, retracts updates/deletes, accepts corrections for 35 days, and atomically publishes boundary B; reconciliation R compares a full computation at B by key, count, sum and digest; freshness p95 is below five minutes; policy P applies to source, staging, target and result; rebuild includes tombstones; consumers C1–C4 are pinned to V7 and retire V6 after rollback expiry.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish logical views, managed materialized views, pipeline-derived tables, caches, indexes, and serving projections;
2. state correctness as equality between a versioned definition over a source boundary and a published target generation;
3. derive incremental maintenance for inserts, updates, deletes, filters, joins, sums, counts, averages, distinct values, minima/maxima, and windows;
4. identify required keys, source versions, before-images, multiplicities, candidate sets, temporal dimension state, and auxiliary data;
5. design idempotent, ordered, overlap-safe refresh with explicit progress, retry, cancellation, and atomic publication;
6. handle late data, corrections, partition replacement, backfills, tombstones, and full rebuilds without double counting or resurrection;
7. reconcile full and incremental results at a pinned common boundary using keys, versions, aggregates, digests, and business invariants;
8. evolve definitions and schemas through parallel generations, consumer migration, validation, rollback, and retirement;
9. govern classification, access, masking, lineage, audit, retention, deletion, backup, restore, and residency of derived state; and
10. evaluate latency/cost benefit against refresh compute, storage, lag, operations, incidents, and unused-materialization debt.

## Core Exposition

### Choose what deserves materialization

Materialize when a stable repeated workload has material latency or cost, when source isolation is required, when a consumer needs a curated contract, or when data must be placed near a serving system. Capture baseline query frequency, bytes, compute, concurrency, latency, freshness tolerance, and incidents. Estimate maintenance and lifecycle cost.

Avoid copies for speculative or rapidly changing questions. A logical view may centralize semantics without stored-state drift. Better clustering, indexes, query rewrite, workload isolation, or source layout may solve the problem. The narrowest materialization that covers a family of queries often provides more reuse than a dashboard-specific final table, but overly general results lose performance.

Record consumers and usage. A target with no reads, redundant definitions, or an expired purpose should be deprecated and removed under policy. Materialization is not free just because a platform refreshes it automatically.

### Define grain, identity, and source boundary

Write one sentence defining a row: “one tenant-product-day under UTC event date and settled-order semantics.” Choose a key that is actually unique at that grain. Test null, duplicate, and collision behavior. A merge on `(day, product)` that omits tenant silently combines customers.

Version the definition, schema, code, dependencies, configuration, reference data, policy, and timezone. Identify each source snapshot, transaction boundary, offset range, or watermark. Multi-source materializations need a consistent or explicitly mixed boundary. “Current” is not a reproducible input version.

The target records definition and source boundary at generation and, where useful, per row/key. Consumers can then distinguish value time, event time, materialization time, and publication time. These fields support freshness and investigation; they do not replace independent completeness checks.

### Model deltas with insertions and retractions

Treat an update as retraction of an old contribution plus insertion of a new one when the output depends on changed fields. This requires a before-image or access to prior source/contribution state. A delete is a retraction. Append-only logic that processes only new images will overcount.

Filters need boundary transitions. If a row changes from failing to passing a predicate, insert its contribution; passing to failing, retract it; passing to passing, update affected values; failing to failing, no target change. Keys and predicate columns must be available in change evidence.

For grouped sum/count, retain both. Average is `sum/count`, not average of batch averages. Distinct counts need value multiplicities or a suitable exact/approximate data structure; deleting one occurrence must not remove a value that still appears. Deleting the current minimum or maximum requires remaining candidates or recomputation of affected groups. State cost is part of incrementalizability.

### Maintain joins and temporal meaning

A join delta depends on changes from every input. Inserting one fact may join several dimension rows if cardinality is violated. Updating a dimension can affect all prior joined facts or only future facts, depending on whether semantics are current-state or historical-as-of. Declare it.

For historical correctness, store effective intervals and join facts using event/business time under a specified late-correction policy. For current-profile views, a dimension correction may require finding and updating every affected target key. Indexes or reverse mappings become auxiliary maintenance state.

Outer joins, anti-joins, and negation are non-monotone: arrival or removal on one side can create or retract output rows. Test transitions from zero to one to multiple matches and back. Do not infer incremental support merely because SQL syntax is accepted by a tool.

### Choose full, partition, or incremental refresh

Full refresh is conceptually simple: compute $f_v(B_t)$ and replace the target. It can be the safest baseline for bounded data but consumes resources and needs atomic publication. Truncate-then-insert exposes emptiness or partial state unless isolated behind staging and swap.

Partition refresh bounds work when changes are localized and partition ownership is exact. Late data and dimension changes can affect older partitions; compute the changed partition set from evidence, not only today's date. Overwriting a partition must include its complete intended contents at the boundary.

Incremental maintenance is valuable when changes are small relative to source state and sufficient deltas/auxiliary state exist. Its complexity grows with mutable joins, deletes, long correction windows, and non-monotone operations. Maintain a full-rebuild path as a correctness oracle and recovery mechanism.

### Do not use target maxima as accidental progress

The common predicate `source.updated_at > max(target.updated_at)` assumes clocks, strict ordering, no ties, immutable timestamps, complete prior runs, and a target column representing source progress. A failed partial run can advance the maximum past missing records. Equal timestamps can be skipped. Late corrections can fall behind.

Prefer durable source offsets, change versions, transaction IDs, or overlap windows with idempotent merge. Persist input range, target generation, and completion atomically where possible. If timestamp windows are unavoidable, use inclusive overlap, stable keys/versions, deduplication, bounded lateness, and reconciliation.

Watermarks represent an assertion about progress under a source's lateness model. They are not general completeness proof. Keep captured, processed, committed, published, and consumer-visible positions distinct.

### Make refresh idempotent and publication atomic

Give each change, batch, run, attempt, target key, and definition generation stable identity. Apply only newer source versions per key, or use transactional batch markers and deterministic replacement. Duplicate delivery then produces the same state. Out-of-order older changes cannot regress it.

Prevent overlapping runs from publishing out of order with leases, compare-and-swap on applied position, transactional checkpoints, or generation promotion. Cancellation must leave staging identifiable and retryable. A timeout means outcome unknown; inspect committed state before retrying destructive replacement.

Build into a staging generation, validate schema, counts, keys, policy, and boundary, then atomically swap a pointer/view/catalog reference when supported. If consumers must read partial state, expose completion status and scope explicitly; never label it the complete generation.

### Backfill, catch up, and cut over

Pin a source boundary $b$ before bulk build. Compute historical state from snapshots and definition dependencies at $b$. Meanwhile retain or capture changes after $b$. Validate the build, replay $(b,c]$ idempotently to a target boundary $c$, pause or coordinate final change, reconcile, and publish generation $(v,c)$.

Backfills should be bounded by stable keys/partitions and carry definition/source versions. Throttle them away from live refresh and consumers. Reprocessing an interval must retract or replace prior output, not append a second contribution. Record which ranges are complete, failed, or unknown.

Rollback may mean repointing to the prior generation, but only while it still meets freshness and policy. Continue or buffer compatible changes if rapid fallback is required. Do not keep old sensitive generations indefinitely in the name of rollback.

### Reconcile at one boundary

Compute expected and observed state from the same source boundary and definition. Compare row/key sets, uniqueness, per-key source versions, group counts/sums, null/distribution constraints, and deterministic canonical digests where appropriate. Row-count equality alone misses substituted keys and values.

Use stratified samples only as supplemental evidence unless a statistical claim is defined. Full key comparison can be partitioned. Aggregated checks localize mismatches; drill down to missing, extra, stale, duplicate, value mismatch, tombstone mismatch, policy mismatch, and unknown.

Continuously reconcile high-risk targets, not only at launch. Alert by consequence and age. Automated repair should use exact bounded selectors and the same idempotent protocol; unexplained drift is an incident, not a reason to overwrite evidence silently.

### Evolve definitions with explicit generations

Classify changes: additive compatible fields, corrected bugs, changed grain/key, new temporal semantics, new source, policy changes, or breaking output meaning. A SQL text diff is not enough. Version the semantic contract and communicate which consumers can move automatically.

For breaking changes, build a parallel generation, replay representative history, compare expected deltas, shadow consumer queries, validate latency/cost/freshness/security, then migrate consumers with a rollback interval. Do not mix rows computed under incompatible definitions in one unlabeled table.

When a bug is corrected, decide whether to restate history. Record affected boundaries and downstream outputs. Rebuild or repair under the corrected version, notify consumers, and preserve sufficient provenance to explain why historical reports changed.

### Understand managed materialized-view semantics

Database-managed materialized views vary. Some use full refresh, some support restricted incremental SQL, some merge recent base changes at query time, some rewrite compatible base queries automatically, and some expose configurable target lag. Capabilities depend on product, source types, operations, regions, editions, and versions.

Inspect actual query plans to confirm rewrite, base fallback, or materialization use. Validate freshness and cost behavior under updates and deletes. A feature called “automatic” transfers maintenance implementation to the provider but not ownership of definition, access, SLO, cost, testing, or incident response.

Portable pipeline-derived tables offer control and cross-platform operation but require explicit scheduling, progress, merge, publication, and reconciliation. Choose based on the workload and required semantics, not the prestige of automation.

### Govern and operate derived state

Classify derived columns and infer sensitivity from sources, joins, aggregates, and output use. Aggregation may reduce or increase inference risk. Apply tenant, row, column, masking, purpose, and export policy to staging, target, caches, backups, and downstream copies. Query rewrite must not bypass stricter base or target policy.

Propagate deletions and retention. Tombstones prevent a rebuild from reintroducing removed records. Legal holds and snapshot retention can constrain full refresh inputs. Keep audit evidence of definition, inputs, decisions, runs, boundaries, validation, publication, access, and retirement without logging sensitive results unnecessarily.

Operate lag, queue, refresh duration, changed rows/bytes, fallback scans, target size, duplicates, late/retracted changes, dead letters, reconciliation mismatches, consumer errors, cost, and usage. Assign on-call and runbooks. A derived table is production state when a consumer depends on it.

### Evaluate total value and retire safely

Measure query time/cost saved, concurrency isolated, source load avoided, consumer reliability, freshness success, and reuse. Subtract refresh compute, storage, change capture, indexes, full rebuild, reconciliation, governance, engineering, on-call, incident, and migration cost.

Materializations can proliferate because creation is visible and deletion feels risky. Catalog consumers from query/access evidence and declared contracts. Deprecate, notify, block new dependencies, observe a defined quiet period, archive only if policy requires, then remove refresh, target, caches, grants, lineage state, backups, and keys under governed lifecycle.

Retirement evidence includes owner approval, consumer migration, last successful boundary, retention/deletion outcomes, and cost removal. Preserve definition and minimal provenance if required without retaining data indefinitely.

## Definitions and Notation

Let base relations at boundary $t$ be $B_t$, definition version be $f_v$, and materialization generation be $M_{v,t}$. Correctness is equality under declared bag/set, type, null, collation, time, policy, and approximation semantics—not byte identity unless required.

Represent changes as signed multisets $\Delta B=\Delta^+B\uplus(-\Delta^-B)$, where insertions have positive multiplicity and retractions negative. Updates can be a paired retraction/insertion. For grouped sum of measure $x$, delta for group $g$ is

$$
\Delta Sum(g)=\sum_{r\in\Delta^+B_g}x(r)-\sum_{r\in\Delta^-B_g}x(r).
$$

Maintain $Sum(g)$ and $Count(g)$ so $Avg(g)=Sum(g)/Count(g)$ when count is positive. Exact distinct count maintains multiplicity $m_g(x)$ and counts $x$ with $m_g(x)>0$. A deletion changes distinct count only when multiplicity crosses one to zero.

Let $p_s$ be latest eligible captured source position, $p_a$ applied position, and $p_p$ atomically published position, with comparable order $p_p\preceq p_a\preceq p_s$. Position lag and event-time freshness are different measures. Let generation state be `building`, `catching_up`, `validated`, `published`, `deprecated`, or `retired`.

## Mechanisms, Invariants, or Proof Structure

### Materialization lifecycle mechanism

1. Measure consumer query/service needs and determine whether a logical view, physical design, cache, managed view, or derived table is justified.
2. Define stable identity, owner, grain/key, schema, semantics, policy, consumers, SLOs, definition version, and exact source boundary model.
3. Characterize every input change: insertion, update, delete, before/after, identity/version, ordering, duplicate, lateness, correction, partition replacement, and retention.
4. Derive maintenance rules and auxiliary state for filters, joins, aggregates, distinct/min/max, windows, nondeterminism, and reference history; retain a full oracle.
5. Implement stable batch/event identity, target version guards, idempotency, checkpoints, overlap prevention, staging, cancellation, retry, and atomic publication.
6. Backfill at pinned boundary, catch up retained changes, apply current tombstones/policies, validate, reconcile at a common boundary, and cut over with bounded rollback.
7. Observe source/capture/applied/published/client progress, lag, refresh work, retries, failures, drift, security, consumer impact, usage, and total cost.
8. Evolve through explicit compatible or parallel generations; restate affected history deliberately and migrate consumers with evidence.
9. Test inserts, transitions, corrections, deletes, duplicates, reorder, late data, gaps, source rewrites, schema/policy change, overlap, crash, rebuild, failover, and restore.
10. Deprecate and retire unused or superseded state across refresh jobs, storage, grants, caches, backups, lineage, keys, and documentation.

### Correctness and publication claims

**Incremental correctness claim.** Suppose each key's source changes are completely captured with comparable versions and required before-state; the maintained delta rule is algebraically equivalent to $f_v$ for every supported change; duplicates are idempotent, older versions cannot regress state, and a common-boundary reconciliation finds no missing, extra, stale, value, or tombstone mismatches. Then published $M_{v,t}$ equals $f_v(B_t)$ under the declared semantics.

**Proof sketch.** Induct over ordered source transitions. The base full build equals $f_v(B_0)$. Each transition applies an equivalent view delta; duplicate application is neutral and reordering cannot overwrite a newer key version. Thus equality is preserved. Complete capture and reconciliation close operational gaps. The claim fails for unsupported nondeterminism, missing before-state, cross-key transactions not atomically represented, or an incomplete oracle.

**Atomic publication claim.** If readers resolve one immutable generation pointer per query/transaction, a new generation is fully built and validated before one atomic pointer change, and old generations remain readable for in-flight readers, no reader observes a partition-level mixture of old and new generations through that path.

**Proof sketch.** Before the pointer change all resolutions return old; after it all new resolutions return new; immutability preserves each generation for its reader lifetime. Direct table access, per-object cache, multi-table publication, weak client transactions, or early old-generation deletion require additional coordination.

### Executable correction and deletion illustration

This deterministic fixture maintains regional sums from versioned order changes, ignores a duplicate, retracts an update and deletion correctly, and compares with a full rebuild. It illustrates per-key state; it does not prove complete delivery, cross-key atomicity, or production recovery.

<!-- bijux-verify: {"id":"incremental-retraction-equivalence","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"groups=2\nnorth_total=125\nsouth_total=40\nduplicate_ignored=true\nincremental_matches_rebuild=true\n","stderr":""}} -->
```python
changes = [
    {"id": "o1", "version": 1, "region": "north", "amount": 100, "deleted": False},
    {"id": "o2", "version": 1, "region": "north", "amount": 50, "deleted": False},
    {"id": "o3", "version": 1, "region": "south", "amount": 40, "deleted": False},
    {"id": "o1", "version": 2, "region": "north", "amount": 125, "deleted": False},
    {"id": "o2", "version": 2, "region": "north", "amount": 50, "deleted": True},
    {"id": "o1", "version": 2, "region": "north", "amount": 125, "deleted": False},
]
current = {}
sums = {}
duplicate_ignored = False

for change in changes:
    prior = current.get(change["id"])
    if prior is not None and change["version"] <= prior["version"]:
        duplicate_ignored = True
        continue
    if prior is not None and not prior["deleted"]:
        sums[prior["region"]] -= prior["amount"]
    current[change["id"]] = change
    if not change["deleted"]:
        sums[change["region"]] = sums.get(change["region"], 0) + change["amount"]

rebuilt = {}
for order in current.values():
    if not order["deleted"]:
        rebuilt[order["region"]] = rebuilt.get(order["region"], 0) + order["amount"]
sums = {region: amount for region, amount in sums.items() if amount != 0}

print(f"groups={len(sums)}")
print(f"north_total={sums['north']}")
print(f"south_total={sums['south']}")
print(f"duplicate_ignored={duplicate_ignored}".lower())
print(f"incremental_matches_rebuild={sums == rebuilt}".lower())
```

## Alternatives and Trade-Offs

1. **Logical view versus materialization.** Logical views avoid stored-state drift and stay current but repeat work; materializations reduce latency/cost while adding refresh and lifecycle obligations.
2. **Managed materialized view versus pipeline-derived table.** Managed features integrate rewrite and maintenance but restrict SQL/platform; pipelines offer control and portability but require explicit correctness machinery.
3. **Full versus incremental refresh.** Full computation is simpler and a useful oracle; incremental work scales with change but needs richer deltas, state, and proof.
4. **Partition overwrite versus row merge.** Overwrite gives complete partition replacement and easier retractions; merge limits writes but depends on correct unique keys, versions, and delete behavior.
5. **Scheduled versus event-driven refresh.** Schedules bound operational cadence and coalesce work; events reduce lag but increase continuous state, backpressure, and ordering complexity.
6. **Push versus pull changes.** CDC/change events expose mutations quickly; source queries can recover or verify state. Combining captured deltas with periodic reconciliation is often strongest.
7. **Before-images versus target contribution state.** Before-images simplify retractions but cost capture/storage; target-side contribution state supports maintenance but becomes another governed structure.
8. **Current versus historical dimension semantics.** Current values simplify correction but restate history; as-of joins preserve historical meaning and require effective-time versions.
9. **Atomic generation swap versus in-place merge.** Swaps isolate readers and rollback cleanly but duplicate storage; in-place merge is efficient but exposes transaction/concurrency and repair complexity.
10. **Fresh fallback versus bounded staleness.** Querying base changes with a materialization can return fresher results at variable cost; bounded stale results stabilize latency. Promise one deliberately.
11. **Broad reusable aggregate versus narrow consumer table.** Broad results enable reuse but scan/store more; narrow forms optimize one contract and multiply copies.
12. **Exact versus approximate distinct/quantile state.** Exactness can require large multiplicity/state; sketches reduce it but need merge/retraction limitations and error contracts.
13. **Parallel versions versus in-place definition change.** Parallel generations enable validation and rollback but cost more; in-place changes are safe only when compatibility is proven.
14. **Continuous reconciliation versus periodic audit.** Continuous checks shorten drift duration but consume resources; periodic checks must match consequence and known failure modes.

## Failure Modes and Misconceptions

1. **“Materialized means current.”** Persisted results can lag or require base-table merge.
2. **“A derived table is only an implementation detail.”** Consumers make its schema, freshness, and meaning a contract.
3. **“Incremental means new rows.”** Updates, deletes, late arrivals, and partition rewrites are changes too.
4. **“Updated-at greater than target max is a checkpoint.”** Partial failure, ties, late clocks, and corrections break it.
5. **“An overlap window guarantees completeness.”** It helps only with bounded lateness and idempotent stable identity.
6. **“Merge is idempotent.”** A wrong/nonunique key or additive update can still duplicate effects.
7. **“Exactly-once processing means exactly-once result.”** Target transactions, identity and recovery determine the effect.
8. **“Update equals insert latest.”** Old aggregate/join contributions must be retracted.
9. **“Delete disappears downstream.”** Explicit tombstones or snapshot-difference logic must propagate it.
10. **“Average of daily averages is monthly average.”** Group sizes differ; retain sums and counts.
11. **“Distinct is just a set.”** Deleting one duplicate requires multiplicities before removing the value.
12. **“MIN and MAX are easy to subtract.”** Deleting the winner requires remaining candidate state or recomputation.
13. **“Joins change only when facts change.”** Dimension updates can affect many prior outputs.
14. **“Latest dimension value is always correct.”** Historical-as-of semantics may require the old version.
15. **“Watermark proves all data arrived.”** It is conditional on source/lateness and can coexist with capture gaps.
16. **“Full refresh is always safe.”** It can expose partial state, overload sources, change boundaries, or resurrect deletes.
17. **“Partition refresh touches only today.”** Late facts and reference corrections can reach older partitions.
18. **“A successful run is published.”** Validation or pointer swap may still fail.
19. **“Matching row counts prove equality.”** Different keys and values can have identical counts.
20. **“A sample proves no drift.”** It supplies scoped statistical evidence, not universal equality.
21. **“Rebuild can read current sources.”** Reproducibility requires pinned versions and the intended definition/policy.
22. **“Old generation is a free rollback.”** It grows exposure and becomes stale; bound its lifetime.
23. **“Automatic maintenance removes ownership.”** Consumers, semantics, policy, SLO, cost, and incidents remain.
24. **“Query rewrite is invisible and harmless.”** Verify semantic containment, freshness, policy, plan, and cost.
25. **“Aggregates are nonsensitive.”** Small groups, joins, and derived attributes can disclose protected facts.
26. **“Revoking source access protects the target.”** Materializations have independent data and grants.
27. **“Unused copies cost only storage.”** Refresh, governance, lineage, backup, attack surface, and cognitive load remain.
28. **“Definition changes should overwrite history.”** Restatement and consumer migration require explicit decisions.

## Worked Examples

### Example 1

**Situation.** A daily sales table filters `updated_at > max(target.updated_at)`. **Reasoning.** A failed run wrote one future-timestamp row, advancing the maximum beyond missing rows. Use source offsets or inclusive overlap with key/version idempotency and reconcile. **Conclusion.** Target values are not automatically trustworthy progress.

### Example 2

**Situation.** Order amount changes from 100 to 125. **Reasoning.** Aggregate maintenance retracts 100 and adds 125, using before-image/contribution state and a newer version guard. Appending 125 would produce 225. **Conclusion.** Mutable facts require signed deltas.

### Example 3

**Situation.** One of three duplicate category rows is deleted from an exact distinct count. **Reasoning.** Multiplicity falls from three to two, so distinct count stays one. A plain set receiving a delete would incorrectly remove the category. **Conclusion.** Retractions determine auxiliary state.

### Example 4

**Situation.** The minimum delivery time for a region is deleted. **Reasoning.** Retaining only the minimum cannot identify the next candidate. Maintain an ordered multiset/index or recompute the affected region. **Conclusion.** Some aggregates are cheap to add but costly to retract.

### Example 5

**Situation.** A customer dimension corrects a tier effective six months ago. **Reasoning.** Historical-as-of revenue requires recomputing affected fact intervals; current-tier reporting updates all facts by customer. The team versions two definitions rather than mixing them. **Conclusion.** Temporal join meaning precedes refresh method.

### Example 6

**Situation.** Two refresh runs overlap and the older finishes last. **Reasoning.** A compare-and-swap allows publication only if its base boundary matches current pointer; the stale run remains an unserved generation. **Conclusion.** Successful computation must not regress published progress.

### Example 7

**Situation.** A new generation is built from snapshot 500 while changes continue. **Reasoning.** Capture changes after 500, apply through 560, reconcile both expected and target at 560, then atomically switch. **Conclusion.** Pin-build-catch-up-validate is the safe cutover shape.

### Example 8

**Situation.** Counts match between base query and target. **Reasoning.** Key comparison finds one missing and one extra row; group sums find a stale correction. Counts were necessary but insufficient. **Conclusion.** Reconciliation needs multiple independent invariants.

### Example 9

**Situation.** A managed materialized view sometimes scans its base table. **Reasoning.** The engine merges recent changes or falls back to maintain freshness/semantics. Query plans and bytes reveal actual behavior; latency/cost tests include changed-base states. **Conclusion.** Persisted data does not guarantee materialization-only execution.

### Example 10

**Situation.** An aggregate has had no consumers for 120 days. **Reasoning.** Owners confirm replacements, block new dependencies, observe a deprecation window, stop refresh, remove grants/caches/data/backups under policy, and retain minimal provenance. **Conclusion.** Retirement is part of reliable materialization ownership.

## Cross-Program Connections

- [DE-035](035-incremental-models.md) introduces high-water marks, lookback, changed keys, merge and incremental/full equivalence.
- [DE-046](046-backfill-planning.md) supplies bounded selection, concurrency, checkpoint, cutover and reconciliation for historical computation.
- [DE-055](055-delivery-semantics-in-streaming-pipelines.md), [DE-056](056-exactly-once-effects.md), and [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) ground transport versus effect, identity, ordering and correction.
- [DE-057](057-event-time-and-processing-time.md) and [DE-058](058-windows-and-watermarks.md) distinguish temporal grouping, progress, lateness and finality.
- [DE-063](063-table-metadata-and-snapshots.md) and [DE-066](066-time-travel-and-reproducible-reads.md) provide atomic source/generation identities and pinned comparisons.
- [DE-071](071-completeness-validity-accuracy-and-consistency.md), [DE-072](072-schema-and-constraint-tests.md), [DE-073](073-reconciliation-tests.md), and [DE-074](074-freshness-and-timeliness.md) supply verification dimensions.
- [DE-082](082-dataset-and-column-lineage.md), [DE-086](086-access-control-for-analytical-data.md), [DE-088](088-retention-and-deletion.md), and [DE-089](089-auditability-and-provenance.md) govern derivation, access, lifecycle and proof.
- [DE-091](091-warehouses-query-engines-and-serving-stores.md) frames when a materialized serving projection is justified and how it fits a workload contract.
- [API-038](../../28-api-and-service-engineering/modules/038-concurrency-control-at-the-api-boundary.md) connects version guards and atomic publication; [API-067](../../28-api-and-service-engineering/modules/067-idempotent-consumers.md) connects duplicate delivery to target effects.
- [PLAT-034](../../29-platform-engineering/modules/034-deployment-capability.md) connects parallel generations, validation, rollback and retirement to controlled delivery.
- [DE-093](../ROADMAP.md) uses maintained derived tables to drive external operational state, adding a new side-effect boundary.

## References

- PostgreSQL Global Development Group, “Materialized Views,” PostgreSQL 18 current documentation. <https://www.postgresql.org/docs/current/rules-materializedviews.html>
- Google Cloud, “Introduction to Materialized Views,” BigQuery current documentation. <https://cloud.google.com/bigquery/docs/materialized-views-intro>
- Snowflake, “Dynamic Tables,” current documentation. <https://docs.snowflake.com/en/user-guide/dynamic-tables-about>
- dbt Labs, “About Incremental Models,” current documentation. <https://docs.getdbt.com/docs/build/incremental-models-overview>
- Materialize, “What Is Materialize?”, current documentation. <https://materialize.com/docs/get-started/>
- Apache Software Foundation, “Dynamic Tables,” Apache Flink current documentation. <https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/concepts/dynamic_tables/>
- Apache Software Foundation, “Spark Procedures,” Apache Iceberg current documentation. <https://iceberg.apache.org/docs/latest/spark-procedures/>
- Delta Lake Project, “Use Delta Lake Change Data Feed,” current documentation. <https://docs.delta.io/latest/delta-change-data-feed.html>
- Oracle, “Basic Materialized Views,” Oracle Database 26 documentation. <https://docs.oracle.com/en/database/oracle/oracle-database/26/dwhsg/basic-materialized-views.html>
- Microsoft, “Materialized Views,” Azure Data Explorer current documentation. <https://learn.microsoft.com/en-us/azure/data-explorer/kusto/management/materialized-views/materialized-view-overview>

## Exercises

### Exercise 1

Distinguish logical view, managed materialized view, derived table, index, cache, snapshot, and serving projection. State definition ownership, source-boundary, freshness, update, recovery, and governance questions for each.

### Exercise 2

A group contains values 10, 20, and 30. Apply an update 20→50, delete 10, insert another 30, then delete one 30. Recompute sum, count, average, minimum, maximum, and exact distinct count after each change. Identify the auxiliary state needed for incremental maintenance.

### Exercise 3

Design an incremental view joining mutable orders to a slowly changing customer segment and aggregating daily revenue. Cover grain/key, temporal semantics, before-images, both-input changes, late/corrected events, deletes, ordering, idempotency, watermarks, partitions, and reconciliation.

### Exercise 4

Design a zero-partial-read migration from definition V1 to breaking V2 while sources continue changing. Include pinned build boundary, capture, catch-up, validation, atomic publication, consumer migration, rollback, audit, policy, and old-generation retirement.

### Exercise 5

A company has 900 derived tables, 40% without owners, 25% without observed reads, overlapping definitions, target-max timestamp incrementals, unknown tombstone behavior, and no full-rebuild tests. Design a risk-prioritized recovery and define evidence of completion without freezing all consumers.

## Answers to the Exercises

### Answer 1

A **logical view** stores definition and computes at read, so source query snapshot/freshness and definition/access ownership matter but no persistent result recovery exists. A **managed materialized view** persists results under platform rules; verify supported change operations, refresh/rewrite, boundary, staleness, recovery, policy, and cost. A **derived table** is pipeline-owned persisted output; its team owns every one of those mechanisms explicitly.

An **index** is a maintained access structure tied to base-table semantics; ask transaction consistency, supported predicates, rebuild and storage. A **cache** reuses a prior result under key/invalidation/expiry; ask whether it is authoritative, user/policy scoped, and safe when stale. A **snapshot** is immutable source state at a boundary, not a maintained transformation. A **serving projection** is an access-shaped derived product with keys, change propagation, SLO, reconciliation, recovery and lifecycle. All persisted forms inherit classification, access, retention, deletion, audit, lineage, backup, and residency obligations.

### Answer 2

Start with multiset `{10,20,30}`: sum 60, count 3, average 20, min 10, max 30, distinct 3. After 20→50: `{10,30,50}`, sum 90, count 3, average 30, min 10, max 50, distinct 3. Delete 10: `{30,50}`, sum 80, count 2, average 40, min 30, max 50, distinct 2. Insert another 30: `{30,30,50}`, sum 110, count 3, average $110/3$, min 30, max 50, distinct 2. Delete one 30: `{30,50}`, sum 80, count 2, average 40, min 30, max 50, distinct 2.

Maintain sum and count for average; retain value multiplicities `{value: count}` for exact distinct and correct duplicate deletion. An ordered multiset or candidate index supports min/max after retractions. Before/after values or prior contribution state is necessary for update. A target storing only sum, average, min, max, and distinct count cannot generally maintain all these deletions correctly.

### Answer 3

Define one row per `(tenant, UTC event_day, segment_version or segment label)` and stable keys. Choose semantics: for historical-as-of reporting, join each order's event time to the customer's effective segment interval; corrections to intervals identify affected order/time ranges. Current-segment reporting instead moves prior contributions when a customer changes segment. Keep these as different definition versions.

Capture order and segment changes with stable IDs, versions, before/after images, source positions, and transaction context. For an order update/delete, retract its old `(day, segment)` contribution and add the new if present. For segment interval changes, find affected orders through time/customer indexes and recompute their contributions. Apply per-entity version guards and idempotent event/batch IDs; reject old reorder regressions. Use event-time lateness policy and reopen affected historical partitions rather than processing only today's date.

Record source-captured, order-applied, segment-applied and published boundaries separately; do not claim a consistent multi-source boundary without coordination. Stage complete changed partitions or transactional keyed deltas and atomically publish. Reconcile at pinned order and segment snapshots using key/version sets, per-day/segment counts and sums, sampled/canonical record digests, tombstones, uniqueness and total-revenue invariants. Periodically compare to a full as-of join and alert missing, extra, stale, temporal-overlap and unknown cases.

### Answer 4

Create immutable generation V2 rather than changing V1 rows. Pin all sources and dependencies at boundary $b$, record definition/schema/policy/configuration, and start or retain a complete change stream after $b$. Build V2 in staging from the snapshots, apply current deletions/holds/policies, validate keys/schema and full-query equivalence at $b$, then replay changes $(b,c]$ idempotently with source versions.

At $c$, reconcile V2 against V2's definition over sources at the same boundary by keys, versions, aggregates, digests and business invariants; test security, latency, freshness, cost, failure and restore. Atomically publish a versioned pointer/view so new reads resolve one complete generation. Migrate consumers in cohorts with contract tests and record their version; shadow compare V1 only where semantic changes have an expected mapping.

Rollback repoints compatible consumers while V1 remains within an explicit freshness/policy bound or uses a maintained rollback path. Audit build, decisions, boundaries, checks, publication, consumer moves and exceptions. After the rollback window and confirmed migration, deprecate V1, block new uses, then stop refresh and delete target, caches, grants, backups and keys according to retention/hold policy while preserving minimal required provenance.

### Answer 5

Inventory stable target IDs, definitions, sources, keys/grain, consumers/read evidence, owners, classifications, grants, refresh methods, boundaries, lag, failures, costs, lineage, retention and deletion. Immediately contain high-risk unknowns: sensitive ownerless outputs, external activations, permanent broad grants, broken/dead refreshes, and targets whose tombstone behavior can resurrect data. Do not mass-delete or broadly republish them.

Assign accountable owners or escalation. Classify targets by business criticality, sensitivity, consumer count, mutation/delete exposure, reconciliation status, freshness failure, cost and rebuild feasibility. Require new materializations to use the contract and reject unsafe target-max patterns. For existing targets, replace target maxima with source positions or inclusive overlap plus key/version idempotency; verify unique keys and update/delete behavior.

Confirm no-read candidates with declared consumers and seasonal windows, then deprecate and retire in bounded cohorts. Consolidate overlapping definitions only after semantic/grain/policy comparison and consumer migration. Build full-refresh or pinned oracle queries and reconciliation for critical incrementals; test duplicate, late update, delete, partial failure, overlap, rebuild and restore. Add tombstone retention and current-policy application to rebuilds.

Measure owner, consumer, classification, policy, source-boundary, key, tombstone, idempotency, full-oracle, reconciliation, freshness, recovery and retirement coverage; mismatch/incident age; target-max removal; unused/duplicate state; storage/refresh cost; and consumer migration. Completion means every active materialization has a reviewed contract, effective governance, tested change/rebuild semantics and reconciled boundary—or a named, time-bounded approved exception. Legitimate consumers stay on monitored generations while cohorts are repaired.
