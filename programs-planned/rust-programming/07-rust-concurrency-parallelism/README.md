# Rust Concurrency and Parallelism

## Threads, Coordination, Atomics, and Work Distribution

This is Course 7 of the Rust Programming path and covers Modules 61–70. The first six courses established typed program construction, ownership and memory, architectural contracts, explicit dataflow, compile-time authority, and systems boundaries. This course asks what remains true when several execution agents may advance at once.

Concurrency is not introduced as a bag of synchronization primitives. Every design is reviewed through seven questions:

1. **Ownership:** which thread owns each value, endpoint, handle, and cleanup obligation?
2. **Visibility:** which operation makes one thread's writes observable to another?
3. **Atomicity and exclusion:** which facts form one indivisible transition, and which states must never be observed simultaneously?
4. **Progress:** what can each operation wait for, and which event lets it continue or terminate?
5. **Failure:** what happens after domain error, panic, disconnect, poison, cancellation, or thread-spawn failure?
6. **Determinism:** which outputs must be schedule-independent, and which timing facts remain intentionally unspecified?
7. **Resources:** what bounds threads, queued work, active work, retained results, payloads, and auxiliary pools?

The course book is the primary product. Each chapter teaches one reasoning model in depth. Workbooks expose whether that model is operational. Labs isolate one mechanism. The cumulative capstone, **BatchWeave**, forces those mechanisms to coexist in one bounded and deterministic batch engine.

## Prerequisites

Begin only after you can:

- move and borrow values deliberately;
- explain `Send`, `Sync`, `Arc`, `Mutex`, and atomics at an introductory level;
- design RAII cleanup and panic-safe state transitions;
- review unsafe code through explicit invariants;
- use traits, iterators, channels, tests, and Cargo workspaces;
- distinguish language guarantees from implementation observations.

The [course overview](course-book/index.md) includes a readiness check and repair route.

## Ten modules

61. [Threads, Schedules, Send, Sync, and Race Freedom](course-book/module-61-threads-schedules-send-sync-and-race-freedom/index.md) — What may move or be shared between threads, and which correctness properties remain unprotected after data races are ruled out?
62. [Structured Threads: Scopes, Joins, and Panic Boundaries](course-book/module-62-structured-threads-scopes-joins-and-panic-boundaries/index.md) — How can thread lifetime, borrowed data, completion, and panic handling be bounded by one parent operation?
63. [Shared State: Locks and Protected Invariants](course-book/module-63-shared-state-locks-and-protected-invariants/index.md) — Which invariant does each lock protect, how small can guard scope be, and what state is valid after panic or recovery?
64. [Coordination: Condvars, Barriers, and Phase Protocols](course-book/module-64-coordination-condvars-barriers-and-phase-protocols/index.md) — How do threads wait for conditions and phases without polling, lost wakeups, or confusing notification with truth?
65. [Message Passing, Backpressure, and Shutdown](course-book/module-65-message-passing-backpressure-and-shutdown/index.md) — Which values cross ownership boundaries, how is capacity bounded, and what exact event ends the protocol?
66. [Liveness: Deadlock, Cancellation, and Recovery](course-book/module-66-liveness-deadlock-cancellation-and-recovery/index.md) — How can a concurrent system make progress and terminate when locks, workers, panics, cancellation, or partial failure interact?
67. [Atomics, Happens-Before, and Memory Ordering](course-book/module-67-atomics-happens-before-and-memory-ordering/index.md) — Which facts become visible because of an atomic operation, and what is the weakest ordering that proves that relationship?
68. [Lock-Free Protocols, Reclamation, and Unsafe Send/Sync](course-book/module-68-lock-free-protocols-reclamation-and-unsafe-send-sync/index.md) — What proof turns unsynchronized-looking shared storage into a sound concurrent abstraction, and where do ABA and reclamation defeat naive designs?
69. [Rayon, Work Stealing, and Deterministic Parallelism](course-book/module-69-rayon-work-stealing-and-deterministic-parallelism/index.md) — How can partitionable computation use many cores while preserving result meaning, associativity, ordering requirements, and bounded overhead?
70. [Integrated Concurrent Architecture, Testing, and Audit](course-book/module-70-integrated-concurrent-architecture-testing-and-audit/index.md) — How do bounded work, failure, cancellation, metrics, deterministic output, and testing form one reviewable concurrent product?


## Course rhythm

One module is one dense day:

```text
chapter → frozen predictions → diagnosis → focused construction
        → independent lab → BatchWeave increment → explanation
```

Do not read a reference solution before your own design is recorded. Concurrent code often has many implementations that pass ordinary tests but differ sharply in liveness, backpressure, panic behavior, or schedule dependence. Your written protocol is part of the engineering evidence.

## Main dependency policy

The standard library owns the instructional core through Modules 61–68 and 70. Module 69 and the BatchWeave reporting stage use exactly pinned `rayon = 1.12.0` to study data parallelism and work stealing. The course does not use an async runtime, a networking framework, or a third-party channel library; those would blur the boundary with Course 8.

## Commands

```bash
make audit
make compiler-labs
make check
make test
make starters
make fmt
make clippy
make docs
make proof
```

[Open the course book](course-book/index.md) · [Open the ten-day plan](course-book/study-plan.md) · [Open BatchWeave](course-book/capstone.md) · [Return to the program](../README.md)
