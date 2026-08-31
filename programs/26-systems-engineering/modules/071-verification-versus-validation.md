---
module_id: SYSENG-071
program: Systems Engineering
level: 2
module_number: 71
title: Verification Versus Validation
status: complete
last_verified: 2026-08-31
---

# Verification Versus Validation

## One-Page Review

### Governing question

What claim is being evaluated, about which configured object, against which reference, in what environment, with what evidence—and does the result show conformance to specified requirements, fitness for intended use, both, or neither?

### Essential definitions

- **Verification** provides objective evidence that a specified object fulfills specified requirements. In product realization, it asks whether the realized product conforms to its allocated and system requirements: *Was the specified thing built right?*
- **Validation** provides objective evidence that the system fulfills requirements for its specific intended use and satisfies stakeholder needs in the intended operational context: *Was the right thing built, and does it work for its purpose?*
- The **object** is the configured item being evaluated: requirement set, design, model, component, integrated system, procedure, service, or operational capability.
- The **reference** is what the object is compared with: formatting rules, source needs, specified requirements, design description, stakeholder expectations, measures of effectiveness (MOEs), concept of operations (ConOps), or intended-use claims.
- **Objective evidence** is inspectable information relevant to a claim, such as configuration-bound results, observations, analyses, trace records, measurements, anomaly dispositions, and provenance. “Objective” does not mean assumption-free or conclusive.
- A **verification method** may be analysis, inspection, demonstration, or test. The same physical activity can contribute to validation if its configuration, scenario, participants, environment, measures, and oracle address intended use.
- **Representativeness** is the defensible similarity between evaluation conditions and the intended population of configurations, users, environments, workloads, interfaces, and situations.
- An **oracle** is the rule or authority by which observed behavior is classified as acceptable, unacceptable, or inconclusive.
- **Qualification** establishes capability under specified stresses or conditions; **acceptance** is an authorized decision to receive or use a deliverable; **certification** is an attestation under a governing scheme. None is automatically synonymous with V&V.
- A **discrepancy/anomaly** is a difference between expected and observed result or condition. It remains evidence until explained, corrected, retested, waived by proper authority, or explicitly left open.

### Central model, mechanism, or theorem

Treat every V&V result as a bounded evidence tuple

\[
E=(O,R,C,M,P,D,Q,A,L),
\]

where $O$ is the object/configuration, $R$ the reference baseline, $C$ the context/environment, $M$ the method, $P$ the procedure and participants, $D$ the observed data, $Q$ the oracle/decision rule, $A$ anomalies and dispositions, and $L$ limitations. A verification claim is valid only for specified requirements actually traced and exercised under applicable conditions. A validation claim additionally requires credible stakeholder/intended-use references and representative operational context. Passing one does not logically imply the other.

### Critical invariants

- Always name the object and reference; “the system was validated” is incomplete without configuration, use, context, and evidence.
- Verify specified requirements and validate intended use/stakeholder expectations; do not substitute one baseline for the other.
- Requirements themselves can be verified for form/quality and validated against source needs; these are different from product verification and system validation.
- V&V is recursive, iterative, and lifecycle-wide—not a single test event after implementation.
- Evidence binds product version, requirement/expectation version, environment, procedure, instrumentation/tool versions, data, date, and responsible roles.
- Test success covers sampled conditions only. Analysis, inspection, demonstration, and test have different observability and inference limits.
- A shared activity may serve both verification and validation only with separate claims, references, measures, and conclusions.
- Simulators, models, stubs, and test equipment require credibility evidence proportionate to the claim they support.
- Human users, operators, maintainers, procedures, organizations, external systems, and degraded modes remain inside validation context where relevant.
- Anomalies, deviations, waivers, assumptions, untested conditions, and negative evidence remain visible.
- Acceptance and certification decisions use V&V evidence but require their own scope, criteria, authority, and record.
- Change to configuration, intended use, environment, stakeholder need, or evidence basis triggers impact analysis and selective re-V&V.

### Common failures

Common failures include using “V&V” as one undifferentiated test phase; verifying a complete but wrong requirement set; validating a prototype unlike the delivered configuration; claiming operational validity from a laboratory demonstration; letting a passed system test imply every requirement is verified; treating a requirements review as product validation; using the same developers and assumptions without independence review; testing nominal paths only; omitting operators, maintainers, external services, data, workload, and degraded conditions; confusing test method with verification purpose; treating no observed failure as proof of absence; accepting simulator output without model credibility; closing anomalies administratively; validating only once while use drifts; and equating customer signature with technical evidence.

### Compact example

A dispatch service has four specified requirements: accept a call, authenticate dispatch, acknowledge within five seconds, and retain an audit record. A controlled test passes all four, so the tested configuration is verified against that requirement subset. In a representative storm exercise, the service cannot prioritize life-threatening calls when demand triples. Stakeholders require emergency prioritization, but the need was never translated into a system requirement. Verification passes; validation fails; the proper response is to correct needs/requirements/design and assess impacted evidence—not reinterpret the four passing tests.

