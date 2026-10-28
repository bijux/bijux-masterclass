# Module 72 — Tokio Runtimes, Tasks, and Structured Async Lifecycles

**Course 8 · Day 2 · Module 72 of 100**
`██████████████████░░░░░░░` **72/100**

[Program](../../../README.md) · [Course 8](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-02-task-nursery/README.md) · [JobWire guide](../capstone.md)

[← Module 71: Futures, Polling, Wakers, and Async State Machines](../module-71-futures-polling-wakers-and-async-state-machines/index.md) · [Module 73: Async I/O, Buffers, Streams, and Framing →](../module-73-async-io-buffers-streams-and-framing/index.md)

## The question

> Once futures are understood as poll-driven state machines, how should a runtime own, schedule, observe, cancel, and finish the tasks that execute them?

## Why this comes now

Module 71 deliberately avoided a runtime. You learned what a future promises before learning how Tokio schedules one. That order prevents a common mistake: treating `tokio::spawn` as an async version of “call this function in the background.” A spawned task is an independently scheduled lifecycle with an owned future, a terminal result or panic, possible cancellation, and resource cleanup. The creating function does not automatically wait for it.

Tokio supplies a reactor for I/O readiness, timers, scheduling queues, synchronization primitives, and runtime workers. Those mechanisms make async systems practical; they do not decide the product’s ownership tree. A service that drops join handles, spawns without admission limits, performs blocking work on runtime workers, or shuts down without draining tasks can be type-correct and operationally broken.

This module uses structured concurrency as a design principle even where the library does not enforce it as one universal construct: child tasks should be owned by a scope or manager whose lifetime contains their work, whose shutdown reaches them, and whose terminal outcomes are observed.

### Prerequisite bridge

Module 71 established **Futures, Polling, Wakers, and Async State Machines**. Before continuing, verify that you can produce a future-state ledger for a larger operation. This module preserves that capability and adds the ability to distinguish a runtime, worker thread, task, future, reactor, and blocking pool;. Module 73, **Async I/O, Buffers, Streams, and Framing**, will rely on both when it asks: *How do arbitrary, partial byte transfers become complete bounded messages without confusing readiness, reads, buffers, frames, or protocol meaning?*

### Scope boundary

This module owns the reasoning for **tokio runtimes, tasks, and structured async lifecycles** inside Course 8. The course builds a process-local network service. It does not attempt distributed consensus, TLS implementation, database transactions, service meshes, or framework-driven web development. Those concerns are discussed only where they affect the stated protocol and lifecycle guarantees. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- distinguish a runtime, worker thread, task, future, reactor, and blocking pool;
- explain the `Send + 'static` requirements of ordinary multi-threaded task spawning;
- derive when a task should borrow through an enclosing async scope versus own cloned or moved data;
- use `JoinHandle` and `JoinSet` as explicit result, panic, cancellation, and cleanup obligations;
- distinguish dropping a join handle from aborting the task;
- design a task tree with one owner for every child;
- use `LocalSet` for intentionally non-`Send` futures without presenting it as a generic workaround;
- move blocking or CPU-heavy work to a bounded blocking boundary;
- explain why `spawn_blocking` cancellation is limited after work begins;
- construct a phased task nursery that observes every terminal outcome.

## Core model

### The runtime has several jobs

An async runtime coordinates at least four kinds of work:

1. **Scheduling:** selecting ready tasks and polling their futures.
2. **I/O readiness:** registering sockets and waking tasks when the OS reports useful readiness.
3. **Time:** waking tasks when timers or deadlines expire.
4. **Blocking isolation:** running blocking functions away from the cooperative async worker set.

These are implementation services, not application ownership. Tokio can wake a task; it cannot know whether the task should still exist after its parent request fails. Tokio can abort a task; it cannot infer whether abandoned external work requires compensation.

A useful runtime diagram is:

```text
ready task queue ──> runtime workers ──poll──> futures
       ▲                                  │
       │                                  ├─ Ready(result)
I/O driver / timer / channel waker ───────└─ Pending

blocking queue ──> blocking worker pool ──> synchronous functions
```

The async worker pool should stay available to poll many short state transitions. A blocking syscall or long CPU loop on one of those workers prevents unrelated ready tasks from advancing.

### Spawn transfers ownership of the future

`tokio::spawn(future)` requires an independently owned future that can generally move between runtime worker threads and outlive the caller’s stack frame. That is why the boundary requires `Send + 'static` for the future and `Send + 'static` for its output.

`'static` here does not mean “the task runs forever.” It means the future contains no borrowed reference whose validity depends on a shorter stack frame. Owned `String`, `Arc<T>`, and other owned data can satisfy `'static` even when dropped milliseconds later.

