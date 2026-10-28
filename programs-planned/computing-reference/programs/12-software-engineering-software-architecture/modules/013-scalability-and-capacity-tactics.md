---
module_id: SARCH-013
program: Software Engineering: Software Architecture
level: 1
module_number: 13
title: Scalability and Capacity Tactics
status: complete
last_verified: 2026-09-05
---

# Scalability and Capacity Tactics

## One-Page Review

### Governing question

How should architecture preserve defined service outcomes as demand changes across users, data, work mix, geography, tenants, and time?

### Essential definitions

- **capacity** is the maximum workload a defined system configuration can sustain while all required outcome constraints hold.
- **scalability** is how behavior and required resources change as one or more workload dimensions change.
- **elasticity** is the ability to adjust allocated resources in response to changing demand within stated time, cost, and correctness bounds.
- **headroom** is deliberately unused capacity reserved for bursts, failures, recovery, maintenance, estimation error, or growth.
- A **bottleneck** is the constraining resource, dependency, serialized activity, or policy at a given workload and configuration.
- **vertical scaling** changes the capacity of a resource instance; **horizontal scaling** changes the number of cooperating instances.
- **partitioning** assigns subsets of data or work to different resources by an explicit rule.
- **work amplification** is the ratio between internal work performed and useful external work completed.
- A **capacity envelope** is the tested region of workloads, configurations, and conditions for which objectives are met.

### Central model, mechanism, or theorem

Represent workload as a vector rather than one request rate:

$$
w=(r, c, b, d, q, f, g, t, m),
$$

where terms may describe arrival rate, concurrency, bytes, data size, query mix, fan-out, geography, tenant skew, and mutation ratio. For resource $i$, let $D_i(w)$ be average service demand per useful completion and $C_i$ its usable service capacity. A first-order utilization estimate is

$$
\rho_i=\frac{X D_i(w)}{C_i}.
$$

Architecture identifies the limiting constraint, reduces or partitions demand, increases usable capacity, and controls admission while preserving correctness and fairness. This estimate is a planning model; variability, coordination, failures, imbalance, and queueing require measured evidence.

### Critical invariants

- define useful outcomes and every workload dimension that can change resource demand;
- measure capacity only while latency, correctness, availability, fairness, and cost constraints hold;
- identify per-resource demand and the current bottleneck rather than averaging utilization;
- preserve authoritative state and partition ownership during scaling and rebalancing;
- bound queues, concurrency, retries, fan-out, replication, and background work;
- reserve justified headroom for bursts, failure, rollout, repair, and estimation error;
- include control-plane, supplier-quota, identity, network, storage, and operator limits;
- test skew, hotspots, cold starts, resharding, failover, and scale-in—not only even steady load;
- make tenant isolation and priority policy explicit;
- bind claims to workload, topology, version, data, window, and evidence.

### Common failures

Common failures include calling a high-throughput benchmark “scalable”; scaling stateless workers while one database or quota remains serial; averaging tenant or key skew away; treating autoscaling as instantaneous; adding replicas that multiply reads, writes, storage, or coordination; using an unbounded queue as burst capacity; ignoring scale-in correctness; assuming partition count equals usable parallelism; preserving no failure headroom; measuring accepted requests rather than correct completions; and extrapolating far beyond the tested capacity envelope.

### Compact example

A request consumes 8 ms of one CPU core on average. At 600 correct completions/s, demand is $600\times0.008=4.8$ core-seconds per second. Six ideal cores would average 80% utilization, but six is not a safe provisioned answer: traffic variability, uneven scheduling, garbage collection, retries, failure capacity, deployment overlap, and tail objectives need margin and evidence. The calculation reveals a lower-level demand relationship, not production capacity.

### Connections

[SARCH-003](003-functional-scope-and-system-context.md) supplies dependency boundaries; [SARCH-011](011-availability-and-recovery-tactics.md) supplies failure capacity and recovery; [SARCH-012](012-performance-and-latency-tactics.md) supplies latency, queues, and admission control. [SARCH-020](../ROADMAP.md) resolves competing quality attributes, while [SARCH-066](../ROADMAP.md) later develops advanced quantitative performance and capacity models.

## Governing Question

A service may handle ten times more traffic after adding ten workers—or collapse because they contend on one lock, exhaust one connection pool, overload one database, or exceed a supplier quota. A data system may scale in record count but not in write-key skew. A platform may provision quickly but recover slowly because new instances start cold. What makes a scaling claim architecturally meaningful?

