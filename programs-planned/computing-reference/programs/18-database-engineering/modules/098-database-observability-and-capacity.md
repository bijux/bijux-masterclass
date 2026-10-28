---
module_id: DBE-098
program: Database Engineering
level: 2
module_number: 98
title: Database Observability and Capacity
status: complete
last_verified: 2026-09-05
---

# Database Observability and Capacity

## One-Page Review

### Governing question

How can operators infer database health and future capacity from workload, latency, errors, queues, storage, maintenance, replication, and failure evidence without turning dashboards, averages, or utilization into false causal claims?

### Essential definitions

- **Observability** is the ability to infer relevant internal state and behavior from available evidence; it is not a synonym for collecting many metrics.
- A **service-level indicator (SLI)** is a measured quantity tied to user-visible correctness or service; an **SLO** is its target over a defined population and window.
- **Offered load** is attempted work; **throughput** is completed work. Retries, rejection, and client throttling can make them diverge.
- **Latency** is elapsed operation time under a named boundary; queue, execution, lock, network, and client time must not be conflated.
- **Utilization** is busy fraction of a resource; **saturation** is queued or delayed demand that cannot receive immediate service.
- A **wait event** classifies why work is not progressing; it is evidence, not a root cause by itself.
- **Headroom** is usable capacity beyond current demand under specified failure, maintenance, and growth scenarios.
- **capacity envelope** is the tested region of workload dimensions within which correctness and SLOs hold.
- **coordinated omission** occurs when a load generator stops issuing work while waiting and therefore under-samples slow periods.
- **high-cardinality telemetry** creates many identity combinations and can overload the monitoring system or leak sensitive values.

### Central model, mechanism, or theorem

Correlate one causal chain: offered operations enter queues, consume database and dependency service, complete or fail, and create maintenance/recovery work. Observe user outcomes and every constraining resource along that chain with stable time and configuration identity.

Little's law $L=\lambda W$ relates average in-system work $L$, average completion rate $\lambda$, and average residence time $W$ only for a stable observed system with compatible boundaries. The utilization law $U=X D$ relates throughput $X$ and average service demand $D$ for a resource under consistent accounting. These equations expose measurement inconsistency and capacity pressure; they do not predict tail latency or prove causality alone.

### Critical invariants

- workload, latency, error, correctness, and resource measurements use explicit populations, units, clocks, and boundaries;
- offered load, accepted work, completed work, retries, aborts, timeouts, and unknown outcomes reconcile;
- histograms preserve meaningful tails and are not replaced by averages or averaged percentiles;
- database state such as locks, MVCC history, WAL, checkpoints, compaction, vacuum, replication, and backups is correlated with service impact;
- telemetry collection has bounded overhead, cardinality, access, redaction, and retention;
- capacity claims include peak/skew, failure, maintenance, growth, recovery, and free-space headroom;
- alerts identify actionable user risk and include runbook context rather than firing on every internal fluctuation;
- experiments and forecasts remain within evidence and retain configuration/version provenance.

### Common failures

- measuring only successful completed requests and hiding rejected or timed-out offered work;
- reporting mean latency while p99.9 and maximum outage windows fail;
- treating 100% CPU as universally bad or 20% fleet average as proof of headroom;
- alerting on connection count without state, pool limit, query, or saturation;
- using one `EXPLAIN` plan from an unrepresentative parameter and cache state;
- increasing timeouts or pools while queues and lock contention grow;
- sizing live data without WAL, replicas, indexes, bloat, compaction, backups, rebuild, and free space;
- assuming monitoring is free and exporting SQL text, tenant IDs, or object names as labels;
- forecasting a regime change with a linear trend from a quiet week;
- validating normal capacity but not failover, repair, backup, or schema/index maintenance.

### Compact example

A stable workload completes 1,200 queries/s with average end-to-end database residence time 20 ms. Little's law estimates $L=1{,}200\times0.020=24$ concurrent in-system queries. If instrumentation reports 240, either boundaries/populations disagree, the system is not stable, or one measure is wrong. The equation diagnoses evidence; it does not say which component caused latency.

### Connections

The previous module, [Vector Search Engines](097-vector-search-engines.md), illustrates a system whose quality, latency, memory, updates, and recall must be measured jointly. The roadmap's next module, [Online Schema and Version Upgrades](../ROADMAP.md), uses observability and capacity to govern change. Prerequisites include [Profiling a Query Operator Pipeline](060-profiling-a-query-operator-pipeline.md), [Statistics and Histograms](063-statistics-and-histograms.md), [Cost Models](065-cost-models.md), and [Physical and Logical Backup](079-physical-and-logical-backup.md).

## Governing Question

A database dashboard is green at 35% average CPU, yet users experience minute-long stalls. Storage has 30% free bytes, but a rebuild fails. Query latency rises, connections accumulate, replication lags, and operators debate whether the cause is load, a plan, locks, I/O, vacuum, compaction, or the monitoring itself. What evidence can distinguish these mechanisms and prove enough capacity for the next failure and growth interval?

