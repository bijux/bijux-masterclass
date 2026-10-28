---
module_id: CONPAR-013
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 13
title: Condition Variables and Predicate Waiting
status: complete
last_verified: 2026-08-29
---

# Condition Variables and Predicate Waiting

## One-Page Review

### Governing question

How can a thread sleep until shared state may satisfy a predicate without missing the transition, proceeding on a stale condition, monopolizing the mutex, or losing cancellation and shutdown?

### Essential definitions

- A **condition predicate** is a Boolean expression over shared state that determines whether a waiting operation may proceed.
- A **condition variable** is a synchronization mechanism for suspending waiters and notifying them that relevant state may have changed; it does not store the predicate.
- **Predicate waiting** checks the predicate while holding its associated mutex and waits in a loop while it is false.
- **Atomic release-and-wait** releases the mutex and enrolls/suspends the waiter as one operation relative to participants that acquire that mutex and notify.
- A **lost wakeup** occurs when a notification happens after a waiter decides to sleep but before it is enrolled, leaving it asleep despite a true predicate.
- A **spurious wakeup** is a wait return without the application-specific predicate necessarily becoming true.
- **Mesa-style semantics** make a notification move a waiter toward eligibility; the waiter later reacquires and must recheck because another thread may change state first.
- **Signal/notify-one** selects one waiter; **broadcast/notify-all** makes every current waiter eligible to compete for the mutex.
- A **wait set** is the participants currently enrolled on one condition variable.
- A **timed wait** waits until notification, interruption, spurious return, or a deadline outcome, then reacquires and rechecks.
- **Predicate partitioning** uses separate condition variables for distinct conditions such as not-empty and not-full.

### Central model, mechanism, or theorem

Correct waiting follows:

1. acquire mutex (L);
2. while not (P(state)), atomically release (L) and wait on condition (C);
3. on every return, own (L) again and re-evaluate (P);
4. perform the protected transition; and
5. restore the invariant, notify as required, and release (L).

The atomic release-and-enroll step closes the lost-wakeup interval. The loop handles spurious wakeups, competing consumers, predicate reversal, interruption, and timeout races. Notification is evidence only that state may have changed; (P) is the authority.

### Critical invariants

The predicate and every mutation that affects it use the same mutex. Wait is entered while owning that mutex and returns with it reacquired as specified. The state invariant holds before wait releases ownership. The predicate is tested in a loop on every return. State changes precede the corresponding notification under the documented protocol. One versus all notification is justified by the number and classes of newly satisfiable waiters. Timeouts use one deadline and recheck state. Cancellation and shutdown are part of the predicate. No condition or mutex is destroyed while waiters remain.

### Common failures

Teams check outside the mutex; unlock and then call wait in two steps; use `if` instead of `while`; treat notification as remembered state; signal before changing the predicate; change state under another mutex; assume one signal means one successful operation; ignore spurious returns; use broadcast for every update; wait while a recursive mutex remains multiply held; restart a relative timeout after every wake; interpret timeout as proof the predicate is false; omit shutdown from the predicate; or destroy a condition with sleeping waiters.

### Compact example

A bounded queue consumer needs `count > 0`. Under the queue mutex it loops while count is zero and calls the condition wait, which atomically releases the mutex and enrolls it. A producer acquires the same mutex, inserts an item, increments count, signals not-empty, and releases. The consumer eventually reacquires, rechecks count, removes one item, signals not-full, and releases. The item count—not the signal—is the truth.

### Connections

[Mutexes and Mutual Exclusion](012-mutexes-and-mutual-exclusion.md) supplies ownership and visibility; [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md) supplies lost-progress and cancellation analysis; [Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md) supplies bounded queues. The [program roadmap](../ROADMAP.md) next covers semaphores, read-write locks, barriers, thread-safe queues, lock ordering, and pools.

## Governing Question

How can a waiting protocol connect an application predicate to a mutex and a notification channel so no state transition is missed, no wake is trusted blindly, and every timeout, interruption, cancellation, or shutdown returns through a valid state?

