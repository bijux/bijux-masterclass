---
module_id: SYSENG-034
program: Systems Engineering
level: 1
module_number: 34
title: Interface Contracts and Assumptions
status: complete
last_verified: 2026-08-31
---

# Interface Contracts and Assumptions

## One-Page Review

### Governing question

How can independently developed elements state, compose, challenge, monitor, and change their mutual assumptions and guarantees without hiding incompatibility behind ambiguous requirements or circular reasoning?

### Essential definitions

- An **engineering assumption** is a proposition treated as true for a bounded decision despite incomplete confirmation. It has a source, owner, applicability, evidence basis, consequence if false, and closure or monitoring plan.
- An **interface obligation** is a normative responsibility assigned to an endpoint or joint authority and made verifiable at a declared interface plane.
- An **assume–guarantee contract** is a pair (C=(A,G)): when the environment satisfies assumption predicate (A), the component promises guarantee predicate (G).
- A **contract interface** identifies the variables, events, physical quantities, ports, directions, and observation planes over which (A) and (G) are interpreted.
- A **compatible environment** satisfies the contract assumptions over the declared applicability domain.
- An **implementation satisfies a contract** when its behaviors meet the guarantee whenever the assumptions hold.
- **Consistency** means the contract does not demand a logically impossible combination in its intended domain; **realizability** means an implementation strategy can produce the required guarantees against every allowed environment behavior.
- **Composition** derives an assembly contract and discharges connected assumptions using other components' guarantees.
- **Refinement** replaces a contract with one that is safe wherever the original contract was promised: it assumes no more and guarantees no less under the original context.
- A **contract gap** is an environmental behavior allowed by a producer but rejected by a consumer, an unassigned conversion, or an assumption not discharged by evidence or another guarantee.
- A **circular assumption** occurs when components justify guarantees only by mutually presuming those same guarantees, without an independent invariant, initialization condition, progress argument, or verified fixed point.
- An **assumption ledger** is the controlled set of assumptions, dependencies, owners, evidence, risk, consumers, status, and closure/monitoring actions.
- An **assumption monitor** observes whether a runtime or lifecycle condition remains inside the valid contract domain and triggers defined response when it does not.

### Central model, mechanism, or theorem

Let behaviors be (b\in\mathcal B), contract (C=(A,G)), implementation predicate (M), and environment predicate (E). Under the convention used in this module:

\[
M\models C\iff \forall b:\ M(b)\land A(b)\Rightarrow G(b),
\]

\[
E\sim C\iff \forall b:\ E(b)\Rightarrow A(b).
\]

If (M\models C) and (E\sim C), then:

\[
\forall b:\ E(b)\land M(b)\Rightarrow G(b).
\]

For a producer contract (C_P=(A_P,G_P)) connected to consumer contract (C_C=(A_C,G_C)), a central compatibility obligation is:

\[
Context\land G_P\Rightarrow A_C.
\]

The implication must cover values, semantics, units, timing, state, faults, versions, environments, and lifecycle conditions—not only nominal scalar ranges. False or impossible assumptions can make an implication vacuously true, so assumption satisfiability and reachable compatible environments must be checked separately.

### Critical invariants

- Every assumption is stated as a falsifiable proposition with stable identity, source, owner, applicability, consumers, evidence, status, and consequence if false.
- Assumptions are not disguised needs, requirements, design decisions, unresolved values, optimistic targets, or risks; each concept retains its own governance.
- Every guarantee has an accountable provider, observable plane, modes/configurations, measurable success condition, and verification mapping.
- The producer guarantee entails the consumer assumption for every authorized connection and applicable condition, with conversions and path effects included.
- Contract assumptions are satisfiable, reachable, and no stronger than necessary; guarantees are internally consistent and realizable under them.
- A component cannot claim satisfaction merely because its assumption is false in every relevant case.
- Composition eliminates or exposes internal assumptions; it never silently exports them as someone else's problem.
- Refinement preserves substitutability under the declared convention, interface variables, and behavior domain.
- Circular dependencies have explicit initialization, invariant/progress reasoning, fault handling, and non-vacuity evidence.
- Each critical assumption is confirmed before the dependent baseline or explicitly carried as bounded risk with decision authority and mitigation.
- Runtime-monitorable assumptions define observation, threshold, persistence, uncertainty, response, authority, and evidence retention.
- Any change to an assumption, guarantee, interface variable, applicability domain, or evidence basis triggers impact analysis across all dependent contracts, requirements, hazards, tests, versions, suppliers, and operations.

### Common failures

Common failures include writing “assume nominal conditions”; assigning assumptions no owner; treating a required property as an assumption to avoid allocating it; confusing an environmental fact with a design choice; using point estimates without ranges or confidence; failing to list assumption consumers; accepting a supplier promise outside its stated configuration; proving (A\Rightarrow G) with an impossible (A); allowing producer and consumer units or time bases to differ; checking each pair but not shared-resource composition; claiming refinement because values are “better”; weakening a guarantee without revisiting consumers; relying on two components to initialize each other; monitoring a condition without safe response; closing an assumption from one favorable test; and updating a spreadsheet without rebaselining the actual interface obligations.

### Compact example

A sensor guarantees an output update every 80–100 ms while powered, synchronized, and in normal mode. A controller assumes a fresh update at least every 120 ms, considers data stale after 150 ms, and enters hold after staleness. A network path guarantees at most 15 ms delivery under an allocated load. The connected arrival interval is therefore at most 115 ms under the joint assumptions, so it discharges the controller's 120 ms input assumption with 5 ms arithmetic margin. The claim remains conditional on power, synchronization, mode, load, restart, loss, clock semantics, and whether “update” and “arrival” use compatible events. Those conditions need owners, evidence, and fault responses; the inequality alone is not the contract.

### Connections

SYSENG-031 found the boundary; SYSENG-032 controlled interface information; SYSENG-033 characterized domain-specific behavior. This module makes dependencies explicit as assumptions and guarantees. SYSENG-035–040 use them to derive physical architecture, decompose subsystems, plan integration, and construct verification evidence. Requirements, risk, configuration, supplier, safety, security, operations, and model-based engineering all depend on the same assumption identities and applicability domains.

## Governing Question

Which claims may each endpoint legitimately assume, which outcomes must it guarantee, and what reasoning and evidence establish that the assembled system remains compatible when those contracts are composed or changed?

