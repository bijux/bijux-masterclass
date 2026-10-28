---
module_id: DBE-046
program: Database Engineering
level: 1
module_number: 46
title: Multi-Version Concurrency Control
status: complete
last_verified: 2026-08-30
---

# Multi-Version Concurrency Control

## One-Page Review

### Governing question

How can a database retain several logical versions of an item so readers obtain a transactionally meaningful past state while concurrent writers advance the current state, without losing correctness or allowing history to grow without bound?

### Essential definitions

**Multi-version concurrency control (MVCC)** is a family of mechanisms in which a logical write creates or makes reconstructible a new version rather than immediately destroying every prior readable image. A **version** is a value plus identity and metadata sufficient to decide creation, invalidation/supersession, transaction outcome, and visibility. A **snapshot** describes which transaction effects a reader may observe; it may be represented by a timestamp, sequence number, high-water mark plus active set, or another engine-specific structure. A **visibility rule** chooses at most one appropriate version of a logical row for a reader and treats deletion as versioned state. A **version chain** relates newer and older images. A **write conflict** coordinates concurrent attempts to change the same logical item. The **reclamation horizon** (safe point/oldest-needed boundary) summarizes the oldest state still possibly required by active snapshots, rollback, replicas, backups, or time-travel policy. **Vacuum/purge/version cleanup** makes obsolete versions and index entries reclaimable only after those obligations end.

### Central model, mechanism, or theorem

In a simplified commit-sequence model, each committed version v has `commit(v)` and a logical key. A reader at snapshot s chooses the version for that key with greatest commit sequence `<= s`; it excludes aborted and still-active versions from other transactions, while normally seeing its own earlier writes through a transaction-local rule. A writer creates a candidate successor, coordinates with concurrent writers, and publishes its outcome atomically at commit. Old readers continue using earlier committed versions; new readers can use the successor. Thus read/write overlap can avoid S-versus-X row-lock blocking.

This mechanism alone does not define an isolation level or prove serializability. Statement snapshots, transaction snapshots, first-updater/committer-wins rules, predicate conflict handling, and serializable validation yield different histories. MVCC can still permit write skew, stale decisions, phantoms, deadlocks among writers, schema blocking, and version-store exhaustion. Correctness is the composition of visibility, write-conflict policy, transaction outcome, predicate treatment, and recovery.

### Critical invariants

- Every physical version maps unambiguously to a stable logical item and has durable creator/outcome/ordering metadata.
- A reader selects only versions allowed by its exact snapshot and transaction-local writes; aborted/uncommitted other-owner versions never leak.
- At most one version of one logical item is returned for a normal point read, including deletion/tombstone semantics.
- Commit publishes version outcome/order consistently with WAL/recovery; abort leaves no version visible to other transactions.
- Concurrent writers coordinate on the logical item or validate conflicts before commit; versions do not make conflicting writes safe automatically.
- Index lookup and heap/version-chain traversal implement the same visibility and logical-key semantics.
- Cleanup reclaims a version only when no active or retained reader, rollback, replica, backup, online operation, or policy can require it.
- Version identifiers/timestamps handle wraparound, reuse, clock/order, and status lookup without misclassifying past as future.

### Common failures

Failures include equating MVCC with snapshot isolation or serializability; saying readers and writers “never block”; using wall-clock time as a visibility proof; ignoring the active-transaction set around a snapshot boundary; exposing a candidate before commit status is durable; treating deletes as immediate physical removal; allowing two writers to publish incompatible successors; checking a multirow invariant from one snapshot without predicate/conflict protection; reclaiming from minimum query start time alone; forgetting idle transactions/replicas/backups that pin history; assuming indexes are version-neutral; letting long snapshots create undo/version-store bloat; confusing visibility metadata with user audit history; and applying PostgreSQL, InnoDB, or SQL Server storage details to another engine.

### Compact example

Logical account A has committed versions `v1=(ts1,100)`, `v2=(ts4,120)`, and `v3=(ts7,135)`. Snapshots 3, 5, and 8 read 100, 120, and 135. T4 creates uncommitted `v4=150`: T4 can read its own candidate, while T5 at snapshot 10 still reads 135. If active snapshots are 5 and 8, the safe horizon is 5. `v1` can be reclaimed because committed successor v2 was already visible by 4; v2 must remain for snapshot 5, v3 for newer readers, and active v4 for T4/rollback. This scalar model is intentionally smaller than real active-set snapshots.

### Connections

