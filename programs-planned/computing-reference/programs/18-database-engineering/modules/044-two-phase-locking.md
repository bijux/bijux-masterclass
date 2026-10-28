---
module_id: DBE-044
program: Database Engineering
level: 1
module_number: 44
title: Two-Phase Locking
status: complete
last_verified: 2026-08-30
---

# Two-Phase Locking

## One-Page Review

### Governing question

Which restrictions on acquiring and releasing logical locks are sufficient to make every admitted transaction history conflict-serializable, and which additional restrictions are needed for safe recovery and practical operation?

### Essential definitions

A **history** (schedule) is an interleaving of transaction operations that preserves each transaction's program order. Two operations **conflict** when they belong to different transactions, access the same logical item, and at least one writes. A history is **conflict-serializable** when repeatedly swapping adjacent nonconflicting operations can transform it into a serial history; equivalently, its precedence graph is acyclic. **Two-phase locking (2PL)** requires a transaction to acquire or strengthen locks only in a **growing phase** and, after its first unlock or weakening conversion, to release or weaken locks only in a **shrinking phase**. Its **lock point** is the position of its last successful lock acquisition or strengthening conversion. **Basic 2PL** imposes only that two-phase rule. **Conservative/static 2PL** obtains the entire declared lock set atomically before data operations. **Strict 2PL** additionally retains every exclusive/write lock through commit or abort. **Rigorous/strong-strict 2PL** retains all shared and exclusive locks through commit or abort. A **strict history** never lets another transaction read or overwrite an item written by an uncommitted transaction.

### Central model, mechanism, or theorem

Assume correct shared/exclusive compatibility, every conflicting data operation is covered by a lock on the same logical conflict domain, and lock operations themselves are atomic. If transactions obey basic 2PL, every admitted history is conflict-serializable. For any conflict edge `Ti -> Tj`, Ti's conflicting lock precedes Tj's incompatible lock. Tj cannot obtain its lock until Ti releases, and Ti cannot acquire any lock after that release. Therefore Ti's lock point precedes Tj's lock point. A cycle in the precedence graph would imply an impossible strict cycle among lock-point positions. Sorting transactions by lock point gives a serialization order consistent with every conflict edge.

That theorem does not make basic 2PL strict, deadlock-free, phantom-safe, starvation-free, or durable. Strict 2PL ties write-lock release to outcome and blocks dirty reads/writes; rigorous 2PL retains read locks too. Predicate/key-range resources are required when the conflict domain is a set rather than an existing row. Recovery, logging, commit, abort, deadlock handling, and retry remain separate mechanisms.

### Critical invariants

- Every read/write obtains a sufficient compatible lock before access on the same canonical logical resource or predicate domain.
- A transaction that has released or weakened any lock never later acquires or strengthens one.
- The recorded lock point is the final successful acquisition/upgrade, not request time, statement start, or commit time.
- A granted incompatible request cannot overlap another owner's held lock on the same resource.
- Strict 2PL retains X locks until commit/abort; rigorous 2PL retains both S and X locks until commit/abort.
- Abort restores data through the recovery protocol before—or atomically with—making protected uncommitted writes accessible.
- Hierarchical and predicate locking rules remain in force; 2PL orders locks but does not choose a complete conflict domain.
- Deadlock victimization, timeout, cancellation, and retry preserve atomicity and release every owned lock exactly once.

### Common failures

Common failures are equating serializability with strictness; releasing X locks before commit under “2PL” and permitting cascading aborts; treating commit as the lock point; claiming 2PL prevents deadlock; acquiring a new row after an early unlock; allowing an S-to-X upgrade during shrinking; locking returned rows but not gaps; confusing lock requests with grants; assuming lock-point order equals wall-clock start order; treating a product's MVCC-plus-locking behavior as pure textbook 2PL; holding locks across human or remote waits; retrying a deadlock victim without idempotency; and confusing two-phase locking with two-phase commit.

### Compact example

T1 obtains `X(A)`, writes A, obtains `X(C)` (its lock point), and releases `X(A)` before commit. T2 then obtains `S(A)` (its lock point) and reads T1's uncommitted value. Both transactions can obey basic 2PL because neither acquires after its first release; the only conflict edge is `T1 -> T2`, consistent with lock-point order. Yet the history is not strict. If T1 aborts, T2 has consumed a value that must disappear. Retaining T1's X(A) through commit/abort—strict 2PL—prevents that exposure.

### Connections

Retrieve [Lock Modes and Granularity](043-lock-modes-and-granularity.md), [Read and Write Anomalies](042-read-and-write-anomalies.md), and [ACID and Transaction Boundaries](041-acid-and-transaction-boundaries.md). Continue through the Database Engineering [roadmap](../ROADMAP.md) to DBE-045, Deadlock Detection and Resolution, then the topics on multiversion concurrency control and serializable snapshot isolation.

