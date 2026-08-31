---
module_id: SYSENG-062
program: Systems Engineering
level: 2
module_number: 62
title: Fault Trees
status: complete
last_verified: 2026-08-31
---

# Fault Trees

## One-Page Review

### Governing question

How can engineers deductively decompose one precisely defined undesirable event into logically sufficient combinations of causes, validate the model against real system behavior, and quantify it without silently assuming independence, simultaneity, completeness, or data precision?

### Essential definitions

- A **fault tree analysis (FTA)** is a top-down deductive analysis that starts with a defined undesirable **top event** and develops combinations of lower-level events sufficient to produce it under declared boundaries and assumptions.
- A **fault** is an abnormal condition that may arise from failure, external disturbance, human action, software behavior, or state/configuration. A component failure is only one source of fault.
- An **intermediate event** is produced by lower events through a gate. A **basic event** is not developed further in that tree because it is at the chosen resolution or is quantified directly.
- An **undeveloped event** is intentionally not expanded because information, scope, or consequence does not justify development. Its reason and treatment must be visible.
- An **OR gate** means its output occurs when at least one input event occurs. An **AND gate** means all input events occur within the modeled mission/state/timing semantics. A gate is Boolean logic, not a drawing of physical flow.
- An **inhibit condition** qualifies an event under a stated enabling condition. A **house event** represents a condition fixed true or false for a scenario/configuration; misuse can hide state uncertainty.
- A **cut set** is a set of basic events whose joint occurrence implies the top event. A **minimal cut set (MCS)** has no proper subset that is itself a cut set.
- A **prime implicant** is a minimal sufficient assignment in Boolean logic; for coherent positive trees it corresponds to a minimal cut set. Noncoherent trees with complemented events need more careful treatment.
- A **coherent tree** is monotone: changing a basic event from nonfailed to failed cannot make the top event false. NOT/success conditions can create a noncoherent model.
- **Qualitative evaluation** finds logic structure, MCSs, single points and dependencies. **Quantitative evaluation** combines event probabilities/frequencies under a specified probabilistic model.
- **Common-cause failure (CCF)** causes multiple modeled components or channels to fail from a shared mechanism. **Dependency** also includes functional, environmental, operational, maintenance, software, power, support, and recovery coupling.
- An **importance measure** describes sensitivity or contribution under a model, such as Birnbaum, Fussell–Vesely, risk achievement worth, or risk reduction worth. It is not an intrinsic property independent of top event, mission, configuration, data and dependencies.

### Central model, mechanism, or theorem

Let basic event indicators be $x=(x_1,\ldots,x_n)\in\{0,1\}^n$ and top-event structure function $\phi(x)$. For a coherent tree, $x\le y$ componentwise implies $\phi(x)\le\phi(y)$. OR and AND gates implement

\[
OR(x_1,\ldots,x_n)=1-\prod_i(1-x_i),\qquad AND(x_1,\ldots,x_n)=\prod_i x_i
\]

for binary indicators. After Boolean reduction, a coherent top event can be written as an OR of MCS conjunctions:

\[
T=\bigvee_{K\in\mathcal K}\bigwedge_{i\in K}x_i.
\]

For independent basic events with probabilities $q_i$, a single AND product is $\prod q_i$, and an OR of mutually independent/disjoint branches can be evaluated by complement. The rare-event approximation

\[
P(T)\approx\sum_{K\in\mathcal K}\prod_{i\in K}q_i
\]

neglects intersections among cut sets. It can overcount, and independence of basic events is never created by drawing separate symbols.

### Critical invariants

- The top event states system/function, failure condition, performance threshold, state/mission phase, duration, environment and configuration; vague “system failure” is rejected.
- Physical and analytical boundaries, success criteria, initial conditions, allowed recovery, human/software behavior, support systems and truncation rules are explicit.
- Development follows immediate, necessary and sufficient causes at one abstraction level; gates express causal logic, not chronology or proximity.
- Repeated basic events use one stable identity. Copying a shared event as independent occurrences corrupts both cut sets and quantification.
- AND gates receive special challenge for actual joint sufficiency, timing/window, state, ordering, shared cause, detection and recovery assumptions.
- A logical model is validated against architecture, requirements, FMEA, hazards, interfaces, procedures, software, tests and operational experience.
- MCS generation is checked for absorption and truncation effects. Single-event cut sets and high-consequence low-order sets receive explicit disposition.
- Quantification separates probabilities from frequencies/rates and matches mission-time, demand, repair, standby, sequence and state semantics.
- Independence, exclusivity and common-cause/dependency assumptions are justified. Parameter sources, uncertainty, population and applicability are configuration-controlled.
- Importance measures retain definitions and context; rankings do not alone prescribe design changes or prove causality.
- Model and data uncertainty are reported; point estimates do not imply completeness or precision.
- Changes, anomalies and controls update the tree, linked evidence and affected risk decisions while retaining prior baselines.

