# Ten-day study plan — Rust Concurrency and Parallelism

This course is designed for two calendar weeks with ten intensive study days. A full day is approximately eight focused hours plus breaks. Concurrency work degrades quickly when done while fatigued; stop before the final review if you are no longer accurately tracing ownership or wait conditions.

## Daily method

Use the same four artifacts every day:

- a **thread ownership map** showing who owns values and joins;
- a **synchronization ledger** naming every lock, condition, channel, or atomic relation;
- a **schedule table** containing at least three legal interleavings;
- a **failure matrix** covering normal completion, cancellation, panic, disconnect, and cleanup.

The suggested day is:

```text
08:30–09:00  closed-book retrieval
09:00–11:00  authoritative chapter
11:15–12:30  frozen predictions
13:30–15:00  diagnosis and focused construction
15:15–17:15  independent laboratory
18:00–19:15  BatchWeave increment
19:15–20:00  tests, explanation, and final schedule review
```

Do not use sleeps as correctness mechanisms. A sleep can widen one schedule during a demonstration, but it does not prove ordering, progress, or absence of races.

## Day 1 — Threads, Schedules, Send, Sync, and Race Freedom

Read the chapter, complete the workbook predictions before compiling, and build **Thread Handoff Matrix** from its starter. In BatchWeave, define the job, outcome, schedule, and determinism contracts before creating any worker thread.

End the day by answering the module question in one paragraph: *What may move or be shared between threads, and which correctness properties remain unprotected after data races are ruled out?* Your answer must name the decisive ownership, synchronization, liveness, and determinism facts rather than list APIs.

## Day 2 — Structured Threads: Scopes, Joins, and Panic Boundaries

Read the chapter, complete the workbook predictions before compiling, and build **Scoped Slice Analysis** from its starter. In BatchWeave, build a structured worker group whose lifetime, joins, and panic outcomes are owned by one run operation.

End the day by answering the module question in one paragraph: *How can thread lifetime, borrowed data, completion, and panic handling be bounded by one parent operation?* Your answer must name the decisive ownership, synchronization, liveness, and determinism facts rather than list APIs.

## Day 3 — Shared State: Locks and Protected Invariants

Read the chapter, complete the workbook predictions before compiling, and build **Protected Inventory** from its starter. In BatchWeave, introduce the shared run ledger and make every lock guard correspond to one named invariant.

End the day by answering the module question in one paragraph: *Which invariant does each lock protect, how small can guard scope be, and what state is valid after panic or recovery?* Your answer must name the decisive ownership, synchronization, liveness, and determinism facts rather than list APIs.

## Day 4 — Coordination: Condvars, Barriers, and Phase Protocols

Read the chapter, complete the workbook predictions before compiling, and build **Phase Gate** from its starter. In BatchWeave, replace polling with a bounded queue whose not-empty and not-full conditions are represented by state plus condition variables.

End the day by answering the module question in one paragraph: *How do threads wait for conditions and phases without polling, lost wakeups, or confusing notification with truth?* Your answer must name the decisive ownership, synchronization, liveness, and determinism facts rather than list APIs.

## Day 5 — Message Passing, Backpressure, and Shutdown

Read the chapter, complete the workbook predictions before compiling, and build **Bounded Map Pipeline** from its starter. In BatchWeave, route worker outcomes through an explicit result channel and make producer completion, cancellation, and queue closure distinct events.

End the day by answering the module question in one paragraph: *Which values cross ownership boundaries, how is capacity bounded, and what exact event ends the protocol?* Your answer must name the decisive ownership, synchronization, liveness, and determinism facts rather than list APIs.

## Day 6 — Liveness: Deadlock, Cancellation, and Recovery

Read the chapter, complete the workbook predictions before compiling, and build **Cancellable Worker Group** from its starter. In BatchWeave, add fail-fast and complete-all policies, panic containment, join auditing, and a termination proof for every run path.

End the day by answering the module question in one paragraph: *How can a concurrent system make progress and terminate when locks, workers, panics, cancellation, or partial failure interact?* Your answer must name the decisive ownership, synchronization, liveness, and determinism facts rather than list APIs.

## Day 7 — Atomics, Happens-Before, and Memory Ordering

Read the chapter, complete the workbook predictions before compiling, and build **Atomic Progress** from its starter. In BatchWeave, publish monotonic run metrics and cancellation state with orderings justified by a happens-before ledger rather than habit.

End the day by answering the module question in one paragraph: *Which facts become visible because of an atomic operation, and what is the weakest ordering that proves that relationship?* Your answer must name the decisive ownership, synchronization, liveness, and determinism facts rather than list APIs.

## Day 8 — Lock-Free Protocols, Reclamation, and Unsafe Send/Sync

Read the chapter, complete the workbook predictions before compiling, and build **Bounded SPSC Ring** from its starter. In BatchWeave, audit whether BatchWeave needs a lock-free queue, document the rejected design, and keep unsafe code out of the product when blocking backpressure is the actual requirement.

End the day by answering the module question in one paragraph: *What proof turns unsynchronized-looking shared storage into a sound concurrent abstraction, and where do ABA and reclamation defeat naive designs?* Your answer must name the decisive ownership, synchronization, liveness, and determinism facts rather than list APIs.

## Day 9 — Rayon, Work Stealing, and Deterministic Parallelism

Read the chapter, complete the workbook predictions before compiling, and build **Parallel Histogram** from its starter. In BatchWeave, add a Rayon report stage whose reduction is associative, whose output order is explicit, and whose thread pool is owned by the run configuration.

End the day by answering the module question in one paragraph: *How can partitionable computation use many cores while preserving result meaning, associativity, ordering requirements, and bounded overhead?* Your answer must name the decisive ownership, synchronization, liveness, and determinism facts rather than list APIs.

## Day 10 — Integrated Concurrent Architecture, Testing, and Audit

Read the chapter, complete the workbook predictions before compiling, and build **Concurrent Verifier** from its starter. In BatchWeave, finish the CLI, deterministic report, adversarial tests, schedule-oriented audit, and independent cross-cutting change.

End the day by answering the module question in one paragraph: *How do bounded work, failure, cancellation, metrics, deterministic output, and testing form one reviewable concurrent product?* Your answer must name the decisive ownership, synchronization, liveness, and determinism facts rather than list APIs.

## Weekend consolidation

After Day 5, reconstruct the complete protocol of the bounded map pipeline without notes. Draw its channel topology, capacity, sender count, receiver ownership, and shutdown event. Then inspect one earlier solution and write a correction note explaining where your own model was too weak or too broad.

After Day 10, do not immediately begin async Rust. Re-run the final independent construction after at least one night of sleep. Concurrency knowledge that exists only while the chapter is open is not yet a usable skill.

## Recovery rules

Repeat a module before advancing when any of these is true:

- you cannot explain why a value is `Send` or why `&T` requires `T: Sync`;
- a wait has no predicate loop;
- a channel protocol depends on a sender being dropped “somewhere”;
- a lock order is informal or changes by code path;
- cancellation can leave an unjoined thread;
- an atomic ordering is justified by “stronger is safer” rather than a visibility argument;
- parallel output order is accidental;
- a test passes only because of timing sleeps.

[Open Day 1](module-61-threads-schedules-send-sync-and-race-freedom/index.md)
