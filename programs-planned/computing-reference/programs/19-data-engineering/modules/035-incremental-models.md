---
module_id: DE-035
program: Data Engineering
level: 1
module_number: 35
title: Incremental Models
status: complete
last_verified: 2026-09-02
---

# Incremental Models

## One-Page Review

### Governing question

How can a model update only the affected portion of its result while remaining equivalent to a full recomputation over the same source cut, including late arrivals, updates, deletes, reference changes, retries, code/schema changes, and atomic publication?

### Essential definitions

- A **full model** computes a result $F(S_c)$ from the complete governed source state $S_c$ at cut $c$.
- An **incremental model** derives a new result from a prior trusted result plus a bounded set of relevant changes and state.
- A **change cursor** is a source-native monotone position such as a log sequence number, offset vector, snapshot ID, or immutable manifest boundary.
- A **high-water mark** is the greatest safely committed source position, not simply the maximum business timestamp found in output.
- A **change event** identifies an occurrence and operation—insert/upsert/update/delete—plus entity key, source order/version, before/after data as available, schema, and transaction context.
- A **tombstone** is explicit delete evidence retained so an entity does not reappear when older state is replayed.
- A **lookback window** deliberately reprocesses an overlapping source interval to absorb bounded lateness; it is not proof that later arrivals cannot exist.
- The **affected set** is the exact set of output keys/partitions/windows whose values may change because of a source, reference, code, or schema change.
- An **incremental state transition** applies canonical changes to prior state under identity, ordering, and conflict rules.
- **idempotence** means replaying the same logical change interval produces no additional logical effect.
- A **checkpoint** binds the last committed source cut to the exact published model generation and transformation version.
- A **full-refresh oracle** recomputes the complete result independently enough to test incremental equivalence.

### Central model, mechanism, or theorem

Let $S_c$ be complete source state at cut $c$, $F_v$ the full transformation at version $v$, $O_a=F_v(S_a)$ the trusted output at prior cut $a$, and $\Delta_{(a,b]}$ the complete ordered change interval through cut $b$. An incremental transition $U_v$ is correct only if

$$
U_v(O_a,\Delta_{(a,b]},R_a,R_b)=F_v(S_b),
$$

under the declared output equivalence relation and reference states $R_a,R_b$. This is an obligation, not a property conferred by the word “incremental.”

Checkpoint advancement and publication must be coupled:

$$
(O_a,a)\longrightarrow(O_b,b)
$$

as one conditional logical commit. Advancing to $b$ before $O_b$ is trusted can lose changes; publishing $O_b$ without binding $b$ makes retry ambiguous.

If a change to source key $x$ can influence output keys $I_v(x)$, the affected set for change set $\Delta$ is

$$
A_v(\Delta)=\bigcup_{x\in\Delta}I_v(x).
$$

Rows selected merely by their own modified timestamp can be smaller than $A_v$: joins, aggregates, windows, mutable dimensions, deletes, and changed code propagate influence.

### Critical invariants

- Prior output and checkpoint are one trusted generation created by the same model/contract/runtime lineage.
- Source interval is expressed with exact monotone cursor bounds, source epoch/identity, transaction semantics, and retention evidence.
- Every delivered change has stable occurrence identity, entity key, operation, ordering/version, schema, and delete behavior.
- Duplicate/out-of-order delivery is resolved deterministically; older changes cannot overwrite newer state or resurrect tombstones.
- The affected set covers direct and transitive influence through joins, aggregates, windows, reference data, and downstream models.
- Incremental predicates are completeness rules first and scan optimizations second; destination pruning never changes match semantics.
- State transition is idempotent and stages one isolated candidate; unknown commit outcomes are reconciled before retry.
- Quality gates compare candidate keys, multiplicities, schema, deletes, components, source controls, and business results—not just row counts.
- Checkpoint advances only with conditional/atomic publication of the validated generation and records source/output identities.
- Full rebuilds remain possible from retained raw/source history, code/config/runtime, schemas, and reference generations.
- Incremental-versus-full differential checks run periodically and after logic, schema, strategy, engine, or reference changes.
- Drift, lag, lateness, replay, duplicate/conflict, delete, state-size, cost, and rebuild-horizon SLOs are observable.

### Common failures

Common failures include using output `max(event_time)` as a source cursor; using `>` and losing ties; using `>=` with append and duplicating ties; assuming modified timestamps are immutable/monotone; ignoring deletes; filtering tombstones before winner resolution; accepting nullable/nonunique keys; applying changes in arrival order; advancing a checkpoint before publication; retrying an ambiguous merge; treating a fixed lookback as completeness proof; scanning only changed fact rows when a dimension/relation changed; incrementing nonadditive metrics; forgetting window neighbors; mixing old logic with new rows after a code change; synchronizing columns without backfilling historical values; reading append-only snapshot deltas as if they included overwrites/deletes; pruning destination rows so matching old keys appear absent; and declaring parity from equal totals.

### Compact example

An initial cut contains orders `o1=100`, `o2=200`, and `o3=300`. The next log interval delivers an `o1` update to 150, an `o2` tombstone, new `o4=50`, a duplicate delivery of the `o1` update, and a late `o3` correction to 250 whose business timestamp is old. Cursor/identity-aware application yields `o1=150`, `o3=250`, `o4=50`, total 450; a full replay agrees and replaying the interval is idempotent. A naive filter on business time captures only `o4` and yields 650, silently retaining stale `o1`, `o2`, and `o3`.

### Connections

[DE-021](021-full-and-incremental-extraction.md) defines bounded acquisition, [DE-026](026-database-change-data-capture.md) defines CDC, [DE-027](027-idempotent-loads.md) defines replay-safe effects, [DE-030](030-designing-replayable-raw-ingestion.md) preserves raw history, and [DE-032](032-sql-transformation-pipelines.md) through [DE-034](034-partitioned-processing.md) define transformation graphs, frames, and partition commits. DE-036 next treats merge/upsert mechanics; DE-037 through DE-040 treat backfills, corrections, determinism, and testing.

## Governing Question

What evidence establishes that updating less data produced the same trusted answer as recomputing everything that the model means?

Incremental computation is an optimization around state. The prior output becomes an input, a change interval substitutes for a complete source scan, and an update strategy mutates or replaces only an affected region. That saves work only by adding obligations: prior-state validity, source cursor completeness, change identity/order, affected-set analysis, idempotence, concurrency, checkpoint publication, and periodic full comparison.

