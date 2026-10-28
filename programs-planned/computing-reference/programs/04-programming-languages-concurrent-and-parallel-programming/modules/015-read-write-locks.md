---
module_id: CONPAR-015
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 15
title: Read-Write Locks
status: complete
last_verified: 2026-08-29
---

# Read-Write Locks

## One-Page Review

### Governing question

When does admitting many readers but only one writer preserve a shared object's invariant and improve useful concurrency, and which progress, upgrade, visibility, failure, and lifecycle rules must be specified rather than assumed?

### Essential definitions

- A **read-write lock** has a shared/read mode and an exclusive/write mode.
- A **reader** holds shared admission and promises not to mutate the protected representation.
- A **writer** holds exclusive admission and may read or mutate the complete protected representation.
- **Compatibility** permits reader-reader overlap but excludes writer-reader and writer-writer overlap.
- **reader preference** admits readers while writers wait; **writer preference** blocks new readers behind a waiting writer.
- **phase-fair** policy alternates or batches reader and writer phases under a defined ordering.
- **writer starvation** is indefinite writer postponement by readers; **reader starvation** is the dual.
- **upgrade** attempts read-to-write conversion; **downgrade** converts write to read without an unprotected gap.
- An **optimistic read** reads without a stable shared hold and later validates a version or stamp.
- **lock granularity** is the amount of state protected by one lock; **sharding** partitions it among locks.
- **linearization point** is the instant at which an operation takes effect in its abstract history.
- **quiescence** means no holder, waiter, callback, or future accessor can use the lock.

### Central model, mechanism, or theorem

Let (R) be the number of active readers and (W) indicate an active writer. Legal held states satisfy (R>=0), (W in {0,1}), and:

(W=1 implies R=0).

A reader may enter only when no writer holds the lock and the admission policy permits it. A writer may enter only from (R,W)=(0,0). These rules prove incompatible critical sections do not overlap. They do not prove starvation freedom, bounded latency, protected-data correctness, or performance benefit.

### Critical invariants

Every protected-data access uses the appropriate mode. Readers do not mutate representation, including hidden caches or lazy fields. Writers hold exclusivity across each invariant-restoring transition. Failed or cancelled acquisition creates no unlock obligation; successful acquisition does. Every exit unlocks the matching mode exactly once. Upgrade never waits while retaining an ordinary read hold unless the API explicitly guarantees conversion. Downgrade, if needed, preserves coverage. Memory visibility and recursion claims follow the selected API. Destruction occurs only after quiescence.

### Common failures

Teams choose an RW lock merely because reads outnumber writes; hold a read lock during slow I/O; mutate lazy caches under read mode; assume FIFO or writer preference; recursively read while a writer waits; have two readers upgrade and deadlock; release read then write without rechecking; implement downgrade with a gap; use monitoring counts for check-then-act; unlock the wrong mode; hold a blocking guard across suspension; copy or move a lock illegally; ignore panic/exception recovery; or benchmark averages while tail latency and cache-line contention worsen.

### Compact example

A catalog has two readers and one updater. State (2,0) is legal: both readers observe one stable version. The updater waits. After both readers leave, state becomes (0,0); policy admits the updater to (0,1). It changes all correlated fields, restores the catalog invariant, then releases. A later reader sees the completed state through the API's synchronization guarantee. Nothing in this trace proves the updater will eventually be selected under every policy.

### Connections

[Mutexes and Mutual Exclusion](012-mutexes-and-mutual-exclusion.md) establishes exclusive ownership and protected invariants; [Condition Variables and Predicate Waiting](013-condition-variables-and-predicate-waiting.md) separates predicates from wakeups; [Semaphores and Resource Counting](014-semaphores-and-resource-counting.md) separates capacity from ownership. The [program roadmap](../ROADMAP.md) next develops barriers, latches, phasers, queues, lock ordering, and thread pools.

## Governing Question

How can an engineer prove many-reader/one-writer exclusion, decide whether shared-read concurrency repays its overhead, and specify admission, upgrade, downgrade, cancellation, memory visibility, recovery, and lifetime without importing guarantees the chosen API does not make?

