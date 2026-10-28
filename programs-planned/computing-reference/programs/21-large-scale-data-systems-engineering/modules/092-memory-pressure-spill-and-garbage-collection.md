---
module_id: LSDS-092
program: Large-Scale Data Systems Engineering
level: 2
module_number: 92
title: Memory Pressure, Spill, and Garbage Collection
status: complete
last_verified: 2026-09-04
---

# Memory Pressure, Spill, and Garbage Collection

## One-Page Review

### Governing question

How should an engineer account for every worker memory domain, distinguish healthy pressure and bounded spill from leaks or impending failure, and reduce allocation and working-set demand before changing garbage-collector or container limits?

### Essential definitions

- A **memory domain** is a separately allocated or governed pool such as JVM heap, managed off-heap, direct/network buffers, native libraries, child-process memory, or page cache.
- **live memory** remains reachable or semantically required; **garbage** can be reclaimed; **retained memory** remains reachable longer than intended.
- **allocation rate** is newly allocated bytes per unit time; **promotion rate** is bytes surviving into a longer-lived generation.
- **headroom** is the process/container limit minus all concurrently resident domains and safety margin.
- **spill** externalizes intermediate state to bounded local or remote storage so an operator can continue with less resident memory.
- **reclaim** frees or evicts memory; it includes GC, cache eviction, allocator release, and kernel page reclamation.
- **GC pause** stops or constrains application progress while the collector performs work; concurrent GC still consumes CPU and memory bandwidth.
- **RSS** is resident process memory observed by the operating system; it is not identical to heap usage or allocator-accounted live bytes.
- **OOM** may mean heap exhaustion, direct/native allocation failure, allocator-budget rejection, kernel/container kill, or local-disk exhaustion after spill.
- **thrashing** is a positive feedback loop in which GC, spill, reclaim, retries, and rereads consume capacity faster than useful work completes.

### Central model, mechanism, or theorem

For container/process limit $L$, require at every relevant instant:

$$H+O+N+P+C+K+\epsilon\le L,$$

where $H$ is heap, $O$ engine-managed off-heap, $N$ other native/direct memory, $P$ child processes, $C$ charged cache or memory-backed storage, $K$ runtime overhead, and $\epsilon$ safety headroom. Separately, an operator with incoming working set $W$ and usable execution budget $M$ spills approximately $S=max(0,W-M)$ before write/read amplification, but only if it can partition, serialize, merge, and publish intermediate runs safely.

GC can reclaim garbage inside managed heap; it cannot reclaim live state, leaked native buffers, another process, or required cache. Spill can bound some operator state; it cannot repair an unspillable object, insufficient disk, a leak, or a container ledger whose non-heap domains already exhaust $L$. Correct tuning first identifies the growing domain and lifetime, then reduces demand, bounds concurrency, or provisions the corresponding resource.

### Critical invariants

- All resident domains, child processes, memory-backed volumes, and allocator reservations are included in the same limit ledger without double counting.
- Peak and high-quantile concurrency, not averages or post-GC snapshots, fit beneath the enforced limit with margin.
- Every allocation has an owner, lifetime, limit, release path, and observable accounting signal.
- Spill preserves record coverage, key/partition semantics, comparator/serialization compatibility, and deterministic merge results required by the operator.
- Spill storage has reserved capacity, bounded fan-out, checksums, cleanup ownership, and failure behavior.
- Backpressure or admission control acts before irreversible OOM or disk-full thresholds.
- GC objectives specify pause, throughput, and footprint trade-offs for a pinned JDK, collector, heap, workload, and container cohort.
- Retries do not multiply retained cache, orphan spill files, or simultaneous memory-heavy attempts without a bound.
- Heap dumps, GC logs, native-memory evidence, and spill data are access-controlled because they may contain production data.
- A tuning change is accepted only with end-to-end latency, throughput, CPU, I/O, recovery, and cost evidence.

### Common failures

