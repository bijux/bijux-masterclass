---
module_id: DE-097
program: Data Engineering
level: 2
module_number: 97
title: Pipeline Capacity and Cost
status: complete
last_verified: 2026-09-03
---

# Pipeline Capacity and Cost

## One-Page Review

### Governing question

How can a team provision, schedule, isolate, scale, and economically govern an end-to-end data pipeline so forecast and burst demand meet freshness/completeness deadlines under failures and backfills—without mistaking average CPU, worker count, vendor autoscaling, or an allocated invoice for usable bottleneck capacity and consumer value?

### Essential definitions

- **demand** is arriving work described in semantic units such as events, bytes, partitions, keys, queries, or windows and their resource profiles.
- **service rate** $\mu$ is sustainable completed useful work per unit time at a named stage and workload mix.
- **capacity** is the bounded work a system can complete within required correctness and SLO conditions, not its theoretical peak throughput.
- **utilization** $\rho=\lambda/\mu$ compares arrival rate $\lambda$ with service rate under compatible units and intervals.
- A **bottleneck** is the resource or stage whose usable capacity constrains end-to-end throughput or deadline recovery.
- **backlog** is admitted but incomplete work; **backlog age** and drain time are often more decision-relevant than item count.
- **headroom** is capacity intentionally reserved above expected demand for uncertainty, failover, replay, skew, and scaling delay.
- A **capacity envelope** states sustainable and breaking behavior across workload shape, resources, dependencies, and failure modes.
- **elasticity** is the ability to change resources; **scalability** is useful performance gained from added resources. Elastic but serial work does not scale.
- **cost attribution** maps measured resource usage and shared costs to accountable pipelines, products, tenants, workloads, and consumers through a versioned rule.
- **unit cost** is attributable effective cost divided by a meaningful output or value unit, with quality and SLO context.
- **marginal cost** is the additional cost of one more unit of demand or tighter objective; it differs from average allocated cost.

### Central model, mechanism, or theorem

For discrete interval $t$, backlog evolves as

$$
Q_{t+1}=\max(0,Q_t+A_t-S_t),
$$

where $A_t$ is eligible arriving work and $S_t$ is useful successfully completed work under correctness constraints. For projected backlog $Q$, arrival rate $\lambda$, service rate $\mu>\lambda$, and drain deadline $D$, a fluid lower bound is

$$
T_{drain}=\frac{Q}{\mu-\lambda}\le D\quad\Longrightarrow\quad \mu\ge\lambda+\frac{Q}{D}.
$$

Pipeline capacity is limited by the minimum effective stage rate after fan-out, skew, retries, and dependency limits. Cost over interval $W$ is

$$
Cost_W=\sum_r usage_{r,W}\,rate_{r,W}+allocated\ shared_W,
$$

but cost effectiveness requires an SLO-qualified denominator: cheaper runs that miss deadlines, lose data, or shift cost downstream are not efficient.

### Critical invariants

- Demand and capacity share units, workload mix, data distribution, time window, correctness mode, and SLO; averages never stand in for peaks/tails without an explicit model.
- Every stage records input, useful output, retries/rework, backlog age, concurrency, resource saturation, throttling, dependency limits, and cost.
- End-to-end plans account for serial fractions, key/partition skew, state size, shuffle, spill, serialization, compression, fan-out, sinks, quotas, and scaling/provisioning delay.
- Capacity covers the intended failure domain, maintenance, backfill/replay, correction, and recovery deadline—not only healthy steady state.
- Queues, deadlines, admission, backpressure, load shedding, priorities, and fairness are bounded; retries cannot amplify demand without limit.
- Autoscaling has measured signals, min/max, quotas, startup/state-transfer time, stabilization, scale-down safety, and a non-scaling fallback.
- Cost identity binds resource, owner, product, tenant/workload, environment, billing interval, rate/discount, allocation rule, and unallocated remainder.
- Shared-cost rules are documented, versioned, conserved, explainable, and avoid incentives that punish efficient tenants for unrelated use.
- Optimization preserves correctness, freshness, completeness, security, recovery, and consumer outcomes, with before/after evidence.
- Load and failure tests identify the knee, breaking point, recovery path, and telemetry behavior; production is not the first experiment.

### Common failures

Sizing from average daily rows; treating bytes as equal-cost records; dividing peak rate by benchmark rate from a different schema/key distribution; averaging utilization across hot/cold workers; adding workers beyond keys/partitions or a serial sink; relying on CPU while I/O, memory, shuffle, state or quotas bind; scaling on backlog count without age or service rate; ignoring startup and state redistribution; setting maximum workers above provider quota; allowing backfills to starve production; retrying timeouts into overload; assuming a queue creates capacity; optimizing scans while exploding egress or downstream work; allocating all shared cost by raw row count; treating list price as effective cost; using utilization as value; deleting headroom because it appears idle; and claiming savings after relaxing SLOs or dropping data.

### Compact example

A one-minute pipeline receives `[80,140,180,60,40]` events while useful capacities are `[100,120,160,160,100]`. Backlog becomes `[0,20,40,0,0]`: peak input 180 exceeds capacity, but later spare capacity drains 40 events. At five, six, eight, eight, and five workers, usage is 32 worker-minutes or 0.533 worker-hours; at \$0.12 per worker-hour, direct compute is \$0.064. **Conclusion:** throughput, temporary backlog, recovery and cost must be evaluated together; average arrival alone would hide the peak.

### Connections

[DE-049](049-run-metadata-and-operational-state.md) supplies attempt/resource evidence, [DE-074](074-freshness-and-timeliness.md) supplies end-to-end latency, [DE-091](091-warehouses-query-engines-and-serving-stores.md) supplies workload placement, and [DE-096](096-freshness-and-completeness-slos.md) supplies the objectives capacity must protect. [PLAT-073](../../29-platform-engineering/modules/073-resource-quotas.md) and [PLAT-077](../../29-platform-engineering/modules/077-admission-control.md) govern shared limits and overload.

