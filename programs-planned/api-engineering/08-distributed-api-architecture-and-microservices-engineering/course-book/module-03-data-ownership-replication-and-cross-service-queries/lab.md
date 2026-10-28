# Lab — Split authority without splitting truth

**Module:** Data Ownership, Replication, and Cross-Service Query Design

## Objective

Create service-owned data histories and cross-service query paths that declare consistency honestly.

## Setup

Load the data ownership map, legacy migrations 001–015, and final service catalogue.

## Controlled actions

1. Create independent migration heads for Control, Artifact, Notification, and Platform Catalogue.
2. Implement a versioned Notification run projection and inject duplicate, stale, and gap schedules.
3. Design `run-with-artifacts` using bounded gateway composition and explicit partial response.
4. Create orphan, missing artifact, and missing notification fixtures.
5. Run `make data-proof` and `make reconciliation-proof`.
6. In a PostgreSQL environment, set `TEST_DATABASE_URL` and run `make postgres-proof` to apply every owner-local migration history in an isolated schema.

## Correctness oracle

No service writes another service fact; projections detect gaps; staleness is declared; all planted divergent states produce exact findings.

## Required evidence

- `capstone/architecture/consistency-policy.yaml`
- `capstone/database/`
- `reports/module-03-data-proof.json`
- live `make postgres-proof` output when PostgreSQL is available

## Cleanup

Reset projection fixtures and remove generated database state.

## Completion gate

Data and reconciliation proofs pass with no hidden shared-table access.

A successful command without the required evidence does not complete the lab.
