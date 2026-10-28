---
module_id: SARCH-067
program: Software Engineering: Software Architecture
level: 2
module_number: 67
title: Availability and Reliability Models
status: complete
last_verified: 2026-09-06
---

# Availability and Reliability Models

## One-Page Review

### Governing question

How can an architect represent failure, continued service, repair, redundancy, and common causes precisely enough to make a defensible availability or reliability decision without turning uncertain assumptions into false assurance?

### Essential definitions

- a **fault** is an adjudged or hypothesized cause; an **error** is an incorrect internal state; a **failure** occurs when delivered service deviates from its specification at the system boundary;
- **reliability** $R(t)$ is the probability of failure-free service over a declared mission interval, conditional on initial state, workload, environment, and failure definition;
- **availability** $A(t)$ is the probability that required service is usable at a stated time; long-run availability is the fraction of a suitable observation scope in an up state;
- **maintainability** concerns the ability and time to restore or modify service under stated procedures and resources;
- **hazard rate** describes instantaneous failure propensity conditional on survival, not a universal constant;
- **coverage** is the probability that detection, isolation, switching, and recovery succeed given the modeled fault;
- a **common-cause failure** defeats supposedly separate elements through a shared cause or dependency;
- an **error budget** is the permitted amount of an explicitly defined unreliable outcome during a window;
- **durability** concerns preservation of data over time; it is not service availability;
- a **fault tree** relates an undesired top event to contributing events through logical and, in dynamic variants, order-dependent structure.

### Central model, mechanism, or theorem

For a simple alternating up/down process with finite mean time to failure $MTTF$ and mean time to restore $MTTR$, steady-state availability is

$$
A=\frac{MTTF}{MTTF+MTTR}.
$$

For independent components all required in series, $A_s=\prod_i A_i$. For independent redundant alternatives where any one suffices, $A_p=1-\prod_i(1-A_i)$. These expressions are conditional on boundary, state semantics, independence, repair interaction, and coverage. Shared identity, software, power, network, operator, control, or recovery dependencies often invalidate the easy parallel product.

### Critical invariants

- service and failure are defined from the relevant consumer or mission boundary;
- reliability, availability, maintainability, durability, safety, integrity, and security remain distinct;
- time-, request-, session-, object-, and business-outcome measures are not silently mixed;
- every probability names population, interval, conditions, estimator, and uncertainty;
- series/parallel arithmetic never assumes independence without evidence;
- failover includes detection, isolation, decision, state, switch, and recovery coverage;
- degraded service counts as success only for the outcomes it actually preserves;
- redundancy includes common dependencies and repair-resource contention;
- missing telemetry and unobserved demand do not count as success;
- experiments and incidents update, but do not certify, the model.

### Common failures

Common failures include calling uptime reliability; converting a request SLI directly into outage minutes; multiplying component dashboards with different windows; interpreting MTBF as a guarantee; fitting a constant hazard to every lifecycle; assuming zones, regions, clouds, or vendors are independent; ignoring shared software and control planes; treating automatic failover as perfect coverage; counting slow, stale, duplicate, unsafe, or incorrect responses as available; averaging away critical cohorts; using redundancy without repair capacity; and claiming zero observed failures proves zero risk.

### Compact example

A service target of 99.95% time availability over a declared 30-day window permits $0.0005\cdot30\cdot24\cdot60=21.6$ unavailable minutes. That translation is valid only for a time-based binary SLI with the same window. It does not translate a request-success target, prove recoverability, or authorize 21.6 unsafe minutes.

### Connections

[SARCH-066](066-performance-and-capacity-models.md) supplies workload and capacity states that shape failure. [SARCH-068](../ROADMAP.md) next treats architecture-scale threats. Reliability Engineering owns deeper stochastic estimation and assurance methods; this module owns architectural composition, coverage, and decision boundaries.

## Governing Question

Availability and reliability are claims about service at a boundary, under conditions, over time. They are not properties produced automatically by adding replicas. An architecture must explain what can fail, which outcomes remain acceptable, how the system detects and responds, what dependencies remain shared, and how the quantitative model is tied to evidence.

The purpose of a model is not to manufacture a string of nines. It is to reveal sensitive assumptions, compare mechanisms, allocate responsibility, design tests, and bound residual risk.

## Why This Matters

Systems can be frequently repaired yet fail almost every long mission; they can remain technically reachable while returning corrupt answers; they can preserve data while an application is unavailable; they can satisfy a global request ratio while abandoning one region or accessibility path. Imprecise aggregation hides these distinctions.