## Governing Question

For every forecast, burst, failure, replay, query, and backfill class, what is the demand shape, bottleneck service envelope, headroom, admission/priority policy, scaling delay, recovery time, and fully attributable cost per SLO-qualified consumer outcome—and what evidence shows that adding, removing, or moving resources changes useful capacity rather than symptoms?

## Why This Matters

Data pipelines combine networks, brokers, object stores, compute engines, shuffles, state, catalogs, warehouses, serving stores, and external APIs. Each exposes different capacity units and pricing. A job may show 20% average CPU while one partition is saturated, a sink quota throttles all workers, or a shuffle spills terabytes. Increasing workers can raise cost without increasing throughput and may worsen contention.

Demand is temporal and heterogeneous. Hourly batches create cliffs. Streaming rates spike. Records vary in encoded/decoded size, key fan-out, join matches, and transformation cost. Backfills compete with recurring work. Failure recovery replays retained backlog while new work continues. Planning from average daily volume makes the expensive, reliability-defining periods invisible.

Queues translate a capacity deficit into time. If arrivals exceed sustainable completion, backlog grows. Even after demand falls or capacity recovers, the pipeline must serve both new work and accumulated debt before freshness returns. Autoscaling reacts after measuring demand, then waits for provisioning, code loading, state transfer and warm-up. The maximum is bounded by quotas and parallelism.

Cost is similarly multidimensional. Compute, storage, operations, requests, network, egress, licenses, orchestration, observability, support, commitments and idle reserves accrue at different scopes. Provider bills rarely map cleanly to data products. An arbitrary shared-cost allocation can create false incentives. A lower bill can reflect delayed processing, reduced retention, lost rows or cost shifted to consumers.

Capacity and cost therefore belong in one governed model tied to SLOs and product value. The goal is not maximal utilization or minimal spend. It is enough tested capacity and recovery margin to deliver correct useful data, with explainable economics and safe overload behavior.

## Prerequisites and Retrieval

Retrieve consumer/product objectives: freshness/completeness SLOs, deadlines, query latency, availability, recovery objectives, critical keys/tenants, fallback, workload class, growth forecast, launches, seasonality, and business-value unit.

Retrieve demand history at useful resolution: events/bytes/partitions/keys/windows/queries, distributions and peaks, record size/compression/expansion, cardinality, fan-out, join matches, state, late/correction/retry rates, backfills, concurrency, tenant/source mix, forecast uncertainty, and correlated surges.

Retrieve stage topology: sources, brokers, transforms, shuffle/exchange, state/checkpoints, storage, catalog/publication, serving/API, dependencies, serial paths, queues/buffers, partitioning, locality, batch sizes, compression, network, and control-plane operations.

Retrieve resources and limits: worker shapes, CPU/GPU, heap/off-heap, disk/IOPS/throughput, ephemeral/storage, network/egress, file descriptors, threads, connections, partitions, slots, executor concurrency, sink quotas, API rates, account/project/region quota, scheduler fairness, startup, state transfer, warm cache, and failure capacity.

Retrieve operations: autoscaler signals/min/max/targets/stabilization, scale event history, backlog/age/watermarks, utilization/saturation, backpressure, spill/GC/OOM, throttling, retries, failures/restarts, skew, speculative work, job duration, queue delay, useful output, SLO burn, and incidents.

Retrieve cost inputs: billing exports, usage quantities/units, list/effective/amortized rates, commitments/discounts/credits, idle/reserved capacity, shared platform and support, storage tiers/retention, requests/operations, network/egress, observability, licenses, environments, tags/labels, product/tenant/run identity, allocation coverage, currency and billing adjustments.

Distinguish arrival from admitted demand; attempts from useful output; throughput from latency; utilization from saturation; worker maximum from usable parallelism; queue capacity from service capacity; source backlog count from work/time; scale-out from speedup; healthy steady state from failover/recovery; direct from shared cost; list from effective rate; spend from efficiency; allocation from causation; unit cost from value; and savings from a reduced bill caused by violated service.

Create a capacity-and-cost contract:

| Concern | Required evidence and decision |
|---|---|
| Demand | Units, mix, distribution, forecast, peaks, bursts, replay/backfill and uncertainty |
| Service | Per-stage useful rate, resource envelope, skew, serial work, dependencies and knee |
| Reliability | SLO, headroom, failure domain, backlog drain, deadlines and recovery |
| Control | Admission, queues, priority, fairness, backpressure, retry, degradation and kill switch |
| Elasticity | Signal, min/max, quota, parallelism, startup/state cost, stabilization and fallback |
| Cost | Usage/rates, ownership, allocation, shared/idle, discounts, unit economics and quality |
| Evidence | Load/failure tests, forecasts, actuals, lineage, receipts, reconciliation and variance |
| Lifecycle | Launch, seasonal event, migration, backfill, optimization, commitment and retirement |

Write a falsifiable claim: “Pipeline P version V sustains 12k representative events/s with p99 end-to-end freshness below 90 seconds and 99.99% completeness, survives loss of one zone at 9k/s, admits production before backfill, bounds queue age at five minutes, and drains a 20-minute outage backlog within 45 minutes; capacity tests include skew/state/sink limits; autoscaling operates between 20 and 120 workers within quota; every run reports useful records, resource usage and effective cost with at least 98% direct allocation; and cost per million SLO-good events stays below budget K without reducing retention, validation, or recovery.”

## Learning Objectives

After completing this module, you should be able to:

1. express demand, service rate, utilization, backlog, drain time, headroom, recovery and capacity in compatible units;
2. find end-to-end bottlenecks across CPU, memory, I/O, network, shuffle, state, partition/key parallelism, sinks, quotas and control planes;
3. design representative steady, burst, skew, failure, replay, query and backfill capacity tests;
4. size batch and streaming pipelines against deadlines and SLO-qualified useful throughput rather than averages;
5. design bounded queues, admission, priorities, fairness, backpressure, retries, degraded modes and recovery waves;
6. evaluate autoscaling signals, delay, parallelism ceilings, hysteresis, state movement, quotas and cost behavior;
7. construct attributable direct/shared/idle cost models with effective rates, conservation and versioned allocation rules;
8. compare cost per good event, dataset, query, tenant and business outcome without hiding quality or shifting costs;
9. forecast, budget, optimize and validate changes through common-boundary before/after evidence; and
10. govern capacity through launches, seasonal peaks, failures, migrations, commitments, incidents and retirement.

## Core Exposition

### Define useful work and demand shape

Choose semantic demand units at each boundary. Events/s is insufficient when records vary 1,000-fold in size or join fan-out. Track events, compressed/decoded bytes, keys, partitions, window timers, state touches, rows scanned, shuffle bytes, output rows, API calls, and resource-weighted work. Bind workload mix, schema and transformations to every benchmark.

Measure distributions over intervals relevant to scaling and deadlines: one second, minute, batch window, hour, day and season. Record percentiles, maxima with duration, burst arrival curves, autocorrelation and correlated tenants/sources. A 30-second spike and a six-hour plateau with the same peak need different plans.

Separate eligible arrivals, admitted work, attempts and useful terminal output. Retries, speculative tasks, duplicates and recomputation consume capacity but do not increase product output. Define useful throughput only after required correctness and publication evidence. A fast pipeline that drops poison records without governed disposition is not high capacity.

Forecast from business drivers and pipeline coefficients: customers, transactions, devices, features, retention, joins, data size and query mix. Use scenarios with uncertainty, launches, migrations, holidays, source changes and new consumers. Reconcile forecast to actual and explain model error rather than adding an unexplained percentage forever.

### Model every stage and bottleneck

Draw the work graph with rates and expansion. If one input event fans to five enrichments, one stage receives five times the upstream event rate. Filters contract; joins can multiply; compression changes network versus memory units. Express stage $j$ demand $\lambda_j$ and sustainable useful capacity $\mu_j$ under the same workload.

End-to-end rate is constrained by a bottleneck, but it can move with load. CPU may bind at normal mix, shuffle disk under skew, object request limits during small-file backfill, and sink connections during recovery. Dependency quotas and control-plane operations are capacity even when worker dashboards cannot see them.

Inspect saturation, not average utilization alone. CPU run queues/throttling, memory pressure/GC/OOM, disk queue/IOPS, network loss/throughput, spill, connection pools, broker partition lag, backpressure and quota throttles reveal ceilings. Average CPU across workers hides one hot key. Report max/quantile and work distribution.

Test the serial fraction and parallelism ceiling. Adding workers stops helping when keys/partitions are fewer, one global aggregation serializes, the sink accepts fixed concurrency, state transfer dominates, or scheduler/control plane saturates. Measure speedup and efficiency across resource levels; do not assume linear scale.

### Size steady work, deadlines and backlog recovery

Stable streaming requires long-run $\mu>\lambda$ with headroom. Near $\rho=1$, variability creates long queues even when averages balance. Choose headroom from arrival/service variance, scale delay, failure loss, forecast error and recovery requirement, then validate empirically.

Backlog drain uses spare rate $\mu-\lambda$, not total rate. If 3.6 million events accumulate, new arrivals are 20k/s and useful service is 30k/s, drain takes at least 360 seconds. A plan saying “30k/s capacity” without subtracting arrivals underestimates recovery.

For a batch with work $W$ and deadline $D$, the crude lower bound is $W/D$, but startup, skew, serial stages, retries and publication consume the same window. Build a stage schedule and critical path. Reserve time for validation and atomic publication; completing computation at the deadline can still miss consumer usability.

Capacity under failure is different. N+1 worker arithmetic is not enough when losing a zone also removes partitions, quota, network paths or state replicas and triggers replay. Test declared failure domains with concurrent demand. Headroom must be reachable within quotas and not share the failed dependency.

### Bound queues and overload

Queues absorb finite bursts; they do not fix sustained deficits. Bound items, bytes, age and deadlines at each source, broker, executor, shuffle, sink and retry path. Backlog age connects waiting to freshness. Define overflow: reject/defer new low-priority work, spill durably, degrade, pause sources, or escalate—never unbounded memory.

Propagate backpressure from the true bottleneck. If a sink throttles, upstream workers should not generate unlimited intermediate state. Admission should consider estimated work and current deadlines, not job count alone. Reserve capacity for recurring production, corrections, deletions and safety work before exploration/backfill.

Use workload classes and fair queues by product/tenant with weights, concurrency and quotas. Backfills have rate and cost budgets plus pause/kill controls. Prevent one large tenant or pathological key from monopolizing shared partitions. Fairness must be measured in scarce-resource work, not equal task count.

Retries amplify overload. Budget attempts per operation and deadline, use backoff/jitter, deduplicate/idempotently apply, and stop obsolete work. After recovery, release queued/retry work in waves; instant replay can recreate the incident. Protect control paths so operators can cancel or reprioritize while data lanes are saturated.

### Design autoscaling as a delayed control loop

Select signals tied to demand and bottleneck: backlog age/work, input/service rate, busy/backpressure time, CPU/memory, timer/state backlog and deadline risk. CPU-only scaling misses I/O throttling; backlog count ignores item cost. Custom source progress must be truthful or the autoscaler operates blind.

Measure detect, decide, provision, initialize, state-restore/rebalance and warm-up delays. The pipeline must buffer within SLO during this interval or keep minimum warm capacity. Scaling down too quickly causes oscillation and repeated state movement. Use hysteresis, stabilization and minimum residence based on measurements.

Set min/max from floor workload, failure headroom, quota, parallelism ceiling, cost exposure and recovery target. A maximum above regional/account quota is fictional. More workers than available keys do not help. Autoscaling can increase resource count while a serial sink remains fixed.

