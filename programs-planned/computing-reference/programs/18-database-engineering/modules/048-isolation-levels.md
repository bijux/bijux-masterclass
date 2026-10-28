---
module_id: DBE-048
program: Database Engineering
level: 1
module_number: 48
title: Isolation Levels
status: complete
last_verified: 2026-08-30
---

# Isolation Levels

## One-Page Review

### Governing question

What concurrent histories may a transaction observe and commit under an isolation contract, and how can an engineer prove that those admitted histories preserve the application's invariants?

### Essential definitions

An **isolation level** is a contract restricting transaction histories, not a promise that transactions literally run alone. A **history** records operations, versions read, commit/abort outcomes, and relevant real-time order. A history is **serializable** when its committed effect and observations match some serial order of those transactions. **Strict serializability** additionally respects real-time precedence for nonoverlapping transactions. **Read committed**, **repeatable read**, and **serializable** are standardized names with minimum protections, but products may provide stronger behavior or different mechanisms. **Snapshot isolation** gives each transaction a stable committed snapshot plus its own writes and normally rejects overlapping writes to the same item; it can still admit **write skew**. An **anomaly** is a history forbidden by a named model or an application invariant, not merely an unexpected value.

### Central model, mechanism, or theorem

Model an isolation contract `I` by its admitted histories `H(I)`. A stronger contract admits a subset: `I_strong >= I_weak` when `H(I_strong) subseteq H(I_weak)`. The useful proof is compositional: specify each transaction's invariant-bearing reads and writes, identify the histories admitted by the actual engine/configuration/read type, and show that every admitted committed history refines a valid serial/application outcome. Serializability supplies this ordering property for participating transactions, but durability, constraint correctness, external side effects, authorization, and retry semantics remain separate obligations.

The classic SQL phenomena are useful tests, not a complete semantics. Preventing dirty reads, nonrepeatable reads, and phantoms does not by itself characterize every implementation or rule out write skew. Product names must be bound to engine, version, storage engine, database options, statement kind, and transaction scope.

### Critical invariants

- Every claim names the model and the complete observable history, including read-from versions and outcomes.
- The configured level is confirmed on the same session/transaction that executes the work.
- All invariant-bearing reads and writes share the intended transaction boundary and conflict domain.
- Snapshot and current/locking reads are not mixed without an explicit combined-view argument.
- A serialization/deadlock/write-conflict abort invalidates all results and external decisions from that attempt.
- Retry restarts the entire transaction function from fresh reads with a stable external operation identity.
- Native constraints remain authoritative for representable invariants; isolation is not a substitute for schema correctness.
- Tests force boundary schedules and compare them with serial and domain-specific oracles.

### Common failures

Failures include treating isolation names as portable behavior; assuming repeatable read means serializable; inferring a guarantee from MVCC alone; checking only final rows; ignoring predicates and absent rows; treating statement snapshots as transaction snapshots; mixing ordinary and locking reads accidentally; setting isolation after the transaction has acquired its snapshot; allowing one library call to escape onto another pooled connection; retrying only `COMMIT`; publishing side effects before successful commit; making retries non-idempotent; weakening isolation to cure contention without restating invariants; and claiming safety because a random load test found no anomaly.

### Compact example

Initially doctors A and B are both on call, and the invariant requires at least one. T1 and T2 read the same snapshot `(A=1,B=1)`. T1 sets A to 0; T2 sets B to 0. Their write sets are disjoint, so ordinary snapshot-isolation write-conflict checks can admit both. Final `(0,0)` violates the invariant. The read-write antidependencies form `T1->T2` and `T2->T1`, so no serial order explains both decisions. Serializable execution must prevent one commit or the application must materialize/lock an exact shared conflict.

### Connections

Retrieve [Read and Write Anomalies](042-read-and-write-anomalies.md), [Snapshot Visibility](047-snapshot-visibility.md), and [Transaction Boundaries](041-acid-and-transaction-boundaries.md). Continue through the Database Engineering [roadmap](../ROADMAP.md) to DBE-049, Serializable Snapshot Isolation, and DBE-050, Concurrency-Control Testing.

## Governing Question

How do we move from an isolation label on a connection to a defensible statement about every concurrent outcome an application may commit?

## Why This Matters

Isolation is where database theory becomes an application safety decision. A service may use perfectly atomic, durable transactions and still oversell inventory, schedule no doctor, allocate overlapping reservations, produce an incoherent report, or lose a logical update. These failures arise because each transaction is correct in isolation while their admitted interleaving is not correct together.