Common failures include equating heap with process RSS; sizing heap equal to the container limit; treating allocator estimates as physical residence; calling allocator-retained pages a leak without evidence; increasing heap while starving native/network headroom; tuning GC before reducing object churn; reading cumulative GC or spill counters as instantaneous rates; considering any spill a failure or any successful spill healthy; placing spill on a tiny shared root disk; letting speculative attempts double peak state; caching inputs that evict execution memory; retrying deterministic OOM indefinitely; scaling out while a hot key remains unspillable; collecting heap dumps without security controls; and declaring success because OOM disappeared while runtime and cost exploded.

### Compact example

A worker has a 16-GiB limit. Its planned peak ledger is 9 GiB heap, 2 GiB managed off-heap, 1 GiB network/direct buffers, 1.5 GiB Python/native processes, 0.5 GiB charged cache, and 0.5 GiB runtime overhead: 14.5 GiB, leaving 1.5 GiB headroom. A sort sees a 12-GiB working set with a 7-GiB execution budget, so the lower-bound spill is 5 GiB before merge/write amplification. Raising heap to 12 GiB would exceed the process ledger even though it appears to help the JVM.

### Connections

[LSDS-057](057-memory-cpu-and-i-o-isolation.md) supplies resource isolation, [LSDS-060](060-diagnosing-scheduler-delay-and-resource-fragmentation.md) supplies cohort diagnosis, [LSDS-064](064-distributed-hash-and-merge-joins.md) and [LSDS-065](065-partial-and-final-aggregation.md) supply memory-intensive operators, [LSDS-066](066-vectorized-execution-at-cluster-scale.md) supplies off-heap vectors, and [LSDS-091](091-partition-count-and-task-granularity.md) supplies per-task working-set control.

## Governing Question

Large-scale data workers combine several allocators and control loops. A JVM collector manages heap objects. An execution engine may reserve managed native pages for sort, hash, shuffle, or state. Network libraries own direct buffers. Native codecs and columnar libraries allocate outside the heap. Python or other language workers are separate processes. The kernel accounts resident anonymous pages, file-backed cache, and memory-backed volumes against a cgroup or host budget.

A single graph can therefore exhibit low heap occupancy and still be OOM-killed, or high RSS and no actual leak. It can spill successfully yet become slower with every retry because spill files, rereads, and disk contention accumulate. The governing question is how to establish a complete resource ledger, relate pressure signals to task/operator lifetimes, preserve correctness during spill, and choose the narrowest effective control.

## Why This Matters

Memory failures are discontinuous. An operator may appear healthy until one partition crosses a hash-table or sort threshold; the worker then spills, pauses, loses locality, fills disk, times out, and gets retried elsewhere. Speculation can reproduce the same peak twice. A kernel OOM kill may leave no language-level exception, while a heap OOM may leave the process alive long enough to create evidence.

Overcorrection is expensive. Oversized heaps can increase footprint and change pause behavior. Excessive spill adds serialization, compression, writes, reads, merge passes, and remote shuffle traffic. Lower concurrency can protect memory but waste CPU. More workers can reduce per-worker state but increase shuffle and coordination. Correct diagnosis keeps those mechanisms separate and evaluates the whole job rather than one reassuring metric.

## Prerequisites and Retrieval

Review isolation in [LSDS-057](057-memory-cpu-and-i-o-isolation.md), scheduler evidence in [LSDS-060](060-diagnosing-scheduler-delay-and-resource-fragmentation.md), hash/merge joins in [LSDS-064](064-distributed-hash-and-merge-joins.md), partial aggregation in [LSDS-065](065-partial-and-final-aggregation.md), vectorized execution in [LSDS-066](066-vectorized-execution-at-cluster-scale.md), task recovery in [LSDS-081](081-task-level-failure-recovery.md), worker loss in [LSDS-082](082-worker-and-executor-loss.md), and partition granularity in [LSDS-091](091-partition-count-and-task-granularity.md).

You should understand virtual and resident memory, heap and native allocation, reachability, generational/concurrent collection, page cache, container/cgroup limits, serialization, external sort, hash aggregation/join, shuffle, backpressure, retries, percentiles, and time-series correlation.