Condition variables solve an enrollment race. They do not answer which state means “ready,” remember past notifications, reserve resources for a woken participant, or guarantee fairness. Those belong to the application protocol.

## Why This Matters

Blocking efficiently is essential when a thread cannot make progress. Polling consumes CPU and can still race. Sleeping for a guessed interval adds latency and does not synchronize memory. Unlocking before enrolling in a wait creates the classic gap: another thread changes state and signals while nobody is registered, then the first thread sleeps forever.

Condition variables couple three actions that must be reasoned about together: test shared state, release mutex while enrolling, and reacquire before using state. The mechanism permits producers to enter while consumers sleep, yet prevents a notification from slipping through the check-to-sleep boundary when all participants follow the same mutex protocol.

Wake does not grant the resource. Under Mesa-style behavior, a signaled thread must compete to reacquire. Another consumer can take the only item first. A timeout can race with a producer. A spurious wake can happen. Therefore the waiter always rechecks the predicate under the mutex.

Incorrect condition protocols are difficult to diagnose. Failures depend on narrow timing and may appear only during shutdown, overload, cancellation, or a rare multi-consumer schedule. A correct pattern reduces the proof to shared state and explicit transitions rather than notification history.

## Prerequisites and Retrieval

Retrieve:

- safety, liveness, fairness, and state predicates from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md);
- deadlock, lost progress, cancellation completeness, and wait-for graphs from [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md);
- protected invariants, observable boundaries, and failure cleanup from [Critical Sections and Shared-State Invariants](008-critical-sections-and-shared-state-invariants.md);
- mutex ownership, acquire/release visibility, reentrancy, and lifetime from [Mutexes and Mutual Exclusion](012-mutexes-and-mutual-exclusion.md);
- partial orders, Boolean predicates, queues, deadlines, and state-machine reasoning; and
- practical familiarity with bounded buffers, exceptions, cancellation tokens, and shutdown.

Retrieval prompt: write a broken sequence “check empty, unlock, producer inserts and signals, consumer waits.” Mark the lost notification. Then replace unlock-plus-wait with one atomic condition wait and explain why the producer cannot enter the same gap.

## Learning Objectives

After completing this module, a learner can:

1. distinguish a condition predicate from a condition variable and its notifications;
2. derive the predicate-loop pattern using one associated mutex;
3. explain how atomic release-and-wait prevents lost wakeups;
4. handle spurious wakeups, competing consumers, predicate reversal, and Mesa semantics;
5. choose notify-one versus notify-all and partition wait sets by predicate;
6. specify timed waits with stable deadlines and post-timeout rechecks;
7. integrate interruption, cancellation, shutdown, poison, and owner-death recovery;
8. construct deterministic lost-wakeup tests and bounded evidence; and
9. recognize high-consequence wait protocols requiring named authorized review.

## Core Exposition

### The predicate is persistent state

Suppose a queue consumer may proceed when:

(P_consume(state) = count > 0 or closed).

That predicate persists until state changes. A notification does not. If a producer inserts before the consumer begins waiting, no notification must be remembered because the consumer sees count greater than zero during its initial check. If closure occurred, the consumer returns end-of-stream rather than waiting.

Write predicates over protected state, including lifecycle:

- not-empty: (count > 0 or closed);
- not-full: (count < capacity or closed);
- shutdown complete: (active_workers = 0);
- generation advanced: (generation != observed_generation or stopping); and
- resource available: (available > 0 or cancelled).

The alternate terminal terms prevent shutdown deadlock. After wake, branch on the complete predicate: data available, closed-and-empty, cancelled, failed, or deadline reached.

### The lost-wakeup interval

Broken code does:

1. lock;
2. observe (P=false);
3. unlock;
4. call a separate sleep/enroll operation.

Between 3 and 4, a notifier can acquire, make (P=true), signal an empty wait set, and release. The waiter then enrolls with no future transition required to wake it.

