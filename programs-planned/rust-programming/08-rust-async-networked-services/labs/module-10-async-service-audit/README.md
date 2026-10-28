# Laboratory 80 — Async Service Audit

**Course 8 · Module 80: Integrated Async Service Architecture, Testing, and Audit**

[Chapter](../../course-book/module-80-integrated-async-service-architecture-testing-and-audit/index.md) · [Workbook](../../course-book/module-80-integrated-async-service-architecture-testing-and-audit/workbook.md) · [JobWire guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Integrated Async Service Architecture, Testing, and Audit**: Can the complete service be explained as one coherent set of lifecycle, protocol, capacity, cancellation, failure, compatibility, and operational contracts rather than as a pile of async APIs? The product must make **Construct a complete async service dossier** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **async service dossier** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> How can a complete async service be reviewed through authorities, bounds, commit points, cancellation paths, tests, and explicit non-guarantees?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build a compact in-memory notification service with bounded submissions, one dispatcher task, idempotent message keys, a status snapshot, and graceful shutdown. Then produce all nine Course 8 ledgers and inject failures at three mechanism intersections.

## Product-specific design pressure

The final lab tests transfer. It is not a smaller copy of JobWire and does not require sockets. The challenge is to prove that the same reasoning models apply to a new service with different domain state.

## Contract

At most 16 committed pending notifications and four active deliveries exist. The pre-commit mailbox, idempotency-record table, and duplicate waiters per key are independently bounded. One dispatcher owns idempotency and terminal results. Duplicate keys with changed recipients conflict. Shutdown rejects new work, drains for a finite grace, aborts leftovers, joins tasks, and leaves one terminal state per committed message.

## Resource envelope

| Resource | Required bound | Meaning |
|---|---:|---|
| Pre-commit mailbox | `1..=16` | Commands not yet inspected by the dispatcher |
| Committed pending queue | `1..=16` | Accepted notifications waiting for active capacity |
| Active deliveries | `1..=4` | Spawned delivery tasks |
| Idempotency records | `1..=64` | In-progress and completed semantic keys retained for the service lifetime |
| Duplicate waiters per key | `1..=8` | Callers waiting for one in-progress semantic result |
| Shutdown grace | Nonzero duration | One absolute drain deadline before abort |

## Required milestones

1. Freeze product guarantees and non-guarantees.
2. Define authority and task tree.
3. Implement bounded admission and commit.
4. Add cancellation and idempotent recovery.
5. Build the dossier and intersection tests.

## Adversarial cases

- duplicate during delivery
- changed recipient conflict
- queue saturation
- delivery failure
- caller cancellation after commit
- shutdown with active work
- grace expiry
- status query during saturation

## Evidence to produce

- all nine ledgers
- resource envelope with exclusions
- failure-cut trace
- at least three causal fault injections
- architecture defense and multi-process limitation

## Prohibited shortcuts

- copying JobWire types or names
- unbounded tasks or channels
- one generic error string
- health that waits behind delivery work
- claiming exactly-once behavior across process restart

## Transfer

Transfer the final dossier method to an async crawler. Identify which resource dimension—URLs, connections, bodies, parsed pages, retries, or results—dominates first.

## Comparing with the reference

Compare coherence across documents and code. A reference is weaker when its capacity table, task tree, and shutdown behavior contradict each other.

The `solution/` directory is a reference after independent work, not a sequence of blanks to copy. Compare invariants, task ownership, cancellation behavior, bounds, and tests before comparing line count.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Begin in `starter/`. Do not open `solution/` until the state diagram, failure cases, and transfer design are written or a precise blocker is recorded.

The laboratory is complete when its tests pass and you can answer the governing question without the chapter:

For **Laboratory 80 — Async Service Audit**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Async Service Audit**.
2. Draw the smallest **async service dossier** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to JobWire so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Construct a complete async service dossier.
- Trace one request from accepted socket through terminal response and cleanup.
- Identify the authoritative owner of protocol, broker, idempotency, metrics, and shutdown state.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 80 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **async service dossier**. Defend why your design is simpler than one plausible alternative under the new requirements.