Before spawning, ask whether independence is real. If the child must finish before the parent operation returns, a structured local concurrency mechanism may be clearer than manufacturing owned clones. If it is a service-lifetime task, move the required owned state and retain its handle in a service owner.

### A join handle has two channels of outcome

Awaiting a Tokio `JoinHandle<T>` produces a `Result<T, JoinError>`. There are two layers:

```text
task execution outcome: T (which may itself be Result<Domain, DomainError>)
runtime task outcome:   JoinError for panic or cancellation
```

Flattening these too early loses important distinctions. A domain error is an expected task result. A panic indicates an invariant failure or unexpected defect. Cancellation may be deliberate during shutdown or accidental because an owner aborted work.

A robust task report can represent:

```rust
pub enum TaskOutcome<T, E> {
    Completed(T),
    Failed(E),
    Panicked(String),
    Cancelled,
}
```

The exact type depends on the product, but the categories should not disappear into a single string before policy is applied.

### Dropping the handle detaches; aborting requests cancellation

Dropping `JoinHandle` does not wait and does not cancel. The task continues detached until it completes or the runtime shuts down. Detachment may be intentional for process-lifetime telemetry, but then another owner must define failure observation and shutdown.

Calling `abort` schedules cancellation. The task is cancelled when it next reaches a point where the runtime can stop polling and drop the future. Synchronous code between await points is not preempted. Destructors for future-owned fields run when the future is dropped; external effects remain.

Await the handle after abort when shutdown requires proof that the task has reached a terminal state.

### `JoinSet` is a dynamic child owner

A `JoinSet<T>` owns a dynamic set of spawned tasks and yields terminal outcomes as they finish. It is useful when the number of children is discovered at runtime. It does not automatically provide a complete failure policy. You still decide:

- whether one failure cancels siblings;
- whether all terminal results are drained;
- how panics are translated;
- whether new children may be spawned during shutdown;
- how long draining may continue;
- what happens after the grace period.

Dropping a `JoinSet` aborts its tasks, which can be a useful final cleanup guarantee but should not substitute for an explicit drain-and-abort sequence.

### The task-tree ledger

Represent the service as a tree even when Tokio does not enforce a lexical scope:

| Task | Parent owner | Spawn reason | Owned resources | Cancellation source | Join owner | Terminal policy |
|---|---|---|---|---|---|---|
| TCP accept loop | service supervisor | service admission | listener, connection permits | service token | supervisor | stop on shutdown; report fatal accept error |
| connection 17 | connection set | accepted peer | socket, permit, broker client | child token | connection set | contain protocol error; report panic |
| broker | service supervisor | state authority | receiver, idempotency map | service token | supervisor | fatal if unexpectedly exits |
| job 42 | broker job set | execute accepted request | owned request, permit | job token | broker | cache terminal outcome |
| health server | service supervisor | operational HTTP surface | listener, state reader | service token | supervisor | fatal bind/serve error |

The tree answers “who joins this?” before the question becomes a leak.

### Structured concurrency is a lifecycle property

A structured async operation has these properties:

- child work starts within an owning parent operation;
- child lifetime does not silently exceed the owner’s intended scope;
- cancellation reaches descendants;
- all terminal outcomes are observed or deliberately classified as ignorable;
- cleanup completes before the owner reports completion.

This can be implemented with `JoinSet`, explicit handle vectors, cancellation tokens, task groups, or carefully designed channel ownership. The mechanism is secondary to the lifecycle proof.

### Non-`Send` work belongs on a local executor only when locality is meaningful

`LocalSet` and `spawn_local` allow futures that are not `Send`, such as those using `Rc` or thread-affine state. This is not a way to avoid understanding why a future is non-`Send`. First diagnose the retained value. Use a local executor when the resource is genuinely thread-local or an API requires affinity.

A local task is still concurrent. `RefCell` reentrancy, cancellation, task leakage, and lifecycle obligations remain. “Single thread” removes cross-thread movement, not logical races or borrow panics.

### Blocking work must cross an explicit boundary

A blocking filesystem call, native library call, compression loop, or expensive parse can monopolize an async worker. `spawn_blocking` moves a synchronous closure to a separate blocking pool. The closure should own its inputs and return owned outputs.

The boundary has three important limits:

1. Once the blocking closure begins, aborting the async wrapper does not preempt arbitrary synchronous code.
2. The blocking pool can grow substantially; CPU-heavy submissions still need a semaphore or dedicated bounded pool.
3. Runtime shutdown may wait for blocking work according to runtime policy, so an unbounded or stuck native call remains a shutdown risk.

For short CPU work, measure before adding complexity. For large partitionable work, Course 7’s Rayon model may be more appropriate. For cancellable CPU work, the function must cooperate by checking a cancellation flag or processing bounded chunks.

