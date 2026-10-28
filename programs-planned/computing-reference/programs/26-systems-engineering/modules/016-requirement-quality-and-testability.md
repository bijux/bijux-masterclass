---
module_id: SYSENG-016
program: Systems Engineering
level: 1
module_number: 16
title: Requirement Quality and Testability
status: complete
last_verified: 2026-08-31
---

# Requirement Quality and Testability

## One-Page Review

### Governing question

How can a team determine that individual requirements and the requirement set are necessary, correct, clear, feasible, consistent, traceable, and verifiable—and that proposed evidence can actually discriminate satisfaction—before ambiguity becomes architecture, code, hardware, procedure, or acceptance dispute?

### Essential definitions

- **Requirement quality** is the degree to which a requirement expression and its set support faithful understanding, justified implementation, controlled change, and conclusive verification.
- **Requirement verification** reviews whether requirements are expressed and structured correctly according to governed rules and quality characteristics.
- **Requirement validation** checks whether requirements faithfully transform the right stakeholder needs, operational concepts, parent obligations, and constraints.
- **Product/system verification** evaluates objective evidence that a realized system meets specified requirements; it is distinct from verifying the requirement artifact.
- A **verifiable requirement** admits a feasible method and success criteria capable of distinguishing satisfaction from non-satisfaction at the requirement's stated level and conditions.
- **Testability** is the degree to which controlled or observed evidence can support that discrimination; test is one verification method alongside analysis, inspection, and demonstration.
- An **oracle** is the rule, reference, model, or authority that determines the expected result for an observation.
- **Atomicity/singularity** means one independently necessary, traceable, changeable, and verifiable obligation is controlled as one requirement.
- **Completeness** is primarily a set-relative claim: the requirements adequately cover the authorized source and relevant operational space for a named decision.
- A **verification success criterion** defines configuration, stimulus/condition, observation, calculation, tolerance, uncertainty, and pass/fail rule before evidence is interpreted.

### Central model, mechanism, or theorem

For a requirement $r$, record:

$$
r=\langle id,text,subject,source,rationale,conditions,obligation,
attributes,relations,qualityFindings,verificationConcept,status\rangle.
$$

For verification evidence $v$:

$$
v=\langle requirement,method,level,configuration,preconditions,
stimulus,observations,oracle,calculation,tolerance,uncertainty,
coverage,artifacts,authority\rangle.
$$

Evidence discriminates only if:

$$
Result(v)=Pass \iff Observed(v)\;\models\;AcceptancePredicate(r),
$$

where the predicate and evidence scope are fixed before the result. A passing finite observation supports only the stated configurations and conditions; it is not universal proof.

### Critical invariants

- Requirement verification and validation are separate, recorded judgments; grammatical quality cannot prove the requirement is needed.
- Every obligation has an identifiable subject, authoritative source/rationale, scope, conditions, and controlled terminology.
- Atomicity is judged by independent source, change, allocation, verification, and satisfaction—not by sentence length or conjunction count alone.
- Feasibility is evaluated for the complete set under operational, technical, resource, schedule, lifecycle, safety, and regulatory constraints.
- Verifiability requires observable evidence and a discriminating oracle at the same abstraction level as the requirement.
- Success criteria define configuration, environment, inputs, outputs, method, tolerances, uncertainty, repetitions/population, exclusions, and authority.
- Nominal evidence never substitutes for boundary, invalid, degraded, interrupted, concurrent, failure, recovery, and lifecycle cases where applicable.
- Individual quality never substitutes for set coverage, consistency, interface closure, source coverage, or combined feasibility.
- Automated lint, link counts, test counts, and code coverage are bounded signals, not semantic or outcome proof.
- High-consequence acceptance requires applicable independence, domain competence, and safety/security/regulatory authority.

### Common failures

Failures include equating `shall` syntax with quality; using vague adjectives/adverbs; undefined pronouns, acronyms, units, quantifiers, and temporal words; hidden conditions and exceptions; compound obligations; passive voice that hides the responsible entity; unverified assumptions; implementation detail without necessity; thresholds without workload or tolerance; “verify by test” without an oracle; using inspection for dynamic behavior; testing a component against a system-level requirement; accepting a simulation without validating its assumptions; declaring a set complete because every row is linked; and rewriting a requirement merely to fit an easy test.

### Compact example

