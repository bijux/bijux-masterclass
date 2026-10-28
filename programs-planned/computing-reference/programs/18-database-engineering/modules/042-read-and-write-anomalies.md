---
module_id: DBE-042
program: Database Engineering
level: 1
module_number: 42
title: Read and Write Anomalies
status: complete
last_verified: 2026-08-30
---

# Read and Write Anomalies

## One-Page Review

### Governing question

Which concurrent transaction histories violate an application's observation or invariant contract, how can those histories be named and proved anomalous, and which mechanism prevents them without relying on isolation-level folklore?

### Essential definitions

A **history** is an ordering (or partial ordering) of transaction reads, writes, commits, and aborts. Use `r_i(x=v)`, `w_i(x=v)`, `c_i`, and `a_i` for transaction `i`. A **serial history** has no interleaving; a history is **serializable** when its committed effect/observations are equivalent to some serial history under the selected formal model. A **dirty read** observes an uncommitted value; a **dirty write** overwrites another uncommitted write. A **nonrepeatable read** sees one item change between reads; a **phantom** sees the membership of a predicate result change. A **lost update** occurs when a read-modify-write based on stale state overwrites a concurrent update. **Read skew/fractured read** combines versions that violate a cross-item snapshot expectation. **Write skew** lets transactions read a shared constraint and write disjoint items so both commit an invariant-breaking state. An `rw` **antidependency** points from a reader to a transaction that later overwrites what it read or a matching predicate; cycles in the appropriate serialization graph establish nonserializability.

### Central model, mechanism, or theorem

Do not diagnose from final rows alone. Record the history, read sources, predicates, commit/abort state, and application invariant. Build dependency edges: `wr` when `T_j` reads a version written by `T_i`; `ww` when committed writes order versions of the same logical item; and `rw` when `T_i` reads a version/predicate and `T_j` installs a later conflicting version. For single-version conflict serializability, an acyclic precedence graph admits a topological serial order; a cycle proves the history is not conflict-serializable. Multiversion models require version-order-aware definitions, but the practical discipline remains: prove or refute a serial explanation. Snapshot isolation can give stable snapshots and reject some same-item write conflicts while still admitting a two-`rw` write-skew cycle on disjoint writes.

### Critical invariants

- Every anomaly claim includes initial state, transaction program, exact schedule/read versions, commits/aborts, final state, and violated oracle.
- Isolation is identified by engine, version, storage engine, statement/read type, explicit settings, and retry behavior—not only a standardized label.
- Predicate reads include gaps/nonexistent rows and index/search domain; protecting only rows already present may not protect the predicate.
- A transaction that aborts for deadlock/serialization is not an anomaly if the application retries the whole logical transaction correctly; treating abort as success is an application failure.
- Atomic conditional writes, constraints, locks, and serializable validation protect only the invariant/domain they actually cover.
- Tests force schedules and compare results with a serial/reference oracle or invariant; absence of a failure in uncontrolled load is not proof.
- Mitigation preserves semantic failures, stable command identity, bounded retry, observability, and service budgets.

### Common failures

Failures include calling every stale value a dirty read; checking only final state; confusing nonrepeatable read with lost update; assuming repeatable item reads prevent phantoms or write skew; claiming snapshot isolation is serializable; treating MVCC as lock-free correctness; locking rows after decision reads; failing to lock/query nonexistent predicate members; using `SELECT` then unconditional `UPDATE`; retrying only the last statement; suppressing serialization errors; using `SKIP LOCKED` for a consistent business view; depending on a default isolation name across engines; assuming a unique constraint protects a multi-row threshold; and testing concurrent code without a schedule barrier or oracle.

### Compact example

Two doctors `A` and `B` are initially on call; invariant: at least one remains. `T1` and `T2` both read `(A=true,B=true)`. `T1` writes `A=false`; `T2` writes `B=false`; both commit because they update different rows under a snapshot-style regime that permits this history. Final `(false,false)` violates the invariant. Each transaction saw a valid snapshot and no same-row lost update occurred. The two `rw` antidependencies form a cycle: `T1→T2` through read `B`, and `T2→T1` through read `A`. Serializable validation, locking/materializing the shared constraint, or another exact enforcement mechanism must abort/block one.

