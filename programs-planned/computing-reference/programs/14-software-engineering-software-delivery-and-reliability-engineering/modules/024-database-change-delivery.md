---
module_id: SDRE-024
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 24
title: Database Change Delivery
status: complete
last_verified: 2026-09-06
---

# Database Change Delivery

## One-Page Review

### Governing question

How can a team change persistent schema and data while old and new application versions coexist, writes continue, and recovery remains honest?

### Essential definitions

- a **database migration** is a versioned transformation of schema, database code, reference data, or stored records;
- **schema version** identifies an intended structural state, while **data state** describes the records actually transformed;
- **expand–migrate–contract** first adds compatible structure, then moves traffic or data, then removes obsolete structure;
- **backward compatibility** means newer database state still serves an older live consumer;
- **forward compatibility** means a newer consumer can operate against an earlier supported database state;
- a **backfill** transforms existing rows after compatible structure exists;
- a **migration ledger** records migration identity, checksum, order, state, actor, and timestamps;
- **online DDL** is vendor-defined DDL intended to permit some concurrent work; it does not mean lock-free or risk-free;
- a **destructive change** removes or reinterprets data or an interface;
- a **compatibility window** is the period in which all live consumer/database pairs must work;
- **roll forward** applies a corrective migration; **rollback** restores a prior state only when its data semantics remain recoverable;
- **drift** is disagreement among declared migrations, ledger, schema, and effective database state.

### Central model, mechanism, or theorem

Let application versions live at time $t$ be $A_t$, database state be $D_t$, and $Compat(a,D)$ mean that application version $a$ can read and write safely against $D$. Delivery requires

$$
Safe(t)=\bigwedge_{a\in A_t} Compat(a,D_t)\land I(D_t)\land O(D_t)\land R(D_t),
$$

where $I$ is integrity, $O$ operational boundedness, and $R$ recoverability. For an incompatible rename, expand–migrate–contract preserves this predicate by adding the new field, making consumers tolerant, backfilling and reconciling, moving reads, stopping old writes, and only then dropping the old field.

### Critical invariants

- every production change is a uniquely identified, immutable, reviewed migration;
- the ledger checksum must match the reviewed migration; never edit an applied migration;
- every live application version is compatible with the current database state;
- schema, code, data transformation, constraints, indexes, and dependent consumers move in an explicit order;
- backfills are bounded, resumable, observable, retry-safe, and distinguish scanned from successfully transformed rows;
- dual writes have a declared authority and reconciliation rule; two independent sources of truth are forbidden;
- destructive contraction waits for proof that old reads and writes have ceased and recovery no longer needs the old representation;
- DDL lock, rewrite, log, replication, disk, and transaction behavior is verified for the exact engine and version;
- backups are not rollback unless restoration and lost-write consequences satisfy the recovery objective;
- failure, cancellation, retry, and operator takeover preserve evidence and a known state.

### Common failures

Common failures include running ad hoc SQL, editing an applied migration, deploying code that assumes a column before it exists, renaming or dropping in one release, adding a table-wide default that rewrites unexpectedly, calling vendor “online” DDL lock-free, doing an unbounded backfill in one transaction, dual-writing without reconciliation, adding a constraint before existing rows satisfy it, deleting the old field after observing only new reads, assuming transactional DDL exists everywhere, retrying a partially committed script blindly, and claiming code rollback can undo irreversible data changes.

### Compact example

To rename `customer.name` to `display_name`, first add nullable `display_name`. Deploy writers that update the authoritative old field and derive or dual-write the new field under a reconciliation rule. Backfill in bounded key ranges with checkpoints and compare values. Deploy readers that prefer the new field but tolerate the old. After telemetry proves every supported consumer stopped depending on `name`, enforce the new constraint, stop old writes, retain a recovery window, and finally drop `name` in a separate migration.

### Connections

[SDRE-023](023-configuration-and-secret-separation.md) supplies credential and configuration boundaries. [SDRE-025](../ROADMAP.md) uses compatible database state during blue-green deployment. [DBE-099](../../18-database-engineering/ROADMAP.md) owns engine-internal online schema and version upgrades; this module owns their delivery protocol.

