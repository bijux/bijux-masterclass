---
module_id: LSDS-070
program: Large-Scale Data Systems Engineering
level: 2
module_number: 70
title: Diagnosing a Distributed Query from Plan to Network
status: complete
last_verified: 2026-09-04
---

# Diagnosing a Distributed Query from Plan to Network

## One-Page Review

### Governing question

How should an engineer turn one slow, stuck, failed, resource-heavy, or incorrect distributed query into a time-aligned causal explanation that connects logical/physical plan choices to stages, attempts, operators, exchanges, workers, storage, network, client behavior, and cluster contention?

### Essential definitions

- A **query fingerprint** groups logically equivalent requests while a **query instance ID** identifies one execution with parameters, snapshot, user, configuration, and timestamps.
- A **query lifecycle** divides wall time into admission/queue, planning, scheduling, execution, result production, and client-drain intervals.
- The **critical path** is the dependency chain whose completion determines query wall time; summed task time is work, not latency.
- A **plan estimate error** compares estimated and actual rows/bytes for the same node and scope.
- A **stage** or **fragment** is a physical subgraph separated by exchanges or other scheduling/materialization boundaries.
- A **task attempt** executes one logical stage partition; retry and speculation can create several attempts for one partition.
- **skew** is uneven work or time across comparable partitions/tasks; a long task is not automatically skewed data.
- **backpressure** is upstream blocking caused by insufficient downstream consumption or output-buffer capacity.
- A **network symptom** is evidence at transport/NIC/path level—such as retransmission, congestion, loss, queueing, or bandwidth ceiling—not merely an operator waiting on exchange.
- A **causal intervention** changes one plausible mechanism in a controlled reproduction or cohort and observes whether the predicted symptom changes.

### Central model, mechanism, or theorem

Diagnosis is constrained causal inference. Build a single evidence timeline and map every metric to `(query, plan epoch, stage, task, logical partition, selected attempt, operator, worker, source, interval)`. Decompose

$$T_{query}=T_{queue}+T_{plan}+T_{schedule}+T_{execute}+T_{drain},$$

then analyze $T_{execute}$ by stage dependencies and task distributions rather than adding parallel durations. For estimate $e>0$ and actual $a>0$, multiplicative error is

$$Q=\max(a/e,e/a).$$

For comparable task duration distribution, ratios such as $t_{max}/\operatorname{median}(t)$ identify tails but not their cause. A defensible conclusion triangulates plan/operator facts, task/exchange evidence, and worker/storage/network evidence in the same interval, rules out competing explanations, and survives a safe predicted intervention.

### Critical invariants

- Evidence retains query ID/fingerprint, parameters redaction, snapshot, user/tenant, session/configuration, engine/build, plan and adaptive epochs, cluster topology, and synchronized timestamps.
- Estimated and actual values compare the same plan node, units, semantic scope, and completed attempt set.
- Stage/task statistics use logical partitions and selected attempts; retries and speculative duplicates are separately counted.
- Wall time follows dependency/overlap; CPU/task-time sums are not reported as elapsed latency.
- Medians, percentiles, maxima, distributions, and sample counts remain available; averages alone do not hide tails.
- Busy, idle, blocked, queued, backpressured, spilling, throttled, and client-blocked states are distinguished.
- Exchange wait is not called network failure without host/path evidence; network counters are correlated to the query's endpoints and interval.
- Scan, decode, compute, memory, spill, disk, GC, scheduler, connector, and client bottlenecks remain competing hypotheses until evidence separates them.
- A diagnostic intervention changes one bounded factor, preserves correctness, records its cohort/configuration, and includes rollback.
- Logs/plans/traces redact credentials and sensitive literals while preserving low-cardinality correlation keys and durable artifacts.

### Common failures

Common failures include diagnosing from the SQL text but not the executed plan; reading only the final adaptive plan; treating `BLOCKED` as proof of network trouble; averaging away one straggler; comparing compressed scan bytes to decoded memory; blaming skew when one worker had GC or disk failure; reading node-wide retransmits without query endpoint/time correlation; counting losing attempts as useful work; optimizing a non-critical stage; ignoring client result backpressure; changing five settings at once; reproducing against a different snapshot or cluster load; and collecting screenshots without machine-readable plans, events, configs, and timestamps.

### Compact example

A node estimated 2 million rows but produced 50 million, so $Q=25$. Five comparable tasks take 40, 42, 44, 45, and 210 seconds: median 44 and maximum/median 4.77. The 210-second task reads five times the bytes with normal CPU, disk, and TCP evidence, supporting partition skew. If bytes are equal but that worker shows long GC pauses or retransmissions only during the task, the causal hypothesis changes. The plan error explains why partitioning may be poor; aligned task and host evidence explains the tail mechanism.

### Connections