For diagnosis retain worker/container/node IDs; job/stage/operator/partition/attempt IDs; heap pool used/committed/max; allocation/promotion/reclamation rates; pause events and causes; managed/off-heap/direct/native/child-process bytes; RSS and cgroup current/peak/events; cache and memory-backed-volume charges; task concurrency; input/state/skew; spill bytes/files/runs/merge passes; disk capacity/latency/throughput; eviction, pause, kill, retry, and recovery events; configuration; JDK/collector/runtime/library versions; and deployment cohort.

## Learning Objectives

After this module, you should be able to:

1. construct a non-overlapping process/container memory ledger;
2. distinguish live demand, garbage, retention, fragmentation, allocator caching, and leaks;
3. correlate allocation, promotion, GC, RSS, cgroup, spill, disk, and task signals;
4. derive headroom and operator spill requirements under concurrent peaks;
5. explain external sort/hash spill mechanics and their correctness invariants;
6. classify heap OOM, native/direct failure, allocator rejection, and kernel/container kill;
7. reduce memory demand through representation, partitioning, algorithms, caching, and concurrency;
8. evaluate GC choices against explicit pause, throughput, and footprint objectives;
9. design pressure admission, backpressure, retry, and spill-disk controls; and
10. validate changes under skew, failure, cold cache, and resource contention.

## Core Exposition

### Build the whole-process ledger

Begin at the enforced boundary. A container limit can include heap, direct buffers, native libraries, subprocess RSS, thread stacks, code cache, mapped/resident pages, and memory-backed volumes. Engine dashboards may report only their managed pool. Add domains only when their meanings do not overlap; RSS already includes many resident process components, so it is a reconciliation measure rather than a term to add beside them.

Record configured ceilings, current values, high-water marks, and ownership. Reconcile bottom-up allocator/runtime metrics with top-down RSS and cgroup metrics. A persistent unexplained residual is a diagnostic clue, not automatically a leak.

### Separate capacity from lifetime

The same peak can mean three different problems: a legitimate live working set larger than capacity, garbage accumulating faster than collection, or objects/buffers retained beyond their intended lifetime. Sample before, during, and after operator completion and full/concurrent collection. A true leak shows retained ownership growing across comparable completed-work cycles.

Allocator caches and fragmentation may keep RSS high after logical release. That can still breach a container limit, but its remedy differs from a reachable-object leak. Compare allocator active/allocated/resident figures where available and test whether pages are reused in the next cycle.

### Model concurrency explicitly

Per-task memory multiplied by concurrent tasks is only the start. Add shared cache, broadcast data, shuffle receive buffers, state backend, runtime overhead, and overlap between producer/consumer pipelines. Retries, speculation, checkpoint snapshots, and asynchronous writes can increase simultaneous copies.

For task classes $j$, use $\sum_j c_j m_j$ with concurrency $c_j$ and high-quantile task peak $m_j$, then add shared domains. Scheduler slots are not a memory guarantee unless admission control also accounts for task memory profiles.

### Understand allocation and promotion

High allocation rate can consume CPU even when live-set size is stable. Row-object materialization, boxing, strings, per-record collections, deserialization, and copying create short-lived churn. Objects that survive collections may promote, increasing long-lived occupancy and later collection work.

Reduce unnecessary objects and copies before selecting low-level collector flags. Prefer compact/vectorized/serialized representations when semantics allow, reuse bounded buffers safely, project columns early, and aggregate/filter before widening records. Confirm CPU and latency effects because compact representation may cost encode/decode work.

### Interpret garbage collection correctly

Collectors trade pause time, throughput, CPU, memory overhead, and predictability. A pause target is a goal for a particular collector, not proof that every pause stays below it. Concurrent phases reduce some pauses but compete with application threads for CPU and bandwidth.

Measure pause distributions and causes, concurrent-cycle time, allocation/promotion rate, reclaimed bytes, post-collection occupancy, application throughput, and CPU. High total GC time can be many short collections or a few catastrophic pauses; cumulative counters require interval deltas and worker uptime.

