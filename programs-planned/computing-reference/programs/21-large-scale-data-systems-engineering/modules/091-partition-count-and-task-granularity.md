---
module_id: LSDS-091
program: Large-Scale Data Systems Engineering
level: 2
module_number: 91
title: Partition Count and Task Granularity
status: complete
last_verified: 2026-09-04
---

# Partition Count and Task Granularity

## One-Page Review

### Governing question

How should an engineer choose and adapt partitions and task sizes so a distributed dataflow uses available parallelism, fits per-task memory, limits skew and retry loss, and avoids drowning the scheduler, storage, network, and output catalog in tiny work?

### Essential definitions

- A **logical partition** is a deterministic subset of records/keys owned as one unit by an operator.
- A **task** is one physical attempt to process one or more logical partitions for a stage.
- **parallelism** is the maximum number of task instances that may execute simultaneously for an operator/stage.
- A **wave** is up to one task per available execution slot running concurrently.
- **task granularity** is useful work/bytes/records/time per scheduled task.
- **scheduler overhead** is control-plane work to create, serialize, launch, track, retry, and retire tasks.
- **partition expansion factor** maps encoded input bytes to peak in-memory working bytes for an operator.
- **skew** is imbalance in bytes, records, keys, CPU, state, or duration among partitions.
- **coalescing** combines partitions; **repartitioning** redistributes data; **splitting** divides an oversized/skewed partition.
- **small-file amplification** is output file/metadata/request growth caused by excessive writer partitions.
- **adaptive partitioning** uses runtime statistics to coalesce small or split skewed partitions while preserving semantics.

### Central model, mechanism, or theorem

For stage input $B$ bytes, $N$ partitions, $S$ available slots, per-task fixed scheduler cost $o$, usable per-task memory $M$, and expansion factor $\alpha_i$ for partition $i$, a candidate must satisfy:

$$N\ge\left\lceil\frac{B}{b_{max}}\right\rceil,\qquad \alpha_i b_i+s_i\le M\ \forall i,$$

where $s_i$ is additional state/sort/hash/buffer memory. To expose several waves of work, target $N\ge kS$ for workload-specific $k$, while total scheduler work grows roughly $No$ and output writers may create $O(N)$ files.

Choose a range, not a magic count: enough partitions for memory fit, utilization, locality, skew splitting, and bounded retry loss; few enough for useful task duration, driver/coordinator capacity, source/object request rate, shuffle metadata/connections, and target file sizes. Measure distributions at each stage and adapt because source splits, shuffle partitions, keyed state, and sink files have different constraints.

### Critical invariants

- Partition identity and coverage are complete, nonoverlapping where required, and stable across retry.
- Per-task peak working set includes decoded expansion, aggregation/join state, sort/spill buffers, runtime overhead, and concurrent operators.
- Parallelism is bounded by runnable partitions, slots, locality, and downstream capacity—not partition count alone.
- Task overhead and useful work are measured separately; subsecond tasks may still overload the control plane.
- Skew is measured by distributions and normalized work, not hidden behind average partition size.
- Repartition/coalesce/split operations preserve keys, ordering, watermarks, state ownership, and output semantics promised by the stage.
- Adaptive changes are versioned and observable; retry/recovery uses the executed mapping.
- Writer parallelism and target file layout are designed explicitly rather than inherited accidentally.
- Speculative/retried attempts publish through one-winner idempotent or transactional output.
- Tuning is compared under the same input, code, resources, cache state, and failure/load cohort.

### Common failures

Common failures include setting partitions equal to cores; using one global default for every stage; choosing by compressed bytes while decoded rows expand; ignoring per-key state and join build-side memory; creating one task per tiny file; assuming more partitions always increase throughput; using average size while one partition holds half the data; coalescing to one writer and serializing the job; repartitioning without accounting for shuffle cost; changing key partitioning across state recovery; letting adaptive plans disappear from evidence; tuning task time without output-file/catalog consequences; and benchmarking warm cache against cold production.