Redundancy also creates mechanisms: replication, detection, quorum, state transfer, routing, fencing, repair, and reintegration. Each mechanism introduces dependencies and failure modes. Quantitative reasoning helps only when the structure matches the real architecture and when uncertainty is visible.

## Prerequisites and Retrieval

Retrieve probability, conditional probability, survival function, distribution, expectation, independence, correlation, confidence interval, state machine, Markov property, rate, steady state, series and parallel composition, quorum, replication, failover, timeout, retry, fault containment, error budget, recovery point, recovery time, and quality-attribute scenario.

From SARCH-051 through SARCH-060 retrieve distributed failure, resilience, recovery, and multi-region mechanisms. SARCH-061 through SARCH-066 supply scenario, risk, fitness-function, dependency, and capacity analysis. This chapter does not replace reliability statistics, safety engineering, security engineering, or domain certification.

## Learning Objectives

After completing this module, you should be able to:

1. define fault, error, failure, reliability, availability, maintainability, and durability at explicit boundaries;
2. distinguish mission reliability from repairable steady-state availability;
3. construct time-, request-, session-, object-, and outcome-based indicators without invalid conversion;
4. apply exponential survival, repair availability, series/parallel, and k-of-n models with stated assumptions;
5. build fault-tree and state-transition representations for architectural mechanisms;
6. include detection, isolation, switchover, state, and repair coverage;
7. identify common-cause, correlated, dependency, and repair-contention failures;
8. represent degraded modes and data integrity separately from reachability;
9. calibrate and challenge rare-event estimates with incidents and fault experiments;
10. make a bounded architecture decision with owners, uncertainty, and residual risk.

## Core Exposition

**Define delivered service.** A failure exists relative to a specification at a boundary. For a search user, excessive latency or inaccessible results may be failure even when servers return status 200. For a payment ledger, duplicate application or wrong balance is failure even if the endpoint responds quickly. For a controller, an unsafe command is not “available service.”

Name actor, operation, success criteria, latency or freshness limit, data and authorization correctness, geography, workload, and excluded states. Different outcomes need different models rather than one blended availability number.

**Trace fault, error, and failure.** A latent software defect, exhausted certificate, operator action, compromised credential, damaged cable, or environmental disturbance may be a fault. Activation creates an erroneous state. Containment, detection, correction, or masking may prevent the error from reaching the service boundary; propagation produces failure [1].

The chain is not deterministic. The same fault may remain dormant, be tolerated, or produce different failures under different workload and state. Model activation and propagation conditions rather than equating defect count with failure rate.

**Separate dependability attributes.** Reliability concerns continuity over an interval. Availability concerns readiness at a time or fraction of a scope. Maintainability concerns restoration and change. Data durability concerns preservation. Safety concerns unacceptable harm; integrity concerns improper alteration; confidentiality concerns disclosure.

Improving one may worsen another. Aggressive failover may improve reachability but risk split-brain writes. A safe controller may deliberately stop. A durable queue may preserve work while missing its deadline. Architecture decisions retain every material attribute.

**Specify the indicator.** Time availability labels each eligible interval up or down. Request availability counts eligible good events over eligible valid events. Session or journey availability requires a whole sequence. Object durability asks whether each committed object remains recoverable. Business availability may require inventory, authorization, fulfillment, and reconciliation.

Define eligibility, synthetic versus real traffic, sampling, missing data, low-volume periods, retries, client cancellation, partial response, planned maintenance, and window. A request ratio cannot be converted to minutes without an arrival distribution and a time-based interpretation.

**Model mission reliability.** Let $T$ be time to first defined failure. Reliability is the survival function $R(t)=P(T>t)$. With a constant hazard $\lambda$, the exponential model gives

$$
R(t)=e^{-\lambda t},\qquad MTTF=\frac{1}{\lambda}.
$$

Constant hazard is an assumption. Software activation, infant mortality, wear, maintenance, learning, workload, and environmental cycles can make hazard time- or state-dependent. Use empirical or physics-informed distributions when appropriate.

**Model repairable availability.** In a simple alternating renewal model, $A=MTTF/(MTTF+MTTR)$. Restoration includes detection, diagnosis, authorization, repair, validation, state reconciliation, warm-up, and return to useful capacity—not merely process restart.

The mean ratio does not describe outage count, tail duration, customer concentration, or catastrophic modes. Two services can have equal availability with many brief interruptions or one long outage and require different architecture.