The answer combines formal and practical discipline. Formal assume–guarantee reasoning provides explicit predicates, satisfaction, compatibility, refinement, and composition. Practical assumption management supplies the source, evidence, ownership, lifecycle, human judgment, physical uncertainty, supplier context, and change control that formulas alone do not provide. Use the strongest representation justified by the decision, but never allow notation to make an unconfirmed premise look true.

## Why This Matters

Every design decision depends on claims outside the chosen element boundary. A power converter is designed under source-voltage and load assumptions. Software is timed under processor, scheduler, traffic, and clock assumptions. A structure is sized under load, attachment, temperature, and manufacturing assumptions. An operator allocation assumes staffing, training, information, time, and physical access. A supplier plan assumes an external standard, delivery configuration, and change notice. If these premises remain implicit, local designs diverge while each team believes it is compliant.

Interface contracts turn dependency into an inspectable object. They let teams ask whether a provider guarantee covers a consumer assumption, whether a component remains substitutable after change, which system claim follows from component claims, and which unresolved premise prevents a baseline. Contract-based design research provides rigorous operations for composition, refinement, quotient, and viewpoint merging. Current Pacti research and tooling demonstrate practical computational support for such operations. This module uses a deliberately elementary predicate model; richer trace, timed, probabilistic, hybrid, and reactive contract theories require their own semantics and tools.

NASA's current Interface Management guidance calls for compatibility, strict interface control, verification, and capture of assumptions used in interface change decisions. NASA's current requirements guidance calls for sources/owners, bidirectional traceability, baseline consistency, and impact assessment of changes. NASA's current requirement-writing checklist says assumptions should be explicit and confirmed before baselining. In practice, early programs cannot always confirm every premise before decisions are needed. The honest response is not to erase the assumption; it is to bound it, expose its consumers and risk, collect evidence, and obtain decision authority for any temporary dependence.

An assumption differs from a requirement. “Ambient temperature will remain between 10 and 35 °C” is an assumption only if the team is provisionally treating that proposition as true. If the system must be provided such an environment, it becomes an allocated environmental requirement on a facility or enclosing system. If the product itself must operate over that range, it becomes a product requirement. If engineers select a heater, that is a design decision. If temperature may exceed the range and cause failure, that is a risk scenario. Classification determines ownership and evidence.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. interface endpoints, plane, direction, modes, configurations, environment, lifecycle, and ownership;
2. requirements as normative, traceable, feasible, verifiable obligations rather than descriptive prose;
3. provider guarantees, receiver acceptance envelopes, conversions, path effects, and compatibility checks;
4. state/mode behavior, initialization, degraded operation, fault response, recovery, and version compatibility;
5. logical implication, set containment, satisfiability, conjunction, and counterexample reasoning;
6. uncertainty, ranges, measurement evidence, and the difference between observation and universal claim;
7. risk as an uncertain event or condition with consequence, distinct from the proposition being assumed;
8. configuration control, so assumptions, contracts, implementations, and evidence refer to exact baselines.

As a retrieval test, examine “The partner service is available 99.9% of the time.” Ask: Is this a measured historical fact, contractual obligation, design target, planning assumption, or marketing claim? What service boundary, observation period, exclusions, maintenance, region, request class, and measurement source apply? Does “available” mean reachable, timely, correct, authorized, or all four? Which components consume the value? What happens during the allowed outage? What evidence and monitoring exist? Until these are answered, the number cannot safely discharge a system availability assumption.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish assumptions, facts, constraints, requirements, guarantees, goals, decisions, risks, and evidence;
2. write an assumption record with proposition, source, owner, applicability, consumers, evidence, consequence, closure, and monitoring;
3. express a bounded assume–guarantee contract over declared interface variables and behavior domains;
4. test compatibility, consistency, non-vacuity, and elementary realizability using implication and counterexamples;
5. compose producer/path/consumer contracts and expose undischargeable internal assumptions;
6. evaluate contract refinement and substitution using an explicit convention rather than informal “better than” language;
7. detect circular assumptions, hidden initialization dependencies, and shared-resource composition failures;
8. connect assumptions to requirements, architecture, risk, verification, suppliers, versions, and change control;
9. design runtime assumption monitors and safe responses without treating monitoring as prevention;
10. state bounded conclusions and select when informal records, executable checks, or richer formal methods are warranted.

## Core Exposition

**Classify the claim before governing it.** A fact is supported as true for a declared context. An assumption is provisionally treated as true. A requirement imposes an obligation. A guarantee is an obligation conditioned by a contract assumption. A constraint limits solution space. A goal expresses desired direction without the same verification force. A design decision selects an approach. A risk describes uncertainty and consequence. Evidence supports or challenges a claim. Misclassification creates gaps: a required supplier behavior written as “assumed” has no accountable provider.

**Write the proposition precisely.** Replace “assume adequate bandwidth” with a falsifiable proposition: “For network profile N7 in normal mode, other allocated traffic at plane NP-1 will not exceed 4 Mbit/s over any 100 ms interval.” Define quantities, units, plane, interval, inclusivity, mode, configuration, environment, and exceptions. Precision enables confirmation, sensitivity analysis, contract compatibility, and monitoring.

**Create a controlled assumption record.** Record stable ID, proposition, type/domain, source and rationale, author, accountable owner, decision supported, affected interface/requirements/components, applicability, consumers, dependencies, current evidence, confidence/uncertainty language, consequence if false, risk link, validation method, due event, status, monitor, contingency, change authority, and history. The record should be queryable from every dependent baseline.

**Identify the source honestly.** Sources include stakeholder statements, supplier commitments, standards, measurements, models, analogous systems, physics, regulations, operational plans, architecture decisions, or expert judgment. “Engineering judgment” is not meaningless, but it should name the expert domain, reasoning, alternatives considered, and uncertainty. A source may be authoritative yet inapplicable to the chosen configuration.

**Assign ownership and consumers.** The assumption owner coordinates confirmation and change; the source owner may be different. List every design, requirement, model, budget, hazard control, test, procedure, supplier, and decision that consumes it. Consumers determine impact, not who entered the row. A generic systems-engineering owner cannot absorb endpoint accountability.

**Bound applicability.** State lifecycle phase, product version, location, environment, mode, operational scenario, population, supplier lot, and time interval. Evidence valid for a prototype at room temperature may not support production at environmental extremes. An assumption can be true in normal mode and deliberately false in degraded mode; contracts must define the alternate guarantee.