An RW lock is not a universally faster mutex. It is a compatibility mechanism plus an admission policy. Correct selection begins with a named state invariant and measured workload, not the label “read-heavy.”

## Why This Matters

Shared structures are often queried more frequently than they are changed: routing tables, configuration snapshots, symbol indexes, catalogs, metadata caches, and in-memory trees. A mutex serializes every query even when read operations would be mutually compatible. An RW lock may let them use several cores concurrently.

That possible concurrency has costs. The implementation tracks reader counts, queues or state bits, and memory-order transitions. Reader entry and exit contend on shared metadata. Writers wait for all active readers. A long reader can dominate tail latency, and a stream of new readers can starve writers under permissive policy. For a tiny critical section, a plain mutex can be faster and easier to reason about.

The abstraction also invites semantic mistakes. “Read” means no mutation of the protected representation—not merely a method named `get`. Lazy initialization, access-time updates, reference-count changes inside the object, iterators that repair structure, and supposedly benign caches may write. Conversely, a writer that replaces an immutable snapshot might need only a short exclusive publication step.

Current APIs intentionally differ. POSIX.1-2024 defines read and write acquisition, try/timed variants, memory synchronization, priority qualifications, ownership, and lifecycle. Java SE 26 `ReentrantReadWriteLock` offers optional fairness, reentrancy, downgrade support, interruptible acquisition, and conditions only on the write lock. Rust 1.98 delegates priority policy to the operating system and describes poisoning. Go's current `sync.RWMutex` blocks new readers behind a waiting writer and prohibits upgrade, downgrade, and recursive read locking. Portable reasoning must stay inside the selected contract.

## Prerequisites and Retrieval

Retrieve:

- protected-state invariants, owner obligations, memory visibility, timeouts, and destruction from [Mutexes and Mutual Exclusion](012-mutexes-and-mutual-exclusion.md);
- predicate loops, cancellation wakeups, and monitoring-versus-control distinctions from [Condition Variables and Predicate Waiting](013-condition-variables-and-predicate-waiting.md);
- permit-accounting and admission-policy distinctions from [Semaphores and Resource Counting](014-semaphores-and-resource-counting.md);
- safety, liveness, starvation, fairness, and schedule reasoning from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md); and
- set cardinality, implication, partial orders, linearizability, cache coherence, exception safety, and monotonic deadlines.

Retrieval prompt: enumerate legal (R,W) states for at most three readers. Then trace two readers, one waiting writer, one arriving reader, and both reader- and writer-preferring policies. Mark safety facts separately from progress choices.

## Learning Objectives

After completing this module, a learner can:

1. formalize reader-writer compatibility and prove exclusion safety;
2. name the exact invariant and classify every access as read or write;
3. distinguish reader-, writer-, fair-, and phase-oriented admission policies;
4. analyze writer starvation, reader starvation, convoys, and tail latency;
5. design safe release-and-recheck upgrade or supported atomic conversion;
6. preserve coverage during supported downgrade and handle exceptions;
7. compare RW locks with mutexes, sharding, snapshots, optimistic reads, and RCU;
8. test finite histories and benchmark workloads without universal claims; and
9. identify safety-critical shared-state decisions requiring named human review.

## Core Exposition

### Start with compatibility, not implementation

Model the lock's held state as active-reader set (A) and optional writer (w). Reader critical sections are pairwise compatible. A writer conflicts with every reader and writer. The compatibility matrix is:

<!-- bijux-verify: {"id":"rw-compatibility-matrix","mode":"data","language":"text","toolchain":"none","reason":"The matrix records abstract mode compatibility rather than an executable program."} -->
```text
requested \ held | none | read | write
read             | yes  | yes  | no
write            | yes  | no   | no
```

Acquisition atomically changes admission state; it does not make the application operation correct by itself. A reader must observe the protected invariant at entry and preserve it. A writer may temporarily violate internal relations only while excluded, and must restore them before release.

