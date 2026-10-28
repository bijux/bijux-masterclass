---
module_id: LSDS-098
program: Large-Scale Data Systems Engineering
level: 2
module_number: 98
title: Capacity Planning for Batch and Streaming
status: complete
last_verified: 2026-09-04
---

# Capacity Planning for Batch and Streaming

## One-Page Review

### Governing question

How should an engineer translate uncertain batch volumes, streaming arrival rates, service demands, state, deadlines, failure recovery, maintenance, and dependency limits into an executable capacity plan with enough headroom, lead time, and feedback to meet objectives economically?

### Essential definitions

- **demand forecast** estimates future logical work by class, horizon, distribution, and scenario.
- **service demand** is measured resource busy time or consumption per correct unit of workload at a named operating point.
- **capacity envelope** is the tested region of workload, resources, configuration, and service levels within which objectives hold.
- **headroom** is deliberately unused effective capacity reserved for bursts, uncertainty, failures, and recovery.
- **batch deadline capacity** is the effective parallel capacity required to finish all required work by its deadline.
- **sustainable streaming capacity** is the correct output rate maintainable without unbounded backlog, latency, state, error, or resource growth.
- **catch-up capacity** is output capacity above continuing input that drains recovery backlog within a target time.
- **critical path** is the longest precedence-constrained sequence that additional parallel resources cannot shorten directly.
- **parallelism ceiling** is the smallest operator, partition, key, connection, quota, or scheduler bound that limits usable concurrency.
- **failure domain reserve** is capacity retained across the declared node, rack, zone, or dependency loss scenario.
- **provisioning lead time** spans forecast detection, approval, quota, procurement, deployment, data movement, validation, and readiness.
- A **capacity plan** is versioned intent plus assumptions, scenarios, resource mapping, triggers, owners, and validation evidence.

### Central model, mechanism, or theorem

For workload class $i$ with rate $\lambda_i$ and measured demand $d_{ir}$ on resource $r$, required capacity units $m_r$ at target utilization $u_r^*$ satisfy:

$$m_r\ge \frac{\sum_i \lambda_i d_{ir}}{u_r^*}.$$

This demand bound must be combined with memory/state, partition/key parallelism, storage/request, network, dependency, placement, and failure-domain bounds; the maximum binding requirement governs, not an average of them.

For batch work $W_r$ due within effective processing window $H$, an ideal resource bound is $m_r\ge W_r/(H u_r^*)$, but precedence, startup, skew, shuffle, checkpoint, commit, and maintenance extend elapsed time. For streaming input $\lambda$, outage/recovery backlog $Q$, and catch-up target $R$:

$$\mu_{recovery}\ge \lambda+Q/R.$$

If an outage lasts $F$ while input continues, $Q\approx\int_F\lambda(t)dt$ before loss, expiry, or replay adjustments. Capacity must also satisfy the relevant peak/forecast scenario. Autoscaling can allocate within a planned envelope; it cannot create quota, keys, partitions, dependency capacity, or instant state transfer.

### Critical invariants

- Forecast units map unambiguously to measured workload units and correct completions.
- Service demand comes from representative, unsaturated or explicitly modeled operating regions and is versioned with code/data/configuration.
- Every CPU, memory, storage, IOPS/request, network, state, scheduler, partition, and dependency constraint is evaluated separately.
- Batch timing includes reads, startup, queueing, shuffle, spill, checkpoints, retries, durable commits, validation, and required maintenance.
- Streaming capacity includes event-time latency, backlog, watermarks, state, checkpoints, sinks, recovery, and catch-up while new input continues.
- Headroom is tied to named uncertainty, burst, maintenance, or failure scenarios rather than an unexplained percentage.
- Replicas and standby resources are discounted for correlated failure, placement, rebuild, quorum, and usable throughput.
- Autoscaling minimum, maximum, reaction time, stabilization, quotas, and indivisible parallelism ceilings are explicit.
- Forecast and demand uncertainty produce scenarios/ranges; point estimates are not presented as guarantees.
- Plans have review dates, leading indicators, thresholds, owners, provisioning lead times, rollback, and load-test evidence.

### Common failures

