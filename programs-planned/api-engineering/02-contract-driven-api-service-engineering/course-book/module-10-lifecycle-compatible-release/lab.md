# Lab — Module 10: Lifecycle and Compatible Release

> **Module 10:** Lifecycle and Compatible Release

## Objective

Execute one controlled transition from service 1.0/API 1.1.0 on migrations 001–002 to service 1.1/API 1.2.0 on migrations 001–005, while preserving the predecessor contract during the supported coexistence window.

## Why this lab matters

This lab turns the module’s governing question—**How can old and new service versions coexist through a database change and still preserve the public contract?**—into a falsifiable experiment. Finalize configuration schema, startup validation, and role-specific health routes. Implement graceful API and worker shutdown with bounded drain and cleanup. Build selected-track image from pinned dependencies and verify non-root/write boundaries. Deploy PostgreSQL, receiver, API, and worker from clean state; run predecessor workflow. Apply migration 003, run old and new versions in the allowed coexistence window, and create data.

It advances the cumulative Analysis Runs Platform by requiring this result: **Build lifecycle controls, compatible expand/backfill/enforce migrations, rollback evidence, and release proof**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **A single proof command exposes missing transactions, stale-worker writes, unstable cursors, unbounded uploads, and lost outbox intent.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *Can the service start, migrate, coexist, drain, roll back, and recover without violating its public contract or data?*

## Hypothesis

The clean implementation should satisfy this claim: **Service 1.0 and 1.1 both work on the expanded/backfilled schema; rollback succeeds before enforcement; the final constraint is applied only after old writers are gone.** When the lab introduces this fault—**The lab is successful only when service 1.0 fails during the coexistence experiment, the failure is traced to the premature constraint, and the repaired expand migration is preserved as a regression fixture**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Implement and test: Distinguish startup, liveness, readiness, and draining.
2. Implement and test: Order application and schema releases safely.
3. Implement and test: Keep old and new service versions compatible during expansion.
4. Implement and test: Define the rollback boundary explicitly.
5. Implement and test: Release API 1.2 without breaking API 1.1 consumers.

### Required planted defect

Change migration 003 so `result_summary` is immediately non-null without a compatible default.

The lab is successful only when service 1.0 fails during the coexistence experiment, the failure is traced to the premature constraint, and the repaired expand migration is preserved as a regression fixture. Do not “fix” the test by removing service 1.0 from the supported matrix.

### Investigation notes

Before editing code, predict the first observable divergence caused by **The lab is successful only when service 1.0 fails during the coexistence experiment, the failure is traced to the premature constraint, and the repaired expand migration is preserved as a regression fixture**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Execute one controlled transition from service 1.0/API 1.1.0 on migrations 001–002 to service 1.1/API 1.2.0 on migrations 001–005, while preserving the predecessor contract during the supported coexistence window**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Service 1.0 and 1.1 both work on the expanded/backfilled schema; rollback succeeds before enforcement; the final constraint is applied only after old writers are gone.

## Required evidence

- baseline transcript proving the previous checkpoint before **Lifecycle and Compatible Release** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Lifecycle and Compatible Release**
- focused result for: Distinguish startup, liveness, readiness, and draining.
- public, durable, security, or operational observation showing: Course 2 ends with a release-ready service, migrations 001–005, and an additive API 1.2 contract.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **compatible service and schema release**
- a limitation statement naming every live dependency required to support the strongest **Lifecycle and Compatible Release** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Lifecycle and Compatible Release**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **The lab is successful only when service 1.0 fails during the coexistence experiment, the failure is traced to the premature constraint, and the repaired expand migration is preserved as a regression fixture** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Lifecycle and Compatible Release**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Lifecycle and Compatible Release** experiment.
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

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Lifecycle and Compatible Release**. A green command without the negative case and causal explanation does not satisfy this gate.
