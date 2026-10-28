---
module_id: DE-021
program: Data Engineering
level: 1
module_number: 21
title: Full and Incremental Extraction
status: complete
last_verified: 2026-09-02
---

# Full and Incremental Extraction

## One-Page Review

### Governing question

When should a data pipeline reread an entire source dataset, and when can it safely extract only changes while preserving the same governed result under inserts, updates, deletes, concurrent writes, failures and schema evolution?

### Essential definitions

- A **full extraction** reads every in-scope record as of a declared source cut and emits a complete snapshot.
- An **incremental extraction** reads only records or change events after a durable prior position and through a new declared position.
- A **source cut** is the logical point in source history represented by an extraction, such as a transaction-log position or consistent snapshot identity.
- A **cursor** is an ordered value used to resume query-based extraction; it is safe only when its ordering and tie-breaker prevent gaps.
- A **checkpoint** records the last source position whose effects are durably represented downstream.
- **Change data capture (CDC)** observes committed inserts, updates and deletes, usually from a source log or change stream.
- A **tombstone** represents deletion of an identified record.
- A **snapshot-to-stream handoff** joins a baseline snapshot to subsequent changes at one precise source position without gap or double effect.
- A **reconciliation** independently compares source and extracted key sets, counts, digests or aggregates at compatible cuts.
- A **repair extraction** selectively or fully rebuilds state when incremental continuity or trust is lost.

### Central model, mechanism, or theorem

Let $S_c$ be a complete source snapshot at cut $c$, and let $\Delta_{(c,t]}$ be every committed change after $c$ through cut $t$, ordered sufficiently to preserve each key's source history. If `apply` implements insert, update and delete semantics and duplicate delivery has one durable effect, then

$$
I_t=apply^*(S_c,\Delta_{(c,t]})=S_t.
$$

The equality follows by induction over the ordered change sequence. It fails if the snapshot is inconsistent, the handoff has a gap, log history is missing, identities are unstable, deletes are invisible, changes are applied out of order for a key, or a checkpoint advances before downstream effects are durable.

For query extraction with cursor tuple $x=(u,k)$—update value $u$ and stable unique key $k$—read half-open/closed batches

$$
B_i=\{r\mid x_{i-1}<x(r)\leq x_i\}
$$

under a stable source cut. A timestamp alone is unsafe when multiple rows share it and batches split the tie.

### Critical invariants

- Scope, columns, filters, source cut, schema version and security context are recorded for every extraction.
- A full extraction is consistent at one cut or explicitly labeled as a fuzzy scan with bounded reconciliation.
- Incremental ordering is total through a stable tie-breaker, or the source provides an opaque ordered resume token.
- The snapshot and change stream meet at one retained position; any overlap is idempotent and no gap is permitted.
- The checkpoint never represents data whose downstream effect is not durable.
- Inserts, updates and deletes all have defined representations; missing rows are not automatically deletions.
- Replays produce the same materialized state through event identity, version comparison or idempotent merge.
- Schema/semantics at the change position are available to decode every record.
- Source load, rate limits, transaction/log retention, destination capacity and recovery objectives are governed.
- Periodic independent reconciliation can detect silent drift that checkpoints cannot.

### Common failures

Calling a table scan a snapshot without consistent isolation; using `updated_at > last_timestamp` when timestamps tie; paginating a mutating API with offsets; advancing a cursor after fetch but before durable load; assuming retries are exactly once; ignoring hard deletes; interpreting absence from a filtered page as deletion; beginning CDC after the baseline scan; allowing the log position to expire; replaying updates without source version; overwriting newer state with an older event; silently changing filters or schema at a checkpoint; running full extracts that harm the source; and trusting row counts without key- or component-level reconciliation.

### Compact example

At source cut 4, a consistent full snapshot contains keys `a`, `b`, and `c`. Changes 5–7 update `b`, delete `c`, and insert `d`. Applying all three after the exact snapshot cut yields the same final state as a full extraction at cut 7: `a`, updated `b`, and `d`. If change 6 is absent, `c` survives incorrectly. If change 5 is replayed, an idempotent consumer ignores its already-applied event identity or version.

### Connections

[DE-008](008-schemas-nullability-and-type-fidelity.md) governs extracted representation, [DE-009](009-time-time-zones-and-event-timestamps.md) separates business time from ingestion time, [DE-010](010-designing-a-reproducible-data-boundary.md) defines reproducible source boundaries, and [DE-020](020-validating-an-analytical-model-against-business-questions.md) supplies reconciliation discipline. Planned [DE-022](../ROADMAP.md) develops watermarks, DE-024 handles API ingestion, DE-025 handles database snapshots, DE-026 handles CDC, and DE-027 handles idempotent loads.

## Governing Question

How can an extractor minimize repeated work without changing the logical dataset it delivers or making recovery depend on luck?

Full and incremental extraction are not merely performance modes. They are different evidence and state-management strategies. A full extraction repeatedly asks the source for all in-scope state. It can repair drift and capture hard deletes by set comparison, but it consumes source, network and destination resources and still needs a consistent cut. An incremental extractor reduces work by trusting continuity from a durable position. That trust introduces cursors, checkpoints, retention, ordering, deletion and replay obligations.

The desired equivalence is simple to state: materializing a valid baseline plus every subsequent change should equal a fresh full snapshot at the same cut. Achieving it requires coordination among source transaction semantics, connector state, transport delivery, raw storage, destination merge behavior and reconciliation.

