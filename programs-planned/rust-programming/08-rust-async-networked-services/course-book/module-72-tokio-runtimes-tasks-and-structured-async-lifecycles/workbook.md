# Workbook — Module 72: Tokio Runtimes, Tasks, and Structured Async Lifecycles

[Return to the chapter](index.md) · [Open the solutions](solutions.md) · [Open the JobWire guide](../capstone.md)

## Part 1 — Predict

1. A function spawns a task and immediately drops its `JoinHandle`. Does the task stop?
2. A task returns `Result<u64, DomainError>` and panics before returning. What type-level layers appear when awaiting the handle?
3. A spawned future borrows a local `String`. Why does “the parent awaits the handle immediately” not by itself satisfy the ordinary spawn boundary?
4. A `JoinSet` is dropped with three live tasks. What lifecycle effect should the owner expect?
5. An async task calls `std::thread::sleep` for five seconds. What happens to the runtime worker?
6. A `spawn_blocking` closure has begun an uninterruptible native call. The handle is aborted. Does the native call necessarily stop?
7. A non-`Send` future is moved to `LocalSet`. Which correctness problems remain?
8. A fail-fast task group returns immediately after the first domain error without draining children. Which obligations remain unresolved?

## Part 2 — Diagnose and repair

A service function accepts 50,000 paths, calls `tokio::spawn` for each, performs synchronous file hashing inside the task, and collects only the first 100 handles. Diagnose ownership, capacity, blocking, panic, and shutdown failures.

Produce a repair with:

- bounded admission;
- an explicit blocking boundary;
- one owner for all handles;
- stable input indices;
- complete terminal classification;
- a shutdown policy.

Then explain when a dedicated Rayon pool or synchronous worker group would be more honest than `spawn_blocking`.

## Part 3 — Focused exercises

### Exercise 1 — Task tree

Write a task tree for a service containing a listener, broker, health server, connection tasks, and job tasks. Name parent, cancellation source, join owner, and terminal policy.

### Exercise 2 — Spawn diagnosis

Create an async block that is non-`Send` because a `MutexGuard` or `Rc` remains live across `.await`. Repair it by narrowing liveness rather than adding a local executor.

### Exercise 3 — Nursery policy

Implement complete-all and fail-fast modes. Fail-fast must cancel siblings, drain every handle, and preserve the original failure separately from later cancellation outcomes.

### Exercise 4 — Blocking boundary

Wrap a CPU-heavy synchronous function in `spawn_blocking`. Add a semaphore that limits active closures and ensure permit ownership covers the whole closure.

### Exercise 5 — Locality defense

Give one legitimate reason to use `LocalSet` and one illegitimate reason. State how shutdown and panic observation work in both cases.

## Part 4 — Independent laboratory

Build [Task Nursery](../../labs/module-02-task-nursery/README.md). Required evidence:

- a task-tree diagram;
- source-indexed terminal outcomes;
- tests for success, domain failure, panic, cancellation, and a child that yields before completing;
- fail-fast behavior that still drains every child;
- no detached task after the nursery returns;
- a written bound on task count.

## Part 5 — Capstone transfer

Define JobWire’s top-level runtime owner and task tree. At minimum include:

```text
signal watcher
TCP accept loop
HTTP accept loop
broker
connection task set
job task set
```

For each, define startup failure, unexpected exit, shutdown signal, grace behavior, abort behavior, and join owner. Add a blocking-work policy even if the first JobWire operations are lightweight; the architecture must say what happens when an operation becomes CPU-heavy.

## Part 6 — Reconstruct and defend

1. Why does a spawned task need independent ownership?
2. What is the difference between detaching and aborting?
3. Why must an aborted handle still be awaited during complete shutdown?
4. Which outcomes can `JoinError` represent?
5. Why is `spawn_blocking` not an unlimited CPU-work solution?
6. When is a local task architecturally justified?

### Independent transfer

Design an async thumbnail service that accepts at most 200 requests, runs at most four CPU-heavy encoders, and shuts down within five seconds. Draw the task tree, capacity ledger, blocking boundary, and terminal-outcome policy before writing code.