### Treat spill as an algorithm

External sort creates sorted runs that fit memory, writes them, and merges them. A partitioned hash operator can flush partitions or partial aggregates and later merge/reprocess them. Spillability depends on decomposability, serialization, comparison/hash consistency, and bounded records or keys.

Track logical bytes evicted from memory separately from physical bytes written/read. Compression, checksums, metadata, merge fan-in, repeated passes, and retries make them differ. Spill is healthy when it is bounded, provisioned, observable, and cheaper than the alternative; it is pathological when it saturates disk/network or repeats without progress.

### Preserve spill correctness

Each input record must appear in exactly the required run/partition, and merge must preserve the operator's ordering, grouping, aggregation, or join semantics. Version serializers and comparators. Use checksums and attempt-private paths. Publish only the winning attempt and clean abandoned artifacts with ownership and age rules.

Floating-point aggregation order may change after spill; define whether bitwise reproducibility, numerical tolerance, or exact arithmetic is required. Encryption and access controls apply because spill may contain plaintext derived from protected data.

### Provision the spill path

Capacity must cover overlapping attempts, runs, merge outputs, shuffle fetches, logs, and safety reserve—not only estimated logical spill. Isolate spill from the operating-system root and from unrelated tenants where possible. Bound file count and merge fan-in to avoid inode, open-file, and metadata exhaustion.

Monitor free bytes/inodes, queue depth, throughput, latency, errors, throttling, and cleanup backlog. Decide whether disk-full causes controlled task failure, upstream backpressure, alternate volume use, or job abort. Remote spill changes durability and elasticity but adds service limits and network cost.

### Classify the failure surface

A Java heap error implicates heap allocation but not necessarily heap size: a giant record, leak, fragmentation-sensitive request, or excessive concurrency may be the cause. A direct-buffer or native allocator error implicates a different pool. A worker that vanishes with a cgroup OOM event may have no heap exception. A managed allocator can reject a request below the container limit by design.

Correlate timestamps across runtime logs, kernel/cgroup events, orchestrator status, task history, and storage metrics. Preserve the first failure; retry storms obscure it. Classify deterministic input/operator failures separately from transient noisy-neighbor or node faults.

### Apply controls in causal order

First reduce required live bytes: prune columns/rows, pre-aggregate, replace object-heavy structures, bound groups/windows, choose a spillable algorithm, split skew, or broadcast only when the build side fits. Then adjust partitions and task concurrency. Then balance cache, execution, network, state, and native pools. Increase the process/container limit only with node capacity and placement evidence.

Tune or change GC after the heap workload and objective are known. One change at a time is easiest to attribute, but designed multi-factor experiments may be appropriate when interactions are explicit.

### Coordinate backpressure and admission

Pressure controls need ordered thresholds and hysteresis: begin eviction/spill, reduce new work/transfers, pause admission, and finally fail cleanly before an external killer chooses the outcome. Leave time and disk for spill to complete. A threshold based on allocator-managed bytes can miss unmanaged growth; an RSS threshold can overreact to allocator-retained pages.

Use several signals and require sustained conditions where appropriate. Recovery must not immediately admit the same peak and oscillate. Persist enough evidence to explain each transition.

### Diagnose cache competition

Cached datasets, broadcast variables, indexes, state, and execution structures have different recomputation and eviction costs. A unified pool does not eliminate contention; it defines eviction and borrowing rules. Cache only data with measured reuse value, serialized/compact representation, and bounded residency.

Eviction may shift cost to rereads and recomputation. Include downstream I/O, network, and tail latency before deciding that less cache is better. Conversely, a high cache hit rate is not valuable if execution spills and misses its SLO.

### Respect native and child-process memory

Off-heap vectors avoid managed-heap objects and can reduce GC, but their buffers need explicit ownership and deterministic release. Reference-count mistakes can leak or free too early. JNI libraries and native codecs may have independent pools. Language workers can materialize another copy of a batch.

