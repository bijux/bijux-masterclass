# Reasoned Solutions — Module 67: Atomics, Happens-Before, and Memory Ordering

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-07-atomic-progress/README.md) · [BatchWeave guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 67: Atomics, Happens-Before, and Memory Ordering**. Compare the reasoning against this question: *Which fact does an atomic operation publish, which earlier writes become visible because of it, and what is the weakest ordering that proves the required relationship?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Prediction solutions

### Prediction 1

The consumer has no synchronizes-with edge for the ordinary payload. Store ready with `Release` after initialization and load with `Acquire`; read payload only when that acquire observes the published ready value.

### Prediction 2

It orders only the counter’s own atomic modification order. It does not make job data visible or act as a completion barrier.

### Prediction 3

No. Each load is individually atomic, but the pair may combine observations from different moments. Protect the relation or treat the snapshot as advisory.

### Prediction 4

Failure performs no write, so `Release` is invalid as a failure ordering. Use `Relaxed` or `Acquire` according to what the observed current value must publish.

### Prediction 5

`fetch_update` may invoke the closure repeatedly under contention, duplicating the log. Return only the proposed value from the closure and perform effects once after successful update.

### Prediction 6

Only that the current bits equal 7. It does not prove the location was unchanged. Add a version tag or use a protocol that does not rely on unchanged history.

### Prediction 7

Data races through non-atomic memory, deadlocks, lost wakeups, unbounded queues, logical race conditions, and lifecycle defects remain. SeqCst strengthens atomic order only.

### Prediction 8

No. Queue mutex/condition-variable operations carry queue visibility and wakeup. The relaxed flag communicates only cancellation state and must not be used to infer other memory.

## Part 2 — Repair reasoning

The first repair is architectural: a mutex or one-shot channel likely expresses result ownership better. A raw shared `Option` with multiple producers is not saved by orderings. For a true one-producer slot, use fixed role ownership, `UnsafeCell<MaybeUninit<T>>`, one publication state, release/acquire, no concurrent reset, and a drop/reuse protocol. That proof belongs in an unsafe abstraction like Module 68’s queue, not ordinary application code.

## Part 3 — Focused construction guidance

### Construction 1

Producer initializes all payload fields then performs a release state store. Consumer acquire-loads that state and, only after observing ready, reads payload. Program order plus synchronizes-with gives happens-before.

### Construction 2

`fetch_update(Relaxed, Relaxed, |current| current.checked_sub(amount))` is enough when quota publishes no other data. Success of the RMW is the reservation linearization point; log afterward once.

### Construction 3

All live atomics are advisory. Final report counts scan the unique outcome slots after joins. The documentation allows transient cross-counter inconsistencies.

### Construction 4

Use monotonic legal transitions, compare-exchange where competing initiators exist, and release/acquire only when a state publishes related data. Cancellation state alone can be relaxed when queue close carries synchronization.

### Construction 5

A mutex is appropriate when the snapshot relation matters. Independent atomics are appropriate for approximate telemetry. Performance is measured later, not assumed.

## Part 4 — Laboratory comparison

Compare the written ordering proof before syntax. The solution should use the weakest justified ordering, reject illegal transitions, and document snapshots that are not coherent. A `SeqCst` blanket is not a superior answer unless the state machine truly needs a global order.

## Part 5 — Capstone comparison

BatchWeave’s final report must ignore live metric races and count the authoritative outcome vector. Relaxed counters are useful for progress display and tests of monotonic individual values. Queue closure and joins, not metric loads, prove completion.

## Part 6 — Reconstruction and defense

A complete defense identifies atomicity, publication, and product invariants separately. It can draw the release/acquire edge, state CAS linearization and failure ordering, and explain why relaxed telemetry is honest. It also names ABA and overflow assumptions rather than relying on practical improbability.

A strong defense states what is guaranteed for every allowed schedule, what is merely likely on one machine, and what the design intentionally leaves unspecified.

## Deep reasoning and transfer

### Decisive model

> Which fact does an atomic operation publish, which earlier writes become visible because of it, and what is the weakest ordering that proves the required relationship?

Build a **happens-before graph**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Separate atomicity of one location from visibility of other memory.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Reason with sequenced-before, synchronizes-with, and happens-before relations.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Use relaxed atomics for independent counters whose exact snapshots are advisory.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Derive release/acquire publication when one atomic state makes ordinary writes visible.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Select valid success and failure orderings for compare-exchange loops.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Separate atomicity of one location from visibility of other memory.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the happens-before graph.

### Reference implementation comparison

For [Atomic Progress](../../labs/module-07-atomic-progress/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In BatchWeave, Module 67 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Atomics, Happens-Before, and Memory Ordering**, which relationship decides this question: “Which fact does an atomic operation publish, which earlier writes become visible because of it, and what is the weakest ordering that proves the required relationship?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to BatchWeave?
