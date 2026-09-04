---
module_id: LSDS-097
program: Large-Scale Data Systems Engineering
level: 2
module_number: 97
title: Cluster Benchmarking
status: complete
last_verified: 2026-09-04
---

# Cluster Benchmarking

## One-Page Review

### Governing question

How should an engineer design, execute, and interpret a distributed-data benchmark so that its workload is relevant, its systems are comparable, its measurements are reproducible, its outputs are correct, and its conclusions remain valid under scale, contention, failure, and cost constraints?

### Essential definitions

- A **benchmark contract** fixes the question, workload, system boundary, metric, constraints, and validity rules before results are observed.
- A **system under test (SUT)** includes every component whose resources or behavior contribute to the reported result.
- A **workload model** specifies inputs, operations, arrival process, concurrency, data distribution, locality, state, and correctness oracle.
- A **load generator** creates offered work and must not become the hidden bottleneck.
- **open-loop load** schedules arrivals independently of completions; **closed-loop load** waits for responses before issuing more work.
- **warm-up** is controlled activity before the measurement interval to reach a named cache, code, state, allocation, or autoscaling condition.
- **steady state** is a bounded interval whose workload and relevant resource processes satisfy stated stability criteria.
- **throughput** is accepted, correct completed work per unit time, not merely submitted or attempted work.
- **service demand** is resource busy time per completed unit of work for a named resource and workload class.
- **coordinated omission** occurs when a blocked load generator fails to record requests that should have arrived during a stall.
- A **paired comparison** runs baseline and candidate under matched blocks such as input, cluster, time, and trial order.
- A **full disclosure record** preserves configuration, data, code, environment, procedure, raw measurements, exclusions, and calculation logic.

### Central model, mechanism, or theorem

For run duration $T$, correct completed work $C$, and offered work $A$, define:

$$X=C/T,\qquad g=C/A,\qquad D_r=B_r/C,$$

where $X$ is useful throughput, $g$ is completion-goodput ratio, $B_r$ is busy time at resource $r$, and $D_r$ is measured service demand. When one capacity unit of resource $r$ has utilization $U_r=B_r/T$, the utilization law gives $U_r=XD_r$ under consistent boundaries.

For a streaming system with accepted input rate $\lambda(t)$ and correct output rate $x(t)$, backlog changes as:

$$Q(t_1)-Q(t_0)=\int_{t_0}^{t_1}(\lambda(t)-x(t))dt.$$

Thus a short run can report high input acceptance while backlog grows. Sustainable throughput requires bounded backlog, latency, errors, state, and resource use over a declared interval, including any required recovery and maintenance work.

Compare paired trial outcomes with explicit direction. If smaller elapsed time is better, paired improvement can be represented by $d_i=\log(T_{base,i}/T_{cand,i})$; report the estimate, interval, raw pairs, and practical threshold rather than one best run.

### Critical invariants

- Baseline and candidate execute the same semantic work and pass the same correctness oracle.
- The measured interval, warm-up, teardown, retries, failures, and excluded time are explicit.
- Data scale, shape, skew, compression, partitioning, freshness, and cache state are controlled or disclosed.
- Hardware, topology, quotas, software, configuration, placement, and background load are pinned or measured.
- Offered, accepted, attempted, retried, failed, and correct completed work remain separate.
- Load generation, telemetry, validation, and sinks have measured headroom and cannot silently cap the SUT.
- Batch completion includes all required materialization/commit work; streaming stability includes backlog and event-time latency.
- Trial order is randomized or blocked, repetitions are independent enough for the stated analysis, and exclusions are predetermined.
- Percentiles are computed from mergeable distributions or raw observations, never by averaging worker percentiles.
- Cost, energy, recovery, maintenance, and resource amplification use the same boundary as the performance claim.

### Common failures