[LSDS-031](031-shuffle-architecture.md) defines shuffle evidence, [LSDS-053](053-fair-and-capacity-scheduling.md) explains admission/fairness, [LSDS-057](057-memory-cpu-and-i-o-isolation.md) bounds worker resources, [LSDS-060](060-diagnosing-scheduler-delay-and-resource-fragmentation.md) covers scheduler diagnosis, [LSDS-061](061-distributed-logical-and-physical-plans.md) supplies plan lineage, [LSDS-063](063-exchange-operators.md) supplies flow control, [LSDS-064](064-distributed-hash-and-merge-joins.md) and [LSDS-065](065-partial-and-final-aggregation.md) supply state costs, and [LSDS-068](068-adaptive-query-execution.md) supplies plan revisions.

## Governing Question

A slow distributed query presents many simultaneous observations: high wall time, blocked operators, a skewed stage graph, spill, worker CPU, remote reads, network queues, retries, or a client that consumes slowly. None is automatically the root cause. Backpressure deliberately propagates a downstream limitation upstream. A failed worker can resemble data skew. A poor join estimate can manifest as memory pressure or network expansion several stages later.

The diagnostic task is to connect the user's symptom to the executed physical plan and one time-aligned chain of resource and flow effects. That requires stable identities from query to sockets, complete attempt accounting, distributions rather than averages, and a model of dependencies. It also requires humility: often the evidence supports a bounded mechanism, not a universal root cause.

The governing question is how to collect enough reproducible evidence to discriminate plan, scheduling, operator, storage, exchange, host, network, connector, and client hypotheses—then validate the leading explanation with the smallest safe intervention.

## Why This Matters

Distributed query incidents consume expensive specialist time because symptoms cross team boundaries. A query planner owns estimates; a scheduler owns queueing; workers own CPU and memory; storage owns throughput; the network owns paths; connectors own remote behavior; clients own result consumption. Without correlation, each dashboard can look locally plausible while the query remains unexplained.

Bad diagnosis creates regressions. Raising memory can hide a cardinality error and reduce concurrency. Increasing partitions can worsen scheduler overhead and small packets. Disabling backpressure can turn a bounded queue into an outage. Changing join strategy can fix one snapshot and fail on the next. Node replacement may appear to solve a transient source throttle.

A durable diagnostic artifact does more than close one incident. It identifies observability gaps, improves plan estimates and runbooks, supplies regression queries, calibrates capacity policy, and establishes whether a change improved critical path rather than shifting work.

## Prerequisites and Retrieval

Review shuffle in [LSDS-031](031-shuffle-architecture.md), fair/capacity scheduling in [LSDS-053](053-fair-and-capacity-scheduling.md), resource isolation in [LSDS-057](057-memory-cpu-and-i-o-isolation.md), scheduler diagnosis in [LSDS-060](060-diagnosing-scheduler-delay-and-resource-fragmentation.md), plan structure in [LSDS-061](061-distributed-logical-and-physical-plans.md), coordinator/worker state in [LSDS-062](062-coordinator-and-worker-architecture.md), exchange in [LSDS-063](063-exchange-operators.md), joins in [LSDS-064](064-distributed-hash-and-merge-joins.md), aggregation in [LSDS-065](065-partial-and-final-aggregation.md), vectorization in [LSDS-066](066-vectorized-execution-at-cluster-scale.md), runtime filtering in [LSDS-067](067-runtime-filtering-and-dynamic-pruning.md), AQE in [LSDS-068](068-adaptive-query-execution.md), and federation in [LSDS-069](069-federated-query.md).

You should understand DAGs, critical paths, task attempts, percentiles, query plans, cost/cardinality estimates, hash partitioning, backpressure, memory accounting, spill, TCP basics, clocks, traces, experiment design, and production safety.

## Learning Objectives

After this module, you should be able to:

1. preserve a complete, redacted, reproducible query evidence bundle before state expires;
2. decompose query wall time into lifecycle phases and execution critical path;
3. map logical nodes and plan revisions through fragments, stages, exchanges, tasks, attempts, workers, and endpoints;
4. quantify estimate error, task/partition skew, parallelism, amplification, throughput, spill, and retry waste;
5. distinguish busy, idle, blocked, backpressured, throttled, GC, disk, network, connector, and client behavior;
6. analyze scan, join, aggregation, sort, exchange, and adaptive-plan evidence by operator contract;
7. correlate exchange symptoms with socket/NIC/path evidence without overclaiming network causality;
8. rank hypotheses by predictions, disconfirming evidence, critical-path relevance, and scope;
9. design one-factor safe interventions, controls, rollback, and post-change verification; and
10. produce a durable causal handoff with findings, uncertainty, gaps, and follow-through.

## Core Exposition

### Start with the exact symptom and success criterion

Write the symptom in measurable terms: p95 latency rose from 90 to 260 seconds; query failed at 32 GiB peak memory; no progress for 12 minutes; output differed; source load exceeded policy; cost doubled. Include first/last occurrence, affected fingerprint/tenants, frequency, and comparison baseline.

Define success before tuning. A query may need lower latency, lower cost, bounded memory, predictable tails, reduced source impact, or restored correctness. Improving median while worsening p99 or fleet throughput can fail the actual objective.

