# Workbook — Module 61: Threads, Schedules, Send, Sync, and Race Freedom

[Chapter](index.md) · [Laboratory](../../labs/module-01-thread-handoff-matrix/README.md) · [BatchWeave guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Threads, Schedules, Send, Sync, and Race Freedom** has become a usable model rather than remembered vocabulary. Its governing question is: *What may cross a thread boundary, what may be shared through a reference, and which correctness problems remain after Rust has ruled out data races?* Preserve your first prediction and record decisive facts in a **thread ownership map**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 60 — Integrated Systems Design, Testing, and Audit that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **What may cross a thread boundary, what may be shared through a reference, and which correctness problems remain after Rust has ruled out data races?**
3. Draw the smallest **thread ownership map** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### Prediction 1

A `String` is moved into `thread::spawn`, then printed by the parent. Predict the compiler result and identify the surviving owner.

Record: **outcome, ownership transfer, and the smallest requirement-preserving repair**.

### Prediction 2

An `Rc<Vec<u8>>` is cloned and one clone is moved into a worker. Predict whether reference-count liveness is enough.

Record: **outcome, auto-trait cause, and the correct ownership topology**.

### Prediction 3

An `Arc<RefCell<u64>>` is moved into two workers. Predict whether `Arc` repairs the inner sharing contract.

Record: **outcome, `Sync` obligation, and an appropriate replacement**.

### Prediction 4

Two threads use `AtomicUsize::load` followed by `store` to reserve the last unit. Predict whether safe Rust prevents over-reservation.

Record: **data-race status, product-race status, and atomic transition needed**.

### Prediction 5

Four workers finish in different orders and send `(index, value)` to one coordinator. The coordinator sorts by index. Classify schedule and output determinism.

Record: **which facts vary and which remain stable**.

### Prediction 6

A function drops all `JoinHandle`s immediately after spawning finite work. Predict whether work completion is part of the function contract.

Record: **compile status, lifecycle behavior, and missing obligation**.

### Prediction 7

The join loop returns on the first panic. Two later handles have not been joined. Predict the failure-state consequence.

Record: **language safety, product lifecycle defect, and repair**.

### Prediction 8

A wrapper contains only `Arc<Mutex<Vec<u8>>>`. Predict whether it is normally `Send` and `Sync` and explain from its components.

Record: **derived auto-trait reasoning, not a memorized answer**.

## Part 2 — Diagnose and repair

Analyze a download processor that stores all payloads in `Arc<Mutex<Vec<Vec<u8>>>>`, lets each worker lock the entire vector, removes one item, computes while holding the guard, and pushes its result into a second shared vector. It spawns one thread per item, discards handles, and prints the result vector directly.

Produce a defect table with one row for ownership topology, exclusion granularity, progress, thread lifecycle, failure, result ordering, and resource bounds. Then repair the architecture by moving each payload into a bounded set of workers or by using scoped partitioning. Do not begin by replacing `Mutex` with another primitive; first determine which sharing is unnecessary.

### Weak repairs to reject

Reject each of these shortcuts and replace it with the smallest repair that preserves the product requirement:

- adding `.clone()` until values satisfy the closure without deciding whether duplication is semantically required;
- replacing `Rc` with `Arc` while leaving unsynchronized interior mutation unchanged;
- wrapping the entire product state in one mutex and holding it through expensive work;
- dropping join handles because detached threads are memory-safe;
- sorting results without preserving stable source identity;
- calling a check-then-act sequence safe because each individual operation is atomic;

For every repair, identify which of the six review dimensions it restores: ownership, visibility, exclusion, progress, failure, or determinism. A repair that improves one dimension may damage another; record both effects.

## Part 3 — Focused exercises

### Construction 1

Construct a `Send`/`Sync` derivation table for `String`, `Rc<String>`, `Arc<String>`, `Cell<u64>`, `Mutex<Vec<u8>>`, and `Arc<Mutex<Vec<u8>>>`.

Required evidence: For each row, state whether ownership or a shared reference crosses the boundary and which component decides the result.

### Construction 2

Implement parallel byte sums over owned payloads without shared mutable state.

Required evidence: Join every handle, preserve input order, and report all panics after completing the join phase.

### Construction 3

Design a race-free but logically incorrect quota reservation with two atomics, then repair it with one atomic state transition.

Required evidence: Give a concrete schedule that violates the original quota and state the linearization point of the repair.

### Construction 4

Write a thread ledger for a finite image-processing operation.

Required evidence: Include input ownership, immutable configuration, worker return values, join ownership, cleanup, and result ordering.

### Construction 5

Bound a thread-per-item implementation honestly.

Required evidence: State the maximum accepted item count and explain when a fixed worker group becomes necessary.

### Interleaved reasoning pass

1. For **Distinguish concurrency, parallelism, scheduling, interleaving, data races, and broader race conditions**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the thread ownership map.
2. For **Derive whether an owned value may move into a thread from its `Send` obligation**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the thread ownership map.
3. For **Derive whether a shared reference may cross a thread boundary from the referent’s `Sync` obligation**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the thread ownership map.
4. For **Explain why `Arc<T>` provides shared ownership but not automatic mutation safety**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the thread ownership map.

5. Identify one guarantee from an earlier course that a careless implementation of **Threads, Schedules, Send, Sync, and Race Freedom** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Thread Handoff Matrix](../../labs/module-01-thread-handoff-matrix/README.md) from the starter. Before opening the solution, produce:

- a completed `Send`/`Sync` derivation matrix for every public payload type;
- a thread ledger covering ownership, joins, panic observation, and cleanup;
- tests proving deterministic source-order output under deliberately varied completion order;
- a check-then-act counterexample and its single-transition repair;
- an explicit maximum input or thread count;

Your submission must also identify one schedule that the implementation handles correctly and one product claim it deliberately does not make.

### Laboratory acceptance trace

Before opening the reference implementation for **Thread Handoff Matrix**, record:

- the public behavior that demonstrates **Distinguish concurrency, parallelism, scheduling, interleaving, data races, and broader race conditions**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Define BatchWeave’s core identities before building a queue: `JobId`, source index, `Job`, operation, `JobOutcome`, failure policy, and engine limits. Write the ownership row for each value from manifest parsing through worker execution to final reporting. The coordinator must remain the unique owner of output assembly; workers return indexed outcomes rather than mutate a shared report.

Required capstone evidence:

- a thread ledger for coordinator, workers, jobs, result sender, and join handles;
- a decision explaining why output order follows source index rather than completion order;
- a maximum job count and worker count;
- a test that feeds jobs with deliberately different execution durations and still produces stable output;

Add at least one regression test that fails if this module's governing contract is removed. Tests that merely sleep and hope for a schedule do not count as causal evidence.

### Capstone invariant trace

For the Module 61 BatchWeave increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. What exact relationship does `Send` describe?
2. What exact relationship does `Sync` describe?
3. Why can safe, data-race-free atomic code still violate a quota?
4. What obligations are represented by a `JoinHandle`?
5. How can completion remain nondeterministic while output is deterministic?

### Independent transfer

Design a thumbnail generator for at most 32 in-memory images. Each image is owned, the immutable rendering profile is shared, and the result must remain in request order. Write the thread ledger, choose a bounded thread topology, define panic behavior, and state whether one failed image cancels the rest. Then change the product to accept 100,000 images and explain which architectural assumption becomes invalid first.

### Closed-book defense

In five minutes, answer “What may cross a thread boundary, what may be shared through a reference, and which correctness problems remain after Rust has ruled out data races?” using the **thread ownership map**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside BatchWeave. A list of APIs without the deciding relationship is incomplete.
