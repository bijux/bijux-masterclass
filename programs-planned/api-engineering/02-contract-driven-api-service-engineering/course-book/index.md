# Contract-Driven API Service Engineering

**Course 2 of 6 — Make the promise durable**

> **Central question:** Which internal mechanisms keep the public contract true under concurrency, restart, and partial failure?

## Course responsibility

Implement the fixed contract with durable application, database, worker, storage, and release mechanisms. The course inherits earlier guarantees rather than restating them as new work. Its purpose is to add one mature engineering responsibility to the same Analysis Runs Platform.

## Incoming and outgoing boundaries

**Incoming boundary:** The immutable Course 1 API 1.1 handoff and its provider-neutral proof corpus.

**Outgoing boundary:** A durable API 1.2 service handoff with migrations 001–005, idempotency, optimistic concurrency, stable pagination, worker recovery, artifact integrity, and transactional webhook delivery.

## What you will be able to do

After completing the course, you can:

- create transport, application, and adapter boundaries for the fixed operation ledger.
- implement project, dataset, run, cancellation, and artifact rules as testable domain behavior.
- persist principals, projects, datasets, runs, artifacts, and ownership with constraints and deterministic migrations.
- implement persistent request fingerprints, replayed outcomes, version columns, ETags, and transaction rollback.
- implement owner-bound, filter-bound, high-water keyset traversal and evidence-backed query plans.
- add durable jobs, leases, heartbeats, fencing, cancellation, duplicate-safe effects, and abandoned-work recovery.
- implement streamed upload, content-addressed publication, checksums, SSE/NDJSON progress, and authorized download.
- add a transactional outbox, signed deliveries, retry state, deduplication, and destination constraints.
- assemble pure, integration, concurrent, process-kill, conformance, and planted-defect proofs.
- build lifecycle controls, compatible expand/backfill/enforce migrations, rollback evidence, and release proof.

## Ten-module learning path

| Day | Module | Governing question | Capstone result |
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


## How the book is organized

Each numbered module has five learner-facing files:

1. `index.md` — the complete explanation, worked designs, implementation reading, failure analysis, and transition;
2. `exercises.md` — twelve transfer questions;
3. `exercise-answers.md` — matching reasoned reference answers;
4. `lab.md` — one controlled failure, pressure, or release experiment;
5. `checkpoint.md` — the evidence required before progression.

The course book is authoritative. Capstone source, fixtures, reports, and proof scripts make the material executable; they do not replace the explanation.

## Completion standard

You complete the course only when every module checkpoint, the capstone proof, and the final defense pass. A strong result states not only what worked but which claim was established, which evidence class supports it, and what remains unexecuted.

Continue with [Start here](start-here.md).
