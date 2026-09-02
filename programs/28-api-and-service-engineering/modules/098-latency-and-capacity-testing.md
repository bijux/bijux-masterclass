---
module_id: API-098
program: API & Service Engineering
level: 2
module_number: 98
title: Latency and Capacity Testing
status: complete
last_verified: 2026-09-02
---

# Latency and Capacity Testing

## One-Page Review

### Governing question

How can teams measure an API's latency distribution, sustainable throughput, resource envelope, overload behavior, scaling lag, and recovery under a production-relevant workload without letting the load generator, environment, coordinated omission, caches, or unsafe side effects invalidate the result?

### Essential definitions

- **response time** is elapsed time observed at a named boundary; **service time** is time actively spent by a component and excludes some queue/network delay.
- **latency distribution** is the population of response times, summarized with counts, histograms, quantiles, and threshold fractions—not only a mean.
- **throughput** is completed work per unit time; **arrival rate** is attempted new work per unit time; accepted and successful throughput can differ.
- An **open workload model** schedules arrivals independently of response completion. A **closed model** holds a fixed population whose next operation waits for the previous one.
- **coordinated omission** occurs when a generator reduces observations/arrivals while the system is slow and therefore under-reports the delay users at the intended arrival schedule would experience.
- **capacity** is the greatest offered workload mix satisfying correctness, latency, error, saturation, stability, and recovery criteria in a declared configuration—not an unconstrained maximum RPS.
- The **saturation knee** is the region where added offered load produces disproportionate queueing/latency/error rather than useful throughput.
- A **capacity envelope** maps workload, mix, data, topology, configuration, dependency state, resource allocation, and failure assumptions to verified outcomes.
- **soak**, **spike**, **stress**, **breakpoint**, and **recovery** tests emphasize steady duration, abrupt change, controlled overload, failure threshold, and restoration respectively.

### Central model, mechanism, or theorem

Little's Law relates average concurrency $N$, completed/accepted arrival rate $\lambda$, and average time in system $W$ under a stable boundary:

$$
N=\lambda W.
$$

As utilization approaches a bottleneck's limit, queues and latency usually become nonlinear. A simplified M/M/1 model gives $W=1/(\mu-\lambda)$ for service rate $\mu$ and $\lambda<\mu$; real services are not M/M/1, but the divergence explains why operating at the measured breakpoint is unsafe. Define usable capacity $C$ as the largest offered load for which correctness, latency/error SLOs, resource guardrails, steady-state slope, and post-load recovery all pass under the declared workload vector.

### Critical invariants

The test specifies user journeys, operation mix, payload/data distributions, identities/tenants, protocol/client behavior, cache state, think time, arrival model, duration, regions, versions, dependencies, retry policy, side effects, and exact artifacts/configuration/resources. The generator is independently capacity-tested, synchronized, close enough to real clients, and reports scheduled, started, dropped, accepted, completed, successful, and retried work separately.

Warm-up, steady-state, ramp, overload, cooldown, and recovery windows are labeled; results never blend them accidentally. Latency is measured end to end and by phase using aggregatable histograms, with failures/timeouts included in outcome accounting. Correctness and invariant checks continue under load. Tests locate the bottleneck and demonstrate graceful shedding/recovery, not merely reach a high number. Results carry uncertainty, repetitions, raw distributions, telemetry, cost, environment provenance, and expiry.

### Common failures

Testing one trivial endpoint; replaying uniform tiny payloads; unrealistic cache hit; warm cache presented as cold capacity; empty database/index; one tenant/connection; no auth/TLS/proxy; unlimited generator connections; generator CPU/network bottleneck; closed model used for fixed arrival claim; dropped iterations ignored; only successful latency measured; averages/p99 of per-instance p99s; no correctness checks; retries counted as demand; load test causes real payments/email; shared noisy environment; autoscaling during baseline without recording lag; short run hiding leak/GC; breakpoint called capacity; no overload/recovery; dependency sandbox throttles; unpinned versions; and comparing runs with different mixes/configuration.

