---
module_id: OS-023
program: Operating Systems
level: 1
module_number: 23
title: Mutexes, Semaphores, and Condition Variables
status: complete
last_verified: 2026-09-04
---

# Mutexes, Semaphores, and Condition Variables

## One-Page Review

### Governing question

How should systems choose and compose sleepable synchronization primitives so that ownership, capacity, predicates, wakeups, cancellation, recovery, and lifetime remain correct under every permitted schedule?

### Essential definitions

- A **mutex** grants exclusive ownership to one thread or task, which normally must unlock it after restoring a protected invariant.
- A **semaphore** stores a nonnegative count of available units; wait decrements when a unit is available and post increments, without mutex-style owner identity.
- A **condition variable** lets a thread wait for a predicate protected by an associated mutex; the notification is not the predicate.
- A **predicate** is a durable Boolean fact over shared state, such as `count > 0 || closed`.
- A **spurious wakeup** is a wait return without the desired predicate becoming true.
- **broadcast** makes all relevant waiters compete to recheck; **signal** or wake-one selects at least a bounded subset under API semantics.
- A **robust mutex** reports that its prior owner died while holding it so a successor can repair or reject protected state.
- A **completion** represents occurrence of a specific event and may retain completion state; it differs from a general resource count or arbitrary predicate.

### Central model, mechanism, or theorem

Choose by represented state. A mutex protects invariant `I(S)` and has owner `O`. A semaphore represents integer capacity `0 <= C <= C_max`. A condition variable has no independent truth; waiter and producer synchronize around predicate `P(S)`:

`lock(M); while not P(S): cond_wait(CV,M); consume_or_act(); unlock(M)`.

The wait operation atomically releases `M` and blocks relative to the condition protocol, then reacquires `M` before returning. Producers change `S` under `M`, make `P` true, and notify according to cardinality. Timeouts, cancellation, owner death, process sharing, and destruction add outcomes and lifetime obligations.

### Critical invariants

- Each mutex protects a named invariant and has at most one valid owner under its type and state.
- Semaphore count equals available unclaimed units under a protocol that prevents overflow, duplication, and lost ownership.
- Every condition wait evaluates its predicate while holding the same mutex used by predicate writers.
- Waiters loop after notification, timeout boundary, interruption, cancellation cleanup, and competition.
- Signal versus broadcast corresponds to how many waiters may make progress after the state change.
- Robust recovery either restores the invariant and marks state consistent or makes the object unusable according to the API.
- No primitive or protected object is destroyed while a waiter, owner, callback, or process can still reference it.

### Common failures

Common mistakes are unlocking a mutex from a non-owner, using recursive mutexes to hide broken structure, using a binary semaphore where ownership matters, reading a semaphore count as a reservation, waiting on a condition with `if`, signaling without publishing the predicate, using different mutexes for one condition, waking one when closure affects all waiters, ignoring cancellation cleanup, treating owner death as automatic recovery, selecting a wall-clock timeout unintentionally, and destroying synchronization while waiters remain.

### Compact example

A bounded queue uses one mutex protecting buffer, head, tail, count, and closed. Consumers loop while `count == 0 && !closed`, waiting on `not_empty`. Producers loop while `count == capacity && !closed`, waiting on `not_full`. Insert wakes one consumer; removal wakes one producer; close broadcasts both conditions. Cancellation cleanup preserves mutex and item ownership. Destruction closes admission, joins users, verifies no waiters or items remain, then destroys conditions and mutex.

### Connections

[OS-015](015-process-states-and-wait-queues.md) explains predicate waiting, [OS-021](021-critical-sections-in-the-kernel.md) defines invariant and lifetime proof, and [OS-022](022-spinlocks-and-interrupt-context.md) explains why sleepable primitives are invalid in hard-interrupt context. [OS-024](../ROADMAP.md) develops atomics beneath fast paths.

## Governing Question

Mutexes, semaphores, and condition variables all cause waiting, but they encode different domain facts. A mutex says one owner may open an invariant. A semaphore says a countable unit can be claimed. A condition variable says some predicate may have changed and must be checked under a mutex. Substituting one because its API “blocks and wakes” usually loses meaning.

The difficult behavior occurs outside the happy path. A waiter times out as a producer signals. A cancellation arrives after resource acquisition. An owner dies halfway through updating durable shared state. A process unmaps shared synchronization. Shutdown awakens many waiters while callbacks still hold references.