Common failures include choosing a famous benchmark unrelated to production; changing data and cluster size together; reporting submitted instead of completed work; accepting wrong results faster; timing only a lazy query submission; excluding load, checkpoint, compaction, or commit time without saying so; warming only one candidate; benchmarking through an undersized client; comparing different regions, quotas, versions, or storage states; keeping only the fastest run; averaging percentiles; hiding timeouts; using a closed loop to claim open-loop tail behavior; ending a stream test while backlog grows; tuning specifically to query identities; changing several factors without isolation; and publishing a ratio without raw measurements, uncertainty, or full configuration.

### Compact example

A baseline completes a fixed 12-billion-record suite in paired elapsed times of 1,220, 1,180, 1,205, 1,195, and 1,210 seconds. A candidate records 990, 970, 1,005, 985, and 980 seconds under the same randomized blocks and passes an exact result digest. Mean elapsed time falls from 1,202 to 986 seconds, an elapsed-time speedup of about 1.219. Useful throughput rises from about 9.98 to 12.17 million records/s. The comparison still requires latency/resource distributions, trial uncertainty, generator headroom, cache state, cost, and recovery evidence before a production claim.

### Connections

[LSDS-005](005-distributed-task-graphs.md) defines execution boundaries, [LSDS-049](049-backpressure-across-operators.md) supplies overload mechanics, [LSDS-090](090-designing-recovery-for-multi-hour-and-multi-day-jobs.md) identifies recovery work, [LSDS-091](091-partition-count-and-task-granularity.md) controls task shape, [LSDS-096](096-skew-detection-and-mitigation.md) supplies distribution diagnostics, and LSDS-098 will turn measured demands into forecasts.

## Governing Question

A benchmark is an experiment, not a race. “Which cluster is faster?” is incomplete until faster is defined for a particular semantic workload, scale, arrival pattern, completion boundary, reliability requirement, resource envelope, and cost horizon.

The governing question is how to construct evidence that isolates meaningful causal differences while preserving real operating constraints. A defensible answer must say what was held constant, what changed, what was measured, what uncertainty remains, and where the result does not generalize.

## Why This Matters

Cluster changes are expensive and often irreversible in practice. An engine upgrade, instance family, storage layout, serializer, scheduler, or partition policy may improve one synthetic kernel while regressing joins, state recovery, tail latency, or cost. A weak benchmark converts measurement noise and hidden boundary choices into architecture decisions.

Distributed systems make experimental control difficult. Placement changes locality; caches persist; autoscalers lag; noisy neighbors appear; failures trigger retries; cloud capacity and quotas vary; and monitoring itself consumes resources. Correct benchmarking makes those influences visible rather than pretending they do not exist.

## Prerequisites and Retrieval

Review execution boundaries in [LSDS-005](005-distributed-task-graphs.md), representative distributions in [LSDS-039](039-skewed-keys-and-heavy-hitters.md), backpressure in [LSDS-049](049-backpressure-across-operators.md), failure/retry behavior in [LSDS-081](081-task-level-failure-recovery.md), isolation in [LSDS-088](088-backfill-isolation.md), long-running recovery in [LSDS-090](090-designing-recovery-for-multi-hour-and-multi-day-jobs.md), and skew in [LSDS-096](096-skew-detection-and-mitigation.md).

You should understand batch and streaming execution, rates and latency distributions, resource utilization, queues, caching, statistical sampling, confidence intervals, experimental blocking/randomization, retries, checkpoints, storage consistency, cost accounting, and semantic output validation.

For every trial retain run/suite/workload IDs; immutable code, dependency, runtime, OS/image, firmware, configuration, and infrastructure identities; topology/placement; source and generated-data digests; query/pipeline plan; scale and distribution; warm-up and measured timestamps; offered/accepted/completed/error/retry counts; output digest; latency histograms; stage/task/resource metrics; autoscaling/failure events; costs; exclusions; and raw logs.

## Learning Objectives

After this module, you should be able to:

1. translate a decision into a benchmark contract and system boundary;
2. choose representative micro, component, application, and standard workloads;
3. control data scale, shape, state, cache, topology, versions, and background load;
4. distinguish open-loop from closed-loop load and detect coordinated omission;
5. define batch completion and streaming sustainable throughput correctly;
6. validate semantic output before interpreting performance;
7. use blocking, randomization, repetition, raw distributions, and uncertainty;
8. diagnose load-generator, telemetry, storage, network, scheduler, and sink bottlenecks;
9. include failure, recovery, cost, energy, and maintenance when the decision requires them; and
10. publish reproducible evidence with explicit validity limits.

