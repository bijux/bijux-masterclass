---
module_id: LSDS-095
program: Large-Scale Data Systems Engineering
level: 2
module_number: 95
title: Storage Throughput and Request Limits
status: complete
last_verified: 2026-09-04
---

# Storage Throughput and Request Limits

## One-Page Review

### Governing question

How should an engineer model and test storage byte, operation, request, metadata, connection, and client limits so a distributed data workload meets throughput and latency objectives without creating small-file amplification, throttling, unsafe retries, or a new network/compute bottleneck?

### Essential definitions

- **throughput** is bytes successfully served per unit time for a declared read/write and logical/physical boundary.
- **IOPS** is storage operations per second under the service's operation-size accounting rules.
- **request rate** is API requests per second, often governed independently from bytes per second.
- **latency** is end-to-end time for one operation; **queue depth** is outstanding operations waiting or executing.
- **goodput** is useful committed payload per unit time after excluding retries, metadata, replicas, and discarded attempts.
- A **scale target** is a documented service envelope, not a universal guarantee for every object size, key pattern, region, or client.
- **throttling** deliberately limits service and may appear as explicit status codes, delayed responses, or quota metrics.
- **small-file amplification** turns a byte workload into many opens, range requests, listings, metadata objects, commits, and downstream tasks.
- **range request** retrieves a byte interval of an object, enabling projection and parallelism when format boundaries permit.
- **multipart transfer** divides a large object into independently transferred parts under a final assembly/commit contract.
- **retry amplification** is extra load caused when slow/throttled/ambiguous operations are repeated.

### Central model, mechanism, or theorem

For useful bytes $D$, object/request count $N$, deadline $T$, mean useful bytes per request $s=D/N$, bandwidth ceiling $B$, and request ceiling $Q$, the simplest service bound is:

$$G\le min(B,Qs),\qquad T\ge max(D/B,N/Q).$$

The real bound also includes client instance bandwidth/CPU, connection pools, metadata/list/commit limits, per-key/partition scaling, disk IOPS and operation-size accounting, replicas/erasure coding, encryption/compression, retries, and downstream processing. With steady arrival rate $\lambda$ and mean request latency $W$, Little's Law gives average in-flight requests $L=\lambda W$ for a stable system; it does not prescribe a safe concurrency ceiling under tail latency or bursts.

Model reads, writes, listings, metadata, deletes, and commits independently. Use a safe envelope below each sustained limit, ramp new access patterns when the service requires it, and make retries exponential, jittered, bounded, idempotent, and charged to the same admission budget.

### Critical invariants

- Byte, request, IOPS, object, metadata, connection, and client/network demand are all computed for matching direction and time windows.
- Logical bytes are reconciled with encoded/compressed, replicated, range-read, retried, and physically billed/transferred bytes.
- Read pruning/range selection preserves complete required records and validates format/page boundaries.
- Multipart or speculative writes publish exactly one complete object/table commit; ambiguous outcomes are reconciled before retry.
- Retry/backoff and adaptive concurrency reduce offered load under throttling instead of multiplying it.
- Naming/key distribution, partitioning, and ramp-up follow current service behavior without becoming correctness dependencies.
- File/object sizing preserves splitability, parallelism, memory bounds, failure isolation, and target downstream layout.
- Capacity planning reserves headroom for compaction, checkpoints, recovery, lifecycle, and control/metadata work.
- Credentials, encryption, checksums, retention, and authorization remain correct when paths, clients, or transfer modes change.
- Benchmarks use isolated test data/resources where destructive or write-heavy behavior could affect production.

### Common failures

Common failures include sizing only bytes/s; treating request and IOPS limits as interchangeable; assuming one large sequential benchmark represents tiny random reads; averaging away microbursts; increasing concurrency after throttling; retrying non-idempotent writes blindly; ignoring client instance/network caps; listing the whole namespace per task; creating one object per tiny result; using sequential hot keys against a range-partitioned index; range-reading compressed data without valid boundaries; choosing files so large that tasks and retries serialize; choosing files so small that metadata dominates; counting cached reads as storage throughput; relying on burst credits for sustained jobs; and scaling storage without retesting network, CPU, memory, catalog, and consumers.

### Compact example

