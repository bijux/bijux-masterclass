---
module_id: SYSENG-064
program: Systems Engineering
level: 2
module_number: 64
title: Availability Modeling
status: complete
last_verified: 2026-08-31
---

# Availability Modeling

## One-Page Review

### Governing question

How can engineers model whether a repairable or restorable system is capable when demanded—over time, across degraded states, and under real maintenance and logistics constraints—without confusing availability with reliability, averaging away mission-critical outages, or using MTBF/MTTR formulas beyond their assumptions?

### Essential definitions

- **Availability** is the probability or observed fraction that an item is in a state capable of performing a required function under stated conditions at a specified time or over an interval. The function, performance threshold, demand schedule, configuration and downtime policy matter.
- **Point availability** $A(t)$ is the probability the system is up at time $t$. **Interval/mean availability** averages up-state probability or uptime over a stated interval. **Steady-state availability** is a limiting value when a stable limit exists.
- **Inherent availability** $A_i$ emphasizes corrective-maintenance design characteristics, commonly using uptime between corrective failures and active corrective repair while excluding preventive maintenance and logistics/administrative delay under a declared convention.
- **Achieved availability** $A_a$ generally includes corrective and preventive maintenance but excludes some logistics/administrative delay, using the governing organization's exact definition.
- **Operational availability** $A_o$ includes the operating and support environment actually credited, typically corrective/preventive maintenance plus logistics and administrative delay. Definitions must be written, not assumed from the subscript.
- **Uptime** is time a system is capable by the declared success criterion. **Downtime** can include detection, isolation, access, repair, verification, preventive maintenance, waiting for spares/personnel/facility/authorization, and restart; inclusion depends on the measure.
- **MTBF** is a mean time between failures for a repairable process under a stated failure and operating-time convention. **MTTF** is mean time to first failure for a nonrepairable item/population. Neither alone determines a distribution.
- **MTTR** is an ambiguous acronym unless expanded: mean time to repair, restore, or corrective maintenance. The included clock phases and distribution must be stated.
- **Maintainability** $M(t)$ is the probability that a maintenance action can be completed within time $t$ under stated procedures and resources. It is a distribution, not merely a mean.
- **Repair rate** $\mu$ often parameterizes exponential restoration time. A rate of occurrence of failures $\lambda$ for a repairable process is not automatically the hazard of a nonrepairable lifetime.
- **Degraded availability** gives credit to states that deliver some required capacity/quality. It must define capability thresholds and value/weight; “up” versus “down” can hide partial mission loss.
- **Maintainability/supportability/logistics** cover accessibility, diagnosis, repair, verification, personnel, spares, tools, facilities, data and policy that restore capability.
- A **renewal process**, **continuous-time Markov chain (CTMC)**, **semi-Markov model**, **Petri net**, **queueing model**, or **discrete-event simulation** represents different failure/restoration/state assumptions; no one method is universal.

### Central model, mechanism, or theorem

Let $X(t)$ be the system state and $U$ the set of states meeting the capability criterion. Then

$$
A(t)=P[X(t)\in U],
\qquad
\bar A(0,T)=\frac{1}{T}\int_0^T A(t)\,dt.
$$

For an alternating renewal process with independent, identically distributed finite uptime $U_k$ and downtime $D_k$, long-run availability is

$$
A_{\infty}=\frac{E[U]}{E[U]+E[D]}.
$$

The familiar $MTBF/(MTBF+MTTR)$ is a convention-specific instance of this renewal-reward relationship, not a universal point-availability formula.

For a two-state CTMC with failure intensity $\lambda$, restoration intensity $\mu$, and initially up system:

$$
A(t)=\frac{\mu}{\lambda+\mu}+\frac{\lambda}{\lambda+\mu}e^{-(\lambda+\mu)t},
\qquad
A_\infty=\frac{\mu}{\lambda+\mu}.
$$

At equilibrium, failure and restoration flows balance: $\lambda A_\infty=\mu(1-A_\infty)$. Multi-state systems require a generator/state model with valid transitions and capacity mapping.

### Critical invariants