The central danger is confusing “recent rows” with “all relevant changes.” An entity can be corrected today with an old event time. A delete has no surviving row to satisfy a predicate. A mutable dimension can change millions of joined outputs even when facts are untouched. A seven-day rolling metric needs neighbors around a changed day. A new exchange rate or business rule can invalidate history.

The correct target is equivalence to the declared full model at the same source/reference cut and code version. Sometimes an organization explicitly chooses bounded correction—such as “results older than 90 days are final.” That is a different business contract with a stated residual error/repair policy, not exact incremental equivalence.

## Why This Matters

Full recomputation is conceptually simple but can exceed warehouse cost, source-retention, batch-window, or latency budgets. Incremental models make large histories operationally tractable by processing only new/changed inputs and impacted outputs.

Small daily deltas can hide large semantic blast radii. Updating one customer’s region may reattribute years of facts if the model uses current attributes. Changing a sessionization threshold can regroup all events. Replacing a currency rate changes every dependent measure for that date/currency. Incremental design begins with influence, not scan size.

Sources redeliver. PostgreSQL documents that logical decoding slots can replay recent changes after a crash, making clients responsible for avoiding harmful duplicate effects. Debezium documents duplicate change events during recovery and explicit delete/tombstone behavior. A production model must expect at-least-once delivery around failures even when normal operation appears once-only.

Time is not one cursor. Event time expresses domain occurrence; update/commit/log position expresses change discovery; ingestion and processing times express transport/operation. A watermark is an estimate or progress statement with source-specific meaning, not a proof that all old-event-time corrections are impossible. Late-data policy determines whether to update, quarantine, reopen, or declare final.

Incremental output accumulates history. A defect can persist long after the source interval that created it. Logic and schema changes can split one table into eras with different semantics. Therefore full refresh, snapshot comparison, drift monitoring, and migration policy are part of the normal design rather than emergency afterthoughts.

## Prerequisites and Retrieval

Retrieve the business/output contract; source owners and immutable raw/history retention; source system/epoch, transaction log, offsets/LSNs/snapshot IDs/manifests and retention; extraction checkpoints; source/event/entity/occurrence keys; inserts, updates, deletes, key changes, before/after images and tombstones; source transaction ordering; duplicate/redelivery behavior; source schemas and evolution; event/effective/transaction/commit/ingestion/processing times; lateness distributions and correction SLAs; current full transformation code; model DAG and column/row influence; joins/cardinalities; mutable dimensions/reference versions; aggregates/windows/sessionization; existing target grain/key/schema; incremental strategy and predicates; destination pruning; partitions; state/history/tombstone retention; engine/adapter/version/transaction behavior; concurrency/retry/timeouts; candidate/publication/checkpoint store; full-refresh procedure/cost/horizon; tests/reconciliation and historical controls; lineage/metrics; security/residency; SLOs/cost; incidents; rollback; and disaster recovery.

Distinguish source log cursor from event timestamp; high-water mark from maximum target value; extraction checkpoint from model checkpoint; occurrence identity from entity key; delivery duplicate from legitimate repeat; entity version from arrival order; delete event from null-valued update; source state from change log; append delta from row-level change delta; source predicate from destination-scan predicate; affected input from affected output; current dimension from as-of dimension; incremental transition from merge syntax; task completion from committed generation; checkpoint write from data publication; full refresh from destructive unvalidated replacement; late data from delayed processing; bounded lookback from completeness guarantee; schema compatibility from historical backfill; and numerical parity from full semantic equivalence.

Create an incremental contract before implementation:

| Field | Required content |
|---|---|
| Full semantics | Full function/version, source/reference cuts, output grain/key/schema, equivalence |
| Prior state | Trusted generation, checkpoint, contract/code/runtime lineage, validation status |
| Change feed | Source/epoch, cursor domain/bounds, transaction/order, event identity, retention |
| Operations | Insert/update/delete/key-change/tombstone/before-after/conflict semantics |
| Affected set | Direct/transitive key, join, aggregate, window, dimension, code/schema influence |
| Transition | Strategy, dedup/winner rule, destination match, idempotence, concurrency/timeout |
| Validation | Delta controls, candidate/global checks, incremental/full differential cadence |
| Commit | Candidate identity, expected prior, atomic/conditional publication plus checkpoint |
| Recovery | Replay horizon, full rebuild, rollback, unknown-outcome lookup, repair/backfill |
| Operations | Lag/lateness/drift/state/cost SLOs, lineage, ownership, alerts and evidence |

Do not adopt incremental execution until a trusted full baseline exists and can be recomputed or otherwise independently controlled. An incremental table without a known full meaning is merely accumulated state.

## Learning Objectives

After completing this module, you should be able to:

1. specify an incremental model as a state transition equivalent to a named full transformation;
2. choose source-native cursors and half-open change intervals instead of unsafe output timestamps;
3. model insert, update, delete, key-change, duplicate, out-of-order, and tombstone behavior;
4. derive affected outputs through joins, dimensions, aggregates, windows, and a model DAG;
5. distinguish source completeness predicates from destination-scan performance predicates;
6. design idempotent transitions and couple checkpoint advancement to output publication;
7. handle late data through explicit exact, bounded, or repair policies;
8. migrate code, schema, strategy, and reference changes without mixed historical semantics;
9. validate incremental results against source controls and full-refresh/differential oracles; and
10. operate lag, drift, state, cost, recovery, security, and audit controls over the model lifecycle.

## Core Exposition

### Begin with the full model

Write the complete transformation $F_v$ first. Name exact source/reference states, row grain, key, filters, versions/deletes, joins, measures, time semantics, schema, ordering promises, and publication. If the full answer is ambiguous, its incremental optimization cannot be correct.

Build a trusted baseline in isolation and validate it with independent controls. Record its source cuts, code/config/runtime, schema, reference generations, output manifest, checks, and publication receipt. This baseline plus checkpoint becomes prior state.

Define the equivalence relation. Exact key/multiplicity/schema/integer/decimal equality is often required. Floating/approximate outputs may use justified tolerances. Physical file order/partitioning need not match unless promised. Security and visibility are part of equivalence.

Retain a runnable full path. It is the repair mechanism, migration route, and strongest practical oracle. A codebase whose incremental branch is valid but full branch has rotted is not recoverable.

### Identify what kind of source changes

