---
module_id: SYSENG-030
program: Systems Engineering
level: 1
module_number: 30
title: Checking Completeness and Consistency of a Logical Architecture
status: complete
last_verified: 2026-08-31
---

# Checking Completeness and Consistency of a Logical Architecture

## One-Page Review

### Governing question

How can a team determine whether a logical architecture is sufficiently complete and internally consistent for its declared scope, decisions, and evidence threshold—without mistaking syntactic validity, full-looking diagrams, or a passing model checker for proof that the architecture is correct, feasible, safe, or complete in an absolute sense?

### Essential definitions

- **Completeness** is sufficient coverage of required concerns, behavior, structure, relationships, qualities, lifecycle conditions, rationale, and evidence relative to a declared scope and purpose.
- **consistency** is the absence of unresolved contradiction among controlled statements, models, views, allocations, budgets, interfaces, states, assumptions, and evidence under their declared semantics and applicability.
- **correctness** is conformance of an architecture description to its governing rules and intended facts; it is distinct from stakeholder adequacy.
- **adequacy** is fitness of the architecture and its description to support the intended decisions and stakeholder concerns.
- **well-formedness** is conformance to a metamodel, grammar, schema, or structural rule set.
- A **view** is an architecture work product governed by a viewpoint and addressing selected stakeholder concerns.
- A **correspondence** is a declared relationship among architecture elements or views; a **correspondence rule** constrains how those relationships should agree.
- A **coverage obligation** identifies something that must be represented, allocated, exercised, justified, or evidenced for the scope.
- An **orphan** is an element or relationship without a justified source; an **uncovered item** is a required concern or behavior without an adequate target.
- A **contradiction** exists when two applicable controlled claims cannot both hold; a difference between viewpoints is not automatically a contradiction.
- A **waiver/deviation** is an authorized, bounded departure from a rule with rationale, risk, owner, expiry, and closure criteria.
- An **architecture debt item** records a knowingly unresolved weakness, its consequence, owner, deadline, and removal evidence.
- A **completeness frontier** states what remains deliberately unresolved because further detail is unnecessary, infeasible, or deferred for the current decision.

### Central model, mechanism, or theorem

Treat the architecture description as a typed attributed graph plus a set of governed views:

$$
AD=\langle N,E,V,R,H,Q,B,X\rangle,
$$

where nodes (N), relations (E), views (V), trace/rationale (R), assumptions (H), quality/property claims (Q), baselines/configurations (B), and evidence (X) are versioned. Let obligations (O(S,P)) be derived from scope (S) and purpose (P). Declared completeness is:

$$
Complete_{S,P}(AD)\Rightarrow\forall o\in O(S,P),\ AdequatelyDischarged(o,AD,X).
$$

Let applicable claims be (K(AD,b,m)) for baseline (b) and mode/configuration (m). Consistency requires:

$$
Consistent_{b,m}(AD)\Rightarrow SAT(K)\land
CorrespondencesHold\land BudgetsClose\land InterfacesCompatible\land
ScenariosExecutable.
$$

These predicates require semantic and empirical judgment. A solver can establish satisfiability only for the encoded fragment; it cannot prove that obligations, assumptions, environments, or real-world phenomena were modeled completely.

### Critical invariants

- Completeness and consistency claims name architecture scope, system boundary, lifecycle interval, decision purpose, viewpoints, baseline, modes/configurations, assumptions, and evidence date.
- Every stakeholder concern is addressed by an appropriate viewpoint/view or explicitly dispositioned outside scope by authorized rationale.
- Every authoritative requirement traces to behavior, architecture responsibility, interface/quality obligations, and planned evidence as applicable; every derived item traces back to a justified source/decision.
- Functions, scenarios, states/modes, logical elements, allocations, and control/data flows agree on identity, applicability, semantics, and version.
- Every required input/control has a source, every output has an intended sink/effect, and every cross-element flow has a compatible governed interface.
- Every responsibility, state variable, policy, decision authority, failure response, and lifecycle function has an accountable owner or an explicit external authority.
- Nominal, alternate, degraded, emergency, maintenance, update, recovery, startup, shutdown, transition, and retirement scenarios are covered where applicable.
- Performance/resource budgets use compatible conditions and composition rules, retain margin, and do not allocate more capability or resource than exists.
- Safety, security, privacy, reliability, accessibility, human workload, operability, support, and other crosscutting qualities have local responsibilities and end-to-end composition arguments.
- Contradictions are resolved by authority and semantics, not hidden through duplicate names, view isolation, or tool suppression.
- Open assumptions, decisions, risks, waivers, and debt have owners, consequences, due/expiry conditions, and closure evidence.
- Automated checks state their encoded scope and limitations; stakeholder, practitioner, domain, and empirical review remain necessary.

### Common failures

