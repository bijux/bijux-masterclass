# Lab — Module 03: Relational Modeling and Migrations

> **Module 03:** Relational Modeling and Migrations

## Objective

Migrate an empty PostgreSQL database, persist all core resources, survive process restart, and prove critical invalid states cannot be inserted even when application code is bypassed.

## Why this lab matters

This lab turns the module’s governing question—**How should relational structure and migrations reinforce rather than merely store application invariants?**—into a falsifiable experiment. Review the relational model and write one justification per table, key, nullable column, and constraint. Start PostgreSQL 18.4 and create a disposable database for the chosen track. Apply migrations 001 and 002 from an empty state; rerun and inspect the ledger. Implement repositories for projects, datasets, runs, artifacts, and subscriptions.

It advances the cumulative Analysis Runs Platform by requiring this result: **Persist principals, projects, datasets, runs, artifacts, and ownership with constraints and deterministic migrations**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **The Analysis Runs state machine rejects impossible transitions before any database write.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How does PostgreSQL reinforce the service invariants instead of acting as an unstructured persistence dictionary?*

## Hypothesis

The clean implementation should satisfy this claim: **The database—not a mock—must reject an impossible owner/reference/state relation with the named constraint and SQLSTATE.** When the lab introduces this fault—**Plant a removed ownership component in one foreign key, reproduce cross-owner insertion, restore the constraint with a new local migration, and preserve the test**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant a removed ownership component in one foreign key, reproduce cross-owner insertion, restore the constraint with a new local migration, and preserve the test**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Migrate an empty PostgreSQL database, persist all core resources, survive process restart, and prove critical invalid states cannot be inserted even when application code is bypassed**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

The database—not a mock—must reject an impossible owner/reference/state relation with the named constraint and SQLSTATE.

## Required evidence

- baseline transcript proving the previous checkpoint before **Relational Modeling and Migrations** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Relational Modeling and Migrations**
- focused result for: Map relationships and ownership to keys and constraints.
- public, durable, security, or operational observation showing: Projects, datasets, runs, jobs, artifacts, idempotency records, and subscriptions survive restart.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **migration ownership**
- a limitation statement naming every live dependency required to support the strongest **Relational Modeling and Migrations** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Relational Modeling and Migrations**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant a removed ownership component in one foreign key, reproduce cross-owner insertion, restore the constraint with a new local migration, and preserve the test** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Relational Modeling and Migrations**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Relational Modeling and Migrations** experiment.
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

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Relational Modeling and Migrations**. A green command without the negative case and causal explanation does not satisfy this gate.