An immutable append-only event source differs from mutable entity state. Append-only facts can often be processed by occurrence identity/cursor and combined. Mutable tables require updates, deletes, key changes, and sometimes transaction-level consistency.

For CDC, capture operation, source entity key, stable event identity, source transaction and order, source epoch, schema, before/after images where available, and log cursor. Do not infer delete from absence in a partial extract.

A primary-key change may be represented as delete-old plus insert-new. Debezium’s PostgreSQL connector documents delete and tombstone events for old keys followed by the new-key record. Consumers must preserve these operations rather than treating them as one ordinary update without old-key knowledge.

Snapshot-diff sources need two complete comparable snapshots and identity rules. API/file sources may provide mutable pages or revised objects without an ordered log. Choose exact version manifests and explicit comparison; timestamp filtering alone may be insufficient.

### Use a source-native cursor

A cursor should order discovery of relevant changes and support an immutable interval such as $(a,b]$. Examples include transaction log position/LSN, per-partition broker offsets, source commit sequence, table snapshot ancestry, or immutable manifest generations.

Bind cursor to source identity/epoch. Log positions can be reused or invalid after failover, reset, resnapshot, topic recreation, or source migration. A numeric offset without source epoch is not globally meaningful.

For partitioned logs, the checkpoint is a vector rather than one scalar. Define consistent transaction/cut behavior across partitions or record that atomic source transactions can be observed in stages. Never take the maximum of incomparable positions.

Verify retention before processing. If prior cursor fell behind the oldest available log/snapshot, stop and resnapshot/reconcile; do not jump to current and silently lose changes.

### Avoid target-derived timestamp checkpoints

Using `max(updated_at)` from target is attractive and fragile. Output may omit filtered rows, deletes, invalid records, or fields. Several records can share the maximum. Clocks can move; timestamps can be edited, null, truncated, or late. A failed partial write can advance target max without complete processing.

With `>` a tie at the previous maximum may be lost. With `>=`, ties repeat; append-only destinations duplicate them unless identity makes replay safe. Neither operator repairs missing deletes or old-timestamp corrections.

A target-derived value also couples checkpoint to transformation. A business rule that filters the maximum-timestamp record can move the apparent cursor backward. Keep source progress in a dedicated control record bound to the candidate generation.

If a timestamp is the only source mechanism, define a lookback plus stable occurrence identity, immutable snapshots, overlap deduplication, null/precision/time-zone handling, and an explicit maximum-lateness/repair contract. State residual risk honestly.

### Canonicalize change delivery

Expect duplicate and out-of-order events. Deduplicate by stable change occurrence identity when the source provides it; do not collapse two legitimate updates that happen to have equal payloads.

Within an entity, apply source authority: transaction/log order, version, valid/transaction time, source priority, and tie/conflict rules. Arrival or task completion order is not authority. Detect two different payloads with the same claimed version/event identity.

Store tombstone/version state sufficiently long to prevent an older replayed upsert from resurrecting a deleted entity. Garbage collection needs a source-retention and lateness proof or a full resnapshot boundary.

Preserve transaction grouping where model semantics require it. Applying half of a multi-row source transaction can violate balances or relationships. Batch boundaries and checkpoint commits should respect source transaction semantics or validate/repair partial visibility.

### Derive the affected set

A changed source row does not imply only the same output key changes. Define an influence relation $I_v(x)$ for each source/model input key and union it across the change interval.

For key-preserving row transformations, the affected output may be the same key. For group aggregates, a row moving from group A to B affects both A and B. For joins, changes affect all matching rows on the other side. For current-dimension enrichment, a dimension-key change can affect every joined fact if current attribution is intended.

Windows require context. A change at time $t$ can affect windows whose frames include $t$, plus ranking/session neighbors. Recompute a halo large enough for the mathematical dependency, not an arbitrary number of rows.

Graph propagation is transitive. A changed base model may invalidate downstream keys/partitions even if their direct source timestamps are old. Maintain model/column/row-key lineage where feasible, or conservatively rebuild a wider region.

### Separate source filtering from destination pruning

The source predicate decides which changes enter candidate computation. It must be complete for the interval and affected-set contract. A too-narrow source filter loses semantic input.

The destination predicate limits how much existing target state is scanned during a merge/delete/replace operation. It is only safe if every possible matching target row lies inside the scanned region. A late old key can otherwise appear “not matched” and be inserted as a duplicate.

dbt documents both model-side incremental filters and optional destination `incremental_predicates`; it also notes the latter are arbitrary SQL not syntax-checked by dbt. Treat source completeness and destination performance as different proof obligations.

Measure scan benefit only after key/time containment is proved. A predicate based on seven recent days is unsafe for keys whose prior target rows may be older unless key layout/index/table partitioning or a different strategy guarantees discovery.

### Choose append only when the contract is append only

Append is correct for immutable uniquely identified output occurrences when the source interval is complete and replay does not reappend accepted occurrences. It is wrong for mutable entity rows, replacement aggregates, deletes, or repeated overlapping windows unless another identity/compaction layer resolves them.

An append table can preserve revisions as events rather than current state. That is a different output grain: one row per change occurrence, not one row per entity. Consumers need current-state resolution or version queries.

Table/snapshot incremental readers may expose only appended files/rows. Iceberg’s current Spark documentation says its incremental read covers append operations and does not support replace, overwrite, or delete operations. Never infer a general change feed from an append-delta API.

Record accepted occurrence IDs or use a transactional table/source mechanism that makes interval application idempotent. File/object names generated anew on retry do not establish logical uniqueness.

### Treat updates and deletes as state transitions

An entity-state target needs a unique nonnull match key, source version/order, operation, and conflict policy. The target transition should reject or quarantine duplicate candidate keys before mutation.

Deletes may physically remove rows, mark soft-delete state, close validity intervals, or emit tombstone records. Choose from consumer and audit semantics. A delete must participate in ordering; filtering it before selecting the authoritative version can resurrect history.

Key changes require old and new keys. Apply the old-key delete and new-key upsert consistently. If the source lacks old-key information, resnapshot or maintain a mapping; searching target by changed payload is unsafe.

DE-036 treats database/table `MERGE`, delete-insert, overwrite, and upsert details. Here the invariant is engine-independent: applying canonical changes to prior state must equal full current-state resolution at the same cut.

### Recompute aggregates from sufficient state

For additive append-only measures, incrementing sum/count by new events can be valid. Updates/deletes require subtracting old contribution and adding new, or recomputing affected groups from authoritative source state.

