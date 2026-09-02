---
module_id: DE-022
program: Data Engineering
level: 1
module_number: 22
title: Watermarks and High-Water Marks
status: complete
last_verified: 2026-09-02
---

# Watermarks and High-Water Marks

## One-Page Review

### Governing question

What progress value may an ingestion system persist and publish without skipping unseen, late, tied, out-of-order or not-yet-durable data—and how should that extraction position be distinguished from an event-time completeness estimate?

### Essential definitions

- A **position** is a source-defined or extractor-defined point in an ordered history, such as a log sequence number, opaque resume token or composite row cursor.
- A **low-water mark** is the exclusive lower boundary from which a run resumes or rewinds.
- An **extraction high-water mark** is the greatest position through which every required effect is durably represented under a declared scope and contract.
- A **candidate high bound** is a fixed upper boundary selected for a run; it is not committed progress until its interval is complete and durable.
- A **composite cursor** combines a potentially tied value with a stable unique tie-breaker, such as `(updated_at, id)` under lexicographic order.
- A **lookback** or **overlap** deliberately rereads a range before the committed mark so late changes can be recovered idempotently.
- A **partition watermark** records progress for one shard, tenant, table or other independent ordered stream.
- A **global safe watermark** is commonly the minimum of required partition watermarks, not their maximum.
- An **event-time watermark** estimates a frontier behind which events are considered late for windowing/state decisions.
- A **checkpoint** durably binds a watermark to source identity, scope, schema/configuration and downstream evidence.

### Central model, mechanism, or theorem

For a totally ordered position domain, let $D$ be positions whose required downstream effects are durable and let $R$ be positions known to exist or be closed. The safe extraction frontier is the greatest closed contiguous prefix:

$$
W=\max\{p\mid \forall q\leq p,\ q\in R\Rightarrow q\in D\}.
$$

`max(D)` is unsafe when position 4 is durable but position 3 is missing: the maximum is 4 while the safe contiguous watermark is 2.

For required partitions $i=1,\ldots,n$ with safe frontiers $W_i$, a combined computation that needs all partitions can advance only to

$$
W_{global}=\min_i W_i.
$$

For an event stream, a common bounded-out-of-orderness estimate is $E=M-L$, where $M$ is maximum observed event time and $L$ is an allowed-lateness assumption. $E$ is an operational policy frontier, not proof that no older event will arrive.

### Critical invariants

- Watermark type, position domain, ordering, inclusivity and scope are explicit.
- A committed extraction watermark never exceeds the greatest position durably reflected downstream.
- Cursor ordering is total or an opaque source token is preserved exactly; timestamp ties cannot be skipped.
- Every run fixes its upper bound before paging, and records the exact interval attempted and committed.
- Watermarks advance monotonically within one source generation; rewind/backfill uses separate state or an explicit generation change.
- All required partitions contribute to a global frontier; idle and retired partitions have explicit evidence.
- Overlap is paired with stable identity/version and idempotent effect.
- Late updates whose cursor does not advance require lookback, audit/change history or reconciliation.
- Future timestamps, clock skew, precision loss, timezone conversion and source resets cannot push progress incorrectly.
- Checkpoint metadata and downstream manifests are atomically related and independently reconcilable.

### Common failures

Persisting the maximum value merely observed; checkpointing fetched rather than durable records; using a timestamp without a tie-breaker; changing `>=` to `>` across retries; selecting “now” repeatedly during pagination; allowing one fast partition to advance a global mark; treating a quiet partition as complete; letting future-dated data leap the cursor; relying on mutable `updated_at`; overwriting the primary watermark during a backfill; comparing incomparable log positions after failover; confusing event-time lateness policy with source completeness; and resetting a watermark forward to clear backlog.

### Compact example

A page ends at `(10,a)` while another record `(10,b)` remains. Timestamp-only resume with `updated_at > 10` loses `b`; composite resume with `(updated_at,id) > (10,a)` retrieves it. Separately, durable sequence positions `{1,2,4}` have maximum 4 but safe contiguous watermark 2 because position 3 is unresolved. Both examples show that “largest seen” is not “complete through.”

### Connections

[DE-009](009-time-time-zones-and-event-timestamps.md) distinguishes time meanings, [DE-010](010-designing-a-reproducible-data-boundary.md) defines reproducible cuts, and [DE-021](021-full-and-incremental-extraction.md) introduces extraction checkpoints and snapshot/stream handoff. Planned DE-023 covers file manifests, DE-024 covers API cursors, DE-026 covers CDC offsets, and DE-058 later develops streaming windows and watermarks; see the [Data Engineering roadmap](../ROADMAP.md).

## Governing Question

What exactly does a stored progress value authorize the next extraction to omit?

That question is more useful than “what is our latest timestamp?” A safe watermark is a claim: everything in the governed scope at or before this position has been handled according to contract. The claim must survive equal timestamps, missing pages, concurrent updates, partition skew, retries, crashes, clock defects, late mutations and source failover.

Teams use “watermark” for at least two related but different ideas. Batch and CDC extraction use a position to resume without rereading all history. Stream processors use an event-time estimate to decide when to fire windows, emit final-looking results or discard state. Both describe progress, but their evidence and consequences differ. A database log position can be exact within retained history; a maximum event timestamp minus ten minutes is a lateness policy derived from observations.

