# Course 7 — Rust Concurrency and Parallelism

## Threads, Coordination, Atomics, and Deterministic Work Distribution

Course 7 moves from single-threaded resource correctness to schedule-independent product reasoning. It covers thread transfer, scoped lifetimes, locks and invariants, condition predicates, message passing, liveness, atomics, one narrow lock-free proof, and deterministic parallel reduction.

> **Governing question:** Which facts remain true across every legal thread schedule, and what ownership, synchronization, progress, failure, and normalization arguments make those facts reviewable?

## Entry point

You should be able to audit ownership, unsafe boundaries, cleanup, representation, and system calls, and to distinguish semantic state from observational or platform-dependent facts.

The immediate prerequisite is [Course 6: Rust Systems Programming](../06-rust-systems-programming/course-book/index.md). Entering mid-program is reasonable only when you can complete the previous course’s final review and one independent construction without following its solution.

## Ten-day route

| Day | Module | Capability added | Independent laboratory |
|---:|---|---|---|
| 1 | [61 — Threads, Schedules, Send, Sync, and Race Freedom](course-book/module-61-threads-schedules-send-sync-and-race-freedom/index.md) | Distinguish concurrency, parallelism, scheduling, interleaving, data races, and broader race conditions | [Thread Handoff Matrix](labs/module-01-thread-handoff-matrix/README.md) |
| 2 | [62 — Structured Threads: Scopes, Joins, and Panic Boundaries](course-book/module-62-structured-threads-scopes-joins-and-panic-boundaries/index.md) | Explain the real meaning of a `T: 'static` bound and why owned values can satisfy it | [Scoped Slice Analysis](labs/module-02-scoped-slice-analysis/README.md) |
| 3 | [63 — Shared State: Locks and Protected Invariants](course-book/module-63-shared-state-locks-and-protected-invariants/index.md) | Name the state invariant protected by each `Mutex` or `RwLock` rather than treating the primitive as a generic thread-safety wrapper | [Protected Inventory](labs/module-03-protected-inventory/README.md) |
| 4 | [64 — Coordination: Condvars, Barriers, and Phase Protocols](course-book/module-64-coordination-condvars-barriers-and-phase-protocols/index.md) | Write every condition-variable wait as a predicate loop over mutex-protected state | [Phase Gate](labs/module-04-phase-gate/README.md) |
| 5 | [65 — Message Passing, Backpressure, and Shutdown](course-book/module-65-message-passing-backpressure-and-shutdown/index.md) | Model channel operations as ownership transfer rather than shared access | [Bounded Map Pipeline](labs/module-05-bounded-map-pipeline/README.md) |
| 6 | [66 — Liveness: Deadlock, Cancellation, and Recovery](course-book/module-66-liveness-deadlock-cancellation-and-recovery/index.md) | Distinguish deadlock, starvation, livelock, priority inversion, and slow work | [Cancellable Worker Group](labs/module-06-cancellable-worker-group/README.md) |
| 7 | [67 — Atomics, Happens-Before, and Memory Ordering](course-book/module-67-atomics-happens-before-and-memory-ordering/index.md) | Separate atomicity of one location from visibility of other memory | [Atomic Progress](labs/module-07-atomic-progress/README.md) |
| 8 | [68 — Lock-Free Protocols, Reclamation, and Unsafe Send/Sync](course-book/module-68-lock-free-protocols-reclamation-and-unsafe-send-sync/index.md) | Distinguish obstruction-free, lock-free, and wait-free progress claims from ordinary nonblocking API behavior | [Bounded SPSC Ring](labs/module-08-spsc-ring/README.md) |
| 9 | [69 — Rayon, Work Stealing, and Deterministic Parallelism](course-book/module-69-rayon-work-stealing-and-deterministic-parallelism/index.md) | Distinguish task parallelism, data parallelism, and a long-lived message-driven worker service | [Parallel Histogram](labs/module-09-parallel-histogram/README.md) |
| 10 | [70 — Integrated Concurrent Architecture, Testing, and Audit](course-book/module-70-integrated-concurrent-architecture-testing-and-audit/index.md) | Construct one architecture diagram connecting coordinator, queue, workers, result channel, metrics, report pool, and CLI boundaries | [Concurrent Verifier](labs/module-10-concurrent-verifier/README.md) |

The route is cumulative. Day 1 establishes this course’s vocabulary and Day 10 requires an architectural change that preserves all earlier guarantees.

## Working method

Map owners, protected invariants, waits, visibility edges, terminal events, bounds, and deterministic reconstruction across every legal schedule. Use the module-specific reasoning record named in each chapter. Freeze predictions before compiling, preserve causal diagnostics, and compare the lab reference only after recording your own design.

## Capstone — BatchWeave

BatchWeave runs a bounded manifest through a fixed worker group, records one terminal outcome for every accepted job, contains panic and cancellation, uses advisory atomics honestly, and renders final results in source order.

The [engineering guide](course-book/capstone.md) supplies the ten integration steps. The executable [capstone directory](capstone/README.md) contains the product and tests. Each increment must name the changed invariant, the component that owns it, state after failure, and the earlier guarantee that must remain unchanged.

## Scope

The course uses operating-system threads and Rayon. Async runtimes, sockets, network protocols, and async cancellation remain Course 8 topics. Lock-free code is taught as a proof exercise, not as a default replacement for locks and channels.

Course 8 replaces blocking thread stacks with suspended futures and adds network peers, byte-stream framing, protocol state, deadlines, retries, and graceful service shutdown.

## Exit standard

Complete this independent construction:

> Build a bounded concurrent verifier with a fixed worker group, explicit failure policy, cancellation, panic containment, complete join accounting, and deterministic final reconstruction.

Then complete this capstone extension:

> Add bounded retry to BatchWeave while preserving one terminal outcome per source job, fail-fast semantics, queue bounds, and deterministic final reporting.

The next step is [Course 8: Rust Async and Networked Services](../08-rust-async-networked-services/course-book/index.md).

## Reading and execution routes

- [Course book](course-book/index.md)
- [Ten-day study plan](course-book/study-plan.md)
- [Course reference](course-book/reference.md)
- [Final review](course-book/final-review.md)
- [Compiler and design investigations](compiler-labs/README.md)
- [Laboratories](labs/)

```bash
make static-proof
make compiler-labs
make check
make test
make starters
make docs
make proof
```

Static inspection and compilation answer different questions. The strongest completion route uses the pinned toolchain, executes tests and investigations, renders the book, and preserves the resulting evidence with the code under review.
