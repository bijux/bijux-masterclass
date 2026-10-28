---
module_id: SARCH-076
program: Software Engineering: Software Architecture
level: 2
module_number: 76
title: Data Migration Architecture
status: complete
last_verified: 2026-09-06
---

# Data Migration Architecture

## One-Page Review

### Governing question

How can an organization move authoritative data between representations or systems while concurrent change continues, preserve declared meaning and history, prove the destination is ready, transfer authority once, and retire the old data path without silent loss or duplication?

### Essential definitions

- a **migration unit** is the smallest independently identified item whose state and outcome are tracked;
- a **source of authority** is the system allowed to decide a fact during a named migration state;
- a **snapshot** is a consistent view of source data at a declared logical position;
- a **high-water mark** is the greatest source position durably incorporated into the destination;
- **change data capture** (CDC) derives an ordered stream of inserts, updates, and deletes from an authoritative change record;
- a **backfill** copies or derives pre-existing data, normally in bounded restartable chunks;
- an **idempotency identity** lets repeated application of the same logical change have one intended effect;
- **reconciliation** compares source, destination, and movement evidence against semantic invariants;
- a **fence** rejects writes from an authority epoch that has ended;
- a **tombstone** represents deletion explicitly when absence alone would be ambiguous;
- **cutover** transfers named read or write authority under predeclared gates;
- **rollback** restores an earlier compatible authority state, while **roll forward** repairs or advances the new state when reversal is unsafe.

### Central model, mechanism, or theorem

Let $S_{w_0}$ be a consistent source snapshot at log position $w_0$, and let $\Delta_{(w_0,w_c]}$ be every committed source change after that snapshot through cut position $w_c$, in a declared order. With transformation $f$ and deterministic, idempotent application $\operatorname{apply}$, the intended destination is

$$
T_{w_c}=\operatorname{fold}(\operatorname{apply}, f(S_{w_0}), f(\Delta_{(w_0,w_c]})).
$$

This equality is an obligation, not an automatic property of a migration tool. It depends on snapshot consistency, complete capture, ordering scope, transformation semantics, duplicate handling, deletion propagation, and an authority fence at cutover.

### Critical invariants

- every migration unit has stable identity, lineage, and one terminal state;
- one system owns each mutable fact in every migration state;
- the snapshot and change stream meet at a known boundary without a gap;
- replay is safe at the promised idempotency scope;
- ordering is preserved wherever later state depends on earlier state;
- deletes, nulls, defaults, units, time zones, precision, and history retain declared meaning;
- validation covers semantic invariants and unmatched work, not only row counts;
- cutover fences stale writers and accounts for in-flight work;
- copied sensitive data has authorized purpose, access, retention, and deletion;
- rollback claims match actual destination state and external effects;
- source retirement includes replicas, exports, jobs, credentials, backups, recovery, and legal retention.

### Common failures

Common failures include copying a moving database without a change boundary; treating row count as correctness; replaying non-idempotent changes; ordering globally when only per-key order exists; ignoring deletes; inventing destination defaults; truncating precision; confusing event time with commit order; allowing backfill to overwrite newer CDC state; dual-writing without repair authority; comparing only successful rows; routing reads before indexes or derived state are ready; leaving two writers after cutover; promising rollback after irreversible new writes; leaking production data into migration stores; and decommissioning the primary database while hidden consumers remain.

### Compact example

A customer table is snapshotted at log position 410. While its rows are copied, changes 411–468 accumulate. Backfill writes carry source version 410; CDC writes carry each later position, and the destination accepts a write only if its source version is newer than the stored one. A repeated change at 447 is ignored, a delete at 455 becomes a tombstone, and reconciliation reports all source identities, destination-only identities, versions, and business invariants. At cutover, epoch 8 rejects old writers before the destination becomes authoritative. The migration is safe because boundary, version, deletion, evidence, and authority are explicit—not because a copy command finished.

### Connections

[SARCH-075](075-strangler-and-parallel-run-architectures.md) supplies interception, comparative operation, and authority routing. [SARCH-073](073-versioned-contracts-and-compatibility.md) supplies expand-migrate-contract compatibility. [SARCH-077](../ROADMAP.md) next applies modernization judgment to distributed monoliths.

## Governing Question

Data migration is a controlled change of representation and authority, not merely movement of bytes. The destination may use different keys, constraints, partitions, encodings, ownership boundaries, retention rules, or derived models. Concurrent source writes mean that even a perfect bulk copy can be obsolete when it ends. The architecture must therefore answer three questions together: what each value means, which changes constitute the intended state, and who may write at every instant.

The difficulty rises with scale, availability requirements, weak identifiers, historical defects, sensitive data, external consumers, and irreversible new behavior. A credible plan names its consistency boundary, capture semantics, reconciliation evidence, cutover protocol, and retirement obligations. It never converts “the tool reported success” into “the data is correct.”

## Why This Matters

