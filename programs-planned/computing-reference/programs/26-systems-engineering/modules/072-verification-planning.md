---
module_id: SYSENG-072
program: Systems Engineering
level: 2
module_number: 72
title: Verification Planning
status: complete
last_verified: 2026-08-31
---

# Verification Planning

## One-Page Review

### Governing question

How will every applicable specified requirement be converted early enough into feasible, configuration-bound, resource-backed, reviewable objective evidence, with dependencies, risks, anomalies, and closure decisions visible before commitment makes correction prohibitively expensive?

### Essential definitions

- A **verification plan** defines scope, baselines, organization, methods, levels, articles, environments, facilities, procedures, resources, schedule, evidence, anomaly handling, and completion governance for demonstrating conformance to specified requirements.
- A **verification strategy** explains the governing logic: what is verified where and when, why each method/level is credible, how evidence composes, and how risk drives depth. A calendar and test list are not a strategy.
- A **verification cross-reference matrix (VCRM/RVM)** traces each requirement to method, level, article, configuration, environment, procedure, result, evidence, anomaly, and status. It is a controlled decision view, not a completeness proof.
- **Method** identifies how evidence is obtained: analysis, inspection, demonstration, or test. **Level** identifies the system hierarchy/integration state at which the claim is evaluated.
- A **verification article** is the configured object used: model, prototype, engineering unit, qualification unit, production representative, delivered item, software build, interface emulator, or other declared pedigree.
- An **enabling product** is equipment, software, data, facility, fixture, simulator, instrumentation, procedure, trained person, or external service needed to generate credible evidence.
- **Qualification** demonstrates design capability under specified conditions; **acceptance** checks delivered items and workmanship/required function under defined criteria. Their evidence and articles are not automatically interchangeable.
- A **verification closure criterion** states what evidence, review, anomaly disposition, configuration match, and authorization are required before a requirement is declared satisfied, failed, waived, or inconclusive.
- **Verification credit** is authorized reuse or composition of existing evidence after relevance, configuration, assumptions, quality, and limitations are assessed.
- **Test readiness** is the evidence-backed judgment that objectives, baselines, article, environment, facility, instrumentation, procedure, personnel, safety controls, data handling, and anomaly processes can support the planned claim.

### Central model, mechanism, or theorem

For every requirement $r$, build a verification claim record

$$
V_r=(B_r,M_r,L_r,A_r,C_r,P_r,O_r,E_r,D_r),
$$

where $B$ is the requirement/configuration baseline, $M$ method, $L$ level, $A$ article/pedigree, $C$ conditions/environment, $P$ procedure and prerequisites, $O$ oracle/acceptance rule, $E$ evidence record, and $D$ disposition including anomalies. Planning is complete only when these records compose into an executable dependency/resource schedule and every high-consequence claim has a credible inference path. A filled matrix with impossible facilities, unavailable articles, invalid assumptions, or circular evidence is not a plan.

### Critical invariants

- Start planning while requirements and architecture are still changeable; verification is designed with the system.
- Every applicable requirement has at least one adequate evidence path, and every planned activity traces to a requirement, interface, risk, or justified learning objective.
- Method, level, article, environment, and oracle are selected together; none is credible in isolation.
- Requirement and product configurations, procedures, tools, models, data, instrumentation, and results remain version-bound.
- Lower-level evidence is credited upward only when allocation, interfaces, integration, emergence, assumptions, and configuration justify composition.
- Test is not the default. Use the least hazardous and resource-intensive method that produces adequate evidence; use multiple methods when consequence or inference demands corroboration.
- Qualification, verification, validation, acceptance, certification, developmental evaluation, and regression retain distinct purposes and credit rules.
- Resources include people, competence, training, facilities, logistics, spares, data, external systems, calibration, analysis time, anomaly capacity, and rework margin—not only test execution hours.
- Schedule follows integration and evidence dependencies, including review, data reduction, anomaly resolution, corrective action, and retest.
- Human, software, hardware, data, physical, cyber, interface, degraded, maintenance, and recovery requirements receive appropriate evidence.
- Deviations and waivers preserve technical nonconformance; authority cannot rewrite an observed failure as a pass.
- Change impact analysis determines selective re-verification and invalidated credit.

### Common failures

Common failures include writing the plan after design freeze; mapping every requirement to “test”; copying methods from a predecessor; using “analysis” without a model, inputs, uncertainty, or oracle; assigning verification above the level where the state is observable; relying on component evidence for emergent behavior; omitting external interfaces, people, software/data, fault modes, maintenance, and recovery; planning facilities after schedules are committed; ignoring test-article pedigree; double-booking scarce equipment; assuming simulators need no credibility evidence; counting execution but not analysis/anomaly/retest time; measuring percent complete rather than critical closure; merging qualification and acceptance credit without rationale; using ambiguous pass criteria; allowing verification to create uncontrolled configuration; and postponing impossible requirements until formal test.