Retrieve [Two-Phase Locking](044-two-phase-locking.md), [Read and Write Anomalies](042-read-and-write-anomalies.md), and [Index Maintenance and Write Amplification](039-index-maintenance-and-write-amplification.md). Continue through the Database Engineering [roadmap](../ROADMAP.md) to DBE-047, Snapshot Visibility, DBE-048, Isolation Levels, and DBE-049, Serializable Isolation.

## Governing Question

Which version should each read observe, how do concurrent writes and transaction outcomes safely change the version graph, and when can obsolete history be reclaimed without invalidating a legitimate observer?

## Why This Matters

Single-version locking forces a choice: a reader holds protection against overwriting, or a writer may destroy the exact state the reader needs. MVCC changes the storage/concurrency geometry. The writer can preserve an older readable image while producing a successor, so a reader of an earlier snapshot need not wait merely because the current row is changing.

That benefit underpins analytical queries alongside OLTP, consistent backups, online operations, replica snapshots, and row-versioned isolation. It also moves cost rather than removing it. Each update creates version metadata and often additional storage, cache traffic, index work, undo/redo, and cleanup. Long readers can pin history. A version chain can become expensive to traverse. Running out of version-store or transaction-ID safety margin becomes an availability risk.

The phrase “MVCC database” is therefore incomplete. PostgreSQL keeps multiple heap tuple versions and cleans dead tuples with vacuum; InnoDB keeps current clustered records with roll pointers and reconstructs earlier images from undo; SQL Server can chain previous images through a version store. Each combines versioning with locks, latches, transaction status, indexes, recovery, and isolation-specific policy.

Engineers must reason at two levels. The durable abstract model explains version identity, snapshot, visibility, write conflict, outcome, and safe reclamation. Current vendor documentation explains where bytes live, when snapshots are taken, what still locks, how cleanup is observed, and what configuration changes semantics.

## Prerequisites and Retrieval

You should understand transaction boundaries/outcomes, conflict serializability, read/write anomalies, two-phase locking, B+ tree indexes, WAL/undo, and finite ordered sets. Retrieve logical versus physical identity, snapshot, transaction ID, commit sequence, active set, tombstone, write skew, phantom, index entry, garbage collection, safe point, and crash recovery.

This module gives the cross-engine MVCC architecture. DBE-047 derives visibility using transaction states and snapshot boundaries in greater detail. DBE-048 compares isolation-level contracts; DBE-049 handles serializable enforcement; later recovery modules develop WAL, undo, redo, and checkpoints.

## Learning Objectives

After this module, you can:

1. separate MVCC mechanism from isolation-level and serializability guarantees;
2. model logical items, physical versions, version order/chains, transaction outcome, snapshots, and visibility;
3. trace inserts, updates, deletes, own writes, commits, aborts, and concurrent writers;
4. explain append-version, undo-reconstruction, and external version-store physical designs;
5. derive a safe reclamation horizon and identify every history-pinning obligation;
6. reason about indexes, key changes, tombstones, HOT-like optimizations, and cleanup amplification;
7. diagnose write skew, lost-update policy, stale decisions, phantom domains, and writer deadlocks under MVCC;
8. interpret current PostgreSQL, InnoDB, and SQL Server MVCC behavior without false portability;
9. design metrics and incident response for version bloat, chain depth, cleanup lag, wraparound, and space exhaustion; and
10. test visibility, write conflict, recovery, cleanup, and boundary races with independent oracles.

## Core Exposition

**Start with a logical history, not a product layout.** A table row is a logical item identified by a durable key/row identity. Its physical history contains versions `v0,v1,...`. A version stores value plus enough metadata to establish who created it, whether creation committed/aborted/remains active, when it belongs in the serialization/visibility order, and whether a later version/delete supersedes it. Links may run newest-to-oldest or live in separate undo records; the abstract order matters more than pointer direction.

An insert creates the first candidate. An update creates a successor while retaining a way to read the predecessor. A delete creates a deletion marker or marks a version deleted; physical bytes and index entries cannot necessarily disappear until old readers no longer need the pre-delete state. An abort removes or marks the candidate invisible and restores any current representation. A commit makes the new logical state eligible under future snapshots at one defined publication point.

**Snapshots are logical visibility descriptions.** A scalar timestamp model is easy: snapshot s sees commits at or before s. Real systems often cannot use a scalar alone. A transaction that received a lower ID might still be active while a higher-ID transaction committed; a high-water mark plus an in-progress set distinguishes those outcomes. Commit sequence numbers can impose order but require atomic assignment/publication. Distributed systems need a causally/consistently obtained boundary rather than unsynchronized wall clocks.

