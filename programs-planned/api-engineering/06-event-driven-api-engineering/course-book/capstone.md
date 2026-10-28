# Capstone — Event-Driven API Engineering

## One continuing platform

The capstone is the Analysis Runs Platform. Principals create projects, register datasets, submit analysis runs, observe progress, retrieve verified artifacts, and receive or consume completion facts. Course 6 does not replace the platform; it adds the responsibility **extend the promise across asynchronous time**.

## Starting state

The Course 5 API 1.2 service with Security, Reliability, and Performance Profiles 1.0 and migrations 001–009.

## Course increments

| Module | Platform increment |
|---:|---|
| 1 | Create the minimal message taxonomy, publication decision record, owner catalogue, and synchronous/asynchronous boundary. |
| 2 | Publish Analysis Events API 1.0 with canonical envelopes, message schemas, examples, operation ownership, and deterministic bundles. |
| 3 | Implement deterministic delivery attempts, partition order, group independence, acknowledgement expiry, negative acknowledgement, and redelivery. |
| 4 | Implement transactional outbox publication, inbox deduplication, effect-version identity, and atomic consumer effects. |
| 5 | Classify compatibility, add upcasters, preserve source bytes, define retention, and run bounded dry-run replay. |
| 6 | Build notification, analytics, audit, and orchestration consumers with stable derived-command identities and explicit state. |
| 7 | Implement windowed analysis metrics, watermark progression, late-event correction revisions, and quarantine. |
| 8 | Add producer policy, tenant-scoped subscriptions/replay, exact-byte signatures, freshness, classification, and privacy rules. |
| 9 | Implement failure classification, bounded retry, dead-letter records, lag health, replay controls, and operational runbooks. |
| 10 | Publish the catalogue, consumer declarations, accepted/rejected release candidates, final defense, and Course 7 handoff. |


## Language tracks

Choose one primary implementation track. Compare canonical bytes, delivery outcomes, replay semantics, and consumer effects across both languages.

Shared fixtures, vectors, operation maps, releases, and black-box scenarios define parity. Identical class names or directory shape do not.

## Capstone reading order

1. read the module chapter and identify the owning mechanism;
2. inspect the narrow source path named by the chapter;
3. inspect the corresponding test or vector;
4. run the focused proof;
5. perform the lab modification in a working branch;
6. return to the chapter and explain how the implementation realizes the model.

## Handoff discipline

The predecessor material is read-only evidence. The current course may add a compatible public interface, migration, or profile only when its release rules permit it. It must not rewrite earlier history to simplify the present implementation.

**Outgoing handoff:** Analysis Events API 1.0, Event Profile 1.0, AsyncAPI 3.1.0 contract, CloudEvents 1.0 envelope profile, migrations 010–012, replay and dead-letter policy, and governed consumer declarations.

## Final capstone question

Can you trace one accepted case and one rejected, failed, overloaded, or duplicated case from the public boundary to the authoritative outcome, then name the proof and limitation at every layer this course owns?