The lock's read/write labels are promises. If a “reader” increments a hit counter stored inside the same protected object, reader-reader overlap is no longer compatible. Move the counter to an atomic or separate shard, eliminate it, or use write mode.

### The safety proof

Assume initialization (A=empty,w=none). A read acquisition requires (w=none) and produces (A union {t},none). A read release removes its matching hold. A write acquisition requires (A=empty,w=none) and produces (empty,t). A write release returns to (empty,none).

Induction over legal transitions preserves:

- at most one writer exists;
- a writer never overlaps an active reader;
- each successful hold has one matching release obligation; and
- the protected invariant holds at every unlocked boundary and throughout each reader interval.

The fourth claim depends on application review, not merely lock state. The proof also assumes all accesses participate in the same protocol and the API supplies the required memory synchronization. An unsynchronized alias invalidates it.

### Admission policy is a separate progress contract

When readers and writers wait together, the compatibility rule does not select the next entrant. Major policies include:

- **reader preference:** admit a reader whenever no writer is active, maximizing read batching but risking writer starvation;
- **writer preference:** once a writer waits, stop admitting new readers, allowing the active reader phase to drain but potentially delaying readers;
- **approximately FIFO/fair:** respect queue arrival subject to batching compatible readers, often improving bounded bypass at throughput cost; and
- **phase-fair:** alternate reader and writer phases with stated batch rules.

Do not infer policy from the type name. Java's fair mode is approximately arrival ordered, while its untimed try-lock methods can bypass the fair setting. Rust deliberately leaves priority policy platform-dependent. Go documents a writer-progress rule that blocks new readers when a writer waits, with consequences for recursive read attempts. POSIX contains scheduling and priority qualifications; portable application claims must match them exactly.

Safety permits starvation. A system can maintain perfect exclusion while a writer never enters. Define the required property—eventual entry under finite holds, bounded bypass, deadline success probability, or maximum wait—and test the supported one.

### When shared reading pays

Read frequency alone is insufficient. Estimate:

- fraction of operations requiring write mode;
- read and write hold-time distributions, especially tails;
- number of simultaneously runnable cores and threads;
- time spent doing actually parallel work under read mode;
- cost of reader-count cache-line traffic and wakeups;
- interaction with NUMA placement and preemption;
- writer latency requirement; and
- contention displaced to objects used inside the critical section.

An RW lock is promising when read sections are substantial, independent, frequent, and parallel; writes are sufficiently rare and short; and progress policy fits the service. It often loses when reads are tiny, the object itself causes cache misses, writers are frequent, one reader blocks, or the runtime cannot schedule readers concurrently.

Benchmark a mutex and candidate alternatives with production-like read/write ratios, core counts, data sizes, hold-time variance, cancellations, and preemption. Report throughput plus reader and writer percentiles, starvation events, CPU time, context switches, and scalability. A microbenchmark is evidence for its stated environment, not a theorem.

### Scope every hold around invariant access

Acquire after inputs are validated and before the first protected access. Under read mode, copy or derive the minimal stable result, then release before slow formatting, logging, callbacks, network I/O, disk I/O, or waiting on another subsystem. Under write mode, compute expensive independent work first, acquire, revalidate assumptions, commit the minimal transition, and release.

Returning an iterator, pointer, slice, or reference into protected mutable storage can outlive the guard and invalidate the proof. Return an owned snapshot, couple the view's lifetime to the guard through the type system, or use immutable/versioned storage.

Callbacks under either mode are dangerous: unknown code can block, reenter, attempt upgrade, or acquire another lock in a conflicting order. Treat effect scope and lock scope as separate designs.

### Upgrade is not ordinary acquisition

Suppose readers (a) and (b) both decide to write while retaining read holds. Each waits for all readers to leave, but each is itself a reader. This is deterministic hold-and-wait deadlock.

Most designs should:

1. read the state and record a version or predicate;
2. release read mode;
3. acquire write mode;
4. recheck because another writer may have changed the state; and
5. mutate only if the condition still holds.