The governing question is how demand dimensions map to resources, state, coordination, topology, and control so the system remains inside a defined outcome envelope. Scalability is not a product label or a topology name. It is a relationship among workload, configuration, outcomes, cost, and time.

## Why This Matters

Growth exposes implicit serialization and shared limits. One global sequence, schema migration, identity tenant, certificate authority, deployment controller, metadata service, or operator team can limit an otherwise distributed system. Capacity analysis must cross system and organizational boundaries.

Demand also changes shape. Traffic may grow while payload size, data retention, tenant skew, write ratio, fan-out, query complexity, geography, and security checks change independently. A scalar requests-per-second forecast hides these drivers and produces false confidence.

Scaling creates correctness work. Adding and removing resources changes routing, ownership, caches, replicas, leases, and in-flight operations. Repartitioning can lose, duplicate, reorder, or expose stale state. Architecture must specify transition invariants, not only steady-state topology.

## Prerequisites and Retrieval

Retrieve workload, useful completion, arrival rate, concurrency, service demand, utilization, throughput, latency distribution, queue, bottleneck, saturation, partition, replication, consistency, idempotency, admission control, backpressure, load shedding, headroom, elasticity, failover, and evidence limitation.

From prior modules, retrieve context crossings, quality-attribute scenarios, constraints and assumptions, trade-off points, availability fault models, performance budgets, Little's Law, tail behavior, and overload control. You should be able to distinguish offered load, accepted load, attempted work, and correctly completed work.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish capacity, scalability, elasticity, and performance;
2. define multidimensional workload and outcome envelopes;
3. estimate per-resource service demand and utilization;
4. locate shifting bottlenecks across configurations and workloads;
5. choose vertical, horizontal, replication, partitioning, and demand-reduction tactics;
6. reason about state ownership during rebalance and scale-in;
7. define headroom for bursts, failures, rollout, and recovery;
8. design autoscaling with signal, delay, hysteresis, and safe bounds;
9. test skew, hotspots, quotas, cold starts, and work amplification;
10. reject unsupported extrapolation beyond measured evidence.

## Core Exposition

**Define outcomes before capacity.** Capacity is not the point where a process crashes. It is the greatest workload within a declared family for which correct completion, latency, availability, durability, fairness, security, and resource constraints all hold. If throughput rises because the system returns errors or stale data, useful capacity did not rise.

State configuration, versions, topology, data, workload, warm state, failure state, test duration, and cost boundary. A capacity number without these conditions cannot guide design or operation.

**Model workload as dimensions.** Record arrival distributions, concurrency, payload and result sizes, data volume, retention, operation mix, read/write ratio, fan-out, locality, geography, tenant and key skew, background work, and seasonality. Include invalid, malicious, and retry traffic if it consumes resources.

Choose independent axes for experiments. Increasing only request rate while keeping a tiny dataset and uniform keys does not test data growth or hotspots. Use named workload classes rather than one synthetic average.

**Build a resource-demand map.** Trace each useful operation across CPU, memory, storage, network, connections, locks, threads, accelerators, external quotas, and human or control-plane work. Estimate demand per operation class and validate it with measurements. The same request rate can require radically different capacity when the mix changes.

Resource utilization averages can hide local exhaustion. Inspect per-core, per-device, per-partition, per-pool, per-tenant, and per-dependency constraints. Saturation signals include queue growth, allocation failure, throttling, lock wait, connection wait, eviction, retry amplification, and latency growth.

**Find the present bottleneck.** At a fixed configuration and workload, the bottleneck is the first constraint that prevents all objectives from holding. Removing it usually reveals another. Treat bottlenecks as workload-dependent: a read-heavy workload may be storage-bound, a write-heavy workload coordination-bound, and a large-payload workload network-bound.

Do not optimize a non-limiting resource merely because it is easy to measure. Use path traces, queues, service demand, controlled experiments, and configuration changes to establish causality.

**Reduce demand.** Remove unnecessary work, improve algorithms and representations, batch fixed overhead, cache valid results, compress selectively, precompute stable products, coalesce duplicates, and avoid unneeded synchronous fan-out. Rate-limit abusive or low-value traffic and make expensive operations explicit.