Current platforms expose this pattern directly. AWS Database Migration Service documents a `full-load-and-cdc` mode that migrates existing data while capturing ongoing changes. Debezium's PostgreSQL connector documents taking a snapshot, recording a log sequence number, and continuing the stream from that position. These are implementation examples of the general handoff invariant, not substitutes for validating the specific source and sink.

The governing choice is therefore not “full or incremental?” once. It is which mode, source cut, recovery path and verification strength apply to each dataset and lifecycle event.

## Why This Matters

Extraction is the first opportunity to lose or distort source history. Downstream transformations cannot reconstruct a delete never captured, distinguish an old update applied late without version metadata, or repair a page skipped because a timestamp tie was split incorrectly.

Full extraction appears stateless but is not automatically correct. A scan spanning concurrent transactions can combine old and new rows into a state that never existed. Replacing a destination from such a scan may publish an impossible snapshot. Long reads can also increase source I/O, retain database versions, consume API quotas and compete with production workloads.

Incremental extraction scales with change volume rather than total volume, lowers repeated transfer and can reduce latency. Its correctness depends on durable history and local state. A deleted checkpoint, expired log segment, changed cursor meaning or non-idempotent retry can create silent divergence.

Deletes are decisive. Querying rows whose `updated_at` advanced can observe inserts and updates, but a hard-deleted row is no longer available to query. Without tombstones, a change log or periodic source-to-target set reconciliation, the extracted state accumulates ghosts.

Recovery changes the economics. A full rebuild may be slow but operationally simple when datasets are small. For very large sources, retained raw changes and replayable checkpoints may be the only way to meet recovery time objectives. Hybrid designs use incremental extraction routinely and scheduled partition/full reconciliation to bound drift.

Finally, the source is a production system owned by someone else. Extraction must honor access, load budgets, maintenance windows, retention, rate limits and data-minimization policy. Correctness that destabilizes the producer is not an acceptable design.

## Prerequisites and Retrieval

Retrieve the producer owner and service-level agreement; source engine/API/file system and version; authoritative tables/resources; business keys and tenant scope; expected row grain; column types; null/default semantics; source schema history; table/view/filter definitions; transaction and isolation behavior; commit/log sequence model; CDC or audit capabilities; cursor candidates; update timestamp precision and mutation rules; delete behavior; soft-delete fields; tombstones; API ordering and pagination guarantees; rate limits; snapshot/export endpoints; transaction-log retention; source volume and change rate; peak write periods; source query plans/indexes; access credentials and network controls; encryption requirements; initial baseline state; checkpoint store; raw landing format; event identity/version; destination merge semantics; batch size; parallelism; retry policy; late/out-of-order behavior; schema-evolution policy; reconciliation controls; replay and repair procedures; retention; observability; recovery objectives; and consumer freshness/completeness requirements.

Distinguish source state from source history; extraction time from source commit time; full scan from consistent snapshot; row update time from change-stream position; event identity from entity identity; cursor from watermark; fetched batch from durably committed batch; at-least-once delivery from exactly-once effect; soft delete from hard delete; absence from deletion; record version from arrival order; retry from replay; initial snapshot from recurring full refresh; source log retention from raw-data retention; operational lag from data loss; schema compatibility from semantic compatibility; count reconciliation from key reconciliation; partition repair from global rebuild; and extraction completeness from downstream transformation correctness.

Before selecting a mode, build a decision table:

| Concern | Evidence to retrieve |
|---|---|
| Correct source cut | Snapshot/isolation/export guarantee and cut identity |
| Change completeness | Cursor/log ordering, retention and supported operations |
| Deletes | Tombstone, soft-delete, audit log or set-reconciliation path |
| Resume safety | Stable total order or opaque token; checkpoint durability |
| Destination effect | Idempotent insert/update/delete application and version rule |
| Source impact | Indexed predicate/export path, scan cost, locks/version retention |
| Recovery | Maximum replay horizon, raw retention, repair/full reload duration |
| Verification | Counts, key sets, controls, digests and compatible source cuts |

Use a disposable or read-replica environment to measure extraction behavior when production impact is uncertain. Never infer isolation, ordering or deletion semantics solely from connector setting names.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish complete state snapshots from change streams and query deltas;
2. choose full, incremental or hybrid extraction from data and recovery requirements;
3. define a consistent source cut and snapshot-to-stream handoff;
4. construct safe composite cursors and batch intervals;
5. preserve inserts, updates and deletes under retries and out-of-order delivery;
6. place checkpoints so acknowledged progress implies durable downstream effect;
7. reason about source impact, retention, throughput and recovery economics;
8. reconcile incremental materialization against independent source controls;
9. respond safely to schema changes, lost history and mode transitions; and
10. test extraction with concurrent writes, ties, crashes, replays and repairs.

## Core Exposition

### Define the extraction contract

Specify source objects, columns, predicates, tenant/security scope, source cut semantics, schema version, identity, ordering, delete representation, output envelope and checkpoint format. Treat changes to any of these as governed compatibility events.

Record what “complete” means. A table may exclude archived partitions, privacy-deleted subjects, provisional transactions or rows outside a tenant. A full scan of the wrong scope is still incomplete.

Include lineage metadata on every batch: extractor version, run, source identity, low/high positions, snapshot identity, fetch time, row/event count, schema fingerprint, status and retry lineage.

### Understand full extraction