The safest extraction design treats a high-water mark as a committed boundary, not an incidental maximum. It fixes a candidate high bound, processes the interval, durably commits effects, and only then advances state. A partitioned design carries a vector of positions and derives global progress conservatively.

The objective is not zero duplicate delivery. It is no skipped required effect, bounded replay and auditable completeness. Deliberate overlap plus idempotency is often safer than a brittle perfectly adjacent boundary.

## Why This Matters

A watermark converts an unbounded or changing source into bounded units of work. It enables incremental extraction, restart, lag measurement, backfill planning, window closure, state cleanup and consumer freshness reporting. A wrong watermark makes all of those confidently wrong.

Advancing too far is usually worse than lagging. A lagging checkpoint causes replay and cost; a leading checkpoint can skip data permanently after source history expires. Therefore checkpoint protocols commonly prefer at-least-once delivery and idempotent downstream effect.

Timestamps are especially deceptive. They look ordered and human-readable, yet may have coarse precision, shared values, application-clock skew, timezone ambiguity, manual corrections, future values and code paths that fail to update them. A maximum timestamp says little about whether every record below it was read.

Partitioning complicates progress. If shard A reaches time 100 and shard B reaches 80, a join requiring both cannot safely claim completeness through 100. Taking the maximum favors latency by discarding B's unresolved interval; taking the minimum protects completeness but can stall on idle or failed partitions. Idleness must be a governed signal, not an absence interpreted optimistically.

Event-time watermarks expose an unavoidable trade: wait longer for completeness or emit sooner and handle late corrections/drops. A watermark is not a natural law. Its lateness allowance should come from producer behavior, network outages, offline devices, incident history and business correction policy.

Finally, watermark state is production data. Losing, editing or mismatching it can be as damaging as corrupting the extracted dataset. It needs schema, ownership, durability, backup, audit and recovery controls.

## Prerequisites and Retrieval

Retrieve source owner and contract; source engine/API/stream/version; in-scope objects and filters; entity/event identity; candidate cursor fields; source log or opaque tokens; ordering guarantees; position comparison rules; timestamp origin, precision, timezone and mutability; update/delete behavior; commits and transactions; pagination semantics; partition/shard/tenant topology; partition lifecycle; idle signals; schema history; source head/current position; retention horizon; extraction batch size and schedule; candidate high-bound query; low-bound inclusivity; lookback window; maximum observed lateness distribution; incident/outage duration; future timestamp policy; raw event/version metadata; destination idempotency; checkpoint store; atomicity between data and state; run manifests; quarantine; reconciliation; lag/freshness objectives; backfill and repair workflows; failover/source-generation semantics; state backup; monitoring; alerts; and manual-operation controls.

Distinguish maximum observed value from safe frontier; candidate high bound from committed high-water mark; source position from event time; event time from processing and ingestion time; per-record cursor from per-partition checkpoint; scalar from vector progress; logical completion from process liveness; no new records from failed observation; idle from finished; late arrival from late source mutation; overlap from duplicate effect; source head from consumer watermark; timestamp precision from display formatting; monotonic within generation from globally comparable; rewind from normal regression; backfill progress from primary progress; event-time finality from business/accounting finality; and data freshness from watermark freshness.

Before implementation, write a watermark contract:

| Field | Required decision |
|---|---|
| Kind | Extraction position, event-time estimate, business finality or another named frontier |
| Scope | Source, table/stream, partition, tenant, filters and schema/configuration generation |
| Domain/order | Opaque token, integer sequence or composite tuple and comparison rule |
| Boundary | Exclusive low, inclusive/exclusive high and fixed high-bound selection |
| Evidence | Records/manifest durably represented and reconciliation status |
| Lateness | Lookback/allowed lateness, derivation, exceptions and correction path |
| Lifecycle | Initialization, monotonic advance, rewind, reset, failover and retirement |
| Observability | Source head, committed mark, lag, age, stalls, gaps and retention headroom |

Test candidate fields against real data: duplicates/ties, nulls, regressions, future values, update coverage, key changes, precision conversion and administrative writes. A cursor is a contract property, not just a sortable column.

## Learning Objectives

After completing this module, you should be able to:

1. define extraction, partition and event-time watermarks without conflating them;
2. distinguish maximum observed position from a safe contiguous durable frontier;
3. design composite cursors and precise batch boundaries;
4. choose fixed high bounds, overlaps and lookbacks under source behavior;
5. combine partition watermarks conservatively and handle idleness explicitly;
6. persist checkpoints only after durable downstream effect;
7. prevent future timestamps, clock skew and source resets from corrupting progress;
8. separate primary, backfill and repair watermark generations;
9. measure lag, retention headroom and late-data consequences; and
10. test and reconcile watermark behavior under failure and concurrency.

## Core Exposition

### Name the kind of watermark

Use qualified names: `orders_extraction_checkpoint`, `events_partition_offset`, `orders_event_time_watermark`, `ledger_closed_period`. A bare `watermark` invites incompatible interpretations.

