# Workbook — Module 64: Coordination: Condvars, Barriers, and Phase Protocols

[Chapter](index.md) · [Laboratory](../../labs/module-04-phase-gate/README.md) · [BatchWeave guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Coordination: Condvars, Barriers, and Phase Protocols** has become a usable model rather than remembered vocabulary. Its governing question is: *How do threads wait for a state predicate or phase transition without polling, lost wakeups, or treating notification itself as truth?* Preserve your first prediction and record decisive facts in a **predicate and wakeup record**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 63 — Shared State: Locks and Protected Invariants that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do threads wait for a state predicate or phase transition without polling, lost wakeups, or treating notification itself as truth?**
3. Draw the smallest **predicate and wakeup record** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### Prediction 1

A consumer changes `while queue.is_empty()` to `if queue.is_empty()` around `Condvar::wait`. Predict a spurious-wakeup failure.

Record: **predicate state, invalid transition, and repair**.

### Prediction 2

A producer notifies before a consumer begins waiting. The item remains in the queue. Predict whether the consumer can still proceed.

Record: **durable state versus notification history**.

### Prediction 3

Two consumers wake for one item. Predict the result when both use a correct loop.

Record: **competition and re-evaluation**.

### Prediction 4

Closing a full queue notifies only consumers. A producer is waiting on `not_full`. Predict termination.

Record: **enabled waiter classes and notification cardinality**.

### Prediction 5

A barrier expects four participants; one worker returns early on validation error. Predict the liveness result.

Record: **arrival obligation and deadlock**.

### Prediction 6

A timed wait restarts the full timeout after every spurious wake. Predict the deadline behavior.

Record: **budget accounting and repair**.

### Prediction 7

`OnceLock` holds mutable global test configuration initialized by the first test. Predict cross-test behavior.

Record: **one-time publication versus configurable dependency**.

### Prediction 8

A condition variable waits with a guard from an unrelated mutex. Predict the protocol defect and possible library behavior.

Record: **predicate/mutex association**.

## Part 2 — Diagnose and repair

Review a queue whose consumer checks emptiness, drops the mutex, then calls `thread::park`; producers push and call `unpark` on one recorded thread. The queue has multiple consumers, no closed state, and shutdown pushes one sentinel per expected worker.

Identify the lost-wakeup window, single-waiter assumption, sentinel-count coupling, and lack of durable termination state. Replace the protocol with a mutex-protected queue plus `not_empty`, `not_full`, and `closed`. State whether close drains buffered items and how all waiters terminate.

### Weak repairs to reject

Reject each of these shortcuts and replace it with the smallest repair that preserves the product requirement:

- changing `if` to one additional check without a loop;
- adding sleeps before waiting so producers have time to notify;
- treating a notification count as the product state;
- using sentinels whose number must equal a changing worker count;
- calling `notify_one` on close when many waiter classes can terminate;
- using a barrier when participants may cancel or panic before arrival;

For every repair, identify which of the six review dimensions it restores: ownership, visibility, exclusion, progress, failure, or determinism. A repair that improves one dimension may damage another; record both effects.

## Part 3 — Focused exercises

### Construction 1

Write the full state machine for a bounded queue.

Required evidence: Include empty, nonempty, full, closed-with-items, and closed-empty states plus enabled operations.

### Construction 2

Implement a deadline-based `pop_timeout`.

Required evidence: Use one `Instant` deadline, loop on the predicate, and distinguish item, closed, and timed-out results.

### Construction 3

Design a reusable two-phase barrier protocol.

Required evidence: State participant count, phase ownership, reuse, and panic behavior.

### Construction 4

Evaluate `OnceLock` for a process-wide parser table and for per-test configuration.

Required evidence: Use one-time publication only in the first case and justify the difference.

### Construction 5

Build a deterministic test that proves a blocked producer wakes after a pop.

Required evidence: Use channels or a barrier to establish that the queue is full and the producer has reached the operation; do not assert nanosecond timing.

### Interleaved reasoning pass

1. For **Write every condition-variable wait as a predicate loop over mutex-protected state**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the predicate and wakeup record.
2. For **Explain the atomic unlock-and-wait transition and why it prevents the ordinary lost-wakeup window**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the predicate and wakeup record.
3. For **Distinguish `notify_one` and `notify_all` by which state transition can enable which waiters**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the predicate and wakeup record.
4. For **Design bounded-buffer `not_empty`, `not_full`, and closure predicates**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the predicate and wakeup record.

5. Identify one guarantee from an earlier course that a careless implementation of **Coordination: Condvars, Barriers, and Phase Protocols** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Phase Gate](../../labs/module-04-phase-gate/README.md) from the starter. Before opening the solution, produce:

- explicit phase and waiting predicates;
- condition-variable loops that tolerate spurious wakeups;
- legal and illegal phase-transition tests;
- a shutdown or terminal phase that wakes every waiter;
- a barrier test with a fixed, fully accounted cohort;

Your submission must also identify one schedule that the implementation handles correctly and one product claim it deliberately does not make.

### Laboratory acceptance trace

Before opening the reference implementation for **Phase Gate**, record:

- the public behavior that demonstrates **Write every condition-variable wait as a predicate loop over mutex-protected state**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Turn BatchWeave’s queue state from Module 63 into a blocking bounded queue. Add `not_empty`, `not_full`, and `close`. Push must return the original job if closure wins. Pop must drain queued jobs and return `None` only at closed-empty. Document poison recovery and ensure no worker operation executes while the queue guard is live.

Required capstone evidence:

- predicate definitions for producer and consumer waits;
- a transition table including closure;
- tests that causally establish blocked push and blocked pop before enabling them;
- a test that close wakes all blocked producers and consumers;
- a guard-scope trace proving job execution happens after pop unlocks;

Add at least one regression test that fails if this module's governing contract is removed. Tests that merely sleep and hope for a schedule do not count as causal evidence.

### Capstone invariant trace

For the Module 64 BatchWeave increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. Why is the predicate, not notification, the source of truth?
2. What atomic relationship does `Condvar::wait` provide?
3. Why must waits loop even without an observed spurious wakeup?
4. Which queue transitions notify producers, consumers, or everyone?
5. Why can a barrier deadlock after one participant returns early?

### Independent transfer

Design a three-phase media pipeline whose fixed workers must all complete decode before transform, and transform before encode. First use barriers and state the participant obligations. Then introduce cancellation during decode and explain why the barrier design becomes unsafe. Replace it with a mutex-protected phase state and condition-variable protocol that can enter a terminal cancelled phase and wake all waiters.

### Closed-book defense

In five minutes, answer “How do threads wait for a state predicate or phase transition without polling, lost wakeups, or treating notification itself as truth?” using the **predicate and wakeup record**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside BatchWeave. A list of APIs without the deciding relationship is incomplete.
