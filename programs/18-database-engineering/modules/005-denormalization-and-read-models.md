---
module_id: DBE-005
program: Database Engineering
level: 1
module_number: 5
title: Denormalization and Read Models
status: complete
last_verified: 2026-08-30
---

# Denormalization and Read Models

## One-Page Review

### Governing question

When is duplicating or precomputing data a justified read-path optimization, and what evidence makes the duplicate correct, fresh, rebuildable, and operable?

### Essential definitions

**Denormalization** deliberately stores a derivable fact more than once or at a coarser/finer grain. A **read model** is a projection shaped for a query or consumer. A **materialized view** persists a query result. **Full refresh** recomputes from authoritative state; **incremental view maintenance** applies source deltas. **Freshness lag** is the distance between an accepted source change and its visibility in the read model. **Drift** is disagreement beyond the declared contract.

### Central model, mechanism, or theorem

Let source state be `S`, deterministic projection be `P`, and materialized state be `M`. Exact correctness requires `M=P(S)` at the observation boundary. An asynchronous contract may permit bounded lag, but must define ordering, duplicate delivery, deletes, schema versions, and failure behavior. Every optimization needs a reference rebuild, idempotent/version-aware updates, a high-water mark, reconciliation, and an atomic repair or replacement path.

### Critical invariants

- Each duplicated field has one authoritative owner and a versioned derivation.
- Read-model grain and key are explicit; one source fact cannot create accidental duplicates.
- Updates are idempotent or deduplicated and reject/ignore obsolete versions safely.
- Ordering is defined per affected key; deletes and retractions are first-class.
- Published freshness and completeness are measurable from source/projection watermarks.
- Rebuild output is comparable with incremental output under the same projection version.
- Consumers know whether reads are exact, monotonic, session-consistent, or eventually fresh.
- The added write, storage, replay, migration, and on-call cost is justified by measured benefit.

### Common failures

Failures include copying columns without ownership, dual-writing without atomicity or recovery, ignoring replays and out-of-order changes, storing aggregates without retractions, measuring only median read latency, confusing event time with processing time, refreshing without a consistent source snapshot, rebuilding into the live table, changing projection logic without versioning, declaring success from row counts alone, and operating more read models than the team can audit and retire.

### Compact example

Normalized `Customer` and `Order` relations produce `OrderCard(order_id, customer_id, customer_name, amount)`. A customer rename must update every affected card or leave measurable bounded staleness. A replayed version must not apply twice. Rebuilding from current source provides an independent reference; comparing keys and values detects a missed rename, and atomic replacement repairs it.

### Connections

[DBE-004](004-normalization-and-functional-dependencies.md) derives the normalized source. [DBE-006](../ROADMAP.md) explains catalog metadata needed to own views and dependencies. Later modules cover query cost, CDC, replication lag, recovery, observability, and online upgrades; [Data Engineering](../../19-data-engineering/ROADMAP.md) owns pipeline-scale read products.

## Governing Question

Normalization localizes truth, but consumer questions may cross many relations, aggregate billions of rows, or require a document-shaped response. Recomputing every answer can exceed latency, concurrency, or cost budgets. Denormalization trades read work for stored derivation and maintenance work.

That trade is safe only when duplication becomes an explicit subsystem. “Copy customer name into orders” leaves unanswered which name is authoritative, whether history should change after rename, how missed writes are repaired, and what a reader sees during lag. The right governing question is therefore not “should we normalize?” but “which read contract justifies materialization, and how will equivalence or bounded divergence be proved continuously?”

## Why This Matters

Denormalization can remove joins, precompute aggregates, localize data, stabilize historical snapshots, and isolate read load. It can also multiply write amplification, storage, locks, replication traffic, schema migrations, failure modes, and privacy-erasure surfaces. A faster query is not automatically a cheaper system.

The distinction between current derivation and historical fact is essential. An invoice description captured at sale time should often remain unchanged when the product is renamed; it is not merely a stale copy. A customer display name in a current dashboard may be a derivation expected to converge after rename. Both duplicate text, but their ownership and update rules differ.

