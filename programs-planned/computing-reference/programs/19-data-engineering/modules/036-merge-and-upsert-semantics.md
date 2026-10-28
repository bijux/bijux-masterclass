---
module_id: DE-036
program: Data Engineering
level: 1
module_number: 36
title: Merge and Upsert Semantics
status: complete
last_verified: 2026-09-02
---

# Merge and Upsert Semantics

## One-Page Review

### Governing question

What source, target, matching, winner, operation, concurrency, and publication contracts make a merge/upsert deterministic, replay-safe, and equivalent to the intended state transition?

### Essential definitions

- An **upsert** conditionally inserts a source candidate when its key is absent and updates an existing target row when the key conflicts or matches.
- A **merge** joins a bounded source relation to a target relation, classifies candidate rows, and applies ordered insert/update/delete/no-op clauses.
- The **target grain** states what one target occurrence represents; its **business key** identifies that entity within an explicit tenant/environment/domain.
- The **match predicate** determines source-target pairing. It is an identity relation only when its equality, null, collation, coercion, and scope rules match the target key contract.
- **source cardinality** is the number of source candidates that can attempt to affect one target row; **target cardinality** is the number of target rows one canonical source row can match.
- A **canonical source row** is the unique, deterministic winner for one target key after exact-duplicate removal and conflict resolution.
- A **source version** is a totally comparable value within a declared source/key epoch that prevents stale changes from overwriting newer state.
- A **tombstone** is versioned evidence that an entity is deleted; retaining it prevents stale replay from resurrecting the entity.
- A **clause partition** divides candidate rows into matched, source-only, and sometimes target-only populations, then selects at most one ordered action for each candidate.
- **full-snapshot absence** means a target key is authoritatively absent from a complete source scope; absence from a delta or filtered extract has no delete meaning.
- An **effect receipt** binds the canonical input, action, target commit/snapshot, and output evidence for replay and reconciliation.

### Central model, mechanism, or theorem

Let target state be a partial map $T:K\rightharpoonup V$, with a retained versioned record (including tombstones) for each governed key. Canonicalize source bag $S$ into at most one candidate $C(k)$ per key. For target record $t=T(k)$ and candidate $c=C(k)$, define a deterministic transition:

$$
U(t,c)=
\begin{cases}
c, & t\text{ absent};\\
c, & c.version>t.version;\\
t, & c.version<t.version;\\
t, & c.version=t.version\land digest(c)=digest(t);\\
\mathrm{error}, & c.version=t.version\land digest(c)\ne digest(t).
\end{cases}
$$

Visible state excludes winning tombstones, but deletion evidence remains in governed state. Under stable keys/versions, deterministic canonicalization, one canonical candidate per key, a physical target uniqueness invariant, atomic effects plus receipt/checkpoint, and sufficient concurrency control, replay is idempotent:

$$
U(U(T,C),C)=U(T,C).
$$

SQL syntax alone does not establish these premises.

### Critical invariants

- Source cut/scope, target generation, target grain, business key, tenant/environment namespace, and transformation/schema versions are explicit.
- Target key uniqueness is enforced physically or proved by a transactional equivalent; preexisting duplicate target rows fail validation.
- Source occurrences are deduplicated by occurrence identity, then reduced to at most one semantically justified candidate per target key.
- Equal source versions with unequal canonical payload/operation fail closed; an arbitrary row order is never called a winner policy.
- Matching uses deliberate null, type, normalization, collation, and key-change semantics and never broadens identity with mutable attributes.
- Clause populations and first-match ordering are mutually exclusive and complete for the intended insert/update/delete/no-op behavior.
- Deletes are explicit for deltas; target-only deletion is permitted only from a complete, authoritative, equivalently scoped snapshot.
- Older changes cannot regress current state or resurrect a tombstone; equal replay produces no new logical effect.
- Additive events merge by stable event/effect identity, not by overwriting an entity row or re-adding a replayed delta.
- Concurrency, isolation, constraint behavior, retries, triggers, defaults, and unknown commit outcomes are tested for the exact engine/version.
- Candidate state and action evidence validate before checkpoint/publication advances; downstream readers see one trusted generation.
- Key sets, multiplicities, operations, versions, deletes, rejected conflicts, values, and business controls reconcile independently of reported affected-row totals.

### Common failures

Common failures include using `MERGE` as a synonym for correctness; merging raw CDC with several changes per key; selecting a winner by nondeterministic row order; using `MAX(value)` instead of the latest whole record; silently breaking equal-version conflicts; allowing duplicate target keys; matching nullable keys with ordinary `=` and repeatedly inserting NULL keys; matching on mutable email/status; updating unconditionally so stale replay regresses state; dropping tombstones; interpreting absence from a delta as deletion; placing a catch-all clause before a special delete clause; using update-all/insert-all across schema drift; replaying `balance = balance + delta`; trusting affected-row count; reading a timeout as rollback; assuming statement atomicity also commits the orchestration checkpoint; ignoring triggers/defaults; pruning old target rows out of match consideration; and assuming identical syntax has identical behavior across engines.

### Compact example

Target state has `a@3=100`, `b@5=200`, and `c@2=300`. A replay-prone batch delivers `a@4=120` twice under the same event identity, stale `b@4=250`, `c@3=DELETE`, `d@1=40`, then `d@2=50`, and `e@1=DELETE`. Canonicalization yields one candidate per key. Version-aware merge updates `a`, ignores stale `b`, tombstones `c`, inserts `d@2`, and retains an `e` tombstone. Visible state is `a=120,b=200,d=50`. Replaying the batch changes nothing; attempting `a@4=999` fails as an equal-version conflict.

### Connections

[DE-026](026-database-change-data-capture.md) supplies versioned operations, [DE-027](027-idempotent-loads.md) defines replay-safe effects, [DE-028](028-deduplication-and-record-identity.md) separates occurrence and entity identity, [DE-030](030-designing-replayable-raw-ingestion.md) preserves repair evidence, and [DE-035](035-incremental-models.md) establishes full-equivalence and affected-set obligations. DE-037 next treats controlled backfills; DE-038 through DE-040 treat restatement, determinism, and batch testing.

## Governing Question

What exactly does one merge mean when duplicate deliveries, multiple source versions, deletes, nullable keys, concurrent writers, schema changes, engine differences, and ambiguous commits are all possible?

A merge is a state transition, not a magic verb. The same four words—`WHEN MATCHED THEN UPDATE`—can implement current-state replacement, a version-guarded projection, an unsafe additive effect, or an ambiguous choice among duplicate source rows. Correctness comes from the relations and rules surrounding the statement.

