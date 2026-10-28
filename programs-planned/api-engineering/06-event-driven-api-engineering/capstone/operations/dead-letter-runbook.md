# Dead-letter runbook

## Trigger

An open dead letter appears or the dead-letter rate crosses its alert threshold.

## Diagnose

1. Confirm consumer, effect version, channel, partition, offset, event type, and failure class.
2. Validate the envelope and producer authorization without mutating consumer state.
3. Distinguish permanent contract or policy failure from exhausted transient failure.
4. Correlate with the original event id and existing inbox rows.

## Decide

- **Discard** only when policy proves the event must never affect state.
- **Quarantine** while a contract or security investigation remains open.
- **Replay** only through an approved bounded replay plan.
- **Repair consumer** before replaying a deterministic software defect.

## Safety

Never edit the original event bytes. Never bypass inbox identity. Never acknowledge an unresolved dead letter merely to reduce a metric.

## Exit evidence

Record the operator, decision, replay id if any, before/after projection evidence, and residual risk.