This is not atomic upgrade; the gap is part of the protocol. If the action must occur exactly once, use the recheck to detect that another writer completed it. Some specialized locks offer one upgradeable-reader role or an atomic conversion operation. Use it only with documented cancellation, fairness, and ownership semantics.

### Downgrade must preserve coverage

Downgrade is useful when a writer publishes a state and then needs a stable read view while allowing other readers. A supported reentrant sequence can acquire read while holding write, then release write. At no instant is the object unprotected.

<!-- bijux-verify: {"id":"rw-downgrade-schema","mode":"schematic","language":"text","toolchain":"none","reason":"Language-neutral pseudocode illustrates a supported downgrade protocol whose exact calls and guarantees are API-specific."} -->
```text
acquire_write()
try:
    mutate_and_restore_invariant()
    acquire_read_while_holding_write()
finally:
    release_write()
try:
    consume_stable_view()
finally:
    release_read()
```

If read acquisition fails or throws, cleanup must still release write and must not release an unowned read hold. An API such as Go `RWMutex` that forbids downgrade requires a different design, usually publication of an immutable snapshot or release-and-reacquire with revalidation.

### Reentrancy and recursive reading

Reentrancy is API-specific, mode-specific state. Java permits a writer to take read mode and supports recursive holds with matched unlock counts. POSIX permits multiple read holds by a thread but defines other ownership conditions separately. Rust warns that a second read may deadlock depending on policy if a writer is waiting. Go explicitly prohibits recursive read locking because a waiting writer blocks new readers.

Never use recursion to compensate for unclear lock ownership. Document whether a function requires a held mode, acquires internally, or accepts an already-stable snapshot. Lock-order and mode assertions in tests can catch accidental reentry. Every recursive success adds a release obligation.

### Memory visibility and protected publication

Exclusion and visibility are related but distinct. A correct API supplies synchronization edges so writes completed before exclusive unlock become visible through a later compatible successful acquisition according to its memory model. POSIX lists successful RW-lock operations as memory-synchronizing. Go specifies relations among `Unlock`, `RLock`, `RUnlock`, and later `Lock`. Java lock implementations follow the `Lock` memory-synchronization contract.

Do not mix protected non-atomic access with unsynchronized “fast” reads. The absence of an active writer is not observable without synchronization. If a pointer to immutable state is published atomically, specify the publication and reclamation protocol separately.

A read lock stabilizes only the state governed by that lock. Following a protected pointer to another mutable object requires that object's ownership protocol. Keep the protection domain explicit.

### Cancellation, interruption, timeout, and failure

Blocking, try, timed, and interruptible methods have distinct postconditions. Cleanup unlocks only after confirmed success. Use one monotonic deadline across retries and mode changes. If cancellation races with acquisition, follow the API's specified outcome and install cleanup across the ownership boundary.

Inside a reader, exceptions normally leave shared state unchanged; hidden mutation can violate that assumption. Inside a writer, an exception can leave the invariant broken. Prefer transaction-like local computation followed by a small commit, or define repair/poison behavior. Rust poisoning is advisory error propagation with documented mode details, not automatic rollback. POSIX and Go do not supply equivalent application repair.

Condition waiting ordinarily requires exclusive mode because the predicate may span mutable state. Java provides conditions on the write lock and rejects them on the read lock. For complex predicates, a mutex/condition design can be clearer than forcing them into an RW-lock protocol.

### Optimistic reads and immutable snapshots

An optimistic read obtains a version or stamp, reads candidate fields, then validates that no conflicting write occurred. If validation fails, retry under a stable mode. Correctness depends on what can safely be read before validation, overflow behavior, memory ordering, reclamation, and whether the candidate can trigger effects. Never perform irreversible I/O from unvalidated data.

Copy-on-write or immutable snapshot publication moves most read work outside locks. Writers create a complete new version and atomically publish it. Readers pay reference-management and memory costs but avoid reader-count contention. Reclamation must ensure no reader uses a retired version.

Read-copy-update specializes this idea with read-side critical sections and deferred reclamation. It is not “RW lock without writers”; its grace-period, memory-order, update, and lifecycle protocols require dedicated treatment.

