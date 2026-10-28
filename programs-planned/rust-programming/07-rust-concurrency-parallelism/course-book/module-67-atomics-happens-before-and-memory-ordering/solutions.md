# Reasoned solutions — Module 67: Atomics, Happens-Before, and Memory Ordering

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the BatchWeave guide](../capstone.md)

Atomic orderings are conclusions of a visibility proof. Strong answers name the ordinary data being published, the exact atomic value observed, and the transitive happens-before path. Counters that publish nothing should not inherit stronger ordering by superstition.

The answers below are reasoning models, not scripts to imitate. A different implementation can be stronger when it proves the same contract more directly. Compare ownership, synchronization, progress, failure, and determinism—not only surface syntax.

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