### Compact example

A stage reads 960 GiB on 120 slots. Targeting 2 GiB creates 480 tasks, four tasks per slot. With expansion factor 2.5, each partition needs about 5 GiB before extra operator state, fitting an 8-GiB usable budget only if buffers/state leave adequate margin. At 0.2 seconds fixed control work per task, total scheduler work is 96 seconds, not necessarily wall time. Skew or a 6-GiB partition would invalidate the average-based plan and require split/salt/range changes.

### Connections

[LSDS-053](053-fair-and-capacity-scheduling.md) supplies capacity allocation, [LSDS-055](055-work-stealing-and-speculation.md) supplies balancing/speculation, [LSDS-056](056-preemption.md) supplies interruption behavior, [LSDS-060](060-diagnosing-scheduler-delay-and-resource-fragmentation.md) supplies scheduler evidence, [LSDS-063](063-exchange-operators.md) supplies shuffle partitioning, and [LSDS-068](068-adaptive-query-execution.md) supplies runtime adaptation.

## Governing Question

Distributed execution needs enough independent work to fill workers and survive slow/failing attempts. But each task consumes coordinator messages, serialized closures, queue operations, process/JVM/runtime setup, connections, shuffle tracking, metrics, and output metadata. Partitioning trades data-path concurrency against control-plane and storage amplification.

The correct count changes across a graph. File scans begin with source splitability and open cost. Hash aggregation depends on key cardinality and state expansion. Joins face heavy keys. Iterations benefit from stable ownership. Sink writers target file/transaction sizes. A count appropriate at ingress can be disastrous after a filter or fan-out.

The governing question is how to derive constraints, observe actual distributions, choose an initial feasible range, run controlled experiments, and let safe adaptive execution refine it without breaking semantics or recoverability.

## Why This Matters

Too few partitions leave cores idle, concentrate memory, increase spill/OOM risk, make stragglers dominate, and enlarge retry loss. Too many create tiny tasks, scheduling delay, driver memory pressure, excessive shuffle blocks/connections, object-store requests, small output files, checkpoint metadata, and long cleanup/listing operations.

Average bytes are misleading. Encoded columnar data can expand when decoded; a hash table adds buckets and object overhead; a sort needs buffers; multiple chained operators coexist; one hot key cannot be divided by ordinary hashing. Duration combines data volume, CPU complexity, locality, spill, throttling, and contention.

Partition topology is also correctness state. Keyed streaming state maps keys to partitions/key groups. Ordering and range boundaries affect merge operations. Recovery, rescaling, and transactional writers need stable mapping or explicit migration. Performance tuning cannot casually rewrite these invariants.

## Prerequisites and Retrieval

Review capacity scheduling in [LSDS-053](053-fair-and-capacity-scheduling.md), work stealing/speculation in [LSDS-055](055-work-stealing-and-speculation.md), preemption in [LSDS-056](056-preemption.md), scheduler delay in [LSDS-060](060-diagnosing-scheduler-delay-and-resource-fragmentation.md), exchanges in [LSDS-063](063-exchange-operators.md), and adaptive execution in [LSDS-068](068-adaptive-query-execution.md).

You should understand partitions, stages/tasks/attempts, slots/cores, shuffle, hash/range partitioners, skew, compression, serialization, working sets, spill, data locality, speculation, adaptive execution, object-store request economics, file formats, state key groups, and percentiles.

For diagnosis retain stage/operator/partition/attempt/executor IDs, input/output/shuffle encoded and decoded bytes, records/keys/groups, CPU/run/deserialize/fetch/scheduler time, peak heap/off-heap/managed/native memory, spill, GC, locality, source files/splits/open requests, slots/waves, skew quantiles, adaptive split/coalesce mapping, retries/speculation, output files/sizes, catalog commits, and configuration/resource/version cohort.

## Learning Objectives

After this module, you should be able to:

1. distinguish logical partitions, physical tasks, parallelism, slots, and waves;
2. derive lower bounds from memory fit, utilization, skew, and retry-loss requirements;
3. derive upper bounds from scheduling, metadata, request, connection, and file overhead;
4. estimate peak working memory using expansion and operator state;
5. diagnose small-task and large/skewed-task regimes from distributions;
6. choose source splits, shuffle partitions, state ownership, and sink writers independently;
7. compare coalesce, repartition, range/hash partitioning, salting, and adaptive split/merge;
8. preserve ordering, key/state, output, and recovery invariants during change;
9. run controlled tuning experiments and model total resource/cost effects; and
10. validate granularity under failure, cold cache, load variation, and skew.

## Core Exposition

### Separate partition, task, and slot

A stage may have $N$ logical partitions and therefore $N$ task attempts, but only $min(N,S)$ can run at once on $S$ eligible slots. Retries and speculation create more physical attempts without new logical coverage. Operator chaining may make several operators one physical task.

Report each count explicitly. “Parallelism 500” does not imply 500 cores, workers, or simultaneous tasks. Placement constraints, resource profiles, locality, unavailable executors, and downstream backpressure reduce concurrency.

### Start from source splitability

Splittable large files/objects can produce multiple scan tasks; unsplittable compressed streams may force one task per object. Tiny files should often be packed into scan partitions using byte plus open/request cost. Partition pruning and predicate/column pushdown change effective work after planning.

Record file count, size distribution, row groups/stripes, compression, object request latency/rate, listing cost, and locality. Do not create more useful scan parallelism than the format/source can support.

### Estimate working-set fit

For partition encoded bytes $b_i$, estimate decoded/vectorized expansion, live columns, object overhead, hash/sort/join state, aggregation cardinality, shuffle buffers, output buffers, runtime/JIT, and co-running chained operators. Use observed peak memory by operator, not only file size.

Require margin for skew and variance. Spill can prevent OOM but adds disk/network and changes tail latency; it is not evidence the partition was well sized. Some algorithms need the full build side or key group regardless of streamed input size.

### Expose enough waves

At least one runnable partition per slot avoids guaranteed idleness; several waves can average hardware/runtime variance and absorb failed/slow tasks. More waves also improve placement flexibility and elastic scheduling.

But wave count is workload-specific. If each task runs hours, more subdivisions reduce retry loss. If each runs tens of milliseconds, launch overhead dominates. Measure useful execution relative to scheduler/deserialization/setup time.

### Bound scheduler and driver pressure

Total task lifecycle events scale with tasks and attempts. Drivers/coordinators store task metadata, shuffle maps, metrics, accumulators, lineage, and status. Serialized closures/configuration and per-task connections add costs.

Measure submission-to-start delay, task launch/completion throughput, event queue lag/drops, driver heap/GC, scheduler CPU, result metadata, and UI/history size. A worker-idle stage with a busy coordinator is overpartitioned even if per-task compute is fast.

### Detect and classify skew

Compare p50/p90/p99/max bytes, records, distinct keys, state, CPU, spill, and duration; normalize duration by input bytes/records to separate heavy data from slow nodes/code paths. Inspect partition/key histograms before and after shuffle.

Heavy keys need salting/two-level aggregation, skew-join replication, or key-specific algorithms. Unequal range distributions need better samples/boundaries. Unsplittable records/groups require upstream model changes. Blindly increasing $N$ may hash the same hot key into one partition again.

### Choose shuffle parallelism per stage

After filters, expansions, joins, and aggregations, data volume/cardinality change. Size each exchange for its downstream operator's memory and parallelism needs, not the original scan count or one session default.

Repartition performs redistribution and can improve balance/parallelism at network/sort/serialization cost. Coalesce may combine existing partitions without a full shuffle but can preserve upstream imbalance and collapse parallelism. Range partitioning helps ordered/range work but depends on representative sampling.

### Account for network topology

More partitions create more shuffle block relationships, requests, buffers, connections, metadata, and small transfers. Too few create huge blocks, long fetches, receiver memory pressure, and expensive retries. Push/merged shuffle changes constants, not the need to measure.