The central task is to turn a replay-prone source bag into a deterministic change function. That requires stable source identity, one governed target grain, exact match semantics, a winner policy, delete rules, version guards, clause precedence, a concurrency protocol, and publication evidence. Each must survive retries and engine upgrades.

Vendor behavior is part of the contract. PostgreSQL documents candidate classification and ordered first-true clauses, and warns that one target row should not join multiple source rows. BigQuery reports a runtime error when multiple source rows update/delete one target. Iceberg's Spark integration also requires no more than one source record to update a target row. Snowflake defaults to error for nondeterministic updating merges but can be configured to choose an undefined row. Portable pipelines therefore canonicalize and prove one-to-one matching before invoking any engine.

## Why This Matters

Most analytical current-state tables are rebuilt through repeated merges: customers, accounts, inventory, devices, subscriptions, order status, feature entities, dimensions, and serving projections. A subtle merge defect does not necessarily fail. It may retain a deleted customer, regress a status from shipped to pending, duplicate a nullable key, or select a different source version after a repartition.

Incremental savings increase the blast radius of bad assumptions. A full rebuild starts from all history and may reveal contradictory versions. A merge touches only selected target files or rows, so missed matches can persist indefinitely. A target-derived predicate can prune the old row that should match, causing an insert that violates uniqueness—or, without a constraint, a silent duplicate.

Retries make non-idempotent actions dangerous. Repeating `SET balance = balance + source.delta` applies the same event twice unless effect identity is separately claimed. Repeating `SET balance = source.absolute_balance` with a version guard can be idempotent. The SQL surface looks similar; the state model is different.

Deletes deserve equal treatment. A delete event can arrive late or be replayed. If deletion is represented only by physical absence, an older upsert may resurrect it. A versioned tombstone keeps the winning source version while excluding the entity from visible output. Retention of tombstones must cover the maximum replay/backfill horizon or be replaced by another authoritative history.

Concurrency converts read-then-write logic into races. Two workers can both observe an absent key, both insert, or one can overwrite a newer value selected by another. Unique constraints, conditional versions, appropriate isolation, retry of the whole transaction, and conditional dataset publication provide enforceable serialization points. A process lock or orchestrator status alone is not the target's truth.

Finally, merge affects physical systems. Row stores acquire locks and maintain indexes; table formats may rewrite data files and commit a new snapshot; warehouses scan/prune target regions and can consume large compute. Semantic predicates, physical pruning predicates, and commit protocols must remain distinct so performance tuning does not alter the set of possible matches.

## Prerequisites and Retrieval

Retrieve the source contract and authoritative cut; target owner, grain, key, uniqueness constraints, schema, partition/layout, and current duplicate profile; occurrence/event identity; entity/business key and namespace; source version/order domain and epoch; insert/update/delete/key-change representation; before/after images; full snapshot versus delta meaning; source duplicates and same-key version distribution; null/invalid key policy; canonical types, normalization, collation, and time precision; transformation and schema versions; expected clause populations; target engine/version; `MERGE`, `INSERT ... ON CONFLICT`, update, delete, and constraint semantics; transaction isolation; locks/conflicts/deadlocks; triggers, defaults, generated columns, foreign keys, and row-level security; statement/transaction retry behavior; target commit/snapshot identifiers; checkpoint/receipt store; affected partitions/files; pruning and statistics; concurrent ingestion/backfill/compaction; validation controls; rejected-event handling; lineage; access classification; retention; rollback; and recovery evidence.

Distinguish upsert from general merge; insert conflict from arbitrary join match; source occurrence ID from business key; exact redelivery from multiple legitimate versions; latest version from latest arrival time; maximum scalar value from the row with maximum version; business event time from source order; target row from target key; SQL equality from null-safe identity; null-safe equality from treating unknown identities as one entity; matched population from action condition; no-op from ignored stale/conflicting input; source-only from target-only; delta absence from full-snapshot absence; explicit delete from physical absence; tombstone from visible row; overwrite from additive change; atomic statement from atomic data-plus-checkpoint; affected-row count from exact effect set; one writer lease from database serialization; and logical row mutation from physical file rewrite.

Create a merge contract before SQL:

| Concern | Required decision and evidence |
|---|---|
| Source | Immutable cut/scope, occurrence identity, operation, source epoch/version/order, schema |
| Target | Grain, business key and namespace, physical uniqueness, existing duplicates, generation |
| Canonicalization | Exact duplicate rule, winner ordering, ties/conflicts, one candidate per key proof |
| Match | Key expressions, types/coercions, normalization/collation, NULL/invalid/key-change behavior |
| Actions | Ordered matched/source-only/target-only clauses and explicit unchanged/reject outcomes |
| Delete | Explicit delta tombstones, authoritative snapshot absence, retention and resurrection guard |
| Concurrency | Isolation, uniqueness/CAS, conflict class, whole-transaction retry, writer ownership |
| Publication | Candidate/transaction boundary, checkpoint/receipt coupling, commit/snapshot identity |
| Assurance | Source/canonical/action/target counts, key sets, versions, values, controls, full oracle |
| Operations | Scan/rewrite/lock cost, observability, security, rollback, rebuild, engine upgrade tests |

## Learning Objectives

After completing this module, you should be able to:

1. specify merge/upsert as a deterministic state transition over a governed target grain;
2. distinguish occurrence deduplication, per-key canonicalization, target matching, and clause selection;
3. prove source-to-target cardinality and enforce target uniqueness before mutation;
4. design explicit null, key normalization, key-change, version, conflict, and tombstone semantics;
5. separate current-state replacement from additive event application and full-snapshot synchronization;
6. write and review ordered insert/update/delete/no-op clauses without unreachable or overlapping intent;
7. make retries and concurrent writers converge using constraints, version guards, isolation, receipts, and conditional publication;
8. account for engine-specific SQL behavior and row-store versus table-format physical effects;
9. validate exact source, canonical, action, reject, and target invariants beyond row counts; and
10. operate merge workloads with measured cost, lineage, security, rollback, and recovery evidence.

## Core Exposition

### Define target grain before matching

State what one target row means. An `account_id` may be unique globally, within a tenant, within a source system, or within an effective-time interval. Omitting part of that namespace can make unrelated entities match. Adding mutable attributes such as email or status to the key can make one entity appear absent whenever the attribute changes.

Represent target uniqueness as a key function $k(t)$ and require

$$
\forall k,\quad |\{t\in T:k(t)=k\}|\le 1.
$$

Enforce this with a primary/unique constraint where the target supports it. In file/table systems without row constraints, validate key uniqueness in the candidate and committed snapshot and prevent concurrent publications from deriving from the same stale base. A preexisting duplicate target makes “the row to update” ambiguous; quarantine and repair it before normal merging.