Read models also change consistency. A transactionally maintained summary may be exact at commit. A materialized view refreshed nightly is a snapshot with a schedule. A CDC projection may be eventually fresh with per-key ordering and at-least-once delivery. Consumers need the actual guarantee to make correct product decisions.

## Prerequisites and Retrieval

Retrieve normalization, keys, foreign keys, joins, aggregation, transactions, logs, monotonic offsets, idempotency, snapshots, and atomic replacement. Understand that a query definition is logical while a materialization stores its result at a time and version.

This chapter uses a single-process finite model to establish basic projection invariants. It does not assume that an event broker, CDC connector, or materialized-view product automatically supplies end-to-end exactly-once semantics.

## Learning Objectives

After this module, you should be able to:

1. classify duplicated data as current derivation, aggregate, cache, snapshot, or independent fact;
2. define a read model's grain, key, projection, owner, and consumer contract;
3. compare full refresh, transactional maintenance, CDC, events, and cache-aside;
4. design idempotent, ordered incremental updates including deletes and corrections;
5. define source and projection watermarks plus freshness/completeness metrics;
6. reconcile materialized state against an independent rebuild;
7. plan backfill, cutover, rollback, and projection-version migration;
8. test duplicates, gaps, reorderings, poison records, and source schema changes;
9. quantify read benefit against write/storage/operational amplification;
10. reject denormalization when indexing, query repair, or caching already meets the need.

## Core Exposition

Begin with a measured consumer query. Record logical result, parameters, ordering, freshness need, latency distribution, concurrency, data volume, and cost. Then establish a normalized or otherwise authoritative source. Denormalization without a stable source contract creates two competing truths.

A read model has a **grain**: what one row/document represents. Its key must uniquely identify that grain. An order-card model might have one row per order; a daily seller summary has one row per `(seller_id,date)`. Mixing grains creates double counting and ambiguous updates.

Classify every stored value:

- a **derived current value** should track current source state;
- an **aggregate** combines multiple source facts and needs additions, deletions, and corrections;
- a **historical snapshot** intentionally freezes value at a business event;
- a **cache** is disposable acceleration with an authority elsewhere;
- an **independent fact** has its own lifecycle and should not be overwritten by source refresh.

Let `P_v(S)` be projection version `v` applied to a consistent source state. A full materialization is correct when `M_v=P_v(S)` for its declared snapshot/watermark. Incremental maintenance accepts changes `delta` and updates `M`. Its proof obligation is equivalence: applying all accepted deltas from a known base should produce the same result as rebuilding with `P_v` at the same source position.

**Full refresh** is conceptually simple and provides a strong oracle. It may be expensive, block reads, or require a consistent snapshot. Build into a separate destination, validate it, then atomically publish or switch consumers. Replacing live contents piecewise exposes mixtures of old and new state.

**Incremental maintenance** computes only affected output. Inserts may add rows; updates may change keys or contributions; deletes retract them. Aggregates require old and new values or a recomputable contribution ledger. `MIN`, `MAX`, distinct counts, top-k, and joins are harder than additive sums because deleting one input may require finding an alternative derivation.

**Transactional maintenance** updates source and read model in one database transaction. It gives a tight boundary but increases lock/write work and coupling. Triggers can centralize it yet hide cost and ordering. Application dual writes without a transaction or durable recovery record can commit only one side.

**Log-based CDC** reads committed changes from database logs and externalizes them. It avoids modifying every writer, but correctness still depends on snapshot handoff, offsets, retention, transaction boundaries, schema changes, source failover, and sink semantics. “CDC enabled” is a mechanism statement, not a freshness or exactly-once guarantee.

**Domain events/outbox** publish intentional semantic changes. An outbox written atomically with source state closes the source/event dual-write gap; a relay and consumers still handle duplicates, ordering, poison records, retention, and replay. Events may omit information needed for a new projection, so rebuildability requires retained events with stable semantics or a source snapshot/query path.

