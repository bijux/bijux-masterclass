---
module_id: CONPAR-012
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 12
title: Mutexes and Mutual Exclusion
status: complete
last_verified: 2026-08-29
---

# Mutexes and Mutual Exclusion

## One-Page Review

### Governing question

What exact ownership, exclusion, memory synchronization, failure, fairness, and lifetime contract does a mutex provide, and what additional proof is still required for the state it guards?

### Essential definitions

- A **mutex** is an ownership-based synchronization primitive that permits at most one successful exclusive owner at a time.
- **Lock/acquire** waits or attempts to change the mutex from unowned to owned by the caller according to its API.
- **Unlock/release** relinquishes ownership and commonly publishes prior protected writes to a subsequent successful acquirer.
- **Mutual exclusion** is the safety property that two distinct participants never simultaneously own the same exclusive mutex.
- A **critical section** is code executed while holding the relevant mutex; its correctness depends on the protected invariant, not merely exclusion.
- A **guard** is a scoped value whose lifetime represents ownership and whose destruction or scope exit releases the mutex.
- A **reentrant/recursive mutex** lets its current owner acquire again and requires matching releases; a non-reentrant mutex does not.
- **Contention** occurs when multiple participants compete for the same mutex.
- **Barging** lets a newcomer acquire before queued waiters; **fair admission** constrains such bypass under a declared policy.
- **Spinning** repeatedly checks availability while consuming execution capacity; **parking** blocks the waiter so the scheduler may run other work.
- **Lock convoying** occurs when serialized ownership and scheduling delays make many waiters follow a slow owner.
- **Poisoning** or **robust-owner-death reporting** warns that a previous owner may have left protected state inconsistent; mechanisms differ.

### Central model, mechanism, or theorem

Let owner state (Owner(L)) be None or one participant. A successful non-reentrant acquisition requires None and sets Owner to the caller. Valid release requires caller ownership and sets None. The inductive exclusion invariant is:

(Owner(L)=None) or (there exists exactly one t such that Owner(L)=t).

This proves only the primitive's ownership safety. Component correctness additionally proves that every dependent access uses (L), the protected invariant holds whenever ownership transfers, release-to-acquire ordering publishes it, failure repairs it, and progress assumptions are adequate.

### Critical invariants

Mutex identity and lifetime are stable. Only the successful owner enters and only an authorized owner releases. Every acquisition result is checked. The guard cannot outlive the protected object. The state invariant holds before release, wait, callback, or failure escape. All dependent accesses use the same authority. Nested locks follow one order. Blocking work and external calls do not occur under the mutex without justification. Recovery validates state after poison or owner death. Destruction happens only after no owner or waiter can reference the mutex.

### Common failures

Teams use different locks for the same data; copy or replace a lock accidentally; unlock from another thread; forget an early-return release; assume try-lock failure synchronized memory; use recursive locking to hide broken boundaries; hold a mutex across I/O, callbacks, join, or await; infer FIFO fairness; spin while the owner cannot run; ignore poison or `EOWNERDEAD`; destroy a mutex with possible waiters; measure average acquisition but not tail hold time; or claim that race-free access proves the sequential state transition correct.

### Compact example

Two threads each execute lock, update, unlock. Their source events admit several textual interleavings, but a real acquisition cannot complete while the other owns the mutex. The only completed ownership histories serialize A before B or B before A. That exclusion makes the update region indivisible to compliant participants; it does not prove the update preserves the application's invariant.

### Connections

[Critical Sections and Shared-State Invariants](008-critical-sections-and-shared-state-invariants.md) provides the predicate proof; [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md) provides lock ordering and progress; [Creating and Joining Threads](011-creating-and-joining-threads.md) provides lifetime and shutdown. The [program roadmap](../ROADMAP.md) next develops predicate waiting, semaphores, read-write locks, barriers, queues, lock-order prevention, and pools.

## Governing Question

How should engineers select, use, validate, recover, and measure a mutex so that exclusive ownership and visibility are correct without introducing hidden deadlock, starvation, latency, or lifetime defects?

A mutex is small in API surface and large in semantic consequence. Correct use requires reasoning about state authority, the memory model, every exit path, wait dependencies, scheduling, failure, and object lifetime.

## Why This Matters

