---
module_id: SYSENG-074
program: Systems Engineering
level: 2
module_number: 74
title: Requirement-Based Verification
status: complete
last_verified: 2026-08-31
---

# Requirement-Based Verification

## One-Page Review

### Governing question

For every applicable requirement in the controlled baseline, what exact, configuration-bound evidence demonstrates satisfaction or nonconformance under its stated conditions, and can a reviewer trace that judgment both backward to the requirement's source and forward through method, procedure, results, anomalies, and authorization?

### Essential definitions

- A **requirement** is a uniquely identified, necessary, unambiguous, feasible, verifiable statement of required function, performance, interface, quality, constraint, or process under declared conditions.
- **Requirement-based verification** organizes evidence and closure around each applicable specified requirement rather than around test events, components, documents, or informal claims.
- A **verification requirement/statement** defines how conformance to a source requirement will be established: object, method, level, conditions, article, observable, oracle, and required evidence.
- **Bidirectional traceability** supports navigation from source/need through requirements, design/implementation, verification activity, result, anomaly, and decision—and backward from evidence or product behavior to the governing requirement and rationale.
- A **requirements verification matrix (RVM/VCRM)** is a controlled view mapping requirements to source, success criteria, method, level, facility/environment, article, responsibility, procedure, result, evidence, anomaly, and status. The authoritative relationships may reside in a model/database.
- **Applicability** declares whether a requirement governs the system/configuration and why. “Not applicable” requires authorized rationale; absence from a matrix is not tailoring.
- A **success criterion** is the predeclared observable decision rule for conformance, including conditions, tolerance, uncertainty, statistical meaning, and fail/inconclusive handling.
- **Objective evidence** is inspectable, configuration-bound information relevant to the claim: approved records, measurements, analysis reports, review findings, logs, artifacts, calibrated results, discrepancy dispositions, and provenance.
- A **verification closure package** is the minimum evidence bundle that permits an authorized technical status for one requirement or an explicitly governed group.
- **Coverage** means a requirement has a planned or executed evidence link; **closure** means adequate reviewed evidence and anomalies support an authorized status. Coverage is not compliance.

### Central model, mechanism, or theorem

Represent each baseline requirement $r$ with a closure record

$$
C_r=(S_r,B_r,V_r,P_r,E_r,A_r,J_r),
$$

where $S$ is source/rationale/applicability, $B$ the requirement and product configuration baseline, $V$ the verification statement/method/conditions/oracle, $P$ the approved procedure and execution pedigree, $E$ raw and analyzed objective evidence, $A$ discrepancies and their dispositions, and $J$ the reviewed status/authority/limitations. The system requirement set is not verified merely because every row has a method or a linked test. Every applicable $C_r$ must be internally consistent, and cross-cutting/emergent requirements need evidence at the level where their property exists.

### Critical invariants

- Every applicable normative requirement has a stable unique identity, authoritative source, version, owner, rationale, and verification path.
- Every verification activity and evidence artifact traces to a justified requirement, interface, hazard control, or explicitly labeled learning objective.
- Requirement text, success criterion, method, level, article, environment, and procedure agree semantically; a convenient proxy cannot silently replace the required property.
- One compound requirement is not closed by evidence for one clause. Split independently verifiable obligations or track every subclaim explicitly.
- Parent requirements are not automatically closed because children pass; allocation completeness, integration, emergent behavior, and parent-level conditions require an argument.
- A test case linked to a requirement is not evidence until the controlled activity executes and reviewed results satisfy its oracle.
- Evidence identity includes requirement/product/procedure/tool/model/data/instrument/environment versions and all deviations.
- Pass, fail, inconclusive, waived/deviated, not applicable, superseded, and open are distinct statuses.
- A waiver/deviation preserves the technical nonconformance, risk, conditions, authority, and expiry; it is not a pass.
- Discrepancies and negative evidence remain linked through correction, regression, retest, and closure.
- Coverage metrics are stratified by criticality and evidence adequacy; aggregate percentages do not hide unclosed critical requirements.
- Baseline or implementation change triggers bidirectional impact analysis and selective re-verification.

### Common failures

Common failures include creating tests first and attaching requirements afterward; treating a requirements-to-test link as closure; omitting inherited, interface, regulatory, hazard-control, process, and nonfunctional requirements; copying requirement text into multiple tools without configuration authority; combining several “shall” clauses; verifying a derived child while ignoring its parent mission condition; using design review as product evidence; accepting a proxy metric; changing success criteria after results; linking only summary reports without raw data/provenance; closing despite open anomalies; counting waived rows as passed; marking difficult requirements not applicable; using green coverage percentages while safety rows remain open; orphaning evidence after renumbering; and reusing heritage results without requirement/configuration comparison.