### Sharding and lock composition

Partition independent keys across locks to reduce shared reader metadata and writer interference. The shard function and resize protocol become invariants. An operation spanning shards needs a global order, optimistic validation, or a higher-level transaction. Otherwise read-to-write mode changes across several locks reintroduce deadlock.

Avoid holding one lock while acquiring another when a snapshot suffices. If nesting is necessary, define a total order over lock identity and mode. Upgrade is especially hazardous because the held read edge and requested write edge can form cycles invisible in a simple lock-name order.

### Blocking locks and suspension

Do not hold a blocking thread RW lock across an asynchronous suspension unless the runtime and abstraction explicitly support it and the awaited operation is proven bounded and non-reentrant. The task may suspend while excluding writers, the executor thread may block, and another task needed for progress may require the lock.

Use an async-aware synchronization primitive, copy a snapshot before awaiting, move effects outside the guard, or serialize ownership in an actor. “The compiler accepts it” does not establish scheduler progress.

### Lifecycle, observability, and testing

Initialize before publication. Do not copy or relocate a lock when the API forbids it. Destroy only after no holder, waiter, callback, returned view, or future accessor remains. Queue counts and owner queries are monitoring estimates, not control predicates.

Measure acquisitions by mode, hold and wait distributions, maximum waiter age, timeouts, cancellation, failed try-locks, reader batch size, writer queue age, upgrade attempts, and poison/repair events. Correlate long holds with operation identity without exposing sensitive data.

Tests should force reader-reader overlap, writer exclusion, waiting-writer admission, recursive edge cases, upgrade rejection, release-and-recheck races, downgrade failures, cancellation, exception paths, lock-order cycles, and shutdown. Controlled schedules and finite models explore semantics; stress, race detectors, model checkers, and production telemetry provide complementary evidence.

## Definitions and Notation

Let active-reader set be (A), reader count (R=|A|), and writer owner (w in T union {none}). Legal states satisfy (R>=0) and (w!=none implies R=0). Let waiting readers and writers be (Q_R) and (Q_W). Admission policy (P) maps the held state and wait queues to eligible entrants.

Protected application state is (x) with invariant (I(x)). Each successful reader interval must observe and preserve (I); each writer must re-establish (I) before exclusive release. A version (v) changes on committed writes where an optimistic protocol requires it.

Reader wait (L_R), writer wait (L_W), hold times (H_R,H_W), throughput, and starvation indicators describe performance and progress. None follows from the exclusion invariant alone.

## Mechanisms, Invariants, or Proof Structure

Apply this workflow:

1. **Name the state and invariant.** List every alias and hidden mutation.
2. **Build compatibility.** Prove reader-reader overlap is actually safe.
3. **Select policy.** State reader/writer admission and required progress.
4. **Scope holds.** Move I/O, callbacks, blocking, and independent computation out.
5. **Define conversion.** Prefer release, acquire, and recheck for upgrade.
6. **Specify visibility.** Use only the API's memory-model guarantees.
7. **Handle failure.** Match successful modes to exactly one release and repair writer failures.
8. **Order composition.** Define nesting across locks, shards, and modes.
9. **Own lifecycle.** Establish initialization, publication, shutdown, and quiescence.
10. **Measure and test.** Compare a mutex and alternatives under adversarial schedules and representative load.

Maintain:

- (w!=none implies A=empty) and at most one writer;
- every protected access uses a compatible held mode;
- readers perform no representation mutation;
- the application invariant holds throughout reads and at unlocked boundaries;
- each successful acquisition creates one mode-correct release obligation;
- failed acquisition creates none;
- ordinary readers never wait for write while retaining read;
- downgrade has continuous protection or explicit revalidation;
- progress and memory claims match the selected API; and
- no participant survives destruction.

The executable model below enumerates all order-preserving enter/exit histories for two labeled readers and one writer. It accepts only histories preserving compatibility.

