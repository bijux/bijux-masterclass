---
module_id: CONPAR-005
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 5
title: Race Conditions and Atomicity Violations
status: complete
last_verified: 2026-08-29
---

# Race Conditions and Atomicity Violations

## One-Page Review

### Governing question

When does correctness depend on relative event timing, how is that broader than a memory data race, and which compound operations must appear indivisible to preserve a product invariant?

### Essential definitions

- A **race condition** exists when correctness or required observation depends on which of several admissible events wins or occurs first.
- A **data race** is a language-memory-model term for conflicting concurrent memory accesses to one location, at least one a write, without the required ordering or synchronization.
- **Conflicting accesses** overlap a memory location and include a write; the exact location and ordering definitions come from the language specification.
- **Race freedom** means the named race class is absent. Data-race freedom does not imply freedom from logical, protocol, filesystem, database, or distributed races.
- An **atomic action** appears indivisible at its specified abstraction boundary; observers see it before or after, not a prohibited intermediate state.
- An **atomicity violation** occurs when interleaving events break an intended atomic region or serializable operation.
- A **check-then-act race** separates a predicate observation from the mutation whose validity depends on that predicate.
- A **read-modify-write race** loses or miscombines updates because read, calculation, and write are not one protected transition.
- A **time-of-check to time-of-use (TOCTOU) race** lets relevant authority or state change between validation and use.
- A **linearization point** is the event at which a completed concurrent operation can be viewed as taking effect atomically between invocation and response.
- **Linearizability** requires each concurrent history to correspond to a legal sequential history that preserves real-time order of nonoverlapping operations.

### Central model, mechanism, or theorem

Let operation (O) have invocation, internal events, and response. Its sequential specification defines allowed state transition (delta_O). An implementation is atomic at its contract boundary when each completed operation can be assigned a point between invocation and response so ordering operations by those points yields a legal sequential history and preserves real-time precedence.

Data-race freedom constrains conflicting memory events. Linearizability constrains whole operation histories. Thus a program can use only atomic variables and remain data-race-free while violating quota, uniqueness, conservation, or authorization because several individually atomic steps fail to form one logical operation.

### Critical invariants

The language memory model defines data race; folklore does not. Source expressions are not presumed atomic. The protected unit follows the product invariant, not merely one variable. Check and state change share one serialization boundary or use validation that can fail safely. Linearization points lie between invocation and response and satisfy the sequential contract. Locks have consistent scope and ownership. Atomic retry loops revalidate every premise. TOCTOU repairs operate on stable handles or authority-bound operations rather than rechecking a mutable name. Race detectors, schedule tests, history checkers, and code review make distinct claims.

### Common failures

Teams call every schedule-sensitive defect a data race; assume a thread-safe collection makes a compound workflow atomic; replace ordinary fields with atomics but retain check-then-act; protect reads and writes with different locks; release a lock before an invariant is restored; hold a lock across unbounded external work; test a pathname and later open it; use a stale version without conditional commit; identify a linearization point that can later roll back; assume absence of detector reports proves absence; or repair one trace with sleeps.

### Compact example

A quota contains one remaining slot. A and B each atomically load one, decide admission, then atomically decrement. There is no non-atomic conflicting memory access, yet both may load before either decrement and admit two clients. The correct transition is not “atomic load plus atomic store”; it is “reserve one slot if positive” through a lock-protected region, compare-and-update loop, transaction, or authoritative conditional operation.

### Connections

[Interleavings and State-Space Explosion](003-interleavings-and-state-space-explosion.md) supplies counterexample schedules; [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md) supplies invariant and progress criteria. The [program roadmap](../ROADMAP.md) next separates deadlock, determinism, critical sections, ownership transfer, locks, atomics, happens-before, and linearizability proofs.

## Governing Question

How can an engineer identify the exact invariant-changing transaction hidden inside ordinary code, prove which interleavings violate it, and choose a repair whose atomicity scope matches the real authority?

