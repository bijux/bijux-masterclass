# Workbook — Module 77: Cancellation Safety, Deadlines, and Graceful Shutdown

[Chapter](index.md) · [Laboratory](../../labs/module-07-graceful-task-tree/README.md) · [JobWire guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Cancellation Safety, Deadlines, and Graceful Shutdown** has become a usable model rather than remembered vocabulary. Its governing question is: *When an async operation loses a race, exceeds a deadline, or receives shutdown, what state survives, which effects may already have committed, and how does every task reach a terminal joined state?* Preserve your first prediction and record decisive facts in a **cancellation and shutdown trace**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 76 — Backpressure, Admission Control, and Fair Work Distribution that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **When an async operation loses a race, exceeds a deadline, or receives shutdown, what state survives, which effects may already have committed, and how does every task reach a terminal joined state?**
3. Draw the smallest **cancellation and shutdown trace** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

1. A `select!` timeout branch wins while a frame send is pending. What happens to the send future?
2. A broker request was queued before the caller timeout. Does timeout prove the operation did not commit?
3. A cancellation token is cancelled. Are child tasks immediately destroyed?
4. A task contains a five-second CPU loop with no await. Can async abort stop it immediately?
5. A service cancels connection tasks before stopping the accept loop. Can new tasks still appear during drain?
6. A shutdown path calls `abort_all` and drops the `JoinSet`. Has it proved all destructors and terminal states were observed?
7. Each request stage gets a fresh one-second timeout. Is the request bounded to one second?
8. A channel receive loses a `select!` race. Is it safe to assume every other async operation would be equally cancellation safe?

## Part 2 — Diagnose and repair

A server handles Ctrl-C by cancelling one token and returning from `main`. Connection handles are stored nowhere, the broker stops immediately, and job tasks may still be running. Diagnose admission, dependency order, drain, grace, abort, join, and process-exit failures.

Produce a phased shutdown protocol and a task table showing which work completes, cancels, or persists for recovery.

## Part 3 — Focused exercises

### Exercise 1 — Cancellation ledger

For connect, frame send, broker enqueue, broker commit, job execution, and response write, record future-owned state, external effects, and retry behavior after drop.

### Exercise 2 — Deadline type

Implement an absolute deadline helper with remaining time and stage caps. Test with paused Tokio time.

### Exercise 3 — Commit race

Use notifications to cancel once before broker commit and once after commit but before response. Prove different retry behavior.

### Exercise 4 — Shutdown tree

Implement stop-admission, signal, drain, abort, and join phases for a `JoinSet`. Preserve panic and cancellation counts.

### Exercise 5 — Blocking limitation

Submit cooperative and noncooperative blocking jobs. Explain what async shutdown can and cannot guarantee.

### Interleaved reasoning pass

1. For **Derive cancellation behavior from future-owned state and external side effects**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the cancellation and shutdown trace.
2. For **Interpret `tokio::select!` as dropping nonselected branch futures**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the cancellation and shutdown trace.
3. For **Distinguish cancellation safety from memory safety**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the cancellation and shutdown trace.
4. For **Define an application commit point and recover ambiguous outcomes**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the cancellation and shutdown trace.

5. Identify one guarantee from an earlier course that a careless implementation of **Cancellation Safety, Deadlines, and Graceful Shutdown** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Graceful Task Tree](../../labs/module-07-graceful-task-tree/README.md). Required evidence:

- hierarchical cancellation;
- idempotent shutdown trigger;
- stopped admission before drain;
- finite grace under paused time;
- abort followed by complete join;
- exact terminal outcome counts;
- no task or permit surviving return.

### Laboratory acceptance trace

Before opening the reference implementation for **Graceful Task Tree**, record:

- the public behavior that demonstrates **Derive cancellation behavior from future-owned state and external side effects**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Add JobWire’s shutdown controller. Define ordering among TCP listener, HTTP listener, connection tasks, broker admission, jobs, and final broker exit. Add tests for idle connection, active pre-commit request, committed job, stuck task, and repeated shutdown signal.

### Capstone invariant trace

For the Module 77 JobWire increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

1. What does cancellation by drop destroy?
2. Why can external effects survive?
3. What does a timeout add beyond cancellation?
4. What does a token signal but not perform?
5. Why stop admission first?
6. Why join after abort?

### Independent transfer

Design shutdown for an async file-upload service. Files may be partially written and metadata commits are idempotent. State which files are deleted, resumed, finalized, or retained after each cancellation point.

### Closed-book defense

In five minutes, answer “When an async operation loses a race, exceeds a deadline, or receives shutdown, what state survives, which effects may already have committed, and how does every task reach a terminal joined state?” using the **cancellation and shutdown trace**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside JobWire. A list of APIs without the deciding relationship is incomplete.