## Governing Question

Application artifacts are replaceable; persistent state is cumulative. A failed binary rollout can often return to an earlier image. A migration may have deleted a column, reinterpreted values, emitted external effects, or transformed millions of rows while new writes continued. Its failure can leave a legitimate intermediate state rather than a clean “before” or “after.”

Database delivery therefore coordinates multiple interfaces over time: schema, application reads and writes, stored data, indexes, constraints, replicas, analytics, change-data capture, and operational recovery. The goal is not the slogan “zero downtime.” The goal is a bounded transition whose compatibility, resource impact, integrity, observation, and recovery claims are explicit.

## Why This Matters

Sadalage and Fowler's evolutionary database guidance treats schema, data, database code, and production fixes as version-controlled migrations with unique identity and an application ledger [1]. The practice makes database state reproducible and reviewable, but versioning alone does not make an operation safe under production size and concurrency.

Engine semantics matter. PostgreSQL 18 documents that many `ALTER TABLE` forms acquire `ACCESS EXCLUSIVE` unless a subform explicitly uses a weaker lock [2]. PostgreSQL's concurrent index creation avoids blocking ordinary writes but performs more work, takes longer, cannot run inside a transaction block, and can leave an invalid index after failure [3]. MySQL 8.4 documents that online DDL may still need exclusive metadata locks, can wait behind long transactions, consume temporary space, accumulate an online DML log, affect replication lag, and be expensive to roll back [4]. “Online” is a capability with conditions, not a portable guarantee.

Humble and Farley connect database changes to the deployment pipeline and emphasize small, automated, tested changes [5]. Kleppmann explains why evolving encodings and mixed-version readers and writers require compatibility reasoning [6]. Together these sources support treating the database interface as a versioned contract shared by concurrently live participants.

## Prerequisites and Retrieval

Retrieve transaction, atomicity, isolation, durability, schema, table, row, key, constraint, index, lock, metadata lock, MVCC, replication, log, checkpoint, backup, restore, idempotency, retry, application version, deployment, canary, rollback, feature flag, and observability.

From SDRE-017 retrieve explicit gate states, from SDRE-021 readiness versus deployment policy, from SDRE-022 immutable deployment subjects and compatibility windows, and from SDRE-023 typed configuration and narrow database credentials. Database Engineering owns relational correctness, storage, concurrency control, and engine internals. This chapter focuses on coordinating those mechanisms through delivery.

## Learning Objectives

After completing this module, you should be able to:

1. model a database change as schema, data, consumer, and operational transitions;
2. design immutable migrations and a trustworthy application ledger;
3. derive mixed-version compatibility requirements;
4. decompose an incompatible change with expand–migrate–contract;
5. design bounded, resumable, retry-safe backfills;
6. explain dual-write authority and reconciliation;
7. assess DDL locks, rewrites, disk, log, replica, and transaction risk;
8. stage indexes and constraints without overstating “online” behavior;
9. distinguish rollback, restore, compensating change, and roll forward;
10. test, observe, pause, resume, and audit database delivery.

## Core Exposition

**Treat migrations as product artifacts.** A migration has a stable identifier, immutable content, checksum, dependency or order, owner, purpose, supported source states, expected result, operational classification, preconditions, verification, pause and recovery rules, and compatibility contract. Review DDL and DML together with the application behavior they enable.

A migration runner records at least identifier, checksum, start and finish time, outcome, runner identity, engine identity, and error. It must acquire ownership so two deployers cannot apply the same migration concurrently. If an identifier is already complete with the same checksum, the runner reports that fact. If the checksum differs, it stops: modifying history makes environments with the “same version” structurally different.

Do not confuse runner idempotence with statement idempotence. `CREATE TABLE IF NOT EXISTS` may avoid an error while accepting a table with the wrong columns. A retry-safe migration examines exact postconditions and recognizes known intermediate states. Some transformations require checkpoints and compensation rather than a single idempotent statement.

