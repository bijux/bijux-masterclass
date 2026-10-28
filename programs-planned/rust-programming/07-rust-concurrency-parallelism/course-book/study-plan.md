# Course 7 Study Plan — Rust Concurrency and Parallelism

Ten dense study days fit into two calendar weeks. The goal is not to maximize reading time; it is to make **Which facts remain true across every legal thread schedule, and what ownership, synchronization, progress, failure, and normalization arguments make those facts reviewable?** answerable through construction and explanation.

## Daily rhythm

Use a **concurrent architecture dossier** across the course. Each day begins by reconstructing yesterday’s decisive relationship and ends by tracing one capstone invariant. Preserve the first prediction, the observed result, the principled repair, and the shortcut you rejected.

## Day 1 — Module 61: Threads, Schedules, Send, Sync, and Race Freedom

**Question:** What may cross a thread boundary, what may be shared through a reference, and which correctness problems remain after Rust has ruled out data races?

**Retrieval:** Without notes, restate the invariant carried from Module 60 — Integrated Systems Design, Testing, and Audit. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 61](./module-61-threads-schedules-send-sync-and-race-freedom/index.md) with a **thread ownership map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-61-threads-schedules-send-sync-and-race-freedom/workbook.md) before observation. The day’s minimum result is: **Distinguish concurrency, parallelism, scheduling, interleaving, data races, and broader race conditions.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Thread Handoff Matrix](../labs/module-01-thread-handoff-matrix/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 61 in the [BatchWeave guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish concurrency, parallelism, scheduling, interleaving, data races, and broader race conditions.** End with one simpler design that would be preferable under a narrower requirement.

## Day 2 — Module 62: Structured Threads: Scopes, Joins, and Panic Boundaries

**Question:** How can borrowed data, thread lifetime, completion, and panic handling be enclosed by one parent operation rather than leaked into the rest of the program?

**Retrieval:** Without notes, restate the invariant carried from Module 61 — Threads, Schedules, Send, Sync, and Race Freedom. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 62](./module-62-structured-threads-scopes-joins-and-panic-boundaries/index.md) with a **join and panic tree** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-62-structured-threads-scopes-joins-and-panic-boundaries/workbook.md) before observation. The day’s minimum result is: **Explain the real meaning of a `T: 'static` bound and why owned values can satisfy it.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Scoped Slice Analysis](../labs/module-02-scoped-slice-analysis/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 62 in the [BatchWeave guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Explain the real meaning of a `T: 'static` bound and why owned values can satisfy it.** End with one simpler design that would be preferable under a narrower requirement.

## Day 3 — Module 63: Shared State: Locks and Protected Invariants

**Question:** Which exact invariant does a lock protect, how small can the protected transition be, and what state remains valid after contention or panic?

**Retrieval:** Without notes, restate the invariant carried from Module 62 — Structured Threads: Scopes, Joins, and Panic Boundaries. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 63](./module-63-shared-state-locks-and-protected-invariants/index.md) with a **protected-invariant table** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-63-shared-state-locks-and-protected-invariants/workbook.md) before observation. The day’s minimum result is: **Name the state invariant protected by each `Mutex` or `RwLock` rather than treating the primitive as a generic thread-safety wrapper.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Protected Inventory](../labs/module-03-protected-inventory/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 63 in the [BatchWeave guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Name the state invariant protected by each `Mutex` or `RwLock` rather than treating the primitive as a generic thread-safety wrapper.** End with one simpler design that would be preferable under a narrower requirement.

## Day 4 — Module 64: Coordination: Condvars, Barriers, and Phase Protocols

**Question:** How do threads wait for a state predicate or phase transition without polling, lost wakeups, or treating notification itself as truth?

**Retrieval:** Without notes, restate the invariant carried from Module 63 — Shared State: Locks and Protected Invariants. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 64](./module-64-coordination-condvars-barriers-and-phase-protocols/index.md) with a **predicate and wakeup record** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-64-coordination-condvars-barriers-and-phase-protocols/workbook.md) before observation. The day’s minimum result is: **Write every condition-variable wait as a predicate loop over mutex-protected state.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Phase Gate](../labs/module-04-phase-gate/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 64 in the [BatchWeave guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Write every condition-variable wait as a predicate loop over mutex-protected state.** End with one simpler design that would be preferable under a narrower requirement.

## Day 5 — Module 65: Message Passing, Backpressure, and Shutdown

**Question:** Which values cross ownership boundaries, how is capacity bounded, and which explicit protocol event proves that every sender, receiver, and worker can terminate?

**Retrieval:** Without notes, restate the invariant carried from Module 64 — Coordination: Condvars, Barriers, and Phase Protocols. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 65](./module-65-message-passing-backpressure-and-shutdown/index.md) with a **channel topology** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-65-message-passing-backpressure-and-shutdown/workbook.md) before observation. The day’s minimum result is: **Model channel operations as ownership transfer rather than shared access.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Bounded Map Pipeline](../labs/module-05-bounded-map-pipeline/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 65 in the [BatchWeave guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Model channel operations as ownership transfer rather than shared access.** End with one simpler design that would be preferable under a narrower requirement.

## Midpoint reconstruction

Do not add a sixth topic on the recovery day. Reconstruct **Threads, Schedules, Send, Sync, and Race Freedom, Structured Threads: Scopes, Joins, and Panic Boundaries, Shared State: Locks and Protected Invariants, Coordination: Condvars, Barriers, and Phase Protocols, Message Passing, Backpressure, and Shutdown** as one dependency chain, rerun the two investigations that changed your model most, and describe the current BatchWeave state from an empty page. Repair incomplete work, then take a real break; consolidation is part of the course rather than unused time.

## Day 6 — Module 66: Liveness: Deadlock, Cancellation, and Recovery

**Question:** Why can every blocked operation eventually continue or terminate, and what happens when cancellation, panic, or partial infrastructure failure interrupts the normal path?

**Retrieval:** Without notes, restate the invariant carried from Module 65 — Message Passing, Backpressure, and Shutdown. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 66](./module-66-liveness-deadlock-cancellation-and-recovery/index.md) with a **wait-for and shutdown graph** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-66-liveness-deadlock-cancellation-and-recovery/workbook.md) before observation. The day’s minimum result is: **Distinguish deadlock, starvation, livelock, priority inversion, and slow work.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Cancellable Worker Group](../labs/module-06-cancellable-worker-group/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 66 in the [BatchWeave guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish deadlock, starvation, livelock, priority inversion, and slow work.** End with one simpler design that would be preferable under a narrower requirement.

## Day 7 — Module 67: Atomics, Happens-Before, and Memory Ordering

**Question:** Which fact does an atomic operation publish, which earlier writes become visible because of it, and what is the weakest ordering that proves the required relationship?

**Retrieval:** Without notes, restate the invariant carried from Module 66 — Liveness: Deadlock, Cancellation, and Recovery. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 67](./module-67-atomics-happens-before-and-memory-ordering/index.md) with a **happens-before graph** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-67-atomics-happens-before-and-memory-ordering/workbook.md) before observation. The day’s minimum result is: **Separate atomicity of one location from visibility of other memory.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Atomic Progress](../labs/module-07-atomic-progress/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 67 in the [BatchWeave guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Separate atomicity of one location from visibility of other memory.** End with one simpler design that would be preferable under a narrower requirement.

## Day 8 — Module 68: Lock-Free Protocols, Reclamation, and Unsafe Send/Sync

**Question:** What proof permits shared raw storage to be accessed without a lock, and where do role confusion, ABA, destruction, or memory reclamation invalidate a locally plausible algorithm?

**Retrieval:** Without notes, restate the invariant carried from Module 67 — Atomics, Happens-Before, and Memory Ordering. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 68](./module-68-lock-free-protocols-reclamation-and-unsafe-send-sync/index.md) with a **atomic state machine** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-68-lock-free-protocols-reclamation-and-unsafe-send-sync/workbook.md) before observation. The day’s minimum result is: **Distinguish obstruction-free, lock-free, and wait-free progress claims from ordinary nonblocking API behavior.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Bounded SPSC Ring](../labs/module-08-spsc-ring/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 68 in the [BatchWeave guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish obstruction-free, lock-free, and wait-free progress claims from ordinary nonblocking API behavior.** End with one simpler design that would be preferable under a narrower requirement.

## Day 9 — Module 69: Rayon, Work Stealing, and Deterministic Parallelism

**Question:** How can divisible computation use a work-stealing pool while preserving item meaning, reduction laws, failure policy, result ordering, and a defensible cost model?

**Retrieval:** Without notes, restate the invariant carried from Module 68 — Lock-Free Protocols, Reclamation, and Unsafe Send/Sync. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 69](./module-69-rayon-work-stealing-and-deterministic-parallelism/index.md) with a **work-partition and reduction map** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-69-rayon-work-stealing-and-deterministic-parallelism/workbook.md) before observation. The day’s minimum result is: **Distinguish task parallelism, data parallelism, and a long-lived message-driven worker service.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Parallel Histogram](../labs/module-09-parallel-histogram/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 69 in the [BatchWeave guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Distinguish task parallelism, data parallelism, and a long-lived message-driven worker service.** End with one simpler design that would be preferable under a narrower requirement.

## Day 10 — Module 70: Integrated Concurrent Architecture, Testing, and Audit

**Question:** How do ownership, bounded work, synchronization, liveness, panic, cancellation, atomics, deterministic reporting, and test evidence become one product whose strongest claims are reviewable?

**Retrieval:** Without notes, restate the invariant carried from Module 69 — Rayon, Work Stealing, and Deterministic Parallelism. Mark the point where that earlier guarantee could be weakened today.

**Chapter:** Read [Module 70](./module-70-integrated-concurrent-architecture-testing-and-audit/index.md) with a **concurrent architecture dossier** beside it. Type the central examples, change one assumption, and predict the earliest compiler, runtime, build, platform, schedule, or review consequence.

**Workbook:** Complete the [workbook](./module-70-integrated-concurrent-architecture-testing-and-audit/workbook.md) before observation. The day’s minimum result is: **Construct one architecture diagram connecting coordinator, queue, workers, result channel, metrics, report pool, and CLI boundaries.** Keep one positive case and one causal negative case.

**Laboratory:** Build [Concurrent Verifier](../labs/module-10-concurrent-verifier/README.md) from `starter/`. Add the adversarial case before the architecture-changing repair, then complete the unrelated transfer task.

**Capstone:** Apply Module 70 in the [BatchWeave guide](capstone.md). Record the owner of the changed fact, state after failure, any order or capacity promise, and the earlier invariant that remains intact.

**Exit:** Explain this capability without notes: **Construct one architecture diagram connecting coordinator, queue, workers, result channel, metrics, report pool, and CLI boundaries.** End with one simpler design that would be preferable under a narrower requirement.

## Final integration

After Day 10, complete the [final review](final-review.md), run the strongest available course route, and implement this unseen capstone change: **Add bounded retry to BatchWeave while preserving one terminal outcome per source job, fail-fast semantics, queue bounds, and deterministic final reporting.**

Seven days later, rebuild the ten-module sequence and the core **concurrent architecture dossier** without the book. Write a fresh example for every relationship you cannot recover. Re-reading a solution without recreating the model does not count as retained learning.