**Cache-aside** reads through on misses and invalidates or expires entries. It is appropriate for disposable results when bounded staleness and miss cost are acceptable. Expiry limits persistence of error; it does not guarantee freshness, and cache stampedes or authorization leakage need controls.

Idempotency means replaying an accepted change does not alter the result again. Use a stable event identity, source position, or per-entity version. A consumer may record the greatest contiguous source offset globally, but partitions make one scalar insufficient for completeness. Per-key versions prevent an old customer rename from overwriting a newer name; gap detection is still required because skipping from version 2 to 4 may hide version 3's delete or relationship change.

Ordering must match dependency scope. Per-order ordering is insufficient when a customer rename affects many orders. Cross-table projections need a transactional source position or a policy for temporary mismatches. Event time describes the domain occurrence; commit/log position establishes source serialization; processing time describes when the projector observed it. Do not substitute one clock for another.

Deletes are data. Choose tombstones, explicit retractions, validity intervals, or hard deletion. A hard-deleted source row may be unavailable when a delayed consumer tries to calculate the old aggregate contribution. Retain before-images, derivation ledgers, or rebuild capability according to the contract.

Freshness can be measured as time or positions: `now - source_commit_time_at_projection_watermark`, source high-water minus applied high-water, and per-key age for critical entities. Completeness needs contiguous processing, not merely the largest observed offset. Publish lag distributions, oldest pending item, retry counts, dead-letter age, and rebuild/audit status.

Reconciliation compares a materialization with an independently recomputed reference at the same source position and projection version. Start with key counts and key-set differences, then compare stable hashes or exact values by partition. Aggregates need totals and group-level differences. Sampled audits reduce cost but cannot prove absence of rare drift; rotate partitions and retain full rebuild capability.

Projection schemas evolve. Additive fields may support mixed versions; renamed meanings, changed keys, or altered aggregation require a new projection version. Backfill the new model from a consistent position, stream changes after that position, validate convergence, shadow reads, then switch consumers. Keep rollback until old consumers and data-retention obligations are resolved.

Security and privacy multiply with copies. Authorization must apply to the read model, not be assumed from the source. Masking, residency, retention, legal hold, and erasure must propagate to every materialization and backup. A read model optimized for broad access may accidentally widen sensitive joins.

Finally, evaluate total economics. Measure source query CPU/I/O, p50/p95/p99 latency, concurrency, cache hit rate, and failure rate before change. Then include maintenance CPU, write amplification, storage/indexes, network, lag SLO, backfills, on-call time, and migration complexity. Remove read models whose consumer value no longer pays that cost.

## Definitions and Notation

- `S_k` is authoritative source state at serialization position `k`.
- `P_v` is deterministic projection logic at version `v`.
- `M_{v,k}` is materialized state claiming coverage through `k`.
- Exact equivalence is `M_{v,k}=P_v(S_k)`.
- **Lag** is the declared distance between source and applied positions or their commit times.
- **Drift set** is the key/value symmetric difference between `M_{v,k}` and an independent `P_v(S_k)`.
- **Write amplification** counts additional durable writes caused by one source change.
- **Read amplification** counts source pages/rows/bytes/operators needed per logical result.
- A change application is idempotent when applying the same identified change twice equals applying it once.

These definitions require a common observation boundary. Comparing today's source with yesterday's view and calling every difference corruption confuses expected lag with drift.

## Mechanisms, Invariants, or Proof Structure

For every proposed read model, record: consumer/query; grain/key; source owners; projection version; maintenance route; snapshot/stream handoff; ordering/deduplication/gap rules; delete/retraction behavior; freshness SLO; reconciliation; rebuild/cutover/rollback; authorization/retention; capacity/cost; and retirement owner.

The finite model below builds order cards from normalized dictionaries. Incremental customer updates accept only a greater per-customer version and update every affected card. A duplicate version is ignored. A deliberately missed source rename produces one drifted key; deterministic rebuild repairs it.

