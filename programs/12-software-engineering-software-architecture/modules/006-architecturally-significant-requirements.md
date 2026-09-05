---
module_id: SARCH-006
program: Software Engineering: Software Architecture
level: 1
module_number: 6
title: Architecturally Significant Requirements
status: complete
last_verified: 2026-09-05
---

# Architecturally Significant Requirements

## One-Page Review

### Governing question

Which requirements must shape architecture early because their consequences, reach, constraints, uncertainty, or reversal cost make local treatment unsafe or expensive?

### Essential definitions

- A **requirement** is a verifiable statement of a needed capability, condition, or quality under defined scope and authority.
- An **architecturally significant requirement** (ASR) materially influences system-wide structures or difficult-to-reverse decisions.
- A **driver** is an input significant enough to shape architecture; ASRs are requirements among the wider set of goals, constraints, assumptions, and risks that can drive decisions.
- **significance** is decision-relative: it depends on consequence, cross-cutting reach, irreversibility, uncertainty, and option loss.
- **allocation** assigns responsibility for satisfying a requirement to system elements and interfaces without losing end-to-end ownership.
- **verification** asks whether the specified requirement was met; **validation** asks whether the requirement and resulting system serve stakeholder needs in context.
- A **derived requirement** follows from a higher-level requirement plus architecture decisions or analysis and must retain its rationale.

### Central model, mechanism, or theorem

Trace each candidate requirement through

$$
goal\rightarrow concern\rightarrow scenario\rightarrow requirement\rightarrow decision\rightarrow evidence.
$$

Assess its significance using a structured profile rather than a universal score. Promote a requirement to the ASR register when it materially constrains multiple structures, system boundaries, quality responses, technology options, delivery or operational organization, or costly lifecycle commitments. Keep the original requirement in its authoritative requirements system; the ASR register is a decision-focused view, not a second source of truth.

### Critical invariants

- preserve requirement source, authority, rationale, scope, and lifecycle state;
- make the required response, conditions, measure, and acceptance authority explicit;
- identify architectural significance with evidence, not reputation or category alone;
- include functional, quality, interface, data, operational, regulatory, migration, and retirement requirements as applicable;
- trace ASRs to context, constraints, assumptions, risks, decisions, and evidence;
- allocate responsibilities without replacing the end-to-end outcome by component proxies;
- record derived requirements and their premises bidirectionally;
- expose conflicts, uncertainty, infeasibility, and unallocated responsibility;
- distinguish verification from stakeholder validation;
- reopen ASRs when context, evidence, architecture, or authority changes.

### Common failures

Common failures include calling every requirement architectural; assuming only quality attributes matter; selecting ASRs by executive emphasis; copying a long specification into an architecture document; rewriting requirements and creating competing authorities; treating technology choices as requirements; allocating latency or availability without a composition model; losing rationale for derived requirements; marking a requirement verified from component tests; ignoring migration and retirement; and freezing early guesses because the register says “approved.”

### Compact example

“Export invoices as CSV” may be a local feature. “Preserve legally required invoice records for seven years, produce a complete authorized export within four hours, and prove provenance after supplier replacement” affects data authority, storage, cryptographic evidence, access, migration, recovery, and retirement. Its consequence and reach make it architecturally significant. The architecture may derive format, replication, audit, and migration requirements, but every derivation needs a traceable premise and evidence plan.

### Connections

[SARCH-002](002-stakeholders-and-architectural-concerns.md) establishes concern provenance; [SARCH-003](003-functional-scope-and-system-context.md) defines the outcome boundary; [SARCH-004](004-quality-attributes-as-architectural-drivers.md) operationalizes qualities; and [SARCH-005](005-constraints-assumptions-and-risks.md) exposes decision conditions. [SARCH-007](../ROADMAP.md) analyzes conflicts among selected ASRs and other objectives.

## Governing Question

Specifications can contain hundreds or thousands of requirements. Architecture cannot treat them all as equally formative, yet overlooking one significant requirement can invalidate an otherwise coherent design. Which requirements deserve early, system-wide attention, and how can that selection remain traceable and revisable?

The problem is not to create a privileged class of vague “architecture requirements.” It is to identify requirements whose satisfaction depends on major structures, boundaries, cross-cutting mechanisms, or lifecycle commitments, then connect them to decisions and evidence without breaking the authoritative requirements chain.