## Core Exposition

### Start with the decision

Write the decision first: choose an instance family, approve a runtime upgrade, size a shared cluster, or detect regression. Name the primary metric, guardrails, target workload population, practical improvement threshold, and decision deadline.

One benchmark rarely answers every question. A regression gate favors stability and short duration; procurement needs representative scale and price; capacity planning needs service demands and saturation curves; a release investigation needs diagnostic detail.

### Define the system boundary

Draw the path from input generation through ingest, storage, compute, network, coordination, output validation, and durable commit. State whether provisioning, data generation, cache fill, compilation, autoscaling, checkpointing, compaction, and teardown are inside timing and cost.

Measure excluded components anyway when they can throttle the result. A remote generator or sink outside the price boundary can still cap throughput.

### Build a workload portfolio

Use microbenchmarks to isolate CPU, serialization, shuffle, storage, state, or network mechanisms. Use component benchmarks for an engine/operator family. Use application traces or replays for relevance. Use standards for shared rules and external comparison.

Triangulate. A scan kernel explains bandwidth; a join/aggregation suite exposes exchange and skew; a streaming suite exposes event time, windows, and state. Do not infer whole-platform value from one friendly kernel.

### Preserve semantic equivalence

Freeze logical operations and an output oracle. Compare exact multisets, ordered results, aggregates with numeric tolerances, state snapshots, or independent reference answers as appropriate. Include nulls, duplicates, late data, retries, and empty inputs.

Engine-specific rewrites are acceptable only if they preserve the contract. Faster wrong output, dropped late events, or weakened durability is not performance.

### Control input data

Record logical and physical size, row count, schema, cardinality, skew, correlations, ordering, compression, encodings, file sizes, partitions, update history, and source locality. A nominal “1 TB” dataset can impose radically different work across encodings and layouts.

Generate data deterministically with seed and tool version, then digest it. Production samples require privacy controls and stable snapshots. Test both representative and adversarial shapes.

### Pin the environment

Capture nodes, CPU/memory/storage/network, topology, placement, power/frequency policy, OS/image, JVM/runtime, engine, connector, dependencies, configuration, quotas, and autoscaling bounds. Record firmware and managed-service versions when exposed.

Dedicated clusters reduce interference but may reduce realism. Shared clusters require measured background load and blocked comparisons. Never assume two cloud allocations are identical because their SKU names match.

### Separate warm-up from measurement

Warm-up can populate filesystem/object caches, JIT code, connection pools, metadata, shuffle services, state, and autoscaling. Define a warm state relevant to production and apply it symmetrically.

Cold-start performance is a separate workload, not an inconvenient first sample to discard. Predetermine warm-up length or stability criteria; retain warm-up traces to detect drift.

### Generate load without hiding stalls

Closed-loop clients model finite users and naturally reduce offered load when latency rises. Open-loop clients model scheduled arrivals and reveal queueing at a fixed rate. Choose the model from reality.

Timestamp intended and actual send time, admission, start, completion, and correctness. If a generator blocks during a stall and records no missing arrivals, its latency distribution suffers coordinated omission. Validate generator CPU, network, connections, clocks, and queue headroom.

### Define completion and goodput

For batch, completion may require all tasks, durable output commit, catalog publication, validation, and cleanup. For streaming, accepted input is not output. Measure event-time and processing latency, correct output rate, backlog, watermark lag, state/checkpoints, and sink durability.

Keep attempts and useful completions distinct. Retries and speculative losers consume resources but do not increase goodput.

### Find sustainable throughput

Sweep offered rate or concurrency through underload, knee, and overload. Hold each point long enough to observe autoscaling, garbage collection, checkpoints, compaction, thermal behavior, quotas, and backlog trends.

Define sustainability as meeting latency/error/backlog/resource/recovery guardrails for a duration. A burst peak and a stable capacity are different products.