### Common failures

Common failures include an ambiguous top event; mixing mission phases; stopping at component names; developing causes that are not sufficient; using AND when events are sequential alternatives; using OR for mutually required conditions; treating a gate as hardware; duplicating common power as independent events; omitting software, human, environmental and maintenance causes; ignoring success/failure of detection and recovery; using constant failure rate for demand or repaired behavior; multiplying dependent probabilities; summing overlapping cut sets as exact; truncating without bounding omitted contribution; using complemented events casually; trusting tool-generated cut sets without a truth-table or independent check; ranking by one importance measure; and treating a small top probability as proof that hazards or scenarios are complete.

### Compact example

A synthetic coherent tree defines loss of cooling as common power loss OR both pumps unavailable OR sensor and controller failure. Enumeration of all 32 basic-event states confirms three MCSs: `{power}`, `{pump_a,pump_b}`, and `{sensor,controller}`. With declared independent probabilities, exact enumeration gives 0.00239836; summing rare cut-set products gives 0.00240000, 0.0684% high. This validates only the declared Boolean fixture and arithmetic—not the event definitions, independence, rates, mission model, completeness or real cooling safety.

### Connections

SYSENG-061 supplies bottom-up modes/effects; SYSENG-062 begins from one end condition and exposes combinations. SYSENG-063 expresses success logic through reliability block diagrams, SYSENG-064 adds repair/availability, and later common-cause, hazard, PRA and resilience modules refine dependencies, sequences and recovery. The same physical architecture can require several trees because each top event and mission context defines a different question.

## Governing Question

Can an independent reviewer reproduce the top-event logic and minimal cut sets, challenge every gate and repeated event against system behavior, reconstruct every probability/frequency and dependency treatment, assess uncertainty and truncation, and understand exactly which risk decision the tree supports?

FTA is powerful precisely because it restricts the question. It does not enumerate everything that can go wrong; it asks what combinations can cause one stated condition. If the top event, boundaries or causal knowledge are weak, polished Boolean output gives false confidence.

## Why This Matters

Complex failures often arise from combinations of individually benign events: a component fault plus unavailable detection, an initiating event plus failed isolation, two redundant channels disabled by common maintenance, or a software command combined with an unsafe plant state. FTA reveals such combinations, single points, shared dependencies, diagnostic/recovery needs, test targets and design leverage.

IEC 61025:2006 remains the published FTA standard with a stability date of 2029 while a third edition is in progress. It covers application, assumptions, events, failure modes, identification rules and symbols. The NRC Fault Tree Handbook codifies construction and evaluation, and NASA's aerospace handbook adapts the method to risk-informed aerospace decisions. NASA guidance consistently describes FTA as top-down Boolean logic and notes its core limitation: relevant top events and contributors must first be identified.

Quantitative results can support probabilistic risk assessment, reliability allocation, design trade, operations, maintenance and test planning. They are conditional models. A value such as $2\times10^{-5}$ must name whether it is probability per mission, frequency per year, unavailability at a time, or another measure; otherwise comparison is meaningless.

## Prerequisites and Retrieval

Before building or accepting a tree, retrieve:

1. decision, top-event owner, consequence and acceptance need, applicable standards/contracts, analysis depth, review independence and update triggers;
2. exact system/function boundary, performance threshold, configuration, mission phase/state, duration, environment, initial conditions and success criteria;
3. architecture, interfaces, energy/material/information/control paths, redundancy, support utilities, software, humans, procedures, maintenance and recovery;
4. requirements, hazards, FMEA, event trees, common-cause analysis, reliability/availability models, fault-management design and prior trees;
5. basic-event identity and taxonomy, failure/demand/repair semantics, latent exposure, diagnostic coverage, state applicability and development rationale;
6. data sources, populations, stress/environment, priors/posteriors, censoring, units, uncertainty, correlation and configuration/effectivity;
7. Boolean gate definitions, dynamic/inhibit/house-event semantics, transfer conventions, repeated-event policy and tool/version;
8. cut-set solver, truncation thresholds, quantification algorithm, dependency/CCF model, importance measures and uncertainty/sensitivity method;
9. test, anomaly, incident, field, maintenance, supplier and operator evidence, including successful recovery and control failures;
10. action/change linkage, verification, residual-risk disposition, model ownership, baseline/export, reproducibility and long-term accessibility.