A full extraction reads all in-scope current records and emits a replacement snapshot or complete batch. It has no dependency on a prior cursor, which makes it attractive for first load, small datasets, periodic verification and recovery from lost history.

It still depends on source consistency. PostgreSQL's [transaction documentation](https://www.postgresql.org/docs/current/sql-set-transaction.html) distinguishes `READ COMMITTED`, where statements can see different committed states, from `REPEATABLE READ`, where statements use one transaction snapshot. Equivalent concepts vary by source.

A one-statement export may inherit a statement snapshot. A multi-query parallel scan needs an explicitly shared cut or a source-native export/snapshot facility. Otherwise partitions can observe different histories.

### Choose replacement semantics deliberately

Full output can replace a complete destination, replace one partition, or be versioned as a new immutable snapshot. Never truncate the trusted destination before the new snapshot is verified and ready to publish.

Prefer stage–validate–publish: land into a run-scoped or immutable location, verify schema/counts/controls, then atomically switch a pointer or commit metadata. Keep the prior trusted version through rollback horizon.

If the source snapshot is fuzzy by design, label it and define tolerated skew plus reconciliation. Do not call it transactionally consistent.

### Understand query-based incremental extraction

Query-based extraction repeatedly asks for rows whose cursor is after a checkpoint and at or before a selected high bound. Candidate cursor fields include a monotonic sequence, source-controlled version, commit timestamp or `(modified_at, primary_key)` tuple.

The cursor must cover every relevant mutation. Application-maintained timestamps can be null, backdated, rounded, updated only on some code paths or changed independently of commit order. Verify triggers, bulk utilities and administrative paths.

Use a stable total order. When many rows share a timestamp, pair it with a unique immutable key and use lexicographic comparison. If the key itself can change, its old identity also requires representation.

### Bound each query batch

At run start, select a high bound $h$ under source guarantees. Extract `(low, h]` rather than an unbounded “greater than low” query whose result grows during pagination.

Within the window, order by the full cursor tuple and use keyset pagination. Offset pagination over a mutating relation can skip or duplicate rows when inserts/deletes shift positions.

Persist the exact last fully processed tuple only after durable sink effect. On retry, repeat an overlap or the entire uncommitted interval and rely on idempotency.

### Treat cursor ties as a correctness case

Suppose 1,000 rows share second-resolution `updated_at=10` and page size is 100. If the extractor stores timestamp 10 after page one and next queries `updated_at > 10`, it loses 900 rows.

A composite `(updated_at, id)` cursor resumes after the last key within the tie. Alternatively, reread a deliberate overlap such as `updated_at >= low` and deduplicate by stable identity/version.

DE-022 develops watermark selection and overlap in depth; here the invariant is that every relevant source mutation belongs to at least one retried batch and duplicate membership has one effect.

### Understand log-based change data capture

CDC reads committed source changes from a transaction log, replication stream or change API. It can expose inserts, updates and deletes with log positions and transaction metadata that polling queries lack.

Debezium's [PostgreSQL connector documentation](https://debezium.io/documentation/reference/stable/connectors/postgresql.html) describes using a logical replication slot and stored log sequence number, taking an initial snapshot when required, and streaming from the captured position so updates during the snapshot are not missed.

CDC is not magic exactly-once delivery. Connectors and sinks can fail between writing effects and checkpoints. Design for replay, retain event/source position, and define how per-key versions resolve duplicates or late delivery.

### Construct the snapshot-to-stream handoff

The baseline must be associated with a change position $c$. Capture changes at or before starting the scan according to the source protocol, read a consistent snapshot at $c$, then apply changes strictly after $c$—or allow a documented overlap handled idempotently.

Starting a change stream only after a long scan creates a gap. Starting it before the scan without a cut can apply an update and then overwrite it with an older snapshot row.

Source-native protocols solve this with a coordinated snapshot and position. Validate failure behavior during the handoff: a failed initial snapshot may restart, retained changes may grow, and partially published baselines must not become trusted.

### Preserve transaction and per-key order

Some consumers need only final per-key state; others need transactionally consistent multi-table history. Declare which guarantee is required.

Preserve source position, transaction identity and operation order even if transport partitions reorder arrival. Apply only a change newer than the stored source version for the key, unless the domain defines commutative operations.

Do not use extractor wall-clock arrival as source order. Network retries and parallel fetches can invert arrival.

### Represent inserts, updates and deletes

An insert establishes a key/version; an update replaces or patches governed fields; a delete removes current state or records a tombstone while retaining audit metadata as policy permits.

Decide whether update events carry before image, after image or field delta. Reconstructing current state from deltas requires a complete ordered history and compatible schema.

MongoDB's [change-stream documentation](https://www.mongodb.com/docs/manual/changeStreams/) illustrates resume tokens, insert/update/delete events, retained oplog dependence and the difference between change deltas and later full-document lookup. The exact event contract is source-specific.

### Do not infer hard deletes from silence

A row absent from an incremental query may be unchanged, filtered, inaccessible, moved or deleted. Query polling cannot generally identify hard deletion because the row no longer exists.

Use source tombstones, soft-delete/version columns, audit tables, CDC, periodic key-set comparison or partition replacement. Define how privacy erasure propagates through raw retention and downstream copies.

Full snapshots can detect deletion only when their scope and cut match the destination comparison and absence is authoritative.

### Place checkpoints after durable effects

