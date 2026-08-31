---
module_id: SEPAT-077
program: Software Engineering: Patterns
level: 2
module_number: 77
title: Monitor Object
status: complete
last_verified: 2026-08-29
---

# Monitor Object

## One-Page Review

### Governing question

How can concurrent caller threads share one object through synchronized methods and condition predicates while preserving private-state invariants, avoiding missed/spurious wake errors, limiting lock scope, preventing nested lockout/deadlock, and shutting down with no stranded waiters?

### Essential definitions

- A **Monitor Object** encapsulates shared state, a mutual-exclusion mechanism, condition variables, and the only methods permitted to access that state.
- The **monitor lock** admits at most one thread into protected monitor execution at a time under the base pattern.
- A **synchronized method** borrows the caller's thread, acquires the monitor, checks/waits for its precondition, mutates/reads state, restores invariants, signals relevant conditions, and releases on every exit.
- A **monitor invariant** is a predicate over private state that holds whenever no method is executing protected mutation and whenever a thread releases the lock to wait.
- A **condition predicate** is the Boolean state fact a waiter needs, such as `count > 0`, not the notification itself.
- A **condition variable/wait set** lets a thread atomically release the associated monitor lock and suspend; successful resumption reacquires the lock before returning.
- A **spurious wakeup** is return from wait without the desired predicate becoming true.
- **Mesa-style signaling** makes a waiter eligible to compete for the lock; the signaler continues and no state handoff is guaranteed.
- **nested monitor lockout** occurs when a thread waits on one monitor while retaining another lock required by the thread that could satisfy its predicate.
- **linearization point** is the instant inside the protected method at which an operation logically takes effect.

### Central model, mechanism, or theorem

For protected state (S) and invariant (I(S)), every public synchronized operation follows

$$
acquire\rightarrow while\;\neg P(S):wait\rightarrow mutate/read
\rightarrow I(S)\rightarrow signal\rightarrow release.
$$

The safety argument requires (I(S)) on monitor entry, before every condition wait (because wait releases the lock), and on every exit. A waiter resumes with the lock but must recheck (P): wakeups may be spurious, another thread may consume the enabling state first, timeout/interrupt may race, and Mesa notification transfers no entitlement.

Mutual exclusion serializes protected method intervals and gives candidate linearization order. It does not guarantee fairness, absence of deadlock across monitors, nonblocking progress, real-time priority, correct external effects, or safety of references that escape the monitor.

### Critical invariants

- All mutable representation is private and accessed only while holding the correct monitor lock; no mutable alias escapes.
- The monitor invariant holds at construction/publication, every normal/exceptional method exit, and immediately before releasing the lock in a wait.
- Every wait is a predicate loop using the same protected state and associated lock; notification is never remembered as state.
- State that can make a predicate true is mutated and the appropriate condition signaled under the monitor protocol.
- Lock acquisition/release is structured so exceptions, timeout, interruption, cancellation, and early returns cannot leak ownership.
- Methods do not perform unbounded I/O, blocking callbacks, future waits, or foreign code while holding the monitor unless the complete dependency protocol proves safety.
- Cross-monitor acquisition follows a global order or another explicit deadlock-avoidance design; a wait never retains a lock needed by its producer.
- Reentrant calls/callbacks cannot observe or publish partially restored invariants.
- Timed waits use an appropriate monotonic deadline, loop with remaining semantics, and distinguish predicate success from timeout/cancel.
- Shutdown changes a protected closed state, wakes all affected waiters, makes every wait predicate terminal, joins/quiesces callers, then destroys synchronization/state.

### Common failures

Common failures include public fields or leaked collections, locking a replaceable/public object, `if` instead of `while` around wait, treating signal as stored state, mutating predicates outside the lock, signaling the wrong condition, missed notification from split check/wait, broadcast storms, waiting while holding an outer monitor, inconsistent lock order, callbacks under lock, blocking network/database work inside a method, returning without invariant restoration after exception, assuming reentrancy makes callbacks safe, wall-clock timeout drift, interrupt swallowing, priority inversion, unfair starvation, and destroying the monitor while threads can enter or wait.

### Compact example

A capacity-two buffer accepts `a` and `b`. A producer attempting `c` sees `not_full` false and must wait in a loop. A consumer takes `a`, changing state under the lock and signaling `not_full`; after reacquiring and rechecking, the producer adds `c`. Closing sets protected `closed=true` and broadcasts. Consumers drain `b` and `c`; an empty closed buffer returns end-of-stream rather than waiting forever. Count always stays between zero and two.

### Connections