Incorrect migrations can remain invisible for months. A dropped deletion may resurrect an account; a rounded amount may alter a ledger; an implicit time zone can reorder treatment events; a newly generated identifier can sever an audit trail; a missing historical state can make an otherwise correct current row legally or operationally unusable. Availability can also fail when backfill saturates logs, locks, caches, storage, or downstream consumers.

Migration is a temporary distributed system. Source, log, copier, transformer, queue, destination, validator, router, and operators fail independently. Messages repeat, arrive late, and may be observable in a different order than business time. The design must tolerate retry while making uncertainty visible.

Current implementation mechanisms demonstrate these concerns without defining a universal solution. PostgreSQL 18 logical replication, checked 2026-09-06, documents an initial snapshot followed by changes that occurred during the copy and notes that destination-side writes can create conflicts [8]. Apache Kafka's current design documentation similarly limits its transactional exactly-once account to coordinated Kafka inputs and outputs; external destination effects require cooperation from that destination [9]. Architecture claims must be no broader than the mechanism boundary.

## Prerequisites and Retrieval

Retrieve transaction, commit, isolation, consistent snapshot, log sequence number, source of truth, system of record, primary key, foreign key, uniqueness, referential integrity, schema, serialization, precision, time zone, null, default, checksum, hash, partition, shard, CDC, outbox, idempotency, deduplication, ordering, replay, tombstone, backfill, watermark, lineage, reconciliation, dual read, dual write, fencing token, canary, cutover, rollback, roll forward, retention, backup, recovery point objective, and recovery time objective.

SARCH-073 explains compatibility across versions, SARCH-074 supplies decomposition seams, and SARCH-075 supplies traffic and parallel-run architecture. This chapter owns movement, transformation, validation, and data authority. Database engine internals belong primarily to DBE; pipeline operations belong to DE; enterprise meaning, lineage, and governance belong to DARCH.

## Learning Objectives

After completing this module, you should be able to:

1. define a migration outcome in terms of meaning, authority, and retirement;
2. inventory datasets, consumers, constraints, history, and sensitive-data obligations;
3. choose offline copy, snapshot plus CDC, event replay, or another movement mode;
4. establish a gap-free boundary between backfill and concurrent changes;
5. design idempotent, ordered, restartable application;
6. prevent stale backfill from overwriting newer destination state;
7. translate schemas without silently changing null, unit, time, precision, or identity semantics;
8. reconcile counts, identities, versions, aggregates, invariants, samples, and unmatched work;
9. transfer authority with fencing and realistic rollback or roll-forward rules;
10. retire old data paths while preserving required records and recovery evidence.

## Core Exposition

**Define the outcome and nonnegotiable invariants.** State why data moves: system replacement, decomposition, jurisdiction, engine change, ownership transfer, model correction, or archival policy. Name the datasets, history horizon, consumers, service expectations, legal and security constraints, and final authority. “Move database A to B” is too weak because it says nothing about semantics or acceptable loss.

Write domain invariants before mapping fields. Examples include ledger balance, unique active entitlement, monotonically increasing case revision, order-line total, valid state transition, retained consent provenance, and absence after an authorized deletion. Distinguish hard gates from statistical indicators. A single violated financial or safety invariant may outweigh millions of matching rows.

**Inventory the real data surface.** Catalog tables, objects, streams, files, search indexes, caches, materialized views, replicas, analytical extracts, backups, reports, manual spreadsheets, partner transfers, and support tools. Classify each as authoritative, replicated, derived, cached, archival, or ephemeral. Identify direct readers and writers, including credentials and scheduled jobs.

Record volume, growth, update and delete rates, key quality, largest object, skew, hot partitions, transaction boundaries, retention, locality, encryption, and recovery requirements. Unknown consumers are a retirement risk. Query logs, network evidence, access records, configuration, job schedulers, code search, and interviews each reveal different parts of the surface.

**Specify the semantic data contract.** For every field or relation, define identity, type, unit, precision, scale, collation, encoding, time basis, null meaning, default meaning, cardinality, allowed state, provenance, and retention. A source empty string, absent field, and SQL null may carry different meanings. Converting all three to one destination null loses information.

Separate representation from meaning. Dollars stored as decimal and cents stored as integer can be equivalent under an exact declared conversion. A local timestamp without a known zone may be impossible to transform uniquely. Do not manufacture certainty: quarantine ambiguous units and assign an accountable resolution process.

**Choose a migration mode.** An offline migration stops writes, takes a consistent copy, validates, and starts the destination. It offers a simpler proof but may exceed the permitted outage. Snapshot plus CDC copies a consistent baseline and then applies captured changes through a cut position. Event replay derives state from a complete authoritative history. Incremental domain migration transfers bounded cohorts or aggregates.

The choice follows recovery and availability constraints, not fashion. If an outage comfortably fits and rollback is simple, an offline move may be safer. Online movement introduces a log boundary, replication lag, duplicate handling, conflict policy, capacity isolation, and a more complex cutover.