Statement-level snapshots can change between statements, allowing nonrepeatable results while each statement is internally consistent. Transaction-level snapshots normally remain fixed, producing repeatable historical reads but pinning history longer. Own writes are usually overlaid so a transaction sees its earlier changes even when their commit is absent from the base snapshot. Locking/current reads may intentionally use a different path than consistent historical reads. State these rules; “snapshot” alone is not enough.

DBE-047 will formalize visibility around active, committed, aborted, creator/deleter, and boundary sets. For this module, the simplified rule is: among committed versions no later than snapshot, choose the newest; exclude other owners' uncommitted/aborted candidates; prefer an applicable own candidate. This is a teaching abstraction, not PostgreSQL `xmin/xmax`, InnoDB read-view, or SQL Server XSN pseudocode.

**Read path.** First locate candidate logical records through an index/table access path. Then apply visibility to tuple(s) or traverse from current representation toward older versions until finding the required image. Return no row if the selected state is a visible deletion or no visible creation exists. Avoid returning both old and new physical versions as two logical rows. Predicate scans must handle index entries whose heap versions are invisible, deleted, or require recheck.

A consistent read can avoid a shared row lock that conflicts with a writer because it reads an older immutable/reconstructible version. It can still wait on schema/metadata locks, buffer I/O, latches, page faults, recovery, remote storage, version fetch, or explicit locking reads. It may fail if required versions cannot be supplied. “Readers do not block writers and writers do not block readers” is a useful idealized data-row property, not a universal system statement.

**Write path.** A writer reads an appropriate base, obtains or validates authority to change the logical item, creates undo/version data, modifies indexes/current representation, records recovery information, and later commits or aborts. Two writers targeting the same logical row cannot blindly append incompatible successors. Engines lock, use compare-and-swap/validation, choose first-updater/first-committer-wins, or abort on detected conflict. Write/write deadlocks remain possible when transactions modify multiple items in different order.

The commit point must coordinate version outcome and recovery. Before commit, other transactions exclude the candidate. After durable commit/publication, snapshots whose policy includes it may select it. A crash between data write and outcome recovery cannot leave ambiguous visible state. MVCC uses transaction status and WAL/undo/redo; it does not replace recovery.

**MVCC is not an isolation level.** The same version store can implement statement-level read committed, transaction-level snapshot isolation, repeatable read variants, consistent backups, and serializable algorithms. The snapshot lifetime and conflict rules change the guarantee. Snapshot isolation prevents dirty reads and gives a consistent transaction snapshot under its formal model, yet disjoint writes based on a common predicate can both commit: write skew. Plain versions do not create a conflict edge for an absent row or multirow invariant.

Lost update behavior also varies. If two writers both derive a replacement from one old version, a write lock/validation rule may abort or serialize one; some lower isolation/read-modify-write sequences can still overwrite. Explicit atomic updates, constraints, locking reads, or serializable validation may be needed. A successful version lookup is not proof that an application invariant survived concurrent change.

**Physical version organizations.** In an append-version design, an update places a new tuple/image and the old tuple remains until vacuum/cleanup; indexes point to physical tuple locations and may accumulate dead entries. This simplifies historical images but consumes heap/index space and can scatter chains. PostgreSQL's documented MVCC/vacuum behavior is in this family, with implementation optimizations and transaction metadata beyond the abstraction.

In an undo-reconstruction design, the current clustered record is updated and points to undo records containing information needed to reconstruct earlier values. Traversing rollback pointers walks backward. InnoDB documents `DB_TRX_ID`, `DB_ROLL_PTR`, rollback segments, consistent reads, delete marking, and purge. Secondary indexes have different version metadata and can require clustered-record checks.

In an external version-store/copy-on-write design, the current row remains in the database and prior images are chained in a separate store. SQL Server documents previous committed images in a version store, with storage location depending on features such as accelerated database recovery. Snapshot and read-committed-snapshot policies choose transaction- versus statement-level historical state.

These categories can overlap. Engines compress/delta versions, keep short-lived versions in memory, optimize non-key updates, or move undo. Do not infer correctness/performance from layout name. Evaluate chain traversal, cache locality, write amplification, crash durability, cleanup, and index consistency.

**Indexes participate in MVCC.** Updating an indexed key usually creates new index membership and leaves old membership until safe cleanup, so scans must filter visibility. A non-key update may avoid touching some indexes if the engine can link versions locally (for example, a HOT-like optimization), but eligibility is engine/page-specific. Unique constraints must coordinate concurrent uncommitted candidates; a snapshot that cannot see another insert may still wait or fail uniqueness to preserve the constraint.