## Governing Question

How can a lock scheduler convert local incompatibility decisions into a global proof of serial execution, while preserving the recovery, liveness, and performance properties a production database actually needs?

## Why This Matters

Shared and exclusive locks prevent simultaneous conflicting access to one resource, but compatibility alone does not prevent a globally nonserializable history. A transaction could lock A, modify it, unlock A, and later lock B while another transaction does the reverse. Each local grant is legal at the instant it occurs, yet the resulting precedence graph can cycle. Two-phase locking adds an ordering discipline: once a transaction begins giving up protection, it cannot expand its protected set again.

That small rule is foundational because it yields a compositional proof. The scheduler need not enumerate every possible serial order or retain an unbounded history of reads and writes. It enforces lock compatibility and one monotone state transition per transaction. The final acquisition—the lock point—places each transaction in an order that respects all realized conflicts.

Production engineering starts where that theorem stops. Basic 2PL may release a write lock before the transaction outcome, exposing data that can still be undone. It can deadlock. It can lock the wrong physical rows and miss a logical predicate. It can reduce throughput through long waits and convoys. Modern systems mix locks with versions, transaction-ID dependencies, predicate tracking, validation, and specialized index protocols. Engineers therefore need to know exactly which guarantee comes from which rule.

The durable lesson is not “turn on 2PL.” It is to state the history model, conflict domain, lock modes, acquisition/release discipline, recovery coupling, and progress policy; prove the intended property under those assumptions; then verify how the selected engine and isolation configuration realize or depart from that model.

## Prerequisites and Retrieval

You should be able to construct precedence graphs, distinguish conflict from view equivalence, trace transaction boundaries and rollback, apply S/X compatibility, and identify row versus predicate/range resources. Retrieve partial order, directed cycle, topological order, serial history, conflicting operations, dirty read/write, recoverable/cascadeless/strict history, intention locks, lock conversion, write-ahead logging, and wait-for graph.

DBE-042 supplied anomaly histories and DBE-043 supplied modes, hierarchy, conversion, and predicate domains. This module supplies the global two-phase discipline. DBE-045 develops deadlock detection and victim policy; later modules compare timestamp ordering, MVCC, optimistic validation, and serializable snapshot isolation.

## Learning Objectives

After this module, you can:

1. formalize a lock-augmented history and identify each transaction's growing phase, shrinking phase, and lock point;
2. prove that basic 2PL admits only conflict-serializable histories under explicit coverage assumptions;
3. construct serializable histories that basic 2PL rejects and explain why 2PL is sufficient but not necessary;
4. distinguish basic, conservative, strict, and rigorous 2PL by acquisition, release, recovery, and liveness properties;
5. show why basic 2PL can permit dirty reads and cascading rollback;
6. reason correctly about upgrades, downgrades, hierarchical locks, and predicate/key-range coverage;
7. separate transaction lock discipline from write-ahead logging, deadlock handling, isolation policy, and two-phase commit;
8. map the abstract model cautiously onto current PostgreSQL, MySQL InnoDB, and SQL Server behavior;
9. diagnose blocking, convoys, lock footprint, and retry amplification with transaction-level evidence; and
10. design deterministic schedule tests and invariant checks for a 2PL scheduler.

## Core Exposition

**Begin with histories and conflicts.** Let a history preserve each transaction's internal operation order. Reads and writes by different transactions conflict if they address the same logical item and at least one is a write. Add edge `Ti -> Tj` when Ti's conflicting operation occurs first. The history is conflict-serializable exactly when this precedence graph is acyclic. Its topological orders are conflict-equivalent serial orders.

Locks mediate those conflicts. Before `read_i(x)`, Ti must hold an S or X lock covering x; before `write_i(x)`, it must hold X. A request waits while another owner holds an incompatible mode on the same resource. “Same resource” is a semantic assumption: if one path names a heap tuple while another names a unique key or an absent interval, local compatibility cannot establish the intended application conflict. Multiple-granularity intentions and predicate/key-range locking from DBE-043 extend the resource model; 2PL does not replace them.

**Basic 2PL is a state machine.** A transaction begins growing. It may acquire S/X locks and strengthen a held mode, such as S to X, subject to compatibility. Its first unlock or weakening conversion begins shrinking. While shrinking it may release or weaken locks, but cannot acquire or strengthen any lock. Commit/abort eventually terminates it and releases any remainder.

“Two phase” does not mean two statements, two locks, prepare/commit, or a synchronized global acquisition barrier. Transactions can overlap arbitrarily. One can acquire and operate repeatedly while growing. The boundary is semantic and local to each transaction. A transaction that retains all locks until outcome has a growing interval followed by a degenerate release interval and still obeys 2PL.

