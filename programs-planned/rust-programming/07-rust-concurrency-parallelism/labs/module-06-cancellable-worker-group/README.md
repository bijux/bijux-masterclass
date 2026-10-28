# Laboratory 66 — Cancellable Worker Group

**Course 7 · Module 66: Liveness: Deadlock, Cancellation, and Recovery**

[Chapter](../../course-book/module-66-liveness-deadlock-cancellation-and-recovery/index.md) · [Workbook](../../course-book/module-66-liveness-deadlock-cancellation-and-recovery/workbook.md) · [BatchWeave guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Liveness: Deadlock, Cancellation, and Recovery**: Why can every blocked operation eventually continue or terminate, and what happens when cancellation, panic, or partial infrastructure failure interrupts the normal path? The product must make **Distinguish deadlock, starvation, livelock, priority inversion, and slow work** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **wait-for and shutdown graph** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> How does cancellation wake blocked work, contain panic, preserve accepted-job identity, and terminate every worker exactly once?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build a bounded worker group over source-ordered indexed text tasks. Worker count, queue capacity, task count, and cumulative text bytes all have explicit product limits. Tasks can succeed, return a domain error, or deliberately panic. Continue mode contains either failure at the job boundary; fail-fast mode closes the queue after the first domain failure or contained panic. Every accepted task ends as completed, failed, panicked, or cancelled.

## Product-specific design pressure

The product combines the first five mechanisms and evaluates liveness directly. Cancellation must be durable state and a wake event; panic containment must remain outside queue invariants.

## Contract

The queue is closed on explicit cancellation and on fail-fast failure. Blocked push/pop operations wake. Workers catch panic only around task execution, send one terminal outcome for every popped task, and are all joined. Unsubmitted jobs rejected by a closed queue become explicit cancellations. Duplicate, out-of-range, missing, or outer-worker outcomes are infrastructure errors rather than silently fabricated cancellations.

## Required milestones

1. Freeze lifecycle and outcome models.
2. Implement idempotent cancellation and queue close.
3. Add checkpoints before execution.
4. Contain panic at the job boundary.
5. Reconcile all accepted indices after joining.

## Adversarial cases

- cancel with producer blocked
- cancel with consumers blocked
- first task domain failure
- middle task panic
- result receiver dropped
- zero tasks
- noncontiguous task indices
- cumulative text above the product bound
- repeated shutdown calls

## Evidence to produce

- wait-for graph
- state/wake/checkpoint table
- panic boundary
- exact terminal accounting and protocol-error precedence
- idempotent shutdown trace

## Prohibited shortcuts

- flag-only cancellation
- barrier-based shutdown
- catching panic around queue internals
- returning before all joins
- waiting forever for an exact message count

## Transfer

Transfer the design to file indexing. Add a task that takes a long loop and define the maximum cancellation checkpoint interval rather than claiming immediate interruption.

## Comparing with the reference

Compare liveness before output. The reference should wake blocked operations, join after panic, label every accepted index, and avoid relying on sleep to reach a state.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the protocol, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer the governing question without the chapter:

For **Laboratory 66 — Cancellable Worker Group**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Cancellable Worker Group**.
2. Draw the smallest **wait-for and shutdown graph** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to BatchWeave so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish deadlock, starvation, livelock, priority inversion, and slow work.
- Construct a wait-for graph over locks, channels, joins, barriers, and conditions.
- State a global lock order and identify operations that violate it.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 66 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **wait-for and shutdown graph**. Defend why your design is simpler than one plausible alternative under the new requirements.