Set hierarchical allocator limits where supported, close resources on success and failure, and observe child processes separately. Never infer native safety from a quiet GC graph.

### Tune with reproducible cohorts

Pin input, skew, code, runtime/JDK/collector, worker shape, partitions, concurrency, cache state, spill device, and neighboring load. Warm-up and steady-state behavior may differ. Repeat runs and compare distributions, not one maximum.

Measure end-to-end time, useful CPU, GC CPU/pause, memory peaks, spill reads/writes, disk/network saturation, retries, output correctness, worker-hours, and resource cost. Test near the intended limit rather than extrapolating from a small dataset.

### Observe continuously

Dashboard heap pools and post-GC live set; allocation/promotion/reclamation rates; pause and concurrent-GC distributions; managed/off-heap/direct/native/child bytes; RSS/cgroup current/peak/events; task concurrency; operator/partition state and skew; spill bytes/files/runs/merge passes; disk capacity/latency; evictions; kills; retries; and cost.

Segment by application/job/stage/operator/partition/attempt, worker/container/node/zone, runtime/JDK/collector/library version, resource profile, input and skew cohort, cache state, deployment, failure mode, percentile, and window. Aggregate ratios can hide one leaking worker or one hot partition.

## Definitions and Notation

Let:

- $L$ be the enforced process/container memory limit;
- $H,O,N,P,C,K$ be heap, engine-managed off-heap, other native/direct, child-process, charged cache, and runtime-overhead memory;
- $\epsilon=L-(H+O+N+P+C+K)$ be instantaneous headroom under a non-overlapping ledger;
- $A$ and $R$ be allocation and reclamation rates;
- $G$ be measured GC elapsed time over observation interval $T$;
- $W$ be operator working set and $M$ its usable in-memory budget;
- $S=max(0,W-M)$ be a lower bound on logical bytes externalized;
- $\omega_w$ and $\omega_r$ be physical spill write/read amplification factors;
- $c_j$ and $m_j$ be concurrency and high-quantile peak for task class $j$; and
- $D_f$ and $D_i$ be free spill bytes and inodes after reserve.

$G/T$ is an elapsed-time ratio, not necessarily lost wall time when collection is concurrent. RSS, heap committed, heap used, allocator-accounted bytes, and cgroup charge are different observations. Spill counters are often cumulative and may count logical memory bytes differently from physical I/O.

## Mechanisms, Invariants, or Proof Structure

### Ledger-safety argument

Enumerate every domain charged to $L$, remove overlap, use synchronized high-quantile/peak observations under worst supported concurrency, and retain positive $\epsilon$. Reconcile against cgroup/process peaks. This establishes capacity for the tested cohort, not all future inputs.

### Lifetime argument

Associate allocations with operator/task/job scopes. After comparable work completes and eligible collection/release occurs, live owned bytes should return to a bounded baseline. Monotonic retained ownership across cycles supports a leak hypothesis; high RSS alone does not.

### Spill-coverage argument

Map every record to an attempt-private spill run or resident partition exactly as required, checksum/version artifacts, and merge all and only those runs under the operator's comparator/aggregation semantics. Commit one winning result, then remove losing/orphaned artifacts.

### Progress argument

Under pressure, spill/eviction/backpressure must reduce memory faster than admitted work adds it, while disk/network service remains below capacity. If $A-R$ stays positive and spill queues grow, the system is delaying failure, not recovering.

### Adversarial verification

Test empty/tiny/huge inputs, incompressible/wide rows, a giant record, hot keys, bursty allocation, high survivor rate, retained cache, native leaks, child-process copies, allocator fragmentation, low cgroup limit, memory-backed volumes, disk/inode exhaustion, slow/corrupt spill, retries/speculation, worker kill, cold cache, and mixed-tenant contention.

## Alternatives and Trade-Offs