### Compact example

At 800 arrivals/s, p99 is 180 ms and success is 99.95%. At 900/s, accepted throughput reaches only 835/s, p99 becomes 1.4 s, database pool wait rises, in-flight work doubles, and the generator reports 20 dropped arrivals. A closed 200-user test misleadingly reports only 820/s and p99 600 ms because slow completions suppress new work. **Conclusion:** capacity is below the knee under an open workload and must include scheduled/dropped work, queueing, correctness, and recovery—not the highest completed rate.

### Connections

[Timeout Budgets](071-timeout-and-deadline-budgets.md), [Retries](072-retries-and-backoff.md), [Circuit Breaking](073-circuit-breaking-and-bulkheads.md), [Load Shedding](074-api-level-load-shedding.md), [Backpressure](075-backpressure-across-service-boundaries.md), [Fan-Out and Tail Latency](077-fan-out-and-tail-latency.md), [Failure Amplification](080-preventing-failure-amplification-across-service-calls.md), [Service Mesh](093-service-mesh-relationships.md), [Integration Testing](095-integration-and-end-to-end-api-testing.md), and [API Telemetry](097-api-metrics-logs-and-traces.md) define the behavior and evidence. Readiness review consumes the capacity envelope.

## Governing Question

How should teams design, execute, analyze, reproduce, and operationalize API performance experiments so that latency and capacity claims remain valid across real workloads, state, scale, overload, change, and recovery?

## Why This Matters

Performance is a system property. An endpoint that takes 20 ms alone can take seconds when its connection pool queues, cache misses, authorization service slows, large tenants scan more data, retries amplify, garbage collection thrashes, or all replicas refresh simultaneously. Average resource utilization can look safe while one shard or lock saturates.

Capacity planning needs an empirical mapping from resources and configuration to useful user work. Google SRE guidance explicitly recommends load testing instead of tradition to establish resource-to-capacity ratios and testing beyond rated capacity to verify overload behavior. A number measured months ago on a different binary, dataset, dependency, or traffic mix is not current evidence.

Bad tests create dangerous optimism. A closed generator slows its own arrivals when the SUT slows. Success-only histograms omit timeouts. A cached read benchmark says nothing about writes. A generator bottleneck masquerades as server capacity. A five-minute run misses memory growth and compaction. “Maximum RPS” rewards rejection, corruption, and unstable queues.

The goal is a decision-ready envelope: what load this exact system can serve at defined quality, what saturates first, how it sheds, how it scales, what it costs, and whether it returns to a healthy state.

## Prerequisites and Retrieval

Retrieve [HTTP Versions](009-http-1-1-http-2-and-http-3-semantics.md), [Long-Running Operations](018-long-running-operations.md), [Bulk and Batch](019-bulk-and-batch-operations.md), [Rate Limits](039-rate-limits-and-quotas.md), [gRPC Streaming](053-unary-and-streaming-grpc.md), [GraphQL Execution](056-graphql-execution-resolvers-and-batching.md), [Ordering and Partition Keys](065-ordering-and-partition-keys.md), [Timeouts](071-timeout-and-deadline-budgets.md), [Retries](072-retries-and-backoff.md), [Load Shedding](074-api-level-load-shedding.md), [Backpressure](075-backpressure-across-service-boundaries.md), [Caching](076-api-caching-and-invalidation.md), [Tail Latency](077-fan-out-and-tail-latency.md), [Failure Amplification](080-preventing-failure-amplification-across-service-calls.md), [Integration Testing](095-integration-and-end-to-end-api-testing.md), and [API Telemetry](097-api-metrics-logs-and-traces.md).

Retrieve production arrival/concurrency distributions and seasonality; journey/operation/payload/tenant/client/version/region mix; cache hit/miss and data size/skew; SLOs and correctness invariants; gateway/mesh/discovery/TLS/auth; retries/timeouts/connections; topology/resources/limits/autoscaling; database/broker/cache/dependency capacity; deploy/config/schema revisions; generator/tool/network limits; previous runs/incidents; cost and forecast; and rollback/load-shed/degradation/recovery policy.

