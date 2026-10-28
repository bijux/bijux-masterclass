---
module_id: DBE-043
program: Database Engineering
level: 1
module_number: 43
title: Lock Modes and Granularity
status: complete
last_verified: 2026-08-30
---

# Lock Modes and Granularity

## One-Page Review

### Governing question

How does a database lock manager protect reads, writes, predicates, schemas, and application-defined resources at multiple granularities while preserving correctness without collapsing useful concurrency?

### Essential definitions

A **logical lock** is a transaction-level claim on a named resource; incompatible requests wait, fail, skip, or trigger victim selection under policy. A **latch** is a short-lived internal synchronization primitive protecting in-memory/page structure, not a user transaction's logical history. **Granularity** is the resource size—database, table, partition, index, page, key/range, row, or application/advisory identity. **Shared (`S`)** permits compatible readers; **exclusive (`X`)** excludes competing access on the same resource. **Intent shared (`IS`)** announces `S` locks below; **intent exclusive (`IX`)** announces `X`/`IX` below; **shared with intent exclusive (`SIX`)** holds `S` on the node plus intends `X` below. **Compatibility** says whether modes from different owners may coexist on one resource. **Conversion** changes an owner's held mode. **Escalation** replaces many descendant locks with a coarser ancestor lock. A **key-range/predicate lock** protects a search domain, including absent/future keys, to prevent phantoms. An **advisory/application lock** protects a conventionally named application resource only when every participant honors the convention.

### Central model, mechanism, or theorem

Resources form a containment hierarchy. Under the canonical multiple-granularity protocol, a transaction acquires ancestors before descendants: `IS` ancestors before `S/IS`, and `IX` ancestors before `X/IX/SIX`. An `S` table request checks only table-level holders because every descendant writer must advertise `IX` above; `S` conflicts with `IX`, so hidden row writers cannot escape detection. Intention locks do not themselves lock descendant data. Compatibility for distinct owners is: `IS` with `IS,IX,S,SIX`; `IX` with `IS,IX`; `S` with `IS,S`; `SIX` with `IS`; `X` with none. This hierarchy reduces lock-manager search while retaining row-level concurrency. Correctness additionally depends on duration/order rules, covered predicate domain, conversions, and engine-specific semantics.

### Critical invariants

- Each logical resource has a canonical identity, hierarchy parent, mode, owner, acquisition time, duration, and release/abort path.
- Descendant locks are preceded by the required ancestor intention modes; coarse requests therefore detect incompatible hidden descendants.
- A request is granted only if compatible with every other owner's granted mode on the same logical resource.
- Conversion and escalation acquire the stronger/coarser protection before releasing weaker/descendant protection; no unprotected gap is introduced.
- Predicate/range protection covers existing keys, gaps, boundaries, collation/operator semantics, and the actual access path needed by the invariant.
- Lock duration matches isolation/recovery policy; write protection needed for rollback/strictness is not released early by convenience.
- Timeouts, `NOWAIT`, `SKIP LOCKED`, cancellation, deadlock victimization, and retries are explicit semantic outcomes.
- Lock observability is interpreted with snapshots/races and joined to transaction, query, resource, wait, and blocker identity safely.

### Common failures

Failures include confusing locks with latches; assuming “row lock” means no table-level lock; treating an intention lock as protection of all rows; applying a compatibility table across different products/modes; locking after the decision read; missing gaps/nonexistent keys; using page locks as semantic row identity; releasing fine locks before escalation succeeds; disabling escalation without lock-memory analysis; forcing row locks for huge scans; relying on `SKIP LOCKED` for complete results; upgrading many `S` locks to `X` in inconsistent order; holding application locks on another connection/session scope; using advisory keys that collide; forgetting DDL/schema locks; and diagnosing blocking from one instantaneous lock snapshot without the completed query/plan/history.

### Compact example

`T1` acquires table `IS` and row A `S`. `T2` acquires table `IX` and row B `X`: table `IS`/`IX` are compatible and rows differ. `T3` requests table `S`; it conflicts with T2's `IX`, proving the intention announcement finds a descendant writer without scanning rows. `T4` obtains table `IX` but waits for row A `X` because T1 holds row A `S`. A table-S escalation by T1 would also conflict with T2's IX and must not release row A before the conversion succeeds.

