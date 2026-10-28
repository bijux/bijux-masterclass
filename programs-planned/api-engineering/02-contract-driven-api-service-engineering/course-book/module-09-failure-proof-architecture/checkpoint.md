# Checkpoint — Module 09: Failure-Oriented Verification

## Required result

Assemble pure, integration, concurrent, process-kill, conformance, and planted-defect proofs.

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

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Failure-Oriented Verification** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Failure-Oriented Verification**
- focused result for: Choose the narrowest oracle for each claim.
- public, durable, security, or operational observation showing: A single proof command exposes missing transactions, stale-worker writes, unstable cursors, unbounded uploads, and lost outbox intent.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **failure-sensitive proof architecture**
- a limitation statement naming every live dependency required to support the strongest **Failure-Oriented Verification** claim but not exercised

## Defend the design

1. Answer the central question: **How do we prove the service’s guarantees rather than infer them from happy-path unit tests?**
2. Demonstrate this capstone result: A single proof command exposes missing transactions, stale-worker writes, unstable cursors, unbounded uploads, and lost outbox intent.
3. Show the **Failure-Oriented Verification** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: a planted defect must cause the smallest relevant oracle to fail before the repair can count as evidence.
5. State which environment-backed **Failure-Oriented Verification** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—A single proof command exposes missing transactions, stale-worker writes, unstable cursors, unbounded uploads, and lost outbox intent.—all focused checks pass, the **Failure-Oriented Verification** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