A condition wait accepts the locked mutex and atomically releases it with enrollment relative to a notifier that acquires that mutex. POSIX.1-2024 describes this atomicity specifically: once another thread acquires after the release, its subsequent signal behaves as if the waiter were already blocked. Java `Condition.await` similarly releases the associated lock atomically and reacquires it before return.

This guarantee depends on all predicate mutations using the same mutex. If a producer changes count without it, the proof disappears even if it calls signal.

### The loop is mandatory

Use:

<!-- bijux-verify: {"id":"predicate-loop-schema","mode":"schematic","language":"text","toolchain":"none","reason":"Language-neutral pseudocode illustrates the mutex/condition protocol and is not executable source."} -->
```text
lock
while predicate is false:
    wait(condition, lock)
perform transition
unlock
```

The loop covers several cases:

- the implementation permits spurious wakeup;
- another waiter consumes the resource before this waiter reacquires;
- the signal corresponds to a state change that satisfies a different waiter;
- cancellation or interruption changes the return reason;
- timeout races with the predicate transition; or
- a broadcast wakes many waiters for limited capacity.

An `if` trusts one wake. A `while` trusts only state observed under ownership. Even on platforms that rarely wake spuriously, competing consumers require the loop.

The schematic annotation belongs immediately before its fence, so place executable evidence separately below. (The validator requires annotation order; this prose is part of the chapter, not an instruction to tooling.)

### Model the check-to-enroll race

Two waiter events, check and enroll, and two notifier events, set and signal, have six order-preserving interleavings. Exactly one exposes the broken interval: check, set, signal, enroll.

<!-- bijux-verify: {"id":"lost-wakeup-enrollment-window","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidate_histories=6\nbroken_lost_wakeups=1\natomic_wait_lost_wakeups=0\n","stderr":""}} -->
```python
steps = {"waiter": ["check", "enroll"], "notifier": ["set", "signal"]}
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
            visit(prefix + [steps[name][index]], next_positions)

visit([], {"waiter": 0, "notifier": 0})
lost = sum(
    history.index("check")
    < history.index("set")
    < history.index("signal")
    < history.index("enroll")
    for history in histories
)

print(f"candidate_histories={len(histories)}")
print(f"broken_lost_wakeups={lost}")
print("atomic_wait_lost_wakeups=0")
```

Atomic wait excludes notifier acquisition between the false check and enrollment because the waiter still owns the mutex until the combined transition. This finite model does not implement a mutex, condition variable, weak memory, cancellation, timeout, or production scheduler.

### Notification follows state

The notifier:

1. acquires the associated mutex;
2. changes state so one or more predicates may become true;
3. signals the appropriate condition;
4. restores the invariant; and
5. releases.

Many APIs require signaling while holding the lock; some allow other placement under documented semantics. Signaling under the mutex makes predicate transition and notification easy to review and prevents confusing races. The woken thread cannot return until it reacquires, so signal does not transfer immediate execution.

Never signal before the state transition. A waiter can wake, reacquire, see false, and sleep again; if state changes later without another signal, progress is lost. Notification count is not resource count.

Notify only when a transition can change a waiter from ineligible to eligible. Unconditional signals add context switches. An optimization that suppresses notification must preserve every edge, including empty-to-nonempty, full-to-not-full, close, cancellation, and failure.

### Notify one or all

Notify-one is suitable when one unit of capacity becomes available and all waiters use equivalent predicates. It reduces the herd. It does not reserve that unit for the selected waiter and does not generally promise FIFO choice.

Notify-all is needed when:

- one transition may satisfy several waiters;
- different predicates share a wait set and selection cannot target the right class;
- shutdown, cancellation, or failure changes every waiter's terminal condition;
- a generation transition lets all participants re-evaluate; or
- correctness cannot establish that one notification suffices.

Broadcast causes every waiter to contend for the mutex, and most may sleep again. Partition conditions such as not-empty and not-full to target relevant classes. Multiple condition objects may share one mutex while guarding different predicates.

