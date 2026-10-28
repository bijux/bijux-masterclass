# Lab — Module 03: Relational Modeling and Migrations

## Objective

Migrate an empty PostgreSQL database, persist all core resources, survive process restart, and prove critical invalid states cannot be inserted even when application code is bypassed.

## Setup conditions

The previous baseline is: **The Analysis Runs state machine rejects impossible transitions before any database write.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How does PostgreSQL reinforce the service invariants instead of acting as an unstructured persistence dictionary?*

## Failure action and investigation

1. **Review the relational model and write one justification per table, key, nullable column, and constraint.**
2. **Start PostgreSQL 18.4 and create a disposable database for the chosen track.**
3. **Apply migrations 001 and 002 from an empty state; rerun and inspect the ledger.**
4. **Implement repositories for projects, datasets, runs, artifacts, and subscriptions.**
5. **Run direct invalid SQL cases for unknown states, broken ownership, duplicate identities, and inconsistent source fields.**
6. **Restart API and verify previously created resources through generated client calls.**
7. **Plant a removed ownership component in one foreign key, reproduce cross-owner insertion, restore the constraint with a new local migration, and preserve the test.**
8. **Review the second track migration runner and explain the transaction/session difference between psycopg and node-postgres.**

### Required planted defect

> Remove `owner_id` from one composite foreign key and demonstrate a dataset can reference a project owned by another principal.

Preserve the following evidence:

```text
prediction:
change introduced:
minimal setup:
first failing command:
public symptom:
durable/process state:
root cause:
repair:
regression path:
remaining limitation:
```

## Operational oracle

The database—not a mock—must reject an impossible owner/reference/state relation with the named constraint and SQLSTATE.

## Required evidence

- baseline transcript proving the previous checkpoint before **Relational Modeling and Migrations** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Map relationships and ownership to keys and constraints.
- public, durable, security, or operational observation showing: Projects, datasets, runs, jobs, artifacts, idempotency records, and subscriptions survive restart.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **migration ownership**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Relational Modeling and Migrations**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=03`.
4. Confirm the system again provides this result: Projects, datasets, runs, jobs, artifacts, idempotency records, and subscriptions survive restart.

## Completion gate

- clean migration succeeds
- migration drift rejected
- durability across restart
- constraints reject invalid corpus
- ownership composite enforced
- parameterized SQL only
- adapter failures translated
- database tests disposable