### Measure distributions and resource demand

Retain request/event latency histograms and per-stage/task/partition distributions. Report percentiles, maxima, failures, timeouts, and censored work. Aggregate histogram buckets or raw observations; do not average percentiles.

Measure CPU, memory, GC, state, storage bytes/requests, network, shuffle, spill, queues, utilization, throttles, and cost. Service demand $D_r=B_r/C$ helps reveal whether an improvement reduced work or merely added capacity.

### Design fair comparisons

Change one intended factor at a time where possible. Block baseline and candidate by cluster allocation, dataset, time window, and load point; randomize or alternate order to reduce drift and cache bias. Rebuild both from automation.

When several factors must move together, call the result a configuration comparison, not attribution to one factor. Match semantics and constraints even when low-level knobs differ.

### Repeat and quantify uncertainty

Run enough independent blocks to estimate variation at the decision-relevant level. Publish raw pairs, center, spread, interval method, sample size, exclusions, and practical threshold. For autocorrelated time series, a million events inside one run are not a million independent cluster trials.

Use paired differences when trials share a block. Avoid selecting the best run. Investigate outliers using predetermined rules; report analyses with and without exclusions when they matter.

### Benchmark failure and recovery

Inject worker loss, coordinator restart, network impairment, storage throttling, and sink ambiguity within safe isolated environments. Measure lost/duplicate output, recovery time, recomputation, backlog catch-up, resource burst, and post-recovery correctness.

Include failure only if the contract defines injection timing and success criteria. Chaos without controlled exposure is not a comparable benchmark.

### Account for cost and externalities

Use billed or amortized cost over the same boundary and interval: compute, storage, requests, network, licenses, reserved idle capacity, setup, recovery, and required maintenance. Report useful work per cost alongside performance.

If energy or carbon matters, specify meter boundary, sampling, location/time accounting, embodied scope, and uncertainty. Do not divide a full-system cost by a partial-work throughput.

### Publish a reproducibility bundle

Preserve the harness, workload definition, generators, seeds, data digests, manifests, infrastructure/configuration, raw observations, validation outputs, calculation code, and environment inventory. Make every plotted point traceable to run IDs.

State internal versus standards-compliant status. TPC-like queries are not a compliant TPC result without the specification's complete rules, audit, disclosure, and fair-use obligations.

## Definitions and Notation

Let:

- $A$ be offered work, $I$ accepted work, and $C$ correct completed work;
- $T$ be the declared measured interval;
- $\lambda=A/T$ be offered rate and $X=C/T$ useful throughput;
- $g=C/A$ be the completion-goodput ratio when boundaries align;
- $L_e$ be event-time end-to-end latency and $L_p$ processing latency;
- $Q(t)$ be queued/backlogged work at time $t$;
- $B_r$ be busy time and $U_r=B_r/T$ utilization for resource $r$;
- $D_r=B_r/C$ be measured resource service demand per correct completion;
- $K$ be cost over the same run boundary and $E=C/K$ useful work per cost;
- $T_{b,i},T_{c,i}$ be baseline/candidate elapsed times in paired block $i$; and
- $d_i=\log(T_{b,i}/T_{c,i})$ be positive log-improvement when lower time is better.

Counts need explicit units: records, bytes, queries, windows, or jobs. Utilization law requires consistent population, resource, and time boundaries. A confidence interval's interpretation depends on sampling/design assumptions and does not make a biased workload representative.

## Mechanisms, Invariants, or Proof Structure

### Conservation and backlog

Over an interval, final backlog equals initial backlog plus accepted input minus completed/removed work, adjusted for explicitly classified loss or expiry. Therefore accepted rate alone cannot demonstrate sustainable output. Stable operation requires backlog and latency distributions not to drift beyond the contract.

### Utilization-law cross-check

Because $B_r=U_rT$ and $C=XT$, $D_r=B_r/C=U_r/X$, hence $U_r=XD_r$. Use this identity as an accounting check. It does not prove causality when resource capacity, work mix, or boundaries change.

