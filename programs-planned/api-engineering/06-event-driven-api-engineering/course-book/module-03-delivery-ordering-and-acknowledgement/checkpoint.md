# Checkpoint — Delivery Semantics, Ordering, Partitioning, and Acknowledgement

Do not progress because the chapter has been read. Progress when the following evidence can be reproduced from a clean working tree.

## Demonstrate

- State at-most-once and at-least-once at the correct semantic layer.
- Draw the delivery state machine and all settlement transitions.
- Explain the per-partition order guarantee and its concurrency consequence.
- Distinguish consumer group identity from consumer instance identity.

## Required result

- `work/module-03/delivery-trace.json`
- `work/module-03/failure-window-table.md`
- `work/module-03/lag-snapshots.json`
- `work/module-03/evidence.json`
- `work/module-03/residual-risk.md`

## Commands

```bash
make delivery-proof
make vector-proof
make module-proof MODULE=03 TRACK=$TRACK
```

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

The checkpoint is complete only when all commands pass, all artifacts are reviewable, and each oral-defense question can be answered without appealing to a broker feature as magic.