Ten TiB stored as 8-MiB objects produces 1,310,720 requests for one full read. Finishing in one hour requires about 364.1 requests/s and 2.844 GiB/s. A 1,000-request/s ceiling at 8 MiB implies 7.812 GiB/s, while the independent bandwidth ceiling is 6 GiB/s, so bandwidth binds at 6 GiB/s. An 80% envelope is 4.8 GiB/s, still above demand. At 50-ms mean latency, Little's Law predicts about 18.2 requests in flight at the required average rate; tail/burst evidence determines practical concurrency.

### Connections

[LSDS-072](072-manifest-and-metadata-trees.md) supplies metadata access, [LSDS-076](076-compaction-planning.md) supplies file consolidation, [LSDS-080](080-operating-table-metadata-under-millions-of-files.md) supplies namespace scale, [LSDS-091](091-partition-count-and-task-granularity.md) supplies work sizing, [LSDS-093](093-serialization-and-compression-trade-offs.md) supplies byte transformation, and [LSDS-094](094-network-saturation.md) supplies path capacity.

## Governing Question

Storage systems expose several service centers. Block devices have IOPS, throughput, latency, queue, and operation-size behavior. Distributed filesystems separate metadata coordination from data paths. Object stores expose per-request and bandwidth behavior, range/multipart APIs, naming indexes, quotas, and throttling. Table formats add manifests, snapshots, catalog commits, delete files, and compaction.

The governing question is how to translate a dataflow plan into demand on each center, find the first binding constraint with evidence, and choose a change that preserves correctness and total lifecycle performance.

## Why This Matters

A workload may read few bytes and still fail because it opens millions of objects. Another may issue few requests and saturate bandwidth. Large I/O can reach throughput before provisioned IOPS; tiny random I/O can reach IOPS far below byte capacity. Metadata or listing can serialize startup while data servers sit idle.

Failures feed back. Throttling raises latency; fixed-concurrency clients accumulate work; timeouts trigger retries; retries consume more requests and bytes; speculative tasks duplicate reads or writes. Small outputs make the next job slower and catalog operations larger. Storage performance is therefore an end-to-end workload-shape and control problem.

## Prerequisites and Retrieval

Review metadata trees in [LSDS-072](072-manifest-and-metadata-trees.md), compaction in [LSDS-076](076-compaction-planning.md), table metadata at scale in [LSDS-080](080-operating-table-metadata-under-millions-of-files.md), transactional sinks in [LSDS-087](087-transactional-sinks.md), partition granularity in [LSDS-091](091-partition-count-and-task-granularity.md), serialization/compression in [LSDS-093](093-serialization-and-compression-trade-offs.md), and network saturation in [LSDS-094](094-network-saturation.md).

You should understand throughput, IOPS, request rate, latency, queueing, Little's Law, block/object storage, range/multipart operations, checksums, idempotency, exponential backoff, file formats, partition pruning, manifests/catalogs, compression, replication, and percentiles.

For diagnosis retain job/stage/operator/partition/attempt IDs; bucket/container/filesystem/volume/object/key/range; operation type/status/retry; logical/encoded/compressed/physical/billed bytes; request/IOPS/throughput rate; object and I/O size distributions; latency and queue depth; connection/client concurrency; throttles/errors/timeouts; cache status; metadata/list/commit calls; disk/service/client/network utilization and caps; burst credits; replicas; compaction/lifecycle/recovery traffic; versions/configuration; and load cohort.

## Learning Objectives

After this module, you should be able to:

1. derive byte, request, IOPS, metadata, and concurrency demand from a workload;
2. identify the minimum of storage, client, network, and downstream service ceilings;
3. use operation-size accounting to explain IOPS-versus-throughput regimes;
4. apply Little's Law without mistaking average in-flight work for a safe concurrency target;
5. design object/file/page/range sizes for access, memory, parallelism, and metadata;
6. implement ramp-up, adaptive concurrency, throttling response, and bounded idempotent retries;
7. preserve read coverage and exactly-once publication across range/multipart/speculative operations;
8. diagnose data-path, metadata-path, key-distribution, and client-side bottlenecks;
9. benchmark representative reads, writes, listings, commits, and recovery safely; and
10. include downstream scans, compaction, retention, and cost in the decision.

## Core Exposition

### Enumerate storage service centers