Observability is an inference discipline. Capacity is a conditional claim about a tested workload and state. Both begin with user-visible correctness and finish with reproducible interventions, not decorative dashboards.

## Why This Matters

Databases combine foreground work with hidden deferred work: dirty-page writeback, WAL archival, checkpoints, compaction, vacuum, statistics, index build, replication, repair, backup, and restore. They also coordinate through locks, latches, transactions, memory, connections, storage, and network. One bottleneck can express itself as latency everywhere.

Poor measurement makes incidents worse. A connection-pool increase can amplify queueing. A cache hit ratio can look healthy while the missed 1% dominates I/O. A replica lag measured in seconds can be wrong under clock skew or variable write volume. An alert on internal state can page constantly without predicting service harm.

Good evidence supports diagnosis, safe limits, forecasting, change review, and recovery. It also records uncertainty: a correlation is not a mechanism, a passing load test is not universal capacity, and an SLO does not prove data correctness.

## Prerequisites and Retrieval

Retrieve throughput, latency distributions, queues, utilization, saturation, Little's law, percentiles, sampling, causal graphs, controlled experiments, query plans, locks, buffer pools, WAL/checkpoints, MVCC/vacuum, replication lag, compaction, backup, and restore. Be able to distinguish counter, gauge, histogram, and event/log.

Retrieve the Google SRE “four golden signals”: latency, traffic, errors, and saturation. Use them as an entry frame, not a complete database schema. Database correctness, durability, stale reads, aborts, recovery point, and maintenance debt require additional evidence.

For each metric, record owner, type, unit, population, labels/dimensions, collection point, clock, reset/wrap, sampling, aggregation, retention, expected range, version, and limitations. For each experiment, record workload generator, open/closed load, dataset, distribution, configuration, topology, cache state, failure, duration, and acceptance criteria.

## Learning Objectives

After completing this module, you should be able to:

1. define workload and service SLIs that reconcile offered, accepted, completed, failed, and retried operations;
2. interpret latency histograms, wait events, utilization, saturation, queues, and maintenance state without causal overreach;
3. apply Little's law and utilization/service-demand arithmetic under stated assumptions;
4. construct a database evidence map from query through CPU, memory, storage, locks, WAL, replicas, and dependencies;
5. build failure- and maintenance-aware capacity envelopes and forecasts;
6. design bounded, secure telemetry and actionable SLO alerts;
7. run production-shaped load, fault, and recovery experiments without coordinated omission;
8. diagnose a bottleneck through competing hypotheses and reversible interventions.

## Core Exposition

**Begin with the service contract.** Define operations: read by key, search, transaction, ingest batch, report, schema change, backup, restore, failover. For each, state correctness, consistency/freshness, durability, latency, availability, throughput, and resource boundaries. A fast stale or incorrect read is not a successful request.

Define the denominator. An availability SLI might be valid requests completed correctly within deadline divided by eligible valid offered requests. State exclusions and unknown outcomes. If clients stop sending during failure, server logs alone cannot reconstruct offered demand.

**Reconcile flow counters.** Over a bounded interval, attempted work should reconcile through client rejection, admission rejection, accepted queue, completion, explicit failure, timeout/cancel, abort/retry, and still-in-flight state. Stable operation IDs help distinguish retry attempts from logical operations.

Throughput can remain flat while offered load grows because the server saturated and rejected/queued more. A success-only graph shows “stable traffic.” Preserve rates and cumulative counters with reset handling, and compare client and server perspectives.

**Measure latency distributions.** Define start and end: user end-to-end, gateway, pool queue, database protocol, transaction, statement, executor, lock wait, storage. Decompose without assuming independent additive percentiles. Sequential stage durations add per request; percentile of sums is not generally sum of percentiles.

Use histograms whose bounds cover objectives and failure tails, or mergeable sketches with documented error. Report p50, p95, p99, p99.9, maxima by relevant window, timeout, and censored/unfinished requests. An average of host p99 values is not fleet p99; aggregate underlying distributions when valid.

**Avoid coordinated omission.** A closed-loop client waits for a response before sending the next request. During a 10-second stall it records few operations, underweighting the outage and lowering offered rate. An open-loop generator schedules arrivals independently and records queue/rejection. Both are useful when named; production users may include feedback and abandonment.

Correct coordinated omission only with justified arrival assumptions and raw timing. Prefer designing the experiment to measure offered load directly. Include warm-up, steady state, burst, overload, recovery, and debt drain.

**Use Little's law carefully.** For a stable system over a long-enough interval with consistent boundaries, $L=\lambda W$. If 1,200 completions/s spend 20 ms on average inside the database boundary, mean in-flight work is 24. Queue-only Little's law uses queue population and wait time, not total response.