## Why This Matters

Architectural capacity for recovery, security, performance, evolution, integration, and migration is expensive to retrofit. A requirement may appear small in prose while forcing broad consequences: data deletion affects every copy and export; offline operation affects identity, storage, conflict, and synchronization; one mandated interface can constrain release and failure behavior across organizations.

The reverse error also costs. Treating every feature as an ASR produces an unreadable architecture, centralizes local decisions, and prevents teams from adapting implementation. Significance should focus attention on decisions with broad reach, consequence, uncertainty, or option loss.

An ASR view also enables auditability. Reviewers can ask which stakeholder goal justified a mechanism, which assumption supports an allocation, what evidence will verify it, who validates the outcome, and what happens when the requirement changes. Without these links, architecture becomes a collection of preferences.

## Prerequisites and Retrieval

Retrieve stakeholder, goal, concern, requirement, constraint, assumption, risk, scenario, source, authority, rationale, scope, interface, invariant, allocation, architecture decision, tactic, verification, validation, acceptance criterion, traceability, baseline, and change control.

From prior modules, retrieve architectural significance, the known-inventory limitation, system context, quality-attribute scenario anatomy, and the difference among constraint, assumption, risk, and issue. Be able to distinguish a stakeholder statement from a normalized requirement and a selected architecture mechanism from both.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish an ASR from an ordinary local requirement and from a general driver;
2. discover ASRs across functional, quality, interface, data, operational, and lifecycle concerns;
3. assess significance using consequence, reach, irreversibility, uncertainty, and option cost;
4. preserve source, authority, rationale, and original requirement identity;
5. allocate requirements while retaining end-to-end ownership;
6. derive lower-level requirements with explicit premises;
7. identify conflict, infeasibility, and hidden coupling among ASRs;
8. design verification and validation evidence appropriate to each claim;
9. maintain an ASR view without creating a duplicate source of truth;
10. reopen architecture when significant requirements or their premises change.

## Core Exposition

**Requirements become significant in context.** A requirement category does not determine architectural significance. A two-second response may be local in a small offline tool and system-wide in a global workflow with several suppliers. A formatting rule may be local until it is a regulated interchange contract used by hundreds of partners. Ask what decisions it constrains and what failure costs.

Assess at least five dimensions: consequence if unmet, reach across elements and organizations, irreversibility or cost of late change, uncertainty requiring early learning, and option cost created by commitment. Also consider concurrency, scale, security, failure, jurisdiction, evolution, and lifecycle duration. Do not sum these blindly; one non-compensable obligation can be decisive.

**Discover beyond quality labels.** Quality scenarios are common ASRs because they cross structures. Functional requirements also qualify when they establish core domain invariants, transactional boundaries, human authority, or end-to-end coordination. External-interface requirements can constrain protocol semantics and organizational contracts. Data requirements determine authority, retention, lineage, residency, and migration. Operational requirements govern observability, recovery, deployment, and support. Acquisition, transition, and retirement requirements shape temporary and terminal architectures.

**Preserve pedigree.** Record stable requirement ID, authoritative source, stakeholder or authority, rationale, status, scope, version, priority basis, and change owner. Link the ASR view to that record. Do not paste and rewrite it into a disconnected architecture document; parallel copies drift and make approval ambiguous.

Trace back to business or mission goal and concern. A requirement with no source can still expose an important gap, but it remains proposed until the proper authority evaluates it. An architect can derive technical obligations from decisions, but cannot manufacture legal, clinical, safety, or business authority.

**Normalize for analysis.** A good ASR states the subject, required response or condition, triggering environment, measure, and scope. Resolve ambiguous pronouns, undefined terms, units, and exclusions. Separate compound requirements when different owners or evidence apply, while preserving their shared rationale.

Use examples and counterexamples with stakeholders. “Recover the service within one hour” needs failure classes, start and end observations, data recovery point, dependencies, capacity, geography, and business windows. “No unauthorized disclosure” needs assets, actors, trust context, behavior, detection, and evidence; absolute language may require refinement rather than quiet weakening.