Common failures include projecting bytes while work is driven by records or keys; extrapolating from saturated throughput; assuming linear scale beyond a tested envelope; dividing total work by cores while ignoring the critical path; sizing batch only for average daily volume; sizing streams only for average input; forgetting backlog catch-up after recovery; counting replicas as fully usable; reserving CPU but not memory, state, network, IOPS, requests, or downstream quotas; treating autoscaling as infinite instantaneous capacity; increasing workers beyond source partitions or hot keys; applying one headroom number to every risk; ignoring provisioning lead time; double-counting correlated safety factors; and never reconciling forecasts with actual demand.

### Compact example

A stream averages 240,000 events/s and plans for a 1.6-times peak, or 384,000 events/s. Measured CPU demand is 120 microseconds/event. At a 65% target utilization, the CPU lower bound is $384,000(0.000120)/0.65=70.9$, so round to at least 71 effective cores before placement and failure reserve. A ten-minute outage accumulates 144 million events at the average rate; draining that backlog in 30 minutes while input continues requires 320,000 events/s, below the peak scenario. Forty million live keys at 320 bytes/key, 1.4 runtime overhead, and two retained copies require 33.38 GiB; at a 60% memory target, plan at least 55.63 GiB of effective state memory before process/system reserves.

### Connections

[LSDS-049](049-backpressure-across-operators.md) supplies streaming stability, [LSDS-059](059-autoscaling-data-clusters.md) supplies control behavior, [LSDS-088](088-backfill-isolation.md) supplies competing-work isolation, [LSDS-090](090-designing-recovery-for-multi-hour-and-multi-day-jobs.md) supplies recovery deadlines, [LSDS-091](091-partition-count-and-task-granularity.md) supplies divisibility bounds, and [LSDS-097](097-cluster-benchmarking.md) supplies measured demands and envelopes.

## Governing Question

Capacity is not a node count. It is a claim that a specific resource topology can execute a forecast workload, preserve correctness, satisfy latency/deadline/recovery objectives, and stay within cost and failure constraints. The same 100 workers may be abundant for a scan and useless for one hot keyed operator.

The governing question is how to join forecasting and performance evidence into a plan whose assumptions can be monitored and whose resource requests can be provisioned before risk materializes.

## Why This Matters

Underprovisioning causes missed batch windows, streaming backlog, checkpoint failure, sink throttling, overload feedback, and recovery that never catches up. Overprovisioning hides inefficient work, consumes scarce quotas, and raises fixed cost. Both are often caused by treating historical cluster size as capacity.

Data workloads also change shape. Compression, schema, key cardinality, join multiplicity, state retention, file sizes, code paths, and downstream limits can shift demand faster than logical bytes grow. A durable plan models workload classes and service demands, then continuously reconciles them.

## Prerequisites and Retrieval

Review streaming pressure in [LSDS-049](049-backpressure-across-operators.md), dynamic resources in [LSDS-052](052-static-and-dynamic-allocation.md), autoscaling in [LSDS-059](059-autoscaling-data-clusters.md), state recovery in [LSDS-085](085-checkpoint-based-recovery.md), backfill isolation in [LSDS-088](088-backfill-isolation.md), long-running recovery in [LSDS-090](090-designing-recovery-for-multi-hour-and-multi-day-jobs.md), resource bottlenecks in [LSDS-092](092-memory-pressure-spill-and-garbage-collection.md), and benchmarking in [LSDS-097](097-cluster-benchmarking.md).

You should understand rates, quantiles, time series, service demand, utilization, queues, critical paths, batch DAGs, keyed streaming state, checkpoints, retries, partitioning, quotas, failure domains, autoscaling, cost accounting, and forecast uncertainty.

Retain workload class/tenant/pipeline/version; logical and physical volumes; event/query/job rates; seasonality, bursts, growth, and launches; keys/state/windows/retention; measured demand by resource; plans/configuration; task/operator/partition distributions; dependency quotas/latency; backlog/watermarks; checkpoint/recovery; placements/failures; allocated/usable/billed resources; forecast model/version; scenario; confidence/range; approval/provisioning status; and actual-versus-plan error.

## Learning Objectives

After this module, you should be able to:

1. define forecast workload units that map to performance measurements;
2. separate organic growth, known events, seasonality, bursts, and uncertainty;
3. derive resource-demand lower bounds at target utilization;
4. size batch work against deadlines and critical-path limits;
5. size streaming work for peaks, state, checkpoints, failure, and catch-up;
6. combine heterogeneous resource, parallelism, placement, and dependency constraints;
7. select explicit headroom and failure-domain policies without double counting;
8. model autoscaling reaction, bounds, state movement, and quota lead time;
9. validate plans with benchmark, overload, and recovery experiments; and
10. reconcile forecasts and triggers through a versioned operational process.

## Core Exposition

### Define the service and objective boundary

Name the pipelines, tenants, data products, regions, failure domains, and downstream services covered. State batch deadlines, freshness/event-time latency, availability, recovery time/point, correctness, and cost objectives.

Decide whether capacity is dedicated, pooled, preemptible, elastic, reserved, or shared. A shared pool needs allocation and admission rules, not just total resources.

### Forecast workload drivers

Forecast the variables that create work: records, encoded/decoded bytes, queries, keys, joins, windows, state churn, files, requests, and external calls. Segment classes with different service demands.

Model organic trend, day/week/year seasonality, launches, backfills, retention changes, customer migrations, and adversarial bursts. Produce base, expected, high, and failure scenarios across a horizon longer than provisioning lead time.

### Establish measured service demand

Use representative benchmark and production observations to estimate CPU-seconds/event, bytes read/written, requests, shuffle/network, memory/state, and dependency calls per correct unit. Record distributions and workload mix.

Measure in a stable region below overload because saturation introduces queueing, retries, spill, and nonlinear demand. Also test the knee and overload separately to define the safe envelope and failure behavior.

### Model each resource center

For resource $r$, sum $\lambda_i d_{ir}$ across classes, divide by target utilization, and compare with physical/allocatable capacity. Repeat for CPU, memory, local disk, object storage throughput/requests, network, coordination, connections, and external services.

Some constraints are stocks rather than rates: resident state, cached datasets, shuffle spill, checkpoints, and metadata. Apply capacity, retention, replication, fragmentation, and rebuild factors with clear boundaries.

### Size batch deadlines

Convert each batch class into required work by resource over the available window after upstream readiness and before downstream deadline. Account for stage precedence, critical paths, skew, task granularity, startup, scheduler delay, exchange, spill, commit, validation, and cleanup.

Use historical/benchmark task distributions to simulate or bound schedules rather than assuming perfect division. Concurrent jobs require queue and interference policies. Reserve time and capacity for retries and planned maintenance.

### Size streaming steady state

Choose a forecast rate at the objective-relevant horizon: instantaneous microburst, multi-minute peak, or sustained high interval. Multiply class rates by service demands and verify the result against target utilization and parallelism.

Check backlog slope, event-time latency, watermark lag, busy/backpressured time, state growth, checkpoint duration/failure, and sink commits. A low mean CPU does not prove capacity when one key, partition, network link, or dependency is binding.

### Calculate recovery catch-up

Estimate backlog accumulated during detection, failover, restore, rescale, and dependency outage. Catch-up output must exceed continuing input by $Q/R$. Include replays, retries, checkpoint/state restoration, cache warming, and output idempotency.

Test whether recovery capacity can run without starving foreground work or overwhelming storage/sinks. If not, change the catch-up target, retain more reserve, isolate replay, or add admission/degradation policy.

### Plan state and checkpoint capacity

Forecast live keys, windows, timers, accumulator bytes, indexes, allocator/storage overhead, replication, and retention. Include state migration and compaction peaks, not only steady resident bytes.

Checkpoint capacity includes change rate, snapshot bytes, duration, concurrent checkpoints, storage bandwidth/requests, retained copies, and restore throughput. Establish baseline capacity with checkpointing enabled.

### Respect parallelism ceilings

Workers cannot exceed useful source partitions, key groups, unsplittable hot keys, operator maximum parallelism, sink shards/connections, or barrier constraints. Estimate usable rather than purchased parallelism.

Remove or redesign ceilings when feasible: split sources, repair skew, preaggregate, shard sinks, or raise governed quotas. Otherwise capacity plans must accept the ceiling and adjust objectives.

### Add failure-domain reserve

Define required survival: one worker, rack, zone, coordinator, network path, or dependency degradation. Recompute placement and resource bounds after the loss, including rebuild/recovery traffic and quorum constraints.