If arrivals exceed completions and backlog grows, steady-state assumptions fail. Little's law does not yield percentile latency, arrival distribution, or service capacity. Use it to check instrumentation and reason about concurrency, not to size blindly.

**Relate utilization and service demand.** If a resource spends fraction $U$ busy while throughput is $X$, measured demand per completion is $D=U/X$ under compatible intervals. With $U=0.8$ and $X=1{,}200$/s, $D\approx0.000667$ resource-seconds per query, or 0.667 ms of one-resource busy time.

The bottleneck throughput bound is approximately $1/D_{max}$ for one unit under simplified closed workload assumptions. Parallel devices, overlap, batching, variable classes, and background work require a multi-class resource model. Utilization near one often causes nonlinear queue tails, but low utilization can still hide a serialized lock or one hot core.

**Distinguish utilization from saturation.** CPU utilization says busy fraction; run queue and scheduling delay reveal demand. Storage utilization percentage of capacity is unrelated to device busy time. Device queue, latency, bandwidth, IOPS, and flush behavior matter. Memory “used” can be healthy cache; allocation stalls, reclaim, faults, and OOM reveal pressure.

The USE method—utilization, saturation, and errors for each resource—is a systematic checklist. Apply it to CPU/core, memory/NUMA, block device, filesystem/volume, network/interface/path, connection/thread/process pools, file descriptors, locks, and external services. Add database semantic state.

**Observe workload shape.** Record operations by normalized query/fingerprint, transaction, tenant/class, database/table/index, read/write, rows/bytes, parameters/selectivity class, result size, concurrency, and priority. Bound high-cardinality raw text and identifiers through secure sampled traces or logs.

Query frequency times service demand determines contribution. The slowest query may be rare; a 2 ms query at 100,000/s may dominate CPU. Report total time, calls, mean/tails, rows, buffers/blocks, WAL, temporary bytes, and failures per normalized identity.

**Read plans as hypotheses.** Estimated plans show the optimizer's model; execution plans add observed rows/timing/buffers depending on engine. A plan can change with parameters, statistics, prepared-plan policy, indexes, memory, parallelism, and version. `EXPLAIN ANALYZE` may execute and mutate for data-changing statements; use official product semantics and safe environments.

Compare estimated and actual cardinality at each operator, loops, rows removed, spill, cache/block activity, memory, and parallel work. A plan captured after caches warm or after statistics refresh may not reproduce the incident. Preserve query fingerprint, bind-value class, schema/statistics/version, configuration, and data snapshot evidence.

**Classify waits, then investigate.** Lock wait suggests contention but not which transaction should change. I/O wait can be buffer miss, checkpoint burst, temp spill, compaction, backup, or device issue. CPU wait can be queueing behind inefficient plans or background maintenance. Map wait episodes to blockers/resources and user impact.

For locks, collect waiter/blocker transaction identities, lock mode/object, age, statement fingerprint, application owner, and rollback cost under access policy. A “kill oldest” runbook needs invariant and unknown-outcome handling.

**Observe transaction health.** Track commit, rollback, retry, deadlock, serialization failure, timeout, long-running/open/idle transaction, snapshot age, undo/version retention, lock footprint, and transaction size. Long idle transactions can pin cleanup and make a storage problem appear later.

Separate application retry success from database abort rate. Excess retries add offered load and hide user latency. Use one logical operation ID across attempts and enforce idempotency where effects can be unknown.

**Observe caches and memory by ownership.** Track buffer/page cache, plan cache, index/filter cache, sort/hash/work memory, connections, maintenance, operating-system cache, and allocator fragmentation. One global hit ratio hides which workload misses and how costly misses are.

A 99% hit ratio over a million accesses still yields 10,000 misses; if each miss is slow and clustered, tails fail. Record bytes/pages, miss latency, eviction, dirty state, working-set change, and pressure. Raising per-query memory times concurrency can exceed physical memory.

**Observe WAL and checkpoints.** Track logical change bytes, WAL generation, sync/group commit latency, flush/write bandwidth, segment/archive backlog, checkpoint frequency/duration, dirty pages, writeback, and recovery replay estimate. Write latency may be stable while archive debt threatens RPO or disk.

Checkpoints can cause bursty I/O if work is concentrated. Spreading writeback reduces spikes but uses sustained capacity. A failover/restart experiment verifies replay time; WAL byte rate alone does not prove RTO.

**Observe MVCC maintenance.** PostgreSQL-style vacuum reclaims or marks reusable storage and protects transaction-ID semantics under product-specific rules. Other engines use compaction or garbage collection. Track dead/obsolete versions, oldest snapshot/transaction, cleanup age, table/index bloat evidence, maintenance progress, and blocked reasons.

Do not run aggressive cleanup without understanding snapshots, replicas, CDC, backups, and I/O. Low dead-row count can coexist with a dangerous oldest transaction; high dead count can be harmless in a soon-dropped partition. Interpret by lifecycle.

