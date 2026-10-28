# Laboratory 80 — Async Service Audit

This is the independent product for **Course 8, Module 80**. Read the [module chapter](../../course-book/module-80-integrated-async-service-architecture-testing-and-audit/index.md) and complete its [workbook](../../course-book/module-80-integrated-async-service-architecture-testing-and-audit/workbook.md) before consulting the reference implementation.

## Learning target

> How can a complete async service be reviewed through authorities, bounds, commit points, cancellation paths, tests, and explicit non-guarantees?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build a compact in-memory notification service with bounded submissions, one dispatcher task, idempotent message keys, a status snapshot, and graceful shutdown. Then produce all nine Course 8 ledgers and inject failures at three mechanism intersections.

## Why this laboratory exists

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

> How can a complete async service be reviewed through authorities, bounds, commit points, cancellation paths, tests, and explicit non-guarantees?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
