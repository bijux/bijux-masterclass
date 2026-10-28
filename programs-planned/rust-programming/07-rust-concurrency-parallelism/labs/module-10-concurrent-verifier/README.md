# Laboratory 70 — Concurrent Verifier

**Course 7 · Module 70: Integrated Concurrent Architecture, Testing, and Audit**

[Chapter](../../course-book/module-70-integrated-concurrent-architecture-testing-and-audit/index.md) · [Workbook](../../course-book/module-70-integrated-concurrent-architecture-testing-and-audit/workbook.md) · [BatchWeave guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Integrated Concurrent Architecture, Testing, and Audit**: How do ownership, bounded work, synchronization, liveness, panic, cancellation, atomics, deterministic reporting, and test evidence become one product whose strongest claims are reviewable? The product must make **Construct one architecture diagram connecting coordinator, queue, workers, result channel, metrics, report pool, and CLI boundaries** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **concurrent architecture dossier** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> How do bounded resources, worker lifecycle, panic, cancellation, atomics, deterministic output, and evidence form one coherent concurrent product?

By the end, the answer must be visible in the public API, protocol diagram, failure behavior, causal tests, and explanation—not merely in a successful run.

## Product

Build a small artifact verifier. Each indexed artifact contains bytes and an expected FNV-1a digest. A bounded worker group verifies artifacts, supports fail-fast cancellation, contains panic injection, reports live metrics, and renders one deterministic outcome per artifact.

## Product-specific design pressure

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

For **Laboratory 70 — Concurrent Verifier**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Concurrent Verifier**.
2. Draw the smallest **concurrent architecture dossier** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to BatchWeave so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Construct one architecture diagram connecting coordinator, queue, workers, result channel, metrics, report pool, and CLI boundaries.
- Maintain ownership, synchronization, liveness, failure, determinism, and resource ledgers together.
- Prove boundedness for jobs, payloads, queue slots, workers, result messages, report threads, and output storage.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 70 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **concurrent architecture dossier**. Defend why your design is simpler than one plausible alternative under the new requirements.
