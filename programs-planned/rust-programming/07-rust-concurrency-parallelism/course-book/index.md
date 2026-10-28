# Course 7 — Rust Concurrency and Parallelism

## Threads, Coordination, Atomics, and Deterministic Work Distribution

## The promise

Course 7 moves from single-threaded resource correctness to schedule-independent product reasoning. It covers thread transfer, scoped lifetimes, locks and invariants, condition predicates, message passing, liveness, atomics, one narrow lock-free proof, and deterministic parallel reduction.

> **Governing question:** Which facts remain true across every legal thread schedule, and what ownership, synchronization, progress, failure, and normalization arguments make those facts reviewable?

Course 6 established how to cross operating-system, allocator, ABI, and foreign-resource boundaries without losing ownership or cleanup. Course 7 adds legal schedule variation. The program must now preserve its claims across interleavings, contention, blocking, panic, cancellation, and nondeterministic completion order.

## Before Day 1

You should be able to audit ownership, unsafe boundaries, cleanup, representation, and system calls, and to distinguish semantic state from observational or platform-dependent facts.

From a blank page, sketch one earlier product or a comparable program. Mark an owner, a valid and invalid state, a failure path, cleanup, and a public promise. Repair any relationship you cannot explain before adding this course’s mechanisms.

## Outcomes

- Distinguish concurrency, parallelism, scheduling, interleaving, data races, and broader race conditions.
- Explain the real meaning of a `T: 'static` bound and why owned values can satisfy it.
- Name the state invariant protected by each `Mutex` or `RwLock` rather than treating the primitive as a generic thread-safety wrapper.
- Write every condition-variable wait as a predicate loop over mutex-protected state.
- Model channel operations as ownership transfer rather than shared access.
- Distinguish deadlock, starvation, livelock, priority inversion, and slow work.
- Separate atomicity of one location from visibility of other memory.
- Distinguish obstruction-free, lock-free, and wait-free progress claims from ordinary nonblocking API behavior.
- Distinguish task parallelism, data parallelism, and a long-lived message-driven worker service.
- Construct one architecture diagram connecting coordinator, queue, workers, result channel, metrics, report pool, and CLI boundaries.
- Integrate all ten mechanisms in BatchWeave without creating competing authorities.
- Complete and defend an unseen change using a concurrent architecture dossier.

## The ten-day line

| Day | Module | Governing question | Capability that must become visible | Laboratory |
|---:|---|---|---|---|
| 1 | [61 — Threads, Schedules, Send, Sync, and Race Freedom](./module-61-threads-schedules-send-sync-and-race-freedom/index.md) | What may cross a thread boundary, what may be shared through a reference, and which correctness problems remain after Rust has ruled out data races? | **Distinguish concurrency, parallelism, scheduling, interleaving, data races, and broader race conditions.** | [Thread Handoff Matrix](../labs/module-01-thread-handoff-matrix/README.md) |
| 2 | [62 — Structured Threads: Scopes, Joins, and Panic Boundaries](./module-62-structured-threads-scopes-joins-and-panic-boundaries/index.md) | How can borrowed data, thread lifetime, completion, and panic handling be enclosed by one parent operation rather than leaked into the rest of the program? | **Explain the real meaning of a `T: 'static` bound and why owned values can satisfy it.** | [Scoped Slice Analysis](../labs/module-02-scoped-slice-analysis/README.md) |
| 3 | [63 — Shared State: Locks and Protected Invariants](./module-63-shared-state-locks-and-protected-invariants/index.md) | Which exact invariant does a lock protect, how small can the protected transition be, and what state remains valid after contention or panic? | **Name the state invariant protected by each `Mutex` or `RwLock` rather than treating the primitive as a generic thread-safety wrapper.** | [Protected Inventory](../labs/module-03-protected-inventory/README.md) |
| 4 | [64 — Coordination: Condvars, Barriers, and Phase Protocols](./module-64-coordination-condvars-barriers-and-phase-protocols/index.md) | How do threads wait for a state predicate or phase transition without polling, lost wakeups, or treating notification itself as truth? | **Write every condition-variable wait as a predicate loop over mutex-protected state.** | [Phase Gate](../labs/module-04-phase-gate/README.md) |
| 5 | [65 — Message Passing, Backpressure, and Shutdown](./module-65-message-passing-backpressure-and-shutdown/index.md) | Which values cross ownership boundaries, how is capacity bounded, and which explicit protocol event proves that every sender, receiver, and worker can terminate? | **Model channel operations as ownership transfer rather than shared access.** | [Bounded Map Pipeline](../labs/module-05-bounded-map-pipeline/README.md) |
| 6 | [66 — Liveness: Deadlock, Cancellation, and Recovery](./module-66-liveness-deadlock-cancellation-and-recovery/index.md) | Why can every blocked operation eventually continue or terminate, and what happens when cancellation, panic, or partial infrastructure failure interrupts the normal path? | **Distinguish deadlock, starvation, livelock, priority inversion, and slow work.** | [Cancellable Worker Group](../labs/module-06-cancellable-worker-group/README.md) |
| 7 | [67 — Atomics, Happens-Before, and Memory Ordering](./module-67-atomics-happens-before-and-memory-ordering/index.md) | Which fact does an atomic operation publish, which earlier writes become visible because of it, and what is the weakest ordering that proves the required relationship? | **Separate atomicity of one location from visibility of other memory.** | [Atomic Progress](../labs/module-07-atomic-progress/README.md) |
| 8 | [68 — Lock-Free Protocols, Reclamation, and Unsafe Send/Sync](./module-68-lock-free-protocols-reclamation-and-unsafe-send-sync/index.md) | What proof permits shared raw storage to be accessed without a lock, and where do role confusion, ABA, destruction, or memory reclamation invalidate a locally plausible algorithm? | **Distinguish obstruction-free, lock-free, and wait-free progress claims from ordinary nonblocking API behavior.** | [Bounded SPSC Ring](../labs/module-08-spsc-ring/README.md) |
| 9 | [69 — Rayon, Work Stealing, and Deterministic Parallelism](./module-69-rayon-work-stealing-and-deterministic-parallelism/index.md) | How can divisible computation use a work-stealing pool while preserving item meaning, reduction laws, failure policy, result ordering, and a defensible cost model? | **Distinguish task parallelism, data parallelism, and a long-lived message-driven worker service.** | [Parallel Histogram](../labs/module-09-parallel-histogram/README.md) |
| 10 | [70 — Integrated Concurrent Architecture, Testing, and Audit](./module-70-integrated-concurrent-architecture-testing-and-audit/index.md) | How do ownership, bounded work, synchronization, liveness, panic, cancellation, atomics, deterministic reporting, and test evidence become one product whose strongest claims are reviewable? | **Construct one architecture diagram connecting coordinator, queue, workers, result channel, metrics, report pool, and CLI boundaries.** | [Concurrent Verifier](../labs/module-10-concurrent-verifier/README.md) |