**Observe replication and durability.** Lag has multiple coordinates: byte/sequence distance, commit/apply position, time since last applied record, and estimated catch-up. Clock-derived seconds can mislead when writes stop or clocks skew. Track send, receive, durable, replay/apply, conflict/error, slot/retention, and oldest required log.

Measure synchronous acknowledgement latency and unavailable writes separately. Verify failover data against acknowledged operation history, not merely role change. Replica reads need staleness/version evidence and query-specific semantics.

**Observe compaction, repair, and indexes.** LSM and specialized engines create flush/compaction debt; distributed stores create repair/streaming debt; index builds create scans, sort, WAL, cache, and temporary space. Record arrival and service rates, pending bytes/tasks, amplification, stalls, free space, and projected drain time.

Maintenance is capacity demand. If foreground uses 80% and required maintenance uses 30%, the system is unstable despite either measurement alone. Schedule concurrent production combinations in tests.

**Capacity is multidimensional.** Define axes: operations/s by class, concurrency, data/index/WAL bytes, working set, key/tenant skew, query range/result, transaction size, replication factor, background work, failure topology, and growth. An envelope is the region where correctness and SLOs pass, not one maximum QPS.

Find the first violated invariant or SLO as load increases. Record knee points, queues, bottleneck resource, debt, and recovery. After overload stops, require backlog/replication/maintenance to drain within objective; otherwise the test has not completed.

**Include failure capacity.** Normal capacity must leave room for one node/AZ failure, failover, replica rebuild, repair, backup, and planned maintenance according to the service contract. For three equal nodes carrying 2,400 units/s, normal average is 800 each; loss of one requires 1,200 each on two nodes before overhead. If tested per-node sustainable service is 1,100, N+1 fails despite normal 73% utilization.

Do not assume load balances evenly after failure. Shard leaders, hot tenants, cache coldness, recovery traffic, and topology constraints create skew. Test the actual failover placement and degraded duration.

**Plan storage completely.** Forecast live data, indexes, replicas, WAL/log retention, snapshots/backups, temp/spill, bloat/obsolete versions, compaction overlap, index rebuild old+new, restore staging, growth between interventions, and reserved free space. A filesystem at 70% can still lack room for a 50% rewrite.

Use logical and physical growth rates. Compression ratio changes with data. Deletion may not reclaim immediately. Forecast uncertainty bands and thresholds tied to action lead time, not a precise exhaustion date.

**Forecast mechanisms, not lines alone.** Decompose growth into customers, events/customer, bytes/event, indexes, retention, replicas, and amplification. Model seasonality, launches, migrations, retention changes, and failure. Backtest forecasts against past windows and update error.

Linear extrapolation within a stable regime can be useful. It is invalid across a shard-count, schema, compression, product, workload, or policy change without a new model. Keep scenario ranges and trigger points.

**Build actionable alerts.** Page on user-visible SLO burn, correctness/durability risk, or imminent capacity loss requiring prompt human action. Ticket slower trends. Dashboard exploratory context. Multi-window burn-rate alerts balance fast severe incidents and slow exhaustion.

Each alert names service, SLI/population, current impact, likely evidence links, runbook, owner, and safe mitigations. Avoid alerting on every host when one service incident is already paging. Test alert delivery and runbooks under actual faults.

**Control telemetry cost and risk.** Instrumentation consumes CPU, allocation, locks, network, storage, and operator attention. Measure overhead at normal and overload states; sampling that changes when load rises can hide incidents. Use bounded label sets and stable fingerprints.

SQL text, bind values, plans, usernames, tenant IDs, object names, and traces may contain secrets or regulated data. Redact at collection, restrict access, encrypt, audit, and expire. Do not export unbounded values as metric labels.

**Diagnose with competing hypotheses.** For a latency increase, list hypotheses such as workload growth, plan regression, lock contention, cache churn, checkpoint, storage degradation, replica/connection dependency, maintenance, or telemetry change. State predicted evidence for each. Seek disconfirming observations.

Use reversible interventions: route a canary, restore one plan, cap one workload, change one resource limit, pause optional maintenance safely, or reproduce from a snapshot. Correlation plus a mechanism-consistent response strengthens causality; avoid changing five knobs together.

**Validate capacity experiments.** Use production-shaped data volume, distribution, hot keys, parameter classes, read/write mix, transactions, cache state, replicas, and maintenance. Record tool and environment versions. Generate offered load independently enough to observe queueing, include failures, and preserve client histories.

Verify result correctness, durability, staleness, aborts, and unknown outcomes alongside latency. Run long enough for checkpoints, compaction, vacuum, rollups, backup, cache turnover, and thermal/storage steady state. Report only the tested envelope.

The executable fixture below checks finite Little's-law, utilization-demand, and N+1 arithmetic. It is not a queueing simulation, capacity forecast, load test, failure experiment, or proof that the modeled workload is stable.

