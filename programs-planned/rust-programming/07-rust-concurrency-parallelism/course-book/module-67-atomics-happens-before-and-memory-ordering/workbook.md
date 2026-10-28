# Workbook — Module 67: Atomics, Happens-Before, and Memory Ordering

[Return to the chapter](index.md) · [Open the BatchWeave engineering guide](../capstone.md) · [Open solutions only after attempting the work](solutions.md)

This workbook tests whether the chapter has become an operational model. Freeze predictions, protocol diagrams, and invariants before compiling. Concurrency is unusually forgiving of explanations written after observing one successful run; that is exactly why the reasoning record must come first.

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

## Part 4 — Independent laboratory

Build [Atomic Progress](../../labs/module-07-atomic-progress/README.md) from the starter. Before opening the solution, produce:

- an atomic state-machine ledger with legal transitions;
- a written happens-before graph for every publication edge;
- tests for failed and competing transitions;
- documentation of advisory snapshot inconsistencies;
- a wraparound or saturation policy for counters;

Your submission must also identify one schedule that the implementation handles correctly and one product claim it deliberately does not make.

## Part 5 — Capstone transfer

Add BatchWeave live metrics: submitted, started, completed, failed, panicked, and cancelled. Use relaxed atomics only for independent telemetry. Do not use them to decide final success. Final authoritative counts come from the complete indexed outcome vector after all workers join. Add an atomic lifecycle state only if its transitions simplify cancellation observation; queue closure remains the wake mechanism.

Required capstone evidence:

- a classification of each metric as advisory or authoritative;
- tests showing final summaries derive from outcomes rather than live loads;
- an atomic transition ledger if a lifecycle atomic is used;
- a statement of saturation or overflow behavior;
- no unexplained `SeqCst` ordering;

Add at least one regression test that fails if this module's governing contract is removed. Tests that merely sleep and hope for a schedule do not count as causal evidence.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. What does atomicity guarantee for one location?
2. When does a release/acquire pair create a synchronizes-with edge?
3. Why can relaxed counters form an incoherent product snapshot?
4. What is the linearization point in a successful CAS loop?
5. What does sequential consistency still not repair?

### Independent transfer

Design a one-producer status publisher with immutable result data and states `EMPTY`, `WRITING`, `READY`, and `CONSUMED`. Write every ordinary access, atomic transition, ordering, and observed-value condition. Then add slot reuse and explain why a generation counter or different ownership protocol becomes necessary.