### Connections

Requirements quality and traceability define the verification reference; ConOps, scenarios, stakeholder value, MOEs, human factors, safety, reliability, interfaces, and operations define validation context. Configuration management, test engineering, model credibility, anomaly control, acceptance, certification, platforms, APIs, data, and security preserve and qualify the evidence.

## Governing Question

Can the engineering team state exactly which conformance and intended-use claims are supported by configuration-controlled evidence, distinguish those claims from acceptance or certification, and identify every assumption, unrepresented condition, discrepancy, and change that limits or invalidates reuse of the evidence?

The familiar phrases “built the thing right” and “built the right thing” are useful memory aids, not sufficient process definitions. “Right” must point to a reference. Verification compares an object with specified requirements or other required characteristics for that object. Validation compares the realized capability with stakeholder expectations, goals, MOEs, ConOps, and conditions of intended use. Different industries and standards also use V&V for requirements, designs, software, models, methods, and data. Avoid semantic disputes by naming the object, reference, purpose, and governing vocabulary.

## Why This Matters

A system can pass every written requirement and still fail its mission because the requirements omitted the real need, modeled the wrong environment, misunderstood users, or froze an obsolete operating concept. That is a validation failure with apparently successful verification. Conversely, a concept can solve the right problem yet be implemented incorrectly, inconsistently, or incompletely. That is a verification failure despite a valid purpose.

NASA's current product-realization guidance separates product verification against specified requirements from product validation against stakeholder expectations and intended operation. It treats configuration, enabling products, trained people, procedures, environments, results, anomalies, and reports as evidence-bearing work products. NASA also emphasizes end-to-end operational scenarios and comparison with ConOps, MOEs, and measures of performance. NIST glossary entries show that the distinction generalizes beyond one agency while warning that definitions must be read in source context.

The separation is economically important. Late discovery of a wrong system can invalidate large quantities of correct implementation evidence. Early validation of needs, scenarios, prototypes, and models can expose a mistaken concept before full realization. Early verification of requirements and design artifacts can expose ambiguity, incompleteness, infeasible tolerances, and interface inconsistency before they become hardware, software, training, or operational debt.

The distinction also prevents assurance theater. A large test count says little if it maps repeatedly to easy requirements while safety, interface, workload, and degraded-mode claims remain uncovered. A compelling user demonstration says little about limits, security, environmental qualification, or repeatability. A single event can generate evidence for both purposes, but the claims and oracles must remain separate.

Modern software-intensive systems make the boundary dynamic. Configuration changes continuously; external APIs and data distributions drift; users invent workflows; cyber threats adapt; models are retrained; feature flags alter behavior; infrastructure regions and suppliers change. Validation is therefore not a ceremonial final activity. Operational monitoring, incident evidence, user research, safety surveillance, and controlled experiments can extend validation—but only when their data, consent, ethics, configuration, and inference limits are governed.

## Prerequisites and Retrieval

Before crediting a V&V result, retrieve:

1. the decision/claim to support, governing standard or policy, terminology, technical authority, customer/stakeholder roles, acceptance and certification authorities, and required independence;
2. the exact object identity: hardware serial/lot, software build and dependencies, model/data version, configuration parameters, interfaces, procedures, documentation, people/skills, and operating mode;
3. the reference baseline: stakeholder needs, goals, objectives, ConOps, scenarios, MOEs, specified requirements, interface controls, safety/security constraints, regulations, standards, and approved changes;
4. bidirectional trace from needs through requirements, architecture/design, implementation, methods/procedures, results, anomalies, and decisions;
5. verification and validation plans, objectives, methods, levels, sequence, facilities, schedules, resources, entry/success/exit criteria, review gates, and re-V&V rules;
6. evaluation environment: physical, climatic, electromagnetic, network, data, load, timing, geography, facilities, external systems, simulated elements, failure/degraded states, and deviations from operation;
7. test/analysis articles and pedigree: production, qualification, engineering, prototype, digital, simulated, emulated, sampled, modified, or reused;
8. procedures, preconditions, inputs, instrumentation, calibration, time synchronization, tools, models, seeds, datasets, operators/testers, training, and chain of custody;
9. expected outcomes/oracles, tolerances, uncertainty, statistical design, stopping rules, multiple-comparison treatment, false positive/negative consequences, and inconclusive rules;
10. raw and processed results, logs, observations, analyst transformations, reproducibility, requirement/expectation disposition, discrepancies, retests, waivers/deviations, and residual/open actions;
11. operational evidence: real users and maintainers, workload, environment, demand, seasons, edge populations, accessibility, workarounds, incidents, near misses, complaints, support records, and outcome measures;
12. changes since evidence generation, including configuration, supplier, intended use, stakeholder, regulation, threat, environment, data distribution, scale, operating procedure, and organizational responsibility.