<!-- bijux-verify: {"id":"rwlock-compatibility-histories","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidate_histories=90\ncompatible_histories=14\nrejected_histories=76\nmaximum_parallel_readers=2\n","stderr":""}} -->
```python
tasks = ("R1", "R2", "W")
histories = []


def extend(prefix, progress):
    if len(prefix) == 2 * len(tasks):
        histories.append(tuple(prefix))
        return
    for task in tasks:
        step = progress[task]
        if step < 2:
            progress[task] += 1
            event = "enter" if step == 0 else "exit"
            extend(prefix + [(task, event)], progress)
            progress[task] -= 1


extend([], {task: 0 for task in tasks})
compatible = 0
maximum_readers = 0
for history in histories:
    readers = 0
    writer = False
    valid = True
    local_maximum = 0
    for task, event in history:
        if task == "W":
            if event == "enter":
                if writer or readers:
                    valid = False
                writer = True
            else:
                writer = False
        elif event == "enter":
            if writer:
                valid = False
            readers += 1
            local_maximum = max(local_maximum, readers)
        else:
            readers -= 1
    if valid:
        compatible += 1
        maximum_readers = max(maximum_readers, local_maximum)

print(f"candidate_histories={len(histories)}")
print(f"compatible_histories={compatible}")
print(f"rejected_histories={len(histories) - compatible}")
print(f"maximum_parallel_readers={maximum_readers}")
```

Limitations: this finite sequential event model does not implement a lock, execute threads, choose among waiters, model weak memory, cancellation, recursion, upgrades, or prove arbitrary application invariants. It checks only the stated compatibility predicate for three labeled participants.

## Alternatives and Trade-Offs

**A mutex** has simpler ownership, progress, and cost behavior and often wins for short sections or frequent writes. Always include it as a baseline.

**An RW lock** allows compatible readers but centralizes admission metadata and complicates writer latency, recursion, and conversion.

**Sharded locks** reduce interference across keys but make cross-shard operations and resizing harder.

**Immutable snapshots/copy-on-write** give cheap stable reads and costly updates, allocation, and reclamation.

**Optimistic/versioned reads** avoid shared locking on the fast path but require safe speculative access, validation, and retry.

**Concurrent data structures** localize synchronization and may scale better, though their operation-level guarantees may not cover multi-operation invariants.

**Actors or ownership transfer** serialize mutation and remove shared guards; message latency, mailbox bounds, and snapshot publication become the design concerns.

**RCU or epoch schemes** offer specialized read paths with demanding memory-order and reclamation protocols. They are appropriate only when those protocols are owned and verified.

## Failure Modes and Misconceptions

- **“More reads means faster.”** Duration, cores, metadata contention, writes, and policy decide.
- **“Read methods never write.”** Lazy fields, caches, iterators, and statistics can mutate.
- **“Safety implies writer progress.”** Exclusion can hold while a writer starves forever.
- **“Fair means strict FIFO.”** Read batching, reentrancy, try-locks, cancellation, and API wording qualify it.
- **“Upgrade is read then write.”** Retaining read while waiting can deadlock; releasing creates a recheck gap.
- **“Downgrade is write unlock then read lock.”** That gap admits another writer.
- **“A guard can escape.”** Views into mutable storage must not outlive protection.
- **“Counts are control state.”** Monitoring observations race with acquisition.
- **“Read recursion is harmless.”** A queued writer can make a second read block.
- **“Poisoning rolls back.”** It reports possible inconsistency; application recovery remains.
- **“Blocking across await is safe.”** It can stall executors and create scheduler deadlock.
- **“A passing benchmark proves selection.”** It supports only the measured workload and environment.

## Worked Examples

### Example 1

**Question:** Are states (3,0), (0,1), and (1,1) legal?

**Reasoning:** Three readers are pairwise compatible, and one writer alone is valid. A reader and writer overlap violates the compatibility implication.

**Conclusion:** The first two states are legal; (1,1) is not.

### Example 2

**Question:** A lookup increments an in-object access counter under read mode.

**Reasoning:** Two lookups can concurrently write the counter, so their sections are not compatible even if the primary lookup data is unchanged.

**Conclusion:** Remove, atomically separate, shard, or protect the counter with write mode.

### Example 3