**Create a gap-free snapshot boundary.** A bulk query over changing rows is not necessarily one database state. Establish snapshot $S_{w_0}$ and a change position $w_0$ such that every committed change belongs either in the snapshot or after it. Database-native consistent snapshots and logs can supply such a boundary; application timestamps usually cannot because clocks, transaction duration, and commit order differ.

Retain the log until the backfill and catch-up complete. Monitor retention headroom. If a capture slot, log segment, or queue expires before application, the migration has a gap and must restore evidence or restart from a trustworthy boundary. Never infer completeness from the destination's latest wall-clock timestamp.

**Design a restartable backfill.** Divide work by stable key range, partition, tenant, or another bounded unit. Each chunk records selection boundary, source snapshot, transform version, attempt, counts, checksum or invariant evidence, destination outcome, and terminal state. Retries must not double effects. Rate limits protect source logs, buffer pools, networks, destination indexes, replicas, and foreground work.

Chunk size trades overhead against recovery granularity and transaction impact. Keyset iteration is usually more stable than offset pagination over a changing or large relation. Skew requires adaptive sizing. A huge tenant or object may need its own plan rather than blocking every ordinary chunk.

**Join backfill and CDC safely.** Backfill and live changes race. If backfill blindly overwrites a row already updated by CDC, the destination regresses. Common designs buffer CDC until the relevant snapshot copy completes, apply backfill first and then ordered deltas, or attach a source version and accept only newer state.

The comparison rule must be atomic at the destination. A read-then-write version check can race with another worker. Deletes need versions too: otherwise late backfill can recreate a deleted record. Preserve enough lineage to explain why each destination value won.

**Define capture semantics.** Prefer an authoritative transaction log, outbox, or domain event record over polling `updated_at`. Polling can miss equal timestamps, late commits, hard deletes, and changes that bypass the timestamp. Triggers improve capture but add write-path behavior and require deployment, recursion, failure, and removal analysis.

Name the ordering guarantee: total, per transaction, per partition, or per key. Do not build a consumer that requires global order from a partitioned source that promises only per-partition order. Preserve transaction boundaries when invariants span records or explicitly design intermediate states that readers cannot observe as valid.

**Make application idempotent at a declared scope.** A migration worker can crash after destination commit but before checkpoint commit, so replay is normal. Stable source event identity, destination uniqueness, conditional upsert, and atomic storage of result plus checkpoint can make retry safe. “Upsert” alone is insufficient when operations are increments, appends, notifications, or state-machine transitions.

Define deduplication retention. An idempotency table expiring before the maximum replay horizon permits old duplicates. Record whether identity is per event, row version, aggregate version, transaction, or chunk. For external side effects, coordinate with the external system or isolate those effects until authority transfers.

**Use expand-migrate-contract for schema evolution.** First expand readers and writers so old and new representations coexist compatibly; then migrate data and usage; finally contract obsolete fields and code. Parallel Change describes this expand, migrate, contract sequence [6]. Compatibility must include constraints and semantics, not only field presence.

Defaults deserve scrutiny. Adding a destination default can transform “unknown” into a real value. Enforcing a new constraint before historical defects are classified may halt the migration; omitting it permanently weakens integrity. Quarantine, remediate, or explicitly grandfather exceptions with provenance.

**Preserve identity and relationships.** Reusing stable identifiers simplifies lineage and references but may expose a legacy namespace or collide after consolidation. Translating identifiers requires a durable bijection where reversibility or audit demands it. Never generate a new identifier on retry without a stable mapping.

Move related data in an order consistent with referential constraints, defer constraint enforcement within a controlled transaction, or stage then validate. Cross-shard relationships and polymorphic references may be implicit. Orphans should be classified, not silently dropped or attached to a fabricated parent.

**Treat time and numeric representation as data.** Identify event time, effective time, observation time, ingestion time, transaction time, and commit order. Daylight-saving folds and gaps make some local wall times ambiguous or nonexistent. Preserve original zone or offset and the governing interpretation when needed.

Define decimal precision and rounding at the business boundary. Binary floating-point is not an automatic substitute for fixed decimal amounts. Test minima, maxima, negative values, zero, scale changes, overflow, special values, and serialization round trips. Aggregate agreement can hide offsetting row-level errors.

**Propagate deletion and retention policy.** Hard deletion disappears from a later snapshot unless the snapshot boundary captures absence correctly. CDC commonly needs explicit delete records or tombstones. Soft deletion needs a defined state and downstream filtering rule. Cascades can have different scope in the destination.

Migration copies do not escape privacy, records, litigation-hold, or deletion obligations. Minimize fields, encrypt movement and staging, restrict identities, audit access, define retention, and delete temporary stores. A backup retained for recovery may require different access and expiry than a reconciliation extract.

**Avoid uncontrolled dual writes.** Writing source and destination in one request creates a distributed atomicity problem. The first write can commit and the second fail; a retry may duplicate one side; latency and availability become coupled. An outbox or authoritative log often provides safer propagation from one write authority.