Track block count/size distribution, fetch wait, local/remote bytes, request concurrency, failures, retransmission, server/client memory, and disk seeks. Partition count should fit both producers and consumers.

### Preserve keyed state semantics

Streaming parallelism maps keys/key groups and operator state to subtasks. Maximum parallelism and stable operator IDs constrain rescaling. Changing hash/serialization can reassign logical keys incorrectly even if throughput improves.

Use supported rescaling with a consistent savepoint/checkpoint and explicit redistribution semantics for union/broadcast/operator state and timers. Measure state per key group and hot-key load before selecting new parallelism.

### Design sink granularity separately

Compute partitions need not equal final files. Add a governed writer exchange/coalesce/compaction when output target size and partitioning differ. Too many writers create small files, transactions, open handles, catalog entries, and downstream scan tasks; too few bottleneck commit and memory.

Target file size is a distribution under compression, not a row-count constant. Preserve table partition boundaries and transaction/manifest atomicity. Background compaction is a cost, not a substitute for reasonable initial layout.

### Use adaptive execution safely

Runtime statistics can coalesce adjacent small shuffle partitions, split skewed partitions, or change join strategy. Record the executed plan/mapping, thresholds, input statistics, and output ownership so failures/retries reproduce compatible work.

Adaptation needs floors/ceilings and semantic guards. Coalescing may affect ordering/locality; skew splitting may replicate the other join side; changing partition count may alter floating-point reduction order and writer files. Validate the required equivalence.

### Tune with controlled experiments

Choose candidate counts around constraints, then run the same pinned input/code/config/resources and cold/warm cache cohort. Collect full distributions and total worker-hours, bytes/requests, scheduler load, spill, failure/retry cost, output layout, and end-to-end latency.

Change one principal lever at a time or use a designed experiment. Repeat enough to characterize noise. A faster isolated stage can slow the job by producing excessive files or saturating a shared service.

### Include failures and elasticity

Smaller units reduce lost work when a task fails and allow finer elastic redistribution, but raise attempt/commit overhead. Speculation only helps splittable/repeatable attempt-private work. Test executor loss, fetch failure, retry, scale-up/down, preemption, and stale attempts.

Adaptive parallelism under reduced slots may preserve liveness but change waves, memory, checkpoint state, and latency. State desired minimum/maximum and performance versus correctness behavior when capacity falls.

### Observe continuously

Dashboard partitions/tasks/attempts, active slots/waves, task and scheduler time, input/output/shuffle bytes and records, peak memory/spill/GC, locality/fetch, skew ratios, retries/speculation, adaptive actions, output files, metadata/requests, and cost.

Segment by job/stage/operator, logical partition/key range, source/table partition, attempt/executor/rack/zone, code/config/engine version, resource profile, input cohort, cache/load/failure mode, and percentile. Static defaults drift as data grows and distributions change.

## Definitions and Notation

Let:

- $B=\sum_i b_i$ be total stage bytes and $N$ partitions;
- $S$ be eligible execution slots and $w=\lceil N/S\rceil$ waves;
- $b_i,r_i,k_i$ be encoded bytes, records, and distinct keys in partition $i$;
- $\alpha_i$ be decode/representation expansion and $s_i$ additional operator state/buffers;
- $M$ be usable per-task memory;
- $o$ be fixed control/setup work per task;
- $t_i$ be task duration and $q_p(t)$ a duration percentile;
- $\rho_b=\max b_i/median(b_i)$ be one byte-skew ratio;
- $F$ be output files and $R$ physical attempts including retries/speculation.

Scheduler work $No$ is not necessarily wall time because coordination can overlap/parallelize. Average $B/N$ does not prove every $α_i b_i+s_i\le M$. Duration ratios need comparable input/operator/resource cohorts. File count may differ from task count through bucket/partition/rolling behavior.

## Mechanisms, Invariants, or Proof Structure

### Coverage proof

