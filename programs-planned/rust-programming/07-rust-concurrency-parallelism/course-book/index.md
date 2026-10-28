# Rust Concurrency and Parallelism

## Course purpose

A sequential Rust program has one visible execution order. A concurrent program has many possible schedules, and correctness must survive all schedules allowed by its protocol. Rust prevents data races in safe code, but it does not prevent deadlock, starvation, stale product assumptions, unbounded queues, incomplete shutdown, nondeterministic output, or a compare-exchange loop whose ordering argument is wrong. This course develops the models needed to reason about those failures before they appear under production load.

The course begins with ordinary threads and auto traits because ownership is the first concurrency boundary. It then adds structure, shared-state protection, waiting protocols, and ownership-transferring channels. Only after those mechanisms are reviewable does it examine liveness and atomics. A bounded lock-free queue is studied as a proof exercise, not a default architecture. Rayon appears near the end, after the reader can distinguish task scheduling from semantic reduction. The final module integrates the complete product.

## What you will be able to do

- distinguish concurrency from parallelism, data races from broader race conditions, and safety from determinism;
- derive whether a type may cross a thread boundary or be shared by reference from its `Send` and `Sync` obligations;
- use owned threads and scoped threads without manufacturing `'static` lifetimes or hiding completion;
- make every spawned thread part of an explicit join, cancellation, or ownership protocol;
- protect named state invariants with `Mutex` or `RwLock` and keep guard scope smaller than effect scope;
- use condition variables, barriers, and one-time initialization as state protocols rather than notification tricks;
- design bounded channels and queues whose capacity, ownership transfer, backpressure, and shutdown events are explicit;
- analyze lock ordering, wait-for graphs, starvation, poisoning, panic containment, and termination;
- derive atomic orderings from a happens-before argument and separate numeric atomicity from publication;
- review compare-exchange loops, spurious failure, ABA exposure, and memory-reclamation requirements;
- construct one bounded SPSC queue whose unsafe `Send` and `Sync` implementations are justified by a written safety proof;
- use Rayon parallel iterators, `join`, scopes, and custom pools without assuming sequential side-effect order;
- state and test associativity, identity, ordering, and determinism requirements for parallel reductions;
- build a bounded worker engine with deterministic result assembly, cancellation, panic handling, and honest metrics;
- audit a concurrent product through ownership, synchronization, liveness, failure, and performance-boundary ledgers.

## The ten-day path

1. [Threads, Schedules, Send, Sync, and Race Freedom](module-61-threads-schedules-send-sync-and-race-freedom/index.md) — What may move or be shared between threads, and which correctness properties remain unprotected after data races are ruled out?
2. [Structured Threads: Scopes, Joins, and Panic Boundaries](module-62-structured-threads-scopes-joins-and-panic-boundaries/index.md) — How can thread lifetime, borrowed data, completion, and panic handling be bounded by one parent operation?
3. [Shared State: Locks and Protected Invariants](module-63-shared-state-locks-and-protected-invariants/index.md) — Which invariant does each lock protect, how small can guard scope be, and what state is valid after panic or recovery?
4. [Coordination: Condvars, Barriers, and Phase Protocols](module-64-coordination-condvars-barriers-and-phase-protocols/index.md) — How do threads wait for conditions and phases without polling, lost wakeups, or confusing notification with truth?
5. [Message Passing, Backpressure, and Shutdown](module-65-message-passing-backpressure-and-shutdown/index.md) — Which values cross ownership boundaries, how is capacity bounded, and what exact event ends the protocol?
6. [Liveness: Deadlock, Cancellation, and Recovery](module-66-liveness-deadlock-cancellation-and-recovery/index.md) — How can a concurrent system make progress and terminate when locks, workers, panics, cancellation, or partial failure interact?
7. [Atomics, Happens-Before, and Memory Ordering](module-67-atomics-happens-before-and-memory-ordering/index.md) — Which facts become visible because of an atomic operation, and what is the weakest ordering that proves that relationship?
8. [Lock-Free Protocols, Reclamation, and Unsafe Send/Sync](module-68-lock-free-protocols-reclamation-and-unsafe-send-sync/index.md) — What proof turns unsynchronized-looking shared storage into a sound concurrent abstraction, and where do ABA and reclamation defeat naive designs?
9. [Rayon, Work Stealing, and Deterministic Parallelism](module-69-rayon-work-stealing-and-deterministic-parallelism/index.md) — How can partitionable computation use many cores while preserving result meaning, associativity, ordering requirements, and bounded overhead?
10. [Integrated Concurrent Architecture, Testing, and Audit](module-70-integrated-concurrent-architecture-testing-and-audit/index.md) — How do bounded work, failure, cancellation, metrics, deterministic output, and testing form one reviewable concurrent product?


## The reasoning progression

```text
thread capability
    ↓
structured lifetime
    ↓
protected invariant
    ↓
wait condition
    ↓
ownership-transfer protocol
    ↓
liveness and failure
    ↓
happens-before proof
    ↓
lock-free safety boundary
    ↓
parallel decomposition
    ↓
whole-product audit
```

Each arrow introduces a new obligation without discarding earlier ones. An atomic counter still has an owner and a cleanup boundary. A Rayon reduction still needs an identity and an associative operation. A lock-free queue still needs an ordinary safe API and a termination protocol.

## Course products

The ten labs are independent products. They keep one mechanism visible and prevent the capstone from becoming the only source of practice. **BatchWeave** is cumulative: a deterministic batch engine with bounded work submission, worker ownership, result channels, cancellation, panic containment, atomic metrics, ordered result assembly, and a Rayon report stage.

Use the [study plan](study-plan.md), [BatchWeave engineering guide](capstone.md), [reference desk](reference.md), [compiler investigations](../compiler-labs/README.md), and [final review](final-review.md).

## Completion standard

You are ready for Course 8 only when you can do all of the following without tutorial imitation:

- draw the ownership and wait-for graph of an unfamiliar concurrent design;
- identify the invariant protected by every lock and the condition tested around every wait;
- explain shutdown for normal completion, cancellation, producer failure, worker panic, and receiver loss;
- derive each non-relaxed atomic ordering from a named publication or synchronization relationship;
- distinguish schedule-independent product output from timing observations;
- reject unnecessary lock-free or parallel complexity when a simpler protocol provides the required bound;
- make a cross-cutting change to BatchWeave and defend its safety, liveness, and determinism.

## Course handoff

Course 8 introduces asynchronous and networked Rust. The vocabulary changes from OS threads to futures, tasks, runtimes, sockets, backpressure, cancellation, and protocol state, but the proof obligations remain: ownership, visibility, progress, bounded resources, failure, and explicit shutdown.

[Return to the program start](../README.md) · [Begin Day 1](module-61-threads-schedules-send-sync-and-race-freedom/index.md)