Key normalization is semantic. Trimming, Unicode normalization, case folding, numeric coercion, collation, composite-field ordering, and tenant prefixing must be versioned and consistent on source and target. Changing the normalizer is a key migration, not merely a query refactor.

### Separate occurrence deduplication from key reduction

A source batch is a bag. It can contain exact redelivery of one event and several legitimate changes to one entity. First deduplicate exact occurrences using stable event identity plus canonical payload digest. If one identity appears with unequal payloads, fail closed.

Then reduce the remaining changes to the state required by the target. A current-state projection usually chooses the greatest source version per key. A valid total order might be `(source_epoch, entity_version, transaction_position, event_position)`, with explicit domain guarantees. Arrival time and worker order are not stable substitutes.

Do not write `ROW_NUMBER() OVER (PARTITION BY key ORDER BY updated_at DESC)` unless ties, nulls, time precision, and source authority are resolved. A hidden engine row identifier or arbitrary final tie-breaker makes execution repeatable only accidentally. Equal semantic versions with unequal payloads should normally be rejected as upstream contradiction, not resolved lexically.

Aggregation is not row selection. `GROUP BY key, MAX(version), MAX(value)` can combine the version from one source row with the value from another. Rank/select one entire canonical record, or compute a declared associative aggregate when the target itself is aggregate state.

### Model the candidate populations

For canonical source keys $K_S$ and unique target keys $K_T$, the basic populations are

$$
M=K_S\cap K_T,\qquad I=K_S\setminus K_T,\qquad A=K_T\setminus K_S.
$$

`MATCHED` candidates belong to $M$; source-only/`NOT MATCHED [BY TARGET]` candidates belong to $I$; target-only/`NOT MATCHED BY SOURCE` candidates belong to $A$. A general join predicate can produce more than these simple key populations, which is precisely why identity joins should be narrow and cardinality tested.

Not every candidate changes state. A matched source record can be stale, exact replay, equal-version conflict, authorized update, or delete. A source-only tombstone may need retention without a visible insert. A target-only row changes only if source scope is a complete authoritative snapshot and the synchronization contract says absence means deletion/expiration.

Most SQL implementations classify match status before action conditions, then evaluate clauses in written order and execute the first qualifying action. Put narrow exceptional clauses—such as authorized delete—before a catch-all update. Prove later clauses are reachable and the total set matches the contract.

### Make match semantics explicit

Ordinary SQL equality is three-valued: `NULL = NULL` is not TRUE. A nullable key merged with `t.key = s.key` can cause every replayed NULL source key to be treated as unmatched and inserted again. PostgreSQL documents `IS NOT DISTINCT FROM` as null-inclusive comparison; BigQuery gives an explicit null-safe pattern for merge conditions.

Null-safe matching is not always correct. If NULL means “unknown customer,” combining every unknown into one entity is false identity. Prefer rejecting/quarantining incomplete keys, deriving a stable surrogate from authoritative fields, or retaining event-grain rows. Decide null meaning before choosing an operator.

Avoid expressions that can match multiple target rows, such as ranges, fuzzy text, nonunique emails, or mutable attributes. If entity resolution is required, perform it as a separately governed probabilistic/decision process that emits a stable resolved identity and evidence. The mutation step should consume that identity, not hide resolution inside `MERGE ON`.

### Apply versioned state transitions

For current state, compare source and target versions inside the mutation condition, not only during batch canonicalization. A newer target may appear between source preparation and commit or may already exist from a previous batch. The target guard is the last defense against regression.

A robust policy is:

- source version greater than target: apply the complete new state or tombstone;
- source version less than target: retain target and record stale input;
- equal version and equal canonical operation/payload: no-op replay;
- equal version and unequal operation/payload: reject conflict;
- absent target: retain source winner, including a tombstone if replay protection requires it.

Comparison is meaningful only within a source/key epoch. If version counters reset after source recreation, add epoch to order and identity. If two independent masters assign incomparable versions, a scalar last-write-wins rule is not justified; use an authoritative sequencer, causal/conflict model, or route conflicts for resolution.

Hash/digest equality must cover semantic state: operation, relevant payload, schema/normalization version, and perhaps source identity. Exclude physical arrival metadata only deliberately. Canonicalize decimals, timestamps, Unicode, maps, nulls, and field order before hashing.

### Represent deletes and key changes

A delta needs explicit delete evidence. Apply a delete only if its source version wins. Retain `(key, version, deleted=true, source evidence)` until no allowed replay/backfill can contain an older change, or retain immutable history from which the tombstone can be reconstructed.

A primary-key change usually becomes a delete of the old key plus an insert/upsert of the new key, ideally within one source transaction envelope. Applying only the new key duplicates the entity; applying only the old-key delete loses it. Cross-key atomicity may require one transaction or one candidate generation rather than independent per-key commits.

`NOT MATCHED BY SOURCE THEN DELETE` is safe only when the source relation is a complete, authoritative snapshot over exactly the same key/tenant/filter scope. It is catastrophic when the source is a daily delta, one partition, one tenant, or a source query whose filter excludes valid target rows. Record completeness and scope evidence with the run.

Physical deletion and logical deletion serve different needs. Hard delete reduces current visible state but can erase replay guards and audit evidence. Soft delete retains state but requires every reader to filter correctly. A governed hidden tombstone/history table or table-format delete files may separate visible semantics from retention.

### Distinguish replacement from additive effects

Upserting absolute current state is naturally idempotent under versions: `balance = source.balance`. Applying a delta is not: `balance = balance + source.delta` repeats on retry. To ingest additive events, first claim stable event/effect identity in a ledger and derive balances from unique accepted events, or couple the increment and receipt in one transaction.

Do not collapse multiple additive source events to only the latest entity row. Each event may be legitimate. Conversely, do not add every CDC after-image; after-images replace state. Declare whether the source is event grain, state snapshots, patches, retractions, or commands.

Partial patch semantics need presence bits. A missing field can mean “leave unchanged,” whereas an explicit NULL can mean “set null.” `COALESCE(source.value,target.value)` destroys the ability to set NULL and quietly invents patch behavior. Carry field presence, or materialize complete after-state before merge.

### Design clause order as a decision table

Write a decision table before SQL. For each matched/source-only/target-only population, list operation, version comparison, payload equality, scope, and action. Make every accepted row land in exactly one action and every invalid combination land in a named reject.

Example logical order for matched rows:

1. newer explicit delete → tombstone/delete;
2. newer upsert → update complete governed fields;
3. older version → no-op stale;
4. equal version and equal digest → no-op replay;
5. equal version and unequal digest → reject/error;
6. unknown operation/schema → reject/error.

