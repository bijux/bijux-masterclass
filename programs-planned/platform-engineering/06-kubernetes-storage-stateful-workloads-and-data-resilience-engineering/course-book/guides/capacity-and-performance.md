# Capacity and storage-performance review

Begin with the application workload, not a provider tier name. Record request sizes, random/sequential pattern, read/write ratio, sync frequency, concurrency, working set, compaction, snapshot, rebuild, and recovery traffic.

## Capacity model

Include:

- current logical and physical data;
- growth rate and uncertainty;
- filesystem and object overhead;
- replica and snapshot amplification;
- maintenance and migration scratch space;
- restore destination capacity;
- namespace/provider quota;
- per-Node attach slots;
- topology-specific free capacity.

## Performance model

Measure p50/p95/p99 latency, throughput, IOPS, queue delay, errors, timeouts, and application commit latency. Separate warm-cache results from backend results. Run long enough to observe throttling, compaction, and burst-credit exhaustion.

## Decision

Approve a class only for the workload shape actually tested. Record headroom, first expected bottleneck, scale lead time, cost, and the correctness properties that must remain unchanged. Reject improvements obtained by weakening flush, replication, encryption, or authorization.