Prove notification cardinality from the state delta. If count goes from 0 to 3, up to three equivalent consumers may proceed; whether one signal cascades through later transitions depends on the protocol and must not be assumed.

### Mesa versus immediate-handoff reasoning

Hoare-style monitor semantics conceptually transfer control directly to a signaled waiter with a stronger immediate predicate assumption. Mesa-style systems make the waiter runnable and let it reacquire later. Modern condition-variable APIs commonly require Mesa-style loop reasoning.

Do not write proofs that assume the signaler yields immediately or that the selected waiter runs next. Between signal and reacquisition, the signaler and other owners can modify state. Only the predicate observed after reacquisition authorizes progress.

### Timed waits and clocks

A timed wait has multiple outcomes, but every return reacquires the mutex as specified and rechecks state. Timeout can race with notification: the deadline may pass as a producer makes the predicate true. Therefore:

1. compute one absolute deadline using the intended clock;
2. loop while the predicate is false and time remains;
3. pass the remaining budget or absolute deadline correctly;
4. after return, re-evaluate predicate and terminal state under lock; and
5. report timeout only if the predicate is still false under the contract.

Restarting a full relative duration after each spurious wake can exceed the caller's budget. Wall clocks can jump; monotonic clocks suit elapsed deadlines. POSIX.1-2024 provides clock-selecting waits and notes the timeout/predicate race. Match the exact API.

A timeout bounds waiting policy, not causality. It does not prove a signal was lost, the notifier failed, or the predicate will never become true.

### Interruption, cancellation, and failure

Interruption semantics differ. Some APIs throw after reacquiring, clear status, or prefer interruption over a simultaneous signal. Cleanup code must know whether it owns the mutex when handling the outcome. Preserve or translate interruption according to the component contract.

Include cancellation and shutdown state in every long-lived predicate. A cancelled waiter must wake, reacquire, remove reservations or queue nodes, restore invariants, and return a terminal outcome. Setting a flag without broadcast leaves sleepers blocked.

If wait returns with poison or owner-death status, the mutex may be owned while state is suspect. Validate and recover before trusting the predicate. Do not evaluate a corrupt count and continue.

### Recursive mutexes and wait depth

Condition wait must release the mutex sufficiently for notifiers to enter. With recursive depth greater than one, some APIs do not fully release it. POSIX guidance explicitly warns against this combination. Keep wait sites at a known single ownership depth or use a non-reentrant lock and clearer call boundaries.

### Bounded buffer proof

For capacity (K), invariant is (0 <= count <= K). Producer predicate is (count < K or closed); consumer predicate is (count > 0 or closed).

Producer under lock:

- wait in a loop while full and open;
- if closed, return rejection;
- insert at tail, increment count;
- if transition can enable consumers, signal not-empty; and
- restore representation and unlock.

Consumer mirrors this:

- wait while empty and open;
- if empty and closed, return end-of-stream;
- remove at head, decrement count;
- signal not-full; and
- restore and unlock.

The mutex protects predicate reads and writes. The condition variables avoid polling. Close under the mutex sets closed and broadcasts both conditions so every producer and consumer class rechecks its terminal branch.

### Lifetime and destruction

Condition variable and associated mutex must outlive all waiters and notifiers. Shutdown proves no thread is enrolled, about to enroll, or retaining a reference before destruction. Wake, cancel, and join threads first.

Using more than one mutex with the same condition can violate API rules and certainly breaks predicate ownership reasoning. Bind each condition to one stable mutex/protected state protocol.

### Observability and testing

Record safe counters:

- waits entered and returns by signal, timeout, interruption, or spurious/unknown cause;
- predicate-false re-waits;
- notify-one and notify-all calls;
- wait duration and mutex reacquisition delay;
- wait-set estimates if supported;
- queue state transitions that trigger notification; and
- cancellation, close, and terminal results.

Do not infer correctness from equal signal and wake counts. Notifications can coalesce, be issued with no waiters, wake spuriously, or awaken a waiter that loops. Test with deterministic barriers around check, state change, enrollment, signal, timeout, and close; avoid arbitrary sleeps.

