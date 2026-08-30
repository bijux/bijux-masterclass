---
module_id: SYSENG-013
program: Systems Engineering
level: 1
module_number: 13
title: Functional Requirements
status: complete
last_verified: 2026-08-30
---

# Functional Requirements

## One-Page Review

### Governing question

How can engineers transform stakeholder needs and operational concepts into necessary, observable obligations for what the system of interest must do—across triggers, states, inputs, outputs, exceptions, and recovery—without confusing function with performance, design, procedure, or aspiration?

### Essential definitions

- A **requirement** is an agreed obligation for an identified entity to perform a function or possess a quality within stated conditions and constraints because it is necessary for an authorized source.
- A **functional requirement** specifies required behavior: a transformation, response, control, interaction, state change, or provision of information or service.
- The **system of interest (SoI)** is the entity obligated by the requirement; its boundary and level must be explicit.
- A **source** is the authorized need, parent requirement, constraint, operational concept, hazard control, interface agreement, or justified derived rationale from which an obligation follows.
- A **trigger** is an event or condition that activates behavior; a **precondition** is state that must already hold; a **guard** selects behavior among alternatives.
- A **response** is the required externally observable behavior or state change; a **postcondition** is the state that must hold afterward.
- A **functional chain** relates input or event through system behavior to output and outcome; it is not an architecture allocation.
- A **derived requirement** is necessary because analysis reveals an obligation not stated verbatim by a stakeholder or parent requirement.
- **Requirement verification** checks the requirement statement/set for quality and later checks the realized system against the obligation; **validation** checks that the right obligations support stakeholder needs in context.
- **Atomicity** means a requirement contains one independently necessary and verifiable obligation, not merely one sentence.

### Central model, mechanism, or theorem

Represent a functional requirement as:

\[
r=\langle id,subject,condition,trigger,input,behavior,output,
postcondition,exceptions,source,rationale,verification,status\rangle.
\]

A useful textual pattern is:

\[
[Condition],\; SoI\; shall\; Behavior(Object)\; [Qualifier].
\]

The transformation obligation is:

\[
Need+OperationalEvidence+Analysis
\xrightarrow{rationale} FunctionalRequirementSet,
\]

with bidirectional coverage:

\[
\forall r\in R_f:\ Source(r)\neq\varnothing,
\qquad
\forall n\in N:\ Covered(n,R_f)\lor JustifiedGap(n).
\]

These predicates expose missing evidence; they do not prove necessity, completeness, feasibility, safety, or correct interpretation.

### Critical invariants

- Every requirement names the obligated entity at the correct system level.
- Every function traces to an authorized source or an explicitly reviewed derived rationale.
- State what observable behavior is required, not an unjustified realization.
- Conditions, triggers, inputs, outputs, modes, exceptions, and end states are explicit where they change meaning.
- Separate function from performance thresholds, quality attributes, interface definitions, external constraints, design decisions, and operator procedures while preserving their links.
- One statement carries one independently traceable and verifiable obligation.
- Terminology, units, identifiers, modal verbs, and logical connectors follow governed conventions.
- Nominal behavior never substitutes for invalid input, timeout, duplicate, conflict, interruption, degraded dependency, cancellation, and recovery behavior.
- The set covers relevant operational threads and does not contain orphan, duplicate, contradictory, infeasible, or unverified obligations.
- High-consequence functional claims require applicable safety, security, human-factors, domain, and independent review.

### Common failures

Failures include copying needs as `shall` statements; writing “support,” “handle,” “manage,” “optimize,” or “be capable of” without observable meaning; naming a component not yet selected; putting several obligations behind `and`; omitting trigger, mode, invalid input, or end state; making the operator the product-requirement subject; embedding rationale in the normative sentence; specifying an algorithm instead of an outcome; deriving functions without source; decomposing by prose intuition alone; treating a parser or template checker as semantic verification; and counting traced links as proof of stakeholder coverage.

### Compact example

Need: emergency dispatchers need a trustworthy location when a caller cannot speak. Weak: “The application shall use GPS to support location.” Better functional obligation: “When an authorized emergency session begins and no dispatcher-confirmed location exists, the emergency-assistance system shall provide the dispatcher with each available location estimate and its source, observation time, and declared uncertainty.” Separate requirements address acquisition latency, authorization, unavailable or conflicting estimates, privacy, retention, user correction, and degraded operation. The better statement preserves alternative sensing and fusion designs while exposing observable behavior.

### Connections