Apply an **evidence-thread audit**: choose one critical stakeholder outcome, trace it to expectation and ConOps scenario, derived requirements and interfaces, realized configuration, verification evidence, validation scenario, observed data, anomaly disposition, acceptance condition, and operational monitor. Then trace backward. A gap shows exactly what is unproven; it should not be hidden by an overall pass label.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish product verification, system validation, requirements V&V, model V&V, qualification, acceptance, and certification;
2. formulate bounded V&V claims using object, reference, context, method, configuration, oracle, evidence, and limitations;
3. explain how a system may pass verification and fail validation, or the reverse;
4. allocate V&V recursively across system levels and throughout the lifecycle;
5. choose analysis, inspection, demonstration, and test according to claim and observability;
6. assess environment, article, participant, workload, data, simulator, and operational representativeness;
7. distinguish observed data from interpretation, disposition, authorization, and assurance;
8. handle anomalies, waivers, inconclusive results, negative evidence, and retest without erasing history;
9. reuse evidence only after configuration, use, context, assumption, and credibility impact analysis;
10. construct a traceable decision package that states both supported claims and remaining uncertainty.

## Core Exposition

**Start with grammar.** Write: “Object O, configuration c, was verified against requirements baseline R using method M under conditions C; results D support claims K subject to limitations L.” For validation replace R with stakeholder/intended-use references and state representativeness. This prevents a one-word status from outrunning evidence.

**Distinguish four common uses.** Requirements verification checks that requirements possess required form and quality: unique, clear, singular, feasible, traceable, measurable, and consistently structured. Requirements validation checks that the requirement set correctly and sufficiently represents stakeholder needs and intended use. Product verification checks the realized item against its specified requirements. System validation checks the realized integrated system in its intended use. Mixing these makes teams believe that reviewing text validated the delivered capability.

**Make reference errors visible.** Verification is only as useful as the baseline. A perfectly executed test of an obsolete, inconsistent, or incomplete requirement proves conformance to the wrong reference. Baseline identity and change history are therefore part of every result. Validation can expose the reference error and drive change; impacted verification must then be repeated or justified.

**Treat V&V as recursive.** At each hierarchy level, an implemented element is verified against its allocated requirements and may be validated against expectations for that level. Lower-level success contributes to higher-level evidence but does not prove integration, emergence, or mission outcome. System behavior is more than the union of component tests.

**Treat V&V as iterative.** Validate problem framing, needs, scenarios, models, prototypes, operational concepts, and human work early. Verify requirements, interfaces, designs, models, code, production processes, and integrated products as they mature. Final system V&V confirms the delivered configuration, but it should not be the first encounter with mission reality.

**Choose the method by claim.** Inspection observes attributes without operating the product; analysis derives conclusions from data/models; demonstration shows capability with limited detailed measurement; test operates an article with controlled inputs and measured outputs. No method is inherently stronger. A test may be unsafe, unrepresentative, or sparse; a proof or analysis may cover a large domain but depend on abstractions and premises.

**Separate activity from purpose.** A thermal-chamber test may verify a temperature requirement. If chamber profiles represent the real mission and outcomes are assessed against intended-use expectations, some data may also support validation. Record two evidence links with distinct criteria. Calling every test “V&V” destroys traceability.

**Define the oracle before observation.** State expected values, tolerances, uncertainty, timing windows, forbidden outcomes, coverage, and inconclusive conditions. Post hoc thresholds invite motivated reasoning. For adaptive or nondeterministic systems, use statistical or property-based oracles with controlled error rates and stated populations.

**Control configuration.** Identify the article and all behavior-affecting elements: firmware, software, dependencies, calibration, flags, data, credentials, network policy, infrastructure, models, documentation, and operator procedure. A passing engineering unit does not automatically cover production units; a passing build does not cover later dependencies.

**Establish readiness.** Confirm approved plan/procedure, baselines, article, environment, enabling systems, calibrated instrumentation, representative participants, trained staff, safety controls, data collection, anomaly process, authority, schedule, and resources. A readiness review is evidence that execution can mean what it claims—not a guarantee of pass.

**Engineer representativeness.** Map operational ranges and populations to the evaluation: demand, temporal patterns, geography, environment, user capability, maintainers, external interfaces, data distributions, fault/degraded states, adversarial behavior, and recovery. State every substitution. Validate the mapping with analysis and operational evidence.

**Include human work.** Users and operators are not generic signal generators. Skill, training, fatigue, protective equipment, accessibility, workload, organizational incentives, communication, and procedure quality can determine outcome. Laboratory experts may overstate usability and recovery performance.

**Preserve end-to-end semantics.** Integrated scenarios should follow inputs through sensors, networks, services, decisions, people, physical effects, records, and downstream outcomes. Passing local interfaces does not prove units, timing, identity, error semantics, authority, or eventual stakeholder effect.

**Challenge nominal success.** Include boundaries, invalid input, overload, timing races, partial failure, common cause, degraded modes, maintenance, recovery, rollback, stale/corrupt data, loss of observability, security misuse, and emergency operations. Validation must also examine whether users recognize limitations and take correct action.

**Bound sampling claims.** Testing finitely many cases never proves universal absence of defects unless a justified finite partition or exhaustive domain applies. Statistical reliability demonstrations need population, independence, censoring, confidence, and stopping assumptions. “Zero failures” is data, not certainty.

