# Module 09 — Storage Performance, Observability, Quotas, and Failure Diagnosis

> **Governing question:** How do we distinguish slow applications, saturated storage, controller lag, mount failure, quota exhaustion, and capacity risk before data service quality collapses?

## Why this module exists

Atlas request latency rises while CPU remains low. The database reports fsync latency spikes. CSI controller metrics look healthy, but a snapshot copy-on-write chain has grown and backend queue depth is saturated. Scaling the API increases pressure and worsens the incident.

This module does not begin with YAML. It begins by locating authority and the earliest missing transition. Kubernetes storage is a set of cooperating control loops around an external data system; the application still owns the meaning and correctness of the data.

## Learning outcomes

- relate IOPS, throughput, latency, queue depth, block size, and concurrency
- separate application, filesystem, node, CSI, network, and backend signals
- design storage service indicators and budgets
- diagnose attach, mount, expansion, snapshot, and restore failures
- apply namespace quotas and backend capacity guardrails
- evaluate performance claims through representative workloads

## Storage performance is a workload interaction

IOPS counts operations, throughput counts bytes per time, and latency measures completion time. Block size links IOPS and throughput. Queue depth and concurrency determine how much work is outstanding. A device can deliver high sequential throughput and poor random-write latency. A database can issue fsync-heavy small writes that are invisible in aggregate bandwidth.

Course 6 performance claims name operation mix, read/write ratio, block size, concurrency, working set, cache state, duration, and failure mode. Vendor maximums are not workload evidence.
## The path has several queues

An application queues operations, the filesystem and kernel cache them, the block layer schedules requests, CSI and transport may add network latency, and the backend maintains its own queues and replication work. A high application latency with low backend latency can indicate lock contention or filesystem behavior. High backend latency with growing queue depth indicates saturation. Mount or attachment failures are control-plane issues rather than steady-state I/O performance.

Atlas observations preserve phase boundaries: provision, attach, stage, publish, read, write, fsync, snapshot, backup, and restore.
## Metrics need bounded dimensions

Useful storage metrics include PVC requested and used bytes, inode use, volume health, attach and mount latency, failed operations by phase, backend latency histograms, throughput, IOPS, queue depth, snapshot age, backup age, restore success, and capacity by class and topology. Labels such as volume handle, Pod UID, or path can create unbounded cardinality.

The platform uses stable class, namespace, workload, driver, operation, and result dimensions for aggregate metrics, while detailed identities remain in logs or traces with retention controls.
## Capacity is more than free bytes

A cluster can run out of storage class capacity, provider quota, volume count, attachment slots, snapshot capacity, inode space, object count, API rate limits, or backup window. Thin-provisioned systems may advertise more logical capacity than physical safety permits. Snapshots consume delta space and can make source writes fail when pools fill.

Atlas capacity plans include growth rate, retention, replication overhead, snapshots, restore scratch space, and emergency headroom. Admission blocks new stateful workloads before the platform reaches an unrecoverable threshold.
## Failure signatures accelerate diagnosis

A Pending PVC with provisioning events is different from a Bound PVC with a Pod blocked on attachment. A successful attachment with `FailedMount` points to node-side preparation. `FileSystemResizePending` identifies a resize phase. A snapshot stuck before content creation differs from one whose backend snapshot exists but status is stale. A full filesystem can manifest as application errors even while the volume and Pod remain healthy.

The course’s failure catalogue maps symptoms to the earliest missing transition, authoritative objects, native evidence commands, and unsafe interventions to avoid.
## Performance changes are data-plane releases

Changing StorageClass parameters, VolumeAttributesClass, filesystem options, mount options, database settings, snapshot retention, or topology can alter cost, durability, and failure behavior. A lower latency result is not sufficient if the change weakens reclaim, backup, or isolation.

Atlas release evaluation applies correctness and recoverability gates before performance gates. Course 5 taught the same principle for network optimizations; Course 6 extends it to storage.

## Cache can hide or create storage behavior

Page cache, database buffer pools, client caches, and backend caches can make short tests look fast and hide durable-write latency. Conversely, cold-cache tests may overstate normal read cost. Performance evidence should declare cache state and use a representative duration.

Atlas separates cached reads, uncached reads, buffered writes, and fsync-complete writes. It does not compare them as though they were one workload.


## Tail latency matters for synchronous commits

A database commit path often waits for the slowest required durable operation. Median storage latency can remain acceptable while p99 or p99.9 spikes cause request timeouts and retry storms. Snapshot, rebuild, compaction, or noisy-neighbor work can create those tails.

Service-level indicators use the application’s commit and query populations, then correlate them with backend and node signals. A storage metric alone is not the user experience.


## Health monitoring needs action semantics

