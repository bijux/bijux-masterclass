---
module_id: SYSENG-068
program: Systems Engineering
level: 2
module_number: 68
title: Redundancy and Common-Cause Failure
status: complete
last_verified: 2026-08-31
---

# Redundancy and Common-Cause Failure

## One-Page Review

### Governing question

Which failures must the system tolerate, which channels are genuinely independent for those failures, what shared causes can defeat them, and does verified coverage, isolation, diversity, switching, maintenance, and operational evidence justify the claimed reliability or safety gain in the exact configuration?

### Essential definitions

- **Redundancy** provides more than the minimum elements, paths, information sources, time, or capability needed to perform a function. It improves outcomes only under stated success logic and dependencies.
- **Active redundancy** operates multiple channels concurrently. **Standby redundancy** keeps one or more channels inactive or lightly loaded until detection and switching. **Load-sharing redundancy** changes component stress as channels enter or leave service.
- A **$k$-out-of-$n$ system** succeeds when at least $k$ of $n$ channels succeed for the defined mission and function. This Boolean threshold alone does not model coverage, common causes, switching, or repair.
- **Fault tolerance** is the ability to continue required behavior in the presence of specified faults. **Fail-safe** behavior moves to or remains in an acceptably safe state after specified failures; it need not preserve mission capability.
- **Fault detection, isolation, and recovery coverage** is the conditional probability that a relevant fault is detected, correctly isolated, contained, and recovered within required time. Coverage is not automatically one.
- **Common-cause failure (CCF)** is failure of two or more components or functions due to one shared event, condition, or causal mechanism. **Common-mode failure** emphasizes the same failure mode; terminology varies, so define the adopted usage.
- A **dependent failure** is statistically or causally dependent on another failure. CCF is one important subset; cascading failure, functional dependency, resource exhaustion, and maintenance coupling are others.
- **Independence** is claim-relative: physical, functional, electrical, informational, environmental, maintenance, organizational, and temporal separation must be adequate for the causal mechanisms under review.
- **Diversity** uses different principles, technologies, designs, implementations, suppliers, data, or teams to reduce shared susceptibility. Diversity can move rather than eliminate common causes.
- A **single point of failure** is an element whose specified failure alone defeats a required function or safety objective, considering the defined boundary and credited recovery.
- In the simple **beta-factor model**, a fraction $\beta$ of a component-group failure measure is assigned to a shared failure that defeats the group; the remaining fraction is treated as independent. The model is a parameterized abstraction, not a causal explanation.

### Central model, mechanism, or theorem

For $n$ identical independent active channels with success probability $p$, a $k$-out-of-$n$ function has

\[
R_{k|n}=\sum_{i=k}^{n}{n\choose i}p^i(1-p)^{n-i}.
\]

For a one-out-of-$n$ function with independent channel failure probability $q=1-p$, failure is $q^n$. If a simple shared-failure probability $q_c$ can defeat every channel and otherwise the channels fail independently with conditional probability $q_i$, then

\[
Q_{sys}=q_c+(1-q_c)q_i^n.
\]

Thus $Q_{sys}\ge q_c$ for every $n$: added identical redundancy cannot cross the common-cause floor. Real models must also account for detection/coverage, switch failure, dormant failure, load sharing, repair, test intervals, mission time, state transitions, and parameter uncertainty.

### Critical invariants