Correctness and safety come first. Wrong results, duplicate/lost output, policy violations, or corrupt exchange artifacts trigger containment before performance experiments.

### Preserve evidence before it expires

Capture query instance/fingerprint, redacted SQL and parameters, user/tenant/workload, source snapshots, session properties, engine/build, coordinator and worker versions, connector versions, cluster/topology, resource group, and exact UTC interval. Export logical and distributed plans in machine-readable form, including estimates, dynamic filters, pushdowns, adaptive revisions, and final operators.

Retain query/stage/task-attempt events, selected attempts, operator metrics, worker/JVM/container/host metrics, storage/connector metrics, network endpoint/path metrics, logs, errors, traces, and client consumption timing. Record collection gaps and sampling/aggregation semantics.

Screenshots are supporting evidence, not a durable dataset. Store raw exports in governed artifacts with checksums, retention, redaction, and access control.

### Decompose the lifecycle

Use consistent boundary definitions:

$$T_{query}=T_{admission}+T_{planning}+T_{scheduling}+T_{execution}+T_{drain}.$$

Admission includes queue and resource-group delay. Planning includes parse/analyze/metadata/optimization. Scheduling includes dependency/resource/task-launch delay not already counted. Execution spans useful physical work and blocked/wait states. Drain includes result buffering and client consumption if the query completion contract waits for it.

Avoid overlapping double counts. Some engines label planning or scheduling differently; define local measurements rather than forcing dashboards into this equation. Compare instances only under the same boundary contract.

### Reconstruct the executed plan, not just the initial plan

Map logical operators to distributed fragments/stages separated by exchanges. Record distribution (`single`, hash, round-robin, broadcast, source), partition count, join build/probe, aggregation phases, sorts, scans, filters, connector pushdowns, and expected rows/bytes.

Then overlay adaptive revisions. A final plan may omit work performed and discarded under an earlier epoch. Record revision triggers, materialized inputs reused, old tasks canceled, extra shuffle, and chosen attempts. Diagnosis must explain the executed revision chain.

Verify the plan belongs to the exact query parameters, snapshot, session, and build. A visually similar explain from later is not evidence of what ran.

### Find the critical path through stage dependencies

Build a DAG with start/end times and dependency readiness. Parallel sibling stages overlap; summing their duration exaggerates latency. A stage with vast CPU may be off the critical path, while a small serial final stage controls completion.

For each stage, distinguish waiting for predecessors/resources, task launch, active execution, output materialization, and downstream drain. Identify the chain whose delay would move query completion. Optimization opportunities off this chain may reduce cost/capacity but not this query's wall time.

Counterfactual question: if this stage/task/operator were instantaneous, how much earlier could the query finish? That upper bound prevents chasing impressive but irrelevant metrics.

### Compare estimates and actuals at matching scope

For positive estimate $e$ and actual $a$, use multiplicative Q-error $\max(a/e,e/a)$. Handle zero separately: estimated zero with positive actual is an unbounded miss; both zero is exact for that scope. Compare rows and bytes, because width error affects network and memory even when cardinality is accurate.

Trace where error first becomes large: scan statistics, filter correlation, UDF selectivity, join containment, duplicate keys, nulls, or aggregation groups. Downstream errors may be inherited amplification, not independent estimator defects.

An estimate error is a plan-cause candidate only if it affected join order/distribution, partition count, memory, pruning, or another decision. Document the counterfactual plan with corrected observations.

### Analyze task distributions and attempt lineage

For comparable logical partitions, inspect task duration, input/output rows/bytes, CPU, blocked time, peak memory, spill, disk, network, GC, scheduler delay, and locality as distributions. Report count, median, p90/p95/p99, maximum, and maximum/median. With few tasks, list values; percentiles can mislead.

Separate logical partitions from attempts. Losing speculative attempts and retries consume resources but should not be added to selected result bytes. Report useful work and wasted retry/speculation work independently.

Long tasks with proportionally larger input suggest data/partition skew. Equal input with high CPU suggests value-dependent compute, contention, or hardware. Equal work with high elapsed/low CPU suggests blocking, I/O, network, GC pause, preemption, or throttling.

### Interpret busy, idle, and backpressured states directionally

An upstream task becomes backpressured when downstream cannot consume its output or buffers are unavailable. Therefore the first black/blocked upstream box may be the victim. Walk downstream until finding a consumer that is busy, slow, spilling, starved, or client-blocked.

Idle can mean no input because an upstream stage is slow, not spare capacity. Busy can include inefficient work. Blocked may reflect memory, splits, output buffers, remote source, downstream compute, or client drain. Use state definitions and operator-specific blocked reasons.

Over an interval, time fractions should be approximately consistent with wall time, subject to sampling. Do not interpret a short aggregate as a complete phase history.

### Diagnose scans and connectors

Separate split enumeration, source queue, open latency, first-byte latency, bytes/rows returned, wire versus decoded bytes, decompression, predicate/projection/dynamic-filter pruning, retries, throttling, and engine-side residual filtering.

