---
module_id: SYSENG-063
program: Systems Engineering
level: 2
module_number: 63
title: Reliability Block Diagrams
status: complete
last_verified: 2026-08-31
---

# Reliability Block Diagrams

## One-Page Review

### Governing question

How can engineers represent the combinations of functions or items required for mission success, calculate reliability or availability under valid assumptions, and use the result for design decisions without confusing functional success with physical layout, nominal redundancy with independence, or a point estimate with demonstrated performance?

### Essential definitions

- **Reliability** $R(t)$ is the probability that an item performs its required function without failure for a specified interval under stated conditions. The time, function, configuration, environment and success criteria are inseparable from the number.
- A **reliability block diagram (RBD)** is a success-space logical network. The modeled function succeeds when at least one operational path connects its input and output under the diagram's semantics.
- A **block** represents a function, item, event or modeled capability with a defined success state. It is not necessarily one physical component.
- **Series logic** means every block in a path must succeed. Under independence, series reliability is the product of block reliabilities.
- **Parallel logic** means at least one branch must succeed. Under independence, parallel reliability is one minus the product of branch unreliabilities.
- A **$k$-out-of-$n$ structure** succeeds when at least $k$ of $n$ blocks succeed. Identical-independent binomial formulas do not apply automatically to unequal or dependent blocks.
- **Active redundancy** has multiple paths operating or immediately able to perform. **Standby redundancy** holds one or more units inactive/degraded until detection and switching; dormant failure, coverage, order and transition time matter.
- A **minimal path set** is a smallest set of successful blocks sufficient for system success. A **minimal cut set** is a smallest set of failed blocks sufficient for system failure.
- A **coherent RBD** is monotone in component success: making an additional block successful cannot make the system fail. Noncoherent or state-dependent structures need careful semantics.
- **Mission reliability** concerns failure-free performance over an interval, usually without repair credit unless explicitly modeled. **Availability** concerns readiness at a time or fraction of time and can credit repair/support. They are not interchangeable.
- **Common-cause failure (CCF)** and other dependencies can defeat multiple nominally redundant blocks. Separate drawing branches do not establish probabilistic independence.
- **Coverage** is the conditional probability that fault detection, isolation, switching and reconfiguration succeed when demanded under stated conditions. It is not merely diagnostic presence.
- **Importance** measures sensitivity or contribution within a specific model. It does not by itself determine the best or safest design action.

### Central model, mechanism, or theorem

Let each block success indicator be $x_i\in\{0,1\}$ and system success be the structure function $\psi(x)$. For a coherent RBD, $x\le y$ implies $\psi(x)\le\psi(y)$. Under independent block successes with $P(x_i=1)=R_i(t)$:

\[
R_{series}(t)=\prod_{i=1}^{n}R_i(t),
\qquad
R_{parallel}(t)=1-\prod_{i=1}^{n}[1-R_i(t)].
\]

For $n$ identical independent blocks with reliability $R$ and success requiring at least $k$:

\[
R_{k|n}=\sum_{j=k}^{n}{n\choose j}R^j(1-R)^{n-j}.
\]

For independent nonrepairable exponential lifetimes, $R_i(t)=e^{-\lambda_i t}$ and series hazards add:

\[
R_{series}(t)=e^{-t\sum_i\lambda_i}.
\]

These formulas are conditional. A general structure is evaluated by enumerating states, minimal paths/cuts, Boolean reduction, binary decision diagrams, factoring, simulation, Markov/Petri/state-space methods or other justified algorithms.

### Critical invariants

- Every RBD states function/success threshold, mission/use phase, time basis, configuration, environment, initial state, allowed degradation and repair/recovery credit.
- Connectivity expresses functional success logic, not electrical, fluid, mechanical, data or organizational topology unless those happen to implement the success relation.
- Blocks have stable identities, success/failure definitions, authority, data provenance, distribution/model, units, uncertainty and configuration applicability.
- Series/parallel/$k$-of-$n$ reductions are used only when the substructure and probabilistic assumptions justify them.
- Redundant branches include required sensing, decision, switching, isolation, support, actuation, capacity and timing. Shared resources are not hidden outside the diagram.
- Independence, mutual exclusivity, conditional dependence and CCF assumptions are explicit and challenged across design, software, power, environment, manufacturing, maintenance and operation.
- Constant failure rates and exponential lifetimes are justified over the mission interval; infant mortality, wear-out, demand, cycle, degradation and systematic behavior use appropriate models.
- Reliability, probability of failure, failure frequency, maintainability and availability are not mixed. Repair and logistics require explicit state/time modeling.
- Minimal path/cut sets, limiting cases, state enumeration and independent reduced calculations validate logic and tools.
- Sensitivity and importance preserve uncertainty and feasibility context. Added redundancy is assessed for new failure modes, mass/cost/complexity and common dependencies.
- Model predictions are compared with test and field evidence using applicable populations/exposure and uncertainty; sparse success histories do not prove high reliability.
- Changes to architecture, configuration, usage, environment, software, process, supplier, data or controls trigger impact, recalculation and retained prior baselines.