Draw client CPU/memory/connection pools, instance storage/network adapter, local/remote device, filesystem metadata, object API/index partition, bucket/account/project quota, catalog, encryption/key service, and downstream decompression/parser. Annotate direction, request type, bytes, and concurrency.

One flat throughput curve can originate anywhere in this chain. Observe both sides before buying storage capacity.

### Derive byte and request demand

For each phase, calculate useful bytes and object/operation counts over the deadline. Include headers, range overfetch, compression, replication, multipart parts, checksums, retries, speculative attempts, listings, metadata, and commits as separate rows.

Use distributions. Mean object size $D/N$ is helpful for a bound but hides tiny manifests and huge data objects. p99 latency and largest I/O determine buffers/timeouts; request-rate bursts determine throttling.

### Separate IOPS and throughput

An operation may be counted in fixed-size units by the provider/device. A 1-MiB application I/O can consume several provisioned operations; adjacent small operations may be merged. With small I/O, the IOPS ceiling can bind. With large sequential I/O, byte throughput can bind first.

Measure application requests, operating-system/device operations, sizes, queue, and latency. Do not infer one layer's IOPS from another without the accounting rule.

### Apply Little's Law carefully

For a stable cohort, average in-flight work equals completed/arrival rate times mean latency. This helps estimate concurrency needed to sustain a target rate. It assumes stable averages and says nothing about tail latency, burst absorption, dependency caps, memory, fairness, or retry behavior.

Sweep concurrency while tracking goodput, p50/p95/p99 latency, errors/throttling, queues, CPU, network, and memory. Stop increasing when marginal goodput disappears or tails/errors violate the envelope.

### Diagnose data versus metadata paths

Distributed filesystems may serve namespace/block-location operations through a coordinator while data flows directly between clients and storage nodes. Object/table workloads may list, fetch manifests, authorize, and resolve metadata before reading data ranges.

Low data bandwidth with high metadata latency/request rate suggests a different remedy from a saturated data path. Cache governed metadata, prune manifests, batch listings, avoid one listing per task, and compact file/manifest counts while preserving snapshot isolation.

### Design object and file sizes

Larger objects/files amortize open, request, metadata, checksum, and commit overhead and often improve sequential throughput. They reduce task parallelism, enlarge retries and buffers, and can force range reads or scan irrelevant data. Smaller objects improve fine-grained parallelism/failure isolation but amplify requests, listings, catalogs, and downstream tasks.

Choose a range tied to encoded size distribution, format row groups/pages, table partitions, expected projections, worker memory, task duration, object range behavior, writer concurrency, and compaction cost. Compute tasks need not map one-to-one to final files.

### Use range reads correctly

Range reads can parallelize large objects and retrieve only needed columnar pages/row groups. They require an index/footer and valid independently decodable boundaries. Compression/encryption framing may force overfetch or preceding state.

Validate complete record coverage, overlaps, boundaries, checksums, short reads, changed objects/version IDs, and retry. Excessively small ranges trade saved bytes for request overhead.

### Use multipart writes safely

Multipart upload can fill bandwidth, retry parts, and avoid one huge buffer. Record upload/session identity, part numbers/checksums, object version/preconditions, expiration, and abort/cleanup ownership. Completion is a publication boundary.

On ambiguous completion, query/reconcile state before repeating a non-idempotent action. Speculative writers use attempt-private destinations and one-winner table/object commit.

### Ramp and distribute access

Some object services scale internal key/index partitions with observed request rate. Sudden traffic on a cold bucket or new key range may temporarily throttle; sequential key patterns may concentrate access depending on current service guidance.

Follow the provider's current ramp and naming recommendations, but do not encode semantic correctness in an assumed partitioner. Monitor latency/errors and pause or reduce ramp when the service signals pressure.

### Treat throttling as control feedback

Explicit 429/503/slowdown responses, quota metrics, or increased latency indicate that clients should reduce admission. Use exponential backoff with jitter, maximum elapsed time/attempts, and idempotency. Global and per-resource concurrency limits prevent thousands of tasks from each retrying independently.

Retry budgets include original and repeated operations. Circuit breaking or scheduler backpressure may be safer than continuing a job that cannot meet its deadline.

### Account for client and network ceilings

Storage volume/account capability is useless if the worker instance, NIC, encrypted transport, SDK connection pool, DNS, memory copy, checksum, compression, or parser binds first. Attached block storage may share a separate instance bandwidth/IOPS ceiling.

