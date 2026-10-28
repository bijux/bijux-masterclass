# Checkpoint — Module 04: Transactional Publication, Inbox Deduplication, and Exactly-Once Effects

## Required result

Implement transactional outbox publication, inbox deduplication, effect-version identity, and atomic consumer effects.

## Demonstrate

- Draw both producer and consumer dual-write windows.
- Explain why mark-before-publish loses events and mark-after-publish duplicates them.
- Define effect-scoped inbox identity.
- State a bounded exactly-once effect claim and its exclusions.

## Commands

```bash
make outbox-inbox-proof
make migration-proof
make module-proof MODULE=04 TRACK=$TRACK
```

## Evidence to retain

- `work/module-04/producer-timeline.json`
- `work/module-04/consumer-timeline.json`
- event-body digests for both broker records
- inbox and projection snapshots
- one external-side-effect boundary design
- output from `make outbox-inbox-proof`
- optional PostgreSQL evidence marked executed or not executed

## Defend the design

- Show the crash-after-broker-accept duplicate.
- Show why an independent consumer is not suppressed by the inbox.
- Explain how concurrent duplicates are arbitrated in PostgreSQL.
- Describe how a notification provider receives a stable idempotency key.

## Continue only when

- Domain state and publication intent are not atomic.
- Inbox and effect are not atomic.
- Deduplication uses delivery token or transport offset.
- An external side effect lacks an idempotency/outbox boundary.

The **Transactional Publication, Inbox Deduplication, and Exactly-Once Effects** checkpoint is complete only when the commands pass, the retained artifacts explain the event-system state, and you can defend the result without treating broker delivery, ordering, or replay as magic.
