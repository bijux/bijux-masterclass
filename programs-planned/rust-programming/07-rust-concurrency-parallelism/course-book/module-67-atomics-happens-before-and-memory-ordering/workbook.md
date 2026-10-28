# Workbook — Module 67: Atomics, Happens-Before, and Memory Ordering

[Chapter](index.md) · [Laboratory](../../labs/module-07-atomic-progress/README.md) · [BatchWeave guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Atomics, Happens-Before, and Memory Ordering** has become a usable model rather than remembered vocabulary. Its governing question is: *Which fact does an atomic operation publish, which earlier writes become visible because of it, and what is the weakest ordering that proves the required relationship?* Preserve your first prediction and record decisive facts in a **happens-before graph**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 66 — Liveness: Deadlock, Cancellation, and Recovery that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Which fact does an atomic operation publish, which earlier writes become visible because of it, and what is the weakest ordering that proves the required relationship?**
3. Draw the smallest **happens-before graph** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### Prediction 1

A producer writes ordinary payload fields then stores `ready = true` with `Relaxed`; a consumer spins on a relaxed load and reads payload. Predict the missing relation.

Record: **publication edge and orderings**.

### Prediction 2

A relaxed attempts counter is used only for telemetry. Predict whether it orders access to job data.

Record: **atomicity versus publication**.

### Prediction 3

Two relaxed counters are loaded into one snapshot. Predict whether the pair represents one instant.

Record: **cross-location coherence claim**.

### Prediction 4

A CAS uses `AcqRel` on success and `Release` on failure. Predict validity.

Record: **failure-path semantics**.

### Prediction 5

A quota loop performs an irreversible log write inside a `fetch_update` closure. Predict duplicate effects.

Record: **closure retry behavior**.

### Prediction 6

A sequence value changes 7→8→7 before CAS. Predict what equality with 7 proves.

Record: **ABA**.

### Prediction 7

All atomics are changed to `SeqCst`. Predict which defects remain possible.

Record: **scope of stronger ordering**.

### Prediction 8

A cancellation flag is relaxed, while queue close under a mutex wakes waiters. Predict whether the flag must publish queue contents.

Record: **separate synchronization roles**.

## Part 2 — Diagnose and repair

Review a result slot with an ordinary `Option<Result>` and atomic `ready`. The producer writes the option through raw shared access and uses a relaxed ready store. The consumer uses a relaxed load, reads the option, then resets ready for reuse. There is no generation tag, and several producers may write.

Identify data-race/unsafe concerns, missing publication, multiple-writer violation, and ABA/reuse risk. First decide whether a mutex or one-shot channel is the correct architecture. If an atomic slot is genuinely required, restrict roles, use an initialization state machine, release/acquire publication, and a non-reused or versioned lifecycle.

### Weak repairs to reject

Reject each of these shortcuts and replace it with the smallest repair that preserves the product requirement:

- changing every ordering to `SeqCst` without repairing multiple writers or lifetime;
- using relaxed because the atomic value itself is observed correctly;
- reading several relaxed counters as one invariant-bearing snapshot;
- performing logging or allocation with external effects inside a retryable CAS closure;
- ignoring wraparound because it is unlikely;
- using atomics for a relation that is clearer under one mutex;

For every repair, identify which of the six review dimensions it restores: ownership, visibility, exclusion, progress, failure, or determinism. A repair that improves one dimension may damage another; record both effects.

## Part 3 — Focused exercises

### Construction 1

Derive orderings for one producer publishing a fixed payload to one consumer.

Required evidence: Name the release operation, acquire observation, and ordinary writes ordered by the edge.

### Construction 2

Implement a bounded quota reservation with `fetch_update`.

Required evidence: Reject insufficient quota, identify the linearization point, and keep the closure free of irreversible effects.

### Construction 3

Classify BatchWeave metrics as live advisory or final authoritative.

Required evidence: State allowed inconsistent snapshots and how final counts are reconstructed.

### Construction 4

Design an atomic phase machine for created, running, cancelling, and finished.

Required evidence: List legal transitions, CAS/store operations, orderings, and published data.

### Construction 5

Compare a mutex counter group with several relaxed atomics.

Required evidence: Choose based on whether snapshots must preserve a relation, not presumed speed.

### Interleaved reasoning pass

1. For **Separate atomicity of one location from visibility of other memory**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the happens-before graph.
2. For **Reason with sequenced-before, synchronizes-with, and happens-before relations**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the happens-before graph.
3. For **Use relaxed atomics for independent counters whose exact snapshots are advisory**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the happens-before graph.
4. For **Derive release/acquire publication when one atomic state makes ordinary writes visible**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the happens-before graph.

5. Identify one guarantee from an earlier course that a careless implementation of **Atomics, Happens-Before, and Memory Ordering** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Atomic Progress](../../labs/module-07-atomic-progress/README.md) from the starter. Before opening the solution, produce:

- an atomic state-machine ledger with legal transitions;
- a written happens-before graph for every publication edge;
- tests for failed and competing transitions;
- documentation of advisory snapshot inconsistencies;
- a wraparound or saturation policy for counters;

Your submission must also identify one schedule that the implementation handles correctly and one product claim it deliberately does not make.

### Laboratory acceptance trace

Before opening the reference implementation for **Atomic Progress**, record:

- the public behavior that demonstrates **Separate atomicity of one location from visibility of other memory**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Add BatchWeave live metrics: submitted, started, completed, failed, panicked, and cancelled. Use relaxed atomics only for independent telemetry. Do not use them to decide final success. Final authoritative counts come from the complete indexed outcome vector after all workers join. Add an atomic lifecycle state only if its transitions simplify cancellation observation; queue closure remains the wake mechanism.

Required capstone evidence:

- a classification of each metric as advisory or authoritative;
- tests showing final summaries derive from outcomes rather than live loads;
- an atomic transition ledger if a lifecycle atomic is used;
- a statement of saturation or overflow behavior;
- no unexplained `SeqCst` ordering;

Add at least one regression test that fails if this module's governing contract is removed. Tests that merely sleep and hope for a schedule do not count as causal evidence.

### Capstone invariant trace

For the Module 67 BatchWeave increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. What does atomicity guarantee for one location?
2. When does a release/acquire pair create a synchronizes-with edge?
3. Why can relaxed counters form an incoherent product snapshot?
4. What is the linearization point in a successful CAS loop?
5. What does sequential consistency still not repair?

### Independent transfer

Design a one-producer status publisher with immutable result data and states `EMPTY`, `WRITING`, `READY`, and `CONSUMED`. Write every ordinary access, atomic transition, ordering, and observed-value condition. Then add slot reuse and explain why a generation counter or different ownership protocol becomes necessary.

### Closed-book defense

In five minutes, answer “Which fact does an atomic operation publish, which earlier writes become visible because of it, and what is the weakest ordering that proves the required relationship?” using the **happens-before graph**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside BatchWeave. A list of APIs without the deciding relationship is incomplete.