CSI volume-health signals can report abnormal conditions when the driver supports them, but an alert needs an owner and action. Does abnormal mean read-only, degraded replication, imminent failure, or transient path loss? Can the application continue? Should a replacement be provisioned?

Atlas maps each health state to readiness, admission, backup, and incident actions. Unknown is not silently treated as healthy.


## Quota should fail before the emergency

ResourceQuota can limit PVC count and requested capacity per namespace or storage class. Backend quotas and cloud limits remain separate. A platform should alert and block growth while enough headroom remains for failover, restore, and emergency expansion. Consuming the last available volume slot for ordinary growth can make recovery impossible.

Atlas reserves recovery headroom in its capacity model and treats it as unavailable for routine admission.

## Worked semantic example

```python
from atlas_data.performance import StorageWorkload

workload = StorageWorkload(
    iops=1200, average_kib=16, p99_latency_ms=8.0, queue_depth=12
)
assert round(workload.throughput_mib_s, 2) == 18.75
assert workload.within_budget(max_p99_ms=10.0, max_queue_depth=16)
```

The example is intentionally small enough to inspect. It establishes one invariant in the dependency-light lane; it does not claim native Kubernetes or storage-system conformance.

## Production-intent API fragment

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: atlas-storage-quota
  namespace: atlas-system
spec:
  hard:
    requests.storage: 500Gi
    persistentvolumeclaims: "20"
    atlas-rwo-durable.storageclass.storage.k8s.io/requests.storage: 300Gi
