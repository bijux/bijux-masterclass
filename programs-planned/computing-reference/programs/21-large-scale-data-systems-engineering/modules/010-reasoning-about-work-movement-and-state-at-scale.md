---
module_id: LSDS-010
program: Large-Scale Data Systems Engineering
level: 1
module_number: 10
title: Reasoning About Work, Movement, and State at Scale
status: complete
last_verified: 2026-09-03
---

# Reasoning About Work, Movement, and State at Scale

## One-Page Review

### Governing question

How can an engineer explain and improve a cluster dataflow by accounting jointly for useful work, dependency span, data movement, live and durable state, failures, bottleneck capacity, cost, and result correctness?

### Essential definitions

- **Work** is total resource consumption across execution, such as CPU-seconds, device-seconds, I/O operations, or decompressed bytes processed.
- **Span** is the duration of the longest dependency path under an explicit stage/operation-duration model.
- **Movement** is data crossing a boundary, annotated by bytes, records, source/destination, distance, bandwidth, latency, serialization, and retry.
- **State** is information retained across records, tasks, stages, iterations, failures, or publication; its size and lifetime both matter.
- A **bottleneck** is the capacity constraint whose marginal relief improves the selected objective under the observed workload.
- **Amplification** is actual work, movement, or state divided by a documented useful or minimum baseline.
- **Critical path** is the dependency path that gates completion; a busy operation off that path may not affect latency.
- A **resource-time integral** measures occupancy such as byte-seconds, core-seconds, or accelerator-seconds rather than only a peak.

### Central model, mechanism, or theorem

For physical graph `G=(V,E)`, keep a resource ledger `L=(W,S,M,Q,F,K,O)`: work by resource `W`; dependency span `S`; movement by edge/boundary `M`; state size/lifetime `Q`; failure/retry work `F`; capacity and contention `K`; and user/domain outcomes `O`.

Elapsed time is bounded below by the critical-path span and by each resource demand divided by usable bottleneck capacity. These are lower bounds, not an additive prediction: overlap, queueing, skew, serialization, spill, barriers, and failures determine the realized schedule. Optimize only after identifying which bound or invariant is active.

### Critical invariants

- Correct result, completeness, freshness, and side-effect semantics are checked before speed.
- Logical work is separated from attempts, retries, speculation, and maintenance.
- Movement is attributed to exact edges and locality tiers; bytes read and bytes transferred are not synonyms.
- State has identity, owner, schema, lifetime, durability, cleanup, and recovery purpose.
- Peaks and tails are retained alongside totals and averages.
- Capacity means usable concurrent service under contention, not nominal hardware sum.
- Optimizations are compared on the same workload, result, failure assumptions, and measurement boundary.
- Cost and consequence include recovery, idle/waiting resources, retained state, and operational burden.

### Common failures

Frequent failures are optimizing CPU while blocked on shuffle, counting cores instead of usable capacity, summing overlapped durations, ignoring the critical path, treating all bytes equally, confusing cached state with durable state, reducing runtime by changing semantics, hiding retry/speculation work, using averages that erase skew, tuning one stage while moving the bottleneck, and celebrating scale-up without a competent small baseline.

### Compact example

A seven-stage toy plan has 61 CPU-seconds, a 23-second dependency path, 600 MB across three movement boundaries, ten seconds of serialized transfer at the stated isolated bandwidths, and 280 MB of peak live state. Four slots give a CPU-work lower bound of 15.25 seconds, but the 23-second path is already larger. Neither number predicts wall time until overlap, contention, and resource feasibility are specified.

### Connections

[LSDS-001](001-workloads-that-require-multiple-machines.md) asks why distribution is necessary. [LSDS-002](002-horizontal-partitioning.md) through [LSDS-009](009-cluster-failure-assumptions.md) provide partitions, locality, graphs, stages, dependency width, serialization, and failure models. The rest of the program applies this integrated ledger to storage, batch, shuffle, streams, scheduling, SQL, lakehouse state, recovery, and cost.

## Governing Question

A distributed job can use every worker and still be inefficient. It can scale linearly while remaining slower than a careful single-machine program. It can reduce CPU yet increase network, storage, or recovery cost. It can finish faster by dropping late data or weakening validation. A dashboard full of green utilization cannot determine whether the system produced the right result at a justified cost.

Engineers need a compact way to connect the physical graph to resource behavior. Work describes how much processing occurs. Span identifies serial dependency. Movement describes where bytes cross expensive boundaries. State describes what remains live, durable, or recoverable. Failure adds repeated work and changes capacity. Outcomes anchor the ledger to correctness, latency, throughput, freshness, availability, and domain consequence.

The governing question is not “How do we minimize everything?” Trade-offs make that impossible. Compression reduces movement while adding CPU. Caching reduces recomputation while adding state. More partitions improve parallelism until scheduling, metadata, tiny blocks, or skew dominate. The question is which constraint gates the chosen outcome, what change relaxes it, what cost moves elsewhere, and what evidence confirms the result.

## Why This Matters