### Paired comparison

Within each matched block, compute a directionally consistent difference or log ratio. Blocking cancels some shared environmental variation; randomized order reduces systematic drift. The inference applies to the sampled block population, not every possible cluster condition.

### Correctness gate

Performance metrics become eligible only after schema, counts, checksums/digests, invariants, numeric tolerance, ordering/window semantics, and durability checks pass. Failed or censored trials stay visible and cannot silently disappear from the denominator.

### Reproducibility chain

A result is traceable when immutable source/config/data/environment identities determine a run manifest, which names raw observations and validation outputs, which deterministically produce published aggregates. Any manual mutation breaks the chain and must be disclosed.

## Alternatives and Trade-Offs

| Design | Strength | Cost or limitation |
|---|---|---|
| Microbenchmark | Isolates one mechanism quickly | Weak application generalization |
| Standard suite | Shared workload and rules | May not represent local data or operations |
| Production replay | High behavioral relevance | Privacy, drift, and reproducibility challenges |
| Synthetic generator | Controlled scale and adversarial shapes | Generator model may miss correlations |
| Closed-loop load | Models finite interactive clients | Offered rate falls during stalls |
| Open-loop load | Exposes queueing at scheduled arrivals | Requires generator headroom and omission-safe timing |
| Dedicated cluster | Lower interference and cleaner attribution | May not represent shared production contention |
| Shared cluster | Exercises realistic contention | Harder control and wider uncertainty |
| Cold trials | Measures startup and cache miss | Expensive and sensitive to provisioning variance |
| Warm steady-state trials | Measures sustained service | Can hide startup, rebuild, and recovery costs |

## Failure Modes and Misconceptions

1. **A standard query set is automatically a standard result.** Compliance includes all rules and disclosures.
2. **One number describes the cluster.** Workload, scale, latency, reliability, and cost are multidimensional.
3. **Submitted work equals throughput.** Only correct completed work belongs in goodput.
4. **The driver is outside the SUT, so it need not be measured.** It can cap or distort offered load.
5. **The first run is an outlier.** It may be the cold-start workload users actually experience.
6. **Warm cache is fair if both labels say warm.** Cache contents and warm-up procedure must match.
7. **Fastest-of-five removes noise.** It selects favorable noise and biases the result.
8. **Millions of events imply a huge sample size.** Cluster trials can remain strongly correlated.
9. **Average latency captures user experience.** Tails, timeouts, and omitted arrivals matter.
10. **Worker p99 values can be averaged.** Quantiles generally require raw/mergeable distributions.
11. **High accepted streaming rate is sustainable.** Backlog and watermark lag may be growing.
12. **Equal node count means equal resources.** SKUs, frequency, topology, storage, and quotas differ.
13. **Changing engine and format attributes speedup to the engine.** It is a bundle comparison.
14. **Correct row count proves correctness.** Values, multiplicity, windows, ordering, and durability may differ.
15. **Lower elapsed time means lower cost.** Parallelism, requests, network, licenses, and idle capacity can rise.

## Worked Examples

### Example 1

Twelve billion correct records completed in 1,202 seconds yield about 9.98 million records/s.

### Example 2

A candidate completing the same work in 986 seconds yields about 12.17 million records/s and 1.219 times elapsed-time speedup.

### Example 3

A streaming test accepts 500,000 events/s but emits 470,000/s; backlog grows by about 30,000 events/s and the rate is not sustainable.

### Example 4

A closed-loop client with 100 threads reduces offered rate during a 20-second stall, hiding arrivals an open-loop schedule would have recorded.

### Example 5

Two candidates share a dataset and allocation within each block, with order randomized; paired log ratios reduce block-level noise.

### Example 6

An engine reports query completion before asynchronous sink commit; the benchmark clock must extend through durable publication if that is the contract.

### Example 7

At 8 million correct records/s and 75% CPU utilization, measured CPU demand is $0.75/8,000,000=93.75$ nanoseconds of one aggregate CPU-capacity unit per record under the stated boundary.

### Example 8