An extraction watermark governs what the next read may omit. An event-time watermark governs how a stateful computation treats earlier timestamps. A business-finality marker states a domain closure policy. One may inform another, but they are not interchangeable.

Document who produces each frontier, what evidence supports it and what irreversible action follows.

### Define the position domain

Prefer a source-native ordered log position or opaque resume token when it represents committed history. Preserve opaque tokens byte-for-byte with their source and configuration identity; do not parse or compare them unless the source contract permits it.

For query extraction, define a total order. A common cursor is `(modified_at, stable_primary_key)`. If multiple versions of one key can share a timestamp, add a source version or event identity.

Never compare positions from different source generations, shards or configurations without an explicit mapping. Log sequence 500 on a promoted primary need not follow 900 on its predecessor.

### Separate observed maximum from safe progress

Seeing position 100 proves only that 100 was observed. It does not prove positions below it were complete, durable or even enumerable.

Track batch/page completeness, gaps and quarantined records. Advance a safe frontier only across a closed contiguous prefix. In sparse domains, “contiguous” means complete according to the source's closure/token protocol, not that every integer exists.

Store the candidate maximum separately for diagnostics. Naming prevents operators from copying it into the committed checkpoint.

### Establish initial state

An empty/new stream needs an explicit start policy: beginning of retained history, source snapshot cut, configured date, current head or consumer-specific subscription token. Each choice omits different data.

Record bootstrap evidence and source generation. A null checkpoint should not silently mean “start now” in one run and “start from beginning” in another.

When baseline snapshot and change stream combine, use the coordinated cut developed in DE-021. The first committed stream watermark is meaningful only relative to the accepted snapshot.

### Fix a high bound per run

Read the source head or compute a candidate high bound $H$ once at run start under the source contract. Extract only `(W,H]`. Newer records belong to a later run.

Repeatedly substituting wall-clock `now()` while paging creates a moving target. Long runs may never finish and pages can interact unpredictably with new rows.

A fixed $H$ makes counts, manifests, retries and reconciliation reproducible. Do not commit $H$ if the interval is incomplete.

### Specify interval boundaries

Write boundary predicates exactly. With exclusive committed low $W$ and inclusive candidate high $H$, use $W<x\leq H$. With composite tuples, compare the entire tuple in the same collation/order used by pagination.

Adjacent non-overlapping runs then partition positions, while a retry repeats the uncommitted interval. If an overlap is used, widen the low boundary deliberately and deduplicate by identity/version.

Test the record exactly at low and high, two records tied at both boundaries, empty intervals and precision truncation between source and state store.

### Use a stable tie-breaker

A timestamp alone is not total when multiple records share it. Store `(timestamp,key)` and order/predicate both fields lexicographically.

The key must be immutable and unique in the cursor scope. If entity keys can change, use a source event identity/version or capture old/new keys through CDC.

Do not assume the database's incidental row order resolves ties. Query plans and parallelism can change it between pages.

### Select the candidate high bound safely

A source-native current log position often bounds committed changes. A query source might select a maximum cursor from a consistent snapshot, or choose a conservative source timestamp below wall clock.

If cursor fields are populated before commit, a transaction can receive an old value, commit after the extractor passes it and be missed. A lookback can reduce risk but only a source commit/version protocol or reconciliation closes it reliably.

Validate whether high-bound discovery and subsequent pages share a snapshot. A maximum from one view plus pages from changing views can still omit backdated commits.

### Pair overlap with idempotency

With lookback $L$, next extraction rereads from $W-L$ (or an equivalent prior ordered position) through new $H$. This captures bounded late mutations and protects boundary ambiguity.

Overlap deliberately creates duplicate delivery. Retain stable event/entity identity and source version so the destination has one effect. Do not deduplicate solely by payload because two real events may be equal.

Measure the actual lateness distribution and set $L$ above a governed percentile or hard producer bound plus failure margin. Preserve a repair path for data later than $L$.

### Understand late mutation

An old entity can change today while retaining an old creation timestamp. A cursor on `created_at` will never revisit it. Use a field that advances for every relevant mutation, a change log, periodic snapshots or reconciliation.

Even `updated_at` can fail if administrative scripts bypass it, precision collapses changes, clocks move backward or values are manually edited. Test every write path.

Hard deletes require tombstones/CDC or set comparison; no scalar row watermark can query a row that no longer exists.

### Commit only durable progress

A checkpoint $W$ means all required effects through $W$ are durable. Fetching, parsing or enqueueing in volatile memory is insufficient.

If destination data and checkpoint cannot commit atomically, write an immutable batch/manifest first, apply idempotently, then persist the checkpoint. A crash before checkpoint causes replay, which is safer than skip.

Airbyte's current [protocol documentation](https://github.com/airbytehq/airbyte/blob/master/docs/platform/understanding-airbyte/airbyte-protocol.md) describes state messages as source-owned checkpoint state returned in order after destination processing. This illustrates why state content and ordering are part of a replication protocol.

### Make checkpoints self-describing

Store source system/instance, stream/table, partition, tenant/filter scope, connector and contract version, schema generation, position/token, boundary semantics, batch/manifest identity, record/control counts, prior checkpoint, commit time and operator/automation identity.