Cluster scale multiplies small inefficiencies. A redundant decode per record becomes thousands of core-hours. A few extra bytes become terabytes of shuffle. One oversized key gates a stage with ten thousand completed peers. Retaining intermediate results avoids replay but consumes storage for every run. Retry storms spend resources without increasing accepted output.

Different metrics can tell contradictory truths. CPU utilization may be low because tasks wait for remote fetch, or high because serialization and garbage collection dominate. Network links may be under nominal capacity while one rack uplink or storage endpoint saturates. Aggregate state may fit while one worker spills. Average task time may fall while the maximum increases and completion slows.

The ledger supports design before deployment and diagnosis afterward. During design, it exposes unavoidable cuts, state horizons, and capacity bounds. During operation, it aligns plan versions with measurements. During optimization, it prevents shifting cost outside the measured boundary. During review, it makes assumptions and consequences explicit.

## Prerequisites and Retrieval

Retrieve from [LSDS-001](001-workloads-that-require-multiple-machines.md) the need for distribution and small-baseline comparison. Recall partition count and skew from [LSDS-002](002-horizontal-partitioning.md), locality from [LSDS-004](004-data-locality.md), graph work/span from [LSDS-005](005-distributed-task-graphs.md), and task attempts from [LSDS-006](006-stages-tasks-and-dependencies.md).

Recall dependency width and recovery cones from [LSDS-007](007-narrow-and-wide-transformations.md), serialized bytes from [LSDS-008](008-serialization-across-workers.md), and conditional recovery assumptions from [LSDS-009](009-cluster-failure-assumptions.md). You should understand DAGs, sums, maxima, rates, capacity, percentiles, integrals, dimensional analysis, and controlled experiments.

## Learning Objectives

After completing this module, you should be able to:

- build a graph-versioned ledger for work, span, movement, state, failure, capacity, and outcomes;
- distinguish total work from critical-path duration and realized wall time;
- derive resource-capacity and cut-based lower bounds without treating them as predictions;
- attribute local, rack, zone, storage, and external movement to physical edges;
- measure state by size, lifetime, durability, ownership, and recovery role;
- calculate useful-work, movement, retry, and storage amplification;
- diagnose CPU, memory, network, storage, scheduler, skew, and coordination bottlenecks;
- compare scale-up and scale-out against competent baselines;
- design controlled optimization experiments with semantic equivalence;
- connect batch completion and streaming stability to capacity and backlog;
- retain evidence that survives adaptive plans and retries; and
- conduct consequence-aware review beyond performance metrics.

## Core Exposition

### Begin with the outcome and boundary

Name the result before measuring resources. For batch, specify records/partitions, schema, input snapshot, validation, completion deadline, and committed output. For streaming, specify event-time behavior, accepted lag, updates/retractions, state and sink semantics. For interactive queries, specify result equivalence, freshness, concurrency, and latency distribution.

Choose the accounting boundary. Does elapsed time include queueing, cluster provisioning, source listing, schema lookup, output commit, and cleanup? Do bytes include storage reads, retries, replication, and cross-zone traffic? Do costs include idle reservation and retained checkpoints? Comparisons require the same boundary.

Correctness is a constraint, not a metric to trade silently. Dropping records, shrinking retention, using stale lookup data, changing floating-point order, or weakening durability can reduce work. Label such changes as semantic/policy decisions and review them independently.

Bind evidence to input, code, configuration, schema, graph, partitioner, engine, cluster, and attempt versions. A runtime number without these identities cannot support a reproducible comparison.

### Work by resource

CPU work can be expressed as core-seconds, but separate useful application computation from serialization, compression, garbage collection, encryption, scheduling, retry, and idle wait. Accelerator work, storage requests, disk bytes, decompressed bytes, and external calls need their own dimensions.

Total work is additive across tasks and attempts. Wall time is not. Eight tasks that each consume five CPU-seconds have 40 CPU-seconds of work; with four fully usable cores and no other constraint, the work bound is ten seconds. Skew, dependencies, placement, or contention can make realization much longer.

Count logical and physical work separately. Accepted logical output may require one task; failures and speculation can execute three attempts. Maintenance work includes checkpointing, compaction, replication, cleanup, and statistics. Hiding it outside a query timer understates system cost.

The useful baseline depends on the question. For an aggregation it may be bytes/records semantically required. For an iterative algorithm it may be the best known implementation on one machine. McSherry, Isard, and Murray's COST framing asks how much hardware a scalable system needs before it beats a competent single-threaded implementation, exposing parallelized overhead.

### Span and the critical path

The span of a weighted DAG is the maximum sum of durations along any dependency path. With unlimited resources and the stated operation durations, execution cannot finish faster. Real stage duration includes its slowest required partition, not its median task.

Critical path changes with the physical plan and runtime. A cached input can remove upstream work. A shuffle creates a materialization/read path. Adaptive skew splitting can shorten one stage while adding tasks. A resource wait can extend the realized critical path even when absent from the logical DAG.

