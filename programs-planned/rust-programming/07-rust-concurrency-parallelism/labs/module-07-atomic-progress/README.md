# Laboratory 67 — Atomic Progress

This is the independent product for **Course 7, Module 67**. Read the [module chapter](../../course-book/module-67-atomics-happens-before-and-memory-ordering/index.md) and complete its [workbook](../../course-book/module-67-atomics-happens-before-and-memory-ordering/workbook.md) before consulting the reference implementation.

## Learning target

> Which atomic values are merely telemetry, which publish state, and what happens-before or linearization proof justifies each ordering?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build an atomic progress object with a lifecycle state, independent live counters, a checked quota reservation, and a one-writer-wins publication slot. Final authoritative counts are supplied separately and may be compared with telemetry.

## Why this laboratory exists

The lab separates three common atomic jobs—state transition, independent metrics, and check-and-update—so orderings are derived rather than copied.

## Contract

Lifecycle transitions are monotonic and reject invalid edges. Live counters use relaxed ordering and document incoherent cross-counter snapshots. Quota reservation is one atomic transition. The lifecycle does not publish ordinary data and therefore uses relaxed ordering. A separate publication slot writes its value before a release transition to ready; an acquire observation of ready permits the value read.

## Required milestones

1. Write the atomic state ledger.
2. Implement legal lifecycle CAS transitions.
3. Implement relaxed saturating or checked counters.
4. Implement quota reservation with `fetch_update` or CAS.
5. Add the claimed/writing/ready publication protocol and ordering proof.

## Adversarial cases

- competing start transitions
- double finish
- quota exactly equal
- quota insufficient under contention
- counter overflow policy
- acquire observes old state
- two publishers compete for one slot
- advisory snapshot finished above started

## Evidence to produce

- happens-before graph
- linearization point
- success/failure ordering rationale
- snapshot honesty
- overflow policy

## Prohibited shortcuts

- SeqCst everywhere without explanation
- multi-field invariant from separate relaxed counters
- irreversible effect in retry closure
- using metrics to decide completion
- ignoring ABA or wraparound

## Transfer

Transfer the state machine to a one-producer result slot. Then add reuse and identify why generation tagging or a different ownership protocol is required.

## Comparing with the reference

Compare the proof ledger, not ordering strength. The reference should use relaxed where no data is published and stronger ordering only where a stated release/acquire edge requires it.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the protocol, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer the governing question without the chapter:

> Which atomic values are merely telemetry, which publish state, and what happens-before or linearization proof justifies each ordering?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
