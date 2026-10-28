# Laboratory 79 — Idempotent Retry Client

This is the independent product for **Course 8, Module 79**. Read the [module chapter](../../course-book/module-79-network-failure-idempotency-retries-and-deterministic-testing/index.md) and complete its [workbook](../../course-book/module-79-network-failure-idempotency-retries-and-deterministic-testing/workbook.md) before consulting the reference implementation.

## Learning target

> How can several wire attempts converge on one semantic operation under ambiguous commit, bounded retries, and deterministic virtual time?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build a retry engine against a scripted async attempt function and an in-memory idempotency store. Attempt one may commit and then report transport failure; a later attempt with the same key must retrieve the original terminal result without re-executing the handler.

## Why this laboratory exists

The lab removes real sockets so retry semantics, commit count, time, and failure classification can be controlled exactly. It proves that idempotency is server state, not a property of looping client code.

## Contract

One semantic key and fingerprint are created before attempts. Retryable failures are explicit. Attempts share one overall deadline. Backoff uses injected deterministic jitter. The store tracks in-progress and completed states, rejects changed fingerprints, bounds records, and exposes execution count for proof.

## Required milestones

1. Define structured failure classes.
2. Implement idempotency state transitions.
3. Implement one-deadline retry.
4. Inject scripted failures and jitter.
5. Test ambiguous commit, conflict, attempt limit, and expiry policy.

## Adversarial cases

- success first attempt
- busy then success
- commit then disconnect
- changed fingerprint
- permanent domain failure
- deadline before next delay
- maximum attempts
- record capacity reached

## Evidence to produce

- retry ledger
- exact attempt and execution counts
- paused-time tests
- same key across attempts
- written process-lifetime limitation

## Prohibited shortcuts

- new key per retry
- retrying every error
- fresh full timeout per attempt
- real sleeps as the test oracle
- caching only successful outcomes while re-running terminal failures

## Transfer

Transfer the design to a payment provider where provider acceptance and settlement are different states. State what the cached result can honestly promise.

## Comparing with the reference

Compare semantic execution count first. Eventual success is insufficient if the handler ran more than once.

The `solution/` directory is a reference after independent work, not a sequence of blanks to copy. Compare invariants, task ownership, cancellation behavior, bounds, and tests before comparing line count.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Begin in `starter/`. Do not open `solution/` until the state diagram, failure cases, and transfer design are written or a precise blocker is recorded.

The laboratory is complete when its tests pass and you can answer the governing question without the chapter:

> How can several wire attempts converge on one semantic operation under ambiguous commit, bounded retries, and deterministic virtual time?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
