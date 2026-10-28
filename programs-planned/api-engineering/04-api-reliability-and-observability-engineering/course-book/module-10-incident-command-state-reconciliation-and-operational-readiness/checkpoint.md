# Checkpoint — Module 10: Incident Command, Reconciliation, and Readiness

## Required result

Course 4 ends with reliability profile 1.0, migration 008, tested runbooks, and an operational handoff to performance engineering.

## Demonstrate

- Assign incident command, operations, communication, and recording roles.
- Construct a timeline with source and confidence.
- Reconcile database, jobs, artifacts, and outbox state.
- Generate stable repair actions before mutation.
- Close only after user outcomes, cleanup, and regressions are verified.

## Commands

```bash
make module-proof MODULE=10
make core-proof
```

## Defend the design

1. Answer the central question: **During a real incident, how do people coordinate, determine durable truth, repair safely, and decide that the service is ready again?**
2. Demonstrate this capstone result: Course 4 ends with reliability profile 1.0, migration 008, tested runbooks, and an operational handoff to performance engineering.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: operators diagnose from telemetry but reconcile and repair from read-only durable facts using stable, idempotent repair identifiers.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Course 4 ends with reliability profile 1.0, migration 008, tested runbooks, and an operational handoff to performance engineering.—all focused checks pass, the **Incident Command, Reconciliation, and Readiness** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