The answer starts by separating vocabulary. A language data race can make memory behavior invalid or weakly constrained. A higher-level race can occur with perfect memory synchronization. An atomicity violation is diagnosed by comparing an intended compound operation with an interleaved history. Repair must move the serialization boundary to the authority that owns the invariant.

## Why This Matters

Race bugs survive code review because every line looks locally reasonable. Check capacity, then allocate. Read balance, compute debit, then write. Test file ownership, then open. Look up an absent key, then create. Read entity version, edit, then replace. Each sequential trace is correct; concurrency inserts another operation between the dependent steps.

The consequences cross layers. Memory data races can produce stale, torn, or language-undefined behavior. Logical races can oversell inventory, exceed quotas, duplicate work, lose updates, violate uniqueness, authorize against stale state, resurrect deleted resources, or select different valid winners. Some winner races are intentional; correctness then defines all permitted winners and downstream effects.

Language specifications differ in racy-program semantics. Java SE 26 defines a data race through conflicting accesses not ordered by happens-before and gives correctly synchronized programs sequential-consistency guarantees. Go's June 2022 memory model defines read-write and write-write races and provides a data-race-free sequential-consistency result while constraining some racy outcomes. Rust lists data races as undefined behavior and safe Rust excludes them, while its official documentation explicitly warns that general race conditions remain.

These differences make “it is atomic on my machine” unusable. The object type, access mode, alignment, compiler, architecture, synchronization, and language model matter. Later memory-model modules provide detailed ordering. Here the central lesson is that eliminating memory races is necessary in many languages but never a complete concurrent-correctness argument.

Atomicity also matters without threads. Async functions interleave at suspension points. Processes race through files, shared databases, or kernels. Services race through conditional requests and queues. A signal handler or callback races with foreground state. The unifying fact is an invariant spanning more than one independently schedulable event.

## Prerequisites and Retrieval

Retrieve interleavings, happens-before as an ordering relation, state invariants, finite bad prefixes, transitions, version numbers, preconditions, idempotency, and basic transactions. Be able to distinguish one memory location from a product invariant over several locations or external effects.

This module does not prescribe detailed memory orders, mutex APIs, database isolation levels, or filesystem flags. It develops reasoning that those mechanisms must satisfy.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish a broad race condition from a language-defined data race;
2. identify conflicting accesses and demand the exact memory-model rule;
3. decompose check-then-act, read-modify-write, lost-update, TOCTOU, and winner-selection races;
4. state the invariant and intended atomic transition behind a workflow;
5. construct a minimal violating interleaving;
6. evaluate locks, atomic read-modify-write, conditional update, transactions, ownership, and message passing as repairs;
7. identify a valid linearization point and reject false points;
8. design history-based tests and deterministic schedule regressions;
9. interpret race-detector evidence without overclaiming; and
10. escalate high-consequence authorization, financial, safety, or integrity races to appropriate human review.

## Core Exposition

“Race condition” is the umbrella. Two operations overlap and the observed outcome depends on order. The outcome is defective only if the contract excludes it. Two workers racing to publish identical cached content may allow either winner. Two withdrawals racing to spend the same funds violate conservation if both succeed. Start from allowed histories, not from nondeterminism alone.

A **data race** is narrower. Most definitions require concurrent or happens-before-unordered conflicting access to the same location, with at least one write and insufficient synchronization or atomic access. Exact consequences vary. A detector implements one model and observes one set of executions; a language specification is authoritative.

Data-race freedom can coexist with a race condition. Two atomic quota loads and stores are individually well defined. Their compound protocol is wrong. A thread-safe map safely implements `contains` and `insert` separately, but `if absent then insert` may create duplicate side effects. An async task can inspect state, await, then act on a premise invalidated by another task without any simultaneous memory access.

Find the **invariant** first. Quota may require (accepted <= capacity). Banking may require conservation and nonnegative available funds. Uniqueness requires at most one active record for a key. Authorization requires decision and effect against one relevant policy/resource version. Then define the intended transition including precondition, state change, result, and externally visible effects.