**Qualify models and simulators.** Verify implementation against equations/specification; validate the model for the intended decision/use; quantify input, parameter, structural, numerical, and measurement uncertainty; and assess the simulator/interface. A model valid for average performance may be invalid for safety tails.

**Use independence deliberately.** Independent V&V can reduce shared assumptions, confirmation bias, and organizational conflict, particularly for high-consequence claims. Independence has dimensions: technical, managerial, financial, and tool/data. It does not replace domain knowledge or make evidence automatically correct.

**Handle anomalies as evidence.** Stop or contain when required; preserve context and raw data; classify product, requirement, procedure, environment, tool, instrumentation, data, or execution cause; assess impact; authorize correction/waiver; rerun affected work; and retain before/after evidence. “Test error” requires evidence.

**Distinguish waiver from satisfaction.** A waiver/deviation may authorize delivery or operation despite nonconformance under defined scope and risk. It does not turn a failed requirement into a passed verification. Report technical status and authorization separately.

**Separate acceptance and certification.** A customer may accept with conditions for contractual or mission reasons; a regulator or delegated body may certify within a scheme; a technical team generates V&V evidence. Each has distinct criteria and authority. One can exist without proving the others beyond its scope.

**Reuse evidence conservatively.** Compare old and new configurations, requirements, environments, uses, populations, interfaces, suppliers, tools, and assumptions. Determine unaffected, reusable-with-analysis, or invalidated evidence. Heritage and COTS reduce development burden only when relevance is established.

**Continue in operation.** Monitor stakeholder outcomes, requirement performance, safety/security constraints, anomalies, user behavior, drift, maintenance, updates, and environment. Operational evidence can strengthen or refute validation claims. Define triggers for restricted use, investigation, rollback, re-verification, and re-validation.

**Report coverage honestly.** A verification matrix needs each requirement, method, level, article, environment, procedure, result, evidence link, anomaly, and status. A validation matrix or case maps stakeholder expectations, scenarios, MOEs, context dimensions, participants, evidence, gaps, and conclusions. Percent complete is secondary to critical uncovered claims.

The following synthetic fixture demonstrates why complete verification of a written subset does not imply validation of intended use.

