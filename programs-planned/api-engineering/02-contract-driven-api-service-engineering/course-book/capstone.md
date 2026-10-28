# Capstone — Contract-Driven API Service Engineering

## Cumulative system

Course 2 continues the Analysis Runs Platform at the point where the previous course stopped. Its capstone exists to implement the promise durably while preserving the same projects, datasets, runs, artifacts, identities, and user journeys.

## Inherited state

The immutable Course 1 API 1.1 handoff and its provider-neutral proof corpus.

The inherited boundary is read-only: The immutable Course 1 API 1.1 handoff and its provider-neutral proof corpus. A difficult implementation is not permission to rewrite predecessor contracts, migrations, profiles, or evidence; the current course must solve the problem at its own owning layer.

## Course additions

- application use cases and domain invariants;
- PostgreSQL persistence and migration ownership;
- transactions, idempotency, ETags, and stable cursors;
- durable workers, leases, and recovery;
- bounded artifact transfer and transactional outbox delivery;

## Increment map

| Module | Mechanism | Cumulative result |
|---:|---|---|
| 1 | Application Use Cases and Boundaries | Create transport, application, and adapter boundaries for the fixed operation ledger. |
| 2 | Domain State and Invariants | Implement project, dataset, run, cancellation, and artifact rules as testable domain behavior. |
| 3 | Relational Modeling and Migrations | Persist principals, projects, datasets, runs, artifacts, and ownership with constraints and deterministic migrations. |
| 4 | Transactions, Concurrency, ETags, and Idempotency | Implement persistent request fingerprints, replayed outcomes, version columns, ETags, and transaction rollback. |
| 5 | Queries, Stable Pagination, and Authorized Access | Implement owner-bound, filter-bound, high-water keyset traversal and evidence-backed query plans. |
| 6 | Durable Workers and Recovery | Add durable jobs, leases, heartbeats, fencing, cancellation, duplicate-safe effects, and abandoned-work recovery. |
| 7 | Streaming and Artifact Integrity | Implement streamed upload, content-addressed publication, checksums, SSE/NDJSON progress, and authorized download. |
| 8 | Transactional Outbox and Webhook Delivery | Add a transactional outbox, signed deliveries, retry state, deduplication, and destination constraints. |
| 9 | Failure-Oriented Verification | Assemble pure, integration, concurrent, process-kill, conformance, and planted-defect proofs. |
| 10 | Lifecycle and Compatible Release | Build lifecycle controls, compatible expand/backfill/enforce migrations, rollback evidence, and release proof. |

## Implementation route

Build the complete Course 2 increment in one primary track. Use the second track only after the chapter model is clear, then run shared vectors to test whether **implement the promise durably** survives an idiomatic implementation in another runtime.

## Final state

A durable API 1.2 service with migrations 001–005, persistent idempotency, atomic conditional updates, stable pagination, worker recovery, artifact integrity, transactional webhook delivery, and compatible-release evidence.

## Handoff discipline

The successor receives only the settled result: A durable API 1.2 service with migrations 001–005, persistent idempotency, atomic conditional updates, stable pagination, worker recovery, artifact integrity, transactional webhook delivery, and compatible-release evidence. Local caches, secrets, ad-hoc reports, and environment-specific artifacts remain outside the handoff.