Maintain sufficient state. Mean needs sum/count; variance needs a correct merge/update state; min/max cannot be reversed from one scalar when the current extremum is deleted unless additional candidates/state exist. Exact distinct and median require membership/order state or recomputation.

When an entity changes group, update both old and new groups. A change event with only after-image may not reveal the old group; retrieve before-state from the prior trusted entity model or source.

Prefer recomputing affected groups/windows from an immutable authoritative slice when inverse logic becomes fragile. Incremental does not mean every output cell must be adjusted arithmetically.

### Handle windows and session boundaries

Rolling windows, ranks, sessionization, funnels, and interval joins propagate changes across neighbors. Define the dependency radius/closure in event time and key space.

A seven-day trailing sum changed on day $d$ can affect outputs $d$ through $d+6$ under daily closed/open rules. Recompute input context before the first affected output and emit only the owned affected outputs.

Sessionization can have unbounded chains under a gap rule: inserting one bridging event may merge two sessions and alter many later IDs. Bound the domain contract or recompute the entity’s complete relevant history.

Watermarks estimate progress and state cleanup. Beam documents that event-time order is not guaranteed and uses watermarks/allowed lateness to classify late elements. Batch incremental models still need a durable policy for data beyond the accepted lateness: reject, correction queue, reopened outputs, or explicit finality.

### Govern late data and lookback

Measure lateness as processing/ingestion/commit time minus the relevant event/effective time, segmented by source, tenant, operation, and incident periods. Pick a lookback from both distribution and consequence, not convenience.

An overlapping lookback must be idempotent: reselecting earlier source rows cannot append duplicate output. Recompute/replace affected partitions or match stable keys. Checkpoint still tracks source progress; lookback defines intentional reprocessing.

No finite empirical lookback proves future completeness. Define maximum accepted lateness contract, residual risk, monitoring, exception/repair path, and finalization. High-consequence corrections may require reopening any historical period.

Separate late event time from delayed CDC. A record with old business time and new log position is not late in log order; source-native cursor captures it. This is why event-time maximum is a poor universal checkpoint.

### Couple checkpoint and output publication

Build an isolated candidate from trusted generation/checkpoint plus immutable change interval. Record exact input events/manifest, affected set, transition version, prior/new candidate state, checks, and proposed next cursor.

Validate before trust. Then conditionally publish candidate and checkpoint against the expected prior generation/cursor. The authoritative control record maps model generation to source cut and code/contract/runtime.

If output/catalog and checkpoint store cannot transact together, use a recoverable protocol: immutable candidate, idempotent publication identifier, durable intent/receipt, compare-and-swap, and reconciliation on restart. Define which system is authoritative.

On timeout, look up source job, target transaction/snapshot, publication receipt, and checkpoint mapping. Never advance cursor based only on task completion or retry mutation blindly.

### Make replay idempotent

Logical run ID identifies the interval and prior generation; attempt ID identifies execution. Retries use the same immutable inputs and write isolated attempt candidates. Only one accepted candidate becomes reachable.

Event application remembers/derives occurrence identity and version authority. Applying the same interval twice to the same prior state must yield an equivalent candidate. Where target operations cannot guarantee this directly, rebuild the affected region and replace it atomically.

Do not perform unkeyed external side effects inside row processing. Version side inputs and keep the transition pure. Necessary downstream effects use an outbox or idempotency key bound to published generation.

Test replay after failure at every boundary: after source read, partial stage, target write, target commit before acknowledgement, checkpoint intent, and checkpoint commit. Verify no lost cursor or duplicate logical row.

### Manage concurrent writers

Serialize incremental writers per logical model unless the state transition and table commit protocol prove safe concurrency. Scheduled run, retry, backfill, correction, and full refresh can overlap.

Two runs starting from $(O_a,a)$ may both compute candidates. Only one may advance the expected prior pointer. The loser rebases/recomputes from the new trusted state or is discarded; last wall-clock writer wins is unsafe.

Disjoint partition changes can sometimes commit independently, but global manifests, aggregates, constraints, and checkpoints still coordinate. Declare ownership and conflict detection.

Full refresh should build a new generation without dropping trusted output first. It publishes only after validation and invalidates/rebases outstanding incremental attempts.

### Treat reference changes as source changes

Mutable dimensions, exchange rates, tax rules, calendars, identity maps, model artifacts, and policy configuration are transformation inputs. Give them versions/generations and influence rules.

If output uses current customer segment, a segment change can affect all historical facts for that customer. If output uses as-of segment, only facts whose valid-time join changes are affected. The semantic contract decides.

Reference feeds may lack CDC. Snapshot/diff them by stable identity and derive affected fact keys/partitions. If influence cannot be enumerated safely, rebuild a conservative region or full model.

Never join incremental facts to an unrecorded “latest” reference during retry. The same source interval could produce different output. Bind reference snapshot to run/candidate.

### Handle code and schema changes

Changing transformation logic creates version $v+1$. Applying it only to new rows yields mixed semantics unless the change is proven history-insensitive and compatible. Classify the change and document its historical effect.

Full rebuild is the default for changed filters, joins, grain, keys, rounding, time, dimensions, UDF/model artifacts, or output meaning. Targeted recomputation is acceptable when affected history is derived and verified.

Schema synchronization does not populate old values automatically. dbt’s current documentation explicitly notes that its `on_schema_change` behaviors do not backfill historical records. A new derived column may require full or targeted history recomputation even if DDL succeeds.

Pin engine/adapter/runtime and compile artifacts. An upgrade can change casts, nulls, merge behavior, ordering, or plans. Differentially compare the same immutable source cut before promotion.

### Validate delta and whole state

Delta controls include cursor continuity, source epoch, transaction boundaries, expected event/operation counts, duplicate/conflict IDs, schema versions, null keys, order monotonicity, deletes/key changes, and quarantine.

Affected-region controls compare old/new keys, version winners, before/after contributions, groups/windows, joins, and both set-difference directions. Reconcile inserts, updates, deletes, unchanged, conflicts, and rejects.

Whole-state controls include output grain/key, schema/null/domain, source population, additive components, reference consistency, business questions, security, partitions/files, and trusted manifest. A small delta can violate a global key.

Run the full model on manageable fixtures and periodic production snapshots. Compare canonical identities, multiplicities, columns/types, nulls, values, components, ordering promises, and deletes. Equal rows/total alone is insufficient.

