# Workbook — Module 77: Cancellation Safety, Deadlines, and Graceful Shutdown

[Return to the chapter](index.md) · [Open the solutions](solutions.md) · [Open the JobWire guide](../capstone.md)

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

## Part 4 — Independent laboratory

Build [Graceful Task Tree](../../labs/module-07-graceful-task-tree/README.md). Required evidence:

- hierarchical cancellation;
- idempotent shutdown trigger;
- stopped admission before drain;
- finite grace under paused time;
- abort followed by complete join;
- exact terminal outcome counts;
- no task or permit surviving return.

## Part 5 — Capstone transfer

Add JobWire’s shutdown controller. Define ordering among TCP listener, HTTP listener, connection tasks, broker admission, jobs, and final broker exit. Add tests for idle connection, active pre-commit request, committed job, stuck task, and repeated shutdown signal.

## Part 6 — Reconstruct and defend

1. What does cancellation by drop destroy?
2. Why can external effects survive?
3. What does a timeout add beyond cancellation?
4. What does a token signal but not perform?
5. Why stop admission first?
6. Why join after abort?

### Independent transfer

Design shutdown for an async file-upload service. Files may be partially written and metadata commits are idempotent. State which files are deleted, resumed, finalized, or retained after each cancellation point.