Let checkpoint $p$ mean all changes through $p$ are durably represented in the governed raw/destination system. Never advance it merely because bytes were fetched or acknowledged by an intermediate queue.

If source-position commit and sink write cannot be atomic, choose replay over loss: durably write data with event identity/version, then checkpoint. A crash may repeat effects, which idempotent application resolves.

Store checkpoint generation, source identity, stream/filter configuration and schema context. Reject a checkpoint from another environment or changed extraction contract.

### Make retries and replay harmless

Assign each raw record a stable source event identity where available. Otherwise retain entity key plus source version/position and operation. Deduplicate deliveries without collapsing legitimate repeated business events.

For current-state targets, merge only when incoming version is newer, apply equal-version duplicates idempotently, and reject/investigate incompatible equal versions. For immutable logs, deduplicate by event identity while preserving arrival metadata.

Retry bounded batches, not ad hoc rows, and record attempt lineage. Poison records go to governed quarantine without letting a checkpoint skip them silently.

### Capture an immutable raw boundary

Land source-shaped records before destructive normalization when policy allows. Retain source position, operation, key, source timestamps, extraction timestamps, schema identity and payload digest.

Immutable raw history separates extraction from downstream interpretation and enables replay after transformation defects. It does not excuse uncontrolled sensitive-data retention; encryption, access, minimization and deletion obligations still apply.

Verify raw manifests and object atomicity. A checkpoint should refer to a complete durable batch/manifest, not a partially uploaded directory.

### Handle schema evolution at position

Changes must be decoded using the schema valid at their source position. Adding a nullable field may be compatible; changing type, key, precision, encoding or field meaning can break replay.

Persist schema identifiers/history with raw events. Quarantine unknown incompatible schemas without advancing beyond unrepresented data, or use an explicitly lossless fallback envelope.

Coordinate snapshot schema and stream schema during handoff. A table definition changing mid-snapshot can make chunks incompatible even if row data is transactionally consistent.

### Control source impact

Full scans consume reads, cache, I/O, CPU, network and possibly version-retention space. Query increments need indexes aligned with the cursor predicate and stable ordering. CDC increases log retention and replication resource use.

Set rate/concurrency limits, batch size, scheduling windows, statement timeouts and backoff with the producer. Observe replica lag, lock/version pressure, query latency and log backlog.

Use a replica only if its lag/consistency and failover semantics fit the source cut. A replica can reduce primary load while delivering stale or discontinuous history.

### Estimate mode economics

Let $N$ be total in-scope rows, $\delta$ changes per interval, $s$ average serialized bytes and $R$ available transfer rate. Approximate transfer time is $T_f\approx Ns/R$ for full and $T_i\approx\delta s/R$ plus checkpoint, merge and reconciliation overhead.

The ratio favors incremental extraction when $\delta\ll N$, but cost is not the only criterion. Add source scan burden, retained-log cost, operational complexity, replay horizon, repair frequency and required freshness.

A small dimension table may be safest as full replacement. A billion-row high-change ledger may require CDC plus immutable history and partition reconciliation.

### Apply backpressure

Destination slowdown must not cause unbounded memory or source-log growth. Bound in-flight batches and use durable queues/raw storage where appropriate.

Measure extraction lag both as source-position distance and wall-clock delay. A low event rate can make event-count lag misleading; a clock metric alone can be skewed.

When pausing, confirm source history will remain available through the maximum outage. Alert before retention headroom is exhausted, not after a resume token becomes invalid.

### Reconcile independently

At compatible source and destination cuts, compare schema, row/key counts, missing/extra keys, partition counts, null counts, control sums and digests. Prefer key/component comparisons over one grand total.

Hash reconciliation requires canonical serialization, field selection, ordering and collision-aware interpretation. A matching non-cryptographic aggregate is evidence, not proof.

Schedule reconciliation by risk and drift tolerance. Investigate every difference or classify it through explicit latency/filter/tombstone policy.

### Repair drift deliberately

If one partition diverges and scope can be isolated, extract and replace that partition at a known cut, then replay changes after its repair cut. If history is lost or scope cannot be trusted, take a new consistent full snapshot.

Do not reset a checkpoint forward to silence lag. That converts known backlog into permanent data loss.

Preserve the suspect extracted state and diagnostics until cause is understood. Repair should produce a new traceable publication, not erase forensic evidence.

### Choose full extraction when it fits

Prefer full extraction for first load, small/slowly changing sources, source exports with strong snapshot semantics, datasets lacking reliable change indicators, periodic drift repair, and destructive schema/key changes.

Full does not mean overwrite immediately. Stage and validate. Parallelize only under a shared source cut and producer-approved load budget.

Measure full duration against source snapshot/log retention and consumer freshness. A refresh taking longer than its interval can overlap itself and create capacity collapse.

### Choose incremental extraction when it fits

Prefer incremental extraction when total state is large, change volume is smaller, low latency matters, source history/cursor semantics are reliable, and operations can sustain checkpoint/replay/reconciliation discipline.

Use CDC where updates/deletes and commit order matter. Query polling can be adequate for append-only or reliably versioned sources.

Do not adopt incremental mode only to reduce runtime without funding its state, observability and repair paths.

### Combine both modes

Common hybrids include initial full snapshot plus continuous CDC; frequent increments plus nightly partition reconciliation; immutable append extraction plus periodic current-state rebuild; and source-native export plus changes captured during export.

The hybrid must define overlap/gap semantics and publication order. A full repair cannot overwrite changes newer than its cut.