### Common failures

Common failures include copying a schematic; modeling parts rather than required functions; using one diagram for incompatible mission phases; assigning “reliability” without time and conditions; multiplying blocks with shared failures; treating nominal parallel components as independent; omitting voter, switch, sensor, power, cooling, software and operator; giving perfect coverage; applying active-parallel formulas to cold standby; treating failure rates as probabilities; using $e^{-\lambda t}$ across wear-out or demand failures; crediting repair in mission reliability; double-counting shared blocks; assuming every connected path has capacity; truncating network paths without bounding effect; validating only with tool output; adding redundancy that worsens system risk; and presenting extra decimal places as evidence strength.

### Compact example

A synthetic success network requires one of two sensors, one controller and one actuator. With declared independent mission reliabilities 0.98, 0.98, 0.99 and 0.97, exact enumeration gives sensor-subsystem reliability 0.99960000 and system reliability 0.95991588. A single-sensor design gives 0.94109400, so the modeled gain is 0.01882188. Enumeration also confirms minimal paths `{sensor_a,controller,actuator}` and `{sensor_b,controller,actuator}`, and minimal cuts `{controller}`, `{actuator}`, `{sensor_a,sensor_b}`. This proves only the declared static Bernoulli fixture.

### Connections

SYSENG-061 identifies failure modes, while SYSENG-062 represents top-event failure logic. SYSENG-063 expresses functional success and exposes series weaknesses and redundancy. SYSENG-064 adds repairable availability, SYSENG-065 maintainability, and later modules add common-cause, PRA, fault management and resilience. A coherent static RBD may be the dual of a compatible fault tree, but the two views must share definitions and assumptions.

## Governing Question

Can an independent reviewer reconstruct what “success” means, verify every required path and shared dependency against the architecture, reproduce the block data and calculations, challenge time/repair/coverage/independence assumptions, and understand how uncertainty affects the design decision?

A path drawn from left to right is not evidence that a system will succeed. An RBD becomes useful when the paths reflect actual functional capacity under the declared mission and every probability is supported by an applicable model and evidence.

## Why This Matters

RBDs make success dependencies visible. They reveal when one series element dominates, when apparent redundancy shares a single support, where switching or coverage limits benefit, how allocation and trade studies change mission reliability, and which tests or data would reduce decision uncertainty. They also support availability, failure-frequency and maintainability studies when repair/state semantics are added correctly.

IEC 61078:2016 defines requirements and procedures for qualitative and quantitative RBD analysis, including reliability, availability and failure frequency, repaired and nonrepaired blocks, and relationships with FTA and Markov methods. It also acknowledges noncoherent and dynamic RBDs. NASA-STD-8729.1A defines RBD analysis as a success-space symbolic-logic model and identifies it as a basis for finding weak areas and informing FMEA, FTA, spares and maintenance.

NASA's reliability practice recommends function-oriented models built concurrently with design and notes that architecture, failure data and mission time are essential. Current NASA post-mission extension guidance warns that RBDs are neither electrical nor mechanical connection diagrams and that changed mission goals and already-failed equipment alter the model. NIST provides the standard series, parallel, $r$-of-$n$ and complex-system reliability relationships; these formulas remain conditional on the statistical model.

## Prerequisites and Retrieval

Before building or accepting an RBD, retrieve:

1. decision, required function, success/performance threshold, mission/use phase, duration/cycles, environment, configuration, consequence and acceptance authority;
2. architecture and functional flows, interfaces, capacity/load sharing, dependencies, redundancy mode, sensors, voters, switches, isolation, support and recovery;
3. initial states, degraded modes, maintenance/test state, demand timing, dormancy, switchover time, allowed repair and logistics/support assumptions;
4. stable block identities, boundaries, success/failure definitions, mapping to configuration items/functions and links to requirements, FMEA, FTA and hazards;
5. lifetime/failure-on-demand/degradation/repair distributions, parameters, units, populations, stress/environment, exposure, censoring and uncertainty;
6. independence/dependency rationale, CCF groups/model, shared design/software/power/environment/process/maintenance/operator and correlation evidence;
7. coverage definition and evidence for detection, isolation, decision, switching, reconfiguration and post-switch capacity/timing;
8. solution algorithm, tool/version/settings, exact/reduction/truncation behavior, state-space or simulation model, seeds and convergence where relevant;
9. test, anomaly, field, maintenance, supplier, inspection and operating evidence plus prior model/data review findings;
10. uncertainty, sensitivity, importance, trade/action workflow, verification, change triggers, baseline/provenance and long-term reproducibility.

Use a retrieval challenge: choose one parallel branch and request the actual function/capacity, failure definitions, common dependencies, switching/coverage, block data and confidence, exact mission/configuration, solver record, linked tests and design conclusion. If “two boxes in parallel” is the only justification, redundancy benefit is unproven.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish RBD functional success logic from physical schematics and organizational block diagrams;
2. define blocks, series/parallel/$k$-of-$n$, active/standby redundancy, minimal paths/cuts, coherence and coverage;
3. derive series, parallel, mixed and identical $k$-of-$n$ reliability under explicit independence;
4. calculate exponential mission reliability and identify when constant-rate assumptions fail;
5. enumerate arbitrary small structures and validate minimal path/cut sets;
6. distinguish mission reliability, failure probability/frequency, availability and maintainability;
7. model or escalate capacity, load sharing, standby, repair, switching, CCF and dynamic/state behavior;
8. interpret importance, allocation, sensitivity and uncertainty for bounded decisions;
9. validate and update RBD logic/data against architecture, FMEA/FTA, tests and field evidence;
10. communicate results without claiming independence, completeness or demonstrated reliability beyond evidence.

## Core Exposition

**Define success first.** Use a performance statement: “deliver at least 8 kW regulated power to essential loads for the 12-hour surface mission in configuration L3 under the specified thermal environment.” Decide whether degraded capacity, interruption, manual recovery or repair counts. Separate functions may need separate RBDs.

**Model functions, then realizations.** Start with required functional stages—sense, decide, actuate, supply, communicate—and map items into each. This prevents a schematic from hiding that two hardware paths require one shared control function. A block may represent one item, a group, software behavior, human action or a transfer function, but its success state must be precise.

**Use series logic for mandatory stages.** If every stage must work, success is their intersection. Under independence, multiply reliabilities. The lowest reliability often dominates, but sensitivity depends on all values and mission. A bypass or degraded alternative changes the structure rather than simply changing one block's value.

**Use parallel logic for sufficient alternatives.** Each branch must independently provide the required function/capacity under the same success criteria. Under independent branch failures, multiply unreliabilities and complement. If branches share support, add shared series blocks or a dependency model; do not bury common support inside both with independent copies.

**Model capacity explicitly.** Two 5 kW units in parallel do not satisfy an 8 kW load after one fails. The structure is 2-out-of-2 at that load, perhaps 1-out-of-2 at a 4 kW degraded requirement. Load sharing can change component stress/failure distributions when one branch fails, requiring state-dependent models.

**Handle $k$-out-of-$n$.** The binomial expression assumes identical independent Bernoulli success probabilities. Unequal independent blocks require summing appropriate state products or a generating/BDD method. Dependencies require joint/state models. Include voter/combiner capacity and failure if it is required.

**Separate active and standby redundancy.** Active parallel units operate simultaneously. Standby units have dormant failure, demand detection, switch/valve/control success, startup delay, capacity after transfer and possibly different active/standby rates. A simple parallel complement assumes immediate equivalent availability and usually overstates standby reliability.

**Define coverage operationally.** Coverage may be a chain: detect within time, correctly diagnose/isolate, issue command, switch/reconfigure, and deliver required performance. Each stage can fail and share dependencies with the initiating fault. Estimate and verify coverage under representative faults, loads, timing and degraded conditions.

**Choose lifetime models from mechanisms and data.** Constant hazard yields exponential reliability, useful in a stable useful-life region. Weibull/lognormal or physics/degradation models may represent early failure and wear-out. Demand-based items use probability of failure on demand; cycle-limited items use cycles; software systematic failure needs trigger/assurance evidence rather than a fabricated random wear rate.