### Connections

Retrieve [ACID and Transaction Boundaries](041-acid-and-transaction-boundaries.md), [Composite and Covering Indexes](035-composite-and-covering-indexes.md), and [Index Maintenance and Write Amplification](039-index-maintenance-and-write-amplification.md). Continue through the [Database Engineering roadmap](../ROADMAP.md) to DBE-043, Lock Modes and Granularity; DBE-044, Two-Phase Locking; and DBE-046, MVCC.

## Governing Question

How do we specify, reproduce, and prove read/write anomalies as histories, then select and verify the narrowest mechanism whose actual engine semantics exclude every history that would violate the application's invariant?

## Why This Matters

Concurrent transactions can each be internally reasonable and still compose into an impossible or invalid outcome. A dashboard may combine balances from different committed moments. Two requests may both reserve the last capacity. A stale form submission can erase a concurrent edit. Two workers may each observe that another doctor remains on call and both leave. These failures often pass unit tests and appear only under carefully timed interleavings.

Isolation names do not settle the question. SQL phenomena historically described dirty, nonrepeatable, and phantom reads, but influential research showed those definitions do not uniquely characterize common locking and multiversion implementations. Engines legitimately provide different behavior under similarly named levels. Statements within one engine can use different read mechanisms. Current PostgreSQL Read Committed takes a new snapshot per command, while its Repeatable Read is snapshot-based and stronger than the SQL minimum for phantoms yet can admit serialization anomalies. Current MySQL InnoDB distinguishes consistent nonlocking reads from locking/current reads and warns about mixing views. SQLite's concurrency depends on journal mode and connection behavior.

The durable skill is therefore history reasoning: name the logical items and predicates, capture which versions each read observed, identify dependencies, state the invariant or serial oracle, and force the schedule in a supported environment. Then choose constraints, atomic statements, locking, version checks, serializable isolation, or redesign based on the actual conflict domain.

## Prerequisites and Retrieval

You should understand transaction boundaries, commit/abort, invariants, keys/predicates, basic SQL reads/writes, and partial orders/graphs. Retrieve serial execution, snapshot, version, conflict, topological ordering, precondition, lost response/idempotent retry, and predicate membership. This chapter diagnoses histories; later modules derive locks, 2PL, deadlocks, MVCC, snapshot isolation, and serializable snapshot isolation mechanisms.

## Learning Objectives

After this module, you can:

1. write a precise transaction history with read versions, predicates, writes, commits, and aborts;
2. distinguish dirty read/write, intermediate read, nonrepeatable read, phantom, lost update, read skew, and write skew;
3. state a serial/reference or invariant oracle rather than infer anomaly from surprise;
4. build `wr`, `ww`, and `rw` dependencies and use cycles appropriately;
5. explain why stable snapshots and first-committer-wins checks do not necessarily prevent write skew;
6. distinguish consistent, current/locking, and modifying statement reads in current engines;
7. map an invariant's exact conflict domain, including absent rows and predicates;
8. choose among atomic DML, constraints, compare-and-set, locks, serializable isolation, and state redesign;
9. implement whole-transaction retry with stable identity for expected concurrency aborts; and
10. construct deterministic schedule/fault tests plus production anomaly evidence.

## Core Exposition

**Represent histories before naming them.** Let initial value be `x_0`. `r_1(x=x_0)` means transaction 1 read that version; `w_1(x=x_1)` creates a tentative version; `c_1` commits; `a_1` aborts. For predicate `P`, write `r_1(P={keys...})` and retain the parameter/collation/snapshot so an insertion into the predicate domain is visible in the model. Program order inside each transaction is mandatory even when wall-clock order across transactions is partial.

Final state is insufficient. Two increments might end at 120 either through correct serial execution or an anomalous history whose effects coincidentally match. Conversely, a final state different from one expected order may still equal another permitted serial order. Include return values and read sources: serializability concerns observed behavior/effects, not merely bytes after commit.

**Dirty phenomena.** Dirty write occurs when `T2` overwrites `T1`'s uncommitted value. If `T1` aborts, recovery cannot naively restore the old value without erasing `T2`; strict write exclusion/version protocols normally prevent it. Dirty read is `w_1(x=5), r_2(x=5), a_1`: `T2` consumed a value that never committed. If `T2` commits a derived effect, aborting `T1` cannot retract it automatically. **Intermediate read** observes a transaction's nonfinal write before that transaction overwrites it again and commits another value.