The governing question is how to select a primitive whose stored state matches the domain, then specify all outcomes, ownership transfers, memory ordering, and teardown.

## Why This Matters

Sleepable synchronization avoids wasting CPU during long waits and allows schedulers to manage contention. These primitives underpin queues, worker pools, connection limits, process-shared state, device completion, and user runtimes.

Misuse produces hangs, lost capacity, duplicate ownership, priority inversion, and corrupted recovery. A semaphore leak can permanently shrink capacity. A missed condition predicate can sleep forever. An inconsistent robust object can make later transactions silently wrong.

Performance and real-time behavior depend on contention paths, wake cardinality, lock hold time, priority protocols, and scheduler interaction. Correctness comes first, but a correct thundering herd or unbounded inversion can still violate operational requirements.

## Prerequisites and Retrieval

Recall wait predicates and lost wakeups from [OS-015](015-process-states-and-wait-queues.md), critical-section invariants from [OS-021](021-critical-sections-in-the-kernel.md), and hard-interrupt restrictions from [OS-022](022-spinlocks-and-interrupt-context.md). Understand ownership, counts, clocks, cancellation, and process lifetime.

Retrieve these distinctions:

- exclusive ownership, countable availability, predicate change, and one-time completion are different state models;
- a condition notification is not saved truth and does not transfer the mutex directly;
- wait return means reacquire and recheck, not guaranteed success;
- a timeout boundary can race with state becoming available;
- robust notification identifies possible inconsistency but does not repair it;
- priority inheritance bounds selected inversion, not overload or all deadlock;
- object destruction is a lifecycle protocol, not merely a destructor call.

## Learning Objectives

After this module, you should be able to:

1. select mutex, semaphore, condition variable, completion, or atomic fast path by represented state;
2. write predicate loops that handle competition, spurious wakeups, timeout, close, and cancellation;
3. derive semaphore conservation and bounded-queue invariants;
4. explain mutex type, robust owner death, consistency recovery, and process-sharing constraints;
5. analyze priority inheritance, wake cardinality, fairness, and thundering herds;
6. design initialization and teardown that cover partial failure and cross-process lifetime;
7. test adverse schedules without treating one passing run as proof.

## Core Exposition

### Mutex ownership

A mutex associates exclusion with an owner. The owner enters, temporarily opens the protected invariant, restores it, and unlocks. Other threads block or spin through implementation fast paths until ownership is available.

Normal, error-checking, recursive, robust, priority-inheritance, and process-shared attributes change semantics. Code must not depend on undefined behavior for wrong-owner unlock or recursive acquisition. An error-checking mutex helps diagnosis but does not fix ownership design.

### Recursive mutexes

Recursive acquisition counts ownership depth. It can support APIs deliberately callable under an existing owner, but often hides unclear layering and makes the invariant's open/closed boundary ambiguous. Callback reentry can observe half-updated state despite recursion avoiding deadlock.

Prefer a locked internal helper plus an unlocked public wrapper when ownership is structurally known. If recursion is required, document depth, invariant visibility, cancellation, and final-unlock behavior.

### Semaphore conservation

A counting semaphore models available units. If initialized to `N`, successful waits claim units and posts return them. Domain conservation requires `available + claimed = N` unless controlled resizing or failure states are part of the model.

Because post need not be performed by the waiter that decremented, semaphores suit handoff and capacity but do not enforce owner cleanup. Double post creates phantom capacity; missing post leaks capacity. The API's maximum count and overflow behavior matter.

### Binary semaphore versus mutex

A count restricted to zero or one can exclude access, but it lacks mutex owner semantics, robust recovery, and often priority behavior. It may be correct for event handoff where one context posts for another. It is a poor substitute when the invariant has a responsible owner.

Choose by state meaning, not initial numeric value. Reviews should ask who owns recovery, whether non-owner release is required, and whether priority inversion must be controlled.

### Condition predicates

A condition variable coordinates a predicate stored elsewhere. The waiter locks the predicate mutex, checks in a loop, and uses the atomic unlock-and-wait operation. Upon return it owns the mutex again and rechecks.

The producer normally changes predicate state while holding the same mutex. Notifying before state publication or using a different lock recreates lost-wakeup or visibility gaps. Notification placement after mutation may occur before or after unlock according to the proven design and API semantics.

### Why a loop is mandatory

Wait can return spuriously. Multiple waiters may wake for one resource. A signaled waiter can lose the mutex race and find another thread consumed the state. Timeout and cancellation boundaries introduce additional outcomes.

