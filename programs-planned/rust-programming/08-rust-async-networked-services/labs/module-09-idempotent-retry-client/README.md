# Laboratory 79 — Idempotent Retry Client

**Course 8 · Module 79: Network Failure, Idempotency, Retries, and Deterministic Testing**

[Chapter](../../course-book/module-79-network-failure-idempotency-retries-and-deterministic-testing/index.md) · [Workbook](../../course-book/module-79-network-failure-idempotency-retries-and-deterministic-testing/workbook.md) · [JobWire guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Network Failure, Idempotency, Retries, and Deterministic Testing**: When a network operation fails without revealing whether the remote side committed it, how do idempotency, retry budgets, failure classification, and deterministic tests preserve one semantic outcome? The product must make **Classify failures by phase, scope, retryability, and commit ambiguity** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **retry and commit matrix** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

> How can several wire attempts converge on one semantic operation under ambiguous commit, bounded retries, and deterministic virtual time?

The completed product must make the answer visible in its types, lifecycle, tests, failure behavior, and explanation. A successful happy-path run is not sufficient.

## Product

Build a retry engine against a scripted async attempt function and an in-memory idempotency store. Attempt one may commit and then report transport failure; a later attempt with the same key must retrieve the original terminal result without re-executing the handler.

## Product-specific design pressure

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

For **Laboratory 79 — Idempotent Retry Client**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Working route

1. Read the product contract and run the starter’s baseline checks for **Idempotent Retry Client**.
2. Draw the smallest **retry and commit matrix** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to JobWire so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Classify failures by phase, scope, retryability, and commit ambiguity.
- Distinguish idempotent operation semantics from retrying an HTTP or TCP request.
- Design idempotency keys with scope, fingerprint, in-progress state, terminal result, and retention.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 79 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **retry and commit matrix**. Defend why your design is simpler than one plausible alternative under the new requirements.