| Lever | Strength | Cost or limitation |
|---|---|---|
| Smaller partitions | Lowers per-task working set and retry loss | More tasks, shuffle blocks, files, and scheduler load |
| Lower concurrency | Reduces simultaneous peaks | May underuse CPU and increase latency |
| Compact/vectorized representation | Reduces object count and often GC | Can raise native accounting and conversion complexity |
| Serialized cache | Reduces heap object graph | Adds encode/decode CPU and may still crowd execution |
| External sort/hash spill | Bounds some operator memory | Adds write/read/merge amplification and needs disk |
| Pre-aggregation/filter/projection | Removes demand early | May require semantic or plan changes |
| More worker memory | Preserves concurrency | Raises cost, placement difficulty, and failure blast radius |
| More workers | Reduces state/work per worker | Raises shuffle, coordination, and baseline overhead |
| GC/heap tuning | Can improve measured heap workload | Cannot repair live-set, native, child, or disk problems |
| Remote spill | Adds elastic capacity/durability | Adds network/service limits, latency, and cost |

## Failure Modes and Misconceptions

1. **Heap equals process memory.** Native, child, cache, and runtime domains remain invisible.
2. **Heap should equal the container limit.** The next non-heap allocation can trigger a kill.
3. **High RSS proves a leak.** Allocator retention, fragmentation, and cache can preserve residence.
4. **Low heap proves safety.** Direct/native or another process may exhaust the cgroup.
5. **GC time alone identifies the cause.** Allocation, promotion, live set, causes, pauses, and CPU matter.
6. **A larger heap always reduces pauses.** Collector behavior and the live set determine the trade-off.
7. **Any spill is bad.** Controlled external algorithms deliberately trade memory for I/O.
8. **Successful spill is healthy.** Repeated merge passes may saturate disk and destroy progress.
9. **Logical spill bytes equal disk bytes.** Compression, rereads, retries, and merges change physical I/O.
10. **More workers fix skew.** One unspillable hot key may remain on one worker.
11. **Retry heals OOM.** Deterministic working sets usually reproduce the failure.
12. **Speculation is free.** Duplicate memory and spill peaks can cause the incident.
13. **Off-heap means unmanaged.** It still needs limits, ownership, release, and container headroom.
14. **One post-GC snapshot proves fit.** Concurrent peaks and future partition tails remain untested.
15. **No OOM means success.** Thrashing can meet correctness while missing latency and cost objectives.

## Worked Examples

### Example 1

A 16-GiB worker ledger totals 14.5 GiB across heap, managed off-heap, direct/network, child/native, cache, and runtime overhead, leaving 1.5 GiB headroom.

### Example 2

Heap falls after each collection but the post-GC baseline rises by 200 MiB per completed stage; ownership paths in a heap dump become a leak hypothesis.

### Example 3

Heap remains flat while RSS and direct-buffer accounting rise until a cgroup OOM kill; changing young-generation sizing cannot address the growing pool.

### Example 4

A 12-GiB sort with 7 GiB usable execution memory has at least 5 GiB logical spill before merge and physical-I/O amplification.

### Example 5

Four concurrent 2-GiB task peaks, a 3-GiB cache, and 2 GiB shared/native overhead need 13 GiB before safety margin.

### Example 6

One 9-GiB hot-key group is not made safe by changing 200 ordinary partitions to 2,000; the key needs a decomposable two-level strategy or isolation.

### Example 7

A speculative duplicate starts while the original is merging six spill runs, doubling local capacity and I/O demand unless admission accounts for attempts.

### Example 8

RSS stays high after logical release because an allocator retains reusable pages; a second identical cycle reuses them without growth, weakening the leak hypothesis.

### Example 9

Reducing cached data removes execution spill but doubles remote rereads, so the end-to-end winner depends on latency, network, and worker-hours.

### Example 10

The executable fixture reconciles a worker ledger and estimates minimum logical spill.