Do not add every stage or metric. Independent branches overlap; CPU time can overlap network wait; serialization can overlap transport; checkpoint I/O can be asynchronous. Conversely, do not assume full overlap. Blocking edges, buffer limits, backpressure, or shared capacity serialize work.

Compute planned dependency span, then reconstruct realized critical path from task/stage events, queue intervals, transfers, and barriers. Ask which predecessor and partition actually gated each downstream start or completion.

### Resource-capacity lower bounds

For resource `r` with total demand `W_r` and usable aggregate service capacity `K_r`, `T >= W_r/K_r` over a stable interval. CPU uses core-seconds/usable cores; network uses bytes/bytes-per-second across the relevant cut; storage can use bytes/throughput or operations/IOPS.

“Usable” accounts for tenancy, reservations, protocol overhead, topology, concurrency, and attainable efficiency. Nominal line rate or core count is an upper hardware label, not measured workload service capacity. One hot partition may use only one core or connection, making its per-task bound stronger than the aggregate bound.

Overall elapsed time is at least the maximum of applicable resource bounds and dependency span. It is not normally their sum because resources overlap. Queueing, contention, startup, tail effects, and feedback can raise actual time above all simple bounds.

A lower bound helps reject impossible expectations and identify headroom. If runtime is near a measured storage bound, CPU micro-optimization cannot yield a large gain. If runtime is far above every credible bound, investigate scheduling, skew, serialization, backpressure, and unaccounted dependencies.

### Movement as a graph property

Annotate each physical edge with records, serialized and compressed bytes, source/destination partitions, locality tier, transfer attempts, and time. Distinguish bytes read from local storage, copied within a process, across processes, across hosts, racks, zones, regions, and external boundaries.

The same byte count has different cost by path. Local memory copy, SSD read, rack network, cross-zone link, and object-store GET differ in latency, capacity, monetary charge, and failure surface. Weight movement only with an explicit objective; retain raw quantities too.

For a network or storage cut, sum bytes that must cross it and divide by usable cut capacity for a lower bound. Per-flow bandwidth is not additive when flows share a link. Aggregate cluster networking can look idle while one rack uplink or storage shard gates the stage.

Measure amplification: actual bytes transferred divided by a declared logical/minimum baseline. Retries, replication, spills, shuffle, format conversion, small-record overhead, and nonselective reads raise it. Compression changes wire bytes but adds compute and may delay first output.

### State size, lifetime, and purpose

State includes input buffers, hash tables, sort runs, shuffle blocks, caches, broadcast data, window/operator state, checkpoints, manifests, dictionaries, indexes, output candidates, and retained history. A byte must have an owner, key/scope, schema/version, creation condition, lifetime, durability, cleanup, and recovery purpose.

Peak state determines capacity and spill risk; byte-seconds reflect occupancy cost. A 1-TB cache for one minute and 10 GB for one day have different peaks and integrals. Distribution matters: 1 TB evenly spread can fit while 200 GB on one worker fails.

Distinguish working state, materialized intermediate state, and durable recovery state. Working hash tables may vanish after a task. Shuffle blocks live through consumers and perhaps retries. Checkpoints survive target faults. A local cache is not a durable source merely because it is on disk.

State reduces other costs. Caching saves repeated work/movement. A pre-aggregation hash table reduces shuffle bytes. A checkpoint caps replay. Evaluate saved expected work against write/read, memory/storage, cleanup, and consistency cost under reuse/failure probability.

### Work, movement, and state interactions

These dimensions exchange cost. Compression spends CPU/state buffers to reduce movement. Columnar batches spend memory and latency to improve vectorized work and compression. Repartitioning spends movement and state to improve later locality, balance, or reuse. Materialization spends storage to reduce recovery work.

Operator fusion reduces serialization, launch, and intermediate state, but lengthens a coupled pipeline and can enlarge retry scope. More partitions expose parallelism and reduce per-task state, but add scheduler work, connections, files, headers, and metadata. Fewer partitions amortize overhead but increase tails and memory.

Map-side aggregation spends CPU and bounded hash state to reduce records across a wide edge. It helps only when keys repeat and the combine algebra is valid. With mostly unique keys, it can add state/work without reducing movement.

Broadcasting spends replicated state on every worker to avoid repartitioning a large input. The correct threshold depends on serialized and expanded size, worker count, reuse, memory headroom, distribution cost, and failure/rebroadcast behavior.

### Skew and tails

Totals describe cost; maxima gate stages. Report per-partition input, output, CPU, wall time, shuffle read/write, remote fetch, spill, peak memory, state, and retry. Compare median, p95, p99, and maximum. Correlate slow tasks with keys, blocks, hosts, attempts, and paths.

Skew can be data volume, record cost, output expansion, key state, network path, storage shard, or placement. Remedies differ. Splitting bytes does not help one indivisible hot-key state; adding memory does not help a throttled endpoint; speculation does not help deterministic work.

Long tails can make nominal parallelism deceptive. A stage with 9,999 ten-second tasks and one ten-minute task completes near ten minutes. Average utilization falls near the end while the critical task gates successors. Measure the completion frontier and outstanding critical work.