[SEPAT-076](076-active-object.md) executes in a separate scheduler thread; a Monitor Object executes on caller threads. [SEPAT-079](../ROADMAP.md) applies monitors to bounded producer-consumer buffers; [SEPAT-080](../ROADMAP.md) examines condition variables directly. Monitor Object also connects to [Operating Systems](../../22-operating-systems/ROADMAP.md), [Computer Architecture](../../23-computer-architecture/ROADMAP.md), [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md), and [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

When shared object state must be called synchronously by many threads, how should the object make mutual exclusion and conditional scheduling inseparable from its interface so callers cannot bypass the state invariant or race the check-to-wait transition?

Monitor Object is a thread-safe passive-object pattern. Unlike Active Object, it has no separate execution thread or activation queue. A caller enters a synchronized method and lends its own thread to the object. Mutual exclusion protects representation; condition variables let methods cooperate when an operation's precondition is temporarily false. The simplicity is powerful, but any blocking or callback inside the monitor directly blocks callers and can entangle other resources.

## Why This Matters

Bounded queues, connection registries, caches, resource pools, device state, ledgers, session managers, and protocol objects often need small atomic operations plus waits for state changes. A monitor localizes lock and condition logic with the data it protects, making invariants reviewable and reducing callers' ability to acquire the wrong lock.

Incorrect monitor code can remain latent for years. Lost notifications, spurious wake assumptions, leaked aliases, exception paths, rare lock-order cycles, close races and priority inversion surface only under adverse schedules. Production quality requires reasoning about state predicates and lifecycle, not merely marking methods `synchronized`.

## Prerequisites and Retrieval

You should understand threads, mutexes, memory models/safe publication, exceptions/resource cleanup, condition variables, deadlines, cancellation, deadlock, and object invariants. Retrieve these facts:

1. Mutual exclusion protects only code that consistently uses the same lock/protocol.
2. Condition wait atomically releases its associated mutex and blocks, then returns owning that mutex.
3. Wait may return spuriously; signal/broadcast is not proof that a predicate is true.
4. Under Mesa semantics the signaler normally continues, so another thread can change state before the waiter reacquires.
5. Waiting releases the associated monitor lock, not arbitrary outer locks already held.
6. Reentrant locks permit same-thread nested entry but do not eliminate invariant exposure or lock-order deadlock.
7. Timeout, interrupt/cancel, signal and predicate change can race; state decides the outcome under the lock.
8. Destroying a referenced/waited-on synchronization object is invalid or undefined in common platforms.

## Learning Objectives

After completing this module, you should be able to:

- identify monitor interface, private state, lock, synchronized methods, condition variables, predicates and callers;
- write and review invariant-preserving method skeletons for normal, exceptional, timed and cancelled paths;
- explain why wait must occur inside a `while` predicate loop and why notification carries no durable state;
- choose signal versus broadcast and one versus multiple conditions from predicate dependencies;
- assign linearization points and distinguish lock serialization from domain/external-effect correctness;
- detect alias escape, public/wrong locks, callbacks under lock, reentrancy hazards, nested monitor lockout and lock-order cycles;
- design monotonic timed waits, interruption policy, fairness/priority handling and bounded critical sections;
- compare Monitor Object with Active Object, immutable state, read-write locking, atomics and message passing;
- implement close/shutdown so waiters terminate and synchronization outlives all users;
- verify with invariant models, controlled schedules, race/deadlock tools, spurious wake injection, overload and fault tests.

## Core Exposition

### Identify the participants

The Monitor Object exposes methods, owns private representation, owns or has stable exclusive access to a lock, and defines condition variables for distinct state predicates. Client threads call methods synchronously. A method entry acquires; exit releases. A method whose precondition is false waits atomically on the corresponding condition, temporarily letting other clients change state.

The synchronization belongs with the representation. Do not require clients to lock around calls; they may forget, compose in inconsistent order, or lock the wrong instance. A Thread-Safe Interface wrapper can protect a separate implementation, but the public path must be exclusive.

### State the invariant first

Write invariant (I(S)) in domain terms: for a circular buffer, (0\le count\le capacity), indices remain within bounds, occupied slots correspond to count, and closed state forbids new puts. For a resource pool, every resource is exactly available, leased with owner/generation, quarantined, or retired.

Construction establishes the invariant before safe publication. Each method assumes it after acquire, may temporarily break it while no other thread can enter, and restores it before release. A condition wait releases the lock, so restore the invariant before calling wait. Exception cleanup must restore or permanently quarantine the object before unlock.

Do not make invariants depend on mutable external objects that can change without the lock. Snapshot/own necessary values or extend the synchronization boundary deliberately.

### Protect the complete representation

All fields participating in the invariant use the same documented strategy. “Mostly under lock” is a data race. Read-only getters need synchronization/atomic publication too because they observe concurrent writes. Do not return internal arrays, collections, iterators, buffers, or mutable elements that let clients mutate without the monitor.

Return immutable snapshots or leased capabilities whose operations return through the monitor. If an object must use multiple independent locks for performance, it is no longer one simple monitor: partition invariants and define their composition/order explicitly.

Use a private final/stable lock, not a public object, string literal, boxed value, or field that can be replaced. External code locking the same object can cause unplanned contention/deadlock.

### Write waits as predicate loops

Canonical logic is:

1. acquire the lock;
2. while the desired predicate is false and no terminal close/cancel/timeout applies, wait on its condition;
3. after every return, with the lock reacquired, recompute the predicate and terminal states;
4. perform mutation/read, restore invariant, signal predicates newly enabled, then release.

Use `while`, not `if`. Wake may be spurious. Multiple consumers may wake and one consumes the only item. A different signal reason may share a wait set. Timeout/interrupt may coincide with a real state change. Only protected state determines permission.

The predicate includes terminal lifecycle. A consumer may wait for `not_empty OR closed`; if empty and closed, return end-of-stream. Otherwise shutdown broadcast wakes it only to wait forever.

### Avoid lost wakeups

The check and transition into waiting must be atomic relative to predicate-changing methods. Condition wait provides this by releasing the associated lock as it enqueues/suspends under the platform contract. A homegrown sequence “unlock; sleep” can miss a signal between steps.

Change predicate state while holding the lock, then signal under the monitor's specified protocol. Even on APIs permitting notification after unlock, doing so requires proof that lifecycle and waiter bookkeeping cannot miss/reorder the condition. Prefer the conventional coherent state-change-plus-notification pattern.

Notification is a hint that state may have changed, not an event counter. If history matters, store a sequence/count/flag in protected state. A signal before a future waiter is not remembered by a condition variable.

### Choose condition granularity and notification

A bounded buffer naturally has `not_empty` and `not_full`. Separate conditions avoid waking producers when only consumers can proceed. Each condition must have a documented predicate over protected fields and all mutation sites that can make it true.

Signal one when one unit of state enables at most one equivalent waiter and no lifecycle/fairness ambiguity requires more. Broadcast when close/reconfiguration enables different predicates, multiple units may enable many waiters, or specific-notification correctness is difficult. Signal-one can wake an ineligible waiter if multiple predicates share a wait set, leaving an eligible peer asleep.

Broadcast improves robustness but creates herd contention. Correctness first, then measure/partition. Never make liveness depend on an unspecified waiter-selection order.

### Understand Mesa versus Hoare semantics

In common Mesa-style monitors, signaling does not immediately hand the lock to the waiter. The signaler continues until release; new entrants or another awakened thread may acquire first. The original predicate can become false before a waiter runs. Hence the loop.

Hoare-style monitors conceptually transfer control under stronger rules, but do not assume them from generic “monitor” terminology. Use the exact language/runtime specification. Java and POSIX condition usage require predicate rechecking and allow spurious wakeups.

### Bound critical sections

Protected code should compute small state transitions. Do not hold the monitor across network/database/file I/O, user callbacks, logging sinks, future joins, process calls, or sleeps. These inflate contention and can introduce dependency cycles. Copy the minimum immutable work under lock, release, perform external work, then reacquire and apply a generation/version-checked result.

This split changes atomicity. Represent `pending` intent/version before release and reconcile failure. For irreversible effects, stable effect identity and durable protocol may be needed. Do not blindly retry after version mismatch if external work already occurred.

Keep allocation/destruction under lock only if bounded and nonreentrant. Destructors/finalizers/callbacks triggered by releasing references can call unknown code; move disposal outside after detaching state safely.

### Handle exceptions and cancellation

Structured locking (`with`, guard, `synchronized`, `defer/finally`) releases on every exit. But unlocking is not enough: restore invariant. Validate before mutation, stage values, use rollback/transaction or mark object failed/quarantined if partial mutation cannot be repaired.

Interruption/cancellation during condition wait usually returns/throws with the associated lock reacquired under the API contract, enabling cleanup. Decide whether to propagate, translate, retry or restore interrupt status. Do not swallow cancellation and wait forever. If cancellation occurs after the predicate becomes true, define whether state operation or cancellation wins under the lock.

Asynchronous termination while inside arbitrary monitor code is unsafe: the thread may own locks and partial state. Prefer cooperative safe points.

### Implement timed waits correctly

Use a monotonic deadline when supported. On each loop, check predicate first, then calculate remaining time against the same absolute deadline. A spurious wake must not restart a full relative timeout. Wall-clock adjustment must not shorten/extend operational deadlines unexpectedly.

At timeout return, reacquire/hold lock and recheck predicate because signal/state change and expiry can race. Define a linearization policy: if resource is available at the final protected check, operation may succeed; otherwise timeout. Report queue/wait duration separately.

### Prevent nested monitor lockout and deadlock

If thread A holds monitor X, enters Y and waits on Y, wait releases Y but retains X. If thread B needs X to make Y's predicate true, both are stuck. This is nested monitor lockout. Avoid calling a blocking monitor method while holding another monitor.

For nonwaiting cross-object operations, impose global lock order by stable IDs or use try-lock/retry, open calls, immutable snapshots, transactions, or a higher-level owner. Do not call foreign code while holding a monitor because its lock behavior is unknown.

Document the wait-for/resource graph. Reentrancy does not fix cycles between different locks. Timeouts expose symptoms but may leave partial external effects and recurring contention.

### Treat reentrancy carefully

Reentrant monitors permit a thread already owning the lock to call another synchronized method. This avoids self-deadlock for internal method composition, but can obscure lock depth and expose partially broken invariants if callbacks reenter at the wrong point.

Keep public methods as invariant boundaries and use private helpers requiring the lock when composing mid-transition. Do not invoke observers/listeners/overridable methods under lock. A subclass can override synchronized behavior and leak state; prefer final composition/private representation for high-integrity monitors.

Wait releases the monitor's reentrant hold count according to platform semantics but does not release other monitors. Verify exact behavior.

### Reason about fairness and priority

Ordinary mutexes/conditions often do not guarantee FIFO admission or waiter selection. A hot thread can barge; signal-one selection may be unspecified; starvation is possible. If fairness is a requirement, add explicit waiter tickets/queue under the monitor or use a documented fair synchronizer, then measure cost and cancellation holes.

Priority inversion occurs when a low-priority holder blocks a high-priority waiter while medium work runs. Use short critical sections, suitable OS/runtime priority-inheritance/protect protocols where available, partitioning, and real-time analysis. Application thread priorities alone are not proof.

### Establish memory visibility and publication

Correct lock release/acquire provides the memory-order relationship defined by the language/runtime. All accesses must participate. Publishing `this` from a constructor before invariant establishment or reading fields without the lock can defeat safety.

Immutable snapshots need final/freeze/safe-publication rules. Atomics can optimize independent counters but mixing them with locked invariant fields requires a coherent snapshot contract. “Volatile” visibility alone does not make multi-field transitions atomic.

### Close and destroy safely

Under the lock set `closed`, update generation and terminal state, then broadcast all conditions whose wait predicates include closure. New calls reject/return according to API. Existing operations drain, fail or cancel under declared semantics. Waiters wake, recheck and exit.

The owner must ensure no thread can newly enter and all current/waiting users have returned before destroying mutexes, conditions or state. Reference counting alone can cycle with waiters; use an external lifecycle/join protocol. A destructor that merely broadcasts and immediately frees is unsafe.

### Observe and verify

Measure method entry wait/hold duration, waiter counts/oldest age by condition, signals/broadcasts and wake-to-success ratio, spurious/timeout/interrupt/cancel outcomes, contention, fairness, priority, invariant failures, exceptions/quarantine, cross-monitor wait graph, callback/open-call duration, close generation and shutdown residue. Instrumentation must not call blocking/foreign code under the lock.

Model state/predicates first. Test zero/full boundaries, many producers/consumers, spurious and redundant wakeups, signal races, timeout at boundary, cancellation, exception at each mutation, alias attempts, reentrancy/callbacks, opposite lock order, nested wait, priority contention, close with every waiter type, and destruction. Use race/deadlock detectors, controlled schedules, stress/soak and model checking where risk warrants.

### A finite executable model

This deterministic bounded-buffer model records predicate outcomes and closure. It does not execute threads, locks, condition waits, spurious wakeups, memory ordering, timing or real scheduling.

<!-- bijux-verify: {"id":"sepat-077-monitor-buffer","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"put=a status=ok count=1\nput=b status=ok count=2\nput=c status=would_wait predicate=not_full:false\ntake=a signal=not_full count=1\nput=c status=ok count=2\nclose=true broadcast=not_empty,not_full\ntake=b,c count=0\ntake=none status=end_of_stream\ninvariant=count_between_0_and_2:true fifo:true\n","stderr":""}} -->
```python
class MonitorBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        self.closed = False
        self.history = []

    def put(self, item):
        if self.closed:
            return "closed"
        if len(self.items) == self.capacity:
            return "would_wait"
        self.items.append(item)
        self.history.append(("put", item))
        return "ok"

    def take(self):
        if self.items:
            item = self.items.pop(0)
            self.history.append(("take", item))
            return item, "ok"
        if self.closed:
            return None, "end_of_stream"
        return None, "would_wait"

    def close(self):
        self.closed = True


buffer = MonitorBuffer(capacity=2)
print(f"put=a status={buffer.put('a')} count={len(buffer.items)}")
print(f"put=b status={buffer.put('b')} count={len(buffer.items)}")
status = buffer.put("c")
not_full = str(len(buffer.items) < buffer.capacity).lower()
print(f"put=c status={status} predicate=not_full:{not_full}")

item, _ = buffer.take()
print(f"take={item} signal=not_full count={len(buffer.items)}")
print(f"put=c status={buffer.put('c')} count={len(buffer.items)}")
buffer.close()
print("close=true broadcast=not_empty,not_full")

first, _ = buffer.take()
second, _ = buffer.take()
print(f"take={first},{second} count={len(buffer.items)}")
item, status = buffer.take()
print(f"take=none status={status}")

bounded = 0 <= len(buffer.items) <= buffer.capacity
taken = [item for operation, item in buffer.history if operation == "take"]
print(f"invariant=count_between_0_and_2:{str(bounded).lower()} fifo:{str(taken == ['a', 'b', 'c']).lower()}")
```

## Definitions and Notation

Let (S) be private monitor state, (I(S)) its representation invariant, (M) the stable monitor mutex, (C_j) a condition variable, and (P_j(S)) its documented predicate. Let (W_j) be waiters and (g) lifecycle generation.

Operation (op) has precondition (Pre_{op}), protected transition (f_{op}), postcondition (Post_{op}), and linearization point (lin(op)) within its monitor interval. Timed operation uses monotonic deadline (D) and remaining (D-now).

For cross-monitor graph (G=(V,E)), (A\to B) means a thread holding/waiting through monitor A needs monitor B or a B-holder needs A to satisfy a predicate. A reachable cycle is a deadlock risk; a condition wait releases only its associated mutex.

## Mechanisms, Invariants, or Proof Structure

### Mutual-exclusion safety argument

Assume all representation access occurs while owning stable lock M, construction is safely published, no mutable alias escapes, and each method restores (I(S)) before unlock/wait. Mutual exclusion serializes protected transitions, so induction over method intervals preserves (I). Runtime/lock correctness and method transition proofs remain assumptions.

### Condition-wait argument

Assume (P_j) depends only on M-protected state, predicate-changing methods signal under the protocol, and wait atomically releases M and suspends. A waiter loops after every return while owning M. It proceeds only from an observed true predicate/terminal state, regardless of spurious wake, barging, redundant/wrong-purpose notification or timeout race. This is safety, not eventual wake/fairness proof.

### Lost-wakeup exclusion

With predicate check and wait transition under M plus the condition API's atomic release/wait contract, a changer cannot interleave between an unprotected false check and waiter registration. The changer acquires M after release, changes state and signals. The waiter either is registered or later observes true state. This depends on exact API use and lifecycle.

### Deadlock and liveness limits

A single monitor method that never blocks except condition wait avoids internal lock-order cycles, but foreign calls, multiple locks and retained outer locks can create cycles. Mutual exclusion is blocking and not lock-free; scheduler fairness and a thread capable of making each predicate true are additional liveness premises.

### Evidence boundaries

Finite models can check state transitions/invariants and close predicates. Schedule-controlled tests sample races. Thread/race tools find classes of defects, not proofs. Source review establishes language/OS semantics for declared versions. Timing, fairness, security and safety-critical claims need empirical/human evidence.

## Alternatives and Trade-Offs

| Design | Advantage | Cost or limitation | Appropriate use |
| --- | --- | --- | --- |
| Monitor Object | Localized synchronous invariant and condition scheduling | Caller blocks; lock/deadlock/reentrancy risk | Short shared-state operations |
| Active Object | Servant confinement and asynchronous futures | Queue/scheduler/temporal semantics | Stateful async interface |
| Immutable snapshot/COW | Lock-free readers and simple publication | Copy/update cost and stale snapshots | Read-heavy modest state |
| Atomics/lock-free structure | Nonblocking progress potential | Complex memory reclamation/composition | Hot simple operations with expert proof |
| Read-write lock | Concurrent readers | Writer starvation, upgrades and complex invariants | Long read-dominant protected state |
| Actor/message passing | Ownership and failure supervision | Queueing/distribution semantics | Isolated message-driven components |
| Database transaction | Durable multi-client isolation | Latency, transaction anomalies/configuration | Durable shared records |
| Thread confinement | No sharing/lock on owned thread | Handoff and ownership routing | Naturally partitionable state |

Coarse monitors are easier to prove but reduce concurrency. Fine-grained locks increase throughput only when contention warrants their larger state/lock-order proof. Signal-one reduces herd cost but is easier to make liveness-wrong. Fair locks reduce starvation but can reduce throughput and do not solve dependency cycles.

## Failure Modes and Misconceptions

- **“Synchronized makes the class thread-safe.”** Only consistently protected complete invariants and safe publication do.
- **“Getters do not need the lock.”** They need coherent visibility/snapshot semantics.
- **“Notify stores an event.”** Conditions have no durable event count; store state.
- **“If wake returned, the predicate is true.”** Spurious wake/barging/other consumers require a loop.
- **“Signal hands the lock to the waiter.”** Common Mesa monitors let the signaler continue.
- **“Wait releases all my locks.”** It releases only the associated monitor lock.
- **“Reentrant means deadlock-free.”** Cross-lock cycles and invariant-reentrant callbacks remain.
- **“Timeout can be a single relative wait.”** Spurious wakes can restart/extend it; use one deadline.
- **“Interrupt means state unchanged.”** It may race after predicate change/partial operation; decide under lock.
- **“Callback under lock is efficient.”** Unknown code can block, reenter, acquire locks or throw.
- **“I/O under lock preserves atomicity safely.”** It creates unbounded hold and dependency cycles.
- **“Returning the collection is read-only enough.”** Aliases/elements/iterators can escape mutation and consistency.
- **“Broadcast is always safer and free.”** It can ensure liveness but cause herds; predicates still loop.
- **“Signal-one is always efficient.”** Wrong/ineligible waiter selection can strand eligible work.
- **“Fair mutex proves response deadlines.”** OS scheduling, holder duration and dependencies remain.
- **“Broadcast then free shuts down.”** Users must exit/join before destruction.

## Worked Examples

### Example 1

**Situation.** A bounded buffer has two consumers waiting for one item; a producer signals one.

**Reasoning.** The selected waiter becomes runnable, not owner of the item. Another thread may acquire first. Each consumer loops on `count > 0 OR closed`; only the one observing positive count takes. The other waits again or exits on close.

**Conclusion.** Permission derives from protected state, not notification.

### Example 2

**Situation.** Code uses `if (empty) wait(); take();` and a spurious wake occurs.

**Reasoning.** `take` reads absent state and violates invariant/contract. Replace `if` with a while predicate including terminal close/cancel/deadline. Recheck after reacquiring for every wake reason.

**Conclusion.** A predicate loop is required even without expected competing consumers.

### Example 3

**Situation.** A producer tests full without the lock, then prepares to wait while a consumer frees space and signals.

**Reasoning.** The signal can occur before registration, and the producer sleeps despite available capacity. Perform check and condition wait while owning the associated monitor so release-and-wait is atomic relative to state change.

**Conclusion.** The monitor closes the check-to-sleep lost-wakeup window.

### Example 4

**Situation.** A method returns its internal mutable map as an “unmodifiable” interface but values remain mutable.

**Reasoning.** Clients mutate value objects outside the lock and break multi-field invariant. Deep immutable snapshot/value projection or monitor-owned capabilities are required; document snapshot consistency and cost.

**Conclusion.** Representation confinement includes transitively mutable aliases.

### Example 5

**Situation.** Thread A holds monitor X and waits on Y; thread B needs X before it can signal Y.

**Reasoning.** Waiting on Y releases Y only, so A retains X. B blocks on X; A awaits B's signal. Redesign to avoid blocking nested calls, use one higher-level monitor, open-call state machine, or explicit global ordering that does not wait while nested.

**Conclusion.** Nested monitor lockout is a wait-specific deadlock.

### Example 6

**Situation.** A monitor calls an observer while its invariant is temporarily broken; the observer calls a getter reentrantly.

**Reasoning.** A reentrant lock permits entry and exposes inconsistent state. Restore invariant and detach immutable notification data under lock, then invoke observers after release on a controlled path.

**Conclusion.** Reentrancy prevents self-locking but can violate abstraction safety.

### Example 7

**Situation.** A timed pool acquisition wakes spuriously three times and restarts a 100 ms wait each time.

**Reasoning.** Total wait can exceed contract. Compute one monotonic deadline, loop and use remaining time. On expiry with lock held, recheck resource/closed/cancel and choose the specified winner.

**Conclusion.** Timed conditions use absolute budget across wakeups.

### Example 8

**Situation.** A low-priority logging thread holds a monitor while a high-priority control thread waits and medium CPU work runs.

**Reasoning.** Priority inversion can exceed deadline. Reduce hold work, move logging I/O outside, use platform priority-inheritance/protect if qualified, partition critical state, and validate worst-case scheduling on target hardware/OS.

**Conclusion.** Mutual exclusion needs priority-aware operational evidence in real-time systems.

### Example 9

**Situation.** Closing a resource pool signals `available` once although ten waiters must terminate.

**Reasoning.** One wakes/exits; others can remain forever because no resource will arrive. Under lock set `closed`, broadcast all related conditions, make predicates `resource available OR closed`, prevent new calls, and join users before destruction.

**Conclusion.** Closure is protected state and normally a broadcast terminal transition.

### Example 10

**Situation.** A surgical-device registry monitor waits for a hardware response while holding patient/session state.

**Reasoning.** Unbounded hardware I/O blocks alarms and can deadlock callbacks. Under lock record generation-qualified pending command and safety state, release, perform bounded authenticated I/O, then reacquire and conditionally apply actual result. Stable effect/audit identity and fail-safe policy handle timeout ambiguity. Named domain review validates invariants.

**Conclusion.** High-stakes monitors keep critical sections bounded and reconcile external effects explicitly.

## Cross-Program Connections

- [Operating Systems](../../22-operating-systems/ROADMAP.md): mutex/condition scheduling, cancellation, priority inheritance and lifecycle implement monitors.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md): cache coherence, memory ordering, false sharing and contention affect lock behavior.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): controlled scheduling, race/deadlock tools, model checking and stress verify invariants.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): private representation, alias prevention, lock denial-of-service, authorization and safe context constrain monitor APIs.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): open-call external effects, generation fencing and reconciliation extend beyond the process lock.
- [SEPAT-076](076-active-object.md) contrasts asynchronous scheduling; [SEPAT-079](../ROADMAP.md) applies bounded buffers; [SEPAT-080](../ROADMAP.md) deepens condition-variable behavior.