Mutexes remain a foundational bridge between sequential reasoning and shared-memory concurrency. While one owner holds the mutex, it can update several concrete fields as one abstract transition. Release publishes the restored representation to a later acquirer under the primitive's specification. This is often the simplest durable solution for tightly coupled state.

The same simplicity invites overreach. A mutex cannot protect writers that do not use it, a database modified by another process, or an escaped mutable pointer. It cannot turn an incorrect sequential operation into a correct one. It does not guarantee fairness, deadlines, or deadlock freedom. Its performance depends less on the uncontended instruction than on hold-time distributions, arrival patterns, scheduling, cache movement, and waiter policy.

Primitive semantics vary. POSIX.1-2024 distinguishes normal, error-checking, recursive, default, robust, process-shared, and priority-protocol attributes. Java SE 26 monitors are reentrant, and `java.util.concurrent.locks` supports broader lock disciplines. Rust 1.98 mutex guards tie data access to scoped ownership and its poisoning mechanism is advisory. Code must follow the actual selected contract.

Failure behavior is particularly important. A panic, exception, cancellation, process death, or forced termination can interrupt a critical section. Some environments release automatically during stack unwinding; others cannot survive abrupt owner death safely. Poison and robust mutex reports are evidence that state needs recovery, not automatic recovery.

## Prerequisites and Retrieval

Retrieve:

- race conditions, atomicity, and linearization from [Race Conditions and Atomicity Violations](005-race-conditions-and-atomicity-violations.md);
- deadlock, lock order, starvation, priority inversion, and cancellation from [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md);
- abstraction functions, lock invariants, open calls, and exception guarantees from [Critical Sections and Shared-State Invariants](008-critical-sections-and-shared-state-invariants.md);
- thread lifecycle and join dependencies from [Creating and Joining Threads](011-creating-and-joining-threads.md);
- happens-before, acquire/release intuition, state machines, and proof by induction; and
- scheduler states, cache coherence, atomic read-modify-write, and resource lifetime.

Retrieval prompt: write owner states None, A, and B for one non-reentrant mutex. List legal transitions. Then attach an inventory invariant to the mutex and explain why the owner-state proof and inventory proof are different.

## Learning Objectives

After completing this module, a learner can:

1. specify mutex ownership as a state machine and prove exclusive-owner safety;
2. distinguish exclusion, memory synchronization, invariant preservation, fairness, and progress;
3. use scoped guards and structured cleanup across every return and failure path;
4. compare normal, error-checking, recursive, robust, fair, and process-shared mutex contracts;
5. choose among blocking, try, timed, spin, park, and adaptive acquisition based on evidence;
6. diagnose contention, convoying, starvation, priority inversion, false sharing, and excessive scope;
7. recover or fail safely after poison and owner-death notifications;
8. test ownership and instrument hold/wait distributions without claiming universal correctness; and
9. identify safety-critical locking decisions requiring named authorized review.

## Core Exposition

### Specify the ownership state machine

For a non-reentrant mutex, start unowned. A successful acquisition by A changes None to A. While A owns, B's blocking lock cannot complete; it waits. A valid unlock changes A to None, after which one contender may acquire. An unlock by B is invalid. Relocking by A may deadlock, fail, or have undefined behavior depending on mutex type.

The exclusion proof is inductive. Initialization has no owner. The only transition that adds an owner requires no current owner and adds exactly one. Release removes the unique owner. Therefore every reachable legal state has at most one owner.

Implementation bugs can invalidate the state machine: copied mutex words, use after destruction, uninitialized storage, unsynchronized custom flags, or unsupported process sharing. Treat mutex objects as opaque and noncopyable unless their API explicitly says otherwise.

Ownership differs from permits. A counting semaphore can allow multiple entrants and may permit release by a different participant. A mutex associates exclusion with one owner and often detects or forbids non-owner release. A condition variable represents waiting for a predicate and must be paired with a mutex protocol; it is not a replacement.

### Acquisition results and publication

Every acquisition variant has a result:

- blocking lock succeeds, fails, or can be interrupted as specified;
- try-lock succeeds immediately or reports unavailable, poison, or another error;
- timed lock either acquires or reaches a time outcome; and
- robust acquisition may return an owner-death condition while granting ownership.

