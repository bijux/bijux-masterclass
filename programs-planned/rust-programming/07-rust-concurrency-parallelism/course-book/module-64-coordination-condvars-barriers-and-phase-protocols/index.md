# Module 64 — Coordination: Condvars, Barriers, and Phase Protocols

**Course 7 · Day 4 · Module 64 of 100**
`████████████████░░░░░░░░░` **64/100**

[Program](../../../README.md) · [Course 7](../index.md) · [Workbook](workbook.md) · [Laboratory](../../labs/module-04-phase-gate/README.md) · [BatchWeave guide](../capstone.md)

[← Module 63: Shared State: Locks and Protected Invariants](../module-63-shared-state-locks-and-protected-invariants/index.md) · [Module 65: Message Passing, Backpressure, and Shutdown →](../module-65-message-passing-backpressure-and-shutdown/index.md)

## The question

> How do threads wait for a state predicate or phase transition without polling, lost wakeups, or treating notification itself as truth?

## Why this comes now

Module 63 built protected transitions but returned `WouldBlock` when a queue was full or empty. Real worker systems often need to wait efficiently until another thread changes the state. A condition variable connects a wait to a mutex-protected predicate. A barrier coordinates a known cohort at a phase boundary. `OnceLock` publishes a value exactly once.

These mechanisms are frequently mislearned as signal APIs: one thread calls `notify`, another wakes, and work continues. That model is unsafe. Notifications carry no durable truth, wakeups may be spurious, and the relevant state may change again before a waiter reacquires the mutex. The predicate under the lock is the protocol; notification only prompts re-evaluation.

This module is not complete when you can name the primitive. It is complete when you can state the ownership transfer, the synchronization edge, the progress argument, the failure behavior, and the schedule-dependent facts that remain intentionally unspecified.

### Prerequisite bridge

Module 63 established **Shared State: Locks and Protected Invariants**. Before continuing, verify that you can design concurrent tests around preserved invariants rather than exact schedules. This module preserves that capability and adds the ability to write every condition-variable wait as a predicate loop over mutex-protected state;. Module 65, **Message Passing, Backpressure, and Shutdown**, will rely on both when it asks: *Which values cross ownership boundaries, how is capacity bounded, and which explicit protocol event proves that every sender, receiver, and worker can terminate?*

### Scope boundary

This module owns the reasoning for **coordination: condvars, barriers, and phase protocols** inside Course 7. The course uses operating-system threads and Rayon. Async runtimes, sockets, network protocols, and async cancellation remain Course 8 topics. Lock-free code is taught as a proof exercise, not as a default replacement for locks and channels. The purpose of the boundary is to keep the decisive relationship visible before later mechanisms are layered on top of it.

## What you will be able to do

- write every condition-variable wait as a predicate loop over mutex-protected state;
- explain the atomic unlock-and-wait transition and why it prevents the ordinary lost-wakeup window;
- distinguish `notify_one` and `notify_all` by which state transition can enable which waiters;
- design bounded-buffer `not_empty`, `not_full`, and closure predicates;
- use barriers only for known cohorts and explicit phase transitions;
- use `OnceLock` for one-time publication without turning it into a general mutable global;
- handle timeout as a return from waiting that still requires predicate re-evaluation;
- test coordination through causal handshakes rather than sleep-based scheduling assumptions.

## Core model

### The predicate is the source of truth

A consumer waits for:

```text
buffer is not empty OR queue is closed
```

It does not wait for “a producer notification.” The producer may notify before the consumer begins waiting; another consumer may take the item first; or the wait may return spuriously. Therefore the consumer holds the mutex, checks the predicate, and loops:

```rust
while state.buffer.is_empty() && !state.closed {
    state = condvar.wait(state)?;
}
```

After the loop, state itself determines whether to pop an item or terminate. Notification is not stored data.

### Wait atomically releases and reacquires the mutex

A naive protocol checks a predicate, unlocks, and then sleeps. Another thread can make the predicate true and notify between unlock and sleep, leaving the waiter asleep despite available work. `Condvar::wait` performs the release-and-block operation as one synchronization action with respect to the associated mutex. On return it reacquires the mutex before exposing the guard.

All waits for one condition variable should use the mutex that protects its predicate. Mixing mutexes destroys the protocol and may panic according to the platform/library implementation.