Protect with transactional replacement, checksum/version and audit history. Back up state independently and verify restore against referenced data manifests.

Reject checkpoints whose source or configuration identity differs. A syntactically valid token can be semantically poisonous in another stream.

### Keep progress monotonic within a generation

Normal commits satisfy $W_{n+1}\geq W_n$. A lower value signals corrupted state, restored backup, rewind or source-generation change and requires an explicit transition.

Do not “fix” lag by moving forward manually. Do not silently move backward and publish duplicates under a sink that is not idempotent.

Record a generation identifier so a rebootstrap or failover can begin a new monotonic sequence without pretending incomparable positions form one order.

### Separate backfill watermarks

A historical backfill should have its own interval state and publication target. It must not move the primary forward watermark or make live extraction skip history.

If live and backfill writes meet, apply source versions or deterministic precedence. Reconcile the repaired interval, then mark backfill complete through its own manifest.

Only replace the primary generation through a governed rebootstrap/cutover with an exact mapping and rollback.

### Track partition watermarks as a vector

For independent partitions, keep $\mathbf{W}=(W_1,\ldots,W_n)$. Each partition can resume and retry independently.

When downstream logic requires all partitions through one comparable time frontier, use the minimum active safe watermark. The maximum overstates completeness by ignoring laggards.

For source offsets that are not comparable across partitions, do not invent a numeric global offset. Maintain the vector and derive wall-clock lag/completeness through separate metadata.

### Handle idle partitions explicitly

A partition with no events may be healthy and quiet, disconnected, unauthorized, deleted or stalled. Absence of records is not evidence of completeness.

Use source heartbeats, end-of-range markers, partition lease/assignment state or a documented idleness timeout. A timeout is an operational assumption that can admit late records when the partition resumes.

Apache Flink's [watermark documentation](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/generating_watermarks/) explains that combined progress is held back by the minimum partition watermark and provides explicit idleness detection to prevent quiet partitions from stalling forever.

### Align fast and slow partitions

One fast source can advance far beyond a slow source, causing downstream joins to buffer large unmatched state even when the global minimum remains safe.

Throttle or align fast partitions to bound skew, state and recovery cost. This exchanges throughput/latency for resource stability.

Observe per-partition frontier, head, lag, idle status and alignment pause rather than only a single global number.

### Distinguish event time from extraction position

Event time describes when the domain event occurred. Extraction position describes where it appears in source history. A late offline event can have old event time and new source position.

Checkpoint by source position for lossless resume; use event-time watermark for window/state policy. Do not resume a source log from maximum business timestamp.

Carry both values through raw ingestion so lateness, lag and corrections remain measurable.

### Treat event-time watermarks as estimates or contracts