The label alone is insufficient. PostgreSQL 18 maps requested read uncommitted to read committed and implements repeatable read with transaction snapshots that exclude phantoms but can admit serialization anomalies. InnoDB 8.4 repeatable read gives ordinary consistent reads a transaction read view while locking reads and writes use current locking behavior; its documentation discourages mixing those table states. SQL Server can implement read committed using locks or statement-level row versioning depending on a database option, and exposes snapshot as a separate transaction-level mode. SQLite serializes writes but, in WAL mode, readers can hold snapshots and receive `SQLITE_BUSY_SNAPSHOT` when attempting an invalid promotion. These are not contradictions: standards specify important minimums, while engines choose distinct mechanisms and sometimes stronger guarantees.

Isolation also defines failure behavior. Strong execution may block, deadlock, reject a stale writer, or abort a dangerous dependency pattern. If the application swallows that outcome, retries only the final statement, duplicates an external charge, or uses results from an aborted attempt, the system-level contract is broken even though the database engine behaved correctly.

The engineering goal is therefore not “choose the strongest level everywhere.” It is to state the invariant, transaction program, conflict domain, admitted histories, and operational cost; choose mechanisms whose coverage proves the invariant; and verify that configuration, drivers, pools, replicas, and retries preserve that choice in production.

## Prerequisites and Retrieval

You should understand transaction boundaries, schedules, read/write sets, commit and abort, MVCC snapshots, locks and predicates, constraints, deadlocks, retries, and graph cycles. Retrieve dirty read/write, nonrepeatable read, phantom, lost update, read skew, write skew, `wr`/`ww`/`rw` dependency, serializability, snapshot visibility, current read, and idempotency.

DBE-042 classified anomalies and built history evidence. DBE-047 derived version visibility for one snapshot. This module organizes those behaviors into isolation contracts and selection proofs. DBE-049 will derive how serializable snapshot isolation detects dangerous dependency structures rather than merely using a stable snapshot.

## Learning Objectives

After this module, you can:

1. define isolation as a set of admitted transaction histories rather than a product label;
2. distinguish serializability, strict serializability, snapshot isolation, and the standard named levels;
3. explain why phenomenon tables provide minimum tests rather than complete product semantics;
4. derive dirty, nonrepeatable, phantom, lost-update, read-skew, and write-skew outcomes from versioned histories;
5. compare locking, statement-snapshot, transaction-snapshot, and dependency-validation implementations;
6. bind an isolation claim to engine, version, configuration, statement kind, connection, and transaction lifetime;
7. select isolation plus constraints/locks/atomic operations for a declared conflict domain;
8. design correct whole-transaction retry and external-side-effect boundaries;
9. build deterministic two-session tests with serial and invariant oracles; and
10. plan an isolation migration using correctness, abort, latency, retention, and capacity evidence.

## Core Exposition

**Begin with histories, not names.** Let a transaction be a program whose database operations include `r_i(x_j)`, meaning Ti reads version of x written by Tj; `w_i(x_i)`; predicate reads; and `c_i` or `a_i`. Include returned values when they affect later writes or externally visible decisions. A history without read-from versions or outcomes is often too weak to classify: the same final state can arise from a valid serial order, an overwritten update, or an aborted intermediate write.

For an isolation contract I, write `H(I)` for the histories it permits. If every history admitted by `I1` is also admitted by `I2`, then `I1` is at least as strong for those observables. This set inclusion is more precise than a single “weak-to-strong” marketing ladder. Two models may be incomparable when each restricts a behavior the other permits, and two implementations with the same label may differ while both meet a standard minimum.

**Serializability is an equivalence claim.** A committed concurrent history is serializable if there exists some total order of its committed transactions whose reads and effects match the history under the declared data model. The order need not equal start or commit time. Strict serializability adds real-time order: if T1 completes before T2 begins, T1 must precede T2. Database `SERIALIZABLE` commonly promises serializability for participating database transactions; do not silently promote that to strict serializability across replicas, clocks, caches, or external services without an explicit guarantee.

Serial execution is not automatically correct. A transaction can contain a wrong formula, omit a row, violate authorization, or call an external system unsafely. Serializability gives composition: if each transaction preserves invariant P when run against a P-valid state, and the successful concurrent history is equivalent to a serial order of those same transactions, then induction over that serial order preserves P. Assumptions include complete participation, correct transaction boundaries, deterministic interpretation of external inputs, and constraints that cover every write path.