## Learning Objectives

After completing this module, you can:

1. distinguish arrival, concurrency, throughput, completion, service time, response time, queue time, utilization and saturation;
2. choose open, closed, hybrid and trace-replay models according to the production mechanism and test claim;
3. detect coordinated omission, generator bottlenecks, dropped work, measurement bias, caching/state and environment confounders;
4. construct representative mixes across operations, payloads, tenants, versions, clients, protocols, data skew, cache state and failures;
5. design baseline, ramp, load, stress, spike, soak, scalability, overload and recovery experiments;
6. apply Little's Law and queueing intuition without confusing models with deployed measurements;
7. measure latency distributions, useful throughput, correctness, resources, queues, dependencies, retries, shedding and cost;
8. locate saturation knees and define safe capacity envelopes/headroom rather than unstable breakpoints;
9. compare versions/configurations with repetitions, controlled variables, raw distributions and uncertainty; and
10. convert results into capacity plans, autoscaling thresholds, SLOs, admission policy, runbooks, regression gates and expiry.

## Core Exposition

### Frame a falsifiable capacity claim

State a claim before a script: “version p12 on eight 4-vCPU replicas, database configuration d7, production-like 60/25/10/5 operation mix and 40% cache hit sustains 1,200 logical arrivals/s for 45 minutes with ≥99.9% correct outcomes, p99 ≤300 ms, no resource above guardrail, no growing queue, and recovery within five minutes after 150% spike.”

Name every controlled variable, pass threshold, observation window, and invalidation condition. Separate baseline per-operation service cost, realistic mixed workload, saturation search, overload behavior, scaling, failure headroom, soak, and regression comparison. One run should answer a bounded question.

Capacity is configuration-specific and time-bounded. Record artifact/image digests, flags, runtime, kernel, instance type/limits, replica count, topology, dependency/data/schema versions, routes, policies, generator/tool version and test data seed. Assign owner and expiry after material code, data, dependency, infrastructure or mix change.

### Model production demand

Measure logical user operations, not only downstream HTTP calls. Build a weighted journey mix including reads/writes/search/bulk/streaming/polling, authentication, cache hit/miss, success/error, payload sizes, tenant/data skew, clients/protocol versions and geographic network.

Preserve correlations: large payloads may belong to large tenants and expensive filters; writes cause later reads/cache invalidation; login creates burst; event fan-out follows orders. Independent uniform fields can create impossible cheap cases.

Model arrival seasonality, burstiness and synchronization. Poisson-like independent arrivals are a useful baseline, but launches, cron jobs, reconnects, cache expiry and client retries can be correlated. Reproduce production interarrival histograms or explicit burst scenarios.

Protect external effects. Use synthetic tenants, sandbox/fake payment/email, idempotency keys, egress controls, quotas and exact cleanup. Test data must be large/skewed enough to exercise indexes, partitions, serialization and cache eviction without copying unredacted production data.

### Choose open and closed workload models

In a closed model, a fixed user/worker population starts new work after completion/think time. This represents a bounded interactive population or connection-constrained protocol. When response time increases, arrival rate falls. It cannot establish behavior at a fixed external arrival schedule unless that feedback is genuinely how clients behave.

In an open model, the generator schedules new iterations independently of SUT completion. It represents arrivals such as public requests, jobs/events, or many independent users. Grafana k6 documents constant/ramping arrival-rate executors and identifies the closed-model slowdown as coordinated omission for fixed-throughput goals.

Hybrid systems require both: fixed streaming connections each generate messages; a finite worker pool consumes an open queue; sessions arrive openly but act closed within a session. Model layers explicitly.

Record scheduled, started, generator-dropped, sent, server-received, admitted, rejected, completed, correct, timed out, cancelled, retried and effects. If the generator cannot start the target schedule because virtual users/CPU/connections are exhausted, the run does not prove SUT capacity at that schedule.