N+1 notation is inadequate when nodes differ, reservations fragment, state is placed unevenly, or a zone contains more than one unit. Prove effective capacity in the exact topology.

### Select headroom explicitly

Allocate headroom to named sources: forecast error, burst absorption, failure, maintenance, recovery, autoscaling delay, and measurement uncertainty. Prefer scenario recomputation over multiplying several opaque percentages.

Avoid double counting the same peak in both forecast and headroom. Conversely, do not let an expected-case confidence interval erase a known launch or correlated failure scenario.

### Model elasticity and lead time

Autoscaling has observation windows, thresholds, stabilization, provisioning, scheduling, state transfer, cache warming, and quota ceilings. Its minimum protects readiness; its maximum is a capacity assertion that must be provisionable.

Keep static reserve for work that arrives faster than scaling. Forecast quotas, IPs, disks, object request rates, licenses, and downstream allocations through acquisition lead time. Rehearse scale-up and scale-down correctness.

### Plan shared-cluster governance

Translate resource intent into requests/limits, queues, priorities, reservations, preemption, concurrency, and admission controls. Separate guaranteed from opportunistic capacity. Backfills and experiments must not consume recovery reserve.

Measure fragmentation and stranded resources by shape. A pool with enough total CPU and memory may not place required executor/pod shapes or failure-domain replicas.

### Validate nonlinear behavior

Load test from underload through the knee and beyond rated capacity. Observe latency, backlog, errors, retries, GC/spill, checkpoints, autoscaling, load shedding, and recovery. Confirm degradation fails predictably instead of cascading.

Repeat with representative data shape, cold/warm state, shared load, and failures. A spreadsheet calculation is a hypothesis until exercised within the relevant envelope.

### Optimize cost after feasibility

First find configurations that meet correctness and objectives. Then compare useful work per billed cost while retaining headroom and failure constraints. Evaluate larger versus more nodes, reserved versus elastic, storage/network/request cost, and standby utilization.

Do not monetize away hard reliability constraints. Record opportunity cost for scarce shared capacity and the cost of missed deadlines/backlog, not just provider charges.

### Operate the plan as a control loop

Version forecasts, demand coefficients, scenarios, allocations, and decisions. Monitor leading indicators: rate/volume forecast error, demand drift, saturation margin, backlog, state, checkpoint/recovery time, quota, and provisioning progress.

Set review cadence and trigger thresholds early enough to cover lead time. Reconcile actuals, explain error, update models, and retire unused capacity or obsolete assumptions.

## Definitions and Notation

Let:

- $\lambda_i$ be forecast correct workload rate for class $i$;
- $d_{ir}$ be measured demand of class $i$ on resource $r$ per correct unit;
- $m_r$ be provisioned effective capacity units for resource $r$;
- $u_r^*$ be target utilization after explicit reserve policy;
- $W_r$ be total batch demand on resource $r$ and $H$ its effective processing window;
- $\mu$ be sustainable correct streaming output capacity;
- $Q$ be recoverable backlog and $R$ the target catch-up duration;
- $F$ be outage/detection/restore duration while input may accumulate;
- $S$ be live logical state bytes and $a_s$ runtime/storage/replication amplification;
- $p$ be useful parallelism bounded by partitions, keys, operators, and dependencies; and
- $L$ be end-to-end provisioning lead time.

Rates, stocks, concurrency, and elapsed time are not interchangeable. Effective capacity discounts reserved system work, placement, failure loss, and nonparallelizable work. Demand coefficients are conditional on workload/configuration and must not be extrapolated blindly.

## Mechanisms, Invariants, or Proof Structure

### Resource-demand bound

Class $i$ consumes $\lambda_i d_{ir}$ units of resource $r$ per second. Summing classes gives offered resource work. Dividing by target utilization gives a lower bound on effective units, provided demand is measured consistently and the system stays in the modeled region.

### Batch lower bounds

Any schedule needs at least $W_r/(m_ru_r^*)$ time at each resource and at least its critical-path duration. The larger lower bound applies; skew, dependencies, setup, queueing, failure, and commit can only increase realized completion time.

### Recovery conservation