Demand reduction can move work elsewhere or later. Cache invalidation, background recomputation, replication, compaction, and indexes consume capacity too. Count total work across steady state, change, failure, and recovery.

**Scale vertically where it fits.** A larger instance can provide more CPU, memory, I/O, or accelerator capacity without distributing state or coordination. It is often operationally simpler and can improve single-operation latency. Limits include maximum size, restart or migration, cost discontinuities, failure blast radius, and inability to divide one hot resource.

Vertical scaling is not inherently temporary or inferior. Choose it when the capacity envelope, availability model, and economics fit. Preserve a tested path for maintenance and failure.

**Scale horizontally with explicit collaboration.** Adding instances helps when work can be distributed and shared limits do not dominate. Stateless request handling is easy only if stateful dependencies have sufficient capacity. Shared locks, connection pools, metadata, coordination, deployment, logging, and network paths can become bottlenecks.

Define discovery, routing, health, membership, warm-up, version compatibility, state, session, and scale-in behavior. New instances add usable capacity only after dependencies, code, data, caches, and security material are ready.

**Replicate reads carefully.** Read replicas can distribute read demand and improve locality. They add write, storage, network, catch-up, routing, and consistency work. Define which reads may be stale, maximum lag, monotonic or read-your-writes needs, failure behavior, and promotion ownership. Replication is not free capacity.

**Partition data and work.** Partition by key, range, hash, geography, tenant, time, or workload class. A good rule distributes the relevant demand, preserves required locality, bounds fan-out, and supports ownership changes. More partitions enable parallelism but increase metadata, coordination, operational, and small-partition overhead.

Skew is the central adversary. One tenant or key can dominate a partition even when total load is modest. Observe distribution, not only averages. Options include better keys, subpartitioning hot entities, isolated tenancy, read replication, aggregation, admission policy, or domain-specific redesign.

**Specify rebalance invariants.** During ownership movement, define source and destination authority, version or epoch, in-flight requests, duplicate delivery, ordering, consistency, rollback, throttling, and completion evidence. Fencing prevents an old owner from continuing writes after transfer. Rebalance work must be capacity-limited so it does not cause the incident it is meant to prevent.

Scale-in deserves equal rigor. Drain work, preserve accepted operations, transfer state, update routing, expire leases, reconcile duplicates, and retain rollback. Terminating “idle” instances without understanding long-lived sessions or delayed work can lose service.

**Reserve headroom by scenario.** Headroom covers bursts, estimation error, traffic growth between changes, one or more failed resources, deployment overlap, maintenance, cold capacity, recovery traffic, and background work. A single percentage is useful only after these scenarios are enumerated.

If peak modeled demand is $L$ and target maximum utilization is $u_{max}>0$, a first-order provisioned capacity is at least $L/u_{max}$. If one of $n$ equal units must fail without violating the target, validate the remaining $n-1$ units, not the nominal fleet. Correlated failures and uneven load require stronger analysis.

**Design elasticity as a control loop.** Autoscaling observes a signal, decides, provisions, warms, routes, and later removes capacity. Each step has delay and error. CPU may be a lagging or misleading signal; queue age, concurrency, arrival forecast, or domain demand may be better. Use minimum and maximum bounds, rate limits, hysteresis, cooldown, and manual authority.

Reactive scaling cannot absorb a burst shorter than provisioning time unless headroom or buffering covers it. Predictive scaling depends on forecast quality. Scheduled scaling handles known events but not surprises. Test signal loss, control-plane outage, quota exhaustion, stuck provisioning, overshoot, oscillation, and safe scale-in.

**Control admission and isolate demand.** Capacity management needs a policy for work beyond the envelope. Bound concurrency and queues, propagate backpressure, shed work, or degrade explicitly. Isolate tenants, priorities, and background jobs so one class cannot consume all capacity. Reserve capacity only when stakeholder consequence justifies it and prevent starvation.

Supplier quotas, connection limits, rate limits, and contractual ceilings are architectural constraints. Cache, batch, queue, or negotiate them; do not discover them only during peak demand.

**Measure work amplification.** Let $U$ be correctly completed external units and $I$ an internal work measure such as calls, bytes, or CPU time. Amplification $I/U$ can rise through retries, fan-out, replication, cache misses, scans, logging, compaction, or reconciliation. A system may appear to need more capacity when the real defect is multiplying work.