**Model the compatibility window.** During a rolling, canary, or blue-green deployment, old and new application versions coexist. A schema change must serve every live reader and writer, including batch jobs, reporting tools, change-data-capture consumers, mobile clients that call indirect data APIs, and emergency rollback versions.

Construct a matrix with application versions as rows and database states as columns. Each cell states read compatibility, write compatibility, assumptions, and evidence. Promotion is permitted only when every cell that can occur operationally is safe. “Deploy database first” is valid only if old code tolerates the expanded state; “deploy code first” is valid only if new code tolerates the old state.

The database is not merely a private implementation when multiple applications query it directly. Inventory consumers through ownership records, query and connection telemetry, views, grants, code search, and interviews. Absence of observed traffic is not proof of absence; define observation duration and confidence.

**Expand before changing meaning.** Add compatible structure without removing the old contract. New columns are often nullable initially; new tables, views, indexes, and optional fields can coexist. Verify the engine's exact behavior: even syntactically small DDL may scan or rewrite a large table, acquire strong locks, generate substantial log volume, or block on old transactions.

Deploy tolerant application code next. Readers may prefer the new representation and fall back to the old. Writers need one declared authority. If the old representation remains authoritative, derive the new form from it. If dual write is necessary, define atomicity: one transaction when the database permits; otherwise an outbox, durable retry, or reconciliation process. Never assume two writes to different systems are atomic.

**Migrate existing data deliberately.** A backfill is production workload. Select a stable traversal key, bounded chunk size, transaction duration, rate limit, checkpoint, retry rule, and stop conditions. Measure rows selected, transformed, skipped, invalid, conflicted, retried, and remaining. Observe latency, lock waits, CPU, I/O, log growth, replica lag, cache churn, and downstream change streams.

Avoid offset pagination on a changing table; rows can shift or make later scans increasingly expensive. Prefer monotonic key ranges or a durable work queue, while accounting for late inserts and key gaps. Each update should guard its expected state so a retry does not overwrite a concurrent user change. A final reconciliation pass covers rows created or modified during the main scan.

Estimate before running. If $N$ rows require work, average sustainable transformation rate is $r$, duty-cycle fraction is $u$, and retry/overhead multiplier is $k\ge1$, estimated elapsed time is

$$
T\approx\frac{kN}{ur}.
$$

This is a planning estimate, not a completion guarantee. Validate it on representative distributions and update it from observed production rate. Storage growth includes new values, indexes, write-ahead or redo logs, temporary files, replicas, and backups—not just final table size.

**Move reads and prove convergence.** Once data is populated, deploy readers that use the new representation. Compare old and new results on bounded samples or every row when feasible. Define equivalence carefully: normalization, rounding, nulls, time zones, collations, duplicate semantics, and lossy conversions can make byte equality inappropriate.

Track reads and writes to the old field. Version-tag database clients or routes so telemetry can identify remaining consumers. A successful backfill proves historical rows were processed at a point in time; it does not prove all concurrent writes used the new path. Reconciliation plus consumer telemetry closes that gap.

**Contract only after the window closes.** Stop old writes, remove fallback reads, enforce new invariants, wait through the declared rollback and consumer window, archive evidence needed for recovery, and then remove old columns, triggers, views, indexes, code, and permissions in separate controlled changes.

Contraction is often the irreversible step. Its gate includes no supported consumer requiring the old interface, all data reconciled, new constraints valid, replicas healthy, restore implications understood, and an approved recovery strategy. Leaving compatibility scaffolding forever has cost and can create inconsistent sources, so track owner and removal criteria from expansion time.

**Stage constraints and indexes.** A new constraint changes which concurrent writes are legal. First make application writes conform, clean historical violations, and prevent new violations. Engines may support creating a constraint without scanning existing rows and validating later; semantics and lock levels are vendor-specific. Validation still consumes resources and can conflict with workload.

Index creation can read an entire table, sort data, use temporary space, generate logs, and delay replicas. PostgreSQL concurrent index builds can leave an invalid index that must be dropped or retried [3]. MySQL online DDL can fail after concurrent DML creates a value incompatible with the new definition [4]. Record exact command, algorithm, lock expectation, disk headroom, cancellation behavior, and cleanup.