**Connect uncertainty to decisions.** Use ranges, distributions, confidence intervals, scenarios, sensitivity, or qualitative evidence grades only when justified. Avoid invented probabilities. Ask which decision changes if the assumption is false, what boundary value reverses the decision, and when better evidence is worth its cost. An assumption whose falsity has no decision impact may not need elaborate closure.

**Convert assumptions into obligations where authority exists.** If the system depends on a condition that another owned element can provide, allocate a requirement or contract guarantee to that element. If no party controls it—weather, market behavior, physical environment—retain an environmental assumption, design a robust envelope, monitor, or constrain operations. Do not “require” nature to cooperate.

**Define the contract interface.** Declare inputs, outputs, shared variables, events, physical quantities, ports, observation planes, units, time semantics, modes, and versions. Formal predicates are meaningless without a shared universe of behaviors. Decide whether a behavior is a point, trace, state sequence, trajectory, probability distribution, or hybrid execution. The simple Boolean notation in this chapter hides that semantic choice and must not be overextended.

**State assumptions and guarantees separately.** Assumptions constrain environment behavior; guarantees constrain component behavior when assumptions hold. Example: assumption (23\le V_{in}\le29\) V and ambient (-10\le T\le50\) °C; guarantee (11.8\le V_{out}\le12.2\) V at load 0–4 A. Include transient, fault, state, and measurement conditions if they matter. A narrative paragraph that mixes both sides impedes blame and composition.

**Check assumption satisfiability and reachability.** A contradiction such as (V<20\land V>25) makes (A\Rightarrow G) true for every implementation. That is vacuity, not success. Use constraint solving, model checking, simulation, review, or witness scenarios to show at least one relevant environment behavior satisfies (A). Also ask whether the intended operational environment can actually reach that domain.

**Check guarantee consistency.** Guarantees such as (x\le3\land x\ge5) cannot be produced together. Conditional guarantees may be consistent only if modes and guards are exclusive or priority is defined. Check requirements, modes, units, time windows, and endpoint baselines together. A syntactically satisfiable contract can still be physically unrealizable.

**Check realizability at the right strength.** Realizability asks whether some strategy can satisfy (G) for every environment behavior allowed by (A), respecting information and causality. A contract requiring output now to equal an unknown future input may be logically consistent as a trace predicate yet unrealizable by a causal component. Formal proof requires a semantics and solver suited to the domain; prototypes and tests demonstrate sampled implementations, not general realizability.

**Check producer–consumer compatibility.** For connected output (y), the producer guarantee plus path effects must entail the consumer assumption. For intervals, the transformed producer interval must be contained in consumer acceptance. For protocols, legal producer traces must be accepted by the consumer state machine. For human or supplier interactions, evidence may be empirical or procedural. Search for a counterexample (G_P\land\neg A_C).

**Include path and adapter contracts.** Networks, harnesses, converters, translators, mounting structures, operators, and procedures transform behavior. Do not compare the source connector directly with the final receiver if an intervening path changes voltage, delay, units, frames, errors, or authority. Assign each conversion and its failure behavior to an owner.

**Compose contracts.** When (G_1\Rightarrow A_2), component 1 can discharge the connected portion of component 2's assumption within the joint context. Hide internal variables only after proving internal obligations. Export remaining environmental assumptions and combined guarantees at the assembly boundary. Composition must also account for feedback, shared resources, simultaneous loads, and common causes.

**Do not overclaim pairwise compatibility.** Suppose two loads each assume at least 60 W is available and a supply guarantees 100 W total. Supply-to-load pairwise checks may pass if each is examined alone, but simultaneous composition requires 120 W. Contracts must express shared-resource allocation and concurrency, not only point-to-point envelopes.

**Define refinement explicitly.** This module uses: (C_1=(A_1,G_1)) refines (C_0=(A_0,G_0)) when (A_0\Rightarrow A_1) and (A_0\land G_1\Rightarrow G_0). Thus the replacement accepts at least the original environments and meets at least the original promises there. Exact refinement definitions vary across contract theories, especially after normalization/saturation, variable hiding, and receptiveness. State the chosen semantics before using the word.

**Use counterexamples for refinement.** A replacement that narrows accepted input from 0–10 to 2–8 assumes more and is not a safe refinement even if its output accuracy improves. A replacement that accepts -1–11 and tightens error from ±0.5 to ±0.2 refines the original under the scalar convention if all other conditions remain. Check modes, timing, faults, and versions, not marketing adjectives.

**Handle multiple viewpoints.** Performance, safety, security, human factors, physical, and cost contracts can share variables and conflict. Merge or conjoin viewpoint constraints only after checking consistency and ownership. A security guarantee that adds authentication latency may violate a control-timing assumption. A mechanical enclosure that improves shielding may violate human access. Viewpoint composition is system design, not clerical aggregation.

**Expose circular dependencies.** Controller A guarantees readiness if B is ready; B guarantees readiness if A is ready. Both contracts are satisfied vacuously if neither becomes ready. Break the circle with initialization responsibility, an independent starting condition, progress/liveness guarantee, timeout, or verified fixed-point reasoning. Feedback contracts need time and causality semantics, not only propositional implication.

**Treat assumptions as risk drivers.** For each important unconfirmed premise, describe the failure scenario, consequence, likelihood evidence if available, affected objectives, detection, mitigation, contingency, and decision owner. The assumption record states what is believed; the risk record governs uncertainty and consequence. Link them without duplicating or confusing them.

**Plan closure.** Confirmation methods include stakeholder agreement, supplier commitment, inspection, analysis, measurement, experiment, prototype, simulation, qualification, interface test, operational trial, or regulatory decision. Define acceptance criterion and due event. One result closes only the proposition and domain it supports. Update the assumption to confirmed fact, contract requirement, invalidated claim, superseded record, or monitored operational condition with preserved history.

**Baseline with honesty.** NASA's checklist recommends confirmation before baselining. If a program must baseline while a premise remains unresolved, do not label the contract fully proven. Bound the design envelope, identify affected requirements and risks, obtain explicit authority, set closure criteria, and prevent downstream users from mistaking provisional values for verified facts.