- State the protected function, mission/time, success criterion, modes, demand, configuration, boundary, and failure set before counting channels.
- Independence is demonstrated against specific mechanisms; it is never inferred solely from separate boxes, labels, teams, suppliers, or code repositories.
- Shared requirements, design concepts, data, sensors, power, clocks, networks, cooling, location, environment, tools, maintenance, operators, and management decisions are analyzed.
- Redundancy management—voters, switches, monitors, arbiters, synchronizers, cross-straps, recovery logic, and common services—is included in the reliability boundary.
- Detection, isolation, containment, reconfiguration, state reconciliation, and recovery coverage are measured separately under relevant timing and faults.
- Standby channels are checked for dormant failure and proof-test limits; active channels are checked for load sharing, interference, and fault propagation.
- Diversity receives an explicit susceptibility analysis. Superficial difference does not establish independence, and diverse channels can disagree dangerously.
- Maintenance, testing, calibration, updates, configuration, credentials, procedures, and staffing cannot silently disable or align multiple channels.
- Quantitative CCF parameters match component group, failure mode, population, environment, time/demand basis, evidence period, and model; uncertainty and sensitivity are reported.
- Additional redundancy is evaluated for new serial elements, complexity, false trips, resource contention, mass/power/cost, maintenance exposure, and recovery hazards.
- Verification includes adverse and common-cause challenges, not only one-at-a-time channel failures.
- No redundancy count, low independent-failure result, or incident-free interval proves the system safe or independent.

### Common failures

Common failures include calculating $q^n$ while assuming independence; omitting voters or switches; treating failover as instantaneous and perfect; ignoring latent standby failures; claiming physical separation while sharing power or cooling; using diverse code generated from the same requirements/model/toolchain; treating two suppliers as independent despite a common part or specification defect; testing channels sequentially while missing simultaneous environment; allowing one calibration or update to corrupt all channels; crediting recovery that cannot reconcile state; ignoring load increase after a channel loss; selecting generic beta factors without applicability; removing observed CCF events as outliers; and adding channels until complexity, false trips, maintenance, and shared services reduce rather than improve system performance.

### Compact example

With conditional independent failure probability $q_i=0.02$, ideal one-out-of-$n$ failure falls from $0.02$ for one channel to $0.0004$ for two and $0.000008$ for three. Add shared failure probability $q_c=0.001$: two-channel failure becomes $0.0013996$, and three-channel failure becomes $0.001007992$. The third channel reduces only the independent remainder; the system approaches, but never beats, $0.001$. This arithmetic illustrates one declared mixture model, not a validated CCF estimate.

### Connections

SYSENG-063 supplies reliability block logic; SYSENG-062 exposes minimal cut sets and shared dependencies; SYSENG-066 turns defeated redundancy into hazards and controls; SYSENG-067 demands an evidence-backed independence argument. Architecture, software, cybersecurity, platforms, data, human factors, maintenance, configuration, and supply chains all create or break redundancy claims.

## Governing Question

Can the program show—causally and quantitatively, within stated uncertainty—that the complete redundant function, including its management and support, tolerates the specified faults and environments without shared or cascading mechanisms defeating multiple channels or creating a worse unsafe state?

The word “redundant” is a design description, not evidence. A diagram may contain three channels while one requirement error, shared sensor, power transient, environmental event, update, operator action, or voter defect defeats all three.

## Why This Matters

Redundancy is attractive because ideal independent-failure mathematics produces dramatic improvement. Two independent channels with failure probability $10^{-3}$ appear to fail together with probability $10^{-6}$. That conclusion can be wrong by orders of magnitude when a common cause contributes even $10^{-4}$, when coverage is incomplete, or when the recovery mechanism is itself a single point.

FAA AC 25.1309-1B requires attention to common-cause and cascading effects and to design/installation techniques such as partitioning, separation, and isolation. NASA analyses emphasize that CCF can dominate highly redundant systems and that more identical channels offer diminishing benefit once a shared-failure floor controls. NRC guidance and databases show that CCF event classification, component-group definition, parameter estimation, and uncertainty are substantive analytical work rather than a generic constant pasted into every model. IAEA guidance connects independence, physical separation, functional independence, diversity, qualification, testing, and maintenance.

Redundancy can also add hazards: disagreement, spurious voting, oscillating control, split brain, stale replicas, unsafe failover, extra valves/connectors/software, shared-resource contention, maintenance errors, and greater attack surface. Engineering must compare the full architecture and operations, not celebrate channel count.

## Prerequisites and Retrieval

Before accepting a redundancy or CCF claim, retrieve:

1. required function, safety objective, mission/time, success/degraded criteria, demand profile, modes, operating envelope, and consequence of loss or spurious activation;
2. architecture and functional dependencies, channel boundaries, $k$-out-of-$n$ logic, active/standby/load-sharing state, voters, switches, arbiters, monitors, recovery, and safe state;
3. physical layout, separation, barriers, routing, fire/flood/seismic/environmental zones, pressure/energy sources, power, grounding, cooling, communications, clocks, and shared support systems;
4. requirements lineage, common design assumptions, algorithms, models, datasets, toolchains, libraries, suppliers, parts, manufacturing lots, firmware, configuration, and credentials;
5. fault models, FMEA/FMECA, fault trees/minimal cut sets, common-cause/common-mode analysis, hazard analysis, dependency analysis, PRA, Markov/state models, and uncertainty/sensitivity studies;
6. detection, isolation, containment, voting, switching, reconfiguration, restart, data/state reconciliation, degraded operation, and restoration requirements with timing and coverage evidence;
7. channel failure/demand data, CCF event records, near misses, degradations, maintenance findings, false trips, failover attempts, censored exposure, and exact population/configuration context;
8. proof-test intervals, dormant-failure detection, inspection/calibration, maintenance procedures, simultaneous outages, test bypasses, return-to-service, staffing, training, and work scheduling;
9. verification plans/results for single, multiple, latent, cascading, environmental, software, cyber, human, maintenance, and recovery faults—including negative/anomalous results;
10. changes, concessions, supplier notices, obsolescence, updates, restrictions, open assumptions, CCF parameters/posteriors, risk decisions, monitoring, and re-analysis triggers.

Perform a shared-dependency challenge: select two allegedly independent channels and trace every upstream input and downstream actuator, plus power, timing, environment, maintenance, configuration, tools, people, suppliers, and governance. Then inject one plausible disturbance at each shared point and explain how both channels remain effective or how the system reaches an acceptably safe state.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish redundancy, fault tolerance, fail-safe behavior, independence, dependence, CCF, common mode, and cascading failure;
2. compute ideal $k$-out-of-$n$ reliability and explain its independence assumptions;
3. model active, standby, load-sharing, voting, switching, coverage, and repair limitations;
4. identify shared causal mechanisms across physical, digital, human, organizational, and lifecycle domains;
5. evaluate separation, isolation, partitioning, diversity, monitoring, and recovery controls;
6. apply simple beta-factor reasoning and state its model/data limitations;
7. interpret CCF operational data with population, classification, censoring, and uncertainty;
8. design adversarial verification for independence and common-cause claims;
9. conduct redundancy trade studies including complexity, false activation, maintenance, resources, and safety;
10. communicate bounded conclusions without treating identical channels as independent by default.

## Core Exposition

**Define success before redundancy.** Name the function and minimum acceptable behavior. A triplicated controller may preserve command computation but not sensing, power, actuation, or safe state. Define whether success means full mission, degraded service, safe shutdown, data integrity, or recoverable interruption.

**Draw the complete dependency graph.** Include nominal and backup elements, voters, switches, cross-straps, detection, power, cooling, network, clocks, data, actuation, operators, procedures, and restoration. Redundant processors behind one power converter are not redundant against converter loss.

**Choose active, standby, or load sharing consciously.** Active channels give immediate availability and comparison but share exposure and can interfere. Standby reduces wear or power but adds dormant failure, detection, start/switch, warm-up, state, and proof-test concerns. Load sharing changes stress after failure, so constant independent rates may be inappropriate.

**Specify $k$-out-of-$n$ semantics.** State how abstention, invalid output, Byzantine behavior, disagreement, degraded accuracy, and late response count. Majority voting masks some faults only if inputs and voters behave within the fault model. Three wrong channels sharing one bad requirement outvote nothing useful.

**Treat coverage as a chain.** Let a fault be detected, isolated, contained, reconfigured, and recovered correctly within time. Overall coverage is not automatically the product of independent stage coverages, because the stages share sensors, logic, and conditions. Measure stage outcomes and failure modes explicitly.

**Analyze the redundancy manager.** A voter may be replicated, self-checking, monitored, bypassable, or a single point. Switching can fail open/closed, select the failed channel, interrupt both, oscillate, or corrupt state. Arbitration can split brain. Recovery can replay unsafe commands or lose safety-critical state.

