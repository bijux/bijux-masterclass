---
module_id: LSDS-096
program: Large-Scale Data Systems Engineering
level: 2
module_number: 96
title: Skew Detection and Mitigation
status: complete
last_verified: 2026-09-04
---

# Skew Detection and Mitigation

## One-Page Review

### Governing question

How should an engineer identify whether unequal distributed-task performance comes from data volume, key frequency, computational cost, state, placement, or resources, then choose a semantics-preserving mitigation for the exact operator and skew type?

### Essential definitions

- **skew** is unequal load across logical partitions, keys, tasks, workers, or time windows under a relevant resource measure.
- A **heavy hitter** or **hot key** contributes a disproportionate share of records, bytes, work, state, or output.
- **partition skew** is imbalance after an assignment function maps work to partitions.
- **computational skew** occurs when equal-looking inputs require unequal CPU, I/O, expansion, or external-service work.
- **temporal skew** is a burst or hotness pattern that changes across windows or time.
- **resource skew** is unequal effective hardware, placement, contention, locality, or failure history rather than unequal logical data.
- **salting** adds a deterministic subkey to split one natural key across partial partitions.
- **two-level aggregation** combines salted partial accumulators and then merges them under the original key.
- **skew splitting** divides an oversized partition/range into smaller work units, sometimes replicating the other join side.
- A **sketch** is a bounded-memory approximate summary with stated error/confidence properties.
- **imbalance ratio** is a maximum or high quantile divided by a robust center such as the median, for one named metric/cohort.

### Central model, mechanism, or theorem

For key set $K$, per-key frequency $f_k$, per-record cost $c_k$, additional state/output cost $s_k$, and partition function $h$, define work:

$$w_k=f_kc_k+s_k,\qquad L_j=\sum_{k:h(k)=j}w_k.$$

With total work $W=\sum_k w_k$ and $P$ partitions, ideal mean load is $\mu=W/P$, but any indivisible key implies:

$$max_j L_j\ge max(\mu,\max_k w_k).$$

Therefore adding ordinary hash partitions cannot reduce a single indivisible hot key below its work. Splitting it into $q$ valid partial keys can lower its ideal partial contribution toward $w_{hot}/q$, but adds a second merge, shuffle/state, ordering, duplicate, and correctness obligations.

Detect skew from distributions and correlations across bytes, records, distinct keys, per-key counts, CPU, duration, memory, spill, state, network, retries, and output. Normalize work by bytes/records to distinguish volume skew from expensive records, and compare logical partitions across workers/retries to distinguish data from resource skew.

### Critical invariants

- Every input record contributes exactly as required after split, salt, replicate, combine, retry, and final merge.
- Natural-key equality, join multiplicity, null semantics, ordering, windowing, watermarks, and state ownership remain explicit.
- Partial aggregation is used only with a valid mergeable accumulator and documented associativity/commutativity/order requirements.
- Join-side replication is bounded, deduplicated by semantics, and legal for the specific inner/outer/semi/anti join direction.
- Salts are deterministic enough for retry/recovery, while their fan-out distribution avoids a new hot subkey.
- Approximate detection states error/confidence, never under/overestimate properties, and candidate-validation method.
- Metrics preserve task/partition/key/window/worker identity and expose distributions rather than averages alone.
- Adaptive split mappings, executed plans, thresholds, and replicated ranges are retained for replay and diagnosis.
- Mitigation is bounded by memory, network, scheduler, output-file, state, and downstream capacities.
- Sensitive literal keys are hashed/redacted in telemetry unless governed access explicitly permits disclosure.

### Common failures

Common failures include diagnosing from average task time; calling every straggler skew; measuring compressed bytes while CPU-heavy rows differ; increasing partitions for one hot key; random salting without an exact final merge; salting a nondecomposable operation; replicating the wrong outer-join side; using a tiny biased sample for range boundaries; logging protected keys; using top-record counts while state or output is the real load; confusing a slow worker with a hot partition; enabling speculation on deterministic skew; using a global fan-out for all keys; changing keyed-state serialization during rescale; declaring success when one stage improves but shuffle/files/cost explode; and hard-coding yesterday's hot keys as distributions drift.