**Separate schema work from long data work.** A short transactional DDL step and a hours-long backfill have different failure modes. Do not hold one giant transaction to make them appear atomic: it can retain locks and row versions, enlarge logs, delay cleanup and replicas, and create a catastrophic rollback. Establish compatible schema, commit it, then backfill with checkpoints.

Transactional DDL differs across engines and statements. Some operations implicitly commit; some cannot run in a transaction; distributed databases may expose asynchronous schema jobs. Test the exact engine version with representative size and concurrency. A migration framework cannot make unsupported atomicity appear.

**Choose recovery honestly.** Reversing `ADD COLUMN` may be easy before use; reversing a data-type conversion or merged field may be lossy. A down script is not proof of rollback. Classify changes as reversibly structural, recoverable from retained representation, compensatable, restore-required, or irreversible.

Code rollback is safe only when the old application remains compatible with current schema and data. Often the safest response is stop, correct, and roll forward while preserving the expanded representation. Restoring a database can lose writes after the recovery point and affect every tenant, so it is a disaster-recovery operation, not a routine migration undo.

**Control execution and evidence.** Before production, apply migrations from multiple supported starting versions to fresh and realistic restored copies. Test dirty historical data, maximum values, nulls, duplicates, invalid encodings, interrupted execution, lost runner, concurrent writers, replicas, cancellation, retry, and cleanup. Measure resource profiles instead of extrapolating only from row counts.

Production execution uses narrow credentials and separated duties. The application account usually should not alter schema. The controller records approval, artifact and migration checksums, database identity, preflight evidence, exact commands, timestamps, progress, resource signals, pause/resume decisions, verification, and final state without exposing data or credentials.

A safe controller can pause before a new chunk; killing an unknown DDL or transaction may make recovery worse. Define cancellation semantics and practice them. If observation is missing, stop expansion of impact. Manual intervention becomes a versioned migration or a recorded governed exception; it must not create invisible drift.

## Definitions and Notation

Let $M=(id,h,p,q)$ be a migration with identifier $id$, content checksum $h$, precondition $p$, and postcondition $q$. Let $L$ be the ledger. Applying $M$ is permitted only when its dependencies are complete, no conflicting owner exists, $p$ holds, and $L[id]$ is absent. If $L[id]$ exists with `complete` and checksum $h$, re-invocation is a no-op report. A different checksum is a history conflict.

Let $A_t$ be live application versions and $D_t$ database state. Let $Compat_R(a,D)$ and $Compat_W(a,D)$ be safe read and write compatibility. Then

$$
Compat(a,D)=Compat_R(a,D)\land Compat_W(a,D).
$$

Integrity $I(D)$ includes declared keys, constraints, and application invariants. Operational boundedness $O(D)$ includes lock, latency, capacity, log, and replica limits. Recoverability $R(D)$ is a tested path consistent with recovery objectives.

For a backfill, let $S$ be selected row identities and $C$, $F$, and $K$ be completed, failed, and skipped sets. Accounting requires disjoint terminal classifications and

$$
S=C\mathbin{\dot\cup}F\mathbin{\dot\cup}K.
$$

A row may be retried many times, but it must not disappear from final accounting.

## Mechanisms, Invariants, or Proof Structure

**Compatibility argument.** Direct rename changes the interface at once: old code requests the old field and new code requests the new. Unless deployment is perfectly atomic across all consumers, at least one reachable pair is incompatible. Expansion makes both names available, so consumers can move independently within a bounded window.

**Contraction argument.** Backfill completion alone does not authorize deletion because live old writers may recreate divergence. Contraction requires backfill completion, reconciliation after or alongside concurrent writes, and proof that old readers and writers have ceased.

**Ledger invariant.** Immutable checksum binding makes a completed identifier denote the same transformation content across environments. It does not prove the database reached the postcondition; the runner must verify $q$ and detect drift independently.