Weak: “The platform shall quickly recover failed services and notify users appropriately.” It combines recovery and notification, uses ambiguous `quickly` and `appropriately`, lacks failure class, service state, user population, end state, workload, threshold, and evidence. Separate source-traceable obligations define detection, minimum-service restoration, state reconciliation, full restoration, and notification. A recovery success criterion specifies injected failure, configuration, dependency states, observation boundary, correct restored state, time distribution, repeats, and oracle. A fast restart with corrupt state fails even if the stopwatch passes.

### Connections

Retrieve needs, operational concepts, functional/performance requirements, and constraints from SYSENG-011–015. Continue to decomposition, allocation, bidirectional traceability, and change/conflict management. Later behavior models, interfaces, integration, verification, validation, anomaly evidence, safety cases, and human factors deepen the evidence mechanism.

## Governing Question

Requirements create contractual and technical meaning long before a product exists. A small ambiguity can propagate into incompatible designs, missing interfaces, false estimates, and tests that confirm different interpretations. Discovering that defect during acceptance is expensive because the parties may all have implemented their own reasonable reading.

The governing question asks for more than clean prose. Does the obligation belong? Does it faithfully transform its source? Is its subject controllable? Can the entire set be realized together? Can evidence at the right level separate pass from fail without silently changing the requirement? These questions connect requirements engineering to architecture, modeling, assurance, and decision governance.

## Why This Matters

A requirement can be grammatically impeccable and still be wrong. “The pump shall infuse whenever commanded” is clear but unsafe if authorization and door state are omitted. Conversely, an important need can be valid but not yet quantified enough for a design baseline. Quality review must expose the specific defect and maturity decision rather than treating every draft as pass/fail prose.

ISO/IEC/IEEE 29148:2018 provides requirements-engineering processes, characteristics, attributes, and guidance for well-formed textual requirements and requirement sets. NASA's current handbook appendix asks whether requirements are clear, complete, consistent, correct, feasible, traceable, implementation-responsible, and verifiable by test, demonstration, inspection, or analysis. SEBoK 2.14 distinguishes verification of requirement quality from validation that requirements communicate the intent of their sources.

Writing rules are useful but secondary. A weak-word list can locate “fast”; it cannot derive an acceptable response threshold or determine whether response time matters. A trace tool can expose an orphan; it cannot tell whether the linked parent semantically justifies the child. Quality comes from controlled language plus source reasoning, behavioral models, feasibility evidence, verification design, and competent challenge.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. a requirement is an agreed obligation for a named entity, not merely desired prose;
2. stakeholder needs and operational concepts remain the validation basis for system requirements;
3. functional requirements constrain observable behavior without unjustified design;
4. performance/quality thresholds require population, workload, method, aggregation, tolerance, and uncertainty;
5. regulatory/constraint translations retain authority, applicability, scope, subject, and evidence;
6. traceability includes transformation rationale, not only identifiers;
7. evidence supports bounded claims under stated assumptions and does not automatically generalize.

As a retrieval test, review “The system shall provide secure, reliable access whenever needed.” Identify subject boundary, access function, actors/assets, authorization, modes, `secure`, `reliable`, `whenever`, workload, external dependencies, unavailable behavior, measures, threats, safety implications, and source. No single test can verify the sentence as written.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish requirement verification, requirement validation, product verification, system validation, acceptance, and certification;
2. assess necessity, appropriateness, correctness, clarity, singularity, completeness, consistency, feasibility, traceability, and verifiability;
3. diagnose lexical, syntactic, semantic, referential, logical, temporal, unit, and scope ambiguity;
4. judge atomicity by obligation governance rather than punctuation;
5. construct verification concepts and success criteria with a defensible oracle;
6. select test, demonstration, inspection, analysis, or combinations appropriate to the claim;
7. evaluate boundary, statistical, model-based, human, failure, recovery, and lifecycle evidence;
8. review requirement sets for coverage, contradiction, interface closure, and combined feasibility;
9. use automated quality checks without overstating what they establish;
10. document findings, dispositions, residual uncertainty, and required external authority.

## Core Exposition

**Define the review object and decision.** State baseline/version, system level, source set, lifecycle maturity, review purpose, entry criteria, reviewers, authority, and allowed dispositions. A concept review can tolerate governed TBRs that a production acceptance baseline cannot. “Approved” is meaningless without the decision and residual issues.

