# Reasoned Solutions — Module 66: Liveness: Deadlock, Cancellation, and Recovery

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-06-cancellable-worker-group/README.md) · [BatchWeave guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 66: Liveness: Deadlock, Cancellation, and Recovery**. Compare the reasoning against this question: *Why can every blocked operation eventually continue or terminate, and what happens when cancellation, panic, or partial infrastructure failure interrupts the normal path?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Prediction solutions

### Prediction 1

Workers can remain blocked forever. Add cancellation to the durable predicate and notify all waiters when the flag/state changes, or close the queue as the wake-carrying state transition.

### Prediction 2

T1 owns A and waits for B; T2 owns B and waits for A. Enforce one global order or redesign so operations do not hold both.

### Prediction 3

One thread can starve, and several can livelock under synchronized retry behavior. Use bounded backoff, queueing, or a simpler lock-based protocol unless lock-free progress is required and proved.

### Prediction 4

The coordinator can wait forever for a message that cannot arrive. Drain until sender disconnect, join workers, and reconcile missing indexed jobs; or send a worker-fault event from an outer panic boundary.

### Prediction 5

A failed push must return the job to the coordinator. It becomes an explicit cancelled/not-submitted outcome rather than disappearing.

### Prediction 6

Queue state may be poisoned or partially transitioned if panic is caught too broadly. Catch around user job execution after pop and outside queue locks.

### Prediction 7

Idempotence lets both paths request cancellation/closure safely without double-joining or inconsistent lifecycle state. One coordinator still owns handle consumption.

### Prediction 8

The timeout bounds the test process but does not establish a production deadlock or intended schedule. Use causal handshakes and inspect the protocol; keep timeout only as a test harness guard.

## Part 2 — Repair reasoning

Remove the shutdown barrier because participant failure invalidates its fixed-cohort premise. Define one lock order or, preferably, release locks before bounded sends. Cancellation transitions durable queue state to closed and notifies both waiter classes. Result collection ends when all worker senders drop; then every worker is joined and source-index reconciliation labels missing work.

This repair eliminates several dependencies rather than adding retries. The resulting termination proof is finite and identity-based.

## Part 3 — Focused construction guidance

### Construction 1

Include thread-to-lock edges, lock ownership edges, sender-to-capacity edges, and capacity-to-receiver edges. A cycle demonstrates a reachable deadlock when all annotated states coexist.

### Construction 2

The protected predicate becomes `work_available || cancelled || closed`. Cancellation changes state while locked and calls `notify_all`; the waiter loops and returns a terminal result.

### Construction 3

Lifecycle transitions move monotonically from running to cancelling/closed to joined. Close and cancel are repeatable; join is owned and performed once; repeated public shutdown returns the recorded final status.

### Construction 4

Catch only the operation call. Send `Panicked { index }`, request cancellation if policy requires, and keep worker reusable only when no mutable worker-local invariant was exposed. Reconcile if result send fails.

### Construction 5

Finite accepted jobs, close-woken queue operations, one terminal path per popped job, finite sender owners, and complete joins imply termination. Jobs rejected by closed push remain coordinator-owned and are labelled.

## Part 4 — Laboratory comparison

Inspect the wake path before happy-path output. The solution should demonstrate cancellation of blocked operations without sleeps, join all workers after panic, and reconcile indexed work. A design that merely exits quickly while losing jobs is not equivalent.

## Part 5 — Capstone comparison

BatchWeave should now survive the first domain failure, explicit cancellation, result-receiver loss, and worker panic without hanging. The queue’s close operation carries wakeup; the relaxed flag is only an observation. Final outcome assembly is authoritative, while live metrics remain advisory.

## Part 6 — Reconstruction and defense

The defense must show a wait-for graph, the state/wake/checkpoint cancellation triad, a narrow panic boundary, and a finite terminal-accounting proof. It should not claim fairness, instantaneous cancellation, or recovery from process abort.

A strong defense states what is guaranteed for every allowed schedule, what is merely likely on one machine, and what the design intentionally leaves unspecified.

## Deep reasoning and transfer

### Decisive model

> Why can every blocked operation eventually continue or terminate, and what happens when cancellation, panic, or partial infrastructure failure interrupts the normal path?

Build a **wait-for and shutdown graph**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Distinguish deadlock, starvation, livelock, priority inversion, and slow work.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Construct a wait-for graph over locks, channels, joins, barriers, and conditions.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **State a global lock order and identify operations that violate it.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Design cancellation as state plus a wake mechanism plus an observation point.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Make shutdown idempotent and safe under concurrent callers.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Distinguish deadlock, starvation, livelock, priority inversion, and slow work.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the wait-for and shutdown graph.

### Reference implementation comparison

For [Cancellable Worker Group](../../labs/module-06-cancellable-worker-group/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In BatchWeave, Module 66 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Liveness: Deadlock, Cancellation, and Recovery**, which relationship decides this question: “Why can every blocked operation eventually continue or terminate, and what happens when cancellation, panic, or partial infrastructure failure interrupts the normal path?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to BatchWeave?
