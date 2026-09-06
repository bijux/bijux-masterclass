---
module_id: SARCH-066
program: Software Engineering: Software Architecture
level: 2
module_number: 66
title: Performance and Capacity Models
status: complete
last_verified: 2026-09-06
---

# Performance and Capacity Models

## One-Page Review

### Governing question

How can an architect predict whether a system will meet response-time, throughput, and backlog objectives as workload, resource demand, concurrency, and failures change—and know when the prediction is not justified?

### Essential definitions

- **workload** describes arrivals, request classes, data, concurrency, timing, locality, and dependencies presented to a system;
- **throughput** $X$ is completed useful work per unit time, while **arrival rate** $\lambda$ is offered work per unit time;
- **response time** $R$ is elapsed time from an agreed start to completion; **service demand** $D_k$ is total busy time demanded from resource $k$ per completed unit;
- **utilization** $U_k$ is the fraction of an observation interval that resource $k$ is busy;
- **capacity** is the sustainable useful throughput satisfying declared quality and failure constraints, not the highest briefly observed request rate;
- **queueing time** is delay before service; **residence time** includes queueing and service at a resource;
- an **open workload** has exogenous arrivals; a **closed workload** has a bounded circulating population and often a think time $Z$;
- a **bottleneck** is the resource whose demand constrains throughput first under the modeled workload mix;
- **headroom** is deliberately unused capacity relative to a stated safe boundary and failure scenario;
- **tail latency** is latency in a declared high percentile or exceedance probability, not “the slow requests” in general.

### Central model, mechanism, or theorem

Operational laws connect measured quantities with few distributional assumptions. In a stable observation scope, Little's law is

$$
N=XR,
$$

where $N$ is mean work in the system, $X$ is completion rate, and $R$ is mean response time. For resource $k$, the utilization law is

$$
U_k=XD_k.
$$

Because $U_k\le 1$ for one unit-capacity resource, $X\le 1/D_k$; therefore the largest resource demand supplies the single-copy bottleneck bound. Queueing models add assumptions about arrivals, service, scheduling, independence, and stationarity. Their formulas are conditional predictions, not operational laws.

### Critical invariants

- every number names workload class, boundary, unit, window, environment, and failure state;
- arrivals, admissions, completions, goodput, and attempts remain distinct;
- latency distributions are not replaced by one mean;
- service demand is measured per completed useful unit and segmented by workload mix;
- utilization below 100% does not imply acceptable latency or recoverability;
- a queue is bounded by memory, deadlines, and useful-work semantics;
- capacity includes dependencies, control planes, warm-up, recovery, and maintenance losses;
- autoscaling delay and scaling limits are part of the model;
- model calibration and holdout validation precede planning reliance;
- overload protection is modeled explicitly rather than inferred from extra replicas.

### Common failures

Common failures include treating requests per second as a workload; using means for tails; extrapolating linearly through saturation; applying $M/M/1$ without Poisson and exponential assumptions; confusing CPU utilization with total capacity; ignoring workload mix, data size, cache state, retries, fan-out, and common dependencies; counting failed attempts as useful throughput; assuming queues absorb sustained overload; sizing only for healthy steady state; letting autoscaling stand in for admission control; and reporting benchmark capacity without correctness checks.

### Compact example

At $X=1{,}200$ completions/s, a request demands $0.55$ ms of CPU and $0.72$ ms of a serialized database resource. The modeled utilizations are $0.66$ and $0.864$. The database is the bottleneck, with an idealized upper bound $1/0.00072\approx1{,}389$ completions/s. That is not safe capacity: tail targets, burstiness, failures, maintenance, demand variance, and model error require a lower governed limit.

### Connections

[SARCH-065](065-dependency-and-coupling-metrics.md) provides the dependency graphs whose paths consume capacity. [SARCH-067](../ROADMAP.md) next models availability and reliability. Performance Engineering owns measurement and optimization technique; this module owns architectural prediction and capacity decisions across boundaries.

## Governing Question

Performance is observed behavior under a workload. Capacity is a decision about how much useful work an architecture can sustain while preserving latency, correctness, availability, recovery, and cost constraints. Neither is an intrinsic scalar attached to a component.

An architecture model must explain why work consumes resources, where it waits, how paths combine, what changes under failure, and which evidence can falsify the forecast. A precise but uncalibrated queueing diagram is less useful than a modest model whose assumptions and error are visible.

## Why This Matters

Performance defects cross architecture boundaries. One request may occupy an admission slot, thread, connection, database lock, storage queue, network path, and downstream quota. Rising delay increases in-flight work; timeouts cause waste; retries add arrivals; health failures remove capacity; traffic shifts overload survivors. Capacity and resilience therefore cannot be planned independently.