**Separate causal and statistical dependence.** Statistical correlation flags non-independence but may not explain it. Causal analysis searches for shared events, conditions, mechanisms, and dependencies that inform controls. Quantitative CCF models summarize residual behavior only after a defensible component-group and evidence basis are established.

**Define the common-cause component group.** Group components sufficiently similar and coupled that one cause may affect multiple members. The grouping depends on failure mode, function, environment, design, maintenance, and operation. An overly broad group dilutes evidence; an overly narrow group hides shared susceptibility.

**Search lifecycle causes.** Requirements defects, design errors, common algorithms, manufacturing lots, contamination, installation, environmental qualification, maintenance/calibration, test equipment, software updates, data corruption, credentials, operator actions, and organizational policy can align failures long after architecture review.

**Use separation and isolation mechanistically.** Distance helps only against hazards whose effects decay with distance. Fire barriers need rating, penetrations, routing, detection, suppression, and maintenance. Electrical isolation needs transient/ground analysis. Software partitioning needs resource, privilege, timing, and failure-containment evidence.

**Use diversity with a susceptibility matrix.** Compare physical principle, technology, design, implementation, requirements interpretation, algorithms, data, tools, suppliers, teams, power, environment, communications, and maintenance. Record common elements. Diversity can introduce disagreement, integration errors, unequal performance, complex arbitration, and common specification faults.

**Prevent cascading failure.** Limit energy and fault propagation, isolate interfaces, rate-limit traffic, reserve resources, shed load, contain corrupt data, and prevent one recovery action from overloading survivors. Analyze post-failure loads and environmental conditions, not only the initiating fault.

**Design for maintainable independence.** Separate channels can be defeated by one procedure, technician, calibration source, laptop, credential, firmware package, spare lot, or simultaneous maintenance window. Use channel-aware authorization, staggered maintenance, independent verification where warranted, configuration diversity controls, and explicit return-to-service tests.

**Do not equate diversity with different vendors.** Suppliers may share components, libraries, standards interpretations, sub-tier sources, certification evidence, and vulnerabilities. Conversely, one supplier can produce meaningfully diverse implementations. Demonstrate the causal differences relevant to the feared failures.

**Quantify ideal logic first, then relax assumptions.** Independent binomial calculations provide a transparent reference. Add CCF, coverage, switching, repair, test intervals, standby failure, load dependence, and uncertainty one mechanism at a time. The difference shows which assumptions drive the claimed gain.

**Use beta-factor models within scope.** For a two-channel group, a simple model may allocate fraction $\beta$ of total failure probability/rate to a shared event and the remainder to independent events. Variants differ in definitions and treatment for larger groups. State convention; do not mix rates and probabilities or copy a beta across failure modes.

**Use richer models when needed.** Multiple Greek letter or alpha-factor models distinguish multiplicities in larger groups; shock/latent-variable models represent shared environments; Bayesian models update uncertain parameters; Markov/semi-Markov models handle switching, repair, coverage, and state-dependent rates. Complexity is useful only when supported by decisions and evidence.

**Treat data classification as analysis.** Decide whether an event is independent, common cause, potential CCF, or unavailable evidence; record cause, coupling factor, shared state, affected fraction, timing, recovery, and uncertainty. Sensitivity to reclassification can dominate parameter estimates.

**Preserve exposure denominators.** Counts need operating time, demands, population size, test opportunities, detection probability, and reporting coverage. Fleet data may not transfer across design, environment, maintenance, software, or operational policy. Zero observed CCFs does not imply zero probability.

**Distinguish simultaneous observation from common causation.** Two channels can fail close in time because one initiates a cascade, because a shared condition damages both, because surveillance discovers two older latent failures together, or by independent coincidence. Coding them identically distorts causal learning and parameter estimation. Preserve chronology, channel condition before discovery, coupling mechanism, failure-mode compatibility, and uncertainty. A “potential CCF” category is useful when evidence is incomplete; forcing uncertain events into independent or definite-common bins manufactures precision.