### Compact example

Ten million equal-cost records across 200 partitions have an ideal mean of 50,000 records. One natural key owns 3.5 million records, imposing a load at least 70 times the mean under ordinary key hashing regardless of partition count. Deterministic 16-way salting yields an ideal hot partial of 218,750 records, 4.375 times the original mean, before other keys and variance. The final accumulator merge is correct for exact sum/count with a mergeable monoid; arbitrary ordered concatenation or a naive distinct count needs a different proof.

### Connections

[LSDS-039](039-skewed-keys-and-heavy-hitters.md) supplies heavy-key foundations, [LSDS-064](064-distributed-hash-and-merge-joins.md) supplies join semantics, [LSDS-065](065-partial-and-final-aggregation.md) supplies mergeable accumulators, [LSDS-068](068-adaptive-query-execution.md) supplies runtime splitting, [LSDS-091](091-partition-count-and-task-granularity.md) supplies partition constraints, and [LSDS-094](094-network-saturation.md) supplies fan-out costs.

## Governing Question

Skew is not one phenomenon. A partition can be large because of a hot key, poor range boundaries, many medium keys colliding, an unsplittable source, data expansion, or output multiplicity. It can run slowly because of CPU-heavy values, spill, remote locality, a noisy worker, dependency throttling, or repeated failures despite equal input bytes.

The governing question is how to classify the imbalance before acting, determine which work is divisible under the operator's semantics, and prove that the chosen transformation preserves results and recovery while improving the end-to-end tail.

## Why This Matters

Distributed stages complete at the tail. Most workers may become idle while one partition processes a hot customer, range, graph vertex, session, or join product. Autoscaling adds workers but cannot split an indivisible key. Speculation duplicates the same deterministic work and can worsen memory, network, and sink contention.

Skew also threatens reliability. Hot state can exceed memory/checkpoint budgets; skewed joins can produce combinatorial output; retries repeat large work; backpressure propagates from one key; and one writer produces a huge file while others produce tiny files. Effective mitigation changes the work decomposition, not only the resource count.

## Prerequisites and Retrieval

Review heavy hitters in [LSDS-039](039-skewed-keys-and-heavy-hitters.md), shuffle cost in [LSDS-040](040-reducing-network-and-disk-cost-in-a-wide-transformation.md), keyed state in [LSDS-043](043-stateful-operators.md), speculation in [LSDS-055](055-work-stealing-and-speculation.md), joins in [LSDS-064](064-distributed-hash-and-merge-joins.md), partial aggregation in [LSDS-065](065-partial-and-final-aggregation.md), adaptive execution in [LSDS-068](068-adaptive-query-execution.md), partition granularity in [LSDS-091](091-partition-count-and-task-granularity.md), and network saturation in [LSDS-094](094-network-saturation.md).

You should understand hash/range partitioning, frequency distributions, quantiles, robust centers, sampling, sketches, joins, monoids/mergeable accumulators, shuffle, state/key groups, windows/watermarks, retries/speculation, data locality, and experimental controls.

For diagnosis retain job/stage/operator/partition/key-bucket/window/attempt/worker IDs; input/shuffle/output bytes and records; distinct keys and key-frequency candidates; normalized CPU/I/O/decode/UDF/external-call work; duration; state; memory/spill/GC; locality/network; join build/probe/output multiplicity; retries/speculation; adaptive split/replication maps; source/range boundaries; resource profile; runtime/config/version; and percentile/cohort.

## Learning Objectives

After this module, you should be able to:

1. distinguish key, partition, computational, state, temporal, output, and resource skew;
2. derive mean-load and indivisible-hot-key lower bounds;
3. detect heavy hitters exactly, by sample, or by sketch with explicit guarantees;
4. interpret partition/task distributions and normalized work without hiding tails;
5. choose among repartitioning, range-boundary repair, salting, partial aggregation, join splitting, isolation, and resource changes;
6. prove aggregation and join correctness for a chosen split/replication direction;
7. preserve keyed-stream state, ordering, windows, timers, and recovery;
8. bound network, memory, scheduler, state, and output amplification;
9. validate adaptive and static mitigations with controlled failure-aware experiments; and
10. monitor drift and retire stale special handling.

