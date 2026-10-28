# Module 10 — Event Platform Governance, Release, and Final Defense

> **Program stage:** Course 6 of 10 — Extend the promise across asynchronous time.

> **Central question:** How are event ownership, compatibility, retention, replay, consumers, evidence, and release decisions governed as a platform capability?

## Where this module fits

Module 09 produced **Implement failure classification, bounded retry, dead-letter records, lag health, replay controls, and operational runbooks**. This final module consolidates the course by asking: **How are event ownership, compatibility, retention, replay, consumers, evidence, and release decisions governed as a platform capability?**

The capstone must now deliver **Publish the catalogue, consumer declarations, accepted/rejected release candidates, final defense, and Course 7 handoff** while preserving every earlier module result. Successful completion establishes the outgoing boundary for the next course or final program defense: **Analysis Events API 1.0, Event Profile 1.0, AsyncAPI 3.1.0 contract, CloudEvents 1.0 profile, migrations 010–012, replay and dead-letter policy, and governed consumer declarations.**

## Learning outcomes

- Treat the event catalogue as an owned product rather than a topic inventory.
- Define lifecycle stages for draft, active, deprecated, last-published, and retired event versions.
- Gate producer releases on contract, compatibility, catalogue, security, replay, and operational evidence.
- Gate consumer releases on accepted versions, idempotency, lag, dead-letter, replay, and rollback evidence.
- Version partitioning, retention, and schema meaning as public operational commitments.
- Design deprecation and retirement around retained records and consumer migration.
- Produce a minimal sanitized handoff for the next course.
- Defend the complete asynchronous workflow under named failure windows.

## Capstone increment

Publish the catalogue, consumer declarations, accepted/rejected release candidates, final defense, and Course 7 handoff.

## Core event model

### 1. The event catalogue is the operational index

A topic list tells operators where bytes flow. A catalogue tells engineers what each message means, who
owns it, who may publish and consume it, how it is partitioned, how long it is retained, which schemas
and examples define it, whether it is replayable, which consumers depend on it, and how it is retired.

Catalogue completeness is a release gate. An unregistered message cannot be published publicly even if
the broker accepts its subject. Ownership and contact information are actionable; generic teams such as
“platform” are insufficient when no one can approve a correction.

The catalogue should be queryable and diffable. Human-readable pages can be generated from it, but the
machine-readable source remains authoritative.

### 2. Event lifecycle includes retained history

Draft events may be tested in isolated environments but are not public. Active events have supported
producers, consumers, schemas, and runbooks. Deprecated events remain valid and supported while
consumers migrate. Last-published records the final producer cutoff. Retired means no supported
production or replay obligation remains after retention/archive policy.

Deleting a producer does not retire an event if retained records can still reach consumers or be
replayed. Removing a consumer does not remove the producer contract if other consumers remain.

Lifecycle changes record dates, owners, migration guidance, and evidence that no active consumer or
retained-history need remains.

### 3. Producer release gates protect public facts

A producer candidate must pass source tests, AsyncAPI/profile validation, payload examples, schema
compatibility, semantic review, catalogue completeness, producer grants, partition policy, outbox
atomicity, duplicate-publication tolerance, security scanning, and observed publication capacity.

A canary producer may dual-publish or publish a new type under explicit migration policy. It must not
silently change type meaning or partition key in place.

Release evidence names the exact contract/profile versions and source revision. “Tests passed” without
artifact identity cannot govern independently deployed consumers.

### 4. Consumer release gates protect effects

A consumer candidate declares accepted event versions, start position, group/effect identity, inbox
migration, schema fixtures, unknown-value behavior, retry/dead-letter policy, replay mode, resource
budgets, observability, and rollback.

A faster consumer that drops authorization or dedupe is invalid. A consumer that cannot read the oldest
retained event is not release-ready unless retention or migration policy intentionally excludes it.

Rolling deploys need compatibility between old/new instances sharing a group and durable state. A new
effect version normally uses a new group/target rather than sharing half-migrated semantics.

### 5. Partition and retention changes are migrations

Changing a partition key can reorder events, move hot keys, and split one subject’s history across old
and new channels. Treat it as a versioned channel/event migration with dual-read or cutover strategy,
checkpoints, and reconciliation.

Retention reduction can destroy replay and audit capability. Retention increase raises privacy, storage,
and schema-maintenance obligations. Both require catalogue and capacity review.