Retrieve stakeholder needs from SYSENG-011 and operational concepts from SYSENG-012, supported by context/scenarios and problem framing in SYSENG-009–010. Continue to performance and quality requirements, constraints, requirement quality/testability, decomposition, allocation, traceability, and change. Later functional architecture, interfaces, verification, validation, safety, and human factors supply deeper models and evidence.

## Governing Question

Stakeholders describe outcomes; operational concepts describe intended work; architecture will organize a realization. Functional requirements occupy the disciplined boundary between them. They assign observable behavioral obligations to the system of interest so designers can explore alternatives and verifiers can later determine whether the system performs those obligations.

The difficulty is not inserting `shall` into prose. Engineers must decide which system behavior is necessary, under which conditions, at which level, with which inputs and outputs, and why. A grammatically clean statement can still be unnecessary, wrong-level, incomplete, infeasible, unobservable, unsafe, or derived from a misunderstood need. Requirements definition is engineering analysis plus controlled expression.

## Why This Matters

Architecture, integration, verification, acceptance, cost, and change control depend on the functional baseline. If behavior is vague, different teams fill gaps with incompatible assumptions. If it is overdesigned, suppliers cannot compare alternatives. If failure behavior is absent, nominal success conceals operational loss. If functions have no legitimate source, the system accumulates cost and attack surface without stakeholder value.

ISO/IEC/IEEE 29148:2018 provides lifecycle requirements-engineering processes, well-formed textual requirement guidance, attributes, information items, and traceability. ISO/IEC/IEEE 15288:2023 positions system requirements definition between stakeholder needs and downstream architecture, design, integration, and verification. NASA describes technical requirements definition as iterative transformation of stakeholder expectations into validated obligations that capture inputs, outputs, relationships, constraints, and interactions.

Current SEBoK 2.14 guidance emphasizes that requirements are engineering decisions, not merely writing: needs and lifecycle concepts are analyzed into design-input requirements for the SoI. This module therefore treats textual patterns as useful controls within a larger mechanism of source analysis, behavioral modeling, set review, and evidence-bounded judgment.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. stakeholder needs preserve outcome, context, rationale, source, conflict, and validation intent;
2. operational concepts expose roles, authority, modes, threads, support, transition, and external dependencies;
3. the system boundary determines what behavior can legitimately be assigned to the SoI;
4. scenarios reveal temporal and exceptional behavior but do not automatically constitute requirements;
5. constraints and assumptions have sources and different logical status;
6. verification asks whether specified obligations are met, while validation asks whether the realized operation satisfies stakeholder needs;
7. traceability requires semantic transformation rationale, not only linked identifiers.

As a retrieval test, analyze “The system shall allow users to quickly manage alerts.” Identify the system, user role, trigger, permitted operations, alert states, authorization, observable responses, invalid actions, concurrency, recovery, and meaning of quickly. The sentence mixes vague function and performance. It cannot yet guide architecture or verification.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish functional requirements from needs, operational statements, performance, quality, interface, constraint, design, and procedure;
2. identify the obligated entity, source, rationale, condition, trigger, input, behavior, output, and postcondition;
3. derive candidate functions from outcomes, scenarios, state models, hazards, interfaces, and lifecycle analysis;
4. write atomic, active, necessary, feasible, unambiguous, implementation-responsible requirements;
5. specify nominal, alternate, invalid, degraded, interrupted, and recovery behaviors;
6. use state, event, data-transformation, and functional-flow models to test textual requirements;
7. separate normative statements from rationale, examples, notes, assumptions, and verification methods;
8. analyze functional coverage, duplication, contradiction, feasibility, and traceability at set level;
9. apply bounded automated quality checks without overstating semantic assurance;
10. escalate consequential interpretations and derived obligations to appropriate authorities.

## Core Exposition

**Fix the obligation boundary.** Name the SoI and its level before writing. “The controller,” “the platform,” and “the service” may denote different product breakdown elements. A system-level requirement should not assign an internal component unless architecture has authorized that allocation. Conversely, a system requirement cannot assign an external operator's work; capture that in the operational concept, agreement, procedure, or personnel requirement and specify the system behavior that enables it.

**Start from sources, not verbs.** Gather baselined stakeholder needs, operational threads, parent requirements, laws and standards as interpreted by authority, hazards, interface agreements, lifecycle concepts, and justified design decisions. For each source ask what must be observably true of the SoI. Preserve source identity and transformation rationale. If no source exists, classify the candidate as derived and obtain the required concurrence rather than inventing ancestry.