**Backfill accounting.** Checkpoints establish progress only if selection is stable and every selected identity reaches $C$, $F$, or $K$. A “last offset” over mutable ordering can skip rows, so stable key ranges and reconciliation are part of the invariant.

**Executable delivery model.** This model checks a three-state schema transition and mixed-version compatibility. It is intentionally a decision model, not SQL or an engine simulation.

<!-- bijux-verify: {"id":"database-change-delivery-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"old_on_old=True\nold_on_expanded=True\nnew_on_old=False\nnew_on_expanded=True\ncontract_before_old_retired=denied:live-consumer\ncontract_before_reconciled=denied:unreconciled-data\ncontract_when_ready=allowed\nretry_completed_migration=no-op:same-checksum\nchanged_applied_migration=denied:checksum-conflict\nbackfill_accounted=True\n","stderr":""}} -->
```python
compatibility = {
    ("old-app", "old-schema"),
    ("old-app", "expanded-schema"),
    ("new-app", "expanded-schema"),
    ("new-app", "contracted-schema"),
}

def compatible(app, schema):
    return (app, schema) in compatibility

def may_contract(live_apps, reconciled, old_writes):
    if "old-app" in live_apps:
        return "denied:live-consumer"
    if not reconciled:
        return "denied:unreconciled-data"
    if old_writes:
        return "denied:old-writes"
    return "allowed"

ledger = {"M024-expand": ("sha256:abc", "complete")}

def apply_migration(identifier, checksum):
    prior = ledger.get(identifier)
    if prior and prior == (checksum, "complete"):
        return "no-op:same-checksum"
    if prior and prior[0] != checksum:
        return "denied:checksum-conflict"
    return "allowed"

print(f"old_on_old={compatible('old-app', 'old-schema')}")
print(f"old_on_expanded={compatible('old-app', 'expanded-schema')}")
print(f"new_on_old={compatible('new-app', 'old-schema')}")
print(f"new_on_expanded={compatible('new-app', 'expanded-schema')}")
print(f"contract_before_old_retired={may_contract({'old-app', 'new-app'}, True, False)}")
print(f"contract_before_reconciled={may_contract({'new-app'}, False, False)}")
print(f"contract_when_ready={may_contract({'new-app'}, True, False)}")
print(f"retry_completed_migration={apply_migration('M024-expand', 'sha256:abc')}")
print(f"changed_applied_migration={apply_migration('M024-expand', 'sha256:def')}")
selected, complete, failed, skipped = 1000, 994, 2, 4
print(f"backfill_accounted={selected == complete + failed + skipped}")
```

## Alternatives and Trade-Offs

**Versioned migrations versus desired-schema diff.** Ordered migrations preserve intent and data transformations. Schema diff can detect structural divergence but may infer a dangerous operation or omit data semantics. Combine explicit transformations with drift comparison.

**Expand–contract versus coordinated outage.** Expansion preserves availability and mixed versions but creates temporary complexity. A maintenance outage may be safer for rare, tightly bounded systems if downtime and queued writes are acceptable and tested.

**Application dual write versus database trigger.** Application code is visible in service behavior but every writer must update. A trigger covers direct writers atomically in one database but hides work, affects latency, and must later be removed. Both need one authority and reconciliation.

**In-place DDL versus copy-and-swap.** In-place operations may use less space and preserve identity but have vendor-specific locks. Copy-and-swap offers controlled transformation and comparison but requires double storage, change capture, cutover, and dependency handling.

**Large transaction versus chunked backfill.** One transaction offers a simple atomic boundary but can create severe locks, logs, and rollback. Chunks bound impact and permit pause, at the cost of intermediate states and retry design.

**Rollback versus roll forward.** Rollback is attractive for reversible unused additions. Once new writes change meaning, a corrective forward migration usually preserves more data. Restore is reserved for recovery whose data-loss consequences are acceptable.

**Automatic versus supervised execution.** Automation gives repeatability and ledger discipline. High-risk operations benefit from accountable human checkpoints, but operators act through the same recorded controller rather than ad hoc terminals.

**Shared database versus owned interface.** Direct multi-application access increases compatibility windows and coordination. Service-owned data narrows consumers but does not remove evolution; APIs, events, replicas, and analytics still form contracts.

## Failure Modes and Misconceptions

- **“A migration tool makes the SQL safe.”** it sequences and records; engine and data behavior remain.
- **“Applied means correct.”** verify postconditions and effective schema.
- **“`IF NOT EXISTS` makes a migration idempotent.”** an existing object may have the wrong definition.
- **“Schema version describes all data.”** partial backfills and dirty rows matter.
- **“Deploy database first.”** only safe when old consumers tolerate the result.
- **“A rename is metadata-only.”** consumer compatibility still breaks, and engine behavior varies.
- **“Online means no locks.”** online DDL can wait for or acquire metadata locks.
- **“Nullable addition is free.”** defaults, indexes, catalogs, replicas, and versions can change cost.
- **“One transaction is safest.”** unbounded transactions can magnify resource and rollback risk.
- **“Backfill count equals correctness.”** concurrent writes, skipped rows, and semantic conversion remain.
- **“Dual write guarantees equality.”** partial failure and ordering create divergence.
- **“No observed old reads means none exist.”** telemetry has blind spots and sampling windows.
- **“A down migration proves rollback.”** deleted or transformed information may be unrecoverable.
- **“Restore is ordinary rollback.”** it may discard all writes after the restore point.
- **“Dropping old structure removes complexity.”** premature contraction removes recovery and breaks hidden consumers.
- **“Schemaless data needs no migration.”** readers and writers still impose an implicit schema.
- **“Replicas will catch up automatically.”** DDL and backfill can cause lag, storage pressure, or failure.
- **“Cancellation is harmless.”** an engine may leave invalid objects or spend substantial time rolling back.

## Worked Examples

### Example 1

**Add a required column.** An orders table needs `currency_code NOT NULL`. Adding it as required before old writers provide a value rejects their inserts. Expand with a nullable column, deploy writers that populate it, backfill and reconcile existing rows, validate allowed codes, then enforce `NOT NULL`. Conclusion: the constraint is the last proof-enforcing step, not the first syntax step.

### Example 2

**Build a compatibility matrix.** Old app reads `name`; new app reads `display_name`. Old schema has only `name`; expanded schema has both; contracted schema has only `display_name`. The reachable safe pairs are old/old, old/expanded, new/expanded, and new/contracted. New/old and old/contracted are unsafe. Conclusion: deploy expansion, then new code, then contraction.

### Example 3

**Estimate a backfill.** There are 48 million rows, observed sustainable rate is 4,000 rows/s, the job runs at duty cycle $u=0.5$, and overhead multiplier $k=1.2$. Then $T\approx1.2(48{,}000{,}000)/(0.5\cdot4{,}000)=28{,}800$ seconds, or eight hours. Conclusion: plan an eight-hour baseline plus uncertainty, not a one-transaction release step.

### Example 4

**Retry a partially completed chunk.** A worker updates rows only where `new_value IS NULL` and records the highest stable key after the transaction commits. It crashes before recording a later attempted chunk. Retrying that key range leaves already committed rows unchanged and processes the rest; reconciliation checks concurrent modifications. Conclusion: guarded updates and commit-aligned checkpoints make retry bounded.

### Example 5

**Reject offset pagination.** A backfill selects `ORDER BY id LIMIT 1000 OFFSET n` while rows are deleted. Deletion shifts later rows toward smaller offsets, so incrementing `n` can skip them. `WHERE id > checkpoint ORDER BY id LIMIT 1000` uses a stable monotonic boundary, followed by reconciliation for late changes. Conclusion: traversal semantics are part of correctness.

### Example 6

**Assess online index creation.** A PostgreSQL team chooses `CREATE INDEX CONCURRENTLY`. Ordinary writes may continue, but the operation takes multiple scans, waits on transactions, cannot run inside a transaction block, and failure can leave an invalid index. The plan includes disk headroom, lock and progress observation, invalid-index cleanup, and replica monitoring. Conclusion: concurrent creation changes trade-offs; it does not remove operational risk.

### Example 7

**Resolve a dual-write disagreement.** During a rename, one request writes old value `A`, then a retry writes new value `B` after a timeout. If both columns are peers, reconciliation cannot infer truth. Instead, define the old column as authority until cutover and deterministically derive the new value with a version marker. Conclusion: dual writes require authority and ordering, not only two assignments.

### Example 8

**Validate a new uniqueness rule.** Historical duplicates exist while the application begins preventing new duplicates. Creating a unique index immediately fails. The team first inventories and resolves historical conflicts under domain policy, prevents new violations, then builds and validates the index while observing concurrent writes. Conclusion: data repair and future-write control precede enforcement.

### Example 9

**Choose roll forward.** A migration converts cents to a decimal amount and new writes begin using fractional cents for internal allocation. The old integer representation cannot preserve that information. Rolling back code would misread new rows. The team halts rollout, fixes the new reader, and rolls forward while retaining raw evidence. Conclusion: irreversible semantics make a down script dishonest.

### Example 10

**Handle a lost migration runner.** The controller loses its network connection after sending DDL. It does not mark failure and rerun blindly. A new owner queries the engine and ledger, compares exact object state and checksum, verifies whether the postcondition holds, and either records completion, resumes a known engine job, or follows cleanup policy. Conclusion: uncertain execution is a state to reconcile, not permission to repeat.

## Cross-Program Connections

- **Database Engineering:** locks, logging, MVCC, constraints, indexes, recovery, and engine-specific DDL determine feasibility.
- **Software Architecture:** data ownership and consumer coupling determine compatibility-window size.
- **API Engineering:** expand–contract is parallel change applied to stored interfaces and external contracts.
- **Data Engineering:** change streams, backfills, late data, and downstream schemas extend migration impact.
- **Distributed Systems:** dual writes, retries, partial failure, ordering, leases, and reconciliation shape transitions.
- **Systems Engineering:** disk, memory, I/O, clocks, processes, signals, and cancellation affect operational safety.
- **Testing and Quality Engineering:** restored datasets, adversarial rows, fault injection, and compatibility matrices create evidence.
- **Platform Engineering:** controllers, credentials, policy, telemetry, and job orchestration implement governed execution.

## References

1. Pramod Sadalage and Martin Fowler, [“Evolutionary Database Design”](https://martinfowler.com/articles/evodb.html), May 2016; retrieved 2026-09-06. Used for version-controlled migrations, ledgers, small changes, collaboration, and mixed application versions.
2. PostgreSQL Global Development Group, [PostgreSQL 18 `ALTER TABLE`](https://www.postgresql.org/docs/18/sql-altertable.html), current major documentation retrieved 2026-09-06. Used for operation-specific lock and validation semantics.
3. PostgreSQL Global Development Group, [PostgreSQL 18 `CREATE INDEX`](https://www.postgresql.org/docs/18/sql-createindex.html), current major documentation retrieved 2026-09-06. Used for concurrent index-build scans, transaction restrictions, waits, and invalid-index failure state.
4. Oracle, [MySQL 8.4 Reference Manual: “Online DDL Limitations”](https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-limitations.html), retrieved 2026-09-06. Used for metadata locks, concurrent DML logs, temporary space, rollback, and replication limitations.
5. Jez Humble and David Farley, *Continuous Delivery*, Addison-Wesley, 2010, Chapters 5, 8, and 12. Used for deployment-pipeline, migration automation, and release coordination.
6. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, Chapter 4. Used for encoding evolution and backward/forward compatibility reasoning.
7. Scott Ambler and Pramod Sadalage, *Refactoring Databases: Evolutionary Database Design*, Addison-Wesley, 2006. Used for transition periods, schema refactorings, data migration, and dependent application changes.
8. PostgreSQL Global Development Group, [PostgreSQL 18 “Constraints”](https://www.postgresql.org/docs/18/ddl-constraints.html), current major documentation retrieved 2026-09-06. Used for relational constraint semantics; operational validation behavior remains command- and version-specific.

## Exercises

### Exercise 1

Define schema migration, data migration, compatibility window, backfill, and contraction. Explain why schema version alone cannot establish that a migration is complete.

### Exercise 2

A backfill has 90 million rows, rate 6,000 rows/s, duty cycle 0.4, and overhead multiplier 1.15. Compute the planning duration in hours. State two reasons actual completion may differ.

### Exercise 3

A runner finds ledger entry `M42` marked complete with checksum `abc`, but the repository file now hashes to `def`; a target column exists but has the wrong type. Diagnose the state and specify the safe response.

### Exercise 4

Compare an application dual-write transition with a database-trigger transition for renaming a shared field. Address atomicity, hidden consumers, observability, performance, ownership, rollback, and cleanup.

### Exercise 5

A globally replicated service must change an identifier from case-sensitive text to normalized case-insensitive form while accepting offline client writes for seven days. Design a safe transition, including collisions, mixed clients, replication, authority, reconciliation, and contraction criteria.

## Answers to the Exercises

### Answer 1

A schema migration changes structural objects or database code. A data migration transforms stored records or governed reference data. A compatibility window is the period during which every reachable live consumer/database pair must work. A backfill transforms existing records after compatible structure is available. Contraction removes obsolete interfaces after consumers and data converge. Schema version records intended ordered structure, but rows may be partially transformed, invalid, concurrently modified, or skipped; indexes or constraints may be invalid; replicas may lag; and consumers may still use old fields. Completion therefore requires postconditions, accounting, compatibility, and observation.

### Answer 2

Using $T\approx kN/(ur)$ gives $1.15(90{,}000{,}000)/(0.4\cdot6{,}000)=43{,}125$ seconds, which is $11.979\ldots$ hours, approximately 12 hours. Actual time can differ because row costs and data distribution vary, foreground load changes sustainable rate, retries exceed the multiplier, pauses or lock waits occur, replicas constrain throughput, or late writes require reconciliation. Any two well-explained mechanisms are acceptable.

### Answer 3

The checksum mismatch is an applied-history conflict: the same identifier no longer denotes the reviewed bytes. The wrong column type also proves the desired postcondition does not hold despite the ledger's complete state. Stop deployment; do not overwrite the ledger, edit production manually, or rerun uncertain SQL. Preserve evidence, identify when and where divergence occurred, compare all environments, and create a new uniquely identified corrective migration from the observed state after review. If repository history was edited accidentally, restore the original migration and retain the corrective migration. The ledger and schema must be reconciled through governed records.

### Answer 4

Application dual write keeps logic visible in service code and can tag versions, but every writer must upgrade and cross-system writes need an outbox or reconciliation. A database trigger covers direct writers and can update both columns atomically inside one database transaction, but it hides work from callers, adds write latency, complicates debugging and replication, and requires database-specific ownership. For a shared field with unknown direct writers, a temporary trigger may provide safer coverage while telemetry discovers consumers; define one authoritative field, instrument disagreements, backfill, move readers, stop old writes, and remove the trigger after the window. If all writes pass through one owned service, application logic is often clearer. Either design needs rollback compatibility and explicit cleanup.

### Answer 5

First define normalization and enumerate collisions by computing the normalized form without changing authority. Add a new nullable normalized identifier plus a stable immutable internal key; do not reinterpret the old primary identity in place. Establish collision policy—reject, merge only with domain authorization, or allocate disambiguators—and resolve existing collisions. New servers accept old and new client forms, write the original value for compatibility, and derive the normalized value under one versioned rule. Replicate both fields and version markers; backfill by stable key with regional checkpoints, then reconcile after at least the seven-day offline-write horizon plus measured replication delay. Route lookups through a compatibility layer that can detect ambiguity. Observe client-version reads and writes, collision and lag metrics, and equality under the normalization rule. Contract only when no supported offline client uses old semantics, every region and replica is reconciled, collision appeals are resolved, recovery no longer needs the old index, and rollback versions are retired. A strong answer must avoid treating lossy normalization or multi-region dual writes as automatically reversible.