Secondary-index entries may lack complete visibility metadata, forcing a base-row/version lookup. Covering/index-only scans depend on whether pages/entries are known visible to all relevant readers. Deletes and key changes amplify index cleanup. Index bloat and stale entries are not merely storage issues: they increase scans, version checks, cache misses, and lock footprint.

**Safe reclamation is a reachability proof.** A version is obsolete for current state but may still be required by the oldest active snapshot, a transaction's own rollback, crash recovery, replica applying/reading older state, backup/online index operation, change-data capture, or retained time-travel/audit policy. Define the complete set of obligations O. A version may be reclaimed only if no member of O can legally select or reconstruct it and recovery no longer needs it.

In a total commit-sequence model, let `h = min(active snapshot sequences)`. A version whose committed successor is already at or before h can be unavailable to every active snapshot, provided there are no other pins and snapshots never move backward. If no snapshots exist, a current boundary can advance h. Real systems use richer horizons: transaction active sets, multiple databases, replicas, slots, undo, and recovery state. Never implement cleanup from a query's wall-clock age alone.

The executable model demonstrates selection and the simplified successor/horizon reclamation rule. `v4` is T4's uncommitted own write. It is visible only to T4 and cannot be reclaimed.

<!-- bijux-verify: {"id":"mvcc-visibility-and-reclamation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"snapshot_reads=((3, 100), (5, 120), (8, 135))\nown_write=150\nother_ignores_uncommitted=135\ngc_horizon=5\nreclaimable=('v1',)\nretained=('v2', 'v3', 'v4')\ninvariants=True\n","stderr":""}} -->
```python
versions = (
    {"id": "v1", "value": 100, "creator": "T1", "status": "committed", "commit_ts": 1},
    {"id": "v2", "value": 120, "creator": "T2", "status": "committed", "commit_ts": 4},
    {"id": "v3", "value": 135, "creator": "T3", "status": "committed", "commit_ts": 7},
    {"id": "v4", "value": 150, "creator": "T4", "status": "active", "commit_ts": None},
)

def visible_value(snapshot, viewer):
    own = [
        version
        for version in versions
        if version["creator"] == viewer and version["status"] == "active"
    ]
    if own:
        return own[-1]["value"]
    candidates = [
        version
        for version in versions
        if version["status"] == "committed"
        and version["commit_ts"] <= snapshot
    ]
    return max(candidates, key=lambda version: version["commit_ts"])["value"]

snapshot_reads = tuple((snapshot, visible_value(snapshot, "reader")) for snapshot in (3, 5, 8))
own_write = visible_value(8, "T4")
other_ignores_uncommitted = visible_value(10, "T5")
active_snapshots = (5, 8)
gc_horizon = min(active_snapshots)
committed = [version for version in versions if version["status"] == "committed"]
reclaimable = []
for position, version in enumerate(committed[:-1]):
    successor = committed[position + 1]
    if successor["commit_ts"] <= gc_horizon:
        reclaimable.append(version["id"])
retained = tuple(version["id"] for version in versions if version["id"] not in reclaimable)
reclaimable = tuple(reclaimable)
invariants = (
    snapshot_reads == ((3, 100), (5, 120), (8, 135))
    and own_write == 150
    and other_ignores_uncommitted == 135
    and reclaimable == ("v1",)
    and retained == ("v2", "v3", "v4")
)

print(f"snapshot_reads={snapshot_reads}")
print(f"own_write={own_write}")
print(f"other_ignores_uncommitted={other_ignores_uncommitted}")
print(f"gc_horizon={gc_horizon}")
print(f"reclaimable={reclaimable}")
print(f"retained={retained}")
print(f"invariants={invariants}")
```

**Cleanup and version debt.** PostgreSQL vacuum identifies dead tuples/index entries, reuses space, updates visibility metadata, and freezes sufficiently old transaction identities to prevent wraparound misclassification. InnoDB purge discards undo/delete-marked records only after no assigned read view could require them. SQL Server tracks the earliest useful sequence and removes older version-store entries subject to its feature/transaction rules. The names and exact thresholds differ; the invariant is retained-observer safety.

Long-running or forgotten idle transactions can hold the horizon while writes continue. Consequences include heap/index bloat, undo/history-list growth, temp/version-store pressure, slower chain traversal, cache churn, autovacuum/purge debt, replica lag interactions, wraparound emergency work, write throttling, and eventual read/write failure when space is exhausted. Killing the oldest transaction can free history but is a destructive operational decision: identify owner, workload, business purpose, rollback cost, replica/backup dependencies, and retry semantics first.

Capacity plan version generation rate times retention duration, with burst/skew/headroom and index/metadata overhead—not only table size. Observe per-database/table version/dead tuple generation, cleanup throughput/lag, oldest snapshot/transaction age, history horizon, chain depth, undo/version-store bytes, free space, autovacuum/purge work, wraparound/freeze age, replica/backup pins, aborted versions, and query latency/CPU/I/O. Alerts should connect the pinned owner to the growing storage surface.

**Correctness and recovery tests.** Use deterministic barriers: reader fixes snapshot; writer updates/commits; reader repeats and sees policy-defined state; new reader sees successor. Test active and aborted writers never leak; own writes do; concurrent same-row writers obey conflict policy; delete/reinsert/key change/unique/foreign-key/range cases preserve identity and constraints; statement versus transaction snapshots differ as documented; serialization validation catches dangerous histories when promised.

For cleanup, pin snapshots around every commit boundary, run cleanup, and verify each reader still obtains exactly its version. Release pins and verify reclamation eventually occurs. Inject crash before/after version data, commit record, status publication, index update, and cleanup marking; restart and compare committed state. Test ID wrap/freeze using supported harnesses rather than production manipulation. Space-exhaustion tests belong in isolated disposable environments.

Performance tests vary update rate, row width, indexed-column changes, chain depth, snapshot duration, read/write mix, hot-key skew, abort rate, storage latency, memory, cleanup capacity, and replicas. Report throughput and p50/p99 with version bytes, cleanup lag, chain steps, WAL/undo, cache/I/O, conflicts/deadlocks/aborts, and invariant oracle. A faster point read with unbounded version growth is not a production win.

## Definitions and Notation

- `x`: stable logical item/key; `V(x)` is its ordered physical/version history.
- `creator(v)`: transaction that produced candidate version v.
- `status(T) in {active, committed, aborted}`: transaction outcome known to visibility/recovery.
- `commit(v)`: publication/order value for a committed version in the simplified model.
- `S`: reader snapshot description; may include scalar boundary plus in-progress/exclusion set.
- `Visible(v,T,S)`: predicate allowing transaction T at snapshot S to select v.
- `LatestVisible(x,T,S)`: newest selectable state for x, with deletion producing absence.
- **Version chain:** navigable relation among current/prior physical images of one logical item.
- **Tombstone/delete marker:** versioned state saying the logical item is absent for applicable readers.
- **Write conflict:** concurrent candidate changes requiring lock, validation, abort, or deterministic order.
- `O`: complete retained-observer/recovery obligation set.
- **Reclamation horizon:** compact lower boundary derived from O; not sufficient if O is incomplete.
- **Version debt:** storage/work accumulated because generation exceeds safe cleanup.
- **Vacuum/purge:** engine-specific processes that identify/remove/reuse obsolete version and index state.
- **Write skew:** two transactions read a shared predicate and write disjoint items, jointly violating an invariant despite no same-row write conflict.

## Mechanisms, Invariants, or Proof Structure

**Selection proof in the scalar teaching model.** Committed versions of one item have unique increasing commit sequences. Snapshot s admits exactly those with commit `<=s`; choosing the maximum returns the item's last committed state at s. Later commits are excluded. Active/aborted other-owner candidates are excluded separately. An own active candidate overrides base history by transaction-local read-your-writes policy. Therefore each point read returns at most one logical state under the model.

**Simplified reclamation proof.** Let h be the minimum active snapshot and assume no other obligations, snapshots never move backward, and committed versions are totally ordered. If successor w of v has `commit(w)<=h`, every active snapshot s satisfies `s>=h>=commit(w)` and selects w or a later version, never v. Future snapshots are no earlier. Thus v is unreachable and reclaimable. If `commit(w)>h`, a snapshot between v and w may need v; retain it. Active own candidates and rollback state use separate rules.

The proof fails with an omitted old snapshot, replica, backup, time-travel request, rollback dependency, non-total/distributed order, or active-set semantics not reducible to h. Production cleanup must prove reachability against its actual O.

**Write safety argument.** Visibility alone selects historical reads but does not serialize successor creation. Require one logical-head authority or commit validation so incompatible concurrent candidates cannot both silently become the unique next state. For multiitem predicates, same-row authority is insufficient; constraints, predicate conflicts, or serializable validation must represent the invariant.

**Independent verification plan.** Recompute visible values from a separate interval/table representation; enumerate snapshots just before/at/after every commit; test own/other active and aborted cases; independently derive required-version sets for each retained observer; compare safe reclamation candidates; and then test physical chain/index cleanup. Separate model proof from current-engine observations.

## Alternatives and Trade-Offs

- **Single-version locking versus MVCC:** locking avoids retained history but blocks conflicting readers/writers; MVCC reduces data read/write blocking at version storage, lookup, status, and cleanup cost.
- **Append versions versus undo reconstruction:** append gives direct old images but grows heap/index state; undo keeps a current record and reconstructs history but can require long backward traversal and durable undo retention.
- **Inline versus external version store:** inline/local chains improve locality for some reads but bloat base pages; external stores isolate history but add pointers, separate capacity, and fetch I/O.
- **Statement versus transaction snapshot:** statement freshness reduces pin duration but permits changing results; transaction snapshot gives repeatability but retains history and can make decisions stale.
- **First-updater/committer-wins versus waiting locks:** abort/validation avoids some waits but wastes work; locking queues writers and can deadlock.
- **Snapshot isolation versus serializable MVCC:** snapshot isolation offers strong consistent reads and disjoint-write concurrency but permits write skew; serializable variants track/validate dependencies or lock predicates and may abort/block more.
- **Aggressive versus conservative cleanup:** aggressive cleanup controls space/chain cost but risks expensive coordination; conservative retention is safer against omitted pins but can exhaust storage.
- **Long snapshot versus materialized export:** one live snapshot gives consistent direct reads but pins history; copying/exporting a point-in-time dataset pays I/O/storage while releasing OLTP retention sooner.
- **Full-row versus delta versions:** full images speed reconstruction at space/write cost; deltas reduce storage but amplify chain CPU and corruption/recovery complexity.
- **Audit history versus MVCC history:** MVCC versions are internal and reclaimed; durable audit/temporal records need explicit schema, retention, security, and correctness contracts.

## Failure Modes and Misconceptions

- “MVCC is an isolation level.” It is a mechanism used by multiple isolation policies.
- “A timestamp alone is a snapshot.” Active lower-ID transactions and publication ordering may require an exclusion set/status.
- “Readers never block.” Schema, explicit locks, recovery, I/O, latches, missing versions, and product rules still block/fail.
- “Writers never block readers, so writers do not conflict.” Same-row and multi-resource writers still coordinate and deadlock/abort.
- “Snapshots are serializable.” Snapshot isolation can admit write skew unless additional mechanisms intervene.
- “Delete removes the row.” Historical readers/rollback/index cleanup can require old state.
- “Two physical tuples mean two rows.” Visibility must collapse versions to one logical state.
- “Indexes just point to the latest version.” Product index/version layouts differ and old memberships need filtering/cleanup.
- “Oldest SQL start time is the GC horizon.” Include every snapshot, recovery, replica, backup, online operation, and retention pin.
- “A long read is free.” It can pin gigabytes/terabytes of version debt and delay wraparound maintenance.
- “Vacuum/purge is optional housekeeping.” It is part of capacity and, for bounded identifiers, correctness/availability.
- “MVCC is an audit log.” Internal versions can disappear and lack business/user semantics.
- “Use wall-clock timestamps.” Clock/order anomalies and transaction publication require a database-defined logical order.
- “Lower cleanup thresholds always help.” Cleanup consumes CPU/I/O and cannot remove versions still reachable.
- “Copy vendor metadata fields into a portable algorithm.” `xmin/xmax`, roll pointers/read views, and XSN/version-store rules are not interchangeable.

## Worked Examples

### Example 1

Versions at commits 1, 4, 7 hold 100, 120, 135. Snapshots 3, 5, 8 choose the greatest commit not exceeding the snapshot. Conclusion: one chain supports different consistent historical reads concurrently.

### Example 2

T4 creates value 150 but has not committed. T4 reads 150 through own-write overlay; T5 reads committed 135. Conclusion: read-your-writes and isolation from other uncommitted candidates are separate visibility clauses.

### Example 3

T6's candidate aborts after an index entry was created. Cleanup/recovery makes it unreachable; no later snapshot selects it. Conclusion: version and index outcome must agree across abort/crash.

### Example 4

Two writers read 135 and both propose replacements. The engine validates the logical head; one commits and the other waits/aborts/retries. Conclusion: multiple versions do not license lost updates.

### Example 5

Two doctors each see the other on call and update different rows to off call. Both row writes are disjoint and can commit under snapshot isolation, leaving none. Conclusion: predicate/multirow invariants require serializable conflict handling or a canonical guard/constraint.

### Example 6

Reader at snapshot 5 remains active after commit 7. Cleanup cannot remove version 120 even though 135 is current. Conclusion: current state is not the same as oldest reachable state.

### Example 7

A forgotten read-only transaction pins InnoDB undo history while updates continue; chain traversal and undo storage rise. Conclusion: read-only can create write-side MVCC cost without taking row write locks.

### Example 8

Updating an indexed email creates new key membership and leaves old membership until safe cleanup. A scan encounters both but visibility returns one logical row. Conclusion: index amplification and visibility recheck are part of MVCC cost.

### Example 9

SQL Server RCSI gives each statement a fresh snapshot; SNAPSHOT fixes one for the transaction. Two SELECTs can differ in the first and repeat in the second, subject to documented exceptions. Conclusion: one version store supports different snapshot-lifetime contracts.

### Example 10

An export holds a six-hour transaction snapshot, filling version storage. A point-in-time materialized export copied early could release the OLTP snapshot sooner. Conclusion: choose retention architecture from consistency need plus capacity evidence.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies persistent structures, linked histories, reachability, garbage collection, B-trees, and cache-aware layout.
- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies immutable snapshots, publication, compare-and-swap, epochs/hazard-style reclamation, and memory-order reasoning.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies virtual-memory/page-cache pressure, background cleanup, writeback, scheduling, and resource exhaustion.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies logical clocks, consistent snapshots, replication horizons, leases, and distributed garbage collection.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) supplies consistent extraction, CDC, retention, compaction, and analytical snapshot workloads.

