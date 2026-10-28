---
module_id: LSDS-100
program: Large-Scale Data Systems Engineering
level: 2
module_number: 100
title: Conducting an End-to-End Large-Scale Data Performance Review
status: complete
last_verified: 2026-09-04
---

# Conducting an End-to-End Large-Scale Data Performance Review

## One-Page Review

### Governing question

How should an engineer conduct a defensible performance review of a large-scale data system from workload arrival through correct durable output, identify the binding mechanisms rather than convenient symptoms, and produce prioritized changes with reproducible evidence, safety constraints, and verification plans?

### Essential definitions

- An **end-to-end review** evaluates objectives, workload, correctness, architecture, execution, resources, reliability, cost, and governance across one declared boundary.
- A **review contract** names the decision, stakeholders, system/workload scope, observation period, service objectives, evidence, exclusions, and approval criteria.
- **useful work** is contract-valid, correct, durably committed output; attempts and submitted work are not substitutes.
- A **critical path** is the precedence-constrained chain whose durations determine completion or freshness.
- A **service center** is a resource or dependency such as CPU, memory, scheduler, storage, network, metadata, or sink that work must consume.
- A **bottleneck** is the binding constraint in the observed operating regime; it can move after an intervention.
- A **performance finding** joins a scoped symptom, evidence, causal mechanism, impact, confidence, and falsification condition.
- A **recommendation** specifies intervention, owner, prerequisites, expected effect, guardrails, experiment, rollback, and decision threshold.
- A **capacity envelope** is the tested workload/resource/configuration region where objectives and invariants hold.
- A **counterfactual** states what evidence should change if a proposed mechanism is causal.
- A **reproducibility bundle** links immutable inputs/configuration to raw observations, calculations, findings, and decisions.
- A **residual risk** is known exposure remaining after the chosen actions, controls, or accepted trade-off.

### Central model, mechanism, or theorem

Define end-to-end elapsed time for workload instance $i$ as:

$$T_i=t_{durable,i}-t_{eligible,i}.$$

Decompose it by non-overlapping lifecycle state when possible:

$$T_i=T_{queue}+T_{startup}+T_{execute}+T_{checkpoint}+T_{commit}+T_{validate},$$

while separately deriving the execution DAG critical path $CP=max_{p\in paths}\sum_{v\in p}t_v$. Wall-clock components may overlap, so a review must not sum arbitrary stage/resource timers as elapsed time.

For correct completed work $C$ over interval $H$, useful throughput is $X=C/H$. At service center $r$, measured demand $D_r=B_r/C$ and utilization $U_r=B_r/H$ obey $U_r=XD_r$ for aligned boundaries. Combine this accounting with queue/backlog conservation, partition/task distributions, critical-path evidence, and resource ceilings to identify the first binding center.

Every conclusion follows a chain:

$$objective\rightarrow workload\rightarrow boundary\rightarrow evidence\rightarrow mechanism\rightarrow intervention\rightarrow verification.$$

Breaking any link turns a recommendation into an unsupported guess.

### Critical invariants

- User/business objectives map to explicit batch deadlines, freshness, throughput, latency, correctness, availability, recovery, and cost measures.
- The input snapshot/stream, code, plan, configuration, infrastructure, placement, and review window are identifiable.
- Offered, accepted, attempted, retried, failed, correct, and durably committed work remain distinct.
- End-to-end timing includes queueing and required publication/validation; overlapping timers are not double-counted.
- Evidence preserves distributions and correlation across execution, stage, task, partition, key, attempt, worker, resource, dependency, and time.
- Causal claims state alternatives, counterfactual predictions, confidence, and evidence limitations.
- Proposed changes preserve data semantics, retry/idempotency, state, ordering, security, retention, recovery, and downstream contracts.
- Performance, reliability, capacity, and cost are evaluated over the same workload and system boundary.
- Experiments predeclare success, regression guardrails, observation duration, rollback, and owner.
- Review artifacts expose missing evidence and residual risk; lack of telemetry is never converted into a passed conclusion.

### Common failures