Broker configuration is therefore not entirely “internal.” When consumers rely on order or recovery
horizon, selected behavior is part of the operational contract.

### 6. Deprecation needs consumer evidence

Announcing deprecation does not migrate consumers. The owner inventories active groups, generated SDKs,
replay jobs, archives, and offline consumers. It publishes a replacement, migration guide, last-publish
date, and retirement conditions.

Consumer telemetry may miss offline or dormant consumers, so registration/catalogue evidence matters.
The team also tests that retained old events can still be interpreted during the deprecation window.

A forced emergency retirement is a security/incident action with explicit risk acceptance and
correction/recovery plan.

### 7. Governance must preserve delivery autonomy

Central standards should define envelope, identity, compatibility categories, security minimums,
catalogue fields, and proof expectations. They should not force every team into one handler framework,
database library, or deployment layout.

Python and TypeScript reference tracks demonstrate this distinction. Public bytes and decisions match;
internal APIs and concurrency models remain idiomatic.

A governance process that requires a central team to manually approve every additive field can become a
bottleneck. Automated gates handle objective rules; owners review semantic and risk decisions.

### 8. The final handoff is deliberately smaller than the course

Course 7 needs the stable asynchronous interface and constraints, not every exercise, local fixture,
incident log, or secret. The handoff includes AsyncAPI, payload schemas, event and consumer catalogues,
profile/policy files, migration 010–012, shared compatibility/security/replay vectors, release identity,
and manifest.

It excludes broker credentials, synthetic signing secrets, dead-letter payloads, local benchmark output,
and private operator evidence. Sanitization is itself tested.

The receiving course verifies the manifest before extending the system, preserving the program’s
continuous story.

### 9. Final defense follows one fact and one failure

The learner traces `AnalysisRunCompleted` from authoritative database transaction to outbox, relay,
broker record, delivery, inbox/effect, acknowledgement, projection, notification intent, replay, and
reconciliation. At each step they name identity, owner, transaction, duplicate window, security check,
and durable oracle.

Then the examiner selects one failure: broker outage, crash after effect, poison schema, compromised key,
late event, partition imbalance, or replay storm. The learner must contain, diagnose, recover, and prove
correctness using course artifacts.

Memorizing product commands is insufficient. The defense is about invariants and evidence.

## Engineering requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Catalogue completeness | Every public command/event has owner, contract, channel, partition, security, retention, replay, and lifecycle. | The broker carries unowned APIs. | Catalogue proof |
| Producer gate | Publication release passes contract, compatibility, atomicity, security, and capacity evidence. | New facts are false, unreadable, or unsafe. | Release report |
| Consumer gate | Effect release passes fixtures, idempotency, replay, failure, lag, and rollback evidence. | Consumers corrupt or lose effects. | Consumer release dossier |
| Lifecycle policy | Deprecation and retirement account for retained records and registered consumers. | Old history becomes unreadable or consumers fail unexpectedly. | Lifecycle record |
| Versioned operational change | Partition and retention changes use migration/cutover plans. | Ordering or recovery guarantees change silently. | Migration plan and reconciliation |
| Sanitized handoff | Only stable public artifacts and non-secret vectors cross course boundary. | Secrets, incidents, or local state become dependencies. | Handoff manifest and scan |
| Proof-sensitive release | Deliberately bad candidates fail for named reasons. | Gates pass everything and provide false confidence. | Planted-defect proof |

## Worked failures

### Case 1 — schema passed, catalogue missing

A new event type validates but has no owner, retention, or replay policy. Reject the release. Contract
structure does not establish organizational responsibility.

### Case 2 — partition key changed in place

A producer switches from run ID to tenant ID to reduce partition count. Per-run event order and hot-key
behavior change for the same event type. Introduce a versioned channel/type migration, dual-consume or
checkpoint, then reconcile before retirement.

### Case 3 — consumer upgrade reused v1 inbox

Analytics v2 changes algorithm but shares group and effect identity with v1. Some events are skipped and
others use mixed logic during rolling deploy. Release v2 as a new effect/group/target and perform
replay/cutover.

### Case 4 — handoff included a signing secret

A synthetic key from the security lab is copied with the public profile. Even fixture secrets can train
unsafe reuse and trigger scanners. Handoff exports verification rules and non-secret vectors, never
private key material.