Correlate client CPU and queues, instance network/storage metrics, service-side metrics, and downstream consumption. Add clients only if partitioning and aggregate service capacity allow useful scaling.

### Plan cache effects

Operating-system, engine, CDN, and local-disk caches can make a repeated read benchmark avoid the target storage. Decide whether the production objective is cold, warm, or mixed. Label cache hits and bytes served at each layer.

Cache can reduce remote requests but costs memory/storage and invalidation. Version immutable objects or use validation/preconditions so reuse cannot return stale data.

### Protect shared and control workloads

Compaction, backfills, checkpoints, lifecycle deletes, repair, replication, catalog maintenance, and interactive reads share storage. Reserve quotas/capacity, use separate buckets/accounts/volumes when justified, and schedule/rate-limit background work.

Priority is meaningful only when enforced at a layer owning the constrained resource. A client-side label cannot protect a saturated account limit by itself.

### Design for failure and recovery

Worker loss repeats ranges/parts/tasks; storage-node or zone loss changes paths and capacity; recovery reads checkpoints and recomputed inputs while normal work continues. Plan the degraded minimum and catch-up rate.

Test partial reads/writes, throttling, timeout after commit, corrupt checksums, stale versions, unavailable metadata, exhausted local spill, and cleanup. Ensure retries preserve one logical effect.

### Benchmark safely and representatively

Use dedicated disposable objects/volumes for destructive or saturation tests. Pin object/I/O sizes, key distribution, read/write mix, range/sequential/random access, compression, cache, concurrency, client/instance type, region/zone, SDK/version, and neighboring load.

Measure useful and physical bytes, requests/IOPS, latency distributions, queue, throttles, CPU/memory/network, metadata, correctness, and cost. Run long enough to expose sustained rather than burst-credit performance.

### Observe continuously

Dashboard logical/encoded/physical bytes; request/IOPS/throughput rates; object/I/O/range/part sizes; queue/concurrency; latency; errors/throttles/timeouts/retries; cache hits; listings/manifests/commits; client CPU/memory/network; volume/service/account quotas and credits; compaction/recovery traffic; and billed operations/bytes.

Segment by job/stage/operator/partition/attempt, tenant, account/bucket/container/filesystem/volume, object prefix/key/range, operation/status, client/instance/zone/region, format/codec, object-size cohort, cold/warm cache, normal/recovery/background workload, percentile, and time window.

## Definitions and Notation

Let:

- $D$ be required useful bytes and $N$ required storage operations/requests;
- $T$ be the completion deadline;
- $s=D/N$ be mean useful bytes per request for one simplified cohort;
- $B$ be the applicable bandwidth ceiling and $Q$ the request-rate ceiling;
- $I$ be IOPS ceiling under the service's operation-size accounting;
- $G$ be useful goodput, bounded by $min(B,Qs)$ before other limits;
- $\lambda$ be stable request arrival/completion rate and $W$ mean latency;
- $L=\lambda W$ be average in-flight requests under Little's Law;
- $a_b,a_r$ be physical-byte and request amplification factors; and
- $\rho_b,\rho_q,\rho_i$ be bandwidth, request, and IOPS utilization against matching envelopes.

$D/B$ and $N/Q$ are lower bounds under ideal independent ceilings. A mixed-size/request workload requires per-class accounting. Rates need direction, scope, and windows; provider limits and defaults are versioned operational inputs, not constants of the model.

## Mechanisms, Invariants, or Proof Structure

### Multi-ceiling bound

Compute demand and capacity for bytes, requests, accounted operations, metadata, clients, networks, and downstream service. The first saturated center bounds end-to-end goodput. Raising a nonbinding ceiling cannot improve the bound.

### Read-coverage argument

An index/manifest maps every required logical record to object ranges. Range reads use stable object versions, cover all required bytes exactly or tolerate explicit overlap, validate boundaries/checksums, and only emit fully decoded valid records.

### Write-publication argument

Every part belongs to an attempt/session and is checksummed. Final assembly/table commit validates required parts and preconditions, then publishes one winner atomically. Ambiguous responses are reconciled; losing/incomplete sessions expire or are safely aborted.

### Stable-control argument