## Core Exposition

### Define the load measure

Start by naming what is unequal: encoded bytes, decoded rows, CPU instructions/time, memory, spill, state, network, external calls, join matches, output, or duration. Different operators have different work functions. Record count can predict a simple sum but not regex parsing, decompression, graph degree, or join multiplicity.

Use several measures and correlate them. A large-byte partition with proportional time is volume skew; equal bytes with extreme CPU per row is computational skew; equal logical partitions that move with a worker indicate resource skew.

### Inspect distributions, not averages

Report p50, p90, p95, p99, maximum, coefficient/robust dispersion, and max-to-median for task input, work, state, spill, output, and duration. Keep zero/empty partitions visible. An average can look healthy while one task determines the stage.

Segment by operator and attempt. Whole-job task histograms mix scans, joins, and writes with different units. Compare the same logical partition across retries/workers to separate deterministic from environmental tails.

### Build key-frequency evidence

Exact counts are authoritative but may require the expensive shuffle being diagnosed. Candidate heavy hitters can come from source statistics, per-partition top-k summaries, stratified samples, or streaming sketches. Validate candidates with exact targeted counts when decisions are high impact.

A Count-Min sketch uses bounded memory and one-sided frequency estimates under its assumptions; collisions can overestimate. Its width/depth and hash independence encode error/confidence. It does not identify arbitrary unseen keys without a candidate mechanism.

### Separate key from partition skew

A partition can be hot because one key is indivisible or because many moderate keys collide. More hash partitions helps the latter probabilistically but not the former. A range partition can be hot because boundaries were learned from an unrepresentative sample or because one value itself dominates.

Compute per-key shares inside hot partitions. Preserve the mapping from key candidates to partition loads so a repartition decision has a causal basis.

### Normalize computational work

Compare CPU/elapsed time per input record/byte, output per input, state per key, spill per byte, and external-call latency per item. Robustly exclude setup where needed but retain it separately. Expensive malformed rows, variable decompression, UDF branches, and high-degree joins can create work skew without frequency skew.

Route pathological records to a bounded special path or repair the algorithm. Do not salt by record count if one record still contains the indivisible work.

### Repartition when work is divisible

If skew comes from coarse source splits or collisions among many keys, increase/rebalance partitions, split large files/ranges, or recompute range boundaries from representative samples. This adds shuffle/metadata and may affect ordering/locality.

Use stable boundaries and validate coverage. Repartitioning cannot divide a required group-by-key state unless the computation itself is decomposed.

### Salt mergeable aggregations

For a hot natural key $k$, derive deterministic salt $u$ in $[0,q)$ from a stable record/event identifier or balanced assignment, aggregate $(k,u)$ independently, then merge partial accumulators by $k$. Choose $q$ from observed work and resource budgets, not one global constant.

This is valid when the accumulator merge has the required algebraic properties. Exact sum/count/min/max and properly designed sketches are straightforward. Average needs sum and count. Exact distinct requires deduplicated sets/partitioning or a correct mergeable structure; averaging partial distinct counts is wrong.

### Split joins by semantic direction

Skewed joins can split a large partition/range on one side and replicate matching data from the other. Replication is safe only when output multiplicity, unmatched-row emission, null semantics, and join type are preserved. Full outer joins are especially resistant to naive splitting because both unmatched sides require global knowledge.

Estimate join output by heavy-key cross-products. A key with $a$ left and $b$ right rows produces $ab$ inner matches; no partitioning eliminates that required output. Sometimes pre-aggregation, existence/semi logic, deduplication, or business-rule filtering is the only real reduction.

### Use partial aggregation before exchange

Combiner lifting reduces repeated values per key before shuffle when the operation is associative and commutative as required. Hot-key fan-out adds an intermediate grouping and final merge; it can increase shuffle when upstream partial combination was already effective.

Measure accumulator size and merge cost. A “combine” whose accumulator is the full list does not remove skew.

### Handle streaming hot keys

Keyed state, timers, per-key ordering, and windows bind a natural key to one logical owner. Application-level sharding may split associative window aggregates, but ordering-sensitive sessionization, per-key sequence logic, or arbitrary state machines may not be decomposable.