The **lock point** `LP(T)` is the position of T's last successful lock acquisition or strengthening conversion. It is grant time, not initial request time: a waiting request has not yet extended the protected set. A transaction with all locks pregranted has an early lock point; a rigorous transaction often has its lock point before commit even though it releases only afterward. Lock point is a proof witness, not necessarily an exposed engine timestamp.

**Serializability theorem.** Consider any precedence edge `Ti -> Tj` produced by conflicting operations on x. Ti held a lock on x incompatible with the lock J needs. Because Ti's operation came first and locks cover operations, Ti's lock was granted before J's conflicting lock. J can receive its lock only after Ti releases its incompatible lock. Under 2PL, once Ti releases that lock it cannot acquire any new lock, so `LP(Ti)` precedes the release. J's successful acquisition is no later than `LP(Tj)`. Thus `LP(Ti) < LP(Tj)`.

Every precedence edge points from smaller to larger lock point. If a cycle `T1 -> T2 -> ... -> Tk -> T1` existed, it would imply `LP(T1) < LP(T2) < ... < LP(Tk) < LP(T1)`, impossible for positions in one history. The graph is acyclic. Sorting by lock point is a topological order and therefore a conflict-equivalent serial order. This is a proof, not merely an intuition, under the compatibility, coverage, atomic-grant, and 2PL assumptions.

The converse is false. Some conflict-serializable histories cannot be produced while every transaction obeys 2PL because their operation order requires a transaction to release one conflict and later acquire another. So 2PL is sufficient, not necessary, for conflict serializability. It also targets conflict equivalence, a tractable conservative subset of view-serializable histories.

**Basic 2PL does not imply strictness.** A transaction can enter shrinking, release X(A), and later commit without taking another lock. Another transaction can then lock/read A. Lock-point order remains acyclic, but the reader has observed an uncommitted value. If the writer aborts, the dependent transaction must abort too; if a third transaction depends on it, rollback cascades. A second writer could overwrite the uncommitted value, complicating undo. Serializability orders operations; strictness constrains visibility relative to transaction outcome.

**Strict 2PL** adds: retain every exclusive lock through commit or abort. Shared locks may be released earlier, after shrinking begins, provided no later acquisitions occur. Other transactions cannot read or overwrite a transaction's written item before its outcome, so admitted histories are strict and therefore cascadeless and recoverable. In a WAL/undo system, outcome processing restores aborted state and durable commit rules establish the outcome before protected writes become available. Exact ordering is an implementation/recovery invariant, not supplied by the word “strict” alone.

**Rigorous 2PL** retains both shared and exclusive locks through commit or abort. It is stronger than strict 2PL and makes lock release simple: all transaction locks depart at outcome. For conflicting committed transactions, the earlier conflict owner must finish/release before the later owner can proceed, so commit order is consistent with conflict serialization order. This does not mean nonconflicting transactions have a unique serial order, nor that wall-clock start order is preserved.

Terminology varies. Some texts and products use “strict 2PL” for holding all locks to outcome—what this module calls rigorous/strong-strict—and others distinguish only X-lock retention. Always state the release rule rather than trusting the label.

**Conservative/static 2PL** requires the scheduler to know a transaction's full read/write lock set and obtain all of it as one all-or-none admission action before data operations. With no lock requests after execution starts, an admitted transaction cannot hold some resources while waiting to acquire another, so lock-wait deadlock among such transactions is prevented. The tradeoffs are advance knowledge, overapproximation, lower concurrency from early locks, admission queues, and difficulty with data-dependent access. “Ask for locks one by one at the start” is not sufficient: holding a partial set while waiting can still deadlock. Conservative acquisition does not by itself specify outcome-time release; many practical formulations combine it with retaining locks, but acquisition and release properties must be stated separately.

**Conversions obey direction.** S-to-X upgrade expands protection and belongs in growing. X-to-S downgrade weakens protection and begins or occurs in shrinking. An upgrade request may wait while the transaction retains S; two transactions that both hold S and request X can deadlock. Releasing S and requesting X later is not an atomic upgrade and introduces an unsafe gap. Update modes or earlier X acquisition may reduce conversion deadlock but cost read concurrency and do not eliminate all deadlocks.

**2PL can deadlock.** T1 locks A then waits for B; T2 locks B then waits for A. Both remain growing and perfectly obey 2PL. Neither can release without abort because releasing merely to acquire the awaited resource later would violate 2PL and may break correctness. Systems prevent selected cycles through total resource order or conservative acquisition, avoid some with timestamp policies, or detect wait-for cycles and abort a victim. Timeouts bound waiting but do not prove a cycle. DBE-045 treats these mechanisms.

**Predicates and phantoms remain a coverage problem.** A transaction tests “no booking overlaps interval I” and locks only rows returned—none. Another inserts a conflicting row. Both can follow row-level 2PL while the application invariant fails because no common resource represents absence/future membership. Serializable locking must cover the predicate through key ranges, index gaps, guard records, or another conflict mechanism. Eswaran, Gray, Lorie, and Traiger's predicate-lock formulation makes this logical-domain requirement explicit.