The minimal counterexample marks events. For quota: A reads one; B reads one; A records success and decrements; B records success and decrements. For lost update: A reads version/value; B reads same; A commits; B overwrites without validating version. For duplicate creation: both observe absence, both perform irreversible external setup, and only later one database insert fails. The uniqueness constraint protects the row but not the duplicated external effect.

An **atomic region** groups events that must appear indivisible to relevant observers. It need not prohibit internal parallel work; it must prevent histories violating the contract. Its scope can span multiple variables. Locking only `remaining` while appending an accepted reservation outside the lock can expose disagreement. Conversely, holding a local process mutex cannot serialize other processes or services.

The **serialization authority** owns the invariant. In one process it may be a mutex or actor. Across processes it may be the kernel, a database row/version/constraint, a compare-and-set service, a single-owner queue, or a consensus-backed store. A client-side check cannot enforce an invariant whose authoritative state changes elsewhere.

Check-then-act repair has several patterns. Put check and mutation under one lock. Use an atomic conditional primitive such as decrement-if-positive. Submit one database statement or transaction with a predicate and inspect affected-row count. Use a uniqueness constraint plus an effect design that does not escape before commit. Transfer ownership to one serial executor. All repairs need failure and retry semantics.

Atomic read-modify-write is stronger than separate load/store, but only for its object and operation. A fetch-add can allocate a unique ticket. It cannot alone update a linked record, emit an effect exactly once, or enforce a multi-field state machine. A compare-and-update loop reads a snapshot, derives a candidate, then commits only if the snapshot remains current; on failure it reloads and recomputes every dependent premise.

Locks establish mutual exclusion only among participants using the same lock with compatible scope. Protect the invariant, not individual getters. Establish state before publishing a reference. Do not access protected data after releasing unless copied safely. Exceptions, cancellation, and panic must restore or mark invariants. Holding locks during network calls can create deadlock, unbounded latency, and failure coupling; split reservation from external work with durable state.

TOCTOU races emphasize authority. Checking a pathname's metadata and opening that pathname later allows namespace change. A safer design opens through authority-constraining primitives, validates the resulting handle when needed, and performs operations on that handle. Similarly, authorization should bind to stable resource identity/version and be enforced at the operation boundary.

**Lost update** is not synonymous with last-writer-wins policy. If last-writer-wins is the declared merge semantics, overwriting may be allowed. If each writer intends to preserve the other's independent change, silent replacement is a violation. Conditional versions make conflict observable; merge logic then resolves field/domain semantics rather than blindly retrying stale replacement.

**Linearizability** gives an operation-level correctness criterion. A concurrent history records invocations and responses. Each completed operation must appear to take effect at one point inside its interval. Ordering these points must form a legal sequential history, and if one response precedes another invocation, that real-time order must remain. Overlapping operations may be ordered either way if the object specification permits it.

A linearization point can be a successful compare-and-swap, insertion under a lock, dequeue pointer update, or authoritative transaction commit. It is not necessarily a source line fixed across paths; helping algorithms can linearize one operation in another participant. A tentative write that can roll back is not automatically the point of externally committed effect.

Linearizability is compositional for independently specified objects, a major benefit. Yet a workflow across two individually linearizable objects may violate a cross-object invariant. Atomic accounts plus atomic ledger append do not make transfer-plus-audit one transaction. Again, the invariant determines scope.

The executable model enumerates two clients, each with a check and reserve event, while preserving local order. It shows that four of six schedules oversubscribe a one-slot quota.