Use bounded windows/TTL where semantics permit, hierarchical aggregation, separate service classes for known hot tenants, and explicit state migration. Preserve stable operator/key identities and checkpoint compatibility.

### Detect temporal skew

A key can be cold daily but hot for five minutes. Long aggregation windows hide bursts; instantaneous alerts may overreact to noise. Measure sliding windows at decision-relevant horizons and retain event-time versus processing-time distinctions.

Adaptive fan-out needs hysteresis and decay so partitions do not oscillate. Persist the executed policy and its effective interval for replay.

### Distinguish resource skew

If the same logical partition is normal on another worker, inspect CPU frequency, NUMA, memory pressure, disk, network locality, noisy neighbors, throttling, GC, and hardware health. Work stealing or speculation can help transient resource stragglers, but not deterministic hot keys.

Use replicated controlled tasks or retry comparisons carefully because caches and contention change. Quarantine defective nodes rather than rewriting data partitioning.

### Bound mitigation amplification

Salting adds intermediate keys/state and a final merge. Join splitting replicates a side. More partitions add scheduler/shuffle metadata. Broadcast multiplies bytes/memory across workers. Isolation can underutilize reserved capacity. Adaptive changes complicate replay and observability.

Budget bytes, blocks, connections, requests, state, memory, output files, attempts, and cost before rollout. Optimize end-to-end stage/job behavior, not only the former straggler.

### Use adaptive execution with evidence

Runtime engines can detect partitions above absolute and relative thresholds and split/coalesce them. Capture initial and executed plans, statistics, thresholds, parent-child mappings, replicated inputs, and fallback reasons. Version-specific support and join-type restrictions matter.

Adaptive relief cannot infer application-specific decomposability or repair an unavoidable output cross-product. Test failure/retry/replay with the executed mapping.

### Validate correctness and performance

Use a reference implementation and adversarial datasets: no skew, one dominant key, several medium hitters, collisions, null keys, empty partitions, bad range samples, hot windows, and expensive values. Compare multisets/order/state/output according to the contract.

Pin input/code/resources and run baseline versus candidates under cold/warm cache, retries, worker loss, and shared load. Report distributions, amplification, recovery, and cost with uncertainty.

### Observe continuously

Dashboard key/partition shares; input/shuffle/output bytes/records; distinct and top candidate keys; normalized CPU/I/O/state/spill/output; task duration; worker/resource/locality; join multiplicity; backpressure; retries/speculation; adaptive actions; fan-out; and cost.

Segment by job/stage/operator, logical partition/range, privacy-safe key bucket, window, attempt/worker/rack/zone, source/table partition, join side, runtime/config/version, input/load/failure cohort, percentile, and time horizon.

## Definitions and Notation

Let:

- $K$ be natural keys and $P$ partitions;
- $f_k$ be records/occurrences for key $k$;
- $c_k$ be average per-record work for key $k$ and $s_k$ additional state/output work;
- $w_k=f_kc_k+s_k$ be modeled key work;
- $h(k)$ assign key $k$ to partition $j$;
- $L_j=\sum_{k:h(k)=j}w_k$ be partition work;
- $W=\sum_k w_k$ and $\mu=W/P$ be total and ideal mean;
- $\rho=max_jL_j/median_j(L_j)$ be one robust imbalance ratio when the median is positive;
- $p_k=f_k/\sum_i f_i$ be key record share;
- $q_k$ be chosen fan-out for key $k$; and
- $A_n,A_b,A_s$ be network-byte, block/task, and state amplification from mitigation.

Frequency is only a proxy when $c_k$ or $s_k$ varies. Median ratios are undefined or misleading with many empty partitions; report the distribution and absolute threshold. Approximate summaries require error/confidence and candidate-recovery details.

## Mechanisms, Invariants, or Proof Structure

### Indivisible-key lower bound

Ordinary key partitioning assigns all work $w_k$ for one natural key to one partition. Therefore the maximum partition load is at least the largest $w_k$ and at least mean $W/P$. Increasing $P$ reduces the mean but cannot reduce that key's bound.

