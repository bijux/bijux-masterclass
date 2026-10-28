# Event-Driven API Engineering

**Course 6 of 6 — Extend the promise across asynchronous time**

Design, evolve, secure, operate, and verify asynchronous contracts when delivery may be delayed, duplicated, reordered within declared limits, or replayed.

> How can independent producers and consumers share durable facts without confusing intent, delivery attempts, processing effects, and historical truth?

## Begin with the course book

1. Read [Course introduction](course-book/index.md).
2. Complete [Start here](course-book/start-here.md) and [orientation](course-book/module-00-orientation/index.md).
3. Follow the ten modules in order.
4. Use the capstone and implementation tracks only through the reading routes named in each chapter.
5. Preserve checkpoint evidence before progressing.

## Modules

01. [Event Thinking, Ownership, and Message Taxonomy](course-book/module-01-event-thinking-and-ownership/index.md)
02. [AsyncAPI, CloudEvents, and Contract Architecture](course-book/module-02-asyncapi-and-contract-architecture/index.md)
03. [Delivery Semantics, Ordering, Partitioning, and Acknowledgement](course-book/module-03-delivery-ordering-and-acknowledgement/index.md)
04. [Transactional Publication, Inbox Deduplication, and Exactly-Once Effects](course-book/module-04-transactional-publication-and-idempotent-effects/index.md)
05. [Schema Evolution, Compatibility, Replay, and Historical Truth](course-book/module-05-evolution-replay-and-historical-truth/index.md)
06. [Consumer Architecture and Asynchronous Workflows](course-book/module-06-consumer-architecture-and-workflows/index.md)
07. [Event-Time Stream Processing, Windows, Watermarks, and Corrections](course-book/module-07-event-time-stream-processing/index.md)
08. [Event Security, Multi-Tenancy, Privacy, and Trust](course-book/module-08-event-security-and-multitenancy/index.md)
09. [Event Reliability, Backpressure, Dead Letters, and Recovery](course-book/module-09-event-reliability-and-recovery/index.md)
10. [Event Platform Governance, Release, and Final Defense](course-book/module-10-governance-release-and-final-defense/index.md)

## Program boundary

**Incoming:** The Course 5 API 1.2 service with Security, Reliability, and Performance Profiles 1.0 and migrations 001–009.

**Outgoing:** Analysis Events API 1.0, Event Profile 1.0, AsyncAPI 3.1.0 contract, CloudEvents 1.0 envelope profile, migrations 010–012, replay and dead-letter policy, and governed consumer declarations.

## Implementation strategy

Choose one primary implementation track. Compare canonical bytes, delivery outcomes, replay semantics, and consumer effects across both languages.

## Verification

```bash
make doctor
make core-proof
make manifest-proof
```

Environment-dependent routes are reported separately. Missing infrastructure is never represented as a passing live proof.