Hierarchical locking remains compatible with 2PL. Acquire ancestor intentions before descendant locks during growing. A later escalation is a new/coarser acquisition or conversion, so it must complete before any release. Release descendants/ancestors during shrinking in an order that preserves hierarchy. If escalation is attempted after an earlier unlock, it violates basic 2PL. Some engine-specific internal substitutions preserve an equivalent protection invariant; assess semantics, not surface lock counts alone.

**Recovery is coupled but distinct.** Strictness prevents other transactions from accessing uncommitted writes, simplifying undo and avoiding cascading rollback. WAL ensures log-before-data and durable commit ordering; it does not establish serializability. 2PL establishes conflict order; it does not reconstruct pages after a crash. Atomic commit defines the transaction outcome. A correct system composes these mechanisms and specifies what happens during abort, savepoint rollback, crash recovery, and connection loss.

**Two-phase locking is not two-phase commit (2PC).** 2PL is concurrency control over conflicts and may operate inside one database. 2PC is a distributed atomic-commit protocol in which participants prepare and later receive a commit/abort decision. A distributed transaction can use 2PL at participants and 2PC for outcome, but neither substitutes for the other. Their blocking causes also differ: 2PL waits on conflicting resources; 2PC can wait for a coordinator decision after prepare.

**Modern systems are hybrids.** PostgreSQL documents that most acquired locks are normally retained to transaction end, with savepoint rollback exceptions, while its serializable implementation uses MVCC plus predicate dependency tracking rather than textbook read-lock 2PL. InnoDB describes a combination of multiversioning and traditional 2PL; consistent reads may avoid S row locks, while updates and locking reads use record/gap/next-key mechanisms with isolation-dependent behavior. SQL Server combines locking and row versioning; current optimized locking may release row/page locks after modification while retaining transaction-ID protection. These products can preserve outcome/conflict dependencies without exposing the exact textbook resource. Configuration and version matter.

**Operational consequences.** Retaining locks strengthens recovery semantics but lengthens contention. A transaction that performs remote RPC, waits for human input, scans excessively, or stalls on I/O while holding locks can create queues, convoys, deadlocks, and retry storms. A blocked transaction may itself block others. Lock footprint depends on access path, granularity, selectivity, isolation, escalation, and versioning policy.

Keep transactional critical sections short without splitting an invariant across commits. Prepare input and remote data before beginning; acquire resources in a durable order where possible; index predicates to narrow the protected domain; bound waits; make retryable operations idempotent; apply admission/backpressure; and test at representative skew. Never “solve” blocking by early unlocking unless a different validated concurrency protocol replaces the lost guarantee.

**Observability and testing.** For each waiter capture transaction/session identity, start/age, query and plan, requested/held mode and logical resource, blocker chain, wait start, isolation/configuration, locks/versions, outcome, victim reason, retry attempt, and invariant result. Redact business values. Snapshots race; correlate repeated samples with completed transaction traces.

At the scheduler boundary, deterministic tests should generate histories and assert: access implies sufficient lock; grants respect compatibility; state changes only growing-to-shrinking; no acquisition/upgrade after release/downgrade; strict/rigorous duration; abort cleanup; and final values. Derive the precedence graph independently and compare its topological order with lock-point inequalities. Include waiting requests, upgrades, phantoms, savepoints, cancellation, deadlock victimization, and retry—not only happy serial histories.

The following executable model checks a basic-2PL history that is conflict-serializable but not strict. It records successful grants only; compatibility is represented by the schedule's explicit nonoverlap.