Do not call every stale read dirty. Reading an older committed snapshot is stale relative to wall clock but not a dirty read. It may be valid under the selected model and invalid under a separate freshness/read-your-writes contract. Terms need histories.

**Nonrepeatable read and phantom.** At a per-statement snapshot level, `T1` reads `x=5`; `T2` commits `x=6`; a later `T1` statement reads `x=6`. The same logical item changed: nonrepeatable read. For `SELECT ... WHERE balance<0`, `T2` inserts/updates a qualifying row and commits; rerunning the predicate returns a changed set: phantom. Protecting only rows returned initially misses the empty gap or rows that did not yet qualify.

Whether these are bugs depends on the transaction contract. A monitoring transaction may want fresh per-statement values; a report requiring one coherent as-of snapshot does not. State the oracle. Even repeatable item reads do not alone imply serializable execution: a stable snapshot can still participate in write skew.

**Lost update.** Initial `x=100`. `T1` reads 100 and plans 110; `T2` reads 100 and plans 110; both unconditionally write 110; both commit. A serial pair of `+10` operations must produce 120, but final is 110. One logical increment vanished. This is a read-modify-write race, not merely two writes.

Prevent it by expressing the operation atomically (`UPDATE ... SET x=x+10`) where the engine serializes the row update; locking before the read; compare-and-set (`UPDATE ... WHERE version=old`) and rejecting/recomputing on zero affected rows; or serializable execution/retry. A last-writer-wins policy may intentionally choose one replacement, but it must not be called preservation of both updates. Version tokens must cover every field/invariant affected and remain inside the authoritative transaction.

**Read skew/fractured observation.** Accounts start `(x=50,y=50)`. `T1` reads `x=50`. `T2` transfers 10 atomically and commits `(40,60)`. `T1` later reads `y=60`, observing total 110—a combination that never existed as a committed database state. A transaction-level snapshot would give `(50,50)` for both reads; a per-statement snapshot may combine moments. Multi-row API responses assembled by independent transactions or replica reads can fracture similarly even when each query is locally correct.

Do not repair read skew by caching the first field in application memory unless that creates the intended snapshot semantics for all data. Group the read under an appropriate database snapshot/transaction, use a consistent version/as-of token, or redesign the representation. Cross-service coherent reads require a broader protocol; one local database isolation setting cannot freeze other authorities.

**Write skew.** Let invariant `A∨B` mean at least one doctor is on call. Both snapshot transactions read `A=true,B=true`; `T1` writes only `A=false`; `T2` writes only `B=false`. Same-row write-conflict detection sees no collision, so both may commit and produce false. Each transition would preserve the invariant if run alone against its read snapshot. Their composition has no serial explanation: whichever runs second should see the first doctor off and refuse.

Write skew generalizes: quota split across rows, overlapping reservations, “at most N active,” double approvals, uniqueness expressed only by a preliminary read, or reciprocal references. The conflict domain is the invariant, not necessarily one row. Remedies include a native unique/exclusion/check mechanism capable of exact enforcement; locking every row/range/advisory key representing the invariant before reading; materializing a shared counter/guard row so conflicting writers touch one item; or serializable isolation with complete retry. Each adds contention or modeling cost but makes the conflict observable.

**Serialization graphs.** Dependencies explain serial order constraints. If `T_j` reads a committed version written by `T_i`, add `T_i→T_j` (`wr`). If `T_j` installs a later version after `T_i`'s version, add `T_i→T_j` (`ww`) under the version order. If `T_i` reads a version or predicate and `T_j` later writes what would change that read, add reader-to-writer `T_i→T_j` (`rw` antidependency).

For single-version conflict histories, acyclicity of the precedence graph permits a topological serial order; a cycle proves non-conflict-serializability. Multiversion serializability graphs additionally depend on which versions reads see and their version order; do not mechanically apply an incomplete single-version graph. Still, cycles are operationally illuminating: doctor write skew has `T1→T2` because `T1` read `B=true` before `T2` wrote false, and `T2→T1` symmetrically through A.