<!-- bijux-verify: {"id":"finite-read-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial_rows=((10, 1, 'Ada', 40), (11, 2, 'Lin', 25))\nrename_applied=True\nduplicate_ignored=True\nrows_after_rename=((10, 1, 'Ada L', 40), (11, 2, 'Lin', 25))\ndrift_after_miss=(10,)\ndrift_after_rebuild=()\nsource_orders=2\nread_rows=2\n","stderr":""}} -->
```python
def rebuild(customers, orders):
    return {
        order_id: (
            order_id,
            order["customer_id"],
            customers[order["customer_id"]]["name"],
            order["amount"],
        )
        for order_id, order in orders.items()
    }


def drift_keys(customers, orders, read_model):
    expected = rebuild(customers, orders)
    keys = set(expected) | set(read_model)
    return tuple(sorted(key for key in keys if expected.get(key) != read_model.get(key)))


def apply_customer(customers, orders, read_model, customer_id, name, version):
    current = customers[customer_id]
    if version <= current["version"]:
        return False
    customers[customer_id] = {"name": name, "version": version}
    for order_id, order in orders.items():
        if order["customer_id"] == customer_id:
            read_model[order_id] = (order_id, customer_id, name, order["amount"])
    return True


customers = {
    1: {"name": "Ada", "version": 1},
    2: {"name": "Lin", "version": 1},
}
orders = {
    10: {"customer_id": 1, "amount": 40},
    11: {"customer_id": 2, "amount": 25},
}
read_model = rebuild(customers, orders)
initial = tuple(read_model[key] for key in sorted(read_model))
applied = apply_customer(customers, orders, read_model, 1, "Ada L", 2)
duplicate = apply_customer(customers, orders, read_model, 1, "stale", 2)
after_rename = tuple(read_model[key] for key in sorted(read_model))

customers[1] = {"name": "Ada Lovelace", "version": 3}
drifted = drift_keys(customers, orders, read_model)
read_model = rebuild(customers, orders)

print(f"initial_rows={initial}")
print(f"rename_applied={applied}")
print(f"duplicate_ignored={not duplicate}")
print(f"rows_after_rename={after_rename}")
print(f"drift_after_miss={drifted}")
print(f"drift_after_rebuild={drift_keys(customers, orders, read_model)}")
print(f"source_orders={len(orders)}")
print(f"read_rows={len(read_model)}")
```

The model is deterministic and bounded. It does not model concurrent commits, global offsets, gaps, deletes, aggregates, snapshots, crashes, broker/sink acknowledgments, schema evolution, or atomic publication. Its rebuild shares projection logic with the incremental card shape, so real systems need additional independent query/hash/audit implementations.

## Alternatives and Trade-Offs

**Query/index repair:** First inspect predicates, cardinality estimates, indexes, partition pruning, batching, and pagination. Avoid a new consistency subsystem when a direct query already meets the SLO.

**Virtual view:** Centralizes query semantics without stored duplication; every read pays computation. Useful when freshness must be transaction-current and cost is acceptable.

**Materialized view:** Stores query results with engine-owned definition and refresh mechanics. Refresh may be full or product-specific incremental, may block or require indexes, and has explicit staleness.

**Transactional summary table:** Tight consistency and simple reads, but every write bears maintenance and contention. Best for small, critical derived state with clear transaction ownership.

**CDC/event projection:** Decouples read stores and scales consumers, but adds lag, ordering, replay, retention, schema, and operational complexity. Use when consumer isolation or heterogeneous storage justifies it.

**Cache:** Lowest ownership for disposable acceleration, but weak completeness and invalidation. Do not use an untracked cache as the sole durable read model.

**Snapshot versus current value:** Snapshot when history must preserve event-time presentation; current projection when consumers expect rename/correction propagation. Name fields accordingly to prevent accidental refresh of historical facts.

## Failure Modes and Misconceptions