Enter only after confirmed ownership. A failed try does not generally establish the release/acquire visibility of a successful acquisition. A timeout does not mean the previous owner is dead or that protected state can be read.

Mutexes also synchronize memory. POSIX.1-2024 specifies memory synchronization for successful acquire and release operations. Java's monitor unlock happens-before subsequent lock of the same monitor, and higher-level `Lock` release/acquire methods define corresponding consistency effects. These edges make prior writes visible to a later owner.

Visibility still depends on participation. An unlocked reader has no guarantee merely because writers use a mutex. A different lock does not establish the same protected order. A volatile version flag or optimistic read needs its own complete memory-order and validation proof.

### Guards and structured release

Prefer block-structured synchronization, RAII guards, `defer`, or `finally` so every normal and exceptional exit releases exactly once. Keep the guard local and prevent it from escaping the protected object's lifetime. In Rust, a mutex guard mediates access to the contained value and unlocks on drop; explicit early drop can shorten scope but must follow invariant restoration.

Manual lock/unlock pairs fail under new return paths, exceptions, cancellation, or maintenance edits. Static analysis helps but cannot decide whether the invariant was restored. Code review should see acquisition adjacent to the construct that guarantees release.

Do not release before all fields are valid merely to reduce hold time. Move private computation before acquisition, revalidate shared premises inside, commit a compact nonthrowing transition, capture an immutable result, restore the invariant, release, then perform slow external effects.

### Mutex types are semantic choices

A **normal non-reentrant mutex** has low overhead and makes recursive acquisition an error, deadlock, or undefined case per API. It exposes accidental recursion.

An **error-checking mutex** reports some misuse such as self-relock or invalid unlock. It is useful for diagnosis but does not prove correct lock scope, ordering, or state transitions.

A **recursive/reentrant mutex** maintains an acquisition count for the owner. Only the final matching release transfers ownership. It supports deliberately recursive abstractions but can hide unclear ownership and expose broken invariants to callbacks. POSIX guidance warns that condition waits may not fully release a recursively acquired mutex when depth exceeds one.

A **robust mutex** can notify a future acquirer that an owner died. POSIX `EOWNERDEAD` grants the mutex while requiring the new owner to make state consistent. If it cannot, mark state unrecoverable according to the API. Robustness is not a transaction log.

Rust poisoning reports that a thread panicked while holding certain mutexes, but current documentation calls poisoning advisory and exposes access to the guard through the error. Recovery must validate the protected representation. An unpoisoned state is not proof that no failure interrupted a logical operation.

### Hold scope and open calls

Hold the mutex across the complete in-memory transition and no longer. Avoid:

- blocking I/O or unbounded allocation;
- callbacks or plugin code;
- joining threads or awaiting tasks;
- sending to a bounded queue that can block;
- acquiring lower-ranked locks; and
- logging paths that may reenter the component.

Open calls capture a safe immutable request or reservation under lock, release, call external code, then optionally reacquire and validate a version before committing. If external work must be atomic with state, use a pending state, transaction authority, outbox, or redesign; simply holding a process mutex across the network does not make the remote effect atomic.

Short code is not necessarily short time. Page faults, cache misses, scheduler preemption, memory allocation, runtime safepoints, and priority inversion can extend a small region. Measure duration distributions.

### Contention paths: spin, park, and adaptive behavior

An uncontended mutex may acquire through one atomic state transition. Under contention, implementations may queue waiters and park them, spin briefly before parking, or use adaptive policies. Application code should not rely on undocumented internals.

Spinning can win when hold times are shorter than park/wake cost and the owner is running on another processor. It wastes CPU when the owner is descheduled, the machine is oversubscribed, the critical section blocks, or contention is sustained. On one runnable processor, a spinner can delay the owner.

Parking frees the processor for other work but adds scheduler and wake latency. A queue lock can reduce cache-line contention and offer ordered handoff, while centralized test-and-set can be compact under low contention. NUMA topology changes cache-transfer cost.

Do not implement a custom mutex from a casual atomic loop. Correctness includes memory ordering, lost wakeup avoidance, cancellation, queue integrity, priority, destruction, and platform integration. Use established primitives unless implementing synchronization is the explicit verified goal.

### Fairness, barging, and convoys

Mutual exclusion says at most one owner; it says nothing about who acquires next. An unfair mutex may barge for throughput and cache locality. A fair or FIFO policy can bound bypass under assumptions but may create handoff latency and convoys.