**Select without losing the whole specification.** The ASR register should be a projection or index over authoritative requirements. It adds significance rationale, affected structures, linked decisions, risks, and evidence. A requirement not classified as an ASR remains binding if authoritative; it is not discarded. Selection determines architecture attention, not validity.

Use workshops, scenarios, utility trees, context walks, hazard or threat analysis, operational reviews, incidents, dependency maps, and change-history evidence. Each method has blind spots. Include maintainers, operators, security, data, support, affected users, suppliers, assurance, and lifecycle owners as applicable.

**Allocate carefully.** Architecture decomposes an end-to-end requirement into responsibilities and budgets. Allocation is valid only with a composition argument. If end-to-end latency is two seconds, arbitrary equal budgets across four components ignore parallelism, queueing, network tails, retries, and shared margin. If availability is 99.9%, assigning 99.9% to every serial dependency cannot produce the same end-to-end result.

Preserve one outcome owner and show how local requirements jointly support it. Record budgets, assumptions, interaction terms, margin, monitoring, and reallocation authority. If no composition model exists, label the allocation provisional and validate end to end.

**Derive requirements explicitly.** Suppose a recovery ASR and an architecture decision introduce asynchronous replication. Derived requirements may constrain replication lag, backup independence, failover authorization, reconciliation, and recovery exercises. Each derived item needs its parent, decision or analysis premise, owner, verification method, and change propagation rule.

Derived does not mean optional or inferior. Once baselined under authority, it becomes part of the requirement set. But when its parent or architecture premise changes, it must be reviewed; otherwise obsolete implementation constraints survive their reason.

**Expose conflict and feasibility.** ASRs compete with one another and with cost, schedule, skills, and constraints. Strong consistency across long network partitions conflicts with continuous availability for some operations. Deep isolation can increase cost and change burden. Immediate global deletion can conflict with immutable audit or recovery obligations unless scope and lawful retention are reconciled.

Do not resolve conflict by silently changing numbers. Record alternatives, sensitivity, evidence, affected stakeholders, authority, and residual risk. If the set is infeasible, report that before selecting technology. Architecture cannot make contradictory obligations simultaneously true.

**Plan evidence at selection time.** Identify inspection, analysis, model, test, demonstration, experiment, exercise, production observation, or qualified review. Verification asks whether the requirement is satisfied as specified. Validation asks whether it expresses the right need and whether the resulting system serves it in context. Both require named environments, versions, and limitations.

Trace evidence to the complete outcome. Passing component tests can support allocated requirements; it does not automatically verify the end-to-end ASR. For high-consequence domains, qualified independent review and domain-specific processes may be mandatory. Internal architectural review cannot substitute for external authority.

**Maintain significance.** Requirements and architecture co-evolve. A local requirement can become architectural after scale, regulation, reuse, or supplier change. An ASR can become local after a platform supplies a well-evidenced capability. Reassess significance after incidents, new populations, boundary shifts, acquisitions, deployment changes, or invalidated assumptions.

## Definitions and Notation

Let $Req$ be the authoritative set of known requirements and $ASR\subseteq Req$ the current architecturally significant projection. For $r\in Req$, define a significance profile

$$
sig(r)=(consequence,reach,irreversibility,uncertainty,optionLoss).
$$

Classification is a governed judgment $classify(r,context,evidence)$ rather than a universal numeric threshold. The same requirement can change classification when context changes.

Let $D$ be architecture decisions, $E_v$ evidence items, and $Elem$ allocated elements. Relations include

$$
motivates\subseteq ASR\times D,
$$

$$
allocatedTo\subseteq Req\times Elem,
$$

and

$$
verifiedBy\subseteq Req\times E_v.
$$

For a derived requirement $d$, record $derive(d)=(parents,premises,decision,rationale)$. A trace-complete known ASR has an authoritative source, significance rationale, responsible outcome owner, decision or explicit unresolved disposition, and evidence plan. Trace completeness is not requirement correctness or discovery completeness.

For serial components with independent availability $a_i$ and a workflow requiring all components, the simplified model is

$$
A_{end}=\prod_i a_i.
$$

If three serial dependencies each have $a_i=0.999$, then $A_{end}=0.999^3\approx0.997003$, below 0.999. Independence, stationarity, binary success, and required-all composition are strong assumptions; shared causes and degraded responses require richer models.

