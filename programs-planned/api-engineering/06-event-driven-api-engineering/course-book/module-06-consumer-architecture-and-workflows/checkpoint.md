# Checkpoint — Consumer Architecture and Asynchronous Workflows

Do not progress because the chapter has been read. Progress when the following evidence can be reproduced from a clean working tree.

## Demonstrate

- Distinguish consumer group, effect version, and deployment version.
- Explain when choreography is simpler and when orchestration is necessary.
- Describe why command publication cannot advance the process to the requested outcome.
- Define durable timeout and compensation semantics.

## Required result

- `work/module-06/consumer-architecture.md`
- `work/module-06/process-table.md`
- `work/module-06/event-trace.json`
- `work/module-06/evidence.json`
- `work/module-06/residual-risk.md`

## Commands

```bash
make workflow-proof
make outbox-inbox-proof
make module-proof MODULE=06 TRACK=$TRACK
```

## Defend the design

- Walk one run through process states and causation IDs.
- Show that analytics replay cannot send a notification.
- Demonstrate stale timeout behavior.
- Defend one choreography boundary and one orchestration boundary.

## Continue only when

- A consumer lacks owner, effect identity, or replay policy.
- One handler mixes rebuildable and external effects.
- A process advances on command publication rather than fact.
- Timeout or compensation exists only in memory.

The checkpoint is complete only when all commands pass, all artifacts are reviewable, and each oral-defense question can be answered without appealing to a broker feature as magic.