If dual writes are unavoidable, state ordering, idempotency, durable intent, conflict resolution, repair owner, observation, and exit conditions. Do not claim atomicity beyond the actual transaction coordinator. Kafka documentation explicitly notes that external destination exactly-once behavior requires destination cooperation [9].

**Reconcile at several layers.** Structural checks validate schema, constraints, partitions, indexes, and permissions. Completeness checks compare identity sets, counts by cohort, min/max positions, and missing terminal states. Content checks compare hashes or normalized values. Semantic checks recompute domain invariants, aggregates, transitions, and selected histories.

Counts are necessary but weak: one missing row plus one duplicate preserves count. Whole-table hashes can detect a difference but localize poorly and may be unstable under ordering or representation. Use hierarchical partition checksums, keyed differences, cohort aggregates, invariant queries, and risk-based record review. Report source-only, destination-only, unequal, ambiguous, and uncheckable records.

**Classify and repair discrepancies.** Differences may be source defects, destination defects, mapping defects, expected policy changes, concurrent movement, missing capture, duplicate application, or comparison error. Do not make the source a correctness oracle. Use domain rules, independent calculations, provenance, and accountable decisions.

Repairs are migration writes and need identity, review, audit, retry safety, and revalidation. Preserve the original discrepancy and resolution. Avoid ad hoc console changes that cannot be reproduced after rehearsal or disaster recovery.

**Gate read and write cutover separately.** Destination reads may begin before writes when freshness and query semantics are sufficient. Shadow or cohort reads can expose performance and compatibility defects. Write authority is higher consequence and requires capture catch-up, reconciliation, fencing, and a named cut position.

At cutover, stop or fence source writers, drain or account for in-flight transactions, record $w_c$, apply through $w_c$, validate gates, advance authority epoch, and route writes. Then observe lagging clients and rejected stale attempts. A DNS, proxy, or flag change alone does not revoke database credentials or queued work.

**Make rollback claims state-aware.** Before destination-only writes, reversal may mean routing back after proving source caught up. After new state, schema, identifiers, or external effects exist, the old system may not interpret them. Bidirectional replication can extend reversibility but creates conflict and doubles the proof surface.

Define the last reversible state. Beyond it, stop admission, preserve evidence, repair, and roll forward. Backups provide recovery points, not instant semantic rollback; restore duration, lost interval, external effects, and replay must be tested.

**Rehearse with production-shaped evidence.** Rehearse mapping, throughput, catch-up, constraint creation, index build, cutover, abort, recovery, and cleanup using authorized representative data. Synthetic data can cover boundaries without exposing production records but may miss skew and historical defects. Masked production data can still be re-identifiable and remains governed.

Record tool versions, configurations, transform digest, input boundary, duration, throughput, error classes, operator decisions, and evidence. Change one controlled variable between rehearsals when interpreting results. A successful rehearsal is evidence for that workload and environment, not a guarantee.

**Operate the migration as a production system.** Monitor source impact, log retention, capture lag, queue depth, retry rate, dead letters, chunk progress, destination write latency, storage growth, constraint failures, discrepancy classes, and consumer errors. Alert on stalled progress and missing evidence, not only process crashes.

Set resource ceilings and pause controls. Backpressure should slow migration before it destabilizes authoritative service. Secure administrative controls and record who changes filters, mappings, gates, or authority. Time-bounded transition components still require recovery and incident ownership.

**Retire the old data path completely.** After a stabilization window, prove there are no authorized writers, readers, jobs, exports, replicas, subscriptions, credentials, support flows, recovery procedures, or contractual dependencies. Preserve only records required by explicit retention and make their nonauthoritative status clear.

Remove capture, translation, repair, dual-read, and comparison infrastructure when its learning purpose ends. Continue observation for unexpected callers and keep a response plan. Retirement realizes cost and attack-surface reduction; cutover alone does not.

## Definitions and Notation

Let:

- $K$ be the set of stable migration-unit identities;
- $w$ be a monotonically ordered source-log position within its declared scope;
- $S_{w_0}$ be a consistent source snapshot whose boundary is $w_0$;
- $\Delta_{(w_0,w_c]}$ be all committed changes after $w_0$ through cut position $w_c$;
- $f$ be the versioned semantic transformation from source to destination representation;
- $A(T,x)$ mean idempotent application of transformed change $x$ to destination state $T$;
- $v_s(k)$ and $v_t(k)$ be source and destination versions for identity $k$;
- $R_s$, $R_t$, and $R_u$ be source-only, destination-only, and unequal identity sets;
- $I_j(T)$ be semantic invariant $j$ evaluated on destination state $T$;
- $e$ be the current authority epoch;
- $H$ be the maximum supported replay horizon;
- $\rho$ be change arrival rate and $\mu$ be sustained application rate.

