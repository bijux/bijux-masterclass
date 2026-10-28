# MetricRail Runbook

## Rising queue residence

1. Confirm offered, admitted, completed, and rejected work.
2. Inspect queue depth, active connections, CPU, and broker service time.
3. Determine whether the bottleneck is parsing, lookup, snapshot work, downstream I/O, or host saturation.
4. Reduce admission or disable expensive snapshots before increasing queue capacity.
5. Roll back if the change correlates with a new artifact and promotion criteria fail.

## Memory increasing with stable series count

1. Compare retained identifier bytes, queue depth, active snapshots, and connection buffers.
2. Check for large reusable buffers, shared views, or trace/cardinality growth.
3. Run a heap or process-memory profile on the profiling artifact.
4. Do not restart repeatedly without preserving a profile if the service remains safe.

## Readiness false

1. Check whether shutdown or quiescing was requested.
2. Confirm broker task health.
3. Inspect overload and internal-failure events.
4. Stop promotion. Restore the last known artifact if readiness does not recover within the defined window.

## Overload rejection rising

1. Confirm that completed throughput is stable and accepted latency remains within objective.
2. Identify the first saturated resource.
3. Verify clients are not amplifying load through retries.
4. Apply per-tenant or global admission policy. Do not hide rejection by growing queues without a new capacity model.

## Snapshot failures

1. Distinguish snapshot-size limit, broker overload, and internal failure.
2. Preserve ingestion if the degraded-mode contract permits it.
3. Reduce snapshot frequency or scope rather than increasing output limits blindly.