A catch-all `WHEN MATCHED THEN UPDATE` placed second makes the stale/conflict cases unreachable. Some engines reject syntactically unreachable later clauses; others execute first match and quietly mask them. Keep rejects in source staging when SQL cannot express fail-closed behavior atomically.

Use explicit target column lists. `UPDATE SET *`, `INSERT *`, or positional rows couple mutation to source/target column layouts, defaults, and schema evolution. Generated/audit columns, tenant keys, security labels, created timestamps, and source metadata often need different insert/update treatment.

### Treat constraints and triggers as semantics

Unique constraints provide the conflict arbiter for `INSERT ... ON CONFLICT` and close concurrent insert races. PostgreSQL documents an atomic insert-or-update outcome for `ON CONFLICT DO UPDATE` under its premises and disallows affecting the same existing row more than once within one statement. This does not canonicalize an invalid multi-row source for you.

Constraints, foreign keys, generated columns, row-level security, and triggers can transform or reject effects. A trigger can modify the proposed insert, emit an audit row, or cause later merge actions to encounter a changed target. Statement triggers may fire even when no row takes that action in some engines. Include their effects in the idempotence boundary and test exact engine behavior.

Defaults are evaluated by the target and may vary by attempt (`current_timestamp`, sequence values, random identifiers). If replay equivalence requires stable values, materialize them once in the canonical source or recover them from a receipt. Do not compare only business columns while silently duplicating external trigger effects.

### Govern concurrency and ambiguous outcomes

Two correct single-writer merges may be incorrect concurrently. Identify conflicts: same key, overlapping source interval, shared target partition/file, schema migration, compaction, or full-snapshot delete. Choose database isolation/locking or table-format optimistic commits that reject stale bases.

At serializable isolation, the engine may abort one transaction; retry the entire transaction from a newly read state, not just its final statement. At weaker isolation, validate whether unique constraints and per-row version predicates are sufficient for the named invariant. Test write skew across multiple keys when the business rule is broader than one row.

For snapshot tables, tasks may write new files while a catalog commit atomically publishes metadata. Conflict detection must cover files/partitions and source/target snapshot assumptions. Iceberg documents `MERGE INTO` as rewriting affected data files in an overwrite commit; logical one-row change can therefore conflict with compaction or another rewrite.

After timeout, read authoritative commit evidence: transaction/receipt, table snapshot, idempotency key, checkpoint-generation mapping, and candidate manifest. Never infer rollback from missing acknowledgement. Effects and receipt/checkpoint should commit together or through a recoverable conditional publication protocol.

### Separate semantic matching from pruning

The semantic match predicate defines identity. A physical pruning predicate limits target scan only when it cannot exclude a possible match. If source keys span dates or records can move partitions, pruning target to the source's newest date may hide older matching rows and convert updates into inserts.

Derive an affected key/partition set from canonical source and target layout. For immutable partition keys, a source partition bound may be safe. For mutable partition columns, both old and new locations may be affected; CDC before images or an index/key lookup is required. Measure plans, scanned bytes, rewritten files, lock duration, spill, and commit conflicts.

Do not add a predicate solely because it makes the plan faster. State and test the implication:

$$
match(t,s)\Rightarrow prunePredicate(t,s).
$$

If a legitimate match can violate the pruning predicate, optimization changes semantics.

### Validate before and after mutation

Pre-merge gates should prove immutable source cut, supported schema/operations, event identity consistency, non-null/valid governed keys, deterministic version order, equal-version payload consistency, one canonical row per key, and target uniqueness. Report exact duplicates, stale rows, conflicts, deletes, and affected scope.

Post-merge gates reconcile candidate actions to target effects. Compare exact key sets and versions for affected keys; visible/tombstoned state; inserted/updated/deleted/no-op/rejected identities; source and target digests; unchanged-region samples/controls; constraints; business totals/components; and full-rebuild differential results.

Affected-row totals are weak. One missing update and one extra insert can preserve total count. Engines differ in whether no-op updates count, how actions are reported, and what triggers add. Persist row/action-level evidence or key-level digests where feasible.

Publish only after gates pass. A failed mutable transaction should roll back as a whole. A file/table candidate should remain unreachable until one catalog pointer/snapshot commit. Bind the new target generation to source cut, canonicalization/version policy, code/schema/runtime, action manifest, review results, and checkpoint.

### Make portability an explicit test surface

`MERGE` implementations share vocabulary but not identical clauses, duplicate behavior, null guidance, concurrency, affected-row reporting, schema evolution, trigger semantics, or physical execution. `INSERT ... ON CONFLICT`, warehouse merge, and table-format merge are different mechanisms.

PostgreSQL forms candidates then evaluates ordered clauses; repeated modification of one target row can raise cardinality errors. BigQuery errors when multiple sources attempt updating/deleting one target. Snowflake documents a configuration that can permit an undefined source winner, so fail-on-nondeterminism must be pinned. Delta Lake tells users to preprocess duplicate source matches and notes source determinism concerns across merge passes in older releases. Iceberg Spark requires extensions for row-level SQL and rewrites affected files.

Pin engine, adapter, catalog/table-format, and configuration versions. Capture compiled SQL and plans. Run a conformance suite for duplicate source/target keys, null keys, clause ordering, stale/equal/new versions, update/delete conflict, full-snapshot absence, schema mismatch, triggers/defaults, concurrent writers, retry, ambiguous acknowledgement, partition movement, and affected-row evidence before upgrade.

### Operate the lifecycle

Observe delivered/unique/canonical counts; per-action and per-reject counts; stale/conflict/version-lag distributions; duplicate target keys; tombstone volume/age; source-to-publication lag; scanned/rewritten bytes/files; locks/deadlocks/serialization retries; catalog conflicts; duration/cost; validation drift; and checkpoint/rebuild horizon.

Alert on invariants, not generic failures only: any equal-version conflict, target duplicate, unsupported operation, retention gap, action-count mismatch, unexpected full-table rewrite, checkpoint without generation, or merge from an untrusted base. Quarantine invalid keys/records with protected raw evidence; do not silently skip and advance.

Restrict privileges to exact staging/source reads and target mutations. CDC payloads and tombstones may contain sensitive historical values. Protect staging, query logs, rejects, receipts, snapshots, and time travel; enforce tenant predicates in canonicalization and target constraints; audit manual overrides and backfills.

Retain raw input, canonical candidate, rejected conflicts, transformation/schema/config versions, target snapshots/history, action receipts, and validation reports through the longest replay, audit, correction, and recovery requirement. Drill rollback to prior snapshot and rebuild from raw history. A merge path that cannot be reconstructed is operationally stateful debt.