Common failures include starting from dashboards instead of a decision; optimizing the longest visible stage while queueing dominates; timing lazy submission rather than durable output; trusting average task time; summing overlapping CPU, shuffle, and wall time; calling high utilization the cause without demand evidence; assuming low CPU means spare capacity; tuning one query on an unrepresentative cache; ignoring skew, retries, output correctness, and failed work; recommending more workers beyond partition/key/sink limits; treating autoscaling as instantaneous; omitting recovery and maintenance traffic; reporting list rather than reconciled cost; changing several levers at once; and ending with vague “monitor” or “optimize” actions that lack thresholds, owners, experiments, and rollback.

### Compact example

A batch becomes eligible at 00:00 and durably validates at 00:33:20, so end-to-end elapsed time is 2,000 seconds. Non-overlapping lifecycle states are 120 seconds queued, 80 startup, 1,620 executing, 100 committing, and 80 validating. Four billion correct records yield 2.0 million records/s end-to-end. The execution critical path is 1,500 seconds, leaving 120 seconds of execution slack/overlap relative to aggregate execute state rather than proving 1,620 seconds of serial work. A proposed exchange change predicts a 120-second critical-path reduction without raising spill, network saturation, output-file count, errors, or cost. It is accepted only after paired representative trials pass exact output and recovery checks.

### Connections

[LSDS-070](070-diagnosing-a-distributed-query-from-plan-to-network.md) supplies plan-to-network diagnosis, [LSDS-080](080-operating-table-metadata-under-millions-of-files.md) supplies metadata operations, [LSDS-090](090-designing-recovery-for-multi-hour-and-multi-day-jobs.md) supplies recovery design, [LSDS-096](096-skew-detection-and-mitigation.md) supplies tail diagnosis, [LSDS-097](097-cluster-benchmarking.md) supplies controlled evidence, [LSDS-098](098-capacity-planning-for-batch-and-streaming.md) supplies resource intent, and [LSDS-099](099-cost-attribution-and-workload-governance.md) supplies reconciled economics.

## Governing Question

Large-scale data performance crosses organizational and technical boundaries. A freshness miss can originate in late upstream data, admission queues, metadata listing, a skewed join, garbage collection, saturated shuffle, checkpoint alignment, sink quotas, catalog conflict, or validation. Each team can show a healthy local dashboard while the product still misses its objective.

The governing question is how to assemble evidence across those boundaries without losing semantic correctness or causal discipline, then turn the result into an executable decision rather than a collection of charts.

## Why This Matters

Performance reviews allocate engineering time, infrastructure money, and operational risk. A plausible but wrong bottleneck diagnosis can shift load to a more fragile center, raise cost, or weaken correctness. A local improvement can worsen the end-to-end critical path by increasing downstream files, requests, state, or retries.

A durable review creates shared language and traceability. It lets stakeholders reproduce the result, distinguish facts from assumptions, revisit decisions after workload drift, and validate that promised gains survived production.

## Prerequisites and Retrieval

Review task graphs in [LSDS-005](005-distributed-task-graphs.md), storage semantics in [LSDS-016](016-object-storage-semantics.md), shuffle in [LSDS-031](031-shuffle-architecture.md), streaming pressure in [LSDS-049](049-backpressure-across-operators.md), scheduler diagnosis in [LSDS-060](060-diagnosing-scheduler-delay-and-resource-fragmentation.md), query diagnosis in [LSDS-070](070-diagnosing-a-distributed-query-from-plan-to-network.md), recovery in [LSDS-090](090-designing-recovery-for-multi-hour-and-multi-day-jobs.md), resource pathologies in [LSDS-092](092-memory-pressure-spill-and-garbage-collection.md), benchmarking in [LSDS-097](097-cluster-benchmarking.md), capacity in [LSDS-098](098-capacity-planning-for-batch-and-streaming.md), and cost in [LSDS-099](099-cost-attribution-and-workload-governance.md).

You should understand DAGs, queueing, partitions, joins, aggregation, streaming time/state, storage, network, memory/GC, metrics/traces/logs, retries, checkpoints, commits, capacity, experimentation, statistics, and cost allocation.