**Question:** Readers arrive continuously under reader preference while one writer waits.

**Reasoning:** Every new reader is compatible with active readers, so the reader count need never reach zero.

**Conclusion:** Safety holds but writer starvation is possible; select a progress policy matching the requirement.

### Example 4

**Question:** Two readers each retain read mode while acquiring write mode.

**Reasoning:** Each writer request requires zero readers, but each requester contributes one retained reader. Neither can enable the other's request.

**Conclusion:** Ordinary read-to-write acquisition deadlocks; release and recheck or use a documented conversion protocol.

### Example 5

**Question:** Reader A releases, acquires write, and assumes its earlier predicate remains true.

**Reasoning:** Writer B can commit during the gap. A's earlier observation is stale although A now has exclusivity.

**Conclusion:** Re-evaluate the predicate and version after write acquisition.

### Example 6

**Question:** A writer releases write before acquiring read to “downgrade.”

**Reasoning:** Another writer can enter between the calls and replace the state, so the original stable view is lost.

**Conclusion:** Use supported continuous downgrade or release/reacquire with explicit revalidation.

### Example 7

**Question:** Ninety percent of operations are ten-nanosecond reads; writes hold for milliseconds.

**Reasoning:** Read frequency alone ignores reader-accounting overhead and long writer blocking. A mutex or immutable snapshot can outperform and reduce tails.

**Conclusion:** Benchmark realistic hold distributions and compare simpler designs.

### Example 8

**Question:** What does the executable enumeration establish?

**Reasoning:** Among 90 order-preserving histories for two readers and one writer, 14 preserve compatibility, 76 contain forbidden overlap, and safe histories can reach two readers.

**Conclusion:** The finite model recomputes exclusion, not fairness, memory behavior, or implementation correctness.

### Example 9

**Question:** May a task retain a read guard while awaiting a remote request?

**Reasoning:** Suspension is unbounded, writers remain excluded, and the completion path may itself need the lock.

**Conclusion:** Copy a stable result and release before awaiting, or use a deliberately designed async protocol.

### Example 10

**Question:** Can an RW lock alone approve concurrent reads and updates of railway interlocking routes?

**Reasoning:** Exclusion does not establish physical topology, fail-safe state, timing, hardware faults, operational rules, redundancy, or certification.

**Conclusion:** No. Named authorized railway signaling, systems, controls, hardware, real-time, functional-safety, verification, cybersecurity, human-factors, and regulatory reviewers must approve the real system. No external review is claimed.

## Cross-Program Connections

- **Programming languages:** effects, exceptions, ownership types, guards, and memory models define protected access.
- **Operating systems:** schedulers, parking, priority inversion, and process sharing influence progress.
- **Algorithms and data structures:** trees, maps, indexes, sharding, snapshots, and linearizability determine useful granularity.
- **Distributed systems:** replica reads and leader writes require consistency protocols, not a process-local RW lock.
- **Performance engineering:** cache coherence, NUMA, hold distributions, and tail latency determine whether reader parallelism pays.
- **Formal methods:** compatibility relations, invariants, wait-for graphs, and temporal progress properties separate safety from policy.

## References