Use a retrieval test: request the top event's plain-language definition, one MCS and its physical story, every repeated/shared dependency, exact basic-event evidence and units, quantification command/version, uncertainty result, truncation bound, linked action/test and authorized conclusion. If only the diagram or top number is available, the analysis is not independently reviewable.

## Learning Objectives

After completing this module, you should be able to:

1. define top, intermediate, basic and undeveloped events plus OR, AND, inhibit, house and transfer semantics;
2. construct a top-down tree using immediate necessary and sufficient causes at consistent abstraction;
3. translate coherent trees into Boolean expressions and derive/validate minimal cut sets;
4. distinguish coherent and noncoherent models and know when simple MCS treatment is insufficient;
5. compute exact small-tree probability and rare-event approximations under explicit independence assumptions;
6. separate probability, frequency, rate and unavailability and select mission/demand/repair models accordingly;
7. identify repeated events, CCF, functional/environmental/software/human/maintenance dependencies and recovery coupling;
8. interpret importance, uncertainty, sensitivity and truncation without overclaiming design priority;
9. validate and maintain fault trees against architecture, complementary analyses, tests and field evidence;
10. communicate bounded results and limitations for risk-informed decisions.

## Core Exposition

**Define one top event.** Use observable criteria: “loss of commanded cooling below 80% required flow for more than 10 seconds during ascent configuration C7.” Identify consequence separately. Avoid combining “loss or fire or degraded control”; those need separate trees or a precisely defined composite.

**Set ground rules.** State whether upstream power, operator action, software, external events, maintenance, detection, automatic/manual recovery, repair and multiple failures are in scope. State mission duration and initial states. House-event scenario switches can specialize one master tree, but every resulting scenario needs controlled interpretation.

**Develop immediate causes.** Ask what direct states are necessary or sufficient for the current event. The first level might be supply unavailable OR distribution blocked OR heat-rejection capacity insufficient. Do not jump immediately to arbitrary part failures; preserve causal levels so reviewers can challenge completeness.

**Apply the sufficiency test.** For an OR gate, each input alone under stated context must cause the output. For an AND gate, all inputs together must cause it and removing one must break that causal combination. If not, the gate or event definition is wrong/incomplete. Mechanistic reasoning precedes symbols.

**Name events as conditions.** “Pump A fails to deliver required flow” is analyzable; “Pump A” is not. Include state/mission qualifiers where needed. Distinguish primary hardware failure, command unavailable, power unavailable, isolation closed, maintenance disabled and insufficient capacity; their causes, data and treatments differ.

**Reuse identity.** A shared bus loss appearing in multiple branches is one basic event. Transfer gates modularize repeated subtrees but do not create independence. Stable IDs let solvers absorb supersets and let change impact find every use.

**Stop deliberately.** Stop development when an event has suitable data, is owned by another controlled tree, is outside boundary, or further detail does not affect the decision. Mark undeveloped events and rationale. A diamond symbol is a visible limitation, not a probability source.

**Challenge AND gates.** AND combinations drive apparent redundancy gains and are common error sites. Ask whether events must overlap in time, whether one causes the other, whether detection/recovery changes the window, and whether common causes bypass the gate. For standby systems, order, coverage and switch success may require Markov, dynamic fault tree or sequence models.

**Derive Boolean form.** Recursively substitute gates, distribute conjunction over disjunction, remove duplicates ($A\land A=A$), and apply absorption ($A\lor A B=A$). The remaining products are MCSs for coherent positive logic. Use independent truth-table enumeration for small fixtures and tested solvers for large trees.

**Handle NOT sparingly.** Complemented success events can represent noncoherent logic where failure of another item prevents the top event. Standard monotone cut-set intuition and importance measures may fail or change sign. Often event trees, state-transition or dynamic models communicate sequence/state more faithfully.