Collect objective/owner/SLO; workload class and correct-output oracle; eligible/admit/start/finish/commit/validate timestamps; input/output identity and data shape; logical/physical/executed plans; job/stage/operator/task/partition/key/attempt/worker IDs; bytes/records/state; CPU/memory/GC/spill/storage/network/requests; scheduler/locality; dependencies/quotas; backlog/watermarks/checkpoints; retries/failures/recovery; cache/load cohort; versions/configuration/topology; allocated/billed cost; and evidence lineage.

## Learning Objectives

After this module, you should be able to:

1. establish a review contract tied to an actual decision and stakeholder objective;
2. define end-to-end workload, correctness, timing, reliability, and cost boundaries;
3. reconstruct execution from plans, events, metrics, logs, and durable outputs;
4. distinguish critical-path work, parallel work, queueing, and overlapping resource time;
5. identify bottlenecks from distributions, service demand, saturation, and counterfactuals;
6. analyze batch, streaming, storage, metadata, network, memory, skew, and dependency constraints;
7. convert observations into falsifiable findings with confidence and alternatives;
8. design safe recommendations with experiments, guardrails, rollback, and ownership;
9. communicate prioritized decisions, missing evidence, and residual risk; and
10. verify realized outcomes and maintain the review as workloads evolve.

## Core Exposition

### Charter the review

Write the decision, sponsor, affected users, owners, deadline, and available actions. State whether the review targets an incident, regression, scaling risk, cost change, migration, or recurring health assessment.

Define in-scope systems/workloads and explicit exclusions. Record conflicts among latency, throughput, cost, correctness, recovery, and delivery timing instead of assuming one optimization objective.

### Translate outcomes into objectives

Map business outcomes to technical measures: completed before deadline, event-time freshness, correct rows, query percentile, backlog age, recovery time, availability, or cost per valid product.

Use both black-box symptoms and white-box causes. A resource metric alone is not a user objective; a user symptom alone rarely identifies the mechanism.

### Freeze the workload contract

Describe arrival pattern, concurrency, operations, data volume/shape/skew/cardinality, state, retention, source/sink, cache, and failure cohort. Identify production population and adversarial cases.

Digest batch snapshots and version stream ranges/generator seeds. Validate output semantics before performance analysis so faster wrong work cannot win.

### Draw the system boundary

Trace eligibility through admission, planning, reads, execution, shuffle/state, checkpoints, writes, durable commit, catalog publication, validation, and downstream visibility. Include shared control planes and external dependencies.

State what time/cost lies outside and why. Measure excluded components when they can throttle the reviewed path.

### Build the evidence map

For every objective and suspected mechanism, name the evidence source, identity keys, units, sampling, retention, clock, and known gaps. Join job events, plans, metrics, logs, traces, storage/catalog records, billing, and validation by stable IDs.

Preserve raw evidence. Dashboard screenshots and pre-aggregated percentiles are weak substitutes for traceable observations.

### Reconstruct the lifecycle

Create a timeline from eligible through durable validation. Separate admission, startup, active execution, checkpoint, commit, validation, retries, and recovery with non-overlapping states where feasible.

Clock skew, asynchronous APIs, and overlapping stages complicate the timeline. Prefer causal event relationships and monotonic durations; document uncertainty rather than invent precision.

### Reconstruct the execution graph

Compare logical, physical, initial, and executed plans. Map exchanges, joins, aggregation, repartition, adaptive changes, materialization, storage reads/writes, and sink commits to stages/operators.

Compute the precedence critical path. Total task CPU is resource work, not elapsed time; the slowest task matters only when it gates a successor or completion.

### Inspect distributions

Report task/partition/key/worker distributions for input, decoded bytes, CPU, duration, memory, spill, shuffle, state, output, retries, and errors. Segment by operator and attempt.

Correlate logical partitions across retries/workers to separate data skew from resource skew. Preserve empty/failed/censored work and maximum tails.

### Analyze service centers

At CPU, memory, scheduler, storage, metadata, network, shuffle, state, coordination, and sink centers, compare offered demand, utilization, queue, service time, errors, and hard ceilings. Normalize demand per correct work.