Fairness claims require scheduler progress, owner release, and a stable waiter definition. Java's fair `ReentrantLock` policies have API-specific qualifications, and an untimed try-lock can differ. Never infer fairness from a queue-shaped implementation detail.

Convoying occurs when many threads serialize behind a delayed owner, then wake or hand off one by one. Diagnose with wait and hold histograms, owner scheduling, queue length, and critical-section attribution. Reducing work inside, partitioning ownership, or changing data structure may help; adding threads often worsens it.

Starvation can occur through barging, priority policy, reader preference elsewhere, or a descheduled owner. Test adversarial loads and document whether bounded waiting is a contract.

### Priority inversion and real-time protocols

A high-priority thread can block on a mutex owned by a lower-priority thread while medium-priority work preempts the owner. Priority inheritance temporarily raises the owner's effective priority; priority ceiling constrains access and blocking under a task model.

These protocols require platform and mutex support and complete analysis of all relevant locks. They add overhead and do not fix arbitrary deadlock or an unbounded critical section. Real-time correctness needs worst-case blocking and response-time analysis, not average mutex latency.

### Try-lock and timed acquisition

Try-lock supports optional work, deadlock-avoiding multi-lock protocols, or bounded-latency fallback. Failure is a control result, not an exceptional surprise. Immediate retry loops can livelock or consume CPU. Change asymmetry through ordering, queued admission, useful alternative work, or justified backoff.

Timed acquisition bounds caller waiting, not owner lifetime or state validity. Use a monotonic clock where supported and define whether timeout includes scheduling delay. On timeout, release any other resources, preserve invariant, and record an explicit outcome. Never access protected state “for diagnostics” after failure.

### Multiple mutexes and composition

One invariant may require several partition locks. Establish a strict total order, resolve dynamic lock identities before acquisition, and release safely. All participants must use the same order. Try-lock-and-rollback can avoid permanent circular wait but may livelock.

Acquire-many helpers can impose ordering and exception safety. Even with deadlock prevention, prove the cross-partition transition and handle partial preparation. Coarse locking may be better when multi-partition operations dominate.

Avoid holding a private lock while entering foreign code that may acquire another subsystem's lock in an unknown order. Document lock hierarchy at boundaries, not merely inside one class.

### Failure recovery, lifetime, and destruction

Stack unwinding may release a scoped mutex, but protected data can remain inconsistent. Design transitions so throwing operations occur before mutation, roll back, or enter a recoverable state. Poison and owner-death reports initiate this review.

Mutex lifetime must exceed every owner, waiter, and potential accessor. POSIX warns that destroying a locked mutex, a mutex with a thread attempting to lock, or one used in a condition wait is invalid. Shutdown first stops admission, wakes/cancels waiters under protocol, joins users, proves no references remain, and then destroys.

Do not place a mutex in memory that is moved, copied, unmapped, or reused while referenced. Process-shared mutexes require the specified attributes and compatible shared storage; an ordinary process-private mutex cannot coordinate independent processes by coincidence.

### Observe contention without perturbing correctness

Collect:

- acquisition count and success/failure by mode;
- wait-time distribution and maximum;
- hold-time distribution and owner call site;
- queue length or contention events if supported;
- timeout, interruption, poison, and owner-death counts;
- recursive depth where relevant;
- priority and scheduling delays; and
- protected operation outcomes and invariant failures.

Sampling and tracing can perturb timing, so record tooling and rates. Avoid logging under the hot mutex. Correlate by logical resource identity rather than leaking sensitive data or relying on recycled thread IDs.

## Definitions and Notation

Let mutex (L) have owner (Owner_L(s) in T union {None}) and, for a recursive mutex, depth (d_L(s) >= 0). Exclusive-owner invariant is (Owner=None iff d=0) and otherwise exactly one owner with positive depth.

Successful non-reentrant `lock(t)` transitions None to (t,1). Valid `unlock(t)` transitions (t,1) to None. Recursive lock by owner increments depth and release decrements it. Other transitions follow the selected specification.

Let protected invariant (I_L) hold whenever (L) is unowned and at every transfer. Memory relation (release_L happens-before acquire_L) is defined by the language/API, not by the abstract owner state alone.

