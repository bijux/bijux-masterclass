# Module 71: Futures, Polling, Wakers, and Async State Machines

**Course 8, day 1 · Module 71 of 80**

**71/80** · [Course overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [JobWire guide](../capstone.md)

## The question

> What exactly is an async computation before a runtime executes it, what must happen when it cannot complete, and what state remains when it is suspended or cancelled?

## Why this comes now

Course 7 taught that a concurrent program is a set of possible schedules and that every worker needs an ownership, progress, failure, and shutdown story. Async Rust keeps those obligations but changes the execution unit. An OS thread may block while waiting. An async task must instead return control to an executor so that the same runtime worker can advance other tasks.

The syntax is deceptively small: `async fn` and `.await`. The mechanism is not. An async function call creates a future. The body does not run merely because the future exists. The future is a state machine that an executor repeatedly polls. When it cannot finish, it returns `Pending` and must arrange for a useful future wakeup. Values that remain live across `.await` are stored in that state machine. Dropping it destroys that stored state and is the ordinary cancellation mechanism.

Without this model, later APIs become rituals. A reader may add `tokio::spawn`, `timeout`, or `select!` without knowing which future is dropped, whether a partially completed write survives, why a task spins, or why a borrowed value cannot move after the future has started. This module makes the mechanism explicit before a runtime hides the polling loop.

## What you will be able to do

- explain why a future is inert until polled;
- read the `Future::poll` contract and distinguish completion from scheduling;
- state what `Context` and `Waker` permit without treating wake as a stored event count;
- identify busy polling caused by unconditional self-waking;
- derive the state stored across suspension points in an `async fn`;
- explain why futures may become self-referential after polling and why `Pin` appears in the trait signature;
- distinguish `Unpin` from “safe to use asynchronously”;
- analyze cancellation as destruction of an incomplete state machine;
- implement a one-shot future with correct waker replacement and race handling;
- produce a future-state ledger for a larger operation.

## Core model

### Calling an async function constructs a value

Consider:

```rust
async fn fetch_total() -> u64 {
    println!("started");
    42
}

fn main() {
    let future = fetch_total();
    drop(future);
}
```

The message is not printed. Calling an async function constructs a value implementing `Future`; it does not execute the body to completion. This separation is essential because the executor, not the function call, decides when and where the computation is advanced.

A useful first sentence is:

> A future is a value that remembers enough state to continue a computation when polled again.

The value may initially represent “not started.” After one poll it may represent “waiting for socket readability with these local variables retained.” Later it may represent “response parsed, waiting to enqueue work.” Finally it becomes complete.

### `poll` is a cooperative state transition

The core trait can be read conceptually as:

```rust
trait Future {
    type Output;

    fn poll(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>,
    ) -> Poll<Self::Output>;
}
```

A poll attempt may produce:

```text
Ready(output)  terminal completion
Pending        incomplete now; arrange a future wakeup
```

`Pending` does not mean “please poll me immediately.” It means the future has registered interest in an event or otherwise ensured that the owning task will be woken when another poll may make progress. Returning `Pending` without a wake source can stall forever. Waking unconditionally before every `Pending` creates a busy loop that consumes executor capacity without external progress.

The executor owns the outer loop. A simplified conceptual loop is:

```text
mark task ready
while task exists:
    when ready:
        clear ready flag
        poll future
        if Ready: store result and destroy task
        if Pending: wait until a wake marks it ready again
```

Real executors optimize scheduling and may coalesce repeated wakeups. The contract does not promise one poll per wake or one wake per event. A waker says “polling may now be useful,” not “one event has been deposited.”

### The latest waker matters

A future can be moved between tasks before being pinned and polled, and executors may provide a different waker on a later poll. A custom future that stores a waker should generally replace an older one when the incoming waker would wake a different task.

The robust pattern is:

1. lock or otherwise access the shared state;
2. check whether the result is already available;
3. store or replace the current waker;
4. check the state again when the producer can race with registration;
5. return `Pending` only when a producer still owns a path to wake the task.

The exact double-check depends on the synchronization design. The governing invariant is more important than a copied code pattern:

> If `poll` returns `Pending`, either the completion event has not happened and a future wake is arranged, or a race has been detected and the result is returned immediately.

### Wakeups are hints, not counters

Suppose a producer calls `wake_by_ref` three times before the executor polls. The executor is permitted to poll once. Suppose the future is polled spuriously; it must still check its state rather than assume an event occurred. Therefore protocol data cannot live only in wake counts. Store the actual state—bytes available, result ready, cancellation requested—in synchronized memory or in the I/O driver. The waker only connects that state change to scheduling.

This distinction prevents a common incorrect design:

```text
producer increments no state, only calls wake
consumer interprets each poll as one produced item
```

Wake coalescing loses the imagined count. The repaired design queues or counts items explicitly, then wakes the consumer.

### `.await` composes polling

An `.await` expression conceptually polls a child future. If the child is ready, execution continues. If it is pending, the outer future stores the continuation state and itself returns `Pending`. The same task waker flows down through the composed future graph.

For this function:

```rust
async fn exchange(mut stream: Stream) -> Result<Response, Error> {
    let request = build_request();
    stream.write_all(&request).await?;
    let header = read_header(&mut stream).await?;
    let body = read_body(&mut stream, header.length).await?;
    validate(header, body)
}
```

The generated state machine must retain different values at different suspension points. After the write, it still owns `stream`. While reading the body, it owns `stream`, `header`, and the in-progress child future. `request` may no longer be live. This liveness affects future size, auto traits, borrowing, and cancellation.

### Values across `.await` determine `Send`

A future returned by an async block is `Send` only when the values retained across suspension points permit transfer. A non-`Send` temporary that is created and dropped before `.await` may not prevent the future from being `Send`. The same value held across `.await` becomes part of the suspended state and can make `tokio::spawn` reject the future.

This is not an arbitrary runtime rule. A multi-threaded executor may resume the task on another worker thread. Every retained field must therefore satisfy the required transfer contract.

When diagnosing a non-`Send` future, do not add `Send` bounds blindly. Find the exact value live across the suspension point. Often the correct repair is to shorten a lock guard or `Rc` borrow before `.await`, return owned data from a synchronous helper, or use a local task when the non-`Send` design is intentional.

### Why `Pin<&mut Self>` appears

The compiler-generated future may contain references into its own stored state. For example, an outer state may own a buffer while an in-progress child future borrows that buffer. Moving the outer future after those internal references are established could invalidate them.

`Pin<&mut Self>` means that polling code may rely on the future not being moved out of its pinned location unless the type is `Unpin`. Most ordinary async users do not manually project pinned fields; `.await`, `Box::pin`, executor task storage, and pin-aware combinators handle this boundary. Course 2 established the pinning contract. Here the important consequence is:

> Do not interpret a future as an ordinary mutable struct that may always be replaced or moved after polling begins.

`Unpin` is an auto trait saying that pinning adds no movement restriction for that type. It does not say the future is complete, cancel-safe, `Send`, or thread-safe.

### Polling after completion is outside the ordinary contract

Once a future returns `Ready`, its work is complete. Polling it again is not a general-purpose restart operation. Individual future types may panic, return a repeated value, or document another behavior, but callers must not depend on repolling unless the type explicitly permits it. Combinators such as fused futures add a separate post-completion contract.

The executor normally removes a completed task. A custom test harness should do the same.

### Cancellation is drop

There is no universal “cancel method” on `Future`. If a future loses a race in `select!`, a timeout expires, a task is aborted, or an owning scope is dropped, the incomplete future is usually destroyed. Its fields’ destructors run. External side effects already performed do not roll back automatically.

Cancellation analysis therefore asks:

1. Which state has already changed outside the future?
2. Which state is stored inside and will be dropped?
3. Is another task or peer waiting for a message that will never arrive?
4. Can the operation be retried without duplication or corruption?
5. Is there a commit point after which the result must be recovered rather than restarted?

A pure sleep is easy to cancel. A partially written protocol frame may not be. A broker request sent through a channel may commit after the caller times out. Later modules turn these observations into explicit protocols.

### The future-state ledger

For each significant async operation, record:

| State | Stored values | Awaited event | Wake source | External effects already possible | Drop behavior |
|---|---|---|---|---|---|
| Start | configuration, socket | none | initial scheduling | none | close socket |
| Writing | socket, remaining frame | writable readiness | I/O driver | prefix may be visible | close; peer sees truncation |
| Awaiting reply | socket, request id | readable readiness | I/O driver | request may be committed | close; outcome may be ambiguous |
| Complete | response | none | none | committed response known | ordinary drop |

This ledger reveals cancellation and retry questions before code obscures them.

## Use the idea in a complete program

The following one-shot signal is intentionally small enough to inspect. One producer completes it once; one future awaits the value. It uses a mutex because the point is the polling contract, not a custom lock-free primitive.

```rust
use std::{
    future::Future,
    pin::Pin,
    sync::{Arc, Mutex},
    task::{Context, Poll, Waker},
};

#[derive(Default)]
struct State<T> {
    value: Option<T>,
    waker: Option<Waker>,
    receiver_alive: bool,
}

pub struct Sender<T> {
    state: Arc<Mutex<State<T>>>,
}

pub struct Receiver<T> {
    state: Arc<Mutex<State<T>>>,
}

pub fn channel<T>() -> (Sender<T>, Receiver<T>) {
    let state = Arc::new(Mutex::new(State {
        value: None,
        waker: None,
        receiver_alive: true,
    }));
    (
        Sender { state: Arc::clone(&state) },
        Receiver { state },
    )
}

impl<T> Sender<T> {
    pub fn send(self, value: T) -> Result<(), T> {
        let waker = {
            let mut state = self.state.lock().expect("signal state poisoned");
            if !state.receiver_alive || state.value.is_some() {
                return Err(value);
            }
            state.value = Some(value);
            state.waker.take()
        };
        if let Some(waker) = waker {
            waker.wake();
        }
        Ok(())
    }
}

impl<T> Future for Receiver<T> {
    type Output = T;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<T> {
        let mut state = self.state.lock().expect("signal state poisoned");
        if let Some(value) = state.value.take() {
            return Poll::Ready(value);
        }
        let replace = state
            .waker
            .as_ref()
            .is_none_or(|stored| !stored.will_wake(cx.waker()));
        if replace {
            state.waker = Some(cx.waker().clone());
        }
        Poll::Pending
    }
}

impl<T> Drop for Receiver<T> {
    fn drop(&mut self) {
        let mut state = self.state.lock().expect("signal state poisoned");
        state.receiver_alive = false;
        state.waker = None;
    }
}
```

The code still has design choices worth naming. Poisoning is treated as unrecoverable in this teaching implementation. There is exactly one receiver and one send attempt because `send` consumes the sender. Receiver cancellation is communicated so the producer can recover its value. The waker is extracted before waking so user scheduling does not occur while the mutex is held.

A stronger implementation would test producer/drop races, repeated polls before completion, replacement with a distinct waker, and completion before the first poll. The laboratory builds that evidence.

## Practice sequence

1. Draw the state machine for an async function with two `.await` points and one early error.
2. Identify every local live across each suspension point.
3. Predict whether the resulting future is `Send` when one local is `Rc<String>`.
4. Repair a future that holds a `MutexGuard` across `.await` without changing the mutex to an async mutex mechanically.
5. Implement a one-shot future and test the producer-before-poll and poll-before-producer schedules.
6. Write a cancellation ledger for a request that writes a frame and then waits for a reply.
7. Explain why waking is not equivalent to completing or queueing one event.
8. Transfer the model into JobWire’s connection handshake.

## Ready to continue

Continue only when you can explain, without API names:

- why an async function call is inert;
- what must be true before `poll` returns `Pending`;
- why the latest waker may replace an older one;
- which values become fields of the suspended state machine;
- why cancellation destroys local state but does not undo external effects;
- why pinning is part of polling without being a general async-safety marker.

## Primary Rust references

- Rust standard library: `std::future::Future`, `std::task::{Context, Poll, Waker}`;
- Rust standard library: `std::pin::Pin` and `Unpin`;
- The Rust Reference and Async Book sections describing async blocks and generated futures;
- Tokio documentation for task scheduling and cancellation, used from Module 72 onward.

## Continue

Complete the [workbook](workbook.md), use the [reasoned solutions](solutions.md) only after freezing your own answer, build [One-Shot Signal](../../labs/module-01-one-shot-signal/README.md), and add the first [JobWire increment](../capstone.md#increment-1-freeze-the-async-state-vocabulary). Then continue to [Module 72](../module-72-tokio-runtimes-tasks-and-structured-async-lifecycles/index.md).