### Connections

Retrieve [Read and Write Anomalies](042-read-and-write-anomalies.md), [B+ Tree Insertion, Splitting, and Deletion](033-b-tree-insertion-splitting-and-deletion.md), and [Index Maintenance and Write Amplification](039-index-maintenance-and-write-amplification.md). Continue to the [Database Engineering roadmap](../ROADMAP.md) modules DBE-044, Two-Phase Locking, and DBE-045, Deadlock Detection and Resolution.

## Governing Question

Which logical resources and modes must a transaction acquire, in what hierarchy and duration, so every conflicting action becomes visible to the lock manager while compatible work proceeds and operational costs remain bounded?

## Why This Matters

Locking is not simply “read lock versus write lock.” A database can hold millions of row/key locks, a table intention lock, schema stability locks, metadata locks, and internal page latches simultaneously. A query that returns no rows may still need to protect a key range. A table reader cannot inspect every row lock before proceeding, so a hierarchy must summarize descendant intent. A batch can exceed lock memory and escalate into broad blocking. An `S`-to-`X` conversion can deadlock another upgrader.

Poor mental models create correctness defects and incidents. Developers add `FOR UPDATE` after an unprotected read, believe a row hint prevents escalation, use `SKIP LOCKED` for an audit report, or hold a database transaction while acquiring an advisory lock in inconsistent global order. Operators see a table-level intention lock and assume the entire table is blocked. Conversely, suppressing escalation or shortening lock duration can trade visible blocking for memory exhaustion or anomalies.

The durable approach separates semantics from implementation: identify the invariant's conflict domain, choose logical resources/modes/duration, follow hierarchy/order rules, then inspect the current engine's exact mapping. Concurrency benefit and operational risk are measured together.

## Prerequisites and Retrieval

You should understand transaction boundaries, read/write anomalies, predicates/ranges, B+ tree keys/pages, and graphs/partial orders. Retrieve shared versus exclusive access, compatibility relation, hierarchy/tree, ancestor/descendant, phantom, conversion, deadlock, wait-for graph, isolation, and rollback. DBE-044 adds the growing/shrinking rules of two-phase locking; DBE-045 develops deadlock detection/victims.

## Learning Objectives

After this module, you can:

1. distinguish transaction locks from latches, mutexes, MVCC versions, and application leases;
2. derive and apply the canonical `IS/IX/S/SIX/X` compatibility matrix;
3. enforce ancestor intention requirements in a resource hierarchy;
4. choose row/key/range/page/partition/table granularity from correctness and workload evidence;
5. reason about update modes, conversions, escalation, lock memory, and conversion deadlocks;
6. protect absent/future predicate members rather than only returned rows;
7. interpret PostgreSQL, MySQL InnoDB, and SQL Server modes without false portability;
8. design advisory/application lock identity, ownership, ordering, timeout, and cleanup;
9. diagnose blockers/waiters using transaction/query/resource evidence; and
10. test compatibility, hierarchy, phantoms, escalation, cancellation, deadlock, and retry behavior.

## Core Exposition

**Locks protect logical dependencies.** If transaction T bases a decision on resource R, the concurrency-control mechanism must prevent an incompatible change or later validate/abort the history. A lock manager maps canonical resource identities to granted requests and wait queues. A request includes transaction/session owner, mode, duration/scope, priority/time, and sometimes conversion state. Grant requires compatibility with all other owners' granted modes; same-owner requests may combine/convert according to a conversion lattice.

Logical resource is not necessarily physical storage. A “row” lock may be an index-key lock; heap identity can change; a predicate covers gaps; a table/schema lock protects metadata semantics. The execution plan determines which index keys/ranges are visited, so indexes affect lock footprint. Engine documentation, not SQL appearance, tells the actual resource.

**Locks versus latches.** A latch/mutex protects a buffer-frame or B-tree page structure for microseconds/milliseconds while code inspects/modifies it. It generally follows physical access and is not held to transaction commit. A logical lock protects a key/range/row/table semantic dependency across statements and waits. A page split needs latches for in-memory structural integrity and logical locks/transaction protocol for isolation/recovery. Calling every wait a lock wait obscures ownership and remedies.