Contention measures include wait time (W_i), hold time (H_i), queue population (Q(t)), and acquisition outcome. Fairness can be expressed as bounded bypass (B) only with explicit eligibility and scheduler assumptions.

## Mechanisms, Invariants, or Proof Structure

Use this workflow:

1. **Name the predicate and participants.** Confirm one mutex is the right authority.
2. **Select exact semantics.** Reentrancy, robustness, sharing, fairness, interruption, and timing.
3. **Prove owner-state safety.** Acquisition and release preserve one owner.
4. **Prove state preservation.** Every protected operation restores the invariant before transfer.
5. **Prove visibility.** Cite successful release/acquire rules and cover every accessor.
6. **Structure cleanup.** Guard all returns, failures, cancellation, and owner death.
7. **Analyze waits.** Lock order, callbacks, I/O, join, queues, priority, and scheduler.
8. **Validate lifetime.** No destruction, move, reuse, or unmap while referenced.
9. **Measure contention.** Wait and hold distributions, queueing, timeouts, and outcomes.
10. **Test adversarially.** Forced overlap, failure while held, starvation pressure, shutdown, and recovery.

Maintain these invariants:

- at most one exclusive owner exists;
- only successful ownership permits protected access;
- only authorized ownership releases;
- every dependent participant uses the same stable mutex;
- protected state is valid at ownership transfer;
- release/acquire supplies specified visibility;
- nested acquisitions follow one order;
- recovery validates state after abnormal owner exit;
- no owner or waiter exists at destruction; and
- measurement never substitutes for the correctness proof.

## Alternatives and Trade-Offs

**Coarse mutexes** simplify multi-field invariants and snapshots but serialize unrelated work. **Fine-grained mutexes** improve concurrency only when predicates partition cleanly and cross-lock operations follow one order.

**Unfair/barging locks** can improve throughput and cache reuse. **Fair locks** can bound bypass under assumptions but add queue and handoff cost and may convoy.

**Blocking acquisition** conserves CPU during long waits. **Spinning** avoids park/wake latency for very short holds on available processors. **Adaptive locks** depend on runtime heuristics and workload stability.

**Recursive mutexes** support intentional recursion while hiding some boundary defects. **Non-reentrant mutexes** expose accidental reentry. **Error-checking mutexes** improve diagnostics at extra cost.

**Try/timed lock** supports fallback or bounded wait, but complicates control flow and cleanup. **Queued blocking** is clearer when the operation must eventually acquire.

**Ownership/message passing** removes caller-side shared mutation but adds queues and cross-owner protocols. **Atomics** can avoid blocking for narrow invariants but require memory-order and progress proofs.

## Failure Modes and Misconceptions

- **“The mutex makes the code correct.”** It proves exclusion only for participating paths.
- **“Lock success cannot fail.”** Robustness, interruption, timing, and API errors require checks.
- **“Try-lock failure is an acquire fence.”** Only documented successful synchronization supports visibility.
- **“Recursive is safer.”** It can expose broken invariants and requires balanced depth.
- **“Fair means deadline-safe.”** Scheduler behavior and hold time still matter.
- **“Short source code means short hold.”** Preemption, faults, allocation, and callbacks can extend it.
- **“Spin is faster.”** It can waste the processor needed by the owner.
- **“Timeout breaks deadlock.”** It bounds one wait and needs cleanup; it does not repair a cycle.
- **“Poison restores state.”** It reports risk; recovery must validate or reject state.
- **“Robust means crash-proof.”** External effects and interrupted representation updates remain.
- **“Unlocked metrics are harmless.”** They can race or expose impossible state.
- **“An unlocked mutex can be destroyed.”** Waiters and future references must also be absent.

## Worked Examples

### Example 1

**Question:** Two modules guard the same map with different private mutexes.

**Reasoning:** Each mutex excludes only its own callers; cross-module accesses overlap.

**Conclusion:** One stable authority or a proved compatible protocol must cover the map.

### Example 2

**Question:** A non-owner releases a mutex to “help” a blocked owner.

**Reasoning:** Mutex release is ownership-based and may fail or be undefined.

**Conclusion:** Only the authorized owner releases; use a semaphore or message if cross-participant signaling is intended.

### Example 3

**Question:** A recursive acquisition depth is two and the owner unlocks once.