Test every transition: empty start, bootstrap, steady state, restart, checkpoint loss, history expiration, schema change, repair, cutover and retirement.

### Operate extraction as a state machine

Use explicit states such as `initializing`, `snapshotting`, `catching_up`, `steady`, `paused`, `repairing`, `failed` and `retired`. State transitions record reason, source position, snapshot identity and operator.

Do not infer health from process liveness. A connector can run while its position stops advancing or while the source outruns it.

Alerts should identify owner and action for lag, expired/near-expired history, checkpoint age, repeated batches, quarantine, schema incompatibility, source errors, destination errors and reconciliation drift.

### Test the failure windows

Inject crashes after fetch, during raw write, after data commit but before checkpoint, after checkpoint attempt, during snapshot, at snapshot/stream handoff and during repair publication.

Create same-cursor ties, updates during pagination, key change, hard/soft delete, rollback transaction, multi-row transaction, duplicate event, reversed arrival, empty interval, very large row, schema change and log-retention loss.

For each case, assert final state, raw history, checkpoint, quarantine, alerts and recovery path—not just job exit status.

## Definitions and Notation

Let $K$ be the stable in-scope key space. Source state at cut $t$ is a partial mapping $S_t:K\rightharpoonup V_t$, where absence can mean nonexistent/deleted only under a complete authoritative scope.

A change event $d=(e,k,o,v,p)$ has stable event identity $e$, key $k$, ordered source position $p$, operation $o\in\{insert,update,delete\}$, and payload/version $v$ appropriate to the operation.

Let $\Delta_{(a,b]}$ be all committed in-scope events with $a<p\leq b$. Define materialization recursively:

$$
M_0=S_c,\qquad M_i=apply(M_{i-1},d_i).
$$

For correctly ordered complete events after consistent snapshot $S_c$, $M_n=S_t$ at the ending cut $t$.

An idempotent event application satisfies

$$
apply(apply(S,d),d)=apply(S,d).
$$

This property refers to duplicate delivery of the same identified source event, not two legitimate events with equal payloads.

For a query cursor $x(r)=(u(r),k(r))$ with total lexicographic order, batch $i$ is

$$
B_i=\{r\mid x_{i-1}<x(r)\leq x_i\}.
$$

Completeness over a stable cut requires the union of accepted batches to cover every in-scope cursor tuple once by effect, allowing delivery overlap when deduplication is correct.

Let $P_d$ be the last durably applied source position and $P_c$ the persisted checkpoint. Safety requires $P_c\leq P_d$. If $P_c>P_d$, acknowledged history can be lost; if $P_c<P_d$, replay is possible and must be idempotent.

Approximate transfer costs for $N$ total records, $\delta$ changed records, average bytes $s$ and effective bandwidth $R$ are

$$
T_{full}\approx\frac{Ns}{R},\qquad T_{inc}\approx\frac{\delta s}{R}+T_{state}+T_{merge}+T_{reconcile}.
$$

These omit source contention, compression, parallelism, skew and fixed latency; measure them empirically.

For source key set $K_s(t)$ and extracted key set $K_e(t)$ at compatible cut $t$, missing keys are $K_s\setminus K_e$ and ghosts are $K_e\setminus K_s$.

## Mechanisms, Invariants, or Proof Structure

**Mode-selection mechanism.** Determine scope/cut, change and delete observability, ordering, retention, source impact, target semantics, recovery objectives and reconciliation strength; then select full, incremental or hybrid extraction and document a repair mode.

**Snapshot-plus-changes theorem.** Base case: $M_0=S_c$. Inductive step: assume $M_i$ equals source state after the first $i$ committed changes. Correctly applying next event $d_{i+1}$ performs the same insert/update/delete transition as the source, so $M_{i+1}$ equals the next source state. By induction, applying the complete ordered sequence through $t$ yields $S_t$.

**Handoff invariant.** Every committed change belongs to the snapshot or to the subsequent stream, and any overlap has one durable effect. A gap violates completeness; an uncontrolled overlap can overwrite new state or duplicate effects.

**Composite-cursor theorem.** If $(u,k)$ is a total order and pages resume strictly after the last tuple through a fixed high bound, rows sharing $u$ are distinguished by $k$. A cursor using $u$ alone cannot distinguish unconsumed ties.

**Checkpoint safety invariant.** Persisting $P_c$ only after effects through $P_c$ are durable makes failure cause at worst replay. Persisting before effects permits unrecoverable skip after restart.

**Delete observability condition.** Current-row polling cannot distinguish a hard deletion from a row outside the queried result. Exact delete propagation therefore requires a tombstone/change history or authoritative full key-set comparison.

**Version monotonicity invariant.** For current-state materialization, a change older than the stored source version cannot overwrite newer state. Equal identified events have no additional effect.

**Reconciliation boundary.** Matching counts or digests at selected cuts is empirical evidence. It does not prove untested payload fields, historical events or future intervals are complete.