**Separate verification from validation.** Requirement verification asks whether expressions and sets obey quality rules: clear, singular, feasible, traceable, verifiable, consistent. Requirement validation asks whether they capture source intent and enable stakeholder outcomes. Product verification later checks the realization against requirements; system validation evaluates intended use/outcomes. Record all four without collapsing them into “V&V passed.”

**Check necessity and source.** Ask what authorized need, parent, constraint, hazard, interface, lifecycle analysis, or decision makes the obligation necessary and what happens if it is removed. A source link plus rationale should explain transformation. A derived requirement can be necessary; an orphan preference cannot become legitimate through precise wording.

**Check the obligated subject and level.** The subject must be controlled at the requirement's level. A system requirement that names an unselected component leaks allocation. A product requirement that says “the operator shall” assigns work to the wrong entity. If verification is only possible at a component, either allocation is already governed or the system-level evidence needs an integration argument.

**Check correctness relative to evidence.** Correctness means the statement accurately represents the intended obligation within domain knowledge and source authority. Review assumptions, units, physical laws, algorithms, interfaces, hazards, legal interpretations, and operational feasibility. A reviewer cannot declare clinical or legal correctness outside competence.

**Find lexical ambiguity.** Vague words include fast, easy, adequate, robust, seamless, sufficient, appropriate, minimal, optimized, scalable, and user-friendly. They may identify a real concern but need an operational definition. Absolute words—always, never, all, any, zero—also demand boundary and feasibility review rather than automatic deletion.

**Find referential and terminology ambiguity.** Pronouns such as `it`, `this`, and `they`; aliases; undefined acronyms; inconsistent singular/plural; reused names; and overloaded terms create multiple referents. Govern a glossary and data/interface definitions. Repeating the exact controlled noun is often preferable to elegant prose.

**Find logical and quantifier ambiguity.** `And/or`, `unless`, `except`, `only`, `at least`, `up to`, `between`, negation, implication, and nested conditions can change obligation sets. Define inclusivity of bounds and quantifier scope. Use decision tables, truth tables, set notation, or controlled language when prose hides combinations.

**Find temporal ambiguity.** `Before`, `after`, `during`, `until`, `immediately`, `simultaneously`, and `periodically` require event definitions, ordering, clock, duration, and interruption rules. Specify whether a deadline begins at receipt, validation, queue admission, or processing. State behavior if the triggering condition ceases.

**Check completeness of the expression.** Include conditions, trigger, inputs, required behavior/property, outputs/end state, exceptions, units, tolerances, and references needed to interpret the obligation. Avoid repeating rationale inside normative text. Attributes can carry source, rationale, verification, criticality, owner, and status without making the sentence unreadable.

**Judge singularity semantically.** Split obligations when clauses have independent sources, priorities, allocations, change paths, verification methods, or satisfaction states. Keep together inseparable semantics such as one guarded state transition when splitting would permit partial compliance. A conjunction signal prompts review; it is not a verdict.

**Check implementation responsibility.** Requirements specify what the obligated entity must do or be, while constraints may legitimately prescribe some realization. Ask whether a named technology, algorithm, format, supplier, or component is required by an applicable source. If not, move it to architecture/design and preserve the underlying outcome.

**Check feasibility individually and jointly.** Use prototypes, models, supplier evidence, experiments, trade studies, interface analysis, resource budgets, schedule/cost evidence, and domain review. Requirements can be feasible alone but impossible together: latency versus energy, retention versus deletion, autonomy versus safety, or incompatible interface timing. Record assumptions and margin.

**Define verifiability as discrimination.** A method is adequate if controlled observations can support a pass or fail under required conditions. Specify what evidence would refute satisfaction, not only what a successful demo looks like. If no observation distinguishes implementations, the requirement may be vague, at the wrong level, or an unverifiable outcome needing decomposition and validation evidence.

**Choose verification method by claim.** Inspection examines attributes, records, dimensions, markings, configuration, or documentation without executing behavior. Analysis uses justified models, calculations, or prior evidence. Demonstration observes qualitative or functional behavior with limited instrumentation. Test applies controlled stimuli and measures response against criteria. Complex claims commonly need combinations.

**Design the oracle.** Expected results can come from exact mathematics, independent reference implementation, calibrated standard, approved model, hazard boundary, human/domain judgment, or comparison artifact. Avoid using the implementation under test to compute its own expected result without independent checks. Version the oracle and validate its domain.