## Mechanisms, Invariants, or Proof Structure

Use this repeatable ASR process.

1. **Frame:** declare system, lifecycle, decision horizon, authoritative requirement sources, and stakeholder authorities.
2. **Discover:** walk goals, context, quality scenarios, functions, interfaces, data, operations, constraints, risks, migration, and retirement.
3. **Normalize:** make candidate requirements atomic enough for ownership and evidence while preserving original rationale.
4. **Profile significance:** analyze consequence, reach, irreversibility, uncertainty, option loss, and domain obligations.
5. **Select and record:** add a traceable ASR view without duplicating requirement authority.
6. **Analyze interaction:** find conflicts, shared mechanisms, hidden coupling, infeasible combinations, and assumptions.
7. **Allocate and derive:** retain end-to-end ownership, composition models, margin, premises, and change propagation.
8. **Decide:** compare alternatives and trace selected architecture mechanisms to ASRs and residual risk.
9. **Plan and collect evidence:** distinguish verification, validation, and qualified acceptance.
10. **Monitor and reopen:** reassess classification and decisions after requirement, context, evidence, or architecture change.

The governing invariants are authoritative pedigree, explicit significance rationale, no discarded requirement, end-to-end ownership, justified allocation, traceable derivation, visible conflict, claim-specific evidence, separate verification and validation, and lifecycle revision.

Structural trace checks can show that known ASRs have links and required fields. They cannot prove the requirement set is complete, a significance judgment is correct, allocated budgets compose, evidence is valid, or stakeholders accept the outcome.

## Alternatives and Trade-Offs

**Expert selection** is fast and uses architecture experience but inherits individual blind spots and authority bias. **Multi-stakeholder workshops** expose conflicts and context but consume time and reflect participation power. Combine expert preparation, diverse elicitation, and evidence-backed challenge.

**A small ASR list** keeps decisions focused but risks omitting lifecycle or minority concerns. **A broad list** improves visibility but dilutes attention and duplicates the specification. Use explicit selection criteria, preserve the full authoritative set, and audit rejected candidates.

**Central allocation** supports end-to-end coherence and shared budgets but can create bottlenecks and weak local ownership. **Team-local allocation** improves autonomy but can lose composition and margin. Keep outcome ownership and governing budgets central enough to compose, while delegating local implementation and evidence.

**Early baselines** stabilize coordination but freeze uncertain interpretations. **Late baselines** preserve learning but can delay dependent work. Baseline high-confidence external obligations and reversible hypotheses differently; use assumptions, options, and change authority explicitly.

## Failure Modes and Misconceptions

- **“ASRs are nonfunctional requirements.”** Significant functional, interface, data, operational, migration, and retirement requirements also shape architecture.
- **“All quality requirements are ASRs.”** Significance depends on context and decision reach.
- **“The architect decides the requirements.”** Architects analyze and derive, while legitimate authorities own stakeholder, legal, safety, and business obligations.
- **“Selected means more binding.”** Non-ASR requirements remain binding when authoritative.
- **“Copy the requirements into the architecture.”** Duplicate text creates drift and competing sources of truth.
- **“Priority equals significance.”** Business urgency and architectural consequence overlap but are not identical.
- **“Technology is an ASR.”** It is usually a constraint or decision whose underlying requirement must remain visible.
- **“Allocate by dividing the number.”** Budgets require a composition model, interaction analysis, and margin.
- **“Component evidence proves the outcome.”** End-to-end behavior includes dependencies, humans, interfaces, and operational conditions.
- **“Derived means optional.”** Authorized derived requirements can be binding and require traceability.
- **“Approved ASRs never change.”** Significance, premises, and context evolve.
- **“Trace links prove quality.”** Links show correspondence, not truth, completeness, or adequacy.
- **“Architecture can resolve contradictory requirements.”** Infeasible obligations require authority-driven negotiation or scope change.
- **“Verification is validation.”** Conformance to a specified requirement does not establish that it is the right requirement.

## Worked Examples

### Example 1

**Question:** Is a requirement to change a button color an ASR?

**Reasoning:** Usually it affects one presentation element and remains cheap to reverse, so it is local. It becomes significant if color encodes a regulated safety state across devices, must remain perceivable under accessibility constraints, and is shared through a platform theme used by hundreds of applications. Context, consequence, reach, and reversal cost—not wording—determine classification.

