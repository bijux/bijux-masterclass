# Workbook — Module 66: Liveness: Deadlock, Cancellation, and Recovery

[Chapter](index.md) · [Laboratory](../../labs/module-06-cancellable-worker-group/README.md) · [BatchWeave guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Liveness: Deadlock, Cancellation, and Recovery** has become a usable model rather than remembered vocabulary. Its governing question is: *Why can every blocked operation eventually continue or terminate, and what happens when cancellation, panic, or partial infrastructure failure interrupts the normal path?* Preserve your first prediction and record decisive facts in a **wait-for and shutdown graph**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 65 — Message Passing, Backpressure, and Shutdown that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Why can every blocked operation eventually continue or terminate, and what happens when cancellation, panic, or partial infrastructure failure interrupts the normal path?**
3. Draw the smallest **wait-for and shutdown graph** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### Prediction 1

A cancellation flag becomes true while workers wait on a condition variable whose predicate ignores it. Predict termination.

Record: **state/wake/predicate gap**.

### Prediction 2

Two functions acquire locks A then B and B then A. Predict the minimal wait-for cycle.

Record: **resource order and deadlock**.

### Prediction 3

A retry loop uses compare-exchange and immediately retries forever under contention. Classify possible progress failure.

Record: **starvation or livelock and backoff/architecture repair**.

### Prediction 4

A worker panics after popping a job but before sending a result. The coordinator waits for exactly N messages. Predict behavior.

Record: **terminal accounting and receive strategy**.

### Prediction 5

Fail-fast cancellation closes the queue while the coordinator is blocked in push. Predict how the original unsent job should be handled.

Record: **ownership return and reconciliation**.

### Prediction 6

A worker catches panic around both queue operations and user work, then continues. Predict invariant risk.

Record: **containment boundary**.

### Prediction 7

Shutdown can be called from normal completion and a worker fault at the same time. Predict the value of idempotence.

Record: **state transition and duplicate cleanup**.

### Prediction 8

A liveness test sleeps 100 ms and declares deadlock if a worker is not done. Classify the result.

Record: **test timeout versus causal proof**.

## Part 2 — Diagnose and repair

Audit a service with two locks, one bounded result channel, one barrier, and a cancellation flag. The coordinator holds lock A while sending results; workers hold lock B while acquiring A; shutdown waits at the barrier, but a panicked worker never arrives; setting cancellation does not notify queue waiters; and the coordinator expects one result per input forever.

Build a wait-for graph and terminal-accounting table. Remove the barrier from failure-sensitive shutdown, define one lock order or eliminate nested acquisition, close/notify the queue on cancellation, receive until sender disconnect plus worker joins, and reconcile every indexed input.

### Weak repairs to reject

Reject each of these shortcuts and replace it with the smallest repair that preserves the product requirement:

- adding longer sleeps or timeouts without changing the production protocol;
- setting a cancellation flag without waking blocked operations;
- catching panic around an invariant-bearing subsystem and continuing blindly;
- returning after the first worker panic without joining the rest;
- waiting for an exact result count when a worker can die before sending;
- adding random backoff to a livelock without proving eventual progress;

For every repair, identify which of the six review dimensions it restores: ownership, visibility, exclusion, progress, failure, or determinism. A repair that improves one dimension may damage another; record both effects.

## Part 3 — Focused exercises

### Construction 1

Construct a wait-for graph for two locks and a bounded result channel.

Required evidence: Include ownership edges and show one reachable cycle.

### Construction 2

Design a cancellable condition-variable wait.

Required evidence: Add cancellation to the protected predicate and identify the transition that notifies every waiter.

### Construction 3

Specify idempotent worker-group shutdown.

Required evidence: Define lifecycle states, allowed repeated calls, queue closure, sender drops, joins, and returned status.

### Construction 4

Contain one job panic while preserving one outcome per accepted job.

Required evidence: State what worker-local state may be reused and how missing outcomes are reconciled.

### Construction 5

Write a termination argument for a finite queue with fail-fast cancellation.

Required evidence: Cover blocked submitters, queued jobs, active jobs, result senders, and joins.

### Interleaved reasoning pass

1. For **Distinguish deadlock, starvation, livelock, priority inversion, and slow work**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the wait-for and shutdown graph.
2. For **Construct a wait-for graph over locks, channels, joins, barriers, and conditions**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the wait-for and shutdown graph.
3. For **State a global lock order and identify operations that violate it**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the wait-for and shutdown graph.
4. For **Design cancellation as state plus a wake mechanism plus an observation point**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the wait-for and shutdown graph.

5. Identify one guarantee from an earlier course that a careless implementation of **Liveness: Deadlock, Cancellation, and Recovery** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Cancellable Worker Group](../../labs/module-06-cancellable-worker-group/README.md) from the starter. Before opening the solution, produce:

- a wait-for graph for normal and cancellation paths;
- a lifecycle state machine with idempotent shutdown;
- tests for cancellation while producer and consumer are blocked;
- panic containment with complete joining;
- exact terminal accounting for all accepted work;

Your submission must also identify one schedule that the implementation handles correctly and one product claim it deliberately does not make.

### Laboratory acceptance trace

Before opening the reference implementation for **Cancellable Worker Group**, record:

- the public behavior that demonstrates **Distinguish deadlock, starvation, livelock, priority inversion, and slow work**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Add BatchWeave’s `FailurePolicy`, cancellation flag, fail-fast transition, worker panic containment, and terminal reconciliation. Cancellation must close the work queue so blocked submitters and consumers wake. Workers check cancellation before execution. The coordinator records unsent and missing jobs as cancelled or infrastructure failures according to the documented policy, then joins every handle.

Required capstone evidence:

- a wait-for graph showing no cycle among queue, result channel, coordinator, and workers;
- a cancellation state/wake/checkpoint table;
- tests for cancellation while push is blocked and while pop is blocked;
- one terminal outcome per manifest job after a worker panic;
- an idempotent shutdown trace covering competing initiators;

Add at least one regression test that fails if this module's governing contract is removed. Tests that merely sleep and hope for a schedule do not count as causal evidence.

### Capstone invariant trace

For the Module 66 BatchWeave increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. How do safety and liveness claims differ?
2. What nodes and edges belong in a wait-for graph?
3. Why is a cancellation flag alone incomplete?
4. Where should panic containment begin and end?
5. How does final reconciliation prove that accepted jobs did not disappear?

### Independent transfer

Design a cancellable file-indexing group with a bounded path queue. One parser panic must cancel new work, wake blocked submission, preserve already completed results, join every worker, and report every accepted path as indexed, failed, panicked, or cancelled. Write the complete termination argument and a causal test for cancellation while the queue is full.

### Closed-book defense

In five minutes, answer “Why can every blocked operation eventually continue or terminate, and what happens when cancellation, panic, or partial infrastructure failure interrupts the normal path?” using the **wait-for and shutdown graph**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside BatchWeave. A list of APIs without the deciding relationship is incomplete.