Failures include declaring completeness because every template field is populated; counting trace links without checking adequacy; allowing each view to pass alone while cross-view correspondences fail; confusing a missing relation with an intentionally external responsibility; treating all duplicate names as the same element; assuming a tree captures crosscutting flows; accepting a scenario that cannot start because its initial state is undefined; assigning a function but not its exception, state, authority, or interface; balancing mean latency while worst-case modes fail; allocating the same margin several times; modeling redundant elements with one shared cause; suppressing cycles that are real feedback; permitting an unresolved placeholder without owner or expiry; resolving contradictions by changing one diagram but not its source; and claiming satisfiability proves safety or real-world feasibility.

### Compact example

A cold-chain logical architecture contains Sensor Interpretation, Control Policy, Actuation, Evidence, and Operator roles. A structural checker finds unique identifiers and valid edge types. Cross-view review then exposes that degraded mode uses a temperature estimate that the flow view disables; Control Policy and Operator both claim final authority during maintenance; the 2-second freshness requirement conflicts with a 3-second sampling interval; Evidence consumes `actuation complete`, but no element produces it; and the recovery scenario never restores policy version synchronization. The team resolves authority, adjusts or rejects the timing design, adds physical-effect evidence, and completes recovery/reconciliation. Chamber and operator tests remain required. The architecture becomes more complete and consistent for the declared baseline; it is not proven safe in every environment.

### Connections

SYSENG-001–020 establish system context, needs, requirements, constraints, and traceability. SYSENG-021–029 develop functions, decomposition, flow, states/modes, scenarios, logical elements, allocation, interactions, and alternatives. This module integrates those views and closes the Functional and Logical Architecture block. SYSENG-031 onward identifies and controls interfaces, physical realization, integration, qualities, verification, operations, risk, and governance. Every later module can reveal evidence that requires this logical baseline to be revised.

## Governing Question

What set of structural, semantic, behavioral, temporal, quantitative, traceability, authority, lifecycle, and evidence checks is sufficient to justify a bounded claim that a selected logical architecture is complete and consistent for its intended decisions?

The answer is an assurance argument built from explicit obligations and correspondences. Define the scope of the claim, derive a coverage model from stakeholder concerns and lifecycle scenarios, check the integrated architecture rather than isolated diagrams, execute or analyze critical behaviors, reconcile budgets and interfaces, challenge negative space and failures, govern unresolved items, and state what the evidence cannot establish.

## Why This Matters

A logical architecture becomes the basis for derived requirements, interface work, physical design, supplier boundaries, integration planning, verification, operations, and cost. Gaps found after those commitments propagate widely. Conversely, pursuing “absolute completeness” wastes effort because every model abstracts. The engineering task is to know complete enough for what decision, consistent under which conditions, and with what residual uncertainty.

NASA’s current Logical Decomposition guidance says architecture and requirements should be understood as viable, verifiable, and internally consistent before baselining and emphasizes inputs, outputs, failure modes, interfaces, and end-to-end paths. NASA’s System Design guidance describes architecture, ConOps, and requirements as interdependent products requiring iteration to consistency. SEBoK 2.14 calls for functional, behavioral, temporal, and traceability views, executable models where possible, and verification/validation of the selected logical architecture. ISO/IEC/IEEE 42010:2022 distinguishes an entity’s architecture from an architecture description and specifies viewpoints, views, model kinds, and correspondences. OMG SysML 2.0 offers precise requirements, behavior, structure, analysis, verification, and traceability constructs. These sources support rigorous descriptions; none promises that a conforming model is a complete representation of reality.

Completeness and consistency also conflict productively. Adding a missing degraded scenario can reveal contradictions in authority or timing. Resolving a contradiction can create a new interface or derived requirement. Therefore the work is iterative: discover, classify, resolve, re-run affected checks, and revisit the claim boundary.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. stakeholder concerns and operational concepts define why architecture views exist;
2. requirements have identity, authority, applicability, rationale, quality attributes, and verification intent;
3. functional, flow, state/mode, and scenario models describe complementary behavior and must correspond;
4. logical components own responsibilities, state/policy, and provided/required interactions;
5. functional allocation is many-to-many and creates interface and quality obligations;
6. architecture alternatives are compared under common frames and uncertainty;
7. trace links and test results are evidence only for their typed semantics and exact versions;
8. a model is an abstraction whose omissions and applicability must be stated.

As a retrieval test, inspect a model report saying `0 validation errors`. Ask which constraints ran, which artifact versions were loaded, which views and configurations were included, whether requirements/scenarios were complete, whether quantities shared units and conditions, whether external assumptions were checked, and whether the solver explored real failure behavior. Zero encoded errors is useful evidence, not a comprehensive conclusion.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish completeness, consistency, correctness, well-formedness, adequacy, feasibility, verification, and validation;
2. define a bounded architecture-assurance claim and derive coverage obligations from scope, purpose, concerns, and lifecycle;
3. audit traceability for semantic adequacy, bidirectionality, exact versions, and evidence applicability;
4. check correspondences among requirements, functions, scenarios, modes, elements, allocations, flows, state, and interfaces;
5. detect missing responsibilities, sources/sinks, authorities, lifecycle behavior, crosscutting qualities, and enabling systems;
6. analyze interface compatibility, state ownership, behavioral reachability, concurrency, cycles, and recovery closure;
7. reconcile performance and resource budgets using consistent conditions, composition rules, and margins;
8. combine static validation, model execution, simulation, review, prototype, and empirical evidence without overclaim;
9. govern contradictions, assumptions, waivers, debt, open evidence, and completeness frontiers;
10. conduct an architecture readiness review and write a conditional, auditable conclusion.