Low throughput may be storage, connector serialization, remote quota, tiny requests, lack of parallelism, backpressure, or client-side decode. Compare source-service metrics and connector spans. High engine scan time with source idle can indicate local decode or downstream blocking.

Check snapshot and object/file distribution. One huge unsplittable object can create a scan tail. Many tiny files/splits can create scheduler and metadata overhead. Compare work considered, scheduled, opened, read, decoded, and retained.

### Diagnose joins, aggregates, and sorts

For joins, inspect actual build/probe rows and bytes, key distribution, build-side selection, join type, residual selectivity, hash-table memory, collisions, unmatched handling, spill, repartition/broadcast bytes, and output amplification. A many-to-many key can expand output even with balanced input bytes.

For aggregation, inspect partial reduction ratio, group cardinality/skew, state bytes per group, merge/final single points, spill, and hot keys. For sort, inspect input/output, runs, memory, spill bytes/passes, merge fan-in, comparison CPU, and final ordering bottleneck.

Operator peak memory must include decoded pages, hash/state structures, output buffers, revocable/non-revocable memory, network queues, native/off-heap allocations, and concurrency. Compressed input is not peak live memory.

### Diagnose exchange and flow control

Map producer stage/partition to consumer task and transport endpoint. Measure produced, accepted, buffered, sent, received, acknowledged, decoded, and consumed bytes; in-flight/queued buffers; credit/window; request count; remote/local reads; serialization/compression; blocked time; retries; and discarded attempt data.

If producers are blocked and consumers are CPU-bound or spilling, exchange backpressure is functioning. If producers have data, consumers are idle, queues grow or throughput collapses, then examine transport, endpoint, thread pools, connection limits, and receiver capacity.

Beware logical versus physical byte counts. Compression, framing, encryption, replication, retransmission, and retries make them differ. Align units and attempt scope before computing rates.

### Escalate to worker and JVM/runtime evidence

For implicated tasks and interval, inspect CPU utilization and run queue, steal/throttle, frequency, memory working set/limit, allocation rate, heap/native/off-heap, GC pause/time, page faults, NUMA, disk latency/queue/throughput, filesystem/object client, thread pools, and process/container restarts.

Compare the suspect worker with peers doing comparable partitions. Node-wide degradation across unrelated queries suggests infrastructure; only one operator or data value suggests workload. A replacement worker “fix” is weak evidence unless the original mechanism is identified.

Use profiles only under approved overhead and data-handling rules. Sampling can identify hot functions, locks, serialization, compression, hashing, or allocation, but one profile interval must map to the affected task.

### Require real evidence before naming the network

Exchange waiting is application-level evidence. Network causality needs endpoint/path evidence in the same interval: throughput near a known ceiling, send/receive queues, RTT change, retransmissions/loss, congestion-window behavior, ECN, drops, NIC errors, interface saturation, connection churn, DNS/TLS setup, load balancer behavior, or cross-zone/region routing.

Socket tools can show process-associated endpoints, queues, timers, retransmissions, RTT, and congestion state. Kernel counters show host-wide transport behavior but require baselines and query attribution. NIC and switch/path telemetry further separates host, rack, zone, and remote-service issues.

Retransmissions are not automatically root cause: establish rate, baseline, affected flows, direction, timing, and whether application throughput/RTT changed. Likewise full receive queues may be a slow consumer rather than path congestion.

### Include client and result-drain behavior

A query can finish computation yet remain running because the client fetches slowly, pauses, disconnects, or cannot deserialize results. Final-stage/output buffers backpressure the entire graph. Record time to first row, production rate, client fetch cadence, server buffered rows/bytes, output blocked time, and time to last acknowledgment.

`SELECT *` or unbounded exports can make result delivery the workload. Tuning joins will not remove client/network output volume. Use result limits, asynchronous exports, or destination-native writes only when they preserve the requested outcome.

### Account for concurrency and cluster context

Compare the query against contemporaneous tenant/cluster load: admission queue, active queries, memory pool, CPU, disk, network, source quotas, autoscaling, failures, deploys, and maintenance. A fast isolated reproduction does not disprove contention.

Use matched cohorts by fingerprint, snapshot/data volume, parameters, engine/config, cluster class, cache state, concurrency, and region. Report whether the incident is query-specific, worker-specific, source-specific, tenant-specific, or fleet-wide.

### Rank hypotheses by predictions and disconfirming evidence

Write a table mentally or explicitly: hypothesis; mechanism; predicted metrics/timeline; evidence for; evidence against; missing evidence; critical-path impact; safe test. Examples include underestimated build causes broadcast OOM, hot partition causes one large/long task, downstream spill causes upstream backpressure, source throttle causes low scan rate and remote throttle counters, or client drain causes final output blocking.

Prefer the narrowest hypothesis explaining the full chain. “Network” is too broad; “receiver worker `w17` had a 95-second GC pause, stopped draining exchange buffers, then producers backpressured” is testable. Keep alternatives when evidence is incomplete.

