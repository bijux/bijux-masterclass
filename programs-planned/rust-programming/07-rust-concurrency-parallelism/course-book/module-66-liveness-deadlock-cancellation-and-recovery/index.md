# Module 66: Liveness: Deadlock, Cancellation, and Recovery

**Course 7, day 6 · Module 66 of 90**  

**66/90** · [Course overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [BatchWeave guide](../capstone.md)

## The question

> Why can every blocked operation eventually continue or terminate, and what happens when cancellation, panic, or partial infrastructure failure interrupts the normal path?

## Why this comes now

The first five modules established safe ownership, structured lifetime, protected invariants, waiting predicates, and message protocols. None automatically proves progress. A system can be data-race free, preserve every invariant, and wait forever. Liveness must be reviewed as carefully as safety.

This module gives concrete methods: wait-for graphs for deadlock, progress classes for waiting operations, cancellation wake paths, idempotent shutdown, panic containment, and terminal accounting. It also corrects a recurring design mistake: a cancellation flag is only information. A thread blocked on a condition variable or channel needs an event that makes it re-evaluate that information.

This module is not complete when you can name the primitive. It is complete when you can state the ownership transfer, the synchronization edge, the progress argument, the failure behavior, and the schedule-dependent facts that remain intentionally unspecified.

## What you will be able to do

- distinguish deadlock, starvation, livelock, priority inversion, and slow work;
- construct a wait-for graph over locks, channels, joins, barriers, and conditions;
- state a global lock order and identify operations that violate it;
- design cancellation as state plus a wake mechanism plus an observation point;
- make shutdown idempotent and safe under concurrent callers;
- contain worker panic without abandoning joins or losing accepted jobs;
- prove one terminal outcome or one explicit run-level explanation for every accepted job;
- write event-driven liveness tests and bounded test timeouts without mistaking timeout for the production protocol.

## Core model

### Safety and liveness are different proof dimensions

Safety says something bad never occurs: no invalid state, double free, data race, duplicate outcome, or capacity overflow. Liveness says something good eventually occurs: a blocked producer proceeds or learns closure, every worker terminates, every accepted job receives a terminal status, and shutdown returns.

A correct concurrent product needs both. A mutex can preserve an invariant forever while two threads deadlock. A cancellation flag can remain correctly set while a sleeping worker never wakes to see it.

### Wait-for graphs expose cycles

Represent threads or tasks as active nodes and resources/conditions as dependencies. Add an edge when one waits for another:

```text
T1 → lock B
lock B → T2
T2 → result capacity
result capacity → T1
```

A cycle is a deadlock candidate. Not every cycle is reachable, so annotate the state and acquisition order that creates each edge. Include non-lock resources: bounded channel capacity, join dependencies, barriers, queue predicates, and callbacks that re-enter the caller.

A global lock order eliminates cycles only for locks included in the order and only when all operations obey it. Never acquire a lower-ranked lock while holding a higher-ranked one. Dynamic resource sets may use stable IDs to establish order.

### Starvation and livelock have no fixed cycle

Starvation occurs when one operation remains enabled but is repeatedly denied service. Livelock occurs when participants keep changing state but fail to complete, such as two polite retry loops continually yielding to each other. Priority inversion occurs when a high-priority thread waits on work held by a lower-priority thread, potentially delayed by unrelated medium-priority work.

Rust’s standard locks do not promise a universal fairness policy. Avoid product correctness that depends on fair acquisition. Bounded retries, explicit queues, or single-owner protocols can make progress rules clearer.

### Cancellation needs state, wake, and checkpoint

A robust cancellation protocol has three parts:

1. **state:** an atomic flag or protected lifecycle enum records cancellation;
2. **wake:** closing a queue, notifying a condition variable, or disconnecting a channel releases blocked operations;
3. **checkpoint:** workers inspect cancellation before taking more work and at safe points in long computation.

Missing any part breaks liveness. A flag without wake leaves sleepers blocked. A notification without durable state can be missed. A state and wake without checkpoints lets long work ignore cancellation indefinitely.

Cancellation is usually cooperative. State the maximum granularity at which an operation observes it.

### Shutdown should be idempotent

More than one path may initiate shutdown: normal completion, the first domain failure under fail-fast policy, a worker panic, coordinator error, or explicit cancellation. The transition should be safe when called repeatedly:

```text
Running → Cancelling → Closed → Joined
```

Repeated cancellation keeps the state at or beyond `Cancelling`. Repeated queue close does not panic. Joining remains owned by one coordinator so handles are consumed exactly once. Idempotence reduces races among failure paths.

### Panic containment has a boundary

`catch_unwind` can translate a panic into a typed worker outcome when code is unwind-safe and the product chooses containment. It is not a universal recovery mechanism: process abort configuration bypasses unwinding, panic payloads are not stable diagnostics, and invariants may have been interrupted.

Catch panic around the smallest job-execution boundary, after the job has left the queue and before a terminal outcome is sent. Do not catch around queue internals and then continue without checking their invariants. The worker thread can survive one job panic only if its reusable state remains valid.

### Terminal accounting closes the semantic loop

Accepted jobs must not disappear because submission stopped or a worker died. Use stable indices and define exactly one terminal category:

```text
Completed | DomainFailed | Panicked | Cancelled
```

The coordinator rejects duplicates. After queues close, channels drain, and workers join, any missing accepted job becomes an explicit infrastructure fault or cancelled outcome according to policy. This reconciliation is essential because channel disconnect and thread join alone do not map lifecycle back to product identities.

### Tests should establish events, then bound hangs

Use barriers and channels to establish that an operation has reached a waiting point. Trigger the enabling or cancelling event, then assert termination and invariant preservation. A test-level timeout is useful to prevent the suite from hanging forever, but it is not the production liveness protocol and should not become a sleep-based ordering assertion.

For deadlock-prone code, isolate the scenario in a subprocess when possible so a hung thread cannot block the entire test process. Course 9 will add systematic tooling and stress methodology; here the focus is causal protocol tests.

### Write a termination argument

For a finite worker engine, a useful proof is:

- accepted job count is finite and bounded;
- submission either enqueues a job or records it as not accepted/cancelled;
- close wakes blocked queue operations;
- each worker loop either obtains a job, observes closed-empty, or records infrastructure failure;
- each obtained job leads to exactly one terminal outcome despite domain error or panic;
- result reception ends after all sender clones drop;
- every handle is joined once;
- reconciliation terminates over a finite indexed vector.

This is stronger than “workers exit when the channel closes” because it covers every obligation and failure path.

## Use the idea in a complete program

This worker loop shows cancellation as state plus queue closure plus checkpoints. It contains panic at the job boundary and always emits a terminal outcome for a job it has popped:

```rust
use std::panic::{self, AssertUnwindSafe};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::mpsc::Sender;
use std::sync::Arc;

#[derive(Debug)]
pub enum JobOutcome {
    Completed { index: usize, value: String },
    Failed { index: usize, message: String },
    Panicked { index: usize },
    Cancelled { index: usize },
}

pub trait WorkQueue<T>: Send + Sync {
    fn pop(&self) -> Option<T>;
    fn close(&self);
}

pub fn worker_loop<Q, F>(
    queue: Arc<Q>,
    cancelled: Arc<AtomicBool>,
    results: Sender<JobOutcome>,
    fail_fast: bool,
    execute: F,
) where
    Q: WorkQueue<(usize, String)> + 'static,
    F: Fn(&str) -> Result<String, String>,
{
    while let Some((index, input)) = queue.pop() {
        if cancelled.load(Ordering::Relaxed) {
            let _ = results.send(JobOutcome::Cancelled { index });
            continue;
        }

        let outcome = match panic::catch_unwind(AssertUnwindSafe(|| execute(&input))) {
            Ok(Ok(value)) => JobOutcome::Completed { index, value },
            Ok(Err(message)) => {
                if fail_fast {
                    cancelled.store(true, Ordering::Relaxed);
                    queue.close();
                }
                JobOutcome::Failed { index, message }
            }
            Err(_) => {
                cancelled.store(true, Ordering::Relaxed);
                queue.close();
                JobOutcome::Panicked { index }
            }
        };

        if results.send(outcome).is_err() {
            cancelled.store(true, Ordering::Relaxed);
            queue.close();
            break;
        }
    }
}
```

The relaxed cancellation flag is not the wake mechanism. `queue.close()` updates protected queue state and notifies blocked operations; the flag is a fast shared observation. Its ordering can remain relaxed because no other data is published through it. Later modules will teach that this is a proof, not a default incantation.

A popped job always receives an outcome even if cancellation was already requested. Domain failure under fail-fast closes the queue. Queued jobs can still be popped and marked cancelled according to the queue’s drain-on-close policy. Jobs that were never successfully enqueued remain the coordinator’s responsibility and must be reconciled.

The code ignores a failed result send only after converting it into cancellation and queue close. The full engine still joins workers. Panic containment assumes `execute` does not leave reusable worker-local state invalid; the capstone keeps execution functions stateless.

## Practice sequence

1. Draw wait-for graphs containing locks, bounded channels, joins, and barriers.
2. Distinguish deadlock, starvation, livelock, and ordinary slow work.
3. Add wake and checkpoints to a flag-only cancellation design.
4. Make shutdown transitions idempotent.
5. Contain a job panic without skipping terminal accounting.
6. Write a finite termination argument for a worker engine.
7. Complete Cancellable Worker Group and implement BatchWeave fail-fast behavior.

The corresponding independent product is [Cancellable Worker Group](../../labs/module-06-cancellable-worker-group/README.md). The same reasoning then changes one explicit invariant in [BatchWeave](../capstone.md).

## Ready to continue

Continue only when you can do all of the following without using the chapter as a script:

- construct a wait-for graph and identify a reachable cycle;
- state cancellation state, wake event, and checkpoints;
- explain why a relaxed flag can be correct when closure carries wakeup;
- account for every accepted job after panic or cancellation;
- write a shutdown sequence that is safe when initiated twice.

## Primary Rust references

- [`catch_unwind`](https://doc.rust-lang.org/std/panic/fn.catch_unwind.html)
- [`UnwindSafe`](https://doc.rust-lang.org/std/panic/trait.UnwindSafe.html)
- [`AtomicBool`](https://doc.rust-lang.org/std/sync/atomic/struct.AtomicBool.html)
- [`JoinHandle`](https://doc.rust-lang.org/std/thread/struct.JoinHandle.html)
- [`std::sync` overview](https://doc.rust-lang.org/std/sync/index.html)

The course book is self-contained. These references are for checking the exact library contract and following changes in the language or standard library; they are not substitutes for the reasoning developed above.

## Continue

[Open the workbook](workbook.md) · [Open Cancellable Worker Group](../../labs/module-06-cancellable-worker-group/README.md) · [Open the BatchWeave increment](../capstone.md) · [Review the reasoned solutions](solutions.md)