**Separate outcome, function, and realization.** “Residents receive understandable warnings” is a need/outcome. “The warning system shall distribute each authorized warning to all configured dissemination interfaces” is function. “Use vendor X message broker” is realization or constraint. The functional statement may still imply architecture consequences, but it does not select them without necessity.

**Identify transformations.** A function consumes an event, material, energy, information, or state and produces an observable output or state change. Use black-box questions: what crosses the boundary, what changes, under what condition, and what result is visible? Functions include sense, validate, transform, decide under defined rules, store, retrieve, communicate, control, protect, reconcile, and dispose—not only user-facing features.

**Write the normative kernel.** Use the project's governed modal verb, commonly `shall`, once per obligation. Name the subject and an active, observable predicate. Keep rationale, notes, examples, verification method, and metadata outside the sentence. A stable pattern is “When/while/where [condition], the [SoI] shall [active behavior] [object/result].” Patterns improve consistency but cannot determine truth.

**Make conditions and triggers precise.** Unconditional behavior is rare. Define operational mode, system state, actor authority, input state, environmental condition, time relation, or event that activates the obligation. Distinguish `when` event, `while` continuing state, `where` feature/configuration, and `if` optional condition according to the local grammar. Avoid condition words whose scope is unclear.

**Define inputs and acceptance.** State required information/material and its semantics, provenance, validity, authority, ordering, and freshness where behavior depends on them. Do not make the producer responsible through a requirement on the receiver. Specify how the SoI distinguishes accepted, rejected, duplicate, late, conflicting, incomplete, unauthorized, or unverifiable input.

**Define observable response and end state.** “Process request” hides output and completion. State what is provided, changed, commanded, recorded, rejected, or signaled and what postcondition holds. Observability may be at an interface, through state query, audit record, physical response, or controlled inspection. Internal activity without observable consequence is difficult to justify or verify.

**Separate performance and quality.** Function answers what behavior occurs. Performance answers how much, how fast, how accurately, or under what capacity. Quality addresses attributes such as reliability, usability, maintainability, safety, or security. Link them: one function may have several performance/quality obligations. Do not overload the functional sentence until it becomes compound and hard to change. SYSENG-014 develops these distinctions.

**Separate interface behavior from interface design.** “Provide an authenticated status response to the authorized requester” can be functional. Exact protocol, schema, connector, voltage, or endpoint may belong in interface requirements or design unless externally constrained. Still specify semantic obligations at the correct boundary: what information is exchanged, with whom, under which states, and what failure response follows.

**Treat negative requirements carefully.** Positive statements are often clearer because they specify desired behavior. Yet prohibitions can be necessary: a system shall not energize an actuator while an access guard is open. Define the prohibited state/transition and observable enforcement; consider adding required safe response. Never rewrite a safety prohibition positively if doing so weakens its logical boundary.

**Split compound obligations semantically.** `And` may join a single inseparable object phrase or hide two independently sourced and verifiable behaviors. Split when parts can differ in source, priority, allocation, verification, change, or satisfaction. Conversely, mechanical splitting can destroy one transaction's semantics. Atomicity is about obligation control, not counting conjunctions.

**Cover exceptions and recovery.** For every operationally important function, examine absent, malformed, unauthorized, stale, duplicate, out-of-order, contradictory, excessive, and malicious inputs; unavailable dependencies; timeout; interruption; cancellation; concurrency; partial completion; restart; and recovery. Specify required behavior and end state where necessary. Avoid a universal “handle errors gracefully.”

**Use state and mode reasoning.** Create a state-transition table with current state, event/guard, required action/output, next state, prohibited transition, and evidence. A requirement set should not permit mutually incompatible transitions for the same condition. Initialization, degraded operation, maintenance, emergency, update, and retirement often reveal missing functions.

**Use functional-flow reasoning.** Trace end-to-end operational threads into functions and exchanges. Check that outputs required by downstream functions have producers, inputs have consumers and sources, control loops have observation and action, resources are acquired/released, and failures terminate or recover. Do not allocate flows to components until the architecture decision is authorized.

**Derive obligations without disguising them.** A hazard analysis may derive “Upon loss of verified position during autonomous movement, the vehicle system shall transition to the defined minimum-risk state.” A lifecycle concept may derive secure deletion. Mark the source as hazard or lifecycle analysis, record assumptions and authority, and trace upward. “Derived” does not mean optional; it means the rationale is analytical rather than a copied parent sentence.