### Validate with a bounded causal intervention

Choose one change with a predicted signature: collect statistics, force a different join distribution, increase fine shuffle partitions, isolate a suspect worker, cap source concurrency, disable one adaptive rule, relocate within a zone, or use a fast result sink. Preserve correctness and compare a matched control.

Record change, query/data snapshot, configuration, load, sample count, result equivalence, resource/latency distributions, and rollback. One successful run is suggestive, not proof. Revert if tails, cost, concurrency, or correctness regress.

Avoid permanent hinting when the durable issue is stale statistics, bad partitioning, missing observability, connector behavior, or resource policy. The intervention validates the mechanism; the final fix should live at the responsible boundary.

### Produce a durable diagnostic handoff

Lead with symptom and confirmed scope. Include query/fingerprint, interval, environment, evidence links/checksums, lifecycle breakdown, executed revision chain, critical path, estimate table, task distributions, operator/exchange/worker/network/client findings, source consistency, and cluster context.

State conclusion as confirmed, strongly supported, plausible, or unproven. Show the causal chain and disconfirming evidence. Document intervention and result, correctness check, remaining risks, observability gaps, owner, rollback, and follow-up verification.

Redact SQL literals, credentials, host/user data, and sensitive plans according to policy. A diagnostic artifact should be shareable with the necessary responders without becoming a data leak.

## Definitions and Notation

Let lifecycle boundaries be $t_0\le\cdots\le t_5$ for admission, planning, scheduling, execution, and drain. Durations are differences under one clock model. If boundaries overlap in the engine, represent intervals explicitly instead of forcing an invalid sum.

Let stage DAG be $G=(V,E)$ with stage ready/start/end times. Query execution latency is determined by dependencies and resource delays; total worker effort $\sum_j t_j$ can greatly exceed elapsed time because tasks run in parallel.

For plan node $k$, let estimated/actual rows be $(e^r_k,a^r_k)$ and bytes $(e^b_k,a^b_k)$. Use Q-error only when both are positive and record zero cases separately. Let task metric vector for logical partition $i$ and selected attempt $a_i$ be $x_{i,a_i}$.

Let $b_i$ be input bytes and $t_i$ elapsed task time. The ratio $t_{max}/\operatorname{median}(t)$ is a tail indicator; compare $b_{max}/\operatorname{median}(b)$, CPU, blocked, spill, GC, disk, and TCP evidence to classify cause.

For an exchange interval, define logical producer bytes $B_p$, wire bytes $B_w$, receiver bytes $B_r$, consumed bytes $B_c$, and duration $\Delta t$. Throughput measures use matched endpoints/intervals. Differences require explaining compression, framing, broadcast, retry, retransmission, loss, or incomplete capture.

## Mechanisms, Invariants, or Proof Structure

### The plan-to-network diagnostic audit

1. Define symptom, correctness status, affected scope, time interval, baseline, and success criterion.
2. Preserve redacted SQL/parameters, snapshot, configuration/build/topology, all plan epochs, and raw events before expiry.
3. Decompose lifecycle using documented non-overlapping or explicitly overlapping boundaries.
4. Reconstruct logical-to-fragment-to-stage-to-exchange topology and identify execution critical path.
5. Compare estimates and actual rows/bytes at matching nodes; identify first consequential error and plan decision.
6. Analyze logical-partition/task-attempt distributions for work, time, CPU, blocking, memory, spill, I/O, GC, and retries.
7. Walk flow-control direction through scans, operators, exchanges, output, and client; locate where useful progress stops.
8. Correlate implicated workers/endpoints with source, runtime, disk, socket, NIC, and path evidence in the same interval.
9. Rank causal hypotheses, record counterevidence, and run one bounded correctness-preserving intervention with control/rollback.
10. Verify critical-path and fleet effect, archive evidence and uncertainty, fix observability gaps, and assign durable remediation.

### Causal sufficiency pattern

A strong finding connects:

$$\text{plan/input condition}\rightarrow\text{operator work/state}\rightarrow\text{task/exchange behavior}\rightarrow\text{resource symptom}\rightarrow\text{query outcome}.$$

For example: stale statistics underestimate build by 25×; optimizer selects broadcast; each worker constructs a 30 GiB hash table; memory pressure triggers repeated spill/GC; consumers stop draining; upstream exchange blocks; critical-path stage stretches by 140 seconds. Evidence must support each arrow, and an intervention such as refreshed statistics or partitioned join should change the predicted downstream signature.

### Attempt-aware conservation checks

Within declared encodings and operator semantics, compare selected-attempt inputs/outputs across boundaries. Unexpected row or byte gaps may arise from filtering, aggregation, compression, broadcast replication, retries, or missing telemetry. Reconcile them explicitly. Conservation is semantic, not raw byte equality.

## Alternatives and Trade-Offs

### Live debugging versus postmortem analysis