### Compact example

A synthetic six-requirement matrix has source, bidirectional trace, method, procedure, evidence, and result fields for every row. Five pass; the sixth has an unresolved timing anomaly. Structural coverage is 100%, but only five requirements are closed and baseline closure is incomplete. After the anomaly is corrected, affected evidence rerun, and disposition reviewed, all six close. The fixture validates only synthetic record logic; it does not establish real requirement quality, method adequacy, evidence truth, or authority.

### Connections

Requirements validation ensures the baseline represents stakeholder need; verification planning and methods create credible evidence paths; interfaces, models, integration, safety, reliability, security, configuration, data, anomalies, acceptance, and certification determine whether per-requirement evidence composes into trustworthy system assurance.

## Governing Question

Can an independent reviewer select any applicable requirement and reconstruct, without oral history, why it applies, what configuration and conditions it governs, how conformance was evaluated, what actually happened, which anomalies remain, who authorized the status, and what change would invalidate the result?

Requirement-based verification makes the contractual and engineering claim—not the test campaign—the unit of accountability. Campaigns, reports, simulations, and pipelines are evidence producers. A single activity may support many requirements; one requirement may require several activities. The relationship is many-to-many and must preserve the exact slice of data and reasoning used for each judgment.

## Why This Matters

Projects often possess thousands of passing tests yet cannot answer whether every requirement is satisfied. Tests cluster around easy functions, while interface, failure, environment, human, process, security, and lifecycle obligations remain implicit. Conversely, teams repeat expensive work because evidence cannot be traced to the requirement, configuration, and decision it supports.

NASA's current Requirements Verification Matrix guidance calls for each “shall” to have a unique identifier and definitive source. Product Verification guidance requires controlled requirements and product versions, methods, special equipment/conditions/procedures, recorded results, anomalies, corrective actions, and reports. Current NASA handbook/modeling guidance further treats verification statements, configurations, activities, cases, and artifacts as explicit relationships. This is stronger than a spreadsheet with a method letter.

Requirement-based organization exposes specification defects early. If a team cannot define an observable and success criterion, the requirement may be ambiguous, compound, infeasible, missing conditions, or expressed at the wrong level. Resolving that defect before realization avoids post hoc thresholds and disputes.

It also protects negative evidence. A summary “pass” can hide a failure followed by modification and retest, a waived nonconformance, invalid data, or a different build. Per-requirement closure preserves the chain so reviewers can assess correction, regression scope, residual risk, and evidence validity.

For continuous software and evolving systems, the record becomes an evidence graph. Requirement baselines, source rationale, implementation elements, automated/manual activities, environments, results, anomalies, and releases have immutable identities. Change impact traverses the graph to invalidate or rerun only what is affected—without treating unaffected evidence as disposable or affected evidence as eternally green.

## Prerequisites and Retrieval

Before closing a requirement, retrieve:

1. authoritative requirement ID, exact text, source document/paragraph, version, owner, rationale, criticality, allocation, applicability/tailoring, related needs/goals/hazards/regulations, and change history;
2. requirement quality/validation evidence: singularity, clarity, necessity, feasibility, conditions, units, tolerances, quantifiers, modes/states, statistical population, exceptions, traceability, and verifiability;
3. parent/child, sibling, interface, derived, hazard-control, regulatory, human, security, reliability, performance, data, and operational relationships;
4. verification statement with object, property, observable, method(s), level, article/pedigree, environment/conditions, margin, oracle, uncertainty, sampling, and limitations;
5. approved plan/procedure, preconditions, stimuli, sequence, instruments/tools/models/data, calibration/qualification, personnel, witnesses, safety/security controls, abort/recovery, and invalid-run rules;
6. exact product/build/configuration, dependencies, parameters, interfaces, data/model, hardware serial/lot, manufacturing state, documentation/procedure, external systems, and environment;
7. raw observations, logs, measurements, inspection records, analysis inputs/outputs, transformations, uncertainty, reviewer notes, signatures, timestamps, and immutable artifact locations/digests;
8. result against each clause/condition, pass/fail/inconclusive rationale, method limitations, untested space, and contradictory evidence;
9. discrepancies/nonconformances, cause, impact, corrective action, requirement/design/product/procedure/tool changes, regression, retest, waiver/deviation, residual risk, and authorized disposition;
10. closure reviewer/authority, independence, status/date, acceptance/certification linkage, conditions/expiry, open action ownership, and re-verification triggers;
11. evidence reuse/similarity basis, source configuration/requirement/environment, quality, anomalies, differences, credit scope, and residual work;
12. dashboard/matrix query proving no omitted applicable requirements, no orphan activities/evidence, no dangling superseded links, and no critical closure hidden by aggregation.

