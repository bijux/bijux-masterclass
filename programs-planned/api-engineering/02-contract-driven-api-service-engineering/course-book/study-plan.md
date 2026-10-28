# Two-Week Study Plan — Contract-Driven API Service Engineering

## Rhythm

Course 2 uses ten teaching days over two weeks. Orientation freezes the incoming boundary before Day 1; each day moves from the implement the promise durably model to transfer problems, a controlled experiment, and an evidence defense. The middle weekend is for repairing failed checkpoints, not adding features.

| Day | Module | Required result |
|---:|---|---|
| 1 | [Application Use Cases and Boundaries](module-01-application-use-cases/index.md) | Create transport, application, and adapter boundaries for the fixed operation ledger. |
| 2 | [Domain State and Invariants](module-02-domain-state-invariants/index.md) | Implement project, dataset, run, cancellation, and artifact rules as testable domain behavior. |
| 3 | [Relational Modeling and Migrations](module-03-relational-modeling-migrations/index.md) | Persist principals, projects, datasets, runs, artifacts, and ownership with constraints and deterministic migrations. |
| 4 | [Transactions, Concurrency, ETags, and Idempotency](module-04-transactions-concurrency-idempotency/index.md) | Implement persistent request fingerprints, replayed outcomes, version columns, ETags, and transaction rollback. |
| 5 | [Queries, Stable Pagination, and Authorized Access](module-05-query-pagination-authorization/index.md) | Implement owner-bound, filter-bound, high-water keyset traversal and evidence-backed query plans. |
| 6 | [Durable Workers and Recovery](module-06-durable-workers-recovery/index.md) | Add durable jobs, leases, heartbeats, fencing, cancellation, duplicate-safe effects, and abandoned-work recovery. |
| 7 | [Streaming and Artifact Integrity](module-07-streaming-artifact-integrity/index.md) | Implement streamed upload, content-addressed publication, checksums, SSE/NDJSON progress, and authorized download. |
| 8 | [Transactional Outbox and Webhook Delivery](module-08-webhooks-transactional-outbox/index.md) | Add a transactional outbox, signed deliveries, retry state, deduplication, and destination constraints. |
| 9 | [Failure-Oriented Verification](module-09-failure-proof-architecture/index.md) | Assemble pure, integration, concurrent, process-kill, conformance, and planted-defect proofs. |
| 10 | [Lifecycle and Compatible Release](module-10-lifecycle-compatible-release/index.md) | Build lifecycle controls, compatible expand/backfill/enforce migrations, rollback evidence, and release proof. |

## Suggested day

```text
08:30  retrieval practice and checkpoint repair
09:00  chapter reading and diagram reconstruction
11:00  worked examples and standards review
13:00  primary-track implementation reading
15:00  exercises before answers
17:00  controlled lab
19:30  evidence package and checkpoint defense
```

The two-week schedule is subordinate to evidence. If the implement the promise durably argument becomes unclear, stop at the last green checkpoint, reduce the counterexample, and resume only after the owning mechanism is understood.

## Weekend synthesis

At the Week 1 boundary, reconstruct how Modules 1–5 change the platform while preserving this incoming state: The immutable Course 1 API 1.1 handoff and its provider-neutral proof corpus. Rerun those checkpoints and postpone every feature that does not serve the Course 2 responsibility.

## Recovery route

When a checkpoint fails:

1. isolate the first broken invariant;
2. restore the predecessor baseline if necessary;
3. reduce the failing case;
4. repair the owning mechanism;
5. retain the case as a regression;
6. update your explanation before continuing.
