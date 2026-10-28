# Lab — Module 10: Lifecycle and Compatible Release

## Objective

Execute one controlled transition from service 1.0/API 1.1.0 on migrations 001–002 to service 1.1/API 1.2.0 on migrations 001–005, while preserving the predecessor contract during the supported coexistence window.

## Setup conditions

The previous baseline is: **A single proof command exposes missing transactions, stale-worker writes, unstable cursors, unbounded uploads, and lost outbox intent.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *Can the service start, migrate, coexist, drain, roll back, and recover without violating its public contract or data?*

## Failure action and investigation

1. Implement and test: Distinguish startup, liveness, readiness, and draining.
2. Implement and test: Order application and schema releases safely.
3. Implement and test: Keep old and new service versions compatible during expansion.
4. Implement and test: Define the rollback boundary explicitly.
5. Implement and test: Release API 1.2 without breaking API 1.1 consumers.

### Required planted defect

Change migration 003 so `result_summary` is immediately non-null without a compatible default.

The lab is successful only when service 1.0 fails during the coexistence experiment, the failure is traced to the premature constraint, and the repaired expand migration is preserved as a regression fixture. Do not “fix” the test by removing service 1.0 from the supported matrix.

## Operational oracle

Service 1.0 and 1.1 both work on the expanded/backfilled schema; rollback succeeds before enforcement; the final constraint is applied only after old writers are gone.

## Required evidence

- baseline transcript proving the previous checkpoint before **Lifecycle and Compatible Release** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Distinguish startup, liveness, readiness, and draining.
- public, durable, security, or operational observation showing: Course 2 ends with a release-ready service, migrations 001–005, and an additive API 1.2 contract.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **compatible service and schema release**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Lifecycle and Compatible Release**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=10`.
4. Confirm the system again provides this result: Course 2 ends with a release-ready service, migrations 001–005, and an additive API 1.2 contract.

## Completion gate

- configuration fails before readiness when required values are invalid;
- liveness and readiness answer different questions;
- shutdown has a bounded, observed result;
- migration checksums are immutable;
- service 1.0 and 1.1 coexist only in phases 003–004;
- application rollback succeeds before migration 005;
- migration 004 is idempotent;
- migration 005 is applied only after old writers are drained;
- the accepted API release is classified without a hard break;
- the rejected candidate is blocked for the intended reasons.