**The standard names are minimum protection profiles.** A compact teaching table is:

| Requested level | Dirty read | Nonrepeatable read | Phantom | Serialization anomaly |
| --- | --- | --- | --- | --- |
| Read uncommitted | may occur | may occur | may occur | may occur |
| Read committed | prevented | may occur | may occur | may occur |
| Repeatable read | prevented | prevented | may occur under the minimum | may occur |
| Serializable | prevented | prevented | prevented | prevented |

“May occur” does not mean every compliant implementation must produce it. A product may collapse two levels, prevent additional phenomena, or distinguish snapshot from repeatable read. The classic dirty/nonrepeatable/phantom table also misses dirty write, intermediate read, lost update, read skew, write skew, and implementation-specific current-read behavior. Berenson and colleagues showed that ambiguous phenomenon definitions and lock-centric assumptions fail to characterize important multiversion levels; Adya later provided a dependency-based theory over histories.

**Read uncommitted is not a universal dirty-read switch.** The weakest name permits broad behavior under the minimum, but an MVCC engine may still refuse dirty reads because its architecture exposes only committed versions. PostgreSQL maps read uncommitted to read committed. SQLite says separate database connections see only complete committed transactions except shared-cache plus `PRAGMA read_uncommitted` conditions. Therefore, a test that fails to reproduce dirty read establishes only behavior for that engine/configuration/path; it does not redefine the requested level globally.

**Read committed usually scopes consistency to a statement, but mechanisms differ.** The central promise is no read of another transaction's uncommitted data. PostgreSQL ordinary `SELECT` gets a snapshot at command start, so successive statements may see different commits. Its modifying commands can wait on a concurrent updater and then re-evaluate their predicate against the updated row, producing behavior not captured by “one fixed snapshot per statement” alone. InnoDB read committed gives each consistent read a fresh snapshot and changes gap-lock behavior for searches. SQL Server read committed can use shared locks or, with `READ_COMMITTED_SNAPSHOT`, row-versioned statement snapshots. These choices affect blocking, versions, phantoms, and update races while satisfying the level's minimum.

Read committed is often correct for independent atomic statements. `UPDATE account SET balance=balance-10 WHERE id=? AND balance>=10` can combine decision and write under engine locking/constraint semantics. It is not generally correct to split a multirow decision across statements and assume the enclosing transaction makes them one snapshot. A report that reads header, detail, and total in separate statements may combine different committed moments.

**Repeatable read is especially nonportable.** Under a locking interpretation, retained read/range locks can prevent changes to revisited items or predicates, with blocking and deadlock consequences. Under transaction-snapshot MVCC, ordinary reads reuse a stable snapshot, avoid dirty/nonrepeatable reads, and often avoid phantoms as observed by those reads. Yet two transactions can read the same valid snapshot, write disjoint rows, and commit a write-skew invariant violation. PostgreSQL explicitly implements repeatable read as snapshot isolation and warns that the stable view need not correspond to a serial execution.

InnoDB 8.4 ordinary consistent reads at repeatable read use the snapshot established by the first such read, but locking reads, update, and delete use current index locking rules. A transaction that combines a historical ordinary SELECT with a current locking modification can observe a composite state that never existed as a single database snapshot. That may be intentional and correct, but only with an explicit proof. The phrase “all reads repeat” is too crude to describe this interface.

**Snapshot isolation is a model, not a synonym valid everywhere.** In the common first-committer-wins abstraction, transaction Ti reads a stable committed snapshot plus its own writes. If overlapping concurrent transactions write the same logical item, at most one commits. This prevents many dirty/intermediate/lost-write cases and gives coherent snapshot reads. It does not order conflicts created when Ti reads an item that Tj later writes while Tj reads a different item that Ti later writes. Those read-write antidependencies enable write skew.

The following finite executable history isolates that boundary. Both decisions are individually valid in the shared snapshot; write sets are disjoint; the final invariant fails; and the two antidependencies form a cycle.

