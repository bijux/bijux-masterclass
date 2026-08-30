---
module_id: SYSENG-017
program: Systems Engineering
level: 1
module_number: 17
title: Requirement Decomposition
status: complete
last_verified: 2026-08-31
---

# Requirement Decomposition

## One-Page Review

### Governing question

How can engineers transform a parent obligation into lower-level child requirements that are jointly sufficient, individually justified, consistent, feasible, and verifiable—while preserving parent intent, exposing integration obligations, and avoiding mechanical text splitting or premature architecture allocation?

### Essential definitions

- A **parent requirement** is a higher-level obligation whose intent is supported by one or more lower-level requirements and associated integration evidence.
- A **child requirement** is a lower-abstraction obligation derived to contribute a defined role in satisfying a parent requirement.
- **Requirement decomposition** transforms a higher-level obligation into a structured set of lower-level obligations and rationale using functional, behavioral, temporal, data, performance, state, hazard, interface, or lifecycle analysis.
- **Flowdown** is the governed propagation and transformation of requirements through successive system levels.
- **Allocation** assigns a requirement or contribution to an architecture element; decomposition determines lower-level obligations. The processes iterate but are not synonyms.
- A **derived requirement** arises from analysis, architecture, hazards, interfaces, technology, or lifecycle needs rather than verbatim restatement of a parent.
- A **coverage argument** explains why child requirements, assumptions, and integration obligations are sufficient for the parent under stated conditions.
- A **budget** partitions or constrains a parent quantity—mass, power, latency, capacity, error, cost, reliability contribution, or another measure—across lower-level contributors.
- An **integration requirement** governs behavior or qualities that emerge at interactions and cannot be satisfied by one child in isolation.
- **Over-decomposition** fragments meaning or creates unnecessary lower-level obligations; **under-decomposition** leaves work too vague for design, allocation, or verification.

### Central model, mechanism, or theorem

For parent \(p\), define a decomposition record:

\[
D(p)=\langle children,assumptions,interfaces,integration,
budgets,derived,coverageArgument,verification,authority,status\rangle.
\]

The sufficiency obligation is:

\[
A_p\land I_p\land\bigwedge_{c\in Children(p)} c\Rightarrow p,
\]

where \(A_p\) contains explicit assumptions and \(I_p\) contains integration obligations. The reverse implication is not generally true: a parent often does not uniquely determine one child set.

Every child also needs justification:

\[
\forall c:\ ParentRole(c,p)\lor DerivedSource(c),
\]

and verification closure:

\[
ChildEvidence+IntegrationEvidence\Rightarrow ParentVerificationArgument.
\]

These are review obligations, not automatic proofs of completeness or real-system satisfaction.

### Critical invariants

- Preserve the parent's source, subject, conditions, thresholds, exceptions, rationale, and verification intent.
- Each child is at the correct lower abstraction and has a unique contribution, parent role, or explicit derived source.
- Children are necessary enough to justify their cost and jointly sufficient only with named assumptions and integration obligations.
- Decomposition does not silently select components, suppliers, algorithms, interfaces, or human/system allocation before authority.
- Performance and resource budgets preserve units, boundary, aggregation, margin, uncertainty, and composition assumptions.
- Interfaces, coordination, sequencing, common-cause behavior, and emergent qualities receive explicit requirements/evidence.
- Duplicate parent text is not flowdown; every child expresses a lower-level obligation useful for realization or verification.
- Conflicts and infeasibility found below cause parent or architecture reconsideration rather than forced local compliance.
- Bidirectional traceability includes transformation rationale and impact propagation across every level.
- Parent acceptance uses both child evidence and system/integration evidence at the parent's stated level.

### Common failures

Failures include splitting a sentence at `and`; copying the parent to every subsystem; assuming child passes imply parent satisfaction; losing modes, exceptions, or population; allocating before alternatives are explored; deriving requirements without source; dividing a latency or reliability target with unjustified arithmetic; omitting interface and integration obligations; assigning the same budget twice; cascading excess precision; changing units or boundaries; creating children solely to match organization charts; ignoring humans, enabling systems, support, and retirement; and never revisiting an infeasible parent.

### Compact example