### Use full refresh as oracle and recovery

Schedule differential full refresh according to risk, change volume, source retention, model complexity, incidents, and cost. High-risk mutable models need stronger cadence than append-only logs.

Build full output in isolation from the same source/reference cut and version, validate, then compare with incremental. Classify differences before replacing either. The full path may also be wrong, so retain independent source/business controls.

Track drift by key/partition/age/operation. A growing difference often identifies missed late deletes, window influence, reference changes, or nondeterministic logic.

Test recovery within retention and capacity limits. If a full rebuild takes longer than source/log retention or the business recovery objective, extend raw retention, checkpoint snapshots, or redesign state.

### Observe and secure incremental state

Record prior/new generation and cursor, interval size/age, source lag, event-time lateness, operation/duplicate/conflict/quarantine counts, affected keys/partitions, target inserts/updates/deletes/unchanged, scan bytes, duration, cost, tests, publication receipt, and drift comparisons.

Alert on cursor stalls/gaps/epoch changes, retention margin, unexpected operation ratios, null/duplicate keys, tombstone backlog, lookback overflow, state growth, full-refresh failures, drift, concurrent commit conflicts, and rollback-horizon risk.

CDC before-images and tombstones may expose sensitive historical values. Restrict raw/change/state/candidate/checkpoint access; encrypt logs, spill and artifacts; minimize bounded diagnostics; preserve tenant identity through dedup/merge; and audit publisher/checkpoint authority.

Checkpoint manipulation can skip or replay data and is privileged. Use least privilege, compare-and-swap, immutable audit, backups, and recovery tests. Monitoring should not log payloads unnecessarily.

### Operate incidents and bounded finality

Classify incidents as source-gap/epoch/retention, parser/schema, duplicate/order/conflict, missed affected set, state corruption, strategy/transaction, checkpoint/publication, drift, performance, security, or downstream contract.

Freeze advancement when completeness is uncertain. Preserve raw interval, current checkpoint/generation, candidate, compiled code, logs/job IDs, target receipts, and failed evidence. Resnapshot/rebuild rather than guessing a cursor.

If the business declares periods final, record finality rule, exceptions, materiality threshold, approval, correction/restatement path, and consumer communication. “Too expensive to recompute” is not a semantic finality rule by itself.

After repair, compare full and incremental state, publish a new generation conditionally, and document lineage from defective to corrected outputs. Strengthen the invariant that failed—cursor gap detector, delete fixture, influence map, drift cadence, or checkpoint protocol.

## Definitions and Notation

Let:

- $S_c$ be the complete source state at source-native cut $c$;
- $R_c$ be all governed reference/configuration state at cut/version $c$;
- $F_v$ be the complete transformation under contract/code version $v$;
- $O_c^v=F_v(S_c,R_c)$ be its trusted full result;
- $\Delta_{(a,b]}$ be the complete canonical change sequence after cursor $a$ through $b$;
- $U_v$ be an incremental state transition;
- $I_v(x)$ be output influence of changed source/reference key $x$;
- $A_v(\Delta)=\bigcup_{x\in\Delta}I_v(x)$ be the affected output set;
- $g_a,g_b$ be trusted/candidate output generation identities; and
- $C=(source\ identity,epoch,cursor,generation,v)$ be a checkpoint mapping.

The correctness obligation is

$$
U_v(O_a^v,\Delta_{(a,b]},R_a,R_b)\approx F_v(S_b,R_b),
$$

where $\approx$ is the declared output equivalence. This assumes $O_a^v$ was valid, the interval is complete, and the transition considers all influence.

Idempotence for one logical interval requires

$$
U_v(U_v(O_a,\Delta),\Delta)\approx U_v(O_a,\Delta),
$$

or an equivalent attempt protocol that always rebuilds from $O_a$ and publishes at most one candidate. Idempotence must not erase distinct legitimate changes with equal payloads.

For an additive group with old contribution $q_{old}$ and new contribution $q_{new}$, an update can apply

$$
Q'=Q-q_{old}+q_{new}.
$$

This requires reliable before-state and invertible/additive semantics; otherwise recompute the affected group from authority.

Checkpoint/output advancement is a conditional pair transition:

$$
(g_a,a,v)\xrightarrow[expected=(g_a,a,v)]{validated}(g_b,b,v).
$$

A failure before the transition leaves the old pair trusted; an ambiguous acknowledgement is resolved by reading the authoritative pair/receipt.

For model graph edge influence, affected outputs propagate transitively. A local timestamp predicate is complete only if it selects a superset of $A_v(\Delta)$ under proven source/reference/window rules.

## Mechanisms, Invariants, or Proof Structure

An incremental-model review should:

1. freeze the full model, output equivalence, source/reference cuts, and trusted baseline;
2. choose source-native cursor/epoch and exact half-open change intervals within retention;
3. canonicalize event identity, entity key, operation, transaction/order/version, schema, and tombstones;
4. derive direct/transitive affected outputs through filters, joins, groups, windows, references, and DAGs;
5. prove source completeness separately from destination-scan pruning and select an appropriate transition strategy;
6. verify duplicate/out-of-order replay, deletes/key changes, idempotence, concurrency, and timeout reconciliation;
7. build an isolated candidate and run delta, affected-region, whole-state, security, and resource gates;
8. conditionally/atomically publish candidate plus checkpoint mapping against the expected prior pair;
9. compare periodically with a full-refresh oracle at the same immutable cuts and classify drift; and
10. retain raw/source history, tombstones, code/config/runtime, reference snapshots, receipts, prior state, and evidence for replay, rollback, and rebuild.

The finite model below uses an ordered source cursor distinct from business event time. It preserves versions/tombstones, deduplicates repeated event identity, and binds state to a checkpoint. It demonstrates one bounded equivalence and replay result; it does not prove production CDC completeness, transactions, concurrency, target merge behavior, source retention, arbitrary influence, or atomic publication.