**Examine recovery credit after a shared event.** Equipment may remain physically recoverable, but recovery can depend on the same environment, access route, diagnostics, procedure, crew, power, or spare that the event compromised. Credit recovery only when trigger, authority, time, resources, safe intermediate states, and adverse-condition evidence are explicit. Do not assume repair independence immediately after a flood, fire, cyber compromise, bad update, or organization-wide maintenance error.

**Audit hidden synchrony.** Redundant channels often share calendar time: identical aging, simultaneous firmware rollout, common proof-test intervals, synchronized certificate rotation, or correlated workload peaks. Random-failure models that ignore synchronized exposure can miss concentrated risk. Staggering helps only if it does not leave incompatible configurations or create operational ambiguity; version compatibility must be designed and verified.

**Make the stopping rule explicit.** No analysis enumerates every imaginable shared cause. Define how method breadth, experience, consequence, novelty, design diversity, adversarial review, and residual uncertainty determine sufficient effort. A bounded conclusion states which mechanisms were challenged, which were excluded with rationale, and which operational observations will reopen the assessment.

**Verify with simultaneous and adverse challenges.** Test shared power/environment loss, common input corruption, timing/resource overload, faulty update, calibration error, maintenance bypass, network partition, security compromise, and recovery under real state. Single-channel fault injection is necessary but insufficient.

**Reassess after any channel change.** Replacing one component can improve diversity or create a new interface/common service. Updating all channels simultaneously can align latent software defects. Trace affected fault models, coverage, CCF groups, parameters, evidence, spares, procedures, and risk acceptance.

**Trade the whole system.** Added channels impose mass, power, heat, cost, interfaces, software, test, spares, training, false alarms/trips, and maintenance exposure. Compare reliability, safety, availability, diagnosability, recoverability, cybersecurity, and lifecycle cost with uncertainty. Sometimes simplification or hazard elimination is stronger than another replica.

The executable fixture below compares ideal independence with one explicitly declared shared-failure mixture.

