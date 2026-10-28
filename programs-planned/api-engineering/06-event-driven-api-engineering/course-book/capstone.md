# Capstone — Event-Driven API Engineering

## Cumulative system

Course 6 continues the Analysis Runs Platform at the point where the previous course stopped. Its capstone exists to extend the promise across asynchronous time while preserving the same projects, datasets, runs, artifacts, identities, and user journeys.

## Inherited state

The Course 5 API 1.2 service with Security, Reliability, and Performance Profiles 1.0 and migrations 001–009.

The inherited boundary is read-only: The Course 5 API 1.2 service with Security, Reliability, and Performance Profiles 1.0 and migrations 001–009. A difficult implementation is not permission to rewrite predecessor contracts, migrations, profiles, or evidence; the current course must solve the problem at its own owning layer.

## Course additions

- event taxonomy and ownership;
- AsyncAPI and CloudEvents contract architecture;
- delivery, ordering, partition, acknowledgement, outbox, and inbox semantics;
- schema evolution, replay, workflows, and event-time processing;
- event security, reliability, dead-letter custody, and governance;

## Increment map

| Module | Mechanism | Cumulative result |
|---:|---|---|
| 1 | Event Thinking, Ownership, and Message Taxonomy | Create the minimal message taxonomy, publication decision record, owner catalogue, and synchronous/asynchronous boundary. |
| 2 | AsyncAPI, CloudEvents, and Contract Architecture | Publish Analysis Events API 1.0 with canonical envelopes, message schemas, examples, operation ownership, and deterministic bundles. |
| 3 | Delivery Semantics, Ordering, Partitioning, and Acknowledgement | Implement deterministic delivery attempts, partition order, group independence, acknowledgement expiry, negative acknowledgement, and redelivery. |
| 4 | Transactional Publication, Inbox Deduplication, and Exactly-Once Effects | Implement transactional outbox publication, inbox deduplication, effect-version identity, and atomic consumer effects. |
| 5 | Schema Evolution, Compatibility, Replay, and Historical Truth | Classify compatibility, add upcasters, preserve source bytes, define retention, and run bounded dry-run replay. |
| 6 | Consumer Architecture and Asynchronous Workflows | Build notification, analytics, audit, and orchestration consumers with stable derived-command identities and explicit state. |
| 7 | Event-Time Stream Processing, Windows, Watermarks, and Corrections | Implement windowed analysis metrics, watermark progression, late-event correction revisions, and quarantine. |
| 8 | Event Security, Multi-Tenancy, Privacy, and Trust | Add producer policy, tenant-scoped subscriptions/replay, exact-byte signatures, freshness, classification, and privacy rules. |
| 9 | Event Reliability, Backpressure, Dead Letters, and Recovery | Implement failure classification, bounded retry, dead-letter records, lag health, replay controls, and operational runbooks. |
| 10 | Event Platform Governance, Release, and Final Defense | Publish the catalogue, consumer declarations, accepted/rejected release candidates, final defense, and Course 7 handoff. |

## Implementation route

Build the complete Course 6 increment in one primary track. Use the second track only after the chapter model is clear, then run shared vectors to test whether **extend the promise across asynchronous time** survives an idiomatic implementation in another runtime.

## Final state

Analysis Events API 1.0, Event Profile 1.0, AsyncAPI 3.1.0 contract, CloudEvents 1.0 profile, migrations 010–012, replay and dead-letter policy, and governed consumer declarations.

## Handoff discipline

The successor receives only the settled result: Analysis Events API 1.0, Event Profile 1.0, AsyncAPI 3.1.0 contract, CloudEvents 1.0 profile, migrations 010–012, replay and dead-letter policy, and governed consumer declarations. Local caches, secrets, ad-hoc reports, and environment-specific artifacts remain outside the handoff.