**Keep time bases aligned.** Blocks may operate for different durations or duty cycles. Use each exposure in its reliability model and one consistent mission structure. Conditional phases, dormant periods and transitions may require phased-mission/state models. Never multiply a per-hour rate by a cycle probability.

**Treat repair separately.** Mission reliability usually asks for no loss over an interval. Availability credits restoration and depends on repair distributions, coverage, spares, crews, logistics, preventive maintenance and downtime definition. A repairable RBD can be evaluated with Markov/Petri/simulation or suitable approximations, but labeling steady-state availability as reliability is wrong.

**Find minimal paths and cuts.** Minimal paths expose smallest sufficient success sets; minimal cuts expose smallest failure sets. They support review, allocation and cross-check with FTA. Apply absorption so supersets are removed. Validate small models by enumerating all states; test large solvers with known fixtures and alternative reductions.

**Evaluate bridge networks carefully.** Some networks cannot be reduced by repeated series/parallel operations. Conditioning on a pivotal block, factoring, path/cut inclusion–exclusion, BDDs or enumeration provides exact independent-event solutions. Monte Carlo can handle larger/dynamic cases but needs rare-event strategy, convergence and uncertainty checks.

**Model dependencies rather than narrating them away.** Shared design defects, manufacturing lots, power, cooling, environment, software, data, operator, maintenance, calibration and test equipment can correlate failure. Use explicit common blocks, CCF parameter models, conditional probabilities, Bayesian networks, state-space or sensitivity ranges appropriate to evidence.

**Prevent double counting.** One physical/support function appearing on multiple paths keeps one identity. A common event can be factored outside parallel branches. If component reliability data already include a failure mechanism modeled separately, reconcile it. If coverage includes switch success, do not multiply switch reliability again without definition.

**Calculate importance conditionally.** Birnbaum importance compares system success probability with one block forced successful versus failed. Criticality/Fussell–Vesely and achievement/reduction worth answer different questions. Importance can shift with time/configuration and uncertainty; it is not a universal component ranking.

**Allocate reliability iteratively.** Top-down allocation assigns targets to functions/items; bottom-up prediction estimates from architecture/data. Reconcile gaps through design and evidence, not optimistic parameter adjustment. Allocation is a requirement/trade mechanism, not evidence that components meet targets.

**Propagate uncertainty.** Preserve parameter distributions/intervals and model alternatives. Shared data sources can correlate epistemic uncertainty even if failures are conditionally independent. Report percentiles or bounds, sensitivities and dominant assumptions. Validate rounding and avoid precision beyond evidence.

**Validate the structure.** Walk success paths with design, operations, software, reliability, safety and maintainability owners. Compare requirements, functional models, schematics, FMEA effects, FTA cut sets, fault-management logic, procedures and integrated tests. Challenge every parallel branch for capacity and independence.

**Validate calculation and tool.** Check all-success/all-failed limits, series/parallel closed forms, monotonicity, probabilities in $[0,1]$, units/time, small-state enumeration, repeated identities, solver/version/settings, truncation and simulation convergence. Tool output can verify declared mathematics, not architecture truth.

**Compare with evidence.** Use qualification/life tests, demonstrations, operational exposure, anomalies, maintenance and field populations with censoring and environment/configuration. Reliability demonstration for rare failure may require large exposure; no observed failures yields an upper bound, not reliability one.

**Use results for bounded action.** Improve a weak series function, remove a single point, diversify shared support, improve coverage, reduce stress, add test/data or simplify harmful redundancy. Evaluate mass, cost, power, software, maintenance, human and common-cause effects. Recalculate only after design/evidence changes.

**Maintain the model.** Bind RBD to configuration, success criteria, sources, data, assumptions, solver, reviews, actions and decisions. Update after hardware/software/interface/procedure/supplier/environment/mission changes and failures. Preserve prior baselines so historical approvals remain reconstructible.

The following executable fixture enumerates all sixteen states of two sensors, one controller and one actuator.