## Core Exposition

**Define the claim before checking.** State the entity/system of interest, boundary, architecture level, lifecycle interval, baseline, variants, modes, operational environments, decision purpose, stakeholders, viewpoints, required confidence, evidence date, and exclusions. “The architecture is complete” is meaningless without these qualifiers.

**Distinguish quality dimensions.** Well-formedness checks grammar and metamodel constraints. Internal consistency checks compatible claims. Completeness checks required coverage. Correctness checks conformance to governing facts/rules. Feasibility asks whether a realization can meet constraints. Verification checks specified requirements; validation checks stakeholder need in context. Adequacy asks whether the description supports the decision. Do not use one passing dimension as evidence for another.

**Build an obligation catalogue.** Derive obligations from stakeholder concerns, requirements, operational scenarios, modes, hazards/threats, qualities, lifecycle processes, regulations, architecture decisions, and review criteria. Each obligation names expected artifact/relation, acceptance condition, owner, evidence, applicability, and disposition. A template is only a starting taxonomy.

**Establish configuration integrity.** Record exact baselines of requirements, models, vocabularies, interfaces, analysis inputs, scenarios, and evidence. Resolve duplicated identifiers and stale imports. Cross-view consistency cannot be assessed if each tool silently uses a different requirement or schema version.

**Check vocabulary and identity.** Govern terms, aliases, units, enumerations, states, modes, and identifiers. Same name does not prove same entity; different names may refer to one concept. Map equivalence explicitly. Detect homonyms, synonyms, and copied elements whose identity diverged.

**Check concern/viewpoint coverage.** For every stakeholder concern, identify the viewpoint and views that address it, why the representation is suitable, who interprets it, and what remains outside. Confirm every view conforms to its viewpoint conventions and that the chosen set supports the current decision rather than merely satisfying a documentation list.

**Check requirements coverage semantically.** For each authoritative requirement, identify functions/scenarios, logical responsibilities, interfaces/qualities, and evidence plan as applicable. Inspect contribution semantics, not link count. A security requirement linked to `Security Manager` is not covered unless controls and responsibilities are allocated to influencing elements and compose end-to-end.

**Check upward justification.** Every function, component, interface, derived requirement, budget, and constraint should trace to a stakeholder need, requirement, scenario, hazard/threat treatment, lifecycle need, or architecture decision. Orphans may reveal gold plating, hidden assumptions, or missing source requirements. Do not delete useful derived behavior merely because its source was not recorded; repair the rationale.

**Check functional closure.** Verify parent inputs, outputs, controls, pre/postconditions, timing, failure semantics, and invariants are preserved by child functions. Every required leaf function is allocated for every applicable mode. Examine initialization, monitoring, cancellation, exception, degraded behavior, recovery, evidence, maintenance, and retirement—not only nominal transformations.

**Check scenario coverage.** Use a scenario catalogue with stakeholders, trigger, initial state, preconditions, main/alternate/exception flows, modes, environment, success/failure outcomes, qualities, evidence, and postconditions. Cover normal, peak, boundary, degraded, emergency, maintenance, update, attack/misuse, recovery, transition, and retirement where applicable. Trace scenarios to needs and architecture paths.

**Check scenario executability.** Walk or execute each scenario through functions, states, allocations, logical elements, and flows. Ensure an initial state exists, guards can be satisfied, required data/control arrives, authority exists, resources are available, outputs are consumed, terminal outcomes are defined, and recovery does not rely on unavailable behavior.

**Check state and mode correspondence.** Every behavior’s applicability must agree with state/mode models. Confirm legal transitions, entry/exit actions, timeout/error transitions, nested/concurrent semantics, prohibited combinations, and recovery. Identify flows enabled in one view but consumed in a mode where they are absent.

**Check responsibility and authority.** Create a matrix of accountable owner, contributor, consumer, reviewer, and external authority by function/state/policy/evidence. Search for no owner, multiple conflicting owners, catch-all owners, and mode-dependent authority changes without a handoff protocol. Consultation does not equal accountability.

**Check allocation closure.** For every function/mode, verify adequate contributions and one integrated outcome owner unless a governed joint rule exists. Confirm allocations preserve scenario behavior and qualities. Every logical element’s responsibilities should justify its existence and trace upward.

**Check flow closure.** Every required input/control has a source; every output has a sink/effect; every crossing has a flow contract; every command has authority/lifecycle; every event has time/order/duplication semantics; every state transfer has ownership/reconciliation; every queue has capacity/backpressure; every feedback loop has delay/stability assumptions.