Apache Beam describes a [watermark](https://beam.apache.org/documentation/basics/) as an estimate of when data for an earlier event-time window is expected to have arrived. The system may emit early/on-time/late results according to triggers and allowed lateness.

A formula such as $E=M-L$ assumes bounded out-of-orderness. It does not observe unseen events. Choose $L$ from producer guarantees and empirical tails, and state whether later data is dropped, side-output, accumulated, retracted or restated.

Do not label a window permanently final unless the business's correction policy justifies that stronger claim.

### Govern allowed lateness

Longer allowed lateness retains more state and delays final output but accepts more stragglers. Shorter lateness reduces state/latency while increasing drops or corrections.

Apache Beam's [programming guide](https://beam.apache.org/documentation/programming-guide/) documents allowed lateness and late firings after the event-time watermark. Apache Spark's [Structured Streaming guide](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html) documents watermark thresholds for bounding state and explicit guarantees/limits for late data.

Measure late-record count, age, value impact and source. A “0.1 percent late” rate may conceal a high-value financial adjustment.

### Combine event-time watermarks conservatively

For a join of required inputs, the slowest relevant frontier limits when absence can be inferred. A faster-policy maximum may emit sooner but risks dropping or finalizing against the lagging input.

Spark documents minimum as the default global policy for multiple watermarks and warns that a maximum policy can aggressively drop data from slower streams.

Record the combine policy with the output. It is semantic, not just performance configuration.

### Defend against future timestamps

A device or application clock can emit an event years ahead. If maximum observed event time drives $E$, one bad record can push the watermark forward and classify valid current data as late.

Clamp/quarantine implausible event times relative to trusted ingestion/source time, use robust estimators where supported, and alert on maximum skew. Never silently rewrite domain time without retaining original evidence.

For extraction cursors, future `updated_at` can similarly leap progress. A fixed source high bound and validation policy must prevent it from authorizing skipped normal rows.

### Handle precision and timezone

Round-tripping a microsecond cursor through a seconds-only state store can move boundaries. Store canonical full precision or deliberately overlap at least the lost granularity.

Use an absolute timeline plus declared encoding; daylight-saving local times can repeat or not exist. If the source orders naive local timestamps, add a stable tie-breaker and retrieve the producer's disambiguation policy.

Test minimum/maximum representable values and serialization across language/database drivers.

### Handle source reset and failover

Log truncation, table recreation, connector-filter change, API token invalidation, shard split/merge and primary failover can invalidate position continuity.

Detect source-generation identity and reject silent comparison. If the source provides a mapping, validate it; otherwise rebootstrap from a new snapshot/change cut and reconcile.

Preserve the old checkpoint and evidence for diagnosis. Never coerce an opaque token into the new generation.

### Measure lag correctly

Track source head versus committed watermark in source-native units and, where meaningful, translate positions to commit timestamps. Also track checkpoint age, batch age, processing duration and destination publication time.

Zero position lag with an old source heartbeat may indicate producer outage, not freshness. Large byte/offset lag may contain few records; small offset lag may contain one huge transaction.

Report per-partition distributions and retention headroom: time until the oldest needed position expires under current growth.

### Reconcile the frontier

At a fixed source cut, compare source and extracted key sets, counts and control values through the claimed watermark. Confirm every batch interval is represented exactly once by effect and every checkpoint points to a complete durable manifest.

Sample rows around boundaries and ties. Periodically re-extract an overlap/partition or full snapshot to detect old mutations outside the lookback.

Reconciliation can reveal that the watermark contract is wrong even when state advances monotonically.

### Monitor and alert

Monitor committed/candidate/head positions, per-partition lag, frontier age, non-advancement, regressions, gaps, duplicate/replayed volume, late records, too-late drops, future timestamps, overlap volume, checkpoint failures, state/data mismatch, retention headroom and reconciliation drift.

Alert on consequence and trend. A watermark can be unchanged legitimately on an idle source; combine stall with heartbeat/head/partition evidence.

Every alert needs an owner and action: retry, pause publication, extend retention, rewind, repair, rebootstrap or investigate the producer.

### Test state-machine transitions

Exercise first run, empty source, tied cursors, empty interval, partial page, crash before/after data commit, crash during checkpoint replacement, duplicate state message, out-of-order checkpoint, future record, late update, hard delete, idle partition, partition reactivation, schema change, retention expiry, failover, backfill and rebootstrap.

Assert data, checkpoint, manifests, lag metrics, alerts and next-query boundaries after every transition.

Use model-based tests that generate records and failures, then compare incremental state to an authoritative full reconstruction at the same cut.

## Definitions and Notation

Let $(P,\leq)$ be a totally ordered position domain for one source generation and scope. Let $D\subseteq P$ be positions whose required effects are durably represented. Let $R\subseteq P$ represent positions known to exist or source intervals known closed.

The safe extraction watermark is the greatest closed prefix:

$$
W=\max\{p\in P\mid \forall q\leq p,\ q\in R\Rightarrow q\in D\}.
$$

For dense integer positions with durable set $D$, a simpler frontier is the greatest $w$ such that $\{1,\ldots,w\}\subseteq D$. This is not `max(D)` when gaps exist.

Let $H_n$ be the fixed candidate high bound for run $n$. A non-overlap extraction interval is

$$
B_n=(W_{n-1},H_n].
$$

After every required effect in $B_n$ is durable and verified, commit $W_n=H_n$. With overlap operator $back(W,L)$, read $(back(W_{n-1},L),H_n]$ but keep the logical committed frontier monotonic and make duplicate effects idempotent.

For cursor tuple $x(r)=(u(r),k(r))$, lexicographic order is

$$
(u_1,k_1)<_{lex}(u_2,k_2)\iff u_1<u_2\ \lor\ (u_1=u_2\land k_1<k_2).
$$

For required comparable partition frontiers $\mathbf{W}=(W_1,\ldots,W_n)$,

$$
W_{global}=\min_iW_i.
$$

Let event timestamp of record $r$ be $e(r)$ and maximum trusted observed event time be $M$. A bounded-out-of-orderness policy may estimate

$$
E=M-L
$$

for allowed lateness $L\geq0$. Records with event time behind $E$ are late under that policy; handling is a separate explicit rule.

Watermark lag may be position distance $lag_p=head_p-W_p$ when subtraction is meaningful, or time lag $lag_t=head_{commit\_time}-W_{commit\_time}$. Neither alone proves completeness.

## Mechanisms, Invariants, or Proof Structure

**Watermark-commit mechanism.** Load prior self-describing checkpoint; verify source/configuration generation; fix $H$; read exact ordered interval with stable pagination; land a complete manifest; apply idempotently; validate; then atomically commit a new checkpoint referencing durable evidence.

**Contiguous-prefix theorem.** If every required position at or before $W$ has durable effect, restart strictly after $W$ cannot skip required history through $W$. `max(D)` lacks this implication when a required lower position is absent.

**Composite-cursor theorem.** When $u$ can tie and $k$ is stable/unique within each $u$, lexicographic $(u,k)$ totally orders records. Resumption strictly after the last tuple retrieves unconsumed equal-$u$ keys; resumption on $u$ alone cannot distinguish them.

**Checkpoint safety invariant.** Let $P_d$ be greatest durable position and $P_c$ committed checkpoint. Require $P_c\leq P_d$. A strict inequality causes bounded replay; $P_c>P_d$ permits loss.

**Partition-minimum theorem.** A result requiring every partition cannot be complete beyond the least complete partition. Therefore the minimum is the greatest scalar frontier implied by all $W_i$; the maximum is implied by only one.

**Monotonicity invariant.** Within one source/scope/configuration generation, $W_{n+1}\geq W_n$. Rewind or incomparable failover creates explicit state/generation rather than hidden regression.

**Overlap invariant.** Rereading a lookback is safe only if repeated source versions/events have one downstream effect and the lookback covers the assumed lateness class. It does not repair changes older than the overlap.

**Event-time evidence boundary.** $E=M-L$ is derived from observed maximum and assumed lateness. Without a producer guarantee, it cannot prove no unseen record has $e<E$.

<!-- bijux-verify: {"id":"safe-watermark-frontiers","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"batch_ids=('b', 'c')\nnext_checkpoint=(11, 'a')\ntimestamp_only_loses_tie=True\ncontiguous_watermark=2\nnaive_max=4\ngap_detected=True\npartition_watermark=101\nevent_time_watermark=100\nlate_event_is_late=True\nmonotonic_commit=True\n","stderr":""}} -->
```python
records = (
    {"id": "a", "cursor": (10, "a")},
    {"id": "b", "cursor": (10, "b")},
    {"id": "c", "cursor": (11, "a")},
    {"id": "d", "cursor": (12, "a")},
)
prior = (10, "a")
candidate_high = (11, "a")
batch = tuple(row for row in records if prior < row["cursor"] <= candidate_high)

timestamp_only = tuple(row for row in records if row["cursor"][0] > prior[0])
timestamp_only_loses_tie = records[1] not in timestamp_only

durable_positions = {1, 2, 4}
contiguous = 0
while contiguous + 1 in durable_positions:
    contiguous += 1

partition_frontiers = {"p0": 104, "p1": 101, "p2": 103}
global_frontier = min(partition_frontiers.values())
trusted_event_times = (97, 100, 105)
allowed_lateness = 5
event_watermark = max(trusted_event_times) - allowed_lateness
late_event_time = 99

print(f"batch_ids={tuple(row['id'] for row in batch)}")
print(f"next_checkpoint={candidate_high}")
print(f"timestamp_only_loses_tie={timestamp_only_loses_tie}")
print(f"contiguous_watermark={contiguous}")
print(f"naive_max={max(durable_positions)}")
print(f"gap_detected={contiguous != max(durable_positions)}")
print(f"partition_watermark={global_frontier}")
print(f"event_time_watermark={event_watermark}")
print(f"late_event_is_late={late_event_time < event_watermark}")
print(f"monotonic_commit={candidate_high >= prior}")
```

The executable example proves only these finite calculations. It does not establish a source's closure, durability, lateness or token guarantees.

## Alternatives and Trade-Offs

**Source-native token versus user-selected cursor.** Native tokens align with source history and deletes but may be opaque/retention-bound. User cursors are portable and queryable but depend on mutation and ordering discipline.

**Single field versus composite cursor.** A single monotonic unique sequence is simple. Composite tuples handle tied timestamps but require stable collation, key and serialization.

**Exclusive resume versus inclusive overlap.** Exact exclusive resume reduces duplicates but is fragile under precision and late mutation. Inclusive/lookback overlap costs rereads and needs idempotency but protects known uncertainty.

**Wall-clock high bound versus source position.** Wall clock is intuitive but affected by skew/commit timing. Source positions better represent history but may not map directly to business freshness.

**Global scalar versus partition vector.** A scalar simplifies reporting but may be meaningless for incomparable offsets. A vector preserves truth while requiring richer state and dashboards.

**Minimum versus maximum combine policy.** Minimum protects lagging required inputs and increases latency/state. Maximum emits sooner but can drop or finalize against slower inputs; label that semantic choice.

**Idleness timeout versus heartbeat.** Timeouts work without producer changes but encode assumptions. Heartbeats/closure signals provide stronger evidence at operational cost.

**Short versus long lookback.** Short overlap saves cost but misses longer-late changes. Long overlap improves bounded repair while increasing read/merge load. Measure tails and keep reconciliation.

**Processing-time versus event-time policy.** Processing time is operationally simple but ignores domain time. Event time supports correct windows while requiring lateness/state policy.

**Drop versus update late data.** Dropping bounds state and stabilizes output but loses facts. Updating/retracting preserves more truth but requires mutable sinks and consumer revision semantics.

**One primary watermark versus separate backfill state.** Reusing state is simpler but risks skips. Separate generations preserve live continuity and auditability.

**Automatic versus manual repair.** Automation reduces response time for bounded known cases. Manual approval is safer for source resets, privacy incidents and ambiguous discontinuities.

## Failure Modes and Misconceptions

- **“High-water mark means maximum seen.”** Safe progress requires a complete durable prefix.
- **“Positions are dense integers.”** Many sources use sparse or opaque tokens.
- **“A larger token is always later.”** Opaque tokens may not support comparison.
- **“Timestamp order is commit order.”** Values may be assigned before commit or by skewed clocks.
- **“Timestamps are unique.”** Precision and concurrent writes create ties.
- **“Database row order resolves ties.”** Unordered results are not stable pagination.
- **“Store only the timestamp.”** The tie-breaker and scope are part of state.
- **“Now is a safe high bound.”** Source time, commit visibility and future values differ.
- **“Recalculate now on every page.”** A moving high bound defeats reproducibility.
- **“Fetched means processed.”** Durable effects may lag fetch.
- **“Checkpoint first avoids duplicates.”** It creates a loss window.
- **“Overlap fixes everything.”** It covers only its bounded interval and needs idempotency.
- **“Equal payloads are duplicates.”** Separate real events can have equal values.
- **“Updated time covers every change.”** Deletes and bypass paths may not advance it.
- **“No rows means source is caught up.”** The query or source may have failed.
- **“Idle means complete.”** Quiet and unavailable are observationally similar without signals.
- **“Use the fastest partition's mark.”** Required lagging partitions become incomplete.
- **“Offsets from partitions can be averaged.”** They may not share units or order.
- **“One lag metric is enough.”** Position, time, checkpoint age and retention headroom differ.
- **“Watermark age equals data freshness.”** Producer inactivity and stale heartbeats confound it.
- **“Event time can resume extraction.”** Old-time events can appear at new source positions.
- **“Allowed lateness proves completeness.”** It is a policy/assumption unless guaranteed.
- **“Final window never changes.”** Business corrections may outlive state retention.
- **“Future timestamp is simply newest.”** It can leap and corrupt the frontier.
- **“Timezones affect only display.”** Local ordering can repeat or omit times.
- **“Failover positions are automatically comparable.”** Generation/lineage determines continuity.
- **“Backfill should reset the main checkpoint.”** It can disrupt live progress.
- **“Move forward to clear backlog.”** That discards required history.
- **“Monotonic state proves correct extraction.”** It can monotonically skip data.
- **“Matching counts prove boundary correctness.”** Missing/extra records can cancel.

## Worked Examples

### Example 1

A table has 1,000 rows with identical second-resolution `updated_at=10`. Page one returns 100 rows and state stores only 10.

The next `updated_at > 10` query loses 900. A composite `(updated_at,id)` cursor or inclusive overlap with idempotent versioning preserves the tie.

### Example 2

A worker durably writes positions 1, 2 and 4 while position 3 is quarantined. Metrics report maximum processed position 4.

The committed watermark remains 2. Position 4 may remain staged, but restart cannot omit 3; quarantine requires resolution or an explicitly incomplete publication.

### Example 3

Three partitions report comparable event-time frontiers 104, 101 and 103. A join requires all three.

The global safe frontier is 101. Publishing completeness through 104 would ignore unresolved records from two partitions.

### Example 4

A rarely used tenant partition emits nothing for hours. Its watermark stalls the global minimum.

The system uses authenticated source heartbeats plus assignment state to mark it idle. A timeout alone would be documented as a risk because delayed records may arrive when it resumes.

### Example 5

An offline mobile device uploads an event today with event time last week. Its extraction log position is current while its event time is old.

The source-position checkpoint captures it losslessly; the event-time policy routes it to late correction. Resuming extraction from event time would have missed it.

### Example 6

A producer clock emits year 2099 once. A naive `max(event_time)-10 minutes` watermark advances decades.

The pipeline quarantines implausible skew using trusted ingestion time, retains original evidence and prevents the outlier from driving event-time progress.

### Example 7

A batch writes all records through 500, crashes before checkpointing, and restarts at 450.

The repeated interval is accepted because event/version-aware effects are idempotent. Had state advanced to 500 before data commit, restart could have lost 451–500.

### Example 8

A 14-day lookback captures most late CRM edits, but an administrator corrects a 90-day-old record without changing a reliable version field.

The normal watermark cannot see it. Scheduled source/destination reconciliation detects the mismatch and triggers a partition repair; the incident updates the cursor contract.

### Example 9

A historical backfill from January overwrites the live checkpoint from September with January's final cursor.

The next live run rereads months and may corrupt a non-idempotent sink. Separate backfill state and publication namespaces avoid primary watermark regression.

### Example 10

After source failover, a new primary reports position 100 while the prior generation ended at 900. An operator assumes regression and edits state to 100.

The system instead detects a new generation, verifies whether a source-supported continuity mapping exists, and otherwise reboots from a coordinated snapshot/change cut with reconciliation.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md): transaction visibility, commit order, logs, MVCC and failover determine source positions.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): source contracts, ownership, schema history and finality define what a frontier means.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md): shard vectors, skew, retention, backpressure and state size shape watermark scalability.
- [Network Engineering](../../24-network-engineering/ROADMAP.md): delay, partition and clock behavior create observed lateness and missing heartbeats.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md): progress claims, conservative aggregation, fault states and evidence boundaries are system invariants.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): logical clocks, offsets, partial order, checkpoints and failure recovery explain progress semantics.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): opaque cursors, pagination snapshots, rate limits and token expiry affect API watermarks.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): state stores, connector generations, dashboards, alerts and controlled repairs make watermarks operable.

