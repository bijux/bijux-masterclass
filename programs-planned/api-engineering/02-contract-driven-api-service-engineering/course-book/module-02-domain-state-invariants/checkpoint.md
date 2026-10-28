# Checkpoint — Module 02: Domain State and Invariants

## Required result

Implement project, dataset, run, cancellation, and artifact rules as testable domain behavior.

## Demonstrate

- Model legal and illegal state transitions.
- Distinguish entities, values, commands, and outcomes pragmatically.
- Keep domain failures stable and transport-neutral.
- Control time and identifiers in tests.
- Prove invariants with pure state-transition tests.

## Commands

```bash
make predecessor-proof
make operation-proof
make module-proof MODULE=02 TRACK=python
make module-proof MODULE=02 TRACK=typescript
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Domain State and Invariants** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Domain State and Invariants**
- focused result for: Model legal and illegal state transitions.
- public, durable, security, or operational observation showing: The Analysis Runs state machine rejects impossible transitions before any database write.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **domain invariants and canonical values**
- a limitation statement naming every live dependency required to support the strongest **Domain State and Invariants** claim but not exercised

## Defend the design

1. Answer the central question: **Which rules must remain true regardless of framework, database, worker, or deployment?**
2. Demonstrate this capstone result: The Analysis Runs state machine rejects impossible transitions before any database write.
3. Show the **Domain State and Invariants** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: both tracks reject illegal run transitions and produce identical canonical bytes for fingerprints.
5. State which environment-backed **Domain State and Invariants** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—The Analysis Runs state machine rejects impossible transitions before any database write.—all focused checks pass, the **Domain State and Invariants** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