### Two-level aggregation proof

Map each input exactly once to $(k,u)$, compute partial accumulator $a_{k,u}$, and merge all salts using the same valid associative accumulator operation. The union of salted subsets equals the natural-key input, so the final extracted result matches the unsalted reference under its algebraic contract.

### Join-splitting proof obligation

Define which side is split and replicated, enumerate every matching pair exactly once, and emit unmatched rows exactly once for the join type. A parent-child partition map plus side/version identity supports retry and one-winner output.

### Diagnostic discrimination

If high work follows the logical partition across workers, data/computation is supported; if it follows the worker across partitions, resource skew is supported. Correlating key shares, normalized work, and output multiplicity distinguishes frequency, per-record cost, and result explosion.

### Adversarial verification

Test no skew, one 35%/near-100% key, many medium keys, hash collisions, inaccurate sketches/samples, null keys, giant records, bad range boundaries, join cross-products and every join type, nonmergeable/ordered operations, temporal bursts, hot keyed state/timers, resource stragglers, retry/speculation, adaptive fallback, network/memory limits, and privacy-safe telemetry.

## Alternatives and Trade-Offs

| Lever | Strength | Cost or limitation |
|---|---|---|
| More hash partitions | Helps many-key collisions and coarse work | Cannot split one natural hot key |
| Better range boundaries | Balances ordered divisible ranges | Sampling cost/drift; duplicate values remain hot |
| Salting plus final merge | Splits mergeable hot-key aggregation | Extra shuffle/state and algebraic requirements |
| Join partition splitting | Reduces skewed join tails | Replication and join-type correctness constraints |
| Broadcast small side | Avoids repartitioning one side | Replicated memory/network and size limits |
| Pre-aggregation | Reduces values before exchange | Only valid for mergeable semantics |
| Isolate hot keys/records | Tailored resources and algorithms | Special-path complexity and capacity fragmentation |
| Adaptive execution | Uses runtime distributions | Version/threshold/support and replay complexity |
| Speculation/work stealing | Helps transient resource stragglers | Duplicates deterministic skew and resource demand |
| More/larger workers | May fit indivisible work | Cost; no change to serial lower bound/output explosion |

## Failure Modes and Misconceptions

1. **Average task time is healthy.** One maximum can determine the stage.
2. **Every straggler is skew.** Resource, locality, failure, or dependency effects may dominate.
3. **Record counts measure work.** Bytes, CPU, state, and output can differ per record.
4. **More partitions split a hot key.** Ordinary hashing keeps one key together.
5. **Random salting is automatically correct.** Coverage and final merge must be proven.
6. **Every aggregation is decomposable.** Order-sensitive or full-list operations may not merge.
7. **Partial distinct counts can be summed.** Cross-partial duplicates make that incorrect.
8. **Any join side may be replicated.** Outer/semi/anti unmatched semantics constrain direction.
9. **Splitting removes join explosion.** Required $ab$ matching pairs still exist.
10. **One sample finds all hot keys.** Rare windows and biased ranges can be missed.
11. **Sketch estimates are exact.** State error direction/confidence and verify candidates.
12. **Speculation fixes deterministic skew.** It duplicates the same work and traffic.
13. **Autoscaling fixes keyed state.** An indivisible key remains one logical owner.
14. **One fan-out fits every key.** It over-amplifies cold keys and may undersplit the hottest.
15. **A balanced stage proves success.** Network, merge, state, files, recovery, and cost may regress.

## Worked Examples

### Example 1

Ten million records over 200 partitions have an ideal mean of 50,000 records per partition.

### Example 2

A 3.5-million-record natural key imposes at least 70 times that mean under ordinary key hashing.

### Example 3

Sixteen deterministic salts reduce the ideal hot partial to 218,750 records, 4.375 times the original mean before variance.

### Example 4

Two equal-byte partitions take 20 seconds and 400 seconds because one invokes an expensive parser branch; this is computational skew.

### Example 5

The same partition is slow on three workers, supporting data/work skew; many partitions slow only on one worker, supporting resource skew.

### Example 6

A join key with 100,000 left and 20,000 right rows implies two billion matching pairs unless semantics reduce the inputs.