<!-- bijux-verify: {"id":"snapshot-isolation-write-skew","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"snapshot_reads=(('T1', (1, 1)), ('T2', (1, 1)))\nsame_item_write_conflict=False\ncommitted=('T1', 'T2')\nfinal_state=(0, 0)\ninvariant_holds=False\nrw_edges=(('T1', 'T2'), ('T2', 'T1'))\nserialization_cycle=True\nevidence=finite_snapshot_write_skew_history\n","stderr":""}} -->
```python
initial = {"A": 1, "B": 1}
snapshot_reads = {"T1": (initial["A"], initial["B"]), "T2": (initial["A"], initial["B"])}
writes = {"T1": {"A": 0}, "T2": {"B": 0}}

same_item_write_conflict = bool(set(writes["T1"]) & set(writes["T2"]))
committed = ("T1", "T2") if not same_item_write_conflict else ("T1",)
final = dict(initial)
for transaction in committed:
    final.update(writes[transaction])

# T1 read old B before T2 wrote B; T2 read old A before T1 wrote A.
rw_edges = (("T1", "T2"), ("T2", "T1"))
serialization_cycle = all((right, left) in rw_edges for left, right in rw_edges)

print(f"snapshot_reads={tuple(sorted(snapshot_reads.items()))}")
print(f"same_item_write_conflict={same_item_write_conflict}")
print(f"committed={committed}")
print(f"final_state={(final['A'], final['B'])}")
print(f"invariant_holds={final['A'] + final['B'] >= 1}")
print(f"rw_edges={rw_edges}")
print(f"serialization_cycle={serialization_cycle}")
print("evidence=finite_snapshot_write_skew_history")
```

This program constructs one already-selected abstract history. It does not implement a database scheduler, prove every snapshot-isolation history, model predicate/version ordering completely, or empirically characterize a named engine. Its independent oracle is simple: in either serial order, the second doctor observes the first off call and must remain on call; final `(0,0)` is therefore impossible serially.

**Serializable implementations can lock or validate.** Strict two-phase locking can retain item and predicate/range locks until commit so conflicting transactions block and deadlock cycles are resolved by abort. Optimistic serializable systems can execute speculatively and validate read/write dependencies or timestamps before commit. Serializable snapshot isolation adds dependency tracking to snapshot execution and aborts dangerous structures. Deterministic ordering, certification, and distributed timestamp schemes provide other routes. The guarantee is the admitted-history property; blocking versus aborting is mechanism.

Serializable still requires retry. A serialization failure means the attempt did not commit, so every derived response, cache update, message, file write, or payment action must be withheld, made transactional, or protected by a stable idempotency/outbox protocol. Retry from the transaction function's beginning: reacquire a connection, set/verify isolation at the allowed point, begin, reread state, recompute, rewrite, and commit. Retrying only `COMMIT` cannot make stale decisions fresh. Retries require a deadline, attempt bound, jitter/backoff appropriate to contention, and a clear exhausted result.

**Constraints and atomic operations remain first-class.** A unique index is usually a more direct proof of uniqueness than relying on every caller's isolation discipline. A check constraint protects one row's representable relation; a foreign key protects referenced existence under its documented semantics; exclusion/range constraints can represent some nonoverlap rules. Conditional update or compare-and-set can protect an entity version. A materialized guard row can turn a broad predicate into a shared write conflict. Isolation and constraints compose: serializable handles dynamic intertransaction dependencies, while constraints protect all admitted write paths and implementation mistakes.

Coverage is the hard part. Row locks cover rows locked, not necessarily absent future rows. A predicate such as “no overlapping reservation” includes gaps and all indexes/partitions through which qualifying records can enter. A quota over shards includes every contributing shard or an authoritative aggregate. A replica read, cache lookup, sequence, trigger, background job, or external service can fall outside the transaction's serializable domain. Draw the conflict domain before choosing the mechanism.

**Configuration is executable semantics.** Record engine and exact version; storage engine/table type; database and session isolation settings; row-versioning or snapshot options; autocommit; transaction read-only/deferrable flags; statement lock hints; replica/read-routing policy; and when the snapshot is acquired. Check what a framework actually sends. Pool initialization can be lost when a different connection is leased; a nested transaction may be a savepoint; an ORM may issue preliminary reads before the requested isolation is set; DDL may commit implicitly or be restricted.

At runtime, expose transaction class, isolation setting, attempt count, SQLSTATE/vendor code, deadlock/serialization/write-conflict counts, lock wait, snapshot age, version-store/undo pressure, and latency. Avoid logging sensitive row values or full SQL parameters. Results from a replica need the replica's own consistency contract; primary serializability cannot be inferred through an asynchronously stale read path.

**Testing must force histories.** Use two or more independent database connections and explicit barriers, not sleeps. Seed a known state, begin with verified isolation, pause after both decision reads, release writes/commits in a selected order, and record versions/results/errors/final state. A prevention test passes if the engine blocks then observes safe state, aborts an attempt with the expected class, or a constraint rejects the unsafe write. Treat a timeout as harness evidence, not a correctness proof, unless the expected block and release are controlled.

Test dirty read, nonrepeatable read, phantom/predicate insert, lost update, read skew, write skew, and write-write conflict separately. Include the application invariant and serial reference result. Then test the production transaction function including retry, pool behavior, side-effect boundary, cancellation, ambiguous connection loss, and exhausted attempts. Random stress and history checkers add evidence but do not replace deterministic boundary schedules or formal reasoning.

**Selection is per transaction class.** Inventory a workload as transaction programs, not endpoints alone. A read-only live dashboard may intentionally use fresh statement snapshots; a coherent financial report needs one transaction snapshot or stronger; a single counter increment may use atomic DML; a conditional document edit may use versioned compare-and-set; an appointment allocator may need an exclusion constraint, range/guard locking, or serializable retry. Mixed isolation can be correct when interactions are proved—serializable transactions cannot protect an invariant from another writer that bypasses the protocol.

Evaluate correctness first, then throughput, blocking, abort probability, retry amplification, deadlocks, version retention, memory/disk, connection occupancy, tail latency, and operability. Stronger isolation sometimes improves design simplicity and can outperform widespread explicit locks; sometimes an exact constraint or atomic statement is both stronger for one invariant and cheaper. Benchmark the actual transaction mix and preserve a correctness oracle during migration.

## Definitions and Notation

- `Ti`: transaction i; `r_i(x_j)` means Ti reads x's version written by Tj.
- `w_i(x_i)`, `c_i`, `a_i`: Ti writes x, commits, or aborts.
- `H(I)`: histories admitted by isolation contract I for declared observables.
- **Dirty read/write:** reading or overwriting another transaction's uncommitted effect.
- **Nonrepeatable read:** two reads of one logical item return different committed versions due to concurrency.
- **Phantom:** a repeated predicate returns changed membership due to concurrent committed changes.
- **Lost update:** committed logical read-modify-write effects are absent relative to the transaction program's serial semantics.
- **Read skew:** one required coherent observation combines versions that do not belong to an allowed snapshot.
- **Write skew:** transactions read overlapping constraint state, write disjoint items, and jointly violate serializability or an invariant.
- `wr`, `ww`, `rw`: write-read, write-write, and read-write-antidependency edges under a stated single/multiversion model.
- **Serialization graph:** transactions as vertices and dependencies as directed edges; the applicable cycle theorem depends on the model.
- **Snapshot isolation (SI):** stable committed transaction snapshot plus own writes and a concurrent same-item write-conflict rule in the teaching abstraction.
- **Strict serializability:** serializability plus real-time precedence of nonoverlapping transactions.
- **Conflict domain:** all present, absent, predicate, metadata, and external state through which concurrency can affect an invariant.

## Mechanisms, Invariants, or Proof Structure

For invariant P and transaction programs `T1...Tn`, the serializable composition proof has four steps. First, prove each Ti maps any P-valid state to a P-valid state when executed serially and successfully. Second, require every invariant-bearing operation to participate in the same serializable domain. Third, rely only on committed histories equivalent to some serial order. Fourth, use induction: P holds initially; the first serial transaction preserves P; therefore each successor receives a P-valid state and preserves it. Aborted attempts contribute no database effects and no trusted external observations.

The proof fails if a transaction omits part of the conflict domain, a nonparticipating writer bypasses the level, an external effect escapes before commit, or the implementation's actual contract is weaker than assumed. Strict real-time claims require an additional premise. Domain constraints may be easier to prove directly and should remain as defense in depth.

For the doctor history, T1 reads B's old on-call value before T2 writes B off, yielding `rw T1->T2`; T2 reads A's old value before T1 writes A off, yielding `rw T2->T1`. The cycle refutes serializability in the relevant multiversion dependency model. Independently, both possible serial orders preserve one doctor: the second transaction must see the first off. Two separate oracles reduce the chance of repeating one modeling error.

Strength comparisons must preserve observables. Preventing the three classic read phenomena is not sufficient to infer serializability because the SI write-skew history has stable committed reads and disjoint writes. Conversely, a product that blocks a particular test has not proved a global isolation level; plan choice, predicates, index coverage, and timing may change the schedule.

## Alternatives and Trade-Offs

- **Locking read committed:** avoids dirty reads with short shared locks; can block readers/writers and allows statement-to-statement change.
- **Row-versioned read committed:** gives nonblocking statement snapshots; retains versions and still allows cross-statement skew.
- **Locking repeatable read:** retained item/range locks can prevent revisits/phantoms; increases blocking, lock memory, and deadlock exposure.
- **Transaction-snapshot repeatable read/SI:** stable nonblocking reads and good read/write concurrency; version retention and write skew require explicit treatment.
- **Serializable locking:** direct conflict prevention and mature reasoning; blocking, deadlocks, and broad predicate locks can reduce concurrency.
- **Optimistic/SSI serializable:** preserves speculative concurrency and aborts unsafe histories; dependency memory, false-positive aborts, retry load, and starvation need control.
- **Constraint/atomic DML/CAS:** often minimal and exact for representable local invariants; does not automatically cover multirow predicates or external state.
- **Guard/range locking:** materializes or locks a broad conflict domain; clear proof but possible hotspots and ordering complexity.
- **Weaker isolation with application merge:** can retain availability/concurrency for commutative or explicitly reconciled data; requires a domain algebra and cannot silently repair noncommutative safety rules.

## Failure Modes and Misconceptions

- “The four names form one portable ladder.” They are minimum labels; implementations, read kinds, and configurations differ.
- “MVCC means snapshot isolation.” MVCC is a versioning mechanism used for several isolation contracts.
- “Repeatable read means every operation sees one state.” Current/locking writes may follow different rules from ordinary consistent reads.
- “No dirty/nonrepeatable/phantom read means serializable.” Write skew is the standard counterexample.
- “No same-row writes means no conflict.” Predicates and multirow invariants create read-write antidependencies.
- “Serializable means no errors.” Correct prevention commonly appears as blocking, deadlock resolution, or serialization abort.
- “Retry commit.” The entire decision transaction must restart from fresh reads.
- “A transaction can send the email before commit.” An abort then leaves an irreversible effect for an uncommitted attempt.
- “The ORM default is documented by the database manual.” Driver, framework, pool, and managed-service defaults are independent configuration surfaces.
- “Setting a session variable once configures the pool.” Later work may lease a different or reset connection.
- “A production timeout proves the unsafe history is impossible.” It may reflect incidental blocking, resource exhaustion, or a broken harness.
- “Stronger is always slower.” Workload, indexes, contention, retries, explicit locks, and implementation determine cost.

## Worked Examples

### Example 1

T1 writes price 12 but has not committed; T2 reads 12; T1 aborts. The read has no committed source. Conclusion: dirty read is possible only if the actual path exposes uncommitted data; requesting read uncommitted does not prove that a particular engine will do so.

### Example 2

At read committed, T1 reads balance 50; T2 commits balance 40; T1's next ordinary statement reads 40. Both values are committed and each statement may be internally consistent. Conclusion: this is a nonrepeatable read across statement snapshots, not a dirty read.

### Example 3

T1 counts reservations for room R and gets zero. T2 inserts an overlapping reservation and commits. T1 repeats and gets one. Locking only rows returned by the first query protects nothing because the relevant set was empty. Conclusion: phantom safety requires predicate/range coverage, a materialized guard, an exact exclusion constraint, or serializable validation.

### Example 4

Two clients read document version 7 and each replace the whole row. If the engine serializes writes but the second update re-evaluates against the current row without a version predicate, one edit can be overwritten according to statement semantics. Conclusion: use atomic field operations, `WHERE version=7` compare-and-set with merge/reject, a lock before the read, or a serializable transaction whose full program is retried.

### Example 5

A read committed report reads account A before a transfer and B after it, returning total 110 although every committed state totals 100. Conclusion: no individual dirty value exists; the report needs a common transaction snapshot or another coherent reporting design.

### Example 6

Under the finite SI doctor history, both transactions see `(1,1)`, write disjoint rows, and commit `(0,0)`. Same-item first-committer-wins finds no conflict, but two `rw` edges form a cycle. Conclusion: stable snapshots and write-write conflict prevention do not imply serializability.

### Example 7

SQL Server read committed is tested in two databases: one has `READ_COMMITTED_SNAPSHOT` off and readers block behind writers; the other has it on and readers use earlier committed row versions. Both avoid dirty reads. Conclusion: isolation label, database option, and observed blocking must be recorded separately.

### Example 8

An application starts a transaction, performs a query, and only then asks the driver for repeatable read. The engine rejects or defers the change because the transaction's semantics are already established. Conclusion: set and verify isolation at the documented boundary, ideally through a tested transaction API.

### Example 9

Serializable T1 receives SQLSTATE `40001`; the handler retries only its insert while retaining a quota value read by the aborted attempt. The retry commits a stale decision. Conclusion: the retry unit is the whole transaction function, including all invariant-bearing reads and writes.

### Example 10

A service migrates appointment allocation from read committed to serializable. Invariant breaches disappear in forced schedules, but hot-key aborts drive p99 beyond the SLO. Adding an exact nonoverlap constraint and partitioning conflict domains reduces unnecessary overlap while retaining whole-transaction retry. Conclusion: correctness is the gate; schema and workload design then optimize the cost of preserving it.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies interleavings, happens-before, data races, linearizability, deadlocks, and systematic schedule testing.
- [Software Engineering Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies deterministic harnesses, independent oracles, property testing, and fault injection.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies dependency graphs, cycle detection, partial orders, and state-space exploration.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) supplies snapshot ingestion, exactly-once boundaries, late data, and reconciliation across storage systems.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) distinguishes serializability from strict serializability, replica consistency, consensus order, and distributed transactions.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies idempotency keys, conditional requests, retry budgets, and outbox/inbox integration.