### Compact example

Five synthetic requirements are planned across inspection, analysis, demonstration, and test. The draft plan initially has one requirement without an oracle and another requiring an unavailable chamber. Its nominal row coverage is 100%, but executable readiness is only three of five. After defining the safety-shutdown decision rule and reserving the chamber, readiness becomes five of five. The example proves only that structural fields and resource dependencies are present; it does not prove method adequacy or requirement satisfaction.

### Connections

Requirements engineering makes claims measurable; architecture exposes verification points; integration order determines evidence availability; safety/reliability/security determine rigor; configuration and data management preserve meaning; project planning supplies resources; validation and acceptance consume but do not replace verification evidence.

## Governing Question

Can the project explain, before formal execution, how each configured requirement will be judged by adequate objective evidence on a suitable article at the correct integration level and conditions, with a feasible resource/dependency schedule, controlled anomalies, and an authorized closure path?

Planning is the engineering of evidence production. It transforms “shall” statements into observable claims, exposes unverifiable requirements and architectures, defines enabling systems, sequences integration, and protects scarce facilities and articles. A document can be comprehensive yet nonexecutable. The real plan is the consistent network linking baselines, claims, methods, configuration, resources, schedule, risks, evidence, and decisions.

## Why This Matters

Verification cost and feasibility are largely designed into requirements and architecture. A tolerance tighter than available instrumentation, an internal state hidden after assembly, a destructive test assigned to a unique production item, or an end-to-end requirement dependent on an unavailable external system can make late verification unsafe, expensive, or impossible. Early planning feeds these discoveries back while design alternatives remain.

NASA's current technical-planning guidance explicitly connects method selection to lifecycle timing, product position in the system structure, product form, and cost. Its V&V plan outline covers responsibility/change authority, requirements flowdown, architecture, methods, test articles, support equipment, facilities, integration, matrices, certification, and acceptance. Product-verification guidance adds procedures, controlled requirements/configuration, enabling products, trained personnel, calibrated equipment, environments, discrepancy handling, reports, and closure.

A strong plan also protects inference. One passing component test cannot establish system timing if networks, scheduling, operators, and external services determine the requirement. A high-fidelity system test may be unnecessary for a directly inspectable material marking. Planning decides where evidence is most observable and representative, then determines what integration-level work remains.

Software-intensive systems complicate the schedule: builds change faster than physical campaigns; test data and infrastructure are configuration; external dependencies drift; security evidence may require adversarial work; nondeterminism demands statistical rules; feature flags create many products. Continuous automation helps regression but does not eliminate formal baselines, environment fidelity, independent review, or closure authority.

Verification work competes for scarce articles, chambers, ranges, rigs, networks, datasets, specialists, operator time, and anomaly boards. A resource-loaded dependency network reveals collisions and critical paths that a requirements matrix cannot. The schedule must include preparation, readiness, setup, calibration, execution, teardown, data reduction, analysis, report, discrepancy resolution, correction, regression, and retest.

## Prerequisites and Retrieval

Before baselining a verification plan, retrieve:

1. governing lifecycle, standards, regulation/certification basis, tailoring, definitions, contractual obligations, technical authority, approval/change authority, and independence requirements;
2. stakeholder/system/allocated requirements and interfaces with identifiers, rationale, sources, criticality, tolerances, modes, environments, applicability, verification success criteria, and controlled versions;
3. system boundary, architecture, hierarchy, functions, states/modes, interfaces, human allocations, data/control flows, hazards, threats, failure/degraded/recovery behavior, and external dependencies;
4. integration strategy/order, builds/releases, manufacturing/assembly, supplier deliveries, interface availability, configuration baselines, and transition/operational dates;
5. proposed method and level per requirement, observables, inputs, conditions, margins, uncertainty, oracle, sampling/confidence, analysis/model assumptions, and corroboration needs;
6. article definitions/pedigree, quantities, representativeness, allowed modification, destructive/non-destructive use, refurbishment, production equivalence, software/data/configuration identity, and custody;
7. enabling products: facilities, fixtures, support equipment, simulators/emulators/stubs, instrumentation, calibration, networks, test software, datasets, credentials, time sources, external services, and clean-up;
8. procedures, readiness/entrance/abort/exit criteria, pre/post conditions, safety/security controls, personnel, training/certification, roles, witnesses, independence, and communications;
9. schedule/resource data: availability windows, lead times, permits, logistics, consumables, staff skills, shifts, analysis/report capacity, contingency, anomaly/rework/retest reserve, cost, and competing demand;
10. evidence management: raw data formats, provenance, metadata, logs, chain of custody, transformations, retention, access, tool/model versions, review, report, repository, and trace links;
11. discrepancy/nonconformance process, severity, stop-work authority, triage, root cause, impact, corrective action, waiver/deviation, regression, retest, closure, and escalation;
12. heritage/COTS/supplier evidence, similarity arguments, prior anomalies, limitations, configuration/use differences, acceptance/certification records, field data, and change triggers.

