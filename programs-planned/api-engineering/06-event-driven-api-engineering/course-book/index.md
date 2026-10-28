# Event-Driven API Engineering

**Course 6 of 6 — Extend the promise across asynchronous time**

> **Central question:** How can independent producers and consumers share durable facts without confusing intent, delivery attempts, processing effects, and historical truth?

## Course responsibility

Design, evolve, secure, operate, and verify asynchronous contracts when delivery may be delayed, duplicated, reordered within declared limits, or replayed. The course inherits earlier guarantees rather than restating them as new work. Its purpose is to add one mature engineering responsibility to the same Analysis Runs Platform.

## Incoming and outgoing boundaries

**Incoming boundary:** The Course 5 API 1.2 service with Security, Reliability, and Performance Profiles 1.0 and migrations 001–009.

**Outgoing boundary:** Analysis Events API 1.0, Event Profile 1.0, AsyncAPI 3.1.0 contract, CloudEvents 1.0 envelope profile, migrations 010–012, replay and dead-letter policy, and governed consumer declarations.

## What you will be able to do

After completing the course, you can:

- create the minimal message taxonomy, publication decision record, owner catalogue, and synchronous/asynchronous boundary.
- publish Analysis Events API 1.0 with canonical envelopes, message schemas, examples, operation ownership, and deterministic bundles.
- implement deterministic delivery attempts, partition order, group independence, acknowledgement expiry, negative acknowledgement, and redelivery.
- implement transactional outbox publication, inbox deduplication, effect-version identity, and atomic consumer effects.
- classify compatibility, add upcasters, preserve source bytes, define retention, and run bounded dry-run replay.
- build notification, analytics, audit, and orchestration consumers with stable derived-command identities and explicit state.
- implement windowed analysis metrics, watermark progression, late-event correction revisions, and quarantine.
- add producer policy, tenant-scoped subscriptions/replay, exact-byte signatures, freshness, classification, and privacy rules.
- implement failure classification, bounded retry, dead-letter records, lag health, replay controls, and operational runbooks.
- publish the catalogue, consumer declarations, accepted/rejected release candidates, final defense, and Course 7 handoff.

## Ten-module learning path

| Day | Module | Governing question | Capstone result |
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