1. Denormalizing before measuring the query and workload.
2. Treating copied data as two writable authorities.
3. Failing to define grain and key.
4. Dual-writing without one transaction or durable recovery log.
5. Claiming exactly once because one component uses transactions.
6. Applying duplicates twice to counters or balances.
7. Accepting older versions after newer ones.
8. Advancing a watermark across a gap.
9. Dropping deletes or losing old aggregate contributions.
10. Mixing event, commit, and processing time.
11. Refreshing from a changing source without a snapshot boundary.
12. Rebuilding in place and exposing partial state.
13. Comparing source and view at different positions.
14. Using row counts as the only reconciliation evidence.
15. Sharing the same buggy code between incremental path and oracle.
16. Changing projection meaning without versioning/backfill.
17. Forgetting authorization, retention, residency, or erasure on copies.
18. Ignoring CDC retention and slow-consumer recovery.
19. Measuring read wins but omitting write and operational amplification.
20. Never retiring unused materializations.

## Worked Examples

### Example 1

**Situation:** A join misses its latency SLO. **Reasoning:** The plan shows a missing selective index; adding it meets p99 without duplicate state. **Conclusion:** Prefer the narrower access-path repair.

### Example 2

**Situation:** A nightly sales summary may exclude the current day. **Reasoning:** Define watermark as the last closed date and label the dashboard accordingly. Full refresh from a consistent snapshot is sufficient. **Conclusion:** Scheduled staleness can be correct when contractual.

### Example 3

**Situation:** Customer rename updates order cards asynchronously. **Reasoning:** Carry customer version, apply only newer versions, update all current cards, and measure oldest unapplied commit. **Conclusion:** The duplicated name is a governed current projection.

### Example 4

**Situation:** An invoice description must survive product rename. **Reasoning:** It records sale-time evidence, not current product name. Store it as an immutable snapshot with provenance. **Conclusion:** Do not “repair” intentional history to current source.

### Example 5

**Situation:** An at-least-once consumer increments daily revenue twice after retry. **Reasoning:** Addition is not idempotent. Deduplicate stable event IDs or maintain per-source contribution and replace it by version. **Conclusion:** Delivery semantics must compose with update algebra.

### Example 6

**Situation:** Offset 104 arrives before 103. **Reasoning:** Recording 104 as complete hides a gap. Buffer, retry, track contiguous per-partition watermarks, or rebuild. **Conclusion:** Maximum seen is not completeness.

### Example 7

**Situation:** A refund deletes/reverses an order contribution. **Reasoning:** Keep the old amount or contribution ledger so the projector can subtract it, then add any corrected value. **Conclusion:** Aggregates require retraction semantics.

### Example 8

**Situation:** A new projection changes its key. **Reasoning:** Build version 2 beside version 1, snapshot/backfill at position k, catch up changes after k, reconcile, shadow, cut over, and retain rollback. **Conclusion:** Key changes require versioned replacement, not in-place mutation.

### Example 9

**Situation:** Counts match but customer names drift. **Reasoning:** Compare key sets and per-partition value hashes/exact rows at one watermark; counts cannot detect substitutions. **Conclusion:** Reconciliation must cover content.

### Example 10

**Situation:** A read model serves no active consumer. **Reasoning:** Its CDC slot, storage, privacy surface, alerts, and migrations still cost money. Verify usage, stop writes, retain per policy, and remove ownership safely. **Conclusion:** Retirement is part of read-model design.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) covers CQRS, event-driven boundaries, and ownership.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) develops CDC, batch/stream backfills, quality, and analytical materializations.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains ordering, delivery, consistency, and failure.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) governs authorization, retention, erasure, and copied-data threat surfaces.
- Later DBE work connects read models to plans, materialized views, logs, replication lag, recovery, and capacity.

## References