When throttling or rising tail latency indicates overload, adaptive admission and bounded jittered retries reduce offered load below service long enough to drain queues. Independent unbounded task retries violate this condition.

### Adversarial verification

Test empty/tiny/huge objects, mixed/random/sequential I/O, one hot/new/sequential key range, sudden ramp, cold/warm cache, metadata/list storms, range boundary errors, multipart ambiguity, throttling/timeouts, corrupt data, retry/speculation, burst-credit exhaustion, client/network caps, volume/node/zone loss, recovery plus foreground traffic, and destructive-test isolation.

## Alternatives and Trade-Offs

| Lever | Strength | Cost or limitation |
|---|---|---|
| Larger files/objects | Fewer requests and metadata entries | Larger retries, buffers, and less task granularity |
| Smaller files/objects | Parallelism and failure isolation | Request/list/catalog/task amplification |
| Larger I/O/ranges | Better throughput and request amortization | Overfetch, memory, latency, IOPS accounting |
| Higher concurrency | Hides latency and fills capacity | Queues, throttling, memory, unfairness, retries |
| More clients/volumes/accounts | Raises some aggregate ceilings | Cost, sharding, governance, and shared caps |
| Compression/projection | Reduces storage/network bytes | CPU, memory, and framing constraints |
| Caching | Avoids repeated remote service | Capacity, staleness, invalidation, cold misses |
| Compaction | Reduces small-file/metadata load | Rewrite I/O, temporary capacity, snapshot safety |
| Range/multipart operations | Parallel selective/retryable transfer | More requests, session state, boundary complexity |
| Higher provisioned capacity | Predictable headroom | Cost and unchanged client/downstream limits |

## Failure Modes and Misconceptions

1. **Bytes per second is the only ceiling.** Requests, IOPS, metadata, and clients can bind first.
2. **Requests equal device operations.** Merging, splitting, replication, and accounting units differ.
3. **More concurrency always improves throughput.** It eventually adds queues, tails, and throttling.
4. **Retries restore capacity.** Unbounded retries amplify overload.
5. **A large sequential test represents analytics.** Small random/range/metadata access behaves differently.
6. **One mean object size is sufficient.** Mixed manifests, deletes, and data files need separate cohorts.
7. **Range reads are arbitrary byte slices.** Format, compression, encryption, and record boundaries constrain them.
8. **Multipart completion is obviously failed or successful.** Timeout can make publication ambiguous.
9. **Small files only waste storage.** They amplify opens, requests, metadata, tasks, and commits.
10. **Large files are always efficient.** Parallelism, overfetch, buffers, and retry scope can regress.
11. **Warm-cache throughput is storage throughput.** The target service may not be exercised.
12. **Burst performance is sustained capacity.** Long jobs can exhaust credits or ramp behavior.
13. **Service limits imply achieved performance.** Client, network, key distribution, and workload shape matter.
14. **A quota increase solves the job.** The next service center may already be smaller.
15. **No throttle errors means healthy storage.** Queues and latency can violate objectives first.

## Worked Examples

### Example 1

Ten TiB divided into 8-MiB objects yields 1,310,720 object reads for a complete scan.

### Example 2

That scan in one hour needs about 364.1 requests/s and 2.844 GiB/s useful goodput.

### Example 3

A 1,000-request/s ceiling at 8 MiB implies 7.812 GiB/s, so an independent 6-GiB/s bandwidth cap binds first.

### Example 4

At 50-ms mean latency and 364.1 requests/s, Little's Law gives 18.2 average requests in flight, not a guaranteed safe maximum.

### Example 5

One million 64-KiB files contain only about 61 GiB but require one million opens plus listings/metadata and tasks unless packed.

### Example 6

A 1-MiB application I/O may consume four 256-KiB accounted device operations, reaching IOPS before request count suggests.

### Example 7

A worker reports low storage throughput because its instance storage/network cap binds below the aggregate capacity of attached volumes.

### Example 8

A timed-out multipart completion actually succeeded; reconciliation by object version/checksum prevents a duplicate publication.

### Example 9

Doubling concurrency after 503/slowdown responses raises request rate and tail latency while useful goodput falls.

### Example 10

The executable fixture compares request-derived, bandwidth, safe-envelope, and latency-concurrency estimates.