**Conclusion:** Architectural significance is contextual and decision-relative.

### Example 2

**Question:** Why is offline order capture likely an ASR?

**Reasoning:** It affects local identity, authorization, storage, inventory assumptions, conflict resolution, time, synchronization, user status, security, support, and recovery. It constrains clients, services, data authority, and operational procedures. Define maximum disconnection, accepted operations, conflict policy, data sensitivity, device loss, and convergence evidence.

**Conclusion:** One functional capability can be architecturally significant because it reshapes several structures and invariants.

### Example 3

**Question:** Three serial dependencies each promise 99.9% availability. Does the workflow meet 99.9%?

**Reasoning:** Under the simplified independent required-all model, $0.999^3=0.997002999$, or about 99.7003%. Shared failures can make it worse; fallback or cached degraded responses can change the composition. Arbitrarily assigning the end target to each component is insufficient.

**Conclusion:** Allocation needs an explicit end-to-end model and margin.

### Example 4

**Question:** Is “use PostgreSQL” an ASR?

**Reasoning:** It may be an authorized technology constraint or an architecture decision, not a stakeholder requirement. Trace why it exists: transactional invariants, supported operations, skills, licensing, portability, recovery, or an enterprise mandate. Preserve those sources and test whether PostgreSQL satisfies them. If the mandate is authoritative, record its scope and exception process.

**Conclusion:** Do not disguise a solution as a requirement; preserve its governing rationale.

### Example 5

**Question:** How does a seven-year retention requirement create derived requirements?

**Reasoning:** Architecture analysis may derive durable format, metadata provenance, legal-hold precedence, encryption and key retention, authorized access, integrity checks, backup inclusion, deletion after expiry, migration validation, and supplier-exit requirements. Each derives from the parent plus chosen storage and governance decisions. A change in jurisdiction or storage design must reopen them.

**Conclusion:** Derived requirements translate an end-to-end obligation into traceable architecture responsibilities.

### Example 6

**Question:** Can a load-test pass verify a peak-sale ASR?

**Reasoning:** Only within the tested workload, topology, data, dependencies, instrumentation, and response definition. If the test excludes queue wait, failed payments, cold caches, retries, or user-edge latency, it supports a narrower claim. Validate the workload and outcome against stakeholder context, then combine component and end-to-end evidence.

**Conclusion:** Evidence scope must match the ASR; successful execution alone is not universal verification.

### Example 7

**Question:** Two ASRs demand immutable audit history and immediate deletion. Are they contradictory?

**Reasoning:** They may be until data categories, purposes, lawful retention, cryptographic identifiers, audit minimization, and deletion semantics are clarified. Preserve both authorities, find scope intersections, and design separation or redaction where legitimate. Do not silently weaken either. If obligations truly conflict, qualified legal and governance authorities must resolve scope and residual risk.

**Conclusion:** Conflict analysis is an architecture input, not permission to reinterpret authority privately.

### Example 8

**Question:** When can a platform make an ASR local?

**Reasoning:** Suppose every service once implemented identity-token rotation, making it cross-cutting and risky. A governed platform may supply rotation, observability, rollback, evidence, and a stable interface. Service teams retain authorization semantics and integration verification, but mechanism change becomes local to the platform. Reclassify only after evidence and ownership demonstrate that the boundary is real.

**Conclusion:** Architecture and organizational capability can change significance without removing the underlying requirement.

### Example 9

**Question:** What should happen when a baseline workload assumption triples?

**Reasoning:** Reopen every ASR classification, allocation, and decision using it: latency, capacity, cost, recovery, data placement, supplier limits, and operational staffing. Existing test evidence no longer covers the same premise. Some formerly local requirements may become architectural. Record the change rather than editing history.

**Conclusion:** ASRs are maintained views over changing requirements, context, and evidence.

### Example 10

**Question:** How should ASRs be selected for an autonomous medical transport controller?