High utilization plus queue growth supports saturation; high latency at low utilization may indicate serialization, locks, quotas, locality, or an upstream/downstream wait. Absence of one metric is not absence of demand.

### Review memory and serialization

Trace encoded, decoded, object, accumulator, state, cache, and spill sizes. Attribute GC and allocation by executor/task cohort. Determine whether spill protects correctness or creates critical-path I/O.

Compare codecs/serializers on CPU, size, network/storage transfer, compatibility, and failure. A byte reduction can cost more critical-path CPU.

### Review data movement and storage

Account for logical versus physical bytes, shuffle blocks/connections, locality, retransmission, storage requests, IOPS, bandwidth, metadata operations, file sizes, and cache.

Find the first binding hop. Faster compute cannot outrun a sink quota; more partitions can overload request/connection/metadata centers.

### Review streaming stability

Compare offered, accepted, and correct emitted rates; backlog slope; event-time latency; watermark lag; backpressure; keyed state; checkpoints; timers; and sinks. Segment by operator/key/window.

Run long enough for checkpoints, compaction, autoscaling, state growth, and bursts. A high accepted rate with growing backlog is not sustainable throughput.

### Review failure and recovery

Quantify failed/retried/speculative work, checkpoint/recompute cost, restore time, duplicate suppression, ambiguous commits, and catch-up while input continues. Confirm output after failure.

Capacity and cost include recovery traffic. Test representative worker/coordinator/dependency failures in an isolated environment with explicit success criteria.

### Review capacity and cost

Map forecast workload classes to measured service demands and constraints. Verify peak, deadline, state, parallelism, dependency, placement, and failure reserve within provisioning lead time.

Reconcile billed/effective cost and attribute direct/shared/idle work consistently. Compare correct useful work per cost, not raw attempts or list-price node hours.

### Form causal findings

Write each finding as: scoped symptom; objective impact; evidence; mechanism; alternatives considered; counterfactual prediction; confidence; missing evidence. Separate observation from inference.

Prefer the simplest mechanism explaining correlated evidence across layers. Use profiling, controlled load, retries on different workers, or configuration experiments to discriminate alternatives.

### Design and prioritize interventions

Target the binding mechanism: reduce work, movement, state, requests, serialization, skew, queueing, or failure amplification; raise a real limit only when needed. Predict the next bottleneck.

Rank by objective impact, confidence, effort, reversibility, blast radius, and dependencies. Preserve quick mitigations and durable structural corrections as separately owned actions.

### Specify verification and rollback

For every recommendation, freeze representative input and constraints, define baseline/candidate, correctness oracle, primary metric, guardrails, sample/blocking plan, success threshold, observation period, failure cases, and rollback trigger.

Canary changes where possible. Validate end-to-end because local stage gains can move cost or tail work downstream.

### Communicate the decision

Lead with objective status, binding constraints, quantified impact, highest-confidence actions, and decisions required. Attach evidence map, timelines, plans, distributions, experiment results, and limitations.

Assign owners and dates. State accepted residual risk, telemetry gaps, capacity lead time, and conditions that invalidate conclusions.

### Close the loop

After rollout, compare realized outcomes with predicted counterfactuals and guardrails. Record whether the bottleneck moved, whether demand/unit cost changed, and whether correctness/recovery held.

Version the review and schedule reassessment on workload, data shape, runtime, infrastructure, SLO, or cost-policy changes. Retire stale dashboards and recommendations.

## Definitions and Notation

Let:

- $t_e,t_a,t_s,t_d$ be eligible, admitted, execution-start, and durable-valid timestamps;
- $T=t_d-t_e$ be end-to-end elapsed time;
- $CP$ be the execution DAG critical-path duration;
- $C$ be correct durably completed useful work over observation interval $H$;
- $X=C/H$ be useful throughput;
- $B_r,U_r,D_r$ be busy time, utilization, and service demand at resource $r$;
- $Q(t)$ be queue/backlog at time $t$;
- $L_e$ be event-time end-to-end latency;
- $K$ be reconciled cost over the aligned boundary; and
- $E=C/K$ be useful work per cost.