- Availability requirements state function/capacity/quality, demand schedule, mission/calendar interval, configuration, environment, initial state, exclusions and measurement convention.
- Reliability and availability remain distinct: repair can improve readiness after failures but cannot erase an interruption that violates failure-free mission success.
- Inherent, achieved and operational availability define every included uptime/downtime category; labels alone do not control policy.
- Failure/restoration clocks start and stop at defined events. Detection, diagnosis, access, repair, verification, logistics, administrative and restart times are neither silently omitted nor double-counted.
- Means are accompanied by distributions/tails and dependence where consequence depends on outage duration or deadline.
- State space includes degraded capability, maintenance/test, standby, switching, spares, crews, queues, common cause and recovery when decision-relevant.
- Transition assumptions, units and memorylessness are validated. Exponential CTMCs are not used merely for algebraic convenience.
- Shared repair resources, finite spares, replenishment, priorities and scheduled maintenance are explicit in operational models.
- Dependencies and CCF are modeled across components, support infrastructure, software, people, maintenance and environment.
- Empirical estimates report observation window, population, exposure, censoring, missing data, planned/unplanned classification and uncertainty.
- Average availability is paired with outage frequency, duration distribution, worst/percentile recovery, capacity shortfall and demand-weighted measures where appropriate.
- Model, data, configuration, solver, assumptions and decision remain traceable and are updated after changes or operational discrepancies.

### Common failures

Common failures include calling reliability availability; using “five nines” without service boundary or time window; treating all downtime alike; excluding logistics from an operational claim; using MTTR without clock definition; computing a ratio of means for a nonrenewal or demand-dependent system; assuming exponential repair; ignoring long-tail restoration; granting full availability to degraded capacity; crediting scheduled maintenance outside denominator without policy; treating redundant units as independent; assuming infinite spares/crews; ignoring queueing and repair priority; using steady state for a short mission or transient startup; averaging away a single unacceptable outage; counting planned events inconsistently; fitting one rate across aging or growth; and reporting point estimates without data/model uncertainty.

### Compact example

A synthetic two-state repairable system has $\lambda=0.02$/h and $\mu=0.5$/h, equivalent means 50 h uptime and 2 h restoration under exponential assumptions. Steady-state availability is 0.96153846; the initially-up transient at 10 h is 0.96175064, and equilibrium up/down flows both equal 0.01923077/h. Separately, an observed record of 1,000 up hours plus 20 corrective, 10 preventive, 15 logistics and 5 administrative downtime hours gives operational observed availability 0.95238095. The figures answer different questions.

### Connections

SYSENG-063 supplies success structure; availability adds restoration and support. SYSENG-065 develops maintainability/repair distributions, SYSENG-067 fault tolerance/degradation, and later common-cause, PRA and resilience modules extend multi-state scenarios. Platform and service engineering use the same distinctions when defining SLOs, but software deployments, traffic, dependencies and measurement windows require domain-specific models.

## Governing Question

Can an independent reviewer determine exactly what capability counts as available, reproduce the state/clock and downtime classification, validate failure/restoration/logistics data and dependencies, compare transient and steady-state results, and see whether the modeled measure matches the user's demand and decision?

An availability percentage without semantics is an attractive ambiguity. A system can have high calendar availability but fail every critical scheduled demand, or high average capacity while suffering one intolerable continuous outage. Model the decision, not the slogan.

## Why This Matters

Repairable systems live through cycles of operation, degradation, failure, detection, repair, waiting, test and restoration. Their usefulness depends not only on how often faults occur but on how quickly and reliably capability returns with actual spares, people, access and procedures. Availability modeling connects architecture and operations to staffing, inventory, facilities, maintenance policy, service agreements and lifecycle cost.

IEC 61703:2016 provides mathematical expressions for reliability, availability, maintainability and maintenance-support measures and includes state-transition/Markov and production-availability concepts. IEC 61078:2016 includes availability and failure-frequency calculation for repaired and nonrepaired RBDs. NIST explicitly separates repairable-system recurrence processes from nonrepairable lifetime distributions.

NASA availability guidance distinguishes inherent, achieved and operational measures by downtime inclusion. NASA maintainability work emphasizes that corrective maintenance, preventive maintenance, administrative delay and logistics delay can have very different variability and design ownership. These distinctions prevent a design team from claiming high inherent availability while users experience poor operational readiness caused by inaccessible hardware, scarce spares or authorization queues.

## Prerequisites and Retrieval

