# Lab — Split authority without splitting truth

> **Module 03:** Data Ownership, Replication, and Cross-Service Query Design

## Objective

Create service-owned data histories and cross-service query paths that declare consistency honestly.

## Why this lab matters

This lab turns the module’s governing question—**How can each service own its writes while the system still answers cross-capability questions without shared tables or hidden distributed transactions?**—into a falsifiable experiment. freeze the target data model and identity rules; create the Artifact-owned store; backfill immutable bytes and metadata with source checksums; record source-to-target identity mapping; compare count, checksum, owner, and retention state; shadow reads against both paths; route new writes to one owner only; retain a bounded rollback read path; remove legacy writers; decommission old data after retention and.

It advances the cumulative Analysis Runs Platform by requiring this result: **Split authoritative data ownership, build versioned projections for cross-service reads, define staleness budgets, and prove reconciliation for missing, duplicate, and out-of-order updates**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Load the data ownership map, legacy migrations 001–015, and final service catalogue.

## Hypothesis

The clean implementation should satisfy this claim: **No service writes another service fact; projections detect gaps; staleness is declared; all planted divergent states produce exact findings.** When the lab introduces this fault—**Implement a versioned Notification run projection and inject duplicate, stale, and gap schedules**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Create independent migration heads for Control, Artifact, Notification, and Platform Catalogue.
2. Implement a versioned Notification run projection and inject duplicate, stale, and gap schedules.
3. Design `run-with-artifacts` using bounded gateway composition and explicit partial response.
4. Create orphan, missing artifact, and missing notification fixtures.
5. Run `make data-proof` and `make reconciliation-proof`.
6. In a PostgreSQL environment, set `TEST_DATABASE_URL` and run `make postgres-proof` to apply every owner-local migration history in an isolated schema.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Implement a versioned Notification run projection and inject duplicate, stale, and gap schedules**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Create service-owned data histories and cross-service query paths that declare consistency honestly**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

No service writes another service fact; projections detect gaps; staleness is declared; all planted divergent states produce exact findings.

## Required evidence

- `capstone/architecture/consistency-policy.yaml`
- `capstone/database/`
- `reports/module-03-data-proof.json`
- live `make postgres-proof` output when PostgreSQL is available

## Interpretation and defense

1. Which state or effect is authoritative for **Data Ownership, Replication, and Cross-Service Query Design**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Implement a versioned Notification run projection and inject duplicate, stale, and gap schedules** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Reset projection fixtures and remove generated database state.

## Completion gate

Data and reconciliation proofs pass with no hidden shared-table access.

A successful command without the required evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Data Ownership, Replication, and Cross-Service Query Design**. A green command without the negative case and causal explanation does not satisfy this gate.