### Apply Little's Law carefully

For a stable boundary over a sufficiently long interval, average in-system work $N=\lambda W$. At 1,000 completed operations/s and mean response time 0.2 s, expected average concurrency is about 200. If observed concurrency is 600, boundaries/measurements differ, retries or queueing are counted differently, or the system is not steady.

Little's Law is an accounting relationship, not a latency prediction. Define arrivals/completions and the population boundary consistently; during a growing queue, short-window equality may not hold because the system is not stable.

Queueing intuition explains headroom. In the idealized M/M/1 model with $\mu=1,000$/s, at $\lambda=800$/s mean time is $1/(1000-800)=5$ ms, while at 950/s it is 20 ms—four times larger for 18.75% more arrival rate. Real service distributions, parallel servers, locks and networks differ, so measure the actual curve.

### Validate the generator and path

Capacity-test generators against a controlled fast target or loopback sink. Monitor generator CPU, memory, event-loop lag, sockets, ephemeral ports, DNS/TLS, network bandwidth/packet loss, connection pools, virtual-user allocation, GC and dropped iterations. Distribute generators when needed and synchronize clocks.

Use a real client/protocol stack and production-like connection reuse, HTTP version, compression, TLS/mTLS, DNS, gateway/mesh, headers/auth and serialization. If bypassing layers for component capacity, state that claim separately.

Avoid generating data or doing expensive checks on the timed hot path when production clients do not. Precompute payloads/credentials or measure generator overhead. Still validate response correctness with representative sampling and aggregate invariant checks.

The load generator should be able to exceed the intended SUT breakpoint with margin; otherwise “plateau” may be generator capacity.

### Establish phases and steady state

Run functional smoke first. Warm runtime/JIT, connections, caches, buffer pools and autoscaling according to the claim. A cold-start test intentionally begins cold; do not mix it with steady capacity.

Ramp in steps long enough for queues, caches, GC, autoscaling and dependency pools to respond. Mark warm-up/ramp/steady/overload/cooldown windows. Analyze steady windows separately and preserve transitions for scaling/recovery analysis.

Steady state means arrival/completion/queue/resource trends are bounded, not merely a fixed clock duration. A constant throughput with growing backlog is not sustainable. Require no adverse slope in queue, memory, file descriptors, goroutines/threads, retries, lag or latency.

Repeat runs and randomize comparison order where thermal/cache/noisy-neighbor effects matter. Allow cooldown/reset and verify starting state. One pass is a measurement, not a stable conclusion.

### Measure distributions and useful work

Measure client-observed total response time and, via traces/metrics, DNS/connect/TLS/proxy/queue/application/database/dependency/serialization phases. Keep the boundary and clock source explicit. Include timeouts/cancellations as outcomes rather than deleting their latency.

Use aggregatable histograms with SLO-aligned resolution/buckets. Prometheus guidance distinguishes histograms from client-computed summaries and explains why averaging per-instance quantiles is generally meaningless. Aggregate raw/bucket distributions before computing fleet quantiles.

Report median, SLO threshold fraction, p90/p95/p99/p99.9 when sample volume supports them, maximum with caution, and confidence/repetition. At 1,000 observations, p99 is informed by roughly ten tail observations; a precise-looking p99.99 is not credible.

Useful throughput counts correct completed logical work. Show offered/scheduled, admitted, correct, degraded, rejected, error, timeout, retry and effect rates. An overload test that quickly returns `503` can have excellent response latency but zero useful capacity.

Continue invariant checks: no duplicate effects, cross-tenant leakage, lost writes/events, stale/invalid responses beyond contract, ordering violation, corrupted payload or idempotency failure. Performance success cannot excuse correctness.

### Locate bottlenecks and saturation knees

Observe CPU utilization/throttling/run queue, memory/RSS/GC/allocations, network bandwidth/packet/retransmit, disk IOPS/latency/queue, connections/pools, threads/goroutines/event loop, locks, database queries/locks/buffer/cache, broker partitions/lag, dependency attempts/latency, queues/in-flight, retries/timeouts/ejection/shedding and autoscaler signals.