## References

1. Philip A. Bernstein and Nathan Goodman, [“Multiversion Concurrency Control—Theory and Algorithms”](https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15712-f17/www/papers/bernstein83.pdf), *ACM Transactions on Database Systems* 8(4), 1983; DOI `10.1145/319996.319998`.
2. Philip A. Bernstein, Vassos Hadzilacos, and Nathan Goodman, [*Concurrency Control and Recovery in Database Systems*](https://www.microsoft.com/en-us/research/people/philbe/book/), Addison-Wesley, 1987, multiversion histories, schedulers, and recovery.
3. PostgreSQL Global Development Group, [MVCC Introduction](https://www.postgresql.org/docs/current/mvcc-intro.html), current snapshot/multiversion concurrency overview.
4. PostgreSQL Global Development Group, [Routine Vacuuming](https://www.postgresql.org/docs/current/routine-vacuuming.html), current dead-version reuse, vacuum, freezing, and transaction-ID wraparound behavior.
5. PostgreSQL Global Development Group, [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html), current statement/transaction snapshots, anomalies, locking, and serializable behavior.
6. Oracle, [MySQL 8.4 InnoDB Multi-Versioning](https://dev.mysql.com/doc/refman/8.4/en/innodb-multi-versioning.html), current transaction IDs, roll pointers, undo reconstruction, deletion, purge, and indexes.
7. Oracle, [MySQL 8.4 Consistent Nonlocking Reads](https://dev.mysql.com/doc/refman/8.4/en/innodb-consistent-read.html), current read views, statement/transaction lifetime, own changes, and nonlocking reads.
8. Oracle, [MySQL 8.4 Purge Configuration](https://dev.mysql.com/doc/refman/8.4/en/innodb-purge-configuration.html), current history-list/purge behavior and long-snapshot effects.
9. Microsoft, [Transaction Locking and Row Versioning Guide](https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-locking-and-row-versioning-guide?view=sql-server-ver17), current version chains/stores, RCSI/SNAPSHOT, cleanup, space, and remaining locks.
10. Michael J. Cahill, Uwe Röhm, and Alan D. Fekete, [“Serializable Isolation for Snapshot Databases”](https://www.cs.cornell.edu/~sowell/dbpapers/serializable_isolation.pdf), *SIGMOD*, 2008, snapshot anomalies and serializable dependency tracking.

## Exercises

### Exercise 1

Given committed, active, aborted, own, deleted, and key-changed versions around four snapshot boundaries, determine the one logical result per key and justify every exclusion.

### Exercise 2

Prove the simplified newest-commit visibility and reclamation-horizon rules, then identify which assumptions fail for active-set snapshots, replicas, backups, or distributed clocks.

### Exercise 3

Design a deterministic MVCC implementation/test harness with transaction status, version chains, write conflict, commit/abort, index membership, crash points, and cleanup oracles.

### Exercise 4

Compare append-tuple, undo-reconstruction, and external-version-store layouts for a hot OLTP table plus six-hour analytical snapshot. Include capacity and failure tradeoffs.

### Exercise 5

Diagnose rising query latency, undo/version-store growth, dead tuples/index bloat, cleanup lag, and wraparound pressure. Produce a safe cross-engine response and prevention plan.

## Answers to the Exercises

### Answer 1

Establish snapshot representation and own-write rule first. For each logical key, exclude other-owner active and all aborted candidates; include committed creations allowed by the boundary/exclusion set; apply visible invalidation/deletion; overlay the reader's applicable own candidate; choose the newest remaining state exactly once. A deleted selected state returns absence, not an old row. A key change is deletion from old membership plus insertion/new membership and must not duplicate the logical row when both physical index entries are encountered. At boundaries test just-before, exactly-at, and just-after publication according to the engine's inclusive/order rule. Do not substitute transaction-ID numeric order for commit/visibility status unless the model defines it.

### Answer 2

With unique increasing commits, admitted versions at scalar s are exactly commits `<=s`; maximum is therefore the last committed state at s and unique. For horizon h=min active snapshots, if successor w commits `<=h`, all active/future snapshots are at least w and choose w/later, so predecessor v is unreachable; if w commits after h, an active snapshot may still choose v. Assumptions: total atomic commit order, monotonically advancing snapshots, no active lower-ID exclusions, no own/aborted/rollback complication, and complete observer set. An active-set snapshot can exclude a lower-ID transaction that later commits, so scalar comparison is insufficient. Replicas/backups/time travel can need state older than local active h. Distributed wall clocks may not define a consistent commit order. Use the engine's complete snapshot/horizon and all retention pins.

### Answer 3

Model stable logical key, immutable candidate versions, creator, transaction status, commit order, deletion, links, and index memberships. Atomically coordinate one logical write head or validate at commit. Readers use an independently specified visibility oracle, not the implementation method. Use barriers for active writer/read snapshot/commit/abort boundaries and enumerate all just-before/at/after cases. Assert read-your-writes, no dirty/aborted exposure, one logical result, same-row conflict, write-skew behavior promised by isolation, unique/range constraints, key changes, and deadlock/retry. Inject crash before/after version, index, WAL, commit/status, and cleanup marks; restart and compare committed oracle. Cleanup oracle computes every version required by active snapshots, own rollback, recovery, replicas/backups/test pins and forbids reclaiming their union. Then release pins and assert eventual reclaim. Measure chain steps/bytes/cleanup rather than treating test pass as performance proof.

### Answer 4

Append tuples make old images directly available but expand heap and indexes; hot updates scatter versions and vacuum must recover space. Undo reconstruction keeps the current clustered image compact and older changes often smaller, but six-hour readers force long undo retention and repeated reconstruction; secondary indexes can require base checks. An external store isolates old images and can serve chain traversal without base-page duplication, but needs separate high-availability capacity, pointer integrity, and failure behavior; six-hour retention can fill it. Estimate update bytes/s times six hours plus row/index/metadata, bursts, replicas/online operations, cleanup lag, and headroom. Benchmark hot current reads and historical scans, write/WAL/undo, cache/I/O, chain depth, cleanup, and failure at capacity. A materialized point-in-time analytical copy may release OLTP history earlier at transfer/storage cost.

### Answer 5

First identify the exact pins: oldest active/idle transaction and snapshot, query/application/session, replicas, backup/online index/CDC/time-travel, recovery, and configuration. Correlate version generation, dead tuples, history-list/version-store bytes/free space, chain depth, vacuum/purge throughput/lag, table/index bloat, XID/freeze age, WAL/undo, plans, CPU/I/O, and latency. Do not vacuum/purge away reachable state or kill a transaction blindly. If safe, cancel/finish the responsible forgotten transaction using its rollback/retry contract; restore cleanup capacity; add storage/headroom; throttle writes/admit snapshots during emergency; prioritize anti-wraparound requirements. Then shorten snapshot lifetime, move long analytics to replica/materialized snapshot where correct, tune table-specific cleanup from measured generation, repair indexes/plans, alert on oldest pin plus growth slope, and test space exhaustion/recovery in isolation. Map PostgreSQL vacuum/freeze, InnoDB undo/purge, and SQL Server version-store/ADR behavior separately; verify final data and visibility invariants, not only reclaimed bytes.