Before building or accepting an availability model, retrieve:

1. required capability/capacity/quality, demand schedule, users, consequence, time window, geography, configuration, environment and acceptable degradation/outage;
2. exact availability measure and denominator, included/excluded planned/unplanned states, observation/data policy and acceptance authority;
3. RBD/FTA/FMEA architecture, states/modes, redundancy, standby/switching, dependencies, CCF, fault detection/isolation and restoration paths;
4. failure/ROCOF, demand, degradation, preventive-maintenance and restoration distributions with units, population, exposure, censoring and uncertainty;
5. downtime clock decomposition: detection, diagnosis, safeing, access, disassembly, repair/replacement/reset, assembly, checkout, authorization, restart and return to capability;
6. logistics delay: spares stock/location/replenishment, tools, facilities, transport, documentation, supplier support and obsolescence;
7. resource constraints: crew skills/shifts, competing repairs, priorities, queues, common maintenance, working conditions and human-performance limits;
8. scheduled maintenance/test/update policy, opportunity windows, deferral, induced failures, latent faults and configuration control;
9. model formalism, states/transitions, distribution assumptions, solver/version, simulation seed/runs/warmup/horizon, convergence and validation cases;
10. operating logs, incidents, service tickets, work orders, sensor/monitor coverage, missing/ambiguous intervals, changes, actions and historical baselines.

Use a retrieval challenge: select the longest outage and trace failure/demand, detection, declaration, diagnosis, waiting, access, repair, verification, authorization and restored capability. Compare its classification with the model. A model that includes only hands-on wrench time cannot support operational availability.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish reliability, point/interval/steady availability, inherent/achieved/operational availability and maintainability;
2. define capability, demand and downtime clocks rigorously;
3. derive alternating-renewal and two-state CTMC availability under explicit assumptions;
4. compute transient and steady-state two-state results and verify equilibrium balance;
5. model degraded states, redundancy, standby, coverage, repair resources, spares and scheduled maintenance;
6. select renewal, CTMC, semi-Markov, Petri, queueing or simulation methods by behavior/data;
7. avoid MTBF/MTTR, exponential, independence and average-only errors;
8. estimate observed availability and report uncertainty, tails, frequency and demand weighting;
9. validate availability models structurally, mathematically, computationally and empirically;
10. use results for bounded design, maintenance, logistics and operational decisions.

## Core Exposition

**Define capability and demand.** “Available” may mean full service, safe degraded service, production above a threshold, or readiness within a response deadline. Name demand times: continuous, random, scheduled or mission-window. A backup that can start in five minutes may be available for an eight-hour restoration objective but unavailable for a 100 ms safety demand.

**Choose the measure before the formula.** Point availability answers readiness at time $t$; interval availability averages over a window; steady state describes a long-run limit. Demand availability estimates success when demanded. Production/capacity availability weights states by useful output. Pick the measure that aligns with consequence and user decisions.

**Define availability categories contractually.** For $A_i$, state whether active corrective maintenance includes diagnosis, access, checkout and return-to-service. For $A_a$, define preventive-maintenance inclusion. For $A_o$, include actual delay categories and policy. Organizations vary, so spell out numerator, denominator and clock boundaries.

**Model the simple alternating process carefully.** If an item alternates between iid uptime and downtime cycles with finite means, renewal reward gives long-run uptime fraction. The result does not require exponential distributions, but it does require the renewal structure and appropriate cycle definitions. A ratio computed from incompatible means is invalid.

**Use CTMCs only when memorylessness fits.** Two-state exponential failure/restoration gives simple transient and steady results. More states can represent degraded operation, standby, spares and repair. Exponential holding time means transition intensity does not depend on elapsed state age. If repair deadlines, lognormal times, wear-out or deterministic maintenance matter, use semi-Markov/simulation or phase-type approximation with validation.

**Construct a state model.** Enumerate operational capacity, failed items, standby status, detection/coverage, maintenance/testing, available spares and crew/resource allocation. Prune only unreachable or decision-irrelevant states with rationale. State explosion is a modeling constraint, not permission to erase high-consequence states.

**Map states to reward/capability.** Binary reward is 1 for up and 0 for down. Capacity reward can be $0\le r_s\le1$ relative to required output. Demand-weighted reward changes with user load or mission phase. Verify that reward does not credit unsafe or quality-invalid service merely because hardware produces output.

