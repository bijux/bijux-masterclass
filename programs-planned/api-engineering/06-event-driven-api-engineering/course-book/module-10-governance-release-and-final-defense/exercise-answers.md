# Worked Answers — Module 10: Event Platform Governance, Release, and Final Defense

Use these solutions to audit your reasoning for **Event Platform Governance, Release, and Final Defense**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Complete a catalogue entry

Include stable name/type, description, authoritative owner/source, AsyncAPI message/schema/example, channel/address, producer grant, allowed consumers, partition key/rationale, data classification, retention, replay policy, compatibility/lifecycle status, deprecation dates, operational objectives, dead-letter/replay runbooks, and contact.

The chapter’s decisive distinction is this: A producer switches from run ID to tenant ID to reduce partition count. Per-run event order and hot-key behavior change for the same event type. Introduce a versioned channel/type migration, dual-consume or checkpoint, then reconcile before retirement.

## 2. Gate a producer release

Reject it. Schema validity cannot compensate for a dual-write window that can lose facts or publish uncommitted facts. Require domain/outbox atomicity, duplicate-publication tests, and reconciliation evidence before considering the contract gates complete.

In the cumulative capstone, the rule becomes concrete: The accepted additive candidate adds an optional safe result classification with defined absence semantics, updated examples, catalogue notes, consumer fixtures, and replay evidence. The breaking candidate makes an old field required and is rejected. The replay-unsafe candidate would resend notifications and is rejected.

## 3. Gate a consumer release

Reject or hold as incomplete. Reading current fixtures proves input compatibility, not safe historical deployment. Require new effect/group/target, bounded replay plan, side-effect policy, catch-up/reconciliation, and rollback to v1.

A useful way to reason about the boundary is: Analytics v2 changes algorithm but shares group and effect identity with v1. Some events are skipped and others use mixed logic during rolling deploy. Release v2 as a new effect/group/target and perform replay/cutover.

## 4. Deprecate v1

Publish v2 and migration guide; mark v1 deprecated; inventory registered/observed consumers; establish last-publish date; keep v1 schemas/upcasters and runbooks through retention/archive horizon; verify no active replay dependency; record retirement approval; only then remove producer/consumer support.

The implementation consequence is: Draft events may be tested in isolated environments but are not public. Active events have supported producers, consumers, schemas, and runbooks. Deprecated events remain valid and supported while consumers migrate. Last-published records the final producer cutoff. Retired means no supported production or replay obligation remains after retention/archive policy.

## 5. Migrate partitioning

Create a versioned channel/type or binding profile, dual-publish or route from one committed fact with dedupe semantics, launch new consumer groups at a known checkpoint, reconcile per-run order/effects, cut producers and consumers deliberately, retain old stream until rollback/retention closes. Never switch hash logic in place.

The important nuance is: Changing a partition key can reorder events, move hot keys, and split one subject’s history across old and new channels. Treat it as a versioned channel/event migration with dual-read or cutover strategy, checkpoints, and reconciliation.

## 6. Reduce retention

Identify projection rebuild RTO, audit/legal requirements, offline consumer schedules, incident repair horizon, schema/version support, archive alternatives, storage/privacy benefit, and capacity. If replay requires 30 days, seven-day broker retention needs an immutable archive or snapshots+deltas before approval.

Under concurrency or failure, the distinction becomes: Service release 1.2.6 preserves HTTP API 1.2 and adds Analysis Events 1.0. Its completion transaction writes immutable event bytes to migration-010 outbox. The relay publishes under explicit channel and partition policy. Notification, analytics, and audit consumers use independent groups/effects and migration-010 inboxes. Migration 011 stores replay checkpoints and dead letters; migration 012 records schema releases.

## 7. Register an offline consumer

The consumer catalogue records owner, purpose, accepted versions, schedule, start/checkpoint policy, contact, and retirement status. Release/deprecation review uses registry evidence as well as telemetry. Dormancy is not proof of nonexistence.

The design remains honest only if: Python and TypeScript must agree on catalogue identity, compatibility classification, replay safety, release status, and exported handoff digests. A candidate accepted by one and rejected by the other is a release blocker until the policy or implementation difference is resolved.

## 8. Sanitize a handoff

Export public contracts, payload schemas, synthetic non-secret examples, profiles/policies, catalogues, migrations, release identity, and adversarial vectors. Exclude signing secrets, raw dead-letter bodies, private incident details, broker credentials, and generated runtime state. Export sanitized runbook interfaces where needed.

The consumer-facing consequence is: A synthetic key from the security lab is copied with the public profile. Even fixture secrets can train unsafe reuse and trigger scanners. Handoff exports verification rules and non-secret vectors, never private key material.

## 9. Prove gate sensitivity

Contract proof rejects unresolved refs/examples; compatibility proof rejects required/removal/narrowing; outbox proof rejects dual write; inbox proof rejects duplicate effect; replay proof rejects side effects/unbounded scope; security proof rejects forged/tenant/sensitive cases; reliability proof rejects retry/dead-letter/backpressure defects; handoff proof rejects secrets/manifest drift.

The operational consequence is: Course 7 needs the stable asynchronous interface and constraints, not every exercise, local fixture, incident log, or secret. The handoff includes AsyncAPI, payload schemas, event and consumer catalogues, profile/policy files, migration 010–012, shared compatibility/security/replay vectors, release identity, and manifest.

## 10. Defend technology neutrality

Shared: canonical bytes, envelope/schema decisions, partition function, delivery/effect outcomes, compatibility, replay, security, release status. May differ: class/module layout, async primitives, database adapters, error types, framework middleware, test idioms, and internal optimization—as long as public and durable invariants match.

The strongest engineering interpretation is: The learner traces AnalysisRunCompleted from authoritative database transaction to outbox, relay, broker record, delivery, inbox/effect, acknowledgement, projection, notification intent, replay, and reconciliation. At each step they name identity, owner, transaction, duplicate window, security check, and durable oracle.

## 11. Trace one completion fact

Run/artifact transaction and outbox; relay claim; broker accept; outbox mark; channel partition/offset; group delivery/attempt; envelope/payload/security validation; inbox+effect transaction; optional outbound-command outbox; acknowledgement; downstream dispatch. Failures between each durable step create either retry, duplicate, or reconciliation path.

The defect-oriented view is: The learner traces AnalysisRunCompleted from authoritative database transaction to outbox, relay, broker record, delivery, inbox/effect, acknowledgement, projection, notification intent, replay, and reconciliation. At each step they name identity, owner, transaction, duplicate window, security check, and durable oracle.

## 12. Respond to final failure

Revoke the key and stop affected producer; preserve broker/outbox/signature evidence; identify key interval/types/tenants; reconcile claimed events against authoritative run state; quarantine uncertain consumer effects; publish correction events or repair projections; rotate keys; run security/reliability proofs; issue a compatible emergency release and update threat/catalogue/runbook evidence.

Across the Python and TypeScript tracks, the invariant is: Then the examiner selects one failure: broker outage, crash after effect, poison schema, compromised key, late event, partition imbalance, or replay storm. The learner must contain, diagnose, recover, and prove correctness using course artifacts.