1. PostgreSQL Global Development Group, [PostgreSQL 18: Materialized Views](https://www.postgresql.org/docs/18/rules-materializedviews.html), official documentation, checked 2026-08-30. Persisted query results, refresh, indexing, and explicit staleness.
2. PostgreSQL Global Development Group, [`REFRESH MATERIALIZED VIEW`](https://www.postgresql.org/docs/18/sql-refreshmaterializedview.html), official reference, checked 2026-08-30. Replacement, concurrent-refresh requirements, locking, and population behavior.
3. Ashish Gupta, Inderpal Singh Mumick, and V. S. Subrahmanian, [“Maintaining Views Incrementally”](https://www.cs.umd.edu/projects/hermes/publications/abstracts/mvi.html), SIGMOD, 1993. Author-affiliated primary algorithms for incremental maintenance including deletions, duplicates, aggregation, and recursion.
4. Ashish Gupta and Inderpal Singh Mumick, [“Maintenance of Materialized Views: Problems, Techniques, and Applications”](https://homepages.inf.ed.ac.uk/wenfei/qsx/reading/gupta95maintenance.pdf), 1995. Primary taxonomy of materialized-view maintenance.
5. Debezium Project, [Debezium 3.6 Documentation](https://debezium.io/documentation/reference/stable/index.html), official documentation, checked 2026-08-30. Current log-based CDC mechanisms and change streams.
6. Microsoft, [CQRS Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs), official Azure Architecture Center guidance, checked 2026-08-30. Separate write/read models and synchronization trade-offs.
7. Microsoft, [Materialized View Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/materialized-view), official Azure Architecture Center guidance, checked 2026-08-30. Precomputed views, update strategy, and rebuild considerations.

## Exercises

### Exercise 1

Classify a product name copied into an invoice line and a product name copied into a live search index. State the update rule for each.

### Exercise 2

An at-least-once projector maintains `daily_total += amount`. Explain the replay bug and design an idempotent alternative.

### Exercise 3

Define evidence for claiming that a read model is complete through source position 900 when events are partitioned.

### Exercise 4

Compare a virtual view, nightly materialized view, and CDC projection for a dashboard needing p99 under 200 ms and data no older than five minutes.

### Exercise 5

Design a zero-downtime replacement of a read model whose key and aggregation logic both change, including rollback and reconciliation.

## Answers to the Exercises

### Answer 1

The invoice name is a historical snapshot owned by the invoice event: retain the sale-time value and change it only through an auditable invoice correction. The search-index name is a current derivation owned by Product: propagate newer product versions and delete/retire entries according to source lifecycle. Similar bytes have different semantics.

### Answer 2

Replaying an addition double-counts. Use a stable event ID with durable deduplication, or store one contribution per source order/version and compute/maintain the daily total by replacing that contribution. Corrections subtract/replace the prior contribution. Retain deduplication state at least as long as replay is possible and rebuild from authoritative contributions.

### Answer 3

Record a contiguous applied watermark for every source partition, prove the snapshot/stream handoff, and ensure no unresolved gaps or poison records at or below each claimed offset. A global claim of 900 is valid only under a defined mapping from the source's partition vector/transaction boundary; the maximum observed event is insufficient. Publish lag, pending retries, and reconciliation at the same projection version.

### Answer 4

A virtual view gives current transaction-visible data but may fail latency/cost; test plan/index repair first. A nightly materialized view violates five-minute freshness. A CDC projection can meet both if measured end-to-end lag, ordering, replay, recovery, and reconciliation satisfy the SLO, but has the highest operational cost. An engine-supported frequently refreshed materialized view may be a simpler fourth candidate. Choose from measured refresh/query/write load, not pattern preference.

### Answer 5

Create projection version 2 beside version 1. Capture a consistent source snapshot at position `k`, backfill using new key/logic, then apply retained changes after `k` with version-aware idempotency. Compare key sets, exact/hash values, aggregate totals, and consumer queries at a common watermark; shadow reads and load test. Atomically switch consumers, monitor lag/errors, and keep version 1 fed or reproducibly recoverable for the rollback window. Roll back routing on failure; retire version 1 only after consumer, retention, privacy, and recovery approval.
