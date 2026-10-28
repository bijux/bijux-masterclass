# Laboratory 71 — One-Shot Signal

This is the independent product for **Course 8, Module 71**. Read the [module chapter](../../course-book/module-71-futures-polling-wakers-and-async-state-machines/index.md) and complete its [workbook](../../course-book/module-71-futures-polling-wakers-and-async-state-machines/workbook.md) before consulting the reference implementation.

## Learning target

> How can a custom future return `Pending` without losing completion, waking the wrong task, or treating polls as events?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build a single-producer, single-consumer one-shot signal. The producer transfers exactly one value. The receiver implements `Future`, updates its stored waker, observes completion before and after registration, and communicates receiver cancellation so the producer can recover an unsent value.

## Why this laboratory exists

The product isolates the `Future::poll` contract before Tokio task scheduling adds more lifecycle machinery. It forces you to store protocol state separately from scheduling hints and to reason about producer-before-poll, poll-before-producer, replacement wakers, and drop.

## Contract

There is one sender and one receiver. Sending consumes the sender. A successful send makes the receiver ready exactly once. Dropping the receiver before send makes `send` return the original value. Polling after completion is outside the supported contract and may panic with a clear message. No wake call occurs while the internal mutex is held.

## Required milestones

1. Freeze the state table and terminal states.
2. Implement sender and receiver ownership around one shared state.
3. Implement `Future::poll` with current-waker replacement.
4. Implement receiver drop and sender failure semantics.
5. Add causal tests with distinct wakers and both race orders.

## Adversarial cases

- completion before first poll
- several polls before completion
- a different waker on a later poll
- receiver dropped before send
- sender dropped without send
- poll after terminal completion

## Evidence to produce

- a state-transition table
- the exact invariant behind every `Pending` return
- a test proving the latest waker is used
- a test proving wake occurs outside the lock
- an explicit single-producer/single-consumer non-goal

## Prohibited shortcuts

- unconditional self-waking
- using poll count as produced-event count
- holding the mutex while calling `wake`
- silently overwriting a delivered value
- cloning the payload to avoid ownership reasoning

## Transfer

Transfer the design to a future that completes with either a value or explicit cancellation. Define precedence when both are visible and whether producer cancellation is distinguishable from receiver cancellation.

## Comparing with the reference

The reference is stronger only if no producer/completion schedule can leave a pending receiver without a wake path. Inspect state publication and waker replacement before surface syntax.

The `solution/` directory is a reference after independent work, not a sequence of blanks to copy. Compare invariants, task ownership, cancellation behavior, bounds, and tests before comparing line count.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Begin in `starter/`. Do not open `solution/` until the state diagram, failure cases, and transfer design are written or a precise blocker is recorded.

The laboratory is complete when its tests pass and you can answer the governing question without the chapter:

> How can a custom future return `Pending` without losing completion, waking the wrong task, or treating polls as events?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