## References

1. PostgreSQL Global Development Group, [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; standard phenomena, statement/transaction snapshots, retry, and SSI behavior.
2. Oracle, [MySQL 8.4 InnoDB Transaction Isolation Levels](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html), current documentation, retrieved 2026-08-30; consistent versus locking reads, snapshots, gap locks, and level behavior.
3. Microsoft, [SET TRANSACTION ISOLATION LEVEL (Transact-SQL)](https://learn.microsoft.com/en-us/sql/t-sql/statements/set-transaction-isolation-level-transact-sql?view=sql-server-ver17), current SQL Server documentation, retrieved 2026-08-30; locking, row-versioned read committed, snapshot, and serializable behavior.
4. SQLite Project, [Isolation In SQLite](https://www.sqlite.org/isolation.html), current documentation, retrieved 2026-08-30; separate connections, rollback versus WAL mode, snapshot isolation, and write serialization.
5. Hal Berenson et al., [“A Critique of ANSI SQL Isolation Levels”](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf), Microsoft Research Technical Report MSR-TR-95-51, 1995; phenomenon ambiguities, locking definitions, and snapshot isolation.
6. Atul Adya, [*Weak Consistency: A Generalized Theory and Optimistic Implementations for Distributed Transactions*](https://publications.csail.mit.edu/lcs/pubs/pdf/MIT-LCS-TR-786.pdf), MIT PhD thesis, 1999; history and dependency-based isolation theory.
7. Alan Fekete et al., [“Making Snapshot Isolation Serializable”](https://www.cse.iitb.ac.in/infolab/Data/Courses/CS632/2009/Papers/p492-fekete.pdf), *ACM Transactions on Database Systems* 30(2), 2005, DOI `10.1145/1071610.1071615`; SI anomalies and application-level conditions for serializable execution.
8. Michael J. Cahill, Uwe Röhm, and Alan D. Fekete, [“Serializable Isolation for Snapshot Databases”](https://www.cs.cornell.edu/~sowell/dbpapers/serializable_isolation.pdf), *SIGMOD*, 2008; serializable snapshot isolation by anomaly detection.
9. Kyle Kingsbury and Peter Alvaro, [“Elle: Inferring Isolation Anomalies from Experimental Observations”](https://www.vldb.org/pvldb/vol14/p268-alvaro.pdf), *PVLDB* 14(3), 2021; versioned histories and anomaly inference from observed executions.
10. Cockroach Labs, [Serializable Transactions](https://www.cockroachlabs.com/docs/stable/demo-serializable.html), current documentation, retrieved 2026-08-30; distributed serializable execution, contention, and client retry behavior.

## Exercises

### Exercise 1

For read uncommitted, read committed, repeatable read, snapshot isolation, and serializable execution, state the minimum or modeled protections discussed here. Identify which comparisons are not justified without engine-specific semantics.

### Exercise 2

Analyze the doctor history from the executable example. Derive both possible serial outcomes, construct the `rw` dependency graph, and explain precisely why first-committer-wins does not reject either write.

### Exercise 3

Diagnose a quota breach in which two repeatable-read transactions count qualifying rows and insert disjoint reservations. Specify the missing conflict domain and compare an exact constraint, guard-row locking, and serializable retry.

### Exercise 4

Design a cross-engine verification harness for read committed and repeatable read on PostgreSQL, InnoDB, and SQL Server. Include configuration discovery, barriers, expected blocking/abort alternatives, evidence, cleanup, and limits on portability claims.

### Exercise 5

Design a migration of a payment-allocation transaction from statement-level read committed to serializable execution while it also publishes an event. Cover transaction boundaries, outbox/idempotency, retry, ambiguous commit, canarying, capacity, rollback, privacy, and correctness gates.

## Answers to the Exercises

### Answer 1

The teaching minimums permit dirty/nonrepeatable/phantom behavior at read uncommitted; read committed prevents dirty read but may permit nonrepeatable reads, phantoms, and serialization anomalies; repeatable read prevents dirty and nonrepeatable reads but the standard minimum may permit phantoms and serialization anomalies; serializable excludes histories not equivalent to a serial order. The modeled SI contract supplies a stable committed transaction snapshot plus own writes and rejects concurrent same-item writers, preventing many classic phenomena but permitting write skew. Do not order a product's repeatable read against SI, infer dirty-read support, or infer blocking/snapshot behavior from these names alone. Bind comparisons to engine, version, storage, configuration, statement/read type, and the exact history. Strict serializability is an additional real-time property, not established merely by the SQL label.

### Answer 2

In serial order T1 then T2, T1 sees `(1,1)` and sets A off; T2 then sees `(0,1)` and must keep B on, ending `(0,1)`. In T2 then T1, the symmetric result is `(1,0)`. In the concurrent SI history, T1 reads old B before T2 writes B, so `rw T1->T2`; T2 reads old A before T1 writes A, so `rw T2->T1`. The cycle refutes a serial order. First-committer-wins compares write sets `{A}` and `{B}`; their intersection is empty, so neither same-item writer excludes the other. The invariant and graph oracles independently show why stable reads plus disjoint-write admission is insufficient.

### Answer 3

The conflict domain is the predicate “all qualifying reservations for this tenant/period,” including rows not yet present and any partition/index through which they can enter. Locking only returned rows misses an empty gap; disjoint inserts avoid same-row conflicts. An exact constraint is strongest and simplest when the quota can be represented by unique slots, exclusion, or another native rule, but schema/cardinality can be costly. A tenant-period guard row can be locked and atomically incremented under the limit, producing a clear shared conflict but a possible hotspot/deadlock-order burden. Serializable execution can track the predicate/read-write dependencies and abort an unsafe history, preserving schema flexibility but requiring correct whole-transaction retry and capacity for aborts. Existing breaches must be reconciled, and every writer must use the chosen protection.

### Answer 4

Use disposable schemas and two independent connections per engine. Record exact server/driver versions, storage engine, database/session isolation, SQL Server `READ_COMMITTED_SNAPSHOT`/snapshot options, autocommit, and read/lock hints. Seed fixed rows. For nonrepeatable read, barrier after T1's first read, commit T2's update, then release T1's reread. For phantom, use an indexed predicate and barrier before T2's qualifying insert. For write conflict/skew, pause both transactions after decision reads, then release controlled writes and commits. Capture read values/version identifiers where available, affected rows, waits, SQLSTATE/vendor errors, commits/aborts, and final invariant. Use bounded timeouts only to stop hangs; expected prevention is a controlled block followed by safe state, an abort, or constraint rejection. Reset per schedule. Report each engine/configuration separately: equal labels do not justify equal mechanism or every untested history.

### Answer 5

Place allocation decision reads, protected writes, and an outbox insert in one serializable transaction; do not publish directly before commit. Give the business operation a stable idempotency key with a uniqueness constraint, so whole-transaction retries cannot allocate or enqueue twice. On serialization/deadlock failures, discard all attempt results, reacquire/begin as documented, reread, recompute, and retry with bounded jitter/deadline. On connection loss during commit, treat outcome as ambiguous: query durable operation identity rather than blindly issuing a new logical payment. A separate idempotent publisher sends committed outbox events and records delivery attempts. Canary by transaction class with forced-history invariant tests first, then gates on duplicate/missing allocation and event reconciliation, serialization/deadlock/retry exhaustion, p95/p99, pool occupancy, lock wait, version retention, and outbox lag. Log identifiers and codes without sensitive payment data. Preserve reversible routing/configuration, but rollback to weaker isolation only while an alternative proven invariant protection remains; throughput never overrides a known safety breach.
