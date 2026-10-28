# Workbook — Module 71: Futures, Polling, Wakers, and Async State Machines

[Return to the chapter](index.md) · [Open the solutions](solutions.md) · [Open the JobWire guide](../capstone.md)

Freeze every prediction before compiling or running code. For async questions, identify the state before the poll, the event required for progress, and the effect of dropping the future.

## Part 1 — Predict

1. An async function prints before its first `.await`. The caller constructs the future and drops it. Does the print occur?
2. A custom future always calls `cx.waker().wake_by_ref()` and returns `Pending`. What runtime behavior should you expect?
3. A future stores the first waker it sees and ignores all later wakers. Under what scheduling change can it stall the wrong task?
4. An async block creates `Rc<String>`, uses it, drops it, and only then awaits. May the future still satisfy `Send`?
5. The same `Rc<String>` remains live after the `.await`. What changes?
6. A timeout drops a future halfway through `write_all`. Does the peer necessarily see no bytes?
7. A future returns `Ready(7)` and is polled again. Is the caller entitled to receive `7` again?
8. A producer writes a value under a mutex, takes the stored waker, releases the mutex, and wakes. Why is waking after unlock preferable?

For each answer, name whether the rule belongs to Rust’s future contract, the executor, the I/O protocol, or the application design.

## Part 2 — Diagnose and repair

A custom `CounterFuture` stores only a `Waker`. A producer calls `wake` once for every increment, while `poll` interprets each invocation as one increment and completes after ten polls.

Diagnose the design under wake coalescing and spurious polls. Repair it so the count is stored as protocol state and the waker is only a scheduling bridge. Then add a completion flag so polling after terminal completion is rejected or documented.

A second defect holds `std::sync::MutexGuard` across an `.await` and then fails a `Send + 'static` spawn boundary. Produce two repairs:

- one that shortens the synchronous critical section and returns owned data;
- one that intentionally uses a local non-`Send` task.

Explain why changing to an async mutex is not automatically the principled repair.

## Part 3 — Focused exercises

### Exercise 1 — State-machine derivation

For an async login function that connects, writes credentials, reads a challenge, computes a response, writes it, and reads a verdict, list every state and the locals retained in each state.

### Exercise 2 — Wake invariant

Write a precise invariant for returning `Pending` from a future that waits for a producer thread. Include producer-before-registration and registration-before-producer schedules.

### Exercise 3 — Send diagnosis

Construct three tiny async functions:

- one with a non-`Send` value dropped before `.await`;
- one retaining it across `.await`;
- one converting it into owned `Send` data before `.await`.

Use a helper requiring `Future + Send` to prove the differences without starting a runtime.

### Exercise 4 — Cancellation ledger

Analyze an operation that reserves an ID, writes a request, and waits for a response. For every suspension point, state what dropping the future leaves locally and remotely.

### Exercise 5 — Waker replacement

Design a test waker that records wake calls. Poll a one-shot receiver with one waker, then a second distinct waker. Complete the signal and prove only the current task is scheduled.

## Part 4 — Independent laboratory

Build [One-Shot Signal](../../labs/module-01-one-shot-signal/README.md). Before opening the solution, provide:

- a state diagram;
- the exact `Pending` invariant;
- tests for completion before polling, polling before completion, waker replacement, receiver cancellation, and producer cancellation;
- an explanation of why the implementation does not wake while holding its mutex;
- one explicit non-goal, such as multi-producer support.

## Part 5 — Capstone transfer

For JobWire’s future handshake and request/response path, create a future-state ledger with at least these states:

```text
accepted → framed → negotiating → ready → awaiting broker → responding → closing
```

For each state, list owned values, awaited event, wake source, external effects, and drop behavior. Do not write the TCP server yet. The purpose is to freeze the lifecycle vocabulary before runtime APIs appear.

Add one testable assertion to the capstone design: after a connection task is dropped, no broker reply sender owned only by that task may keep a request waiter alive indefinitely.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. Why is a future inert?
2. What does a waker promise and what does it not count?
3. Why must a future update a stored waker?
4. Which locals affect the future’s `Send` implementation?
5. Why can cancellation be unsafe even though Rust drops every owned field correctly?
6. What role does `Pin` play in `poll`?

### Independent transfer

Design a future that becomes ready when either a producer supplies a value or a cancellation flag is set. Specify precedence when both are visible, waker storage, producer/drop behavior, and repeated-poll behavior. Do not implement it until the state table is internally consistent.