<!-- bijux-verify: {"id":"snapshot-change-equivalence","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"snapshot_rows=3\nchange_events=3\nfinal_rows=3\nfull_equals_incremental=True\nduplicate_replay_idempotent=True\ndelete_propagated=True\ngap_detected=True\ntimestamp_only_remaining=0\ncomposite_cursor_remaining=1\n","stderr":""}} -->
```python
events = (
    {"event": 1, "key": "a", "op": "insert", "value": 10},
    {"event": 2, "key": "b", "op": "insert", "value": 20},
    {"event": 3, "key": "c", "op": "insert", "value": 30},
    {"event": 4, "key": "a", "op": "update", "value": 11},
    {"event": 5, "key": "b", "op": "update", "value": 25},
    {"event": 6, "key": "c", "op": "delete", "value": None},
    {"event": 7, "key": "d", "op": "insert", "value": 40},
)

def apply_changes(state, changes, applied=None):
    result = dict(state)
    seen = set() if applied is None else set(applied)
    for change in changes:
        if change["event"] in seen:
            continue
        if change["op"] == "delete":
            result.pop(change["key"], None)
        else:
            result[change["key"]] = change["value"]
        seen.add(change["event"])
    return result, seen

snapshot, snapshot_events = apply_changes({}, events[:4])
incremental, applied = apply_changes(snapshot, events[4:], snapshot_events)
replayed, _ = apply_changes(incremental, events[4:5], applied)
full, _ = apply_changes({}, events)
with_gap, _ = apply_changes(snapshot, (events[4], events[6]), snapshot_events)

same_timestamp_page = ((10, "a"), (10, "b"))
last_timestamp = same_timestamp_page[0][0]
last_composite = same_timestamp_page[0]
timestamp_only = [row for row in same_timestamp_page if row[0] > last_timestamp]
composite = [row for row in same_timestamp_page if row > last_composite]

print(f"snapshot_rows={len(snapshot)}")
print(f"change_events={len(events[4:])}")
print(f"final_rows={len(incremental)}")
print(f"full_equals_incremental={full == incremental}")
print(f"duplicate_replay_idempotent={replayed == incremental}")
print(f"delete_propagated={'c' not in incremental}")
print(f"gap_detected={with_gap != full}")
print(f"timestamp_only_remaining={len(timestamp_only)}")
print(f"composite_cursor_remaining={len(composite)}")
```

The finite run demonstrates the modeled handoff, replay and tie behavior only; it does not prove a real connector's transaction, retention, schema or durability guarantees.

## Alternatives and Trade-Offs

**Recurring full refresh versus incremental state.** Full refresh reduces checkpoint complexity and repairs drift but scales with total state. Incremental scales with changes but requires continuity, deletes, ordering and recovery state.

**Query polling versus log-based CDC.** Polling is portable and simple when a reliable version column exists. CDC captures deletes and commit history more completely but needs source privileges, retained logs, schema history and connector operations.

**Source-native export versus application queries.** Native exports can provide efficient consistent cuts. Queries allow selective scope but can create long transactions and inconsistent parallel chunks without coordination.

**Timestamp cursor versus monotonic sequence/token.** Timestamps are broadly available but tie, skew and precision rules are hazardous. Source sequences/tokens better represent history but can be opaque, scoped and retention-bound.

**Composite keyset versus offset pagination.** Keyset pagination is stable and indexable under a fixed cut. Offset pagination is easy for static results but shifts under concurrent mutation and becomes costly at deep pages.

**After image versus delta event.** After images simplify current-state application but increase volume and may reflect lookup time rather than change time. Deltas preserve the exact mutation compactly but require complete ordered replay.

**Soft deletes versus tombstones.** Soft-delete rows are easy to poll but burden every source query and can be bypassed. Tombstones are explicit history but need retention and sink application.

**At-least-once with idempotency versus coordinated transaction.** Replay-tolerant design works across heterogeneous systems. Coordinated atomicity can reduce duplicates but is expensive, limited and still requires recovery verification.

**Immutable raw log versus direct current-state load.** Raw history enables replay and audit but increases cost and privacy obligations. Direct loading is simpler but couples extraction defects to materialized state.

**Fixed batch size versus adaptive batching.** Fixed size is predictable; adaptive size responds to row width, rate limits and lag. Either needs upper bounds and reproducible checkpoint intervals.

**Read replica versus primary.** A replica protects primary capacity but introduces lag, failover and history-continuity questions. The primary may offer the authoritative position but stricter load constraints.

**Partition repair versus global rebuild.** Partition repair reduces cost when scope is isolated; a full rebuild restores trust when boundaries or history cannot be proven.

## Failure Modes and Misconceptions

- **“Full means consistent.”** A long scan can mix source states.
- **“One query always means one cut.”** Source isolation and export semantics decide.
- **“Incremental means rows newer than yesterday.”** It requires a durable ordered position and mutation coverage.
- **“Updated time is monotonic.”** Application clocks, precision and write paths may violate that assumption.
- **“Greater-than timestamp is safe.”** Tied unconsumed rows can be skipped.
- **“Offset pagination is deterministic.”** Concurrent inserts/deletes shift pages.
- **“Fetch success means checkpoint success.”** Downstream effect may not be durable.
- **“Retrying creates exactly-once delivery.”** It commonly creates duplicate delivery.
- **“Deduplicate by business fields.”** Legitimate equal-valued events can collapse.
- **“Arrival order is source order.”** Parallelism and retries reorder arrival.
- **“Later timestamp always means newer version.”** Timestamp semantics may differ from commit order.
- **“Polling finds deletes.”** Hard-deleted rows are absent from the poll.
- **“Absence is deletion.”** Filters, access and partial delivery also cause absence.
- **“CDC needs no baseline.”** A stream alone lacks prior state unless all needed history remains.
- **“Start CDC after the scan.”** Writes during the scan form a gap.
- **“Start CDC first and apply immediately.”** An older snapshot can overwrite newer changes.
- **“A checkpoint is portable.”** It is bound to source identity, stream/filter contract and schema context.
- **“Stored offset means retained history.”** Source logs can expire beyond the offset.
- **“Connector running means healthy.”** Position may be stalled or losing retention headroom.
- **“Replica extraction is equivalent.”** Lag and failover can change cuts and continuity.
- **“Schemas only matter at batch start.”** CDC history spans schema versions.
- **“Unknown fields can be dropped safely.”** They may contain required meaning or identity.
- **“Row counts prove completeness.”** Missing and extra keys can cancel.
- **“Hashes prove equality absolutely.”** Canonicalization, coverage and collision limits matter.
- **“A full reload can overwrite in place.”** Failure can destroy the last trusted dataset.
- **“Resetting forward repairs lag.”** It discards unprocessed history.
- **“More parallel readers are always faster.”** They can overload sources and break snapshot consistency.
- **“Small change volume means cheap CDC.”** log retention, schema history and operations carry fixed cost.
- **“Raw means keep everything forever.”** Retention and privacy still govern.
- **“The same mode fits every lifecycle state.”** bootstrap, steady state and repair have different needs.

## Worked Examples

### Example 1

A 20,000-row country dimension changes weekly. A source-native consistent export finishes in seconds, while a CDC connector would add privileges, retained-log and on-call complexity.

The team uses immutable full replacement with stage–validate–publish and daily key/count reconciliation. Simplicity is a correctness advantage at this scale.

### Example 2

A billion-row order table changes by 500,000 rows per hour. Repeated full scans exceed the producer's I/O budget and cannot meet freshness.

The design uses one coordinated baseline plus log-based CDC, durable raw events, per-key source versions and weekly partition reconciliation. Full extraction remains a controlled repair path.

### Example 3

An API returns records ordered by second-resolution modification time. Page one ends at `(10,a)`, while `(10,b)` remains.

Resuming with `modified_at > 10` loses `b`; resuming lexicographically after `(10,a)` retrieves it. The extractor records the composite cursor only after the page manifest and records are durable.

### Example 4

A nightly customer poll sees inserts and updates, but customers hard-deleted for privacy remain in analytics forever.

The team adds a deletion feed with stable subject identity and verifies erasure across raw/curated retention. Until then, periodic authoritative key reconciliation detects ghosts but cannot satisfy a tight deletion SLA alone.

### Example 5

A database snapshot begins at 01:00 and CDC begins at 03:00 after the scan. An order updated at 02:00 is missing from both the 01:00 chunk that read its old value and the later stream.

The corrected protocol captures a log position and consistent snapshot together, retains changes during scanning and applies changes strictly after the cut.

### Example 6

A sink commits event 500, then crashes before checkpointing 500. On restart it resumes from 499 and receives 500 again.

Because the raw record uses source event identity 500 and the current-state merge treats equal version as no-op, final state is unchanged. The design prefers replay to advancing the checkpoint early.

### Example 7

Parallel CDC partitions deliver customer version 12 before version 11. A blind upsert later applies 11 and regresses the row.

The sink compares the source version atomically and applies only newer versions. Both arrivals remain in raw history with transport metadata for diagnosis.

### Example 8

A connector is paused for maintenance while the source retains logs for 24 hours. The pause lasts 30 hours; its recorded position no longer exists.

Operators do not jump the offset forward. They declare incremental continuity lost, take a new consistent baseline, reestablish a handoff position and reconcile before publication.

### Example 9

A full refresh writes directly into the serving table after truncating it. Halfway through, source throttling aborts the scan and consumers see a partial dataset.

The pipeline instead writes a run-scoped snapshot, validates controls and atomically publishes it. The previous snapshot remains available for rollback.

### Example 10

A new non-null source column appears during an initial snapshot while changes are buffered. Some chunks use the old schema and events use the new schema.

The connector records schema history by source position and either coordinates schema locking/versioning or restarts the snapshot. It never fills unknown values silently and calls the mixed baseline complete.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md): MVCC snapshots, transaction logs, isolation, indexes and replication positions determine extraction guarantees.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): authoritative sources, ownership, contracts, retention and lineage bound extraction scope.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md): partitioning, throughput, backpressure, log retention and distributed ordering shape scalable capture.
- [Operating Systems](../../22-operating-systems/ROADMAP.md): files, buffering, atomic publication and durable checkpoints affect observed failure behavior.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): least privilege, network protection, raw-data access and deletion obligations govern extraction.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): delivery semantics, idempotency, partial failure and logical positions explain checkpoint design.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): pagination, rate limits, retries, versioning and authorization matter for API extraction.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): connector lifecycle, credential delivery, observability, repair workflows and self-service controls operationalize extraction.