## References

1. Schmidt, Douglas C. “Monitor Object: An Object Behavioral Pattern for Concurrent Programming.” *C++ Report*, 2000. <https://www.dre.vanderbilt.edu/~schmidt/PDF/monitor.pdf>. Accessed 2026-08-29.
2. Schmidt, Douglas C., Michael Stal, Hans Rohnert, and Frank Buschmann. *Pattern-Oriented Software Architecture, Volume 2*. Wiley, 2000.
3. Hoare, C. A. R. “Monitors: An Operating System Structuring Concept.” *Communications of the ACM* 17, no. 10 (1974): 549–557. <https://doi.org/10.1145/355620.361161>.
4. The Open Group. “pthread_cond_clockwait, pthread_cond_timedwait, pthread_cond_wait,” POSIX.1-2024. <https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_cond_clockwait.html>. Accessed 2026-08-29.
5. The Open Group. “pthread_mutex_destroy, pthread_mutex_init,” POSIX.1-2024. <https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_mutex_destroy.html>. Accessed 2026-08-29.
6. Oracle. *The Java Language Specification, Java SE 25*, section 17, “Threads and Locks.” <https://docs.oracle.com/javase/specs/jls/se25/html/jls-17.html>. Accessed 2026-08-29.
7. Goetz, Brian, et al. *Java Concurrency in Practice*. Addison-Wesley, 2006. Locking, condition queues, safe publication, cancellation and liveness.
8. Lea, Doug. *Concurrent Programming in Java*, 2nd ed. Addison-Wesley, 1999.
9. Herlihy, Maurice, and Nir Shavit. *The Art of Multiprocessor Programming*, revised 1st ed. Morgan Kaufmann, 2012.
10. Butenhof, David R. *Programming with POSIX Threads*. Addison-Wesley, 1997.
11. Downey, Allen B. *The Little Book of Semaphores*, 2nd ed. Green Tea Press, 2016.
12. Bloch, Joshua. *Effective Java*, 3rd ed. Addison-Wesley, 2018. Synchronization and safe API design.