Live inspection reveals queues, thread states, sockets, and evolving backpressure but risks perturbation and evidence loss. Postmortem artifacts are reproducible and safer but may omit transient host/path state. Use low-overhead continuous telemetry plus approved targeted capture.

### Full tracing versus sampled correlation

Full per-task/page tracing offers detail but can overwhelm storage and leak query data. Sampling lowers cost but can miss tails. Prefer stable low-cardinality IDs, metrics/event logs for all work, and targeted exemplars/profiles for anomalous tasks.

### Query-specific versus node-wide metrics

Query/operator metrics map directly to the plan but may lack infrastructure cause. Node-wide metrics show resource contention but mix workloads. Diagnosis requires both, joined by worker and time, with workload context.

### Hints versus durable corrections

A hint is a fast causal test and emergency workaround. It can fossilize assumptions and bypass future optimizer improvements. Durable remedies include statistics, partition design, connector fixes, cost models, memory accounting, scheduling policy, network capacity, or client protocol.

### Reproduction versus production cohort

A controlled reproduction isolates mechanisms and permits profiling. It may omit production load, cache, network path, source state, and failures. Matched production cohorts establish external validity but have confounders. Use both when risk justifies them.

## Failure Modes and Misconceptions

- **“The slowest operator owns all latency.”** It may run off the critical path or overlap siblings.
- **“Task-time sum is query duration.”** Parallel work can sum to many times elapsed wall time.
- **“High Q-error is the root cause.”** Show the changed physical decision and causal downstream chain.
- **“One long task proves skew.”** Compare input/work, CPU, block, GC, disk, network, locality, and retries.
- **“Blocked means broken.”** Blocking/backpressure may be correct bounded flow control and point downstream.
- **“Exchange wait proves network.”** Require socket/NIC/path evidence correlated to endpoints and interval.
- **“High retransmits prove query impact.”** Establish baseline, flow attribution, rate, timing, RTT, and throughput.
- **“Low CPU means no bottleneck.”** The task may wait on I/O, network, locks, memory, source, scheduler, or client.
- **“High CPU means insufficient CPU.”** It may be duplicate work, bad plan, decoding, collisions, or unbounded output.
- **“The final adaptive plan is what ran.”** Earlier epochs may have consumed and discarded critical resources.
- **“A fast rerun disproves the incident.”** Cache, snapshot, load, worker, plan, source, or path may differ.
- **“Changing many settings saves time.”** It destroys causal attribution and complicates rollback.

## Worked Examples

### Example 1

**Separate lifecycle phases.** Queue is 12 seconds, planning 3, execution 240, and result drain 15, totaling 270 seconds under non-overlapping boundaries. Execution is 88.9% of latency, so an admission-only change cannot meet a 100-second target.

### Example 2

**Quantify consequential estimate error.** A join build is estimated at 2 million rows and produces 50 million: Q-error 25. The initial broadcast plan creates 28 GiB per worker and spills. A partitioned control removes replicated memory and spill, linking error to decision and consequence.

### Example 3

**Distinguish data skew from a sick worker.** Task times are 40, 42, 44, 45, and 210 seconds. If the last input bytes are also 4.8× median with normal CPU/GC/disk, data skew is supported. If bytes match but GC pause is 150 seconds only on that worker, node/runtime impairment is stronger.

### Example 4

**Walk backpressure downstream.** Scan tasks show high output-blocked time. The receiving aggregation task is busy, spills five times, and consumes slowly. NIC queues/retransmits are normal. The scan is a backpressure victim; aggregation state/spill is the causal focus.

### Example 5

**Find a client bottleneck.** All compute stages finish by 10:05, but query completion is 10:19. The final output operator is blocked, server buffers remain full, and the client fetches one page every 30 seconds. A fast sink control completes at 10:06. Join tuning cannot recover the 13-minute drain.

### Example 6

**Correlate actual network degradation.** One exchange flow's RTT rises from 2 to 40 ms, retransmission rate from 0.1% to 8%, send queue grows, receiver is idle, and interface/path telemetry shows drops during the same 90 seconds. Peer flows on the path regress. This supports path loss more strongly than exchange wait alone.

### Example 7

**Identify scan metadata overhead.** A scan reads only 4 GiB but enumerates 2 million files/splits, spending 160 seconds in metadata/scheduling and 18 seconds transferring data. Compaction or manifest pruning targets the critical mechanism; adding storage bandwidth does not.

### Example 8

**Account adaptive waste.** Epoch 1 shuffles 600 GiB before AQE changes join strategy. Epoch 2 reuses only 100 GiB and discards/cancels the rest. A dashboard showing epoch 2's 250 GiB understates actual 850 GiB work. Revision-chain accounting explains cost and transition delay.

### Example 9

**Use a one-factor intervention.** Matched runs differ only by refreshed table statistics. Plan changes from broadcast to partitioned join, per-worker peak falls from 30 to 8 GiB, spill disappears, upstream block falls, and p95 drops. Results match. This strongly supports the estimate/plan/memory chain while still requiring broader cohort validation.

### Example 10

**Execute diagnostic arithmetic.**