A candidate cuts compute seconds by 20% but triples object requests; price-performance can regress despite lower job time.

### Example 9

The same logical plan passes record counts but fails a multiset digest because an outer join drops unmatched null keys; the timing result is rejected.

### Example 10

The executable fixture recomputes mean elapsed times, throughput, speedup, and every paired speedup for the compact example.

<!-- bijux-verify: {"id":"cluster-benchmark-pairs","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"trials=5\nrecords=12000000000\nbaseline_mean_s=1202.0\ncandidate_mean_s=986.0\nbaseline_mrecords_s=9.983\ncandidate_mrecords_s=12.170\nratio_of_means=1.2191\npaired_speedups=1.2323,1.2165,1.1990,1.2132,1.2347\n","stderr":""}} -->
```python
baseline = [1220, 1180, 1205, 1195, 1210]
candidate = [990, 970, 1005, 985, 980]
records = 12_000_000_000

baseline_mean = sum(baseline) / len(baseline)
candidate_mean = sum(candidate) / len(candidate)
paired = [b / c for b, c in zip(baseline, candidate)]

print(f"trials={len(baseline)}")
print(f"records={records}")
print(f"baseline_mean_s={baseline_mean:.1f}")
print(f"candidate_mean_s={candidate_mean:.1f}")
print(f"baseline_mrecords_s={records / baseline_mean / 1_000_000:.3f}")
print(f"candidate_mrecords_s={records / candidate_mean / 1_000_000:.3f}")
print(f"ratio_of_means={baseline_mean / candidate_mean:.4f}")
print("paired_speedups=" + ",".join(f"{x:.4f}" for x in paired))
```

## Cross-Program Connections

- **Experimental design:** blocking, randomization, replication, intervals, effect size, and predeclared exclusions control inference.
- **Queueing:** open versus closed arrivals, utilization, service demand, backlog, and saturation distinguish burst from sustainable capacity.
- **Data engineering:** schema, skew, compression, partitions, file layout, late data, and output semantics determine workload relevance.
- **Distributed systems:** placement, retries, speculation, recovery, coordination, and one-winner commits expand the experiment boundary.
- **Observability:** traceable run identities, mergeable histograms, resource counters, plans, events, and raw logs support diagnosis.
- **Economics:** billed compute, storage, requests, transfer, licenses, idle headroom, and maintenance determine useful work per cost.
- **Security and privacy:** production replays require minimization, anonymization, access control, isolation, retention, and deletion evidence.
- **Governance:** standard benchmark names, disclosures, fair-use rules, and reproducibility prevent misleading comparisons.

## References

1. Transaction Processing Performance Council, [Current Specifications](https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp). Current. Lists governed benchmark versions, specifications, and tools.
2. Transaction Processing Performance Council, [TPC-DS](https://www.tpc.org/tpcds/). Current. Describes decision-support workload scope, performance tests, data maintenance, pricing, and comparability boundaries.
3. Transaction Processing Performance Council, [TPC Benchmarks Overview](https://www.tpc.org/information/benchmarks5.asp). Current. Distinguishes workload families and their primary metrics.
4. Apache Beam, [Nexmark Benchmark Suite](https://beam.apache.org/documentation/sdks/java/testing/nexmark/). Current. Documents batch/streaming queries, workload knobs, deterministic generation, output, suites, and comparison caveats.
5. Apache Hadoop, [GridMix](https://hadoop.apache.org/docs/stable/hadoop-gridmix/GridMix.html). Version 3.3.5. Documents trace-derived mixed-job emulation, submission policies, users/queues, cache, compression, and resource profiles.
6. Apache Spark, [Monitoring and Instrumentation](https://spark.apache.org/docs/latest/monitoring.html). Current. Documents event logs, stage/task metrics, executor evidence, and history reconstruction.
7. Apache Spark, [Tuning](https://spark.apache.org/docs/latest/tuning.html). Current. Documents memory, serialization, parallelism, shuffle, and measurement-relevant runtime behavior.
8. Apache Flink, [Metrics](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/metrics/). Current. Documents counters, meters, histograms, latency/state sampling, task metrics, and instrumentation overhead.
9. Kubernetes, [Tools for Monitoring Resources](https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-usage-monitoring/). Current. Distinguishes resource and full metrics pipelines for cluster/application evidence.
10. Prometheus, [Histograms and Summaries](https://prometheus.io/docs/practices/histograms/). Current. Documents aggregatable latency distributions and why averaging precomputed quantiles is invalid.
11. NIST/SEMATECH, [Confidence Limits for the Mean](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm). Engineering Statistics Handbook. Defines interval calculation, assumptions, and repeated-sampling interpretation.
12. Standard Performance Evaluation Corporation, [Cloud Computing Benchmark Suites](https://www.spec.org/cloud/). Current. Identifies the current SPEC Cloud IaaS suite and its target audiences/boundary.
13. Standard Performance Evaluation Corporation, [SPEC Cloud IaaS 2018 Results](https://www.spec.org/cloud_iaas2018/results/). Current. Documents published results plus user guide, run/reporting rules, FAQ, and fair-use context.

## Exercises

### Exercise 1

Write a benchmark contract for choosing between two cluster instance families for a nightly batch join-and-aggregate pipeline.

### Exercise 2

Diagnose a streaming test that accepts 900,000 events/s, emits 830,000/s, maintains low processing latency for completed events, and accumulates watermark lag.

### Exercise 3

Design a paired experiment for a runtime upgrade when only shared clusters are available and daily background load drifts.

### Exercise 4

Explain how to detect coordinated omission and an undersized load generator in an open-loop latency benchmark.

### Exercise 5

Design a reproducibility and correctness bundle for publishing a TPC-DS-derived internal comparison without claiming official TPC compliance.

## Answers to the Exercises

### Answer 1

State the decision, representative immutable dataset and digest, logical plan/output oracle, nightly deadline, useful completion boundary through durable commit, CPU/memory/storage/network limits, fixed node count or equal cost envelope, and guardrails for retries, failures, and cost. Pin images, software, configuration, topology, quotas, cache condition, and background load. Randomize paired trials across matched allocations, repeat across several nights, validate exact outputs, retain task/resource distributions, and require a practical improvement whose interval clears the threshold without cost or recovery regression.

### Answer 2

The system is overloaded under the declared input because backlog grows about 70,000 events/s. Low latency among completed events is conditioned on survivors and may omit queued/expired work. Measure intended/offered/accepted/completed/failed/expired counts, queue age, event-time latency, watermark lag, state/checkpoints, sink commits, and generator timing. Reduce rate or add capacity until backlog is bounded across checkpoints, compaction, autoscaling, and recovery, then report that sustainable point rather than 900,000 accepted events/s.

### Answer 3

Treat cluster allocation and time window as blocks. Provision baseline and candidate from automation on comparable allocations, pin data and constraints, measure co-tenant/background demand, and alternate randomized order within narrow windows. Repeat blocks across days, retain failures, use paired log elapsed-time or throughput differences, and report raw pairs plus an interval. If background work interacts differently with candidates, include that as part of the shared-cluster population rather than subtracting it invisibly.

### Answer 4

Schedule arrivals from an independent clock and record intended send time, actual send/admission time, and completion. During a stall, missing scheduled arrivals or latency measured only from delayed actual send indicates coordinated omission. Run generator-headroom tests above the SUT target; monitor generator CPU, run queue, memory, network, sockets, clocks, internal queues, and dropped scheduling events. Shard generators if needed and prove aggregate generation/sink/telemetry capacity exceeds the offered profile without changing the workload.

### Answer 5

Publish the exact derived query/workload definitions and deviations, generator/tool versions, seed, data/schema/layout digests, semantic oracle, run manifest, infrastructure/configuration/topology, warm-up and timing boundaries, raw metrics/logs, exclusions, cost boundary, and deterministic analysis code. Label results “TPC-DS-derived internal workload,” cite the applicable specification and fair-use context, and explicitly deny audited/compliant comparability. Validate every output, expose failed trials and uncertainty, and make every summary point traceable to immutable run IDs.
