# MetricRail Capacity Model

MetricRail’s initial production envelope must be derived from a named workload and host. This document records the variables and the decision process; it does not embed portable throughput numbers.

## Bounded resources

| Resource | Configuration |
|---|---|
| simultaneous connections | `max_connections` |
| broker mailbox | `mailbox_capacity` |
| active ingestion | `max_active_ingest` |
| series | `max_series` |
| retained identifier bytes | `max_identifier_storage_bytes` |
| input line | `max_line_bytes` |
| snapshot output | `max_snapshot_bytes` |
| offline records | `max_offline_records` |
| offline input bytes | `max_offline_bytes` |

## Memory estimate

Estimate at least:

```text
fixed process and runtime
+ active connections × bytes per connection
+ queued commands × bytes per command
+ series × measured bytes per series
+ retained identifier bytes
+ one maximum snapshot
+ tracing and allocator headroom
```

Use checked arithmetic. Compare the estimate with process-level measurement under common, skewed, high-cardinality, snapshot-heavy, and shutdown workloads. The estimate is a planning model; resident memory remains a target observation.

## Throughput envelope

Run a concurrency sweep and record offered, admitted, completed, rejected, p50, p95, p99, queue residence, service time, CPU, and memory. Identify the knee where latency accelerates or throughput stops scaling. The initial envelope must remain below that point and preserve failover and rollout headroom.

## Revisit triggers

Repeat capacity work when:

- record or identifier limits change;
- the map representation changes;
- batching or sharding is introduced;
- runtime or dependency versions change materially;
- the workload distribution or tenant skew changes;
- the deployment host changes;
- a new snapshot or export path is added.