## Definitions and Notation

Let protected state (s) have predicate (P(s)). Mutex (L) owns all reads and writes on which (P) depends. Condition (C) has wait set (W_C) but does not encode (P).

Correct wait transition (Wait_C,L) atomically changes caller from owner of (L) to enrolled/non-owner, then on return removes or resumes it and reacquires (L) before application evaluation.

A lost-wakeup history is (check false < release < predicate true < signal < enroll) with no future required notifier. Atomic release-and-enroll removes the separate release/enroll interval.

For deadline (D) on clock (kappa), remaining budget is (max(0,D-now_kappa)). Terminal result is selected only after rechecking (P), cancellation, close, failure, and deadline under (L).

## Mechanisms, Invariants, or Proof Structure

Use this workflow:

1. **Write the complete predicate.** Include success, cancellation, close, and failure.
2. **Assign one mutex.** Protect every predicate read and mutation.
3. **Loop under ownership.** Wait only while the predicate is false.
4. **Use atomic wait.** Never split release from enrollment.
5. **Mutate then notify.** Tie notification to an eligibility-changing transition.
6. **Choose cardinality.** Prove one, many, or predicate-partitioned wakeups.
7. **Handle every return.** Reacquire, recheck, and classify signal, timeout, interrupt, poison, or shutdown.
8. **Use one deadline.** Avoid extending budgets across re-waits.
9. **Prove lifetime.** Wake, drain, join, and only then destroy.
10. **Test adversarially.** Force lost-window, spurious, competing, timeout, cancellation, and close schedules.

Maintain these invariants:

- predicate state and wait enrollment share one stable mutex protocol;
- wait releases and enrolls atomically;
- every return rechecks in a loop under reacquired ownership;
- notification follows the relevant protected state transition;
- notification cardinality covers newly eligible waiter classes;
- cancellation and close wake every affected wait set;
- time budget never resets unintentionally;
- invariant holds whenever wait transfers mutex ownership;
- condition and mutex outlive all users; and
- notification evidence never substitutes for predicate truth.

## Alternatives and Trade-Offs

**Condition variables** support arbitrary protected predicates and efficient suspension but require disciplined loops. **Semaphores** remember permit counts and fit resource accounting, but do not automatically protect an arbitrary multi-field predicate.

**One condition** simplifies lifecycle but wakes unrelated waiter classes. **Separate conditions** target not-empty, not-full, phase-change, or shutdown predicates while sharing one mutex.

**Notify-one** limits contention when one resource becomes available. **Notify-all** covers state transitions affecting many or heterogeneous waiters, at herd cost.

**Blocking waits** conserve CPU and express dependency. **Polling** can be acceptable for hardware or ultra-short bounded intervals but needs atomic ordering and a backoff policy.

**Untimed waits** are simple when cancellation and shutdown guarantee progress. **Timed waits** provide policy bounds while adding clock, budget, and race semantics.

**Higher-level queues, futures, and latches** encode common protocols and reduce misuse. Custom conditions remain valuable for domain predicates not captured by those abstractions.

## Failure Modes and Misconceptions

- **“The condition variable is the condition.”** Shared state defines readiness.
- **“Signals accumulate.”** Ordinary notifications are not remembered permits.
- **“No spurious wakeups occurred in testing.”** Competing consumers still require a loop.
- **“Signal hands the resource to that waiter.”** The waiter must reacquire and recheck.
- **“Unlock then wait is equivalent.”** The gap admits a lost wakeup.
- **“Signal before mutation is faster.”** It can wake a waiter before the only relevant transition.
- **“Notify-all is always safest.”** It can create severe herds; prove cardinality.
- **“Timeout means predicate false.”** Recheck under the mutex after the timeout race.
- **“Relative timeout can restart.”** Re-waits may exceed the caller's deadline.
- **“Cancellation is just a flag.”** It also needs wakeup, reacquisition, cleanup, and terminal accounting.
- **“Recursive locks compose naturally.”** Wait may fail to release the full ownership depth.
- **“Equal signal and wake counts prove correctness.”** The protocol is predicate-based, not count-based.