Adaptive split/coalesce changes task counts and mappings; compare realized graph versions. Averages across old and new partitions can manufacture apparent gains or losses.

### Failure and amplification

Failures add work, movement, state reads, and delay while reducing usable capacity. Keep original, retry, speculative, recovery, and cleanup attempts distinct. Define accepted useful output, then calculate attempted-to-accepted CPU and byte ratios.

A lost narrow task replays a bounded cone; a lost shuffle producer can regenerate blocks for many targets. Checkpoints trade periodic work/state for bounded replay. Corrupt output can require a wider trusted recovery boundary than missing output.

Retry storms are resource feedback. More attempts create more source reads, transfers, logs, and scheduler events during reduced capacity. Bound retries, classify faults, add jitter/backoff, and reserve recovery capacity. An optimization benchmark without injected failure says nothing about this amplification.

Expected-cost models can include failure probability times recovery work, but tail scenarios and correlations matter. Keep scenario results alongside expectations. A low average may hide an unacceptable zone-loss recovery cost.

### Batch versus streaming stability

Batch work is finite and commonly optimized for completion time, throughput, deadline, and total cost. Span and tails are visible at job end. Reuse and checkpoint decisions depend on expected future actions and failure horizon.

Streaming is continuing. Stable operation requires sustainable service rate above arrival rate over the relevant horizon. State grows with keys, windows, retained history, and lag. Backpressure moves queues upstream; it does not create capacity. Watermarks/progress affect when state can be released.

Measure records/bytes in and out, busy/backpressured/idle time, event-time lag, checkpoint start/alignment/duration, state size/growth, sink latency, and recovery catch-up. Flink's current metrics expose network buffers, local/remote bytes, busy/idle/backpressured time, initialization, state, and checkpoint signals useful for this ledger.

For unbounded out-of-order data, correctness, latency, and cost are deliberate trade-offs. The Dataflow model emphasizes event-time windows, watermarks, triggers, and accumulating behavior rather than pretending input becomes globally complete.

### Bottleneck diagnosis

First verify input/output correctness and measurement boundary. Draw the realized physical graph. Mark stage starts/ends, gating partitions, queueing, and attempts. Build work, movement, state, and failure ledgers at edge/partition granularity.

Next compare demand with usable capacities and correlate saturation with the critical path. CPU-bound work has high useful CPU and scales until another limit. Network-bound work shows edge bytes/fetch wait and constrained cuts. Storage-bound work shows throughput/IOPS/throttling. Memory pressure shows peak state, spill, GC, or OOM. Scheduler-bound work shows short tasks and launch/queue overhead.

Backpressure indicates downstream inability to accept at current rate; find the first saturated resource rather than tuning the most visibly blocked upstream operator. A blocked task can be the victim, not cause. Use controlled changes—partition count, codec, batch, placement, projection, cache, join strategy—one hypothesis at a time.

After change, revalidate results, graph, resource ledger, failure behavior, and cost. A bottleneck moves: reducing shuffle can expose CPU; adding workers can saturate storage; larger batches can raise memory/tails. Optimization is iterative, not a one-metric victory.

### Cost and consequence

Translate resource quantities into cost only with dated prices/accounting rates and allocation policy. Include worker reservation/runtime, autoscaling lag, storage capacity/time, storage requests, network tiers, managed-service charges, failed/retry work, and operational labor where decision-relevant.

Cost attribution needs shared-resource policy. Peak-provisioned capacity, caches, control planes, and shared shuffle services cannot always be assigned by raw CPU alone. Report both marginal and fully allocated views when they answer different decisions.

Performance objectives reflect consequences. A late fraud report, stale scientific result, delayed recommendation, or missed emergency alert has different harm. Faster results obtained by excluding hard cases can be inequitable. Domain owners define acceptable correctness, freshness, degradation, and priority.

### Evidence and review record

Retain experiment hypothesis, baseline, workload/input digest, graph/plan, code/config/schema, cluster/topology, engine/runtime, start conditions, warm-up, concurrency, failure injection, raw metrics, quantiles, output validation, cost boundary, and conclusion. Preserve rejected hypotheses.

Use competent baselines: a single thread/machine where feasible, scale-up on one node, and alternative physical plans. Report strong and weak scaling with absolute work and dataset size. A curve without absolute time, resources, correctness, and cost can mislead.

Spark's current monitoring API exposes task CPU/run time, serialization, GC, input/output, shuffle, spill, peak execution memory, attempts, and quantile summaries. These are ingredients, not a completed analysis. Connect them to the graph, capacity, state, and outcome.

## Definitions and Notation

For physical graph `G=(V,E)`, let `d_v` be the modeled duration of vertex/stage `v`. Dependency span is `S(G)=max_path sum_(v in path) d_v`. If task tails define stage duration, use the gating required task/attempt evidence rather than mean task duration.