MVCC does not eliminate locks. Versioned reads may avoid `S` row locks, while writers still coordinate write/write conflicts, uniqueness, foreign keys, schemas, relation access, and predicate dependencies. Serializable snapshot systems may track nonblocking predicate dependencies called predicate locks; these need not block like traditional locks. Explain mechanism precisely.

**Compatibility is a relation.** In the canonical teaching system, `S` and `S` coexist; `X` conflicts with every other owner's mode. Intention modes make hierarchy visible:

- `IS`: intends shared descendants;
- `IX`: intends exclusive/intention descendants;
- `SIX`: reads whole node under `S` and may update descendants under `IX` intent.

The matrix is symmetric for requests by different owners:

| held/requested | IS | IX | S | SIX | X |
|---|---:|---:|---:|---:|---:|
| IS | yes | yes | yes | yes | no |
| IX | yes | yes | no | no | no |
| S | yes | no | yes | no | no |
| SIX | yes | no | no | no | no |
| X | no | no | no | no | no |

Compatibility does not specify fairness, queue bypass, conversion priority, duration, deadlock policy, or isolation. It is one component. Product matrices can include update (`U`), schema, bulk, key-range composites, access-share/exclusive families, metadata, or transaction-ID modes; never paste this table onto differently named modes.

**Multiple granularity.** Suppose hierarchy is database → table → partition/index/page → key/row/range. To take `S` or `IS` on node, hold `IS` on ancestors. To take `X`, `IX`, or `SIX`, hold `IX` on ancestors. Acquire top-down so ancestor summaries exist before descendants. In a classical protocol, release bottom-up so an ancestor intent is not removed while descendants remain. Two-phase/duration rules add further restrictions.

Why it works: a table `S` must conflict with any descendant writer. Each writer first takes table `IX`; table `S` conflicts with `IX`, so the lock manager checks only the table queue rather than every descendant. Meanwhile two transactions with table `IX` may update distinct rows because `IX`/`IX` is compatible; their row `X` requests decide actual conflict.

An intention lock is not a coarse data lock. Table `IX` does not grant permission to modify every row without row/key `X` locks under this model, and it does not block another table IX. Table IS does not freeze the table. Operational dashboards should distinguish “granted intent” from blocker.

**Granularity tradeoff.** Fine locks maximize concurrency among disjoint resources but cost lock-table memory, hashing, CPU, queue bookkeeping, log/recovery metadata, and deadlock graph size. Coarse locks reduce overhead and can improve scans/batches but block unrelated work. Page locks are implementation-oriented and may couple unrelated rows; row/key locks align better with logical identity but can be numerous. Partition locks can fit independent tenant/time slices only if invariants and routing do not cross partitions.

The optimizer/lock manager may choose granularity dynamically using estimated/observed cardinality and memory. Hints alter one input and are not durable proof: plan changes can change visited keys, and some engines can escalate despite initial row hints. Benchmark representative concurrency, not one session.

**Escalation.** When a transaction holds many descendant locks, the engine may request a covering ancestor mode—many row S to table S; mixed/writes to X or another sufficient mode—then release descendants only after grant. This preserves coverage. If ancestor conversion conflicts, policies may keep acquiring fine locks, wait, fail, or retry escalation. Releasing first creates a correctness window.

Escalation reduces lock memory/CPU but increases blocking. Disabling it can cause lock-resource exhaustion. Raising thresholds can shift failure rather than fix a transaction scanning/modifying too much. Remedies include smaller invariant-safe batches, better predicates/indexes, partitioning, snapshot/versioned reads where semantics permit, shorter transactions, or planned coarse locking during a maintenance window. Do not split an atomic invariant merely to avoid escalation.

**Conversion and update mode.** A transaction may read under S then decide to write, needing X. If T1 and T2 both hold S and both request X, each waits for the other's S: conversion deadlock. Some systems provide update (`U`) mode, compatible with readers but usually only one updater, then convert U→X. It prevents a common upgrade pattern, not every deadlock. Alternatively acquire X/locking-read from the start when write intent is known, sacrificing read concurrency to make ordering explicit.

Lock conversion should be treated as acquisition of the combined/stronger mode while retaining prior coverage. Downgrade/release timing must obey isolation and recovery. Converting row modes and ancestor intentions may require coordinated hierarchy changes.