Lock reentrancy/fairness, condition wake/cancellation, timed clocks, memory visibility, robust-mutex recovery, priority protocols and destruction vary by language/OS/runtime. Current official specifications were checked on 2026-08-29; verify exact deployed semantics.

## Exercises

### Exercise 1

Design a capacity-(N) closing Monitor Object queue. State representation invariant; `not_empty`/`not_full` predicates; put/take/close linearization; exception, timed wait and cancellation behavior; signal/broadcast policy; and eight safety/lifecycle invariants.

### Exercise 2

A capacity-64 buffer holds fixed maximum 24 KiB payloads. At a measured stable rate of 500 items/s, mean time inside the buffer boundary is 80 ms. Compute maximum queued payload and average resident items. Explain why these figures prove neither enough capacity nor monitor correctness.

### Exercise 3

Design an open-call monitor for a connection/resource pool that must validate a lease with a slow remote system. Cover reservation/generation, invariant boundaries, condition predicates, deadline/cancellation, effect ambiguity, fairness, close and observability.

### Exercise 4

Diagnose a monitor using public mutable fields, a replaceable lock, unlocked getters, `if` waits, one shared wait set with signal-one, relative timeout restarts, nested monitor calls, callbacks and database I/O under lock, swallowed interrupts, and broadcast-then-free shutdown. Provide remediation and verification.

