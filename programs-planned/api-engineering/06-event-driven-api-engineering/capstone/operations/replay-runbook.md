# Replay runbook

## Preconditions

An approved replay plan names the consumer, effect version, tenant, event types, time range, maximum events, mode, and checkpoint interval. External side effects are disabled.

## Dry run

Select historical events without changing the projection. Record selected, rejected, would-apply, and invariant-failure counts. Compare the resulting digest with the expected projection model.

## Apply

Use a new effect version for a projection rebuild. Persist checkpoints. Stop if the event bound is exceeded, a schema is unsupported, invariants fail, or infrastructure degrades.

## Cutover

Compare old and new projections, document accepted differences, switch readers deliberately, and retain rollback evidence.

## Prohibited shortcuts

Do not reset consumer offsets and hope. Do not replay external notifications. Do not mutate historical event bytes. Do not delete the old projection before comparison.
