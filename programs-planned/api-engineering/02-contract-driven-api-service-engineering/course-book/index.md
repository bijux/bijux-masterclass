# Contract-Driven API Service Engineering

**Course 2 of 10 — Implement the promise durably**

## Course promise

Turn the fixed Course 1 contract into a durable modular service whose important guarantees survive concurrent requests and process failure.

> **Governing question:** Which application, database, worker, storage, and release mechanisms keep the public contract true under concurrency, restart, and partial failure?

## Place in the program

**Incoming boundary:** The immutable Course 1 API 1.1 handoff and its provider-neutral proof corpus.

**Outgoing boundary:** A durable API 1.2 service with migrations 001–005, persistent idempotency, atomic conditional updates, stable pagination, worker recovery, artifact integrity, transactional webhook delivery, and compatible-release evidence.

Course 2 treats its incoming handoff as historical evidence, not editable scaffolding. It may add only the implement the promise durably mechanisms governed here; any public or durable change requires an explicit compatibility and release decision.

## What you will add

- application use cases and domain invariants;
- PostgreSQL persistence and migration ownership;
- transactions, idempotency, ETags, and stable cursors;
- durable workers, leases, and recovery;
- bounded artifact transfer and transactional outbox delivery;

## Course-level learning outcomes

- Separate transport, application, domain, and infrastructure responsibilities.
- Model legal and illegal state transitions.
- Map relationships and ownership to keys and constraints.
- Draw the transaction boundary for each use case.
- Bind queries to principal, operation, filters, and order.
- Separate durable acceptance from execution.
- Enforce limits while streaming rather than after buffering.
- Explain the dual-write failure.
- Choose the narrowest oracle for each claim.
- Distinguish startup, liveness, readiness, and draining.

## Module map

| Day | Chapter | Governing question | Capstone increment |
|---:|---|---|---|
| 1 | [Application Use Cases and Boundaries](module-01-application-use-cases/index.md) | How does a public operation become an application use case without letting the framework own the system? | Create transport, application, and adapter boundaries for the fixed operation ledger. |
| 2 | [Domain State and Invariants](module-02-domain-state-invariants/index.md) | Which state transitions and invariants must remain true regardless of framework or database? | Implement project, dataset, run, cancellation, and artifact rules as testable domain behavior. |
| 3 | [Relational Modeling and Migrations](module-03-relational-modeling-migrations/index.md) | How should relational structure and migrations reinforce rather than merely store application invariants? | Persist principals, projects, datasets, runs, artifacts, and ownership with constraints and deterministic migrations. |
| 4 | [Transactions, Concurrency, ETags, and Idempotency](module-04-transactions-concurrency-idempotency/index.md) | How do idempotency and conditional updates remain atomic under concurrent requests and process restarts? | Implement persistent request fingerprints, replayed outcomes, version columns, ETags, and transaction rollback. |
| 5 | [Queries, Stable Pagination, and Authorized Access](module-05-query-pagination-authorization/index.md) | How do filters, stable cursors, and authorization-aware queries remain correct while data changes? | Implement owner-bound, filter-bound, high-water keyset traversal and evidence-backed query plans. |
| 6 | [Durable Workers and Recovery](module-06-durable-workers-recovery/index.md) | What makes a 202 Accepted operation honest after the API process or worker dies? | Add durable jobs, leases, heartbeats, fencing, cancellation, duplicate-safe effects, and abandoned-work recovery. |
| 7 | [Streaming and Artifact Integrity](module-07-streaming-artifact-integrity/index.md) | How can large uploads, progress streams, and artifacts remain bounded, durable, and integrity-checked? | Implement streamed upload, content-addressed publication, checksums, SSE/NDJSON progress, and authorized download. |
| 8 | [Transactional Outbox and Webhook Delivery](module-08-webhooks-transactional-outbox/index.md) | How can a committed business change reliably produce an external webhook without a dual write? | Add a transactional outbox, signed deliveries, retry state, deduplication, and destination constraints. |
| 9 | [Failure-Oriented Verification](module-09-failure-proof-architecture/index.md) | How do tests prove transactions, concurrency, restart, storage, and delivery guarantees rather than only happy paths? | Assemble pure, integration, concurrent, process-kill, conformance, and planted-defect proofs. |
| 10 | [Lifecycle and Compatible Release](module-10-lifecycle-compatible-release/index.md) | How can old and new service versions coexist through a database change and still preserve the public contract? | Build lifecycle controls, compatible expand/backfill/enforce migrations, rollback evidence, and release proof. |

## Deliberate boundaries

This course does not claim or teach the following as part of its completion:

- full security engineering;
- SRE and observability operations;
- performance tuning as a goal;
- service decomposition;

Those boundaries prevent the course from becoming a survey of adjacent tools and make its completion claims defensible.

## How to study

Begin with [Start here](start-here.md). In Course 2, read each chapter around the question **Which application, database, worker, storage, and release mechanisms keep the public contract true under concurrency, restart, and partial failure?**; then use the exercises, controlled lab, and checkpoint to turn the explanation into evidence. [Language strategy](language-strategy.md) and [Evidence model](evidence-model.md) define how implementation and proof support—not replace—the course book.

## Completion

Complete all ten checkpoints, the capstone release or defense, and the outgoing handoff. A green command without a defensible claim and evidence boundary is not sufficient.
