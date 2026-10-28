---
module_id: SARCH-012
program: Software Engineering: Software Architecture
level: 1
module_number: 12
title: Performance and Latency Tactics
status: complete
last_verified: 2026-09-05
---

# Performance and Latency Tactics

## One-Page Review

### Governing question

How should architecture bound the time and resource cost of useful work under a declared workload without sacrificing correctness, availability, fairness, or operational control?

### Essential definitions

- **latency** is elapsed time from a declared start event to a declared completion event.
- **response time** includes all work and waiting visible between a request and its defined response; it is one kind of latency.
- **service time** is time a resource actively spends on an item, excluding time waiting for that resource.
- **queueing time** is time waiting before service begins.
- **throughput** is completed useful work per unit time under defined correctness and workload conditions.
- **utilization** is the fraction of a resource's available service capacity occupied during a window.
- A **percentile** is a distribution quantile: the p99 latency is a value at or below which at least 99% of observed eligible latencies fall under a stated convention.
- **tail latency** is behavior in the high-latency region of a distribution, often represented by high percentiles rather than the mean.
- **backpressure** is feedback that limits or delays offered work when downstream capacity is constrained.
- A **performance budget** allocates an end-to-end objective among communication, queueing, computation, storage, coordination, and margin.

### Central model, mechanism, or theorem

For one request path, reason from an explicit latency decomposition:

$$
T=T_{edge}+\sum_i(T_{queue,i}+T_{service,i}+T_{network,i})+T_{coordination}+T_{margin}.
$$