### Exercise 5

Design and review a Monitor Object for a safety-critical railway route reservation table. Address invariants, conflicting routes, priorities/fairness, condition scheduling, multiple-monitor composition, bounded external interlocking calls, authority, fail-safe close/recovery, security, observability, tests and named review.

## Answers to the Exercises

### Answer 1

Private stable-lock-protected state is fixed array/deque, capacity (N>0), count/head/tail, and closed flag/generation. Invariant: (0\le count\le N); indices valid; exactly count occupied logical slots in FIFO order; no new put after closed. `not_empty` is `count>0 OR closed`; `not_full` is `count<N OR closed` (with closed leading to rejection, not put).

Put acquires, loops while full and open using one monotonic deadline/cancel policy, rejects closed, inserts and increments at its protected mutation linearization point, restores invariant, signals `not_empty`. Take loops while empty/open; if empty/closed returns EOS; otherwise extracts/decrements at its mutation point and signals `not_full`. Close linearizes when setting closed/generation under lock and broadcasts both conditions. Exceptions restore state or quarantine; timeout/cancel returns only after final predicate check with lock.

Invariants include private nonescaping representation; stable lock on every access; invariant at entry/wait/exit; while predicates; atomic wait release; state change plus correct signal; one slot/item owner; FIFO; deadline not reset; cancel distinct from completed operation; no callback/I/O/nested wait under lock; close terminal for every waiter; and no destruction until all callers/waiters join.

