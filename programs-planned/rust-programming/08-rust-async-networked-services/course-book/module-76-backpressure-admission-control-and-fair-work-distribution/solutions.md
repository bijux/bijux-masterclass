# Reasoned Solutions — Module 76: Backpressure, Admission Control, and Fair Work Distribution

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-06-bounded-relay-broker/README.md) · [JobWire guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 76: Backpressure, Admission Control, and Fair Work Distribution**. Compare the reasoning against this question: *When demand exceeds service capacity, where may work wait, which bound is authoritative, and how does overload become an explicit product outcome instead of memory growth, latency collapse, or starvation?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Prediction solutions

1. No. The semaphore bounds execution, while waiting task count and captured request memory remain unbounded.
2. At least the broker capacity plus the per-connection retained requests, subject to which sends have entered the channel. The service must count all layers.
3. Status, cancellation, duplicate-key lookup, shutdown, and new admission can all block behind capacity acquisition.
4. Compute capacity has become coupled to network consumption. Slow clients reduce job throughput.
5. A synchronized retry wave or thundering herd can occur. Clients need jitter and an overall deadline.
6. Tenant-level domination remains. Connection limits are not identity or tenant quotas.
7. No. Queueing delay may already violate deadlines and small bursts may trigger rejection. Sustained high occupancy is an overload signal.
8. Kernel and runtime buffers may retain substantial data, and flow control does not bound decoded requests, tasks, or application state.

## Part 2 — Repair reasoning

The repaired design limits accepted connections, stops each V1 connection at one in-flight request, uses a bounded broker mailbox, keeps waiting jobs in one bounded scheduler rather than one task each, limits active work, stores only bounded results, and gives writers deadlines. Admission before broker commit can return `BUSY`; after commit, idempotency recovers the outcome.

## Part 3 — Focused exercise guidance

The envelope should state assumptions and overhead exclusions. A useful conservative payload calculation sums per-connection frame/request retention, queued requests, active job inputs and results, and idempotency records. It should not claim exact heap usage.

A fair scheduler needs explicit tenant identity and queue ownership. Round-robin can prevent queue monopolization but does not equalize job cost unless weights or cost classes are added. Saturation tests should hold tasks with notifications, not rely on long sleeps.

## Part 4 — Laboratory comparison

A strong broker preserves responsiveness while work runs. It owns a finite waiting structure, classifies job panic, and releases active permits before waiting on slow reply consumers. Every accepted request gets one terminal reply or a documented cancellation outcome.

## Part 5 — Capstone comparison

JobWire’s broker is state authority. It should record the idempotency entry at commit, schedule bounded work, and cache a bounded terminal result. Connection writers observe results but do not retain compute permits. `STATS` reads a snapshot or uses a priority control path rather than waiting behind saturated work.

## Part 6 — Reconstruction and defense

A complete defense names every accumulation point, its unit, maximum, owner, and saturation behavior. It distinguishes stored latency from active work, commit from admission, transport flow control from application bounds, and fairness policy from primitive implementation details.

## Deep reasoning and transfer

### Decisive model

> When demand exceeds service capacity, where may work wait, which bound is authoritative, and how does overload become an explicit product outcome instead of memory growth, latency collapse, or starvation?

Build a **capacity and admission ledger**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Find every accumulation point in an async service.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Distinguish connection admission, queue capacity, active-work permits, response buffering, and retry budgets.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Choose between waiting, rejecting, shedding, degrading, and disconnecting under overload.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Acquire permits before irreversible commitment.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Use bounded `mpsc`, semaphores, and actor ownership without assuming they imply fairness.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Find every accumulation point in an async service.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the capacity and admission ledger.

### Reference implementation comparison

For [Bounded Relay Broker](../../labs/module-06-bounded-relay-broker/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In JobWire, Module 76 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Backpressure, Admission Control, and Fair Work Distribution**, which relationship decides this question: “When demand exceeds service capacity, where may work wait, which bound is authoritative, and how does overload become an explicit product outcome instead of memory growth, latency collapse, or starvation?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to JobWire?
