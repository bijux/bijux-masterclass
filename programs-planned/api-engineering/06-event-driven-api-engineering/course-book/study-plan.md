# Ten-Day Study Plan — Event-Driven API Engineering

This is a dense two-week course with one numbered module per weekday. Orientation is required before Day 1 and is not counted as a teaching module. The middle weekend contains no hidden new curriculum.

| Day | Module | Main intellectual move | Required result |
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