### Example 7

An average is combined safely as partial sum/count pairs, not as an unweighted average of partial averages.

### Example 8

A Count-Min candidate is verified by exact targeted counting before allocating a costly special join path.

### Example 9

A five-minute hot-tenant burst triggers fan-out with hysteresis, then decays without changing event-time window ownership.

### Example 10

The executable fixture computes the indivisible bound and ideal salted partial for the compact example.

<!-- bijux-verify: {"id":"skew-lower-bound","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"records=10000000\npartitions=200\nideal_mean=50000\nhot_key_records=3500000\nhot_share=35.0%\nindivisible_ratio=70.0\nsalt_fanout=16\nideal_hot_partial=218750\nsalted_ratio=4.375\n","stderr":""}} -->
```python
records = 10_000_000
partitions = 200
hot_key_records = 3_500_000
salt_fanout = 16

ideal_mean = records / partitions
indivisible_ratio = hot_key_records / ideal_mean
ideal_hot_partial = hot_key_records / salt_fanout
salted_ratio = ideal_hot_partial / ideal_mean

print(f"records={records}")
print(f"partitions={partitions}")
print(f"ideal_mean={ideal_mean:.0f}")
print(f"hot_key_records={hot_key_records}")
print(f"hot_share={100 * hot_key_records / records:.1f}%")
print(f"indivisible_ratio={indivisible_ratio:.1f}")
print(f"salt_fanout={salt_fanout}")
print(f"ideal_hot_partial={ideal_hot_partial:.0f}")
print(f"salted_ratio={salted_ratio:.3f}")
```

## Cross-Program Connections

- **Algorithms:** heavy hitters, sketches, sampling, hashing, balls-into-bins, range partitioning, and approximation provide detection tools.
- **Algebra:** monoids, associativity, commutativity, idempotence, and numerical stability determine valid partial aggregation.
- **Statistics:** quantiles, robust centers, normalized work, sampling bias, confidence, and drift prevent average-based diagnosis.
- **Query engines:** joins, aggregations, exchanges, adaptive plans, broadcasts, ranges, and spill determine divisibility and amplification.
- **Streaming:** keyed state, windows, timers, watermarks, per-key order, TTL, and rescaling constrain hot-key mitigation.
- **Distributed systems:** retries, speculation, placement, worker heterogeneity, one-winner output, and recovery distinguish logical from resource skew.
- **Security and privacy:** literal hot keys can identify customers or protected values and require redaction, hashing, access control, and retention policy.
- **Economics:** extra shuffle, replicas, state, workers, special paths, output files, and longer tails determine the real benefit.

## References

1. Apache Spark, [SQL Performance Tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html). Current. Documents adaptive skew-join detection, splitting, replication, thresholds, and costs.
2. Apache Spark, [Tuning](https://spark.apache.org/docs/latest/tuning.html). Current. Covers reduce-task working sets, shuffle operators, parallelism, and memory symptoms.
3. Apache Spark, [Monitoring and Instrumentation](https://spark.apache.org/docs/latest/monitoring.html). Current. Documents per-task/stage input, shuffle, spill, memory, locality, duration, and executor evidence.
4. Apache Flink, [Adaptive Batch Execution](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/adaptive_batch/). Current. Documents skewed join splitting, factor/threshold behavior, join-side restrictions, and limitations.
5. Apache Flink, [Metrics](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/metrics/). Current. Documents task/operator bytes, records, state, backpressure, busy/idle, and resource metrics.
6. Apache Flink, [Data Skew in Batch SQL](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/tuning/#data-skew). Current. Documents skew diagnosis and query-level mitigation patterns.
7. Apache Beam, [Basics: Aggregation](https://beam.apache.org/documentation/basics/#aggregation). Current. Explains keyed grouping, mergeable combines, supplementary keys, and hierarchical aggregation.
8. Apache Beam, [Combine](https://beam.apache.org/documentation/transforms/java/aggregation/combine/). Current. Documents associative/commutative partial combining and single-worker grouping implications.
9. Google Cloud Dataflow, [Troubleshoot Bottlenecks](https://cloud.google.com/dataflow/docs/guides/troubleshoot-bottlenecks). Current. Documents hot/insufficient keys, serial per-sharding-key work, uneven workers, and redistribution.
10. Google Cloud Dataflow, [Common Errors: Hot Keys](https://cloud.google.com/dataflow/docs/guides/common-errors#a_hot_key_was_detected). Current. Documents hot-key detection, rekeying, fan-out, and shuffle mitigations.
11. Graham Cormode and S. Muthukrishnan, [An Improved Data Stream Summary: The Count-Min Sketch and its Applications](https://doi.org/10.1016/j.jalgor.2003.12.001). Primary paper. Defines Count-Min structure, update/query behavior, and approximation guarantees.
12. Apache Iceberg, [Spark Writes](https://iceberg.apache.org/docs/latest/spark-writes/). Current. Documents distribution modes, range sampling, partition/task/file-size interactions, and advisory sizing.
13. Apache Kafka, [Consumer Configuration](https://kafka.apache.org/42/configuration/consumer-configs/). Version 4.2. Documents partition assignment/fetch controls relevant to source partition imbalance.

## Exercises

### Exercise 1

Derive the indivisible-key lower bound for 2 billion equal-cost records, 1,000 partitions, and one 120-million-record key; then estimate ideal hot partial size under 24-way salting.

### Exercise 2

Diagnose a stage where p99 input bytes are 1.1 times median, p99 CPU time is 18 times median, and slow logical partitions remain slow across workers.

### Exercise 3

Design exact salting for per-customer average and exact distinct device count, stating accumulator and merge requirements.

### Exercise 4

Design a skewed left-outer join split, including which side may be divided/replicated and how unmatched left rows are emitted exactly once.

### Exercise 5

Design an experiment comparing more partitions, hot-key salting, adaptive join splitting, and a hot-key isolation path under worker loss and network limits.

## Answers to the Exercises

### Answer 1

The ideal mean is $2,000,000,000/1,000=2,000,000$ records. The hot key alone is 60 times the mean, so ordinary key hashing has maximum load at least 120 million regardless of more partitions. With 24 balanced deterministic salts, ideal hot partial size is 5 million records, 2.5 times the original mean before other keys and variance. Budget the final merge and choose fan-out from the actual per-record/state cost.

### Answer 2

Nearly balanced bytes with 18-times CPU tails supports computational rather than volume skew, and persistence across workers weakens a resource-skew hypothesis. Compare records, decoded expansion, value/type/path distributions, UDF/parser profiles, external calls, join output, state, spill/GC, and CPU per record/byte for hot partitions. Identify expensive values or output explosion, then use a better algorithm, preprocessing, bounded special path, or valid work subdivision; adding ordinary hash partitions may not split the costly record/key.

### Answer 3

For average, salt each record deterministically and accumulate `(sum, count)` per `(customer, salt)`; merge by component-wise addition under customer and compute sum/count once. For exact distinct devices, partial counts cannot be summed. Either partition each `(customer, device)` deterministically so duplicates meet before a final customer count, or merge exact device sets with a memory budget; an approximate mergeable distinct sketch changes the contract and needs an error guarantee. Prove one-record coverage, retry stability, numeric behavior, and bounded state.

### Answer 4

Split the matched work for the large left partition into disjoint child ranges/salts and replicate the necessary matching right subset to those children. Every matching pair must appear once. Because this is left outer, determine unmatched left rows within their owning child and emit each once; never replicate left rows across children without ownership/fencing. Track parent-child mapping, right-side version, null-key semantics, checksums, attempts, and one-winner output. Validate against a reference multiset with no/one/many matches, nulls, duplicates, and retries.

### Answer 5

Pin input, hot-key distribution, code, resources, and cache. Compare full task/key/work distributions, stage/job latency, CPU/memory/spill, shuffle bytes/blocks/connections, state, output files, retries, and cost. More partitions should help collision/coarse-partition skew but not the indivisible key. Salting must pass accumulator equivalence. Adaptive joins must record splits/replication and join-type correctness. Isolation needs reserved capacity and reintegration. Kill a worker during hot work and enforce network envelopes to expose duplicate/recovery amplification before choosing the lowest-cost correct tail.