1. P. J. Courtois, F. Heymans, and D. L. Parnas, “Concurrent Control with ‘Readers’ and ‘Writers’,” *Communications of the ACM* 14(10), 1971, [doi:10.1145/362759.362813](https://doi.org/10.1145/362759.362813).
2. Gregory R. Andrews, *Concurrent Programming: Principles and Practice*, Benjamin/Cummings, 1991.
3. David R. Butenhof, *Programming with POSIX Threads*, Addison-Wesley, 1997.
4. IEEE and The Open Group, *POSIX.1-2024*, §2.9.6 “Thread Read-Write Locks,” [official specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/V2_chap02.html) (retrieved 2026-08-29).
5. IEEE and The Open Group, *POSIX.1-2024*, “pthread_rwlock_rdlock,” [official specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_rwlock_rdlock.html) (retrieved 2026-08-29).
6. IEEE and The Open Group, *POSIX.1-2024*, “pthread_rwlock_wrlock,” [official specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_rwlock_wrlock.html) (retrieved 2026-08-29).
7. Oracle, “ReentrantReadWriteLock,” Java SE 26 API, [official API](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/locks/ReentrantReadWriteLock.html) (retrieved 2026-08-29).
8. Rust Project, “RwLock,” Rust 1.98 standard library, [official API](https://doc.rust-lang.org/std/sync/struct.RwLock.html) (retrieved 2026-08-29).
9. The Go Authors, “sync.RWMutex,” Go standard library, [official API](https://pkg.go.dev/sync#RWMutex) (retrieved 2026-08-29).
10. Maurice Herlihy et al., *The Art of Multiprocessor Programming*, second edition, Morgan Kaufmann, 2020.

## Exercises

### Exercise 1

State the legal-state invariant and classify read-read, read-write, and write-write compatibility. Explain what remains unproved.

### Exercise 2

Construct a writer-starvation trace under reader preference and a two-upgrader deadlock trace. Identify the distinct causes.

### Exercise 3

Audit a “read” operation that lazily initializes a cache, returns an internal iterator, logs under the guard, and awaits remote I/O.

### Exercise 4

Choose among mutex, RW lock, sharding, and immutable snapshots for a large catalog with 99% reads, hourly batch writes, and strict ten-millisecond writer latency. Define evidence.

### Exercise 5

A medical monitoring system protects alarm thresholds with an RW lock. State what chapter verification proves and what requires named authorized review.

## Answers to the Exercises

### Answer 1

Let (R>=0) and (W in {0,1}); require (W=1 implies R=0). Read-read is compatible, while read-write and write-write are incompatible. Legal atomic acquisition and matching release preserve this held-state invariant. It does not prove the application invariant, because a reader may secretly mutate or an alias may bypass the lock. It also does not prove fairness, starvation freedom, bounded latency, memory visibility beyond the API, failure recovery, or performance benefit.

### Answer 2

For starvation, reader A holds; writer W queues; reader-preferring policy admits B before A leaves; C arrives before B leaves, and this overlapping chain continues, so (R) never reaches zero. Safety holds, but admission policy denies progress. For upgrade deadlock, A and B both hold read and each requests write without releasing. Each request needs (R=0), yet A and B each keep (R>=1). This is hold-and-wait caused by conversion, independent of reader preference. Repair with writer-aware admission for starvation and release/acquire/recheck or one documented upgradeable role for conversion.

### Answer 3

Lazy initialization is mutation and requires write mode or separate synchronized state. An internal iterator must not outlive the guard; return an owned snapshot or guard-bound view. Logging can block, reenter, or acquire locks, so capture minimal data and log after release. Remote I/O and suspension must occur outside the blocking guard. Refactor into validate/compute, acquire and copy or commit, release, then perform effects. Recheck under write mode when assumptions can change.

### Answer 4

The ratio and size suggest testing an RW lock and immutable snapshots, but the strict writer bound rules out relying on unspecified reader preference. A mutex is the correctness baseline. Sharding helps if reads and writes partition by key, but an hourly whole-catalog batch may touch every shard. Immutable publication makes readers stable and keeps the exclusive publication short, at memory/reclamation cost. Measure production-sized data across target core/NUMA configurations: throughput, reader and writer wait/hold percentiles, maximum writer age, allocation, cache misses, and cancellation. Reject any design that cannot support and verify the ten-millisecond contract under bounded assumptions.

### Answer 5

Internal checks can validate compatibility transitions, matched mode release, source citations, executable finite counts, local links, upgrade/downgrade reasoning, and exercise correspondence. They cannot establish sensor accuracy, clinical alarm thresholds, physiological timing, device hazards, fail-safe behavior, human response, cybersecurity controls, regulatory compliance, or deployment fitness. Named authorized clinical, medical-device systems, hardware, real-time, functional-safety, software verification, cybersecurity, human-factors, quality, and regulatory reviewers must approve the real requirements, implementation, evidence, and deployment. This chapter claims no external review.