Parent: “During a declared emergency, the public-warning capability shall provide the authorized warning to affected people through the defined dissemination boundary.” Decomposition identifies authorization acceptance, audience/area determination, message representation, distribution to multiple channels, channel status, accessible variants, duplicate/update/cancel semantics, degraded operation, audit, and end-to-end outcome observation. Child requirements may later be allocated to services, operators, broadcasters, or devices. No single child proves the parent: interface agreements, timing/coverage budgets, authority, integration behavior, and representative end-to-end validation remain necessary.

### Connections

Retrieve stakeholder needs, operational concepts, functional/performance requirements, constraints, and quality/testability from SYSENG-011–016. Continue to allocation, bidirectional traceability, and requirement change/conflict. Later functional decomposition, flow models, logical components, interfaces, integration, architecture alternatives, verification, and validation deepen the mechanism.

## Governing Question

High-level requirements preserve stakeholder intent and design freedom, but they are often too broad to assign work or verify at lower levels. Lower-level requirements can make the system buildable, yet every transformation risks losing context or creating obligations the parent never justified. Decomposition is therefore an argument about contribution, not document formatting.

The governing question asks what lower-level truths, when combined with assumptions and integration behavior, are sufficient for the higher-level truth. Because multiple decompositions may satisfy the same parent, decomposition interacts with architecture alternatives and trade studies. The team must preserve options until a partition is justified, then keep the rationale and evidence visible.

## Why This Matters

Complex systems fail between apparently compliant children. Every component can meet its local response target while end-to-end latency fails. Two redundant elements can share a power supply and fail together. Product elements can protect their own data while an interface leaks it. A parent-to-child tree that ignores composition creates false confidence.

ISO/IEC/IEEE 29148:2018 defines parent/child and derived-requirement concepts and requires traceability across requirements engineering. NASA's logical-decomposition guidance describes recursive, iterative analysis of function, performance, behavior, time, data flow, state, mode, architecture, and interfaces, with derived technical requirements and willingness to revise parents as lower-level understanding improves. SEBoK 2.14 similarly treats child requirements, allocation roles, and parameter budgets as interdependent engineering decisions.

Decomposition is not always hierarchical in a simple tree. One child can support several parents; one parent can require children across product, human, process, support, and external-system boundaries; qualities crosscut functions; and interfaces create obligations owned jointly or at a higher integration authority. Use a graph with controlled views rather than forcing reality into a misleading tree.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. a requirement is a necessary, source-traceable obligation at a named system level;
2. operational threads expose end-to-end roles, modes, interfaces, failures, and recovery;
3. functions describe transformations, while performance/quality requirements constrain how well they occur;
4. constraints retain authority, scope, applicability, and temporal validity;
5. requirement quality includes necessity, feasibility, singularity, traceability, and verifiability;
6. evidence at a child level does not automatically establish a parent-level outcome;
7. architecture allocation assigns responsibility to selected elements and is developed in SYSENG-018.

As a retrieval test, decompose “The service shall be available 99.9% monthly” by simply giving three services 99.9% each. This does not work: serial composition would be lower under independence; redundancy, shared dependencies, partial service, repair, and end-to-end boundary change the result. The parent must first define required service and conditions; the architecture model then supports a justified availability allocation and integrated verification.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish decomposition, derivation, flowdown, allocation, partitioning, and simple restatement;
2. analyze parent semantics, system level, operational context, and verification intent before decomposition;
3. use functional, state, temporal, data, interface, hazard, and lifecycle models to generate children;
4. construct coverage arguments including assumptions and integration obligations;
5. decompose performance/resource budgets with correct units, margins, dependencies, and uncertainty;
6. identify crosscutting qualities, emergent behavior, human/enabling-system roles, and shared responsibilities;
7. review children for necessity, joint sufficiency, consistency, feasibility, atomicity, and verification closure;
8. detect duplication, gaps, wrong-level requirements, design leakage, and unjustified derived requirements;
9. propagate change and lower-level discoveries bidirectionally;
10. state evidence limits and escalate consequential judgments to appropriate authorities.

## Core Exposition

**Fix parent identity and level.** Record the obligated entity, source, rationale, type, status, operational context, modes, interfaces, thresholds, constraints, criticality, and verification concept. A stakeholder requirement, system requirement, subsystem requirement, and component specification carry different subjects and evidence. Never decompose an ambiguous parent merely to make ambiguity more detailed.

**Validate the parent before flowing it down.** Ask whether it is necessary, correct, feasible enough, singular, solution-responsible, and source-valid. Resolve or govern TBRs. If lower-level analysis exposes impossible physics, contradictory law, missing stakeholder need, or an incorrect boundary, return to the parent. Hierarchy does not make an upstream error authoritative truth.

