# Laboratory 70 — Concurrent Verifier

This is the independent product for **Course 7, Module 70**. Read the [module chapter](../../course-book/module-70-integrated-concurrent-architecture-testing-and-audit/index.md) and complete its [workbook](../../course-book/module-70-integrated-concurrent-architecture-testing-and-audit/workbook.md) before consulting the reference implementation.

## Learning target

> How do bounded resources, worker lifecycle, panic, cancellation, atomics, deterministic output, and evidence form one coherent concurrent product?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build a small artifact verifier. Each indexed artifact contains bytes and an expected FNV-1a digest. A bounded worker group verifies artifacts, supports fail-fast cancellation, contains panic injection, reports live metrics, and renders one deterministic outcome per artifact.

## Why this laboratory exists

The final independent lab is a smaller analogue of BatchWeave. It tests whether the six architecture ledgers agree and whether a new cross-cutting requirement can be transferred without losing previous contracts.

## Contract

Accepted artifacts, identifiers, and cumulative payload bytes are bounded. Worker and queue counts are nonzero and bounded. Every artifact ends completed, mismatched, panicked, or cancelled. Live metrics are advisory; final counts scan outcomes. Under continue policy, complete outcomes are identical across supported worker/queue configurations. Under fail-fast policy, source-order rendering and exactly-once accounting remain deterministic, but the boundary between already-running completion and cancellation may legitimately depend on the schedule.

## Required milestones

1. Write all six ledgers.
2. Implement bounded queue and worker lifecycle.
3. Add typed outcomes, panic containment, and cancellation.
4. Reconcile indexed results and derive final summary.
5. Add continue-mode cross-configuration tests, fail-fast accounting tests, and one independent extension.

## Adversarial cases

- zero artifacts
- capacity one
- workers above artifacts
- one mismatch continue
- one mismatch fail-fast
- panic injection
- result receiver loss
- skewed completion
- maximum payload bound
- duplicate and empty identifiers
- worker or queue count above the configured limit

## Evidence to produce

- six architecture ledgers
- termination proof
- exact terminal accounting
- oracle summary
- deterministic output tests

## Prohibited shortcuts

- sleep-based protocol tests
- metrics as authority
- unbounded payload inside bounded slots
- report before join
- sorting by nonunique display text

## Transfer

Add bounded retry history for transient verifier failures. Preserve one final artifact outcome while recording attempt identities, bounding retries, and preventing duplicate irreversible effects.

## Comparing with the reference

Compare the entire architecture rather than one function. The reference should make every resource and terminal path visible. It must reject missing, duplicate, and out-of-range outcomes as infrastructure faults rather than manufacturing plausible product results. A design that is faster in one run but loses one artifact under panic is not comparable.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the protocol, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer the governing question without the chapter:

> How do bounded resources, worker lifecycle, panic, cancellation, atomics, deterministic output, and evidence form one coherent concurrent product?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
