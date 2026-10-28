# Checkpoint — Module 03: Delivery Semantics, Ordering, Partitioning, and Acknowledgement

## Required result

Implement deterministic delivery attempts, partition order, group independence, acknowledgement expiry, negative acknowledgement, and redelivery.

## Demonstrate

- State at-most-once and at-least-once at the correct semantic layer.
- Draw the delivery state machine and all settlement transitions.
- Explain the per-partition order guarantee and its concurrency consequence.
- Distinguish consumer group identity from consumer instance identity.

## Commands

```bash
make delivery-proof
make vector-proof
make module-proof MODULE=03 TRACK=$TRACK
```

## Evidence to retain

- `work/module-03/delivery-trace.json`
- `work/module-03/failure-window-table.md`
- `work/module-03/lag-snapshots.json`
- the redelivery attempt identities
- the token-reuse failure
- output from `make delivery-proof`
- optional NATS comparison clearly labeled as live or not executed

## Defend the design

- Demonstrate the same record at two delivery attempts.
- Explain why acknowledgement after effect still permits duplicate handling.
- Defend the chosen partition key for run lifecycle.
- Describe what retention must preserve for replay.

## Continue only when

- A delivery claim uses “exactly once” without a named layer.
- Any required order crosses partitions without an explicit mechanism.
- An independent effect shares another effect’s consumer group.
- Retry or acknowledgement timing is unbounded.

The **Delivery Semantics, Ordering, Partitioning, and Acknowledgement** checkpoint is complete only when the commands pass, the retained artifacts explain the event-system state, and you can defend the result without treating broker delivery, ordering, or replay as magic.
