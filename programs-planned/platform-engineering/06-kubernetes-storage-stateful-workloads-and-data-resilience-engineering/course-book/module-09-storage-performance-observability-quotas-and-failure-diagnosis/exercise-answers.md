# Worked answers — Storage Performance, Observability, Quotas, and Failure Diagnosis

These are complete reference solutions. A different design is valid only when it preserves the same authority, failure, recovery, and evidence boundaries.

## 1. Relate IOPS and throughput

The transfer rate is `1200 × 16 KiB = 19,200 KiB/s`, or 18.75 MiB/s. Latency depends on queueing, concurrency, cache behavior, read/write mix, fsync, backend replication, and operation distribution. The same throughput can come from many parallel slow operations or fewer fast ones. A database with synchronous 4 KiB writes may be latency-bound while using little bandwidth. Report IOPS, size distribution, p50/p99 latency, queue depth, and workload semantics together. Vendor throughput limits alone do not prove application performance.

## 2. Use queue depth as evidence

Average outstanding time is approximately `L/λ = 5/100 = 0.05 seconds`, or 50 ms, for the measured population. This is a consistency check, not a direct p99 latency prediction. The queue may contain mixed operations, batching, cache hits, and variable service times. If application latency rises while backend queue depth grows, saturation is plausible; if queue depth is low, the bottleneck may be locks, CPU, filesystem, or network. Ensure the rate and queue measurements use the same interval and population. Course evidence should record both device and application phases.

## 3. Diagnose rising database latency

Hypothesize that copy-on-write snapshot overhead and pool pressure increase write latency. Establish baseline transaction and fsync latency, backend queue depth, snapshot age/count, and capacity. On a non-authoritative replica or controlled test volume, remove or flatten one eligible old snapshot according to retention policy, or reproduce the chain length with synthetic load. Observe whether queue depth and fsync latency improve without changing application code. Do not delete production recovery points merely to test performance. If the metrics do not change, inspect filesystem, network, or database contention. The experiment must preserve recovery coverage and record the exact backend operation.

## 4. Design bounded metric dimensions

Metrics can use driver, controller/node phase, operation, result code, storage class, topology category, and perhaps cluster or node pool. Raw volume handle, PVC UID, Pod UID, mount path, backup ID, and request ID are high-cardinality and belong in structured logs or traces. A separate gauge can aggregate pending claims by class/topology and attachment usage by node pool. Labels must support an operator decision: “node-publish failures rose for driver X in zone B.” Detailed identities are then retrieved through correlated logs. Cardinality limits should be tested under mass Pod churn because observability can become unavailable during storage incidents.

## 5. Enumerate capacity dimensions

The platform can exhaust provider volume count, per-Node attachment slots, zone-specific capacity, StorageClass quota, API rate limits, snapshot count, snapshot delta pool, inodes, filesystem limits, object count, backup window, KMS quota, or recovery scratch space. Thin provisioning can advertise logical bytes beyond safe physical capacity. A single large volume may exceed maximum object size even when aggregate bytes are free. Capacity dashboards and admission should therefore track each limiting dimension by topology and class. Recovery headroom must be protected separately from ordinary workload growth.

## 6. Separate attach, mount, and I/O failure

Inspect VolumeAttachment and controller-publish status first: if attachment never succeeded, focus on topology, backend attachment, and controller logs. If attached, inspect node-plugin `NodeStageVolume` and `NodePublishVolume` requests, device presence, staging path, target path, and mount table. A stage failure may reflect missing device, filesystem type, or credentials; a publish failure may be target/path/context. If mount succeeds but application I/O fails, inspect filesystem health, permissions, full space/inodes, read-only remount, and device/backend errors. Preserve the phase-specific error and avoid force detach until writer state and backend attachment are understood.

## 7. Model snapshot capacity risk

Copy-on-write snapshots consume backend capacity as source blocks change, often outside the filesystem’s visible used-byte metric. A workload can report ample free filesystem space while the backend pool approaches exhaustion and source writes are at risk. Track snapshot count, age, changed-block or delta consumption, pool physical usage, and delete/merge backlog. Retention must consider write rate and recovery value. Alerting should provide an operator action that preserves restore objectives, such as exporting or expiring an eligible snapshot, rather than deleting indiscriminately. Native backend evidence is required because Kubernetes objects may not expose physical consumption.

## 8. Design storage quotas

Limit requested storage and PVC count per StorageClass, snapshot count and retained bytes where the platform can enforce them, object-store bytes and object count, backup retention, and concurrent restore operations. Separate authoritative production quotas from scratch or preview tiers. Reserve platform and recovery headroom outside tenant allocation. Quota rejection must be visible before partial provisioning when possible and must not force deletion of existing recovery assets. Include growth alerts and an exception process with owner, expiry, cost, and cleanup. Kubernetes ResourceQuota covers only part of the system; backend and repository quotas need their own control plane.

## 9. Evaluate a storage benchmark

Missing evidence includes block-size and read/write distribution, sync behavior, queue depth, cache state, working-set size, test duration, warmup, filesystem and mount options, volume size/tier, zone, instance/node limits, background snapshots, failure behavior, and application-level transaction latency. A short empty-volume run can measure burst credits or cache rather than steady state. It says nothing about backup, restore, durability, cost, or noisy neighbors. Reproduce the database’s fsync and random-write pattern, run long enough to exhaust bursts, record tail latency and errors, and correlate backend metrics. Capacity decisions should include uncertainty and headroom.

## 10. Turn an alert into an operator decision

Alert on the age of the newest independently verified restorable recovery point, not only the last Job start. Use a warning before the RPO budget is consumed and a critical alert when it is exceeded, with a duration that tolerates normal schedule jitter but not repeated failure. Include manifest verification and recent restore-certification status as separate signals. The runbook should identify current backup attempts, repository health, log-chain continuity, keys, and whether to pause risky releases. Page only when an operator action is required; dashboards can show ordinary lag. The alert population and clock must be clearly defined.

## 11. Classify a service-tier change

At most `review-required`, and often rejected if the change is necessary for production correctness. API acceptance establishes only schema and object persistence. Without native evidence, the driver may ignore, reject, partially apply, or apply attributes with different cost or durability. The release record should list the unexecuted capability, affected volumes, rollback strategy, and whether the old profile remains safe. If existing production volumes will mutate irreversibly, absence of native proof is a blocker. The platform must not convert an unavailable test environment into a pass.

## 12. Defend the observability boundary

They can prove operations, timings, error codes, object states, and resource consumption. They cannot know the business meaning of rows, artifact references, tenant ownership, or expected transaction generation unless the application publishes explicit domain evidence. A restore can have perfect infrastructure metrics and still contain the wrong backup or stale schema. Course 6 therefore combines platform telemetry with content digests, recovery generations, and service-owned validation. Observability makes transitions inspectable; it does not become data authority. The release gate requires both system and domain oracles.
