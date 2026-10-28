# Checkpoint — Module 09: Failure-Oriented Verification

## Required result

A single proof command exposes missing transactions, stale-worker writes, unstable cursors, unbounded uploads, and lost outbox intent.

## Demonstrate

- Choose the narrowest oracle for each claim.
- Use real PostgreSQL for database concurrency claims.
- Inject failures at transaction and process boundaries.
- Retain planted defects as regression tests.
- Separate deterministic local checks from environment-backed checks.

## Commands

```bash
make predecessor-proof
make operation-proof
make module-proof MODULE=09 TRACK=python
make module-proof MODULE=09 TRACK=typescript
make core-proof
```

## Defend the design

1. Answer the central question: **How do we prove the service’s guarantees rather than infer them from happy-path unit tests?**
2. Demonstrate this capstone result: A single proof command exposes missing transactions, stale-worker writes, unstable cursors, unbounded uploads, and lost outbox intent.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: a planted defect must cause the smallest relevant oracle to fail before the repair can count as evidence.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—A single proof command exposes missing transactions, stale-worker writes, unstable cursors, unbounded uploads, and lost outbox intent.—all focused checks pass, the **Failure-Oriented Verification** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