**Check interface compatibility.** Compare meaning, type/schema, unit, range, reference frame, direction, cardinality, ordering, timing, freshness, quality, security/privacy, modes, versions, errors, failure behavior, and ownership. If an adaptor resolves mismatch, allocate its transformation, state, timing, faults, and evidence.

**Check state and policy ownership.** Each semantic fact and decision policy needs an authoritative owner or explicit replicated/joint model. Identify writers, readers, versions, consistency, conflict resolution, retention, deletion, recovery, and evidence. A shared store is a realization choice, not an ownership rule.

**Check structural rules.** Validate unique identifiers, allowed relation types, endpoint kinds, containment, acyclic hierarchies, multiplicity, required attributes, port directions, and prohibited dependencies. Treat feedback/control cycles separately from accidental dependency cycles. Structural validity is cheap and should be automated, but it is only one layer.

**Check reachability and dead behavior.** Graph analysis can find unreachable states, functions with no trigger, components with no responsibility, disconnected paths, unused interfaces, sinks with no source, and outputs with no consumer. Some are intentional reserves or external boundaries; require disposition rather than automatic deletion.

**Check concurrency and race consistency.** Analyze simultaneous events, shared state, arbitration, ordering, idempotency, cancellation, retry, timeout, and partial completion. Two individually valid scenarios may conflict when concurrent. Define priorities and authority without assuming diagrams execute serially.

**Check temporal budgets.** Establish end-to-end deadlines and measurement points. Sum serial bounds, take appropriate maxima for parallel joins, and include sampling, detection, queues, transport, scheduling, computation, actuation, physical response, retries, and clock uncertainty. Check every applicable path/mode and prevent reuse of the same reserve.

**Check capacity and resources.** Balance arrival/service rates, burst, buffers, fan-out, compute, bandwidth, storage, mass, power, energy, thermal, crew time, spares, facilities, and support. Use consistent conditions and uncertainty. Allocations cannot exceed available totals after reserves, yet local compliance still may not prove end-to-end feasibility.

**Check quality composition.** For reliability, availability, safety, security, privacy, usability, accessibility, maintainability, accuracy, and resilience, state composition rules and evidence. Identify common causes, trust/fault boundaries, human workload, recovery, observability, and residual-risk authority. Crosscutting qualities cannot be covered by one linked component alone.

**Check enabling and lifecycle systems.** Include integration, test, calibration, training, configuration, key/identity management, deployment, update, diagnostics, maintenance, supply, backup, migration, support, incident response, decommissioning, data disposition, and disposal where they affect architecture. Omitting enabling systems makes nominal architecture look simpler than lifecycle reality.

**Check assumptions and external dependencies.** Every material assumption identifies owner, basis, applicability, consequence if false, validation method, due date, and affected claims. External systems/environment flows state service/authority/quality limits and fallback. “The network is available” is neither measurable nor owned.

**Check alternative-decision trace.** Confirm selected boundaries, allocations, and flows match the approved alternative and decision conditions. Preserve rejected alternatives and reversal criteria. A later convenience change can accidentally create a hybrid never evaluated under the original criteria.

**Check view correspondences.** Define rules such as: each scenario action realizes a controlled function; each allocated cross-element flow maps to an interface; each function’s mode matches state applicability; each quality requirement maps to budgets and evidence; each physical realization later maps to logical responsibility without identity confusion. Execute rules where possible and manually review semantic correspondences.

**Classify contradictions.** Distinguish true contradiction, version mismatch, scope difference, viewpoint abstraction, alternative configuration, temporal evolution, terminology mismatch, and incomplete information. Two views may legitimately show different detail. Resolve true contradictions using authority and rationale; do not force every view to contain everything.

**Use satisfiability and model checking carefully.** Solvers can test constraints, reachability, invariants, deadlock, or temporal properties for encoded finite/decidable fragments. Record model abstraction, environment, bounds, fairness, numeric approximations, state-space reductions, and property formalization. “Property holds” means it holds in that model under those assumptions.

**Use simulation and execution.** Execute behavioral/parametric models for scenarios, timing, capacity, control, failure, and resource interactions. Calibrate inputs and compare with independent methods or prototypes. Simulation can expose inconsistency and feasibility risk; it does not validate an omitted phenomenon.

**Conduct independent and stakeholder review.** Include domain, architecture, requirements, operations, maintenance, integration, test, cost/schedule, human-factors, safety, security, privacy, reliability, data, supplier, and affected-stakeholder competence proportional to consequence. Give reviewers the claim, evidence, open items, and adversarial scenarios—not just presentation slides.

**Manage open items honestly.** Classify gaps as blocker, risk, assumption, decision, waiver, deviation, debt, evidence action, or editorial issue. Record owner, consequence, priority, due/expiry, containment, affected baselines, and closure evidence. A list of unexplained placeholders is not governance.

**Define exit criteria and completeness frontier.** Specify which obligations must close before baseline, which may remain with authority, and why further resolution is unnecessary now. Examples include deliberately deferred physical protocols or supplier products while logical semantics and performance constraints are complete. Revisit when decisions need finer resolution.