Cloud elasticity changed provisioning mechanisms, not the underlying conservation laws. Managed services, containers, serverless platforms, accelerators, and autoscalers still have concurrency, rate, quota, warm-up, locality, and dependency limits. The architect must translate demand into resource and coordination consequences without relying on a vendor dashboard's convenient denominator.

## Prerequisites and Retrieval

Retrieve rate, probability distribution, expectation, variance, percentile, conditional probability, stationary observation, conservation, directed dependency path, concurrency, parallelism, queue, scheduling discipline, cache, replication, batching, backpressure, retry, timeout, admission control, load shedding, autoscaling, failure domain, and quality-attribute scenario.

From SARCH-041 through SARCH-050 retrieve integration, data, deployment, and observability boundaries. SARCH-051 through SARCH-060 supply distributed failure behavior. SARCH-061 through SARCH-065 supply scenarios, risk, fitness functions, and dependency analysis. This module uses queueing results but does not replace a course in stochastic processes or performance engineering.

## Learning Objectives

After completing this module, you should be able to:

1. specify a workload as classes, rates, concurrency, data, locality, and time structure;
2. distinguish arrivals, attempts, admissions, completions, goodput, and backlog;
3. apply Little's law, the utilization law, bottleneck bounds, and the interactive response-time law;
4. state and test the assumptions behind elementary queueing models;
5. model multi-resource paths, fork-join work, batching, caching, retries, and workload-mix shifts;
6. interpret mean, percentile, and exceedance evidence without false aggregation;
7. size headroom for bursts, failures, maintenance, warm-up, and forecast error;
8. design bounded queues, backpressure, admission control, and useful load shedding;
9. calibrate and validate a model against measurements and holdout scenarios;
10. make an evidence-bounded capacity decision with explicit residual risk.

## Core Exposition

**Begin with the decision.** A model exists to answer a question: number of replicas for a launch, maximum admitted jobs during recovery, safe database tenancy, effect of a new request mix, or point at which a cheaper degraded response must begin. Specify the quality scenario before choosing mathematics. A capacity forecast without a decision boundary invites false precision.

**Define the system boundary.** State whether response time begins at the client, edge, process, or internal queue and whether it ends at durable commit, acknowledgement, rendering, or business completion. Include shared services and quotas that can constrain the path. A component benchmark cannot establish end-to-end capacity when identity, storage, network, or control dependencies saturate first.

**Specify workload classes.** Requests per second alone omit cost. Partition by operation, data size, key distribution, locality, cache behavior, fan-out, priority, tenant, and correctness requirement. Record arrival process, daily and seasonal variation, bursts, concurrency, closed populations, cancellations, retries, and background work.

Averages can conceal a mix shift. If reads and writes consume different database demand, the same total transaction rate can require radically different resources. Preserve class-specific demands $D_{ck}$ and calculate aggregate demand from the forecast class mix.

**Separate rates.** Offered arrivals may be rejected, deduplicated, abandoned, timed out, retried, or completed incorrectly. Attempt throughput can rise while useful completion throughput falls. Define goodput as completions satisfying the declared correctness and timeliness criteria.

For a stable system, long-run admitted arrivals and departures balance. If offered arrival persistently exceeds useful completion, backlog or loss grows; a finite queue only delays the visible failure.

**Use operational laws first.** Little's law relates average population, completion rate, and response time for a stable, conserved scope. It does not require exponential service, but its boundary and averaging interval must align. The utilization law follows by accounting for total busy time consumed by completions.

For a closed population $M$ with mean think time $Z$, the interactive response-time law is

$$
M=X(R+Z).
$$

It prevents the common error of expecting throughput to increase indefinitely when a fixed user population waits for responses.

**Find the bottleneck bound.** With one unit-capacity resource $k$, $U_k=XD_k\le1$, so $X_{\max}\le1/D_k$. For $m_k$ equivalent parallel units under justified balancing, the idealized bound becomes $m_k/D_k$. Serialization, skew, coordination, shared dependencies, and imperfect balancing lower attainable throughput.

Demand is not merely wall-clock response time. Measure busy resource time attributable to a completed class, including repeated visits. Waiting for a database does not consume caller CPU continuously, while lock holding or occupied connections may consume other constrained resources.

**Add queueing assumptions explicitly.** Kendall notation such as $M/M/1$ identifies arrival, service, and server assumptions. For a stable $M/M/1$ queue with arrival rate $\lambda$, service rate $\mu$, and $\rho=\lambda/\mu<1$, mean residence time is