**Monitor runtime assumptions.** Some conditions cannot be guaranteed before operation: traffic, weather, partner availability, operator staffing, sensor health, contamination, or resource load. Define observable proxy, plane, sampling, threshold, persistence/hysteresis, uncertainty, monitor health, response, authority, logging, and recovery. A monitor detects domain exit; it does not prevent it. The system guarantee must state what happens outside the normal assumption.

**Define guarantees outside the normal domain.** Contracts should avoid “all bets are off” where safety or asset protection matters. If normal assumption (A_N) fails, provide a degraded guarantee (G_D): reject commands, enter safe state, preserve data, limit energy, notify operators, or constrain service. Absolute behavior may remain impossible under catastrophic conditions; state residual limits explicitly.

**Control supplier assumptions.** Pin supplier product, revision, options, manufacturing/configuration, environment, use profile, and evidence. A data sheet typical value is not a guaranteed worst-case value. A contractual guarantee may still require product verification. Define notice, approval, second-source equivalence, obsolescence, and evidence-delivery obligations.

**Manage assumption changes like interface changes.** A change request identifies old/new proposition, source, rationale, affected contracts and consumers, architecture/budget/hazard/test impacts, versions, transition, rollback, re-verification, approvals, and effective date. Changing an assumption can be as consequential as changing a requirement because designs may have consumed it silently.

**Build automated checks carefully.** Requirements databases can detect missing owners or links. Constraint solvers can find interval/polyhedral incompatibility. SMT solvers and model checkers can test richer predicates/traces. Contract tools can compose, refine, merge, or compute missing-subsystem contracts. Tool success is conditional on model semantics, variable mappings, units, completeness, and solver scope. Retain models, versions, commands, results, and interpretation.

**Review evidence and bounded conclusions.** A contract review should produce: compatible, incompatible with counterexample, internally inconsistent, unrealizable under the chosen semantics, provisional pending evidence, or not analyzed. Avoid a generic green status. State variables, versions, contexts, solver/test method, assumptions, evidence, and excluded concerns.

The following checker finds selected governance omissions in six assumption records. It does not confirm the propositions, discharge dependencies, or prove contract compatibility.