Use a **two-way closure walk**. Forward: source need/authority → requirement → allocation/design → verification statement → procedure/activity → raw evidence → finding → anomaly/disposition → closure. Backward: closure → exact evidence slice → activity/configuration → oracle → requirement version → source/rationale. Breaks mean the closure is not independently reconstructable.

## Learning Objectives

After completing this module, you should be able to:

1. make a requirement the unit of verification accountability;
2. distinguish requirement quality/validation, verification planning, execution, evidence, compliance, and acceptance;
3. construct verification statements from requirement semantics and system architecture;
4. design bidirectional traces that preserve versions, rationale, and evidence provenance;
5. handle compound, inherited, derived, parent/child, interface, cross-cutting, and statistical requirements;
6. distinguish coverage, readiness, execution, result, closure, waiver, and applicability;
7. build closure packages with raw evidence, uncertainty, discrepancies, corrective action, and authority;
8. aggregate lower-level evidence without assuming compositional closure;
9. govern evidence reuse and automated continuous verification across configuration change;
10. audit a baseline for omitted requirements, orphan evidence, invalid status, and critical closure risk.

## Core Exposition

**Establish the authoritative baseline.** Decide which repository/model/document owns requirement identity and text. Mirrors must carry source/version and synchronization controls. Unique IDs remain stable across editorial moves; substantive change creates traceable version/change history rather than silently rewriting old evidence.

**Determine applicability explicitly.** Evaluate system, subsystem, class, configuration, mission, contract, jurisdiction, and tailoring. Record applies/not applicable/partially applies with rationale and authorization. Delegated or supplier obligations remain visible to the owner.

**Validate before formal verification.** Ensure the requirement is necessary, correct, complete enough, feasible, singular, unambiguous, consistent, traceable, and verifiable. Verification cannot rescue a wrong baseline. If success criteria require inventing unstated conditions, return the requirement for controlled clarification.

**Parse requirement semantics.** Identify subject; mandatory action/property; trigger/preconditions; modes/states; input/load/environment; threshold/tolerance/units; time/duration; population/quantifier; exceptions; and prohibited behavior. Turn each into observable claims without weakening the obligation.

**Split compound obligations.** “The service shall authenticate users, respond within 200 ms, and retain records for seven years” contains three properties with different methods/levels. Split requirements or create governed subclaims that all must close. Never let one passing clause color the row green.

**Create a verification statement.** Name the configured object, requirement version, method(s), level, article, conditions, inputs, observable, oracle, uncertainty/statistics, procedure/evidence type, and limitations. Make it reviewable while architecture and requirements can change.

**Use architecture to choose level.** Verify a property where it exists and is observable. Component evidence can close local allocations. End-to-end latency, safety interaction, shared-resource capacity, human workflow, and interface semantics often require integrated evidence. Keep lower results for diagnosis and composition.

**Trace implementation without confusing it with evidence.** A requirement-to-design/code/component link shows realization intent. It does not demonstrate the built product conforms. Evidence needs executed inspection/analysis/demonstration/test and reviewed results.

**Build the evidence graph.** Link requirement source and version to verification statement, plan/procedure, activity instance, product/environment configuration, raw artifacts, analysis/report, discrepancy, corrective action, retest, finding, and closure. Use immutable identifiers/digests and access controls appropriate to consequence.

**Preserve many-to-many granularity.** If one test covers twenty requirements, retain the exact steps, measurements, conditions, and oracle supporting each. If one requirement uses analysis plus test, state how their evidence combines and whether either alone is sufficient.

**Handle parent and child requirements.** Children provide evidence only when allocation is complete and logically implies the parent under integration assumptions. Verify parent-specific conditions and emergence. A mass budget may aggregate measured child masses plus integration allowances; an end-to-end outcome rarely follows from independent functions alone.

**Handle derived requirements.** Trace each derived requirement to architecture, analysis, hazard control, interface, or design decision and upward to the source need it enables. Orphan derived requirements may constrain cost without rationale; missing derived requirements leave parent satisfaction unsupported.