### Spurious wakeups are part of the contract

A wait may return even though no relevant state transition occurred. This is not an exceptional edge case; it is why the predicate loop is mandatory. The loop also handles competition: a notification can wake two threads, one consumes the available item, and the other finds the predicate false again.

`wait_while` can express the same model, but understand the loop before using the convenience API. The closure names the condition under which waiting continues, not the event being awaited.

### A bounded queue usually has two enabling conditions

Producers wait while the buffer is full and not closed. Consumers wait while the buffer is empty and not closed. A successful push may enable a consumer, so it notifies `not_empty`. A successful pop may enable a producer, so it notifies `not_full`. Closing can enable every waiter to terminate, so closure normally notifies all waiters on both conditions.

The queue invariants are:

```text
0 <= len <= capacity
closed => future pushes fail
empty && closed => future pops terminate
```

Closing does not necessarily discard buffered items. That is a product choice; BatchWeave will drain queued jobs into completed or cancelled outcomes.

### Notification cardinality follows the transition

Use `notify_one` when one transition creates at most one unit of progress, such as pushing one item into an empty bounded queue. Use `notify_all` when a global phase changes, closure occurs, or several waiters may now satisfy distinct predicates.

This is a progress and performance choice, not a safety requirement by itself. Over-notification is usually correct but can cause a thundering herd. Under-notification can strand enabled waiters if no later transition produces another notification.

### Barriers coordinate cohorts, not arbitrary lifetimes

A barrier releases participants after a fixed number have arrived. It is useful for tests that must start operations together, or algorithms with a known phase count and stable membership. It is dangerous when participants can fail, cancel, or skip the phase: remaining threads may wait forever.

For each barrier, state:

- participant count;
- who owns one arrival obligation;
- whether a panic can remove a participant;
- whether the barrier is reused for another phase;
- how the protocol terminates.

Do not use a barrier as a generic replacement for joins or queue closure.

### `OnceLock` publishes one stable value

`OnceLock<T>` supports one-time initialization followed by shared access. It is appropriate for immutable process configuration, generated tables, or lazily constructed values when initialization failure and reentrancy are handled deliberately.

It does not make later mutation safe, and a process-global cell can make tests and configuration order-dependent. Prefer dependency injection when different operations need different values. Use one-time publication when the value is truly process-wide and immutable after initialization.

### Timeout changes the API, not the predicate rule

A timed wait can return because the deadline elapsed or because it was notified. In both cases the caller must examine the predicate under the reacquired guard. A timeout result often means “the predicate was not observed before the deadline,” not “no notification occurred.”

Deadline arithmetic should use monotonic `Instant`, not wall-clock time. Repeated waits should compute remaining duration against one deadline so spurious wakeups do not reset the full budget.

### Model checkpoint

Before the complete-program example, verify that the model can decide a design rather than merely name its mechanism.

1. **Outcome 1.** For write every condition-variable wait as a predicate loop over mutex-protected state, construct one positive and one causal negative example. Mark the first decisive fact in the **predicate and wakeup record** and state which evidence could falsify the claim.

2. **Outcome 2.** For explain the atomic unlock-and-wait transition and why it prevents the ordinary lost-wakeup window, construct one positive and one causal negative example. Mark the first decisive fact in the **predicate and wakeup record** and state which evidence could falsify the claim.

3. **Outcome 3.** For distinguish `notify_one` and `notify_all` by which state transition can enable which waiters, construct one positive and one causal negative example. Mark the first decisive fact in the **predicate and wakeup record** and state which evidence could falsify the claim.

4. **Outcome 4.** For design bounded-buffer `not_empty`, `not_full`, and closure predicates, construct one positive and one causal negative example. Mark the first decisive fact in the **predicate and wakeup record** and state which evidence could falsify the claim.

5. **Preservation.** Name one earlier invariant that an easier but less precise implementation could regress.

6. **Boundary.** State one claim this module can justify and one adjacent claim that requires a later course, platform contract, peer behavior, or measurement.

A strong answer records state before and after the operation, the failure path, and the public consequence. An API name by itself is not a model.

## Use the idea in a complete program

This bounded queue places truth in one mutex-protected state and uses two condition variables only as wakeup mechanisms:

```rust
use std::collections::VecDeque;
use std::sync::{Condvar, Mutex};

#[derive(Debug)]
struct State<T> {
    items: VecDeque<T>,
    closed: bool,
}

#[derive(Debug)]
pub struct Closed<T>(pub T);

pub struct BoundedQueue<T> {
    capacity: usize,
    state: Mutex<State<T>>,
    not_empty: Condvar,
    not_full: Condvar,
}

impl<T> BoundedQueue<T> {
    pub fn new(capacity: usize) -> Option<Self> {
        (capacity > 0).then(|| Self {
            capacity,
            state: Mutex::new(State { items: VecDeque::new(), closed: false }),
            not_empty: Condvar::new(),
            not_full: Condvar::new(),
        })
    }

    pub fn push(&self, item: T) -> Result<(), Closed<T>> {
        let mut state = self.state.lock().unwrap_or_else(|p| p.into_inner());
        while state.items.len() == self.capacity && !state.closed {
            state = self.not_full.wait(state).unwrap_or_else(|p| p.into_inner());
        }
        if state.closed {
            return Err(Closed(item));
        }
        state.items.push_back(item);
        self.not_empty.notify_one();
        Ok(())
    }

    pub fn pop(&self) -> Option<T> {
        let mut state = self.state.lock().unwrap_or_else(|p| p.into_inner());
        while state.items.is_empty() && !state.closed {
            state = self.not_empty.wait(state).unwrap_or_else(|p| p.into_inner());
        }
        let item = state.items.pop_front();
        if item.is_some() {
            self.not_full.notify_one();
        }
        item
    }

    pub fn close(&self) {
        let mut state = self.state.lock().unwrap_or_else(|p| p.into_inner());
        state.closed = true;
        drop(state);
        self.not_empty.notify_all();
        self.not_full.notify_all();
    }
}
```

The loops recheck state after every wake. Push preserves ownership of a rejected item by returning `Closed<T>`. Pop drains already queued items after closure and returns `None` only when the queue is both closed and empty. Closure wakes both producer and consumer classes.

This example deliberately recovers poisoned state because no user callback or fallible product code runs while the queue lock is held; transitions are short `VecDeque` operations and invariant checks. The production capstone will document this choice. A product using user-defined allocation or callback logic under the lock should choose more conservative poison behavior.

The queue is blocking MPMC, not lock-free. That is the right abstraction for BatchWeave’s bounded backpressure. Module 68’s SPSC queue has a different topology and should not replace this design merely because it avoids a mutex.

## Practice sequence

1. Rewrite notification-based prose as state predicates.
2. Trace producer and consumer wait loops through spurious wakeup and competition.
3. Design closure semantics for a bounded queue.
4. Choose notification cardinality from the enabling transition.
5. Audit a barrier for missing participants and panic.
6. Add one deadline-based wait without resetting the timeout budget.
7. Complete Phase Gate and add waiting to BatchWeave’s queue.

The corresponding independent product is [Phase Gate](../../labs/module-04-phase-gate/README.md). The same reasoning then changes one explicit invariant in [BatchWeave](../capstone.md).

## Ready to continue

Continue only when you can do all of the following without using the chapter as a script:

- write a condition-variable wait as a `while` predicate loop;
- explain why notification is not durable truth;
- name both producer and consumer predicates for a bounded queue;
- state when closure wakes all waiters and whether buffered items drain;
- reject a barrier whose participant obligations are not fixed.

## Primary Rust references

- [`Condvar`](https://doc.rust-lang.org/std/sync/struct.Condvar.html)
- [`Barrier`](https://doc.rust-lang.org/std/sync/struct.Barrier.html)
- [`OnceLock`](https://doc.rust-lang.org/std/sync/struct.OnceLock.html)
- [`Instant`](https://doc.rust-lang.org/std/time/struct.Instant.html)
- [`std::sync`](https://doc.rust-lang.org/std/sync/index.html)

The course book is self-contained. These references are for checking the exact library contract and following changes in the language or standard library; they are not substitutes for the reasoning developed above.

## Continue

Continue to [Module 65 — Message Passing, Backpressure, and Shutdown](../module-65-message-passing-backpressure-and-shutdown/index.md) after completing the workbook, independent laboratory, capstone increment, and closed-book explanation for this module.