### Runtime ownership belongs near the process boundary

Avoid creating nested runtimes inside library functions. A library should generally expose async functions and let the application choose the runtime. Constructing or blocking a runtime from code already running inside one can panic, deadlock, or fragment resource policy.

The binary or top-level application owns:

- runtime flavor and worker count;
- startup configuration;
- signal handling;
- service task tree;
- blocking boundaries;
- shutdown deadline;
- final exit status.

Libraries own future behavior, not the process’s executor policy.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For distinguish a runtime, worker thread, task, future, reactor, and blocking pool, construct one positive and one causal negative example. Mark the first decisive fact in the **task ownership tree** and state which evidence could falsify the claim.

2. **Outcome 2.** For explain the `Send + 'static` requirements of ordinary multi-threaded task spawning, construct one positive and one causal negative example. Mark the first decisive fact in the **task ownership tree** and state which evidence could falsify the claim.

3. **Outcome 3.** For derive when a task should borrow through an enclosing async scope versus own cloned or moved data, construct one positive and one causal negative example. Mark the first decisive fact in the **task ownership tree** and state which evidence could falsify the claim.

4. **Outcome 4.** For use `JoinHandle` and `JoinSet` as explicit result, panic, cancellation, and cleanup obligations, construct one positive and one causal negative example. Mark the first decisive fact in the **task ownership tree** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

The following nursery runs tasks, records all outcomes, and supports a fail-fast policy without abandoning joins. It uses `JoinSet` as the dynamic child owner.

```rust
use std::future::Future;
use tokio::task::{JoinError, JoinSet};
use tokio_util::sync::CancellationToken;

#[derive(Debug, PartialEq, Eq)]
pub enum Outcome<T, E> {
    Completed(T),
    Failed(E),
    Panicked,
    Cancelled,
}

pub async fn run_group<I, F, T, E>(
    tasks: I,
    fail_fast: bool,
) -> Vec<Outcome<T, E>>
where
    I: IntoIterator<Item = F>,
    F: Future<Output = Result<T, E>> + Send + 'static,
    T: Send + 'static,
    E: Send + 'static,
{
    let cancellation = CancellationToken::new();
    let mut set = JoinSet::new();

    for task in tasks {
        let child = cancellation.child_token();
        set.spawn(async move {
            tokio::select! {
                result = task => Some(result),
                () = child.cancelled() => None,
            }
        });
    }

    let mut outcomes = Vec::new();
    while let Some(joined) = set.join_next().await {
        match classify(joined) {
            Outcome::Failed(error) if fail_fast => {
                cancellation.cancel();
                outcomes.push(Outcome::Failed(error));
            }
            outcome => outcomes.push(outcome),
        }
    }
    outcomes
}

fn classify<T, E>(
    joined: Result<Option<Result<T, E>>, JoinError>,
) -> Outcome<T, E> {
    match joined {
        Ok(Some(Ok(value))) => Outcome::Completed(value),
        Ok(Some(Err(error))) => Outcome::Failed(error),
        Ok(None) => Outcome::Cancelled,
        Err(error) if error.is_cancelled() => Outcome::Cancelled,
        Err(_) => Outcome::Panicked,
    }
}
```

This example deliberately leaves result ordering as completion order. A product requiring source order must attach stable indices. It also does not preempt a child that never yields. Cancellation is cooperative. The nursery drains the set after cancellation so every task reaches a terminal observed state.

## Practice sequence

1. Draw the runtime components and identify which product decisions they do not make.
2. Diagnose a `tokio::spawn` error by listing every value live across `.await`.
3. Rewrite a detached spawn loop as an owned `JoinSet` with complete draining.
4. Classify domain failure, panic, and cancellation separately.
5. Move a synchronous parse or native call through `spawn_blocking` and bound admission.
6. Implement a task nursery with complete-all and fail-fast modes.
7. Write a task-tree ledger for JobWire.
8. Explain why abort plus dropping the handle is weaker than abort plus awaiting terminal completion.

## Ready to continue

Continue only when you can state:

- who owns every spawned task;
- why `Send + 'static` appears at the spawn boundary;
- which task outcomes are domain values and which are runtime failures;
- why dropping a handle detaches rather than cancels;
- why blocking isolation still requires capacity policy;
- how shutdown reaches, aborts, and joins every child.

## Primary Rust references

- Tokio runtime and task modules;
- Tokio `JoinHandle`, `JoinSet`, `LocalSet`, and `spawn_blocking` documentation;
- Tokio-util `CancellationToken` documentation;
- Rust standard-library `Future` and `Send` contracts from Modules 61 and 71.

## Continue

Continue to [Module 73 — Async I/O, Buffers, Streams, and Framing](../module-73-async-io-buffers-streams-and-framing/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