**Handle interface requirements bilaterally.** Trace both providers/consumers and authoritative interface baseline. Verify syntax, units, coordinates, timing, sequences, states, errors, version negotiation, capacity, security, physical/electrical properties, human responsibilities, and change compatibility at appropriate levels.

**Handle statistical requirements literally.** “Reliability ≥0.99 with 95% confidence over mission time” needs population, mission definition, failures, censoring, independence, sample/test duration, model, priors if any, confidence rule, environment, and uncertainty. A handful of passes cannot close it.

**Retain process requirements.** Requirements may govern reviews, independence, records, configuration, safety/security process, supplier controls, or operations. Verify them through qualified records, audits, inspections, and objective evidence—not product functional tests. Do not confuse process compliance with product performance.

**Execute against frozen identities.** At activity start, capture requirement/product/procedure/environment/tool/model/data/instrument versions and deviations. If a requirement changes mid-run, preserve the result against the old version and assess credit to the new one.

**Separate data, finding, and status.** Raw result is what happened. Finding compares it with the oracle. Technical status records satisfied/failed/inconclusive. Disposition authorizes correction, waiver, retest, or other action. Acceptance/certification are further decisions. Keep them distinct.

**Close anomalies before green status.** Every discrepancy linked to a requirement needs causal and impact analysis, correction or authorized waiver, affected regression/retest, and reviewed closure. An “unrelated” anomaly requires evidence. Open severe anomalies prevent closure even when the nominal measurement passes.

**Treat waiver honestly.** Record failed requirement, actual result, consequence/risk, compensating controls, scope/configuration, operating limits, monitoring, authority, expiry/removal, and acceptance. Dashboard categories must not count waiver as technical pass.

**Audit coverage qualitatively.** Measure requirements with a credible planned path, ready path, executed evidence, adequate reviewed evidence, open anomalies, and closed status by criticality. Also find orphan activities/evidence and suspicious method uniformity. One 98% number is insufficient.

**Govern evidence reuse.** Compare requirement semantics/version, product configuration, article, environment, procedure, tools, data, evidence quality, anomalies, and intended credit. Reuse can be full, partial with analysis, or invalid. Preserve limitations and source provenance.

**Automate trace, not judgment theater.** Pipelines can generate versioned results and update status candidates. They cannot decide applicability, proxy validity, anomaly impact, waiver authority, or broad evidence sufficiency without governed logic/review. Quarantined critical tests remain gaps.

**Perform change impact in both directions.** Requirement change affects design, procedures, evidence, hazards, operations, and acceptance. Product/tool/environment change affects which requirements/evidence remain valid. Traverse dependencies, classify retained/invalidated/new evidence, and record the rationale.

The following fixture separates structural coverage from closure.