<!-- bijux-verify: {"id":"basic-2pl-not-strict","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"two_phase=True\nlock_points=(('T1', 5), ('T2', 7))\nprecedence_edges=(('T1', 'T2'),)\nserial_order=('T1', 'T2')\nstrict=False\ndirty_read_possible=True\ninvariants=True\n","stderr":""}} -->
```python
events = (
    ("lock", "T1", "X", "A"),
    ("write", "T1", "A", 1),
    ("lock", "T2", "X", "B"),
    ("write", "T2", "B", 1),
    ("lock", "T1", "X", "C"),
    ("unlock", "T1", "A"),
    ("lock", "T2", "S", "A"),
    ("read", "T2", "A", 1),
    ("unlock", "T1", "C"),
    ("commit", "T1"),
    ("unlock", "T2", "A"),
    ("unlock", "T2", "B"),
    ("commit", "T2"),
)

phase = {"T1": "growing", "T2": "growing"}
held = {"T1": {}, "T2": {}}
lock_points = {}
committed = set()
writer = {}
edges = set()
dirty_read_possible = False
strict = True
two_phase = True
access_is_covered = True

for position, event in enumerate(events, 1):
    kind, transaction, *fields = event
    if kind == "lock":
        mode, item = fields
        if phase[transaction] != "growing":
            two_phase = False
        held[transaction][item] = mode
        lock_points[transaction] = position
    elif kind == "unlock":
        item = fields[0]
        mode = held[transaction].pop(item)
        phase[transaction] = "shrinking"
        if mode == "X" and transaction not in committed:
            strict = False
    elif kind == "write":
        item, value = fields
        access_is_covered &= held[transaction].get(item) == "X"
        prior = writer.get(item)
        if prior is not None and prior != transaction:
            edges.add((prior, transaction))
        writer[item] = transaction
    elif kind == "read":
        item, observed = fields
        access_is_covered &= held[transaction].get(item) in {"S", "X"}
        prior = writer.get(item)
        if prior is not None and prior != transaction:
            edges.add((prior, transaction))
            dirty_read_possible |= prior not in committed
    elif kind == "commit":
        committed.add(transaction)

ordered_points = tuple(sorted(lock_points.items(), key=lambda pair: pair[1]))
precedence_edges = tuple(sorted(edges))
serial_order = tuple(transaction for transaction, _ in ordered_points)
edge_ordered = all(
    lock_points[source] < lock_points[target]
    for source, target in precedence_edges
)
all_released = all(not locks for locks in held.values())
invariants = two_phase and access_is_covered and edge_ordered and all_released

print(f"two_phase={two_phase}")
print(f"lock_points={ordered_points}")
print(f"precedence_edges={precedence_edges}")
print(f"serial_order={serial_order}")
print(f"strict={strict}")
print(f"dirty_read_possible={dirty_read_possible}")
print(f"invariants={invariants}")
```

## Definitions and Notation

- `H`: a finite history preserving each transaction's program order.
- `op_i(x)`: operation by transaction Ti on logical item/domain x.
- `conflict(op_i(x), op_j(x))`: `i != j`, same logical domain, and at least one operation writes.
- `SG(H)=(V,E)`: precedence/serialization graph; `(Ti,Tj) in E` when Ti's conflicting operation precedes Tj's.
- `L_i^m(x)`, `U_i(x)`: successful lock grant in mode m and unlock by Ti on x.
- **Growing:** acquisitions and upgrades allowed; releases/downgrades absent.
- **Shrinking:** releases and downgrades allowed; acquisitions/upgrades forbidden.
- `LP(Ti)`: position of Ti's final successful acquisition/upgrade.
- **Basic 2PL:** every transaction has one growing interval followed by one shrinking interval.
- **Conservative 2PL:** the complete declared lock set is granted atomically before data execution.
- **Strict 2PL:** basic 2PL plus retain all X locks through commit/abort.
- **Rigorous 2PL:** basic 2PL plus retain all S and X locks through commit/abort.
- **Strict history:** no other transaction reads or writes an item written by an uncommitted transaction.
- **Recoverable:** a reader commits only after every transaction whose value it read commits.
- **Cascadeless:** transactions read only committed values.
- **Wait-for edge:** `Ti -> Tj` means Ti waits for a resource held incompatibly by Tj; this graph differs from the precedence graph.

## Mechanisms, Invariants, or Proof Structure

**Formal theorem.** If every conflicting access is protected by correctly incompatible locks on the same logical domain and every transaction obeys basic 2PL, the admitted history is conflict-serializable.

**Proof.** Select arbitrary precedence edge `Ti -> Tj` on x. Ti's covering lock was granted before its operation. Tj's incompatible covering lock cannot be granted until Ti releases. Because Ti follows 2PL, its last acquisition occurred before that release; because Tj's selected grant is one of its acquisitions, it occurs no later than Tj's lock point. Hence `LP(Ti) < LP(Tj)`. Applying this to every edge orients the entire precedence graph by strictly increasing lock points. A directed cycle would require a strict value to be less than itself. Therefore no cycle exists, and increasing lock-point order is a topological/serial order. QED.

The proof uses successful grants, not requests. It assumes lock compatibility is atomic and complete for the true logical domain. Missing predicate coverage, inconsistent resource identity, unsafe conversion gaps, or an access before locking invalidates a premise; 2PL syntax alone then proves nothing about the intended history.

**Variant implications.** Rigorous 2PL implies strict 2PL under the stated definitions; strict 2PL implies basic 2PL plus strict histories; strict histories are cascadeless, and cascadeless histories are recoverable. Reverse implications do not generally hold. Conservative acquisition prevents lock-wait cycles only when admission is genuinely all-or-none and every required resource is declared; it is orthogonal to X/all-lock retention.

**Boundary rules.** A transaction with no locks is trivially two-phase. A transaction acquiring one lock and releasing it is two-phase. A downgrade is a release of protection and starts shrinking; an upgrade is acquisition of protection and is forbidden afterward. Reentrant duplicate acquisition that does not strengthen protection needs an explicit scheduler definition, but must not smuggle a new resource into shrinking. Savepoint rollback may release locks acquired after a savepoint in some products; model those documented semantics rather than assuming textbook transaction-wide retention.

**Independent verification plan.** Parse events; check each access is covered; track monotone transaction state; build last-grant positions; independently derive precedence edges from conflicting reads/writes; assert every edge increases lock point; inspect X/all-lock release relative to outcome; and separately construct the wait-for graph for liveness. Test both admitted and deliberately rejected schedules. This separates theorem premises, conclusion, recovery property, and progress property.

## Alternatives and Trade-Offs

- **Basic versus strict:** basic may release early for concurrency but permits uncommitted exposure/cascading undo; strict retains X protection and simplifies recovery at longer blocking cost.
- **Strict versus rigorous:** strict may release S locks after its lock point; rigorous retains all locks, simplifies outcome release and aligns conflict order with commit order, but can block writers longer.
- **Dynamic versus conservative:** dynamic acquisition follows data-dependent paths and locks later but can deadlock; conservative all-or-none admission avoids lock-wait deadlock but requires complete sets and often overlocks early.
- **2PL versus timestamp ordering:** locks wait and preserve a conflict order formed by grants; timestamp protocols reject/abort operations that violate a predetermined order and avoid some waits at restart cost.
- **2PL versus optimistic validation:** 2PL pays coordination during execution; optimistic methods allow speculative overlap then validate/abort, attractive under low conflict but costly under hotspots or long work.
- **Locking reads versus MVCC:** read locks prevent conflicting writes and can block; versions serve an earlier committed state without S-lock blocking but require write-conflict and serializability mechanisms beyond simple snapshots.
- **Range locks versus dependency tracking:** blocking ranges prevent phantoms proactively; SSI-style tracking observes dependencies and aborts dangerous structures, improving read/write concurrency at tracking/retry cost.
- **Early release versus transaction splitting:** early release under basic 2PL can preserve serializability yet weaken recovery; splitting commits creates distinct transactions and is correct only if every intermediate state and retry is valid.
- **Ordering versus detection:** a total resource order prevents cycles when universally followed but can be difficult for dynamic plans; detection allows flexible order but pays graph/victim/retry cost.
- **2PL versus 2PC:** 2PL orders conflicting operations; 2PC coordinates atomic outcome across participants. Distributed transactions may need both and inherit both kinds of blocking.

## Failure Modes and Misconceptions

- “Compatible locks guarantee serializability.” Per-resource compatibility needs the two-phase ordering discipline or another global protocol.
- “Basic 2PL means locks live to commit.” Only strict/rigorous variants add outcome-time retention.
- “Serializable means nobody sees uncommitted data.” Serializability and strictness are different history properties.
- “Lock point is commit time.” It is the final successful acquisition/upgrade.
- “A waiting request advances the lock point.” Only a granted acquisition changes protection.
- “2PL prevents deadlock.” Basic, strict, and rigorous 2PL can deadlock while obeying every rule.
- “Conservative means request everything sequentially before work.” It requires all-or-none admission; partial holding while waiting can cycle.
- “Unlock S, then later upgrade another S to X.” The unlock began shrinking, so the later upgrade violates 2PL.
- “Row 2PL prevents phantoms.” Only if the logical predicate conflict is represented through ranges, guards, or equivalent validation.
- “Strict and rigorous are universally named.” Literature varies; specify exactly which modes remain until outcome.
- “MVCC engines do not use locks.” Writers, locking reads, metadata, constraints, and transaction dependencies still coordinate.
- “Shortening locks is always faster.” It may destroy guarantees; shorten the transaction or adopt another proven protocol.
- “Timeout means deadlock.” A long wait need not be cyclic, and a cycle may be detected before a timeout.
- “Retry fixes victimization.” Retry also needs bounded backoff, idempotency, deadlines, and overload control.
- “Two phases means two-phase commit.” The names describe unrelated concurrency-control and distributed-outcome protocols.

## Worked Examples

### Example 1

T1 obtains S(A), reads A, obtains X(B), writes B, releases A, then releases B. Its last acquisition precedes its first release, so it obeys basic 2PL. Conclusion: operations may interleave with acquisition; the rule concerns the direction of protection changes.

### Example 2

T1 obtains X(A), releases A, then obtains S(B). The local locks never overlap another transaction, but T1 moved shrinking-to-growing. Conclusion: the schedule violates 2PL even if this particular run happens to be serial; protocols constrain all admitted runs.

### Example 3

Conflict edges are `T1 -> T2` and `T2 -> T3`. 2PL implies `LP(T1) < LP(T2) < LP(T3)`, so `(T1,T2,T3)` is a valid serial order. An alleged edge `T3 -> T1` would require an impossible lock-point cycle. Conclusion: lock points are a topological witness.

### Example 4

T1 releases X(A) before commit; T2 locks and reads A, then T1 aborts. Both may obey basic 2PL, but T2 consumed undone state and must abort. Conclusion: basic 2PL is conflict-serializable but not necessarily strict or cascadeless.

### Example 5

Under strict 2PL, T1 retains X(A) until its abort has restored A. T2's S(A) waits, then reads the restored committed value. Conclusion: X-lock retention composes concurrency control with undo to prevent cascading rollback.

### Example 6

T1 and T2 each hold S(A) and request X(A). Both upgrade requests wait for the other's S. Neither has released, so both remain growing. Conclusion: a deadlock can be a valid 2PL execution; victim resolution is a separate liveness mechanism.

### Example 7

A conservative scheduler knows T1 needs X(A), S(B) and T2 needs X(B), S(A). It admits one complete set and queues the other without granting a partial set. Conclusion: all-or-none preclaim prevents this lock-wait cycle, at the price of early locks and declared access sets.

### Example 8

T1 finds no overlapping booking and therefore takes no row lock; T2 inserts an overlap. Each transaction follows row-level rigorous 2PL. Conclusion: rigorous duration cannot repair an incomplete resource model; protect the predicate/range or a canonical guard.

### Example 9

T1 holds table IX and row X, then releases the row and later attempts table-X escalation. The later conversion is an acquisition after shrinking. Conclusion: escalation must complete in growing before any descendant release, or the protocol needs a separately proven equivalent rule.

### Example 10

A service holds strict transaction locks while making a 20-second RPC. Fifty requests queue, some time out and retry immediately, multiplying load. Moving the RPC before the transaction and preserving an idempotent final write reduces hold time. Conclusion: retain correctness-critical locks, but remove unrelated latency from their lifetime.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies mutex semantics, lock ordering, deadlock, fairness, and linearization-style proof reasoning.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies graph topological order and B-tree ranges whose logical identity must be locked.
- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) supplies state machines, invariant-centered design, cancellation, and retry boundaries.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) distinguishes local locks from leases/fencing and 2PL from distributed commit/consensus.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies deadlines, idempotency keys, backpressure, and conflict/retry contracts.