**SQL phenomena are not a complete taxonomy.** Dirty/nonrepeatable/phantom definitions help communicate, but Berenson and colleagues showed ambiguities and omissions when mapping SQL-92 descriptions to locking and snapshot implementations. Adya's generalized theory formalizes dependencies and phenomena across weak consistency. Use terminology with a definition and schedule. Avoid tables that claim every product's level prevents an anomaly universally.

**Snapshot isolation.** A common form gives each transaction a consistent snapshot and aborts/blocks concurrent writes to the same item according to a first-committer/updater rule. It prevents dirty reads and many lost updates while allowing high read concurrency. But disjoint writes based on a shared snapshot can produce write skew. Snapshot isolation is therefore not serializability.

Serializable snapshot isolation (SSI) retains snapshot reads and tracks dangerous `rw` dependency structures, aborting transactions when necessary to prevent serialization cycles. Predicate tracking is about detecting influence, not necessarily blocking like a traditional predicate lock. Applications must handle serialization failure by retrying the entire transaction from fresh reads. Read-only transactions and safe snapshots have specialized optimizations; rely on current engine documentation.

**Current engine specificity.** Current PostgreSQL documents standard phenomena and its implementations: Read Uncommitted behaves as Read Committed; Read Committed usually takes a per-command snapshot; Repeatable Read supplies a transaction snapshot but can raise/update conflicts and permits serialization anomalies; Serializable monitors dependencies and may return SQLSTATE `40001`. Sequences have special nontransactional behavior. These details matter to tests.

Current MySQL InnoDB documents that Repeatable Read consistent nonlocking reads use the snapshot established by the first such read, while locking reads and modifying statements use locking/current behavior; mixing the two views can be difficult to reason about. Under Read Committed each consistent read gets a fresh snapshot and gap-lock behavior differs. `SKIP LOCKED` deliberately returns an inconsistent view suited to queue-like work, not a general coherent query.

SQLite documents serializable transactions by serializing writes in most configurations; WAL mode provides snapshot isolation for readers, and a reader attempting to promote after another writer changed the snapshot can receive `SQLITE_BUSY_SNAPSHOT`. Shared-cache plus `read_uncommitted` changes visibility. A single writer does not make a multi-database or application workflow serializable automatically.

The executable artifact stages three deliberately weak histories. It is a deterministic semantic trace, not a concurrent DBMS test.