## Python implementation

`EventCatalog` rejects duplicate or incomplete entries. `evaluate_event_release()` combines schema
compatibility, replay safety, catalogue completeness, and contract validity.

```text
capstone/tracks/python-fastapi/src/event_engineering/catalog.py
capstone/tracks/python-fastapi/src/event_engineering/release.py
capstone/tracks/python-fastapi/tests_event/test_reliability_catalog_release.py
```

The final workshop loads the real catalogue, validates every AsyncAPI message is registered, evaluates all
release fixtures, and generates a machine-readable decision. Reasons remain ordered and stable enough for
CI review.

## TypeScript implementation

TypeScript evaluates the same release inputs and catalogue identities. It does not convert large retention
or offset values unsafely and uses explicit unknown-value handling.

```text
capstone/tracks/typescript-fastify/src/event-engineering/release.ts
capstone/tracks/typescript-fastify/test-event-core/security-reliability.test.mjs
```

The final comparison is not a benchmark contest. Both implementations must reject the same breaking,
replay-unsafe, unauthorized, and incomplete candidates.

## Cross-language invariant

Python and TypeScript must agree on catalogue identity, compatibility classification, replay safety,
release status, and exported handoff digests. A candidate accepted by one and rejected by the other is a
release blocker until the policy or implementation difference is resolved.

The AsyncAPI contract and handoff manifest are language-neutral authorities.

## Design review

Conduct the final review in this order: event meaning and owner; contract/schema; producer transaction;
delivery/partition; consumer effects; evolution/replay; security/privacy; reliability/capacity; lifecycle;
handoff. Starting with dashboards or broker configuration misses the public promise.

For each green proof, name one planted defect it can reject. A proof with no known failure sensitivity is
weak evidence.

## End-to-end worked example

Service release 1.2.6 preserves HTTP API 1.2 and adds Analysis Events 1.0. Its completion transaction writes
immutable event bytes to migration-010 outbox. The relay publishes under explicit channel and partition
policy. Notification, analytics, and audit consumers use independent groups/effects and migration-010
inboxes. Migration 011 stores replay checkpoints and dead letters; migration 012 records schema releases.

The accepted additive candidate adds an optional safe result classification with defined absence semantics,
updated examples, catalogue notes, consumer fixtures, and replay evidence. The breaking candidate makes an
old field required and is rejected. The replay-unsafe candidate would resend notifications and is rejected.

The release runbook can recover from broker outage and duplicate delivery. The handoff exports the released
AsyncAPI, schemas, catalogues, policies, migrations, and vectors with a deterministic manifest. It contains
no credentials or incident payloads.

## Failure patterns

- **Topic inventory.** Addresses are listed without meaning, owner, consumers, or lifecycle.
- **Schema-only release.** Compatibility, security, replay, and operations are ignored.
- **Invisible consumer.** An offline or wildcard consumer blocks retirement but is not registered.
- **In-place partition change.** Order and distribution semantics change under one type.
- **Mixed effect rollout.** New consumer logic shares old group/inbox/target without compatibility proof.
- **Governance framework lock-in.** Teams are forced to copy internal code instead of preserving public invariants.
- **Handoff dumping.** The next course receives secrets, incidents, and runtime state instead of stable contracts.
- **Green-proof theater.** Gates have no planted failures and therefore unknown sensitivity.

## Module synthesis

You are ready to leave this module when you can **treat the event catalogue as an owned product rather than a topic inventory, define lifecycle stages for draft, active, deprecated, last-published, and retired event versions, and gate producer releases on contract, compatibility, catalogue, security, replay, and operational evidence** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Perform one final trace of AnalysisRunCompleted through producer, broker, analytics, notification intent, replay, and reconciliation** and requiring the following oracle: **Only the additive candidate is accepted. Breaking and replay-unsafe candidates fail for exact reasons. Every public message and consumer is catalogued. The completion trace preserves one fact and one effect per effect version under duplicate windows. The tabletop has containment, recovery, reconciliation, and residual risk. The handoff is complete, deterministic, and sanitized.**

The cumulative platform now includes **Publish the catalogue, consumer declarations, accepted/rejected release candidates, final defense, and Course 7 handoff**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Complete the course final defense and outgoing handoff described in [Capstone](../capstone.md). Course 7 may treat only the manifested handoff as settled.