**Predicate and key-range locking.** Row locks protect existing identities. Query `WHERE 10<key<20` also depends on gaps where new keys could appear. Serializable locking implementations use key-range/next-key/gap/predicate mechanisms based on access path and boundaries. Endpoints, equality on missing key, duplicates, NULL/collation/operator class, index selection, and partitioning determine coverage.

Current InnoDB documents record, gap, next-key, insert-intention, and intention locks. A next-key lock combines an index-record lock with the preceding gap; gap locks can coexist because their purpose is preventing inserts, and insert-intention locks allow nonconflicting inserts within a gap. Unique-index equality can narrow locking compared with ranges. Spatial indexes need predicate locking because linear next-key order is not suitable.

Current SQL Server documents key-range locks under serializable isolation and a larger product-specific mode lattice. PostgreSQL Serializable uses predicate-lock dependency tracking that does not cause blocking like conventional locks; current explicit locking docs separately define table/row/advisory modes. “Predicate lock” therefore does not imply one universal implementation.

**Duration and isolation.** A lock's mode/resource does not state how long it is held. Shared read locks may be statement duration under Read Committed, transaction duration under Repeatable Read/serializable locking, or absent for versioned reads. Write locks are often retained to transaction end for strictness/recovery, but current SQL Server optimized locking changes detailed row/page retention using transaction-ID locks. Table/schema locks have distinct acquisition/duration rules.

The next module formalizes two-phase locking. Here, record `acquired_at`, `granted_at`, `released_at`, and reason. Early release can expose nonrepeatable/rollback interactions; long duration increases blocking/deadlocks. The correct duration follows the isolation/recovery contract, not a global “release ASAP.”

**Wait policies.** An incompatible request can block, return immediately (`NOWAIT`), skip locked resources, time out, or be aborted as deadlock victim. `SKIP LOCKED` intentionally omits locked rows and suits competing queue claimers, not complete reports. `NOWAIT` turns contention into an explicit error; the application must retry/choose policy. A timeout is not proof of deadlock and can leave an aborted/active transaction depending on engine/statement behavior.

Fairness matters. Strict FIFO avoids starvation but can create convoy/head-of-line blocking when a queued X prevents later compatible S grants. Reader preference can starve writers; writer preference can spike reads. Conversion requests may need priority to avoid deadlock/starvation. Observe policy rather than assuming.

The following executable model uses the canonical five-mode table and two-level resources. It omits conversion, hierarchy validation, duration, fairness, deadlock, and product modes, but makes compatibility decisions transparent.