Partitioner maps every admitted record to exactly the required logical partition(s), and the manifest enumerates all partitions. Retry preserves identity; one-winner commit selects one valid attempt. Splitting/coalescing carries an explicit parent→child mapping whose union preserves coverage without unintended overlap.

### Memory-fit argument

For every partition, bound decoded working bytes plus state/buffers/runtime concurrency by usable $M$ with margin. Average bounds are insufficient; use high-quantile/max observations and adversarial heavy keys. Spill changes the execution mode and must be budgeted separately.

### Parallelism bound

At most $min(N,S)$ tasks run concurrently before other placement constraints. Thus raising slots above runnable partitions cannot speed the stage, and raising partitions above slots creates waves rather than direct concurrency. It can still improve balance/retry granularity at added overhead.

### Granularity trade-off

Reducing target bytes increases $N$, lowering average per-attempt work and potential retry loss while increasing approximately linear task lifecycle and often output/shuffle metadata. An optimum depends on measured curves and constraints; no universal bytes/task or tasks/core constant follows.

### Adversarial verification

Test empty/tiny/huge inputs, many tiny/one unsplittable file, compressed expansion, null/oversized record, heavy key, bad range sample, hot partition, low/high slots, lost executor, speculation, spill/disk full, adaptive split/coalesce, rescale/recovery, small-file sink, and scheduler/metadata saturation.

## Alternatives and Trade-Offs

| Lever | Strength | Cost or limitation |
|---|---|---|
| Fewer/larger partitions | Lower scheduler/metadata overhead | Lower concurrency, larger memory/retry/skew tails |
| More/smaller partitions | More waves, balance, elasticity, smaller retry loss | Scheduler, shuffle, request, and file amplification |
| Coalesce without shuffle | Reduces tasks/files cheaply | Can collapse parallelism and preserve skew |
| Full repartition | Rebalances and selects new ownership | Network, serialization, sort, and recovery mapping cost |
| Range partitioning | Supports ordered/range workloads | Sampling error and boundary skew |
| Salting/two-level aggregation | Splits heavy keys | Extra merge and semantic complexity |
| Adaptive coalesce/skew split | Uses runtime evidence | Plan variability, guardrails, and observability required |

Tune each stage boundary and sink deliberately. Defaults are starting points, not architecture.

## Failure Modes and Misconceptions

1. **Partitions equal cores.** It ignores waves, skew, retry loss, and elasticity.
2. **One global count.** Stages have different volumes and operators.
3. **Compressed size means memory.** Decoding/state/buffers expand it.
4. **Average fit means fit.** Tail partition can OOM.
5. **More is always faster.** Control/network/metadata overhead dominates.
6. **Tiny files equal parallelism.** Open/list/request costs can dominate scans.
7. **Increase N fixes hot key.** Hashing preserves the same heavy owner.
8. **Coalesce is free.** It can serialize upstream work and preserve imbalance.
9. **Repartition is only CPU tuning.** It changes shuffle, ordering, state, and files.
10. **Task duration alone.** Scheduler delay and downstream amplification are omitted.
11. **Slots imply concurrency.** Placement/resources/locality/backpressure constrain it.
12. **Adaptive means correct.** Executed mappings and semantic effects need validation.
13. **Compute partitions equal files.** Writer layout deserves an explicit stage.
14. **Warm benchmark generalizes.** Cache and contention alter the result.
15. **No failure experiment.** Retry/speculation/recovery economics remain unknown.

## Worked Examples

### Example 1

960 GiB at 2 GiB target produces 480 partitions; on 120 slots this is four nominal waves.

### Example 2

A 2-GiB compressed partition expands 2.5× to 5 GiB before hash state and buffers; an 8-GiB task needs explicit margin.

### Example 3

Ten thousand 100-ms tasks can expose less useful work than their aggregate scheduler and setup cost.

### Example 4

One unsplittable 500-GiB gzip object remains one scan bottleneck despite requesting 1,000 partitions downstream.