Test scale events with real state and skew. Observe useful throughput, lag, task failure, checkpoint duration, cache loss, network, downstream pressure and billable minimums. Provider autoscalers have specific documented behavior; treat them as implementations, not proof that goals are met.

Provide fallback: admission tightening, pausing batch, reserved capacity, manual bounded override, reduced optional enrichment, or failover. Scaling is too slow for some spikes and impossible during some regional failures.

### Build a representative capacity test program

Start with component microbenchmarks to find resource coefficients, then stage and end-to-end tests to expose interactions. Use production-like schemas, record sizes, compression, key distribution, state, data history, cache state, dependency limits and network topology. Synthetic uniform keys systematically miss skew.

Test steady ramps to find the knee where latency/backlog grows faster than useful throughput, then the breaking point and failure mode. Include step bursts, diurnal waves, hot keys, small files, wide records, high join fan-out, late windows, checkpoint overlap, cold start, worker churn, zone/dependency loss, retry storms and backfill concurrency.

Measure input/admission/useful completion rates, backlog count/bytes/age, end-to-end SLO, correctness/completeness, per-stage resource saturation, skew, spill, GC, backpressure, failures/retries, scale timeline and cost. A test passes only if correctness and recovery remain within contract; output corruption is not graceful overload.

Run above planned capacity in a controlled environment to verify bounded degradation, shedding and operator control. Determine the maximum safe operating point below the knee with uncertainty and failure reserve. Re-test after schema, engine, instance, partition, sink, dependency, transform or runtime changes.

### Attribute cost with conserved identities

Normalize billing and usage by provider/account, resource/service/SKU, region, usage interval/unit, list and effective cost, currency, discounts/credits/commitment amortization, tags and invoice revisions. Preserve raw and normalized records plus allocation rule version.

Join runtime identity from pipeline/product/run/stage/task/tenant/workload to resources. Directly attributable ephemeral compute and query bytes are easiest. Long-lived clusters, storage, network, orchestration, observability, support, commitments and idle reserves require explicit shared rules.

Allocation must conserve cost: direct + allocated shared + intentionally central + unallocated equals authoritative effective total for a common billing boundary. Report unallocated percentage and late billing adjustment. Never force unknown cost into a convenient product and call coverage complete.

Choose shared drivers causally when possible: CPU/memory time, bytes stored, I/O, queries, egress, retained data, control-plane objects. Even split may fund common governance; revenue or direct-spend proportion may reflect policy rather than causation. Document purpose and incentives. Version changes and dual-report before chargeback.

Separate idle/headroom. Reserve capacity exists for SLO/failover and should be visible as reliability insurance, not automatically blamed on the last tenant. Unused commitments, fragmentation and forgotten resources are different from intentional reserve.

### Use unit economics without gaming quality

Compute cost per SLO-good event, published dataset, successful query, active tenant, GB processed, or business outcome. Include the denominator definition, period, product version, quality, freshness/completeness and volume. A falling cost per raw event can hide increased retries or dropped records.

Decompose unit cost: source ingress, compute, shuffle, storage, serving, network/egress, orchestration/metadata, observability and allocated shared. Separate fixed and variable components. Average cost predicts poorly near commitment edges, tier boundaries, minimum billing periods or capacity steps; use marginal scenario models.

Relate technical units to value cautiously. Cost per million records enables engineering comparison; cost per successful decision or customer outcome supports product investment but needs attribution and causal humility. Do not assign all business value to a pipeline merely because it is in the dependency path.

Guard against local optimization. Compacting files costs compute but reduces many future scans. Lower storage retention may raise replay risk. Pushing computation to consumers shifts cost and semantic inconsistency. Evaluate total system and lifecycle cost over a representative horizon.

### Optimize through controlled hypotheses

Form a testable claim: “Partition pruning reduces scanned bytes 60% for workload X without changing rows, latency tails or maintenance cost.” Pin workload/data/SLO and compare before/after actual usage and bill. Normalize for volume/mix and include amortized migration cost.

Common levers include eliminating unused products/queries, incremental rather than full recompute, pruning/projection, data layout/compaction, avoiding small files, right-size worker shapes, bounded parallelism, compression, batching, cache/materialization, shared computation, storage lifecycle, network locality, tuned retention, commitments and scheduling flexible work into idle capacity.

Each has trade-offs. More compression costs CPU. More partitions add metadata/small files. Materialization adds refresh/storage and invalidation. Spot/preemptible compute adds interruption/retry. Commitments reduce rate but create idle risk. Validate the bottleneck moves as predicted.

Keep correctness oracles. Compare row/key/control totals, checksums, schema, freshness/completeness, and outputs at common boundaries. Savings are accepted only after SLO, recovery and incident metrics remain within guardrails for an adequate horizon.

### Forecast and govern portfolio capacity

Roll stage forecasts into provider quota, cluster, reservation, account, region and dependency portfolios. Correlated peaks matter: hundreds of jobs scheduled at midnight can exceed shared control-plane or warehouse capacity even when each plan passes alone.

Maintain base, expected, high and failure scenarios with confidence, lead time and trigger points. Some quota, commitments, hardware and vendor increases take weeks. Record owner and decision date. Compare forecast versus actual demand, capacity, spend and unit cost monthly or at a cadence matching change.

Use budgets as feedback, not abrupt correctness breakers. Alerts distinguish forecast variance, price/rate change, allocation change, anomalous usage, idle waste and genuine growth. Cost caps on query/backfill can prevent runaway spend; recurring critical data needs explicit degraded/stop policy rather than surprise termination.

Capacity changes are reviewed like migrations: canary, load test, rollback, observability and failure validation. Retiring a product removes compute, storage, queues, autoscaling policies, commitments, dashboards, credentials and shared allocations only after consumers and retention obligations close.

## Definitions and Notation