**Establish a capacity envelope.** Sweep relevant workload axes and configuration points while measuring correct useful throughput, latency distributions, errors, rejection, fairness, resource saturation, queues, amplification, and cost. Include cold, burst, skew, failure, rollout, rebalance, recovery, and scale-in conditions.

Interpolate cautiously inside tested regions and do not extrapolate across a mechanism change. A result at 100 GB does not prove behavior at 10 TB if indexes no longer fit memory, partitions rebalance, or algorithms change. Record uncertainty and trigger earlier testing as forecasts approach evidence boundaries.

## Definitions and Notation

Let workload class $k$ have useful throughput $X_k$ and average demand $D_{ik}$ on resource $i$. If $C_i>0$ is usable resource capacity in matching units, a first-order utilization estimate is

$$
\rho_i=\frac{\sum_k X_kD_{ik}}{C_i}.
$$

The model requires a stable observation interval and compatible units. A necessary steady-state condition is $\rho_i<1$ for each finite resource, but that does not ensure latency, fairness, or availability objectives.

For current useful capacity $K_0>0$ and scaled capacity $K(s)$ under scale factor $s>0$, define a context-specific efficiency

$$
E(s)=\frac{K(s)}{sK_0}.
$$

$E(s)=1$ is proportional scaling for the declared experiment; $E(s)<1$ exposes overhead or another constraint; $E(s)>1$ may occur through cache, batching, or configuration effects and requires explanation. This is not a universal scalability score.

If maximum intended load is $L$ and only fraction $u_{max}$ of provisioned capacity may be consumed, require $P\ge L/u_{max}$. Define headroom fraction at observed load $L$ and usable provisioned capacity $P>0$ as $h=1-L/P$. Both are scenario estimates, not guarantees.

## Mechanisms, Invariants, or Proof Structure

Use this scalability and capacity mechanism.

1. **Define success:** state useful outcomes, constraints, workload dimensions, configuration, and evidence boundary.
2. **Map demand:** trace each workload class to resource, dependency, state, coordination, quota, and control-plane demand.
3. **Locate constraints:** observe service demand, saturation, queues, skew, amplification, and the current bottleneck.
4. **Reduce work:** remove, cache, batch, coalesce, precompute, or defer work without violating semantics.
5. **Choose scaling:** increase resource size, add cooperating instances, replicate reads, or partition ownership.
6. **Govern transitions:** specify routing, warm-up, epochs, fencing, drain, rebalance, rollback, and reconciliation.
7. **Protect capacity:** reserve scenario-based headroom and isolate tenants, priorities, background work, and failures.
8. **Control demand:** bound admission, concurrency, queues, retry, fan-out, and overload behavior.
9. **Verify envelopes:** test multidimensional steady, burst, skew, cold, failure, change, recovery, and scale-in conditions.
10. **Reforecast:** track demand and evidence uncertainty and retest before crossing a mechanism or capacity boundary.

The governing invariants are correct useful completion, multidimensional workload identity, visible bottlenecks, stable ownership, bounded amplification, honest headroom, controlled transitions, fair overload policy, representative evidence, and no unsupported extrapolation.

## Alternatives and Trade-Offs

**Vertical or horizontal scaling.** Vertical scaling simplifies state and coordination but has size and blast-radius limits. Horizontal scaling expands aggregate resources but adds routing, coordination, state, and operational complexity.

**Replication or partitioning.** Replication helps selected reads and availability but multiplies write and storage work and introduces freshness. Partitioning distributes ownership and writes but adds skew, metadata, fan-out, and rebalance.

**Reactive or predictive elasticity.** Reactive control follows observed demand but may respond too late. Prediction prepares capacity but can waste resources or miss novel events. Both need bounds, evidence, and failure behavior.

**Shared or isolated capacity.** Sharing raises average utilization and statistical multiplexing. Isolation protects tenants and priorities but can strand capacity. Weighted sharing with floors and ceilings can combine them at added policy complexity.

**Headroom or maximum utilization.** Headroom protects bursts, failure, and change but costs money and energy. High nominal utilization reduces idle resources but increases queueing and fragility. Evaluate unit economics against stakeholder consequences.

## Failure Modes and Misconceptions