Perform a **forward feasibility walk** from each critical requirement to observable, method, level, article, environment, facility, procedure, data, oracle, review, and closure. Perform a **backward resource walk** from every scarce facility/article/specialist date through prerequisites and configuration maturity. If either walk breaks, the plan is aspirational.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish verification strategy, plan, matrix, procedure, report, qualification, acceptance, and validation;
2. derive verification claims from controlled requirements and architecture;
3. select method, level, article, conditions, and oracle as one inference design;
4. allocate evidence across hierarchy and integration without invalid compositional claims;
5. plan representative environments, enabling products, people, data, and model credibility;
6. build resource-loaded schedules with readiness, analysis, anomaly, regression, and retest work;
7. define completion, waiver/deviation, inconclusive, and re-verification governance;
8. evaluate heritage, similarity, COTS, supplier, and automated evidence credit;
9. expose verification risk using feasibility, criticality, dependency, and evidence-quality views;
10. maintain a living, configuration-controlled verification basis through change and operation.

## Core Exposition

**Define scope and authority.** State which system/product layers, configurations, lifecycle decisions, requirements, interfaces, and organizations the plan covers. Identify owner, approver, change board, technical authority, witnesses, independent roles, acceptance/certification interfaces, and document precedence.

**Describe the verification architecture.** Show how requirement allocation, product hierarchy, integration, builds, suppliers, and operational deployment connect to evidence levels. Verification architecture answers where a property becomes observable and what lower evidence is necessary but insufficient.

**Plan from requirements, not test ideas.** For each applicable requirement, identify subject, condition, required behavior/limit, measurement, uncertainty, and pass rule. If the requirement cannot yield a credible oracle, feed back a change rather than invent one in a procedure.

**Assign method by inference.** Inspection is efficient for observable static attributes; analysis covers derived behavior and inaccessible/extreme domains if models are credible; demonstration shows operation without detailed quantitative measurement; test stimulates an article and records detailed data. Combine methods when analysis needs test correlation or consequence warrants independent evidence.

**Choose the level.** Verify at the lowest level where the property is fully meaningful, controllable, and observable—then retain higher-level work for interfaces/emergence. Material strength can be verified below system level; end-to-end latency, workload, safety interaction, and mission threads often cannot.

**Define article and pedigree.** State whether evidence comes from prototype, engineering, qualification, protoflight, production, acceptance, digital, simulated, or operational form. Explain differences from delivered configuration and how they affect credit. Protect scarce/destructively tested articles and plan equivalence evidence.

**Specify conditions.** Cover modes, state, loads, duty cycle, physical environment, interfaces, data, clocks, networks, people, maintenance, failure/degraded/recovery states, tolerances, margins, and preconditioning. Requirements often apply at combinations, not independent extremes; plan interaction coverage.

**Define oracles and uncertainty.** Establish pass, fail, and inconclusive rules before execution. Include measurement uncertainty, calibration, sampling, confidence, numerical tolerance, data exclusion, missing data, statistical stopping, and decision authority. Guard bands may be needed when uncertainty approaches tolerance.

**Plan enabling products as products.** Fixtures, simulators, emulators, test software, data generators, instrumentation, and analysis tools have requirements, configurations, verification, validation-for-use, maintenance, cybersecurity, and readiness. A faulty harness can invalidate an otherwise perfect test.

**Plan human participation.** Name qualifications, training, staffing, shifts, independence, safety roles, operator/maintainer representation, witness needs, workload, access, and communication. Avoid making success depend on undocumented expert intervention.

**Design integration-aware evidence.** Align verification with interface availability and integration sequence. Use contract tests, emulators, hardware/software-in-loop, and progressive assemblies, then retire assumptions with real partners. Plan data continuity so early evidence remains traceable.

**Plan risk-first.** Prioritize high-consequence, high-uncertainty, novel, difficult-to-observe, facility-constrained, long-lead, destructive, supplier-dependent, and integration-heavy claims. Early developmental evaluations reduce risk; formal verification records compliance after configuration maturity.

**Separate developmental and formal work.** Exploratory tests, prototypes, peer reviews, and fault injection find problems. Formal verification follows controlled plans/procedures and produces disposition evidence. Developmental data may receive formal credit only through predeclared or reviewed pedigree/quality rationale.