The table is a dependency chain, not a menu. A later module may use an earlier mechanism but may not silently weaken its ownership, failure, ordering, capacity, safety, compatibility, or evidence contract.

## Decision rules

| Decision | Rule used throughout this course |
|---|---|
| Shared invariant | One lock protects one named invariant; do not hold it through unrelated effects. |
| Waiting | Wait in a predicate loop and include cancellation or terminal state in the predicate. |
| Backpressure | Bound every queue and name the authority that accepts or rejects work. |
| Atomic ordering | Derive ordering from the visibility edge and linearization point, not from a stronger-ordering reflex. |
| Determinism | Normalize final meaning separately from schedule-dependent completion order. |

Use these rules during prediction and review. When a rule does not decide the case, write the missing product requirement instead of selecting an API by habit.

## The reasoning record

The ten module-specific records culminate in a **concurrent architecture dossier**. Map owners, protected invariants, waits, visibility edges, terminal events, bounds, and deterministic reconstruction across every legal schedule. Keep the record small enough to inspect but complete enough to expose the first unsupported assumption.

## Scope and handoff

The course uses operating-system threads and Rayon. Async runtimes, sockets, network protocols, and async cancellation remain Course 8 topics. Lock-free code is taught as a proof exercise, not as a default replacement for locks and channels.

Course 8 replaces blocking thread stacks with suspended futures and adds network peers, byte-stream framing, protocol state, deadlines, retries, and graceful service shutdown.

## Capstone — BatchWeave

BatchWeave runs a bounded manifest through a fixed worker group, records one terminal outcome for every accepted job, contains panic and cancellation, uses advisory atomics honestly, and renders final results in source order.

Open the [engineering guide](capstone.md) before Day 1 so the final architecture is visible. Implement only the current increment. The independent laboratory remains separate so that the mechanism can be learned without hiding behind accumulated capstone code.

## Completion

The course is complete when you can build and defend:

> Build a bounded concurrent verifier with a fixed worker group, explicit failure policy, cancellation, panic containment, complete join accounting, and deterministic final reconstruction.

and then change the capstone under this constraint:

> Add bounded retry to BatchWeave while preserving one terminal outcome per source job, fail-fast semantics, queue bounds, and deterministic final reporting.

A passing test suite is necessary. It is not sufficient unless you can explain why the tests are capable of falsifying the claim and which target-, scheduler-, workload-, peer-, or policy-dependent facts remain outside them.

## Continue

- [Ten-day plan](study-plan.md)
- [Module 61 — Threads, Schedules, Send, Sync, and Race Freedom](./module-61-threads-schedules-send-sync-and-race-freedom/index.md)
- [BatchWeave engineering guide](capstone.md)
- [Course reference](reference.md)
- [Final review](final-review.md)
- [Compiler and design investigations](../compiler-labs/README.md)
- [Independent laboratories](../labs/)