`while` re-establishes the predicate under ownership. It is not a workaround for a bad library; it is the correct abstraction for condition change and competition.

### Signal versus broadcast

Wake one when one newly available unit can let one waiter progress and waiters have equivalent predicates. Broadcast when a transition such as close, generation change, or configuration update can alter every waiter's outcome.

Broadcast can create a thundering herd: all wake, contend for the mutex, and most sleep again. Wake-one can be wrong when different predicates share a condition or when one selected waiter cannot consume the available state. Simpler separate conditions often improve clarity.

### Timeouts and clocks

Timed waits require a clock and deadline convention. Wall-clock adjustment can advance or delay a real-time-clock deadline. Monotonic clocks better model elapsed time when supported and selected through attributes.

At timeout return, the predicate may concurrently have become true. The API defines lock reacquisition and return semantics, while the application defines whether to consume, abandon, retry, or resolve through an atomic winner. Repeated relative timeouts can drift.

### Cancellation and cleanup

Condition waiting is commonly a cancellation point in threading APIs. Cleanup must know whether the mutex is reacquired and which domain resources the thread owns. Cancellation inside an invariant update must be disabled or covered by an installed cleanup protocol.

A claimed semaphore unit, dequeued item, or partially published result needs exactly one terminal owner. Cancellation is a state transition, not permission to leak a token or leave a mutex locked.

### Robust mutex recovery

When a robust mutex reports owner death, the new owner receives exclusive access to potentially inconsistent state. It validates or rolls back a journal, repairs every invariant, and marks the mutex state consistent before unlock. If repair is impossible, it makes the object permanently or explicitly unusable as the API specifies.

Owner death does not restore external side effects, file transactions, device commands, or distributed operations. Recovery design needs idempotence and durable provenance beyond the mutex bit.

### Priority inversion

A high-priority waiter can block on a mutex held by low-priority work while medium tasks preempt the owner. Priority inheritance temporarily propagates urgency to the holder and through nested dependencies. It requires the correct mutex protocol and bounded critical sections.

Inheritance does not solve circular deadlock, CPU overload, interrupt interference, or unbounded owner work. Priority ceilings and admission can address different parts of a real-time proof.

### Futex-backed fast paths

Thread libraries may keep uncontended mutex, semaphore, and condition operations in user space and use futex operations to block or wake under contention. Compare-and-block helps close an expected-value race, but the higher-level object owns the full state machine.

Do not infer pthread semantics from one futex word layout. Library version, robust lists, process sharing, priority inheritance, cancellation, and memory ordering all participate.

### Kernel mutexes and completions

Kernel mutexes are sleepable ownership locks for task context under their documented rules. Kernel completions represent occurrence of an event and can retain a done state. A completion often expresses “initialization finished” more clearly than a semaphore used as a one-shot signal.

Neither is valid in arbitrary interrupt context. Initialization, reinitialization, stack lifetime, and teardown matter: completing an object after its waiter returned and storage expired is a use-after-free.

### Process-shared synchronization

Process-shared primitives live in mappings visible to all participating processes and require matching attributes and supported storage. Mapping lifetime, initialization races, crash recovery, exec, fork, and unmap must be designed.

Destroying or reusing storage while another process may wait is unsafe. An application needs a shared lifecycle protocol and often a durable generation, not merely a reference count stored in one process.

### Initialization and teardown

Initialize state and attributes before publishing the object. On partial failure, destroy only successfully initialized components in reverse ownership order. Do not copy opaque synchronization objects as ordinary bytes unless the API explicitly permits it.

Teardown closes new callers, publishes closed state, broadcasts terminal predicates, joins or drains users, synchronizes callbacks, verifies ownership and waiter counts, destroys primitives, and only then frees or unmaps storage.

### Performance and observability

Measure uncontended and contended acquisition, wait and hold distributions, wake-to-run delay, herd size, retries, timeouts, cancellation, priority donation, and useful throughput. A lower lock time can accompany higher end-to-end latency if work moved elsewhere.

Stress boundary schedules, owner death, signals, clock changes, cancellation, process exit, and shutdown. Preserve workload, topology, policy, library, kernel, clock, tracing, and raw results.

### Security and assurance

Untrusted users can exhaust semaphore capacity, hold mutexes, trigger broadcasts, or corrupt process-shared state. Authority, quotas, timeouts, recovery, and containment must match the threat model.

