# Reasoned Solutions — Module 77: Cancellation Safety, Deadlines, and Graceful Shutdown

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-07-graceful-task-tree/README.md) · [JobWire guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 77: Cancellation Safety, Deadlines, and Graceful Shutdown**. Compare the reasoning against this question: *When an async operation loses a race, exceeds a deadline, or receives shutdown, what state survives, which effects may already have committed, and how does every task reach a terminal joined state?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Prediction solutions

1. The send future is dropped. Some bytes may already be buffered or written, so the connection policy must decide whether continuation is valid.
2. No. The broker may receive and commit after the caller stops waiting. Idempotency or status recovery is required.
3. No. Tasks observe cancellation when polled and when their code selects or checks the token.
4. No. Abort is cooperative at task poll boundaries; nonyielding code monopolizes its worker until it returns.
5. Yes. Admission must stop before draining descendants.
6. No. Dropping aborts as a backstop, but awaiting joins provides terminal evidence and panic/cancellation classification.
7. No. Total latency can be the sum of stage budgets. Carry one overall deadline.
8. No. Cancellation safety is operation-specific and may include data, ordering, and external effects.

## Part 2 — Repair reasoning

The repaired top-level owner records one shutdown reason, closes or cancels admission loops, tells connections and broker to stop accepting new work, drains committed work for a finite grace, aborts leftovers, and awaits every handle. The broker must remain alive while connections need terminal replies. Only after descendants finish does the top-level process return.

## Part 3 — Focused exercise guidance

The commit race should use an explicit gate around broker insertion. Before insertion, cancellation leaves no record. After insertion, retry with the same key observes in-progress or completed state. Paused time proves the deadline without waiting in wall-clock time.

Blocking jobs require separate policy. Cooperative work checks a flag. A noncooperative native call may delay runtime shutdown or require process isolation if a hard deadline is essential.

## Part 4 — Laboratory comparison

A strong task tree has one owner for every handle and one downward cancellation path. Repeated shutdown signals do not create competing drains. The test waits for task terminal states rather than inferring completion from token cancellation.

## Part 5 — Capstone comparison

JobWire should stop TCP and HTTP admission first. Connections stop accepting commands. The broker preserves committed jobs and rejects new submissions. After grace, connection and job sets are aborted and drained. The broker exits last so in-flight idempotency outcomes remain authoritative through drain.

## Part 6 — Reconstruction and defense

A complete defense names the local state dropped, external state preserved, commit boundary, deadline budget, and exact shutdown phase. It never uses “graceful” as a synonym for “sent a cancellation signal.”

## Deep reasoning and transfer

### Decisive model

> When an async operation loses a race, exceeds a deadline, or receives shutdown, what state survives, which effects may already have committed, and how does every task reach a terminal joined state?

Build a **cancellation and shutdown trace**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Derive cancellation behavior from future-owned state and external side effects.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Interpret `tokio::select!` as dropping nonselected branch futures.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Distinguish cancellation safety from memory safety.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Define an application commit point and recover ambiguous outcomes.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Propagate an overall deadline without resetting the budget at each stage.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Derive cancellation behavior from future-owned state and external side effects.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the cancellation and shutdown trace.

### Reference implementation comparison

For [Graceful Task Tree](../../labs/module-07-graceful-task-tree/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In JobWire, Module 77 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Cancellation Safety, Deadlines, and Graceful Shutdown**, which relationship decides this question: “When an async operation loses a race, exceeds a deadline, or receives shutdown, what state survives, which effects may already have committed, and how does every task reach a terminal joined state?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to JobWire?