Aggregate and inspect per-instance/shard/partition/zone distributions. Fleet average 60% CPU can hide one hot shard at 100%. Correlate route/tenant/data key to imbalance without high-cardinality metrics.

The knee appears when incremental offered load yields falling marginal correct throughput, sharply rising queue/latency, errors/retries, resource thrash or imbalance. Step back to a region that passes SLO/guardrails with stable slopes; apply forecast/failure/measurement headroom. Breakpoint and safe capacity are different.

Identify the limiting resource and a causal mechanism. “CPU high” is incomplete: parser cost, GC, logging on errors, retry work, lock spin or serialization may be the driver. Change one factor and rerun.

### Test overload, degradation, and recovery

Drive beyond capacity in controlled isolation. Verify admission/load shedding occurs early/cheaply and preferentially according to policy; deadlines and queues remain bounded; retry advice does not amplify; critical traffic and correctness are preserved; degraded responses are explicit; instances do not enter restart cascades.

Google SRE describes nonlinear overload, GC/logging amplification and the need to test failure modes beyond capacity. Measure correct throughput during overload, not only offered load.

Test spike onset, sustained overload, reduction below capacity and full cooldown. Recovery criteria include backlog drain without renewed overload, latency/error/resource return, autoscaling scale-down safety, connection/discovery health, cache stability, breaker/ejection re-entry, no lost/duplicate effects, and restored redundancy.

Failure-headroom tests remove a replica/zone/dependency capacity during expected peak. Safe capacity must satisfy declared fault assumptions, not all-resources-perfect.

### Test scaling and topology

Scale vertically and horizontally at identical workload/data/config. Ideal capacity $C(n)=nC(1)$ rarely holds because shared database, coordination, load balance and serial work limit gain. Compute scaling efficiency $\eta(n)=C(n)/(nC(1))$ under the same SLO definition.

Measure detection, provisioning, readiness/warm-up, discovery/routing and stabilization lag. A service that scales in ten minutes cannot rely on autoscaling for a thirty-second spike. Include scale-from-minimum and already-warm headroom cases.

Test mixed versions during rolling deploy, uneven traffic, cold replicas, cache prefill, connection drain and zone/locality routing. New capacity that receives no traffic or overloads the database is not effective capacity.

### Run soak and state-growth tests

Run long enough to expose memory/descriptor/connection leaks, cache growth/eviction, log/trace volume, database bloat, compaction, token/key rotation, queue accumulation, periodic jobs, GC phase changes and thermal throttling. Use a duration tied to the slowest relevant cadence; state what cadences were not covered.

Track slopes and periodicity, not just end values. A 0.1% memory increase per minute looks small over five minutes and fails over a day. Ensure generated persistent data reaches steady retention or cleanup without hiding write amplification.

Soak at expected sustained load plus representative bursts, not necessarily breakpoint. Repeat recovery after the soak to find exhausted pools or slow cleanup.

### Compare changes scientifically

Hold workload seed/mix, topology, resources, dependencies, data/cache start, generator and thresholds constant. Promote the exact candidate artifact. Run baseline and candidate multiple times, alternating order where possible.

Compare distributions and correct throughput/resource per unit work, not only a single percentile. Report absolute and relative differences, run-to-run variance, sample counts and practical thresholds. A statistically detectable 1 ms change may be operationally irrelevant; a rare timeout can be critical.

If the candidate changes behavior/mix—compression, cache, payload—document a new experiment rather than calling it a pure code comparison. Preserve raw results and scripts under governed artifacts.

### Convert measurements into decisions

Define capacity per replica/cluster and bottleneck under each key mix/config; forecast organic/launch demand; add failure, deploy, seasonality, growth and uncertainty headroom; compare lead time to provision. Revalidate before expiry.