**Reasoning:** Ownership remains at depth one.

**Conclusion:** Other threads still cannot acquire; balanced release is part of the contract.

### Example 4

**Question:** A failed try-lock path reads protected fields for logging.

**Reasoning:** It has neither ownership nor the successful acquire visibility edge.

**Conclusion:** Log safe external metadata or acquire through a valid path.

### Example 5

**Question:** A panic unwinds through a scoped Rust mutex guard.

**Reasoning:** The guard releases, but the protected representation may be partially updated and poisoning is advisory.

**Conclusion:** Inspect the poison result and validate, repair, or reject state.

### Example 6

**Question:** A POSIX robust lock returns `EOWNERDEAD`.

**Reasoning:** The caller owns the mutex but inherited possibly inconsistent state.

**Conclusion:** Recover and mark consistent, or declare it unrecoverable before normal use.

### Example 7

**Question:** A high-priority task waits behind a preempted low-priority owner.

**Reasoning:** This is priority inversion, potentially extended by medium-priority execution.

**Conclusion:** Shorten the section and apply a supported inheritance/ceiling protocol under real-time analysis.

### Example 8

**Question:** Which completed two-thread ownership histories are legal?

<!-- bijux-verify: {"id":"mutex-exclusive-owner-histories","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidate_histories=6\nserialized_histories=2\nrejected_overlaps=4\nmaximum_owners=1\n","stderr":""}} -->
```python
steps = {"A": ["lock", "unlock"], "B": ["lock", "unlock"]}
histories = []

def visit(prefix, positions):
    if all(positions[name] == 2 for name in steps):
        histories.append(prefix)
        return
    for name in steps:
        index = positions[name]
        if index < 2:
            next_positions = dict(positions)
            next_positions[name] += 1
            visit(prefix + [(name, steps[name][index])], next_positions)

visit([], {"A": 0, "B": 0})
serialized = 0
maximum_owners = 0

for history in histories:
    owner = None
    valid = True
    for name, action in history:
        if action == "lock":
            if owner is not None:
                valid = False
                break
            owner = name
            maximum_owners = max(maximum_owners, 1)
        elif owner != name:
            valid = False
            break
        else:
            owner = None
    if valid:
        serialized += 1

print(f"candidate_histories={len(histories)}")
print(f"serialized_histories={serialized}")
print(f"rejected_overlaps={len(histories) - serialized}")
print(f"maximum_owners={maximum_owners}")
```

**Conclusion:** The model admits A-then-B and B-then-A and rejects four attempted overlapping completion orders. It does not implement blocking, memory ordering, fairness, recovery, or a production mutex.

### Example 9

**Question:** A shutdown destroys an unlocked mutex while a waiter is about to acquire.

**Reasoning:** Absence of a current owner does not prove absence of references or waiters.

**Conclusion:** Stop admission, wake/cancel, join users, prove quiescence, then destroy.

### Example 10

**Question:** Can mutex tests approve access to a nuclear reactor protection state?

**Reasoning:** Hardware independence, deadlines, hazard analysis, fail-safe behavior, and licensing exceed exclusion evidence.

**Conclusion:** No. Named authorized nuclear safety, controls, hardware, verification, cybersecurity, and regulatory reviewers must approve the real design. No external review is claimed.

## Cross-Program Connections

- **Programming languages:** guards, exceptions, ownership types, and memory models define safe use.
- **Operating systems:** parking, wakeups, scheduling, priority, process sharing, and owner death implement behavior.
- **Algorithms:** queue locks, backoff, partitioning, and nonblocking structures offer alternative scalability.
- **Real-time systems:** priority inheritance, ceilings, and worst-case blocking connect locks to deadlines.
- **Software architecture:** encapsulation, open calls, lock hierarchy, and observability make protocols enforceable.
- **Formal methods:** owner-state induction, invariants, happens-before, and wait-for graphs separate proof obligations.

## References