**Add requirement attributes.** Store stable ID, title, text, type, SoI level, source, rationale, owner, status, priority/criticality, assumptions, verification method/level, allocation status, change history, and relations. Keep mutable metadata out of normative text. Attributes support governance but cannot repair a bad obligation.

**Review individual quality.** Ask whether each requirement is necessary, appropriate to level, implementation-responsible, unambiguous, singular, complete enough, feasible, verifiable, consistent, and traceable. “Complete enough” depends on decision maturity: unresolved values need explicit TBR/TBD ownership, resolution evidence, deadline, and impact. Never silently invent precision.

**Review the set.** Individual sentences can pass while the set fails. Build coverage across needs, operational threads, functions, modes, interfaces, hazards, lifecycle stages, and verification. Detect gaps, overlaps, contradictory responses, terminology drift, orphan functions, circular dependence, unreachable states, and requirements whose combined demands are infeasible. Independent challenge matters most at boundaries.

**Plan verification without writing the test into the obligation.** Identify analysis, inspection, demonstration, or test and the evidence needed to distinguish satisfaction. If no plausible observation exists, revise the requirement or explain the abstraction-level verification chain. Do not weaken the obligation merely because the current test environment is inconvenient.

**Validate with stakeholders and operations.** Walk functional requirements back through representative scenarios: would satisfying them enable the intended outcome across relevant populations, modes, and failure conditions? A perfectly verifiable requirement can be the wrong requirement. Preserve dissent and unresolved domain judgments.

**Use language automation as a bounded aid.** Linters can flag missing subject/modal/source, weak verbs, conjunctions, undefined terms, and absent verification fields. They cannot decide necessity, semantic atomicity, correct boundary, feasibility, safety, or coverage. The executable example deliberately reports declared defects rather than “validating” requirements.