<!-- bijux-verify: {"id":"incremental-full-equivalence","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial_rows=3\ndelivered_changes=5\nunique_changes=4\ncheckpoint_before=3\ncheckpoint_after=7\nincremental_rows=((\u0027o1\u0027, 2, 150), (\u0027o3\u0027, 2, 250), (\u0027o4\u0027, 1, 50))\nincremental_total=450\nfull_total=450\nequivalent=True\nreplay_stable=True\nnaive_event_time_total=650\ndelete_applied=True\n","stderr":""}} -->
```python
HISTORY = (
    ("e1", 1, "o1", 1, "upsert", 100, 1),
    ("e2", 2, "o2", 1, "upsert", 200, 2),
    ("e3", 3, "o3", 1, "upsert", 300, 3),
    ("e4", 4, "o1", 2, "upsert", 150, 1),
    ("e5", 5, "o2", 2, "delete", None, 2),
    ("e6", 6, "o4", 1, "upsert", 50, 4),
    ("e7", 7, "o3", 2, "upsert", 250, 2),
)
DELIVERED_DELTA = (HISTORY[3], HISTORY[4], HISTORY[5], HISTORY[3], HISTORY[6])

def apply(prior_state, prior_seen, deliveries, checkpoint):
    state = dict(prior_state)
    seen = set(prior_seen)
    next_checkpoint = checkpoint
    for event in sorted(deliveries, key=lambda item: (item[1], item[0])):
        event_id, position, order_id, version, operation, cents, _ = event
        next_checkpoint = max(next_checkpoint, position)
        if event_id in seen:
            continue
        seen.add(event_id)
        current = state.get(order_id)
        if current is None or version > current[0]:
            state[order_id] = (version, operation, cents)
        elif version == current[0] and current[1:] != (operation, cents):
            raise ValueError("conflicting payload at one version")
    return state, seen, next_checkpoint

def visible(state):
    return tuple(
        (order_id, version, cents)
        for order_id, (version, operation, cents) in sorted(state.items())
        if operation != "delete"
    )

initial_state, initial_seen, checkpoint_before = apply({}, set(), HISTORY[:3], 0)
incremental_state, incremental_seen, checkpoint_after = apply(
    initial_state, initial_seen, DELIVERED_DELTA, checkpoint_before
)
replayed_state, replayed_seen, replayed_checkpoint = apply(
    incremental_state, incremental_seen, DELIVERED_DELTA, checkpoint_after
)
full_state, _, _ = apply({}, set(), HISTORY, 0)

# A business-event-time cutoff after max 3 sees only e6, missing old-time corrections/deletes.
naive_delta = tuple(event for event in HISTORY[3:] if event[6] > 3)
naive_state, _, _ = apply(initial_state, initial_seen, naive_delta, checkpoint_before)

incremental_rows = visible(incremental_state)
full_rows = visible(full_state)
replayed_rows = visible(replayed_state)
naive_rows = visible(naive_state)
print(f"initial_rows={len(visible(initial_state))}")
print(f"delivered_changes={len(DELIVERED_DELTA)}")
print(f"unique_changes={len({event[0] for event in DELIVERED_DELTA})}")
print(f"checkpoint_before={checkpoint_before}")
print(f"checkpoint_after={checkpoint_after}")
print(f"incremental_rows={incremental_rows}")
print(f"incremental_total={sum(row[2] for row in incremental_rows)}")
print(f"full_total={sum(row[2] for row in full_rows)}")
print(f"equivalent={incremental_rows == full_rows}")
print(f"replay_stable={replayed_rows == incremental_rows and replayed_checkpoint == 7}")
print(f"naive_event_time_total={sum(row[2] for row in naive_rows)}")
print(f"delete_applied={'o2' not in {row[0] for row in incremental_rows}}")
```

The model stores delete version 2 for `o2` even though visible output omits the row; that state blocks an older replay from resurrecting it. In a production system, checkpoint 7 becomes authoritative only with publication of the validated 450-cent generation.

## Alternatives and Trade-Offs

**Full recomputation versus incremental transition.** Full builds simplify semantics and absorb deletes/code changes naturally but can exceed time/cost/retention. Incremental builds reduce work while adding state, cursor, influence, idempotence, migration, and drift obligations.

**Source log cursor versus timestamp watermark.** Ordered source logs capture old-business-time updates/deletes and stable intervals, but require retention, source identity, and CDC operations. Timestamps are widely available but need overlap/identity and bounded-lateness risk.

**Append events versus current-state table.** Append preserves history/replay and makes occurrence identity visible. Current state serves simple queries but must resolve updates/deletes/order. Often retain append history and derive current state.

**Arithmetic adjustment versus affected-region recomputation.** Inverse updates can be efficient for sufficient/invertible state. Recomputing authoritative groups/windows is easier to reason about when before-images or nonadditive measures are involved.

**Row-key merge versus partition overwrite.** Merge targets entity keys and preserves unrelated rows but depends on unique match/transaction semantics. Partition overwrite can simplify replacement aggregates but needs exact affected scope and safe table commits. DE-036 compares mechanics.

**Fixed lookback versus change feed.** Lookback is simple and handles commonly bounded lateness with idempotent replacement. It offers no universal completeness and repeatedly scans history. CDC/source versions provide exact changes when configured/retained correctly.

**Eager update versus staged generation.** Direct update uses less temporary space and may be fast, while making validation/rollback/ambiguous retry harder. Isolated candidates/snapshots cost storage but separate computation from trust.

**Per-model versus shared extraction checkpoint.** Per-model progress isolates failures and consumer rates but duplicates retained changes. Shared checkpoints reduce duplication but couple model success/retention. Keep source capture durable and model checkpoints independent where practical.

**Exact influence versus conservative recomputation.** Precise key/column lineage minimizes work but is complex and can miss dynamic dependencies. Wider partition/group/full rebuild costs more and is safer when influence is uncertain.

**Immediate late correction versus finalized periods.** Continuous correction maximizes eventual accuracy and consumer churn. Finality stabilizes reports but needs explicit materiality, exception, restatement, and residual-risk policy.

**Hard delete versus tombstone/soft delete.** Hard removal simplifies current output and privacy deletion, but loses replay/version evidence unless held elsewhere. Tombstones preserve ordering/audit but require access, retention, and eventual cleanup policy.

**Automatic full-refresh cadence versus drift-triggered refresh.** Scheduled refresh bounds undetected drift at predictable cost. Drift-triggered repair is cheaper but depends on detection coverage. High-risk models often need both periodic and event-triggered checks.

## Failure Modes and Misconceptions