Lifecycle durations may be additive only when states are mutually exclusive. Resource busy times across workers and stages often overlap and may exceed wall time. Every rate, percentile, and cost needs named population and window.

## Mechanisms, Invariants, or Proof Structure

### End-to-end conservation

Every input/work item is classified as queued, executing, retried, failed, expired by policy, or correctly committed; streaming backlog change equals accepted minus completed/removed work. Reconcile counts before interpreting throughput.

### Critical-path lower bound

Any DAG execution must take at least the sum of durations along every precedence path, hence at least the maximum path sum. Shortening noncritical parallel work need not change elapsed time.

### Service-demand cross-check

With aligned boundaries, $U_r=B_r/H$, $D_r=B_r/C$, and $X=C/H$, so $U_r=XD_r$. Violations expose mismatched units/windows or measurement loss, not a new performance law.

### Causal falsification

A finding predicts observable changes under a controlled intervention. If exchange bytes fall but critical-path exchange time and downstream constraints do not, the proposed network-volume mechanism is weakened.

### Review traceability

Immutable workload/configuration identities select raw evidence; deterministic calculations derive tables/figures; findings cite those artifacts; recommendations cite findings; decisions and realized outcomes cite experiments.

## Alternatives and Trade-Offs

| Review approach | Strength | Cost or limitation |
|---|---|---|
| Black-box SLO review | Centers user-visible outcomes | Weak causal detail alone |
| White-box runtime review | Rich mechanism evidence | Can optimize internals that do not affect outcomes |
| Trace-led review | Reconstructs cross-layer critical paths | Sampling/context propagation and storage cost |
| Metrics-led review | Efficient trends and distributions | Aggregation can hide identity and causality |
| Profile-led review | Locates CPU/allocation work | Narrow time/process scope and overhead |
| Benchmark-led review | Controlled counterfactuals | Representativeness and environment drift |
| Incident-led review | Exercises real failure modes | Biased toward one exceptional cohort |
| Capacity-led review | Connects forecast to resource risk | Depends on stable demand estimates |
| Cost-led review | Prioritizes economic leverage | Allocation policy can obscure physical mechanism |
| Full-system replay | High end-to-end realism | Expensive, risky, and hard to reproduce |

## Failure Modes and Misconceptions

1. **The dashboard defines the question.** Objectives and decisions define required evidence.
2. **The longest stage is the bottleneck.** Queueing or another critical-path segment may dominate.
3. **Task CPU sums to elapsed time.** Parallel resource work overlaps.
4. **Average task time is representative.** Maximum/straggler distributions gate completion.
5. **High utilization proves causality.** Demand, queues, and controlled changes are needed.
6. **Low CPU means spare capacity.** I/O, locks, quotas, keys, or dependencies can bind.
7. **More workers reduce every delay.** Critical paths and parallelism ceilings remain.
8. **Accepted input is streaming throughput.** Backlog may be growing.
9. **Successful completion proves correctness.** Output semantics and durability need oracles.
10. **Retries are harmless resilience.** They amplify work, cost, and contention.
11. **One warm run represents production.** Cache, mix, scale, failure, and shared load differ.
12. **A local speedup is an end-to-end gain.** Downstream work can expand.
13. **Autoscaling removes capacity planning.** Reaction, quotas, state, and ceilings constrain it.
14. **Cost per node-hour is unit economics.** Reconciled cost and useful output must align.
15. **A review ends with recommendations.** Owners, experiments, rollout, and outcome verification close it.

## Worked Examples

### Example 1

Eligibility at 00:00 and durable validation at 00:33:20 produce 2,000 seconds end-to-end.

### Example 2

Non-overlapping lifecycle states of 120, 80, 1,620, 100, and 80 seconds reconcile exactly to 2,000.

### Example 3

Four billion correct records over 2,000 seconds yield 2.0 million records/s useful throughput.

### Example 4

A 1,500-second execution critical path is a lower bound; 1,620 seconds in execute state includes slack/overlap outside that path.

### Example 5

The slowest task is rerun on another worker; if slowness follows the partition, data/work skew gains support.

### Example 6

CPU remains 45% while storage-request queues and throttles rise, supporting a storage service-center constraint.

