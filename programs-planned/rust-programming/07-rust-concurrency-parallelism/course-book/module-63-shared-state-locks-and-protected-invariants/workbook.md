# Workbook — Module 63: Shared State: Locks and Protected Invariants

[Chapter](index.md) · [Laboratory](../../labs/module-03-protected-inventory/README.md) · [BatchWeave guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Shared State: Locks and Protected Invariants** has become a usable model rather than remembered vocabulary. Its governing question is: *Which exact invariant does a lock protect, how small can the protected transition be, and what state remains valid after contention or panic?* Preserve your first prediction and record decisive facts in a **protected-invariant table**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 62 — Structured Threads: Scopes, Joins, and Panic Boundaries that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Which exact invariant does a lock protect, how small can the protected transition be, and what state remains valid after contention or panic?**
3. Draw the smallest **protected-invariant table** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### Prediction 1

`available` and `reserved` use separate mutexes. A reservation decrements one and then increments the other. Predict an observable invalid state.

Record: **schedule, violated relation, and smallest coherent lock boundary**.

### Prediction 2

A worker holds a mutex guard while sending to a bounded channel whose receiver needs the same mutex. Predict the wait cycle.

Record: **lock/channel dependency and progress failure**.

### Prediction 3

`Arc<State>` contains mutable fields but no synchronization. Predict whether shared ownership permits mutation.

Record: **liveness versus access contract**.

### Prediction 4

A mutex is poisoned after panic. Another thread calls `into_inner()` and continues. Is memory safety violated, and what product proof is missing?

Record: **language safety and invariant-recovery policy**.

### Prediction 5

A public method returns `MutexGuard<State>` to callers. Predict which architectural obligations escape the type.

Record: **guard lifetime, lock order, callbacks, and invariant control**.

### Prediction 6

A read-heavy catalog uses `RwLock`. The design requires writers to be served before new readers. Is that a portable correctness guarantee?

Record: **library contract versus scheduling assumption**.

### Prediction 7

A test sleeps, then asserts that thread A acquired a lock before thread B. Classify the evidence quality.

Record: **causal coordination versus timing guess**.

### Prediction 8

A function copies a snapshot, drops the guard, and then logs it. Predict the exclusion and reentrancy benefits.

Record: **guard scope and external effects**.

## Part 2 — Diagnose and repair

Review a reservation service with three `Arc<Mutex<u64>>` fields: capacity, available, and reserved. It locks them in different orders in `reserve`, `release`, and `snapshot`; logs while all guards are held; exposes one guard to a callback; and recovers every poison with `into_inner`.

Construct the invariant and lock-order tables. Show at least one invalid intermediate observation and one deadlock cycle. Replace the three locks with the minimum coherent state boundary, move logging outside the guard, and define a poisoning policy based on whether state can be validated or reconstructed.

### Weak repairs to reject

Reject each of these shortcuts and replace it with the smallest repair that preserves the product requirement:

- adding more mutexes without identifying independent invariants;
- placing every field behind its own lock to maximize theoretical parallelism;
- holding a guard during channel send, I/O, logging, or user callbacks;
- recovering poison automatically without validating state;
- switching to `RwLock` because the workload is described vaguely as read-heavy;
- using sleeps to force lock acquisition order in tests;

For every repair, identify which of the six review dimensions it restores: ownership, visibility, exclusion, progress, failure, or determinism. A repair that improves one dimension may damage another; record both effects.

## Part 3 — Focused exercises

### Construction 1

Model a two-account transfer under one lock and under two locks.

Required evidence: State the invariant, linearization point, lock order, and snapshot behavior for both designs.

### Construction 2

Refactor a callback-under-lock API into snapshot and commit phases.

Required evidence: Use a revision or expected-state check so the callback runs without the guard.

### Construction 3

Design a poisoning policy for a cache whose values can be rebuilt from immutable source data.

Required evidence: State detection, repair, poison clearing, and failure if rebuilding fails.

### Construction 4

Evaluate whether an `RwLock` is justified for a configuration catalog.

Required evidence: State read duration, write frequency, fairness assumptions, and what must be measured later.

### Construction 5

Write a barrier-coordinated invariant test for concurrent inventory reservations.

Required evidence: Do not assert which thread wins; assert capacity and exactly one successful reservation when supply is one.

### Interleaved reasoning pass

1. For **Name the state invariant protected by each `Mutex` or `RwLock` rather than treating the primitive as a generic thread-safety wrapper**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the protected-invariant table.
2. For **Distinguish shared liveness supplied by `Arc` from exclusion supplied by a lock**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the protected-invariant table.
3. For **Keep guard scope limited to the smallest complete state transition**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the protected-invariant table.
4. For **Avoid performing user callbacks, channel sends, file I/O, or expensive computation while holding a guard**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the protected-invariant table.

5. Identify one guarantee from an earlier course that a careless implementation of **Shared State: Locks and Protected Invariants** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Protected Inventory](../../labs/module-03-protected-inventory/README.md) from the starter. Before opening the solution, produce:

- one written invariant relating capacity, available units, and reservations;
- a guard-scope trace for reserve and release;
- a poisoning decision with a testable outcome;
- barrier-coordinated contention tests that do not depend on sleep;
- a demonstration that logging or callbacks occur after guard release;

Your submission must also identify one schedule that the implementation handles correctly and one product claim it deliberately does not make.

### Laboratory acceptance trace

Before opening the reference implementation for **Protected Inventory**, record:

- the public behavior that demonstrates **Name the state invariant protected by each `Mutex` or `RwLock` rather than treating the primitive as a generic thread-safety wrapper**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Implement the internal state of BatchWeave’s bounded queue, but not waiting yet. Define `QueueState<T>` with buffer, capacity, and closed flag under one mutex. Write invariants for length, closure, and ownership of enqueued jobs. Methods may return `WouldBlock` for full or empty states; Module 64 will add condition variables without changing the state relation.

Required capstone evidence:

- a queue invariant table and private state type;
- tests for capacity zero rejection, full, empty, closed, and FIFO behavior;
- no public mutex guard and no callback while locked;
- a poisoning policy justified by the absence or presence of user code inside the critical section;

Add at least one regression test that fails if this module's governing contract is removed. Tests that merely sleep and hope for a schedule do not count as causal evidence.

### Capstone invariant trace

For the Module 63 BatchWeave increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. What relation does a mutex protect in a correct design?
2. Why is `Arc` not a mutation protocol?
3. Where should guard scope end relative to state transition and effects?
4. What does poisoning communicate, and what does it not prove?
5. When do multiple locks require a global ordering rule?

### Independent transfer

Design a seat-allocation service where one booking may reserve adjacent seats atomically. Start with one lock over the seating map, then propose a finer design. For the finer design, write the complete lock order, explain how adjacency is checked without exposing a partial booking, and decide whether the extra concurrency is worth the proof cost.

### Closed-book defense

In five minutes, answer “Which exact invariant does a lock protect, how small can the protected transition be, and what state remains valid after contention or panic?” using the **protected-invariant table**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside BatchWeave. A list of APIs without the deciding relationship is incomplete.