- **“Incremental means rows newer than target max time.”** Old-time corrections, deletes, nulls, ties, and partial writes violate that shortcut.
- **“`>` prevents duplicates.”** It can lose equal-position/timestamp records. Identity and exact cursor intervals govern replay.
- **“`>=` is safe.”** It reprocesses boundaries; only an idempotent transition makes overlap safe.
- **“Updated timestamps always change.”** Applications can omit updates, backdate, truncate, or move clocks. Verify source contract.
- **“Append delta is a change feed.”** It may exclude replace/overwrite/delete; inspect exact source/table API.
- **“No row means delete.”** Absence in a partial extract is not authoritative deletion evidence.
- **“Filter inactive rows before dedup.”** A newer tombstone/inactive version can be removed, resurrecting older state.
- **“Arrival order is source order.”** Networks, partitions, retries, and workers reorder delivery. Use source authority.
- **“Equal payload is a duplicate.”** Two legitimate occurrences can carry equal values. Deduplicate by occurrence identity.
- **“Unique key configuration creates uniqueness.”** Source/candidate/target keys must be nonnull and actually validated/enforced.
- **“A seven-day lookback handles late data.”** It handles only lateness within seven days and needs a policy beyond it.
- **“Only changed rows affect output.”** Joins, groups, dimensions, windows, and code changes expand influence.
- **“Destination pruning is harmless.”** It can hide an older matching target row and create a duplicate/unapplied update.
- **“Sum is always easy to increment.”** Updates/deletes/group changes need old contributions or recomputation.
- **“Min/max can be decremented.”** Deleting the current extremum requires more state or recomputing candidates.
- **“Schema synchronization backfills history.”** DDL alignment does not compute old derived values.
- **“New logic applies going forward.”** That produces mixed semantics unless explicitly versioned as the contract.
- **“Task success advances the checkpoint.”** Checkpoint and validated output generation must commit together logically.
- **“Timeout means rollback.”** Target/catalog may have committed. Read authoritative receipts before retry.
- **“One writer per partition eliminates conflicts.”** Global checkpoint/manifests/aggregates and backfills can still conflict.
- **“Full refresh should drop the table first.”** Build/validate an isolated generation and publish atomically.
- **“Incremental/full row counts match, so parity holds.”** Keys, values, deletes, nulls, schema, and slices may differ.
- **“Watermark proves completeness.”** It expresses source/runner progress assumptions and late-data policy, not universal finality.
- **“Tombstones can be discarded immediately.”** Older replay may resurrect state until retention/ordering boundaries permit GC.
- **“Incremental is always cheaper.”** State, repeated lookback, merges, fragmentation, compaction, tests, and operations can exceed a full build.

## Worked Examples

### Example 1

Two records share `updated_at=12:00`; a run uses `> 12:00` after processing only one before failure. The other is lost. An exact cursor/checkpoint remains at the prior committed log position, or timestamp-only extraction uses overlap plus stable occurrence identity and does not advance until candidate publication.

### Example 2

An order’s newest CDC event is a delete, delivered twice after connector recovery. Entity version and event identity make the first application install a tombstone and the duplicate a no-op. Filtering deletes before winner resolution would leave the older order active.

### Example 3

A customer moves from region A to B. A current-attribution revenue model must recompute all that customer’s joined facts, subtracting/replacing A and adding B. An as-of model may change nothing historically if valid-time records are correct. “Dimension changed” is incomplete without join semantics.

### Example 4

A late event for day 1 arrives at log position 900 on day 20. The cursor interval captures it even though its event timestamp is old. A target-max event-time predicate misses it. The model recomputes the affected day plus any downstream rolling-window influence.

### Example 5

A rolling seven-day output changes for source day 10. Outputs for days 10 through 16 can include that day under a trailing convention. The job reads sufficient context, recomputes those output days, and does not update day 10 alone.

### Example 6

An Iceberg Spark incremental read between snapshots returns appended data but the interval also contains an overwrite/delete. Current documentation says that read does not support those operations. The pipeline rejects the API as a complete change feed and uses a supported changelog/diff/full reconciliation route.

### Example 7

A destination merge scans only the last seven days for performance, but a corrected customer row already exists from a year ago. It is not found and another row is inserted. The fix proves match containment through a key index/layout or removes/widens destination pruning; source filtering remains separately complete.

### Example 8

A new derived column is added. The incremental schema option creates it for new rows, leaving old rows null. The migration builds a targeted/full candidate for history, compares schema and values, then publishes. Schema presence was not semantic backfill.

### Example 9

Two attempts start from generation 40/checkpoint 800 and produce candidates through 850 and 860. Candidate 850 commits first. Candidate 860 cannot compare-and-swap from expected 40/800; it must rebase from 41/850 and reapply `(850,860]`, not overwrite last.

### Example 10

Periodic full comparison finds equal total revenue but 12 missing keys and 12 extra keys. Key-level differences reveal a missed key-change delete/insert pair whose amounts offset. The team repairs state from raw CDC, republishes, and adds an old/new-key differential fixture.

## Cross-Program Connections

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies logs, snapshots, keys, transactions, isolation, replication, merge/update/delete, materialized views, and query plans. Incremental correctness depends on exact engine semantics.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects offsets, epochs, at-least-once delivery, idempotence, ordering, retries, ambiguous commits, compare-and-swap, and state-machine replication.

[Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) connects dynamic/incremental algorithms, dependency/influence propagation, sufficient statistics, inverse operations, sketches, and complexity trade-offs.

[Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) connects state transitions, event sourcing, immutable logs, pure functions, dependency/version management, migrations, and rollback.

[Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) connects differential tests, independent oracles, metamorphic replay, mutation tests, boundary analysis, drift monitoring, and evidence limits.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects requirements, configuration control, hazards, verification, lifecycle changes, capacity/retention, incident response, and recovery drills.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) connects durable checkpoints, orchestrators, table catalogs, isolated candidates, policy, observability, secrets, cost controls, and paved-road full refresh.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects CDC sensitivity, historical before-images, tombstone/retention conflicts, tenant scope, least privilege, audit, and checkpoint integrity.

## References