$$
R=\frac{1}{\mu-\lambda}=\frac{S}{1-\rho},
$$

where $S=1/\mu$. The nonlinear growth near $\rho=1$ is instructive, but real arrivals may be bursty, service heavy-tailed, servers heterogeneous, scheduling non-FIFO, and requests correlated. Validate rather than merely naming the model.

For an $M/G/1$ FIFO queue, the Pollaczek–Khinchine mean-wait formula

$$
W_q=\frac{\lambda E[S^2]}{2(1-\rho)}
$$

shows why equal mean service with greater variance can produce much greater mean waiting. This conclusion still depends on the model's arrival, independence, service, and discipline assumptions.

**Model networks of resources.** Trace each class through CPU, storage, network, locks, pools, and dependencies. Sum sequential residence times only when boundaries and conditioning align. Averages cannot be naively added across timeouts, retries, cache branches, or conditional paths.

Parallel fan-out completes near a maximum, not a sum. Its tail depends on branch distributions and dependence. Shared congestion makes independence assumptions especially unsafe. Critical-path structure, join policy, cancellation, quorum, and partial-result semantics belong in the architecture model.

**Treat percentiles as distributions.** Name the population, window, sampling, aggregation method, and percentile definition. The percentile of per-host percentiles is generally not the fleet percentile. A one-hour percentile can hide a five-minute incident, and a global percentile can hide a tenant or region.

High percentiles require enough relevant observations and uncertainty reporting. Model tails with empirical distributions, conditional scenarios, or justified stochastic models. Never infer p99 from a mean alone.

**Represent caches and batching as state.** Cache capacity depends on hit ratio by class, key popularity, object size, invalidation, eviction, cold start, and origin behavior. A cache can improve latency while creating miss-storm and consistency risks. Test warm, cold, churn, and failover states.

Batching amortizes setup and improves throughput, but adds fill delay, memory, deadline, fairness, and replay consequences. Averages across batch sizes obscure the latency experienced by sparse classes.

**Model feedback.** Timeouts, retries, hedges, autoscaling, load balancing, and health checks respond to latency and can amplify it. Every retry consumes a budget and creates additional offered work. Removed replicas increase load on survivors. Slow scaling may arrive after a burst and can intensify cold-cache or database pressure.

Write the feedback path and delay explicitly. A static spreadsheet that assumes independent arrivals and instant capacity cannot predict an overload cascade.

**Design queues by usefulness.** Queue size is not a capacity substitute. Bound queues by acceptable waiting time, memory, cancellation propagation, and work expiry. Reject or shed early when completing late work has no value. Preserve priority, fairness, and safety rather than accepting everything into an unbounded backlog.

Backpressure tells producers that downstream capacity is constrained. It requires propagation semantics: block, reduce rate, defer, shed, degrade, or store durably. Moving a queue to a broker does not remove the capacity equation; it changes durability and drain behavior.

**Size for scenarios.** Establish forecast demand, safe measured capacity, required failure tolerance, planned maintenance, deployment surge, recovery work, background tasks, quota ceilings, and uncertainty. Headroom must be attached to a reason. A blanket percentage cannot substitute for losing a failure domain or serving a cold-cache recovery.

For independent replicas, calculate both healthy utilization and utilization after required losses. Then test whether dependencies and load balancing preserve that model. Capacity in a surviving region is useless if a shared control plane cannot authorize or route recovery.

**Calibrate and validate.** Estimate demands from utilization and goodput, traces, profiles, counters, and controlled experiments. Reconcile independent measurements and check units. Fit on one workload range; validate against holdout rates, mixes, bursts, failures, and versions. Record residuals and where error changes sign.

Load tests must verify correctness, not just speed. Ramp, step, impulse, soak, stress beyond the intended limit, recovery, cold start, scale-out, failover, and dependency degradation reveal different mechanisms. Use production-like data and topology while protecting real users and systems.

**Govern the result.** Publish the model version, inputs, equations, assumptions, calibration data, validation error, sensitivity, safe operating envelope, owner, refresh trigger, and decision. Create fitness functions for demand regression, queue age, saturation, mixed-version behavior, and graceful overload.

A model expires when workload, implementation, topology, dependency, hardware, configuration, or failure policy changes materially. Capacity is maintained evidence, not a once-a-year number.

## Definitions and Notation

For a declared steady observation scope:

- $\lambda_c$ is offered arrival rate for class $c$;
- $X_c$ is useful completion throughput for class $c$;
- $R_c$ is mean end-to-end response time for completed class-$c$ work;
- $N_c$ is mean class-$c$ work present in the system;
- $D_{ck}$ is mean service demand placed by one completed class-$c$ unit on resource $k$;
- $U_k$ is mean utilization of resource $k$ in the scope;
- $S$ is service time for one queue visit and $W_q$ is waiting time before service;
- $\rho$ is offered load relative to service capacity in a declared queueing model;
- $M$ is a closed circulating population and $Z$ is mean think time;
- $B(t)$ is backlog at time $t$;
- **safe capacity** is the maximum admitted workload supported by evidence while all named constraints hold;
- **breaking point** is the workload at which one or more declared constraints cease to hold;
- **headroom** is the difference or ratio between forecast demand and a named safe boundary;
- **goodput** counts only timely and correct useful completions.

For multiple classes, utilization is $U_k=\sum_c X_cD_{ck}$ when demands and completions share the same interval and resource normalization. A formula is dimensionally invalid if its units do not cancel as claimed.

## Mechanisms, Invariants, or Proof Structure

### Modeling and validation procedure

1. State the decision, quality scenarios, safety constraints, and time horizon.
2. Define system and measurement boundaries.
3. Segment workload classes and forecast their time structure.
4. Map each class to paths, resources, dependencies, and feedback controls.
5. Measure baseline rates, distributions, demands, utilization, queues, errors, and correctness.
6. Apply operational laws and calculate bottleneck bounds.
7. Add only queueing, fork-join, cache, batch, or scaling assumptions required by the decision.
8. Recompute healthy, burst, maintenance, failure, recovery, and mix-shift scenarios.
9. Calibrate on one data set and validate on independent holdout scenarios.
10. Set a safe envelope, overload behavior, ownership, uncertainty, and refresh triggers.

### Executable resource-demand calculation

The calculation checks arithmetic for one fixed workload and two normalized single-capacity resources. It does not establish a production system's demand, safe utilization, latency, or balancing.