1. Edsger W. Dijkstra, “Solution of a Problem in Concurrent Programming Control,” *Communications of the ACM* 8(9), 1965, [doi:10.1145/365559.365617](https://doi.org/10.1145/365559.365617).
2. John M. Mellor-Crummey and Michael L. Scott, “Algorithms for Scalable Synchronization on Shared-Memory Multiprocessors,” *ACM TOCS* 9(1), 1991, [doi:10.1145/103727.103729](https://doi.org/10.1145/103727.103729).
3. Thomas E. Anderson, “The Performance of Spin Lock Alternatives for Shared-Memory Multiprocessors,” *IEEE TPDS* 1(1), 1990, [doi:10.1109/71.80120](https://doi.org/10.1109/71.80120).
4. Lui Sha, Ragunathan Rajkumar, and John P. Lehoczky, “Priority Inheritance Protocols,” *IEEE Transactions on Computers* 39(9), 1990, [doi:10.1109/12.57058](https://doi.org/10.1109/12.57058).
5. IEEE and The Open Group, *POSIX.1-2024*, “pthread_mutex_lock,” [official specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_mutex_lock.html) (retrieved 2026-08-29).
6. IEEE and The Open Group, *POSIX.1-2024*, “pthread_mutex_destroy,” [official specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_mutex_destroy.html) (retrieved 2026-08-29).
7. Oracle, “Package `java.util.concurrent.locks`,” Java SE 26 API, [official API](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/locks/package-summary.html) (retrieved 2026-08-29).
8. Rust Project, “`Mutex`,” Rust 1.98 standard library, [official API](https://doc.rust-lang.org/std/sync/poison/struct.Mutex.html) (retrieved 2026-08-29).
9. Maurice Herlihy et al., *The Art of Multiprocessor Programming*, second edition, Morgan Kaufmann, 2020.
10. David R. Butenhof, *Programming with POSIX Threads*, Addison-Wesley, 1997.

## Exercises

### Exercise 1

Specify owner-state transitions for normal and recursive mutexes, including invalid release and balanced depth.

### Exercise 2

A cache lock covers lookup, eviction, callback notification, and disk write. Redesign scope while preserving its invariant.

### Exercise 3

Compare spinning and parking for 200-nanosecond holds on dedicated cores versus 20-millisecond holds on an oversubscribed machine.

### Exercise 4

Design recovery for an owner-death or poison report protecting inventory and an external audit effect.

### Exercise 5

A railway interlocking implementation uses fair mutexes and passes stress tests. State what remains for named authorized review.

## Answers to the Exercises

### Answer 1

Normal: None may transition to A or B on successful lock; only the owner transitions back to None. Acquisition by another waits or fails, and self-relock follows the selected API's error/deadlock behavior. Recursive: None becomes (A,1); A may increment depth; only A decrements; ownership becomes None only at zero. B cannot acquire while depth is positive. Invalid release never grants ownership. Both prove at most one owner, while only recursive semantics permit positive depth above one.

### Answer 2

Under lock, validate lookup state, choose eviction, reserve a pending transition, update map/LRU/budget consistently, capture immutable notification and disk intent, then restore and release. Invoke callbacks and durable I/O outside. Reacquire to conditionally finalize against the reservation/version or use an outbox for the external effect. If disk failure changes the abstract contract, model Failed/Pending explicitly. Never call unknown code while the cache invariant is broken.

### Answer 3

For a 200-nanosecond region on dedicated processors with the owner running, a short runtime-supported spin may avoid park/wake cost. Measure cache transfer and contention. For 20 milliseconds under oversubscription, spinning wastes CPU, can delay the descheduled owner, and raises energy and tails; parking is preferable. Adaptive behavior needs evidence about hold distributions and runnable capacity. Application-level busy loops still need correct atomic ordering and should not replace established mutexes.

### Answer 4

On abnormal acquisition, treat inventory as suspect while ownership is held. Validate conservation, reservation uniqueness, journal/intent state, and interrupted transition markers. Roll forward or back through a documented idempotent procedure. Reconcile the external audit effect by durable identity rather than assuming it rolled back. Mark state consistent only after proof; otherwise make it unavailable and escalate. Preserve diagnostics and test failure at every mutation boundary. Poison/robust status is a signal, not a repair.

### Answer 5

Fair acquisition and stress evidence do not establish worst-case blocking, lock hierarchy completeness, scheduler assumptions, hardware faults, fail-safe route state, timing, independence, hazard controls, or certification. Named authorized railway signaling, real-time, hardware, functional-safety, verification, cybersecurity, human-factors, and regulatory reviewers must approve those claims and deployment. This chapter claims no external review.
