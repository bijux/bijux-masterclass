# Consumer lag runbook

## Trigger

Lag count, oldest unprocessed age, or both enter warning or critical state.

## Diagnose

1. Confirm whether offered rate increased or service rate decreased.
2. Inspect the oldest event age; a large count with young events is different from one ancient blocked partition.
3. Check partition skew, poison-message retries, database saturation, and downstream latency.
4. Verify that retry loops are not amplifying load.

## Contain

Pause nonessential replays, enforce admission bounds, isolate a poison partition if the transport supports it, and preserve ordering promises.

## Recover

Increase consumers only when the downstream database and effect boundaries can absorb the concurrency. Validate backlog-drain time rather than relying on instance count.

## Exit evidence

Lag and oldest age return below recovery thresholds, no duplicate effects appear, and the identified bottleneck has a documented owner.
