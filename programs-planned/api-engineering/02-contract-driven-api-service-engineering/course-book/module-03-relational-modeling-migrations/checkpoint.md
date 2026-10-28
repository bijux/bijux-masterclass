# Checkpoint — Module 03: Relational Modeling and Migrations

## Required result

Persist principals, projects, datasets, runs, artifacts, and ownership with constraints and deterministic migrations.

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

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Relational Modeling and Migrations** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Relational Modeling and Migrations**
- focused result for: Map relationships and ownership to keys and constraints.
- public, durable, security, or operational observation showing: Projects, datasets, runs, jobs, artifacts, idempotency records, and subscriptions survive restart.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **migration ownership**
- a limitation statement naming every live dependency required to support the strongest **Relational Modeling and Migrations** claim but not exercised

## Defend the design

1. Answer the central question: **How does PostgreSQL reinforce the service invariants instead of acting as an unstructured persistence dictionary?**
2. Demonstrate this capstone result: Projects, datasets, runs, jobs, artifacts, idempotency records, and subscriptions survive restart.
3. Show the **Relational Modeling and Migrations** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: ordered migration names, one migration history, and atomic application are identical commitments.
5. State which environment-backed **Relational Modeling and Migrations** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—Projects, datasets, runs, jobs, artifacts, idempotency records, and subscriptions survive restart.—all focused checks pass, the **Relational Modeling and Migrations** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
