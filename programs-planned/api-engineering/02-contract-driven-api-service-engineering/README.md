# Contract-Driven API Service Engineering

**Course 2 of 6 — Make the promise durable**

Implement the fixed contract with durable application, database, worker, storage, and release mechanisms.

> Which internal mechanisms keep the public contract true under concurrency, restart, and partial failure?

## Begin with the course book

1. Read [Course introduction](course-book/index.md).
2. Complete [Start here](course-book/start-here.md) and [orientation](course-book/module-00-orientation/index.md).
3. Follow the ten modules in order.
4. Use the capstone and implementation tracks only through the reading routes named in each chapter.
5. Preserve checkpoint evidence before progressing.

## Modules

01. [Application Use Cases and Boundaries](course-book/module-01-application-use-cases/index.md)
02. [Domain State and Invariants](course-book/module-02-domain-state-invariants/index.md)
03. [Relational Modeling and Migrations](course-book/module-03-relational-modeling-migrations/index.md)
04. [Transactions, Concurrency, ETags, and Idempotency](course-book/module-04-transactions-concurrency-idempotency/index.md)
05. [Queries, Stable Pagination, and Authorized Access](course-book/module-05-query-pagination-authorization/index.md)
06. [Durable Workers and Recovery](course-book/module-06-durable-workers-recovery/index.md)
07. [Streaming and Artifact Integrity](course-book/module-07-streaming-artifact-integrity/index.md)
08. [Transactional Outbox and Webhook Delivery](course-book/module-08-webhooks-transactional-outbox/index.md)
09. [Failure-Oriented Verification](course-book/module-09-failure-proof-architecture/index.md)
10. [Lifecycle and Compatible Release](course-book/module-10-lifecycle-compatible-release/index.md)

## Program boundary

**Incoming:** The immutable Course 1 API 1.1 handoff and its provider-neutral proof corpus.

**Outgoing:** A durable API 1.2 service handoff with migrations 001–005, idempotency, optimistic concurrency, stable pagination, worker recovery, artifact integrity, and transactional webhook delivery.

## Implementation strategy

Choose one primary implementation track. Use the second as an idiomatic comparison and shared-vector parity reference.

## Verification

```bash
make doctor
make core-proof
make manifest-proof
```

Environment-dependent routes are reported separately. Missing infrastructure is never represented as a passing live proof.
