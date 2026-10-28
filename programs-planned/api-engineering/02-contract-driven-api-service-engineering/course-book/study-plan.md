# Ten-Day Study Plan — Contract-Driven API Service Engineering

This is a dense two-week course with one numbered module per weekday. Orientation is required before Day 1 and is not counted as a teaching module. The middle weekend contains no hidden new curriculum.

| Day | Module | Main intellectual move | Required result |
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


## Daily rhythm

A productive day uses four blocks:

- **Model:** read the chapter and reconstruct the governing diagram or state machine;
- **Transfer:** answer the exercises and compare with the reasoned answers;
- **Experiment:** perform the lab, including the failure or pressure condition;
- **Defense:** complete the checkpoint and preserve evidence.

Do not treat “morning to night” as uninterrupted screen time. Use deliberate breaks. Stop blind copying when fatigue removes your ability to predict outcomes.

## Middle weekend

Use Saturday for at most one focused repair cycle per failed checkpoint and for a cross-module synthesis note. Sunday contains no required implementation. Rerun predecessor and accumulated course proofs before Week 2.

## Recovery rule

When behind, reduce breadth before reducing evidence. Complete one language track deeply, keep the comparison focused, and do not skip the failure experiment. A copied second implementation is less valuable than one defended invariant.