**Represent redundancy with restoration.** Parallel items may fail and be repaired independently only when support is genuinely separate. Include shared support and CCF. Standby adds dormant failure, coverage, switching and startup. Repair can restore one branch while another carries load; load-dependent failure intensity may then change.

**Model maintenance resources and queues.** Infinite repair crews and immediate spares are convenient assumptions that often inflate availability. Finite-source queueing or simulation can include crew shifts/skills, priorities, travel, access, repair bay, cannibalization, stockouts and replenishment. Validate priority rules, not only mean service time.

**Decompose downtime.** Record time to detect, diagnose, safe, mobilize, access, acquire parts/tools/data, repair, reassemble, test, approve and restart. Each phase has different owners and interventions. Parallel activities require event logic; adding all mean durations may overstate, while using only the maximum may understate dependencies.

**Treat scheduled downtime transparently.** Preventive maintenance, inspection, calibration, proof test, deployment and upgrade can improve future behavior while creating present unavailability and induced risk. Define whether maintenance is excluded by contract, counted in achieved/operational measures, or scheduled outside demand. Report both contractual and user-experienced views when useful.

**Handle observation consistently.** Observed availability is credited uptime divided by credited total time under a classification policy. Preserve missing telemetry, ambiguous partial service, overlapping incidents, planned work and excluded periods. Avoid pausing the denominator during inconvenient events unless the requirement explicitly does so.

**Use event processes correctly.** For a stable repairable system, an HPP may model recurrence with constant ROCOF and exponential interarrival times. Reliability growth, aging, changing utilization and fleet heterogeneity violate that assumption. Recurrence data and first-failure lifetime data answer different questions.

**Examine distributions and tails.** Two designs with the same MTTR can have different probabilities of exceeding a four-hour recovery objective. Use restoration CDF, percentiles, maximum credible delay and causes of long tail. Spares stockout and rare access constraints may dominate user risk while barely shifting the mean.

**Model phased and transient demand.** Startup availability from a known-up state initially equals one and approaches steady state; a system just repaired or entering a mission is not necessarily in equilibrium. Seasonal demand, launch windows and maintenance cycles require time-varying/transient analysis. Do not use steady state because it is easy.

**Measure more than uptime fraction.** Report outage frequency, duration distribution, longest outage, repeated short interruptions, demand failures, capacity shortfall, time to safe degraded service, backlog, stockout and repair-resource utilization. A single ratio hides operational pain and safety constraints.

**Analyze sensitivity and uncertainty.** Vary failure, restoration, coverage, CCF, logistics and policy inputs. Propagate distributions/intervals, distinguish stochastic variability from knowledge uncertainty, and identify data worth. Correlated epistemic estimates and shared operational conditions prevent naive independent sampling.

**Validate structure.** Compare states/transitions/rewards with architecture, RBD, FTA, FMEA, procedures, support plan, staffing, spares and operations. Walk real outages through the model. Confirm every claimed recovery is feasible, authorized and within capacity/timing.

**Validate mathematics and computation.** Check transition units/signs, generator row sums, probabilities/nonnegative state occupancy, total probability one, equilibrium balance, limiting cases, analytic two-state cases, conservation of resources/spares and simulation convergence/reproducibility. Tool execution is not empirical validation.

**Calibrate and back-test.** Estimate from applicable exposure and work-order timestamps with uncertainty. Hold out periods or compare predictions to later outcomes; investigate systematic residuals and missing states. Data generated under a different maintenance policy may not transport to the proposed system.

**Use results for trade decisions.** Improve reliability, access/diagnosis/repair, coverage, spares, staffing, distribution, preventive policy or graceful degradation. Check lifecycle cost, safety, induced maintenance risk and common cause. An apparent availability improvement may shift burden to people or inventory.

**Maintain the model and evidence.** Version requirements, state definitions, configuration, data extraction, distributions, policies, solver and results. Update after changes, outages, support-policy shifts and observed tail events. Retain prior baselines for audit and avoid retroactively applying current classifications to historical decisions without disclosure.

The following fixture contrasts analytic transient/steady availability with one separately observed operational ratio.