<!-- bijux-verify: {"id":"memory-ledger-spill","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"limit_gib=16.0\naccounted_gib=14.5\nheadroom_gib=1.5\nledger_fits=true\nworking_set_gib=12.0\nexecution_budget_gib=7.0\nminimum_spill_gib=5.0\n","stderr":""}} -->
```python
limit_gib = 16.0
domains_gib = {
    "heap": 9.0,
    "managed_off_heap": 2.0,
    "network_direct": 1.0,
    "child_native": 1.5,
    "charged_cache": 0.5,
    "runtime_overhead": 0.5,
}
working_set_gib = 12.0
execution_budget_gib = 7.0
accounted_gib = sum(domains_gib.values())
headroom_gib = limit_gib - accounted_gib
minimum_spill_gib = max(0.0, working_set_gib - execution_budget_gib)

print(f"limit_gib={limit_gib:.1f}")
print(f"accounted_gib={accounted_gib:.1f}")
print(f"headroom_gib={headroom_gib:.1f}")
print(f"ledger_fits={str(headroom_gib >= 0).lower()}")
print(f"working_set_gib={working_set_gib:.1f}")
print(f"execution_budget_gib={execution_budget_gib:.1f}")
print(f"minimum_spill_gib={minimum_spill_gib:.1f}")
```

## Cross-Program Connections

- **Operating systems:** virtual memory, RSS, page cache, cgroups, reclaim, pressure, OOM selection, and filesystem capacity define the physical boundary.
- **Runtime systems:** allocation, reachability, generations, pauses, concurrent collection, JIT/code cache, threads, and native interfaces define lifecycle costs.
- **Data structures:** object layout, hash tables, sort runs, compact vectors, sketches, and decomposable aggregates determine the working set.
- **Query engines:** joins, aggregation, exchange, caching, vectorization, and adaptive plans decide which domains grow.
- **Distributed systems:** retries, speculation, backpressure, one-winner commit, worker loss, and state recovery multiply or constrain peaks.
- **Storage:** spill devices, checksums, encryption, merge fan-in, cleanup, and remote services determine whether external algorithms progress safely.
- **Security:** heap dumps, core files, logs, and spill artifacts may expose records, credentials, or keys and require governed retention.
- **Economics:** memory, worker count, GC CPU, disk I/O, network rereads, retries, and longer runtimes trade against one another.

## References

1. Apache Spark, [Tuning](https://spark.apache.org/docs/latest/tuning.html). Current. Covers execution/storage memory, representation overhead, task working sets, and garbage-collection diagnosis.
2. Apache Spark, [Monitoring and Instrumentation](https://spark.apache.org/docs/latest/monitoring.html). Current. Documents executor heap, RSS, GC, execution-memory, and spill metrics.
3. Apache Spark, [Configuration](https://spark.apache.org/docs/latest/configuration). Current. Documents executor overhead, off-heap, memory fractions, and related limits.
4. Apache Flink, [Set up TaskManager Memory](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/memory/mem_setup_tm/). Current. Defines heap, managed, task/framework off-heap, network, metaspace, and JVM-overhead domains.
5. Apache Flink, [Memory Troubleshooting](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/memory/mem_trouble/). Current. Distinguishes heap, direct-buffer, metaspace, and network-memory failures.
6. Apache Flink, [Application Profiling and Debugging](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/debugging/application_profiling/). Current. Covers heap-dump and memory/GC evidence collection.
7. Apache Flink, [Tuning Checkpoints and Large State](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/large_state_tuning/). Current. Documents managed native state-backend memory and performance trade-offs.
8. Dask Distributed, [Worker Memory Management](https://distributed.dask.org/en/stable/worker-memory.html). Current. Describes managed/process memory, spill, pause, termination, and allocator retention.
9. Oracle, [Introduction to Garbage Collection Tuning](https://docs.oracle.com/en/java/javase/25/gctuning/introduction-garbage-collection-tuning.html). Java SE 25. Defines collector roles and throughput/scale implications.
10. Oracle, [Garbage-First Garbage Collector Tuning](https://docs.oracle.com/en/java/javase/25/gctuning/garbage-first-garbage-collector-tuning.html). Java SE 25. Documents G1 goals, behavior, and diagnostic approach.
11. Apache Arrow Java, [Memory Management](https://arrow.apache.org/java/current/memory.html). Current. Documents direct-memory allocators, limits, ownership, reference counting, and leak diagnostics.
12. Kubernetes, [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/). Current. Documents scheduling requests, cgroup-backed memory limits, and OOM behavior.
13. Linux Kernel, [Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html). Current. Defines memory current/peak/events, protection, throttling, hard limits, reclaim, and OOM controls.

## Exercises

### Exercise 1

Construct a peak ledger for a 24-GiB container with 12 GiB heap, four concurrent 1.5-GiB task-native peaks, 2 GiB network buffers, 1 GiB child processes, and 1 GiB runtime overhead. Decide whether a 2-GiB reserve fits.

### Exercise 2

Diagnose a worker whose heap oscillates between 5 and 9 GiB, post-GC occupancy is stable, RSS grows from 12 to 20 GiB, direct allocator bytes grow, and the container is OOM-killed at 20 GiB.

### Exercise 3

Design a safe external-sort spill plan for a 40-GiB partition with a 10-GiB execution budget, including capacity, integrity, attempts, merge, and cleanup.

### Exercise 4

Design an experiment to distinguish object churn, a retained heap leak, allocator caching/fragmentation, and an off-heap leak.

### Exercise 5

Choose mitigations for a job where reducing cache eliminates spill but increases remote reads, lowering concurrency meets the SLO but raises cost, and a larger heap causes the process to exceed its container limit.

## Answers to the Exercises

### Answer 1

The accounted peak is $12+4(1.5)+2+1+1=22$ GiB. A 2-GiB reserve reaches exactly the 24-GiB limit, leaving no uncertainty margin for unmeasured native pages, cache, overlap, or estimation error. Treat that as infeasible: reduce concurrency or per-task demand, shrink another pool, or increase the enforced limit and node request with measured margin. Do not merely set heap to 14 GiB.

### Answer 2

Stable post-GC heap weakens a managed-heap leak hypothesis. Rising direct allocator bytes and RSS aligned with the 20-GiB cgroup kill implicate off-heap ownership or an unreleased allocator path. Correlate child-process/native metrics and cgroup events, capture allocator ownership/debug evidence, inspect task/operator lifetimes, and reproduce by completed-work cycles. Bound the allocator and concurrency, close buffers on every path, and preserve the first kill evidence; GC flags do not reclaim reference-counted direct buffers.

### Answer 3

The minimum logical externalization is 30 GiB, but provision more for run metadata, compression variance, merge outputs coexisting with inputs, retries/speculation, and reserve. Create bounded sorted runs under a versioned comparator/serializer, checksum them, use attempt-private directories, cap file count and merge fan-in, and publish only the winner. Monitor bytes/inodes/latency and throttle before full. On failure, discard incomplete runs and clean losing/orphaned attempts through explicit ownership without deleting a live merge.

### Answer 4

Pin input, tasks, runtime, collector, and concurrency; repeat identical work cycles. Capture allocation/promotion rates, pause events, heap before/after collection, object-class/retention paths, allocator active/allocated/resident bytes, direct/native ownership, RSS/cgroup peaks, and task completion. High allocation with stable post-GC live set indicates churn. Rising post-GC reachable ownership indicates heap retention. High stable RSS that is reused without active-byte growth supports allocator caching/fragmentation. Rising owned native/direct bytes across completed lifetimes supports an off-heap leak. Confirm with controlled release/allocator changes rather than one snapshot.

### Answer 5

Reject the larger heap because it violates the full-process ledger. Compare smaller/serialized/selective cache against reread latency and network cost, and test intermediate concurrency values or memory-aware admission rather than one global reduction. Also reduce input width, pre-aggregate, split skew, and tune task sizes if they lower the live set. Choose the feasible configuration meeting the SLO with the lowest total worker, I/O, and retry cost under repeated cold/warm and failure cohorts; record cache hit value, spill physical I/O, headroom, and tail latency.