Catch-up requires $\mu>\rho$ over a sufficiently long relevant interval; otherwise lag cannot converge under continuing load. This capacity inequality does not prove correctness. For keyed reconciliation over $K$, completeness requires $R_s=R_t=\varnothing$, equality policy requires $R_u=\varnothing$ except approved differences, and semantic readiness requires every hard $I_j(T)$ to hold.

## Mechanisms, Invariants, or Proof Structure

**Snapshot-plus-delta invariant.** If $S_{w_0}$ is consistent, capture includes every committed change in $(w_0,w_c]$, $f$ preserves declared meaning, and application respects necessary order and idempotency, then folding the transformed deltas over the transformed snapshot constructs the intended destination at $w_c$. Remove any premise and the conclusion fails: an inconsistent snapshot can mix times, a capture gap loses state, reordering can regress a transition, and non-idempotent retry can duplicate effects.

**Version monotonicity invariant.** A destination item for key $k$ accepts an incoming state only when its source version is greater than the stored version, except for an explicitly modeled correction. Thus late backfill at $w_0$ cannot overwrite CDC state at $w>w_0$. The check and write must be atomic, and deletion must retain a comparable version.

**Capacity derivation.** Let lag $L(t)$ measure unapplied changes. Ignoring bursts for the simple model, $dL/dt=\rho-\mu$. If $\mu\le\rho$, lag is nondecreasing and the migration cannot reach a zero-lag cutover while writes continue. If $\mu>\rho$, lag falls at rate $\mu-\rho$ while these rates hold. Therefore a plan needs measured headroom or an admission-control interval; average throughput alone is insufficient under bursts.

**Executable replay model.** This finite example applies a snapshot, out-of-order duplicates, a newer update, and a versioned delete. The conditional rule keeps the newest version per key and makes repeated event identity observable.

