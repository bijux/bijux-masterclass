# Module 77: Cancellation Safety, Deadlines, and Graceful Shutdown

**Course 8, day 7 · Module 77 of 80**

**77/80** · [Course overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [JobWire guide](../capstone.md)

## The question

> When an async operation loses a race, exceeds a deadline, or receives shutdown, what state survives, which effects may already have committed, and how does every task reach a terminal joined state?

## Why this comes now

Modules 71–76 created a service that can suspend, own tasks, frame messages, manage connections, validate protocol state, and reject overload. The remaining lifecycle danger is abandonment. Async cancellation is common and often implicit: a `select!` branch loses, a timeout expires, a task is aborted, a client disconnects, or a supervisor drops a future during shutdown.

Rust safely drops the future’s owned fields. That does not make the operation semantically cancellation safe. A channel receive may be abandoned before removing an item, while a partially written frame may already have changed the peer’s input. A broker request may commit after the connection times out. A mutex-protected candidate may roll back by drop, while an external payment cannot.

Graceful shutdown is the system-wide form of the same problem. It must stop new commitments, notify all descendants, drain allowed work, impose a finite grace period, abort leftovers, and join every task. “Cancel the token and return” is not a complete shutdown protocol.

## What you will be able to do

- derive cancellation behavior from future-owned state and external side effects;
- interpret `tokio::select!` as dropping nonselected branch futures;
- distinguish cancellation safety from memory safety;
- define an application commit point and recover ambiguous outcomes;
- propagate an overall deadline without resetting the budget at each stage;
- use `CancellationToken` as a tree-shaped signal rather than a cleanup substitute;
- design stop-admission, signal, drain, abort, and join shutdown phases;
- account for tasks that do not yield or blocking work that cannot be preempted;
- write causal cancellation tests with notifications and paused time;
- state which operations may finish during shutdown and which must be rejected.

## Core model

### Cancellation means the future stops being polled and is dropped

At any suspension point, an incomplete future owns some local state. Dropping it runs destructors for those fields. The outside world may already have changed.

Cancellation analysis has two columns:

```text
local state destroyed by drop
external state not automatically undone
```

For a timer, external state is minimal. For a socket write, bytes may have escaped. For a broker command, the message may be queued. For a database operation, the server may commit after the client stops waiting.

Memory safety guarantees that owned Rust resources are cleaned according to their types. Cancellation safety is a higher-level protocol property.

### `select!` has winners and dropped losers

`tokio::select!` polls several branch futures and executes one ready branch. Other branch futures are dropped. If the surrounding loop recreates them, the operation may restart from an earlier state.

Ask of each branch:

- Can it be safely dropped at every pending state?
- If recreated, can it lose data or duplicate effects?
- Does the branch borrow state that survives outside it?
- Is branch order or fairness important when several are ready?
- Does disabling a branch change lifecycle assumptions?

Receiving from many channels, reading into a buffer, and sending through sinks have operation-specific guarantees. Consult the exact API contract and still trace product state.

### Cancellation-safe receive is not universal transaction safety

A channel receive future is often designed so losing a `select!` race does not remove an item. That makes repeated selection useful. Once the item is returned and application work begins, cancellation analysis moves to the application transition.

Similarly, an async mutex acquisition can be abandoned, but many fair queues cancel the waiter’s place. That may affect fairness even when state is not corrupted. Cancellation safety can include ordering and starvation consequences, not only data loss.

### Commit points divide retry semantics

A request lifecycle should identify one application commit point:

```text
before commit: rejection or cancellation means no semantic effect
at commit: state authority records ownership of the operation
 after commit: outcome must be retrieved, not blindly recreated
```

For JobWire, the broker can commit by inserting an idempotency record with the request fingerprint and an in-progress state. After that insertion, connection timeout does not mean “not accepted.” A retry with the same key attaches to or retrieves the same outcome.

This design turns ambiguous transport failure into recoverable application state.

### Deadline is an absolute budget

A duration is relative. A deadline names when the overall operation expires. Passing a fresh 500 ms timeout to connect, handshake, queue admission, job execution, and response write creates a 2.5-second operation and allows late work that can no longer satisfy the caller.

Use one deadline:

```rust
let deadline = Instant::now() + budget;
```

Before each stage, derive remaining time. If no time remains, do not start another stage. Child operations may have smaller stage caps, but they cannot exceed the overall deadline.

Deadlines need clock semantics. Use monotonic time for elapsed budgets. Wall-clock changes should not extend or shorten in-flight request durations.

### Timeout is cancellation plus classification

A timeout wrapper races the operation against a timer. When the timer wins, the operation future is dropped. Therefore every timeout decision includes:

- the underlying operation’s cancellation safety;
- whether external commit is possible;
- whether the connection remains usable;
- which public error is returned;
- whether a retry is permitted;
- how much overall budget remains.

Timeout is not a rollback primitive.

### Cancellation tokens communicate intent

A `CancellationToken` lets one owner signal cancellation to listeners and create child tokens. It is useful for task trees because a parent token can propagate intent downward.

The token does not:

- abort tasks by itself;
- join tasks;
- roll back side effects;
- force CPU loops to yield;
- preempt blocking calls;
- define which work may finish.

Each task must select or check cancellation at meaningful boundaries and then perform its cleanup or drain policy.

### Graceful shutdown is phased

A complete service shutdown can be expressed as:

```text
1. Trigger        record one shutdown reason
2. Stop admission close listeners / stop accepting new requests
3. Signal         cancel connection and service child tokens
4. Drain          allow selected in-flight work to reach terminal outcomes
5. Deadline       wait until grace expiry
6. Abort          abort remaining async tasks
7. Join           await every handle and classify panic/cancellation
8. Finalize       flush final reports and return process status
```

Order matters. If the broker stops before connections, they may hang waiting for replies. If listeners continue accepting during drain, the task set may never empty. If handles are dropped after abort, terminal cleanup is not observed.

### Work classes may have different shutdown policy

Classify work:

| Work | On shutdown |
|---|---|
| not yet admitted | reject immediately |
| queued but uncommitted | reject/cancel and reply when possible |
| committed idempotent job | allow within grace or preserve retrievable state |
| noncritical telemetry | drop |
| protocol response already writing | finish within write deadline or close |
| blocking native call | may outlive async grace unless cooperatively bounded |

“Graceful” does not mean every task always completes. It means the product has a deliberate and finite policy for every class.

### A shutdown future needs one owner

Multiple signals may race: Ctrl-C, admin command, fatal broker exit, health supervisor, or test trigger. Normalize them into one shutdown reason and make the transition idempotent. Repeated cancellation should not start multiple drain loops or close resources twice.

The top-level application owns process exit. Child tasks report fatal conditions upward; they do not call `process::exit` or create their own runtimes.

### Cancellation tests should place the operation

Use a notification or channel to prove the operation reached a specific pre-commit or post-commit state. Then cancel and assert exact cleanup. Examples:

- cancel before broker insertion: no idempotency record;
- cancel after insertion but before reply: retry retrieves one result;
- shutdown while connection idle: permit released and task joined;
- shutdown while job active: completes within grace or receives terminal cancellation;
- grace expires: task aborted and join reports cancellation;
- future with destructor guard: guard runs exactly once.

Real sleeps are poor positioning tools. Paused time and explicit gates make the test causal.

## Use the idea in a complete program

A generic task-tree shutdown helper can make phases visible:

```rust
use std::time::Duration;
use tokio::{task::JoinSet, time};
use tokio_util::sync::CancellationToken;

#[derive(Debug, Default)]
pub struct ShutdownReport {
    pub completed: usize,
    pub failed: usize,
    pub panicked: usize,
    pub cancelled: usize,
}

pub async fn shutdown<T, E>(
    cancellation: &CancellationToken,
    tasks: &mut JoinSet<Result<T, E>>,
    grace: Duration,
) -> ShutdownReport {
    cancellation.cancel();
    let deadline = time::Instant::now() + grace;
    let mut report = ShutdownReport::default();

    loop {
        if tasks.is_empty() {
            return report;
        }
        match time::timeout_at(deadline, tasks.join_next()).await {
            Ok(Some(Ok(Ok(_)))) => report.completed += 1,
            Ok(Some(Ok(Err(_)))) => report.failed += 1,
            Ok(Some(Err(error))) if error.is_cancelled() => report.cancelled += 1,
            Ok(Some(Err(_))) => report.panicked += 1,
            Ok(None) => return report,
            Err(_) => break,
        }
    }

    tasks.abort_all();
    while let Some(result) = tasks.join_next().await {
        match result {
            Ok(Ok(_)) => report.completed += 1,
            Ok(Err(_)) => report.failed += 1,
            Err(error) if error.is_cancelled() => report.cancelled += 1,
            Err(_) => report.panicked += 1,
        }
    }
    report
}
```

The helper does not stop admission; the caller must do that first. It also cannot preempt nonyielding async code or already-running blocking work. Those limitations belong in the service dossier.

## Practice sequence

1. Build a cancellation ledger for JobWire’s connection and broker request.
2. Analyze every future used inside one `select!`.
3. Convert stage timeouts into one propagated deadline.
4. Mark JobWire’s commit point.
5. Design shutdown phases and task order.
6. Write a test cancelling before and after commit.
7. Write a grace-expiry test with paused time.
8. Prove every aborted task is joined.

## Ready to continue

Continue only when you can explain:

- what drop cleans and what it cannot undo;
- which branch futures `select!` abandons;
- why timeout inherits cancellation behavior;
- where the application commit point is;
- how one deadline covers several stages;
- why cancellation tokens do not complete shutdown;
- which task is joined in every phase.

## Primary Rust references

- Tokio `select!`, `time::{timeout, timeout_at, Instant}`, task-abort, and signal documentation;
- Tokio-util `CancellationToken` documentation;
- API-specific cancellation-safety sections for channels, locks, streams, and I/O methods.

## Continue

Complete the [workbook](workbook.md), use the [reasoned solutions](solutions.md) only after freezing your own answer, build [Graceful Task Tree](../../labs/module-07-graceful-task-tree/README.md), and add the seventh [JobWire increment](../capstone.md#increment-7-make-cancellation-and-shutdown-explicit). Then continue to [Module 78](../module-78-http-services-with-hyper-requests-bodies-and-connections/index.md).