1. dbt Labs, [Configure incremental models](https://docs.getdbt.com/docs/build/incremental-models). Documents full versus incremental paths, source filters, unique keys, schema-change modes, and full refresh, including historical backfill limitations. Accessed 2026-09-02.
2. dbt Labs, [Incremental strategy](https://docs.getdbt.com/docs/build/incremental-strategy). Documents append, merge, delete-insert, insert-overwrite, and microbatch strategy availability and trade-offs by adapter. Accessed 2026-09-02.
3. Apache Iceberg, [Spark queries](https://iceberg.apache.org/docs/latest/spark-queries/#incremental-read). Documents snapshot/time-travel metadata and the current append-only scope/limitations of Spark incremental reads. Accessed 2026-09-02.
4. Apache Iceberg, [Reliability](https://iceberg.apache.org/docs/latest/reliability/). Describes snapshot file tracking, atomic metadata replacement, consistent reads, history/rollback, and optimistic concurrent writes. Accessed 2026-09-02.
5. Debezium, [PostgreSQL connector](https://debezium.io/documentation/reference/stable/connectors/postgresql.html). Documents snapshots/streaming, offsets, event envelopes, deletes/tombstones, key changes, schema, and duplicate delivery during recovery. Accessed 2026-09-02.
6. PostgreSQL Global Development Group, [Logical decoding concepts](https://www.postgresql.org/docs/current/logicaldecoding-explanation.html). Documents logical slots, ordered replay, crash-safe persistence, possible post-crash redelivery, and client progress responsibility. Accessed 2026-09-02.
7. Apache Beam, [Programming Guide](https://beam.apache.org/documentation/programming-guide/#watermarks-and-late-data). Documents event versus processing time, windows, watermarks, out-of-order/late data, triggers, allowed lateness, and state cleanup. Accessed 2026-09-02.
8. OpenLineage, [Object model](https://openlineage.io/docs/spec/object-model/). Defines Job, Run, Dataset, run events, dataset versions/facets, and input/output lineage useful for incremental generation evidence. Accessed 2026-09-02.
9. PostgreSQL Global Development Group, [Logical decoding output plugin callbacks](https://www.postgresql.org/docs/current/logicaldecoding-output-plugin.html). Documents begin/change/commit and optional transactional/logical-message callbacks that expose change-stream transaction boundaries. Accessed 2026-09-02.

## Exercises

### Exercise 1

An initial target has `o1=100`, `o2=200`, and `o3=300`, with maximum business event time 3 and source checkpoint 3. The next source-log interval contains `o1=150` at business time 1, delete `o2` at time 2, new `o4=50` at time 4, and `o3=250` at time 2. Compute the correct current state/total and the result/total of filtering only `event_time > 3`. Identify the violated invariant.

### Exercise 2

A timestamp-only source has records A and B at exact timestamp 10. A run writes A, fails before B, and target `max(updated_at)` is now 10. Compare the next run using `> 10` and `>= 10` with an append target. Design a safe fallback when no source log/snapshot cursor exists.

### Exercise 3

A trailing seven-day daily sum includes source days `[d-6,d]`. A correction changes source day 20. Which output days can change? What source context and output ownership are needed? Explain why recomputing only output day 20 is wrong.

### Exercise 4

Two incremental runs start from trusted pair `(generation=50,cursor=1000)`. Run A covers `(1000,1100]`; run B covers `(1000,1200]`. A publishes first. Design the conditional commit/rebase behavior for B and the evidence required after an ambiguous acknowledgement.

### Exercise 5

A model adds a normalized-country column, changes null handling, and upgrades its adapter. The target’s schema-change setting can add the new column without full refresh. Design a migration and differential-validation plan. State why schema success and matching row count are insufficient.

## Answers to the Exercises

### Answer 1

Cursor-aware application updates `o1` to 150, stores/acts on the `o2` tombstone, inserts `o4=50`, and updates `o3=250`. Visible state is `{o1:150,o3:250,o4:50}` and total 450.

Filtering on business time greater than 3 captures only `o4`. It leaves `{o1:100,o2:200,o3:300,o4:50}`, total 650. It violated complete change-interval/affected-state coverage by treating business event time as a monotone change-discovery cursor and by omitting deletes/old-time corrections.

### Answer 2

Using `> 10` skips both equal-time records on the next run, so B is permanently missing. Using `>= 10` selects A and B; appending produces duplicate A even though B is recovered. The operator alone cannot distinguish replay from new occurrence.

The fallback freezes immutable source listings/snapshots, uses a lookback starting before timestamp 10, retains stable occurrence/business identity, canonicalizes precision/time zone/nulls, deduplicates overlap or replaces the exact affected region, and advances a dedicated checkpoint only with publication. It records a maximum-lateness/repair policy and periodically reconciles/full-refreshes because a finite lookback cannot prove future completeness.

### Answer 3

Source day 20 contributes to outputs whose trailing interval contains 20: output days 20 through 26 inclusive. The recomputation reads at least source days 14 through 26 to calculate each affected seven-day frame under the declared boundaries, though optimized retained sufficient state may reduce reads if correct. It emits/replaces only outputs 20–26 and preserves context-only days’ ownership.

Recomputing output day 20 misses six later outputs whose windows still include the corrected value. Tests should place changes at the first/last included instant and compare the affected region against a full calculation.

### Answer 4

A conditionally commits `(generation=51,cursor=1100)` only if the current pair is still `(50,1000)`. B’s same precondition then fails; it must discard/reuse safe staged work as allowed, read generation 51, and compute/reconcile only `(1100,1200]` or rebuild its affected candidate from the new base. It then commits `(52,1200)` against expected `(51,1100)`. Last writer wins from the stale base is invalid.

After ambiguous acknowledgement, B reads the authoritative generation/cursor mapping, target snapshot/transaction/job status, immutable publication receipt keyed by run/candidate, and candidate manifest. If `(52,1200)` is committed it adopts success; if old pair remains it can retry idempotently; if state conflicts it stops/rebases. It never assumes timeout means rollback.

### Answer 5

Treat code/null semantics, output contract, adapter/runtime, and compiled operations as a new version. Freeze one source/reference cut and build the old full output, new full output, and new incremental transition from a trusted old baseline in isolated generations. Decide whether the semantic change intentionally rewrites history; for normalized country and null policy it usually does, so full or provably complete targeted recomputation is required.

Compare exact key multisets, columns/types/nullability, old/new country mappings including invalid/unknown cases, per-key values, null/domain distributions, joins, components/totals, both set differences, rejected rows, downstream questions, security, physical plan, scan/write behavior, and publication/rollback. Test empty/null/Unicode/case/whitespace/new-code cases and replay. Pin adapter/engine/runtime and inspect generated merge/DDL.

Adding the column does not populate historical values, and row-count equality cannot reveal null historical cells, changed mappings, duplicate keys, missed deletes, type changes, or offsetting value differences. Publish the validated new generation conditionally, reset/bind checkpoint to its source cut/version, retain rollback state, and rerun full differential checks after promotion.