## References

1. Philip A. Bernstein, Vassos Hadzilacos, and Nathan Goodman, [*Concurrency Control and Recovery in Database Systems*](https://www.microsoft.com/en-us/research/people/philbe/book/), Addison-Wesley, 1987, formal lock schedulers, 2PL, serializability, deadlock, and recovery.
2. K. P. Eswaran, J. N. Gray, R. A. Lorie, and I. L. Traiger, [“The Notions of Consistency and Predicate Locks in a Database System”](https://doi.org/10.1145/360363.360369), *Communications of the ACM* 19(11), 1976, two-phase restriction and logical predicate domains.
3. Jim Gray, Raymond Lorie, Gianfranco Putzolu, and Irving Traiger, [“Granularity of Locks and Degrees of Consistency in a Shared Data Base”](https://www.cs.cmu.edu/~15721-f24/papers/Granularities_of_Locking.pdf), IFIP Working Conference on Modelling in Data Base Management Systems, 1975, multiple-granularity protocols and lock duration.
4. Hal Berenson et al., [“A Critique of ANSI SQL Isolation Levels”](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf), Microsoft Research Technical Report MSR-TR-95-51, 1995, histories, strict 2PL, and isolation distinctions.
5. C. Mohan et al., [“ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging”](https://cs.stanford.edu/people/chrismre/cs345/rl/aries.pdf), *ACM Transactions on Database Systems* 17(1), 1992, recovery coupling with fine-grained locking.
6. PostgreSQL Global Development Group, [Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html), current lock duration, savepoint rollback, row/table modes, deadlocks, and advisory locks.
7. PostgreSQL Global Development Group, [Serializable Isolation Level](https://www.postgresql.org/docs/current/transaction-iso.html#XACT-SERIALIZABLE), current MVCC serializable behavior and predicate-lock dependency tracking.
8. Oracle, [MySQL 8.4 InnoDB Transaction Model](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-model.html), current combination of multiversioning and traditional 2PL.
9. Oracle, [MySQL 8.4 Transaction Isolation Levels](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html), current isolation-dependent acquisition and retention examples.
10. Microsoft, [Transaction Locking and Row Versioning Guide](https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-locking-and-row-versioning-guide?view=sql-server-ver17), current locking, row versioning, transaction-ID protection, duration, and operational guidance.

## Exercises

### Exercise 1

For three supplied lock histories, mark each successful grant, upgrade, downgrade, release, growing/shrinking transition, and lock point. Decide basic/strict/rigorous compliance and justify every rejection.

### Exercise 2

Prove the lock-point theorem from a precedence edge, then construct one conflict-serializable history that cannot be generated by basic 2PL. State every assumption and why the converse fails.

### Exercise 3

Implement or specify a deterministic 2PL scheduler test harness covering compatibility, waiting grants, conversion, strict release, abort, predicate coverage, and violation detection. Define independent oracles.

### Exercise 4

Choose among basic, strict, rigorous, and conservative 2PL for a short account transfer, a data-dependent graph traversal, and a statically declared nightly batch. Compare correctness, recovery, deadlock, and concurrency.

### Exercise 5

A production service reports long lock queues, deadlock retries, missing range invariants, and an operator proposal to release row locks before an RPC returns. Produce a diagnosis and remediation plan transferable across MVCC/locking engines.

## Answers to the Exercises

### Answer 1

Scan each transaction independently. It starts growing; every new resource or S-to-X upgrade is allowed only there. The first unlock or X-to-S downgrade changes it irreversibly to shrinking. Any later acquisition/upgrade rejects basic 2PL. The lock point is the position of the final successful grant/upgrade, including one granted after waiting—not request time. Basic compliance says nothing about outcome release. Strict additionally rejects any X release before commit/abort completes; rigorous rejects any S or X release before outcome. Check access coverage and compatibility separately: a syntactically two-phase history with an unprotected write is not a correct locking history. A transaction with no locks is trivially compliant; a transaction retaining all locks to outcome has a degenerate shrinking/release interval.

### Answer 2

For edge `Ti -> Tj` on x, Ti's incompatible covering lock precedes Tj's. J's lock cannot be granted until Ti releases. Ti's lock point precedes that release by 2PL; J's selected grant is no later than J's lock point. Hence `LP(Ti)<LP(Tj)`. All graph edges strictly increase lock point, so a cycle is impossible and lock-point order is serial. Assumptions: correct common logical resource, sufficient incompatible modes, locks before access, atomic grants/releases, and two-phase state. For the converse, use a serializable operation history whose transactions' nonconflicting arrangement requires T1 to make one conflict available, then later acquire protection for another resource after T2 has used the first. Its precedence graph can remain one-directional while T1 would need release-then-acquire. Thus conflict serializability is a property of the realized history; 2PL is a sufficient online discipline that rejects some safe histories because it cannot rely on future knowledge.

### Answer 3

Represent events with transaction, resource/domain, mode, request/grant/release/outcome, and data operation. Maintain an atomic lock table, queues, held modes, and monotone per-transaction state. Oracle one checks every access has S/X coverage and every grant is compatible. Oracle two rejects acquisition/upgrade after first release/downgrade. Oracle three independently derives read/write conflicts, precedence graph, and lock points, asserting every edge increases. Oracle four checks strict/rigorous release relative to commit/abort and validates restored final state. Add barriers rather than sleeps for wait/upgrade/deadlock schedules; model absent-key predicates as resources; inject abort/cancel; ensure victim cleanup releases once. Compare emitted trace, output, graph, and invariant state. Passing finite histories supports the implementation but does not universally prove all scheduler executions; retain the formal invariant argument.

### Answer 4

Use strict or rigorous 2PL for the account transfer: X locks through outcome prevent exposure of partially undone balances; deterministic account order reduces deadlock. Rigorous S retention may be needed if repeated current reads form the invariant, but can block more than a strict/MVCC combination. A data-dependent graph traversal cannot accurately predeclare all nodes, so conservative 2PL risks gross overapproximation or is infeasible; dynamic strict/rigorous acquisition plus cycle detection/retry or a validated MVCC alternative fits better. The nightly batch with a known static read/write partition can use conservative all-or-none admission to prevent lock-wait deadlock, perhaps retaining writes/all locks to outcome for recovery semantics. It may acquire broad locks early and delay interactive work; partitioning/admission windows can control this. In every case predicates, hierarchy, WAL/abort, deadlines, idempotent retry, and measured workload remain explicit.

### Answer 5

First capture blocker/waiter chains, transaction ages, queries/plans, isolation/configuration, logical resources/modes, range coverage, deadlock graphs/victims, retry attempts, RPC timing, lock/version footprint, and invariant failures. Separate liveness from correctness. Missing range protection is a resource-model defect: add an exact constraint, range/predicate/guard lock, or serializable validation and test concurrent absent-key inserts. Do not release correctness-critical locks around the RPC under the same transaction assumption. Move the RPC and human/remote preparation before the transaction where possible; if external effects must coordinate, use an idempotent workflow/outbox/saga with explicit semantics rather than pretending early unlock is atomic. Narrow plans/indexes, use deterministic acquisition order, bound waits, back off/jitter retries, enforce retry budgets and admission control, and keep the critical section short. Reproduce on each pinned engine/version because PostgreSQL SSI, InnoDB MVCC/next-key behavior, and SQL Server row-versioning/optimized locking expose different resources. Assert final invariants and outcome histories, not merely fewer waits.