**Specify configuration and pedigree.** Identify system version, hardware/software/firmware/data/model, interfaces, calibration, tools, simulators, environment, dependencies, operators, and test article relationship to delivered units. Evidence from a prototype, mock, simulation, or supplier component has limited transfer unless an argument connects it to the acceptance configuration.

**Specify stimuli and operational coverage.** Cover equivalence classes, boundaries, invalid and missing input, ordering, duplicates, concurrency, load, environment, modes, transitions, faults, dependency loss, interruption, recovery, maintenance, update, migration, and retirement according to risk. One nominal case proves only that case.

**Specify observations and end state.** Observe outputs, physical effects, state, records, resource/custody, alerts, interfaces, timing, side effects, and residual hazards. A request returning `200` does not prove downstream settlement; a reboot does not prove recovered state integrity. Define observation boundaries and synchronization.

**Specify calculation and uncertainty.** For statistical requirements, define population, sampling, repetitions, window, estimator, missing/censored observations, confidence/acceptance rule, and false-decision consequences. For physical measures, include calibration, resolution, tolerance, and uncertainty. Never decide the inference rule after seeing results.

**Check verification feasibility without weakening intent.** Estimate facilities, equipment, access, test article risk, time, data, expertise, independence, and cost. If direct test is destructive, unsafe, impossible, or too narrow, combine analysis, lower-level evidence, inspection, and demonstration with an explicit argument. Do not rewrite a stakeholder-critical obligation solely because the easiest test cannot measure it.

**Review set coverage.** Map sources and operational threads across functions, qualities, interfaces, modes, hazards, support, transition, and lifecycle. Check every applicable source is covered or has an authorized gap; every requirement has a source; inputs have producers; outputs have consumers; requirements have verification paths; and terms/states align. Missing axes remain possible, so invite independent challenge.

**Review consistency with models.** Use context, state, sequence, decision, data, dimensional, interface, resource, and hazard models. Contradictory next states, impossible timing budgets, circular preconditions, unreachable functions, and inconsistent units often remain invisible in isolated prose. Model consistency does not prove source validity.

**Record findings and dispositions.** A finding contains requirement/set identity, quality characteristic, evidence, consequence, severity, owner, proposed correction, decision, authority, and closure evidence. Corrections trigger trace and impact analysis. Preserve rejected findings and rationale; do not silently edit baselines during review.

**Use automation as bounded triage.** Linters can flag absent fields, weak phrases, pronouns, conjunctions, modal misuse, unit patterns, missing verification concepts, duplicate text, or broken links. False positives and negatives are inevitable. The executable checker below reports declared and lexical signals only.