<!-- bijux-verify: {"id":"check-then-reserve-race","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"schedules=6\nsafe=2\noversubscribed=4\nmaximum_accepted=2\n","stderr":""}} -->
```python
steps = {"A": ["check", "reserve"], "B": ["check", "reserve"]}
schedules = []

def visit(prefix, positions):
    if all(positions[name] == len(steps[name]) for name in steps):
        schedules.append(prefix)
        return
    for name in steps:
        index = positions[name]
        if index < len(steps[name]):
            next_positions = dict(positions)
            next_positions[name] = index + 1
            visit(prefix + [(name, steps[name][index])], next_positions)

visit([], {"A": 0, "B": 0})
safe = 0
oversubscribed = 0
maximum_accepted = 0

for schedule in schedules:
    available = 1
    eligible = {}
    accepted = 0
    for name, action in schedule:
        if action == "check":
            eligible[name] = available > 0
        elif eligible[name]:
            accepted = accepted + 1
            available = available - 1
    maximum_accepted = max(maximum_accepted, accepted)
    if accepted <= 1:
        safe = safe + 1
    else:
        oversubscribed = oversubscribed + 1

print(f"schedules={len(schedules)}")
print(f"safe={safe}")
print(f"oversubscribed={oversubscribed}")
print(f"maximum_accepted={maximum_accepted}")
```

Execution proves counts for this four-event sequentially consistent model only. It does not establish any real language's memory behavior, atomic instruction, transaction isolation, quota protocol, external-effect safety, retry correctness, or production capacity integrity.

Detection techniques have different coverage. Dynamic data-race detectors instrument memory access and infer happens-before or lockset violations in observed executions. They are excellent evidence for executed conflicting accesses but may miss unexecuted paths, unsupported code, processes, devices, or custom synchronization. They do not generally detect a logical race over properly synchronized atomic calls.

Atomicity-violation detection compares access patterns or operation histories against expected serial regions. Systematic scheduling forces windows around check/action or read/write pairs. Linearizability checkers search for a legal sequential history. Static analysis over-approximates paths but can report false positives or miss reflection and foreign code. Domain assertions catch violated outcomes. Use several and preserve the distinction.

Regression tests should control the boundary, not sleep. Place a deterministic hook or barrier after both checks and before either act, prove the flawed implementation oversubscribes, then verify the repair allows one success and one explicit rejection/retry. Capture initial state, operations, event trace, version, results, and final invariant. Remove test-only hooks from public behavior or make their ownership clear.

Repairs change compatibility. Adding conditional update can turn silent success into conflict. Serializing can reduce throughput or create blocking. Retrying may duplicate non-idempotent effects. Stronger database isolation can abort transactions. The public contract must state conflict, retry, ordering, cancellation, and idempotency behavior.

## Definitions and Notation

Let events (e,f) **conflict** when they access overlapping memory and at least one writes, under the language's location model. A data race commonly requires conflict plus absence of the required happens-before or synchronization ordering; consult the exact specification.

Let abstract state (q) satisfy invariant (I(q)). Intended operation (O) has precondition (Pre_O), transition (delta_O), and result (r). Its implementation expands to events (e_1,...,e_m). An atomicity violation is a legal interleaving with other events that produces a history not equivalent to allowed sequential applications of (delta).

A history contains invocation (inv(O,x)) and response (ret(O,y)) events. Real-time order places (O_1) before (O_2) when response of (O_1) precedes invocation of (O_2). A linearization maps completed operations to points inside their intervals, preserves this order, and satisfies the sequential object specification.

**Serializability** usually concerns equivalence of transactions to some serial order; **strict serializability** additionally respects real time and is close to transactional linearizability. Isolation names vary by platform, so never substitute a label for documented phenomena and tests.

## Mechanisms, Invariants, or Proof Structure

Use this analysis:

1. **Name the contract.** List valid results, ordering, conflicts, retries, and external effects.
2. **Write the invariant.** Include every field, resource, identity, and authority it spans.
3. **Mark events.** Split observations, validation, calculation, commit, publication, and effect.
4. **Construct a minimal trace.** Place one competing event between dependent steps.
5. **Classify correctly.** Apply the language data-race definition and separately assess logical atomicity.
6. **Locate authority.** Identify the component able to serialize or conditionally reject changes.
7. **Choose a repair.** Lock, atomic RMW, versioned conditional write, transaction, constraint, ownership, or redesign.
8. **Propose a linearization point.** Check interval, sequential legality, real-time order, failure, retry, and rollback.
9. **Verify adversarially.** Use deterministic scheduling, race detection, history checking, invariant assertions, and failure injection.
10. **Review trade-offs.** Examine progress, deadlock, throughput, latency, compatibility, idempotency, and recovery.

For invariant proof, show each serialized successful transition maps a state satisfying (I) to another satisfying (I), and failed/conflicting attempts leave authoritative state unchanged or enter an explicit recoverable state. Then show the implementation admits only histories equivalent to those transitions. A lock proof uses common-lock exclusion and scope. A compare-update proof uses successful commit as linearization point and failed validation as no state change.

Maintain these invariants:

- terminology follows the language and object contract;
- product invariants determine atomic region scope;
- every stale observation is either harmless or validated at commit;
- synchronization authority covers all writers;
- external effects do not escape an abortable region without an outbox/reservation protocol;
- retries recompute from current state and are effect-safe;
- proposed linearization points survive failure and rollback;
- detector silence is not proof of absence;
- counterexamples are deterministic and minimized; and
- high-consequence races receive authorized domain review.

## Alternatives and Trade-Offs

**Coarse locks** make multi-field invariants direct and reduce races, but serialize work and risk convoying or deadlock. **Fine-grained locks** improve concurrency but complicate ownership, ordering, and cross-lock invariants.

**Atomic RMW** gives efficient single-location conditional transitions. It requires retry and memory-order reasoning and does not automatically cover other state. **Transactions** cover richer invariants but add conflict aborts, isolation semantics, and effect restrictions.

**Pessimistic coordination** reserves authority before work and avoids wasted conflict effort. **Optimistic versioning** permits parallel preparation and rejects stale commits, working well when conflicts are rare and effects remain reversible.

**Single ownership/message passing** serializes decisions through one owner and makes order explicit. It introduces queues, backpressure, lifecycle, and failover. **Immutable state** removes mutation races for snapshots but not races over which version becomes authoritative.

**Uniqueness constraints** provide a final authoritative guard. They do not undo duplicated work before the insert. **Idempotency keys** suppress repeated logical effects when scope, identity, expiry, and result replay are correct; they do not resolve conflicting different operations.

## Failure Modes and Misconceptions

- **“Race condition and data race are synonyms.”** Data race is a narrower memory-model category.
- **“Safe Rust, atomics, or thread-safe containers eliminate races.”** They remove specific unsafe access classes, not compound protocol defects.
- **“Each operation is atomic, so the workflow is atomic.”** Composition needs one higher-level serialization rule.
- **“A lock anywhere fixes it.”** All relevant participants must use the same authority and scope.
- **“Double-checked locking is obviously faster.”** Publication and visibility require language-specific support.
- **“A database constraint makes pre-commit effects unique.”** Losing transactions may already have emitted effects.
- **“Retry always fixes a conflict.”** Retry can duplicate effects or repeat a permanently invalid decision.
- **“Last writer wins is always a lost update.”** It may be declared policy; compare against contract.
- **“The line that stores is always the linearization point.”** Rollback, helping, and multi-stage commit can move it.
- **“No race-detector report means race-free.”** Dynamic tools cover executed supported paths.
- **“Sleeping reproduces the defect.”** Deterministic boundaries and schedule traces are stronger.
- **“Race freedom implies determinism.”** Several correct winners or output orders may remain.

## Worked Examples

### Example 1

**Question:** Is unsynchronized ordinary read/write of one shared counter a data race?

**Reasoning:** The accesses conflict, at least one writes, and no ordering/synchronization exists under the assumed memory model. Exact consequences come from the language.

**Conclusion:** It is a data race under the standard definition pattern.

### Example 2

**Question:** Can two atomic quota accesses still race logically?

**Reasoning:** Both clients can load one before either decrements, then both admit. Atomic memory events are well defined while the compound invariant fails.

**Conclusion:** Data-race freedom does not imply protocol atomicity.

### Example 3

**Question:** Does a thread-safe map make contains-then-insert safe?

**Reasoning:** Each method is safe separately. Two callers can both observe absence and perform duplicate setup before one insertion wins.

**Conclusion:** Provide an atomic entry operation or move all effects behind authoritative success.

### Example 4

**Question:** How does a version prevent lost update?

**Reasoning:** A writer reads value at version seven and commits only if version remains seven. Another successful writer advances it, causing stale commit rejection rather than overwrite.

**Conclusion:** Conditional commit turns a hidden race into explicit conflict.

### Example 5

**Question:** Why is checking a pathname then opening it a TOCTOU risk?

**Reasoning:** Namespace resolution can change between operations. The later open may refer to another object despite a correct earlier check.

**Conclusion:** Bind validation and use to a stable handle or authority-constrained primitive.

### Example 6

**Question:** A mutex protects balance but not the audit append. Is withdrawal atomic?

**Reasoning:** Another observer can see changed balance without audit, and failure can separate them permanently. The invariant spans both effects.

**Conclusion:** Serialization scope must cover the full contract or use a durable staged protocol.

### Example 7

**Question:** Is a failed compare-and-swap a linearization point?

**Reasoning:** Usually it changes no abstract state. It observes interference and causes retry or failure. Successful conditional update commonly linearizes the state change.

**Conclusion:** Linearization follows abstract effect, not merely atomic instruction execution.

### Example 8

**Question:** Can race-detector silence validate check-then-act?

**Reasoning:** If both steps use atomics, no data-race report is expected. A schedule test or invariant/history checker is needed.

**Conclusion:** Choose evidence for the defect class.

### Example 9

**Question:** Two concurrent cache fills compute the same immutable value. Must one be a bug?

**Reasoning:** If duplicate computation and either identical winner are allowed, the race is benign by contract. Resource limits or non-idempotent effects may make it harmful.

**Conclusion:** Schedule dependence is defective only relative to requirements.

### Example 10

**Question:** A medication service uses a database uniqueness constraint for one active prescription but sends pharmacy orders before commit. Is it safe?

**Reasoning:** Concurrent transactions can both send before one loses the insert. Database uniqueness does not retract the external order. Use durable intent/outbox or reserve authority before the effect, and require named clinical, pharmacy, safety, privacy, security, data, and regulatory review.

**Conclusion:** High-consequence atomicity must include external effects and human authority.

## Cross-Program Connections

- [Interleavings and State-Space Explosion](003-interleavings-and-state-space-explosion.md) provides schedule enumeration and reduction limits.
- [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md) supplies invariants and repair progress trade-offs.
- The [CONPAR roadmap](../ROADMAP.md) deepens critical sections, locks, atomics, happens-before, and linearizability.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns transactions, constraints, isolation, and lost-update policies.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) owns file handles, namespaces, and kernel atomicity.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) applies conditional requests, idempotency, and authoritative service operations.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) treats TOCTOU and stale authorization as exploitable integrity races.

