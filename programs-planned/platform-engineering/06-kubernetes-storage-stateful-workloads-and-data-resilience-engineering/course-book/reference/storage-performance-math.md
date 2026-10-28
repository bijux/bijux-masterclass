# Storage performance mathematics

Useful first-order relationships:

```text
throughput ≈ IOPS × average operation size
utilization = offered work / service capacity
queue time grows rapidly as utilization approaches saturation
```

A device performing 8,000 operations/s with 4 KiB requests transfers roughly 31.25 MiB/s. The same throughput with 1 MiB requests requires only about 31 operations/s. This is why IOPS and bandwidth must be interpreted with request size and access pattern.

## Little’s Law

For a stable system:

```text
concurrency ≈ throughput × average time in system
```

If 200 operations/s each spend 50 ms in the storage path, average in-flight work is approximately 10 operations. Rising concurrency without higher throughput indicates queueing or saturation.

## Tail latency

Average latency hides flush, compaction, rebuild, snapshot, garbage collection, and noisy-neighbour effects. Record p50, p95, p99, timeout rate, and queue depth. Separate buffered write latency from durable commit latency.

## Capacity headroom

Usable capacity must reserve space and performance for maintenance. A system that can hold current data but cannot compact, rebuild, snapshot, or restore is already over capacity. Forecast growth, recovery copies, temporary migration space, and attach-slot limits together.

## Correctness gate

Performance evidence is invalid when the candidate changes durability, consistency, encryption, authorization, or recovery semantics without an approved contract change.