## References

1. Airbyte, [Incremental Sync](https://github.com/airbytehq/airbyte/blob/master/docs/platform/connector-development/config-based/understanding-the-yaml-file/incremental-syncs.md). Documents cursor-based incremental ranges, state emission, lookback windows and partition/global cursor choices.
2. Airbyte, [Airbyte Protocol: State and Checkpointing](https://github.com/airbytehq/airbyte/blob/master/docs/platform/understanding-airbyte/airbyte-protocol.md). Documents source-owned state messages, ordered checkpoint return and restart from accepted state.
3. MongoDB, [Change Streams](https://www.mongodb.com/docs/manual/changeStreams/). Documents event and high-watermark resume tokens, retained-history constraints and resume behavior.
4. Apache Beam, [Basics of the Beam Model](https://beam.apache.org/documentation/basics/). Defines event time, processing time, watermark estimates, triggers and late data.
5. Apache Beam, [Programming Guide](https://beam.apache.org/documentation/programming-guide/). Documents windowing, allowed lateness, early/late firings and watermark estimation.
6. Apache Flink, [Generating Watermarks](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/generating_watermarks/). Documents event-time timestamp assignment, minimum watermark combination, idleness and alignment.
7. Apache Spark, [Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html). Documents event-time watermark thresholds, state cleanup, late-data guarantees and multiple-watermark policies.

## Exercises

### Exercise 1

Design a watermark contract for incremental extraction from a table whose `updated_at` has millisecond precision and ties, whose immutable key is `(tenant_id,record_id)`, and whose hard deletes are recorded in an audit stream. Include ordering, boundaries, overlap, checkpoint evidence and reset behavior.

### Exercise 2

Durable integer positions are `{1,2,3,5,6,8}` and required known positions are 1 through 8. Compute the safe contiguous watermark and the naive maximum. Explain what must happen before the watermark can advance through 8.

### Exercise 3

Four required partitions have event-time watermarks 120, 118, 121 and 90; the fourth has produced no records for one hour. Choose a global frontier and design evidence for idleness or failure. Explain the consequence of using maximum instead.

### Exercise 4

An event-time job observes maximum trusted time 14:00 with allowed lateness 20 minutes. Compute its watermark, classify events at 13:39, 13:40 and 13:41 under a strict “earlier than watermark is late” rule, and state what this calculation does not prove.

### Exercise 5

Design failure-injection and reconciliation tests for a checkpoint protocol that lands immutable batch manifests, applies current-state merges and then writes watermark state. Cover ties, partial durability, replay, future timestamps, late old-row mutation, backfill and source-generation change.

## Answers to the Exercises

### Answer 1

Use lexicographic cursor `(updated_at,tenant_id,record_id)` with canonical UTC millisecond encoding and binary/stable key collation. At run start capture fixed high tuple $H$ from a consistent source view. Read records with full tuple greater than prior committed $W$ and at or below $H$, paginating by the same order. Use a lookback longer than measured/bounded late timestamp updates, accept overlap by source version, and ingest the delete audit stream with its own ordered position/vector so hard deletes are not inferred from silence.

Checkpoint only after record/delete batches, manifests and destination effects are durable. State includes source/table/generation, filters, schema, all live/delete positions, inclusivity, prior state, counts/digests and manifest identity. On source recreation, key/cursor semantic change or lost audit history, reject the old generation and rebootstrap from a new coordinated snapshot plus delete/change cut; never coerce old positions.

### Answer 2

The safe contiguous watermark is 3 because positions 1, 2 and 3 are durable and required position 4 is missing. The naive maximum is 8, which would incorrectly authorize restart after unresolved 4 and 7.

Before advancing through 8, positions 4 and 7 must gain durable required effects, or authoritative source evidence must establish that they are not required/are closed gaps under the position protocol. Any quarantined record must be resolved or publication explicitly remain incomplete. Then the durable prefix 1–8 is complete and watermark 8 is justified.

### Answer 3

Without additional evidence, the global frontier is the minimum, 90. Silence does not reveal whether partition four is idle, disconnected, unauthorized or delayed. Retrieve assignment/lease health, source head and an authenticated heartbeat or end-of-range signal. If the documented policy declares it idle after verified conditions, exclude/advance it according to that policy and record the risk when it resumes.

Using maximum 121 would treat partitions at 120, 118 and 90 as complete beyond their evidence. A join/window could finalize or evict state and later drop legitimate records from the slow partitions.

### Answer 4

The watermark is 13:40 because 14:00 minus 20 minutes is 13:40. Under the stated strict rule, 13:39 is late; 13:40 and 13:41 are not earlier than the watermark and are not classified late by this boundary rule.

The calculation does not prove that no event at or before 13:40 will arrive. It assumes the maximum is trusted and that 20 minutes represents acceptable lateness. Handling of late records—drop, revise, side-output or retain state—remains separate, as do business finality and source-position extraction completeness.

### Answer 5

Create several rows sharing a cursor and crash after each page to prove the full tuple resumes without loss. Crash during object upload and manifest commit; partial objects must remain unpublished. Crash after manifest/destination merge but before watermark; restart replays with one version-aware effect. Corrupt or partially write the checkpoint and prove atomic state replacement/recovery from audit history.

Inject a future timestamp and verify it is quarantined/clamped from driving progress while original evidence remains. Mutate a row older than lookback and confirm scheduled fixed-cut reconciliation detects it. Run a backfill and prove primary state never changes. Change source-generation identity or invalidate the token and require controlled rebootstrap rather than comparison. At each case compare fixed-cut source/extracted key sets and controls, manifest intervals, checkpoint-to-durability inequality, alerts and next-query boundaries.