For resource `r`, total demand is `W_r=sum_a w_(a,r)` over relevant attempts/maintenance actions `a`. With usable capacity `K_r`, `T >= W_r/K_r`. Overall `T >= max(S(G), max_r W_r/K_r, max_c M_c/B_c)`, where `M_c` crosses cut `c` and `B_c` is usable cut bandwidth. Avoid double-counting when a demand already contributes to modeled `d_v`.

For edge `e`, movement record is `M_e=(records, logical_bytes, serialized_bytes, wire_bytes, locality, attempts, time)`. Total wire movement is a sum; elapsed transfer is not generally the sum because edges overlap and contend.

Let state objects `q` have size function `size_q(t)` and live interval. Peak state is `Q_peak=max_t sum_q size_q(t)`. State occupancy is `Q_time=integral sum_q size_q(t) dt`. Compute per worker/tier as well as globally.

For resource dimension `r`, amplification `A_r=actual_r/useful_baseline_r`, with numerator, denominator, scope, and zero-baseline behavior declared. Retry amplification can be attempted task work divided by accepted logical task work.

For streaming arrival rate `lambda` and sustainable processing rate `mu`, stable backlog requires long-run `mu>lambda` with sufficient burst/state headroom. A failure backlog `B` clears no faster than `B/(mu-lambda)` under a constant-rate idealization.

## Mechanisms, Invariants, or Proof Structure

To reason about a workload at scale:

1. Freeze the outcome semantics, workload, versions, and measurement boundary.
2. Recover the realized physical graph, partitions, attempts, and critical path.
3. Account work by resource and separate accepted, retry, speculative, and maintenance work.
4. Attribute movement by edge, boundary, locality tier, bytes, and attempt.
5. Inventory state by owner, distribution, size, lifetime, durability, and purpose.
6. Compare demands with usable capacities and compute only valid lower bounds.
7. Diagnose skew, queueing, backpressure, spill, and failure amplification.
8. Change one causal mechanism and predict which ledger entries should move.
9. Revalidate outputs, failure behavior, tails, capacity, and total cost.
10. Review operational and human consequences beyond runtime.

The following executable fixture calculates several ledger entries for a toy plan. Its stage seconds, CPU work, bandwidths, and state lifetimes are assumed inputs; the outputs are arithmetic, not a performance forecast.