For stage $j$ and interval $t$, let arrivals be $A_{j,t}$, admitted work $D_{j,t}$, attempts $X_{j,t}$, and useful successful completions $S_{j,t}$. Backlog $Q_{j,t+1}=\max(0,Q_{j,t}+D_{j,t}-S_{j,t})$. Attempt amplification is $X/S$; it is undefined when no useful output and must not be hidden.

Let arrival and sustainable service rates be $\lambda_j$ and $\mu_j$ in compatible work units. Utilization proxy $\rho_j=\lambda_j/\mu_j$ describes mean load, not queue delay under variance. Fluid drain time is $Q/(\mu-\lambda)$ only for $\mu>\lambda$ and stable rates; measured recovery supersedes it.

For resource vector $r=(cpu,memory,io,network,state,connections,quota)$ and workload mix $m$, define empirical capacity envelope $C_j(r,m,f)$ under failure mode $f$ as greatest useful rate meeting correctness and SLO. Pipeline capacity is constrained by transformed stage demand and dependencies, not simply $\min_j\mu_j$ when fan-out differs.

Let authoritative effective cost over billing boundary $W$ be $K_W$. Allocation conservation requires

$$
K_W=K_{direct}+K_{shared\ allocated}+K_{central}+K_{unallocated}.
$$

For SLO-good useful units $G_W>0$, unit cost $U_W=K_W/G_W$. Always report numerator scope, denominator, SLO/quality, price basis, allocation version and uncertainty.

Parallel speedup for $n$ resources is $speedup(n)=T(1)/T(n)$ and efficiency $speedup(n)/n$ under identical work; state/caches and provider differences can make comparison nonidentical and must be controlled.

## Mechanisms, Invariants, or Proof Structure

### Capacity and cost planning mechanism

1. Freeze consumer SLOs, workload classes, useful work units, correctness gates and recovery objectives.
2. Measure and forecast arrivals, size, skew, fan-out, state, queries, retries, backfills and correlated peaks.
3. Map stage topology, expansion and dependencies; identify every queue, quota, serial fraction and resource.
4. Benchmark representative useful service envelopes across resource levels, skew and failure modes; find knee/breaking point.
5. Calculate steady headroom, deadline capacity, backlog drain and failover needs; validate with end-to-end tests.
6. Configure bounded admission, priority/fairness, backpressure, retry, degradation and recovery waves.
7. Configure autoscaling signals/min/max/stabilization within parallelism and quota; test full scale timeline and fallback.
8. Instrument useful throughput, backlog age, saturation, scale events, correctness/SLO and per-stage resource usage.
9. Normalize bills/effective rates; join runtime identity; allocate shared/idle/unallocated cost with conserved versioned rules.
10. Report cost per SLO-good technical and business unit plus forecast/actual variance and allocation coverage.
11. Optimize one measured bottleneck/cost hypothesis at a time with common-boundary correctness and SLO guardrails.
12. Rehearse bursts/failures/backfills, review forecasts and prices, govern commitments, and retire all resource/cost residue.

### Conditional claim: positive spare capacity drains a fixed backlog

**Claim.** If arrivals and useful service are constant with $\mu>\lambda\ge0$, no new retry amplification occurs, and a backlog $Q_0$ is served work-conservingly, then it drains by time $Q_0/(\mu-\lambda)$ in the fluid model.

**Proof sketch.** While backlog is positive, its derivative is $dQ/dt=\lambda-\mu=-(\mu-\lambda)$. Thus $Q(t)=Q_0-(\mu-\lambda)t$ until zero, reached at the stated time. The claim fails with variable rates, pauses, priority starvation, discreteness, skew, failed work, unavailable dependencies, or service measured as attempts rather than useful completions.

### Conditional claim: conserved allocation prevents double-counted total cost

**Claim.** If each authoritative cost record is assigned exactly once among direct, allocated shared, central, or unallocated categories and allocations partition each shared record, the sum of reported categories equals authoritative effective cost.

**Proof sketch.** The categories form a disjoint exhaustive partition of cost records/fractions, so additivity yields equality. The claim says nothing about causal fairness or value. It fails when records are duplicated/missing, billing boundaries/currencies/rates differ, shared fractions do not sum to one, credits/commitments are omitted, or allocation versions overlap.

### Executable backlog and direct-cost illustration

This deterministic fixture applies the discrete backlog recurrence to five one-minute intervals and calculates peak/final backlog, useful totals, worker-hours and direct compute cost. It does not model stochastic queues, failed work, parallelism, startup, dependencies, shared cost, billing minimums or SLO correctness.