**Choose decomposition viewpoints.** Functional analysis identifies input-output transformations. State/mode analysis identifies behavior by condition and transitions. Temporal/sequence analysis exposes ordering, concurrency, deadlines, and recovery. Data/material/energy flow exposes producers, consumers, custody, and conservation. Hazard/threat analysis derives controls. Lifecycle analysis exposes production, training, maintenance, update, transition, and disposal. Use several views because each reveals different gaps.

**Separate decomposition from allocation.** You can identify functions such as detect, authorize, decide, act, confirm, and recover without assigning them to components. Allocation later assigns requirements or contributions to selected logical/physical elements, humans, suppliers, or processes. In practice they iterate: candidate architectures reveal necessary children, but mark architecture-derived requirements and do not disguise choices as inevitable parent meaning.

**Define each child's contribution.** Store parent link, contribution role, transformation rationale, level, conditions, obligation, derived sources, siblings, interfaces, verification, and change coupling. A child may produce information, constrain quality, enforce safety, coordinate an interface, provide support, or consume a budget. “Supports parent P” is too vague.

**Construct a coverage argument.** State how children combine, which assumptions are required, what integration behavior closes the chain, and what evidence will test the parent. Walk representative operational scenarios from trigger to settled end state. Ask for a counterexample: can every child pass while the parent fails? Any plausible counterexample identifies a missing child, interface, assumption, integration requirement, or faulty composition rule.

**Use counterexamples as design work, not rhetorical objections.** Instantiate actual states, values, actors, timing, and failures. For a parent requiring correct account revocation, a counterexample might have identity credentials revoked while cached sessions remain active; all credential-service children pass but the parent outcome fails. Record which child, interface, cache-consistency rule, or system-level evidence closes the example. Re-run accepted counterexamples whenever decomposition, architecture, or assumptions change. A catalog of resolved counterexamples becomes durable rationale and an input to integration and verification planning.

**Check child necessity.** Remove one child conceptually. If the parent remains satisfied under all relevant conditions and no independent derived source exists, the child may be gold plating or duplicated. Necessity can be conditional: a recovery child matters only under a failure mode, yet that mode may be required. Record its condition rather than deleting it.

**Check joint sufficiency.** Sibling requirements may leave gaps between outputs and inputs, inconsistent states, unowned decisions, or omitted failures. Use producer-consumer matrices, state tables, sequence diagrams, functional flows, interface models, budgets, and hazard analyses. Sufficiency is always relative to named scope and evidence; unknown conditions remain possible.

**Preserve parent semantics.** Propagate exact modes, environments, population, timing boundary, definitions, exclusions, tolerances, and source authority. Children can refine but cannot silently narrow. If a child covers only one region or user class, siblings or an authorized parent change must address the rest.

**Avoid copydown.** Repeating “Subsystem A shall ensure system safety” does not identify controllable behavior or evidence. Restatement can preserve a constraint at multiple levels when genuinely applicable, but mark it as inherited and avoid counting duplicates as decomposition. Generate children that expose what each level must do or be.

**Decompose functions through transformations.** For a parent `provide verified location`, model acquisition, validation, source/provenance, conflict, fusion/selection, uncertainty, presentation, correction, and unavailable behavior. Children should preserve black-box obligations until allocation is justified. Do not select sensor or algorithm merely because functional verbs need owners.

**Decompose state and timing.** A response-time parent may span admission, queue, processing, dependencies, transmission, and presentation. Establish a deterministic or statistical composition model and preserve end-to-end measurement. Timing children can be budgets, not independent promises: changing one requires rebalancing siblings and margin.

**Budget additive resources carefully.** For mass, power, energy, storage, or deterministic worst-case time, define system boundary, operating profile, reserves, margin, sign, units, and aggregation. If parent maximum is \(B\), a simple budget may require

\[
\sum_i b_i + reserve \le B.
\]

Do not allocate the reserve twice. Predictions and design margin remain separate from mandatory child limits.

**Do not naively decompose statistical qualities.** Percentile latency, reliability, availability, accuracy, and security assurance depend on joint distributions, success logic, repair, correlation, shared dependencies, workload, and attack/failure models. A parent probability cannot usually be divided equally. Use architecture models, sensitivity, common-cause analysis, and integrated evidence.