**Compose static structures carefully.** A series model requires every component for success; independent availability multiplies. A parallel model succeeds if any alternative succeeds; independent unavailability multiplies. A k-of-n system succeeds when at least $k$ of $n$ elements succeed:

$$
R_{k|n}=\sum_{i=k}^{n}{n\choose i}r^i(1-r)^{n-i}
$$

for identical independent element reliability $r$ over the mission. Load, repair, switching, state, and shared dependencies can violate every simplifying adjective in that sentence.

**Challenge independence.** Separate repositories or regions do not establish probabilistic independence. Look for common software, image, configuration, schema, identity, DNS, network, power, facility, provider, supplier, pipeline, operator, clock, and recovery resources. Correlated demand can activate identical defects simultaneously.

Model common causes explicitly as events or shared nodes. When evidence cannot estimate dependence, analyze plausible bounds and adversarial scenarios instead of selecting zero correlation for convenience.

**Represent logical causes.** Fault trees work backward from a top event through AND and OR gates to contributing events. Minimal cut sets reveal combinations sufficient for failure. OR probability is not a simple sum unless events are disjoint; inclusion-exclusion or a joint model is required.

Static trees struggle with order, standby, coverage, repair, and feedback. Dynamic fault trees, state machines, Markov or semi-Markov models, stochastic Petri nets, simulation, or explicit scenario analysis may represent these mechanisms. Complexity must earn validation value.

**Represent state and time.** A continuous-time Markov chain assigns transition rates between states such as healthy, degraded, failed, and repairing. It can calculate transient mission behavior and steady-state occupancy when exponential transition and Markov assumptions fit. Semi-Markov or simulation approaches support richer holding times.

State explosion and poorly identified rates can make an elaborate model less credible. Aggregate only states that preserve the decision-relevant behavior, and validate transition evidence.

**Include coverage.** Redundancy helps only if the system detects the relevant fault, isolates the right element, prevents stale or conflicting authority, routes work, has compatible state, and survives the transition. Coverage $c$ conditions the branch in which that sequence succeeds.

Measure false positives, false negatives, detection delay, fencing, switchover, state loss, cold capacity, retry surge, and reintegration. “Automatic” describes an implementation trigger, not a success probability of one.

**Include repair systems.** Repairs compete for operators, spares, network, build systems, credentials, and physical access. Multiple failures can create a repair queue. A design with redundant units but one fragile repair authority may have poor long-duration availability.

Model detection-to-restore distributions, not only a mean. Exercise simultaneous faults, unavailable experts, lost tooling, bad replacement, rollback, and recurrence. Maintenance and deployment are intentional state transitions with reliability consequences.

**Model degraded service.** Define an outcome vector rather than one up/down bit when partial operation matters: read, write, search, purchase, administer, recover, audit, or actuate. A degraded mode is successful only for dimensions whose requirements it meets.

Avoid hiding harm in a weighted composite. Report critical cohorts and functions separately. Product and domain authorities decide which degradation is acceptable; engineering metrics do not grant that permission.

**Distinguish data durability.** Replication count is not durability. Correlated deletion, software defects, administrative authority, encryption-key loss, silent corruption, retention policy, legal deletion, and untested restore cross replicas. Durability models need object boundary, time horizon, fault set, detection, repair, and verifiable restore.

Availability may be restored from stale state while correctness is not. Track recovery point, reconciliation, duplicate or lost effects, and authoritative history independently from endpoint reachability.

**Use budgets as control.** An SLO and indicator define permitted unreliable outcomes in a window. Time-based targets yield time budgets; request-based targets yield event budgets. Budget policy governs release, risk, and remediation but does not make each failure interchangeable.

Protect safety, security, legal, contractual, and catastrophic constraints separately. A remaining aggregate budget does not authorize a forbidden event or concentration on one tenant.

**Estimate with uncertainty.** Rare failures provide sparse data. Report exposure, censoring, definition changes, confidence, and model sensitivity. Zero observed failures produces an upper bound under assumptions; it never proves probability zero.

Incident data is biased by detection and reporting. Synthetic probes miss some journeys; production traffic may miss dormant recovery paths. Combine operational observation, structural analysis, historical evidence, fault injection, recovery exercises, and domain review.

**Test the mechanism.** Test detection, masking, failover, state continuity, capacity after loss, repair, reintegration, and repeated faults. Vary timing and combinations. Confirm both service indicators and correctness invariants during and after disturbance.