## References

1. Oracle, “Java Language Specification, Java SE 26, Chapter 17: Threads and Locks,” accessed August 29, 2026, [official specification](https://docs.oracle.com/javase/specs/jls/se26/html/jls-17.html).
2. The Go Authors, “The Go Memory Model,” version June 6, 2022, [official specification](https://go.dev/ref/mem).
3. The Rust Project Developers, “Behavior Considered Undefined,” accessed August 29, 2026, [official Rust Reference](https://doc.rust-lang.org/reference/behavior-considered-undefined.html).
4. Maurice Herlihy and Jeannette Wing, “Linearizability: A Correctness Condition for Concurrent Objects,” *ACM TOPLAS* 12(3), 1990, [DOI](https://doi.org/10.1145/78969.78972).
5. Hans-J. Boehm and Sarita V. Adve, “Foundations of the C++ Concurrency Memory Model,” *PLDI 2008*, [DOI](https://doi.org/10.1145/1375581.1375591).
6. Cormac Flanagan and Stephen N. Freund, “FastTrack: Efficient and Precise Dynamic Race Detection,” *PLDI 2009*, [DOI](https://doi.org/10.1145/1542476.1542490).
7. Shan Lu, Joseph Tucek, Feng Qin, and Yuanyuan Zhou, “AVIO: Detecting Atomicity Violations via Access Interleaving Invariants,” *ASPLOS 2006*, [bibliographic record](https://dblp.org/rec/conf/asplos/LuTQZ06).
8. Shan Lu, Soyeon Park, Eunsoo Seo, and Yuanyuan Zhou, “Learning from Mistakes: A Comprehensive Study on Real World Concurrency Bug Characteristics,” *ASPLOS 2008*, [DOI](https://doi.org/10.1145/1346281.1346323).
9. Maurice Herlihy et al., *The Art of Multiprocessor Programming*, 2nd ed., Morgan Kaufmann, 2020.
10. Austin T. Clements et al., “The Scalable Commutativity Rule,” *SOSP 2013*, [DOI](https://doi.org/10.1145/2517349.2522712).

## Exercises

### Exercise 1

Define data race, race condition, atomic action, atomicity violation, and linearization point. Give one race condition with no data race.

### Exercise 2

Construct the minimum interleaving that oversubscribes a one-slot quota with separate atomic load and store. State the invariant and intended transition.

### Exercise 3

Repair an absent-key-then-create workflow that allocates an external resource before inserting a unique database row. Address failures, retries, and cleanup.

### Exercise 4

Compare a coarse mutex, compare-and-update loop, database conditional update, and single-owner actor for multi-client reservation.

### Exercise 5

A hospital scheduling system must prevent two procedures from reserving one operating room while coordinating staff notifications and billing holds. Design atomicity boundaries, evidence, failure handling, and required human review.

## Answers to the Exercises

### Answer 1

A data race is conflicting memory access, including a write, without ordering required by the language. A race condition is any correctness dependence on admissible relative timing. An atomic action appears indivisible at a declared abstraction boundary. An atomicity violation interleaves an intended compound action into a history excluded by its sequential contract. A linearization point is where a completed operation can be viewed as taking effect between invocation and response. Two atomic loads of quota followed by atomic stores can be data-race-free yet admit two reservations, a logical race.

### Answer 2

Invariant is (accepted <= capacity), initially capacity one and accepted zero. Intended transition is reserve-if-positive: if remaining exceeds zero, decrement and return success as one indivisible decision; otherwise reject. Trace: A loads one; B loads one; A stores zero and succeeds; B stores zero or decrements from its stale decision and succeeds. Both accepted while capacity is one. One conditional RMW, lock region, or authoritative transaction must make exactly one success linearize.

### Answer 3

Do not let irreversible allocation escape before authoritative ownership. Options include first inserting a durable pending row under the uniqueness constraint, letting only its winner allocate, then marking ready; or writing transactional outbox intent processed idempotently by a worker. Persist idempotency identity and resource correlation. On conflict, return/replay the winner. On allocation failure, mark retryable/terminal state. On crash, reconciliation resumes or compensates. Cleanup must prove ownership before deletion. A local mutex is insufficient across processes.

### Answer 4

A coarse mutex directly covers multi-field local state and simplifies proof but serializes and is process-local. A compare-update loop provides nonblocking optimistic commit for state representable in one atomic snapshot but requires recomputation, memory-order, retry, and reclamation reasoning. Database conditional update centralizes cross-process authority and durability but can conflict, block, or depend on isolation. A single-owner actor makes order and ownership explicit but adds queue capacity, backpressure, failover, and availability concerns. Choose the mechanism at the invariant's authority and verify external effects separately.

### Answer 5

Make room/time reservation an authoritative conditional transition over room version, time interval, procedure identity, and status. Only successful durable reservation may create staff and billing intents, preferably in the same transaction through an outbox; downstream consumers use stable idempotency keys. Define cancellation, reschedule, partial notification, expired holds, reconciliation, and compensation. Test deterministic competing requests, stale versions, retries, crashes before/after commit, duplicate delivery, and recovery; audit histories against one legal reservation order. Technical checks cannot decide clinical priority, staffing adequacy, lawful data use, billing policy, or acceptable disruption. Named clinical-operations, patient-safety, scheduling, staffing, finance, privacy, security, reliability, data, quality, and regulatory authorities must review. No external review is claimed here.