<!-- bijux-verify: {"id":"transaction-anomaly-histories","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"lost_update_final=110\nlost_update_serial=120\nread_skew_observed_total=110\nread_skew_committed_total=100\nwrite_skew_on_call=(False, False)\nwrite_skew_invariant=False\nall_anomalies_reproduced=True\n","stderr":""}} -->
```python
# Lost update: both transactions derive a replacement from the same old version.
counter = 100
t1_read = counter
t2_read = counter
counter = t1_read + 10
counter = t2_read + 10
lost_update_final = counter
lost_update_serial = 100 + 10 + 10

# Read skew: one reader combines x before and y after an atomic transfer.
x, y = 50, 50
t1_x = x
x, y = x - 10, y + 10
t1_y = y
read_skew_observed_total = t1_x + t1_y
read_skew_committed_total = x + y

# Write skew: both decisions use the same valid snapshot but update disjoint rows.
on_call = {"A": True, "B": True}
t1_snapshot = dict(on_call)
t2_snapshot = dict(on_call)
if t1_snapshot["B"]:
    on_call["A"] = False
if t2_snapshot["A"]:
    on_call["B"] = False
write_skew_on_call = tuple(on_call[name] for name in ("A", "B"))
write_skew_invariant = any(write_skew_on_call)

print(f"lost_update_final={lost_update_final}")
print(f"lost_update_serial={lost_update_serial}")
print(f"read_skew_observed_total={read_skew_observed_total}")
print(f"read_skew_committed_total={read_skew_committed_total}")
print(f"write_skew_on_call={write_skew_on_call}")
print(f"write_skew_invariant={write_skew_invariant}")
print(
    "all_anomalies_reproduced="
    f"{lost_update_final != lost_update_serial and read_skew_observed_total != 100 and not write_skew_invariant}"
)
```

The code omits transaction engines, versions, predicates, locks, commit/abort, retries, graphs, failures, and performance. Its Python statement order constructs already-chosen histories; it does not claim Python concurrency has database semantics.

**Choosing a remedy.** Start from invariant and access pattern:

- single-item arithmetic: atomic update/constraint, optionally return the committed value;
- replacement based on a version: compare-and-set and recompute/merge/reject conflict;
- parent/child existence or capacity: lock the authoritative parent/guard plus relevant rows before decision;
- uniqueness/nonoverlap: native unique or exclusion mechanism when exact;
- dynamic predicate/multirow invariant: serializable isolation or complete predicate/range locking/materialized conflict;
- commutative operations: represent deltas/events/sets so concurrent effects combine, while still enforcing bounds;
- queue claiming: atomic claim/locking with documented `SKIP LOCKED` semantics, leases/fencing where work escapes transaction;
- cross-authority invariant: redesign ownership/workflow; local isolation cannot provide a global transaction implicitly.

Lock ordering, deadlocks, aborts, retry load, hot guard rows, and starvation are part of the design. Stronger isolation can reduce application proof burden but does not remove domain constraints or retry correctness. Weaker isolation may be safe for a transaction whose invariant is protected by exact constraints/atomic statements. Select per transaction class with evidence, not globally by fear or throughput folklore.

**Testing.** A concurrency test needs barriers/hooks that force the intended interleaving: both transactions complete their decision reads; then writes/commits proceed in controlled order. Use separate connections, explicit isolation, exact SQL/parameters, known initial data/statistics/indexes, and capture transaction IDs/snapshots where supported. Assert results, errors, final state, constraint records, and serial/invariant oracle. Repeat across engine/version/configuration but do not treat random stress as exhaustive proof.

Model checking or systematic schedule exploration is valuable for small transaction programs. Include abort/retry and crash/ambiguity. For production, monitor isolation settings, transaction class/version, commit/abort/deadlock/serialization rates, retry count/exhaustion, zero-row compare-and-set conflicts, constraint conflicts, invariant reconciliation, long snapshots, locks/waits, and p99. A rising retry rate can be correct protection and still an SLO/capacity problem.

## Definitions and Notation

- `r_i(x_j)`: transaction `i` reads version of `x` written by transaction `j`; `x_0` is initial.
- `w_i(x_i)`: transaction `i` writes a new version; `c_i`/`a_i` are commit/abort.
- `r_i(P=K)`: predicate read returns key set `K` under a declared snapshot and predicate domain.
- **Dirty read/write:** read or overwrite involving another transaction's uncommitted version.
- **Nonrepeatable read:** same logical item yields different committed versions within one transaction.
- **Phantom:** repeated predicate yields changed membership due to a concurrent commit.
- **Lost update:** committed read-modify-write effects fail to include a concurrent logical update that a serial execution would preserve.
- **Read skew:** one logical observation combines incompatible versions/moments and violates its snapshot oracle.
- **Write skew:** transactions read overlapping constraint state, write disjoint items, and jointly violate invariant/serializability.
- `wr`, `ww`, `rw`: write-read, write-write, and read-write-antidependency edges with model-specific version rules.
- **Serialization graph:** transactions as vertices and dependency edges; cycle criteria depend on the selected single/multiversion theory.
- **Conflict domain:** all existing/absent logical items or predicates through which concurrent actions can affect an invariant.

## Mechanisms, Invariants, or Proof Structure

For lost update, the serial oracle is decisive: both `+10` functions composed from 100 yield 120 in either serial order. The reproduced history yields 110, so it is not equivalent with respect to the returned/final counter semantics. If operations were explicit replacement commands with a documented last-writer-wins policy, the oracle would differ; name intent.

For read skew, committed database totals before and after transfer are both 100, yet the reader returns 110. No committed snapshot contains its pair `(50,60)`. This proves violation of a coherent-snapshot read contract, although each individual value was committed at some time.

For doctor write skew, any serial order refuses the second leave because it observes the first doctor off. The committed false/false state therefore has no valid serial execution. Graphically, `T1` read B before `T2` wrote B, giving `T1→T2`; `T2` read A before `T1` wrote A, giving `T2→T1`; the cycle proves nonserializability in the applicable multiversion dependency model.

Constraint/lock proofs require coverage. A unique index serializes duplicate keys only in its key domain; it does not enforce “at most N” generally. Row locks protect rows actually locked; a predicate over absent/future rows needs range/predicate locking or a materialized guard. Serializable validation protects admitted histories only if every invariant-bearing read/write occurs inside the retried transaction.

## Alternatives and Trade-Offs

- **Atomic DML versus read-then-write:** atomic expressions are concise and serialize one item; complex decisions still need broader conflict protection.
- **Compare-and-set versus pessimistic lock:** CAS avoids waiting but exposes conflicts/recompute to callers; locking blocks and can deadlock while simplifying one decision.
- **Constraint versus serializable isolation:** constraints give exact continuous enforcement for representable invariants; serializable covers dynamic read/write logic but aborts and needs retry.
- **Guard row versus predicate tracking:** guard materializes conflict simply but can hotspot; predicate/SSI preserves concurrency but adds engine-specific tracking/abort behavior.
- **Per-statement freshness versus transaction snapshot:** fresh reads suit monitoring; one snapshot suits coherent reports but can become stale and retain versions.
- **Snapshot isolation versus serializable:** snapshot gives stable reads and good concurrency but admits write skew; serializable excludes nonserial histories at monitoring/abort or locking cost.
- **Fail conflict versus merge/commute:** rejecting stale replacement preserves intent visibility; domain-specific merge/delta designs can keep both effects but need algebra and bounds.

## Failure Modes and Misconceptions

- “Stale equals dirty.” Dirty specifically means uncommitted; older committed snapshot has different semantics.
- “Repeatable reads mean serializable.” Stable item/snapshot reads can still admit write skew.
- “No two writers touched the same row, so it is safe.” Multirow/predicate invariants create disjoint-write conflicts.
- “Final rows look plausible.” Include read returns and serial/invariant oracle.
- “`SELECT FOR UPDATE` after reading fixes it.” The decision was already made from an unprotected version; lock before authoritative read.
- “Lock every returned row.” Empty gaps and future predicate members can still create phantoms/skew.
- “A version column prevents all races.” It protects the entity/version included in its conditional write, not unrelated invariant rows.
- “Serialization failure is a database bug.” It can be the mechanism correctly rejecting a dangerous history; whole-transaction retry is required.
- “Retry only `COMMIT` or `UPDATE`.” Fresh decision reads and writes form the retry unit.
- “`SKIP LOCKED` gives a consistent view.” Current MySQL explicitly warns it does not; it is useful for queue-like access.
- “The isolation name is portable.” Engine, version, read kind, storage engine, and configuration determine behavior.
- “No failure in load test proves safety.” Rare schedules need deterministic forcing or formal exploration.

## Worked Examples

### Example 1

`T1` writes price 12 without commit; `T2` reads 12 and emits an invoice; `T1` aborts. The invoice derives from no committed price. Conclusion: this is dirty read, and a later database rollback cannot retract the external invoice.

### Example 2

`T1` reads stock 5; `T2` commits stock 4; `T1` reads 4. If T1 is a coherent calculation, it suffered nonrepeatable read; if it is a live monitor, the change may be intended. Conclusion: schedule plus application oracle determines harm.

### Example 3

`T1` counts active sessions as 9; `T2` inserts the tenth and commits; T1 recounts 10. Locking the original nine rows would not cover the absent tenth key. Conclusion: phantom protection needs predicate/range or materialized capacity conflict.

### Example 4

Two clients read document version 7, edit different fields, and both replace the whole row. Final row contains only one edit. Conclusion: use conditional version update plus merge/reject, field/delta operations, lock, or serializable retry; last response timing is not a merge policy.

### Example 5

Account transfer remains total 100, but a per-command report reads old source 50 and new destination 60. Conclusion: read skew violates coherent snapshot without any dirty value or invalid committed database state.

### Example 6

Doctors write disjoint rows from the same valid snapshot and violate at-least-one-on-call. Conclusion: no same-row conflict is needed for write skew; dependency cycle follows the invariant reads.

### Example 7

Two transactions test “no reservation overlaps interval,” both see empty, and insert different overlapping rows. Row locks on an empty result lock nothing in some mechanisms. Conclusion: use an exact exclusion constraint, serializable predicate tracking, or appropriately locked range/guard.

### Example 8

Serializable execution aborts T2 with `40001`; application catches it, returns success, and never retries. Database excluded the anomaly, but business effect is missing. Conclusion: abort is part of the interface and must drive bounded whole-transaction retry or explicit failure.

### Example 9

Worker query uses `SKIP LOCKED`; two workers claim different available jobs and process in parallel. A dashboard reuses it and reports missing locked jobs as total queue state. Conclusion: an intentionally inconsistent queue-selection primitive is not a general reporting snapshot.

### Example 10

An atomic `UPDATE counters SET value=value+1` preserves two increments on one row, but the same technique does not enforce “combined counters ≤100” across shards. Conclusion: mechanism coverage must match the full conflict domain.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies races, interleavings, linearizability, atomics, and schedule testing.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies dependency graphs, cycle detection, topological ordering, and systematic exploration.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies conditional requests/version tokens, idempotent retry, and conflict responses.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies consistency models, histories, causal/serial orders, and cross-node testing.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies deterministic concurrency harnesses, oracles, property tests, and fault injection.

## References

1. PostgreSQL Global Development Group, [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html), current phenomena, snapshot behavior, serializable dependency monitoring, and retry guidance.
2. Oracle, [MySQL 8.4 InnoDB Transaction Isolation Levels](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html), current consistent/locking read and gap-lock behavior.
3. Oracle, [MySQL 8.4 Consistent Nonlocking Reads](https://dev.mysql.com/doc/refman/8.4/en/innodb-consistent-read.html), current snapshot/read-view behavior and mixed-view anomaly warning.
4. SQLite Project, [Isolation in SQLite](https://www.sqlite.org/isolation.html), official rollback/WAL isolation, snapshot behavior, and `SQLITE_BUSY_SNAPSHOT`.
5. Hal Berenson et al., [“A Critique of ANSI SQL Isolation Levels”](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf), Microsoft Research Technical Report MSR-TR-95-51, 1995.
6. Atul Adya, [*Weak Consistency: A Generalized Theory and Optimistic Implementations for Distributed Transactions*](https://publications.csail.mit.edu/lcs/pubs/pdf/MIT-LCS-TR-786.pdf), MIT PhD thesis, 1999.
7. Alan Fekete et al., [“Making Snapshot Isolation Serializable”](https://www.cse.iitb.ac.in/infolab/Data/Courses/CS632/2009/Papers/p492-fekete.pdf), *ACM Transactions on Database Systems* 30(2), 2005.
8. Michael J. Cahill, Uwe Röhm, and Alan D. Fekete, [“Serializable Isolation for Snapshot Databases”](https://www.cs.cornell.edu/~sowell/dbpapers/serializable_isolation.pdf), *SIGMOD*, 2008.
9. Peter Bailis et al., [“Highly Available Transactions: Virtues and Limitations”](https://www.vldb.org/pvldb/vol7/p181-bailis.pdf), *PVLDB* 7(3), 2013, formal transactional guarantees and anomalies under availability.
10. Kyle Kingsbury and Peter Alvaro, [“Elle: Inferring Isolation Anomalies from Experimental Observations”](https://www.vldb.org/pvldb/vol14/p268-kingsbury.pdf), *PVLDB* 14(3), 2021, history-based anomaly detection.

## Exercises

### Exercise 1

Given six interleaved histories with read versions, predicate results, commits, and aborts, classify dirty/intermediate/nonrepeatable/phantom/lost-update/read-skew cases and identify when the supplied evidence is insufficient.

### Exercise 2

Build `wr`, `ww`, and `rw` dependencies for a doctor write-skew history and a lost-update history. Give or refute serial orders and state where multiversion version order matters.

### Exercise 3

Diagnose a production quota breach under a documented snapshot isolation level: queries read separate usage rows and writers insert disjoint reservations. Propose three remedies and compare correctness coverage, contention, retries, indexing, and operational evidence.

### Exercise 4

Design a deterministic two-connection test harness for nonrepeatable read, phantom, lost update, and write skew across two database engines, including barriers, isolation/read types, cleanup, timeouts, errors, retries, and oracles.

### Exercise 5

Design an anomaly-monitoring and migration program from weaker isolation to serializable execution for a high-volume service, covering transaction inventory, invariants, retry identity, capacity, canary, rollback, privacy, and proof limitations.

## Answers to the Exercises

### Answer 1

For every history first bind each read to committed/uncommitted/initial version and record transaction outcomes. Reading another's uncommitted write followed by its abort is dirty read; overwriting an uncommitted write is dirty write; reading an early uncommitted write when the writer later changes it before commit is intermediate read. Re-reading one item after a concurrent commit is nonrepeatable; changed predicate membership is phantom. Two committed read-modify-writes whose serial semantic effects are not both present are lost update. Values individually committed but never coexisting under the required snapshot are read skew. If version source, predicate domain, commit/abort, or application oracle is missing, answer “insufficient evidence” and name the missing fact; do not classify from timestamps/final rows alone.

### Answer 2

Doctors: T1 reads B's old true before T2 writes false, so `rw T1→T2`; T2 reads A's old true before T1 writes false, so `rw T2→T1`; the cycle has no serial order. In either serial order, the second transaction would observe the first off and refuse. Lost update: both read `x0`; writes `x1` and `x2` are version-ordered by the final overwrite, adding `ww`; reader-to-overwriter antidependencies and exact model show a cycle/nonserial outcome when both increment effects are required. In a multiversion graph, identify which version each read saw and choose/version-order later writes; omitting that order can add wrong edges. Independently, serial functional oracle `(+10)∘(+10)(100)=120` refutes final 110.

### Answer 3

The conflict domain is total qualifying reservations, including rows not yet present; snapshot readers can both see capacity and insert disjoint keys. Remedy one: serializable isolation with every quota read/insert in one retried transaction; broad correctness, but dependency aborts and capacity planning. Two: lock/update one tenant-period quota/guard row atomically (`used+amount≤limit`); clear proof and index key, but hotspot/deadlock ordering. Three: exact native constraint/materialized slot allocation, such as one uniquely owned capacity unit or supported exclusion/range constraint; strong enforcement but schema/cardinality complexity. Plain locks on current reservation rows may miss empty predicate gaps. Compare p99, abort/retry, WAL, guard contention, partition keys, cleanup, and failure tests; reconcile existing breaches before migration.

### Answer 4

Use isolated schemas and two independent connections with explicit engine/version/storage/isolation and autocommit off. Seed exact rows. Coordinate barriers after both decision reads, after one writer/commit, and before rereads/writes; never rely on sleeps. Capture returned versions/sets, affected rows, SQLSTATE/vendor errors, commits/aborts, and final state. Nonrepeatable: T1 read, T2 update/commit, T1 reread. Phantom: predicate read, T2 qualifying insert/commit, reread. Lost update: both read, then controlled unconditional replacements. Write skew: both read invariant, disjoint writes/commits. Expect blocking/abort where the engine prevents a history; bounded timeouts stop hangs, and serializable failures trigger whole-transaction retry in a separate test. Reset state per schedule and compare to serial/invariant oracle. Document differing read kinds and unsupported histories rather than forcing identical labels.

### Answer 5

Inventory transaction programs, actual isolation/read kinds, decision predicates, constraints, owners, call rates, durations, contention keys, retries, and external identities. Write executable invariant and serial-reference oracles; capture minimized privacy-safe history metadata and reconciliation discrepancies. Reproduce critical histories on current version, then run serializable in clone/shadow/canary with whole-transaction stable-ID retry, fresh reads, bounded exponential jitter/deadline, and explicit exhaustion response. Capacity-test abort storms, locks, CPU/memory, p99, pool pressure, WAL/replica lag, and long snapshots. Move class by class with gates on results/invariants, abort/retry/exhaustion, SLOs, and resources; preserve prior configuration and reversible routing where supported. Monitor dependency/serialization errors and reconciliation, not raw sensitive values. Rollback isolation only if compensating invariant protections remain; never trade known corruption for throughput silently. State schedule/model coverage and that monitoring cannot prove absence of all anomalies.
