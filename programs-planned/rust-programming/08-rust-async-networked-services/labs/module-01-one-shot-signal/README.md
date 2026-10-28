# Laboratory 71 — One-Shot Signal

**Course 8 · Module 71: Futures, Polling, Wakers, and Async State Machines**

[Chapter](../../course-book/module-71-futures-polling-wakers-and-async-state-machines/index.md) · [Workbook](../../course-book/module-71-futures-polling-wakers-and-async-state-machines/workbook.md) · [JobWire guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Futures, Polling, Wakers, and Async State Machines**: What exactly is an async computation before a runtime executes it, what must happen when it cannot complete, and what state remains when it is suspended or cancelled? The product must make **Explain why a future is inert until polled** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **future state and wake-source table** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> How can a custom future return `Pending` without losing completion, waking the wrong task, or treating polls as events?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build a single-producer, single-consumer one-shot signal. The producer transfers exactly one value. The receiver implements `Future`, updates its stored waker, observes completion before and after registration, and communicates receiver cancellation so the producer can recover an unsent value.

## Product-specific design pressure

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

For **Laboratory 71 — One-Shot Signal**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **One-Shot Signal**.
2. Draw the smallest **future state and wake-source table** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to JobWire so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Explain why a future is inert until polled.
- Read the `Future::poll` contract and distinguish completion from scheduling.
- State what `Context` and `Waker` permit without treating wake as a stored event count.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 71 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **future state and wake-source table**. Defend why your design is simpler than one plausible alternative under the new requirements.