Set admission/rate/queue/concurrency limits below destructive knee, autoscaling signals early enough for lag, connection/database pool sizes, SLO thresholds, dashboards/alerts, dependency budgets, and cost per correct operation. Update runbooks with observed degradation/recovery.

Gate regressions using shorter representative tests with noise-aware thresholds; schedule full saturation/soak/failure tests periodically or for material changes. Never freeze architecture to an obsolete benchmark.

## Definitions and Notation

Let $\lambda$ be accepted/completed arrival rate at a stable boundary, $W$ mean time within it, and $N$ mean concurrent work. Let $\mu$ be service rate in a simplified queue, $\rho=\lambda/\mu$ utilization, $C(x)$ usable capacity for declared workload/configuration vector $x$, $C(n)$ capacity with n equivalent replicas, and $\eta(n)=C(n)/(nC(1))$ scaling efficiency.

Let offered $O$, scheduled $Q$, started $S$, admitted $A$, correct completed $G$, rejected $R$, failed $F$, timed out $T$, and retried attempts $Y$ be separate counts/rates. A **capacity claim** is valid only with an exact boundary, time window, workload vector, quality constraints and provenance.

## Mechanisms, Invariants, or Proof Structure

**Little's Law accounting.** Over a stable interval, total work-time accumulated equals average population times interval and also completed work times average residence time, yielding $N=\lambda W$. Mismatched boundaries or nonsteady queues invalidate naive comparison.

**Queueing-knee illustration.** In the stated M/M/1 model, increasing $\lambda$ from 800 to 950 with $\mu=1000$/s changes W from 5 ms to 20 ms. The model is not a service forecast; it proves nonlinear growth is possible near saturation and motivates headroom measurement.

**Coordinated-omission counterexample.** A closed generator waits during a 10-second stall and produces few/no scheduled observations inside the stall, while independent real arrivals would queue/time out. Therefore its observed latency distribution cannot represent a fixed open arrival process.

**Safe-capacity argument.** If load L meets throughput but violates correctness, SLO, resource stability or recovery, L is not usable capacity. Therefore maximum completed RPS and breakpoint are upper observations, not C.

## Alternatives and Trade-Offs

Open models preserve an external arrival schedule and reveal queueing but require generator concurrency and can overwhelm shared environments. Closed models represent bounded interactive/worker populations and are easier to control but self-throttle. Hybrid models add realism and complexity.

Production traffic replay preserves correlations but risks secrets/effects, stale distributions and opaque semantics. Synthetic generators are safe/reproducible but can miss correlations. Use privacy-safe statistical models plus selected synthetic edge cases and validate against production aggregates.

Shared staging supplies managed dependencies/topology but has noise/contention. Ephemeral environments isolate artifacts/config but may lack production scale/services. Component tests locate bottlenecks cheaply; full-path tests validate composition. Maintain a tiered portfolio.

Autoscaling during tests represents production behavior but makes fixed-resource capacity unclear. Run fixed-capacity baseline first, then scaling experiment with lag/readiness/topology measured.

## Failure Modes and Misconceptions

- “Maximum RPS is capacity” ignores correctness, latency, stability and recovery.
- “Users equal requests per second” confuses closed concurrency and open arrival.
- “The generator sent it” may mean scheduled work was dropped before send.
- “p99 is 100 ms” lacks boundary, window, population, sample size and failures.
- “Average p99 across pods” does not yield fleet p99.
- “Successful latency is fast” can omit slow timeouts and errors.
- “CPU is 50%, so headroom is 50%” ignores shards, locks and dependencies.
- “Warm-cache result is capacity” is only a warm-cache envelope.
- “Autoscaling solved the spike” ignores detection/provision/warm/routing lag.
- “A five-minute plateau is sustainable” misses slow state/resource growth.
- “More retries improve throughput” may multiply attempts and reduce useful work.
- “Breakpoint proves overload safety” omits degradation and recovery.
- “Same script means comparable” ignores artifacts, data, topology and environment.
- “Load tests prove production” ignores unknown traffic, failures and scale differences.

## Worked Examples