## Definitions and Notation

Let:

- $K$ be the governed target-key domain, including tenant/source namespace;
- $T_g$ be target state at committed generation $g$;
- $S_{(a,b]}$ be the delivered source bag for one immutable source interval/cut;
- $e=(eventId,key,version,op,payload,position)$ be one delivered change occurrence;
- $D(S)$ remove exact event redeliveries while rejecting reused identities with unequal content;
- $C(S):K\rightharpoonup E$ choose at most one whole-record candidate per target key;
- $U(T,C)$ be the versioned state transition;
- $V(T)$ be visible target state after filtering winning tombstones;
- $R$ be the receipt/action evidence bound to the commit; and
- $H(x)$ be a versioned canonical digest over semantic operation/payload.

The source-cardinality invariant is

$$
\forall k\in K,\quad |\{c\in C(S):c.key=k\}|\le 1.
$$

The target-cardinality invariant is

$$
\forall k\in K,\quad |\{t\in T_g:t.key=k\}|\le 1.
$$

These are separate. Canonical source cannot repair preexisting duplicate target rows; target uniqueness cannot choose between contradictory source versions.

For one-key current-state merge, define version relation $\prec$ only inside a named epoch/order domain. If $c.version\succ t.version$, $c$ wins whether it is an upsert or tombstone. If $c.version\prec t.version$, it is stale. Equal versions require semantic digest equality for replay; unequal digests are conflicts. This rule is deliberately not wall-clock last-write-wins.

Let action function $A(t,c)$ return one of `insert`, `update`, `tombstone`, `stale`, `replay`, or `conflict`. The action manifest should satisfy conservation:

$$
|C|=N_{insert}+N_{update}+N_{tombstone}+N_{stale}+N_{replay}+N_{conflict},
$$

where categories are mutually exclusive under the declared policy. If source-only tombstones are counted separately from inserts, define that vocabulary once and keep it consistent across metrics and receipts.

For a full-snapshot synchronization with complete key set $K_S$, target-only population $A=K_T\setminus K_S$ can produce deletes/expiry. For a delta, no such inference exists:

$$
k\notin K_{delta}\centernot\Rightarrow k\text{ deleted}.
$$

Publication is modeled as a conditional transition

$$
(T_g,checkpoint=a)\xrightarrow[expected=g]{candidate\ C,\ evidence\ R}(T_{g+1},checkpoint=b).
$$

If the expected base is no longer current, the commit must fail/rebase. If acknowledgement is unknown, read the authoritative generation/receipt before retry.

Use “deterministic” carefully. Deterministic source reduction means equal governed input and policy produce the same canonical candidates. Deterministic merge means candidate classification/action/outcome is invariant under permitted execution order. Idempotent replay means repeating an accepted logical interval has no additional logical effect. Serializable concurrency means concurrent transactions appear in some permitted serial order or abort. These properties support one another but are not synonyms.

## Mechanisms, Invariants, or Proof Structure

The reference mechanism has five boundaries.

1. Freeze source and target identities. Record source cut/epoch, target generation, schemas, code/runtime, key policy, and complete-versus-delta scope.
2. Normalize and validate occurrences. Canonicalize types and payloads, reject missing keys/versions/operations, deduplicate stable event IDs, and fail reused IDs with different content.
3. Canonicalize by target key. Sort by authoritative source version/order, choose the winning whole record, and fail semantically conflicting ties. Prove at most one candidate per key.
4. Apply candidates against a unique target using a version-aware action table. Stage actions, preserve tombstones, and produce exact receipts/rejects.
5. Validate and publish atomically/conditionally. Bind action evidence, target commit/snapshot, and source checkpoint; reconcile unknown outcomes from target truth.

For exact replay $C$, each winning candidate is equal-version/equal-digest after the first application. Thus the second application selects `replay` and retains target state. Stale candidates remain stale. Therefore $U(U(T,C),C)=U(T,C)$, assuming no external untracked effects and the same comparison/canonicalization policy.

For concurrency, suppose writers derive candidates $C_1,C_2$ from generation $g$. If both can publish unconditionally, later publication can erase the earlier writer's disjoint or newer effects. Conditional commit allows one transition from expected $g$; the other observes failure, reloads $T_{g+1}$, reapplies its version rules, revalidates, and attempts from the new base. Row-store constraints/version predicates provide a similar per-row serialization only when broader multi-row invariants do not require stronger isolation.

The executable below is a finite semantic model. It removes an exact delivery duplicate, chooses a whole-record winner for each key, rejects equal-version contradictions, applies explicit tombstones, ignores stale state, checks replay, and compares the result with one full-history reduction. It does not emulate SQL null/collation rules, isolation, locks, triggers, table-format files, schema evolution, or external effects.