## References

1. PostgreSQL Global Development Group, [SET TRANSACTION](https://www.postgresql.org/docs/current/sql-set-transaction.html). Documents visibility under transaction isolation levels and importing transaction snapshots.
2. PostgreSQL Global Development Group, [COPY](https://www.postgresql.org/docs/current/sql-copy.html). Documents bulk transfer between PostgreSQL tables/queries and files or client streams.
3. Debezium, [PostgreSQL Connector](https://debezium.io/documentation/reference/stable/connectors/postgresql.html). Documents initial snapshots, log sequence positions, replication slots, snapshot modes and restart behavior.
4. Amazon Web Services, [Creating an AWS DMS Task](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.Creating.html). Documents full load, full-load-plus-CDC and CDC-only migration modes.
5. Amazon Web Services, [Creating Tasks for Ongoing Replication](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html). Documents database-log change capture, source-specific positions and full-load-plus-CDC handoff considerations.
6. MongoDB, [Change Streams](https://www.mongodb.com/docs/manual/changeStreams/). Documents change events, resume tokens, resume constraints, oplog retention and update-image behavior.

## Exercises

### Exercise 1

Choose and justify an extraction strategy for three sources: a 10,000-row reference table with no update timestamp, a 5-billion-row transactional table with database-log CDC, and an API exposing append-only events with stable cursor pagination. Include steady-state and repair modes.

### Exercise 2

A source has rows `(updated_at,id)` equal to `(10,a)`, `(10,b)`, `(10,c)`, `(11,a)`. Page size is two. Show how timestamp-only resumption can lose data and enumerate safe composite-cursor batches through high bound `(11,a)`.

### Exercise 3

Design crash tests for a pipeline that extracts source changes, writes an immutable raw batch, merges current state and persists a checkpoint. Cover crashes after fetch, during raw write, after raw commit, after merge and before/after checkpoint.

### Exercise 4

A CDC connector at position 900 is offline until the source retains history only from 950. Explain why resuming or moving the checkpoint to 950 is unsafe. Design a rebootstrap with a new snapshot cut, buffered changes, validation and publication.

### Exercise 5

Design a reconciliation plan for customer current state where hard deletes are possible, the source is continuously changing and a full source scan takes two hours. Include compatible cuts, keys, payloads, privacy, drift repair and evidence limitations.

## Answers to the Exercises

### Answer 1

Use staged full replacement for the 10,000-row reference table because it is small and lacks a trustworthy mutation indicator. Read it at a consistent source cut, validate schema/key set and atomically publish; use the same process for repair.

Use coordinated initial snapshot plus log-based CDC for the 5-billion-row table. Retain log position, transaction/event identity, schema history and immutable raw changes; apply idempotently by source version and reconcile partitions. If history expires or global drift is unbounded, take a new consistent baseline rather than skipping ahead.

Use incremental cursor extraction for the append-only API, fixing a high bound if supported and following the opaque stable cursor until exhausted. Persist page/batch manifests before the cursor, retry with idempotent event identities, respect rate limits and periodically compare event ranges/counts. Repair a bounded cursor range if the API supports it; otherwise re-extract from an earlier retained position into a new raw generation.

### Answer 2

If page one returns `(10,a)` and `(10,b)` and the extractor stores timestamp 10, a next predicate `updated_at > 10` returns only `(11,a)` and loses `(10,c)`. If it stores time only after finishing all ties, it needs an independent way to know the tie is complete.

With tuple order and page size two, choose fixed high bound `(11,a)`. Batch one is tuples greater than the prior low through `(10,b)`: `(10,a)`, `(10,b)`. Persist last tuple `(10,b)` only after durable effect. Batch two uses `(updated_at,id) > (10,b)` and `<= (11,a)`, returning `(10,c)`, `(11,a)`. The intervals are disjoint by tuple while retries can repeat an uncheckpointed batch safely.

### Answer 3

After-fetch crash must leave the checkpoint unchanged and permit refetch. A partial raw write must remain unpublished; its manifest is absent or invalid and cleanup/retry cannot be mistaken for a complete batch. After raw commit, restart may find the durable batch and rerun merge without duplicating effects. After merge but before checkpoint, the same changes are replayed; version/event-aware merge must be idempotent. After checkpoint, restart begins strictly according to the checkpoint contract and verifies referenced raw/merge evidence exists.

For every injection, assert the final raw manifest, event identities, current state, checkpoint relationship $P_c\leq P_d$, quarantine and alerts. Also crash during checkpoint persistence to prove atomic record replacement and reject corrupt/partial checkpoint state.

### Answer 4

Position 900 cannot resume because required events 901–949 may no longer be available. Setting the checkpoint to 950 asserts those unknown effects are durable when they are not, creating silent data loss.

Create a new extraction generation. Establish a source-native consistent snapshot and corresponding position $c\geq950$ while retaining changes after $c$. Land the baseline into an isolated location, capture its schema/cut identity, validate keys/counts/controls, then apply buffered changes strictly after $c$ idempotently. Catch up to a recorded publication cut, reconcile with an authoritative source view at that cut, atomically switch publication, preserve the prior generation for investigation/rollback, and retire its invalid checkpoint explicitly.

### Answer 5

Obtain a consistent snapshot or exported key/payload digest at source cut $c$; a two-hour fuzzy scan is not directly comparable to a destination moving through later changes. Either hold/import one source snapshot across chunks or capture CDC position $c$, scan the associated snapshot, and compare the extracted materialization at the same cut before applying later changes.

Compare complete tenant-scoped key sets to find missing and ghost customers, then canonical payload digests or selected field components on shared keys. Protect identifiers/digests and minimize retained personal data. Classify expected filters and privacy deletions explicitly. Repair affected partitions from known cuts and replay changes after each repair cut; use a new global baseline when partition scope is uncertain. Record source/destination versions, cuts, schema, canonicalization, exclusions and results. Matching finite keys/digests is strong empirical evidence for covered fields at $c$, not proof of historical-event completeness or future extraction correctness.