<!-- bijux-verify: {"id":"multiple-granularity-compatibility","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"IS=IS,IX,S,SIX\nIX=IS,IX\nS=IS,S\nSIX=IS\nX=-\nt1_table_is=True\nt2_table_ix=True\nt3_table_s=False\nt4_row_a_x=False\nwaiting=(('T3', 'table', 'S'), ('T4', 'row_a', 'X'))\ninvariants=True\n","stderr":""}} -->
```python
modes = ("IS", "IX", "S", "SIX", "X")
compatible = {
    "IS": {"IS", "IX", "S", "SIX"},
    "IX": {"IS", "IX"},
    "S": {"IS", "S"},
    "SIX": {"IS"},
    "X": set(),
}
granted: dict[str, list[tuple[str, str]]] = {}
waiting: list[tuple[str, str, str]] = []


def request(owner: str, resource: str, mode: str) -> bool:
    holders = granted.setdefault(resource, [])
    allowed = all(
        held_owner == owner or held_mode in compatible[mode]
        for held_owner, held_mode in holders
    )
    if allowed:
        holders.append((owner, mode))
    else:
        waiting.append((owner, resource, mode))
    return allowed


for mode in modes:
    permitted = ",".join(candidate for candidate in modes if candidate in compatible[mode])
    print(f"{mode}={permitted or '-'}")

t1_table_is = request("T1", "table", "IS")
assert request("T1", "row_a", "S")
t2_table_ix = request("T2", "table", "IX")
assert request("T2", "row_b", "X")
t3_table_s = request("T3", "table", "S")
assert request("T4", "table", "IX")
t4_row_a_x = request("T4", "row_a", "X")

print(f"t1_table_is={t1_table_is}")
print(f"t2_table_ix={t2_table_ix}")
print(f"t3_table_s={t3_table_s}")
print(f"t4_row_a_x={t4_row_a_x}")
print(f"waiting={tuple(waiting)}")
print(
    "invariants="
    f"{t1_table_is and t2_table_ix and not t3_table_s and not t4_row_a_x and len(waiting) == 2}"
)
```

The model assumes caller obeys ancestor requirements; it does not prove them. Same-owner modes are simply allowed rather than correctly converted/combined. It is not an implementation of PostgreSQL, InnoDB, SQL Server, a lock queue, or concurrency.

**Advisory/application locks.** These map an application-chosen key to engine/session/transaction lock machinery. They can serialize work whose conflict is awkward to represent as a row, such as one job per tenant-period. Correctness requires canonical collision-resistant identity, namespace/version, consistent acquisition order, correct session versus transaction scope, connection-pool discipline, bounded timeout, and cleanup after errors/disconnect. Advisory locks do not automatically protect table rows from code that ignores them, and a hash collision can create false contention—or unsafe aliasing if encoding is ambiguous.

Prefer database constraints/row locks when the invariant naturally lives in data. Use advisory locks when all writers share a controlled protocol and document that dependency. Never hold a session advisory lock on one pooled connection while assuming a transaction on another owns/releases it.

**Observability and diagnosis.** Capture waiter transaction/session, blocker, requested/held mode, resource type/identity/hierarchy, wait start/duration, conversion flag, query/plan, transaction age/isolation, application command/tenant class, and lock count/memory/escalation. Redact values. Build a wait-for graph over a consistent-enough sample and correlate with completed query/transaction telemetry.

One `pg_locks` or product DMV snapshot races with grant/release and may show fast transient locks incompletely. A blocker can itself wait on another resource. The oldest transaction is not necessarily root cause; query plan/cardinality, missing index, batch size, hot key, inconsistent ordering, or external wait inside transaction may be causal. Confirm with repeated traces and the actual current engine documentation.

**Testing.** Unit-test the compatibility matrix for symmetry and intended conflicts; hierarchy validator for every leaf mode; conversion lattice; escalation no-gap invariant; canonical resource encoding; and timeout cleanup. Integration-test separate sessions: compatible row operations proceed, same-row conflict waits, table coarse request sees descendant intent, absent-range inserts block/abort as promised, conversion deadlock is detected, escalation succeeds/fails safely, cancellation releases correct scopes, connection pooling resets state, and recovery releases/reconstructs locks according to engine rules.

Performance tests vary rows/ranges, selectivity/index plan, concurrency, read/write mix, transaction duration, memory pressure, isolation/versioned reads, and hot-key skew. Measure throughput, p50/p99, waits, deadlocks, aborts/retries, lock count/memory, escalation, latches, CPU, I/O, and invariant oracle. A lower lock count with worse table blocking is not automatically better.

## Definitions and Notation

- `R`: logical resource in a containment tree; `parent(R)` is its ancestor.
- `M={IS,IX,S,SIX,X}`: canonical teaching modes; product sets may differ.
- `Compat(m,n)`: symmetric compatibility predicate for different owners on the same resource.
- `Held(T,R,m)`: transaction T has granted mode m on R; `Wait(T,R,m)` is queued/ungranted.
- `join(m,n)`: least mode covering both same-owner requirements when the product lattice defines it.
- **Conversion:** same owner requests a stronger/combined mode while retaining coverage.
- **Escalation:** replace many descendant locks with sufficient ancestor protection.
- **Key-range lock:** protects ordered keys plus a defined gap/range boundary.
- **Predicate lock/tracking:** protects or records dependency on a logical predicate, potentially without blocking.
- **Lock footprint:** count/types/duration/memory/resources held or waited on by a transaction/statement.
- **Convoy:** compatible/short work queues behind a blocked/incompatible head under policy.
- **Starvation:** an eligible request waits unboundedly because other requests repeatedly bypass it.

## Mechanisms, Invariants, or Proof Structure

Hierarchy safety follows from intention advertisement. Assume every descendant X writer holds IX on each ancestor. A transaction requesting S on ancestor A is granted only if compatible with every A holder. Since `Compat(S,IX)=false`, no descendant writer can coexist unseen. Similar reasoning covers ancestor X, which conflicts with every intention/read mode. The proof fails if a participant skips ancestors or resource identities disagree.

Fine-grained concurrency follows because IX/IX coexist at an ancestor; disjoint leaf X locks occupy distinct resources and therefore do not conflict. If both target one leaf, X/X conflicts. Thus the hierarchy summarizes possible descendant conflicts without falsely serializing all writers at the table.

Escalation safety requires acquiring/confirming coarse mode C whose protected set includes every descendant lock before releasing descendants. During overlap, protection is redundant but safe; release-before-grant creates an interval with neither coverage. C must be at least the join of descendant access needs: escalating mixed S/X descendants to S would lose write exclusion.

Predicate safety requires set coverage, not row enumeration: any concurrent insertion/update whose new key would enter protected predicate P must conflict or create a validated dependency. If the chosen index/order/collation encodes a different range than P, the proof is incomplete. Observe exact engine behavior for residual predicates and multiple access paths.

## Alternatives and Trade-Offs

- **Fine versus coarse:** fine improves disjoint concurrency at lock-memory/CPU/deadlock cost; coarse reduces overhead at blocking/latency cost.
- **Row/key versus page:** logical key/row aligns with application conflicts; page reduces count but couples unrelated records and physical reorganization.
- **Blocking locks versus MVCC reads:** locks prevent changes/ensure current decision but block; snapshots avoid reader/writer blocking but may need validation/SSI for write skew.
- **S then conversion versus U/X intent:** S maximizes initial readers but risks conversion deadlock; U/X announces write intent earlier at concurrency cost.
- **Range locks versus serializable predicate tracking:** range locks block conflicting inserts; SSI-style tracking preserves nonblocking reads but aborts dangerous histories and consumes tracking memory.
- **Escalation versus batching:** escalation preserves one large atomic transaction with coarse blocking; batches reduce footprint only if each commit leaves a valid workflow state.
- **Engine-managed versus advisory:** native locks integrate with rows/plans/constraints; advisory locks model custom conflict but require universal application discipline.
- **Wait versus NOWAIT/SKIP:** wait preserves requested semantics but adds tail/deadlock; NOWAIT exposes contention; SKIP intentionally changes result membership.

## Failure Modes and Misconceptions

- “IX locks the whole table exclusively.” IX announces descendant writes and is compatible with other IX.
- “IS protects all rows for reading.” It only announces shared locks below.
- “Row locking needs no table lock.” Multiple-granularity protocols use ancestor intentions.
- “Locks and latches are synonyms.” They protect different identities/durations/layers.
- “MVCC removes locking.” Writers, schemas, constraints, and serializable dependencies still coordinate.
- “Lock returned rows to prevent phantoms.” Absent keys/gaps/predicate membership also matter.
- “Escalation releases rows then requests table.” Correct escalation secures coarse coverage first.
- “Disable escalation for concurrency.” Unbounded lock memory/CPU can fail the system.
- “A row hint guarantees row locks.” It may alter initial choice while escalation/plan/product rules remain.
- “Timeout proves deadlock.” It proves a deadline elapsed; deadlock requires a wait cycle.
- “SKIP LOCKED is faster SELECT.” It deliberately omits locked rows and changes semantics.
- “Advisory locks protect the database.” Only cooperating code and correctly scoped ownership honor them.

## Worked Examples

### Example 1

T1 table IS+row A S and T2 table IX+row B X coexist. Conclusion: intention compatibility enables disjoint row concurrency while advertising descendant access.

### Example 2

T3 requests table S while T2 holds table IX for row B X. It waits without scanning the row-lock table. Conclusion: ancestor intent is a conflict summary, not a data lock.

### Example 3

Two transactions hold S on the same row and each converts to X. Each waits for the other's S. Conclusion: conversion can deadlock; use update/write intent or deterministic victim/retry.

### Example 4

A transaction holds 20,000 row S locks and escalates to table S. Another transaction's table IX blocks conversion, so descendants remain held until later retry. Conclusion: failed escalation must not create a protection gap.

### Example 5

Query finds no reservation in `[10,20)`, so there are no row locks. Concurrent insert at 15 succeeds and breaks a nonoverlap check. Conclusion: lock/validate the gap/range/predicate or use an exact exclusion mechanism.

### Example 6

InnoDB next-key protection covers record 20 plus preceding gap; two insert-intention requests for distinct keys may coexist before their row X locks. Conclusion: gap-related mode compatibility serves insertion concurrency and cannot be inferred from S/X alone.

### Example 7

Batch forces row locks to “avoid blocking,” exhausts lock memory, and fails; table lock would have completed within a maintenance window. Conclusion: granularity is a workload/resource tradeoff, not a moral ranking.

### Example 8

Workers use `SKIP LOCKED` to claim different jobs; missing locked jobs are intended. An audit count using the same clause is incomplete. Conclusion: wait policy is part of result semantics.

### Example 9

Service takes advisory key `tenant + ':' + date`; ambiguous escaping maps two tuples to one string and causes false serialization. Conclusion: use canonical typed/bounded encoding and namespace/version collision analysis.

### Example 10

A B-tree page split briefly latches pages while transaction key locks remain until commit. Removing the latch corrupts structure; releasing logical lock permits anomaly. Conclusion: structural latches and transactional locks are complementary layers.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies mutex/latch semantics, fairness, starvation, atomics, and lock ordering.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies B-tree key/page hierarchies, ranges, splits, and identity.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies resource wait queues, scheduling, priority, memory pressure, and diagnostics.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies leases/fencing and why remote coordination differs from local locks.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies conflict responses, deadlines, retries, idempotency, and queue claiming.

## References

1. PostgreSQL Global Development Group, [Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html), current table, row, page, deadlock, and advisory lock semantics.
2. PostgreSQL Global Development Group, [Viewing Locks](https://www.postgresql.org/docs/current/view-pg-locks.html), current `pg_locks` interpretation and blocker-observation guidance.
3. Oracle, [MySQL 8.4 InnoDB Locking](https://dev.mysql.com/doc/refman/8.4/en/innodb-locking.html), current shared/exclusive, intention, record, gap, next-key, insert-intention, AUTO-INC, and predicate locks.
4. Oracle, [MySQL 8.4 Locking Reads](https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-reads.html), current `FOR SHARE`, `FOR UPDATE`, `NOWAIT`, and `SKIP LOCKED` behavior.
5. Microsoft, [Transaction Locking and Row Versioning Guide](https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-locking-and-row-versioning-guide?view=sql-server-ver17), current SQL Server resource hierarchy, modes, compatibility, key ranges, and escalation.
6. Jim Gray, Raymond Lorie, Gianfranco Putzolu, and Irving Traiger, [“Granularity of Locks and Degrees of Consistency in a Shared Data Base”](https://www.cs.cmu.edu/~15721-f24/papers/Granularities_of_Locking.pdf), IFIP Working Conference on Modelling in Data Base Management Systems, 1975.
7. Goetz Graefe, [“A Survey of B-Tree Locking Techniques”](https://people.eecs.berkeley.edu/~kubitron/courses/cs262a-F13/handouts/papers/a16-graefe.pdf), *ACM Transactions on Database Systems* 35(3), 2010; DOI `10.1145/1806907.1806908`.
8. C. Mohan and Frank Levine, [“ARIES/IM: An Efficient and High Concurrency Index Management Method Using Write-Ahead Logging”](https://research.ibm.com/publications/ariesiim-an-efficient-and-high-concurrency-index-management-method-using-write-ahead-logging), *SIGMOD*, 1992.
9. Michael J. Cahill, Uwe Röhm, and Alan D. Fekete, [“Serializable Isolation for Snapshot Databases”](https://www.cs.cornell.edu/~sowell/dbpapers/serializable_isolation.pdf), *SIGMOD*, 2008, nonblocking predicate dependency tracking.
10. Philip A. Bernstein, Vassos Hadzilacos, and Nathan Goodman, [*Concurrency Control and Recovery in Database Systems*](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/05/ccontrol.zip), Addison-Wesley, 1987, formal locking and concurrency-control foundations.

## Exercises

### Exercise 1

Reconstruct the canonical compatibility matrix from each mode's meaning, prove symmetry, and trace grants/waits for table/row requests including `SIX` and one conversion.

### Exercise 2

Given database→table→partition→index→key resources, validate or repair ten lock sequences. State required ancestor modes, acquisition/release order, and protected logical domain.

### Exercise 3

Diagnose a batch with lock-memory growth, repeated failed escalation, table blocking, conversion deadlocks, and p99 regression. Separate correctness constraints from performance mitigations.

### Exercise 4

Design exact protection for empty-key uniqueness, interval nonoverlap, tenant quota, and queue claiming using constraints, rows/guards, ranges/predicates, advisory locks, or serializable validation; compare failure semantics.

### Exercise 5

Design a cross-engine test/observability program for lock modes and granularity, including compatibility, hierarchy, conversions, phantoms, escalation, cancellation, deadlocks, pooling, recovery, privacy, and limitations.

## Answers to the Exercises

### Answer 1

IS announces shared descendants, so it coexists with IS/IX/S/SIX but not ancestor X. IX announces possible exclusive descendants, so it coexists only with IS/IX; ancestor S/SIX/X would promise conflicting broad read/write exclusion. S coexists with IS/S but not IX/SIX/X. SIX combines S+IX, so only IS coexists. X conflicts with all other owners. The table is symmetric. Trace same resource against every granted other-owner mode, not only queue head unless policy says so. Same-owner S→X is conversion: retain S while requesting X; another S holder blocks it and two mutual converters can deadlock. Product U/schema/range modes require their own matrix.

### Answer 2

For leaf S, acquire IS on database/table/partition/index top-down; for leaf X acquire IX on all ancestors. Node SIX needs IX ancestors. A transaction cannot take key X with only table IS, cannot release table IX while descendant X remains, and cannot jump directly to a partition if ancestor protocol is enforced. Release descendants before ancestors under the classical hierarchy, additionally respecting 2PL/strict duration. Resource identity must follow actual containment: a secondary-index key and base row may be separate resources, and a predicate may span partitions/index ranges. Repair sequences by acquiring missing intentions before descendants; if changing modes, convert ancestor first while retaining old coverage. State whether protection is row identity, index key, gap, or whole predicate.

### Answer 3

Preserve atomicity/isolation and required write-lock duration first. Capture transaction/query/plan, row/range counts, modes/resources, lock memory, escalation attempts/conflicting table holders, wait graph, conversion sites, isolation, duration, retries, p99, and invariant oracle. Failed escalation must retain fine locks; do not release to “unstick.” Mitigations: better predicate/index to touch fewer keys; deterministic acquisition/update-intent to remove conversion pattern; shorter nontransactional preparation; smaller commits only if each is valid/restartable; partition-aligned work; versioned reads where semantics allow; planned coarse lock; or capacity/rate limit. Disabling escalation risks memory exhaustion; forcing row locks risks the same. Test one change at representative concurrency and include deadlock/retry/rollback cost.

### Answer 4

Empty-key uniqueness: native unique constraint is strongest/simple; locking no returned row is insufficient. Interval nonoverlap: native exclusion/range constraint where available, otherwise serializable predicate/key-range or canonical interval guard with proof. Tenant quota: lock/atomic-update one tenant-period counter/guard, exact materialized units, or serializable predicate over reservations; guard hotspots trade concurrency for clear conflict. Queue claim: atomic update/locking read with `SKIP LOCKED` is appropriate because omission is intended; add status/lease/fencing if work leaves transaction. Advisory locks can serialize a canonical tenant/interval resource only if all writers comply and scope/pooling are correct. Every design specifies timeout/abort, retry identity, deadlock order, nonexistent members, cleanup, and reconciliation.

### Answer 5

Pin engine/version/config/isolation and use separate explicit connections. Unit-test the documented product compatibility modes plus canonical model; integration-test disjoint row compatibility, same-row conflict, table request versus descendant intentions, S→X conversion, empty/range insert, NOWAIT/SKIP semantics, escalation under count/memory, cancel/timeout, deadlock victim, connection loss/pool reset, and recovery. Use barriers/hooks rather than sleeps and assert grants/waits/errors/final invariant. Capture waiter/blocker graph, mode, resource hierarchy, conversion, query/plan, transaction age, lock count/memory, escalation, abort/retry, p99 and latches, with hashed tenant/command identity and no sensitive key values. Compare current PostgreSQL/MySQL/SQL Server behavior without forcing identical names. Report snapshot races, inaccessible internal latches, destructive tests not run, schedule coverage, and that passing sampled histories is not a proof of universal correctness.