<!-- bijux-verify: {"id":"finite-capacity-arithmetic","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"mean_in_flight=24.0\nservice_demand_ms=0.667\nnormal_per_node=800\ndegraded_per_node=1200\ndegraded_capacity_pass=false\nspare_per_degraded_node=-100\nstable_assumption_required=true\nevidence=finite_capacity_arithmetic\n","stderr":""}} -->
```python
throughput_qps = 1200
mean_latency_seconds = 0.020
resource_utilization = 0.80
total_load = 2400
nodes_normal = 3
nodes_degraded = 2
tested_per_node = 1100

mean_in_flight = throughput_qps * mean_latency_seconds
service_demand_ms = resource_utilization / throughput_qps * 1000
normal_per_node = total_load // nodes_normal
degraded_per_node = total_load // nodes_degraded
spare = tested_per_node - degraded_per_node
print(f"mean_in_flight={mean_in_flight:.1f}")
print(f"service_demand_ms={service_demand_ms:.3f}")
print(f"normal_per_node={normal_per_node}")
print(f"degraded_per_node={degraded_per_node}")
print(f"degraded_capacity_pass={str(tested_per_node >= degraded_per_node).lower()}")
print(f"spare_per_degraded_node={spare}")
print("stable_assumption_required=true")
print("evidence=finite_capacity_arithmetic")
```

## Definitions and Notation

- **Offered load** is attempted work rate; **accepted load** enters service; **throughput** completes under a named success definition.
- **Latency** is elapsed time under named endpoints; **queue time** is waiting before service.
- **Utilization** $U$ is busy fraction; **saturation** is delayed demand; **error** is failed/incorrect behavior under the contract.
- $L$ is mean work in a boundary, $\lambda$ compatible mean completion rate, and $W$ mean residence time in Little's law.
- $X$ is throughput and $D$ measured average resource service demand per completion under utilization law $U=XD$.
- An **SLI** measures service; an **SLO** sets its target and window; **error budget** is permitted bad fraction/count under that contract.
- A **histogram** counts observations in value ranges; a **percentile** is a distribution quantile.
- A **wait event** classifies blocked/non-progress state at an observation point.
- **Maintenance debt** is pending required work such as vacuum, compaction, repair, archive, or rebuild.
- A **capacity envelope** is a tested multidimensional workload/state region where requirements hold.
- **Headroom** is capacity beyond demand under specified normal/degraded scenarios.
- **Coordinated omission** under-samples slow periods because new requests depend on prior completion.
- A **query fingerprint** groups structurally equivalent statements without retaining raw sensitive values.
- **Burn rate** compares observed error-budget consumption speed with sustainable budget rate.

## Mechanisms, Invariants, or Proof Structure

**Flow conservation.** Over interval boundaries, starting in-flight plus offered attempts equals rejected before acceptance plus accepted outcomes plus ending in-flight, with retry attempts and logical operations separately identified. Disagreement reveals missing instrumentation, incompatible clocks/populations, or unclassified outcomes.

**Little's-law premise.** In a stable observed boundary without indefinite loss of work, integrate number in system over time and divide by interval to obtain $L$; completed arrivals sample residence $W$; long-run arrivals/completions approach $\lambda$, yielding $L=\lambda W$. Growing queues, short windows, and mismatched populations break the use.

**Utilization law.** Total busy time over interval is approximately completions $X\Delta t$ times mean service demand $D$, so dividing by $\Delta t$ gives $U=XD$. Background classes and overlapping/parallel service require separate accounting; the equation does not give queue-delay distribution.

**Histogram aggregation.** Fleet percentile requires a merged distribution with compatible buckets/sketch semantics and weights. Averaging node percentiles loses population sizes and distribution shape; two fleets can share average p99 and have different global tails.

**Failure-headroom obligation.** For every required failure/maintenance placement, route the modeled workload and background recovery to remaining units, include skew/cold state, and show every unit/resource and SLO remains within tested envelope. Normal fleet average is not this proof.

**Storage safety.** Before an operation that can require temporary bytes $T$, physical used $B$, growth during completion $G$, and reserve $R$, capacity $C$ must satisfy $B+T+G+R\le C$ under the scenario. Reclamation that itself needs $T$ cannot be the only response after free space falls below it.

**Causal diagnosis standard.** Correlation establishes co-occurrence. A credible mechanism adds temporal order, scope correspondence, resource/query evidence, exclusion of alternatives, and preferably a reversible intervention or reproduction. Observability narrows claims; it does not automatically prove them.

## Alternatives and Trade-Offs

**Metrics versus traces/logs/profiles.** Metrics provide bounded aggregates and alerting; traces connect sampled request stages; logs capture discrete detail; profiles attribute CPU/allocation. Combine them with stable identity and privacy rather than forcing one signal to answer everything.

**Polling versus event instrumentation.** Polling is simple and bounded but can miss short states. Events preserve transitions at volume/cardinality cost. Cumulative counters plus sampled gauges often provide robust accounting.

**High-cardinality detail versus bounded telemetry.** Full dimensions speed diagnosis but threaten monitoring cost and privacy. Keep bounded metric labels, sampled secured exemplars/traces, and on-demand database views with access controls.

**Static threshold versus SLO burn.** Static resource thresholds can predict exhaustion but page during harmless variation. SLO burn follows user impact but may react after hidden durability/capacity risk. Use both, with clear urgency and ownership.

**Scale up versus scale out.** Larger nodes improve local working set and reduce distribution; more nodes add aggregate capacity and fault units but require repartitioning/replication. Hot keys and coordination may not scale out.

**More connections versus admission control.** Connections can expose concurrency needed for throughput; excessive active work increases memory, locks, queues, and context switching. Bound active work and queue intentionally.

**Reactive versus scheduled maintenance.** Aggressive reactive work restores health but competes with users; scheduled service preserves steady debt at reserved capacity. Workload surprises require both headroom and throttles.

**Forecast versus load test.** Forecasts explore future scenarios from historical drivers; tests measure one controlled envelope. Backtest forecasts and use tests to calibrate mechanism assumptions. Neither replaces failure evidence.

## Failure Modes and Misconceptions

- **“Green dashboard means healthy.”** Missing correctness, offered load, tails, or debt can conceal failure.
- **“Average CPU is capacity.”** hot cores, locks, storage, skew, and failure placement can bind first.
- **“Mean latency predicts tails.”** distributions and queueing are not summarized by one mean.
- **“Percentiles add across stages.”** per-request dependence and distributions prevent simple addition.
- **“A wait event is the root cause.”** it identifies where work waited, not why demand/service changed.
- **“More connections increase throughput.”** after useful concurrency they amplify queues and memory.
- **“Cache hit ratio close to 100% is enough.”** miss count, cost, burst, and workload slice matter.
- **“Replication lag in seconds is precise.”** clock and write-rate semantics can make it misleading.
- **“Free space equals usable headroom.”** rebuild, compaction, WAL, growth, and reserve consume it.
- **“Load-test QPS is production capacity.”** dataset, mix, load model, duration, failures, and correctness bound the claim.
- **“Monitoring has negligible overhead.”** locks, cardinality, collection, export, and storage can perturb service.
- **“Correlation proves regression cause.”** change and latency may share a third driver.
- **“Linear forecast gives exhaustion date.”** regime, seasonality, uncertainty, and action lead time matter.
- **“Failover success proves N+1 capacity.”** degraded tails, staleness, debt, and recovery must pass.
- **“Restart clears the incident.”** it can erase evidence and postpone/deepen underlying debt.

## Worked Examples

### Example 1

**Situation.** Clients attempt 10,000 requests; server accepts 8,000, completes 7,700 successfully, fails 200, and has 100 in flight. Two thousand were rejected at admission.

The accounting reconciles: 2,000 rejected plus 7,700 success plus 200 failure plus 100 ending in-flight equals 10,000, assuming none started in flight and no retries are double-counted. A server success rate of 7,700/7,900 hides admission rejection; user success is 77% before deadline rules.

**Conclusion.** Flow reconciliation prevents a success-only denominator from hiding overload.

### Example 2

**Situation.** 1,200 queries/s average 20 ms within the database; observed mean active-plus-queued is 240.

Little's law predicts 24 for stable compatible boundaries. Tenfold mismatch suggests latency measured only execution while population includes pooled clients, one rate excludes retries, sampling is biased, or backlog grows. Inspect definitions before using either value.

**Conclusion.** Queueing arithmetic is an instrumentation consistency test, not an automatic fix.

### Example 3

**Situation.** One CPU-equivalent resource is 80% busy at 1,200 completions/s.

Measured service demand is $0.8/1{,}200=0.000667$ seconds, about 0.667 ms per completion. A naive single-resource ceiling is 1,500/s, but background work, classes, parallelism, and tail objectives require lower tested capacity.

**Conclusion.** Utilization yields a scoped demand estimate, not a production limit by itself.

### Example 4

**Situation.** Node A serves 1,000 requests at p99 10 ms; node B serves one million at p99 200 ms. An operator averages node p99 to 105 ms.

The value has no fleet-percentile meaning. Node B dominates population, but even weighting p99 values would not reconstruct distribution. Merge compatible histograms/sketches or retain raw samples under policy.

**Conclusion.** Percentiles must be aggregated from distributions, not averaged.

### Example 5

**Situation.** A query plan estimates 100 rows from an index and observes 10 million, then spills a hash operation.

The cardinality error explains a plan/memory hypothesis. Investigate data/parameter skew, stale or inadequate statistics, correlation, predicate semantics, and prepared-plan behavior. Compare alternative plan in a canary and verify outputs; do not simply raise work memory fleet-wide.

**Conclusion.** Estimated-versus-actual operator rows connect optimizer evidence to resource consequences.

### Example 6

**Situation.** Buffer hit ratio is 99%, with ten million page accesses/minute and 12 ms average miss service.

One percent means 100,000 misses/minute, about 1,667/s. Multiplying by 12 ms yields roughly 20 seconds of device-service demand per wall second before parallelism/caching details. Slice by query and timing; a “good” ratio can still saturate storage.

**Conclusion.** Convert ratios into rates and service demand.

### Example 7

**Situation.** Three nodes carry 2,400 units/s; one node fails; each survivor is tested to 1,100.

Normal average is 800/node. Degraded demand is 1,200/node before rebuild and cache-cold overhead, exceeding tested service by 100. The cluster lacks N+1 capacity even though normal utilization is about 73% of 1,100.

**Conclusion.** Failure placement defines headroom.

### Example 8

**Situation.** A 10 TB volume has 7 TB used. An index rebuild needs 2.5 TB candidate space, expected growth during build is 0.4 TB, and reserve is 0.5 TB.

Required footprint is $7+2.5+0.4+0.5=10.4$ TB, so “30% free” is insufficient. Add space, rebuild in smaller governed units if supported, reduce safe retained bytes, or move the operation. Do not rely on failure cleanup.

**Conclusion.** Capacity must include temporary, growth, and reserve bytes.

### Example 9

**Situation.** p99 latency rises exactly when checkpoint bytes spike.

This correlation supports but does not prove a checkpoint cause. Check storage queue/latency, dirty pages, query waits, other jobs, and scope. Reproduce with controlled checkpoint pacing or compare an otherwise equivalent canary. Preserve durability; pausing checkpoints blindly can move risk to WAL/recovery.

**Conclusion.** Mechanism and reversible evidence turn correlation into a stronger diagnosis.

### Example 10

**Situation.** A closed-loop load test reports stable 5,000 QPS and p99 100 ms during a 10-second database stall.

Waiting clients issued little new work during the stall, so offered rate fell and few latency samples represented users who would have arrived. Re-run with scheduled arrivals, record rejected/queued/censored work, preserve client history, and include recovery/debt drain. State whether production feedback resembles either model.

**Conclusion.** Load generation determines what latency and capacity evidence means.

## Cross-Program Connections

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies queueing, utilization, saturation, capacity, telemetry, fault experiments, and causal diagnosis. Database state provides domain-specific mechanisms.

[Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) connects SLOs, burn alerts, incident response, canaries, rollback, and change evidence. Database reliability must be user-visible and operational.

[Operating Systems](../../22-operating-systems/ROADMAP.md) connects CPU scheduling, memory pressure, page cache, storage queues, filesystem, networking, and observability primitives. Database waits must map to those resources.

[Data Engineering](../../19-data-engineering/ROADMAP.md) connects pipeline freshness, backlog, replay, data quality, and workload maintenance. Database telemetry must include ingestion and downstream consequences.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) connects standardized telemetry, quotas, tenancy, capacity provisioning, and operational interfaces. Abstraction must retain database-specific signals.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects sensitive SQL/parameters, telemetry access, audit, retention, injection, and incident evidence. Observability data is production data.