### Answer 2

Maximum queued payload is

$$
64\times24\text{ KiB}=1536\text{ KiB}=1.5\text{ MiB}.
$$

Little's Law gives

$$
L=\lambda W=500\times0.08=40
$$

average items inside the measured buffer boundary.

The memory figure excludes container metadata, object graphs, producers/consumers, in-flight items, thread stacks/waiters and allocator overhead. Average occupancy does not bound bursts, percentiles or correlations and may hide upstream/downstream queues. Neither calculation verifies invariants, alias safety, memory ordering, waits/signals, fairness, cancellation, close or workload stability. Test actual distributions and concurrency semantics.

### Answer 3

Under the monitor choose an available resource, mark it `validating` with lease ID, owner and generation, decrement availability and restore invariant. Release the lock before remote validation. The resource is not visible as available during the call. On response, reacquire, compare pool/resource/lease generations and terminal/deadline/cancel state. If current and valid, mark leased and signal result; otherwise quarantine/return it and reconcile remote effect. On failure mark available/quarantined according to evidence and signal conditions.

Predicates include `eligible available resource OR closed`; fairness uses explicit waiter tickets/aging if required. One monotonic deadline covers local wait and remote validation. Cancel before reservation exits; during validation records intent but reaps result. Close stops new leases, broadcasts waiters, fences generation, cancels/reconciles validations, waits for/forces lease return by policy, then destroys after join. Observe wait/hold, validation duration/outcome, tickets/starvation, resource states/generations, stale results, cancels/timeouts, quarantine and shutdown residue. Verify every race, remote stall/duplicate/late response and close/reuse.