<!-- bijux-verify: {"id":"query-diagnostic-metrics","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"q_error=25.0\nmedian_task_seconds=44\nskew_ratio=4.77\nlifecycle_seconds=270\nexecution_share_percent=88.9\n","stderr":""}} -->
```python
import statistics

estimated_rows = 2_000_000
actual_rows = 50_000_000
q_error = max(actual_rows / estimated_rows, estimated_rows / actual_rows)

task_seconds = [40, 42, 44, 45, 210]
median_task = statistics.median(task_seconds)
skew_ratio = max(task_seconds) / median_task

queue_seconds = 12
plan_seconds = 3
execution_seconds = 240
drain_seconds = 15
lifecycle = queue_seconds + plan_seconds + execution_seconds + drain_seconds

print(f"q_error={q_error:.1f}")
print(f"median_task_seconds={median_task:g}")
print(f"skew_ratio={skew_ratio:.2f}")
print(f"lifecycle_seconds={lifecycle}")
print(f"execution_share_percent={100 * execution_seconds / lifecycle:.1f}")
```

These summary values guide investigation; classifications still require aligned operator, attempt, and infrastructure evidence.

## Cross-Program Connections

- **Database systems:** plans, estimates, operator semantics, statistics, joins, aggregates, sorts, and snapshots locate logical causes.
- **Distributed systems:** DAGs, attempts, retries, speculation, backpressure, partial failure, clocks, and recovery locate execution causes.
- **Operating systems:** CPU scheduling, memory, GC/runtime, page faults, disks, filesystems, sockets, and containers locate worker causes.
- **Network engineering:** endpoints, queues, RTT, loss, retransmission, congestion, NICs, paths, and topology locate transport causes.
- **Data engineering:** files, splits, pruning, compression, partitions, connectors, and source quotas locate input causes.
- **Platform engineering:** admission, resource groups, multi-tenancy, deploys, autoscaling, telemetry, retention, and access enable diagnosis.
- **Reliability engineering:** symptom definition, hypothesis testing, containment, runbooks, canaries, rollback, and follow-up turn evidence into action.
- **Security and governance:** redaction, least-privilege diagnostics, artifact access/retention, tenant isolation, and audit prevent observability leaks.

## References

1. Trino. [EXPLAIN.](https://trino.io/docs/current/sql/explain.html) Current logical/distributed/IO plan formats, fragments, exchanges, and distribution descriptions.
2. Trino. [EXPLAIN ANALYZE.](https://trino.io/docs/current/sql/explain-analyze.html) Current distributed-plan execution statistics and verbose operator diagnostics.
3. Trino. [Web UI.](https://trino.io/docs/current/admin/web-interface.html) Current query states, timelines, stage/task views, JSON detail, blocking guidance, and query history.
4. Trino. [Monitoring with JMX.](https://trino.io/docs/current/admin/jmx.html) Current JVM, cluster, query, task, memory, latency, input, and connector metrics.
5. Trino. [Metrics with OpenMetrics.](https://trino.io/docs/current/admin/openmetrics.html) Current authenticated coordinator/worker metric exposure and selection.
6. Apache Spark. [Monitoring and Instrumentation.](https://spark.apache.org/docs/latest/monitoring.html) Current application/stage/task/executor/SQL UI, event log, history server, REST, and metrics interfaces.
7. Apache Spark. [Web UI.](https://spark.apache.org/docs/latest/web-ui.html) Current jobs, stages, tasks, executors, SQL plans, environment, storage, and diagnostic fields.
8. Apache Spark. [SQL Performance Tuning.](https://spark.apache.org/docs/latest/sql-performance-tuning.html) Current statistics, runtime plans, joins, partitions, AQE, skew, and performance controls.
9. Apache Flink. [Metrics.](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/metrics/) Current task bytes, busy/idle/backpressured time, buffers, mailbox, and runtime metric definitions.
10. Apache Flink. [Monitoring Back Pressure.](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/monitoring/back_pressure/) Current flow direction, output-buffer basis, task-state interpretation, aggregation, and UI guidance.
11. OpenTelemetry. [Database Client Span Semantic Conventions.](https://opentelemetry.io/docs/specs/semconv/db/database-spans/) Current operation, system, namespace, server/network, query summary/text, parameter, response, error, and cardinality guidance.
12. Linux Kernel. [SNMP Counter Documentation.](https://docs.kernel.org/networking/snmp_counter.html) Current TCP/IP counters, retransmission, congestion, listen queues, loss, and counter interpretation.
13. Linux man-pages. [ss(8).](https://man7.org/linux/man-pages/man8/ss.8.html) Current socket, queue, process, timer, retransmission, RTT, congestion, and endpoint inspection interface.

## Exercises

### Exercise 1

Design a complete evidence bundle and diagnostic workflow for a query whose p95 tripled after a release. Include identity, plan epochs, lifecycle, attempts, operators, workers, network, client, cluster context, redaction, hypotheses, and intervention.

### Exercise 2

A node estimates 800,000 rows and produces 72 million; six task times are 31, 32, 33, 35, 36, and 198 seconds. Compute Q-error, median, and max/median. Explain what additional evidence separates data skew, compute skew, GC, disk, and network.

### Exercise 3

Diagnose `scan -> exchange -> aggregation -> result` where scans are backpressured, one aggregation spills, and the client is intermittently slow. Build the timeline, identify competing causal chains, and propose two one-factor tests.

### Exercise 4

Design a network escalation for a slow exchange. Include endpoint mapping, query interval, logical/wire bytes, queues, RTT, retransmits/loss, NIC/path evidence, baselines, confounders, privacy, and stopping conditions.

### Exercise 5

Write the outline of a durable diagnostic handoff for an AQE query that retried tasks and changed join strategy. Include claim strength, evidence, discarded work, verification, gaps, remediation ownership, and rollback.

## Answers to the Exercises

### Answer 1

Capture query instance/fingerprint, redacted SQL/parameters, user/tenant, snapshots, UTC interval, session/resource group, engine/connector/build, worker topology, release/control cohorts, initial/all adaptive/final plans, estimates, stage DAG, task logical partitions and all attempts, selected commits, operator metrics, dynamic filters/pushdowns, worker/JVM/container/disk metrics, storage/source metrics, endpoint/socket/NIC/path metrics, client fetch timing, cluster workload/deploys/failures, logs/traces, collection definitions, raw artifact checksums, retention, and gaps. Verify correctness first. Decompose lifecycle, find critical path, compare matching estimates/actuals, analyze distributions and retry waste, walk backpressure downstream, correlate suspect tasks to host/path evidence, rank mechanisms with counterevidence, and run one bounded change against a matched control. Verify results, p50/p95/p99, critical path, cost/fleet impact, and rollback; archive a redacted causal chain and uncertainty.

### Answer 2

Q-error is $72{,}000{,}000/800{,}000=90$. Sorted durations have median $(33+35)/2=34$ seconds. Maximum/median is $198/34\approx5.82$. Compare input/output rows and bytes plus key frequencies: proportionally high work supports data skew. Equal bytes but high CPU/instructions/hot functions supports compute/value skew. Equal work with long GC pauses/allocation/heap pressure supports runtime memory. High disk latency/queue/spill or slow local reads supports disk. Growing socket queues, RTT/loss/retransmits, NIC/path anomalies, low CPU, and idle receiver/sender evidence supports network. Also check scheduler delay, preemption, locality, source throttle, and whether 198 seconds belongs to a retry/losing attempt.

### Answer 3

Align operator states and bytes over time. Chain A: aggregation group cardinality or skew exceeds memory, spill slows consumption, exchange buffers fill, and scans backpressure. Chain B: slow client fills result buffers, final output blocks aggregation, which stops draining exchange, eventually backpressuring scans; spill may be secondary because state lives longer. Identify when client fetch pauses, result buffers fill, aggregation spill begins, consumer throughput falls, and scan blocking rises. Test one: route identical output to an approved fast sink while holding plan/data/load constant; disappearance of downstream/upstream blocking supports client drain. Test two: keep the client fixed but force bounded partitioned/partial aggregation or increase fine partitions; disappearance of spill and improved consumer throughput supports aggregation pressure. Compare exact results, critical path, memory, spill, output timing, and cluster cost; roll back each independently.

### Answer 4

Map exchange stage/task attempts to producer/consumer workers, IPs/ports/connection IDs, topology, and exact UTC interval. Reconcile logical producer, framed/compressed/encrypted wire, receiver, consumed, retry, broadcast, and discarded bytes. Collect send/receive queues, throughput, request sizes, connection churn, RTT, congestion window where available, retransmit/loss/ECN, socket timers, NIC bytes/drops/errors/queue saturation, host CPU/interrupt pressure, and switch/path/zone telemetry. Compare same hosts/path before/after and peer flows, plus application consumer CPU/GC/disk/backpressure. Redact addresses or query fields under policy and restrict raw captures. Escalate when correlated endpoint/path anomalies predict the throughput collapse and alternatives are weaker; stop packet/profile capture at approved duration/overhead/data bounds. Do not call exchange waiting a network incident absent transport evidence.

### Answer 5

Include symptom/scope/baseline, query and fingerprint, snapshot/config/build/topology, correctness status, evidence artifact links/checksums, lifecycle and critical path, initial/revision/final plan hashes, AQE triggers, state reused, tasks canceled, all attempts and selected commits, useful versus discarded shuffle/CPU, estimates versus actuals, operator/task distributions, worker/network/client and concurrency findings. State the conclusion's strength and causal arrows, evidence against alternatives, and gaps. Describe the one-factor intervention/control, exact result comparison, latency/resource/tail/fleet outcome, and sample limits. Assign durable remediation—statistics, AQE transition accounting, memory/partition policy, network, connector, or telemetry—to an owner with verification date. Document rule/hint rollback and conditions for immediate reversal.
