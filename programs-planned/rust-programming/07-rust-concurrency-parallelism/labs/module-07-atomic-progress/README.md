# Laboratory 67 — Atomic Progress

**Course 7 · Module 67: Atomics, Happens-Before, and Memory Ordering**

[Chapter](../../course-book/module-67-atomics-happens-before-and-memory-ordering/index.md) · [Workbook](../../course-book/module-67-atomics-happens-before-and-memory-ordering/workbook.md) · [BatchWeave guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Atomics, Happens-Before, and Memory Ordering**: Which fact does an atomic operation publish, which earlier writes become visible because of it, and what is the weakest ordering that proves the required relationship? The product must make **Separate atomicity of one location from visibility of other memory** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **happens-before graph** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> Which atomic values are merely telemetry, which publish state, and what happens-before or linearization proof justifies each ordering?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build an atomic progress object with a lifecycle state, independent live counters, a checked quota reservation, and a one-writer-wins publication slot. Final authoritative counts are supplied separately and may be compared with telemetry.

## Product-specific design pressure

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

For **Laboratory 67 — Atomic Progress**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Atomic Progress**.
2. Draw the smallest **happens-before graph** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to BatchWeave so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Separate atomicity of one location from visibility of other memory.
- Reason with sequenced-before, synchronizes-with, and happens-before relations.
- Use relaxed atomics for independent counters whose exact snapshots are advisory.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 67 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **happens-before graph**. Defend why your design is simpler than one plausible alternative under the new requirements.