**Resource the whole loop.** Estimate plan/procedure writing, reviews, model/tool development, fixtures, article preparation, logistics, permits, calibration, execution, data reduction, uncertainty analysis, report, anomaly board, correction, regression, retest, evidence archival, and independent review. Reserve time by risk rather than one generic percentage.

**Build dependency and resource schedules.** Activities depend on requirement maturity, design/configuration, article, integration, facility, support equipment, staff, external systems, and approved procedure. Model scarce resources and alternative windows. Maintain critical-path and risk views, not only dates.

**Establish readiness gates.** A Test Readiness Review or equivalent checks objective, baseline, article, environment, interfaces, procedure, instrumentation/calibration, data, staff/training, hazards/controls, configuration, prerequisites, anomaly process, abort/recovery, and schedule. Tailor rigor to consequence; do not turn the checklist into ceremonial approval.

**Plan evidence management.** Give each result immutable identity and trace to requirement, procedure, configuration, environment, tool/instrument, raw data, transformation, analyst/reviewer, anomaly, and decision. Store actual observations separately from interpretations and dispositions.

**Plan discrepancy handling.** Define who stops work, preserves state, declares invalid runs, classifies product/procedure/facility/tool/data problems, performs causal/impact analysis, approves correction, updates baselines, authorizes retest, and closes. Preserve failed runs and avoid “test error” without evidence.

**Define closure.** Requirement status can include planned, ready, executed, passed, failed, inconclusive, waived/deviated, superseded, and not applicable with rationale. Closure requires evidence adequacy, configuration match, anomaly disposition, review, trace completeness, and correct authority—not merely a green row.

**Govern evidence credit.** For heritage, similarity, supplier, COTS, model, and lower-level evidence, compare requirement, configuration, environment, use, interfaces, process, data quality, independence, and anomalies. Record credit scope and residual work. Certification or supplier claims do not automatically satisfy owner requirements.

**Plan regression and change.** Map requirement/design/interface/tool/environment changes to evidence dependencies. Define selective regression logic, mandatory safety/security sets, baseline diffs, trigger thresholds, and approval. A tiny code change can affect large behavioral evidence; a documentation correction may not.

**Use automation without losing governance.** Automated pipelines provide repeatable fast evidence when environment, data, dependencies, seeds, tools, oracles, reports, and retention are controlled. Flaky tests, mutable infrastructure, hidden retries, and overwritten results destroy confidence. Formal closure still needs traceable review and anomaly disposition.

**Maintain rolling forecasts.** Report critical requirements without credible paths, readiness blockers, facility/article conflicts, evidence age, open severe anomalies, retest load, assumption retirement, and schedule confidence. Percent executed can rise while the hardest claims remain untouched.

The following fixture checks a synthetic plan for structural readiness.