**Capture interface and integration obligations.** When child A produces what child B consumes, define semantics, units, timing, quality, authority, failure, ownership, configuration, and compatibility. If no individual child owns orchestration or reconciliation, create an integration-level requirement with authority. Shared responsibility without an integrator is a gap.

**Treat crosscutting qualities explicitly.** Security, safety, privacy, accessibility, reliability, maintainability, resilience, and observability rarely decompose along one functional tree. Create crosscutting requirement views and trace them to every affected function/interface/lifecycle state. Avoid a single “security subsystem” child that falsely absorbs systemwide responsibility.

**Include humans and enabling systems.** Operational outcomes may depend on operator decisions, training, facilities, support, supply, calibration, emergency services, authorities, or external platforms. Define system behavior enabling human work and separate personnel/process obligations. Do not place an external entity under product control; use agreements, assumptions, interface requirements, and validation evidence.

**Derive requirements transparently.** Architecture, hazard analysis, interface selection, technology limits, regulation, or support concepts may create lower-level obligations absent from parent wording. Label source category, rationale, assumptions, owner, and approving authority. A derived requirement can be essential, but its legitimacy cannot be inferred from having a parent link.

**Define verification closure.** Each child needs a feasible verification concept. Parent verification must combine child results with integration/system evidence and a composition argument. An interface timing test, end-to-end scenario, hazard demonstration, or system analysis may be necessary even when every child has passed. Preserve configuration correspondence and uncertainty.

**Review sibling consistency and combined feasibility.** Check units, thresholds, timing, states, terminology, interface semantics, resource budgets, concurrency, precedence, and constraints. Model combined loads and failure modes. Children may each be feasible on separate assumptions that cannot coexist; reconcile the assumption set.

**Control recursion and stopping.** Decompose until an obligation is specific enough for the receiving design authority to realize and verify without hidden decisions, not until every sentence is tiny. Stop where further split would dictate internal design prematurely or fragment one invariant. Record the receiving level and unresolved choices.

**Propagate change bidirectionally.** Parent changes trigger child, budget, interface, architecture, test, supplier, and evidence impact analysis. Child infeasibility or operational learning can trigger parent revision. Maintain versioned rationale so deletion, merging, reparenting, and reassignment remain auditable.

**Govern the decomposition graph.** Store stable identities and typed edges such as `refines`, `contributes-to`, `inherits-constraint`, `derives-from-hazard`, `shares-budget`, `coordinates-with`, and `verified-with`. Define edge ownership and allowed source/target levels. Detect cycles that represent circular justification, but do not confuse legitimate behavioral feedback with a requirements-rationale cycle. Baseline graph snapshots with the requirement texts and models so a regenerated tree cannot silently omit crosscutting or many-to-many relationships.

**Use automated checks as bounded triage.** A tool can detect absent parent, rationale, lower level, verification, or declared integration link. It cannot establish semantic contribution, necessity, sufficiency, correct budgeting, or parent satisfaction. The example intentionally reports metadata defects only.