### Example 1

At 1,000 completed/s and mean 200 ms, Little's Law predicts about 200 in-flight operations. Telemetry shows 600 because it counts three attempts per logical operation. **Conclusion:** align boundary and attempt semantics.

### Example 2

Closed 100-user workload slows from 10 to 2 iterations/s during stalls, reducing offered load. Open 1,000/s schedule exposes queue/timeouts. **Conclusion:** choose the model matching production feedback.

### Example 3

At $\mu=1000$/s, M/M/1 illustration moves from 5 ms at 800/s to 20 ms at 950/s. **Conclusion:** small load increases near saturation can multiply latency.

### Example 4

Run reports p99 250 ms for 900 successes but omits 100 ten-second timeouts. Correct outcome table shows 10% failure and user tail at deadline. **Conclusion:** never condition latency silently on success.

### Example 5

Fleet CPU averages 55%, but one tenant's shard is CPU 100% with long lock queue. Per-shard telemetry finds knee. **Conclusion:** averages hide imbalance.

### Example 6

One replica capacity is 200/s; four replicas sustain 620/s under SLO. $\eta(4)=620/(4\cdot200)=0.775$. Database pool is shared bottleneck. **Conclusion:** horizontal scaling is not automatically linear.

### Example 7

Autoscaler adds pods in 90 seconds, but synchronized retry spike peaks in 20 seconds. Warm headroom/load shedding is required. **Conclusion:** capacity control must respect actuation lag.

### Example 8

Soak memory grows 60 MiB/hour and never returns after cooldown. Short ramp passed. Heap/corpus diagnosis finds unbounded idempotency cache. **Conclusion:** duration must cover slow accumulation.

### Example 9

At overload, API returns cheap `429/503`, preserves 99% priority traffic and recovers in four minutes with no duplicate effects. **Conclusion:** overload quality and recovery are capacity properties.

### Example 10

Candidate is 4% faster in one run but baseline/candidate repetition varies ±6%. More controlled alternating runs show no meaningful change. **Conclusion:** report variance and controlled provenance.

## Cross-Program Connections