### Answer 4

Public fields/getters bypass consistency; replaceable/public lock breaks shared exclusion; `if` fails on spurious/competing wake; one signal may select an ineligible waiter; restarted relative waits exceed deadline; nested calls and callbacks/I/O create cycles/unbounded hold; swallowed interruption defeats cancellation; immediate free races waiters.

Make representation private and return immutable snapshots; use one private stable lock with all accesses. Define distinct condition predicates and while loops, mutate/signal under lock, broadcast where multiple predicate/lifecycle classes require it, and use one monotonic absolute deadline. Eliminate blocking nested monitor calls via global order or open-call state transitions; detach callbacks and external I/O outside with generation/version reconciliation. Propagate/translate interrupts deliberately and restore invariant on exceptions.

Close under lock, fence state, broadcast all conditions, reject entry, wait/join every user, then destroy. Verify state-machine invariants, alias attempts, spurious/redundant wake, wrong waiter, lost-wake barriers, timeout/signal/cancel races, exception injection, opposing lock orders, reentrant callback, slow DB, close with every waiter and destructor race using race/deadlock tools, stress/soak and target runtime tests.

### Answer 5

Private state maps routes/segments/switches to free, provisionally reserved, locked, occupied, releasing or failed with train/request/authority/generation, sequence, deadline and effect IDs. Invariants prohibit incompatible route overlap, unsafe switch combinations and conflicting authorities; every resource belongs to one state and generation. One stable monitor serializes table transitions. Predicates encode compatible route availability, current authority, lifecycle and fail-safe state.

Use explicit priority with aging/reserved emergency semantics proven not to starve safety prerequisites. Wait loops include close/failure/deadline; state mutation signals affected conditions and fail-safe closure broadcasts. Avoid holding monitor across interlocking hardware/network calls: record provisional intent/generation, release, issue authenticated bounded idempotent command, reacquire and apply only matching result; late/ambiguous effects enter fail-safe reconciliation. Multiple tables use one higher-level owner or fixed lock order and never condition-wait while nested.

Authenticate/authorize dispatchers, protect command/state/audit data, enforce quotas/replay defense and tamper evidence. Close blocks new routes, commands safe signals/state, wakes waiters, reconciles all hardware effects and joins users; recovery reads protected durable ledger and physical state before reopening. Observe invariant/route conflicts, wait age/priority, lock hold, interlocking results, stale/cancel/timeout, fail-safe and residue.

Verification includes formal route-conflict/invariant models, model checking of waits/priority, controlled concurrent schedules, hardware-in-the-loop, sensor/switch/network/power/process fault injection, overload, security tests, safe-close/restart drills and worst-case timing. Production claims require named railway signaling/domain/safety, controls/concurrency, human-factors, security, reliability/operations and regulatory reviewers with traceable hazards and acceptance evidence.