**Write the bounded conclusion.** Report scope, baseline, checks, evidence, findings resolved, open items, waivers, residual risks, limitations, and competent approvals. State whether the architecture is sufficiently complete, internally consistent, and adequate for the named next decisions—not “the architecture is proven correct.”

The following checker finds selected declaration defects in five integrated logical-architecture records. It cannot assess semantic adequacy or real-world completeness.

<!-- bijux-verify: {"id":"logical-architecture-integrity-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"records_total=5\nwell_formed_declared=1\nmissing_source=ARCH-002\nmissing_owner=ARCH-003\nmissing_modes=ARCH-004\nmissing_evidence=ARCH-005\nunresolved=ARCH-002,ARCH-003,ARCH-004,ARCH-005\nevidence=declared_fields_only\n","stderr":""}} -->
```python
records = [
    {"id": "ARCH-001", "source": "REQ-014", "owner": "Control Policy",
     "modes": ["normal", "degraded"], "evidence": ["scenario SC-08"]},
    {"id": "ARCH-002", "source": "", "owner": "Sensor Interpretation",
     "modes": ["normal"], "evidence": ["flow FL-03"]},
    {"id": "ARCH-003", "source": "REQ-021", "owner": "",
     "modes": ["maintenance"], "evidence": ["state ST-05"]},
    {"id": "ARCH-004", "source": "HAZ-007", "owner": "Independent Protection",
     "modes": [], "evidence": ["fault scenario SC-19"]},
    {"id": "ARCH-005", "source": "DEC-011", "owner": "Evidence Custodian",
     "modes": ["all"], "evidence": []},
]
required = ("source", "owner", "modes", "evidence")
valid = [record for record in records if all(record[field] for field in required)]
print(f"records_total={len(records)}")
print(f"well_formed_declared={len(valid)}")
for field in required:
    print(f"missing_{field}=" + ",".join(record["id"] for record in records if not record[field]))
print("unresolved=" + ",".join(record["id"] for record in records if record not in valid))
print("evidence=declared_fields_only")
```

ARCH-001 may still be semantically wrong, infeasible, stale, or insufficiently evidenced despite its populated fields.

## Definitions and Notation

Let requirements (R), functions (F), scenarios (S), modes (M), states (T), logical elements (L), flows/interfaces (I), qualities (Q), decisions (D), assumptions (H), and evidence (X) remain typed domains. Trace relations must name semantics:

$$
Trace\subseteq (R\cup D\cup H)\times(F\cup S\cup L\cup I\cup Q)\times Type\times Version.
$$

For obligation set (O), a simple declaration coverage ratio is:

$$
C_d=\frac{|\{o\in O:declared(o)\}|}{|O|}.
$$

This is a dashboard, not proof: (declared(o)) may be semantically inadequate. A stronger review records (adequate(o,e,a)) under evidence (e) and assumptions (a), with unresolved/waived states kept separate.

For resource (r), allocations (b_i), reserve (m), and available capacity (B):

$$
\sum_i b_i+m\leq B.
$$

All terms must share units, reference configuration, conditions, and statistical/worst-case basis. The equation cannot detect a missing consumer, common-cause dependency, or incorrect availability model.

For correspondence rules (C_j), automated conformance is (\bigwedge_j C_j(AD)). The conclusion is limited to the encoded rules and loaded baseline.

## Mechanisms, Invariants, or Proof Structure

Use an architecture-integrity loop:

1. **Frame the claim:** identify scope, purpose, baseline, variants/modes, stakeholders, viewpoints, assumptions, exclusions, and evidence threshold.
2. **Derive obligations:** build coverage from concerns, requirements, scenarios, qualities, lifecycle, hazards/threats, decisions, and review criteria.
3. **Validate structure/configuration:** check identities, versions, metamodel rules, relation types, endpoints, vocabulary, and loaded artifacts.
4. **Check correspondences:** reconcile requirements, functions, scenarios, states/modes, elements, allocations, flows, interfaces, qualities, decisions, assumptions, and evidence.
5. **Analyze behavior/properties:** execute scenarios; analyze reachability, concurrency, cycles, timing, capacity, state, failure, trust, humans, lifecycle, and composition.
6. **Challenge and resolve:** inspect negative space and adversarial cases; classify contradictions; resolve or govern open items with authority and evidence.
7. **Conclude and govern:** document bounded readiness, limitations, waivers/debt, completeness frontier, approvals, monitoring, and change/recheck triggers.

Evidence layers should accumulate: structural checking supports well-formedness; trace review supports source/coverage; scenario execution supports behavioral consistency; analysis supports property feasibility; prototype/integration tests support realization assumptions; stakeholder validation supports adequacy. No lower layer automatically establishes a higher one.

## Alternatives and Trade-Offs

**Checklist versus obligation graph.** Checklists are accessible and useful for known omissions but can encourage box-ticking. Typed obligation graphs expose dependencies and impact but require tool/model discipline. Use both with semantic review.

**Central integrated model versus federated models.** One repository can improve identity and automation but become rigid or falsely authoritative. Federated domain models preserve specialist semantics but require configuration, vocabulary, and correspondence governance.

**Manual review versus automated checking.** Humans interpret meaning, context, and omissions; automation handles repeatable structure, traversal, arithmetic, and state exploration. Neither replaces the other.

**Strict closure versus governed openness.** Requiring every issue closed can create false declarations or delay learning. Allowing open items preserves iteration but can normalize debt. Risk-based exit criteria, owners, expiry, and closure evidence balance them.

**Broad shallow coverage versus narrow deep evidence.** Broad review detects omissions; deep analysis tests critical paths. Risk and decision purpose determine where depth is required, while the completeness frontier records intentional limits.

**Single master view versus multiple viewpoints.** One diagram is easy to navigate but cannot serve every concern without overload. Multiple views improve relevance but require explicit correspondences and version control.

**Formal proof versus empirical assurance.** Formal methods can give strong results for a model/property; empirical tests address realization and environment. High-consequence claims may need both, plus domain and stakeholder authority.

## Failure Modes and Misconceptions

- **Absolute-completeness claim:** no scope/purpose is named. Define the bounded claim and frontier.
- **Zero-errors fallacy:** a validator found no encoded issue. Record rule set, inputs, versions, and semantic limits.
- **Trace-count theater:** every requirement has a link, but contributions are meaningless. Review typed semantics and evidence.
- **View-local success:** each diagram passes while views contradict. Execute correspondence rules and integrated scenarios.
- **Nominal closure:** normal paths work but degraded/recovery/lifecycle paths are missing. Use a controlled scenario-mode matrix.
- **Orphan deletion:** an unjustified element is removed though it represents a missing derived need. Repair source and rationale first.
- **Name equality:** copied labels are treated as one identity. Govern identifiers and equivalence.
- **Owner ambiguity:** `system`, `shared`, or several components own a decision. Establish accountable authority and conflict rules.
- **Connected-interface fallacy:** ports connect but meaning, unit, time, quality, or failure semantics differ. Check full compatibility.
- **Budget basis mismatch:** mean and worst-case values, modes, or units are added. Normalize conditions and composition.
- **Margin reuse:** the same reserve covers several independent allocations. Assign and govern reserve once.
- **False redundancy:** logical duplicates share unmodeled causes. Analyze physical and organizational dependencies later and bound current claims.
- **Cycle purge:** all cycles are banned, destroying intentional feedback. Type cycles and analyze delay/stability/ownership.
- **Suppressed contradiction:** a tool warning is waived without consequence/expiry. Govern deviation and affected claims.
- **Evidence-version drift:** tests cover an obsolete model/configuration. Bind evidence and assess applicability after change.
- **Baseline-by-deadline:** unresolved blockers are relabeled editorial. Apply exit authority and state residual risk honestly.

## Worked Examples

### Example 1

A cold-chain model passes schema checks but fails integrated review: degraded mode disables the sensor flow used by Control Policy; two owners claim maintenance authority; sampling is slower than allowed freshness; and recovery omits policy reconciliation. The team corrects views and runs chamber/operator tests. The claim remains bounded to the tested configuration and temperature envelope.

### Example 2

A requirement `issue warning within 30 seconds` links to Warning Coordination. Trace count says covered. Scenario review shows authorization, carrier queue, cancellation, and evidence times are absent. The team creates allocated budgets and interfaces, then tests peak/degraded paths. One link became a meaningful end-to-end argument rather than administrative coverage.

### Example 3

A rail model has functions `detect obstruction`, `inhibit closure`, and `report disposition`. The logical allocation covers the first two but no element produces the disposition consumed by audit and operations. Flow-closure analysis identifies the orphan sink. A governed physical-state observation and Evidence Custodian responsibility close it; self-reported command receipt is rejected as effect proof.

### Example 4

A response deadline is 500 ms. Allocations are sensing 80, decision 120, communication 90, actuation 140, and reserve 50 ms, totaling 480 ms. A separate diagram adds a 40 ms authentication step but reuses the same 50 ms reserve and reports 470 ms. Integrated budget review finds the true serial total (80+120+90+140+40+50=520) ms, so the architecture does not close.

### Example 5

Two state views use `Safe`: one means hazards are controlled; the other means communications are minimal. Both can occur independently. Treating labels as identity creates contradictory transitions. The team defines `hazard_control_state` and `communications_mode`, their allowed combinations, and correspondence rules. Multiple viewpoints remain without forced semantic collapse.

### Example 6

A platform lists 100% function allocation. The `Operations` element owns backup, restore, key rotation, incident response, migration, monitoring, and retirement without contracts or capacity. Negative-space and ownership review decomposes these lifecycle responsibilities, derives flows/requirements, quantifies workload, and exposes supplier dependencies. The matrix was full but not adequate.

### Example 7

A redundant warning path shows two logical channel adaptors. Common-cause review finds one identity provider, one policy database, and one regional power source. The logical model records independence as an unverified assumption rather than claiming availability improvement. Physical architecture and fault testing must later justify or revise it.

### Example 8

A satisfiability solver proves no mode combination violates encoded invariants for up to three devices. Review discovers the real system supports 200 devices and the model omits simultaneous update and recovery. The result remains useful for the bounded fragment; additional abstraction, induction, simulation, and scale tests are required before a system claim.

### Example 9

A clinical alert architecture covers nominal and downtime scenarios but not alert fatigue, accessibility, or contested patient identity. Clinician and accessibility review adds workload, presentation, acknowledgement, correction, and escalation obligations. The logical model can support technical consistency; clinical safety and population adequacy require authorized external evidence.

### Example 10

An architecture review has twelve open items. Three are interface blockers, two are expired safety deviations, four are bounded evidence actions, and three are editorial. A single “open count” hides consequence. The team classifies owner, affected claim, due/expiry, containment, and exit authority. Baseline is withheld for blockers/expired deviations while bounded evidence actions remain visible under approved conditions.

## Cross-Program Connections

- **Platform engineering:** desired-state, policy, cell, tenancy, control/data plane, and operational models need cross-view reconciliation and failure closure.
- **API and service engineering:** contract compatibility, call/event flows, state ownership, retries, and end-to-end SLO budgets expose consistency defects.
- **Data engineering:** schemas, lineage, event time, quality, retention, deletion, and authoritative-source models require semantic/version consistency.
- **Object-oriented programming:** type checking and tests establish bounded properties; responsibility, invariants, concurrency, and system behavior still need integrated reasoning.
- **Functional programming:** composition and types expose data/control dependencies, while effects, resources, time, and environment bound completeness.
- **Security and safety:** threat/hazard controls require coverage, independence, failure behavior, evidence, residual-risk authority, and lifecycle governance.
- **Verification:** requirements, architecture, tests, configurations, and results must form exact evidence chains without using one layer to overclaim another.
- **Operations:** monitoring, update, recovery, support, and retirement reveal negative space often omitted from development-centered architecture.

## References

1. NASA, *Systems Engineering Handbook, Section 4.3: Logical Decomposition*, current web edition, updated 2023. <https://www.nasa.gov/reference/4-3-logical-decomposition/>
2. NASA, *Systems Engineering Handbook, Section 4.0: System Design Processes*, current web edition, updated 2023. <https://www.nasa.gov/reference/4-0-system-design-processes/>
3. NASA, *Systems Engineering Handbook Appendix C: How to Write a Good Requirement*, current web edition, updated 2023. <https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/>
4. Systems Engineering Body of Knowledge, *Logical Architecture*, SEBoK version 2.14, 2026. <https://sebokwiki.org/wiki/Logical_Architecture>
5. ISO/IEC/IEEE, *42010:2022 Software, systems and enterprise—Architecture description*, 2022. <https://www.iso.org/standard/74393.html>
6. ISO/IEC/IEEE, *15288:2023 Systems and software engineering—System life cycle processes*, 2023. <https://www.iso.org/standard/81702.html>
7. Object Management Group, *Systems Modeling Language Version 2.0*, formal specification, 2026. <https://www.omg.org/spec/SysML/2.0>
8. Object Management Group, *Systems Modeling Language Version 2.0, Part 1: Language Specification*, 2026. <https://www.omg.org/spec/SysML/2.0/Language/PDF>

## Exercises

### Exercise 1

Define a completeness/consistency claim and obligation catalogue for a municipal flood-warning logical architecture. Include scope, viewpoints, requirements, scenarios/modes, elements, allocations, flows, qualities, lifecycle, assumptions, evidence, and completeness frontier.

### Exercise 2

A 600 ms deadline has serial allocations of 90, 110, 140, 80, and 70 ms, interface overheads of 15 ms across four boundaries, clock allowance 20 ms, and required reserve 40 ms. Determine whether the budget closes and identify at least five consistency checks the arithmetic cannot establish.

### Exercise 3

Review this architecture: every requirement has one trace link; two elements may update authoritative customer status; recovery mode consumes a flow available only in normal mode; one scenario has no terminal failure outcome; and an availability calculation assumes two logical replicas are independent. Identify defect classes, affected correspondences, and corrective evidence.

### Exercise 4

An obligation catalogue has 80 items: 68 adequately discharged, 6 declared but semantically inadequate, 3 approved time-bounded waivers, and 3 unaddressed blockers. Compute declaration and adequate-coverage ratios under clearly stated counting rules. Explain why neither ratio decides readiness.

### Exercise 5

Design an architecture-integrity review for a multi-region authorization platform. Include automated and manual checks, adversarial scenarios, budget/resource reconciliation, state/authority, common cause, security/privacy, migration/recovery, evidence/version binding, open-item governance, exit criteria, and bounded conclusion.

## Answers to the Exercises

### Answer 1

Claim that the selected logical architecture baseline is sufficiently complete, internally consistent, and adequate to derive interface/element requirements and begin physical architecture for named river basins, normal/peak storm, uncertain forecast, communications-degraded, emergency, maintenance, update, recovery, and retirement conditions as of the review date. Exclude specific carrier protocols and purchased devices while retaining their logical semantics and bounds.

Obligations cover community/regulator/operator concerns; warning accuracy/timing/authorization/privacy/accessibility requirements; observation, interpretation, policy, warning, cancellation, evidence, and recovery functions; operational and failure scenarios; modes/states; Hydrologic Interpretation, Policy Authority, Warning Coordination, Channel Adaptation, Evidence, and Operator responsibilities; function allocations; observation/policy/command/disposition flows; state/policy authority; timing/capacity/security/privacy/accessibility/reliability/workload budgets; calibration/training/update/maintenance/support/data disposition; external forecast/carrier assumptions; and verification plans. Each records owner, applicability, source, evidence, disposition, and version. The frontier defers physical channel products and deployment topology until trade evidence exists; no safety/timing/interface blocker may be deferred.

### Answer 2

Stage allocations total (90+110+140+80+70=490) ms. Four interfaces contribute (4(15)=60) ms. With 20 ms clock allowance and 40 ms reserve:

$$
T=490+60+20+40=610\text{ ms}>600\text{ ms}.
$$

The architecture misses the declared deadline by 10 ms. Arithmetic also cannot establish that stages are truly serial; measurement points and clock bases match; values are worst-case or distributionally compatible; queue/load assumptions hold; retries and degraded paths are included; interfaces agree semantically; allocated functions have owners; commands are authorized; physical response is included; or evidence applies to the current configuration. Resolve rather than silently consuming required reserve.

### Answer 3

One trace per requirement is declaration coverage, not semantic adequacy; inspect contribution, modes, evidence, and derived obligations. Two authoritative status writers create an ownership/consistency contradiction; establish one owner or explicit version/conflict/reconciliation protocol. Recovery consuming a normal-only flow is a mode/flow correspondence failure; supply an applicable recovery source or redesign the scenario. Missing terminal failure outcome is scenario incompleteness and can leave state/resources/authority undefined; add bounded failure, evidence, and recovery. Logical replicas do not establish independence; record the assumption and analyze shared power, software, data, network, environment, supplier, and operator causes in physical realization and fault tests.

Corrective evidence includes typed trace review, state/authority model, mode-qualified flow contract, executable recovery/failure scenario, fault tree or dependency analysis, physical mappings, common-cause review, and configuration-specific tests. Re-run affected correspondence and budget checks after changes.

### Answer 4

If `declared` includes adequate items, semantically inadequate declarations, and approved waivers, but excludes unaddressed blockers, declared coverage is:

$$
C_d=(68+6+3)/80=77/80=96.25\%.
$$

If adequate coverage counts only adequately discharged obligations and does not count waivers as adequate, then:

$$
C_a=68/80=85\%.
$$

An alternative dashboard could report 3.75% waived, 7.5% inadequate, and 3.75% blocked separately. Neither ratio decides readiness because obligation consequence differs: one safety blocker can prevent baseline while many editorial obligations may not. Waiver authority/expiry, evidence quality, dependencies, claim scope, and exit criteria govern the decision. Ratios aid navigation; they do not aggregate risk or semantic adequacy.

### Answer 5

Bind exact requirements, policies, schemas, threat models, scenarios, logical views, test evidence, regions, tenant classes, and versions. Automate unique identity, allowed relations, trace endpoints, port direction/type, mode applicability, required fields, ownership cardinality, flow sources/sinks, forbidden dependency, budget arithmetic, reachability, and stale-evidence checks. Manually review semantic trace adequacy, policy/state authority, privacy purpose, human administration, threat/hazard controls, supplier/organization dependencies, and correspondence among scenarios, modes, allocations, flows, and qualities.

Exercise nominal authorization, cache hit/miss, urgent revocation, stale policy, network partition, identity/key failure, compromised region, clock fault, partial deployment, rollback, overload, tenant migration, region evacuation, recovery/rejoin, audit reconstruction, maintenance, and retirement. Reconcile latency/capacity/storage/update-bandwidth/admin-workload budgets with common conditions and reserve. Analyze shared identity, keys, policy source, software, telemetry, power, network, administrators, and suppliers. Verify least privilege, anti-replay, confidentiality, integrity, residency, retention/deletion, incident response, and evidence independence.

Classify findings as blockers, risks, assumptions, decisions, waivers, debt, evidence actions, or editorial issues with owner, consequence, due/expiry, containment, affected claim, and closure evidence. Exit only when hard security/privacy/authorization/recovery constraints and critical correspondences close; approved bounded items remain visible. Conclude that the named logical baseline is sufficiently complete and consistent for the named scale, topology, modes, threats, and next decisions, while physical independence, production performance, operational workload, and stakeholder validation remain bounded future evidence obligations.