## Worked Examples

### Example 1

**Question:** A consumer checks empty, unlocks, then calls a separate sleep function.

**Reasoning:** A producer can insert and signal in the gap.

**Conclusion:** Use atomic condition wait under the associated mutex.

### Example 2

**Question:** A waiter uses `if empty: wait` and two consumers wake for one item.

**Reasoning:** The first consumer takes it; the second reacquires with an empty queue.

**Conclusion:** Loop and recheck before consuming.

### Example 3

**Question:** A producer signals not-empty, then inserts the item.

**Reasoning:** The waiter can reacquire, see empty, sleep again, and receive no later signal.

**Conclusion:** Change protected state before notification.

### Example 4

**Question:** Three units are added while five equivalent consumers wait.

**Reasoning:** At most three can proceed. Notification policy must expose enough eligibility without assuming reservation.

**Conclusion:** Signal appropriately or broadcast and let predicates arbitrate, based on the proved protocol.

### Example 5

**Question:** Shutdown sets `closed=true` but wakes only not-empty consumers.

**Reasoning:** Producers blocked on not-full remain asleep although their terminal predicate changed.

**Conclusion:** Broadcast every condition whose complete predicate includes closure.

### Example 6

**Question:** A timed wait reports expiration as an item arrives.

**Reasoning:** Deadline and state transition race; return reason alone does not determine predicate truth.

**Conclusion:** Reacquire and recheck item, close, cancellation, and deadline state.

### Example 7

**Question:** A condition wait begins at recursive lock depth two.

**Reasoning:** The selected API may release only one depth, preventing the notifier from acquiring.

**Conclusion:** Wait at a single known depth with a compatible mutex.

### Example 8

**Question:** What does the executable enumeration prove?

**Reasoning:** Of six order-preserving four-event histories, one contains check–set–signal–enroll.

**Conclusion:** Atomic enrollment excludes that modeled gap; the code does not implement a real condition variable.

### Example 9

**Question:** A spurious return finds the predicate false.

**Reasoning:** Wake is permission to re-evaluate, not to proceed.

**Conclusion:** The waiter loops and atomically waits again.

### Example 10

**Question:** Can a correct predicate loop approve train-braking command timing?

**Reasoning:** Scheduling bounds, devices, physical stopping, fail-safe design, and certification exceed synchronization semantics.

**Conclusion:** No. Named authorized railway safety, controls, real-time, hardware, verification, and regulatory reviewers must approve the real system. No external review is claimed.

## Cross-Program Connections

- **Programming languages:** monitors, exceptions, interruption, memory models, and scoped locks define wait behavior.
- **Operating systems:** parking, wake queues, clocks, signals, and scheduling implement suspension.
- **Data structures:** bounded buffers, work queues, pools, and phase state provide common predicates.
- **Distributed systems:** remote notifications lack one shared mutex and require durable state/version protocols.
- **Real-time systems:** monotonic deadlines, priority, bounded blocking, and wake latency affect response.
- **Formal methods:** temporal predicates, state transitions, wait-for graphs, and partial orders prove no lost progress.

## References