- **“It handled one million requests.”** Duration, correctness, workload, latency, configuration, and resource limits are missing.
- **“Requests per second is the workload.”** Payload, mix, data, skew, fan-out, geography, and background work also matter.
- **“Average utilization is low.”** A local partition, core, lock, pool, quota, or interval may be exhausted.
- **“Stateless services scale linearly.”** Their stateful dependencies and shared control paths may not.
- **“More replicas add capacity.”** Coordination, replication, and consistency can add more work than capacity.
- **“More partitions remove hotspots.”** A bad key or dominant entity can remain hot.
- **“Autoscaling removes capacity planning.”** Signals, delay, quotas, warm-up, failure, and maximum bounds remain.
- **“The queue is our burst buffer.”** It has finite age, memory, recovery, and stakeholder latency budgets.
- **“Scale-out is only topology.”** Routing, state ownership, compatibility, security, and operations must transition.
- **“Scale-in is harmless.”** In-flight work, leases, sessions, and state can be lost or duplicated.
- **“Headroom is waste.”** It is an explicit risk-control allocation when tied to scenarios.
- **“A benchmark curve predicts the future.”** Mechanism changes and untested workload axes break extrapolation.

## Worked Examples

### Example 1

**Question:** A request consumes 8 ms of one CPU core and the target is 600 correct completions/s. What first-order CPU demand follows?

**Reasoning:** $600\times0.008=4.8$ core-seconds per second. Six ideal cores average $4.8/6=0.8$, or 80%. Variability, per-core skew, other work, failure, and latency objectives require additional evidence and margin.

**Conclusion:** Service demand converts useful throughput into a resource estimate, not a production guarantee.

### Example 2

**Question:** Peak demand needs 800 units/s and policy caps planned utilization at 65%. What usable capacity is required?

**Reasoning:** $P\ge800/0.65\approx1230.77$ units/s, so provision at least 1,231 in matching discrete capacity before other scenario margins. The unused fraction covers the stated utilization policy, not automatically zone loss, rollout, or estimation error.

**Conclusion:** Headroom must be calculated against named scenarios and rounded to deployable units.

### Example 3

**Question:** Eight workers provide 720 correct operations/s; four workers provide 400. What is scale efficiency from four to eight?

**Reasoning:** Baseline $K_0=400$ at scale factor $s=2$. $E(2)=720/(2\times400)=0.9$. The doubled fleet gives 1.8 times capacity, not twice, suggesting coordination, imbalance, or another constraint.

**Conclusion:** Scaling efficiency reveals lost proportionality but does not identify its cause.

### Example 4

**Question:** A workload completes 1,000 external requests/s, each causing 1.2 database calls normally. Retries raise the rate to 2,400 database calls/s. What changed?

**Reasoning:** Database-call amplification rose from $1.2$ to $2.4$ calls per useful completion. Scaling the database treats a symptom; first identify timeout, retry ownership, duplicate work, and failure conditions.

**Conclusion:** Measure internal work per useful outcome before concluding that demand alone requires capacity.

### Example 5

**Question:** A ten-partition system averages 40% utilization, but one partition is at 100%. Is capacity available?

**Reasoning:** The hot partition is the bottleneck for its keys even though fleet average is low. Identify tenant and key distribution, then consider a better key, hot-key subdivision, isolation, replication for safe reads, aggregation, or admission control. Rebalancing unrelated cold keys does not solve the hotspot.

**Conclusion:** Capacity is constrained by local demand and ownership, not fleet averages.

### Example 6

**Question:** An autoscaler provisions in four minutes, while a flash crowd reaches ten times normal demand in thirty seconds. Can reactive scaling alone protect service?

**Reasoning:** No. The demand transition completes long before new capacity becomes usable. Preserve pre-warmed or baseline headroom, forecast known events, bound admission and queues, degrade safely, and reduce provisioning and warm-up delay. Test quota and control-plane failure too.

**Conclusion:** Elasticity response time must be shorter than the demand transition or another mechanism must bridge the gap.

### Example 7

**Question:** Does adding four read replicas provide five times read capacity?

**Reasoning:** Only if routing distributes eligible reads, replica service is the constraint, consistency permits replica answers, primary and network can carry replication, and lag and cache effects stay within objectives. Writes, hot keys, query imbalance, and shared storage can dominate.

**Conclusion:** Replica count is not usable end-to-end capacity.

### Example 8

**Question:** What must hold while a tenant partition moves from node A to node B?