Safety-relevant synchronization needs bounded blocking, priority analysis, owner-death behavior, shutdown, and named review. Passing tests and robust-mutex recovery are not certification.

## Definitions and Notation

Let shared state be `S`, invariant `I(S)`, mutex `M` with owner `O(M)`, condition variable `CV`, predicate `P(S)`, semaphore capacity `N`, available count `C`, and outstanding claimed units `K`. Without resizing, conservation requires `C + K = N` and `0 <= C <= N`.

Let outcomes be `success`, `timeout`, `interrupted`, `canceled`, `closed`, `owner_dead`, `not_recoverable`, or error as applicable. Let waiter set be `W(CV)` and live-user set `U`. Destruction requires admission closed and `W(CV)` and `U` empty, plus all external callbacks synchronized.

These abstract names do not override the exact POSIX, Linux, library, or kernel API contract.

## Mechanisms, Invariants, or Proof Structure

A reviewable synchronization proof follows eight obligations:

1. Identify whether domain state is ownership, count, predicate, or completion.
2. Define invariant, owner or token transfer, and all access paths.
3. For conditions, pair every predicate read and write with one mutex and require a loop.
4. Enumerate success, competition, spurious wake, timeout, interruption, cancellation, close, and owner death.
5. Prove semaphore conservation and exactly-once item or token ownership.
6. Analyze lock order, priority inversion, clock, process-sharing, and fast-path ordering.
7. Close admission, awaken terminal waiters, drain users and callbacks, then destroy.
8. Test adversarial schedules while preserving evidence scope.

The executable model shows why two awakened consumers must recheck a one-item predicate.

