# Checkpoint — Module 02: Domain State and Invariants

## Required result

The Analysis Runs state machine rejects impossible transitions before any database write.

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

## Defend the design

1. Answer the central question: **Which rules must remain true regardless of framework, database, worker, or deployment?**
2. Demonstrate this capstone result: The Analysis Runs state machine rejects impossible transitions before any database write.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: both tracks reject illegal run transitions and produce identical canonical bytes for fingerprints.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—The Analysis Runs state machine rejects impossible transitions before any database write.—all focused checks pass, the **Domain State and Invariants** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