<!-- bijux-verify: {"id":"rbd-series-parallel-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"blocks=4\nstates=16\nminimal_paths=2\nminimal_cuts=3\nsensor_subsystem_reliability=0.99960000\nsystem_reliability=0.95991588\nsingle_sensor_reliability=0.94109400\nmodeled_reliability_gain=0.01882188\nstate_sum=1.00000000\nstructure_monotone=1\nstatus=declared_rbd_fixture_passed\nevidence=synthetic_independent_events_only\n","stderr":""}} -->
```python
names = ("sensor_a", "sensor_b", "controller", "actuator")
reliability = {"sensor_a": 0.98, "sensor_b": 0.98, "controller": 0.99, "actuator": 0.97}

def succeeds(state):
    return (state["sensor_a"] or state["sensor_b"]) and state["controller"] and state["actuator"]

states = []
system = 0.0
total = 0.0
for mask in range(1 << len(names)):
    state = {name: bool(mask & (1 << index)) for index, name in enumerate(names)}
    weight = 1.0
    for name in names:
        weight *= reliability[name] if state[name] else 1 - reliability[name]
    states.append(state)
    total += weight
    if succeeds(state):
        system += weight

minimal_paths = [
    {"sensor_a", "controller", "actuator"},
    {"sensor_b", "controller", "actuator"},
]
minimal_cuts = [{"controller"}, {"actuator"}, {"sensor_a", "sensor_b"}]
sensor_subsystem = 1 - (1 - reliability["sensor_a"]) * (1 - reliability["sensor_b"])
single_sensor = reliability["sensor_a"] * reliability["controller"] * reliability["actuator"]
monotone = all(not succeeds(left) or succeeds(right) for left in states for right in states if all(not left[name] or right[name] for name in names))
print(f"blocks={len(names)}")
print(f"states={len(states)}")
print(f"minimal_paths={len(minimal_paths)}")
print(f"minimal_cuts={len(minimal_cuts)}")
print(f"sensor_subsystem_reliability={sensor_subsystem:.8f}")
print(f"system_reliability={system:.8f}")
print(f"single_sensor_reliability={single_sensor:.8f}")
print(f"modeled_reliability_gain={system - single_sensor:.8f}")
print(f"state_sum={total:.8f}")
print(f"structure_monotone={int(monotone)}")
print("status=declared_rbd_fixture_passed")
print("evidence=synthetic_independent_events_only")
```

The fixture does not model common cause, sensor accuracy, voter/selection, controller interpretation, capacity, timing, repair, standby, environment or real failure data. Its gain is conditional on the declared independent static success events.

## Definitions and Notation

Let $B$ be block identities and $\psi: \{0,1\}^{|B|}\to\{0,1\}$ the success structure. A path $P\subseteq B$ is sufficient when $\psi(1_P)=1$ with other blocks failed, and minimal when no proper subset suffices. A cut $C$ is sufficient for failure when $\psi(1_{B\setminus C})=0$, and minimal when no proper subset causes failure.

For arbitrary independent block reliabilities, exact success is

\[
R_S(t)=\sum_{x:\psi(x)=1}\prod_i R_i(t)^{x_i}[1-R_i(t)]^{1-x_i}.
\]

Enumeration is transparent but exponential. The expression is invalid for dependent block states unless replaced by their joint distribution.

For nonrepairable lifetime $T$, $R(t)=P(T>t)=1-F(t)$. Hazard $h(t)=f(t)/R(t)$ is not failure probability; under constant hazard $h(t)=\lambda$, reliability is exponential.

## Mechanisms, Invariants, or Proof Structure

A defensible RBD conclusion follows an evidence chain:

1. **Success validity:** function, threshold, interval, configuration, state, environment and permitted degradation/recovery are explicit.
2. **Structural validity:** blocks and paths are necessary/sufficient, capacity-correct and faithful to functional architecture.
3. **Dependency validity:** common support, CCF, conditional state, switching and shared human/software/process causes are represented.
4. **Stochastic validity:** event measures, distributions, time/exposure, data population, repair and uncertainty fit the use.
5. **Computational validity:** reductions, paths/cuts, algorithms, repeated identity, solver settings and checks are reproducible.
6. **Empirical validity:** predictions are compared with applicable test/field evidence and discrepancies are investigated.
7. **Decision validity:** sensitivity, uncertainty, actions, side effects and acceptance are bounded to the declared question.

Connectivity plus arithmetic establishes none of the other gates automatically.

## Alternatives and Trade-Offs

**RBD versus fault tree.** RBD emphasizes success paths and is intuitive for redundancy/capacity; FTA emphasizes causes of an unwanted event and combinations. Static coherent models may be logical duals, but event scope and data must match.

**Analytical reduction versus state enumeration/BDD.** Series-parallel reduction is simple and reviewable; bridge networks need more general algorithms. Enumeration is exact for small independent structures; BDDs scale many Boolean models but can be ordering-sensitive.

**Static versus Markov/Petri/simulation.** Static RBDs communicate structure. Dynamic methods handle standby, order, repair, shared resources, phases and dependencies at the cost of state explosion, data demands and harder validation.

**Active versus standby redundancy.** Active redundancy avoids transition delay but increases operating exposure and shared load/environment. Standby may reduce active exposure but adds dormant failure and imperfect coverage. Compare complete architectures.

**Component versus function blocks.** Component blocks map easily to parts data but can obscure software/human/interfaces and mission functions. Functional blocks clarify success and can later map to configured items. Maintain traceability both ways.

**Prediction versus demonstration.** Prediction explores designs and combines evidence; tests directly observe bounded populations/conditions but rare failures demand exposure and may not cover systematic/common-cause behavior. Use both without claiming equivalence.

## Failure Modes and Misconceptions

- **“The RBD is the schematic.”** It is a success-logic model; physical topology is evidence used to construct it.
- **“Parallel boxes are independent.”** Independence requires evidence and explicit shared-cause treatment.
- **“Two units mean one can fail.”** Capacity, voter, support and transition may still require both.
- **“Standby equals parallel.”** Dormancy, detection, switching, delay and post-transfer performance change reliability.
- **“Failure rate is unreliability.”** A rate has inverse-time units; probability depends on a lifetime model and interval.
- **“MTBF is mission reliability.”** Mean lifetime does not determine the survival probability without a distribution and conditions.
- **“Availability proves failure-free mission.”** Repairable readiness can be high while interruptions violate mission success.
- **“More redundancy always helps.”** Added complexity and common dependencies can reduce reliability or safety.
- **“The most important block should be redesigned first.”** Importance excludes feasibility, cost, consequence, uncertainty and introduced risks.
- **“A calculated value is demonstrated reliability.”** It remains a conditional prediction until supported by applicable evidence.

## Worked Examples

### Example 1

Three independent mandatory stages have reliabilities 0.99, 0.98 and 0.97 for one mission. Series reliability is $0.99\times0.98\times0.97=0.941094$. The result is conditional on all stages being required, success definitions and independence. It does not justify replacing one stage's test with multiplication.

### Example 2

Two identical independent active pumps each have mission reliability 0.95 and either has full capacity. Parallel reliability is $1-(0.05)^2=0.9975$. If they share one power bus with reliability 0.98, system reliability becomes $0.98\times0.9975=0.97755$ under independence between bus and pump failures. The common series block dominates much of the apparent gain.

### Example 3

Three independent sensors each have reliability 0.98 and two valid signals suffice. Reliability is ${3\choose2}(0.98)^2(0.02)+(0.98)^3=0.998816$. This omits voter failure, common environment/calibration, correlated bias and whether two plausible wrong sensors defeat correctness. Hardware-up probability is not necessarily measurement-valid probability.

### Example 4

A cold standby unit has low dormant failure but requires detection, isolation, switch and startup within ten seconds. Modeling two units as active parallel assumes perfect instantaneous coverage. A state/event model includes primary lifetime, standby dormancy, demand timing, coverage chain, startup failure and mission remaining time. Tests must inject representative faults and delays.

### Example 5

Two 5 kW supplies feed an 8 kW load. Both are required, so the success structure is 2-out-of-2, not 1-out-of-2. If the system can shed load to 4 kW within an allowed interruption, there are separate full-performance and degraded-success criteria. State-dependent load sharing and thermal stress may alter post-failure reliability.

### Example 6

A component with constant hazard $2\times10^{-5}$/h over 1,000 h has $R=e^{-0.02}\approx0.98020$, not exactly $1-0.02$. The approximation is close, but constant hazard and applicable rate must be supported. Wear-out, cycling or repaired service invalidates the simple mission calculation.

### Example 7

A bridge network cannot be reduced by simple series/parallel steps. Condition on the bridge block working and failed, solve the resulting networks, and combine by total probability under independence. An enumerated truth table validates the factorization. A solver's answer remains conditional on the bridge event not sharing causes with the paths.

### Example 8

An API service is drawn as three instances in parallel, but all use one database, identity provider, region network, deployment artifact and control plane. The functional RBD includes these shared series dependencies and capacity under failover. Availability/repair may be the correct measure for a continuously restored service, while a no-interruption transaction needs mission reliability for its duration.

### Example 9

No failures occur in 300 independent device-missions. This does not prove reliability one. Under a simple binomial model, a rough one-sided 95% upper failure-probability bound is about $3/300=0.01$. Applicability, independence, configuration, environment and censoring still matter. Prediction and demonstration evidence should be combined transparently, not cherry-picked.

### Example 10

A redesign adds a redundant controller. It also adds voter software, synchronization, configuration management and a shared update pipeline. The revised RBD and FMEA/FTA include voter failure, disagreement handling, latent mismatch and common software/update events. Fault injection verifies coverage. Redundancy is accepted only if the complete architecture and uncertainty improve the intended function.

## Cross-Program Connections

- **Data engineering:** survival data, censoring, population selection, uncertainty, provenance and Bayesian updating govern block estimates.
- **API and service engineering:** replication, quorum, capacity, retries, shared backends and failover map naturally to RBDs but often require availability/state models.
- **Platform engineering:** shared control planes, regions, identity, networks and deployment pipelines are common dependencies hidden by application replicas.
- **Object-oriented programming:** interfaces and composition help define functional blocks; shared base implementations and services can create common cause.
- **Functional programming:** Boolean structure functions, immutable state enumeration and property tests support model verification.
- **Security engineering:** redundant availability paths may share compromise mechanisms; adversarial adaptation is not random independent failure.

## References

1. International Electrotechnical Commission, [IEC 61078:2016, Reliability block diagrams](https://webstore.iec.ch/en/publication/25647), edition 3.0, stability date 2028.
2. International Electrotechnical Commission TC 56, [Dependability Standards and Supporting Standards](https://tc56.iec.ch/dependability-standards/), RBD/FTA/Markov relationship summary, accessed 2026-08-31.
3. NASA, [NASA-STD-8729.1A, NASA Reliability and Maintainability Standard for Spaceflight and Support Systems](https://s3vi.ndc.nasa.gov/ssri-kb/static/resources/nasa-std-8729.1a.pdf), 2017.
4. NASA Office of Safety and Mission Assurance, [Reliability and Maintainability](https://sma.nasa.gov/sma-disciplines/reliability-and-maintainability), current policy and guidance index, accessed 2026-08-31.
5. NASA Lessons Learned, [System Reliability Assessment Using Block Diagramming Methods](https://llis.nasa.gov/lesson/825), Lesson 825, 1999.
6. NASA Kennedy Space Center, [Reliability Preferred Practices](https://extapps.ksc.nasa.gov/Reliability/Preferred_practices.html), including RBD practice PD-AP-1313, accessed 2026-08-31.
7. NIST/SEMATECH, [Reliability or survival function](https://www.itl.nist.gov/div898/handbook/apr/section1/apr122.htm), Engineering Statistics Handbook, accessed 2026-08-31.
8. NIST/SEMATECH, [Complex systems](https://www.itl.nist.gov/div898/handbook/apr/section1/apr186.htm), Engineering Statistics Handbook, accessed 2026-08-31.
9. NASA and partner agencies, [Tri-Agency Reliability Engineering Guidance: Post Mission Disposal and Extension Assessment](https://ntrs.nasa.gov/api/citations/20210024973/downloads/20210024973.pdf), 2021.
10. NASA, [Systems Engineering Handbook](https://www.nasa.gov/reference/systems-engineering-handbook/), current web edition, accessed 2026-08-31.

## Exercises

### Exercise 1

Construct an RBD for a communications function requiring sensor data, one of two processors, one of two links, and one ground receiver, while both processors and links share power. State success and independence assumptions.

### Exercise 2

Calculate mission reliability for three independent series blocks with $R=(0.99,0.97,0.96)$, then add a fully capable independent parallel duplicate to the 0.96 block. Quantify gain and limits.

### Exercise 3

Derive 2-out-of-3 reliability for identical independent $R=0.9$, identify omitted voter/common-cause behavior, and propose a corrected architecture model.

### Exercise 4

Audit a cold-standby claim modeled as $1-(1-R)^2$. Specify the state model, data and tests needed for a defensible result.

### Exercise 5

Design a validation and lifecycle-update plan for an RBD used to justify a high-consequence design trade, including uncertainty and evidence comparison.

## Answers to the Exercises

### Answer 1

Define success as delivery of valid sensor data through processing and communication to the ground receiver within required latency/capacity for configuration and mission interval. The series stages are sensor, shared power, processor subsystem, link subsystem and receiver. Processor subsystem succeeds if P1 or P2 succeeds; link subsystem if L1 or L2 succeeds only if either link independently meets capacity and routing/switching works.

Place shared power once in series, not independently inside four branches. Add any common clock, software, switch/router, antenna, spectrum/environment and ground-network dependencies. If processors and links have cross-pair compatibility constraints, a simple product of parallel subsystems may admit impossible paths; model allowed end-to-end paths explicitly.

Quantification requires compatible mission reliabilities, justified conditional independence, coverage and capacity. Validate against architecture, interface/timing tests, fault injection and FMEA/FTA. The RBD supports functional reliability for its stated interval; continuous ground service with repair may require availability modeling.

### Answer 2

Original series reliability is

\[
R_0=(0.99)(0.97)(0.96)=0.921888.
\]

An independent fully capable active duplicate makes the last stage $1-(0.04)^2=0.9984$, so

\[
R_1=(0.99)(0.97)(0.9984)=0.95876352.
\]

The modeled absolute gain is $0.03687552$. This assumes the duplicate has reliability 0.96, either unit alone has capacity, failures are independent, selection/combining is perfect, and common support is already represented. Add common power/control/environment, voter/switch, load sharing and new modes before using the gain. Component data and mission/time/environment uncertainty limit precision.

### Answer 3

At least two successes means exactly two or three:

\[
R_{2|3}=3(0.9)^2(0.1)+(0.9)^3=0.243+0.729=0.972.
\]

This is the reliability of an ideal identical-independent voting population, not necessarily system correctness. Add a voter/combiner block if required. Represent shared power, common sensor bias/environment/calibration, shared design/software/manufacturing and maintenance as common blocks or dependency/CCF models. Define whether two agreeing wrong outputs count as failure and link measurement validity to the success condition.

Corrected quantification may condition on common-event states or use a joint/state model. Test independent faults, common biased inputs, voter faults, disagreement handling, timing and degraded capacity. The value 0.972 should not survive unchanged unless those assumptions are evidenced.

### Answer 4

The active-parallel formula assumes either unit is immediately capable throughout the mission. A standby model needs primary active failure distribution; standby dormant failure/degradation; demand arrival; fault detection and diagnosis; isolation and switch command; switch hardware/software success; startup distribution; transfer deadline; standby active reliability for remaining mission; repair if credited; and shared power/environment/design/maintenance.

Represent states such as primary operating, primary failed-undetected, transfer in progress, standby operating, failed system and repaired/restored if applicable. Use Markov/semi-Markov, event tree plus conditional RBD/FTA, or simulation according to distribution/memory assumptions. Estimate coverage as the complete successful transition, not an arbitrary constant.

Test dormant storage, periodic proof test, representative primary faults, detection boundaries, switch/start timing, load/environment extremes, common support failures and long-duration post-transfer performance. Validate reduced cases analytically and propagate uncertainty. If no adequate data exist, report bounds/sensitivity instead of false precision.

### Answer 5

Freeze the decision and success definition, configuration, mission/state/time, environment, permitted degradation/repair and acceptance criteria. Map each block/path to architecture, requirements and stable configuration identities. Cross-check FMEA modes, fault-tree cuts, common-cause inventory, fault management, procedures and capacity/timing tests. Challenge every parallel path and shared support.

Independently reproduce series/parallel/$k$-of-$n$ reductions, enumerate reduced models, check minimal paths/cuts, monotonicity, units, bounds, repeated identity, solver/version/settings and dynamic/simulation convergence. Review lifetime/repair distributions, populations, exposure, censoring, parameter and model uncertainty, correlation and coverage evidence. Compare predictions with applicable qualification, life, fault-injection and field data; explain discrepancies.

Record sensitivity and uncertainty alongside the point estimate. Evaluate design alternatives for mass, cost, power, software, maintenance, human and introduced common-cause effects. Link actions and verification to the chosen configuration and authorized decision. Changes or anomalies trigger impact and recalculation; preserve prior baselines and evidence so historical decisions remain reconstructible. Neither solver agreement nor a target-crossing mean proves the design's reliability or safety.