The terms are random variables, not fixed constants. Architecture controls them by reducing demand, reducing performed work, managing resource use, controlling concurrency and queues, exploiting safe locality and parallelism, scheduling by consequence, and measuring end-to-end distributions under representative workloads. [Little's Law](https://doi.org/10.1287/opre.9.3.383), $N=\lambda W$, connects average in-system work $N$, completion rate $\lambda$, and average time in system $W$ for a stable observed system.

### Critical invariants

- define start, completion, eligible population, correctness, window, and observation point;
- retain the latency distribution and workload segmentation rather than only an average;
- separate service time from queueing, network, admission, retry, and coordination;
- preserve correctness, authorization, freshness, durability, and side-effect identity;
- bound queues, concurrency, fan-out, retries, and work amplification;
- make cache validity and invalidation semantics explicit;
- distinguish throughput from arrival rate and useful completion from attempted work;
- state stationarity, stability, independence, and workload assumptions used by models;
- measure warm-up, overload, failure, recovery, and maintenance conditions;
- bound conclusions to the tested topology, software, data, workload, and environment.

### Common failures

Common failures include optimizing the mean while the tail violates the objective; measuring inside the server instead of at the user boundary; reporting throughput while errors or stale answers rise; using unbounded queues to hide overload; adding retries that amplify work; treating p99 values as additive constants; parallelizing onto a saturated shared resource; caching without validity rules; batching without latency bounds; confusing low test utilization with production headroom; omitting coordinated omission in load generation; and changing timeouts without analyzing availability and duplicate effects.

### Compact example

A search request fans out to 100 independent shards. If each shard is slow with probability 1%, the chance that at least one shard is slow is $1-0.99^{100}\approx63.4\%$. The per-shard p99 therefore cannot stand in for end-to-end p99. The architecture may reduce fan-out, partition by relevance, use bounded hedging for safe reads, return an explicitly partial result, or improve slow shards. Each option changes cost, completeness, load, and failure behavior.

### Connections

[SARCH-004](004-quality-attributes-as-architectural-drivers.md) supplies measurable scenarios; [SARCH-007](007-trade-offs-and-competing-objectives.md) supplies competing-objective reasoning; [SARCH-011](011-availability-and-recovery-tactics.md) supplies timeout, retry, overload, and degraded-service interactions. [SARCH-013](../ROADMAP.md) develops growth and capacity tactics; this module owns response-time mechanisms under a declared workload rather than long-horizon capacity planning.

## Governing Question

A system can be fast in a developer benchmark and slow for users. It can complete many requests per second while starving a tenant, returning stale data, or dropping work. It can have efficient components whose queues, fan-out, coordination, and retries produce an unacceptable end-to-end tail. What architecture decisions make a performance claim meaningful and controllable?

The governing question is how to translate a stakeholder timing scenario into a workload model, path model, resource model, tactics, and bounded evidence. “Fast” is not an architectural property until operation, load, state, percentile, time boundary, environment, and required outcome are explicit.

## Why This Matters

Latency changes behavior. A late fraud decision can be useless, a delayed control signal can be unsafe, and a slow checkout can cause duplicate submission. Timeouts turn latency into apparent failure. Retries and failover turn apparent failure into more load. Performance therefore interacts with availability, consistency, security, cost, energy, and human operation.

Queueing makes systems nonlinear near saturation. A small increase in offered load or service-time variance can create a large increase in waiting time. Unbounded admission can make every request slow instead of rejecting or deferring a controlled subset. Architectural control must begin before the system exhausts a resource.

Optimization also moves costs. Caching reduces remote work but introduces freshness and invalidation. Batching amortizes overhead but makes early items wait. Parallelism shortens independent work but consumes more resources and exposes the request to more tail events. The right tactic depends on the scenario and its invariants.

## Prerequisites and Retrieval

Retrieve quality-attribute scenario, stakeholder outcome, workload, arrival rate, service time, queue, resource, throughput, utilization, average, median, percentile, variance, concurrency, parallelism, batching, cache, locality, backpressure, timeout, retry, idempotency, overload, and evidence limitation.

From earlier modules, retrieve end-to-end system boundaries, ASRs, explicit assumptions, trade-off sensitivity, candidate evaluation, and recovery semantics. You should be able to distinguish a target from a measurement and a model prediction from observed behavior.

## Learning Objectives

After completing this module, you should be able to:

1. define latency and throughput scenarios from stakeholder-visible work;
2. decompose end-to-end time into service, waiting, communication, and coordination;
3. interpret averages, percentiles, histograms, and segmented distributions;
4. use Little's Law and simple queue models under stated assumptions;
5. explain why utilization and variability affect tail latency;
6. allocate and review end-to-end latency budgets;
7. select demand-, resource-, queue-, locality-, scheduling-, and concurrency-control tactics;
8. analyze batching, caching, parallelism, hedging, and load shedding trade-offs;
9. design representative and non-misleading performance evidence;
10. identify when latency optimization violates correctness, fairness, or safety.

## Core Exposition

**Frame the timing scenario.** Define stimulus, source, operation, data size, state, arrival pattern, concurrency, completion semantics, response measure, and environment. “Page loads in 200 ms” is incomplete: first byte or useful render, cold or warm, which network, which device, which percentile, which cohort, and whether data is correct?

Measure from the boundary that owns the stakeholder claim. Internal handler time omits client scheduling, name resolution, connection establishment, queues, proxies, serialization, networks, dependencies, and rendering. Record both end-to-end and component spans so a decomposition can be tested without redefining success.

**Treat latency as a distribution.** A mean hides dispersion and rare stalls. Percentiles summarize order, not cause. Segment by operation, payload, tenant, region, cache state, release, and load where aggregation would hide different populations. Publish sample count, interval, eligibility, clock method, dropped observations, and percentile convention.

Percentiles do not generally add. The slowest 1% of one component need not coincide with the slowest 1% of another, and dependencies may be correlated. Summing component p99 values is a conservative bound in some specially reasoned cases, an underestimate in others, and never automatically the end-to-end p99. Use request-correlated traces and end-to-end measurements.

**Decompose work and waiting.** Service time is active demand at a resource. Response time includes waits. Break the critical path into admission, queues, computation, storage, network, coordination, serialization, client, and margin. Decomposition exposes whether to remove work, move work, overlap independent work, improve locality, change scheduling, or control demand.

Not all path terms are serial. If independent branches run concurrently, the join waits roughly for their maximum, plus coordination—not their sum. This can reduce median latency while worsening resource consumption and tail exposure. A dependency graph and critical-path trace are more faithful than a flat list.

**Connect flow with Little's Law.** For a stable observed system over a suitable interval, average in-system work $N$, average throughput $\lambda$, and average time $W$ satisfy $N=\lambda W$, as established in [Little's original proof](https://doi.org/10.1287/opre.9.3.383). The relation is an accounting law, but measurements must describe the same population and boundary. It does not predict percentile latency, identify bottlenecks, or guarantee stability.

**Reason about utilization and queues.** Let $S$ be service time at one resource and $\lambda$ the arrival rate. A simplified single-server utilization is $\rho=\lambda E[S]$. Sustained $\rho\ge1$ means offered work equals or exceeds service capacity under the model, so backlog cannot drain without admission control or changed capacity. Even below one, bursts and variable service times create waits.

Under the restrictive M/M/1 assumptions—Poisson arrivals, independent exponential service, one server, stable $\rho<1$, infinite queue, and first-come service—mean response time is $W=1/(\mu-\lambda)$. This formula illustrates nonlinear delay near saturation; it is not a universal service model. Real workloads often have burstiness, priorities, finite queues, correlated requests, multiple servers, and heavy-tailed service.

**Control demand before exhaustion.** Admission control rejects, defers, or degrades work according to explicit policy. Concurrency limits cap active work. Bounded queues cap waiting and memory. Backpressure propagates capacity information upstream. Load shedding preserves selected high-value work. These mechanisms need fairness, retry, user-message, priority, and recovery semantics.

A queue is not capacity. It absorbs bounded mismatch between arrival and service rates. An unbounded queue converts overload into rising latency, memory pressure, stale work, and slow recovery. Define maximum queue length or wait, expiration, cancellation, priority, tenant isolation, and observable rejection.

**Reduce performed work.** Avoid redundant computation and data movement. Precompute stable results. Choose representations and algorithms that fit the access pattern. Eliminate unnecessary synchronous dependencies. Compress only when saved transfer time exceeds CPU, energy, and latency costs. Performance architecture should remove work before purchasing faster execution.

**Exploit locality through caches.** A cache can avoid network and service work, but requires key, scope, authorization, validity, freshness, invalidation, eviction, stampede, failure, and observability semantics. Compute a hit ratio by eligible lookup population, not by requests chosen after misses are discarded. A cache hit that serves incorrect or unauthorized data is not successful performance.

Use request coalescing, randomized expiration, refresh-ahead, or bounded stale service where appropriate. Each tactic changes dependency load and failure behavior. A cold-cache or mass-expiry event belongs in the workload model.

**Batch with a waiting bound.** Batching amortizes fixed setup, network, storage, or coordination cost. It also delays early items and can create bursty downstream demand. Trigger by size, time, or both; cap bytes and item age; preserve ordering and failure semantics; and expose partial success. Under uniform arrivals and a fixed time-only batch interval $B$, an item's additional batching wait averages $B/2$, but real arrivals and early triggers change the result.

**Use parallelism deliberately.** Parallel execution helps when work is independent and resources are not already saturated. Amdahl's Law gives a simplified upper bound: if fraction $p$ is parallelizable across $k$ ideal workers, speedup is

$$
Speedup=\frac{1}{(1-p)+p/k}.
$$

Coordination, imbalance, contention, data transfer, scheduling, and tail amplification reduce realized benefit. Fan-out multiplies downstream work and the chance that one slow branch delays a join, a phenomenon analyzed by Dean and Barroso in [“The Tail at Scale”](https://research.google/pubs/the-tail-at-scale/). Bound width and define partial-result semantics.

**Schedule according to consequence.** First-come service is simple but may let large work block small urgent work. Priorities can protect critical operations but starve others. Fair scheduling can isolate tenants and classes but adds state and policy. Deadlines can discard work too late to matter, but require trustworthy clocks and end-to-end budget propagation.

Make priority part of the contract: source authority, maximum share, aging, preemption, cancellation, and observability. Security or payment work must not be bypassed as a “fast path.”

**Hedge only safe work.** A hedged request starts a duplicate after a delay and accepts the first valid result. It can reduce tail latency for idempotent reads when slow instances are not caused by shared saturation. It increases load and can worsen overload. Side effects require stronger identity and cancellation semantics; many writes should not be hedged at all.

**Budget and propagate time.** Allocate an end-to-end objective across client, edge, services, storage, communication, and margin. Pass a remaining deadline rather than independently granting every hop the full timeout. A component should avoid starting work that cannot finish usefully, while accounting for cleanup and uncertainty. Timeout design must be coordinated with retries and recovery, consistent with the failure interactions in Google's [SRE book](https://sre.google/sre-book/table-of-contents/) and [SRE workbook](https://sre.google/workbook/table-of-contents/).

**Test without measurement traps.** Use representative operations, payloads, data distributions, cache states, arrival processes, concurrency, geography, dependencies, security controls, and failure modes. Separate warm-up. Measure client-observed correctness, latency distribution, useful throughput, resource saturation, queues, errors, retries, drops, and recovery.

Open-loop generators should preserve intended arrivals when the system slows; closed-loop generators model clients that wait before issuing more. A closed-loop test can understate overload because slow responses suppress offered load, a form of coordinated omission. Record generator semantics and clocks. Reproduce runs, change one variable when possible, and retain raw histograms or traces rather than screenshots.

## Definitions and Notation

For eligible completed operation $j$, define latency $T_j=t_{complete,j}-t_{start,j}\ge0$ using declared events and a clock suitable for elapsed time. For observations $T_{(1)}\le\cdots\le T_{(n)}$, one explicit nearest-rank percentile convention is

$$
Q_p=T_{(\lceil pn\rceil)},\qquad 0<p\le1.
$$

Other tools interpolate differently, so record the convention. Define useful throughput over interval $\Delta t>0$ as

$$
X=\frac{C}{\Delta t},
$$

where $C$ counts correctly completed eligible operations, not attempts or errors. Let $\lambda$ denote an average rate for the same population and boundary, $W$ average time in system, $N$ average number in system, $S$ service time, $\mu=1/E[S]$ a simplified service rate, and $\rho=\lambda E[S]$ single-resource utilization.

Models using averages do not imply percentile results. Queue formulas require their stated arrival, service, scheduling, capacity, and stability assumptions. Performance objectives remain scenario predicates over operation, workload, state, environment, and distribution—for example, $Q_{0.99}(T)\le200$ ms while correctness and rejection bounds hold.

## Mechanisms, Invariants, or Proof Structure

Use this performance-analysis mechanism.

1. **Define outcome:** specify useful completion, time boundary, population, workload, state, environment, and objective.
2. **Trace the path:** map serial and parallel work, queues, networks, coordination, and resource demands.
3. **Measure distributions:** retain end-to-end histograms, segment populations, and correlate component traces.
4. **Model flow:** apply latency decomposition, Little's Law, utilization, and queue approximations only under stated assumptions.
5. **Find constraints:** identify saturated, serialized, variable, contended, remote, or amplified work.
6. **Select tactics:** remove work, improve locality, bound queues and concurrency, schedule, batch, parallelize, or degrade deliberately.
7. **Protect invariants:** preserve correctness, authorization, freshness, durability, fairness, and side-effect identity.
8. **Verify:** test steady, burst, cold, tail, overload, failure, recovery, and change conditions from the claim boundary.
9. **Observe:** record useful throughput, distributions, saturation, queues, amplification, rejection, and resource cost.
10. **Reassess:** reopen budgets, assumptions, and tactics when workload, topology, implementation, or consequence changes.

The governing invariants are end-to-end outcome timing, declared populations, bounded demand, correct completion, visible distributions, stable flow, controlled amplification, valid locality, fair admission, representative evidence, and explicit limitations.

## Alternatives and Trade-Offs

**Precompute or compute on demand.** Precomputation lowers response latency but adds storage, invalidation, update delay, and unused work. On-demand computation preserves freshness and avoids unused results but spends request-path time and capacity.

**Cache or fetch authoritatively.** Caching improves locality and shields dependencies, but freshness, authorization, eviction, and invalidation become architectural concerns. Direct reads simplify authority but add remote work and dependency latency.

**Batch or stream.** Batching amortizes overhead and improves throughput; streaming reduces item waiting and memory but performs more per-item coordination. Hybrid size-or-time triggers bound both overhead and age.

**Parallelize or serialize.** Parallelism can shorten the critical path but increases resource demand, coordination, and tail exposure. Serialization conserves resources and simplifies ordering but lengthens independent work.

**Queue or reject.** A bounded queue absorbs short bursts but spends latency budget. Early rejection preserves capacity and honest feedback but requires client and product semantics. Unbounded waiting is not a safe compromise.

**Hedge or wait.** Hedging can reduce independent straggler impact but adds load and duplicate work. Waiting avoids amplification but exposes the tail. Hedge only with safe semantics, delay, budget, cancellation, and overload disablement.

## Failure Modes and Misconceptions

- **“Average latency is good.”** The tail, important cohorts, or critical windows may still fail.
- **“Component p99s add to end-to-end p99.”** Percentile composition depends on joint behavior and path structure.
- **“High throughput means good performance.”** Errors, stale results, unfairness, or long queues may inflate the number.
- **“A queue absorbs load.”** It stores delay and work; sustained overload still requires control.
- **“CPU is only 50%, so capacity is safe.”** One core, lock, disk, network, allocator, dependency, or queue may constrain the path.
- **“Caching is transparent.”** Keys, identity, freshness, invalidation, and failure change semantics.
- **“Parallel is always faster.”** Serial fractions, contention, coordination, and tail amplification bound gains.
- **“Retry is a latency optimization.”** It consumes time and load and can duplicate effects.
- **“A benchmark is the architecture.”** Evidence is bounded to its code, data, workload, topology, and environment.
- **“Timeouts can be set independently.”** Nested full budgets create useless work and retry amplification.
- **“More samples remove bias.”** A biased population or generator remains biased at scale.
- **“Fast failure is always acceptable.”** Rejection and degradation require stakeholder and safety semantics.

## Worked Examples

### Example 1

**Question:** A user objective is 120 ms. Edge and client work consume 20 ms, two serial services are budgeted 30 ms and 35 ms, and storage is budgeted 15 ms. How much margin remains?

**Reasoning:** The allocations total $20+30+35+15=100$ ms. Margin is $120-100=20$ ms. This is a planning budget, not a percentile proof; correlations, retries, queues, and measurement boundaries still require end-to-end evidence.

**Conclusion:** A latency budget makes ownership and missing margin visible without pretending deterministic composition.

### Example 2

**Question:** Under nearest-rank convention, what are p50 and p90 for latencies 8, 10, 11, 13, 20, 21, 23, 40, 70, and 200 ms?

**Reasoning:** The values are sorted and $n=10$. Rank for p50 is $\lceil0.5(10)\rceil=5$, so p50 is 20 ms. Rank for p90 is 9, so p90 is 70 ms. The 200 ms maximum barely changes the median but matters to the tail.

**Conclusion:** State the percentile convention and retain the distribution; a median alone hides rare delay.

### Example 3

**Question:** A stable observed service completes 240 requests/s and requests spend 75 ms on average inside its boundary. What average concurrency follows from Little's Law?

**Reasoning:** Convert 75 ms to 0.075 s. $N=\lambda W=240\times0.075=18$ requests. This checks population-consistent averages; it does not predict p99 or say where the 18 requests wait.

**Conclusion:** Little's Law connects flow, residence time, and average in-system work without diagnosing the bottleneck.

### Example 4

**Question:** A simplified M/M/1 resource serves one request in 5 ms on average and receives 180 requests/s. What are utilization and modeled mean response time?

**Reasoning:** $\mu=1/0.005=200$/s and $\rho=180/200=0.9$. Under all M/M/1 assumptions, $W=1/(200-180)=0.05$ s, or 50 ms—ten times mean service time. At 100 requests/s the same model gives 10 ms, showing nonlinear queueing near saturation.

**Conclusion:** High utilization can spend far more time waiting than serving, but the formula is only a bounded model.

### Example 5

**Question:** A request waits for 100 independent shards, each slow with probability 1%. How often is at least one shard slow?

**Reasoning:** The probability none is slow is $0.99^{100}\approx0.3660$. Therefore at least one is slow with probability $1-0.99^{100}\approx0.6340$, or 63.4%. Shared causes would invalidate independence and can make behavior better or worse than this calculation.

**Conclusion:** Wide fan-out amplifies tail exposure even when each component's tail looks rare, as described in [“The Tail at Scale”](https://research.google/pubs/the-tail-at-scale/).

### Example 6

**Question:** A time-triggered batch closes every 40 ms and arrivals are uniform. What extra wait does batching add on average and at worst?

**Reasoning:** Under the stated idealization, arrival position is uniform in the interval. Average added wait is $40/2=20$ ms; the supremum approaches 40 ms for an item just after a batch closes. Size triggers, bursts, processing, and downstream queues alter these values.

**Conclusion:** Batching exchanges bounded item latency for amortized work and often higher throughput.

### Example 7

**Question:** A profile cache reaches 95% hits, but cache keys omit tenant identity. Is it a successful performance tactic?

**Reasoning:** No. It can serve another tenant's data quickly, violating authorization and correctness. Include every value-affecting and access-affecting dimension, define freshness and invalidation, and test eviction, cold start, stampede, and dependency failure. Count only correct authorized hits.

**Conclusion:** Locality is useful only while semantic and security invariants hold.

### Example 8

**Question:** A worker pool handles 100 items/s, receives a burst of 400 items/s for ten seconds, and has an unbounded queue. What happens?

**Reasoning:** Ignoring initial backlog and variance, arrivals add 4,000 items while service removes 1,000, leaving 3,000. After the burst, even with zero new arrivals, draining needs 30 seconds. With continuing normal traffic it takes longer. Bound admission, queue age, concurrency, priority, and retry behavior; decide which work to defer or reject.

**Conclusion:** A queue moves overload into future latency and recovery time; it does not create capacity.

### Example 9

**Question:** Should a second request be hedged after 80 ms when a read has a 100 ms objective?

**Reasoning:** Only if the read is safe to duplicate, the remaining budget can use a second result, stragglers are sufficiently independent, cancellation works, and added load will not worsen saturation. Disable or tighten hedging under overload, cap duplicates, and observe amplification. Do not copy this tactic to side-effecting writes.

**Conclusion:** Hedging is a conditional tail tactic with correctness and capacity costs, not free redundancy.

### Example 10

**Question:** How should an architecture address latency for an emergency dispatch decision?

**Reasoning:** Define the start event, safe completion, deadlines by incident class, stale-data rules, operator workflow, geographic and failure conditions, fairness, and safe degradation. Trace identity, location, communications, decision, and acknowledgment. Use bounded admission and priority with anti-starvation rules; test tail, overload, network loss, recovery, and manual operation. No external emergency-services, safety, regulatory, accessibility, security, human-factors, or practitioner review is claimed; named qualified authorities must validate objectives, hazards, procedures, evidence, release, and residual risk.

**Conclusion:** High-consequence latency is timely correct action under declared conditions, not the fastest isolated function.

## Cross-Program Connections

- [Algorithms Engineering](../../16-algorithm-engineering/ROADMAP.md) owns algorithmic cost, data-dependent behavior, and optimization foundations.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) owns scheduling, virtual memory, I/O, clocks, and resource contention mechanisms.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns pipelines, caches, memory hierarchy, and hardware performance.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) owns transport, congestion, delay, loss, and routing mechanisms.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns coordination, partial failure, replication, and distributed tail behavior.
- [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) operates SLOs, load control, monitoring, incidents, and performance change.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects timing to hazards, physical processes, operators, and lifecycle evidence.