<!-- bijux-verify: {"id":"work-movement-state-ledger","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"critical_path_seconds=23\ntotal_cpu_seconds=61\nwork_bound_4_slots=15.25\nmovement_bytes=600000000\nserial_movement_seconds=10.00\npeak_state_bytes=280000000 at_second=2\nfinish_times=('scan:4', 'map:7', 'shuffle_write:9', 'shuffle_read:14', 'aggregate:20', 'checkpoint:22', 'publish:23')\n","stderr":""}} -->
```python
stages = {
    "scan": {"seconds": 4, "parents": (), "tasks": 8, "cpu_each": 3},
    "map": {"seconds": 3, "parents": ("scan",), "tasks": 8, "cpu_each": 2},
    "shuffle_write": {
        "seconds": 2, "parents": ("map",), "tasks": 4, "cpu_each": 1
    },
    "shuffle_read": {
        "seconds": 5,
        "parents": ("shuffle_write",),
        "tasks": 4,
        "cpu_each": 2,
    },
    "aggregate": {
        "seconds": 6, "parents": ("shuffle_read",), "tasks": 4, "cpu_each": 2
    },
    "checkpoint": {
        "seconds": 2, "parents": ("aggregate",), "tasks": 1, "cpu_each": 1
    },
    "publish": {
        "seconds": 1, "parents": ("checkpoint",), "tasks": 1, "cpu_each": 0
    },
}

finish = {}
for name, stage in stages.items():
    start = max((finish[parent] for parent in stage["parents"]), default=0)
    finish[name] = start + stage["seconds"]

total_cpu = sum(stage["tasks"] * stage["cpu_each"] for stage in stages.values())
movements = (
    (400_000_000, 100_000_000),
    (160_000_000, 40_000_000),
    (40_000_000, 20_000_000),
)
movement_bytes = sum(byte_count for byte_count, _ in movements)
serial_move = sum(byte_count / bandwidth for byte_count, bandwidth in movements)

lifetimes = (
    ("mapped", 120_000_000, 0, 5),
    ("shuffle", 160_000_000, 2, 8),
    ("aggregate", 40_000_000, 5, 10),
    ("checkpoint", 40_000_000, 8, 12),
)
usage = {
    second: sum(
        size for _, size, start, end in lifetimes if start <= second < end
    )
    for second in range(13)
}
peak_second = max(usage, key=usage.get)

print(f"critical_path_seconds={finish['publish']}")
print(f"total_cpu_seconds={total_cpu}")
print(f"work_bound_4_slots={total_cpu / 4:.2f}")
print(f"movement_bytes={movement_bytes}")
print(f"serial_movement_seconds={serial_move:.2f}")
print(f"peak_state_bytes={usage[peak_second]} at_second={peak_second}")
print(f"finish_times={tuple(f'{name}:{finish[name]}' for name in stages)}")
```

The dependency schedule yields a 23-second span. Sixty-one CPU-seconds over four ideal slots gives 15.25 seconds, so the CPU-work bound is weaker in this assumed model. The three transfers total 600 MB and would take ten seconds if serialized at their isolated stated bandwidths; they are not automatically added to 23 because overlap and inclusion in stage durations are unspecified.

Half-open state lifetimes peak at second two, when the 120-MB mapped artifact and 160-MB shuffle artifact coexist. A real engine needs continuous timestamps, per-worker distributions, buffers, replicas, spills, and retained recovery copies. The fixture's exactness does not make its assumptions representative.

Proof obligations include result equivalence, graph/attempt completeness, dimensional consistency, non-overlap/double-counting checks, usable-capacity evidence, per-partition distributions, and causal experiment results. A resource ledger can be internally consistent and still omit the true bottleneck.

## Alternatives and Trade-Offs

Scale-up uses shared memory and fast local channels, reducing distributed overhead until one machine's capacity, availability, or administrative boundary is insufficient. Scale-out adds aggregate capacity and failure isolation while adding movement, coordination, skew, and cost. Compare both to a competent baseline.

Recompute avoids retained state but repeats work and movement. Cache reduces repeated latency at memory/consistency cost. Durable materialization reduces recovery cones at storage/write/cleanup cost. Select from reuse count, failure probability, recomputation cost, state size, and durability objective.

Move compute to data to reduce input transfer, or move data to specialized compute to gain faster processing. Placement competes with queue time, accelerator availability, rack balance, and future stages. Locality is one term in the objective.

Compression reduces wire/storage bytes but adds CPU, buffers, and latency. Faster codecs may yield larger output; higher compression may be counterproductive on CPU-bound work. Benchmark end-to-end with realistic batches and concurrency.

More partitions improve balance and concurrency but increase task, file, connection, and metadata overhead. Coalescing reduces overhead and can worsen tails. Adaptive partitioning uses runtime evidence but complicates reproducibility and state mappings.

Approximate algorithms, sampling, late-data limits, and degraded results can reduce work/state/latency, but change outcome semantics. They require explicit error bounds and domain approval, not presentation as infrastructure tuning.

Managed services reduce some operational work and expose price/limit/dependency trade-offs. Self-managed clusters offer control and can internalize fixed cost. Compare full boundary, reliability, lock-in, expertise, and opportunity cost.

## Failure Modes and Misconceptions

1. **More workers always make a job faster.** Serial span and bottlenecks remain.
2. **High scaling efficiency proves good performance.** A slow baseline can scale impressively.
3. **CPU-seconds equal wall seconds.** Concurrency and waits differ.
4. **Stage durations should all be summed.** Independent branches and resources overlap.
5. **Resource lower bounds predict runtime.** Queueing, skew, barriers, and overhead raise it.
6. **Nominal capacity is usable capacity.** Topology, tenancy, and protocols reduce it.
7. **Aggregate capacity serves one hot partition.** Per-task concurrency may be limited.
8. **All bytes have equal cost.** Boundary, locality, requests, and retries matter.
9. **Bytes read equal network bytes.** Reads can be local, cached, replicated, or retried.
10. **Compression is free movement reduction.** It consumes CPU, memory, and latency.
11. **State is only user records.** Buffers, indexes, shuffle, checkpoints, and metadata count.
12. **Aggregate state fit prevents OOM.** One worker/partition can exceed capacity.
13. **A cache is a durable checkpoint.** Failure survival and authority differ.
14. **More partitions only add parallelism.** They add scheduler and metadata work.
15. **Fusion is always beneficial.** It can couple backpressure and enlarge replay.
16. **Pre-aggregation always reduces cost.** Unique keys can add state without savings.
17. **Speculation reduces every tail.** Deterministic skew repeats work.
18. **Backpressure identifies the cause.** It often appears upstream of the bottleneck.
19. **Average task time explains completion.** The maximum required task gates the stage.
20. **Failed attempts are irrelevant overhead.** They consume real capacity and cost.
21. **Restarted streaming tasks are recovered.** Backlog may still grow.
22. **Optimization can ignore correctness.** Changed results invalidate comparison.
23. **One benchmark represents a workload.** Size, skew, concurrency, and failures vary.
24. **Lower monetary cost proves better design.** Reliability, labor, and consequence matter.
25. **Technical efficiency proves social value.** Domain outcomes need independent review.

## Worked Examples

### Example 1

**Question:** A job has 1,000 CPU-seconds and 100 usable cores. Can it finish in five seconds?

**Reasoning:** The CPU-work lower bound is ten seconds even before span and other resources.

**Conclusion:** The target is impossible under the stated capacity/demand.

### Example 2

**Question:** Two independent branches take 30 and 40 seconds, then a join takes 10. Is span 80 seconds?

**Reasoning:** The branches overlap, so span is `max(30,40)+10=50` under unlimited resources.

**Conclusion:** Sum along paths, not across the whole graph.

### Example 3

**Question:** CPU is 25% while shuffle fetch wait is high. Add cores?

**Reasoning:** The active constraint is likely movement/storage/network or skew, not aggregate CPU.

**Conclusion:** Inspect edge bytes, locality, cut capacity, and gating partitions first.

### Example 4

**Question:** Compression halves shuffle bytes but adds 40% CPU. Is it better?

**Reasoning:** It helps a movement-bound job with CPU headroom and may hurt a CPU-bound job. Measure end-to-end.

**Conclusion:** Optimization depends on the active bottleneck.

### Example 5

**Question:** Why measure byte-seconds as well as peak state?

**Reasoning:** Peak predicts capacity failure; byte-seconds captures occupancy/cost over time.

**Conclusion:** State size and lifetime answer different questions.

### Example 6

**Question:** One of 2,000 tasks takes 15 minutes while the median is 20 seconds. What gates completion?

**Reasoning:** The required maximum task on the critical stage, not median or average.

**Conclusion:** Diagnose that partition's data, work, movement, state, and attempts.

### Example 7

**Question:** A cache saves 100 CPU-hours per day but stores 20 TB continuously. Keep it?

**Reasoning:** Compare storage/replication/cleanup and invalidation cost with recomputation, latency, reliability, and reuse—not CPU alone.

**Conclusion:** Cross-resource exchange needs a common outcome/cost boundary.

### Example 8

**Question:** A stream processes 9,000 events/s while 10,000/s arrive. Is backpressure a fix?

**Reasoning:** No; backlog grows by 1,000/s. Backpressure controls queues but cannot create service capacity.

**Conclusion:** Raise sustainable capacity, reduce valid work, or govern input/degradation.

### Example 9

**Question:** Runtime fell 30% after dropping late events. Is that an engine optimization?

**Reasoning:** The result semantics changed. Evaluate correctness and domain acceptability before performance.

**Conclusion:** Hold outputs equivalent in optimization comparisons.

### Example 10

**Question:** Can a low-cost, low-latency model pipeline approve prioritization of disaster relief?

**Reasoning:** No. Eligibility, need, geography, timeliness, uncertainty, appeals/corrections, accessibility, bias, privacy, security, degraded operations, and harm from delay/exclusion require named emergency-management, relief-policy, field-operations, accessibility, privacy/security, data-governance, civil-rights/ethics, and independent assurance review. No external approval is claimed here.

**Conclusion:** Resource efficiency is not a public-interest decision rule.

## Cross-Program Connections

[Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies work/span, lower bounds, approximation, and benchmarking. [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies memory layout, hashing, sketches, external structures, and amortization. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies memory hierarchy, bandwidth, vectorization, and accelerators.

[Operating Systems](../../22-operating-systems/ROADMAP.md) owns CPU, memory, I/O, scheduling, and isolation. [Network Engineering](../../24-network-engineering/ROADMAP.md) owns topology, throughput, congestion, and transfer. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns usable cluster capacity, telemetry, quotas, and cost allocation.

[Data Engineering](../../19-data-engineering/ROADMAP.md) owns pipeline outcomes, quality, orchestration, and backfills. [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns data semantics, placement, lifecycle, and governance. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns coordination, consistency, progress, and recovery.

MapReduce, Dryad, and RDDs expose computation, movement, partition, and recovery trade-offs. Naiad exposes timely progress and retained state for iterative computation. The Dataflow model frames correctness, latency, and cost for unbounded data. COST supplies a disciplined scalability baseline. Spark and Flink expose task, shuffle, spill, state, and backpressure measurements; Google SRE connects latency, traffic, errors, and saturation to user-facing service behavior.

## References

- Jeffrey Dean and Sanjay Ghemawat, [*MapReduce: Simplified Data Processing on Large Clusters*](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/), OSDI, 2004. Primary computation, locality, shuffle, task, failure, and cluster-scale evaluation design.
- Michael Isard et al., [*Dryad: Distributed Data-Parallel Programs from Sequential Building Blocks*](https://www.microsoft.com/en-us/research/wp-content/uploads/2007/03/eurosys07.pdf), EuroSys, 2007. Primary vertex/channel graph and execution-resource model.
- Matei Zaharia et al., [*Resilient Distributed Datasets*](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf), NSDI, 2012. Primary lineage, partition, working-set, shuffle, and recovery trade-offs.
- Derek G. Murray et al., [*Naiad: A Timely Dataflow System*](https://www.microsoft.com/en-us/research/wp-content/uploads/2013/11/naiad_sosp2013.pdf), SOSP, 2013. Primary iterative dataflow, timestamps, progress, state, and performance design.
- Tyler Akidau et al., [*The Dataflow Model*](https://research.google/pubs/the-dataflow-model-a-practical-approach-to-balancing-correctness-latency-and-cost-in-massive-scale-unbounded-out-of-order-data-processing/), VLDB, 2015. Primary unbounded-data correctness, latency, and cost framework.
- Frank McSherry, Michael Isard, and Derek G. Murray, [*Scalability! But at what COST?*](https://www.usenix.org/system/files/conference/hotos15/hotos15-paper-mcsherry.pdf), HotOS, 2015. Primary competent-baseline and distributed-overhead critique.
- Apache Spark Project, [*Monitoring and Instrumentation*](https://spark.apache.org/docs/latest/monitoring), checked 2026-09-03. Official current task CPU/run time, serialization, GC, input/output, shuffle, spill, memory, attempt, and quantile metrics.
- Apache Spark Project, [*RDD Programming Guide: Shuffle Operations*](https://spark.apache.org/docs/latest/rdd-programming-guide#shuffle-operations), checked 2026-09-03. Official current shuffle redistribution, I/O, serialization, memory, spill, and intermediate-file behavior.
- Apache Flink Project, [*Metrics*](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/metrics/), checked 2026-09-03. Official current network, state, checkpoint, busy/idle/backpressure, and initialization metrics.
- Rob Ewaschuk, [*Monitoring Distributed Systems*](https://sre.google/sre-book/monitoring-distributed-systems/), Google SRE Book. Official latency, traffic, errors, saturation, tail, and cause-oriented monitoring guidance.

## Exercises

### Exercise 1

A DAG has branches `A=20s -> C=10s` and `B=35s -> C`, followed by `D=5s`. Compute span. With 800 CPU-seconds and 32 usable cores, compute the CPU-work bound and combined lower bound.

### Exercise 2

A shuffle transfers 12 TB logical bytes, 8 TB after compression, and 11 TB actual network bytes after retry. Compute compression and retry/movement amplification with clearly stated denominators, then list missing locality/cost evidence.

### Exercise 3

State objects are 500 GB live for two hours, a 200-GB checkpoint retained seven days, and four 50-GB replicas retained one day. Compute simple GB-hours and peak if all overlap; explain why this is insufficient for capacity.

### Exercise 4

Diagnose a job with low aggregate CPU, 90% tasks complete quickly, one rack's remote shuffle fetch wait high, several retries, and object-store throughput below global quota.

### Exercise 5

A public-health stream trades late-data completeness for faster outbreak indicators. Design the work/movement/state experiment and name semantic, operational, and independent review requirements.

## Answers to the Exercises

### Answer 1

`C` waits for both branches, so span is `max(20,35)+10+5=50` seconds. The CPU-work bound is `800/32=25` seconds. The combined simple lower bound is `max(50,25)=50` seconds, assuming the stage durations and CPU work/capacity model are compatible and not double-counted. Actual time can exceed 50 through queues, skew, transfer, startup, contention, or failures.

### Answer 2

Using logical/uncompressed bytes over compressed bytes, compression factor is `12/8=1.5`. Using actual network over compressed intended transfer, retry/path amplification is `11/8=1.375`; using actual over logical would be `11/12≈0.917`, which mixes compression and retry. State the chosen question. Missing evidence includes local versus remote bytes, rack/zone/region cuts, block/request counts, retransmission versus task retry, bandwidth/time distributions, compression CPU/state, topology, shared capacity, monetary egress/request charges, and whether all logical bytes were required.

### Answer 3

Working state contributes `500*2=1,000 GB-hours`; checkpoint contributes `200*7*24=33,600 GB-hours`; replicas contribute `4*50*24=4,800 GB-hours`, total 39,400 GB-hours. If all coexist, simple aggregate peak is `500+200+200=900 GB`. Capacity also needs per-worker/tier distribution, replication placement, encoding/metadata/temporary copies, growth and skew, billing units, cleanup delay, durability, simultaneous buffers/spill, and whether the intervals truly overlap.

### Answer 4

The rack-specific fetch wait and retries point to a topology/path or serving-shard constraint hidden by cluster aggregates. Map gating partitions and block sources to rack links, shuffle service and storage endpoints; compare local/remote bytes, requests, retransfers, queueing, errors, bandwidth, and usable per-cut capacity. Object-store global headroom does not exclude a per-prefix, endpoint, connection, rack, or request limit. Check whether retry load amplifies it and whether placement concentrated producers/consumers. Test a bounded placement/routing or concurrency change, validate output and failure behavior, and observe whether the bottleneck moves.

### Answer 5

Freeze event sources, time semantics, window/watermark/trigger policy, correction/retraction behavior, output equivalence/error bounds, and affected populations. Compare plans on identical captured inputs including late/out-of-order extremes; measure CPU/attempt work, local/remote movement, operator/window/timer/checkpoint state and byte-time, lag, completeness by delay/population, update count, sink effects, failure replay, catch-up, and cost. Validate deterministic replay and corrections, test overload/partition/checkpoint/sink failure, and retain graph/schema/config/data digests. Named review includes epidemiology, surveillance/public-health informatics, laboratories/reporters, field operations, statistics, accessibility/language access, privacy/security/governance, civil-rights/ethics, distributed-data/platform reliability, and independent public-health assurance. A faster incomplete indicator requires explicit domain approval; internal performance evidence is not external approval.