[Probability, testing, and experimental methods](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supply distributions, sampling, reproducibility, comparison and test validity.

[Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) supplies SLOs, capacity planning, progressive delivery, overload, recovery and regression gates.

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies query/index cost, pools, locks, transactions, caches, replication, compaction and data skew.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies queueing, partial failure, retries, backpressure, load balance, consistency, time and recovery.

[Cloud & Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) supplies compute/network/storage limits, autoscaling, topology, cost, failure domains and capacity provisioning.

## References

1. Grafana Labs, [k6 Open and Closed Workload Models](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/).
2. Grafana Labs, [k6 Ramping Arrival Rate](https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/ramping-arrival-rate/).
3. Grafana Labs, [k6 Performance Thresholds](https://grafana.com/docs/k6/latest/examples/get-started-with-k6/test-for-performance/).
4. Prometheus, [Histograms and Summaries](https://prometheus.io/docs/practices/histograms/).
5. Google, [Site Reliability Engineering: Production Services Best Practices](https://sre.google/sre-book/service-best-practices/).
6. Google, [Site Reliability Engineering: Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/).
7. Google, [Site Reliability Engineering: Reliable Product Launches at Scale](https://sre.google/sre-book/reliable-product-launches/).

## Exercises

### Exercise 1

Write a falsifiable capacity claim and workload manifest for a multi-tenant order API with reads, writes, search, payment calls, event publication, cache and autoscaling.

### Exercise 2

A stable test completes 2,400 logical operations/s with mean response time 125 ms. Compute expected concurrency. Observed service attempts in flight average 900; diagnose plausible accounting or system causes.

### Exercise 3

Design experiments to distinguish generator bottleneck, coordinated omission, database-pool saturation, hot shard, retry amplification and autoscaling lag.

### Exercise 4

One replica sustains 180/s, two sustain 330/s, four sustain 540/s and eight sustain 680/s under the same SLO. Compute scaling efficiency and propose next measurements/decisions.

### Exercise 5

A test passes 1,500/s for ten minutes, fails at 1,700/s, recovers throughput after load drops, but memory, queue lag and error logs remain elevated. Decide usable capacity and remediation evidence.

## Answers to the Exercises

### Answer 1

Example claim: exact artifact/config on six named-resource replicas plus database/broker/cache revisions sustains 900 logical arrivals/s for 60 steady minutes and a 1,350/s 60-second spike, using measured 45% reads, 25% creates, 15% search, 10% status/poll and 5% cancel; production payload/tenant/data skew, 35% cache hit, TLS/auth/gateway/mesh, fixed client retry/deadline and synthetic payment/event effects. Require ≥99.9% correct accepted outcomes, p99 ≤350 ms for priority create/read, stable queues/memory, bounded dependency pools, planned rejections, one effect per operation, scaling before configured limit and recovery ≤5 minutes. Manifest pins all digests/resources/topology/seed/generator and reports scheduled/started/admitted/correct/rejected/timeout/retry/effect. Separate fixed-six baseline from autoscaling experiment; include cold/warm cache and one-replica-loss envelope.

### Answer 2

$N=\lambda W=2400\times0.125=300$ average logical operations in the stated boundary. Nine hundred in-flight service attempts could be three concurrent attempts/hops per logical operation, retry/fan-out multiplication, inclusion of queued work outside the response-time boundary, or mismatched windows. It could also indicate nonsteady backlog: arrivals exceed completions so Little's Law over the short interval is inapplicable. Reconcile logical IDs to attempts, client/gateway/service/dependency boundaries, accepted versus completed rate, queue population and window. Verify clocks and whether W excludes queue/network. Do not infer a defect until definitions align; if aligned and stable, the measurements are inconsistent.

### Answer 3

Generator: test against fast sink and monitor its CPU/event loop/network/ports/connections/dropped starts; distribute it and show higher offered load. Coordinated omission: compare fixed closed users with independent open arrival schedule and account for scheduled/dropped/timeouts. Database pool: hold route/data mix, vary pool and observe wait/active/query latency/DB resources; excessive pool can worsen contention. Hot shard: inspect per-shard key/tenant distribution and rerun balanced versus skewed keys. Retry amplification: disable/limit one layer under same fault, count logical/attempt/effect and compare dependency load. Autoscaling: fixed-capacity baseline, then measure detection→provision→ready→discovery→traffic and queue/latency during ramp/spike. Change one factor per experiment and retain exact environment/data start.

### Answer 4

$\eta(2)=330/(2\cdot180)=0.917$; $\eta(4)=540/720=0.75$; $\eta(8)=680/1440=0.472$. Marginal capacity falls sharply: +150, +210, then +140 despite doubling resources. Locate shared bottleneck via database/lock/pool, broker partitions, load imbalance, coordination, network and downstream telemetry; verify generator margin. Measure per-instance/shard utilization and fixed mix/cache. Test vertical resources and dependency scaling independently. Do not provision eight replicas expecting linearity; set safe capacity below knee with failure headroom and decide whether optimizing/shared-dependency scaling or fewer better-utilized replicas improves cost and resilience.

### Answer 5

Do not call 1,500/s sustainable: residual memory/lag/error state violates stability/recovery even if immediate throughput returns. Current usable capacity is the highest lower rate repeatedly satisfying latency/correctness/resource slopes and full recovery for a duration covering the accumulation cadence; evidence may not yet establish one. Freeze exact artifacts/config, inspect memory slope/leak/cache retention, queue production-versus-consumption and retry/log amplification, then wait through bounded cooldown/backlog drain. Require memory and lag return to baseline/defined steady envelope, error amplification stop, no lost/duplicate effects and repeatable recovery after overload. Run longer soak at candidate safe rate and fault-headroom scenario. Set temporary admission below demonstrated stable point with monitoring/runbook; remediate root cause and remeasure rather than merely increasing limits.
