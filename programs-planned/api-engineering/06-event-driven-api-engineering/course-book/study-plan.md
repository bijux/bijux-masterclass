# Two-Week Study Plan — Event-Driven API Engineering

## Rhythm

Course 6 uses ten teaching days over two weeks. Orientation freezes the incoming boundary before Day 1; each day moves from the extend the promise across asynchronous time model to transfer problems, a controlled experiment, and an evidence defense. The middle weekend is for repairing failed checkpoints, not adding features.

| Day | Module | Required result |
|---:|---|---|
| 1 | [Event Thinking, Ownership, and Message Taxonomy](module-01-event-thinking-and-ownership/index.md) | Create the minimal message taxonomy, publication decision record, owner catalogue, and synchronous/asynchronous boundary. |
| 2 | [AsyncAPI, CloudEvents, and Contract Architecture](module-02-asyncapi-and-contract-architecture/index.md) | Publish Analysis Events API 1.0 with canonical envelopes, message schemas, examples, operation ownership, and deterministic bundles. |
| 3 | [Delivery Semantics, Ordering, Partitioning, and Acknowledgement](module-03-delivery-ordering-and-acknowledgement/index.md) | Implement deterministic delivery attempts, partition order, group independence, acknowledgement expiry, negative acknowledgement, and redelivery. |
| 4 | [Transactional Publication, Inbox Deduplication, and Exactly-Once Effects](module-04-transactional-publication-and-idempotent-effects/index.md) | Implement transactional outbox publication, inbox deduplication, effect-version identity, and atomic consumer effects. |
| 5 | [Schema Evolution, Compatibility, Replay, and Historical Truth](module-05-evolution-replay-and-historical-truth/index.md) | Classify compatibility, add upcasters, preserve source bytes, define retention, and run bounded dry-run replay. |
| 6 | [Consumer Architecture and Asynchronous Workflows](module-06-consumer-architecture-and-workflows/index.md) | Build notification, analytics, audit, and orchestration consumers with stable derived-command identities and explicit state. |
| 7 | [Event-Time Stream Processing, Windows, Watermarks, and Corrections](module-07-event-time-stream-processing/index.md) | Implement windowed analysis metrics, watermark progression, late-event correction revisions, and quarantine. |
| 8 | [Event Security, Multi-Tenancy, Privacy, and Trust](module-08-event-security-and-multitenancy/index.md) | Add producer policy, tenant-scoped subscriptions/replay, exact-byte signatures, freshness, classification, and privacy rules. |
| 9 | [Event Reliability, Backpressure, Dead Letters, and Recovery](module-09-event-reliability-and-recovery/index.md) | Implement failure classification, bounded retry, dead-letter records, lag health, replay controls, and operational runbooks. |
| 10 | [Event Platform Governance, Release, and Final Defense](module-10-governance-release-and-final-defense/index.md) | Publish the catalogue, consumer declarations, accepted/rejected release candidates, final defense, and Course 7 handoff. |

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

The two-week schedule is subordinate to evidence. If the extend the promise across asynchronous time argument becomes unclear, stop at the last green checkpoint, reduce the counterexample, and resume only after the owning mechanism is understood.

## Weekend synthesis

At the Week 1 boundary, reconstruct how Modules 1–5 change the platform while preserving this incoming state: The Course 5 API 1.2 service with Security, Reliability, and Performance Profiles 1.0 and migrations 001–009. Rerun those checkpoints and postpone every feature that does not serve the Course 6 responsibility.

## Recovery route

When a checkpoint fails:

1. isolate the first broken invariant;
2. restore the predecessor baseline if necessary;
3. reduce the failing case;
4. repair the owning mechanism;
5. retain the case as a regression;
6. update your explanation before continuing.
