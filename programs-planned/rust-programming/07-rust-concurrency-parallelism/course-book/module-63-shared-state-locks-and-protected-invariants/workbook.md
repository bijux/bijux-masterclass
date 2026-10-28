# Workbook — Module 63: Shared State: Locks and Protected Invariants

[Return to the chapter](index.md) · [Open the BatchWeave engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether the chapter has become an operational model. Freeze predictions, protocol diagrams, and invariants before compiling. Concurrency is unusually forgiving of explanations written after observing one successful run; that is exactly why the reasoning record must come first.

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

## Part 4 — Independent laboratory

Build [Protected Inventory](../../labs/module-03-protected-inventory/README.md) from the starter. Before opening the solution, produce:

- one written invariant relating capacity, available units, and reservations;
- a guard-scope trace for reserve and release;
- a poisoning decision with a testable outcome;
- barrier-coordinated contention tests that do not depend on sleep;
- a demonstration that logging or callbacks occur after guard release;

Your submission must also identify one schedule that the implementation handles correctly and one product claim it deliberately does not make.

## Part 5 — Capstone transfer

Implement the internal state of BatchWeave’s bounded queue, but not waiting yet. Define `QueueState<T>` with buffer, capacity, and closed flag under one mutex. Write invariants for length, closure, and ownership of enqueued jobs. Methods may return `WouldBlock` for full or empty states; Module 64 will add condition variables without changing the state relation.

Required capstone evidence:

- a queue invariant table and private state type;
- tests for capacity zero rejection, full, empty, closed, and FIFO behavior;
- no public mutex guard and no callback while locked;
- a poisoning policy justified by the absence or presence of user code inside the critical section;

Add at least one regression test that fails if this module's governing contract is removed. Tests that merely sleep and hope for a schedule do not count as causal evidence.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. What relation does a mutex protect in a correct design?
2. Why is `Arc` not a mutation protocol?
3. Where should guard scope end relative to state transition and effects?
4. What does poisoning communicate, and what does it not prove?
5. When do multiple locks require a global ordering rule?

### Independent transfer

Design a seat-allocation service where one booking may reserve adjacent seats atomically. Start with one lock over the seating map, then propose a finer design. For the finer design, write the complete lock order, explain how adjacency is checked without exposing a partial booking, and decide whether the extra concurrency is worth the proof cost.