<!-- bijux-verify: {"id":"availability-two-state-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"failure_intensity_per_hour=0.02000000\nrestoration_intensity_per_hour=0.50000000\nmean_uptime_hours=50.00000000\nmean_restoration_hours=2.00000000\nsteady_state_up=0.96153846\nsteady_state_down=0.03846154\nbalance_failure_flow=0.01923077\nbalance_restoration_flow=0.01923077\ntransient_up_at_10h=0.96175064\nobserved_operational_availability=0.95238095\nstatus=declared_availability_fixture_passed\nevidence=synthetic_two_state_and_observed_counts_only\n","stderr":""}} -->
```python
failure_intensity = 0.02
restoration_intensity = 0.5
mean_uptime = 1 / failure_intensity
mean_restoration = 1 / restoration_intensity
steady_up = restoration_intensity / (failure_intensity + restoration_intensity)
steady_down = 1 - steady_up
transient_10h = steady_up + steady_down * 2.718281828459045 ** (-(failure_intensity + restoration_intensity) * 10)
observed_up = 1000
observed_down = 20 + 10 + 15 + 5
observed_operational = observed_up / (observed_up + observed_down)
print(f"failure_intensity_per_hour={failure_intensity:.8f}")
print(f"restoration_intensity_per_hour={restoration_intensity:.8f}")
print(f"mean_uptime_hours={mean_uptime:.8f}")
print(f"mean_restoration_hours={mean_restoration:.8f}")
print(f"steady_state_up={steady_up:.8f}")
print(f"steady_state_down={steady_down:.8f}")
print(f"balance_failure_flow={failure_intensity * steady_up:.8f}")
print(f"balance_restoration_flow={restoration_intensity * steady_down:.8f}")
print(f"transient_up_at_10h={transient_10h:.8f}")
print(f"observed_operational_availability={observed_operational:.8f}")
print("status=declared_availability_fixture_passed")
print("evidence=synthetic_two_state_and_observed_counts_only")
```

The analytic result assumes stationary exponential transitions and an initially-up independent two-state process. The observed ratio is separate synthetic bookkeeping; it is not a sample from that CTMC and carries no confidence interval.

## Definitions and Notation

Let $S$ be states, $U\subseteq S$ acceptable states and reward $r(s)$ the fraction/value of required capability. State probability vector $p(t)$ gives binary availability $\sum_{s\in U}p_s(t)$ or capacity availability $\sum_s r(s)p_s(t)$.

For a finite homogeneous CTMC generator $Q$, off-diagonal $q_{ij}\ge0$ are transition intensities, $q_{ii}=-\sum_{j\ne i}q_{ij}$, and

$$
p'(t)=p(t)Q.
$$

A stationary distribution $\pi$ satisfies $\pi Q=0$ and $\sum_s\pi_s=1$ when a suitable unique limiting regime exists. Steady availability is then $\sum_{s\in U}\pi_s$. Not every process is stationary, irreducible or memoryless.

## Mechanisms, Invariants, or Proof Structure

A defensible availability claim follows this chain:

1. **Measure validity:** capability, demand, window, availability category, denominator and downtime clocks match the decision.
2. **Structural validity:** states, transitions, capacity/rewards, dependencies, maintenance/logistics and policies reflect real operations.
3. **Stochastic validity:** failure/restoration/queue/distribution assumptions and units match mechanisms and data.
4. **Computational validity:** analytic limiting cases, conservation, solver/simulation settings and convergence are reproducible.
5. **Empirical validity:** extraction/classification, population/exposure, uncertainty and out-of-sample discrepancy are assessed.
6. **Decision validity:** averages, tails, outage frequency, degraded capacity, actions, side effects and residual acceptance are visible.

No high steady-state percentage compensates for an invalid measure or an unacceptable single outage.

## Alternatives and Trade-Offs

**Analytic renewal versus CTMC.** Renewal reward handles general iid alternating durations for long-run fraction. CTMC handles multi-state exponential transitions and transient/equilibrium probabilities. Neither naturally handles every calendar/policy/resource dependence.

**Semi-Markov versus phase-type CTMC.** Semi-Markov models permit general holding-time distributions but are computationally harder. Phase-type approximations retain Markov solvers but require fit and can expand states. Validate tail behavior important to decisions.

**Queueing versus discrete-event simulation.** Queueing yields insight under tractable arrival/service/priority assumptions. Simulation handles complex spares, crews, policies and calendars but needs verification, many runs, rare-event treatment and careful uncertainty.

**Binary versus multi-state availability.** Binary measures are simple and contractual. Multi-state/capacity measures represent degraded service but require stakeholder value/threshold definitions and must not credit unsafe output.

**Inherent versus operational focus.** Inherent availability isolates design repairability and reliability; operational availability reflects user experience and support. Track both so engineering and operations owners cannot hide causes in each other's exclusions.

**Scheduled maintenance versus run-to-failure.** Preventive work creates planned downtime and induced risk but may reduce failures/tails. Optimize total consequence and lifecycle cost under uncertainty, not availability ratio alone.

## Failure Modes and Misconceptions

- **“Availability is reliability with repair.”** They answer different event questions; an interruption can violate reliability even if quickly repaired.
- **“$MTBF/(MTBF+MTTR)$ always applies.”** It needs compatible renewal/steady-state definitions and included downtime.
- **“Steady state describes the mission.”** Short, phased, seasonal or initially-known systems can be dominated by transient behavior.
- **“MTTR is repair time.”** Define detection through restoration clocks; logistics and approval may dominate.
- **“Five nines means 5.26 minutes.”** Only under a specific annual continuous denominator and binary service; outage pattern and demand still matter.
- **“Planned downtime does not count.”** It depends on the measure/contract and user demand; disclose both policy and experience.
- **“Redundant repairable items are independent.”** Common failure and shared crews/spares create dependence.
- **“The mean outage is enough.”** Tail recovery and outage frequency can drive safety and operations.
- **“Simulation is realistic by default.”** It executes encoded assumptions; missing states and invalid distributions remain wrong.
- **“Observed uptime validates the model.”** Classification, censoring, configuration, policy and uncertainty must be assessed.

## Worked Examples

### Example 1

A continuously repaired device has mean uptime 100 h and mean corrective restoration 4 h under an alternating renewal definition. Long-run inherent availability is $100/(100+4)=0.961538$. If logistics adds 6 h per failure, a corresponding operational cycle estimate becomes $100/(100+10)=0.909091$. The difference is scope, not contradiction.

### Example 2

A safety system is needed only during a weekly test demand. Calendar availability 0.999 can coexist with systematic unavailability during the demand because maintenance is scheduled then. Demand-weighted availability conditions on demand time and configuration. Reschedule maintenance or add protected capacity; do not average the conflict away.

### Example 3

Two repairable servers share one technician. Independent parallel formulas assume restoration can proceed without contention. Simultaneous failures queue; repair priority and service distribution change degraded/full availability. A finite-source queue or simulation models technician state, and sensitivity tests whether another shift or better diagnosis outperforms extra hardware.

### Example 4

One spare is stocked for five identical units with replenishment taking days. Infinite-spares Markov results overstate fleet readiness after clustered failures. Add on-hand inventory, reorder/replenishment, repairable/condemned parts, cannibalization and transport. Common environmental damage can both consume many spares and delay supply, creating dependency.

### Example 5

A two-state system starts known-up for a 30-minute operation. Steady availability may understate its early readiness; transient $A(t)$ begins at one. Conversely, a system emerging from maintenance with unverified configuration may not be known-up. Initial distribution is evidence, not a default.

### Example 6

Two repair-time distributions both have mean 2 h. One is nearly deterministic; another is usually 20 min but has rare 18-hour delays. They have similar simple long-run means but very different probability of missing a four-hour restoration objective. Report $M(4)$, percentiles and tail causes, not only MTTR.

### Example 7

A service delivers 100%, 60% or 0% capacity. Binary availability at any service counts the 60% state as up, but the user requires at least 80%. Threshold availability marks it down; production availability can credit 0.6 for capacity planning. Safety/quality criteria may forbid fractional credit. State reward follows decision.

### Example 8

Preventive calibration causes two planned hours monthly and reduces drift failures. Operational availability includes those hours if users cannot access service. Model alternative intervals with induced failure, detection quality, failure cost and maintenance windows. Selecting the highest availability may be unsafe if it delays necessary calibration.

### Example 9

An API reports 99.95% request success, while one region was unavailable for four hours. Request-weighted availability hides low overnight volume and regional users. Report time-, request-, user/region- and critical-transaction-weighted measures plus longest outage. Define retries and partial responses consistently to avoid denominator gaming.

### Example 10

Observed restoration exceeds the model because security approval and configuration verification add delay. Rather than inflate hardware MTTR, decompose the clock and assign owners. Automate safe evidence collection and preapprove bounded recovery while preserving controls. Revalidate end-to-end recovery; shortening one clock must not increase unsafe restoration.

## Cross-Program Connections

- **Data engineering:** event-time histories, bitemporal corrections, censoring, fleet heterogeneity, distributions and uncertainty underpin observed/model availability.
- **API and service engineering:** SLO windows, retries, partial service, load weighting, failover and dependency availability are direct applications with measurement caveats.
- **Platform engineering:** shared repair/on-call teams, regions, control planes, deployment calendars and quotas form state and resource dependencies.
- **Object-oriented programming:** explicit state machines and responsibility boundaries help represent restoration workflows; hidden global dependencies corrupt independence.
- **Functional programming:** CTMC generators, immutable event histories, state rewards and simulation property tests support reproducibility.
- **Operations research:** queues, inventory, scheduling, optimization and simulation connect engineering design to support capacity.

## References

1. International Electrotechnical Commission, [IEC 61703:2016, Mathematical expressions for reliability, availability, maintainability and maintenance support terms](https://webstore.iec.ch/en/publication/25646), edition 2.0, stability date 2028.
2. International Electrotechnical Commission, [IEC 61078:2016, Reliability block diagrams](https://webstore.iec.ch/en/publication/25647), edition 3.0, 2016.
3. International Electrotechnical Commission TC 56, [Dependability FAQs](https://tc56.iec.ch/faqs/), availability/reliability/maintainability context, accessed 2026-08-31.
4. NIST/SEMATECH, [Repairable systems, non-repairable populations and lifetime distribution models](https://www.itl.nist.gov/div898/handbook/apr/section1/apr121.htm), Engineering Statistics Handbook, accessed 2026-08-31.
5. NIST/SEMATECH, [Homogeneous Poisson Process](https://itl.nist.gov/div898/handbook/apr/section1/apr171.htm), Engineering Statistics Handbook, accessed 2026-08-31.
6. NASA Office of Safety and Mission Assurance, [Reliability and Maintainability](https://sma.nasa.gov/sma-disciplines/reliability-and-maintability), current policy/training index, accessed 2026-08-31.
7. NASA, [Availability Prediction and Analysis](https://ntrs.nasa.gov/api/citations/19950025109/downloads/19950025109.pdf), Reliability Preferred Practice AT-3, 1995.
8. NASA, [Space Transportation System Availability Requirements and Its Influencing Attributes Relationships](https://ntrs.nasa.gov/citations/20130012696), publication record, 2008.
9. NASA, [Maintainability Allocations](https://ntrs.nasa.gov/api/citations/20160003132/downloads/20160003132.pdf), 2016.
10. NASA, [Designing for Maintainability and System Availability](https://ntrs.nasa.gov/api/citations/19970013665/downloads/19970013665.pdf), 1997.

## Exercises

### Exercise 1

Define inherent, achieved and operational availability clocks for a repairable imaging system, including diagnosis, preventive calibration, spares delay, security approval and checkout. Explain differing owners.

### Exercise 2

For a two-state CTMC with $\lambda=0.01$/h and $\mu=0.2$/h initially up, calculate steady availability and point availability at 5 h. Check equilibrium flow.

### Exercise 3

Design a multi-state availability model for two active units sharing one repair crew and one spare, with 100%, 50% and 0% capacity states. Identify where simple parallel formulas fail.

### Exercise 4

Audit a “99.99% available” claim based only on MTBF 10,000 h and MTTR 1 h. List assumptions/evidence required and operational measures that could contradict it.

### Exercise 5

Plan validation and lifecycle maintenance for an operational-availability simulation used to choose spare inventory and staffing.

## Answers to the Exercises

### Answer 1

Define capability as producing images meeting quality/throughput within the required schedule. Inherent downtime may include fault confirmation, diagnosis, access, corrective replacement/repair, reassembly, checkout and return to capable state under ideal resources, while excluding preventive calibration, spares/personnel/facility and administrative delay. Design and maintainability owners govern much of this.

Achieved availability includes corrective and preventive active maintenance under the selected convention, so scheduled calibration duration/frequency enters. Operational availability additionally includes spares transport/stockout, crew mobilization/queue, facility, documentation, security authorization and operational restart delay. Logistics, operations, security and management own many of these clocks.

Record timestamps for detection, declaration, diagnosis, safeing, access, part request/receipt, hands-on work, checkout, approval and restored user capability. Overlap must be represented rather than blindly summed. Publish numerator/denominator and excluded states. The measures can differ legitimately, but none should be mislabeled as user-experienced availability.

### Answer 2

Steady availability is

$$
A_\infty=\frac{0.2}{0.01+0.2}=0.95238095.
$$

Starting up,

$$
A(5)=A_\infty+(1-A_\infty)e^{-0.21(5)}.
$$

Since $e^{-1.05}\approx0.34994$, $A(5)\approx0.969045$ (rounding depends on retained precision). Equilibrium flow is $\lambda A_\infty=0.00952381$/h and $\mu(1-A_\infty)=0.00952381$/h.

This assumes stationary exponential failure/restoration, one binary capability, continuous repair and an initially-up system. It is neither operational availability with logistics nor evidence that real clocks are exponential.

### Answer 3

State must include number of operational units (2, 1, 0), whether the failed unit is waiting/under repair, spare state (available/installed/failed/replenishing), and crew assignment. Rewards are 1.0, 0.5 and 0 under the stated capacity measure; if required capacity is 100%, binary availability credits only the two-up state.

Transitions include unit failures with load-dependent intensities, common-cause both-unit failure, crew diagnosis/repair, replacement from spare, repair completion, spare replenishment and failures during replacement. One crew prevents simultaneous repairs and creates a queue. One spare prevents unlimited immediate replacement. Switching/coverage and maintenance-induced faults may add states.

Simple parallel formulas assume static independent block states and omit repair contention, stock depletion, transition delay, common cause and capacity. Use CTMC only if holding times are plausibly exponential; otherwise semi-Markov or simulation. Check state probability conservation, limiting cases, resource counts and reduced analytical cases.

### Answer 4

The ratio gives $10{,}000/(10{,}001)=0.99990001$ only under compatible long-run alternating-cycle definitions. Required evidence includes capability/demand, configuration/environment, failure definition and operating-time clock, restoration clock, stationary renewal behavior, applicable MTBF/MTTR estimates and uncertainty, and included/excluded downtime. MTTR must specify diagnosis, access, repair, verification and restart.

Operational availability can be lower because of preventive maintenance, logistics, staff, travel, facilities, authorization, software/configuration restoration and queues. Shared/common-cause outages and planned downtime may be absent. A short mission may need transient reliability; a scheduled demand may coincide with maintenance. Longest outage, duration percentiles, frequency, demand failures, degraded capacity and user/region-weighted service can contradict the favorable mean ratio.

Do not claim four nines from two uncertain means without observation window/population, confidence/uncertainty and model validation.

### Answer 5

Define service/capacity reward, operational downtime policy, demand/calendar, fleet/configuration and trade outputs: availability, stockouts, outage duration/frequency, crew utilization, backlog, cost and safety constraints. Build states/events from RBD/FMEA/FTA, maintenance process, inventory/replenishment, shifts/skills, priorities, access and common causes. Version distributions and policy.

Verify code with deterministic event cases, fixed seeds, resource conservation, event ordering/ties, no-negative inventory, probability/bound checks and reduced analytic queue/renewal/CTMC cases. Run sufficient replications, horizon/warmup/convergence analysis and rare-tail methods. Independently review input extraction and units.

Validate against held-out work orders, stockouts, restoration phase timestamps, capacity telemetry and outage patterns; investigate discrepancies and missing states. Propagate parameter/model uncertainty and test staffing, replenishment, demand, CCF and tail alternatives. Do not optimize to the mean alone.

After selecting inventory/staffing, link assumptions, costs, actions and acceptance. Monitor policy, supplier lead time, fleet aging, configuration and observed tails; update prospectively and retain prior baselines. Simulation evidence informs the decision but does not guarantee future availability or safe maintenance.