**Reasoning:** Establish a versioned ownership epoch; copy and validate state; route new operations by the agreed cutover; fence stale writes from A; preserve operation identities; handle in-flight and duplicate messages; throttle transfer; observe lag and correctness; retain rollback; and reconcile before deleting the source.

**Conclusion:** Rebalancing is a correctness-sensitive state transition, not merely data copying.

### Example 9

**Question:** A benchmark scales linearly from 10 GB to 100 GB. May architects predict the same curve at 10 TB?

**Reasoning:** No. At 10 TB, indexes may not fit memory, partitions and metadata may multiply, compaction and backup change, queries may fan out, and hardware or algorithms may cross thresholds. Test intermediate logarithmic points and mechanism boundaries with representative distributions.

**Conclusion:** Extrapolation across untested mechanism changes is an assumption, not evidence.

### Example 10

**Question:** How should capacity be designed for a regional emergency-notification system?

**Reasoning:** Model ordinary traffic, localized incidents, regional disasters, multilingual payloads, acknowledgments, retries, carrier quotas, network loss, geographic skew, operator actions, and recovery. Prioritize by authorized consequence, prevent one region or channel from exhausting all capacity, reserve disaster headroom, and test cold alternate routes and manual control. No external emergency-management, telecommunications, accessibility, regulatory, security, human-factors, or practitioner review is claimed; named qualified authorities must validate demand scenarios, policies, evidence, release, and residual risk.

**Conclusion:** High-consequence capacity must preserve authorized useful delivery under correlated demand and failure, not maximize nominal message rate.

## Cross-Program Connections

- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) owns advanced scale mechanisms and production-scale data-system behavior.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) owns resource scheduling, memory, I/O, process, and contention mechanisms.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) owns bandwidth, congestion, transport, and network capacity.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects demand, physical capacity, hazards, suppliers, operators, and lifecycle planning.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns partitioning, replication, consistency, membership, and distributed coordination algorithms.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) operates shared capacity, tenancy, quotas, scheduling, and paved-road controls.
- [Cloud & Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) owns provider-specific elastic infrastructure and cost mechanisms.

## References

1. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*, fourth edition, Addison-Wesley, 2021. Performance and availability scenarios, resource tactics, and architectural trade-offs.
2. André B. Bondi. “Characteristics of Scalability and Their Impact on Performance.” *Proceedings of the Second International Workshop on Software and Performance*, ACM, 2000. Scalability terminology, load and structural dimensions, and evaluation concerns.
3. Neil J. Gunther. *Guerrilla Capacity Planning*, Springer, 2007. Capacity models, bottleneck analysis, scalability, and measurement.
4. Raj Jain. *The Art of Computer Systems Performance Analysis*. Wiley, 1991. Workloads, metrics, bottlenecks, experimental design, and queueing foundations.
5. Mor Harchol-Balter. *Performance Modeling and Design of Computer Systems: Queueing Theory in Action*. Cambridge University Press, 2013. Resource demand, queueing, scheduling, and capacity reasoning.
6. Martin Kleppmann. *Designing Data-Intensive Applications*, O'Reilly, 2017. Partitioning, replication, skew, rebalancing, distributed data, and failure trade-offs.
7. Betsy Beyer et al., editors. [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/table-of-contents/), O'Reilly, 2016. Load balancing, overload, cascading failure, capacity planning, and production evidence; consulted 2026-09-05.
8. Betsy Beyer et al., editors. [The Site Reliability Workbook](https://sre.google/workbook/table-of-contents/), O'Reilly, 2018. Implementing SLOs, load balancing, overload protection, and operational control; consulted 2026-09-05.

## Exercises

### Exercise 1

Define capacity and scalability for a collaborative document service without reducing workload to requests per second.

### Exercise 2

Three workload classes complete at 200, 100, and 50 operations/s and require 2, 5, and 8 ms of CPU respectively. Estimate CPU demand and utilization on two usable cores.

### Exercise 3

Diagnose a system with twenty stateless workers, one database writer, uniform test keys, unbounded queues, rapid retry, 70% average CPU, five-minute autoscaling, and no scale-in test.

### Exercise 4

Compare vertical scaling, read replication, and key partitioning for a growing catalog service. Address workload fit, state, consistency, transitions, failure, cost, and evidence.

### Exercise 5

Design capacity assurance for an unfamiliar national vaccine-appointment service. Separate workload evidence, architectural controls, operational exercises, qualified authority, and blockers.

## Answers to the Exercises

### Answer 1

Define useful outcomes such as correctly authorized document open, edit acceptance, durable synchronization, collaborator update, search, export, and recovery. Workload axes include active documents, concurrent editors per document, operation rate, operation and document size, history length, read/write mix, hot-document skew, tenants, geography, presence updates, offline reconciliation, attachments, search scope, and background indexing.

Capacity is the largest declared workload region a fixed configuration sustains while latency percentiles, durability, convergence or consistency, authorization, availability, fairness, cost, and rejection bounds hold. Scalability is how those outcomes and required resources change as each workload axis and configuration changes. Publish topology, versions, data distribution, cache state, duration, failures, maintenance, and evidence uncertainty.

### Answer 2

Total CPU demand per second is

$$
200(0.002)+100(0.005)+50(0.008)=0.4+0.5+0.4=1.3
$$

core-seconds per second. On two usable cores, first-order average utilization is $1.3/2=0.65$, or 65%. This estimate assumes the class demands and rates share the same boundary and stable interval. It does not establish per-core balance, queueing, tail latency, memory or I/O capacity, failure headroom, or correctness. Measure the complete outcome envelope.

### Answer 3

The stateless tier can outgrow its single writer and connection limit; more workers may increase contention. Uniform keys hide tenant and key hotspots. Unbounded queues turn overload into latency and long recovery. Rapid retries amplify database and network work. Average CPU hides local saturation. Five-minute provisioning cannot cover shorter demand transitions without headroom or load control. Untested scale-in risks dropping in-flight work, sessions, leases, or routing state.

Define multidimensional workload classes and correct outcomes. Measure writer demand, pools, locks, queues, per-key and tenant skew, retries, useful throughput, tail latency, and quotas. Bound admission, queues, concurrency, fan-out, and retry. Evaluate write partitioning or domain decomposition only with authority and transition invariants. Add scenario headroom, predictive or scheduled preparation where justified, warm-up evidence, controlled draining, fencing, reconciliation, and scale-in and recovery tests.

### Answer 4

Vertical scaling increases CPU, memory, or I/O with minimal distribution complexity and may fit moderate growth, but has size, cost, maintenance, and blast-radius limits. Read replicas distribute eligible reads and locality, but add replication work and require lag, consistency, routing, failure, and promotion semantics; they do not scale the writer. Key partitioning can distribute reads and writes, but requires a key that spreads real demand, explicit ownership, bounded fan-out, metadata, rebalancing, fencing, and hotspot handling.

Characterize operation mix, data and result size, write ratio, query fan-out, key and tenant skew, growth, geography, and availability. Test each configuration under steady, burst, hot-key, cold, failure, rollout, rebalance, recovery, and scale-in conditions. Measure correct useful throughput, distributions, freshness, resource demand, amplification, fairness, and cost. Choose the simplest tactic whose measured envelope and transition behavior meet the scenarios; combinations remain possible but compound complexity.

### Answer 5

Model ordinary booking, eligibility windows, campaign openings, regional outbreaks, multilingual access, accessibility needs, household and provider workflows, appointment inventory, identity dependencies, cancellations, reminders, malicious traffic, retries, geographic and cohort skew, supplier quotas, and recovery. Capacity success includes correct eligibility and inventory authority, fairness, bounded latency, availability, privacy, and safe rejection—not raw HTTP throughput.

Architect bounded admission and queues, stable operation identity, regional and cohort isolation where policy permits, hot-inventory protection, read caching with authorization and freshness, scenario headroom, controlled retry, degradation, explicit supplier quotas, and tested scale transitions. Automated evidence can cover workload generation, invariants, distributions, queues, saturation, skew, amplification, quotas, and recovery. Operational exercises can cover campaign opening, region loss, identity outage, cold capacity, reconciliation, scale-in, and manual authority. No external public-health, clinical, equity, accessibility, privacy, security, regulatory, operations, or practitioner review is claimed. Named qualified authorities must own eligibility, allocation and fairness policy, demand scenarios, hazards, validation, release, and residual risk. Ambiguous inventory authority, discriminatory overload policy, unverified peak demand, unsafe duplicate booking, failed recovery, or unresolved high-severity risk blocks readiness.