**Quantify events consistently.** A nonrepairable component with constant hazard $\lambda$ has failure probability $1-e^{-\lambda t}$, approximately $\lambda t$ only when small. An on-demand protection has probability of failure on demand. A repairable component has time-dependent or steady-state unavailability. Mixing these without scenario semantics is dimensionally wrong.

**Calculate exact overlap when possible.** For $T=A\lor B$, $P(T)=P(A)+P(B)-P(A\cap B)$. Summing cut-set products omits intersections. Binary decision diagrams or inclusion–exclusion can provide exact Boolean probability under independent basic events; dependencies still require a valid joint model.

**Model common cause explicitly.** Redundant channels may share design, manufacturing lot, software, environment, power, cooling, calibration, test, maintenance or operator action. Add common-cause events/model parameters supported by evidence and sensitivity. A beta-factor or other model is a conditional abstraction, not proof that all dependencies are captured.

**Treat human and software events as contextual.** Define the action/behavior, cues, timing, procedure, workload, interface, system state and recovery. Software events often depend on triggering states and systematic defects rather than random constant rates. Human reliability and software assurance require complementary evidence; guessed probabilities should not dominate a precise-looking total.

**Include detection and recovery correctly.** If top-event prevention depends on alarm, diagnosis, switching and response, model their failure under available time and conditions. Avoid double credit across protection layers sharing sensors, logic, power or personnel. Recovery success belongs only where the top definition permits recovery.

**Compute importance with context.** Birnbaum importance is the change in top probability between forcing event failed and working. Fussell–Vesely describes the fraction of top risk involving an event under a model. Risk achievement/reduction worth compare forced states. High values identify leverage/sensitivity, not necessarily cheapest action or root cause; uncertainty and feasibility matter.

**Quantify uncertainty.** Separate aleatory variability from epistemic uncertainty where useful. Propagate parameter distributions or intervals, perform sensitivity and report model alternatives. Rare events often have sparse data and correlated uncertainty. More digits do not reduce epistemic uncertainty.

**Control truncation.** Large trees may omit cut sets above order or below contribution thresholds. State algorithm and thresholds, demonstrate convergence/sensitivity, and bound omitted contribution where possible. Truncation can hide combinations important under changed probabilities or configurations.

**Validate qualitatively.** Walk down and bottom-up with domain owners. Compare FMEA modes/effects, hazards, interface models, procedures, state machines, common-cause lists and historical events. Inject each MCS as a physical narrative. Confirm impossible combinations, mutual exclusions, timing and recovery.

**Validate quantitatively.** Check units, bounds $0\le P\le1$, limiting cases, duplicate/repeated identities, exact enumeration for reduced trees, alternative solvers, rare-approximation error, parameter traceability, sensitivity and Monte Carlo/analytical agreement where applicable. Tool success is not model validity.

**Use results for action.** Single points may drive elimination or verified containment; repeated support events may drive diversity; uncertain high-importance events may drive tests/data; diagnostic/recovery combinations may drive fault-management changes. Recalculate after implementation and assess introduced dependencies.

**Maintain lifecycle evidence.** Bind the tree to requirements, hazards, architecture/configuration, FMEA, data, solver, results, reviews and decisions. Update after design/software/procedure/supplier/environment changes and test/field anomalies. Preserve prior baselines so approvals remain reconstructible.

The following fixture enumerates a five-event coherent tree and independently checks declared MCS sufficiency/minimality.