If backlog $Q$ must drain in $R$ while new input arrives at $\lambda$, excess service $\mu-\lambda$ must be at least $Q/R$. Thus $\mu\ge\lambda+Q/R$. Loss, expiry, deduplication, and replay change $Q$ only when explicitly modeled.

### Multi-constraint maximum

CPU, memory, storage, network, state, parallelism, quota, placement, and dependency calculations each impose a feasibility constraint. A configuration is feasible only if all hold, so the binding maximum or incompatible shape governs.

### Forecast feedback

Compare observed workload and demand with the versioned forecast, decompose error into volume, mix, demand, placement, and events, then update coefficients/scenarios before lead time expires. Monitoring without a decision trigger is not a capacity process.

## Alternatives and Trade-Offs

| Lever | Strength | Cost or limitation |
|---|---|---|
| Dedicated reserve | Immediate predictable headroom | Idle cost and fragmentation |
| Shared pooled reserve | Higher utilization across workloads | Admission, priority, and correlated-demand risk |
| Horizontal scale | More parallel slots/failure spread | Partition, network, scheduler, and state-movement limits |
| Vertical scale | Fits large state/tasks and reduces fan-out | Larger failure unit and SKU/availability constraints |
| Autoscaling | Adapts allocation to demand | Delayed, bounded, quota-dependent, and stateful |
| Admission/load shedding | Protects critical service | Deferred/rejected work and product policy |
| Backfill isolation | Prevents historical work from consuming foreground reserve | Longer backfill and duplicated capacity |
| Preaggregation/data redesign | Reduces service demand structurally | Engineering complexity and semantic constraints |
| Higher target utilization | Lowers nominal resource cost | Nonlinear latency and reduced failure/burst margin |
| Longer deadline/catch-up target | Reduces required peak capacity | Freshness and recovery objectives weaken |

## Failure Modes and Misconceptions

1. **Historical node count is capacity.** Workload, demand, topology, and constraints may have changed.
2. **Bytes predict every pipeline.** Records, keys, state, compression, joins, and requests may dominate.
3. **Peak throughput equals safe throughput.** Saturation and short bursts violate stable envelopes.
4. **Batch work divides perfectly by cores.** DAG precedence, skew, and critical paths remain.
5. **Average input sizes a stream.** Peaks, bursts, and catch-up drive objectives.
6. **Recovery begins after traffic stops.** New input usually continues while backlog drains.
7. **Replicas are spare capacity.** Quorum, placement, rebuild, and failure requirements consume them.
8. **CPU headroom covers all risk.** Memory, state, I/O, network, requests, and dependencies bind independently.
9. **More workers always help.** Keys, partitions, state groups, sinks, and quotas cap parallelism.
10. **Autoscaling is instant and unlimited.** Detection, provisioning, rescale, warming, and quotas delay it.
11. **One safety factor is rigorous.** It hides scenarios and encourages double counting.
12. **A forecast interval includes known launches.** Planned discontinuities need explicit scenarios.
13. **Checkpointing is overhead to exclude.** Production capacity must carry it.
14. **Total pool resources guarantee placement.** Shape and failure-domain fragmentation can block work.
15. **A plan is finished when approved.** Forecast and demand drift require reconciliation and triggers.

## Worked Examples

### Example 1

At 384,000 events/s and 120 microseconds/event, offered CPU demand is 46.08 core-seconds/s.

### Example 2

At 65% target utilization, 46.08/0.65 requires 70.9, rounded up to 71 effective cores.

### Example 3

A ten-minute outage at 240,000 events/s produces 144 million queued events before replay adjustments.

### Example 4

Draining 144 million events over 1,800 seconds needs 80,000 events/s above continuing input, or 320,000 events/s total.

### Example 5

Forty million keys at 320 bytes/key with 1.4 overhead and two copies occupy about 33.38 GiB.

### Example 6

At a 60% state-memory target, the unrounded state estimate implies 55.63 GiB effective state memory before other process reserves.

### Example 7

A batch requires 120 core-hours within two hours at 70% planned utilization, imposing at least 86 effective cores before critical-path effects.

### Example 8

Two hundred workers cannot accelerate a stage with 64 indivisible source partitions beyond 64 useful concurrent tasks.

### Example 9

A zone-loss scenario is recomputed after removing that zone's capacity and adding restore/network/sink demand; it is not represented by an arbitrary 20% factor.