<!-- bijux-verify: {"id":"requirement-quality-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"requirements_total=5\nwell_formed_declared=1\nmissing_source=RQ-004\nmissing_oracle=RQ-003\nmissing_conditions=RQ-002\nvague_signals=RQ-002:quickly\ncompound_signals=RQ-005:and\nwrong_modal=RQ-004:should\nquality_set_ready=false\nevidence=declared_fields_and_lexical_signals_only\n","stderr":""}} -->
```python
requirements = [
    {"id": "RQ-001", "text": "When authorized, the service shall record the decision.",
     "source": ["N-accountability"], "conditions": ["authorized"], "oracle": ["record comparison"]},
    {"id": "RQ-002", "text": "The service shall quickly recover.",
     "source": ["N-continuity"], "conditions": [], "oracle": ["state and timing oracle"]},
    {"id": "RQ-003", "text": "The sensor shall report temperature within tolerance.",
     "source": ["N-monitoring"], "conditions": ["operating range"], "oracle": []},
    {"id": "RQ-004", "text": "The controller should reject stale commands.",
     "source": [], "conditions": ["command age exceeds limit"], "oracle": ["state-machine oracle"]},
    {"id": "RQ-005", "text": "The platform shall revoke access and notify the owner.",
     "source": ["N-revocation"], "conditions": ["revocation approved"], "oracle": ["interface trace"]},
]

vague = ("quickly", "appropriately", "robust", "user-friendly")
complete = [r for r in requirements if r["source"] and r["conditions"] and r["oracle"]
            and " shall " in r["text"] and not any(w in r["text"] for w in vague)
            and " and " not in r["text"]]

print(f"requirements_total={len(requirements)}")
print(f"well_formed_declared={len(complete)}")
print("missing_source=" + ",".join(sorted(r["id"] for r in requirements if not r["source"])))
print("missing_oracle=" + ",".join(sorted(r["id"] for r in requirements if not r["oracle"])))
print("missing_conditions=" + ",".join(sorted(r["id"] for r in requirements if not r["conditions"])))
vague_hits = sorted(f'{r["id"]}:{w}' for r in requirements for w in vague if w in r["text"])
print("vague_signals=" + ",".join(vague_hits))
print("compound_signals=" + ",".join(sorted(f'{r["id"]}:and' for r in requirements if " and " in r["text"])))
print("wrong_modal=" + ",".join(sorted(f'{r["id"]}:should' for r in requirements if " should " in r["text"])))
print(f"quality_set_ready={str(len(complete) == len(requirements)).lower()}")
print("evidence=declared_fields_and_lexical_signals_only")
```

## Definitions and Notation

Let $N$ be authorized needs/source obligations, $R$ requirements, $D$ designs/realizations, $V$ verification evidence, and $O$ stakeholder outcomes.

Distinguish four relations:

$$
ReqVerified(R)\quad\text{(requirements are expressed correctly)},
$$

$$
ReqValidated(N,R)\quad\text{(requirements faithfully transform sources)},
$$

$$
ProductVerified(D,R,V)\quad\text{(realization satisfies requirements)},
$$

$$
SystemValidated(D,O)\quad\text{(realized operation satisfies intended outcomes)}.
$$

None implies all others without additional evidence. Let $A_r(x)$ be the acceptance predicate for requirement $r$ applied to observation set $x$. Let $Scope(V)$ denote the tested/analyzed configuration, conditions, population, and time. A pass supports $A_r$ only within that scope and inference model.

## Mechanisms, Invariants, or Proof Structure

The review mechanism has six passes: source/necessity; expression/semantics; model/set consistency; feasibility; verification concept; validation against operational intent. Findings and corrections loop through traceability and change control until the named baseline decision is supported.

For individual requirement $r$, use:

$$
Quality(r)=Necessary\land CorrectLevel\land Clear\land Singular\land
Feasible\land Traceable\land Verifiable.
$$

For set $R$, add:

$$
SetQuality(R)=SourceCoverage\land OperationalCoverage\land Consistency
\land CombinedFeasibility\land VerificationClosure.
$$

These are review predicates, not mechanically decidable theorems. Evidence and authority bound every judgment.

Maintain five invariants. **Meaning invariant:** controlled terminology and logic preserve one authorized interpretation. **Source invariant:** necessity and rationale remain traceable. **Discrimination invariant:** evidence can separate pass from fail. **Scope invariant:** evidence conclusions never exceed configuration and conditions. **Set invariant:** individual quality never substitutes for coverage and combined consistency.

## Alternatives and Trade-Offs

**Checklist versus model-based review.** Checklists cheaply enforce recurring discipline; behavioral and quantitative models reveal cross-requirement defects. Use both, weighted by complexity and consequence.

**Controlled natural language versus formal specification.** Controlled text improves shared review; formal models enable stronger analysis. Formal precision can encode the wrong intent, while prose can remain ambiguous. Maintain semantic correspondence and competent review.

**Direct test versus analysis.** Test observes a realization; analysis can cover rare, destructive, or continuous spaces using assumptions. Prefer a justified combination when neither alone supports the claim.

**Early permissive draft versus strict baseline.** Drafts support discovery and TBRs; design/contract baselines require stronger closure. Make maturity explicit so early uncertainty is neither hidden nor prematurely frozen.

**Independent review versus embedded expertise.** Authors know context; independent reviewers expose assumptions and confirmation bias. High-consequence work needs both, with clear competence and authority.

**One integrated verification versus decomposed evidence.** End-to-end evidence matches system claims but can be costly and diagnostically weak. Lower-level evidence scales but needs a composition argument. Preserve at least enough integrated evidence to test interfaces and emergence.

## Failure Modes and Misconceptions

1. **“The sentence passes the template, so it is good.”** Templates cannot establish necessity, source fidelity, feasibility, or coverage.
2. **“Testable and verifiable are synonyms.”** Test is one method; some claims need analysis, inspection, demonstration, or combined evidence.
3. **“One requirement per sentence is atomic.”** Independent obligations can hide in one sentence, and one transition can require several clauses.
4. **“A test case proves the requirement.”** The oracle, scope, configuration, uncertainty, and execution result determine evidence strength.
5. **“No failures means pass.”** Inadequate exposure, disabled checks, or wrong conditions can produce zero failures.
6. **“Inspection can verify any document-linked claim.”** Dynamic behavior and performance require observations or justified analysis.
7. **“Model proof verifies the product.”** It proves properties of a model under assumptions; implementation and environment correspondence remain.
8. **“Every source has a link, so the set is complete.”** Missing sources, wrong semantics, and omitted modes remain possible.
9. **“Rewrite the requirement to match available tools.”** Evidence strategy serves the obligation; tool limits do not redefine stakeholder need.
10. **“Passed verification means valid system.”** A system can meet the wrong requirements.

## Worked Examples

### Example 1

**Situation.** “The service shall respond quickly.” **Reasoning.** `Quickly` lacks boundary, request population, workload, mode, aggregation, threshold, and clock. Trace the user outcome, then specify eligible requests, start/stop, workload, window, percentile/proportion, threshold, timeout/error handling, and estimator. **Conclusion.** Weak-word detection identifies a defect; outcome evidence supplies the repair.

### Example 2

**Situation.** “The access system shall revoke credentials and notify owners.” **Reasoning.** Revocation and notification have distinct sources, completion states, failure consequences, and verification. Split them and link both to an end-to-end revocation thread. **Conclusion.** Atomicity follows independent governance, not the presence of `and` alone.

### Example 3

**Situation.** “The controller shall never energize while the guard is open.” **Reasoning.** `Never` is a strong but appropriate safety prohibition if scope is defined. Verification combines state-model analysis, interface inspection, fault injection, transition tests, and safety evidence across modes; finite tests alone cannot prove universal absence. **Conclusion.** Do not weaken a necessary invariant merely because exhaustive testing is impossible.

### Example 4

**Situation.** A p99 latency requirement has a test with 20 requests. **Reasoning.** The nominal empirical 99th percentile is effectively dominated by the maximum and has weak tail evidence. Define workload, minimum sample, repetitions, estimator, confidence/acceptance rule, and false-accept consequence. **Conclusion.** A runnable test is not necessarily a discriminating statistical verification.

### Example 5

**Situation.** Maintainability requires field restoration within four hours. **Reasoning.** Define failure classes, detection, diagnosis, access, parts, technician competence, environment, repair, calibration, verification, and return-to-service state. Use representative maintenance demonstrations plus analysis of logistics and censored cases. **Conclusion.** The test must reproduce the operational maintenance system, not only bench replacement.

### Example 6

**Situation.** A retention requirement is verified by inspecting a configuration value. **Reasoning.** Inspection shows declared configuration, not actual lifecycle behavior. Add clock/aging tests, deletion/hold conflicts, backup/archive behavior, access records, configuration enforcement, and operational audit. **Conclusion.** Select methods that observe the claim rather than its intended setting.

### Example 7

**Situation.** A routing requirement prescribes Dijkstra's algorithm. **Reasoning.** If the source requires correct feasible routes under conditions, the algorithm is design leakage. Move selection to design and define an independent path/cost oracle. If certification or interoperability mandates the algorithm, retain exact source and analyze implementation correctness. **Conclusion.** Testability does not justify unnecessary implementation constraint.

### Example 8

**Situation.** Two requirements demand `closed` and `open` as next state for the same event. **Reasoning.** Isolated prose reviews pass. A state table exposes overlapping current state, event, guard, and incompatible postconditions. Resolve mode/priority or source conflict under authority. **Conclusion.** Set consistency needs relational models.

### Example 9

**Situation.** “The AI system shall be fair.” **Reasoning.** Identify affected decisions, groups, harms, legal/ethical authority, distribution, reference outcomes, metrics, uncertainty, recourse, and tradeoffs. No universal fairness metric or test exists; multiple measures can conflict. **Conclusion.** Preserve the stakeholder concern, derive governed measurable obligations, and require affected/domain review without claiming automation proves fairness.

### Example 10

**Situation.** Emergency shutdown testing observes a command acknowledgment. **Reasoning.** The system-level requirement concerns hazardous energy and safe state. Verify command path, actuators, stored energy, feedback independence, timeout, dependency loss, operator indication, reset authority, records, and residual hazard using inspection, analysis, fault injection, and integrated tests. **Conclusion.** Evidence must close the end-to-end physical outcome at the requirement's level.

## Cross-Program Connections

- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) supplies invariants, commands, events, and state models that expose ambiguous requirements.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) tests feasibility and quality tradeoffs without silently rewriting sources.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) governs test-data representativeness, lineage, missingness, oracles, and reproducible evidence.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) adds adversarial requirements, assurance claims, negative testing, and threat-informed evidence.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) makes boundary conditions, state, errors, idempotency, timing, and compatibility testable.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) provides reusable evidence infrastructure while keeping acceptance authority with requirement owners.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html), second edition, 2018. Consulted 2026-08-31.
2. ISO/IEC/IEEE. [ISO/IEC/IEEE 15288:2023 — System life cycle processes](https://www.iso.org/standard/81702.html), second edition, 2023. Consulted 2026-08-31.
3. NASA. [Appendix C: How to Write a Good Requirement](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/), *NASA Systems Engineering Handbook*, Rev. 2. Consulted 2026-08-31.
4. NASA. [Systems Engineering Handbook Appendix](https://www.nasa.gov/reference/system-engineering-handbook-appendix/), verification and validation plan guidance. Consulted 2026-08-31.
5. SEBoK Editorial Board. [System Requirements Definition](https://sebokwiki.org/wiki/System_Requirements_Definition), *Guide to the Systems Engineering Body of Knowledge*, version 2.14. Consulted 2026-08-31.
6. SEBoK Editorial Board. [System Verification](https://sebokwiki.org/wiki/System_Verification), *Guide to the Systems Engineering Body of Knowledge*, version 2.14. Consulted 2026-08-31.
7. INCOSE Requirements Working Group. [*Guide for Writing Requirements*, version 4](https://www.incose.org/docs/default-source/working-groups/requirements-wg/gtwr/incose_rwg_gtwr_v4_040423_final_drafts.pdf), 1 July 2023. Consulted 2026-08-31.
8. Mavin, A., Wilkinson, P., Harwood, A., and Novak, M. [“Easy Approach to Requirements Syntax (EARS)”](https://doi.org/10.1109/RE.2009.9), IEEE International Requirements Engineering Conference, 2009. Consulted 2026-08-31.

## Exercises

### Exercise 1

Review “The system shall securely process all requests as soon as possible” against individual requirement quality characteristics. List findings without inventing a replacement threshold or security policy.

### Exercise 2

Split and rewrite “When a payment fails, the service shall retry, notify the customer, reverse all charges, and update the audit log” into candidate atomic obligations. Identify unresolved semantics, sources, and verification concepts.

### Exercise 3

Design a discriminating verification concept for “During regional network loss, authorized responders shall obtain the current evacuation boundary within 30 seconds.” Include system boundary, configuration, oracle, degraded conditions, population, timing, correctness, repetitions, and evidence limits.

### Exercise 4

Compare test, demonstration, inspection, and analysis for verifying a spacecraft safe-mode requirement. Build a combined argument and identify model/test-article limitations.

### Exercise 5

Conduct an individual and set-level quality review for requirements governing an AI-assisted medication-allergy warning capability. Cover source validity, ambiguity, completeness, consistency, feasibility, verification, human factors, safety, data, and external authority.

## Answers to the Exercises

### Answer 1

The subject `system` needs a controlled boundary. `Process` hides required input acceptance, transformation, output, rejection, and end state. `Securely` combines undefined protection properties, assets, threats, and assurance. `All` needs an eligible request domain, including invalid, duplicate, unauthorized, excessive, and malicious input. `As soon as possible` supplies neither threshold nor decision meaning and may demand unsafe resource use. Conditions, modes, workload, dependencies, units, tolerance, source, rationale, oracle, and verification level are absent.

The statement may combine functional behavior, security qualities, capacity/timing performance, and exception handling with independent sources and tests. Record findings rather than fabricating values. Retrieve stakeholder/operational needs, threat/risk and policy authority, request taxonomy, performance outcome evidence, system boundary, and failure modes. Then derive separately controlled obligations and a set-level coverage argument.

### Answer 2

First define `payment fails`: authorization declined, timeout, unknown outcome, capture failure, settlement failure, or local error require different behavior. Retry is permitted only for retryable classes and must address identity, idempotency, limit/backoff, authorization, and unknown outcomes. Notification requires recipient, content, channel, privacy, timing, and delivery failure. “Reverse all charges” needs transaction/state scope and may be wrong when no charge occurred. Audit requires event, provenance, time, decision, access, and durability.

Candidate obligations separately require classifying an observed failure; preventing duplicate financial effect; issuing an authorized retry only for defined states; initiating compensation when a completed effect must be reversed; recording each decision/state transition; and providing the customer a governed status when notification conditions hold. Sources include customer recourse, financial integrity, operational recovery, interface contracts, and regulatory/records authority. Verification uses a payment-state oracle and provider simulator across every failure/state pair, delayed/duplicate responses, restart, concurrency, compensation failure, notification failure, and audit reconciliation. Atomic requirements remain linked by an end-to-end state model.

### Answer 3

Name whether the SoI includes responder device, local cache/relay, identity, network, and boundary-data authority. Define authorized responder and current boundary, including version, issuer, effective time, geometry, uncertainty, conflict, and revocation. The 30-second interval needs start event and stop observation. Define regional network-loss profiles, power/device states, locations, concurrency, prior synchronization, and unavailable/corrupt data behavior.

Use an independent authoritative boundary/version oracle and synchronized observation clock. Exercise representative responder roles/devices/locations, cold/warm states, stale/conflicting caches, interruption, recovery, update during partition, unauthorized access, and false data. Require both timing and correct/provenant boundary; a fast stale response fails. Specify repetitions, population/coverage rationale, statistical acceptance if not a hard bound, missing results, artifacts, and configuration identity. Controlled tests support only covered outages and environments; field exercises and affected/emergency authority validate operational usefulness. They cannot prove all disasters, legal sufficiency, or human comprehension.

### Answer 4

Inspection can establish configured safe-mode logic, drawings, parts, limits, commands, labels, and traceability, but not dynamic transition. Analysis/model checking can cover state combinations, fault trees, timing/power/thermal/orbital behavior, and cases too destructive to test, conditional on model fidelity and assumptions. Demonstration can show operator initiation and observable mode behavior in representative sequences but usually lacks precise stress/fault measurement. Test applies controlled faults, power/interface conditions, and measures transition and retained functions on qualified articles.

Combine requirement/source inspection; formal/state/hazard and engineering analysis; software/hardware-in-loop and fault-injection tests; environmental qualification; integrated end-to-end tests; and operational demonstrations. Verify trigger detection, transition authority, prohibited functions, retained communications/control, energy/thermal state, data preservation, observability, failed transition, recovery, and reset. Record simulator and test-article pedigree, flight differences, untestable destructive conditions, common-cause assumptions, and composition evidence. Independent mission and safety authorities decide whether residual evidence is sufficient; model proof or ground pass alone does not prove flight safety.

### Answer 5

Sources include patient/clinician needs, medication workflow, allergy and reaction data definitions, clinical safety hazards, human-factors evidence, privacy/security obligations, interoperability, operations/support, and applicable regulatory authority. Verify every requirement has correct subject/level and trace rationale. Diagnose vague terms such as “significant allergy,” “appropriate warning,” “accurate,” and “immediately”; define timing, provenance, uncertainty, missing/conflicting/stale data, patient identity, medication classes, overrides, acknowledgment, escalation, record, downtime, update, and recovery.

At set level, model medication-order states and clinical roles; ensure data producers/consumers, alert generation, suppression, display, override, audit, correction, monitoring, and incident feedback close. Check consistency among privacy minimization, clinical context, alert fatigue, accessibility, latency, availability, and safety. Feasibility evidence includes terminology mapping, representative data analysis, workflow prototypes, interface tests, performance tests, and support capability without treating historical labels as truth.

Verification combines glossary/schema inspection, independent clinical rule/data oracle where justified, state/decision-table analysis, interface and fault tests, representative clinician/patient human-factors evaluation, subgroup/missing-data analysis, security/privacy review, and integrated clinical scenarios. Metrics cover missed hazardous cases, false/low-value warnings, overrides, comprehension, workflow delay, and outcome guardrails with uncertainty. Internal review cannot establish clinical correctness, safety, fairness, legal conformity, or acceptable residual risk; patient, clinical, pharmacy, human-factors, safety, data, privacy/security, ethics, quality, and regulatory authorities must review applicable claims. No external review is claimed.