### Example 5

Median shuffle partition is 128 MiB and maximum is 8 GiB: byte skew ratio 64 demands targeted splitting, not average tuning.

### Example 6

Coalescing 1,000 partitions to one can make upstream processing execute through one narrow consumer; a shuffle repartition preserves more parallelism at network cost.

### Example 7

A hot customer key is salted into 16 partial aggregates, then merged once, with exact count/sum invariants checked.

### Example 8

Compute uses 800 partitions while a writer exchange produces 80 approximately target-sized files, decoupling CPU from table layout.

### Example 9

Executor loss repeats one 4-minute partition rather than one 40-minute partition, but the smaller design adds ten times more task metadata.

### Example 10

The executable fixture computes partition waves, memory expansion, and total scheduler work for a candidate plan.

<!-- bijux-verify: {"id":"partition-granularity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"input_gib=960\nslots=120\npartitions=480\ntasks_per_slot=4.0\npartition_gib=2.0\nexpanded_gib=5.0\nfits_memory=true\nscheduler_work_seconds=96.0\n","stderr":""}} -->
```python
import math

input_gib = 960
slots = 120
target_partition_gib = 2.0
expansion = 2.5
usable_memory_gib = 8.0
fixed_task_overhead_seconds = 0.2
partitions = math.ceil(input_gib / target_partition_gib)
partition_gib = input_gib / partitions
expanded_gib = partition_gib * expansion

print(f"input_gib={input_gib}")
print(f"slots={slots}")
print(f"partitions={partitions}")
print(f"tasks_per_slot={partitions / slots:.1f}")
print(f"partition_gib={partition_gib:.1f}")
print(f"expanded_gib={expanded_gib:.1f}")
print(f"fits_memory={str(expanded_gib <= usable_memory_gib).lower()}")
print(f"scheduler_work_seconds={partitions * fixed_task_overhead_seconds:.1f}")
```

## Cross-Program Connections

- **Algorithms:** work/span, load balancing, external memory, hashing, sorting, and sampling explain partition behavior.
- **Distributed systems:** ownership, retries, locality, speculation, fencing, and recovery constrain task identity.
- **Storage:** splitability, row groups, compression, requests, file sizes, manifests, and compaction shape both ends.
- **Networking:** shuffle blocks, fan-out, connections, buffers, and transfer granularity impose separate limits.
- **Streaming:** key groups, state, timers, watermarks, backpressure, and rescaling require stable semantics.
- **Schedulers:** slots, waves, placement, queues, resource profiles, driver throughput, and elasticity determine concurrency.
- **Reliability:** smaller retry units trade expected lost work against more attempts and commit metadata.
- **Economics:** worker time, coordinator load, storage requests, shuffle, spill, and future scan cost all matter.

## References

1. Apache Spark, [Performance Tuning](https://spark.apache.org/docs/latest/sql-performance-tuning). Current. Documents file/shuffle partition controls, coalescing, and adaptive skew handling.
2. Apache Spark, [Tuning](https://spark.apache.org/docs/latest/tuning.html). Current. Covers parallelism, task/closure overhead, memory, and locality.
3. Apache Spark, [Configuration](https://spark.apache.org/docs/latest/configuration). Current. Documents scheduler, speculation, resource, and partition settings.
4. Apache Spark, [RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide). Current. Defines partitions, transformations, stages, persistence, and execution.
5. Apache Flink, [Jobs and Scheduling](https://nightlies.apache.org/flink/flink-docs-stable/docs/internals/job_scheduling/). Current. Defines job/execution graphs, subtasks, slots, and result partitions.
6. Apache Flink, [Parallel Execution](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/execution/parallel/). Version 2.3. Documents operator parallelism, maximum parallelism, and key groups.
7. Apache Flink, [Configuration](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/config/). Current. Documents slot, memory, parallelism, slow-task, and resource controls.
8. Apache Flink, [Elastic Scaling](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/elastic_scaling/). Current. Describes adaptive batch/streaming parallelism under changing slots.
9. Dask, [Best Practices](https://docs.dask.org/en/stable/best-practices.html). Current. Discusses task overhead, partitions, chunks, and graph size.
10. Dask, [Array Chunks](https://docs.dask.org/en/stable/array-chunks.html). Current. Documents chunk-size trade-offs, alignment, and rechunking.
11. Ray Data, [Performance Tips and Tuning](https://docs.ray.io/en/latest/data/performance-tips.html). Current. Covers block sizing, task parallelism, memory, and streaming execution.
12. Apache Beam, [Runtime Model](https://beam.apache.org/documentation/runtime/model/). Current. Defines bundle execution, fusion, retries, and runner-controlled granularity.

## Exercises

### Exercise 1

Derive a feasible partition-count range for 12 TiB input, 300 slots, 6 GiB usable task memory, and measured 3× decoded expansion plus 1 GiB operator state.

### Exercise 2

Diagnose a stage with low CPU utilization, 50-ms median tasks, 40-minute scheduling delay, and two million output files.

### Exercise 3

Design a skew fix when one customer owns 35% of records and aggregation must preserve exact sums and distinct counts.

### Exercise 4

Design separate scan, shuffle, keyed-state, and writer parallelism for a pipeline, including adaptive rules and recovery evidence.

### Exercise 5

Design an experiment comparing 240, 480, 960, and 1,920 partitions under cold/warm cache, executor loss, and output-file constraints.

## Answers to the Exercises

### Answer 1

12 TiB is 12,288 GiB. Memory leaves at most 5 GiB for expanded input before the 1-GiB state, so encoded partition target is at most $5/3$ GiB and memory lower bound is $\lceil12288/(5/3)\rceil=7,373$ partitions (before further margin). That is about 24.6 tasks per slot, so utilization is available. The upper bound must come from measured scheduler/task overhead, source splits/requests, shuffle metadata, and target files. Reduce expansion/state, spill deliberately, or add memory if 7,373 tasks are too fine; never choose 900 merely from three waves because it violates memory fit.

### Answer 2

This is the overpartitioned/tiny-task regime: useful execution is dwarfed by lifecycle overhead and sink metadata. Verify driver event queue/CPU/heap, launch throughput, task setup/serialization, object requests, and file-size distribution. Coalesce/repartition at the appropriate stage into longer tasks, decouple writer count to target file size, and compact existing output if justified. Retest memory, skew, locality, failures, and end-to-end scans; do not infer the fix from CPU alone.

### Answer 3

Increasing ordinary hash partitions keeps the heavy key together. Salt that customer's records by a stable subkey into enough bounded partial partitions, compute mergeable sum and a rigorously correct distinct structure or exact deduplicated ID sets, then merge by unsalted customer. Prove coverage/no overlap, stable retry IDs, and exact final invariants; size/replicate any join counterpart deliberately. If the aggregation is not safely decomposable, use a key-specific algorithm or isolate the customer with more resources.

### Answer 4

Pack splittable source row groups/files by bytes plus open cost; choose each shuffle count from downstream expansion/state and slots; keep keyed-state maximum parallelism/stable key-group mapping independent of momentary slots; add a writer exchange for target table partitions/file sizes. Runtime coalesces only small adjacent shuffle partitions and splits measured skew within floors/ceilings. Persist the executed parent-child mapping, operator/key identities, input/output metrics, and checkpoint compatibility so retry/restore uses the same logical coverage.

### Answer 5

Pin input/code/config/resources and run repeated cohorts for each count with cold and warm cache. Collect scheduler/submission delay, launch rate, task-duration distribution, CPU, memory, spill/GC, locality, shuffle blocks/fetch, requests, worker-hours, output file sizes/count, catalog time, and end-to-end latency/cost. Kill an executor at comparable progress and measure repeated work/recovery. Reject candidates violating memory, SLO, scheduler, dependency, or file constraints; compare remaining feasible points with uncertainty rather than choosing the lowest single run.