<!-- bijux-verify: {"id":"verification-plan-readiness-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"requirements=5\nrows_mapped=5\nmethods=analysis,demonstration,inspection,test\ninitial_ready=3\ninitial_blockers=REQ-004:missing_oracle,REQ-005:facility_unavailable\nrevised_ready=5\nrevised_blockers=none\nstatus=declared_verification_plan_fixture_consistent\nevidence=synthetic_structural_readiness_only\n","stderr":""}} -->
```python
rows = {
    "REQ-001": {"method": "inspection", "oracle": True, "article": True, "facility": True},
    "REQ-002": {"method": "analysis", "oracle": True, "article": True, "facility": True},
    "REQ-003": {"method": "test", "oracle": True, "article": True, "facility": True},
    "REQ-004": {"method": "demonstration", "oracle": False, "article": True, "facility": True},
    "REQ-005": {"method": "test", "oracle": True, "article": True, "facility": False},
}

def blockers(plan):
    result = []
    for requirement, row in plan.items():
        for field in ("oracle", "article", "facility"):
            if not row[field]:
                label = "facility_unavailable" if field == "facility" else f"missing_{field}"
                result.append(f"{requirement}:{label}")
    return result

initial = blockers(rows)
print(f"requirements={len(rows)}")
print(f"rows_mapped={len(rows)}")
print("methods=" + ",".join(sorted({row["method"] for row in rows.values()})))
print(f"initial_ready={len(rows) - len({item.split(':')[0] for item in initial})}")
print("initial_blockers=" + ",".join(initial))
rows["REQ-004"]["oracle"] = True
rows["REQ-005"]["facility"] = True
revised = blockers(rows)
print(f"revised_ready={len(rows) - len({item.split(':')[0] for item in revised})}")
print("revised_blockers=" + (",".join(revised) if revised else "none"))
print("status=declared_verification_plan_fixture_consistent")
print("evidence=synthetic_structural_readiness_only")
```

This fixture treats all fields as booleans and does not assess requirement quality, method adequacy, configuration, environment, resource capacity, schedule, uncertainty, evidence, or technical correctness. Structural readiness is necessary, not sufficient.

## Definitions and Notation

Let requirements $r\in R$ be controlled claims. Let activities $a\in A$ generate evidence, with trace relation $T\subseteq R\times A$. Each activity has method $m(a)$, level $l(a)$, article $q(a)$, conditions $c(a)$, resource vector $u(a)$, duration $d(a)$, predecessors $pred(a)$, oracle $o(a)$, and risk/criticality $k(a)$.

A row is **mapped** when it names an activity; **feasible** when prerequisites/resources can exist; **ready** when current entrance criteria are satisfied; **executed** when the controlled activity ran; and **closed** when adequate reviewed evidence and anomaly disposition support an authorized technical status. These states must not be collapsed.

Let evidence credit from activity $a$ to requirement $r$ be conditional $credit(r,a\mid B,C,H)$ on baseline/configuration $B$, conditions $C$, and inference/heritage rationale $H$. Credit is not transitive by default. If a component passed, its assembly and system implications still require explicit architectural reasoning.

## Mechanisms, Invariants, or Proof Structure

A credible plan follows this chain:

1. control requirement applicability, criticality, conditions, and success criteria;
2. identify where the property is meaningful and observable in the system hierarchy;
3. select method(s), level, article, environment, and oracle with an inference rationale;
4. specify enabling products, people, procedures, data, controls, and evidence metadata;
5. connect activities through integration, configuration, facility, resource, and review dependencies;
6. challenge feasibility, representativeness, uncertainty, hazards, common causes, and invalid assumptions;
7. baseline readiness, execution, anomaly, retest, report, credit, and closure governance;
8. maintain traces and forecasts through change until every applicable requirement has an honest status.

Key invariants are coverage without orphan requirements or unjustified activities; configuration identity from baseline to evidence; conservation of limitations when evidence is composed/reused; and separation of mapped, ready, executed, and closed. Schedule compression cannot remove these logical states; it can only overlap work when dependencies and risk allow.

## Alternatives and Trade-Offs

**Centralized versus distributed planning.** A central team improves consistency and resource coordination; product teams understand detail. Use governed common fields/authority with distributed authorship and integrated system ownership.

**Document versus model/database.** Documents support review and contracts; structured repositories support scale, trace queries, change impact, and automation. A hybrid can baseline human-readable decisions while keeping authoritative structured links. Avoid duplicate unsynchronized truth.

**Early low-fidelity versus late high-fidelity evidence.** Early evidence reduces design risk; late evidence matches delivery. Predeclare credit and assumption-retirement rules so prototypes help without being mistaken for production proof.

**Analysis versus test.** Analysis spans conditions cheaply and safely but depends on models/data. Test observes physical/implemented behavior but samples, costs, and can damage. Correlate them where margins or consequences demand.

**Combined versus separate activities.** Combining requirements into one campaign saves setup but couples schedule and can obscure oracles. Separate work localizes evidence but consumes resources. Preserve per-requirement trace and abort/retest logic either way.

**Qualification-plus-acceptance regimes.** Qualifying a design and accepting production items avoids destructive repetition, but requires production equivalence, workmanship screens, configuration/process control, and rules for change. One-off systems may use different regimes.

**Physical versus virtual facilities.** Virtual environments scale and inject faults; physical work exposes real interfaces/environment. Model credibility, timing, hardware, people, and consequence determine mix.

**Risk-based depth versus uniform coverage.** Uniform fields aid completeness. Risk-based independence, corroboration, margins, scenario breadth, and review focus resources where failure matters. Low criticality is not permission for zero evidence.

## Failure Modes and Misconceptions

**“The matrix is the plan.”** A matrix may map rows but omit strategy, dependencies, resources, facilities, configuration, anomaly flow, evidence handling, and governance.

**“Every shall must be tested.”** Every applicable requirement needs adequate verification; test is only one method and may be wasteful, unsafe, or incapable of observing the property.

**“Verify at the highest level to be safe.”** Higher integration may hide internal state, make fault isolation hard, or prevent extreme conditions. Use the lowest adequate level plus integration/emergence evidence.

**“Component passes add up to a system pass.”** Interfaces, timing, common resources, people, environment, and emergence invalidate simple composition.

**“A booked date means feasible.”** Article/configuration maturity, prerequisites, facility certification, instrumentation, personnel, logistics, permits, and analysis capacity may not exist.

**“Execution equals closure.”** Raw data needs reduction, uncertainty, review, anomaly disposition, trace, and authority. A run can be invalid or inconclusive.

**“Retest is a small schedule line.”** Diagnosis, correction, change review, regression, facility remobilization, and repeated analysis often dominate.

**“Supplier certificates close owner requirements.”** Supplier evidence has scope, configuration, process, standards, and limitations. Assess relevance and retained responsibility.

**“Automation makes results reproducible.”** Mutable dependencies, environment drift, hidden retries, nondeterminism, flaky oracles, and overwritten artifacts can make automated evidence irreproducible.

**“Waiver closes verification.”** It can close a program action under authority, but technical nonconformance and residual risk remain explicit.

## Worked Examples

### Example 1

**Situation.** A mass requirement is assigned to a full-system vibration test.

**Reasoning.** Mass is directly observable by calibrated inspection/measurement before the costly campaign. Vibration may reveal dynamics but is a poor mass oracle. Assign inspection at article level and use mass properties as an input/configuration check for vibration analysis/test.

**Conclusion.** Select the least costly adequate method; do not default every requirement to system test.

### Example 2

**Situation.** Software shall respond within 200 ms end-to-end, but component tests exclude network, identity, queue, and display.

**Reasoning.** Component timing helps budget allocation but cannot close end-to-end latency. Plan component measurements, interface/integration tests, representative workload/network, clock synchronization, percentile oracle, warm/cold modes, overload, and full path evidence.

**Conclusion.** Lower-level evidence supports diagnosis and budgets; system-level measurement closes the end-to-end claim.

### Example 3

**Situation.** A unique flight item must survive a destructive margin test.

**Reasoning.** Testing the delivered item would consume it. Plan qualification on a representative dedicated article, analysis for differences, production/process control, and acceptance screens on the flight item. Define configuration equivalence and changes that invalidate qualification.

**Conclusion.** Article strategy is part of verification inference, not logistics afterthought.

### Example 4

**Situation.** A supplier offers a certificate that a valve meets pressure requirements.

**Reasoning.** Retrieve standard, lot/configuration, procedure, calibration, conditions, sample, acceptance rule, anomalies, and independence. Compare owner requirement/environment and interface. Credit may be full, partial with incoming inspection/analysis, or rejected.

**Conclusion.** Supplier evidence receives bounded credit only after relevance and quality assessment.

### Example 5

**Situation.** A simulation will verify thermal limits, but contact resistance is guessed.

**Reasoning.** Plan model implementation verification, input pedigree, mesh/numerical convergence, parameter sensitivity, uncertainty/margin, correlation tests, configuration matching, and a domain of validity. If the decision reverses across plausible resistance, obtain data or redesign margin.

**Conclusion.** “Analysis” is not a method description until model credibility and oracle are planned.

### Example 6

**Situation.** A chamber is reserved for Monday; the article arrives Friday and the procedure is awaiting approval.

**Reasoning.** The date is at risk because incoming inspection, configuration audit, instrumentation install, calibration, dry run, safety review, procedure approval, and TRR precede execution. Model dependencies and alternative windows; do not compress by silently skipping gates.

**Conclusion.** Resource booking is not readiness; schedule every prerequisite and decision.

### Example 7

**Situation.** A demonstration checks emergency shutdown but says only “operator shuts down successfully.”

**Reasoning.** Define initial state, fault cue, representative operator/training/equipment, allowed actions, maximum response time, safe state, prohibited side effects, measurements, uncertainty, abort, and inconclusive rule. If quantitative time is required, demonstration may need instrumented test evidence.

**Conclusion.** A method label without an oracle and context is not executable verification planning.

### Example 8

**Situation.** One campaign has 20% rework reserve distributed uniformly.

**Reasoning.** Low-risk inspections need little; novel integration and destructive/environmental tests have high mobilization and retest risk. Estimate anomaly paths by claim/facility/article, include diagnosis and review, and protect critical scarce-resource windows.

**Conclusion.** Risk-shaped reserves produce a more credible schedule than uniform padding.

### Example 9

**Situation.** A continuous pipeline reports 98% passing tests, but safety tests are quarantined as flaky.

**Reasoning.** Aggregate percentage hides critical invalid evidence. Treat flaky behavior as anomaly, control environment/dependencies/seeds, preserve failed runs, repair oracle or product, and block safety closure until reproducible adequate evidence exists.

**Conclusion.** Automation throughput cannot compensate for missing critical evidence.

### Example 10

**Situation.** A security library update changes no system requirements, so the team proposes no re-verification.

**Reasoning.** Compare dependency behavior, interfaces, cryptography, timing, error paths, supported platforms, vulnerabilities, and affected safety/mission threads. Run targeted static/analysis, unit, integration, performance, security, recovery, and regression evidence based on impact; preserve unaffected credit.

**Conclusion.** Re-verification is driven by evidence dependency and consequence, not only requirement text changes.

## Cross-Program Connections

- **API/service engineering:** contract, compatibility, load, failure, idempotency, recovery, and consumer evidence need coordinated levels and environments.
- **Platform engineering:** reproducible environments, delivery pipelines, observability, test data, ephemeral infrastructure, and policy-as-code are enabling products.
- **Data engineering:** dataset lineage, quality, replay, reconciliation, privacy, freshness, and distribution are both verification subjects and evidence infrastructure.
- **OOP:** unit boundaries, mocks, contracts, substitutability, and dependency injection affect observability and integration credit.
- **FP:** properties, types, proofs, deterministic cores, effect boundaries, and generators can strengthen analysis and automated evidence.
- **Safety/reliability/security:** consequence drives rigor, independence, corroboration, statistical design, fault injection, adversarial work, and closure authority.
- **Configuration management:** baselines, article identity, tools, data, procedures, results, and change impact preserve evidence validity.
- **Project engineering:** resources, suppliers, facilities, critical paths, cost, contingency, and decision gates make the strategy executable.
- **Human factors:** representative users, training, workload, PPE, maintenance, accessibility, and organizational context require planned evidence.
- **Validation/acceptance:** verification establishes conformance; later decisions need distinct intended-use and authorization evidence.

## References

1. NASA, [Verification and Validation Plan Outline, Systems Engineering Handbook Appendix I](https://www.nasa.gov/reference/appendix-i-verification-and-validation-plan-outline/), accessed 2026-08-31.
2. NASA, [Technical Planning, Systems Engineering Handbook section 6.1](https://www.nasa.gov/reference/6-1-technical-planning/), accessed 2026-08-31.
3. NASA, [Product Verification, Systems Engineering Handbook section 5.3](https://www.nasa.gov/reference/5-3-product-verification/), updated 2023.
4. NASA, [NPR 7123.1C, NASA Systems Engineering Processes and Requirements, Change 2](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001C_&page_name=all), accessed 2026-08-31.
5. NASA Software Engineering Handbook, [SWE-028: Verification Planning](https://swehb.nasa.gov/spaces/7150/pages/16450576/SWE-028%2B-%2BVerification%2BPlanning), accessed 2026-08-31.
6. NASA Software Engineering Handbook, [Software Test Estimation and Testing Levels](https://swehb.nasa.gov/spaces/7150/pages/16449817/7.06%2B-%2BSoftware%2BTest%2BEstimation%2Band%2BTesting%2BLevels), accessed 2026-08-31.
7. NASA, [Human Systems Integration Plan Content Outline, Systems Engineering Handbook Appendix R](https://www.nasa.gov/reference/appendix-r-hsi-plan-content-outline/), accessed 2026-08-31.
8. Federal Aviation Administration, [Acquisition Management System Lifecycle Verification and Validation Guidelines, Version 3.0](https://www.faa.gov/sites/faa.gov/files/2022-02/vandvguidelines.pdf), 2017.
9. Federal Aviation Administration, [FAA-STD-074: Preparation of Service Requirements Documents](https://www.faa.gov/sites/faa.gov/files/air_traffic/technology/swim/governance/FAA-STD-074%20FINAL%207-20-20.pdf), 2020.
10. NASA, [NASA Systems Engineering Handbook, NASA/SP-2016-6105 Rev. 2](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf), 2016.

## Exercises

### Exercise 1

For requirements concerning enclosure color, end-to-end response time, maximum structural stress, emergency shutdown by an operator, and recovery after database corruption, propose method, level, article, conditions, and oracle. Explain where combined methods are warranted.

### Exercise 2

A plan maps 80 of 80 requirements, but 12 use an unavailable external system, 5 have no quantitative pass criteria, one destructive test uses the only delivered unit, and analysis inputs are not configuration controlled. Assess readiness and define corrective planning actions.

### Exercise 3

Build a resource/dependency plan for an environmental qualification campaign with a shared chamber, two articles, one specialist, a three-day calibration, readiness review, five-day execution, two-day data reduction, anomaly board, and possible retest. Identify critical scheduling risks.

### Exercise 4

Evaluate whether to credit predecessor-system evidence for a new service whose core software is unchanged but cloud provider, identity system, workload, data residency, and recovery objective differ. Partition reusable, conditionally reusable, and invalid evidence.

### Exercise 5

Design verification planning governance for weekly releases of a safety-relevant software-intensive system. Include baselines, automated/manual evidence, flaky tests, independence, change impact, regression, formal closure, emergency release, and operational feedback.

## Answers to the Exercises

### Answer 1

Enclosure color: inspection at component/final article against controlled color specification under defined illumination or calibrated color measurement if tolerance is quantitative. End-to-end response: instrumented test at integrated-system level with representative network, dependencies, workload, modes, synchronized clocks, percentile/tail oracle, and measurement uncertainty; component analysis/tests support budgets but do not close it. Structural stress: validated finite-element analysis across load cases with material/geometry/configuration inputs, convergence and uncertainty, correlated by strain/static test where consequence/margin demands. Emergency shutdown: demonstration or instrumented test on representative integrated article with representative operator, training/PPE, fault cues, initial states, time/safe-state/prohibited-effect oracle; inspection verifies controls/labels separately. Database-corruption recovery: integrated fault-injection test with production-representative build/data topology, backups, identity, timing, reconciliation, RTO/RPO/integrity oracle, repeat cases, and analysis for untested corruptions.

The mix follows observability and inference. Static attributes favor inspection, large/extreme domains favor analysis with correlation, and socio-technical/emergent behavior requires integrated representative operation.

### Answer 2

Row coverage is 100%, but readiness is not. At least 12 paths have an unavailable dependency; five lack an oracle; the destructive article strategy is infeasible; and uncontrolled inputs invalidate reproducible analysis. Overlap may reduce the count of affected requirements, so report blockers by unique row and criticality rather than subtracting 18 blindly.

For external-system rows, secure availability windows, use a qualified emulator for early evidence, plan final partner evidence, or redesign level/method. Rewrite or clarify the five requirements/success criteria with stakeholders and technical authority; define tolerances, uncertainty, fail/inconclusive rules. Create a representative qualification article or choose non-destructive analysis/correlation plus acceptance evidence, with equivalence to the delivered unit. Put analysis models, inputs, data, tools, assumptions, and configuration under control and plan credibility/review. Rebuild dependencies, costs, schedules, risks, and closure. Do not baseline formal execution until critical infeasibilities have owned dispositions.

### Answer 3

Predecessors are approved objectives/baselines, article configuration and incoming inspection, chamber/support readiness, specialist availability, approved procedure, hazards/controls, instrumentation calibration, and TRR. Schedule calibration for three days before readiness with validity through execution; prevent the specialist from being double-booked. The five-day chamber reservation follows passed TRR. Plan article installation, preconditioning, changeover between two articles, daily checks, teardown, and custody, which may extend the nominal five days. Two-day data reduction precedes requirement findings and anomaly board.

Reserve a conditional chamber/specialist/recalibration window for retest after diagnosis, corrective action, configuration review, procedure change, regression assessment, and new readiness authorization. Critical risks include chamber contention/failure, late article/configuration, calibration expiry or damage, single-specialist absence, first-article anomaly blocking the second, consumables/logistics, unsafe abort/recovery, slow data analysis, and no retest window. Track alternative facility, cross-trained staff, spares, and decision deadlines; do not hide them in generic contingency.

### Answer 4

Potentially reusable evidence includes implementation-level unit/static/property results for unchanged source, toolchain, dependencies, flags, and configuration—after confirming “unchanged” by traceable comparison. Algorithmic proofs and deterministic core tests may also transfer within their premises.

Conditionally reusable evidence includes interface behavior if identity/provider adapters preserve semantics; performance models after recalibration to new cloud/workload; security controls whose threat/identity assumptions are rechecked; and recovery mechanisms whose storage/data topology remains similar. Require configuration diffs, analysis, targeted correlation, and residual limitations.

Invalid for direct closure are old cloud availability/failure-zone evidence, identity integration, real workload/tail performance, data residency/compliance, external dependency behavior, and recovery/RTO evidence under the changed provider/topology/objective. Plan new integration, load, fault, security, residency, backup/restore/reconciliation, and end-to-end work. Supplier certifications may inform but not replace owner-specific requirements. Record each credit decision, source anomaly, configuration, assumption, and change trigger.

### Answer 5

Define each releasable configuration by source, dependencies, build, infrastructure/policy, data/model, flags, interfaces, procedures, and requirements baseline. Map requirements to tiered evidence: fast controlled unit/property/static/contract/security checks on change; integration and hardware/software-in-loop suites; periodic representative system campaigns; manual inspection/demonstration where automation is inadequate; operational monitors as supplementary evidence. Preserve immutable reports, environments/tool versions, raw logs, traces, and anomaly links.

Change-impact analysis selects regression using requirements, architecture, dependency, hazard/security, and evidence traces, with mandatory critical sets that cannot be optimized away. Quarantined/flaky critical tests are open anomalies and block their claims; diagnose product, environment, timing, or oracle rather than rerunning to green. Independent reviewers assess high-consequence changes, evidence credit, anomalies, and closure. A release authority sees passed, failed, inconclusive, waived, and not-run states separately.

Emergency release policy defines qualifying conditions, minimum nonwaivable evidence, independent/technical and operational authority, usage limits, monitoring, rollback, retrospective completion, and expiry. Operational incidents, drift, near misses, monitor loss, new threats, and workaround patterns trigger evidence impact and re-verification. Weekly cadence changes schedule mechanics, not configuration integrity, adequate inference, anomaly truth, or authorized closure.