## References

1. Betsy Beyer et al., editors. [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/), O'Reilly, 2016. Service-level objectives, monitoring, cascading failure, overload, and distributed-system performance; consulted 2026-09-05.
2. Betsy Beyer et al., editors. [The Site Reliability Workbook](https://sre.google/workbook/table-of-contents/), O'Reilly, 2018. Implementing SLOs, load balancing, overload protection, and operational evidence; consulted 2026-09-05.
3. John D. C. Little. “A Proof for the Queuing Formula: L = λW.” *Operations Research* 9(3), 1961, pp. 383–387. Original proof of the average-number, arrival-rate, and average-time relation under stated conditions.
4. Jeffrey Dean and Luiz André Barroso. [“The Tail at Scale.”](https://research.google/pubs/the-tail-at-scale/) *Communications of the ACM* 56(2), 2013, pp. 74–80. Tail amplification and latency-tolerance techniques for large online services; consulted 2026-09-05.
5. Raj Jain. *The Art of Computer Systems Performance Analysis*. Wiley, 1991. Performance metrics, measurement, experimental design, simulation, and queueing foundations.
6. Mor Harchol-Balter. *Performance Modeling and Design of Computer Systems: Queueing Theory in Action*. Cambridge University Press, 2013. Workload models, scheduling, queueing, and performance design.
7. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*, fourth edition, Addison-Wesley, 2021. Performance scenarios, resource-demand, resource-management, and resource-arbitration tactics.
8. Gil Tene. [“How NOT to Measure Latency.”](https://www.infoq.com/presentations/latency-pitfalls/), QCon San Francisco 2015. Coordinated omission, latency distributions, and measurement pitfalls; consulted 2026-09-05.

## Exercises

### Exercise 1

Define a complete latency objective for product search. Include outcome, boundary, population, workload, percentile, state, and correctness.

### Exercise 2

A stable boundary completes 500 operations/s with average residence time 40 ms. Apply Little's Law, then explain what the result cannot establish.

### Exercise 3

Diagnose a service with 40% average CPU, p50 60 ms, p99 4 s, an unbounded queue, five nested full-timeout retries, 98% cache hits, and a closed-loop load test.

### Exercise 4

Compare batching, caching, parallelism, and admission control for an image-transformation service. Address latency, throughput, correctness, resource cost, overload, and evidence.

### Exercise 5

Design performance assurance for an unfamiliar automated railway-crossing warning network. Separate architectural controls, automated evidence, operational exercises, qualified authority, and blockers.

## Answers to the Exercises

### Answer 1

For syntactically valid, authorized search operations from interactive users in declared regions, measure elapsed time at the client from submission of a normalized query to presentation of the first correct usable result set. During normal and seasonal-peak workloads defined by arrival distribution, concurrency, catalog size, query mix, payload, device, and network classes, require at least 99% to complete within the stakeholder-approved bound and at least 99.9% within a second bound. Define the numeric bounds with product owners from consequence and evidence rather than inventing them.

Success requires authorization, query semantics, freshness, completeness or explicitly allowed partiality, and correct error behavior. Segment region, device, cache state, query class, release, and peak window; publish exclusions, sample counts, dropped observations, clock method, percentile convention, dependency failures, and rejection rate. Also bound incorrect, unavailable, stale, and shed outcomes so latency cannot be improved by returning bad or empty results.

### Answer 2

Use consistent units: $W=40$ ms $=0.04$ s. Then

$$
N=\lambda W=500\times0.04=20.
$$

The observed boundary contains 20 operations on average. This does not locate them among service and queues, predict p50 or p99, show per-resource utilization, establish independence or stationarity, prove the system can accept more load, or validate correctness and fairness. Arrival and completion populations and the measurement window must match; instability or hidden dropped work makes the interpretation misleading.

### Answer 3

Average CPU can hide one saturated core, lock, disk, network, allocator, dependency, tenant, or short peak. The p50/p99 gap requires distribution and request-correlated traces segmented by operation, payload, cache state, cohort, release, and load. The unbounded queue can convert bursts into seconds of waiting. Five layers granting full timeouts multiply attempts and retain useless work after upstream deadlines. A 98% cache-hit aggregate can hide expensive misses, invalid hits, stampedes, or critical cohorts. Closed-loop clients reduce offered load as latency grows and can hide overload.

Define end-to-end correct outcomes and deadlines; inspect queue age, active concurrency, saturation, dependency time, retry amplification, hit validity, and cold behavior. Propagate remaining deadlines, coordinate retry budgets, bound queues and concurrency, shed or degrade by approved policy, and test open-loop bursts plus realistic closed-loop users. Preserve raw distributions and verify recovery after overload. Do not optimize the mean until the tail cause and correctness constraints are known.

### Answer 4

Batching amortizes decode, setup, transfer, and accelerator invocation but adds item wait and creates bursts; use size-or-time triggers and bound age and bytes. Caching can avoid transformation for content-addressed, authorization-safe, versioned requests but needs key completeness, invalidation, eviction, storage, and stampede control. Parallelism can use independent cores or accelerators but may contend for memory and I/O and amplify fan-out. Admission control bounds active work and queues, preserves selected traffic, and exposes overload honestly, but needs tenant fairness, priority, client retry, and rejection semantics.

Evaluate representative image sizes, formats, transformations, tenants, cache states, arrival patterns, concurrency, hardware, dependency behavior, and failure. Measure correct useful completions, end-to-end distributions, queue age, batch wait, cache validity, resource saturation, amplification, rejection, cost, and recovery. A sound design may combine a bounded admission queue, per-tenant fairness, content-addressed cache, size-or-time batches, and concurrency matched to measured resources. Results remain bounded to the tested versions and environment.

### Answer 5

Define physical start and completion events for detection, warning activation, acknowledgment, safe-state transition, and recovery. Model train speed, road geometry, sensor uncertainty, power, network, controller, actuator, environment, maintenance, operator, cybersecurity, and simultaneous faults. Separate hard safety deadlines from monitoring and administrative latency. Architect independent local safe behavior, bounded communication and queues, explicit stale-data handling, deterministic priority, clock assumptions, fail-safe states, and observable manual authority.

Automation can check protocol timing, state-machine invariants, deadline propagation, queue and concurrency bounds, configuration, sensor plausibility, clock health, logs, trace completeness, and evidence freshness. Hardware-in-the-loop and field exercises can test timing distributions under load, degraded power and communications, sensor faults, obstruction, recovery, manual procedures, and false activation. Simulation and software tests do not establish physical stopping distance, sensor coverage, human response, regulatory compliance, or acceptable risk. No external railway, safety, regulatory, accessibility, cybersecurity, hardware, human-factors, or practitioner review is claimed. Named qualified authorities must own hazard analysis, timing objectives, physical validation, operating rules, release, and residual risk. Unverified safe-state timing, ambiguous authority, missing physical evidence, failed degraded operation, or unresolved high-severity hazard blocks readiness.
