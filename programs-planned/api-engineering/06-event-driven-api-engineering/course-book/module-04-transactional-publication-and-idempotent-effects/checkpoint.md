# Checkpoint — Transactional Publication, Inbox Deduplication, and Exactly-Once Effects

Do not progress because the chapter has been read. Progress when the following evidence can be reproduced from a clean working tree.

## Demonstrate

- Draw both producer and consumer dual-write windows.
- Explain why mark-before-publish loses events and mark-after-publish duplicates them.
- Define effect-scoped inbox identity.
- State a bounded exactly-once effect claim and its exclusions.

## Required result

- `work/module-04/producer-timeline.json`
- `work/module-04/consumer-timeline.json`
- `work/module-04/effect-proof.json`
- `work/module-04/external-side-effect-design.md`
- `work/module-04/residual-risk.md`

## Commands

```bash
make outbox-inbox-proof
make migration-proof
make module-proof MODULE=04 TRACK=$TRACK
```

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

The checkpoint is complete only when all commands pass, all artifacts are reviewable, and each oral-defense question can be answered without appealing to a broker feature as magic.