<!-- bijux-verify: {"id":"backlog-and-direct-cost","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"backlog=0,20,40,0,0\npeak_backlog=40\nfinal_backlog=0\narrivals=500\ncompleted=500\nworker_hours=0.533\ndirect_cost=0.064\n","stderr":""}} -->
```python
arrivals = [80, 140, 180, 60, 40]
capacities = [100, 120, 160, 160, 100]
workers = [5, 6, 8, 8, 5]

queue = 0
backlogs = []
completed = 0
for arrived, capacity in zip(arrivals, capacities):
    available = queue + arrived
    served = min(available, capacity)
    completed += served
    queue = available - served
    backlogs.append(queue)

worker_hours = sum(workers) / 60
direct_cost = worker_hours * 0.12
print(f"backlog={','.join(str(value) for value in backlogs)}")
print(f"peak_backlog={max(backlogs)}")
print(f"final_backlog={queue}")
print(f"arrivals={sum(arrivals)}")
print(f"completed={completed}")
print(f"worker_hours={worker_hours:.3f}")
print(f"direct_cost={direct_cost:.3f}")
```

## Alternatives and Trade-Offs

- **Peak provisioning versus elasticity:** peak capacity gives immediate predictable headroom at idle cost; elasticity reduces idle spend but adds signal, startup, quota, state and stabilization risk.
- **Fixed workers versus autoscaling:** fixed size simplifies performance and billing; autoscaling adapts to variance but is a delayed control loop requiring tested bounds.
- **High utilization versus headroom:** utilization can improve unit cost; near saturation magnifies queueing, recovery time and cascade risk. Optimize within SLO/failure reserve.
- **Shared versus isolated pools:** sharing improves utilization and idle-capacity reuse; isolation limits noisy neighbors and gives predictable failure capacity at fragmentation cost.
- **Event versus resource-weighted fairness:** equal event quotas are simple; heterogeneous event cost may still monopolize CPU/memory/I/O, motivating weighted work estimates.
- **Queue versus rejection/defer:** queues preserve finite bursts; rejection/defer bounds latency and resources when deadlines cannot be met. Both need explicit semantics.
- **More partitions versus larger partitions:** more partitions raise parallelism and skew tolerance; they add metadata, connections, small files and control-plane load.
- **Scale compute versus remove work:** more resources preserve design speedily; pruning, incrementality and reuse can permanently lower demand but require semantic and migration review.
- **On-demand versus commitments:** on-demand follows uncertainty at higher rates; commitments lower predictable cost but create lock-in and idle/allocation risk.
- **Spot/preemptible versus reserved compute:** interruptible capacity lowers price for restartable work; critical deadlines and stateful recovery need bounded interruption strategy.
- **Direct chargeback versus central funding:** chargeback creates accountability but can induce gaming; central funding supports shared guardrails but can hide demand. Transparent showback often precedes charging.
- **Causal shared driver versus simple allocation:** usage drivers improve behavior/equity but cost to measure; simple even or spend-proportional rules are explainable but may be unfair.
- **Technical versus business unit cost:** technical units guide engineering; business units guide investment but require stronger attribution and outcome definitions.
- **Local versus total-system savings:** local changes are easier to measure; total lifecycle accounting catches egress, consumer, recovery, observability and migration cost shifts.

## Failure Modes and Misconceptions

1. **“Average demand sizes capacity.”** Peaks, bursts, variance and deadlines create the critical envelope.
2. **“A record is a stable work unit.”** Size, key, fan-out, state and transform cost differ.
3. **“High CPU means CPU bottleneck.”** It can be useful saturation or retry/GC/spin caused by another limit.
4. **“Low average CPU means spare capacity.”** One hot task, I/O, memory, sink or quota may bind.
5. **“Workers multiply throughput linearly.”** Serial work, partitions, skew, state and dependencies cap speedup.
6. **“A queue adds capacity.”** It stores delay and helps only for finite deficits with later spare service.
7. **“Service rate drains backlog.”** Only rate above continuing arrivals drains it.
8. **“Stable mean utilization means stable latency.”** Variance near saturation can produce long queues.
9. **“N+1 workers prove failover.”** Failure can remove data, quota, network, state and dependency capacity together.
10. **“Autoscaling is instantaneous.”** Detection, provisioning, initialization, rebalance and warm-up consume SLO.
11. **“Maximum workers is available capacity.”** Quota, keys, sink and regional supply can make it fictional.
12. **“Backlog count is enough.”** Work size and oldest age determine effort and harm.
13. **“Retries improve recovery.”** Unbounded retries amplify overload and duplicate work/effects.
14. **“Backfills are harmless background work.”** They compete for every shared bottleneck and can violate production SLOs.
15. **“Benchmark throughput is production capacity.”** Workload, history, cache, skew, failures and correctness must match.
16. **“Passing at target load is enough.”** The knee, overload behavior and recovery must be known.
17. **“Provider autoscaling proves the objective.”** It applies implementation heuristics within limits; measure consumer outcomes.
18. **“The invoice identifies the owner.”** Shared resources and missing runtime identity require allocation.
19. **“List price is actual cost.”** Discounts, credits, commitments, tiers, currency and adjustments change effective cost.
20. **“Allocation is causal truth.”** It is a policy/model that must be explicit and conserved.
21. **“All idle cost is waste.”** Some is tested headroom/failover insurance; other idle may be avoidable.
22. **“Maximum utilization minimizes unit cost.”** SLO failures, spill, retries and tail latency can increase cost per good unit.
23. **“Lower bill proves optimization.”** Volume, mix, rates, retention, quality or shifted downstream cost may explain it.
24. **“Cost per event equals business value.”** It is a technical efficiency measure unless outcome attribution is established.
25. **“Stopping compute retires cost.”** Storage, egress, licenses, commitments, telemetry and shared allocations can remain.

## Worked Examples

### Example 1

**Situation.** Mean traffic is 50k/s, but five-minute launch peaks reach 180k/s. **Reasoning.** Planning uses arrival curves, scale delay and backlog-age SLO, not daily mean; warm minimum plus bounded queue covers the ramp. **Conclusion.** Duration and elasticity determine peak headroom.

### Example 2

**Situation.** Doubling workers leaves throughput unchanged. **Reasoning.** Only 32 keys exist and one sink allows 20 concurrent writes. Repartitioning and sink negotiation matter before more workers. **Conclusion.** Resource count is not usable parallelism.

### Example 3

**Situation.** Average worker CPU is 35% while one task is at 100% with growing lag. **Reasoning.** A hot tenant key serializes the stage. Key salting/domain aggregation and tenant isolation are tested. **Conclusion.** Fleet averages hide skew bottlenecks.

### Example 4

**Situation.** A 20-minute outage accumulates work while new traffic continues. **Reasoning.** Recovery planning subtracts arrival rate from service and reserves production priority; replay releases in waves. **Conclusion.** Backlog drain depends on spare useful capacity.

### Example 5

**Situation.** Autoscaler reaches its configured maximum but lag persists. **Reasoning.** Regional VM quota and limited source partitions cap actual capacity. The runbook tightens admission, pauses backfill and uses reserved failover. **Conclusion.** Scaling bounds must be feasible across dependencies.

### Example 6

**Situation.** A backfill starves a deletion pipeline. **Reasoning.** Workload classes reserve capacity for recurring and urgent governance operations, cap backfill work/cost, and support pause/kill. **Conclusion.** Priority belongs at the scarce-resource boundary.

### Example 7

**Situation.** Row-count allocation charges a tenant with many tiny events more than one running expensive joins. **Reasoning.** Shared compute uses CPU/memory/shuffle time, storage uses byte-time, and central guardrail cost is explicit. **Conclusion.** Allocation drivers shape incentives.

### Example 8

**Situation.** Compression lowers network cost but raises CPU and misses freshness. **Reasoning.** The comparison measures total compute/network cost per SLO-good GB and selects a different codec/level. **Conclusion.** Local resource savings can reduce total efficiency.

### Example 9

**Situation.** A one-year commitment appears cheap at list-rate comparison. **Reasoning.** Scenario analysis includes utilization, growth uncertainty, failover reserve, opportunity cost and unused commitment allocation. **Conclusion.** Lower rates do not guarantee lower effective unit cost.

### Example 10

**Situation.** A team claims 40% savings after shortening retention and disabling validation. **Reasoning.** Replay/recovery and completeness objectives fail, so the cheaper service is not comparable. **Conclusion.** Savings require unchanged or explicitly renegotiated outcomes.

## Cross-Program Connections

- [DE-035](035-incremental-models.md), [DE-049](049-run-metadata-and-operational-state.md), and [DE-063](063-table-metadata-and-snapshots.md) provide changed-work reduction, run/resource evidence, and storage state.
- [DE-074](074-freshness-and-timeliness.md), [DE-073](073-reconciliation-tests.md), and [DE-096](096-freshness-and-completeness-slos.md) define latency, useful correctness, and recovery constraints.
- [DE-091](091-warehouses-query-engines-and-serving-stores.md), [DE-092](092-materialized-views-and-derived-tables.md), and [DE-094](094-data-apis.md) connect workload placement, materialization and query budgets.
- [DE-095](095-feature-and-training-dataset-pipelines.md) supplies feature/training backfill, online/offline and retraining demand classes.
- [API-071](../../28-api-and-service-engineering/modules/071-timeout-and-deadline-budgets.md), [API-073](../../28-api-and-service-engineering/modules/073-circuit-breaking-and-bulkheads.md), [API-074](../../28-api-and-service-engineering/modules/074-api-level-load-shedding.md), and [API-075](../../28-api-and-service-engineering/modules/075-backpressure-across-service-boundaries.md) connect deadlines and overload control.
- [PLAT-073](../../29-platform-engineering/modules/073-resource-quotas.md), [PLAT-077](../../29-platform-engineering/modules/077-admission-control.md), and [PLAT-082](../../29-platform-engineering/modules/082-control-plane-capacity.md) connect shared resource governance.
- [PLAT-089](../../29-platform-engineering/modules/089-cost-allocation-and-efficiency.md) develops platform-wide allocation and unit economics; this module specializes them for data-stage work and SLO-good outputs.
- [DE-098](../ROADMAP.md) uses the capacity, headroom, failure and cost envelope to design disaster recovery for data products.

## References

- Google, “Addressing Cascading Failures,” *Site Reliability Engineering*. <https://sre.google/sre-book/addressing-cascading-failures/>
- Google Cloud, “Tune Horizontal Autoscaling for Streaming Pipelines,” current Dataflow documentation. <https://docs.cloud.google.com/dataflow/docs/guides/tune-horizontal-autoscaling>
- Apache Flink project, “Monitoring Back Pressure,” current stable documentation. <https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/monitoring/back_pressure/>
- Apache Spark project, “Job Scheduling,” current documentation. <https://spark.apache.org/docs/latest/job-scheduling.html>
- Kubernetes project, “Resource Management for Pods and Containers,” current documentation. <https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/>
- Google Cloud, “Understand Slots,” current BigQuery documentation. <https://docs.cloud.google.com/bigquery/docs/slots>
- Google Cloud, “Estimate and Control Costs,” current BigQuery documentation. <https://docs.cloud.google.com/bigquery/docs/best-practices-costs>
- FinOps Foundation, “Allocation,” current FinOps Framework capability. <https://framework.finops.org/framework/capabilities/allocation/>
- FinOps Foundation, “Unit Economics,” current FinOps Framework capability. <https://www.finops.org/framework/capabilities/unit-economics/>
- FinOps Foundation, *FinOps Open Cost and Usage Specification 1.2*. <https://focus.finops.org/wp-content/uploads/2025/05/FOCUS-spec-v1_2.pdf>

## Exercises

### Exercise 1

Recompute the executable’s backlog and cost. Then hold arrivals fixed and reduce interval-four capacity from 160 to 100. Calculate final backlog and minimum constant capacity during two additional intervals if new arrivals are 40 per interval and the queue must drain by the second.

### Exercise 2

A stream receives 20k/s, accumulates 3.6 million events during an outage, and must drain within six minutes while serving new traffic. Derive the fluid service-rate bound. Add 25% uncertainty/headroom and identify why worker count cannot be derived without workload tests.

### Exercise 3

Design a capacity test for a stateful pipeline with 128 partitions, Zipf-like keys, 2 TiB state, hourly checkpoints, external enrichment and a quota-limited sink. Include workloads, failures, metrics, pass/fail, scaling and recovery.

### Exercise 4

Allocate a monthly \$100k pipeline estate: \$55k directly tagged compute/query, \$15k storage attributable by byte-month, \$10k observability shared by telemetry volume, \$8k central governance, \$7k intentional failover reserve, and \$5k unknown. Define conservation, allocation coverage, showback and unit-cost rules without pretending fairness is automatic.

### Exercise 5

An estate has 300 pipelines sized from average rows, unbounded backfills, CPU-only autoscaling, no load tests, 65% cost allocation, and a mandate to cut 30%. Design a risk-prioritized recovery and evidence required to call savings durable.

## Answers to the Exercises

### Answer 1

Original recurrence starts at zero. Interval results are `max(0,0+80-100)=0`, `0+140-120=20`, `20+180-160=40`, `max(0,40+60-160)=0`, and `max(0,0+40-100)=0`. Total arrivals and useful completions are 500. Workers total 32 minutes, so usage is `32/60=0.5333` worker-hours and direct cost at \$0.12 is \$0.064.

With interval-four capacity 100, backlog after it is `40+60-100=0`; it still drains exactly, so interval five remains zero. If the intended reduction were below 100, use the same recurrence rather than intuition. For illustration, if interval four were 80, backlog would be 20, interval five capacity 100 with arrival 40 would drain it. If 20 remained after interval five and two more intervals each receive 40, constant capacity $c$ must satisfy `2c >= 20+80`, hence $c\ge50$ work/interval. This is a fluid/discrete aggregate bound; skew and failures may require more.

### Answer 2

The drain window is 360 seconds. Required spare rate is `3,600,000/360=10,000` events/s. Add continuing arrivals 20,000/s, yielding at least 30,000 useful events/s. Applying 25% headroom to the modeled total gives 37,500 events/s; alternatively teams may apply uncertainty separately to arrivals and service degradation, which must be documented and can produce a different bound.

Worker count is not `37,500 / a remembered worker benchmark`. It requires representative per-worker useful rate with actual record sizes, transforms, key skew, state, checkpoint overlap, enrichment latency/quota, sink limits, failures and correctness. Parallelism is capped by partitions/keys and dependencies; adding workers can increase contention. Provisioning/state-restore delay also determines warm minimum. Validate drain with new arrivals and the declared failure mode.

### Answer 3

Generate production-like records and state history with real size/compression and Zipf keys, including one/two hot keys, uniform control, normal and peak rates, step bursts, late events, replay, and concurrent bounded backfill. Model enrichment latency/error/rate limits and enforce the real sink quota. Start warm and cold; test 128 and changed partition counts only as supported.

Run steady ramps to knee/breaking point. Inject worker loss, zone loss, enrichment slowdown/outage, sink throttling, checkpoint delay/failure, state restore, network impairment and retry storm. Exercise scale-out/down while 2 TiB state redistributes and hourly checkpoints overlap. Verify control paths remain available and backfill pauses.

Measure eligible/admitted/attempted/useful rates, per-partition backlog count/bytes/oldest age, end-to-end freshness/completeness, hot-key distribution, CPU/memory/GC/disk/network/spill, busy/idle/backpressure, state/checkpoint duration/bytes, enrichment/sink quota, retries, autoscaling timeline, cost and result reconciliation. Track per-stage and consumer-visible boundaries.

Pass requires the target workload and failure scenario to meet SLO/correctness, bounded queues and resource limits; backlog drains within objective while new work continues; no unbounded retry/cascade; scaling remains within quota and useful throughput increases; checkpoints/restores complete; sink/enrichment remain protected; backfill yields; and overload sheds/degrades only approved work. Record capacity envelope, knee, breaking behavior, recovery and cost—not one headline rate.

### Answer 4

Authoritative effective total is \$100k. Direct tagged cost is \$55k. Allocate \$15k storage by governed byte-month per retained product and \$10k observability by validated telemetry volume or a hybrid base-plus-volume rule. Keep \$8k central governance explicitly central if organization policy funds common controls. Show \$7k failover reserve as reliability insurance, allocated by protected-capacity share or central policy—not as waste or last-user demand. Keep \$5k unknown unallocated with owner and reduction target.

Conservation report is `55+15+10+8+7+5=100`. Direct-plus-driver allocation coverage is 80%; if central/reserve are deliberately categorized, classified coverage is 95%, while true direct/usage allocation remains separately reported. Every record has one category; shared fractions sum to one; billing period, currency, discounts/credits and allocation version match.

Showback reports direct, each shared driver, central/reserve and unknown distinctly with rule/uncertainty. Chargeback follows explicit organizational policy after dual reporting. Unit cost divides relevant attributed cost by SLO-good outputs for the same product/month, not raw attempts, and includes freshness/completeness. Driver choice is a governance hypothesis: telemetry volume may reflect verbosity rather than benefit and byte-month may not capture access tier. Review incentives and revise versionedly.

### Answer 5

Inventory SLOs, consumers, demand units/mix, peaks, stage topology, bottlenecks, queues, backfills, autoscalers, quotas, failure objectives, resources and full costs. Freeze indiscriminate 30% cuts and new unbounded backfills. Prioritize pipelines tied to safety/security/finance, tight freshness, deletion/correction, large spend, known lag, shared bottlenecks and missing ownership.

Instrument useful throughput, backlog age, stage saturation/skew, retries, correctness/SLO and resource identity. Replace average-row sizing with high-resolution arrival/work forecasts, stage expansion and representative service envelopes. Bound backfill admission, cost, priority and kill switches. Add multi-signal autoscaling with feasible min/max/quota, startup/state delay, stabilization and fallback. Load/failure test knee, overload, recovery and correlated schedules.

Raise allocation by joining runtime pipeline/product/run/tenant/workload identity to normalized effective billing. Preserve direct, causal shared, central, reserve and unknown categories; publish coverage and conservation. Establish cost per SLO-good unit and portfolio forecast/actual variance.

Optimize largest validated drivers: retire unused outputs, incrementalize, prune/project, compact/layout, right-size shapes/parallelism, reduce retries, tune retention with recovery review, share computations, schedule flexible work, and model commitments. Each change pins workload and compares source/output reconciliation, freshness/completeness, tail/recovery, actual usage/cost and downstream shifts.

Durable savings require a full representative/seasonal horizon; unchanged or explicitly renegotiated contracts; all correctness/SLO/failure tests passing; no rising backlog/incidents/toil or cost shifted to another account/consumer; allocation conservation and high coverage; volume/rate/mix normalization; migration cost included; capacity forecast still covers growth/failover; and removed resources/commitments/storage actually gone. Thirty percent is an outcome only if evidence supports it, not a quota to manufacture by hidden degradation.
