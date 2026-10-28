# Checkpoint — Module 03: Relational Modeling and Migrations

## Required result

Projects, datasets, runs, jobs, artifacts, idempotency records, and subscriptions survive restart.

## Demonstrate

- Map relationships and ownership to keys and constraints.
- Use nullability and checks to exclude invalid states.
- Choose indexes from actual query patterns.
- Own migrations explicitly and apply them from an empty database.
- Map rows to domain objects without leaking persistence shape.

## Commands

```bash
make predecessor-proof
make operation-proof
make module-proof MODULE=03 TRACK=python
make module-proof MODULE=03 TRACK=typescript
make core-proof
```

## Defend the design

1. Answer the central question: **How does PostgreSQL reinforce the service invariants instead of acting as an unstructured persistence dictionary?**
2. Demonstrate this capstone result: Projects, datasets, runs, jobs, artifacts, idempotency records, and subscriptions survive restart.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: ordered migration names, one migration history, and atomic application are identical commitments.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Projects, datasets, runs, jobs, artifacts, idempotency records, and subscriptions survive restart.—all focused checks pass, the **Relational Modeling and Migrations** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
