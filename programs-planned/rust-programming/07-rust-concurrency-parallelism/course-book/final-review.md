# Course 7 Final Review — Rust Concurrency and Parallelism

Begin every part from a blank page. You may use your code and the records you created, but do not follow the chapters line by line. The purpose is to expose whether the model can be reconstructed and transferred.

## Part 1 — Reconstruct the ten questions

For each question, supply a smallest working example, a causal negative example, the earliest decisive phase or event, a requirement-preserving repair, and one limit on the evidence you would use.

61. **Threads, Schedules, Send, Sync, and Race Freedom** — What may cross a thread boundary, what may be shared through a reference, and which correctness problems remain after Rust has ruled out data races?
62. **Structured Threads: Scopes, Joins, and Panic Boundaries** — How can borrowed data, thread lifetime, completion, and panic handling be enclosed by one parent operation rather than leaked into the rest of the program?
63. **Shared State: Locks and Protected Invariants** — Which exact invariant does a lock protect, how small can the protected transition be, and what state remains valid after contention or panic?
64. **Coordination: Condvars, Barriers, and Phase Protocols** — How do threads wait for a state predicate or phase transition without polling, lost wakeups, or treating notification itself as truth?
65. **Message Passing, Backpressure, and Shutdown** — Which values cross ownership boundaries, how is capacity bounded, and which explicit protocol event proves that every sender, receiver, and worker can terminate?
66. **Liveness: Deadlock, Cancellation, and Recovery** — Why can every blocked operation eventually continue or terminate, and what happens when cancellation, panic, or partial infrastructure failure interrupts the normal path?
67. **Atomics, Happens-Before, and Memory Ordering** — Which fact does an atomic operation publish, which earlier writes become visible because of it, and what is the weakest ordering that proves the required relationship?
68. **Lock-Free Protocols, Reclamation, and Unsafe Send/Sync** — What proof permits shared raw storage to be accessed without a lock, and where do role confusion, ABA, destruction, or memory reclamation invalidate a locally plausible algorithm?
69. **Rayon, Work Stealing, and Deterministic Parallelism** — How can divisible computation use a work-stealing pool while preserving item meaning, reduction laws, failure policy, result ordering, and a defensible cost model?
70. **Integrated Concurrent Architecture, Testing, and Audit** — How do ownership, bounded work, synchronization, liveness, panic, cancellation, atomics, deterministic reporting, and test evidence become one product whose strongest claims are reviewable?

API names without the governing relationship do not answer this part.

## Part 2 — Independent construction

Build this product without copying a course domain:

> Build a bounded concurrent verifier with a fixed worker group, explicit failure policy, cancellation, panic containment, complete join accounting, and deterministic final reconstruction.

Before implementation, write:

```text
product promise and non-goals
owners and authorities
valid and invalid states
success transition
failure, cleanup, and retry state
order and capacity
external assumptions
public API
verification plan
three rejected designs
```

After implementation, preserve six traces: ordinary success, malformed input, rejected state, partial work before failure, cleanup, and one compatibility, platform, scheduler, workload, or peer edge relevant to this course.

## Part 3 — Capstone change

Apply this change to BatchWeave:

> Add bounded retry to BatchWeave while preserving one terminal outcome per source job, fail-fast semantics, queue bounds, and deterministic final reporting.

Do not introduce a second source of truth for validation, state, ordering, storage, protocol, scheduling, generation, measurement, or compatibility. Revise the authority map first when the change does not fit the current architecture.

Review the change through:

1. public behavior;
2. owner of the new invariant;
3. state after each failure point;
4. ownership and cleanup;
5. ordering and resource bounds;
6. compatibility or format consequences;
7. independent tests and their limits;
8. the simpler design you rejected.

## Part 4 — Cross-course preservation

Select one guarantee from Course 6 — Rust Systems Programming and prove that the new construction does not regress it.

Trace one requirement from input to internal state, effect, output, and test. If Course 7 introduces a stronger mechanism, explain why the earlier simpler design is no longer sufficient rather than assuming that greater abstraction is automatically better.

## Part 5 — Diagnosis sprint

Choose three unfamiliar cases from the course: one valid, one rejected by an early decisive phase, and one that compiles or runs while violating the product contract. Freeze the prediction, use a **concurrent architecture dossier**, observe the result, and explain every mismatch between prediction and evidence.

## Part 6 — Oral defense

- **Module 61 — Threads, Schedules, Send, Sync, and Race Freedom:** answer “What may cross a thread boundary, what may be shared through a reference, and which correctness problems remain after Rust has ruled out data races?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 62 — Structured Threads: Scopes, Joins, and Panic Boundaries:** answer “How can borrowed data, thread lifetime, completion, and panic handling be enclosed by one parent operation rather than leaked into the rest of the program?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 63 — Shared State: Locks and Protected Invariants:** answer “Which exact invariant does a lock protect, how small can the protected transition be, and what state remains valid after contention or panic?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 64 — Coordination: Condvars, Barriers, and Phase Protocols:** answer “How do threads wait for a state predicate or phase transition without polling, lost wakeups, or treating notification itself as truth?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 65 — Message Passing, Backpressure, and Shutdown:** answer “Which values cross ownership boundaries, how is capacity bounded, and which explicit protocol event proves that every sender, receiver, and worker can terminate?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 66 — Liveness: Deadlock, Cancellation, and Recovery:** answer “Why can every blocked operation eventually continue or terminate, and what happens when cancellation, panic, or partial infrastructure failure interrupts the normal path?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 67 — Atomics, Happens-Before, and Memory Ordering:** answer “Which fact does an atomic operation publish, which earlier writes become visible because of it, and what is the weakest ordering that proves the required relationship?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 68 — Lock-Free Protocols, Reclamation, and Unsafe Send/Sync:** answer “What proof permits shared raw storage to be accessed without a lock, and where do role confusion, ABA, destruction, or memory reclamation invalidate a locally plausible algorithm?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 69 — Rayon, Work Stealing, and Deterministic Parallelism:** answer “How can divisible computation use a work-stealing pool while preserving item meaning, reduction laws, failure policy, result ordering, and a defensible cost model?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 70 — Integrated Concurrent Architecture, Testing, and Audit:** answer “How do ownership, bounded work, synchronization, liveness, panic, cancellation, atomics, deterministic reporting, and test evidence become one product whose strongest claims are reviewable?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.

End with a fifteen-minute defense of BatchWeave: product and non-goals, ownership and authority, main invariant, failure model, ordering and bounds, one difficult proof boundary, one rejected shortcut, evidence limits, and the handoff to the next course.

## Completion standard

Course 7 — Rust Concurrency and Parallelism is complete when another competent Rust reader can reproduce the product behavior and causal explanation from your public contract, tests, and reasoning records. You must be able to say which claims are guaranteed by Rust, supplied by a library, chosen by the product, conditioned on a target or peer, or merely observed for one artifact and workload.

## Seven-day retention check

Without opening the course, redraw the ten-module chain and the core **concurrent architecture dossier**. Rebuild one small example in a new domain. Revisit only the relationships you cannot recover, then repeat the reconstruction rather than rereading the answer passively.