<!-- bijux-verify: {"id":"apply-versioned-migration","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"active=['a:15@13', 'c:30@10']\ntombstones=['b@14']\nduplicates=1\nstale=2\nhigh_watermark=14\n","stderr":""}} -->
```python
state = {"a": (10, 10, False), "b": (20, 10, False), "c": (30, 10, False)}
seen = set()
duplicates = 0
stale = 0
events = [
    ("e13", "a", 15, 13, False),
    ("e12", "a", 12, 12, False),
    ("e13", "a", 15, 13, False),
    ("e14", "b", None, 14, True),
    ("e11", "b", 21, 11, False),
]
for event_id, key, value, version, deleted in events:
    if event_id in seen:
        duplicates += 1
        continue
    seen.add(event_id)
    if version <= state.get(key, (None, -1, False))[1]:
        stale += 1
        continue
    state[key] = (value, version, deleted)
active = [f"{key}:{value}@{version}" for key, (value, version, deleted) in sorted(state.items()) if not deleted]
tombstones = [f"{key}@{version}" for key, (_, version, deleted) in sorted(state.items()) if deleted]
print(f"active={active}")
print(f"tombstones={tombstones}")
print(f"duplicates={duplicates}")
print(f"stale={stale}")
print(f"high_watermark={max(version for _, version, _ in state.values())}")
```

Execution establishes only the stated finite state transition under one in-memory rule. It does not verify database atomicity, capture completeness, crash recovery, performance, or production suitability.

**Deletion invariant.** If a delete at version $v_d$ is represented only by physical absence, a late snapshot item at $v_0<v_d$ can recreate it. Retaining a tombstone or equivalent authoritative delete position until no older input can arrive prevents this resurrection under the version rule.

**Authority invariant.** At each epoch and for each mutable fact, one owner may accept final writes. At transfer from $e$ to $e+1$, all writes bearing $e$ must fail at the authoritative decision boundary. Replication convergence after two independent writers is not a substitute for this property.

## Alternatives and Trade-Offs

**Offline copy versus online migration.** Offline movement simplifies boundary and authority reasoning but consumes outage. Online movement preserves availability but adds CDC, lag, replay, conflict, and cutover mechanisms. Choose from tolerated outage and recovery risk.

**Log-based CDC versus triggers or polling.** Logs usually preserve commit evidence with low application coupling but depend on engine semantics and retention. Triggers are explicit yet affect writes. Polling is portable but weak for deletes, equal timestamps, and commit order.

**Backfill-first versus CDC-first buffering.** Backfill-first with retained deltas is conceptually direct but needs enough log retention. Starting CDC into a buffer protects the boundary but adds storage and ordering. Concurrent apply needs atomic version arbitration.

**Preserve identifiers versus translate them.** Preservation reduces mapping and lineage work. Translation can escape legacy constraints or consolidate namespaces, but requires durable mapping, retry stability, and reference repair.

**Checksums versus semantic recomputation.** Checksums detect exact representation differences efficiently; semantic checks evaluate meaning across transformed representations. Use both at appropriate hierarchy and never call either sufficient alone.

**Rollback versus roll forward.** Rollback limits exposure before incompatible destination writes. Roll forward avoids reverse transformation after the point of no return but demands repair capability. Declare the boundary before migration.

**One-time migration code versus durable replication.** One-time code can be optimized for removal and audit. A durable integration needs long-lived product ownership, compatibility, service objectives, and evolution. Do not leave the former accidentally serving as the latter.

## Failure Modes and Misconceptions

1. **“A successful copy means a successful migration.”** It proves neither semantics nor authority.
2. **“The latest timestamp is a safe boundary.”** commit order and clock time are different.
3. **“Row counts prove completeness.”** a duplicate can mask a missing row.
4. **“Upsert makes replay idempotent.”** increments, appends, transitions, and effects can repeat.
5. **“CDC gives global order.”** guarantees may be only transactional, partitioned, or per key.
6. **“Deletes are just missing rows.”** absence lacks the version needed to defeat late input.
7. **“Backfill and CDC can write freely.”** older bulk state can overwrite newer live state.
8. **“The source is correct by definition.”** legacy defects and policy changes need adjudication.
9. **“Equivalent values have equivalent meaning.”** unit, precision, time basis, provenance, and null semantics matter.
10. **“A default repairs missing data.”** it may manufacture a false fact.
11. **“Dual writes keep both systems current.”** partial failure and retry create ambiguity.
12. **“Exactly once is end to end.”** the guarantee ends where the coordinated mechanism ends.
13. **“A small lag is harmless.”** the missing interval can contain a critical change.
14. **“Read cutover and write cutover are one event.”** their gates and consequences differ.
15. **“A flag fences old writers.”** queued work and direct credentials can bypass routing.
16. **“A backup guarantees rollback.”** restore, replay, external effects, and semantic compatibility remain.
17. **“Masked production data is unregulated test data.”** re-identification and governance risks remain.
18. **“Cutover completes retirement.”** hidden consumers, replicas, credentials, jobs, and recovery paths persist.

## Worked Examples

### Example 1

**Situation.** A table copy begins at 09:00 and selects pages for forty minutes while customer rows continue changing.

**Reasoning.** The result is not necessarily a state that existed at any instant: an early page can contain an old address while a later page contains a related new preference. Wall-clock start time does not identify included commits. The team obtains a consistent snapshot tied to log position $w_0$, retains changes after $w_0$, copies that snapshot, and applies deltas through a declared cut.

**Conclusion.** Online migration needs a snapshot-log boundary, not merely a copy start time.

### Example 2

**Situation.** A destination has 1,000,000 rows, exactly matching the source count.

**Reasoning.** Key comparison finds source key 417 missing and destination key 991 duplicated under two translated identifiers. Counts cancel. Partitioned keyed checks localize the discrepancy, and lineage reveals a retry generated a fresh destination ID.

**Conclusion.** Equal counts are useful evidence but cannot prove identity completeness.

### Example 3

**Situation.** CDC updates customer `a` to version 13 before its version-10 backfill chunk arrives.

**Reasoning.** An unconditional backfill overwrites new state. The destination stores source version with the row and atomically accepts only versions greater than the current value. Version 10 is classified stale, while reconciliation records that the key was covered by both paths.

**Conclusion.** Atomic version arbitration prevents late backfill regression.

### Example 4

**Situation.** A worker replays `increase-credit-by-10` after crashing between destination commit and checkpoint commit.

**Reasoning.** A plain increment raises credit twice. The migration assigns a stable change ID and commits both its effect and processed identity atomically, or transforms the operation into setting a source-versioned absolute value where semantics permit. Deduplication persists for at least replay horizon $H$.

**Conclusion.** Retry safety belongs to the logical operation and checkpoint boundary, not the transport label.

### Example 5

**Situation.** Backfill applies 2,000 changes per second while the source produces 2,400 per second.

**Reasoning.** Under the simple sustained-rate model, $dL/dt=2400-2000=400$ changes per second. Lag grows, so an online zero-lag cut cannot occur. The team increases verified capacity above peak-relevant arrival, reduces admitted writes during a controlled window, or revises the cutover design.

**Conclusion.** When $\mu\le\rho$, waiting longer does not produce catch-up.

### Example 6

**Situation.** A source stores local appointment time `2026-10-25 02:30` without offset in a jurisdiction whose daylight-saving clock repeats that hour.

**Reasoning.** Two instants share the representation. A transformer cannot infer which occurred from the value alone. It quarantines the record, seeks provenance such as original offset or event sequence, and records an accountable resolution rather than choosing silently.

**Conclusion.** Some legacy representations are genuinely ambiguous and require evidence or policy, not clever parsing.

### Example 7

**Situation.** A source deletion at version 48 is applied, then a delayed version-30 backfill row arrives.

**Reasoning.** If deletion removed every trace, the late row looks new and resurrects data. A version-48 tombstone remains until all inputs at version 48 or below are impossible. The conditional rule rejects version 30; retention then follows both replay and deletion obligations.

**Conclusion.** Versioned delete evidence prevents resurrection by stale migration input.

### Example 8

**Situation.** An order migration compares source and destination totals, which agree, but individual line amounts differ by equal and opposite rounding errors.

**Reasoning.** Aggregate equality masks row-level corruption. Validation compares line identities, currency, decimal scale, rounding rule, tax basis, and order invariant. It recomputes totals independently and tests boundary amounts rather than accepting one checksum.

**Conclusion.** Reconciliation must operate at the level where the business invariant can fail.

### Example 9

**Situation.** A router sends new writes to the destination, but an old batch job retains direct source credentials.

**Reasoning.** The route establishes no database fence. The migration stops admission, drains known work, advances an authority epoch enforced by writes, revokes legacy identities, and alerts on rejected stale attempts. It applies capture through the cut position before declaring authority transferred.

**Conclusion.** Cutover is an authority protocol; traffic routing alone is insufficient.

### Example 10

**Situation.** Six weeks after cutover, the source has no ordinary queries.

**Reasoning.** Inventory still finds a quarterly regulator export, a disaster-recovery runbook that restores the source, two analyst credentials, a search reindex job, backups, and a partner decoder contract. Each obligation is migrated, retained explicitly as nonauthoritative, or retired with evidence before infrastructure removal.

**Conclusion.** Data retirement covers obligations and recovery, not just live query volume.

## Cross-Program Connections

- [CONPAR](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies ordering, atomicity, race, and interference reasoning.
- [SDRE](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) develops deployment gates, observability, rollback, recovery, and incident operation.
- [DBE](../../18-database-engineering/ROADMAP.md) owns transaction, log, index, replication, constraint, and database-engine implementation depth.
- [DE](../../19-data-engineering/ROADMAP.md) owns pipeline orchestration, backfill operations, data quality, replay, and workload engineering.
- [DARCH](../../20-data-architecture-engineering/ROADMAP.md) owns enterprise semantics, lineage, governance, master data, retention, and analytical architecture.
- [SEC](../../25-security-engineering/ROADMAP.md) supplies identity, encryption, least privilege, audit, exfiltration, and sensitive-data controls.
- [DIST](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial failure, delivery, ordering, replication, consistency, and fencing models.
- [API](../../28-api-and-service-engineering/ROADMAP.md) develops idempotency, contract, request-routing, and compatibility mechanisms at service boundaries.

## References

1. Martin Kleppmann. *Designing Data-Intensive Applications*. O'Reilly Media, 2017.
2. Jim Gray and Andreas Reuter. *Transaction Processing: Concepts and Techniques*. Morgan Kaufmann, 1992.
3. Pramod J. Sadalage and Martin Fowler. *Refactoring Databases: Evolutionary Database Design*. Addison-Wesley, 2006.
4. Pat Helland. “Life beyond Distributed Transactions: An Apostate's Opinion.” *CIDR*, 2007. https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf
5. Martin Fowler. “Evolutionary Database Design.” Last significant update May 2016. Checked 2026-09-06. https://martinfowler.com/articles/evodb.html
6. Danilo Sato. “Parallel Change.” 13 May 2014. Checked 2026-09-06. https://martinfowler.com/bliki/ParallelChange.html
7. PostgreSQL Global Development Group. “Logical Decoding Concepts.” PostgreSQL 18 documentation. Checked 2026-09-06. https://www.postgresql.org/docs/current/logicaldecoding-explanation.html
8. PostgreSQL Global Development Group. “Logical Replication” and “Architecture.” PostgreSQL 18 documentation. Checked 2026-09-06. https://www.postgresql.org/docs/current/logical-replication.html
9. Apache Software Foundation. “Kafka Design: Message Delivery Semantics.” Current documentation checked 2026-09-06. https://kafka.apache.org/design/
10. Philip A. Bernstein and Eric Newcomer. *Principles of Transaction Processing*. 2nd ed. Morgan Kaufmann, 2009.
11. Ralph Kimball and Joe Caserta. *The Data Warehouse ETL Toolkit*. Wiley, 2004.
12. ISO. “ISO 8000-61:2016 Data quality — Part 61: Data quality management: Process reference model.” Official record checked 2026-09-06. https://www.iso.org/standard/63086.html

## Exercises

### Exercise 1

Define migration unit, source authority, consistent snapshot, high-water mark, CDC, backfill, idempotency identity, reconciliation, fence, tombstone, cutover, rollback, and roll forward.

### Exercise 2

A migration begins with 90,000 unapplied changes. The source sustains 700 changes per second and the destination sustains 1,000 per second. Under the simple constant-rate model, derive catch-up time. Recompute if destination throughput falls to 650 per second and explain the architectural consequence.

### Exercise 3

A snapshot backfill and CDC consumer write concurrently. The destination stores values but no source version; deletes physically remove rows. Diagnose two failure modes and specify a restartable repair.

### Exercise 4

Design an online migration of an order store to a new schema. Include semantic contract, snapshot boundary, capture, chunking, ordering, idempotency, deletes, validation, read and write gates, fencing, rollback boundary, recovery, and retirement.

### Exercise 5

A national archive must migrate multilingual historical records, uncertain dates, access restrictions, legal holds, redactions, provenance, and public search indexes. Propose an architecture without claiming that technical reconciliation determines archival, cultural, accessibility, privacy, or legal correctness.

## Answers to the Exercises

### Answer 1

A migration unit is the smallest independently identified item with tracked outcome. Source authority is the system permitted to decide a fact in a migration state. A consistent snapshot represents one declared transactional view. A high-water mark is the greatest source position durably applied. CDC derives committed changes from an authoritative record. Backfill moves or derives pre-existing data in bounded restartable work. An idempotency identity makes repeated logical application have one intended effect. Reconciliation classifies source, destination, movement, and semantic evidence. A fence rejects ended authority epochs. A tombstone represents a versioned deletion. Cutover transfers named authority under gates. Rollback restores an earlier compatible authority state; roll forward repairs or advances the new state when reversal is unsafe.

### Answer 2

With lag $L_0=90{,}000$, arrival $\rho=700$, and application $\mu=1000$, net drain is $\mu-\rho=300$ changes per second. Under constant rates, catch-up time is $L_0/(\mu-\rho)=90{,}000/300=300$ seconds, or five minutes.

At $\mu=650$, $dL/dt=700-650=50$ changes per second, so lag grows and no finite catch-up time exists while the rates persist. The plan must create verified capacity above the relevant arrival rate, reduce or stop admitted changes in a controlled window, partition the work differently, or choose another authority-transfer design. The calculation omits bursts, failures, checkpoint cost, and validation, so measured headroom is still required.

### Answer 3

First, a late backfill row can overwrite a newer CDC update because the destination cannot compare source order. Second, after CDC deletes a row, late backfill can recreate it because physical absence carries no delete version. Retries can also repeat non-idempotent transforms if event or chunk identity is absent.

Pause authority expansion, preserve logs, and identify a trustworthy snapshot position. Add source version and deletion state or tombstone to staged destination records. Rebuild affected identities from the consistent snapshot plus complete ordered changes, accepting a state atomically only when its version is newer. Give events and chunks stable identities, persist outcome and checkpoint atomically where possible, and retain deduplication for the replay horizon. Reconcile source-only, destination-only, unequal, deleted, stale, duplicate, and unpairable cases before resuming.

### Answer 4

Define stable order, customer, line, payment-reference, and event identities; decimal currency and rounding; time semantics; null and default meaning; state-transition and total invariants; history; retention; and source authority. Obtain a database-supported consistent snapshot at $w_0$ and retain authoritative log changes after it. Backfill by stable order or tenant ranges with bounded load, transform version, counts, keyed evidence, retry identity, and terminal status.

Apply deltas in the order promised for each order and preserve transaction relationships needed by invariants. Store source versions atomically so old backfill cannot overwrite new state. Carry versioned deletes or tombstones. Use one source write authority and an outbox or log rather than uncontrolled dual writes. Validate schema and constraints, identity sets, partition checksums, line values, totals, legal states, history, missing results, lag, query plans, capacity, recovery, and representative cohorts.

Gate reads separately through shadow or stable cohorts. Before write cutover, catch up through $w_c$, stop admission, drain and account for in-flight work, fence old writers at the data boundary, revoke bypass credentials, validate hard invariants, advance authority epoch, and observe rejected stale work. Declare the last reversible state before destination-only schema or effects; afterward stop admission and roll forward through audited repair. Rehearse backup restore and replay. Retire old jobs, readers, replicas, exports, identities, capture, comparison stores, support and recovery paths only after a stabilization window and explicit evidence.

### Answer 5

Establish accountable archival, cultural, language, accessibility, privacy, security, records, legal, preservation, and public-service authorities. Inventory originals, derivatives, catalogs, finding aids, redactions, restrictions, holds, provenance, physical references, search indexes, exports, backups, and manual annotations. Define identifiers and relationships without forcing uncertain dates, names, languages, or provenance into false precision. Preserve original representation alongside governed normalization where required.

Create an immutable migration ledger and a consistent inventory boundary. Backfill bounded collections with transform versions, stable identity mappings, checksums, access classification, lineage, and restartable outcomes; capture authorized catalog or restriction changes during movement. Treat deletion, redaction, embargo, and legal hold as distinct versioned states. Isolate sensitive copies, minimize access, and define temporary-data retention. Reconcile identities, relationships, encodings, rendered scripts, search behavior, restrictions, provenance, and risk-based samples; route ambiguity to qualified decision makers.

Cut public reads by coherent collections only after accessibility, security, performance, completeness, and semantic gates. Fence catalog authority before new writes, preserve recovery points and the final source position, and state when roll forward replaces rollback. Retire hidden exports, credentials, indexes, jobs, and restore procedures while retaining required preservation copies explicitly as nonoperational records. Technical evidence can establish bounded transformation and system behavior; it cannot itself determine cultural description, archival value, lawful access, privacy, accessibility, or legal compliance. Those conclusions remain with responsible people and processes.