```

The manifest is a contract candidate. Its effect depends on admission, installed controllers, CSI capabilities, backend behavior, and application compatibility.

## Failure signatures

| Observation | Likely missing guarantee | Decisive evidence |
|---|---|---|
| high latency | queue saturation hidden by low CPU | phase and backend metrics |
| volume full | Pod healthy while writes fail | filesystem and application signals |
| snapshot sprawl | delta pool consumes capacity | retention and backend accounting |

## Atlas capstone increment

Atlas publishes storage SLOs, capacity budgets, failure signatures, quota policy, and before/after evidence for one service-tier mutation.

## Evidence boundary

The module’s Python and filesystem tests can falsify logical invariants and local durability mechanisms. Cluster controller behavior, CSI RPC behavior, snapshot semantics, cloud durability, and operated recovery require the corresponding native evidence lane. Record unavailable evidence as `not-executed`.

## Transition

Module 10 combines data safety with migration, maintenance, release, and the Course 7 desired-state handoff.

## Advanced design review — observe transitions and saturation separately

Provision, attach, stage, publish, expand, snapshot, backup, and restore are control-plane transitions. Read, write, flush, and transaction latency are data-plane behavior. Combining them into one “storage latency” graph makes incidents harder. Build phase-specific indicators and connect them through stable operation identity.

Saturation should be diagnosed at every queue: application, database, filesystem, block layer, network, storage controller, and backend. Increasing application concurrency can improve throughput until one queue saturates, then tail latency and timeouts grow. Retries can amplify the load. Use workload rate, outstanding work, completion rate, errors, and queue depth together.

## Capacity policy should preserve recovery

Ordinary tenant growth must not consume the space, volume quota, snapshot capacity, or API budget required for restore and migration. Reserve headroom and test admission before the emergency. A full backup repository or snapshot delta pool can turn a recoverable source failure into data loss even when PVC dashboards look normal.

## Performance incidents can threaten correctness

Storage saturation does more than make requests slow. Timeouts can trigger retries and duplicate external operations; database heartbeats can miss deadlines; leases can expire; snapshot freezes can exceed safe budgets; backup windows can overlap; applications can fill local queues and exhaust memory. Reliability and performance therefore share one control problem.

Admission control and backpressure should protect the data service before it reaches a state where recovery work cannot make progress. Reserve I/O and capacity for logs, checkpoints, backups, and repair. A workload that consumes every provisioned IOPS token can violate its own RTO by starving recovery.

## Measure the user-visible operation and the storage phases

A database transaction includes lock acquisition, execution, log write, flush, replication, and response. Device latency is only one phase. A lower block latency that does not reduce transaction p99 may not justify migration. Conversely, application latency can reveal a storage bottleneck before backend averages move if tail behavior or one shard is affected.

Build traces or correlated events that connect application operation to filesystem and storage observations without putting raw volume IDs into unbounded metric labels. The goal is an explanation, not a larger dashboard.
## Measure the workload-visible path

Storage performance is produced by a chain:

```text
application request
→ runtime and filesystem
→ kernel page cache and block layer
→ CSI/node path
→ network or device
→ storage controller
→ media and replication
```

A single “disk latency” metric cannot explain this path. Application p99 latency may rise while device latency stays low because the process waits on locks, queue depth, filesystem ownership changes, or throttling. Device latency may rise without user impact because writes are asynchronous and buffered—until a flush causes a tail-latency spike.

The performance model begins with workload shape:

- operation mix;
- request size distribution;
- random versus sequential access;
- read/write ratio;
- synchronization frequency;
- concurrency;
- working-set size;
- cache hit rate;
- growth and compaction pattern;
- recovery and snapshot load.

Without this profile, IOPS and throughput numbers are marketing units rather than service evidence.

### Latency, throughput, IOPS, and queue depth interact

Throughput is approximately operation size multiplied by operations per second. For a fixed device capability, larger operations can achieve high throughput with fewer IOPS; small random operations may exhaust IOPS while using little bandwidth. Queueing can improve device utilization while increasing latency. Tail latency grows sharply as utilization approaches saturation.

A service-level budget should therefore include at least:

```text
p50 and p99 operation latency
sustained IOPS and throughput
maximum queue delay
error and timeout rates
recovery/rebuild impact
capacity headroom
```

Course 5 introduced general queueing and capacity models. Course 6 applies them to storage and adds data-safety constraints: an optimization that disables durable flushes or weakens replication is not acceptable merely because latency improves.

### Observe each control-plane phase

Storage incidents require both data-plane and control-plane signals. Useful populations include:

- pending claims and age;
- provisioning attempts and errors;
- VolumeAttachment age and transitions;
- node stage/publish failures;
- mount duration;
- expansion phase and age;
- snapshot creation and readiness age;
- backup freshness;
- restore duration and validation result;
- per-class capacity and attach-slot headroom;
- application-level commit and read latency;
- fencing rejections and stale-writer attempts.

Events are useful for recent diagnosis but are not a durable telemetry system. Export stable metrics and structured logs with volume, claim, driver, node, class, and tenant identifiers carefully bounded to avoid cardinality explosions or sensitive data exposure.

### Capacity alarms should lead the incident

Waiting for a filesystem to reach 100% is too late. Set thresholds based on growth rate, allocation delay, compaction needs, and restore headroom. A database may need significantly more temporary space for maintenance than its steady-state footprint. Snapshot copy-on-write behavior can consume backend capacity unexpectedly during high churn.

A capacity forecast should answer:

- when the current class or pool reaches the operational threshold;
- how long expansion or migration takes;
- whether quota and provider limits permit the change;
- whether topology contains enough capacity;
- what happens if growth accelerates;
- whether backup and restore destinations have equal or greater capacity.

Alerts should point to an actionable runbook and a remaining decision window, not merely report a red percentage.

### Quotas protect shared platforms

Namespace quotas can limit claim counts and requested storage by class. Backend quotas may limit capacity, snapshots, IOPS, or object count. Quotas prevent one tenant from consuming all resources, but they can also block recovery or scaling if emergency headroom is not reserved.

Separate normal allocation from recovery capacity. A restore during an incident should not fail because the production namespace consumed its entire quota. Break-glass quota changes need time bounds, approval, and cleanup evidence.

### Performance experiments must preserve correctness

A valid storage experiment controls data set, workload, concurrency, cache state, filesystem, storage class, topology, and background activity. It reports environment identity and repeats runs. It also verifies the application result.

Examples of invalid “optimizations” include:

- disabling synchronous commit without changing the durability contract;
- benchmarking warm cache while claiming backend performance;
- comparing different data sizes or zones;
- ignoring timed-out or failed operations;
- measuring only averages;
- running without recovery or snapshot load;
- removing encryption or authorization;
- testing a local directory and claiming CSI or cloud evidence.

The release gate evaluates correctness before speed.

### Diagnosis by earliest divergence

When latency or errors rise, compare planes in order:

1. application operation and commit latency;
2. process CPU, memory, locks, and queueing;
3. filesystem capacity, errors, and mount state;
4. kernel block or network evidence;
5. CSI operation and node-plugin evidence;
6. backend latency, throttling, replication, and capacity;
7. topology, quota, or provider control-plane state.

The earliest divergence is usually more useful than the loudest downstream alert. Restarting Pods may briefly clear queues while preserving the underlying bottleneck.

### Atlas performance dossier

Atlas records a profile for each data class. Transactional state prioritizes durable commit latency and predictable tails. Artifact publication prioritizes streaming throughput, checksum cost, and atomic publication. Backup prioritizes sustained throughput, repository integrity, and completion before the next RPO deadline. Restore prioritizes end-to-end RTO and validation.

The dossier includes the test workload, evidence class, environment, results, variance, correctness oracle, and limits. This makes performance an engineering claim rather than a class name.