<!-- bijux-verify: {"id":"verification-validation-distinction-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"specified_requirements=4\nrequirements_verified=4\nverification_status=passed_for_declared_subset\nstakeholder_expectations=3\nexpectations_validated=2\nvalidation_gap=prioritize_life_threats_under_surge\nvalidation_status=failed\nacceptance_status=not_decided\nstatus=declared_vv_distinction_consistent\nevidence=synthetic_trace_and_scenario_results_only\n","stderr":""}} -->
```python
requirements = {
    "accept_call": True,
    "authenticate_dispatch": True,
    "acknowledge_within_5s": True,
    "retain_audit_record": True,
}
expectations = {
    "receive_emergency_requests": True,
    "dispatch_authorized_resources": True,
    "prioritize_life_threats_under_surge": False,
}

verified = sum(requirements.values())
validated = sum(expectations.values())
gaps = [name for name, result in expectations.items() if not result]

print(f"specified_requirements={len(requirements)}")
print(f"requirements_verified={verified}")
print("verification_status=passed_for_declared_subset" if verified == len(requirements)
      else "verification_status=failed")
print(f"stakeholder_expectations={len(expectations)}")
print(f"expectations_validated={validated}")
print("validation_gap=" + ",".join(gaps))
print("validation_status=passed" if validated == len(expectations)
      else "validation_status=failed")
print("acceptance_status=not_decided")
print("status=declared_vv_distinction_consistent")
print("evidence=synthetic_trace_and_scenario_results_only")
```

The fixture assumes boolean results and omits configuration, procedure, uncertainty, coverage, severity, representativeness, anomalies, and evidence pedigree. It demonstrates logical separation only; it does not establish a real verification, validation, readiness, safety, or acceptance result.

## Definitions and Notation

Let $O$ be an evaluation object with configuration $c$, $R_v$ a versioned specified-requirements set, and $R_u$ a versioned intended-use/stakeholder-expectation set. Let $C$ describe conditions and $D$ observed evidence.

A bounded verification judgment can be written

\[
J_{ver}=Q_v(O_c,R_v,C,D,A,L),
\]

and validation as

\[
J_{val}=Q_u(O_c,R_u,C,\rho,D,A,L),
\]

where $Q_v,Q_u$ are declared decision rules, $A$ anomalies/dispositions, $L$ limitations, and $\rho$ the argument that $C$ and participants/data/article represent intended operation. These expressions are accountability structures, not numeric formulas or proofs.

Let trace relation $T_v\subseteq R_v\times E$ connect requirements to evidence and $T_u\subseteq R_u\times S\times E$ connect expectations to scenarios and evidence. Coverage counts are necessary diagnostics but not sufficiency claims: criticality, method adequacy, negative evidence, configuration, and inference all matter.

An **evaluation result** is observed data plus context; a **finding** interprets it against a criterion; a **disposition** decides what happens to a discrepancy; an **authorization** permits delivery/use; an **assurance claim** explains why the evidence supports confidence. Keeping these types separate prevents management decisions from rewriting technical facts.

## Mechanisms, Invariants, or Proof Structure

A trustworthy V&V claim follows this chain:

1. **Purpose:** state the decision and exact conformance or intended-use claim.
2. **Reference:** control the applicable requirement, expectation, ConOps, MOE, and rule versions.
3. **Object:** identify the product/model/procedure/system configuration and article pedigree.
4. **Context:** define conditions, populations, interfaces, participants, data, faults, and operational mapping.
5. **Method:** select analysis, inspection, demonstration, or test and justify inference.
6. **Oracle:** predeclare expected results, tolerances, uncertainty, pass/fail/inconclusive rules, and authority.
7. **Execution:** preserve procedure adherence, calibration, tool versions, raw data, deviations, and chain of custody.
8. **Analysis:** recompute transformations, quantify uncertainty, challenge alternatives, and retain negative evidence.
9. **Disposition:** trace findings, anomalies, corrections, waivers, retest, and open limitations without relabeling failure.
10. **Decision:** state bounded conclusion, acceptance/certification status, residual gaps, owners, and re-open triggers.

Three invariants dominate. First, **reference integrity**: a result cannot support a baseline it did not evaluate. Second, **configuration integrity**: a result cannot silently migrate to a different article or environment. Third, **claim proportionality**: the conclusion cannot be broader than method coverage and representativeness.

There is no logical implication $J_{ver}=pass\Rightarrow J_{val}=pass$. An omitted need is a counterexample. Nor does validation success imply verification: a prototype can delight representative users while violating a specified safety margin, audit rule, or interface limit. Both judgments are required when both claim types matter.

## Alternatives and Trade-Offs

**Early versus late evidence.** Early models, prototypes, and simulations cheaply expose wrong assumptions but have lower article fidelity. Late integrated evidence has fidelity but high correction cost and limited schedule. Use progressive evidence with explicit credit rules.

**Component versus end-to-end evaluation.** Component work localizes defects and covers boundaries efficiently. End-to-end work exposes integration and emergent behavior. Neither substitutes for the other; allocate based on claim and failure consequence.

**Laboratory versus operational evaluation.** Laboratory control improves repeatability, measurement, and safety. Operational context improves ecological validity but introduces uncontrolled variables, ethics, risk, and reproducibility challenges. Hybrid facilities, shadow modes, pilots, and staged rollout can bridge the gap.

**Real versus simulated elements.** Simulation supports rare, hazardous, large-scale, or not-yet-built conditions. Real elements expose physical and organizational effects. Credit depends on model validity, simulator verification, interfaces, latency, data, and intended inference.

**Scripted versus exploratory/adversarial work.** Scripted procedures support repeatability and formal disposition. Exploratory and adversarial work discovers unknown interactions. Preserve exploratory evidence and convert important findings into controlled regression and requirements/scenarios.

**Developer versus independent evaluation.** Developers have detailed knowledge and fast diagnosis. Independent teams challenge shared assumptions and conflicts. Consequence, novelty, regulation, and organizational incentives determine needed independence.

**Requirement-by-requirement versus scenario-based evidence.** Atomic mapping proves stated conformance; scenarios expose interactions and stakeholder outcomes. One scenario may cover many requirements but still needs exact evidence links; a matrix may be complete yet miss mission coherence.

**One-time versus continuous validation.** Formal baselines support accountable release decisions. Continuous telemetry and user/outcome evidence detect drift. Operational collection must address privacy, safety, bias, observability, causality, and change control.

## Failure Modes and Misconceptions

**“Testing equals verification.”** Test is one method. Verification is the evidence-backed conformance purpose. Inspection, analysis, and demonstration may be appropriate; a test without a traced criterion proves little.

**“Verification is internal; validation is customer acceptance.”** Roles vary. The distinction is reference and claim, not merely who attends. Acceptance is a separate authorized decision.

**“The V-model puts V&V at the end.”** The diagram connects definition/decomposition with integration/evaluation. Good practice validates and verifies artifacts throughout, recursively and iteratively.

**“All shall statements passed, so the system is valid.”** The requirement set may be incomplete, stale, inconsistent with need, or wrong for operation. Passing it proves only bounded conformance.

**“Users liked the demo, so it is validated.”** Participants, tasks, environment, training, duration, stakes, workload, and configuration may be unrepresentative. Satisfaction is one observation, not full mission evidence.

**“A prototype result transfers to production.”** Manufacturing, dependencies, calibration, performance, hardening, data, interfaces, and procedure can differ. Perform configuration/pedigree impact analysis.

**“No failures means reliability is verified.”** A finite zero-failure sample produces a conditional statistical bound at best; it does not prove universal reliability or safety.

**“The simulator is conservative.”** Conservatism must be parameter- and outcome-specific. A model can overpredict one load while missing another mechanism. Verify and validate it for use.

**“We waived it, so it passed.”** Waiver is authorization despite nonconformance under conditions. Preserve failed technical status and risk ownership.

**“Retest erased the anomaly.”** Retest can show correction for a bounded configuration. The original result informs cause, recurrence, coverage, and regression impact.

**“Production telemetry validates automatically.”** Observational data may be biased, confounded, censored, privacy-limited, or blind to near misses. Define outcome, population, instrumentation, and inference.

**“Reuse saves all V&V.”** Heritage evidence applies only where configuration, requirements, environment, use, interfaces, and assumptions remain relevant.

## Worked Examples

### Example 1

**Situation.** A requirement set uses unique identifiers, shall language, units, tolerances, and trace links, but omits emergency surge priority.

**Reasoning.** A requirements-quality review can verify conformance to syntax and quality rules. Comparing the set with stakeholder interviews and storm scenarios reveals the missing need, so requirements validation fails. No product exists yet; neither result is product verification or system validation.

**Conclusion.** Label the object and reference: the requirements are structurally verified but not validated as a sufficient representation of intended use.

### Example 2

**Situation.** A pump delivers the specified 100 L/min across the required pressure range in a calibrated rig, but operators cannot reach the emergency isolation valve while wearing required protective equipment.

**Reasoning.** Flow verification passes for the tested configuration and conditions. The operational task fails with representative users/equipment, contradicting safe intended use. Check whether access requirements were missing or incorrectly allocated, update hazard/requirements/design, and re-run impacted evidence.

**Conclusion.** Successful performance verification coexists with failed validation of emergency operation.

### Example 3

**Situation.** Representative clinicians safely complete a dosing workflow on a prototype, but the implementation stores audit events without the specified immutable signature.

**Reasoning.** Workflow evidence supports a bounded validation claim about usability and purpose. Inspection/test against the audit requirement fails. Acceptance or continued pilot authority cannot relabel the nonconformance.

**Conclusion.** Validation evidence does not imply verification; correct the audit implementation and reassess integration and operational claims.

### Example 4

**Situation.** One integrated disaster exercise is claimed to verify 120 requirements.

**Reasoning.** The exercise may generate observations relevant to many requirements, but each needs a trace, applicable preconditions, observable output, calibrated measurement, oracle, and result. Some requirements—storage endurance, cryptographic properties, inaccessible internal states—need other methods. Scenario success supports mission coherence but not unseen attributes.

**Conclusion.** Credit only requirements for which the event produced adequate evidence; keep scenario validation and atomic verification distinct.

### Example 5

**Situation.** A controller passes in a simulator for 10,000 weather sequences. The aerodynamic model was calibrated only for nominal icing.

**Reasoning.** Controller implementation may be verified against its algorithm, and the simulator may be verified against equations. Validation for severe icing is unsupported because model-form/data coverage excludes that regime. More runs amplify an invalid premise rather than add real-world coverage.

**Conclusion.** Restrict the claim to the validated model domain and obtain severe-icing evidence or redesign the decision.

### Example 6

**Situation.** A service passes a latency requirement with 1,000 requests per second, but the operational workload is bursty, tenant-skewed, and triggers retries across shared dependencies.

**Reasoning.** Verification may pass for the specified constant-load procedure. Validation mapping shows workload and dependency behavior are unrepresentative. Update workload scenarios and perhaps requirements; test bursts, skew, retry amplification, failure, recovery, and user outcomes.

**Conclusion.** Laboratory conformance is bounded by its workload; operational fitness remains unvalidated.

### Example 7

**Situation.** A test fails once, the team calls it “operator error,” retrains the tester, and a retest passes.

**Reasoning.** Preserve both runs. Determine whether procedure ambiguity, interface design, training assumption, fatigue, tooling, or product behavior caused the error. If intended users can make the same action, it is validation evidence, not disposable noise. Retest confirms only the corrected conditions.

**Conclusion.** Do not erase the anomaly; disposition cause, impact, recurrence, and representative-user implication.

### Example 8

**Situation.** A supplier component was qualified in a previous product with a benign indoor environment; the new use adds vibration, salt fog, and an emergency function.

**Reasoning.** Compare requirements, environment, interfaces, mission time, configuration, manufacturing change, and failure consequence. Prior evidence may support material or nominal behavior but not new stresses or safety use. Allocate additional qualification, integration verification, and operational validation.

**Conclusion.** Heritage is evidence with a domain, not a transferable pass label.

### Example 9

**Situation.** A customer accepts a release with a waived capacity requirement because seasonal demand begins tomorrow.

**Reasoning.** Technical verification remains failed for capacity. Acceptance records authorized delivery conditions, usage limits, monitoring, residual risk, corrective owner/date, and rollback. Validation of intended peak use is also limited or failed. The business decision and evidence status coexist.

**Conclusion.** Report “accepted with conditions; requirement not verified,” not “verified by waiver.”

### Example 10

**Situation.** Six months after launch, users apply an image classifier to a new sensor and population not in the intended-use statement; confidence scores remain high while outcomes degrade.

**Reasoning.** Configuration may be unchanged, but use and data distribution changed. Original validation does not cover the new population/sensor. Detect drift through outcome monitoring, restrict unsupported use, investigate representativeness and bias, update intended use/requirements, and perform selective re-validation and perhaps re-verification.

**Conclusion.** Intended-use drift invalidates broad reuse of the original claim even without a code change.

## Cross-Program Connections

- **API and service engineering:** contract conformance verifies schemas/protocols; validation requires real consumer workflows, failure semantics, scale, migration, and outcomes.
- **Platform engineering:** deployment checks verify configuration; developer productivity, safety, recovery, and cognitive load validate platform purpose.
- **Data engineering:** schema and pipeline tests verify specified transformations; validation examines semantic correctness, freshness, representativeness, downstream decisions, and drift.
- **Object-oriented programming:** unit/interface conformance can verify contracts; substitutability and real collaboration scenarios expose emergent behavior.
- **Functional programming:** types, proofs, and properties strengthen verification within models; intended-use validity still depends on premises, effects, data, and context.
- **Security engineering:** control implementation can be verified; validation requires threat, mission, human, recovery, and adaptive-adversary context.
- **Reliability and safety:** demonstrations, hazard-control evidence, statistical assumptions, common causes, operational exposure, and risk authority require both claim types.
- **Human factors:** representative participants, work, training, workload, accessibility, fatigue, and organizational setting are validation essentials.
- **Modeling and simulation:** implementation verification and model validation for a purpose must precede credible system evidence reuse.
- **Governance:** configuration, traceability, anomaly disposition, waiver, acceptance, certification, independence, and change control preserve evidence meaning.

## References

1. NASA, [Product Verification, Systems Engineering Handbook section 5.3](https://www.nasa.gov/reference/5-3-product-verification/), updated 2023.
2. NASA, [Product Validation, Systems Engineering Handbook section 5.4](https://www.nasa.gov/reference/5-4-product-validation/), accessed 2026-08-31.
3. NASA, [Product Realization, Systems Engineering Handbook section 5.0](https://www.nasa.gov/reference/5-0-product-realization/), accessed 2026-08-31.
4. NASA, [Product Integration, Systems Engineering Handbook section 5.2](https://www.nasa.gov/reference/5-2-product-integration/), accessed 2026-08-31.
5. NASA, [Verification and Validation Plan Outline, Systems Engineering Handbook Appendix I](https://www.nasa.gov/reference/appendix-i-verification-and-validation-plan-outline/), accessed 2026-08-31.
6. NASA, [NPR 7123.1B, NASA Systems Engineering Processes and Requirements, Change 4](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001B_&page_name=all), effective 2020.
7. NIST Computer Security Resource Center, [Validation glossary entry](https://csrc.nist.gov/glossary/term/validation), accessed 2026-08-31; source-specific definitions are identified on the page.
8. NIST, [Verification glossary entry](https://www.nist.gov/glossary-term/34441), accessed 2026-08-31; measurement-context notes are retained on the page.
9. Federal Aviation Administration, [Acquisition Management System Lifecycle Verification and Validation Guidelines, Version 3.0](https://www.faa.gov/sites/faa.gov/files/2022-02/vandvguidelines.pdf), 2017.
10. NASA, [NASA Systems Engineering Handbook, NASA/SP-2016-6105 Rev. 2](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf), 2016.

## Exercises

### Exercise 1

For each activity, identify the object, reference, and best label: reviewing system requirements for unique IDs and measurable tolerances; comparing requirements with stakeholder emergency scenarios; testing delivered software against response-time requirements; observing representative users achieve mission goals in the field; and a customer signing conditional delivery acceptance.

### Exercise 2

A cold-storage controller has verified requirements for maintaining 2–8°C, logging every minute, and alarming after two minutes outside range. In a realistic exercise, staff receive alarms but cannot identify which physical room is affected because room naming differs across displays and procedures. Analyze verification, validation, requirement quality, and next actions.

### Exercise 3

Construct an evidence tuple and trace for validating an emergency offline mode in a payment service. Include configuration, needs/ConOps, participants, environment, data, dependencies, oracle, anomalies, limitations, and what must be separately verified.

### Exercise 4

A reusable navigation model was validated for urban passenger cars at speeds below 130 km/h. A new project proposes using it for autonomous mining vehicles on unpaved sites with dust, poor maps, and no lane markings. Decide what evidence is reusable and plan model/system V&V without merely saying “retest everything.”

### Exercise 5

An adaptive decision system passed release V&V, but operational outcome disparity grows for one population after a data-source change. Design a bounded investigation and re-V&V decision including containment, configuration/data trace, causal limits, requirements/intended-use review, evidence, authority, and reopening criteria.

## Answers to the Exercises

### Answer 1

Unique-ID/tolerance review has the requirements set as object and the organization's requirements-quality rules as reference: requirements verification. Comparing those requirements with emergency scenarios has the same object but stakeholder needs/ConOps as reference: requirements validation. Testing delivered software against response-time requirements is product/software verification, bounded by build, environment, workload, procedure, and measurement. Observing representative users achieve mission goals in the intended field context is system validation, provided representativeness and outcome oracles are defensible. Customer signature is acceptance, an authorized commercial/mission decision; it may consume V&V evidence but is not itself sufficient technical verification or validation.

The labels matter because each result supports a different claim. A well-formed requirement may still be wrong, a conforming product may be unfit, a useful demonstration may hide nonconformance, and acceptance may tolerate known gaps.

### Answer 2

The configured controller may be verified against the three stated requirements if calibrated evidence covers range, log interval, and alarm timing. The realistic exercise reveals failed validation of the operational outcome: staff cannot locate and respond to the affected room. The issue may reflect an omitted stakeholder need/requirement for consistent identity, an interface requirement conflict, inadequate display/procedure design, configuration/data mismatch, or training—not necessarily failure of the alarm timing requirement.

Preserve the result and trace naming across sensor, controller, alarm, display, facility map, procedure, and staff vocabulary. Update stakeholder expectations and ConOps, verify/validate revised requirements, analyze hazards and affected interfaces, correct design/data/procedure/training as appropriate, verify each changed requirement, and repeat representative validation including multiple rooms, shifts, degraded communications, and response timing. Existing temperature/log/alarm evidence is reusable only after configuration-impact analysis. The bounded conclusion is “declared functions conformed, operational identification failed.”

### Answer 3

Object/configuration includes payment-service build, feature flags, ledger/database schemas, identity, keys, offline device/app versions, synchronization rules, network policy, operator procedure, and dependent services. Reference includes the need to continue bounded essential payments during network loss without duplicate value or unauthorized spending, ConOps, safety/security/legal constraints, RTO/RPO, and user expectations. Participants represent merchants, customers, fraud/operations, accessibility needs, and support roles. Context includes realistic transaction mix, device clocks, intermittent connectivity, stale credentials, limits, geographic load, queue duration, recovery, and a second interruption.

Oracles cover authorized offline eligibility, amount/count limits, durable local record, user-visible mode, duplicate/conflict behavior, audit/provenance, reconciliation, fraud exposure, recovery time, and prohibited irreversible loss. Evidence tuple records exact configuration/reference, scenario, procedures, participant sampling, instrumentation/time, raw logs and observations, anomalies, deviations, and limitations. Separately verify cryptography, storage durability, schema/protocol rules, boundary calculations, access control, timing, failure handling, and every allocated requirement by suitable methods. Validation cannot infer exhaustive security or all populations from one exercise; verification cannot establish usability and ecosystem recovery alone.

### Answer 4

Reuse the model's implementation-verification evidence if code, equations, numerical methods, dependencies, and configuration remain unchanged. Reuse urban calibration data as provenance and perhaps evidence about generic sensor/algorithm behavior, but not as validation for the mining use. Compare domains explicitly: vehicle dynamics and speed may overlap, while surface, dust, vibration, sensor occlusion, map quality, geometry, lane assumptions, obstacles, communications, maintenance, and consequence differ.

Identify model assumptions and operational design domain. Verify new interfaces, coordinate frames, units, timing, hardware, degraded behavior, and safety constraints. Validate submodels using representative mining data and physical tests; quantify measurement, parameter, numerical, and structural uncertainty. Exercise boundary and hazardous scenarios with hardware-in-loop or controlled site trials, then integrated vehicles with trained operators/maintainers and emergency authority. Preserve urban evidence for unaffected claims; mark lane/map and dust-sensitive claims invalid; use analysis to justify any transferable dynamics. System validation covers actual missions and human/organizational work, while the model is validated only for each credited decision and domain.

### Answer 5

Contain first according to consequence: restrict the affected use, add human review, rollback the data source/model if safe, or suspend automated decisions while preserving records. Freeze and identify model, code, feature, threshold, data-source/schema, training/evaluation datasets, infrastructure, and policy versions before and after change. Confirm instrumentation quality and whether disparity reflects outcome, selection, missingness, delayed labels, population shift, treatment difference, or another confounder; do not claim causality from a dashboard alone.

Revisit stakeholder needs, intended-use population, fairness/safety/legal constraints, and requirements. Determine whether the data-source change violated a verified interface/data requirement, invalidated training assumptions, or expanded use. Re-verify ingestion, lineage, schema, missingness handling, feature transformations, model artifact, thresholds, access, monitoring, rollback, and relevant performance requirements. Re-validate with representative affected stakeholders and outcomes, stratified uncertainty, plausible alternatives, human workflow, feedback effects, and operational context. Record anomalies and negative results.

The authorized product, domain-risk, legal/privacy, data, model, and acceptance roles decide release/restriction under the governing process. Reopen on material data/population/use/model/policy change, outcome-control-limit breach, monitoring loss, incident, or evidence invalidation. The conclusion must state population, period, configuration, causal limits, residual disparity, containment, and external-review limits rather than declaring the system globally “revalidated.”