<!-- bijux-verify: {"id":"assumption-ledger-declaration-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"assumptions_total=6\nwell_governed_declared=1\nmissing_source=ASM-002\nmissing_bounds=ASM-003\nmissing_owner=ASM-004\nmissing_evidence=ASM-005\nmissing_contingency=ASM-006\nunresolved=ASM-002,ASM-003,ASM-004,ASM-005,ASM-006\nevidence=declared_fields_only\n","stderr":""}} -->
```python
records = [
    {"id": "ASM-001", "source": "supplier guarantee SG-17",
     "bounds": "23-29 V at plane P1, normal/degraded-source modes",
     "owner": "Power Interface Lead", "evidence": "qualification report QR-4",
     "contingency": "inhibit startup and notify operations"},
    {"id": "ASM-002", "source": "", "bounds": "0-4 Mbit/s over 100 ms",
     "owner": "Network Lead", "evidence": "traffic analysis TA-8",
     "contingency": "shed nonessential telemetry"},
    {"id": "ASM-003", "source": "operations concept OC-2", "bounds": "",
     "owner": "Operations Lead", "evidence": "staffing study SS-3",
     "contingency": "restrict concurrent maintenance"},
    {"id": "ASM-004", "source": "thermal model TM-5", "bounds": "10-35 C",
     "owner": "", "evidence": "chamber test CT-6",
     "contingency": "enter thermal hold"},
    {"id": "ASM-005", "source": "partner agreement PA-9", "bounds": "99.9% monthly",
     "owner": "Service Owner", "evidence": "",
     "contingency": "queue requests for bounded retry"},
    {"id": "ASM-006", "source": "prototype measurement PM-2", "bounds": "40-60 ms",
     "owner": "Control Lead", "evidence": "raw trace RT-2",
     "contingency": ""},
]
fields = ("source", "bounds", "owner", "evidence", "contingency")
valid = [record for record in records if all(record[field] for field in fields)]
print(f"assumptions_total={len(records)}")
print(f"well_governed_declared={len(valid)}")
for field in fields:
    print(f"missing_{field}=" + ",".join(r["id"] for r in records if not r[field]))
print("unresolved=" + ",".join(r["id"] for r in records if r not in valid))
print("evidence=declared_fields_only")
```

Even `ASM-001` may cite inapplicable evidence, omit consumers, or contain an incorrect proposition. Populated fields are governance declarations, not truth.

## Definitions and Notation

Let (mathcal B) be the behavior universe for a declared interface signature and semantics. Predicates (A,G,M,E:\mathcal B\rightarrow\{true,false\}) denote assumption, guarantee, implementation behavior, and environment behavior.

Contract:

\[
C=\langle I,O,S,A,G,D,V\rangle,
\]

where inputs (I), outputs (O), shared/observed variables (S), assumptions (A), guarantees (G), applicability domain (D), and contract version (V) are controlled.

Implementation satisfaction:

\[
M\models C\iff M\land A\Rightarrow G.
\]

Environment compatibility:

\[
E\sim C\iff E\Rightarrow A.
\]

Non-vacuity requires at minimum:

\[
\exists b:\ E(b)\land A(b),
\]

for an intended environment (E). Contract consistency requires a behavior satisfying relevant assumptions and guarantees:

\[
\exists b:\ A(b)\land G(b),
\]

but this is weaker than causal realizability.

For producer (P), path (T), and consumer (C), compatibility over shared variable (y) is:

\[
Context\land T(G_P(y))\Rightarrow A_C(y),
\]

or equivalently no counterexample is satisfiable:

\[
Context\land T(G_P(y))\land\neg A_C(y).
\]

For interval guarantee (G_P=[g_l,g_u]), additive path effect ([d_l,d_u]), and consumer assumption (A_C=[a_l,a_u]):

\[
[g_l+d_l,g_u+d_u]\subseteq[a_l,a_u].
\]

Under this module's refinement convention, (C_1\preceq C_0) means:

\[
A_0\Rightarrow A_1,
\]

\[
A_0\land G_1\Rightarrow G_0.
\]

The first condition prevents the replacement from demanding a narrower environment than originally allowed; the second preserves original guarantees in original contexts. Formal contract theories may use saturated forms or different semantic universes, so operators must not be transferred mechanically.

An assumption record is:

\[
h=\langle id,p,source,owner,domain,consumers,evidence,uncertainty,
consequence,closure,monitor,contingency,status,version\rangle.
\]

Dependency relation (Dep\subseteq H\times Artifacts) supports change reachability. If (h) changes, every artifact reachable through (Dep) requires disposition; reachability does not prove the recorded graph is complete.

## Mechanisms, Invariants, or Proof Structure

The core proof pattern is compositional:

1. define the behavior universe, interface signature, plane, modes, versions, and observation semantics;
2. establish each component contract's assumption satisfiability, guarantee consistency, and—where claimed—realizability;
3. show each implementation satisfies its contract under the chosen semantics;
4. show connected producer/path guarantees entail consumer assumptions;
5. discharge internal assumptions and export remaining environmental assumptions;
6. prove the composed contract refines the allocated system contract;
7. validate physical, human, supplier, and operational premises that the formal model abstracts;
8. retain counterexamples, models, evidence, and applicability limits.

From (M\land A\Rightarrow G) and (E\Rightarrow A), conjunction gives (E\land M\Rightarrow M\land A), then (G). This elementary rule explains assume–guarantee reasoning. It does not by itself prove (E\Rightarrow A), implementation correctness, completeness of (G), or realizability.

**Classification invariant.** Every controlled claim has one governing role. The same proposition may trace across roles—for example, an environmental assumption motivates a facility requirement—but the records remain distinct.

**Scope invariant.** Every assumption and guarantee is interpreted in one declared behavior domain, plane, configuration, mode, environment, lifecycle interval, and version. Scope cannot be supplied from oral context.

**Ownership invariant.** The environment assumption has an owner for confirmation and response; every guarantee has an accountable provider; every conversion has an implementer; every joint change has an authority.

**Non-vacuity invariant.** Intended compatible behaviors exist. A false assumption, unreachable mode, empty input interval, or mutually exclusive initialization cannot justify a green contract result.

**Compatibility invariant.** For every internal connection, provider/path behavior is contained in consumer acceptance under all applicable combinations. Shared resources and feedback are analyzed compositionally.

**Realizability invariant.** Claimed guarantees can be produced causally with available information and resources for every allowed environment behavior. Satisfiability alone is insufficient.

**Refinement invariant.** A replacement accepts at least original environments and preserves original promises under the explicit semantic convention. Changes in hidden variables, fault behavior, timing, or modes are included.

**Initialization/progress invariant.** Feedback and circular dependencies have a base condition and a progress or fixed-point argument. Mutual implication alone does not establish startup or liveness.

**Evidence invariant.** Every confirmation names source, method, article/model, version, conditions, criterion, result, anomalies, and limitations. Evidence supports only the proposition and domain examined.

**Change invariant.** No altered assumption or guarantee becomes effective until dependent requirements, architectures, hazards, budgets, tests, suppliers, versions, transitions, monitors, and contingencies are dispositioned.

Adversarial review searches for witnesses to (G_P\land\neg A_C), (A\land\neg G), contradictory assumptions, impossible guarantees, unobservable monitor conditions, future-dependent outputs, simultaneous resource demands, old/new version mixes, initialization deadlock, environmental extremes, stale evidence, and conditions outside the normal domain. Counterexamples are engineering results, not review failures to hide.

## Alternatives and Trade-Offs

**Informal ledger versus formal contract.** A ledger accommodates physical, organizational, supplier, and human propositions and uncertain evidence. Formal predicates enable solver-backed compatibility and composition. Use both: formalize high-value analyzable subsets while preserving context and governance. False precision is worse than explicit qualitative uncertainty.

**Strong assumptions versus robust guarantees.** Strong assumptions simplify components but restrict environments and shift burden outward. Weaker assumptions enlarge the accepted environment but can increase mass, capacity, complexity, cost, or verification. Optimize at system level and allocate the burden explicitly.

**Static confirmation versus runtime monitoring.** Static evidence can close stable physical/configuration claims. Operational conditions may require monitoring. Monitoring adds sensors, false/missed detection, latency, authority, and response needs; it does not make an unsafe out-of-domain transition acceptable by itself.

**Point estimates versus envelopes.** Point values simplify models but hide variation. Worst-case envelopes can be conservative. Probabilistic models can support risk-informed design but require distributions, dependence, stationarity, tails, and decision criteria. Never invent a distribution merely to make composition pass.

**Central ledger versus federated ownership.** One ledger improves search and impact analysis but may become a detached administrative database. Federated domain repositories preserve expert ownership but risk duplicate IDs and inconsistent state. Use stable identities, authoritative fields, synchronized views, and cross-repository validation.

**Designing out an assumption versus accepting risk.** Redundancy, margin, adaptation, isolation, or alternate suppliers can remove dependence but cost resources and create new interfaces. Accepting risk may be rational for low consequence or short duration. Record the trade and decision authority rather than labeling the assumption “reasonable.”

**Early baseline versus delayed decision.** Baselining supports procurement and parallel work; unresolved assumptions can cause rework. Delaying may reduce technical risk but harm schedule. Use bounded interim envelopes, option-preserving architecture, prototypes, and explicit decision dates to manage—not conceal—the tension.

**Bilateral negotiation versus provider-controlled contract.** Joint contracts fit peer or safety-critical interfaces. A platform/vendor may control guarantees unilaterally subject to notice and version terms. Consumers then own qualification, fallback, and exit. Governance must reflect actual authority.

**Pairwise composition versus system-level analysis.** Pairwise checks scale and localize blame but miss shared capacity, correlated faults, timing cycles, security policy, and human workload. Use pairwise checks as building blocks, then analyze the composed architecture and scenarios.

**Manual proof versus automated algebra.** Manual review supports meaning and broad context; automated tools handle large constraint sets and reproducibility. Tool use requires controlled semantics, units, variables, model versions, solver configuration, and interpretation. An automated `satisfiable` result is not a complete system assurance claim.

## Failure Modes and Misconceptions

**“Assumption means we do not need evidence.”** Assumptions exist because evidence is incomplete. That increases the need for ownership, bounds, sensitivity, closure, monitoring, and contingency.

**“If we need it, we can assume it.”** Need creates an obligation or design problem. Treating it as an environmental premise shifts accountability invisibly.

**“A requirement and a guarantee are identical.”** A guarantee is a requirement interpreted conditionally within a contract and interface semantics. The underlying normative requirement still needs authority and traceability.

**“The implication passed, so the contract is correct.”** An impossible assumption makes any implication true. Check satisfiability, reachability, realizability, model completeness, and variable semantics.

**“Satisfiable means realizable.”** A trace can exist while no causal component can produce it against every allowed environment behavior.

**“Typical values are guarantees.”** Typical data-sheet or historical values are observations under stated conditions. A guarantee needs controlled bounds, applicability, and authority.

**“Pairwise compatibility proves system compatibility.”** Simultaneous loads, shared resources, common causes, feedback, and human workload can fail only in composition.

**“More precise output makes a replacement a refinement.”** The replacement may accept fewer inputs, drop a fault guarantee, change timing, or require a new initialization sequence.

**“Mutual assumptions handle feedback.”** They may produce vacuous satisfaction or startup deadlock. Establish initial conditions, causality, invariants, and progress.

**“A monitor guarantees the assumption.”** A monitor observes imperfectly and after some delay. Safety depends on detection coverage, uncertainty, response, and out-of-domain guarantees.

**“Closing the assumption means it disappears.”** Preserve identity, evidence, and history; dependent decisions need trace to the confirmed fact or requirement.

**“An expert reviewed it.”** Record domain, method, evidence, dissent, applicability, and conclusion. Authority alone does not establish physical truth.

**“All assumptions must be eliminated.”** Some environmental or operational premises remain inherent. They must be bounded, validated where possible, monitored where useful, and paired with contingencies.

## Worked Examples

### Example 1

**Voltage producer–consumer contract.** A source assumes load current (0\le I\le4\) A and ambient 0–40 °C, then guarantees 24–28 V at plane P1. A harness assumes the same current and guarantees a drop in ([-1.0,0]\) V. A controller assumes 22.5–28.5 V at P2.

The composed delivered interval is ([24-1,28+0]=[23,28]\) V, contained in ([22.5,28.5]\) V. Margins are 0.5 V at both bounds. Compatibility is conditional on current, ambient, planes, steady/transient basis, return path, and harness configuration. If controller startup draws 5 A, the source/harness assumptions are violated; a degraded guarantee or startup redesign is needed.

### Example 2

**Freshness with path composition.** A sensor assumes synchronized clocks and normal power and guarantees publication no later than 100 ms after the previous publication. A network assumes traffic profile N7 and guarantees delivery within 15 ms. The controller assumes arrivals no more than 120 ms apart.

Serial composition yields 115 ms, leaving 5 ms. But if the sensor's 100 ms is measured publication-to-publication and the network's 15 ms applies separately to each message, arrival spacing can differ by latency variation: one message may take 0 ms and the next 15 ms, still giving 115 ms; the reverse gives 85 ms. The bound holds under those path bounds. Clock loss, queue overload, restart, packet loss, and stale-value behavior remain explicit assumptions/fault guarantees.

### Example 3

**Supplier mass assumption becomes an obligation.** A vehicle architecture reserves 120 kg for a payload based on an early supplier estimate of 110 kg “typical.” Structural, propulsion, handling, and cost models consume it. Treating 110 kg as fact creates hidden exposure.

The ledger records a provisional payload mass envelope 0–120 kg including mounting hardware at the controlled plane, supplier source, vehicle mass-property owner, consumer models, consequence, and contract date. Procurement allocates a requirement that delivered payload mass shall not exceed 120 kg and requires measured mass/center-of-mass evidence. The early assumption is closed only when the supplier obligation and evidence apply to the delivered configuration; the history remains traceable.

### Example 4

**Human response assumption.** Safety analysis assumes an operator acknowledges and isolates a leak within 30 s. The claim came from an expert workshop, but no interface, workload, staffing, or environmental basis was recorded.

The team separates obligations: alarm presentation and control availability requirements on the system; staffing/training/procedure obligations on operations; and an empirical human-performance assumption for representative qualified operators under defined concurrent tasks, noise, protective equipment, and leak scenarios. Human-in-the-loop evidence supports a bounded distribution and failure observations. If 30 s is essential for hazard control, independent automatic protection may be needed rather than assuming perfect response.

### Example 5

**Circular readiness.** Component A guarantees `ready_A` within 2 s if `ready_B`; B guarantees `ready_B` within 2 s if `ready_A`. Both remain false after startup. Each implication is true because its assumption never holds, yet the assembly never becomes ready.

The redesign assigns A as initializer: under power-good and configuration-valid, A guarantees `ready_A` within 2 s without assuming B. B then guarantees `ready_B` within 2 s of `ready_A`; A guarantees operational service within 1 s of `ready_B`. Timeouts transition to diagnosed safe state. The base condition and progress chain replace vacuous mutual implication.

### Example 6

**Refinement counterexample.** Original sensor contract accepts temperature -20–60 °C and guarantees error within ±0.5 °C. A replacement guarantees ±0.2 °C but accepts only 0–50 °C.

It is not a refinement: the original assumption does not imply the replacement assumption. Environments at -10 °C were allowed before and are rejected now. A second replacement accepts -25–65 °C and guarantees ±0.3 °C across -20–60 °C; under the scalar convention and unchanged timing/fault behavior, it refines the original. Complete substitution still requires connector, power, data, calibration, failure, version, and evidence review.

### Example 7

**Conditional normal and degraded guarantees.** A positioning service assumes at least four healthy satellites and valid time, then guarantees horizontal error at most 5 m with freshness 1 s. With fewer satellites it cannot sustain that guarantee.

The contract adds degraded behavior: when health monitor detects fewer than four, the service shall mark position invalid within 1 s, preserve last-valid occurrence time, and prohibit consumers from treating it as current. Consumers assume either valid data meeting the normal envelope or explicit invalid state within the detection bound. The contract does not promise accuracy outside its physical domain, but it does promise safe, observable degradation.

### Example 8

**Assumption change propagation.** A cooling analysis assumes rack power 8 kW, sourced from the electrical budget. A software change raises compute utilization and the electrical budget to 9.5 kW. The power interface still passes electrically, so the change is called software-only.

Dependency traversal finds cooling capacity, airflow, acoustic level, room power, battery runtime, rack mass, fire load, human working environment, and qualification tests. Thermal analysis shows inlet temperature exceeds the component contract under one failure mode. The board changes workload allocation and fan control, revises assumptions and guarantees, and repeats thermal/acoustic/integrated verification. Interface impact follows energy, not organizational labels.

### Example 9

**Runtime assumption monitoring.** An autonomy function assumes localization uncertainty (u\le0.8\) m. A monitor estimates (u), but estimate uncertainty is ±0.1 m and updates every 200 ms. Triggering at displayed (0.8) m can detect actual violation late.

The operational threshold is set at 0.65 m after allocating estimation uncertainty, sampling, trend, stopping distance, and response latency. Persistence/hysteresis prevents chatter without masking rapid degradation. On trigger, the system limits speed and requests operator disposition; if monitor health is lost, it enters the same conservative mode. Tests inject uncertainty growth, delay, monitor faults, and recovery. The monitor manages domain exit; it does not prove localization remains valid.

### Example 10

**System composition and shared capacity.** Two pumps each assume 300 W available during start and guarantee flow after 2 s. A supply guarantees 500 W total. Pairwise, each pump fits the supply. Simultaneous start demands 600 W and violates the shared contract.

The system contract introduces start arbitration: at most one pump may be in `starting`; the running pump draws at most 120 W; the starting pump draws at most 300 W; other loads are allocated 60 W, totaling 480 W. The controller guarantees sequencing under normal authority, and hard protection handles control failure. Verification checks power waveforms, arbitration, command duplication, restart after power loss, protection, and required flow transition. Composition required concurrency semantics.

## Cross-Program Connections

**Platform engineering.** Platform teams publish guarantees for availability, latency, identity, quotas, compatibility, and support while assuming bounded tenant behavior and dependencies. Consumer-driven contract tests, SLO monitoring, and deprecation policies are operational forms of assume–guarantee governance.

**API and service engineering.** Preconditions, postconditions, error models, idempotency, authorization, rate limits, timeouts, and version support form service contracts. Schema compatibility alone does not discharge semantic or operational assumptions.

**Data engineering.** Data contracts pair producer guarantees for schema, meaning, quality, lineage, freshness, and retention with consumer assumptions. Backfill, replay, late data, and partition behavior must compose across pipelines.

**Object-oriented programming.** Behavioral subtyping echoes refinement: replacement implementations should not strengthen client preconditions or weaken promised postconditions/invariants. System contracts extend the idea to time, resources, physical environments, faults, and organizations.

**Functional programming.** Function domains/codomains and types make some assumptions explicit; total functions reduce hidden failure cases. Effects, partiality, timing, distributed state, physical resources, and human actions still require broader contracts.

**Formal methods.** Temporal logic, automata, SMT, model checking, theorem proving, abstract interpretation, and contract algebras support non-vacuity, compatibility, refinement, composition, and realizability under explicit semantics. Tool proof remains conditional on model fidelity.

**Risk and configuration management.** Unconfirmed assumptions drive risk; confirmed or invalidated assumptions change baselines. Stable identity, dependency trace, change authority, evidence, transition, and rollback connect technical reasoning to governance.

**Safety, security, and human factors.** Safety cases depend on environmental, independence, timing, diagnostic, and response assumptions. Security depends on trust, attacker, key, identity, and update assumptions. Human allocations depend on population, staffing, workload, information, training, and recovery assumptions. These must be challenged, not buried.

## References

1. NASA, *Systems Engineering Handbook, Section 6.3: Interface Management*, current web edition, updated 2023. <https://www.nasa.gov/reference/6-3-interface-management/>
2. NASA, *Systems Engineering Handbook, Section 6.2: Requirements Management*, current web edition, updated 2023. <https://www.nasa.gov/reference/6-2-requirements-management/>
3. NASA, *Systems Engineering Handbook, Appendix C: How to Write a Good Requirement*, current web edition, updated 2023. <https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/>
4. NASA, *Systems Engineering Handbook, Appendix L: Interface Requirements Document Outline*, current web edition, updated 2023. <https://www.nasa.gov/reference/appendix-l-interface-requirements-document-outline/>
5. NASA, *Systems Engineering Handbook, Section 6.4: Technical Risk Management*, current web edition, updated 2023. <https://www.nasa.gov/reference/6-4-technical-risk-management/>
6. Benveniste, A., et al., *Contracts for System Design*, Foundations and Trends in Electronic Design Automation 12(2–3), 2018, DOI 10.1561/1000000053. <https://research-explorer.ista.ac.at/record/5677>
7. Incer, I., et al., *Pacti: Assume-Guarantee Contracts for Efficient Compositional Analysis and Design*, ACM Transactions on Cyber-Physical Systems 9(1), 2025, DOI 10.1145/3704736. <https://authors.library.caltech.edu/records/j06fg-7xf75>
8. Pacti Project, *Getting Started: Assume–Guarantee Contracts and Contract Operations*, current documentation. <https://www.pacti.org/docs/getting_started/>
9. Object Management Group, *Systems Modeling Language Version 2.0*, formal specification, 2025. <https://www.omg.org/spec/SysML/2.0>

## Exercises

### Exercise 1

Classify each statement as fact/evidence claim, assumption, requirement/guarantee, goal, design decision, or risk. Explain any ambiguity and rewrite it for control: (a) “The partner API will usually respond within 200 ms”; (b) “The gateway shall reject an expired credential”; (c) “Use two network paths”; (d) “Regional network loss may prevent emergency notification”; (e) “Operators can handle ten simultaneous alarms”; and (f) “The prototype produced 42 W at 20 °C in test T7.”

### Exercise 2

A producer assumes input supply 20–30 V and guarantees output data age 40–70 ms. A path assumes data rate at most 2 Mbit/s and adds 10–25 ms. A consumer assumes arriving age at most 90 ms. Compute the delivered age interval and compatibility margin. Identify the additional assumptions needed before composition is defensible.

### Exercise 3

Original contract (C_0) accepts input (x\in[0,10]) and guarantees output error (|e|\le1.0). Evaluate two replacements under this module's refinement convention: (C_A) accepts (x\in[-1,11]) and guarantees (|e|\le0.8); (C_B) accepts (x\in[2,9]) and guarantees (|e|\le0.2). State the result and its limits.

### Exercise 4

Review this assumption record: “ASM-77: vendor service available 99.95%; owner: architecture; close before launch.” List at least twelve missing governance fields or ambiguities. Rewrite it as a bounded provisional record without inventing false evidence.

### Exercise 5

Three components form a cycle: detector D guarantees `alarm` if controller C is armed; C guarantees `armed` if power P is stable; P guarantees `stable` if D reports no fault. Explain the circularity and propose contracts with initialization, progress, fault, monitoring, and verification obligations that avoid vacuity.

## Answers to the Exercises

### Answer 1

(a) is ambiguous and presently unusable. “Will” plus “usually” could be forecast, assumption, or provider promise. A provisional assumption might be: “ASM-API-01: for partner version 4 in region R during normal operations, 99% of eligible requests are assumed to complete within 200 ms measured gateway-send to gateway-receive over each calendar hour; source is partner proposal PP-4; Service Integration owns confirmation; consumers and fallback are linked.” If it is required behavior, allocate a provider guarantee with authority and verification.

(b) is a requirement and can serve as a security guarantee when its contract assumptions hold. It still needs gateway identity, definition of expired, clock basis, all modes, response/audit behavior, and verification.

(c) is a design decision, not the underlying need. Record the decision, alternatives, rationale, selected failure independence, and requirements it satisfies. The real requirement may concern tolerated path failure or delivery availability.

(d) is a risk statement: uncertain regional loss with operational consequence. It should link to assumptions about path independence/availability, notification requirements, detection, mitigations, contingency, and risk owner.

(e) is an unbounded human-performance assumption, not a fact. Define operator population, alarm types/priorities, concurrence window, tasks, environment, training, performance criteria, evidence plan, consequence, and owner. If ten-alarm performance is essential, derive system/operations requirements and test them.

(f) is a bounded evidence claim or observation: one prototype produced 42 W at 20 °C in named test T7. Add article/version, plane, input/load, instrument uncertainty, procedure, duration, result record, and anomalies. It does not by itself guarantee production output or other temperatures.

### Answer 2

Assuming the path age contribution is additive and the intervals share compatible events and units:

\[
Age_{arrival}=[40+10,70+25]=[50,95]\text{ ms}.
\]

The consumer accepts age at most 90 ms. The lower values are acceptable, but the worst case exceeds the assumption by 5 ms. Therefore (G_P\land G_{path}\not\Rightarrow A_C); the counterexample is producer age 70 ms plus path 25 ms. Compatibility fails with upper margin (90-95=-5\) ms.

Additional premises include producer supply actually within 20–30 V; traffic within 2 Mbit/s; whether producer age and path delay bounds may coincide; occurrence/publication/receipt event definitions; clock synchronization and timestamp uncertainty; data rate measurement window; queue and retransmission coverage; loss/duplicate/restart behavior; normal/degraded modes; versions; path and endpoint configuration; and whether 90 ms is inclusive. Options are tighter producer/path guarantees, a wider justified consumer assumption, a faster architecture, or degraded behavior—never averaging away the violation.

### Answer 3

For (C_A), original assumption (x\in[0,10]) implies replacement assumption (x\in[-1,11]). Under original contexts, (|e|\le0.8) implies (|e|\le1.0). Therefore (C_A\preceq C_0) under the stated scalar convention.

For (C_B), (x\in[0,10]) does not imply (x\in[2,9]); values 1 or 9.5 are counterexamples. Although (|e|\le0.2) is a stronger output guarantee where B operates, B assumes more and is not a safe refinement of (C_0).

The conclusion covers only these input/error predicates. It does not establish timing, faults, initialization, resource use, physical/electrical interface, measurement uncertainty, modes, or implementation conformance. Richer contract theories may define normalization and refinement differently, so the formalism and variable universe must travel with the claim.

### Answer 4

Missing or ambiguous items include: stable source and quoted authority; meaning of service; endpoint/plane; region; service/version/configuration; what counts as available; request class; observation window; permitted maintenance/exclusions; measurement method and data owner; whether 99.95% is assumption, historical evidence, target, or guarantee; owner named as a person/role with authority rather than a broad function; consumers; decision supported; applicability modes; uncertainty/confidence; current evidence; consequence if false; risk link; validation criterion; due event more precise than launch; monitoring; contingency; change authority; status; and history.

A defensible provisional rewrite is:

“ASM-SVC-77, provisional: For partner service version family V4, endpoint E1, region R, and eligible authenticated production requests in normal operations, the architecture provisionally assumes monthly successful-availability at least 99.95%, where success means a semantically valid response within the separately controlled latency limit. Scheduled exclusions, measurement source, and error classification remain unresolved and therefore this value shall not be presented as confirmed. Source: partner proposal PP-9 dated [controlled date]. Owner: Partner Service Integration Lead. Consumers: notification availability model, queue sizing, operating procedure OP-6, and risk R-21. Consequence if false: delayed notification and queue exhaustion. Closure: obtain an approved definition and provider commitment plus applicable evidence before operational readiness review. Monitor: gateway outcome telemetry under the approved definition. Contingency: bounded local queue, alternate manual notification, and escalation at controlled thresholds. Changes require Service Interface Board disposition.”

The bracketed date is a field to populate from the controlled source, not invented evidence. Until definitions and commitment exist, the baseline remains explicitly provisional.

### Answer 5

The original cycle has no base condition. If D never reports, P need not become stable; if P is not stable, C need not arm; if C is not armed, D need not alarm. All implications may be true while the system makes no progress.

One redesign is:

1. P assumes external input within its source envelope and no latched internal fault, then guarantees `stable` or explicit `power_fault` within 2 s of startup. This guarantee does not depend on D.
2. C assumes `stable` and valid configuration, then guarantees `armed` or explicit `controller_fault` within 1 s. On loss of stable power, it transitions to a defined safe/unarmed state and records cause.
3. D assumes stable power and armed status for its normal detection guarantee, then guarantees either bounded-time `alarm`, healthy heartbeat, or explicit `detector_fault` for defined stimuli and self-test conditions.
4. A supervisory monitor observes deadlines and health channels. If power, arming, or detector progress fails, it announces startup failure and inhibits operation; monitor loss itself produces a conservative response.
5. Recovery defines who clears latched faults, rechecks configuration, and restarts the sequence; repeated automatic cycling is bounded.

Verification should include source-envelope boundaries, startup timing, each fault output, lost/late status, reset at every stage, monitor failure, power interruption, old/new version pairs, and evidence of the exact initialization sequence. A state-machine or temporal model can check deadlock and progress under modeled faults; hardware/software integration tests confirm selected implementations and timing. Neither alone proves omitted environmental or physical assumptions.