### Example 7

A stream accepts 300,000 events/s and commits 270,000/s; backlog grows 30,000/s despite low completed-event latency.

### Example 8

A partition change shortens a join by 90 seconds but adds 130 seconds of sink metadata work, regressing end-to-end completion.

### Example 9

Retry cost rises while correct output stays fixed; useful work per cost falls even though submitted throughput rises.

### Example 10

The executable fixture reconciles lifecycle time, throughput, critical-path slack, and candidate prediction.

<!-- bijux-verify: {"id":"end-to-end-review","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"end_to_end_s=2000\nlifecycle_sum_s=2000\nreconciled=True\ncorrect_records=4000000000\nuseful_mrecords_s=2.000\nexecution_critical_path_s=1500\nexecution_slack_s=120\npredicted_candidate_s=1880\npredicted_speedup=1.064\n","stderr":""}} -->
```python
eligible_s = 0
durable_valid_s = 2_000
lifecycle = {
    "queue": 120,
    "startup": 80,
    "execute": 1_620,
    "commit": 100,
    "validate": 80,
}
correct_records = 4_000_000_000
critical_path_s = 1_500
predicted_reduction_s = 120

end_to_end_s = durable_valid_s - eligible_s
lifecycle_sum_s = sum(lifecycle.values())
candidate_s = end_to_end_s - predicted_reduction_s

print(f"end_to_end_s={end_to_end_s}")
print(f"lifecycle_sum_s={lifecycle_sum_s}")
print(f"reconciled={lifecycle_sum_s == end_to_end_s}")
print(f"correct_records={correct_records}")
print(f"useful_mrecords_s={correct_records / end_to_end_s / 1_000_000:.3f}")
print(f"execution_critical_path_s={critical_path_s}")
print(f"execution_slack_s={lifecycle['execute'] - critical_path_s}")
print(f"predicted_candidate_s={candidate_s}")
print(f"predicted_speedup={end_to_end_s / candidate_s:.3f}")
```

## Cross-Program Connections

- **Systems engineering:** boundaries, objectives, constraints, interfaces, failure modes, trade studies, and verification frame the review.
- **Experimental design:** representative cohorts, controls, blocking, repetition, uncertainty, and falsification support causal decisions.
- **Algorithms:** DAG critical paths, partitioning, joins, aggregation, sketches, and complexity explain scalable work.
- **Operating systems:** CPU scheduling, memory, allocation, GC, storage, networking, and isolation explain worker behavior.
- **Distributed systems:** retries, speculation, consensus, checkpoints, state, idempotency, and recovery shape useful work.
- **Data architecture:** schemas, layouts, metadata, retention, lineage, and downstream contracts constrain optimization.
- **Platform/SRE:** SLOs, monitoring, capacity, automation, rollout, incident response, and ownership operationalize findings.
- **Economics/governance:** reconciled cost, shared allocation, budgets, quotas, priorities, and residual risk guide choices.

## References

1. Google, [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/). Defines black/white-box evidence, symptoms versus causes, and latency/traffic/errors/saturation.
2. Google, [Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/). Describes systematic problem reporting, diagnosis, hypothesis testing, and root-cause discipline.
3. Google, [Testing for Reliability](https://sre.google/sre-book/testing-reliability/). Connects tests, failure, scale, configuration, and production reliability evidence.
4. Google, [Postmortem Culture](https://sre.google/sre-book/postmortem-culture/). Describes evidence-based learning, root causes, actions, ownership, and institutional follow-through.
5. Apache Spark, [Monitoring and Instrumentation](https://spark.apache.org/docs/latest/monitoring.html). Current. Documents application, job, stage, task, executor, event-log, history, REST, and metrics evidence.
6. Apache Spark, [Tuning](https://spark.apache.org/docs/latest/tuning.html). Current. Documents memory, serialization, task sizing, shuffle, GC, and diagnosis-relevant trade-offs.
7. Apache Spark, [SQL Performance Tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html). Current. Documents statistics, caching, partitions, joins, adaptive execution, and executed-plan evidence.
8. Apache Flink, [Production Readiness Checklist](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/production_ready/). Current. Covers parallelism, stable operator identity, state, checkpoints, high availability, security, and testing.
9. Apache Flink, [Metrics](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/metrics/). Current. Documents job/operator/task/system, I/O, backpressure, checkpoint, latency, state, and resource metrics.
10. Apache Flink, [Tuning Checkpoints and Large State](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/large_state_tuning/). Current. Covers checkpoint evidence, state, backpressure, recovery, and catch-up capacity.
11. Apache Beam, [Programming Guide](https://beam.apache.org/documentation/programming-guide/). Current. Documents pipeline graphs, watermarks, state/timers, counters, distributions, gauges, metric queries, and metric export.
12. Prometheus, [Histograms and Summaries](https://prometheus.io/docs/practices/histograms/). Current. Documents aggregatable distributions and why precomputed quantiles should not be averaged.
13. NIST/SEMATECH, [Product and Process Comparisons](https://www.itl.nist.gov/div898/handbook/prc/prc.htm). Engineering Statistics Handbook. Covers assumptions, intervals, tests, outliers, trends, and multi-process comparisons.

## Exercises

### Exercise 1

Charter an end-to-end review for a nightly pipeline missing its publication deadline and define the evidence map.

### Exercise 2

Diagnose a batch whose CPU utilization is low, task duration is balanced, and commit time rises with output-file count.

### Exercise 3

Write a falsifiable finding for a streaming freshness regression with growing backlog, checkpoint delay, and sink throttling.

### Exercise 4

Design a safe experiment for changing partition count and compression together, then improve the design for causal attribution.

### Exercise 5

Produce the structure of a final review decision package, including verification and residual risk.

## Answers to the Exercises

### Answer 1

Name the publication decision, users, deadline, correctness/freshness/cost/recovery guardrails, pipelines/dependencies, and immutable workload cohort. Trace eligible input through admission, planning, storage, DAG stages, shuffle/state, commit, catalog, validation, and visibility. Map each segment to stable IDs and raw events/metrics/logs/plans, task distributions, resource centers, quotas, output oracle, failures/retries, configuration/topology, and reconciled cost. Record clocks, sampling, gaps, owners, exclusions, and conditions that invalidate comparison.

### Answer 2

Balanced tasks and low CPU weaken compute/skew hypotheses. Correlate file count with commit/catalog/list/request latency, metadata CPU/locks, storage request rate/throttles, retries/conflicts, and downstream visibility. Control total bytes while varying file count, then compact or change writer/task sizing. Predict lower requests and commit critical-path time without lost records, oversized files, reduced parallel reads, or higher upstream spill; verify end-to-end and retain rollback.

### Answer 3

Finding: for workload/version/window X, event-time freshness violates Y because correct sink throughput remains below accepted input during checkpoint-aligned bursts; backlog and watermark lag rise with sink throttle latency while upstream CPU has headroom. Alternatives include hot keys and source bursts. Prediction: raising governed sink capacity or reducing request amplification will lower throttle time and make backlog slope nonpositive without changing input, correctness, or checkpoint semantics. Confidence and missing per-key/request evidence are stated.

### Answer 4

The bundled comparison can answer whether the combined configuration helps, but cannot attribute effect. Pin data, plans, resources, cache, workload, output oracle, and trial blocks; predeclare elapsed-time primary metric plus CPU, bytes, network, spill, files, cost, and recovery guardrails. For attribution use a factorial or sequential design with baseline, partition-only, compression-only, and combined candidates in randomized paired blocks. Verify exact output and interactions, then canary the chosen configuration with rollback thresholds.

### Answer 5

Lead with review contract, objective status, workload/boundary, and decisions requested. Present lifecycle and critical path, correctness evidence, workload/data shape, plan, distributions, service-center constraints, streaming/recovery/capacity/cost findings, alternatives, confidence, and telemetry gaps. Rank recommendations with expected effect, owner, dependencies, blast radius, experiment, success/guardrail thresholds, rollout, and rollback. Attach reproducibility artifacts and record accepted residual risks, review expiry triggers, and post-rollout comparison against predictions.
