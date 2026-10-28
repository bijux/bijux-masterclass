# Reference Answers — Module 10: Worked answers — Module 10 — Event Platform Governance, Release, and Final Defense

Read after attempting all twelve Event Platform Governance, Release, and Final Defense exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Complete a catalogue entry

Include stable name/type, description, authoritative owner/source, AsyncAPI message/schema/example, channel/address, producer grant, allowed consumers, partition key/rationale, data classification, retention, replay policy, compatibility/lifecycle status, deprecation dates, operational objectives, dead-letter/replay runbooks, and contact.

## 2. Gate a producer release

Reject it. Schema validity cannot compensate for a dual-write window that can lose facts or publish uncommitted facts. Require domain/outbox atomicity, duplicate-publication tests, and reconciliation evidence before considering the contract gates complete.

## 3. Gate a consumer release

Reject or hold as incomplete. Reading current fixtures proves input compatibility, not safe historical deployment. Require new effect/group/target, bounded replay plan, side-effect policy, catch-up/reconciliation, and rollback to v1.

## 4. Deprecate v1

Publish v2 and migration guide; mark v1 deprecated; inventory registered/observed consumers; establish last-publish date; keep v1 schemas/upcasters and runbooks through retention/archive horizon; verify no active replay dependency; record retirement approval; only then remove producer/consumer support.

## 5. Migrate partitioning

Create a versioned channel/type or binding profile, dual-publish or route from one committed fact with dedupe semantics, launch new consumer groups at a known checkpoint, reconcile per-run order/effects, cut producers and consumers deliberately, retain old stream until rollback/retention closes. Never switch hash logic in place.

## 6. Reduce retention

Identify projection rebuild RTO, audit/legal requirements, offline consumer schedules, incident repair horizon, schema/version support, archive alternatives, storage/privacy benefit, and capacity. If replay requires 30 days, seven-day broker retention needs an immutable archive or snapshots+deltas before approval.

## 7. Register an offline consumer

The consumer catalogue records owner, purpose, accepted versions, schedule, start/checkpoint policy, contact, and retirement status. Release/deprecation review uses registry evidence as well as telemetry. Dormancy is not proof of nonexistence.

## 8. Sanitize a handoff

Export public contracts, payload schemas, synthetic non-secret examples, profiles/policies, catalogues, migrations, release identity, and adversarial vectors. Exclude signing secrets, raw dead-letter bodies, private incident details, broker credentials, and generated runtime state. Export sanitized runbook interfaces where needed.

## 9. Prove gate sensitivity

Contract proof rejects unresolved refs/examples; compatibility proof rejects required/removal/narrowing; outbox proof rejects dual write; inbox proof rejects duplicate effect; replay proof rejects side effects/unbounded scope; security proof rejects forged/tenant/sensitive cases; reliability proof rejects retry/dead-letter/backpressure defects; handoff proof rejects secrets/manifest drift.

## 10. Defend technology neutrality

Shared: canonical bytes, envelope/schema decisions, partition function, delivery/effect outcomes, compatibility, replay, security, release status. May differ: class/module layout, async primitives, database adapters, error types, framework middleware, test idioms, and internal optimization—as long as public and durable invariants match.

## 11. Trace one completion fact

Run/artifact transaction and outbox; relay claim; broker accept; outbox mark; channel partition/offset; group delivery/attempt; envelope/payload/security validation; inbox+effect transaction; optional outbound-command outbox; acknowledgement; downstream dispatch. Failures between each durable step create either retry, duplicate, or reconciliation path.

## 12. Respond to final failure

Revoke the key and stop affected producer; preserve broker/outbox/signature evidence; identify key interval/types/tenants; reconcile claimed events against authoritative run state; quarantine uncertain consumer effects; publish correction events or repair projections; rotate keys; run security/reliability proofs; issue a compatible emergency release and update threat/catalogue/runbook evidence.