<!-- bijux-verify: {"id":"storage-limit-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"dataset_tib=10.0\nobject_mib=8.0\nobjects=1310720\nrequired_request_s=364.1\nrequired_gib_s=2.844\nrequest_limited_gib_s=7.812\nbandwidth_limit_gib_s=6.000\neffective_limit_gib_s=6.000\nsafe_limit_gib_s=4.800\nsafe_envelope_fits=true\nconcurrency_at_50ms=18.2\n","stderr":""}} -->
```python
dataset_tib = 10.0
object_mib = 8.0
deadline_seconds = 3600.0
request_limit_s = 1000.0
bandwidth_limit_gib_s = 6.0
safe_fraction = 0.80
mean_latency_seconds = 0.050

dataset_bytes = dataset_tib * 1024**4
object_bytes = object_mib * 1024**2
objects = int(dataset_bytes / object_bytes)
required_request_s = objects / deadline_seconds
required_gib_s = dataset_bytes / deadline_seconds / 1024**3
request_limited_gib_s = request_limit_s * object_bytes / 1024**3
effective_limit_gib_s = min(bandwidth_limit_gib_s, request_limited_gib_s)
safe_limit_gib_s = safe_fraction * effective_limit_gib_s
concurrency = required_request_s * mean_latency_seconds

print(f"dataset_tib={dataset_tib:.1f}")
print(f"object_mib={object_mib:.1f}")
print(f"objects={objects}")
print(f"required_request_s={required_request_s:.1f}")
print(f"required_gib_s={required_gib_s:.3f}")
print(f"request_limited_gib_s={request_limited_gib_s:.3f}")
print(f"bandwidth_limit_gib_s={bandwidth_limit_gib_s:.3f}")
print(f"effective_limit_gib_s={effective_limit_gib_s:.3f}")
print(f"safe_limit_gib_s={safe_limit_gib_s:.3f}")
print(f"safe_envelope_fits={str(required_gib_s <= safe_limit_gib_s).lower()}")
print(f"concurrency_at_50ms={concurrency:.1f}")
```

## Cross-Program Connections

- **Operating systems:** block queues, I/O schedulers, page cache, filesystems, direct I/O, device statistics, and failure define local behavior.
- **Queueing:** Little's Law, utilization, burstiness, tail latency, and stable feedback govern concurrency.
- **Distributed systems:** replication, erasure coding, metadata coordinators, retries, idempotency, quorum, and recovery amplify operations.
- **Data formats:** pages, row groups, compression/encryption frames, footers, and checksums determine valid selective ranges.
- **Table systems:** manifests, snapshots, partition pruning, file sizing, commits, compaction, and lifecycle determine request shape.
- **Networking:** instance bandwidth, connections, DNS, TLS, cross-zone paths, and endpoint caps can bound storage access.
- **Security:** credentials, authorization, encryption, object versions, retention, and destructive-test isolation constrain tuning.
- **Economics:** operation classes, transferred/stored bytes, retrieval tiers, compaction, cache, and worker wait time determine cost.

## References

1. Amazon S3, [Performance Guidelines](https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance-guidelines.html). Current. Covers measurement, horizontal connections, ranges, retries, locality, and 503 monitoring.
2. Amazon S3, [Performance Design Patterns](https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance-design-patterns.html). Current. Covers scaling to request rates, slowdown responses, timeouts, retries, ranges, and caching.
3. Google Cloud Storage, [Request Rate and Access Distribution Guidelines](https://cloud.google.com/storage/docs/request-rate). Current. Documents request ramp-up, key distribution, latency/errors, and backoff guidance.
4. Google Cloud Storage, [Quotas and Limits](https://cloud.google.com/storage/quotas). Current. Documents operation, bandwidth, object, and resource quotas/limits.
5. Google Cloud Storage, [Bandwidth Usage Monitoring](https://cloud.google.com/storage/docs/bandwidth-usage). Current. Documents regional bucket bandwidth measurement and quota handling.
6. Microsoft Azure Storage, [Scalability and Performance Targets](https://learn.microsoft.com/en-us/azure/storage/common/scalability-targets-standard-account). Current. Documents account request/ingress/egress targets and throttling behavior.
7. Amazon EBS, [I/O Characteristics and Monitoring](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-io-characteristics.html). Current. Defines IOPS, operation sizes, throughput, queue depth, latency, and microburst evidence.
8. Amazon EC2, [EBS-Optimized Performance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-optimization-performance.html). Current. Documents the minimum of attached-volume and instance storage ceilings.
9. Apache Hadoop, [HDFS Architecture](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html). Current. Defines NameNode metadata and direct client-DataNode data paths, blocks, and replication.
10. Apache Hadoop, [NameNode Fine-Grained Locking](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/NamenodeFGL.html). Current. Describes namespace metadata bottlenecks and operation classes.
11. Apache Iceberg, [Spark Writes](https://iceberg.apache.org/docs/latest/spark-writes/). Current. Documents task, partition, compression, distribution, and target-file-size interactions.
12. Apache Iceberg, [Structured Streaming Maintenance](https://iceberg.apache.org/docs/latest/spark-structured-streaming/). Current. Documents small-file, manifest, snapshot, and compaction implications.
13. Apache Parquet, [Configurations](https://parquet.apache.org/docs/file-format/configurations/). Current. Documents row-group/page sizing for memory, latency, I/O, and resilience trade-offs.

## Exercises

### Exercise 1

Determine whether 20 TiB in four hours fits a 2-GiB/s bandwidth envelope and a 500-request/s limit when mean useful object size is 2 MiB.

### Exercise 2

Diagnose a scan with low byte throughput, two million 32-KiB files, high open/list latency, idle network, and a busy metadata coordinator.

### Exercise 3

Design adaptive request concurrency and retry control for a service returning slowdown errors during a sudden backfill.

### Exercise 4

Design a safe multipart write protocol that tolerates worker loss and an ambiguous final-completion response.

### Exercise 5

Design a benchmark matrix separating cache, client/instance, request, IOPS, throughput, metadata, and downstream parse limits.

## Answers to the Exercises

### Answer 1

Twenty TiB over 14,400 seconds requires about 1.422 GiB/s. At 2 MiB per request it needs $20\cdot2^{40}/(2\cdot2^{20})/14400\approx728.2$ requests/s, exceeding the 500-request/s limit. The request-derived byte ceiling is $500\cdot2$ MiB/s = 0.977 GiB/s, so requests bind before the 2-GiB/s byte envelope. Use larger valid ranges/objects, more applicable request capacity/shards, or a longer deadline while testing metadata, client, and downstream limits.

### Answer 2

This is a metadata/request/small-file regime, not a data-bandwidth shortage. Correlate file opens/listings/block-location calls, coordinator locks/CPU/heap/queues, task scheduling, and cache state. Compact files and manifests under snapshot safety, batch/cache metadata reads, prune before listing, and avoid one listing per task. Retest file-size balance against task parallelism, retry scope, writer output, and downstream scans; adding data nodes or bandwidth alone will not relieve the coordinator path.

### Answer 3

Apply global and per-bucket/key-range token limits shared across tasks. On sustained latency/throttle signals, multiplicatively reduce admission; recover gradually with hysteresis. Retry only idempotent/reconciled operations using exponential backoff plus jitter, maximum attempts/elapsed time, and a retry budget that includes originals. Pause the backfill before interactive/control traffic loses its reserve. Follow current service ramp guidance and record request/byte goodput, latency, throttle/error rate, queue, and key distribution.

### Answer 4

Create an attempt-private upload session, assign deterministic part numbers/ranges, checksum every part, persist session/part evidence, and upload under bounded concurrency. A coordinator validates all parts and an object-version/precondition before one-winner completion. If completion times out, query object/session state and compare version/size/checksum before retrying. Fence losing attempts, abort incomplete sessions only after liveness/ownership checks, and expire orphans by governed age. Publish the table/catalog reference only after the object is complete and verified.

### Answer 5

Use disposable resources and pin data, sizes, access pattern, client, region, SDK, compression, concurrency, and neighbors. Run cold and warm cache; large sequential and tiny random/range I/O; low/high request rates; metadata/list-only; one/many clients; and parse-disabled versus full consumer paths. Collect logical/physical bytes, requests/device IOPS, object/I/O size, latency/queue, throttle/errors, client CPU/memory/network, instance/service quotas/credits, coordinator metrics, and output correctness. Sweep long enough to exhaust burst effects and inject controlled latency/failure without risking production data.