**Reasoning:** Include mission functions, human authority, fail-safe behavior, timing, sensing, cybersecurity, accessibility, environmental limits, update, diagnostics, recovery, evidence, and retirement. Use applicable medical, transport, and safety processes rather than a generic architecture checklist. No external clinical, transport, safety, regulatory, cybersecurity, human-factors, or practitioner review is claimed; named qualified authorities must own requirements, hazards, verification independence, validation, release, and residual-risk acceptance.

**Conclusion:** High-consequence ASR selection requires explicit pedigree, domain assurance, and qualified authority.

## Cross-Program Connections

- [Software Engineering Methods & Evolution](../../10-software-engineering-methods-and-evolution/ROADMAP.md) provides requirements discovery, prioritization, baselining, and change practices.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) designs verification and validation evidence for allocated and end-to-end requirements.
- [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) turns operational ASRs into deployment, observability, recovery, and feedback mechanisms.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) develops authority, lineage, retention, residency, and migration requirements.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies threat-driven security requirements and assurance boundaries.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) governs requirement allocation, interfaces, lifecycle traceability, verification, validation, and technical baselines.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) realizes external-interface ASRs through explicit semantics and evolution policies.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018, Systems and software engineering—Life cycle processes—Requirements engineering](https://www.iso.org/standard/72089.html), edition 2, November 2018. Requirements information, characteristics, processes, traceability, and lifecycle application; consulted 2026-09-05.
2. Paul Clements and Len Bass. [Relating Business Goals to Architecturally Significant Requirements for Software Systems](https://www.sei.cmu.edu/library/relating-business-goals-to-architecturally-significant-requirements-for-software-systems/), CMU/SEI-2010-TN-018, 2010. Business-goal pedigree and derivation of quality-attribute requirements; consulted 2026-09-05.
3. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*, fourth edition, Addison-Wesley, 2021. Architecture drivers, ASRs, quality scenarios, tactics, and evaluation.
4. Software Engineering Institute. [Quality Attribute Workshop Collection](https://www.sei.cmu.edu/library/quality-attribute-workshop-collection/), Carnegie Mellon University, 2016. Stakeholder elicitation, prioritization, and refinement of architecture-critical quality scenarios; consulted 2026-09-05.
5. Rick Kazman, Mark Klein, and Paul Clements. [ATAM: Method for Architecture Evaluation](https://www.sei.cmu.edu/library/atam-method-for-architecture-evaluation/), CMU/SEI-2000-TR-004, 2000. Scenario-based evaluation, utility trees, risks, sensitivity points, and trade-offs.
6. ISO/IEC/IEEE. [ISO/IEC/IEEE 42010:2022, Software, systems and enterprise—Architecture description](https://www.iso.org/standard/74393.html), edition 2, November 2022. Architecture-description concerns, stakeholders, viewpoints, views, and correspondence; consulted 2026-09-05.
7. NASA. [NASA Systems Engineering Handbook, Revision 2](https://www.nasa.gov/reference/systems-engineering-handbook/), NASA/SP-2016-6105 Rev2, 2016. Requirements definition, allocation, technical baselines, decision analysis, verification, and validation; consulted 2026-09-05.
8. Karl Wiegers and Joy Beatty. *Software Requirements*, third edition, Microsoft Press, 2013. Requirements quality, business requirements, elicitation, prioritization, traceability, validation, and change.

## Exercises

### Exercise 1

Classify whether each is architecturally significant for a small local payroll service and explain the context: a logo change, a statutory tax calculation, a two-hour recovery requirement, and support for ten additional report templates.

### Exercise 2

Build a complete ASR record and trace for offline field inspection, from stakeholder goal through scenario, requirement, significance, decisions, derived requirements, and evidence.

### Exercise 3

Diagnose an architecture document that copies 400 requirements, labels every quality requirement an ASR, links none to decisions, and claims all are verified because unit tests pass.

### Exercise 4

Allocate a two-second end-to-end response objective across client, gateway, service, database, and one external dependency. Explain why simple equal division is inadequate and how you would preserve margin and validate composition.

### Exercise 5

Define ASR governance for an unfamiliar national emergency-call routing platform. Separate automated trace checks, engineering evidence, stakeholder validation, qualified authority, and readiness blockers.

## Answers to the Exercises

### Answer 1

The logo change is usually local and reversible unless it participates in a safety, legal identity, or shared platform constraint. Statutory tax calculation is likely significant because correctness, effective dates, audit, data authority, and legal change can span rules, records, interfaces, and evidence. Two-hour recovery is likely significant if it covers payroll processing and accepted work because it affects topology, data recovery, dependencies, operations, and exercises. Ten report templates may be local if they use a stable reporting capability; they become significant if each directly couples to the transaction schema, regulated definitions, or separate deployment.

Full credit requires stating system size, jurisdictions, users, lifecycle, dependencies, and consequences. The labels alone do not settle significance, and non-ASR requirements remain binding.

### Answer 2

Goal: inspectors must continue authorized safety inspections where connectivity is unavailable. Scenario: an authenticated inspector begins, records, signs, and reviews an inspection during a declared disconnection of up to eight hours; the device preserves authorized work, exposes provisional state, and synchronizes without silent loss or duplicate final records after reconnection. Measures include supported tasks, duration, storage bound, identity lifetime, conflict behavior, sync completion, and evidence at device and authority.

Significance follows from cross-cutting client storage, identity, security, data authority, time, conflict, synchronization, support, and recovery. Decisions may select an encrypted local journal, stable operation IDs, explicit provisional/final states, and authority-side reconciliation. Derived requirements cover device-loss protection, clock handling, schema compatibility, retention, replay, conflict queues, observability, and migration. Evidence combines model/invariant review, executable sync and conflict tests, long-disconnection and device-loss exercises, security review, field workflow validation, and bounded production observation. Every derived item traces to the parent and decision premise.

### Answer 3

The document creates a competing requirements source and will drift from authoritative versions and approvals. Category-only ASR selection ignores context and overwhelms architecture attention. Missing decision links prevent justification and gap analysis. Unit tests support selected component behavior; they cannot verify every interface, deployment, quality, migration, operational, or end-to-end requirement, nor validate stakeholder need.

Keep authoritative IDs and use an ASR projection with source, rationale, significance profile, affected structures, owner, status, assumptions, risks, decisions, derived requirements, and evidence plan. Reassess candidates with stakeholders and lifecycle/context walks. Preserve non-selected requirements in their authority. Design claim-specific inspection, analysis, test, experiment, demonstration, exercise, and qualified review. Report unresolved, infeasible, or unverified ASRs rather than manufacturing completion through links or test counts.

### Answer 4

Begin with the user-edge clock and define eligible requests, workload, percentile, errors, retries, and environments. An initial budget might reserve 300 ms for client/network, 100 ms gateway, 350 ms service work, 500 ms database, 500 ms external dependency, and 250 ms margin, but these are hypotheses. Equal 400 ms shares ignore parallel execution, queueing, tail dependence, caching, retry amplification, external variability, and what teams can control.

Model the critical path and distributions, measure representative components, account for concurrency and dependency tails, and allocate both time and failure behavior. Give each budget an owner and observation point. Preserve margin for unknowns and coordination, test boundary and degraded cases, and validate end to end under the declared workload. Reallocate when evidence changes. Component budget passes are necessary evidence but cannot replace the end-to-end measurement.

### Answer 5

Discover ASRs across call intake, location, language and accessibility, routing authority, carrier and center interoperability, identity, prioritization, overload, partial failure, cybersecurity, recording, privacy, audit, operator control, disaster recovery, migration, and retirement. Preserve statutory, telecommunications, emergency-service, and local authority sources and expose conflicting jurisdictions. Construct normal, peak, disaster, malicious, degraded, reroute, callback, and recovery scenarios.

Automated checks can validate requirement schemas, unique IDs, trace relations, interface-model consistency, configuration bounds, evidence age, and selected routing invariants. Engineering evidence includes formal analysis where applicable, protocol conformance, load and fault tests, carrier/center integration, exercises, failover, recovery, security assessment, and operational observation. These do not establish public-safety needs or acceptable residual risk alone. No external emergency-services, telecommunications, safety, accessibility, regulatory, cybersecurity, or practitioner review is claimed. Named qualified authorities must own requirements, hazard and threat analysis, human factors, validation, independent assurance, release, and risk acceptance. Ambiguous routing authority, unverified location semantics, inaccessible critical interaction, failed overload/degraded operation, missing end-to-end exercise, or unresolved high-severity hazard blocks the corresponding readiness claim.
