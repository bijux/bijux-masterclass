# Checkpoint — Module 06: Consumer Architecture and Asynchronous Workflows

## Required result

Build notification, analytics, audit, and orchestration consumers with stable derived-command identities and explicit state.

## Demonstrate

- Distinguish consumer group, effect version, and deployment version.
- Explain when choreography is simpler and when orchestration is necessary.
- Describe why command publication cannot advance the process to the requested outcome.
- Define durable timeout and compensation semantics.

## Commands

```bash
make workflow-proof
make outbox-inbox-proof
make module-proof MODULE=06 TRACK=$TRACK
```

## Evidence to retain

- `work/module-06/consumer-architecture.md`
- `work/module-06/process-table.md`
- `work/module-06/event-trace.json`
- final states for all four consumers
- command outbox and stale-timer evidence
- planted-defect rejection
- output from `make workflow-proof`

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

The **Consumer Architecture and Asynchronous Workflows** checkpoint is complete only when the commands pass, the retained artifacts explain the event-system state, and you can defend the result without treating broker delivery, ordering, or replay as magic.