<!-- bijux-verify: {"id":"versioned-merge-reference-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"delivered_rows=8\nunique_events=7\ncanonical_keys=5\nfirst_actions=(('a', 'update'), ('b', 'stale'), ('c', 'tombstone'), ('d', 'insert'), ('e', 'insert_tombstone'))\nvisible_rows=(('a', 4, 120), ('b', 5, 200), ('d', 2, 50))\ntombstones=(('c', 3), ('e', 1))\nreplay_stable=True\nfull_equivalent=True\nequal_version_conflict=True\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Change:
    event_id: str
    key: str
    version: int
    operation: str
    amount: int | None
    position: int

    def semantic(self):
        return (self.key, self.version, self.operation, self.amount)


def deduplicate(deliveries):
    by_event = {}
    for change in deliveries:
        previous = by_event.get(change.event_id)
        if previous is not None and previous.semantic() != change.semantic():
            raise ValueError("event identity reused with different semantics")
        by_event[change.event_id] = change
    return tuple(by_event[event_id] for event_id in sorted(by_event))


def canonicalize(changes):
    grouped = {}
    for change in changes:
        grouped.setdefault(change.key, []).append(change)
    winners = {}
    for key, candidates in grouped.items():
        greatest = max(change.version for change in candidates)
        tied = [change for change in candidates if change.version == greatest]
        semantics = {change.semantic() for change in tied}
        if len(semantics) != 1:
            raise ValueError("equal entity version has conflicting semantics")
        winners[key] = min(tied, key=lambda change: (change.position, change.event_id))
    return winners


def merge(target, candidates):
    state = dict(target)
    actions = []
    for key in sorted(candidates):
        source = candidates[key]
        current = state.get(key)
        if current is None:
            state[key] = source
            action = "insert_tombstone" if source.operation == "delete" else "insert"
        elif source.version > current.version:
            state[key] = source
            action = "tombstone" if source.operation == "delete" else "update"
        elif source.version < current.version:
            action = "stale"
        elif source.semantic() == current.semantic():
            action = "replay"
        else:
            raise ValueError("equal target version has conflicting semantics")
        actions.append((key, action))
    return state, tuple(actions)


initial = {
    "a": Change("base-a", "a", 3, "upsert", 100, 1),
    "b": Change("base-b", "b", 5, "upsert", 200, 2),
    "c": Change("base-c", "c", 2, "upsert", 300, 3),
}
deliveries = (
    Change("ev-a4", "a", 4, "upsert", 120, 10),
    Change("ev-a4", "a", 4, "upsert", 120, 10),
    Change("ev-b4", "b", 4, "upsert", 250, 11),
    Change("ev-c3", "c", 3, "delete", None, 12),
    Change("ev-d1", "d", 1, "upsert", 40, 13),
    Change("ev-d2", "d", 2, "upsert", 50, 14),
    Change("ev-e1", "e", 1, "delete", None, 15),
    Change("ev-d2-copy", "d", 2, "upsert", 50, 16),
)

unique = deduplicate(deliveries)
candidates = canonicalize(unique)
merged, actions = merge(initial, candidates)
replayed, _ = merge(merged, candidates)
full, _ = merge({}, canonicalize(tuple(initial.values()) + unique))
visible = tuple(
    (key, row.version, row.amount)
    for key, row in sorted(merged.items())
    if row.operation != "delete"
)
tombstones = tuple(
    (key, row.version)
    for key, row in sorted(merged.items())
    if row.operation == "delete"
)

try:
    merge(merged, {"a": Change("conflict", "a", 4, "upsert", 999, 17)})
    conflict = False
except ValueError:
    conflict = True

print(f"delivered_rows={len(deliveries)}")
print(f"unique_events={len(unique)}")
print(f"canonical_keys={len(candidates)}")
print(f"first_actions={actions}")
print(f"visible_rows={visible}")
print(f"tombstones={tombstones}")
print(f"replay_stable={replayed == merged}")
print(f"full_equivalent={full == merged}")
print(f"equal_version_conflict={conflict}")
```

Why the model works:

- exact replay of `ev-a4` is removed by event identity without erasing legitimate `d@1` and `d@2` versions;
- the two `d@2` occurrences have different event identities but equal semantic state, so they agree rather than conflict;
- `d@2` wins as one whole record; amount 50 is never paired with version 1;
- stale `b@4` cannot replace `b@5`;
- `c@3` and source-only `e@1` remain tombstones even though they are hidden from visible rows;
- replay meets equal-version/equal-semantic no-op conditions; and
- reconstruction from initial-history records plus the batch yields the same governed state.

The proof stops at the model boundary. In production, validate that source positions/versions really form the assumed order, database comparisons match canonical keys, target uniqueness holds under concurrency, receipts include trigger/external effects, and one committed dataset generation contains every action.

## Alternatives and Trade-Offs

| Strategy | Appropriate semantics | Main strength | Main risk or proof obligation |
|---|---|---|---|
| Append immutable events | Every accepted occurrence is history | Simple writes and replayable audit | Stable event identity; duplicates and retractions remain explicit |
| Insert-if-absent | First accepted identity wins | Naturally conditional | Conflict key must equal intended identity; later corrections need another mechanism |
| Versioned upsert | One current row/tombstone per key | Efficient current-state projection | Total version order, equal-version conflict rule, target uniqueness |
| General `MERGE` | Ordered insert/update/delete cases | Expresses several actions atomically in one statement | Cardinality, clause order, nulls, concurrency, and vendor semantics |
| Full-snapshot synchronize | Target should equal a complete source scope | Can remove target-only rows | Completeness/scope proof; accidental filtered-source deletion is severe |
| Partition replacement | Entire affected region can be recomputed | Avoids row-match complexity | Exact region ownership, context reads, atomic publication, concurrent overlap |
| Immutable generation rebuild | Full candidate can be staged | Strong validation and rollback boundary | Temporary capacity, runtime, publication/GC coordination |
| Event ledger plus derived state | Additive/retractable events | Exactly-once effect identity and auditable history | More storage and derivation complexity; ledger uniqueness/retention |
| Database `ON CONFLICT` | Conflict matches a supported unique arbiter | Strong concurrent insert/update primitive | Narrower than general merge; source duplicates, triggers, versions still governed |
| Application read-then-write | Almost never without transactional guard | Flexible code | Race between read/write, partial effects, ambiguous retry |

Prefer the simplest mechanism matching the state model. An append-only event ledger may be clearer than a complicated merge. Partition replacement may be safer when influence is naturally partition-bounded. A database upsert may be ideal for one-key current state. The choice follows semantics, not syntax availability.

Versioned last-writer-wins is not a universal conflict resolver. It intentionally discards losing concurrent states. Use it only when the version authority is legitimate and full replacement is the domain rule. Inventory increments, collaborative edits, multi-master commands, and financial postings often require ledgers, serializable commands, or domain-specific conflict handling.

Soft deletes simplify replay protection and audit but expand storage and require correct visibility filters. Hard deletes support minimization but must not violate legal holds, audit, correction, or stale-replay defense. Separate current serving state from restricted historical evidence when requirements differ.

Row-level merge can minimize logical changes but cause broad physical rewrites in file-backed tables. Partition replacement may scan/write more logically but produce simpler files and fewer equality-delete/read-amplification costs. Measure the selected engine rather than extrapolating row-store intuition.

## Failure Modes and Misconceptions

**“The source is sorted, so the last row wins.”** Distributed sort ties may be unordered, retries may repartition, and arrival is not source authority. Require a total semantic order and reject contradictory ties.

**“`DISTINCT` removes source duplicates.”** `DISTINCT` removes identical projected values, not reused event identities or multiple versions. It can erase legitimate occurrences and leave same-key conflicting rows.

**“Grouping with maxima reconstructs the latest row.”** Independent column maxima can create a record that never existed. Select the complete row carrying the greatest authoritative version.

**“The target constraint handles source cardinality.”** It may fail after expensive work or after different clauses compete; some systems choose undefined winners or insert duplicate unmatched sources when no constraint exists. Prove canonical cardinality first.

**“A unique business key cannot be NULL.”** The source or staging type may still admit NULL, normalization may create NULL/empty values, or the target constraint may treat nulls specially. Test target and match semantics explicitly.

**“Null-safe equality solves missing identity.”** It can merge all unknowns into one false entity. Null-safe comparison is correct only when NULL is itself one governed identity value.

**“Newer timestamp means newer source state.”** Clocks regress, precision ties, late records carry older business time, and upstream corrections may rewrite timestamps. Use source-native versions/order.

**“An upsert can apply deltas safely.”** Repeating `x=x+delta` repeats the effect. Claim event identity atomically or use absolute versioned state.

**“Delete means remove the row.”** Without versioned evidence, stale replay can resurrect it. Retain tombstone/history through the replay horizon.

**“Missing from source means deleted.”** Only a complete authoritative snapshot over the same scope supports that inference. A delta, filtered batch, or incomplete page does not.

**“Clause order is cosmetic.”** First-qualified action semantics makes order observable. A broad update can swallow a delete, stale, or conflict branch.

**“Update all keeps schemas synchronized.”** It can overwrite target-owned metadata, populate historical rows differently, depend on column names/order, or silently change after schema evolution.

**“One statement makes the whole pipeline atomic.”** Source checkpoint, external receipts, downstream publication, and messages may remain outside the transaction.

**“A timeout means merge failed.”** The target may have committed and lost the response. Reconcile authoritative transaction/snapshot/receipt state.

**“One writer means concurrency is irrelevant.”** Backfills, compaction, schema jobs, manual repair, retries, and failover can overlap. Enforce ownership or conflict checks at the target.

**“Affected-row count proves correctness.”** Counts do not prove identities, winner versions, delete state, or unchanged regions; no-op reporting differs across engines.

**“Partition pruning is harmless.”** Excluding an old matching row changes an update into an insert. Prove every possible match remains visible.

**“SQL `MERGE` is portable.”** Clause vocabulary overlaps; duplicate behavior, extensions, isolation, triggers, schema handling, and physical rewrite behavior do not.

## Worked Examples

### Example 1

Target contains `(customer=7, version=12, tier='gold')`. Source contains versions 13 silver, 14 platinum, and an exact redelivery of version 14 under the same event ID. Occurrence deduplication removes only redelivery; per-key reduction selects the complete version-14 record; target guard accepts 14 over 12. A later replay sees equal version and equal digest and changes nothing.

### Example 2

Source has `(k=9,v=21,status='active')` and `(k=9,v=21,status='closed')`. Choosing the lexically greatest status is deterministic computation but unjustified semantics. The batch fails as an equal-version contradiction, preserving both source events in quarantine. An upstream owner must establish correction authority or issue version 22.

### Example 3

A target has no unique constraint and already contains two rows for `email='a@example.test'`. One canonical source row matches both and updates both, violating one-entity grain. The correct precondition is a stable customer identifier plus uniqueness validation/constraint; email remains a mutable attribute.

### Example 4

Both source and target contain NULL `external_id`. With ordinary `=`, they do not match, so replay inserts another NULL row. With null-safe equality they match—but only correctly if NULL denotes one real governed entity. If it means unknown, the pipeline quarantines or uses occurrence grain instead of inventing identity.

### Example 5

A daily delta contains only customers changed today. `WHEN NOT MATCHED BY SOURCE THEN DELETE` would delete every unchanged customer. Target-only deletion is disabled. A monthly full snapshot may use it only after page/partition completeness, tenant scope, extract controls, and source cut are proven.

### Example 6

An account receives event `credit-88` for +10. Replaying an upsert clause `balance=balance+10` produces +20. A unique effect ledger keyed by `credit-88`, committed atomically with the balance change, makes the second attempt a receipt lookup/no-op. Alternatively, derive balance from the immutable unique ledger.

### Example 7

Two writers load `device=4`: A carries version 31 and B version 32. If B commits first, A's target predicate `source.version > target.version` rejects regression. If each overwrites from a copied snapshot and publishes unconditionally, A can erase B. Conditional snapshot commit/rebase is required even though row logic is correct.

### Example 8

A source key moves from region `west` to `east`, and region is a physical partition column. A correct change removes/tombstones the old west row and writes east. Pruning the target scan to east cannot discover the old row. The pipeline uses a stable non-region entity key plus before image/old partition and validates both affected partitions.

### Example 9

Clause order is `WHEN MATCHED THEN UPDATE`, followed by `WHEN MATCHED AND op='delete' THEN DELETE`. The delete clause is unreachable or rejected because the catch-all matched clause wins first. Reversing the order and adding explicit version/conflict staging implements intended semantics.

### Example 10

An Iceberg-backed merge changes 100 rows distributed through 20 data files. The logical action count is 100, but the engine rewrites affected files and commits a new snapshot. Acceptance records logical key/action evidence and physical added/removed files, snapshot ID, scan/write bytes, conflicts, and rollback ancestry; “100 rows affected” is not the publication proof.

## Cross-Program Connections

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies keys, uniqueness, null comparison, insert conflict, merge, transactions, isolation, locks, triggers, constraints, indexes, MVCC, and query plans.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects epochs, versions, ordering, at-least-once delivery, idempotence, compare-and-swap, retries, ambiguous commits, consensus, and conflicting concurrent writers.

[Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) connects stable sorting, equivalence relations, map reduction, total orders, conflict detection, hash canonicalization, and state-transition proofs.

[Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) connects repositories, units of work, optimistic concurrency, event sourcing, outbox/receipt patterns, decision tables, and explicit domain commands.

[Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) connects model-based testing, property tests, concurrency schedules, mutation tests, differential oracles, boundary analysis, and evidence limitations.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects requirements, interfaces, configuration control, failure modes, verification, lifecycle change, observability, recovery, and human overrides.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) connects managed database/table services, job orchestration, policy, conditional catalog commits, leases, secrets, cost controls, and paved-road recovery.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects tenant-bound keys, least-privilege DML, row policies, sensitive before/after images, deletion obligations, audit evidence, and tamper-resistant receipts.

## References

1. PostgreSQL Global Development Group, [INSERT](https://www.postgresql.org/docs/current/sql-insert.html). Documents conflict targets, unique-index inference, `ON CONFLICT` actions, atomic insert/update behavior, deterministic single-row effects, privileges, triggers, and `RETURNING`. Accessed 2026-09-02.
2. PostgreSQL Global Development Group, [MERGE](https://www.postgresql.org/docs/current/sql-merge.html). Documents candidate classification, ordered first-true clauses, insert/update/delete actions, repeated target-row effects, triggers, privileges, and result evidence. Accessed 2026-09-02.
3. PostgreSQL Global Development Group, [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html). Documents visibility, concurrent update behavior, serialization anomalies/failures, and whole-transaction retry requirements. Accessed 2026-09-02.
4. PostgreSQL Global Development Group, [Comparison Functions and Operators](https://www.postgresql.org/docs/current/functions-comparison.html). Documents three-valued comparison and `IS [NOT] DISTINCT FROM` behavior for nullable values. Accessed 2026-09-02.
5. Google Cloud, [Data Manipulation Language Statements in GoogleSQL](https://cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax). Documents BigQuery `MERGE` populations, ordered clauses, null-safe matching guidance, constant-false replacement, and multiple-source-row errors for updates/deletes. Accessed 2026-09-02.
6. Snowflake, [MERGE](https://docs.snowflake.com/en/sql-reference/sql/merge). Documents clause syntax/order, source duplicate insert behavior, nondeterministic update/delete cases, and `ERROR_ON_NONDETERMINISTIC_MERGE`. Accessed 2026-09-02.
7. Apache Iceberg, [Spark Writes](https://iceberg.apache.org/docs/latest/spark-writes/). Documents Spark extension requirements, `MERGE INTO` first-matching clauses, one-source-row-per-updated-target restriction, affected-file rewrites, overwrite commits, branches, and snapshot metrics. Accessed 2026-09-02.
8. Delta Lake, [Table Deletes, Updates, and Merges](https://docs.delta.io/delta-update/). Documents merge clause behavior, ambiguous multiple source matches, source preprocessing, schema validation/evolution, source determinism, deletes, and partition predicates. Accessed 2026-09-02.
9. dbt Labs, [Incremental Strategy](https://docs.getdbt.com/docs/build/incremental-strategy). Documents adapter-specific append, merge, delete-insert, insert-overwrite, and microbatch strategies plus unique-key and incremental-predicate configuration. Accessed 2026-09-02.

## Exercises

### Exercise 1

Target contains `x@5=40`, `y@7=80`, and `z@2=30`. A batch delivers `x@6=50`, exact redelivery of that event, `y@6=90`, `z@3=DELETE`, `n@1=20`, and `n@2=25`. Under the reference policy, derive unique-event count, canonical candidates, actions, visible final state, and replay outcome.

### Exercise 2

A source contains `(k=1,version=9,value=100)`, `(k=1,version=9,value=120)`, and `(k=1,version=8,value=999)`. Explain why `MAX(version),MAX(value)` and arbitrary `ROW_NUMBER` tie-breaking are wrong. Design a fail-closed canonicalization result and the evidence needed to resume.

### Exercise 3

A target contains one row with nullable business key NULL. A source replay contains another NULL-key row. Compare `t.key = s.key`, null-safe equality, and quarantine. State when each result would or would not satisfy the target grain.

### Exercise 4

A daily source delta has 2,000 changed customer keys; the target has 20 million active customers. Evaluate an unconditional `WHEN NOT MATCHED BY SOURCE THEN DELETE`. Then define the evidence under which target-only deletion would be valid for a full snapshot.

### Exercise 5

Two snapshot writers start from generation 40. Writer A merges `p@11` and publishes generation 41. Writer B has `p@12,q@1`, finishes later, and its commit acknowledgement times out. Design base-generation checks, rebase behavior, and unknown-outcome reconciliation. Include validation evidence beyond affected-row count.

## Answers to the Exercises

### Answer 1

There are six deliveries but five unique events after removing the exact `x@6` redelivery. Canonical candidates are `x@6=50`, `y@6=90`, `z@3=DELETE`, and `n@2=25`; `n@1` is a legitimate earlier version, not an occurrence duplicate, but it is not the current-state winner.

Actions are update `x` because 6>5, stale/no-op `y` because 6<7, tombstone `z` because 3>2, and insert `n@2`. Visible final state is `x@6=50`, `y@7=80`, `n@2=25`; retained deleted state includes `z@3`. Replaying the same canonical candidates yields equal-version/equal-payload no-ops for `x`, `z`, and `n`, while `y@6` remains stale, so governed and visible state are unchanged.

### Answer 2

Independent maxima yield `(version=9,value=999)`, a record that never existed: value 999 belongs to version 8. Ranking by version alone leaves the two version-9 rows tied, so an engine/partition-dependent row may win. Adding lexical value as a tie-breaker makes execution stable but invents an authority rule not supplied by the source.

Canonicalization must reject key 1 because equal authoritative version 9 has unequal semantic payloads. Preserve both event identities, raw payloads/digests, positions/transactions, schema and source epoch, source cut, and target generation in a conflict record. Do not advance the checkpoint past the conflict unless policy explicitly permits quarantined partial progress. Resume after the owner identifies one authoritative correction—commonly a new version 10—or supplies a governed conflict resolution whose policy/version becomes lineage.

### Answer 3

With ordinary equality, NULL does not match NULL; the source falls into the source-only population and may insert a second unknown-key row on every replay. This violates one-row-per-entity if both rows meant the same entity and violates a non-null key contract regardless.

Null-safe equality makes them match. That is correct only if NULL is explicitly one key value denoting the same governed entity. If NULL means unknown identity across potentially many entities, it falsely combines unrelated records. Quarantine is the safe choice for a required non-null entity key. If the desired target grain is events rather than entities, use a stable occurrence ID as key and retain nullable business key as an attribute.

### Answer 4

The daily delta omits roughly 19,998,000 unchanged active customers, so unconditional target-only deletion would remove them. Delta absence carries no state meaning; the clause must be disabled.

Deletion becomes valid only for a source proven complete and authoritative over exactly the target scope. Evidence includes immutable snapshot/cut ID, all expected pages/files/partitions and versions, source query/filter, tenant/environment boundaries, extraction and quarantine counts, schema/key rules, coverage reconciliation against source controls, no retention/page gap, target base generation, explicit source-absence deletion policy, protected exceptions, candidate delete key set, rollback snapshot, and conditional publication. A scoped snapshot may delete only within that proven scope.

### Answer 5

Both candidates must carry expected base 40. A's compare-and-swap succeeds and publishes 41. B's stale-base commit must not overwrite 41. It reloads generation 41, reapplies canonical candidates: `p@12` wins over A's `p@11`, and `q@1` is inserted; it revalidates a candidate for expected base 41 and conditionally publishes generation 42.

If B's generation-42 acknowledgement times out, it queries the authoritative current pointer/snapshot history and immutable receipt keyed by run/candidate digest. If 42 with B's candidate digest and checkpoint is committed, it adopts success; if 41 remains current and no receipt exists, it can retry the same conditional commit; if another generation is current, it rebases again. It never assumes timeout means rollback.

Validation includes exact canonical keys/versions/digests, action identities (`p` update, `q` insert), no equal-version conflicts or duplicate target keys, expected old/new values, source/candidate/action conservation, unchanged-key controls, target snapshot/file manifest, constraints, business components/totals, source cut, code/schema/runtime, checkpoint-generation binding, and replay/full-rebuild differential evidence—not merely a total of two affected rows.