Fault injection supports causal evidence within the tested environment. It does not establish completeness of the fault model. Stop conditions, blast-radius controls, rollback, observation, and authorized scope are part of the experiment.

**Govern the model.** Record model version, boundary, top events, states, distributions, dependencies, data, estimators, uncertainty, sensitivity, validation, owners, decisions, and refresh triggers. Link assumptions to architecture decisions and tests.

Refresh after workload, topology, provider, software, dependency, repair, telemetry, SLO, threat, or operational-policy change. Reliability evidence decays when the system changes.

## Definitions and Notation

For a declared service and environment:

- $T$ is time to first defined failure;
- $R(t)=P(T>t)$ is mission reliability;
- $h(t)$ is hazard conditional on survival to time $t$;
- $A(t)=P(\text{service usable at }t)$ is point availability;
- $MTTF$ is mean operating time from restoration or start to failure;
- $MTTR$ is mean time from failure to restored useful service under declared procedure;
- $Q=1-A$ is unavailability for a binary availability model;
- $c$ is conditional coverage of a declared detection and recovery sequence;
- $r$ is one element's mission reliability in a declared k-of-n model;
- a **cut set** is a set of basic events whose joint occurrence causes the fault-tree top event;
- a **common cause** is one cause capable of affecting multiple nominally redundant elements;
- **residual risk** is risk remaining after accepted controls and evidence.

Probabilities cannot be composed solely because their labels use the same number of nines. Population, time horizon, conditional state, failure definition, and dependence must agree.

## Mechanisms, Invariants, or Proof Structure

### Modeling and validation procedure

1. Define consumer, mission, service boundary, success, failure, and unacceptable outcomes.
2. Select time, request, session, object, or business indicators and windows.
3. Map faults, error propagation, dependencies, common causes, and top events.
4. Represent healthy, degraded, failed, repair, and reintegration states.
5. Choose series, parallel, k-of-n, fault-tree, state, simulation, or scenario models whose assumptions can be checked.
6. Estimate failure, coverage, repair, and transition behavior with uncertainty.
7. Calculate mission, steady, failure, maintenance, recovery, and correlated scenarios.
8. Validate with independent operational data, fault experiments, and recovery exercises.
9. Review safety, security, integrity, durability, accessibility, legal, and stakeholder consequences separately.
10. Decide controls, safe operating envelope, residual risk, owners, and refresh triggers.

### Executable composition calculation

This calculation checks arithmetic under explicit binary and independence assumptions. It does not show that real components, requests, or failure domains are independent.