<!-- bijux-verify: {"id":"requirement-decomposition-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"children_total=5\nwell_formed_declared=1\nmissing_parent=CH-002\nmissing_rationale=CH-003\nnon_decreasing_level=CH-004\nmissing_verification=CH-005\nmissing_integration_trace=CH-003,CH-005\ndecomposition_ready=false\nevidence=declared_fields_only\n","stderr":""}} -->
```python
children = [
    {"id": "CH-001", "parent": "P-warning", "parent_level": 1, "level": 2,
     "rationale": "transforms authorized warning into channel request",
     "verification": ["interface scenario"], "integration": ["INT-warning-chain"]},
    {"id": "CH-002", "parent": "", "parent_level": 1, "level": 2,
     "rationale": "records channel response", "verification": ["record test"],
     "integration": ["INT-warning-chain"]},
    {"id": "CH-003", "parent": "P-warning", "parent_level": 1, "level": 2,
     "rationale": "", "verification": ["accessibility inspection"], "integration": []},
    {"id": "CH-004", "parent": "P-warning", "parent_level": 1, "level": 1,
     "rationale": "preserves cancellation semantics", "verification": ["state test"],
     "integration": ["INT-warning-chain"]},
    {"id": "CH-005", "parent": "P-warning", "parent_level": 1, "level": 2,
     "rationale": "reports terminal delivery state", "verification": [], "integration": []},
]

complete = [c for c in children if c["parent"] and c["rationale"] and c["level"] > c["parent_level"]
            and c["verification"] and c["integration"]]
print(f"children_total={len(children)}")
print(f"well_formed_declared={len(complete)}")
print("missing_parent=" + ",".join(sorted(c["id"] for c in children if not c["parent"])))
print("missing_rationale=" + ",".join(sorted(c["id"] for c in children if not c["rationale"])))
print("non_decreasing_level=" + ",".join(sorted(c["id"] for c in children if c["level"] <= c["parent_level"])))
print("missing_verification=" + ",".join(sorted(c["id"] for c in children if not c["verification"])))
print("missing_integration_trace=" + ",".join(sorted(c["id"] for c in children if not c["integration"])))
print(f"decomposition_ready={str(len(complete) == len(children)).lower()}")
print("evidence=declared_fields_only")
```

## Definitions and Notation

Let \(P\) be parent requirements, \(C\) child requirements, \(A\) explicit assumptions, \(I\) interface/integration requirements, \(B\) budgets, and \(V\) verification evidence.

For parent \(p\), \(Children(p)=\{c\in C\mid Trace(c,p,role)\}\). `Trace` includes a contribution role and rationale. Let \(Derives(c,s)\) identify a non-parent analytical source such as hazard, architecture, interface, regulation, or lifecycle analysis.

Define a counterexample set:

\[
CE_p=\{x\mid A_p(x)\land I_p(x)\land\bigwedge Children(p)(x)
\land \neg p(x)\}.
\]

Finding a feasible \(x\in CE_p\) refutes the current sufficiency argument. Failure to find one does not prove the set empty.

A **requirement tree** is a useful hierarchical view; the authoritative relation is often a graph because children can support multiple parents and integration requirements cross branches. A **budget allocation** is a coupled set whose sum/composition and margin support a parent parameter; it is not simply several unrelated thresholds.

## Mechanisms, Invariants, or Proof Structure

The mechanism has seven passes: validate parent; select analysis viewpoints; identify lower-level transformations/qualities; derive interfaces, budgets, and controls; construct the coverage argument; review children/set; close parent verification. Architecture and evidence feed back recursively.

Use a decomposition readiness predicate:

\[
Ready(D_p)=ParentValid\land ChildJustification\land CoverageArgument
\land InterfaceClosure\land BudgetConsistency\land CombinedFeasibility
\land VerificationClosure.
\]

The predicate structures expert review. `CoverageArgument` and `CombinedFeasibility` are not established by nonempty fields.

Maintain five invariants. **Intent invariant:** parent semantics and authority survive. **Contribution invariant:** every child has a unique role or derived source. **Composition invariant:** assumptions/interfaces/integration needed for sufficiency are explicit. **Budget invariant:** quantities preserve boundary, units, margin, and dependency rules. **Evidence invariant:** child evidence plus integration evidence supports but does not overclaim parent verification.

## Alternatives and Trade-Offs

**Top-down versus bottom-up discovery.** Top-down decomposition preserves intent; bottom-up knowledge reveals technology, interface, and operational reality. Iterate both, while preventing existing components from redefining needs without authority.

**Functional versus product decomposition.** Functional views preserve alternative realizations; product views support ownership and procurement. Develop function/behavior first enough to compare allocations, then maintain correspondence rather than forcing one hierarchy to serve both.

**Tree versus graph.** Trees communicate levels and ownership; graphs express shared children, crosscutting qualities, and integration. Use controlled tree views over an authoritative graph.

**Equal budgets versus optimized budgets.** Equal splits are simple but rarely reflect difficulty or consequence. Model sensitivities, margins, feasibility, cost, and risk; retain coupled change control.

**Local verification versus parent-level evidence.** Local evidence is efficient and diagnostic; end-to-end evidence captures interfaces/emergence. Combine them according to consequence and composition confidence.

**Deep decomposition versus design freedom.** More detail can reduce ambiguity but freeze architecture and increase management cost. Stop at a verifiable obligation accepted by the receiving design authority.

## Failure Modes and Misconceptions

1. **“Decompose means split the sentence.”** Logical contribution and system level, not punctuation, determine children.
2. **“Every child needs exactly one parent.”** Derived and crosscutting requirements can have several justified sources.
3. **“A tree proves coverage.”** It shows recorded links, not semantic sufficiency or undiscovered gaps.
4. **“Allocation and decomposition are the same.”** One derives obligations; the other assigns roles to selected elements.
5. **“Equal numerical allocation is neutral.”** It embeds feasibility and risk assumptions and may be impossible.
6. **“All child passes imply parent pass.”** Integration, common cause, interfaces, and emergent behavior remain.
7. **“Copying a constraint downward is decomposition.”** Inheritance can be valid but does not explain each lower-level contribution.
8. **“Derived requirements are gold plating.”** Properly sourced hazard, interface, lifecycle, or architecture obligations can be essential.
9. **“Lower-level infeasibility is a local problem.”** It may invalidate parent, budget, or architecture.
10. **“Decomposition ends at code modules.”** Stop level depends on acquisition, design authority, system type, and verification.

## Worked Examples

### Example 1

**Situation.** Decompose an emergency-warning distribution parent. **Reasoning.** Use authorization, audience, representation, channel distribution, accessible variants, update/cancel, status, audit, degraded mode, and recovery functions. Add channel interface and end-to-end integration obligations. Preserve affected people and emergency conditions. **Conclusion.** Children plus channel agreements and integrated observation form the coverage argument; a message-sender child alone does not.

### Example 2

**Situation.** A 500 ms deterministic end-to-end deadline spans four stages. **Reasoning.** Model start/stop, concurrency, dependencies, and worst-case composition. Allocate 80+120+180+70 ms and 50 ms integration/reserve only if maxima share semantics and can compose. Control coupled changes and retain end-to-end test. **Conclusion.** A timing budget is an analytical contract with margin, not four arbitrary targets.

### Example 3

**Situation.** A parent mission reliability is 0.99. **Reasoning.** Equal 0.995 requirements on two elements are meaningless without series/parallel success logic, mission time, repair, coverage, independence, and common-cause model. Derive failure containment, detection, switching, state consistency, and integrated mission evidence. **Conclusion.** Reliability decomposition follows architecture and probability assumptions, not division.

### Example 4

**Situation.** “Protect patient records from unauthorized disclosure.” **Reasoning.** Decompose identity/authorization, least privilege, data-flow control, encryption/key lifecycle where justified, logging/detection, backup/export, support access, incident response, deletion, supplier and physical interfaces. Crosscut every data path and mode. **Conclusion.** One security component cannot inherit the whole parent; systemwide policy and integration evidence are required.

### Example 5

**Situation.** Retain regulated records for a stated horizon. **Reasoning.** Children cover classification, creation/provenance, clock, durable storage, access, integrity, legal holds, migration, backup, retrieval, disposition, and evidence. Interfaces with deletion/privacy obligations require authority. **Conclusion.** A storage-duration configuration is insufficient without lifecycle and conflict behavior.

### Example 6

**Situation.** A rescue outcome depends on dispatcher judgment and automated location. **Reasoning.** Decompose system-provided estimates/provenance/uncertainty, dispatcher information and authority, training/procedure, communication, escalation, and unavailable/conflict behavior. Do not make software responsible for human judgment or hide system support behind a personnel requirement. **Conclusion.** Human-system decomposition preserves distinct controlled subjects and joint validation.

### Example 7

**Situation.** Two redundant controllers pass every child requirement but share corrupted configuration. **Reasoning.** Redundancy children do not cover configuration independence, diversity, common power/network, fault detection, voting, transition, or recovery. Add system/integration obligations and common-cause analysis. **Conclusion.** Emergent reliability lives in relationships and cannot be proven by duplicated component passes.

### Example 8

**Situation.** A regulation requires an organization to report defined incidents. **Reasoning.** Allocate organizational decision/reporting duties separately from system capabilities for detection evidence, time/provenance, classification support, secure record, report preparation, and transmission. Preserve legal authority for reportability. **Conclusion.** Decomposition must not turn governance judgment into an autonomous product duty.

### Example 9

**Situation.** A parent requires equitable AI decision support. **Reasoning.** Derive data provenance/coverage, missingness, performance distributions, uncertainty/abstention, explanation/context, human review, override/recourse, monitoring/drift, and change governance across affected groups. Metrics and tradeoffs need domain/affected-stakeholder authority. **Conclusion.** Quality decomposition produces multiple interacting obligations but cannot prove fairness from component metrics.

### Example 10

**Situation.** Emergency shutdown must reach a safe physical state. **Reasoning.** Children cover trigger/authority, command propagation, actuator isolation, stored-energy release, feedback, timeout, indication, records, reset, and degraded/fault behavior. Safety analysis identifies common cause and end-state hazards; integrated tests observe the physical boundary. **Conclusion.** Parent verification closes only with child, interface, hazard, and end-to-end system evidence.

## Cross-Program Connections

- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) provides domain invariants, commands, events, policies, and boundaries for semantic decomposition.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) supplies candidate structures and composition assumptions without making them inevitable parent meaning.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) decomposes data transformation, quality, provenance, retention, reconciliation, and evidence obligations.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) derives crosscutting protection and assurance requirements from threats, assets, policy, and risk.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) turns boundary contributions into explicit semantic, state, timing, error, and compatibility contracts.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) coordinates shared requirements and budgets across product teams while preserving end-to-end ownership.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html), second edition, 2018. Consulted 2026-08-31.
2. ISO/IEC/IEEE. [ISO/IEC/IEEE 15288:2023 — System life cycle processes](https://www.iso.org/standard/81702.html), second edition, 2023. Consulted 2026-08-31.
3. NASA. [Logical Decomposition](https://www.nasa.gov/reference/4-3-logical-decomposition/), *NASA Systems Engineering Handbook*, Rev. 2. Consulted 2026-08-31.
4. NASA. [System Design Processes](https://www.nasa.gov/reference/4-0-system-design-processes/), recursive decomposition and design guidance. Consulted 2026-08-31.
5. NASA Software Engineering Handbook. [Software Requirements](https://swehb.nasa.gov/spaces/7150/pages/146540272/SWE-050%2B-%2BSoftware%2BRequirements), requirements decomposition and flowdown guidance. Consulted 2026-08-31.
6. SEBoK Editorial Board. [System Requirements Definition](https://sebokwiki.org/wiki/System_Requirements_Definition), *Guide to the Systems Engineering Body of Knowledge*, version 2.14. Consulted 2026-08-31.
7. INCOSE Requirements Working Group. [Needs and Requirements Manual, Section 6 overview](https://www.incose.org/docs/default-source/working-groups/requirements-wg/needsandrequirementsmanual/nrm_section_6_overview_042023s.pdf), including child requirements that meet allocated-parent intent. Consulted 2026-08-31.
8. INCOSE Requirements Working Group. [*Guide for Writing Requirements*, version 4](https://www.incose.org/docs/default-source/working-groups/requirements-wg/gtwr/incose_rwg_gtwr_v4_040423_final_drafts.pdf), 2023. Consulted 2026-08-31.

## Exercises

### Exercise 1

Distinguish decomposition, flowdown, allocation, derivation, restatement, and budgeting using one system-level emergency-notification requirement.

### Exercise 2

Decompose “The service shall restore correct order-processing capability within 30 minutes of a regional compute loss.” Include assumptions, states, interfaces, correctness, timing budget, recovery, and parent verification.

### Exercise 3

Construct and challenge a mass/power/timing budget for a small autonomous field device. Show units, reserve, operating profiles, coupled change, and counterexamples.

### Exercise 4

Compare functional, state, data-flow, hazard, and lifecycle decompositions for an electronic medication administration capability. Explain why no single tree is sufficient.

### Exercise 5

Develop a coverage argument and verification closure for a remotely supervised rail-crossing safety parent requirement. Include human roles, interfaces, common cause, degraded operation, maintenance, cybersecurity, and external authority.

## Answers to the Exercises

### Answer 1

Start with the parent outcome and function: during an authorized emergency, the warning capability provides governed information to affected people across defined conditions. **Decomposition** derives lower-level obligations for authorization, audience, message semantics, dissemination, accessibility, status, update/cancel, audit, degradation, and recovery. **Flowdown** is the controlled recursive transformation of those obligations through system levels. **Allocation** assigns contribution roles to selected elements—operator, warning service, carrier/broadcaster, local device, support process—after architecture authority.

**Derivation** adds necessary obligations from hazards, privacy/security, interfaces, support, or law that the parent did not state verbatim. **Restatement** repeats the parent at a lower level; it may inherit a genuine constraint but adds no contribution analysis. **Budgeting** partitions coupled quantities such as end-to-end dissemination time, capacity, or power with margin and composition rules. Every child retains source/role/rationale, while interface and system evidence close the parent.

### Answer 2

Define correct capability and regional compute loss, detection/decision authority, start event, acceptable degraded modes, order states, data-loss point, dependencies, workload, and restored end state. Children cover loss detection; isolation of uncertain processing; preservation of accepted-order identity/state; activation of alternate capacity; dependency and credential readiness; replay/idempotency; reconciliation of partial/duplicate/conflicting effects; validation of inventory/payment/fulfillment interfaces; restoration of intake and processing; status/notification; evidence and rollback. A fast but inconsistent restart fails.

Assumptions about independent regions, data replication, network, suppliers, and staff receive evidence and failure behavior. A 30-minute budget may partition detection, decision/failover, recovery, reconciliation, and readiness verification with reserve, but only if worst-case/percentile semantics compose. Parent verification combines child tests, failure injection, interface/state reconciliation, workload and dependency-loss cases, restart/repeated failure, and an end-to-end oracle proving correct order outcome within the same timing boundary. Operational exercises validate staff and external dependencies; finite tests do not prove every regional event.

### Answer 3

Define device boundary and operating profiles: sensing idle, computation, communication burst, actuation, charging, degraded, emergency, cold/hot environment, and mission duration. Suppose mass limit is 5 kg: allocate explicit element maxima plus integration hardware and a separately controlled reserve such that their sum is at most 5 kg. Power needs instantaneous and average/energy views: battery energy in Wh cannot be added to W; duty cycles and conversion losses matter. Timing budgets define end-to-end event boundaries and whether component maxima can coexist.

Track prediction, allocation, uncertainty, margin, owner, and configuration for each row. Coupled change means an antenna mass increase consumes system reserve; extra compute raises peak power, thermal load, and perhaps sensing latency. Counterexamples include all components meeting average power while simultaneous peaks brown out; mass rows omitting harness/fasteners; timing maxima occurring under incompatible test profiles; and reserve counted at both subsystem and system levels. Verify component values plus integrated profiles and rebaseline only under system budget authority.

### Answer 4

Functional decomposition identifies prescribe/authorize, identify patient/medication, validate order, prepare, administer, observe, document, reconcile, and respond. State decomposition exposes ordered, prepared, held, cancelled, administered, uncertain, corrected, and adverse-event transitions. Data flow covers identity, allergies, medication/order, lot/dose, time, provenance, signatures, records, and external systems. Hazard analysis derives wrong-patient/drug/dose/route/time controls, duplicate prevention, stale/conflicting data behavior, alarm/escalation, and safe downtime. Lifecycle analysis adds procurement, configuration, training, calibration, cleaning, updates, support, audit, recall, migration, and retirement.

No tree captures all cross-links. Identity and authorization affect many functions; hazards cross states and interfaces; record obligations persist after administration; humans and pharmacy/lab/EHR systems sit outside product control; safety and accessibility are crosscutting. Maintain an authoritative graph with functional, state, data, hazard, and lifecycle views, plus coverage and interface/integration requirements. Clinical, pharmacy, nursing, human-factors, safety, privacy/security, quality, and regulatory authorities validate the resulting obligations.

### Answer 5

The parent must define safe crossing outcome, road/rail users, train/road/environment states, warning horizon, supervised role, and degraded/maintenance conditions. Children cover train approach/state acquisition; crossing occupancy/obstruction evidence; command and warning behavior; barrier/light/sound states; interlocking; local minimum-risk behavior; remote status/control with authority; event timing/provenance; communication loss; power loss; fault detection; alarm/escalation; maintenance isolation and return-to-service; records; and emergency coordination. Interfaces specify railway signaling, roadside equipment, control center, power/network, responders, and maintainer custody.

Assumptions include sensor coverage, communication independence, human response, environmental limits, train braking envelope, and common power/configuration. Hazard and cybersecurity analysis derive protection against stale/false commands, unauthorized override, common cause, concealed failure, and unsafe reset. The coverage argument walks normal approach through settled state and counterexamples: every device locally passes but clocks disagree, shared power fails, remote control masks local fault, or maintainer leaves bypass active.

Verification combines child inspection/test/analysis, state and fault-tree review, interface timing, environmental and power tests, cyber fault/adversarial tests, communication partition, maintenance transition, human supervision exercises, and integrated train/road scenarios observing the physical safe-state boundary. Parent acceptance needs child plus integration evidence and applicable railway, road, safety, human-factors, cybersecurity, maintenance, emergency, and regulatory authority. Internal analysis cannot establish public safety or legal conformity; no external review is claimed.
