# Reasoned Solutions — Module 71: Futures, Polling, Wakers, and Async State Machines

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the JobWire guide](../capstone.md)

The central correction is that async syntax does not create autonomous execution. It creates state that an executor advances cooperatively. Every correct answer connects stored state, wake source, poll result, and destruction behavior.

## Part 1 — Prediction solutions

1. No print occurs. Constructing and dropping the future never polls it, so the body does not begin.
2. The task remains continuously runnable and is likely polled repeatedly, consuming executor time without external progress. The future has built a busy loop.
3. If the future is later polled by a task with a different waker, the producer can wake the obsolete task. The current owner may never be scheduled. Replace when `will_wake` is false.
4. Yes, provided the `Rc` truly does not remain live across the suspension point. It need not become a stored field of the suspended future.
5. The future retains a non-`Send` field across suspension and cannot satisfy a multi-threaded spawn boundary requiring `Send`.
6. No. Some prefix may already have reached the socket or peer. Drop cleans local state; it does not reverse external I/O.
7. No general future contract grants repeat polling after `Ready`. Treat completion as terminal unless a specific type documents otherwise.
8. Waking may schedule immediate polling on another thread. Unlocking first avoids reentrant contention and keeps executor activity outside the critical section.

## Part 2 — Repair reasoning

Wake calls cannot represent protocol count because they may be coalesced and polls may be spurious. Store the count in synchronized state. The producer increments the count and wakes when a waiter exists. `poll` reads the count; if the terminal condition is false, it stores the current waker and returns `Pending`. Completion is a state transition, not the tenth scheduling event.

For the guard defect, the strongest ordinary repair is usually:

```text
lock → copy or move the needed owned data → unlock → await
```

This keeps a synchronous lock’s critical section non-suspending and allows the future to be `Send` when the owned data is. A `LocalSet` repair is appropriate only when thread-local state is an intentional architectural choice. Replacing the mutex with an async mutex permits waiting without blocking a runtime worker, but it may also preserve an overly large critical section, create head-of-line blocking, or hide that no shared mutable state was needed.

## Part 3 — Focused exercise guidance

### Exercise 1

The state list should separate connect, first write, challenge read, response computation, second write, and verdict read. Pure computation with no await is part of the transition between states. Only locals live after a suspension point are retained. The socket survives throughout; credentials may be dropped after the first write; challenge data survives until the response is computed.

### Exercise 2

A defensible invariant is: before returning `Pending`, the future has observed that no terminal value exists and has installed a waker that the producer will take or clone after publishing the terminal state. If publication races with registration, one side must observe the other through the same synchronization mechanism so completion cannot occur without either returning `Ready` or scheduling another poll.

### Exercise 3

The proof should use a type-level helper such as `fn assert_send<T: Send>(_: T) {}`. The point is not Tokio. It is whether retained fields make the generated future transferable.

### Exercise 4

Reserving an ID may be reversible if it is only local, but once the request is visible to a remote server, timeout creates an ambiguous commit. Retrying requires an idempotency key or a status-recovery protocol. The ledger must distinguish local destructor cleanup from remote state.

### Exercise 5

The stored first waker should be replaced when the second would wake a different task. On completion, take the current waker while locked, publish the value, unlock, then wake. A test that only counts total wakes is weaker than one proving which waker received the call.

## Part 4 — Laboratory comparison

A strong one-shot implementation has one authoritative state, one completion transition, and one receiver-cancellation transition. It never interprets polling frequency as data. It handles producer-before-poll and poll-before-producer symmetrically. It updates the waker and does not call arbitrary scheduling behavior while holding the internal lock.

## Part 5 — Capstone comparison

The JobWire ledger should reveal two important facts before code exists. First, a request may be committed by the broker after the connection task stops waiting. Second, dropping a connection task must release its reply receiver and connection permit, but it must not corrupt broker-owned work. These facts motivate idempotency and explicit task ownership in later modules.

## Part 6 — Reconstruction and defense

A complete defense says that `poll` is a cooperative attempt, `Pending` carries a wake obligation, and the waker schedules rather than stores application events. It identifies values retained across await, states that pinning protects movement-sensitive future state, and explains cancellation as destruction at an arbitrary incomplete state. The strongest answer always names external effects that destructors cannot roll back.