### Example 10

The executable fixture recomputes peak rate, CPU, recovery, and state-memory bounds from the compact example.

<!-- bijux-verify: {"id":"batch-stream-capacity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"average_events_s=240000\nplanned_peak_events_s=384000\ncpu_demand_cores=46.08\ncpu_effective_cores=71\noutage_backlog_events=144000000\ncatchup_events_s=80000\nrecovery_output_events_s=320000\nstate_gib=33.38\nstate_effective_memory_gib=55.63\n","stderr":""}} -->
```python
import math

average_rate = 240_000
peak_factor = 1.6
cpu_seconds_per_event = 120e-6
cpu_target = 0.65
outage_seconds = 10 * 60
catchup_seconds = 30 * 60
keys = 40_000_000
bytes_per_key = 320
state_overhead = 1.4
state_copies = 2
memory_target = 0.60

peak_rate = int(average_rate * peak_factor)
cpu_demand = peak_rate * cpu_seconds_per_event
cpu_cores = math.ceil(cpu_demand / cpu_target)
backlog = average_rate * outage_seconds
catchup_rate = backlog // catchup_seconds
recovery_rate = average_rate + catchup_rate
state_gib = keys * bytes_per_key * state_overhead * state_copies / 2**30

print(f"average_events_s={average_rate}")
print(f"planned_peak_events_s={peak_rate}")
print(f"cpu_demand_cores={cpu_demand:.2f}")
print(f"cpu_effective_cores={cpu_cores}")
print(f"outage_backlog_events={backlog}")
print(f"catchup_events_s={catchup_rate}")
print(f"recovery_output_events_s={recovery_rate}")
print(f"state_gib={state_gib:.2f}")
print(f"state_effective_memory_gib={state_gib / memory_target:.2f}")
```

## Cross-Program Connections

- **Forecasting and statistics:** trends, seasonality, scenarios, error bands, change points, and model reconciliation characterize demand uncertainty.
- **Performance engineering:** benchmarks, service demands, saturation curves, critical paths, and bottleneck shifts map work to resources.
- **Queueing:** utilization, bursts, backlog, latency, recovery catch-up, and admission determine stability.
- **Distributed systems:** partitions, skew, state, checkpoints, placement, correlated failures, retries, and recovery limit usable capacity.
- **Platform engineering:** quotas, requests/limits, queues, autoscalers, topology, provisioning, and observability implement resource intent.
- **Data architecture:** schemas, retention, compression, file layout, key cardinality, and table maintenance change workload demand.
- **Reliability:** failure-domain reserve, overload behavior, graceful degradation, recovery objectives, and drills define headroom.
- **Economics:** fixed/elastic resources, idle reserve, scarce quota, transfer/requests, licenses, and missed-objective cost shape choices.

## References

1. Google, [Site Reliability Engineering: Introduction](https://sre.google/sre-book/introduction/). Describes demand forecasting, organic/inorganic growth, capacity planning, load testing, and provisioning.
2. Google, [Production Services Best Practices](https://sre.google/sre-book/service-best-practices/). Recommends measured resource-to-capacity ratios, forward-looking plans, overload tests, and controlled retries.
3. Google, [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/). Connects capacity plans to tested breaking points, redundancy, load balancing, overload, and failure.
4. Google, [Reliable Product Launches at Scale](https://sre.google/sre-book/reliable-product-launches/). Documents nonlinear overload behavior, launch demand, degradation, and load-test requirements.
5. Apache Flink, [Tuning Checkpoints and Large State](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/large_state_tuning/). Current. Documents checkpoint/state metrics, capacity planning, failure backlog, and catch-up reserve.
6. Apache Flink, [Elastic Scaling](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/elastic_scaling/). Current. Documents reactive/adaptive scaling, checkpoints, parallelism, stabilization, restarts, and limitations.
7. Apache Flink Kubernetes Operator, [Autoscaler](https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-main/docs/managing/autoscaler/). Current. Documents busy-time measurement, target utilization, parallelism changes, metrics-only evaluation, and scaling application.
8. Apache Spark, [Configuration](https://spark.apache.org/docs/latest/configuration). Current. Documents resource bounds, scheduling, dynamic allocation, backlog triggers, executor limits, and shuffle tracking.
9. Apache Spark, [Monitoring and Instrumentation](https://spark.apache.org/docs/latest/monitoring.html). Current. Documents application, executor, stage, task, event-log, and resource evidence.
10. Kubernetes, [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/). Current. Documents capacity, scheduling requests, enforceable limits, CPU, memory, and placement behavior.
11. Google Cloud Dataflow, [Monitor Autoscaling](https://docs.cloud.google.com/dataflow/docs/guides/autoscaling-metrics). Current. Documents worker targets, CPU utilization, backlog time, parallelism limits, convergence, and cost/latency trade-offs.
12. Google Cloud Dataflow, [Tune Horizontal Autoscaling](https://docs.cloud.google.com/dataflow/docs/guides/tune-horizontal-autoscaling). Current. Documents scaling ranges, backlog, utilization, available keys, dampening, and practical scale-up constraints.
13. Google Cloud Dataflow, [Plan Your Pipeline](https://docs.cloud.google.com/dataflow/docs/guides/plan-pipelines). Current. Documents resources, backlog, dependencies, quotas, external-service limits, and autoscaling amplification.

## Exercises

### Exercise 1

Size CPU for three streaming workload classes with forecast rates and measured CPU demands, then explain the limits of the calculation.

### Exercise 2

Derive batch capacity for a six-hour workload with a four-hour deadline, a 90-minute critical path, retries, and a competing maintenance job.

### Exercise 3

Design a recovery-capacity calculation for a stateful stream with variable arrivals, 20-minute restore, and a one-hour catch-up objective.

### Exercise 4

Create an autoscaling and failure-domain plan for a pipeline limited by source partitions, sink connections, and zone placement.

### Exercise 5

Design the operational feedback loop and evidence required to approve a one-year capacity plan.

## Answers to the Exercises

### Answer 1

For each class multiply forecast correct events/s by measured CPU-seconds/event, sum the demands, divide by target utilization, and round up effective cores. Recompute for peak, launch, and failure scenarios. The bound assumes representative mix and an operating region where demand is stable; it does not cover memory/state, I/O, network, dependencies, skew, partitions, scheduler overhead, retries, checkpointing, or nonlinear overload. Measure those separately and take the binding feasible configuration.

### Answer 2

Use the effective window between input readiness and deadline, not nominal six-hour coverage. Estimate resource work for the target volume, including exchange/spill/checkpoint/commit/validation and expected retry work; reserve the maintenance job's governed demand or schedule it elsewhere. Required resource units are at least work divided by effective window and target utilization, while elapsed time is also at least the 90-minute critical path. Simulate stage/task distributions and concurrency to prove the deadline with failure reserve rather than relying on ideal division.

### Answer 3

Integrate forecast arrivals over detection plus 20-minute restore to compute backlog, adding required replay and subtracting only governed expiry/loss. For catch-up duration $R=3,600$ seconds, require sustainable output at least continuing scenario rate plus $Q/R$. Include restore CPU/I/O/network, state repartition, cache warming, checkpoints, sink capacity, retries, and event-time correctness. Load test the full sequence and verify backlog/watermark lag declines within the hour without stealing protected foreground or failure reserve.

### Answer 4

Set autoscaling maximum no higher than useful source/key/operator parallelism or sink connection/quota capacity; split sources or shard the sink if more throughput is required. Set a minimum that carries immediate peaks and checkpoint/recovery health during provisioning delay. Place stateful replicas across declared zones, recompute capacity after the largest required zone loss, and reserve state-transfer/network/sink demand. Test metrics-only decisions, scale-up/down, quota exhaustion, partition ceilings, zone loss, restore, and one-winner output before enabling automation.

### Answer 5

Version workload classes, organic/inorganic scenarios, service-demand coefficients, resource/placement constraints, objectives, headroom reasons, lead times, allocation mapping, and cost. Support them with representative benchmarks, saturation/overload tests, recovery drills, raw production distributions, and immutable configurations. Assign forecast, quota, provisioning, and service owners; monitor forecast error, demand drift, saturation margin, backlog, state, checkpoint/recovery, failure reserve, cost, and lead-time milestones. Trigger reforecast/provisioning before lead time, reconcile monthly or on change, and record approvals and retired assumptions.