<!-- bijux-verify: {"id":"redundancy-common-cause-floor-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"conditional_independent_failure=0.020000\nshared_failure=0.001000\nideal_n1=0.020000000\nideal_n2=0.000400000\nideal_n3=0.000008000\nccf_n1=0.020980000\nccf_n2=0.001399600\nccf_n3=0.001007992\nthird_channel_improvement_factor=1.388503\ncommon_cause_floor_respected=1\nstatus=declared_redundancy_model_consistent\nevidence=synthetic_parameters_only\n","stderr":""}} -->
```python
q_i = 0.02
q_c = 0.001

def ideal(n):
    return q_i ** n

def with_common_cause(n):
    return q_c + (1 - q_c) * q_i ** n

print(f"conditional_independent_failure={q_i:.6f}")
print(f"shared_failure={q_c:.6f}")
for n in range(1, 4):
    print(f"ideal_n{n}={ideal(n):.9f}")
for n in range(1, 4):
    print(f"ccf_n{n}={with_common_cause(n):.9f}")
print(f"third_channel_improvement_factor={with_common_cause(2) / with_common_cause(3):.6f}")
print(f"common_cause_floor_respected={int(all(with_common_cause(n) >= q_c for n in range(1, 20)))}")
print("status=declared_redundancy_model_consistent")
print("evidence=synthetic_parameters_only")
```

The one-channel mixture includes both the shared branch and conditional independent branch, so it differs from the ideal reference. The parameters are synthetic and dimensionless; no rate/probability conversion, uncertainty estimate, component population, or real independence claim is implied.

## Definitions and Notation

Let channel states be success/failure over declared mission $t$. Under independent identical success probability $p$, $X\sim Binomial(n,p)$ and $P(X\ge k)$ gives ideal $k$-out-of-$n$ reliability. Nonidentical independent channels require a Poisson-binomial calculation; dependent channels require a joint model rather than substitution of marginal probabilities.

Let $C$ denote successful fault-management coverage and $S$ successful switching/reconfiguration. A standby system's success depends on active survival, standby availability, detection, switch success, timing, and post-switch operation. Multiplying these terms is valid only where conditional structure supports it.

Let $G$ be a common-cause component group and $M$ a failure mode. A CCF parameter is indexed by $(G,M,environment,mission,data\ period,model)$; suppressing these indices risks false transfer. Let $D$ be the set of identified shared dependencies and $V(d)$ the evidence that dependency $d$ is eliminated, isolated, tolerated, or bounded.

## Mechanisms, Invariants, or Proof Structure

A defensible redundancy claim follows this chain:

1. **Function validity:** success, degraded success, safe failure, mission, demand, timing, and modes are explicit.
2. **Architecture validity:** the complete channels and management/support elements implement the claimed threshold logic.
3. **Fault-model validity:** independent, dependent, cascading, latent, spurious, Byzantine, environmental, human, cyber, and maintenance faults are scoped.
4. **Independence validity:** each relevant common mechanism is traced through physical, functional, informational, organizational, and lifecycle dependencies.
5. **Coverage validity:** detection, isolation, containment, switching, state reconciliation, and recovery work within required time and uncertainty.
6. **Quantification validity:** model, parameters, evidence population, units, mission, grouping, uncertainty, and sensitivity match the decision.
7. **Verification validity:** single and simultaneous faults, shared stresses, adverse timing, bypass, degraded modes, and recovery are challenged in applicable configuration.
8. **Lifecycle validity:** maintenance, proof testing, updates, suppliers, operations, anomalies, and changes preserve or reopen the claim.

## Alternatives and Trade-Offs

**Active versus standby.** Active redundancy gives immediate comparison and capacity but shares exposure and power. Standby can reduce wear yet adds latent failure and switching/state risks.

**Identical versus diverse.** Identical channels simplify verification, spares, and behavior but share susceptibility. Diversity may reduce selected CCFs while increasing integration, disagreement, training, and supply complexity.

**Voting versus monitored primary/backup.** Voting masks bounded channel faults but adds voter and consensus behavior. Primary/backup simplifies authority but requires trustworthy detection and transfer.

**More channels versus simpler architecture.** More channels reduce an independent tail but add serial elements and operational burden. Simplification, hazard elimination, passive protection, or stronger isolation can dominate another replica.

**Generic versus plant/product-specific CCF data.** Generic data helps sparse analysis but may mismatch design and environment. Specific data improves relevance but are scarce and censored. Use hierarchical or sensitivity reasoning rather than silent transfer.

## Failure Modes and Misconceptions

- **“Two channels square failure probability.”** Only under the declared independence and success logic.
- **“Different boxes are independent.”** Shared requirements, power, data, environment, maintenance, or decisions can defeat both.
- **“Diverse means no common cause.”** Common specification, interface, environment, or organization remains.
- **“The voter is perfect.”** Include voter, input validity, timing, disagreement, and spurious output.
- **“Standby does not fail while off.”** Dormant failure, storage degradation, unavailable state, and switch failure matter.
- **“Coverage equals detection.”** Correct isolation, containment, reconfiguration, and recovery are additional gates.
- **“Generic beta is conservative.”** Applicability and direction of bias require evidence and sensitivity.
- **“Zero observed CCF means zero risk.”** Sparse exposure and detection/reporting limits prevent that inference.
- **“A one-at-a-time test proves tolerance.”** Shared and simultaneous challenges require separate evidence.
- **“More redundancy cannot hurt.”** Complexity, propagation, false trips, resource contention, and maintenance can worsen outcomes.

## Worked Examples

### Example 1

Two pumps in active parallel each have mission failure probability 0.02. Ideal one-out-of-two failure is 0.0004. A shared contaminated supply can disable both with probability 0.001; the declared mixture gives 0.0013996. The independence-only answer understates failure more than threefold, and the result remains bounded by the assumed mixture and synthetic inputs.

### Example 2

A 2-out-of-3 flight-control voter masks one failed processor, but all processors share one air-data source. Frozen data can produce three consistent wrong outputs. The redesign adds diverse sensing and plausibility constraints; triplication remains useful for processor faults but never supported sensor independence.

### Example 3

A cold-standby generator passes monthly start tests. During an outage it fails because the transfer switch seized. The reliability boundary had omitted detection, switch power, starting battery, fuel, warm-up, and load acceptance. A standby claim is rebuilt as a state transition with proof-test and coverage evidence.

### Example 4

Two software implementations use different languages and vendors but the same ambiguous requirement and generated test oracle. Both command an unsafe transition. Diversity review records shared specification and oracle, then adds an independently derived safety monitor. Different syntax was not causal diversity.

### Example 5

Physically separated network paths share one routing control plane and credential authority. A bad policy deployment withdraws both. Configuration isolation, staged rollout, independent break-glass routing, and failure injection address the actual mechanism; cable separation addressed only physical hazards.

### Example 6

Three cooling trains share a room. Flooding disables their motors and switchgear. Moving one train behind a rated boundary improves spatial diversity only after penetrations, drains, access, detection, and maintenance of the barrier are verified under the design-basis flood.

### Example 7

After one load-sharing converter fails, survivors exceed thermal ratings and cascade. A static parallel RBD misses state-dependent load. A Markov or load-flow model plus thermal tests supports controlled shedding and derating; redundancy without post-failure capacity was illusory.

### Example 8

A technician applies the same incorrect calibration file to four channels. Channel-aware credentials, independent file validation, staggered work, and comparison against a physical reference reduce coupling. Blaming the technician would miss the configuration system that enabled simultaneous corruption.

### Example 9

Fleet data contain one definite CCF, two potential CCFs, and many independent failures. Reclassifying potential events materially changes beta. The analyst reports coding rationale and sensitivity instead of one precise estimate. Data classification uncertainty is part of the result.

### Example 10

A fourth identical channel lowers the independent tail but adds heat, common software, another interface, and maintenance demand while the shared-failure floor dominates. Trade analysis selects three channels plus better isolation, environmental protection, and update controls. “More” is rejected for a bounded architectural reason.

## Cross-Program Connections

Reliability engineering supplies $k$-out-of-$n$, state, repair, and uncertainty models. Safety engineering identifies consequences and control independence. Software and platform engineering contribute replication, consensus, partitioning, rollout, and shared-service failure. Data engineering governs replicated-state correctness and lineage. Cybersecurity tests common credentials/control planes. Human factors, maintenance, and configuration management govern lifecycle coupling.

## References

1. Federal Aviation Administration, [AC 25.1309-1B: System Design and Analysis—active record](https://www.faa.gov/regulations_policies/advisory_circulars/index.cfm/go/document.information/documentID/1043037), 2024.
2. Federal Aviation Administration, [AC 25.1309-1B: System Design and Analysis](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_25.1309-1B.pdf), 2024.
3. NASA, [Common Cause Failures Dominate and Defeat Redundancy](https://ntrs.nasa.gov/citations/20240013667), 2024.
4. NASA, [Common Cause Failure Modes](https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20110015733.pdf), 2011.
5. NASA, [Reliability of Diverse Redundant Systems](https://ntrs.nasa.gov/api/citations/20160001252/downloads/20160001252.pdf), 2016.
6. NASA, [Reliability Impacts in Life Support Architecture and Technology Selection](https://ntrs.nasa.gov/api/citations/20120006481/downloads/20120006481.pdf?attachment=true), 2012.
7. U.S. Nuclear Regulatory Commission, [NUREG-2225: Basis for the Treatment of Potential Common-Cause Failure](https://www.nrc.gov/reading-rm/doc-collections/nuregs/staff/sr2225/index), 2018.
8. U.S. Nuclear Regulatory Commission, [Availability of Common-Cause Failure Database](https://www.nrc.gov/reading-rm/doc-collections/gen-comm/admin-letters/1998/al98004), 1998.
9. U.S. Nuclear Regulatory Commission, [NUREG/CR-7151: Fault Injection-Based Dependability Assessment for Digital I&C Systems](https://www.nrc.gov/reading-rm/doc-collections/nuregs/contract/cr7151/index), 2012.
10. International Atomic Energy Agency, [SSG-39: Design of Instrumentation and Control Systems for Nuclear Power Plants](https://nucleus.iaea.org/sites/nss-oui/Published%20Collections/m_3df5a9eb-7e9b-4968-a0d6-4864db84d434/m_3df5a9eb-7e9b-4968-a0d6-4864db84d434__18_0.Html), 2016.

## Exercises

### Exercise 1

Analyze a 2-out-of-3 active sensor architecture. Compute ideal reliability, enumerate shared dependencies, add imperfect voter/coverage and one CCF model, and state evidence limits.

### Exercise 2

Design cold-standby power for a safety function. Model dormant failure, proof testing, detection, transfer, start, warm-up, fuel, load acceptance, repair, and common environmental hazards.

### Exercise 3

Build a diversity susceptibility matrix for two independently developed software channels. Cover requirements, algorithms, data, tools, libraries, hardware, suppliers, teams, environment, interfaces, and operations.

### Exercise 4

Review a fleet CCF dataset containing definite, potential, and independent events. Define the component group, coding rules, denominators, uncertainty, sensitivity, and transfer limits.

### Exercise 5

Compare adding a fourth identical channel with redesigning separation and common services. Include reliability, safety, false trips, complexity, maintenance, cyber exposure, resources, verification, and lifecycle cost.

## Answers to the Exercises

### Answer 1

For independent channel success $p$, ideal reliability is $3p^2(1-p)+p^3$. This assumes identical independent binary outcomes and a perfect voter. Enumerate common sensing principle, mounting/environment, power, clock, network, calibration, requirements, algorithms, voter, maintenance, and update. Add voter success and conditional coverage through an explicit event/state model, not blind multiplication. A beta/mixture term can bound shared failure only after group/mode/data definition. Report parameter and model uncertainty; arithmetic does not prove independence.

### Answer 2

Model states for primary operation, detected failure, transfer, standby start/warm-up, load acceptance, degraded service, repair, and total loss. Standby availability depends on dormant failure accumulated between proof tests, test effectiveness, start battery/fuel, switch and controls. Challenge flood, fire, temperature, ventilation, common fuel contamination, shared switchgear, procedure, maintenance outage, and cyber/control loss. Verification combines proof-test data, transfer/load demonstrations, environmental qualification, fault injection, and representative operations; conclusions apply only to tested intervals/configuration.

### Answer 3

Rows are shared-cause classes and columns the two channels. Record common/different requirement interpretation, hazard assumptions, algorithms, training/test data, compiler/toolchain, libraries, OS/runtime, hardware, supplier/sub-tier, team/review, timing/power/environment, interfaces, deployment, monitoring, and maintenance. For each common cell, identify a plausible fault, prevention/detection evidence, and residual coupling. Different languages alone score little if requirements and oracle are shared; diverse algorithms may still share corrupt input. Also assess disagreement/arbitration hazards introduced by diversity.

### Answer 4

Define the group by comparable design, function, failure mode, environment, maintenance, and observation period. Preserve definite and potential labels with cause/coupling evidence; define independent-event criteria and detection/reporting rules. Denominators include component time or demands, population, surveillance opportunities, and censoring. Estimate under multiple potential-event weights/classifications and report uncertainty. Compare plant/product-specific and generic populations. Transfer requires similarity in design, environment, procedures, software, and era; otherwise use sensitivity or hierarchical reasoning rather than declaring the generic estimate conservative.

### Answer 5

Baseline ideal and dependence-aware models show whether the fourth channel affects the dominant cut sets. Then include voter/input changes, heat/power, interfaces, false votes/trips, diagnostics, spares, testing, procedures, common software/update, cyber control plane, and maintenance exposure. The separation alternative may remove shared power/cooling/location and improve evidence for existing channels without another replica. Compare mission/safety outcomes, uncertainty, mass/power/cost, verification burden, repair, and change risk. Select the option with the stronger whole-system risk argument; if the CCF floor dominates, isolation/redesign commonly provides more credible benefit than another identical channel.