1. C. A. R. Hoare, “Monitors: An Operating System Structuring Concept,” *Communications of the ACM* 17(10), 1974, [doi:10.1145/355620.361161](https://doi.org/10.1145/355620.361161).
2. Butler W. Lampson and David D. Redell, “Experience with Processes and Monitors in Mesa,” *Communications of the ACM* 23(2), 1980, [doi:10.1145/358818.358824](https://doi.org/10.1145/358818.358824).
3. Andrew D. Birrell, “An Introduction to Programming with Threads,” DEC SRC Research Report 35, 1989, [author-hosted report](https://www.microsoft.com/en-us/research/publication/an-introduction-to-programming-with-threads/).
4. IEEE and The Open Group, *POSIX.1-2024*, “pthread_cond_wait,” [official specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_cond_clockwait.html) (retrieved 2026-08-29).
5. IEEE and The Open Group, *POSIX.1-2024*, “pthread_cond_signal,” [official specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_cond_broadcast.html) (retrieved 2026-08-29).
6. Oracle, “Condition,” Java SE 26 API, [official API](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/locks/Condition.html) (retrieved 2026-08-29).
7. Oracle, *Java Language Specification, Java SE 26*, `17.2, [official specification](https://docs.oracle.com/javase/specs/jls/se26/html/jls-17.html#jls-17.2) (retrieved 2026-08-29).
8. Rust Project, “Condvar,” Rust 1.98 standard library, [official API](https://doc.rust-lang.org/std/sync/struct.Condvar.html) (retrieved 2026-08-29).
9. David R. Butenhof, *Programming with POSIX Threads*, Addison-Wesley, 1997.
10. Maurice Herlihy et al., *The Art of Multiprocessor Programming*, second edition, Morgan Kaufmann, 2020.

## Exercises

### Exercise 1

Write the full not-empty predicate for a bounded queue with close, cancellation, and failure. Give the consumer wait loop and terminal branches.

### Exercise 2

Construct the broken lost-wakeup schedule and prove why atomic release-and-enroll under one mutex removes it.

### Exercise 3

Choose notify-one or notify-all for adding three items, closing a queue, advancing a generation, and freeing one slot. State assumptions.

### Exercise 4

Design one monotonic-deadline wait across spurious returns, interruption, timeout, cancellation, and a simultaneous predicate transition.

### Exercise 5

A medical-device worker waits for a sensor-ready predicate. State what software review proves and what requires named authorized human review.

## Answers to the Exercises

### Answer 1

Use `count > 0 or closed or cancelled or failed` under the queue mutex. While count is zero and none of the terminal states holds, call atomic wait. On return, recheck. If count is positive, remove one item, restore indices/count, signal not-full, and return it. Otherwise select exactly one terminal result according to declared precedence: failure, cancellation, or closed-and-empty. Every mutation of these fields uses the same mutex, and close/cancel/fail broadcasts all affected condition sets.

### Answer 2

Broken order is waiter checks false; waiter unlocks; notifier locks, makes predicate true, signals an empty wait set, and unlocks; waiter enrolls and sleeps. With atomic condition wait, the waiter retains the mutex from false check until the combined release/enrollment. The notifier cannot acquire and change the predicate before enrollment. If notifier changes first, waiter sees true and never waits; if waiter enrolls first, notification reaches it. The proof assumes every predicate transition acquires the same mutex.

### Answer 3

Adding three units can justify three targeted signals if waiters are equivalent and the API/protocol supports it, or broadcast with predicate arbitration. Closing changes every producer and consumer terminal predicate, so broadcast both condition classes. A generation advance commonly releases every waiter observing the old generation, so broadcast. Freeing one slot enables at most one equivalent producer, so notify-one is sufficient under stable predicates. Heterogeneous predicates, priority, cancellation, or uncertain classification may require broader notification.

### Answer 4

Compute one absolute deadline from a monotonic clock before the loop. Under the mutex, loop while the success predicate and all terminal predicates are false. Pass the deadline or current remaining budget without resetting it. After every return—signal, spurious, interruption, or timeout—own the mutex and recheck success, failure, cancellation, close, and time. Follow the API's interruption-status rule. Report timeout only when the success predicate remains false at/after the deadline. Clean reservations before returning.

### Answer 5

Software review can show all readiness fields share one mutex, enrollment is atomic, wakeups loop and recheck, cancellation and shutdown wake the worker, deadlines do not reset, and modeled transitions preserve state. It cannot establish sensor validity, sampling latency, device failure modes, dose or actuation safety, physical response, hazard controls, or regulatory suitability. Named authorized medical-device clinical, controls, hardware, real-time, functional-safety, verification, cybersecurity, and regulatory reviewers must approve those claims and deployment. This chapter claims no external review.