<!-- bijux-verify: {"id":"requirement-closure-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"requirements=6\nbidirectional_traces=6\nplanned_evidence_paths=6\npassed_results=5\nopen_anomalies=1\nclosed_requirements=5\nclosure_status=incomplete\nafter_disposition_closed=6\nfinal_status=complete_for_synthetic_baseline\nevidence=synthetic_matrix_structure_only\n","stderr":""}} -->
```python
rows = {
    f"REQ-{number:03d}": {
        "source": True,
        "backward_trace": True,
        "forward_trace": True,
        "method": True,
        "procedure": True,
        "evidence": True,
        "passed": number < 6,
        "open_anomaly": number == 6,
    }
    for number in range(1, 7)
}

traced = sum(row["source"] and row["backward_trace"] and row["forward_trace"]
             for row in rows.values())
planned = sum(row["method"] and row["procedure"] and row["evidence"]
              for row in rows.values())
closed = sum(row["passed"] and not row["open_anomaly"] for row in rows.values())
print(f"requirements={len(rows)}")
print(f"bidirectional_traces={traced}")
print(f"planned_evidence_paths={planned}")
print(f"passed_results={sum(row['passed'] for row in rows.values())}")
print(f"open_anomalies={sum(row['open_anomaly'] for row in rows.values())}")
print(f"closed_requirements={closed}")
print("closure_status=complete" if closed == len(rows) else "closure_status=incomplete")
rows["REQ-006"]["passed"] = True
rows["REQ-006"]["open_anomaly"] = False
closed = sum(row["passed"] and not row["open_anomaly"] for row in rows.values())
print(f"after_disposition_closed={closed}")
print("final_status=complete_for_synthetic_baseline")
print("evidence=synthetic_matrix_structure_only")
```

The final two field changes stand in for a real correction, configuration-controlled rerun, reviewed evidence, and anomaly disposition; they do not perform those acts. The fixture cannot establish requirement quality, evidence truth, method adequacy, or authorized closure.

## Definitions and Notation

Let $R_B$ be the applicable requirements in baseline $B$. Let evidence artifacts $e\in E$ and activities $a\in A$. Relations include source $T_s$, realization $T_i$, verification $T_v\subseteq R_B\times A\times E$, anomaly $T_a$, and decision $T_d$. Bidirectionality means each relation can be navigated and interpreted both ways; it does not mean every node has exactly one parent.

Define coverage indicators $p_r$ (credible planned path), $x_r$ (executed), $q_r$ (adequate reviewed evidence), and $c_r$ (authorized technical closure with anomalies resolved). Generally $c_r\Rightarrow q_r\Rightarrow x_r\Rightarrow p_r$, but the converses do not follow. A waiver may close an administrative action while $c_r$ as “satisfied” remains false; model statuses explicitly.

For a compound requirement with subclaims $r_1,\ldots,r_n$, satisfaction may require $\bigwedge_i c_{r_i}$ plus integration conditions. For a parent derived from children, the implication from child closure to parent closure must be justified; it is not a default theorem.

## Mechanisms, Invariants, or Proof Structure

A defensible closure follows this chain:

1. establish source, identity, applicability, rationale, and validated requirement semantics;
2. derive observable subclaims, success criteria, method, level, article, and conditions;
3. trace architecture/implementation and prepare controlled procedures/enabling products;
4. execute against frozen configurations and preserve raw evidence/provenance;
5. analyze uncertainty and compare every clause with its predeclared oracle;
6. record discrepancies, causes, impacts, corrections, waivers, regression, and retest;
7. review adequacy, contradictory evidence, limitations, and cross-level composition;
8. authorize an honest status and retain change/re-verification triggers.

The invariants are baseline identity, semantic equivalence between requirement and oracle, bidirectional provenance, evidence-before-closure, anomaly visibility, status separation, and limitation preservation under aggregation/reuse.

## Alternatives and Trade-Offs

**Matrix versus graph/model.** Matrices are reviewable snapshots; graphs/models represent many-to-many, versioned dependencies and impact. Use a controlled database/model for scale with generated human views, or a matrix for small systems. Avoid competing authorities.

**Requirement-centric versus scenario-centric execution.** Requirement-centric mapping proves atomic conformance; scenarios expose interactions and mission threads. Link scenario evidence back to every credited requirement and retain separate validation meaning.

**Atomic versus grouped closure.** Atomic closure is auditable but administratively heavy. Group closure is efficient for identical criteria/configuration/evidence, but must enumerate membership and preserve clause-specific failures/limitations. Never group merely to make dashboards green.

**Lower-level versus system-level evidence.** Lower levels improve controllability and diagnosis; system level captures interfaces/emergence. Compose only with allocation and integration arguments.

**Manual versus automated trace.** Manual curation applies judgment but drifts at scale. Automated relationships/diffs improve consistency but propagate wrong identifiers/semantics quickly. Use schema validation plus accountable review.

**Pass/fail versus richer states.** Binary displays are simple but erase inconclusive, waived, not applicable, superseded, and open-anomaly states. Preserve rich technical states and derive executive views without losing truth.

**New versus reused evidence.** Reuse reduces cost/schedule and avoids destructive repetition. New work is needed where semantics, configuration, environment, quality, or consequence changed. Make credit per claim.

## Failure Modes and Misconceptions

**“Every row has T, so coverage is complete.”** A method letter lacks conditions, level, article, oracle, procedure, and evidence path.

**“The test passed, so linked requirements pass.”** Each requirement needs the relevant result slice and oracle; a campaign's overall success is not per-row evidence.

**“All children pass, so the parent passes.”** Only if allocation is complete and the implication including integration/emergence is demonstrated.

**“The requirement changed editorially.”** Even editorial change needs controlled comparison; semantic change invalidates or narrows prior evidence.

**“Not applicable means hard to verify.”** Applicability derives from authority/system scope. Difficulty is planning risk, not tailoring rationale.

**“Waived equals compliant.”** Waiver is authorized relief from nonconformance under conditions, not satisfaction.

**“Objective evidence is any artifact.”** An artifact must be relevant, authentic, configuration-bound, interpretable, and adequate for the claim.

**“Traceability proves correctness.”** Trace links prove relationships exist, not that requirements are right or evidence adequate.

**“Coverage percentage measures readiness.”** Planned links may be infeasible; executed data may be invalid; critical anomalies may remain.

**“Automation owns closure.”** Automation produces evidence and candidate findings; governed roles own applicability, anomaly impact, waiver, and closure authority.

## Worked Examples

### Example 1

**Situation.** Requirement R-17 says “The unit shall be lightweight, rugged, and easy to carry.”

**Reasoning.** It is compound and subjective. Retrieve source need; define mass limit/condition, ruggedness environments/performance, and carry task/population. Split into singular requirements with units, conditions, oracles, and validation. Do not create arbitrary tests after build.

**Conclusion.** Requirement-based verification begins by rejecting an unverifiable requirement, not manufacturing a green result.

### Example 2

**Situation.** One test measures 180 ms response and is linked to requirements for 200 ms normal mode and 500 ms degraded mode.

**Reasoning.** Identify test mode/configuration/load. If only normal mode ran, it can support the first requirement under its conditions, not degraded mode. Create a separate degraded activity or justified evidence slice; retain distinct oracles.

**Conclusion.** One result can support multiple requirements only when each requirement's conditions were actually covered.

### Example 3

**Situation.** Three subsystem mass requirements pass, and the system mass parent is marked passed.

**Reasoning.** Sum controlled measured masses, integration hardware, harnesses, consumables, payload, software-independent items, growth/uncertainty per rule, and exact system configuration. Check allocations are exhaustive and parent conditions match. Otherwise child closure is insufficient.

**Conclusion.** Parent closure requires an explicit aggregation and completeness argument.

### Example 4

**Situation.** A supplier certificate is linked as evidence for a pressure requirement.

**Reasoning.** Check requirement/standard, part/lot/revision, sample, environment, calibration, procedure, results, anomalies, authority, and integration conditions. The certificate may support material/process or part qualification, while owner interface/system evidence remains.

**Conclusion.** A linked document becomes creditable only after provenance and semantic relevance are established.

### Example 5

**Situation.** R-42 passes, but its test showed an unrelated reboot anomaly.

**Reasoning.** “Unrelated” requires causal/impact analysis. The reboot may invalidate duration, state, data, or other requirements. Preserve run, link anomaly to affected graph, correct/disposition, perform regression/retest, and close only when evidence remains adequate.

**Conclusion.** Nominal metric pass does not override an unresolved anomaly in the evidence event.

### Example 6

**Situation.** A requirement is relaxed from 100 ms to 150 ms after a 130 ms result.

**Reasoning.** Preserve failure against old baseline; control rationale and stakeholder/hazard/interface impact of the change; validate the new requirement; assess design/operations; then credit the old measurement only if configuration, conditions, procedure, and evidence meet the new claim. Avoid result-driven threshold manipulation.

**Conclusion.** A controlled requirement change can enable new closure, but it cannot rewrite historical evidence or skip validation.

### Example 7

**Situation.** Reliability shall be at least 0.99; ten missions pass.

**Reasoning.** Define mission duration/profile, failure, population, environment, independence, censoring, confidence requirement, model and sample plan. Ten successes alone do not establish 0.99 at conventional high confidence. Use justified demonstration/analysis and report bounds.

**Conclusion.** Literal quantifiers and statistical confidence govern closure, not intuitive success counts.

### Example 8

**Situation.** A safety control is implemented in code and unit-tested, so the system hazard-control requirement is closed.

**Reasoning.** Trace control through sensors, assumptions, timing, interfaces, deployment configuration, authority, failure/common cause, human action, physical effect, monitoring, and integrated scenarios. Unit evidence is necessary for software allocation, not sufficient for system control effectiveness.

**Conclusion.** Cross-cutting hazard requirements close at the level where the controlled outcome exists.

### Example 9

**Situation.** Automated tests pass on build 8, but release candidate uses build 9 with a dependency update.

**Reasoning.** Evidence stays attached to build 8. Traverse changed dependency to requirements/tests/hazards, determine unaffected/targeted/full regression, execute on build 9, and preserve credit rationale. Similar names do not establish configuration identity.

**Conclusion.** Green evidence does not float across builds without change impact and configuration-bound rerun/credit.

### Example 10

**Situation.** A dashboard reports 99% closed: 990 low-criticality requirements pass; all ten safety requirements are inconclusive.

**Reasoning.** Aggregate percentage is actively misleading. Report criticality-weighted counts without treating weights as compensation, list blockers, decision impact, owners, evidence gaps, and risk authority. The system is not verification-complete for safety-relevant release.

**Conclusion.** Coverage metrics must expose critical closure, not average it away.

## Cross-Program Connections

- **API/service engineering:** requirements map to contracts, timing, errors, compatibility, security, availability, recovery, and consumer evidence across versions.
- **Platform engineering:** policy-as-code and pipelines generate configuration-bound evidence, but platform/user outcome requirements still need integrated claims.
- **Data engineering:** lineage, schemas, freshness, quality, reconciliation, retention, and privacy need versioned data/evidence traces.
- **Object-oriented programming:** class/unit tests map to local contracts; system requirements require collaboration, substitutability, and integration arguments.
- **Functional programming:** types, proofs, properties, and deterministic tests strengthen requirement evidence within explicit assumptions/effects.
- **Safety/security:** hazards, threats, controls, assumptions, independence, negative evidence, and residual risk create cross-cutting verification obligations.
- **Models/simulation:** analytical evidence needs model implementation verification and validation for the requirement's use/domain.
- **Configuration/data management:** immutable identities, provenance, baselines, and impact graphs make closure reconstructable.
- **Quality/assurance:** audits and process evidence verify applicable process requirements without substituting for product outcomes.
- **Acceptance/certification:** these authorities consume requirement closure packages while retaining distinct decision scopes.

## References

1. NASA, [Requirements Verification Matrix, Systems Engineering Handbook Appendix D](https://www.nasa.gov/reference/appendix-d-requirements-verification-matrix/), updated 2023.
2. NASA, [How to Write a Good Requirement, Systems Engineering Handbook Appendix C](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/), accessed 2026-08-31.
3. NASA, [Product Verification, Systems Engineering Handbook section 5.3](https://www.nasa.gov/reference/5-3-product-verification/), updated 2023.
4. NASA Safety and Mission Assurance, [Identifying Objective Evidence Improves Requirement Implementation](https://sma.nasa.gov/news/articles/newsitem/2026/03/25/identifying-objective-evidence-improves-requirement-implementation), 2026.
5. NASA, [NPR 7123.1C, NASA Systems Engineering Processes and Requirements, Change 2](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001C_&page_name=all), accessed 2026-08-31.
6. NASA, [NASA-HDBK-1009A: Systems Modeling Handbook for Systems Engineering](https://standards.nasa.gov/system/files/tmp/2025-03-12-NASA-HDBK-1009A.pdf), 2025.
7. NASA, [NASA-HDBK-4008 with Change 2](https://standards.nasa.gov/system/files/tmp/NASA-HDBK4008%20w%20-Change%202.pdf), 2024.
8. NASA, [Requirement Assurance Process](https://ntrs.nasa.gov/api/citations/20110014948/downloads/20110014948.pdf), 2011.
9. Federal Aviation Administration, [Acquisition Management System Lifecycle Verification and Validation Guidelines, Version 3.0](https://www.faa.gov/sites/faa.gov/files/2022-02/vandvguidelines.pdf), 2017.
10. NASA, [NASA Systems Engineering Handbook, NASA/SP-2016-6105 Rev. 2](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf), 2016.

## Exercises

### Exercise 1

Rewrite and plan verification for: “The platform shall be secure, fast, reliable, and easy to recover.” Identify source questions, singular requirements, conditions, metrics, methods, levels, and evidence limitations.

### Exercise 2

A matrix has 200 applicable requirements: 200 methods assigned, 190 procedures ready, 170 activities executed, 160 results passed, 8 failed, 2 inconclusive, and 12 executions awaiting review; three passed results have open critical anomalies. Build an honest status view without double counting.

### Exercise 3

Construct a closure package for a requirement that a service retain an auditable, immutable record of every privileged configuration change for seven years. Address semantics, identities, failure paths, time, storage, access, evidence, and operational change.

### Exercise 4

Decide whether four component requirements can close a parent end-to-end emergency-notification requirement. Components separately verify detection, message generation, network delivery, and display. State the missing composition evidence.

### Exercise 5

Design a requirement/evidence graph and change-impact workflow for a continuous delivery system with weekly builds, supplier dependencies, hazard controls, automated/manual verification, waivers, and periodic certification review.

## Answers to the Exercises

### Answer 1

The statement is compound and undefined. Retrieve threat model/assets/authority for “secure,” workload and response boundary for “fast,” mission/failure/environment/confidence for “reliable,” and recovery outcomes/RTO/RPO/integrity/roles for “easy.” Split, for example: authenticated/authorized privileged operations with specified prohibited paths; 99.9th-percentile end-to-end latency under declared workload; mission success/reliability with stated probability/confidence and interval; and restoration/reconciliation within RTO/RPO after named failures by representative operators.

Trace each to stakeholder, hazard/threat, ConOps, architecture, and interfaces. Use inspection/formal/static/adversarial/integration evidence for security; instrumented system test/statistical analysis for latency; reliability analysis plus appropriately designed demonstrations/field evidence; and fault-injection/recovery tests plus human demonstration/validation. Define configurations, environments, oracles, uncertainty, negative cases, anomalies, and evidence limits. Validation remains necessary because measurable replacements can still misrepresent the stakeholder need.

### Answer 2

Report states as a pipeline, not additive percentages. All 200 have planned method coverage; 190 are procedure-ready and 10 are not ready. Of 170 executed, 160 nominally passed, 8 failed, and 2 inconclusive. The remaining 30 are unexecuted, including at least the 10 without ready procedures. Twelve of the 160 nominal passes await review, so at most 148 have reviewed pass candidates. Three of those passed results have open critical anomalies; if included among the reviewed 148, at most 145 are technically closable as satisfied. If their review membership is unknown, report a range and resolve identity rather than assuming.

Failures and inconclusive results are separate; awaiting-review results are not closed. Show waiver/deviation and not-applicable separately if any. Break all categories down by criticality and list the three critical blockers. Do not claim 80% complete from 160/200 or count method assignment as compliance. Query exact row identities to eliminate overlap and compute authoritative closed status.

### Answer 3

Define privileged change, configuration object, actor/service identity, request/approval, before/after value, timestamp/time source, reason/ticket, source interface, success/failure, transaction/order, cryptographic integrity/immutability meaning, retention start, deletion, access, jurisdiction, and seven-year availability. Split functional capture, completeness, integrity, ordering/time, authorization, confidentiality, retention, retrieval, backup/recovery, and disposal requirements as needed.

Inspect schemas, policies, roles, retention and immutable-store configuration; analyze cryptographic/key/time and storage/retention architecture; test every privileged path including API/UI/automation/emergency/break-glass, denied/failed/partial changes, concurrency, clock skew, outage, full storage, tampering, restore, migration, key rotation, and seven-year equivalence via lifecycle/accelerated evidence; verify monitoring and reconciliation. Evidence binds build, infrastructure, schema, keys/policies, datasets, procedure, raw records, anomalies, and results. Long-term closure needs periodic operational monitoring, restore/audit exercises, supplier/configuration change triggers, and preserved migration provenance; a short test alone cannot prove seven future years.

### Answer 4

Component passes are necessary but not sufficient. The parent requires an end-to-end causal thread: detection signal semantics and timing; message identity/content/priority; routing/addressing; network latency/loss/duplicate/reorder/retry; display availability and cueing; acknowledgments/escalation; clocks; security/authority; external dependencies; common causes; overload; degraded modes; operator recognition/action; and the total deadline/reliability under the parent environment.

Verify interface contracts bilaterally and run production-representative integrated scenarios across boundaries, failures, timing corners, demand, and recovery with synchronized measurement. Analyze coverage and common causes; trace every component result and integration assumption. If the parent is about intended emergency outcome, separate system validation with representative users/operations is also needed. Close the parent only when allocation completeness plus integrated/emergent evidence implies its full conditions.

### Answer 5

Nodes include source needs/hazards/regulations; versioned requirements and subclaims; architecture/design/code/configuration/dependencies; verification statements; procedures/cases; environments/tools/data; activity instances; immutable raw/processed artifacts; findings; anomalies/corrections/regression; waivers with authority/expiry; release/builds; and certification claims/reviews. Typed bidirectional edges record source, derives, allocates, implements, verifies, produced, contradicts, corrects, waives, included-in, and depends-on relationships.

Each build freezes an SBOM/dependency, infrastructure/policy, data/model, flag, procedure/tool/environment, and requirement baseline. A diff traverses outward to impacted requirements, hazards, methods, evidence, waivers, and certification claims. Classify prior evidence retained, reusable with analysis, invalidated, or newly required; run mandatory critical regression plus targeted work. Automated results become immutable evidence candidates, while human review closes high-consequence claims and anomalies. Flaky/quarantined critical activities remain open.

Supplier changes trigger provenance/similarity and owner integration evidence. Waivers retain nonconformance, scope, conditions, monitor, expiry, and removal. Periodic certification review consumes exact release closure packages and open limitations. Operational incidents, drift, new threats, requirement or environment changes traverse back into impact and re-verification. Dashboards derive from the graph but never collapse failed, inconclusive, waived, unreviewed, or open-critical states into green.