<!-- bijux-verify: {"id":"resource-demand-bound","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"cpu utilization=0.660\ndatabase utilization=0.864\ndatabase ideal bound=1388.9 per second\n","stderr":""}} -->
```python
throughput = 1200.0
demands = {"cpu": 0.00055, "database": 0.00072}

for resource in ("cpu", "database"):
    print(f"{resource} utilization={throughput * demands[resource]:.3f}")

bottleneck = max(demands, key=demands.get)
print(f"{bottleneck} ideal bound={1 / demands[bottleneck]:.1f} per second")
```

### Invariants

- arrival, admission, attempt, completion, goodput, rejection, abandonment, and backlog accounts reconcile;
- every rate and demand carries compatible units;
- steady-state laws are not applied across an accumulating backlog without disclosure;
- every queueing result states stability, arrival, service, scheduling, and dependence assumptions;
- percentiles name population, window, and calculation method;
- healthy, degraded, failure, maintenance, recovery, and cold states remain separate;
- the forecast workload remains inside the validated range or extrapolation is explicit;
- capacity is not accepted without correctness and overload-behavior evidence.

## Alternatives and Trade-Offs

- **Operational laws versus stochastic queues:** operational laws need fewer distributional assumptions; queueing models predict waiting only under stronger hypotheses.
- **Analytical model versus simulation:** equations expose sensitivity and bounds; simulation represents richer policies but adds implementation and validation risk.
- **Simulation versus load test:** simulation explores unbuilt or dangerous scenarios; load tests observe a real implementation in a bounded environment.
- **Open versus closed generator:** open load preserves offered rate during slowdown; closed load can hide overload because clients wait before issuing more work.
- **Mean versus percentile objective:** means support conservation accounting; percentiles expose tail experience but need population and sampling discipline.
- **Scale up versus scale out:** larger nodes reduce coordination; more nodes add balancing, partitioning, and shared-service pressure.
- **Queue versus rejection:** queues absorb bounded bursts and smooth work; early rejection protects deadlines and resources during sustained overload.
- **Backpressure versus durable buffering:** backpressure limits production; durable buffers tolerate disconnection but create backlog, expiry, and drain obligations.
- **Autoscaling versus reserved headroom:** autoscaling adapts to trends; headroom serves disturbances during detection, provisioning, and warm-up delay.
- **Caching versus origin capacity:** caching lowers common-case demand; origin capacity and miss-storm controls remain necessary.
- **Batching versus immediacy:** batching improves amortization and throughput; it adds fill delay and fairness risk.
- **Global pooling versus cells:** pooling improves utilization; cells constrain blast radius and may strand capacity.
- **Peak provisioning versus degradation:** peak provisioning protects full quality at cost; graceful degradation preserves selected outcomes with explicit product trade-offs.

## Failure Modes and Misconceptions

1. **“Capacity is requests per second.”** Request classes, cost, correctness, and latency define useful capacity.
2. **“Average latency predicts p99.”** Many distributions share a mean and have radically different tails.
3. **“Fifty percent CPU means fifty percent spare capacity.”** Another resource, one hot shard, queue, quota, lock, or tail target may bind first.
4. **“Utilization grows linearly through saturation.”** Throughput may flatten while waiting and errors grow nonlinearly.
5. **“Little's law predicts queueing.”** It relates long-run averages; it does not determine a latency distribution.
6. **“$M/M/1$ is a generic server formula.”** Its arrival, service, independence, stationarity, discipline, and stability assumptions matter.
7. **“A closed load test proves open-arrival capacity.”** Client waiting can throttle offered load and hide backlog growth.
8. **“A queue adds capacity.”** It stores work temporarily and adds waiting, memory use, and expiry risk.
9. **“Autoscaling prevents overload.”** Detection, quota, provisioning, startup, warm-up, and downstream limits create delay and ceilings.
10. **“Retries improve success without changing capacity.”** They consume attempts and can form positive feedback.
11. **“Async work has no latency target.”** Queue age, deadline, freshness, and drain time are latency constraints.
12. **“Caches permanently remove origin demand.”** Cold starts, churn, invalidation, skew, and failover can restore or amplify it.
13. **“Parallel branch latencies add.”** Completion often depends on a maximum, quorum, or cancellation policy.
14. **“Per-host p99 can be averaged.”** Aggregated percentiles require the underlying population or an appropriate mergeable distribution.
15. **“A benchmark run is capacity evidence.”** Topology, data, correctness, duration, workload, and failure state determine relevance.
16. **“More replicas always add proportional throughput.”** Serialization, skew, coordination, and shared bottlenecks violate the assumption.
17. **“Healthy peak sizing covers failover.”** Loss, maintenance, recovery work, and cold state consume the margin.
18. **“The model is the system.”** Calibration error and missing mechanisms are evidence, not inconveniences to hide.

## Worked Examples

### Example 1

**Infer concurrency with Little's law.**

**Situation.** A stable service completes 800 correct requests/s with mean end-to-end response time 120 ms.

**Reasoning.** Align units: $R=0.120$ s. Then $N=XR=800\cdot0.120=96$ requests on average. The result includes whatever waiting and service lie inside the response-time boundary. It neither states the maximum concurrency nor predicts the distribution.

**Conclusion.** The declared boundary contains mean population 96 under the stable observation.

### Example 2

**Find a bottleneck bound.**

**Situation.** At 1,200 useful completions/s, CPU demand is 0.55 ms and serialized database demand is 0.72 ms per completion.

**Reasoning.** $U_{cpu}=1200(0.00055)=0.66$ and $U_{db}=1200(0.00072)=0.864$. The ideal one-resource bounds are about 1,818/s and 1,389/s. Database demand is largest, so it binds first. Queueing and tail objectives require operating below the ideal limit.

**Conclusion.** The database is the modeled bottleneck; 1,389/s is a bound, not safe capacity.

### Example 3

**Expose queueing nonlinearity.**

**Situation.** An $M/M/1$ model has mean service time 8 ms and arrival rate 100/s.

**Reasoning.** $\mu=1/0.008=125$/s and $\rho=100/125=0.8$. Conditional on the model assumptions, $R=1/(125-100)=0.040$ s. Only 8 ms is service; 32 ms is mean waiting. Raising utilization from zero to 0.8 multiplied residence time by five.

**Conclusion.** Near saturation, small load changes can create disproportionate waiting under the stated queue model.

### Example 4

**Show the cost of service-time variance.**

**Situation.** Two $M/G/1$ FIFO systems have $E[S]=10$ ms and $\lambda=60$/s, hence $\rho=0.6$. One has deterministic service; the other has coefficient of variation 2.

**Reasoning.** Deterministic service has $E[S^2]=0.0001$ s², so $W_q=60(0.0001)/[2(0.4)]=7.5$ ms and mean residence is 17.5 ms. With $CV=2$, variance is $4(0.01)^2=0.0004$ and $E[S^2]=0.0005$ s². Waiting becomes $60(0.0005)/0.8=37.5$ ms and residence 47.5 ms.

**Conclusion.** Equal mean demand and utilization do not imply equal latency when service variability differs.

### Example 5

**Avoid a percentile boundary trap.**

**Situation.** Under nearest-rank calculation, 990 of 1,000 requests take 50 ms and ten take 5 s.

**Reasoning.** Mean latency is $[990(50)+10(5000)]/1000=99.5$ ms. Nearest-rank p99 is observation $\lceil0.99(1000)\rceil=990$, or 50 ms; p99.1 is observation 991, or 5 s. Neither the mean nor p99 alone describes the cliff. Time-window and class segmentation can expose whether the slow ten cluster in one tenant or incident.

**Conclusion.** Percentile choice and population boundary can hide a consequential minority.

### Example 6

**Model a closed population.**

**Situation.** Two thousand interactive users have mean think time 1.6 s and mean response time 0.4 s.

**Reasoning.** The interactive law gives $X=M/(R+Z)=2000/(0.4+1.6)=1000$/s. If response grows to 0.9 s with the same population and think time, offered throughput falls to $2000/2.5=800$/s. A closed generator can therefore report only 800/s during slowdown rather than reveal the backlog an open 1,000/s arrival stream would create.

**Conclusion.** Workload population mechanics determine what a test can prove.

### Example 7

**Calculate retry amplification.**

**Situation.** A service receives 800 original requests/s; 5% fail on the first attempt and every such request makes exactly one retry.

**Reasoning.** Retries add $800(0.05)=40$ attempts/s, so the backend sees 840 attempts/s, a 5% amplification, before considering whether retries also fail or overlap timed-out original work. If capacity was planned from originals only, the safety margin was overstated.

**Conclusion.** Retry policy belongs in offered-load and feedback models.

### Example 8

**Size replica headroom for loss.**

**Situation.** One warmed replica has tested safe capacity 150 requests/s. Forecast peak is 1,200/s, and policy requires surviving two unavailable replicas without exceeding that tested limit.

**Reasoning.** Eight healthy replicas exactly serve 1,200/s, leaving no loss margin. Provision ten warmed replicas: after losing two, eight remain at 150/s each. Healthy utilization against the tested limit is $1200/(10\cdot150)=0.8$. This arithmetic assumes balanced load and independent replicas; shared database and control-plane capacity require separate checks.

**Conclusion.** Ten is the replica count implied by this narrow N+2 scenario, not proof of end-to-end capacity.

### Example 9

**Determine whether a backlog can recover in time.**

**Situation.** A burst adds 90,000 valid jobs. New work continues at 500 jobs/s, processing capacity is 650 jobs/s, and jobs lose value after five minutes.

**Reasoning.** Net drain is $650-500=150$ jobs/s. Drain time is $90{,}000/150=600$ s, or ten minutes. Even if no additional failures occur, the last jobs exceed the five-minute usefulness limit. Required action is shedding, prioritization, extra verified capacity, or a changed product guarantee—not a larger queue alone.

**Conclusion.** Positive drain rate is insufficient when backlog deadlines are tighter than drain time.

### Example 10

**Detect a workload-mix capacity failure.**

**Situation.** A database receives 900 reads/s at 0.4 ms demand and 100 writes/s at 4 ms demand.

**Reasoning.** Utilization demand is $900(0.0004)+100(0.004)=0.36+0.40=0.76$. At the same total 1,000 operations/s but a 600/400 mix, it becomes $600(0.0004)+400(0.004)=0.24+1.60=1.84$, beyond one normalized resource. Total operations/s did not change; class mix did.

**Conclusion.** Capacity forecasts must preserve class-specific service demand and mix.

## Cross-Program Connections

- **Algorithm Engineering:** owns efficient algorithms, approximation, profiling-aware selection, and cost growth.
- **Operating Systems:** owns scheduling, virtual memory, I/O, synchronization, and kernel resource behavior.
- **Computer Architecture:** owns pipelines, caches, memory hierarchy, vectorization, accelerators, and hardware counters.
- **Networking:** owns transport, congestion control, queue management, topology, and network measurement.
- **Distributed Systems Engineering:** owns replication, partitioning, consensus, distributed queues, failure, and coordination.
- **Large-Scale Distributed Systems:** owns fleet-scale scheduling, storage, serving, and tail behavior.
- **Software Delivery and Reliability Engineering:** owns SLO operation, incident feedback, delivery regression, and production reliability evidence.
- **Data Engineering:** owns pipeline throughput, watermarks, backlog, state, and data-quality consequences.
- **Platform Engineering:** owns quota, autoscaling, placement, tenancy, and shared platform capacity mechanisms.
- **Systems Engineering:** owns end-to-end physical, supplier, human, safety, and lifecycle capacity constraints.
- **Performance Engineering:** owns deep measurement, benchmarking, experiments, statistical analysis, and optimization; this architecture module uses that evidence for structural decisions.

## References

1. John D. C. Little, “A Proof for the Queuing Formula: $L=\lambda W$,” *Operations Research* 9(3), 1961. <https://doi.org/10.1287/opre.9.3.383>
2. Peter J. Denning and Jeffrey P. Buzen, “The Operational Analysis of Queueing Network Models,” *ACM Computing Surveys* 10(3), 1978. <https://doi.org/10.1145/356733.356735>
3. Edward D. Lazowska, John Zahorjan, G. Scott Graham, and Kenneth C. Sevcik, *Quantitative System Performance: Computer System Analysis Using Queueing Network Models*, Prentice-Hall, 1984. <https://homes.cs.washington.edu/~lazowska/qsp/>
4. Raj Jain, *The Art of Computer Systems Performance Analysis*, Wiley, 1991.
5. Mor Harchol-Balter, *Performance Modeling and Design of Computer Systems*, Cambridge University Press, 2013.
6. Leonard Kleinrock, *Queueing Systems, Volume 1: Theory*, Wiley, 1975.
7. Neil J. Gunther, *Guerrilla Capacity Planning*, Springer, 2007. <https://doi.org/10.1007/978-3-540-31010-5>
8. Mike Ulrich, “Addressing Cascading Failures,” in *Site Reliability Engineering*, O'Reilly Media, 2016, retrieved 2026-09-06. <https://sre.google/sre-book/addressing-cascading-failures/>
9. Niall Richard Murphy and David K. Rensin, “Handling Overload,” in *Site Reliability Engineering*, O'Reilly Media, 2016, retrieved 2026-09-06. <https://sre.google/sre-book/handling-overload/>
10. ISO/IEC 25010:2023, *Systems and software engineering—Systems and software Quality Requirements and Evaluation (SQuaRE)—Product quality model*, 2nd ed., November 2023. <https://www.iso.org/standard/78176.html>

## Exercises

### Exercise 1

Define workload, arrival rate, throughput, goodput, response time, service demand, utilization, capacity, queueing time, bottleneck, headroom, open workload, closed workload, backpressure, and tail latency. State the distinction between an operational law and a queueing-model prediction.

### Exercise 2

A stable service completes 600 useful requests/s with mean response time 250 ms. Each completion demands 0.8 ms from one CPU resource and 1.2 ms from one storage resource. Compute mean in-system work, both utilizations, each ideal resource bound, and the bottleneck. Explain what cannot be concluded.

### Exercise 3

Diagnose a capacity test that uses 200 closed-loop clients, reports only mean latency and total attempts, runs for three minutes against warm caches, stops at the first error, omits background work, and extrapolates linearly to regional failover. Design corrected evidence.

### Exercise 4

Compare reserved headroom, autoscaling, buffering, backpressure, admission control, and graceful degradation for a bursty document-conversion service. Specify triggers, time constants, fairness, expiry, dependencies, and failure behavior.

### Exercise 5

Design a performance and capacity model for an international rail reservation platform facing commuter peaks, flash-sale traffic, seat contention, payment calls, pricing fan-out, mobile retries, regional loss, timetable updates, fraud checks, accessibility needs, and a hard prohibition on duplicate confirmed seats. Include boundaries, workload classes, equations, experiments, overload policy, correctness evidence, uncertainty, ownership, and refresh triggers.

## Answers to the Exercises

### Answer 1

A **workload** describes the classes, arrival or population mechanics, data, locality, concurrency, timing, and dependencies presented to a system. **Arrival rate** is offered work per time; **throughput** is completed work per time; **goodput** counts timely, correct, useful completions. **Response time** is elapsed time across a declared boundary. **Service demand** is busy time required from a resource per completed unit. **Utilization** is its busy fraction. **Capacity** is sustainable goodput satisfying named constraints.

**Queueing time** precedes service. A **bottleneck** constrains throughput first for the modeled mix. **Headroom** is unused capacity against a safe scenario boundary. Open workloads receive exogenous arrivals; closed workloads circulate a bounded population. **Backpressure** propagates constrained downstream capacity to producers. **Tail latency** is a declared high percentile or exceedance probability. An operational law follows from conservation over a suitable stable scope with comparatively few distributional assumptions; a queueing prediction adds assumptions about arrivals, service, independence, scheduling, and stationarity.

### Answer 2

Convert 250 ms to 0.25 s. Little's law gives $N=XR=600(0.25)=150$ requests on average inside the boundary. CPU utilization is $600(0.0008)=0.48$; its ideal bound is $1/0.0008=1{,}250$/s. Storage utilization is $600(0.0012)=0.72$; its ideal bound is about $833.3$/s. Storage has the largest demand and is the modeled bottleneck.

These means do not determine a latency distribution, safe operating point, burst response, correctness, class mix, failure capacity, or whether another omitted dependency binds first. The bounds assume one normalized unit-capacity resource and stable per-completion demands; queueing, skew, coordination, and quality targets lower attainable safe capacity.

### Answer 3

Closed clients reduce offered rate as responses slow, so add an open-loop generator for forecast arrivals while retaining a closed test for interactive behavior. Record arrivals, admissions, attempts, retries, errors, cancellations, completions, correct goodput, backlog, and per-class latency distributions. Report fleet and segmented percentiles with windows, counts, and confidence or repetition—not only a mean.

Test cold, warm, churn, and failover caches; include realistic data, key skew, request mix, fan-out, background work, quotas, and dependencies. Run ramp, step, impulse, soak, breaking-point-and-beyond, recovery, scale-out, maintenance, and regional-loss scenarios long enough to expose leaks and controls. Continue safely beyond first rejection to distinguish graceful shedding from throughput collapse. Measure demands and bottlenecks, validate correctness during overload, and model regional loss from the measured surviving topology rather than linear multiplication. Calibrate on selected runs and reserve independent holdouts for validation.

### Answer 4

Reserve headroom for work that must start before new instances become useful and for required replica or zone loss. Autoscaling follows sustained leading demand with explicit observation, decision, provisioning, startup, warm-up, quota, placement, cooldown, and scale-in delays; it cannot outrun an impulse or a fixed downstream quota. A bounded durable buffer absorbs document bursts only when storage, deadline, tenant fairness, and net drain rate keep work useful.

Backpressure should reduce producer admission or defer submissions when queue age, predicted deadline, or downstream saturation crosses a warning boundary. Admission control rejects cheaply before expensive parsing and isolates tenant and priority budgets. Graceful degradation may skip optional previews, choose cheaper rendering, or defer nonurgent formats, but must never silently corrupt output or bypass security scans. Use per-class queue-age and completion SLOs, resource saturation, dependency health, and predicted drain time as triggers. Test overload, poison documents, retries, regional loss, cold workers, autoscaler exhaustion, and recovery; preserve accessibility-critical conversions and publish explicit rejection or delay semantics.

### Answer 5

Place the user boundary at intent submission and define separate outcomes for search, quote, seat hold, payment authorization, durable confirmation, notification, and business completion. Segment commuter search, flash-sale purchase, timetable ingestion, operator changes, refund, fraud review, and accessibility-assisted flows by region, itinerary complexity, data size, cache state, fan-out, payment method, retry behavior, and priority. Keep arrivals, admissions, attempts, holds, expirations, payments, confirmed unique seats, rejections, and backlog in a reconciling account.

Use Little's and utilization laws for stable measured scopes, class-resource demands for search, pricing, inventory, payment, fraud, storage, network, and operator control, bottleneck bounds per surviving region, closed-population laws only for genuinely closed sessions, and bounded queue/drain equations for deferred work. Model seat locks or compare-and-set serialization, pricing and search fork-join tails, cache miss states, retry amplification, autoscaling delays, quota ceilings, shared control dependencies, and region-loss traffic. Analytical queues or simulation must state arrival, service, dependence, priority, abandonment, and stationarity assumptions.

Calibrate with traces, resource accounting, profiles, ledger invariants, and production-like controlled runs. Validate on holdout peak mixes, hot trains, cold caches, timetable changes, payment degradation, fraud latency, step and impulse load, soak, breaking point, two-sided retry behavior, maintenance, regional loss, and recovery. At every load, reconcile each confirmed seat to one authoritative inventory transition and test duplicate, timeout, ambiguous payment, cancellation, and replay cases. A fast duplicate confirmation is a failure, never goodput.

Reserve warmed failure headroom for critical confirmation; shed speculative search, previews, or low-priority refresh by explicit policy; use per-route and per-tenant fairness; bound holds and queues by expiry; propagate cancellation; and degrade only features whose omission preserves safety, accessibility, financial, and passenger commitments. Publish model version, forecast, inputs, equations, validation residuals, sensitivity to mix and fan-out, safe envelope, unknowns, and residual risk. Service, database, payments, fraud, network, regional operations, accessibility, security, finance, safety, and product owners approve relevant boundaries. Refresh after timetable seasons, launch policy, workload mix, topology, code, provider, quota, retry, consistency, or failure-policy changes.