<!-- bijux-verify: {"id":"fault-tree-enumeration-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"basic_events=5\nstates=32\nminimal_cut_sets=3\ncut_sets=controller+sensor,power,pump_a+pump_b\ncut_sets_valid=1\nexact_top_probability=0.00239836\nrare_event_approximation=0.00240000\nrelative_error_percent=0.0684\ncoherent=1\nstatus=declared_fault_tree_fixture_passed\nevidence=synthetic_independent_events_only\n","stderr":""}} -->
```python
names = ("power", "pump_a", "pump_b", "sensor", "controller")
probability = {"power": 0.001, "pump_a": 0.01, "pump_b": 0.02, "sensor": 0.03, "controller": 0.04}

def top(state):
    return state["power"] or (state["pump_a"] and state["pump_b"]) or (state["sensor"] and state["controller"])

states = []
exact = 0.0
for mask in range(1 << len(names)):
    state = {name: bool(mask & (1 << index)) for index, name in enumerate(names)}
    weight = 1.0
    for name in names:
        weight *= probability[name] if state[name] else 1 - probability[name]
    states.append(state)
    if top(state):
        exact += weight

cut_sets = [frozenset(("power",)), frozenset(("pump_a", "pump_b")), frozenset(("sensor", "controller"))]
valid = True
for cut_set in cut_sets:
    asserted = {name: name in cut_set for name in names}
    valid = valid and top(asserted)
    valid = valid and all(not top({name: name in cut_set - {removed} for name in names}) for removed in cut_set)
rare = 0.0
for cut_set in cut_sets:
    contribution = 1.0
    for name in cut_set:
        contribution *= probability[name]
    rare += contribution
coherent = all(not top(left) or top(right) for left in states for right in states if all(not left[name] or right[name] for name in names))
print(f"basic_events={len(names)}")
print(f"states={len(states)}")
print(f"minimal_cut_sets={len(cut_sets)}")
print("cut_sets=" + ",".join("+".join(sorted(cut_set)) for cut_set in sorted(cut_sets, key=lambda value: tuple(sorted(value)))))
print(f"cut_sets_valid={int(valid)}")
print(f"exact_top_probability={exact:.8f}")
print(f"rare_event_approximation={rare:.8f}")
print(f"relative_error_percent={100 * (rare - exact) / exact:.4f}")
print(f"coherent={int(coherent)}")
print("status=declared_fault_tree_fixture_passed")
print("evidence=synthetic_independent_events_only")
```

The fixture imports only the standard-library math product through a bounded expression. It assumes five independent Bernoulli events for one mission. It does not represent rates, repair, sequence, standby, common cause, diagnostics, human/software dependence or real cooling behavior.

## Definitions and Notation

For event set $B$, a structure function $\phi: \{0,1\}^{|B|}\rightarrow\{0,1\}$ maps basic states to the top state. A set $K\subseteq B$ is sufficient when $\phi(1_K)=1$ with other events false, and minimal when every $K\setminus\{e\}$ is insufficient.

For independent Bernoulli basic events, exact probability is

\[
P(T)=\sum_{x:\phi(x)=1}\prod_i q_i^{x_i}(1-q_i)^{1-x_i}.
\]

This enumerative expression demonstrates semantics but scales exponentially. Solvers use Boolean reduction, inclusion–exclusion, BDDs or other algorithms. Algorithm efficiency does not repair invalid event probability or dependence assumptions.

Define Birnbaum importance for event $i$ as

\[
I_B(i)=P(T\mid x_i=1)-P(T\mid x_i=0).
\]

It is sensitivity to forcing one event state within the rest of the model, not probability that event $i$ “caused” an observed accident.

## Mechanisms, Invariants, or Proof Structure

A defensible FTA conclusion follows this chain:

1. **Top-event validity:** criteria, system boundary, configuration, mission/state/time and consequence are unambiguous.
2. **Causal completeness within scope:** each gate captures immediate necessary/sufficient contributors using architecture and multidisciplinary evidence.
3. **Logical validity:** identities, gates, complements, transfers, house/inhibit conditions and MCSs match the declared Boolean semantics.
4. **Physical validity:** each MCS has a credible physical/operational story; impossible combinations and mutual exclusions are removed.
5. **Probabilistic validity:** event measures/units/time bases, dependencies, common cause, recovery, data applicability and uncertainty match the question.
6. **Computational validity:** solver/version/settings, reduction, truncation, exact small cases and independent checks are reproducible.
7. **Decision validity:** importance/sensitivity and limitations inform owned actions, verification and authorized residual disposition.

None of these gates proves omitted top events or unknown contributors absent. The conclusion is conditional on declared scope and knowledge.

## Alternatives and Trade-Offs

**FTA versus FMEA.** FTA efficiently targets one high-consequence outcome and combinations; FMEA systematically scans modes bottom-up. FTA can miss unselected top events; FMEA can miss combinations. Cross-link both.

**Fault tree versus reliability block diagram.** FTA models failure logic and can include nonhardware causes; RBD expresses success paths and is often intuitive for repairable availability. Duals match only under compatible coherent static assumptions.

**Static versus dynamic models.** Static Boolean trees are transparent and tool-supported. Order, standby, repair, resource contention, control loops and phased missions may need dynamic trees, Markov/state-space, Petri nets or simulation, with higher data and validation cost.

**Exact versus rare-event quantification.** Exact BDD/enumeration handles overlap under independent basics; rare sums are simple and often close when cut sets are very rare. Always calculate approximation error on representative reduced models and check dependencies.

**Detailed trees versus modular trees.** One enormous tree enables integrated reduction but overwhelms ownership/review. Modular transfer trees support domain ownership but require controlled interfaces, shared IDs and configuration.

**Point estimates versus distributions/intervals.** Points communicate easily but hide uncertainty. Distributions/intervals enable uncertainty and sensitivity yet can imply unjustified distributional knowledge. Preserve raw evidence and model alternatives.

## Failure Modes and Misconceptions

- **“The tree proves the top event cannot happen.”** It models identified contributors; missing causes remain possible.
- **“An AND gate means two failures happen at the same instant.”** Timing semantics must be defined; overlap, sequence and recovery may matter.
- **“Separate branches are independent.”** Shared design, support, environment, people and software create dependencies across drawings.
- **“OR probabilities can always be added.”** Intersections must be subtracted; rare-event sums are approximations.
- **“A rate times mission time is always probability.”** Only under appropriate nonrepairable constant-hazard, small-probability assumptions.
- **“MCS order equals risk.”** Event probabilities, dependencies, consequence, uncertainty and feasibility matter; a higher-order common configuration may dominate.
- **“Highest importance identifies root cause.”** Importance is model sensitivity/contribution, not causal investigation.
- **“Redundancy guarantees an AND gate.”** Common cause, switching, support and latent faults can bypass nominal redundancy.
- **“The tool validated the tree.”** A solver validates syntax/logic it implements; physical causality and data need independent review.
- **“One tree covers the system.”** Different top events, mission phases and configurations require distinct or scenario-controlled models.

## Worked Examples

### Example 1

Replace “vehicle failure” with “loss of commanded braking deceleration below 3 m/s² for more than 500 ms during autonomous operation on dry pavement, configuration R4.” This names threshold, persistence, mode and configuration. Collision is a consequence, not necessarily the top event. Separate trees may address inadvertent braking and loss under wet/low-friction conditions.

### Example 2

Top event is no coolant flow. Immediate causes are supply unavailable OR flow path blocked. Supply unavailable is both pumps unavailable; path blocked is either isolation closed or line obstruction. Expanding pump unavailability reveals shared power and command. Shared power is one repeated event, so it becomes a single-event MCS—not two independent power failures hidden under the pump AND gate.

### Example 3

For $T=A\lor AB$, absorption gives $T=A$. A solver reporting `{A}` and `{A,B}` as minimal is wrong or unminimized. For $(A\lor B)\land(C\lor D)$, distributivity gives four MCSs `{A,C}`, `{A,D}`, `{B,C}`, `{B,D}`. A truth table independently checks sufficiency/minimality.

### Example 4

Two independent events with probabilities 0.01 and 0.02 under OR have exact probability $0.01+0.02-(0.01)(0.02)=0.0298$, not 0.03. The sum is 0.6711% high relative to exact. At larger probabilities or many overlapping cut sets, error grows. If events are dependent, even the product intersection is unsupported.

### Example 5

A protection top event requires initiating demand AND protection failure. Protection failure includes sensor failure, logic failure, actuator failure, or power loss. The sensor and logic share power, and actuator proof testing creates downtime. A static product of demand frequency and independent failure-on-demand values misses shared power and test state. Model scenario frequency, unavailability on demand, common cause and maintenance state consistently.

### Example 6

A standby pump succeeds only if demand is detected, switch command arrives, valve reconfigures and pump starts before inventory is depleted. Static AND/OR may approximate mission failure but loses sequence and coverage. An event tree or dynamic/state model makes detection, switch order, delays and recovery explicit. Use the fault tree for constituent failures and link it to sequence logic.

### Example 7

A software watchdog and protected application share scheduler and clock. Treating their failures as independent produces a squared small probability. The tree adds scheduler/clock common causes and unsafe configuration/update events; probabilities remain uncertain and scenario-based. Fault injection and assurance evidence inform coverage, but absence of random-rate data is not permission to enter an arbitrary tiny number.

### Example 8

Birnbaum importance for a bus event is high because forcing bus loss changes many branches. Risk reduction worth may also be high, but redesigning the bus could be infeasible; improving environmental protection or adding diverse backup may be better. Conversely, a low-probability event with weak data can warrant testing. Importance is one decision input alongside uncertainty, cost, consequence and introduced risk.

### Example 9

A solver truncates all cut sets above order three. The top event has many order-four combinations with moderate demand probability. The analyst varies order/probability thresholds, reports convergence and bounds omitted mass using an alternative calculation. The displayed risk changes materially, so order-three results are unsuitable for acceptance though useful for screening.

### Example 10

Field evidence shows a maintenance procedure can disable both redundant channels. Add one shared maintenance basic event, revise MCSs and probabilities using applicable exposure, link affected configurations and introduce independent restoration verification. Recalculate after implementation and retain the prior tree used for earlier decisions. The update improves known modeling; it does not prove no other shared action exists.

## Cross-Program Connections

- **Data engineering:** probability populations, censoring, provenance, correlation, Bayesian updating and uncertainty propagation determine quantitative credibility.
- **API and service engineering:** timeouts, shared dependencies, retries, failure-on-demand, stale data and partial failure supply events whose independence is often false.
- **Platform engineering:** common control planes, identity, networks, regions, deployment pipelines and observability dominate shared-cause structure.
- **Object-oriented programming:** component boundaries help modular trees, while inheritance/shared services can conceal coupling.
- **Functional programming:** Boolean algebra, immutable expressions, algebraic decision diagrams and property-based truth-table tests support logical verification.
- **Security engineering:** attack trees share AND/OR structure but adversaries adapt; probabilities and independence need threat-specific models.

## References

1. International Electrotechnical Commission, [IEC 61025:2006, Fault tree analysis](https://webstore.iec.ch/en/publication/4311), edition 2.0, stability date 2029.
2. International Electrotechnical Commission TC 56, [Dependability Standards and Supporting Standards](https://tc56.iec.ch/dependability-standards/), current program status including IEC 61025 edition work, accessed 2026-08-31.
3. U.S. Nuclear Regulatory Commission, [Fault Tree Handbook (NUREG-0492)](https://www.nrc.gov/reading-rm/doc-collections/nuregs/staff/sr0492/index), publication record and official download, 1981.
4. NASA, [Fault Tree Handbook with Aerospace Applications](https://extapps.ksc.nasa.gov/reliability/Documents/Fault_Tree_Handbook_with_Aerospace_Applications_August_2002.pdf), Version 1.1, 2002.
5. NASA Small Spacecraft Systems Virtual Institute, [Mechanical Fault Tree Analysis](https://s3vi.ndc.nasa.gov/ssri-kb/topics/16/), knowledge-base record, 2021.
6. NASA Office of Safety and Mission Assurance, [System Safety](https://sma.nasa.gov/sma-disciplines/system-safety), FTA/PRA learning and discipline resources, accessed 2026-08-31.
7. NASA Kennedy Space Center, [Reliability Preferred Practices](https://extapps.ksc.nasa.gov/Reliability/Preferred_practices.html), including team FTA practice, accessed 2026-08-31.
8. NASA, [Fault Tree Analysis procedure](https://nodis3.gsfc.nasa.gov/displayCA.cfm?Internal_ID=N_PR_8621_0001_&page_name=AppdxI35), NPR 8621.1 historical appendix, accessed 2026-08-31.
9. NASA, [Probabilistic Risk Assessment Procedures for NASA Programs and Projects](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_8705_0005_&page_name=ALL), NPR 8705.5 historical record, accessed 2026-08-31.
10. International Electrotechnical Commission, [IEC 62502:2010, Analysis techniques for dependability—Event tree analysis](https://webstore.iec.ch/en/publication/7162), standard record, 2010.

## Exercises

### Exercise 1

Define and construct the first three levels of a fault tree for “loss of emergency power for more than 30 seconds during hospital grid outage.” State boundary, configuration, gates, events and assumptions.

### Exercise 2

For $T=A\lor(BC)\lor(BD)$, derive MCSs and compute exact probability for independent $q_A=0.001,q_B=0.02,q_C=0.03,q_D=0.04$. Compare the rare-event sum.

### Exercise 3

Audit a redundant two-channel tree that models $T=A\land B$ with $q_A=q_B=10^{-3}$ but omits shared power, software and maintenance. Explain quantitative and corrective consequences.

### Exercise 4

Choose between static FTA, event tree, Markov/state-space and simulation for a standby recovery sequence with detection, delayed switch, repair and finite inventory. Justify a hybrid model and verification.

### Exercise 5

Design a validation, uncertainty and lifecycle-maintenance plan for a safety-significant tree used in release decisions.

## Answers to the Exercises

### Answer 1

Top event: “AC emergency bus voltage remains below the essential-load threshold for more than 30 seconds after confirmed utility-grid loss, hospital electrical configuration H2.” Consequence such as loss of critical care is analyzed separately. Boundary includes grid-loss confirmation, generators, fuel/start/controls, transfer switch, emergency distribution and credited UPS bridge; state assumptions identify test/maintenance, load and recovery.

First gate: emergency supply unavailable OR emergency path unavailable OR essential demand exceeds available protected capacity. Supply unavailable might be both credited generators unavailable, with shared fuel, room environment, start air/battery, control and maintenance developed explicitly. Path unavailable may be transfer failure OR bus/protection isolation. Capacity condition needs demand/configuration and load-shedding behavior. OR inputs must each suffice; generator AND semantics require overlapping unavailability within 30 seconds and valid switching assumptions.

Use stable repeated identities for shared fuel/control. House events may select maintenance configurations only under scenario control. Do not quantify until demand, failure-on-demand, time-dependent start, UPS duration, CCF and human recovery semantics are established. Validate against one-lines, protection studies, procedures, tests and outage experience.

### Answer 2

The expression is already an OR of products, with MCSs $\{A\},\{B,C\},\{B,D\}$. The latter cut sets overlap whenever $B,C,D$ occur. Factor:

\[
T=A\lor[B(C\lor D)].
\]

Under declared independence, $P(C\lor D)=0.03+0.04-(0.03)(0.04)=0.0688$, so $P(B(C\lor D))=0.001376$. Then

\[
P(T)=0.001+0.001376-(0.001)(0.001376)=0.002374624.
\]

The rare sum is $0.001+(0.02)(0.03)+(0.02)(0.04)=0.0024$, high by $0.000025376$, about 1.069% of exact. This arithmetic is conditional on Bernoulli independence and a common mission; it says nothing about data validity.

### Answer 3

The naive value $10^{-6}$ follows only if A/B are independent event probabilities with compatible mission semantics. Add common power $P$, common software/configuration $S$, and common maintenance-disable $M$ as OR paths, plus channel failures conditional on support. Even small common-event probabilities can dominate the squared independent term. Channel probabilities may also be conditionally correlated.

The original tree exaggerates redundancy and points only to improving A/B. The corrected model may prioritize diverse power/control, partitioning, independent configuration/restoration verification, online proof testing and maintenance interlocks. Evidence must address shared environment, sensors, actuators, communications and recovery too. Use CCF/dependency analysis and sensitivity; do not assign arbitrary tiny values to systematic software or human events. Revalidate architecture and fault injection before residual acceptance.

### Answer 4

Use an event tree for scenario ordering: demand detected or missed; switch command succeeds/fails; standby starts before/after inventory depletion; recovery succeeds/fails. Use fault trees for failure causes of each pivotal event. A Markov or semi-Markov/state-space model can represent standby states, latent failure, repair and time-dependent inventory if transition assumptions are credible. Discrete-event simulation is useful when distributions, resource contention and policies are too complex analytically.

The hybrid shares stable event/state identities and one configuration. Verify fault-tree logic with MCS/truth cases, event-tree sequence completeness, state transition conservation/limiting cases, and simulation against analytical reduced cases. Trace data units and dependencies; compare alternate assumptions and uncertainty. No model choice repairs missing recovery behavior or invalid data.

### Answer 5

Freeze top-event definition, boundary, configuration, mission/time, gate/event dictionary, shared identities, data and criteria. Conduct top-down and bottom-up walkthroughs with system, domain, software, human-factors/operations, reliability and safety owners. Compare FMEA, hazards, interfaces, procedures, common-cause lists, tests and incidents. Narrate every single and important MCS physically; challenge AND gates, timing, recovery, complements and undeveloped events.

Independently reproduce Boolean reduction on a reduced tree, truth-table fixtures, exact probability, rare approximation, truncation convergence, units, bounds, importance and sensitivity. Peer-check solver/version/settings and data provenance. Propagate parameter uncertainty and compare dependency/CCF/model alternatives; report missing contributors and point-estimate limitations.

Link the accepted tree to requirements, controls, actions, tests and release decision. Changes to architecture, configuration, software, procedures, suppliers, environment, data or incidents trigger impact and proportionate rerun. Preserve prior baselines and evidence packages. Authorized reviewers accept residual risk only within stated validity; solver success and low probability never substitute for hazard completeness or system validation.