<!-- bijux-verify: {"id":"functional-requirement-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"requirements_total=5\nwell_formed_declared=1\nmissing_source=FR-004\nmissing_trigger=FR-003\nweak_verbs=FR-002:support\ncompound_signals=FR-005:and\nmissing_verification=FR-003\nrequirement_set_ready=false\nevidence=declared_fields_and_lexical_signals_only\n","stderr":""}} -->
```python
requirements = [
    {"id": "FR-001", "subject": "alert system", "trigger": "authorized warning received",
     "behavior": "distribute warning", "source": ["N-public-warning"], "verification": ["interface test"]},
    {"id": "FR-002", "subject": "alert system", "trigger": "warning active",
     "behavior": "support delivery", "source": ["N-public-warning"], "verification": ["review"]},
    {"id": "FR-003", "subject": "alert system", "trigger": "",
     "behavior": "record acknowledgement", "source": ["OC-alert-closure"], "verification": []},
    {"id": "FR-004", "subject": "alert system", "trigger": "delivery rejected",
     "behavior": "provide rejection reason", "source": [], "verification": ["interface test"]},
    {"id": "FR-005", "subject": "alert system", "trigger": "warning cancelled",
     "behavior": "withdraw warning and notify operators", "source": ["OC-cancellation"],
     "verification": ["scenario test"]},
]

weak = ("support", "handle", "manage", "optimize")
well_formed = [r for r in requirements if all(r[k] for k in ("subject", "trigger", "behavior", "source", "verification")) and not any(w in r["behavior"].split() for w in weak) and " and " not in r["behavior"]]
missing_source = sorted(r["id"] for r in requirements if not r["source"])
missing_trigger = sorted(r["id"] for r in requirements if not r["trigger"])
weak_hits = sorted(f'{r["id"]}:{w}' for r in requirements for w in weak if w in r["behavior"].split())
compound = sorted(f'{r["id"]}:and' for r in requirements if " and " in r["behavior"])
missing_verification = sorted(r["id"] for r in requirements if not r["verification"])

print(f"requirements_total={len(requirements)}")
print(f"well_formed_declared={len(well_formed)}")
print(f"missing_source={','.join(missing_source) or 'none'}")
print(f"missing_trigger={','.join(missing_trigger) or 'none'}")
print(f"weak_verbs={','.join(weak_hits) or 'none'}")
print(f"compound_signals={','.join(compound) or 'none'}")
print(f"missing_verification={','.join(missing_verification) or 'none'}")
print(f"requirement_set_ready={str(len(well_formed) == len(requirements)).lower()}")
print("evidence=declared_fields_and_lexical_signals_only")
```

## Definitions and Notation

Let \(N\) be baselined stakeholder needs, \(O\) operational-concept elements, \(R_f\) functional requirements, \(R_p\) performance requirements, \(R_q\) quality requirements, and \(A\) architecture/design decisions. Keeping these sets distinct does not prohibit links among them.

Model black-box behavior as a conditional state transition:

\[
F:(x,s,e)\mapsto(y,s'),
\]

where \(x\) is accepted input/event, \(s\) current state, \(e\) relevant environment/mode, \(y\) observable output/action, and \(s'\) post-state. A functional requirement constrains this relation without necessarily prescribing its internal computation.

Let \(Trace(a,b,\rho)\) mean artifact element \(a\) justifiably transforms into or supports \(b\) with rationale \(\rho\). Let \(Verify(r,v)\) mean method/evidence \(v\) can discriminate whether a realization meets \(r\) under stated conditions. Neither relation alone establishes correctness.

A **shall statement** is a project convention for a mandatory obligation; the word alone does not make prose a requirement. **Requirement verification** can refer to reviewing requirement quality before baseline and to product verification later; state which meaning is intended. A **functional model** represents transformations and flows, whereas a **functional architecture** may add organization and allocation decisions developed later.

## Mechanisms, Invariants, or Proof Structure

The derivation mechanism has six passes. First, map sources and system boundary. Second, extract outcome-relevant transformations from operational threads. Third, model state, events, inputs, outputs, exceptions, and recovery. Fourth, write atomic normative kernels and attributes. Fifth, analyze coverage, consistency, feasibility, and verification. Sixth, validate the set against needs and operations under named authority.

For a requirement \(r\), define a readiness predicate:

\[
Ready(r)=Subject(r)\land Source(r)\land Necessary(r)\land Observable(r)
\land Feasible(r)\land Atomic(r)\land Unambiguous(r)\land Verification(r).
\]

Most terms require engineering judgment and evidence. A checker can establish only syntactic proxies such as nonempty fields. Consequently, `Ready` is a review claim bounded by reviewers, baseline, and evidence—not a theorem.

Maintain five invariants. **Obligation invariant:** every normative statement has one controlled subject and modal force. **Source invariant:** every function has upward rationale. **Behavior invariant:** the statement constrains observable behavior rather than unjustified internal realization. **Condition invariant:** behavior is defined across relevant state and exception boundaries. **Closure invariant:** the set covers sources downward and provides verification paths without orphans.

Set consistency can be challenged by pairs of requirements over overlapping conditions. If \(r_1\) requires next state \(s_a\) and \(r_2\) requires incompatible \(s_b\) for the same state/event/guard, the set contains a conflict unless priority or mode semantics resolves it. State models, decision tables, model checking, simulation, and review offer evidence; no single method proves correctness for every system.

## Alternatives and Trade-Offs

**Natural language versus formal models.** Natural language is accessible and adaptable but ambiguous. State machines, temporal logic, contracts, and schemas support analysis but require competence and can formalize the wrong intent. Use controlled text plus models for critical behavior, with explicit semantic correspondence.

**Function-first versus scenario-first.** Functional decomposition exposes transformations and reuse; scenarios preserve temporal context and stakeholder meaning. Function-only work can miss sequence and exception; scenario-only work can duplicate behavior and miss coverage. Iterate between them.

**Positive versus negative form.** Positive form usually clarifies required action. Negative form precisely prohibits unsafe or unauthorized states. Select the form that best represents the obligation, then add the required safe response where omission would be ambiguous.

**Coarse versus fine granularity.** Coarse requirements preserve intent but impede allocation and verification. Fine requirements improve control but generate link overhead and can fragment meaning. Split at independent source, change, allocation, or verification boundaries, retaining parent rationale.

**Implementation-neutral versus constrained.** Neutrality preserves competition and learning. Legitimate interoperability, regulation, heritage, safety, or acquisition constraints may fix part of realization. Cite the authority, scope, expiration, and underlying need; do not disguise a preference as function.

**Textual lint versus expert inspection.** Automated rules cheaply find recurring signals and enforce metadata. They create false positives/negatives and cannot understand domain consequences. Use them to focus review, never to replace it.

## Failure Modes and Misconceptions

1. **“A requirement is any sentence containing shall.”** Modal syntax cannot establish source, necessity, feasibility, or correctness.
2. **“Functional means feature.”** Functions include control, protection, diagnosis, recovery, support, migration, and disposal.
3. **“Implementation-free means vague.”** Required behavior, conditions, inputs, outputs, and end states can be precise without selecting internal design.
4. **“One sentence is atomic.”** One sentence can contain independently changeable obligations; several clauses can define one inseparable transaction.
5. **“Operator shall is a product requirement.”** Put human responsibility in operational/procedural artifacts and specify enabling system behavior.
6. **“All errors share one requirement.”** Error classes have different consequences, authority, state, and recovery.
7. **“Traceability proves coverage.”** Links can be semantically wrong, and omitted sources never appear in the matrix.
8. **“Verification method makes the requirement verifiable.”** The method must actually discriminate satisfaction under required conditions.
9. **“Derived means gold plating.”** Properly justified hazard, interface, lifecycle, or design-derived obligations can be necessary; unreviewed additions are not.
10. **“Baselined means finished.”** Requirements change when needs, operations, risks, interfaces, evidence, or architecture change.

## Worked Examples

### Example 1

**Situation.** “The payment platform shall support refunds.” **Reasoning.** `Support` leaves behavior unobservable. Source needs include authorized correction and accountable settlement. Separate initiation acceptance, authorization validation, duplicate detection, state transition, downstream instruction, customer/merchant notification, and audit record. Example kernel: “When an authorized refund request references a settled transaction, the payment system shall create one refund instruction associated with that transaction.” Performance and financial constraints remain linked requirements. **Conclusion.** Replace capability labels with controlled transformations and end states.

### Example 2

**Situation.** A transit requirement says the system shall validate a fare and open the gate. **Reasoning.** Validation and actuation have different safety sources, allocations, failure consequences, and tests. A valid fare can coexist with an obstructed or emergency-open gate. Split fare determination from gate authorization; define states and interface semantics. **Conclusion.** Conjunction revealed two independently governed obligations.

### Example 3

**Situation.** “The dispatch system shall use GPS to locate callers.” **Reasoning.** The source needs trustworthy location, not one technology. Specify provision of available estimates with source, time, uncertainty, and conflict status. Architecture may combine network, device, registered address, or caller/dispatcher input. If a law mandates a mechanism, record it as a constraint. **Conclusion.** Recover the observable function and keep realization open unless authority narrows it.

### Example 4

**Situation.** A controller handles a command duplicated after network retry. **Reasoning.** Nominal “execute command” is unsafe. Define command identity, authorization, accepted states, duplicate recognition, idempotent response or explicit rejection, record, and state preservation. Trace the behavior to operational recovery and hazard analysis. **Conclusion.** Retry behavior is part of function, not merely an implementation detail.

### Example 5

**Situation.** A medical pump requirement says it shall not infuse while the door is open. **Reasoning.** The negative boundary is appropriate but incomplete. Define how door state is established, prohibited transition, cessation behavior if opened during infusion, alarm/status, retained dosage record, and safe restart authorization. Verification needs fault and transition cases; clinical safety needs external authority. **Conclusion.** Preserve the prohibition and specify the observable safe response without claiming clinical sufficiency.

### Example 6

**Situation.** A service receives two conflicting identity attributes. **Reasoning.** “Process identity data” cannot choose silently. Define source trust/authority, freshness, conflict detection, decision state, restricted behavior, operator/user visibility, correction route, audit, and recovery. Avoid embedding a particular identity vendor or merge algorithm unless constrained. **Conclusion.** Conflict is an explicit state with governed behavior.

### Example 7

**Situation.** A data export is cancelled after partial delivery. **Reasoning.** Model requested, authorized, preparing, transferring, cancelling, cancelled, completed, and failed states. Requirements cover cancellation acceptance, cessation boundary, partial artifact validity, credential revocation, cleanup, records, notification, and retry. “Cancel export” alone omits observable closure. **Conclusion.** State analysis exposes functions at interruption and recovery boundaries.

### Example 8

**Situation.** A warehouse function is assigned to `RouteOptimizerService` before architecture. **Reasoning.** The system obligation is to provide authorized work sequencing consistent with safety and operational constraints. A named service is premature allocation. Move it to architecture unless externally fixed; keep interfaces, outcomes, and verification at system level. **Conclusion.** The obligated subject reveals whether design has leaked into requirements.

### Example 9

**Situation.** Every requirement passes a language linter, yet emergency shutdown cannot complete. **Reasoning.** The set contains stop-command acceptance and actuator isolation but omits release of stored energy and confirmation to the responsible role. A hazard thread and state model reveal the gap; no linter could infer the missing function. **Conclusion.** Individual textual quality is necessary but insufficient; set coverage requires domain models and challenge.

### Example 10

**Situation.** An AI triage service must recommend urgency. **Reasoning.** Define accepted input, missing/contradictory data behavior, output categories with uncertainty/provenance, abstention, escalation, clinician override, record, monitoring signal, and model/version identification. Separate latency, subgroup performance, usability, privacy, and clinical-risk requirements. Local tests cannot establish clinical benefit or regulatory sufficiency. **Conclusion.** Functional precision supports evaluation but consequential acceptance requires representative evidence and applicable independent authority.

## Cross-Program Connections

- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) turns governed behavioral language into domain commands, events, policies, invariants, and bounded contexts.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) allocates functional responsibilities only after system obligations and quality drivers are understood.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) specifies transformations, provenance, validation, reconciliation, retention, and recovery for information functions.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) derives authorization, protection, detection, response, and recovery behavior under adversarial conditions.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) expresses boundary behavior as contracts with state, idempotency, errors, compatibility, and observability.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) translates developer and operator needs into platform product functions without confusing portal features with outcomes.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html), second edition, 2018. Consulted 2026-08-30.
2. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018 online browsing platform](https://www.iso.org/obp/ui/#iso:std:iso-iec-ieee:29148:ed-2:v1:en), requirements fundamentals and processes. Consulted 2026-08-30.
3. ISO/IEC/IEEE. [ISO/IEC/IEEE 15288:2023 — System life cycle processes](https://www.iso.org/standard/81702.html), second edition, 2023. Consulted 2026-08-30.
4. NASA. [Technical Requirements Definition](https://www.nasa.gov/reference/4-2-technical-requirements-definition/), *NASA Systems Engineering Handbook*, Rev. 2. Consulted 2026-08-30.
5. NASA. [Systems Engineering Handbook Appendix](https://www.nasa.gov/reference/system-engineering-handbook-appendix/), Appendix C: How to Write a Good Requirement. Consulted 2026-08-30.
6. SEBoK Editorial Board. [System Requirements Definition](https://sebokwiki.org/wiki/System_Requirements_Definition), *Guide to the Systems Engineering Body of Knowledge*, version 2.14. Consulted 2026-08-30.
7. INCOSE. [*Guide for Writing Requirements*, version 4](https://www.incose.org/docs/default-source/working-groups/requirements-wg/gtwr/gtwr-v4-preview.pdf), Requirements Working Group, 2023 preview. Consulted 2026-08-30.
8. Mavin, A., Wilkinson, P., Harwood, A., and Novak, M. [“Easy Approach to Requirements Syntax (EARS)”](https://doi.org/10.1109/RE.2009.9), 17th IEEE International Requirements Engineering Conference, 2009. Consulted 2026-08-30.

## Exercises

### Exercise 1

Classify each statement as stakeholder need, operational statement, functional requirement, performance requirement, quality requirement, constraint, design decision, or procedure: “responders need trustworthy incident location”; “dispatcher confirms location”; “the system shall provide verified location”; “within two seconds”; “available during regional network loss”; “must use vendor X”; “operator selects Confirm.” Explain ambiguous cases.

### Exercise 2

Rewrite “The platform shall quickly and securely support account recovery and notify the user” into atomic candidate functional requirements plus linked performance, security/privacy, and quality questions. State assumptions and sources.

### Exercise 3

Derive a functional requirement set for cancellation of a long-running data export. Include states, authorization, concurrency, partial output, records, notification, retry, and verification without selecting an implementation.

### Exercise 4

Compare natural-language-only, controlled-language-plus-state-model, and formal temporal specification approaches for a railway-door control function. Recommend an evidence strategy proportional to consequence.

### Exercise 5

Develop and review functional requirements for a home energy system coordinating solar generation, a battery, household load, grid signals, manual override, islanded operation, maintenance, and emergency shutdown. Include traceability, boundary behavior, derived safety/security functions, and evidence limits.

## Answers to the Exercises

### Answer 1

“Responders need trustworthy incident location” is a stakeholder need: it states an outcome but needs context and meaning for trustworthy. “Dispatcher confirms location” is an operational role/action unless the dispatcher is the SoI. “The system shall provide verified location” has functional form but `system`, recipient, trigger, verification meaning, sources, uncertainty, and failure behavior remain ambiguous. “Within two seconds” is a performance fragment that must qualify a function under conditions. “Available during regional network loss” is an availability/resilience quality fragment and may imply degraded functions. “Must use vendor X” is a design constraint only if backed by legitimate authority; otherwise it is a preference. “Operator selects Confirm” is a procedure or UI design, not a system-level function. Classification depends on named subject, source, context, and artifact authority; syntax alone is insufficient.

### Answer 2

Assume the source is an authorized account-holder need for recoverable access without unauthorized takeover, plus privacy/security and support concepts. Candidate functions include: when an eligible recovery request is received, the account system shall create a uniquely identified recovery attempt; it shall evaluate the attempt against governed authorization evidence; upon acceptance it shall enable an authorized credential transition; upon rejection or indeterminate evidence it shall enter a restricted state and provide a non-sensitive status; after any terminal outcome it shall record the attempt and notify the account holder through configured independent channels. Split cancellation, expiration, replay, rate limiting, support escalation, and restoration of prior credentials when independently necessary.

Performance questions include notification and recovery-decision horizons under load. Security/privacy questions include evidence strength, enumeration leakage, replay, channel compromise, rate limits, record access/retention, and recourse. Quality questions include accessibility, comprehensibility, availability, recovery, and maintainability. Do not label “securely” verified until threat, risk, controls, and evidence are defined. Trace each candidate to the need, threat/risk analysis, operational thread, or policy authority; mark unresolved thresholds and identity policy with owners.

### Answer 3

Model `requested`, `authorized`, `preparing`, `transferring`, `cancellation-pending`, `cancelled`, `completed`, and `failed`. Candidate functions require validating requester authority and export identity; recording one cancellation decision under duplicate requests; preventing a completed export from being relabeled cancelled; stopping further disclosure at a defined boundary; invalidating or labeling partial artifacts; revoking temporary access credentials; releasing reserved resources; retaining an authorized audit record; notifying the requester of terminal state and partial-output disposition; and allowing a new request only under defined policy.

Address races between completion and cancellation with a single observable terminal-state rule. Define behavior when workers or storage are unavailable and after restart. Keep process, queue, transaction, and object-store choices out of system requirements. Verification uses state-transition/model analysis plus tests for every event/state pair, duplicates, delayed messages, interruption, unauthorized cancellation, partial transfer, restart, and record/notification correspondence. Validation returns to the user's disclosure-control and timely-recovery need.

### Answer 4

Natural language is accessible to operators and authorities but can hide temporal ambiguity such as whether opening is prohibited before or while movement. Controlled language plus a state model makes modes, guards, commands, sensor evidence, transitions, outputs, and prohibited states reviewable and testable. Temporal specification can express invariants such as “movement is never commanded while door-not-secured is observed” and liveness conditions, enabling model checking if environment assumptions are modeled.

For railway-door control, use all three: controlled normative text as the governed obligation, state/mode and interface models with explicit semantic correspondence, and formal safety properties for critical interlocks. Review assumptions about sensing, stale/conflicting state, power loss, override, evacuation, maintenance, communication loss, and common-cause failure. Verify through inspections, model analysis/model checking, interface and fault-injection tests, hardware/system tests, and operational validation. Formal proof of the model does not prove sensors, implementation, human operation, or hazard acceptability; independent safety authority reviews the complete evidence.

### Answer 5

Sources include household needs for energy continuity/control/cost visibility, grid interconnection obligations, operational modes, equipment interfaces, hazards, privacy/security analysis, maintenance, and emergency response. Candidate functions cover observing generation/load/storage/grid state with provenance and freshness; accepting authorized objectives and manual overrides; determining permitted charge/discharge/import/export actions; commanding equipment within authorized operating envelopes; exposing current mode, decisions, uncertainty, alarms, and energy flows; recording material actions; detecting unavailable, stale, contradictory, or unsafe inputs; entering defined degraded or minimum-risk states; transferring between grid-connected and islanded modes; supporting maintenance isolation and return-to-service; and performing emergency shutdown with observable confirmation.

Separate performance/capacity, availability, power quality, interoperability, usability, privacy, security, safety, and environmental constraints. Define priority and authority when household preference, battery protection, grid signal, emergency, and maintenance conflict. Derived functions may include anti-islanding, protection response, authorization, replay rejection, safe update/rollback, audit, and credential/data disposal, each traced to hazard, interface, threat, or lifecycle evidence. Review the set with state and power-flow models, interface contracts, hazard/threat analysis, scenario coverage, simulation, fault injection, hardware tests, and representative household validation. Local reasoning cannot establish electrical safety, grid-code compliance, cybersecurity adequacy, economic benefit, or acceptable residual risk; applicable electrical, utility, safety, security, consumer, and regulatory authorities must review those claims.