## References

- Rob Ewaschuk, [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/), in *Site Reliability Engineering*, 2016. Four golden signals, symptom versus cause, and monitoring design.
- Google SRE authors, [Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/), in *The Site Reliability Workbook*, 2018. Error-budget burn and multi-window alert design.
- Mike Ulrich, [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/), in *Site Reliability Engineering*, 2016. Overload, queues, retries, and graceful degradation.
- PostgreSQL Global Development Group, [Monitoring Database Activity](https://www.postgresql.org/docs/current/monitoring-stats.html), current documentation checked 2026-09-05. Statistics views, cumulative statistics, activity, progress, and wait events.
- PostgreSQL Global Development Group, [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html), current documentation checked 2026-09-05. Estimated and execution-plan interpretation.
- PostgreSQL Global Development Group, [Routine Vacuuming](https://www.postgresql.org/docs/current/routine-vacuuming.html), current documentation checked 2026-09-05. MVCC cleanup, statistics, visibility, and transaction-ID maintenance.
- PostgreSQL Global Development Group, [Resource Consumption](https://www.postgresql.org/docs/current/runtime-config-resource.html), current documentation checked 2026-09-05. Memory, disk, kernel, background writer, and resource settings.
- Oracle, [MySQL 8.4 Performance Schema](https://dev.mysql.com/doc/refman/8.4/en/performance-schema.html), current documentation checked 2026-09-05. Instrumentation architecture, events, consumers, and performance considerations in another engine.
- OpenTelemetry Authors, [Semantic conventions for database client calls](https://opentelemetry.io/docs/specs/semconv/database/), current specification checked 2026-09-05. Database span/metric semantic conventions and stability guidance.
- Brendan Gregg, [The USE Method](https://www.brendangregg.com/usemethod.html), current page checked 2026-09-05. Systematic utilization, saturation, and error analysis by resource.

## Exercises

### Exercise 1

Define offered load, throughput, latency, utilization, saturation, SLI, SLO, wait event, headroom, and capacity envelope. Explain why a database can have low average utilization and still fail.

### Exercise 2

A stable service completes 4,000 transactions/s with 30 ms average residence. CPU utilization is 72% across a normalized one-CPU accounting unit. Compute mean in-system work and measured CPU demand per completion, then list assumptions and missing capacity axes.

### Exercise 3

Users report latency while CPU is 40%, connections are 95% of maximum, lock waits rise, one transaction is three hours old, and dead-version storage grows. Build competing hypotheses, identify the most discriminating evidence, and propose a safe intervention.

### Exercise 4

Design an N+1 capacity test for a six-node sharded database with hot tenants, synchronous replicas, nightly backup, weekly repair, one online index build, and a p99 write SLO. Include workload, faults, accounting, and completion criteria.

### Exercise 5

The telemetry platform is increasing database load and leaking raw SQL parameters. Redesign metrics, traces, logs, sampling, access, and retention while preserving incident diagnosis and validating that the new system does not hide overload.

## Answers to the Exercises

### Answer 1

**Offered load** is attempted work; **throughput** is completed work. **Latency** is elapsed time under named endpoints. **Utilization** is resource busy fraction; **saturation** is waiting/delayed demand. An **SLI** measures a user-relevant outcome and an **SLO** targets it over a population/window. A **wait event** classifies non-progress. **Headroom** is spare usable capacity under named scenarios; a **capacity envelope** is the tested multidimensional passing region. Low fleet average can hide one hot shard/core, a serialized lock, connection queue, storage tail, memory allocation stall, stale replica, maintenance debt, or failed zone placement.

### Answer 2

Little's law gives $L=4{,}000\times0.030=120$ mean transactions in the boundary. CPU demand is $D=0.72/4{,}000=0.00018$ seconds, or 0.18 ms of normalized CPU busy time per completion. Assumptions include stable interval, compatible populations/boundaries, completed-flow accounting, and meaningful one-unit CPU normalization. Missing axes include query classes/skew, p99 latency, concurrency, locks, memory, storage IOPS/bandwidth/latency, network, cache, WAL/sync, replicas, maintenance, failure, data growth, free space, recovery, and correctness.

### Answer 3

The leading mechanism is a long transaction pinning MVCC history and possibly locks, causing waiters/connections and dead-version retention; alternatives include an application pool leak, one lock-hot object, or a slow dependency. Collect waiter-blocker graph, transaction age/state/owner, lock modes/objects, query fingerprints, pool queue/active state, snapshot/cleanup horizon, dead bytes, storage/CPU, and user-operation correlation. Determine whether the three-hour transaction blocks locks, cleanup, or both. Contact owner and choose a safe cancel/rollback only after checking transaction effect, retry/idempotency, rollback cost, and unknown outcomes. Bound idle/statement/transaction duration and admission afterward, then verify waiters drain, connections recover, cleanup catches up without I/O collapse, storage declines, and user tails recover.

### Answer 4

Replay production-shaped operations by shard/tenant with open offered-load accounting, hot-key bursts, realistic transactions/data/cache, and client correctness histories. Establish normal steady state with backup, repair, and index build overlaps scheduled as production permits. Fail one node in the worst placement, verify synchronous quorum/leader movement, cold caches, hot-tenant routing, replica rebuild, and maintenance. Record offered/accepted/completed/retried/unknown writes, p99 and tails, durability/freshness, per-node/shard CPU/memory/storage/network, locks, WAL, lag, queues, debt, and free/temp bytes. Passing requires no correctness/durability violation, p99 write SLO and availability under declared degraded behavior, no unit beyond tested limits, sufficient storage/rebuild reserve, and all lag/debt draining within recovery objective after fault. Repeat relevant placements; one easy node failure is insufficient.

### Answer 5

Use bounded metric labels such as database role, normalized operation class, status, and shard pseudonym; never SQL text, bind values, tenant/user IDs, table names with unbounded tenancy, or error payloads. Retain counters/histograms for offered flow, latency, errors, saturation, waits, and maintenance. Generate stable salted query fingerprints at collection and keep sampled plans/traces in an encrypted, audited, short-retention store with redacted values. Sample adaptively only with a guaranteed error/tail channel and record sampling probability; preserve exemplars linking metrics to secured traces. Rate-limit exporters, batch off critical paths, and expose collection drops/queue/CPU. Validate with production-shaped overload and faults: compare client truth to old/new telemetry, confirm tails/rejections remain visible, measure DB and telemetry overhead, attempt secret extraction, test access/audit/expiry, and verify runbooks still identify blockers and plans.