<!-- bijux-verify: {"id":"availability-composition","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"series=0.9985005\nindependent parallel=0.9999990\n30-day budget minutes=21.6\n","stderr":""}} -->
```python
first = 0.999
second = 0.9995
series = first * second
parallel = 1 - (1 - first) ** 2
budget_minutes = (1 - 0.9995) * 30 * 24 * 60

print(f"series={series:.7f}")
print(f"independent parallel={parallel:.7f}")
print(f"30-day budget minutes={budget_minutes:.1f}")
```

### Invariants

- success and failure are judged at the declared service boundary;
- every estimator uses compatible eligible population and observation window;
- repairable availability is not substituted for mission reliability;
- independence, identical distribution, constant hazard, stationarity, and perfect coverage are never implicit;
- correlated and common-cause events remain in the model;
- degraded success preserves every named invariant for that outcome;
- restore includes state validation and usable capacity;
- no evidence gap, missing signal, or untested failover is recorded as success.

## Alternatives and Trade-Offs

- **Mission reliability versus steady availability:** reliability protects uninterrupted missions; steady availability credits repair and can hide interruption frequency.
- **Time versus request indicator:** time measures service state; request ratios weight by traffic and can hide quiet outages or busy-period concentration.
- **Binary versus multidimensional service state:** binary indicators simplify budgets; vectors preserve partial function and critical cohorts.
- **Static fault tree versus state model:** trees expose causal combinations; state models represent order, repair, and transition timing.
- **Analytical model versus simulation:** analysis exposes structure and sensitivity; simulation handles richer dependence but adds implementation uncertainty.
- **Active-active versus active-standby:** active-active exercises capacity continuously; standby can reduce interference but adds dormant failure and switch risk.
- **Synchronous consistency versus availability:** stronger coordination can protect invariants while refusing operations during partitions; weaker coordination may preserve access with reconciliation cost.
- **More replicas versus more diversity:** replicas tolerate isolated loss; diversity may reduce common software faults but adds complexity and divergent failure.
- **Fast failover versus careful fencing:** speed reduces interruption; inadequate authority control risks split brain and corruption.
- **Automatic versus human recovery:** automation is fast and repeatable; humans handle novelty but add delay, load, and coordination variance.
- **Local autonomy versus central control:** autonomy survives disconnection; central authority simplifies policy and may become a common cause.
- **Error budget versus categorical constraint:** budgets govern aggregate unreliability; safety, security, and integrity prohibitions require separate constraints.

## Failure Modes and Misconceptions

1. **“Reliability means uptime.”** Reliability is continuity over a mission; repairable availability can be high despite frequent interruption.
2. **“A process is available if it answers.”** Late, stale, unauthorized, duplicate, corrupt, or inaccessible service may be failure.
3. **“Request nines equal downtime minutes.”** The conversion is invalid without a time-based binary indicator and matching window.
4. **“Component nines multiply automatically.”** Boundaries, populations, windows, conditional states, and dependence must match.
5. **“Replicas are independent.”** Software, configuration, load, infrastructure, operators, and recovery are common causes.
6. **“A region is a failure domain.”** It may share global identity, DNS, control, artifacts, network, data, or provider authority.
7. **“Automatic failover has perfect coverage.”** Detection, isolation, fencing, routing, state, capacity, and reintegration can fail.
8. **“MTBF is an outage schedule.”** A mean neither predicts the next failure nor defines a distribution.
9. **“Failure rate is constant.”** Lifecycle, workload, activation, wear, repair, and learning may change hazard.
10. **“Parallel redundancy always helps.”** Added coordination, state, repair, and common dependencies can reduce service quality.
11. **“Failover capacity was tested because health checks passed.”** Surviving useful workload and correctness must be exercised.
12. **“A degraded response is success.”** Only explicitly preserved outcomes may count as successful.
13. **“Replication proves durability.”** Shared deletion, corruption, authority, key loss, and restore failure cross replicas.
14. **“Zero failures proves reliability.”** It supplies limited statistical evidence under an exposure and model.
15. **“One global SLI is fair.”** It can hide regional, tenant, operation, and accessibility failures.
16. **“More detailed models are more credible.”** Unidentified rates and unvalidated states create decorative precision.
17. **“Fault injection proves completeness.”** It validates selected mechanisms against selected faults in one environment.
18. **“Remaining error budget authorizes any outage.”** Catastrophic, unsafe, illegal, or concentrated harm remains constrained.

## Worked Examples

### Example 1

**Distinguish reliability from availability.**

**Situation.** Under an illustrative exponential failure model, a device has $MTTF=10$ hours and $MTTR=1$ minute.

**Reasoning.** Repair availability is $10/(10+1/60)\approx0.99834$. Yet reliability for one uninterrupted eight-hour mission is $e^{-8/10}=e^{-0.8}\approx0.4493$. Rapid repair produces high long-run availability but cannot rescue a mission after its first failure.

**Conclusion.** Availability and mission reliability answer different questions and can diverge sharply.

### Example 2

**Translate a time-based error budget.**

**Situation.** A binary time-availability target is 99.95% over a declared 30-day window.

**Reasoning.** The window contains $30\cdot24\cdot60=43{,}200$ minutes. Permitted unavailability is $0.0005(43{,}200)=21.6$ minutes. If the indicator instead counts requests, the budget is failed eligible events and no direct minute conversion follows.

**Conclusion.** The 21.6-minute budget is valid only for the stated time indicator and window.

### Example 3

**Compose a series path.**

**Situation.** A request needs two independent binary components with availabilities 0.999 and 0.9995 over the same scope.

**Reasoning.** Series availability is $0.999(0.9995)=0.9985005$. Over a 30-day time model, expected unavailable fraction corresponds to about $0.0014995(43{,}200)=64.78$ minutes. This arithmetic fails if outages correlate, scopes differ, or fallback bypasses one component.

**Conclusion.** A path can have worse availability than either required component, conditional on the model.

### Example 4

**Expose a common cause in parallel.**

**Situation.** Two replicas each have conditional availability 0.99, but both require one control dependency with availability 0.995.

**Reasoning.** If replicas are mutually independent conditional on the control dependency, their parallel availability is $1-0.01^2=0.9999$. End-to-end availability is $0.995(0.9999)=0.9949005$, not 0.9999. The shared dependency dominates and even makes this modeled service less available than one isolated 0.99 element would be.

**Conclusion.** Parallel products must include common required dependencies.

### Example 5

**Compute a k-of-n mission.**

**Situation.** A mission succeeds when at least two of three identical independent elements survive; each has mission reliability 0.98.

**Reasoning.** Exactly two survive with probability ${3\choose2}(0.98)^2(0.02)=0.057624$. All three survive with $0.98^3=0.941192$. Total mission reliability is 0.998816. Voting logic, common causes, coverage, and unequal loads are outside this simple value.

**Conclusion.** Two-of-three redundancy raises modeled reliability only under the stated assumptions.

### Example 6

**Interpret constant hazard.**

**Situation.** A component is modeled with constant hazard $\lambda=2\times10^{-5}$ per hour for a 1,000-hour mission.

**Reasoning.** $R(1000)=e^{-0.02}\approx0.98020$. The common approximation $1-\lambda t=0.98$ is close because $\lambda t$ is small, but it is not the exact exponential result. Neither applies if hazard changes with age, workload, or environment.

**Conclusion.** Exponential reliability is a conditional model, and even simple approximations retain a range.

### Example 7

**Compare prevention with faster repair.**

**Situation.** A repairable service has $MTTF=720$ hours and $MTTR=2$ hours.

**Reasoning.** Availability is $720/722\approx0.99723$. Cutting restoration to 0.5 hour gives $720/720.5\approx0.99931$. Doubling MTTF while retaining two-hour restoration gives $1440/1442\approx0.99861$. Faster repair improves this availability ratio more, but it does not improve uninterrupted mission reliability before failure as prevention does.

**Conclusion.** The preferred intervention depends on whether interruption, continuity, or both govern the scenario.

### Example 8

**Calculate an OR gate correctly.**

**Situation.** A top event occurs if independent event $A$ with probability 0.01 or event $B$ with probability 0.02 occurs during a mission.

**Reasoning.** Inclusion-exclusion gives $P(A\cup B)=0.01+0.02-(0.01)(0.02)=0.0298$. Simply adding produces 0.03 by double-counting joint occurrence. With dependence, the intersection needs joint evidence rather than multiplication.

**Conclusion.** Even a basic fault-tree OR gate requires explicit overlap assumptions.

### Example 9

**Include recovery coverage.**

**Situation.** Ten relevant failures occur in a month. Failover succeeds with conditional coverage 0.9 and interrupts service one minute; uncovered cases take 60 minutes to restore.

**Reasoning.** Expected interruption under this simplified nonoverlap model is $10[0.9(1)+0.1(60)]=69$ minutes. Approximate time availability in 43,200 minutes is $1-69/43{,}200\approx0.99840$. Treating redundant hardware as perfectly covered would predict only ten minutes.

**Conclusion.** Detection and recovery coverage can dominate redundancy benefit.

### Example 10

**Interpret zero observed failures.**

**Situation.** A recovery mechanism succeeds in 300 independent representative trials with zero observed failures.

**Reasoning.** The approximate rule of three gives a one-sided 95% upper failure-probability bound of $3/300=0.01$ under Bernoulli, independence, representativeness, and no censoring assumptions. It does not establish perfect coverage, and it says little about untested fault combinations.

**Conclusion.** Zero failures is evidence with a finite bound, not proof of zero risk.

## Cross-Program Connections

- **Systems Engineering:** owns system assurance, hazard, lifecycle, physical, human, supplier, and mission reliability boundaries.
- **Distributed Systems Engineering:** owns failure models, replication, consensus, partition behavior, and distributed recovery mechanisms.
- **Large-Scale Distributed Systems:** owns fleet, cell, region, control-plane, storage, and correlated operational failure.
- **Operating Systems:** owns process, kernel, storage, scheduling, isolation, and crash-recovery behavior.
- **Networking:** owns link, routing, congestion, partition, and protocol failure modes.
- **Database Engineering:** owns transactional integrity, recovery, replication, backup, restore, and data correctness.
- **Security Engineering:** owns adversarial fault, compromise, confidentiality, integrity, and security recovery.
- **Software Delivery and Reliability Engineering:** owns SLO operations, error budgets, incidents, change risk, and production reliability practice.
- **Platform Engineering:** owns shared identity, routing, deployment, quota, observability, and recovery dependencies.
- **Testing and Quality Engineering:** owns statistical test design, fault injection, coverage evidence, and oracle quality.
- **Reliability and safety specialists:** retain domain-specific quantitative assurance and acceptance authority; this module does not certify a system.

## References

1. Algirdas Avižienis, Jean-Claude Laprie, Brian Randell, and Carl Landwehr, “Basic Concepts and Taxonomy of Dependable and Secure Computing,” *IEEE Transactions on Dependable and Secure Computing* 1(1), 2004. <https://doi.org/10.1109/TDSC.2004.2>
2. Marvin Rausand and Arnljot Høyland, *System Reliability Theory: Models, Statistical Methods, and Applications*, 2nd ed., Wiley, 2004.
3. Kishor S. Trivedi, *Probability and Statistics with Reliability, Queuing, and Computer Science Applications*, 2nd ed., Wiley, 2002.
4. Joanne Bechta Dugan, Salvatore J. Bavuso, and Mark A. Boyd, “Dynamic Fault-Tree Models for Fault-Tolerant Computer Systems,” *IEEE Transactions on Reliability* 41(3), 1992. <https://doi.org/10.1109/24.159800>
5. W. E. Vesely, F. F. Goldberg, N. H. Roberts, and D. F. Haasl, *Fault Tree Handbook*, NUREG-0492, U.S. Nuclear Regulatory Commission, 1981. <https://www.nrc.gov/reading-rm/doc-collections/nuregs/staff/sr0492/index>
6. Betsy Beyer, Chris Jones, Jennifer Petoff, and Niall Richard Murphy, eds., *Site Reliability Engineering*, O'Reilly Media, 2016. <https://sre.google/sre-book/table-of-contents/>
7. Steven Thurgood and David Ferguson, with Alex Hidalgo and Betsy Beyer, “Implementing SLOs,” in *The Site Reliability Workbook*, O'Reilly Media, 2018. <https://sre.google/workbook/implementing-slos/>
8. ISO/IEC 25010:2023, *Systems and software engineering—Systems and software Quality Requirements and Evaluation (SQuaRE)—Product quality model*, 2nd ed., November 2023. <https://www.iso.org/standard/78176.html>
9. Ron Ross et al., *Developing Cyber-Resilient Systems: A Systems Security Engineering Approach*, NIST SP 800-160 Vol. 2 Rev. 1, December 2021. <https://doi.org/10.6028/NIST.SP.800-160v2r1>
10. Michael T. Nygard, *Release It! Design and Deploy Production-Ready Software*, 2nd ed., Pragmatic Bookshelf, 2018.

## Exercises

### Exercise 1

Define fault, error, failure, reliability, availability, maintainability, durability, hazard rate, MTTF, MTTR, coverage, cut set, common cause, degraded mode, and error budget. Explain why a successful HTTP response may still be a service failure.

### Exercise 2

Two independent services are both required. Each has $MTTF=500$ hours and $MTTR=1$ hour under the same alternating model. Compute each steady-state availability, the series availability, and corresponding expected unavailable time in a 30-day time model. State the assumptions and limitations.

### Exercise 3

Diagnose an architecture report that multiplies vendor nines from different windows, assumes zones and failover are independent, treats missing probes as success, reports MTBF without a distribution, excludes deployment and repair, and counts stale read-only mode as fully available. Design corrected evidence.

### Exercise 4

Compare active-active, active-standby, quorum, local autonomous, and restore-from-backup designs for a regional account service. Address consistency, coverage, common causes, repair resources, capacity after loss, recovery point, and degraded operations.

### Exercise 5

Design availability and reliability models for a remote medical-device monitoring system with wearable sensors, a phone gateway, intermittent networks, cloud ingestion, alert rules, clinician consoles, operator escalation, firmware updates, battery limits, privacy, and a requirement that loss of monitoring must never be reported as healthy. Cover service boundaries, missions, states, fault trees, dependence, coverage, experiments, uncertainty, ownership, and residual risk without claiming clinical or regulatory certification.

## Answers to the Exercises

### Answer 1

A **fault** is an adjudged or hypothesized cause, an **error** is an incorrect internal state, and a **failure** is delivered service deviating from specification at its boundary. **Reliability** is failure-free probability over a mission; **availability** is usable-service probability at a time or fraction of a scope; **maintainability** concerns restoration and modification; **durability** concerns retained data. **Hazard** is instantaneous failure propensity conditional on survival. **MTTF** is mean operating time to failure; **MTTR** is mean time to restored useful service.

**Coverage** is conditional success of detection and recovery. A **cut set** suffices for a fault-tree top event. A **common cause** can affect multiple nominally redundant elements. A **degraded mode** preserves a declared subset of outcomes. An **error budget** permits defined unreliable outcomes in a window. HTTP 200 can still be failure if content is late, stale, incorrect, unauthorized, inaccessible, incomplete, duplicated, or unsafe relative to the service specification.

### Answer 2

Each service has $A=500/(500+1)=500/501\approx0.998004$. Under independence and identical binary time scopes, series availability is $(500/501)^2\approx0.996012$. Its unavailable fraction is about 0.003988; over 43,200 minutes that is about 172.28 minutes, or 2.87 hours.

The calculation assumes alternating up/down behavior with finite means, compatible steady scopes, both services required, binary state, mutual independence, no shared causes, restoration to full useful service, and no coverage or capacity limitation. It does not predict outage distribution, mission reliability, request success, tail repair, correctness, or a particular month's observed downtime.

### Answer 3

Define user and business outcomes and build aligned time, request, journey, and critical-cohort indicators. Record eligible events, missing telemetry, low-traffic periods, retries, latency, freshness, correctness, authorization, and partial modes. Do not multiply vendor claims; measure the composed path and model each shared dependency, population, window, and conditional state.

Map common software, identity, DNS, network, data, control, pipeline, operator, and repair authority across zones. Model detection, fencing, state, capacity, traffic movement, and reintegration as failover coverage, then test them. Estimate failure and restoration distributions with censoring and confidence, separating mission reliability from repair availability. Include maintenance, deployment, simultaneous failure, cold recovery, repair contention, and recurrence. Score stale read-only service only for explicitly satisfied read outcomes, never writes or freshness. Treat missing probes as unknown or failed according to a declared conservative policy, not automatic success.

### Answer 4

Active-active uses capacity continuously and can reduce switch delay, but requires routing, state convergence, fencing, and capacity for skew. Active-standby isolates some work but risks dormant failure, state lag, cold capacity, and imperfect switch coverage. Quorum protects selected consistency properties while enough members communicate; under partition it may reject operations rather than provide unsafe reachability. Local autonomy preserves bounded operations during central loss but needs explicit authority leases, reconciliation, and conflict limits. Backup restore protects selected durable history but usually has longer detection, provisioning, replay, validation, and recovery-point exposure.

For each design, model account read, write, authorization, audit, and recovery outcomes separately. Include shared identity, software, schema, network, control, operator, and provider causes; measure capacity and latency after required losses. Exercise split brain, stale state, ambiguous commit, zone and regional loss, bad deployment, key loss, repair contention, and repeated failure. Define permissible read-only or delayed modes without calling them full availability. Use RPO, restoration distribution, ledger reconciliation, and invariant checks beside service indicators; choose based on outcome criticality rather than maximum aggregate uptime.

### Answer 5

Define separate missions for sensor sampling, local display, phone transfer, cloud receipt, alert evaluation, clinician acknowledgement, escalation, historical retrieval, update, and recovery. A healthy state requires positive evidence with bounded age; missing, stale, untrusted, or corrupt monitoring is unknown or failed, never healthy. Model patient, device, clinician, region, and time cohorts separately and preserve accessibility, privacy, safety, and authorization constraints outside an aggregate error budget.

Construct states for sensing, buffered offline operation, degraded battery, disconnected gateway, delayed cloud ingestion, alert pending, clinician unavailable, update, repair, and data reconciliation. Fault trees include sensor placement or defect, battery, phone process and permission, clock, network, cloud queue, schema, identity, alert rule, notification path, console, operator workload, shared firmware, deployment, and recovery authority. Dynamic or state models represent ordering, buffer exhaustion, stale leases, update rollback, repeated disconnection, and repair. Do not assume devices, networks, regions, or humans are independent; analyze common software, supplier, campaign, environmental, identity, and organizational causes.

Measure detection, isolation, retry, buffering, transfer, deduplication, alert, acknowledgement, escalation, failover, update rollback, and restore coverage with explicit uncertainty. Test representative devices and users, boundary battery and storage, network loss and reconnection surge, clock error, duplicate and reordered data, cloud and identity loss, bad rules, clinician-console impairment, inaccessible workflows, operator overload, firmware faults, and recovery. Verify sequence identity, freshness, authorization, audit, and no false healthy state throughout. Internal engineering evidence informs—not certifies—clinical safety, privacy, human factors, or regulation. Clinical, safety, privacy, security, accessibility, operations, product, device, cloud, and regulatory owners retain acceptance authority; record residual unknowns and refresh after hardware, firmware, phone OS, network, workload, workflow, cloud, policy, threat, or evidence change.