<!-- bijux-verify: {"id":"toy-condition-recheck","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"if-final=-1\nwhile-final=0\nsecond-consumer=waits\n","stderr":""}} -->
```python
count_if = 1
count_if -= 1
count_if -= 1

count_while = 1
count_while -= 1
second = "consumes" if count_while > 0 else "waits"
if second == "consumes":
    count_while -= 1

print(f"if-final={count_if}")
print(f"while-final={count_while}")
print(f"second-consumer={second}")
```

The sequential toy assumes both consumers were awakened and serializes their mutex reacquisition. It does not implement threads, a condition variable, spurious wakeups, memory ordering, or cancellation.

## Alternatives and Trade-Offs

- Mutex ownership makes invariant responsibility explicit but serializes protected work.
- Semaphores model countable capacity and handoff but lack mutex owner recovery.
- Condition variables express arbitrary predicates but require disciplined mutex loops.
- Completions clarify event occurrence but are narrower than general predicates or resource counts.
- Wake-one limits contention; broadcast handles global transitions at herd cost.
- Recursive mutexes permit layered reentry while obscuring invariant boundaries.
- Robust mutexes expose owner death but require application-specific repair.
- Priority inheritance mitigates inversion while adding protocol and scheduler complexity.
- User-space fast paths reduce syscall overhead while expanding implementation state and debugging complexity.

## Failure Modes and Misconceptions

1. **“All blocking primitives are interchangeable.”** They store different domain facts.
2. **“A binary semaphore is a mutex.”** It lacks owner and recovery semantics.
3. **“Semaphore value can be safely inspected for a decision.”** Observation races with claims and posts.
4. **“Signal stores one future wake.”** Condition truth resides in the predicate.
5. **“Wait return means predicate true.”** spurious and competitive wakes require recheck.
6. **“Use `if` around wait.”** a second consumer can invalidate the condition first.
7. **“Signal without the mutex is always faster.”** publication and lost-wakeup protocol must be proved.
8. **“Broadcast is safest.”** it can cause a herd and still needs loops.
9. **“Recursive mutex fixes reentrancy.”** callbacks may observe half-restored invariants.
10. **“Robust means automatically repaired.”** owner death hands recovery to application code.
11. **“Timeout cleanly wins.”** state publication may race at the boundary.
12. **“Cancellation releases everything.”** cleanup owns each mutex, token, and item explicitly.
13. **“Futex semantics equal pthread semantics.”** the library supplies the larger contract.
14. **“Destroy after setting closed.”** waiters and callbacks must actually quiesce.

## Worked Examples

### Example 1

A ledger transfer locks one mutex protecting both account totals and transaction state. The owner restores sum conservation before unlock. A semaphore would not identify the thread responsible for the open invariant.

### Example 2

A pool of four identical devices uses a semaphore initialized to four. Each successful wait owns one device token and every terminal path posts exactly once. Double post would permit five borrowers.

### Example 3

Two consumers wake for one queue item. The first takes it. The second reacquires the mutex, sees `count == 0`, and waits again. An `if` body would underflow or remove nonexistent work.

### Example 4

A queue close changes every consumer's result from wait to terminal exit. Broadcast is appropriate even with zero items; each waiter rechecks `closed && count == 0`.

### Example 5

A timed waiter and producer race. An atomic request-state winner decides whether the item is consumed or returned, while the mutex protects the queue. Merely comparing timestamps after return cannot resolve ownership.

### Example 6

A canceled worker has claimed a semaphore slot but not published a job. Its cleanup returns the slot exactly once. Cancel disabling protects the narrow interval where ownership metadata is inconsistent.

### Example 7

A robust mutex reports owner death during a shared-memory journal update. The successor validates records, rolls back the incomplete entry, restores checksums, marks consistent, and continues. If validation fails, it marks the service unavailable.

### Example 8

High-priority H waits for a mutex held by low-priority L. A priority-inheritance mutex raises L through any nested chain, but a circular lock graph still deadlocks and requires an order redesign.

### Example 9

A kernel driver uses a completion for firmware-ready notification. The completion object lives in device state, not a returning stack frame, and removal synchronizes the callback before freeing it.

### Example 10

Process-shared consumers map a queue. The coordinator closes a generation, broadcasts, waits for process acknowledgments and kernel wait completion, then unmaps. A crashed participant follows a robust recovery policy.

## Cross-Program Connections

[Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) develops mutexes, semaphores, conditions, memory models, and cancellation. [Security Engineering](../../25-security-engineering/ROADMAP.md) frames denial of service and corrupted shared state.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies capacity, timeout, recovery, hazard, and assurance reasoning. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains atomic fast paths and memory ordering.

Within this program, [OS-024](../ROADMAP.md) deepens atomic operations, [OS-025](../ROADMAP.md) develops deadlock, and later IPC modules use these primitives across processes.

## References

- POSIX via Linux man-pages, [pthread_mutex_lock(3p)](https://man7.org/linux/man-pages/man3/pthread_mutex_lock.3p.html), current page checked 2026-09-04. Mutex ownership, types, robust owner death, consistency, errors, and priority protocols.
- POSIX via Linux man-pages, [pthread_mutexattr_settype(3p)](https://man7.org/linux/man-pages/man3/pthread_mutexattr_settype.3p.html), current page checked 2026-09-04. Normal, error-checking, recursive, and default mutex attributes and behavior.
- Linux man-pages project, [pthread_mutexattr_setrobust(3)](https://man7.org/linux/man-pages/man3/pthread_mutexattr_setrobust.3.html), current page checked 2026-09-04. Robust and stalled attributes, owner death, consistency, and Linux history.
- Linux man-pages project, [sem_wait(3)](https://man7.org/linux/man-pages/man3/sem_wait.3.html), current page checked 2026-09-04. Semaphore claim, blocking, try-wait, timed wait, signals, and errors.
- Linux man-pages project, [sem_post(3)](https://man7.org/linux/man-pages/man3/sem_post.3.html), current page checked 2026-09-04. Count increment, waiter wake, overflow, and async-signal safety.
- Linux man-pages project, [sem_overview(7)](https://man7.org/linux/man-pages/man7/sem_overview.7.html), current page checked 2026-09-04. Named and unnamed semaphores, process sharing, persistence, linking, and permissions.
- Linux man-pages project, [pthread_cond_wait(3)](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3.html), current page checked 2026-09-04. Atomic mutex release and wait, reacquisition, timed waits, cancellation, and signal and broadcast.
- POSIX via Linux man-pages, [pthread_condattr_setclock(3p)](https://man7.org/linux/man-pages/man3/pthread_condattr_setclock.3p.html), current page checked 2026-09-04. Condition-variable clock selection, defaults, supported clocks, and errors.
- Linux man-pages project, [futex(2)](https://man7.org/linux/man-pages/man2/futex.2.html), current page checked 2026-09-04. Compare-and-block, wake, priority inheritance, robust synchronization, timeouts, and shared mappings.
- Linux Kernel documentation, [Generic Mutex Subsystem](https://docs.kernel.org/locking/mutex-design.html), current page checked 2026-09-04. Mutex ownership, fast, optimistic-spin and slow paths, implementation, and API rules.
- Linux Kernel documentation, [Completions](https://docs.kernel.org/scheduler/completion.html), current page checked 2026-09-04. Event completion state, initialization, waiting, signaling, reinitialization, and lifetime.
- Linux Kernel documentation, [RT-mutex Implementation Design](https://docs.kernel.org/locking/rt-mutex-design.html), current page checked 2026-09-04. Priority inheritance, owner and waiter state, transitive chains, and locking.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching sleep and wakeup, locks, pipes, process exit, and synchronization invariants.

## Exercises

### Exercise 1

Classify ten synchronization problems as ownership, capacity, predicate, or completion. Select a primitive and state why the alternatives lose domain meaning.

### Exercise 2

Design a bounded multi-producer, multi-consumer queue with close, timeout, cancellation, and restart. Prove buffer and semaphore or condition invariants.

### Exercise 3

Design robust process-shared state recovery for owner death during a journaled update. Cover consistency, unrecoverable state, mapping lifecycle, and repeated crashes.

### Exercise 4

Compare wake-one and broadcast with heterogeneous predicates, priorities, and queue sizes. Design measurements for herd cost, latency, fairness, and throughput.

### Exercise 5

Construct an assurance review for a priority-sensitive synchronization path. Cover inversion, cancellation, owner failure, overload, evidence, and human judgment.

## Answers to the Exercises

### Answer 1

Use a mutex for exclusive update ownership; a semaphore for N interchangeable buffer slots or devices; a condition variable for `queue_nonempty`, `generation_changed`, or `closed`; and a completion for one initialization or teardown milestone. A rendezvous may use a zero-count semaphore when non-owner handoff is intentional. A reference count uses a purpose-built atomic ownership protocol rather than any of these alone.

For every choice, state owner or token transfer, stored state, wake cardinality, timeout, cancellation, process scope, priority behavior, and destruction. Similar wait syntax is not sufficient justification.

### Answer 2

Under one mutex protect buffer, head, tail, count, generation, and closed. With conditions, producers loop on `count==capacity && !closed`; consumers loop on `count==0 && !closed`. Insert and remove update all fields before wake. Close broadcasts. Restart creates a new generation so stale completions cannot affect it.

With semaphores, `empty + count = capacity` and `full = count` must remain consistent, but close and cancellation need extra state and wake strategy. Every successful empty claim either publishes an item or returns the token; every full claim either transfers an item or restores it. Timeout and cancellation use cleanup with explicit ownership. Teardown closes, wakes, joins, drains, verifies invariants, destroys, then frees.

### Answer 3

Store a versioned journal record with operation identity, before or redo data, checksum, and commit marker under a robust process-shared mutex. On owner-dead acquisition, validate the mapping and journal. Roll back an uncommitted operation or replay a committed idempotent operation, restore all invariants, persist as required, then mark mutex state consistent.

If validation or external-effect reconciliation is impossible, mark the generation unrecoverable and rebuild or fail closed. A second crash during recovery repeats the same idempotent procedure. Mapping coordination prevents unmap or reinitialization while any process can wait. Robust mutex state alone does not make storage or external systems transactional.

### Answer 4

Wake-one suits one homogeneous newly available unit; broadcast suits close or a transition affecting all predicates. With heterogeneous predicates on one condition, wake-one may select a waiter that cannot progress. Separate conditions or broadcast with recheck are clearer. Priorities may change selected order but need documented semantics and inversion analysis.

Measure waiters awakened, mutex acquisitions, failed rechecks, wake-to-run and predicate-success latency, context switches, CPU time, completions, fairness, and throughput across queue sizes and priorities. Include spurious returns, cancellation, overload, and tracing-off controls. Retain raw distributions; no one trace proves fairness.

### Answer 5

Define the invariant, owners, predicates, token conservation, lock order, task priorities, critical-section bound, and every cancellation or owner-failure outcome. Use analyzed priority inheritance or ceilings where needed, with admission and bounded nested dependencies. Keep recovery and shutdown capacity outside potentially exhausted resources.

Test contention, inversion chains, timeout boundaries, cancellation points, owner death, repeated recovery crash, broadcast herd, overload, and teardown. Combine static order and lifecycle review, stress, fault injection, tracing, and response-time analysis; observed maxima are not bounds. Named concurrency, runtime or kernel, real-time, platform, security, safety, independent-verification, and acceptance owners review assumptions and residual risk. This chapter claims no certification.
