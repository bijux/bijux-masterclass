# Event-Driven API Engineering

**Course 6 of 10 — Extend the promise across asynchronous time**

## Course promise

Design, evolve, secure, operate, and verify asynchronous message contracts under delay, duplication, reordering, replay, and consumer failure.

> **Governing question:** How can independent producers and consumers share durable facts without confusing intent, delivery attempts, processing effects, and historical truth?

## Place in the program

**Incoming boundary:** The Course 5 API 1.2 service with Security, Reliability, and Performance Profiles 1.0 and migrations 001–009.

**Outgoing boundary:** Analysis Events API 1.0, Event Profile 1.0, AsyncAPI 3.1.0 contract, CloudEvents 1.0 profile, migrations 010–012, replay and dead-letter policy, and governed consumer declarations.

Course 6 treats its incoming handoff as historical evidence, not editable scaffolding. It may add only the extend the promise across asynchronous time mechanisms governed here; any public or durable change requires an explicit compatibility and release decision.

## What you will add

- event taxonomy and ownership;
- AsyncAPI and CloudEvents contract architecture;
- delivery, ordering, partition, acknowledgement, outbox, and inbox semantics;
- schema evolution, replay, workflows, and event-time processing;
- event security, reliability, dead-letter custody, and governance;

## Course-level learning outcomes

- Separate commands, events, queries, notifications, domain events, and integration events.
- Navigate the AsyncAPI 3.1 document model: servers, channels, operations, messages, components, and bindings.
- Distinguish storage, publication, delivery, processing, effect, and acknowledgement.
- Explain the producer dual-write problem and why ordinary exception handling cannot close it.
- Evaluate event-schema changes from producer, current-consumer, and historical-record perspectives.
- Treat a consumer as a versioned application rather than a handler function.
- Distinguish event time, ingestion time, processing time, and observation time.
- Authenticate producers and consumers independently of message content.
- Classify broker, relay, consumer, dependency, schema, security, and capacity failures.
- Treat the event catalogue as an owned product rather than a topic inventory.

## Module map

| Day | Chapter | Governing question | Capstone increment |
|---:|---|---|---|
| 1 | [Event Thinking, Ownership, and Message Taxonomy](module-01-event-thinking-and-ownership/index.md) | Which interactions are commands, immutable facts, queries, notifications, or private domain events, and who owns each public fact? | Create the minimal message taxonomy, publication decision record, owner catalogue, and synchronous/asynchronous boundary. |
| 2 | [AsyncAPI, CloudEvents, and Contract Architecture](module-02-asyncapi-and-contract-architecture/index.md) | How do AsyncAPI, CloudEvents, schemas, channels, operations, bindings, and examples form one governed event contract? | Publish Analysis Events API 1.0 with canonical envelopes, message schemas, examples, operation ownership, and deterministic bundles. |
| 3 | [Delivery Semantics, Ordering, Partitioning, and Acknowledgement](module-03-delivery-ordering-and-acknowledgement/index.md) | What do acknowledgement, redelivery, ordering, partitioning, lag, and consumer groups actually guarantee? | Implement deterministic delivery attempts, partition order, group independence, acknowledgement expiry, negative acknowledgement, and redelivery. |
| 4 | [Transactional Publication, Inbox Deduplication, and Exactly-Once Effects](module-04-transactional-publication-and-idempotent-effects/index.md) | How do producers avoid dual writes and consumers obtain exactly-once effects on top of at-least-once delivery? | Implement transactional outbox publication, inbox deduplication, effect-version identity, and atomic consumer effects. |
| 5 | [Schema Evolution, Compatibility, Replay, and Historical Truth](module-05-evolution-replay-and-historical-truth/index.md) | How do event schemas evolve while retained historical events remain immutable and replay remains intelligible? | Classify compatibility, add upcasters, preserve source bytes, define retention, and run bounded dry-run replay. |
| 6 | [Consumer Architecture and Asynchronous Workflows](module-06-consumer-architecture-and-workflows/index.md) | How do idempotent consumers, projections, and process managers coordinate asynchronous workflows without hidden synchronous coupling? | Build notification, analytics, audit, and orchestration consumers with stable derived-command identities and explicit state. |
| 7 | [Event-Time Stream Processing, Windows, Watermarks, and Corrections](module-07-event-time-stream-processing/index.md) | How do event time, processing time, windows, watermarks, lateness, and corrections affect derived results? | Implement windowed analysis metrics, watermark progression, late-event correction revisions, and quarantine. |
| 8 | [Event Security, Multi-Tenancy, Privacy, and Trust](module-08-event-security-and-multitenancy/index.md) | How are producers authenticated, consumers authorized, tenants isolated, payloads minimized, and event bytes protected? | Add producer policy, tenant-scoped subscriptions/replay, exact-byte signatures, freshness, classification, and privacy rules. |
| 9 | [Event Reliability, Backpressure, Dead Letters, and Recovery](module-09-event-reliability-and-recovery/index.md) | How do lag, backpressure, retry, poison messages, dead-letter custody, broker failure, and replay storms affect recovery? | Implement failure classification, bounded retry, dead-letter records, lag health, replay controls, and operational runbooks. |
| 10 | [Event Platform Governance, Release, and Final Defense](module-10-governance-release-and-final-defense/index.md) | How are event ownership, compatibility, retention, replay, consumers, evidence, and release decisions governed as a platform capability? | Publish the catalogue, consumer declarations, accepted/rejected release candidates, final defense, and Course 7 handoff. |

## Deliberate boundaries

This course does not claim or teach the following as part of its completion:

- teaching a broker before message semantics;
- claiming exactly-once delivery;
- event sourcing every domain;
- microservice decomposition;

Those boundaries prevent the course from becoming a survey of adjacent tools and make its completion claims defensible.

## How to study

Begin with [Start here](start-here.md). In Course 6, read each chapter around the question **How can independent producers and consumers share durable facts without confusing intent, delivery attempts, processing effects, and historical truth?**; then use the exercises, controlled lab, and checkpoint to turn the explanation into evidence. [Language strategy](language-strategy.md) and [Evidence model](evidence-model.md) define how implementation and proof support—not replace—the course book.

## Completion

Complete all ten checkpoints, the capstone release or defense, and the outgoing handoff. A green command without a defensible claim and evidence boundary is not sufficient.
