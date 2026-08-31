---
module_id: SYSENG-067
program: Systems Engineering
level: 2
module_number: 67
title: Safety Cases
status: complete
last_verified: 2026-08-31
---

# Safety Cases

## One-Page Review

### Governing question

What precisely is being claimed safe enough, for whom, in which configuration and operating context, against which criteria—and does a transparent, logically coherent argument connect trustworthy, applicable evidence to that claim while exposing assumptions, uncertainty, counterevidence, and unresolved defeaters?

### Essential definitions

- A **safety case** is a structured, reasoned, auditable justification—supported by evidence—that a system is adequately safe for a stated application and environment. It is the argument and information set, not merely its summary report or diagram.
- A **top-level claim** is the bounded proposition whose acceptance supports a decision, such as authorizing a named configuration for a defined operation under stated restrictions and criteria.
- A **subclaim** decomposes a broader claim into propositions that jointly support it. Decomposition needs an explicit **argument strategy** explaining why the subclaims are sufficient and relevant.
- **Evidence** is information offered to support a claim: verified requirements, analyses, tests, inspections, operational data, competence records, or other artifacts. A citation is not evidence until provenance, content, applicability, result, and limitations are known.
- **Context** defines terms, system boundary, configuration, operating environment, lifecycle state, criteria, and scope. An **assumption** is a proposition accepted for the argument without evidence in that case and must have an owner and validity conditions.
- A **justification** explains why an inference, decomposition, method, criterion, or evidence choice is warranted.
- A **defeater** or **rebuttal** records a credible reason the claim or inference might fail. An **away claim** delegates a bounded obligation to another case without erasing ownership or interface assumptions.
- **Argument validity** asks whether the conclusion follows with the declared strength from premises. **Evidence adequacy** asks whether evidence is credible, relevant, sufficient, independent enough, current, and configuration-applicable.
- A **confidence argument** addresses why the primary safety argument and its evidence should be trusted. It cannot repair a false safety claim by adding more process prose.
- A **safety case report** is a navigable presentation of the case and its conclusions. The governed case may span models, hazard logs, evidence repositories, configuration records, and decisions.
- A **living safety case** is maintained as design, operations, evidence, assumptions, hazards, regulations, and configuration change. “Living” means governed impact and re-acceptance, not an automatically regenerated green dashboard.

### Central model, mechanism, or theorem

Represent an assurance inference as

\[
C \Leftarrow (C_1,\ldots,C_n; E_1,\ldots,E_m; X; A; J),
\]

where claim $C$ is supported by subclaims $C_i$ and evidence $E_j$ under context $X$, assumptions $A$, and justification $J$. The arrow is not automatically deductive: its strength depends on the strategy and warrants. Each evidence item should satisfy a fitness predicate

\[
Fit(E,C)=Credible\land Relevant\land Sufficient\land Current
\land Configured\land Traceable.
\]

A decision-ready case requires more than every claim having an incoming link. It also requires acceptable open-defeater state, applicable evidence, explicit criteria, competent review, and authorized acceptance.

### Critical invariants

- The top claim names the system/configuration, application, environment, lifecycle interval, stakeholders, safety criterion, restrictions, and decision being supported.
- Claims are propositions that can be challenged; headings such as “testing” or activities such as “performed FMEA” are not safety claims.
- Every decomposition includes a stated strategy and completeness rationale. A tree shape alone supplies neither.
- Evidence supports specific claims through explained inference; dumping documents under a goal creates traceability, not justification.
- Evidence provenance, method, inputs, results, uncertainty, independence, date, approval, configuration, and limitations remain inspectable.
- Assumptions, contexts, justifications, unresolved nodes, counterevidence, dissent, and defeaters are first-class governed objects.
- Hazard completeness, control effectiveness, risk acceptance, safe operation, maintenance, emergency response, software, human factors, and organizational capability are addressed proportionately to the claim.
- The case distinguishes verified implementation from validated operational adequacy and distinguishes conformance from achieved safety.
- Modular/away claims define responsibility, interface contract, version, acceptance state, and impact propagation; delegation does not mean omission.
- Review challenges argument validity and evidence fitness independently. Independent assessment does not transfer the dutyholder's responsibility.
- Change invalidates only through analyzed impact, but unassessed change cannot inherit prior acceptance silently.
- A safety case can support a bounded decision; it never proves zero risk, universal safety, or permanent truth.

### Common failures

Common failures include claiming “the system is safe” without scope; turning the document table of contents into an argument; using hazards as claims without explaining adequate control; attaching test reports without interpreting coverage; treating process compliance as product safety; hiding assumptions in prose; confusing absence of evidence with evidence of absence; arguing circularly from acceptance to safety; decomposing by subsystem and missing interactions; reusing copied patterns without a completeness warrant; counting evidence items as confidence; citing stale or wrong-configuration results; using the same model, data, tool, and author as supposedly independent corroboration; suppressing negative evidence; marking unresolved goals as complete; delegating away claims with no contract; and updating diagrams without impact analysis or re-acceptance.

### Compact example

A synthetic case graph contains six claims and seven evidence records. All claims have declared support, all evidence is referenced, every claim has context, three claims expose assumptions, and no evidence belongs to the wrong configuration. Yet one evidence item is stale and one defeater is open, so the fixture reports `not_ready_for_acceptance`. The graph is structurally connected but not decision-ready. This is synthetic metadata only; it establishes no real safety claim.

### Connections

SYSENG-066 supplies hazards, controls, requirements, verification, uncertainty, and residual-risk decisions. SYSENG-067 turns selected propositions and evidence into an auditable decision argument. Requirements, architecture, reliability, software assurance, cybersecurity, human factors, configuration, operations, and governance each provide claims and evidence. Later verification, validation, and lifecycle modules keep the case current.

## Governing Question

Can a skeptical, competent decision maker reconstruct why the named system configuration is adequately safe for the proposed application, understand exactly what evidence and assumptions the conclusion depends on, see credible counterarguments and limitations, and determine whether the case is sufficient under the governing acceptance criteria?

The question is deliberately decision-centered. A safety case does not manufacture safety, replace engineering, or authorize operation. It organizes the justification so weaknesses can be found before a consequential decision and so acceptance remains traceable afterward.

## Why This Matters

Complex systems generate thousands of requirements, analyses, test results, hazard records, concessions, operating procedures, and change records. Volume can obscure the decisive question: why do these particular facts justify this particular safety conclusion? A safety case creates an explicit chain from decision-relevant claims to evidence and assumptions.

NASA's System Safety Handbook describes risk-informed safety cases as a means of connecting safety objectives, claims, evidence, and decision-maker risk tolerances. UK HSE safety-case regimes place responsibility on the dutyholder and use regulator assessment to challenge whether major hazards are understood and controlled. ONR's Safety Assessment Principles emphasize comprehensive assessment, engineering principles, defence in depth, uncertainty, and lifecycle evidence. FDA guidance for infusion pumps recommends a safety assurance case that connects device hazards, mitigations, verification/validation, intended users, and environment of use.

These regimes are not interchangeable. Legal meaning, required content, acceptance terminology, ALARP or other criteria, regulator roles, and authorization differ. The portable lesson is structured justification under explicit governance. Always apply the domain's actual law, standard, contract, and approval process rather than importing a notation as if it were certification.

Safety cases also improve engineering feedback. A weak argument may expose an ambiguous top-level requirement, incomplete hazard analysis, unsupported independence claim, untested mode, stale configuration, missing operational capability, or unresolved counterevidence. The value lies in making such gaps visible and actionable—not in producing a polished diagram at the end.

## Prerequisites and Retrieval

Before constructing or assessing a safety case, retrieve:

1. governing legislation, regulation, certification basis, contract, standards, safety policy, acceptance criteria, proportionality rules, submission format, decision gates, and authorized roles;
2. intended decision: concept selection, design approval, test readiness, release, operational authorization, modification, waiver, continued operation, decommissioning, or another bounded permission;
3. exact system identity, version/configuration, boundary, interfaces, application, users, environment, lifecycle period, operating envelope, restrictions, and interacting services;
4. safety objectives, hazard log, scenarios, initial/current/residual risk, safety requirements, controls, assumptions, open actions, risk acceptances, and aggregate-risk assessment;
5. architecture, functional/control models, interface definitions, software/data/configuration baselines, human tasks, procedures, training, staffing, maintenance, logistics, emergency response, and security dependencies;
6. evidence inventory with stable IDs, owners, provenance, methods, inputs, tool versions, data lineage, results, uncertainty, limitations, approvals, dates, configuration effectivity, and retention/location;
7. requirements traceability, design realization, inspection, analysis, test, simulation, demonstration, validation, operational performance, incidents, near misses, anomalies, concessions, audit findings, and corrective actions;
8. argument notation/metamodel, patterns, modularization rules, controlled vocabulary, review criteria, toolchain, exchange format, repository, access controls, and baseline/change process;
9. prior review comments, rejected claims, contrary evidence, independent assessment, dissent, unresolved nodes, defeaters, assurance deficits, and decisions with conditions;
10. change history, planned releases/modifications, suppliers and away cases, monitoring thresholds, evidence-expiry rules, impact links, revalidation triggers, and re-acceptance schedule.

Run a retrieval challenge: choose one important leaf evidence item and traverse upward to the exact top-level decision; then choose the top claim and traverse downward through every branch. At each edge ask what inference is being made, why the support is relevant and sufficient, which context/assumption bounds it, and how configuration applicability is established. A missing artifact, ambiguous edge, or unowned assumption is a case defect, not a navigation inconvenience.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish a safety case, safety case report, hazard log, compliance matrix, and evidence repository;
2. formulate bounded top-level claims and decision contexts;
3. decompose claims using explicit argument strategies and completeness warrants;
4. assess logical validity and evidence credibility, relevance, sufficiency, currency, and configuration applicability;
5. represent context, assumptions, justifications, counterevidence, defeaters, and away claims explicitly;
6. integrate hazard/control, software, human, reliability, operational, and organizational evidence;
7. build confidence arguments without circularity or document-count proxies;
8. review cases adversarially and record uncertainty, dissent, and unresolved obligations;
9. modularize and maintain a case through configuration and lifecycle change;
10. communicate a decision-ready conclusion without claiming zero risk or external approval.

## Core Exposition

**Start with the decision.** Define who must decide what, under which authority, at which lifecycle gate. A concept-selection case differs from an operational authorization case because available evidence and required conclusions differ. Avoid building a generic case and later searching for a decision it might support.

**Bound the top claim.** Include system/configuration, intended application, environment, operating envelope, stakeholders, time period, restrictions, and criterion. “Vehicle V4.2 is adequately safe for supervised freight operation on mapped private roads below 30 km/h, subject to restrictions R1–R4 and acceptance criterion P” is reviewable. “The vehicle is safe” is not.

**Define adequate.** Adequacy may mean compliance with explicit limits, risk reduced according to law/policy, satisfaction of safety requirements, achievement of quantitative goals, application of relevant good practice, or a combination. State thresholds and decision authority. A case cannot infer adequate safety from an undefined adjective.

**Separate the case from its report.** The case is the maintained claims, reasoning, evidence, context, assumptions, review, and decisions. A report presents a navigable snapshot or summary. The evidence remains in controlled repositories; the report should provide stable references and conclusions without duplicating uncontrolled copies.

**Use claims, not topics.** A claim asserts something capable of truth or falsity: “All identified catastrophic hazards have implemented and validated controls in configuration B.” “Hazard analysis” is a topic; “FMEA performed” is an activity. Topic trees often look orderly while making no inference.

**Write the strategy as a warrant.** If a claim is decomposed by hazards, lifecycle stages, safety functions, or lines of defence, explain why that partition covers the parent claim and how interactions are handled. A decomposition is not complete merely because its branches have familiar labels.

**Choose decomposition axes deliberately.** Hazard-based structures map naturally to control evidence but can duplicate shared controls. Architecture-based structures support ownership but miss emergent interactions. Lifecycle structures reveal evolving evidence but can fragment cross-phase claims. Combine axes with cross-cutting claims and explicit interfaces rather than forcing one universal tree.

**Distinguish deductive and inductive strength.** A deductive argument requires premises that entail the claim, which is rare for whole-system safety. Most safety arguments are defeasible: evidence increases confidence but new information can overturn the conclusion. Use language such as “supports” or “provides sufficient justification under criteria X,” not mathematical proof rhetoric.

**Make context first-class.** Definitions, system boundaries, operational modes, evidence cut-off dates, risk criteria, and configuration apply across nodes. If context changes, affected claims must be discoverable. Do not hide essential qualifications in diagram footnotes that reviewers cannot query.

**Manage assumptions as obligations.** An assumption may concern independence, user competence, demand rate, environmental range, supplier service, emergency response, or data distribution. Give it an owner, rationale, evidence plan if possible, monitoring, validity interval, and failure response. If a claim depends critically on an untestable assumption, make that decision visible.

**Explain evidence use.** A test report does not “prove safety.” State which claim it supports, the tested configuration and environment, coverage, oracle, independence, uncertainty, anomalies, exclusions, and remaining gap. A passing result for nominal mode may be irrelevant to a degraded-mode claim.

**Evaluate credibility.** Ask who produced the evidence, with what competence and independence; whether the method/tool is validated for the purpose; whether data are authentic and traceable; whether review and approvals occurred; and whether negative results were retained. Independence is graded, not a binary badge.

**Evaluate relevance.** Evidence can be high quality but address the wrong claim, configuration, interface, hazard, population, or environment. Analogy requires an explicit similarity argument and identified differences. Standards certification of a component does not automatically support integrated system safety.

**Evaluate sufficiency.** Sufficiency depends on claim consequence, uncertainty, novelty, complexity, and required confidence. Multiple evidence items add value when they cover different failure mechanisms or use genuinely diverse methods. Repeating one test or citing many documents derived from the same model may add little.

**Evaluate currency and effectivity.** Evidence needs configuration identity, date, baseline, change history, and validity window. Tools, calibration, personnel competence, environmental assumptions, operational data, and supplier cases can expire. A live case should calculate impact, not blindly relabel old evidence current.

**Link hazards to claims without copying the log.** The hazard log manages scenarios, controls, actions, risk, and acceptance. The case argues completeness of the hazard-identification process, adequacy of controls, satisfaction of safety requirements, management of aggregate risk, and continuing operational capability. Reference governed records rather than pasting divergent tables.

**Argue control implementation and effectiveness separately.** Inspection may show a guard exists; analysis/test may show it withstands loads; validation may show it prevents exposure in representative operation; monitoring may show it remains available. One branch should not collapse these distinct propositions.

**Address software systematically.** Claims may cover correct safety requirements, architecture, freedom from interference, data/state/timing, verification coverage, tool qualification, anomaly disposition, configuration/update/rollback, cybersecurity interaction, and operational monitoring. Process conformance supports confidence but does not entail correct behavior.

**Address humans and organizations.** Evidence must reflect representative users, tasks, workload, interfaces, training, staffing, maintenance, handover, emergency response, management systems, and safety culture where relevant. A training certificate cannot alone support a claim that an emergency action is feasible under time pressure.

**Use away claims carefully.** A supplier may provide an assurance case for a component or service. Define the assumed/guaranteed behavior, configuration, environment, interface, evidence access, update notification, unresolved risks, and acceptance authority. The integrating organization retains responsibility for integration claims and cannot delegate unknown interactions.

**Modularize for ownership and change.** Modules should correspond to stable responsibility and interfaces, not arbitrary diagram size. Each module declares public claims, required assumptions, provided evidence, version, status, and dependency links. Cycles require explicit joint reasoning; hidden circular support is invalid.

**Search for defeaters.** Ask what would make each claim false, evidence misleading, or inference insufficient. Examples include missing hazard classes, shared-cause failure, wrong configuration, optimistic exposure, invalid model, biased test selection, operator workload, security compromise, stale supplier evidence, and contradictory field data.

**Classify defeater state.** A defeater can be proposed, investigated, resolved with rationale/evidence, accepted as residual uncertainty by authority, or remain open. Deleting it because the team disagrees destroys auditability. A high-consequence open defeater may block acceptance even when every diagram node has a green border.

**Build confidence arguments selectively.** The primary case argues safety; a confidence case argues why its claims, inferences, and evidence are trustworthy. Cover hazard-analysis competence/coverage, model validation, test independence, tool/data integrity, review effectiveness, and change control. Avoid infinite regress by applying proportional criteria and explicit stopping rules.

**Prevent circularity.** “The system is safe because the authority accepted it” confuses decision with evidence. “The evidence is sufficient because the case says so” is also circular. Map the graph and inspect dependency cycles. Some mutual dependencies reflect engineering feedback but must resolve to independent premises or joint claims.

**Keep compliance and safety distinct.** Compliance can be a necessary claim and strong evidence of disciplined engineering. Yet a standard may not cover the exact system, hazard, environment, integration, or novel technology. Conversely, alternative means may establish safety only if the governing regime permits them. State the relationship.

**Make uncertainty visible.** Record parameter uncertainty, model-form uncertainty, incomplete coverage, sampling limits, unknown common causes, future operational change, and contested judgment. Ranges, sensitivity analyses, confidence bounds, qualitative caveats, and explicit residual gaps are preferable to false precision.

**Design review around challenge.** Review the top claim and criteria; argument validity; evidence fitness; hazard/control coverage; assumptions; interfaces; counterevidence; configuration; and decision conditions. Use reviewers competent in relevant domains and sufficiently independent for consequence. Record findings, rationale, dissent, actions, and closure evidence.

**Use visualization as navigation, not content replacement.** Claim–argument–evidence diagrams can expose structure, and GSN-like notations add goals, strategies, solutions, contexts, assumptions, and justifications. OMG SACM supports model interchange concepts. Notation compliance does not establish semantic validity; readable prose and evidence links remain necessary.

**Automate consistency, not judgment.** Tools can detect orphan claims/evidence, unresolved nodes, missing owners, stale artifacts, configuration mismatches, cycles, broken links, and impacted claims. They cannot decide hazard completeness, evidence credibility, argument sufficiency, or acceptable risk without accountable human judgment.

**Baseline the decision package.** Record case version, system configuration, evidence snapshot, open/accepted deficits, restrictions, review record, acceptance authority, date, and expiry/reopen conditions. Cryptographic digests can detect changed artifacts but do not establish their truth.

**Maintain through change.** Trace change to affected context, assumptions, claims, evidence, hazards, controls, interfaces, away cases, and acceptance. Classify impact; update and review proportionately; preserve prior baselines; and obtain re-acceptance where criteria require. Unassessed change should not inherit the old decision.

**Use operational evidence continuously.** Monitor leading indicators, control demands/failures, alarms, bypasses, incidents, near misses, anomalies, maintenance, staffing, environmental exposure, cybersecurity events, and supplier notifications. Confirm or challenge case assumptions. Operational success is evidence within observed exposure, not universal validation.

**Communicate conclusions honestly.** A decision summary should state what is claimed, scope/configuration, criteria, strongest evidence, principal uncertainty, open actions/defeaters, restrictions, monitoring, review result, and requested decision. Avoid “certified safe” unless a named authority has actually issued that certification for that scope.

The following fixture checks structural and lifecycle metadata for a deliberately non-ready synthetic case.

<!-- bijux-verify: {"id":"safety-case-readiness-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"claims=6\nevidence_items=7\nclaims_with_support=6\ncontext_bindings=6\nassumption_bindings=3\norphan_evidence=0\nconfiguration_mismatches=0\nstale_evidence=1\nopen_defeaters=1\ndecision=not_ready_for_acceptance\nevidence=synthetic_case_metadata_only\n","stderr":""}} -->
```python
claims = {
    "C0": {"supports": ["C1", "C2", "C3"], "context": "vehicle-v4.2-private-road"},
    "C1": {"supports": ["E1", "E2"], "context": "hazard-scope-2026-08", "assumption": "mapped routes remain controlled"},
    "C2": {"supports": ["C4", "C5"], "context": "control-baseline-v4.2", "assumption": "credited barriers are independent as analyzed"},
    "C3": {"supports": ["E3", "E4"], "context": "supervised-operations", "assumption": "minimum trained staffing is maintained"},
    "C4": {"supports": ["E5"], "context": "preventive-controls-v4.2"},
    "C5": {"supports": ["E6", "E7"], "context": "mitigating-controls-v4.2"},
}
evidence = {
    "E1": {"configuration": "v4.2", "current": True},
    "E2": {"configuration": "v4.2", "current": True},
    "E3": {"configuration": "v4.2", "current": True},
    "E4": {"configuration": "v4.2", "current": False},
    "E5": {"configuration": "v4.2", "current": True},
    "E6": {"configuration": "v4.2", "current": True},
    "E7": {"configuration": "v4.2", "current": True},
}
referenced = {
    item
    for claim in claims.values()
    for item in claim["supports"]
    if item.startswith("E")
}
open_defeaters = ["D1: emergency-stop independence not reverified after supplier change"]
stale = sum(not item["current"] for item in evidence.values())
mismatches = sum(item["configuration"] != "v4.2" for item in evidence.values())
ready = (
    all(claim["supports"] for claim in claims.values())
    and referenced == set(evidence)
    and stale == 0
    and mismatches == 0
    and not open_defeaters
)
print(f"claims={len(claims)}")
print(f"evidence_items={len(evidence)}")
print(f"claims_with_support={sum(bool(claim['supports']) for claim in claims.values())}")
print(f"context_bindings={sum(bool(claim['context']) for claim in claims.values())}")
print(f"assumption_bindings={sum('assumption' in claim for claim in claims.values())}")
print(f"orphan_evidence={len(set(evidence) - referenced)}")
print(f"configuration_mismatches={mismatches}")
print(f"stale_evidence={stale}")
print(f"open_defeaters={len(open_defeaters)}")
print(f"decision={'ready_for_acceptance' if ready else 'not_ready_for_acceptance'}")
print("evidence=synthetic_case_metadata_only")
```

The fixture deliberately refuses readiness despite complete graph connectivity. It does not evaluate whether claims are true, whether decomposition is logically sufficient, whether evidence is credible, or whether the named context is adequate. Those remain substantive review obligations.

## Definitions and Notation

Let a case be a directed, attributed graph $G=(N,E)$ whose nodes include claims $C$, evidence references $V$, contexts $X$, assumptions $A$, justifications $J$, and defeaters $D$. Edges state relationships such as `supports`, `in-context-of`, `assumes`, `justified-by`, `rebuts`, or `depends-on`. Acyclic support is usually easier to audit, but modular references may form dependencies that require explicit joint treatment.

For evidence item $v$ supporting claim $c$, define a review vector

\[
q(v,c)=(p,r,s,i,u,t),
\]

representing provenance/credibility, relevance, sufficiency contribution, independence/diversity, uncertainty disclosure, and temporal/configuration applicability. This is not necessarily numeric; it is a checklist of distinct questions that must not collapse into “document exists.”

Let $Impact(\Delta)$ be the transitive set of contexts, assumptions, claims, evidence, hazards, controls, modules, and acceptances affected by change $\Delta$. A case remains current only when impact is assessed and required evidence/review/acceptance updates are complete.

Let $Open_D(C)$ be material unresolved defeaters for claim $C$. A simplistic structural predicate might verify that every claim has support, but decision readiness additionally requires criteria such as

\[
Ready(C) \Rightarrow Supported(C)\land FitEvidence(C)\land
Acceptable(Open_D(C))\land Reviewed(C)\land Authorized(C).
\]

This implication states necessary categories, not a universal sufficient theorem.

## Mechanisms, Invariants, or Proof Structure

A defensible safety-case conclusion follows this chain:

1. **Decision validity:** the requested decision and authority are explicit, lawful, and matched to the lifecycle gate.
2. **Claim validity:** the top claim is a challengeable proposition bounded by system, configuration, application, environment, criteria, restrictions, and time.
3. **Decomposition validity:** subclaims, strategy, coverage rationale, and interaction treatment jointly address the parent claim without circularity.
4. **Hazard/control validity:** identified hazards, control requirements, implementation, effectiveness, residual and aggregate risk, and operational capability are represented proportionately.
5. **Evidence validity:** every evidence item has credible provenance, relevant scope, adequate coverage, current configuration, disclosed uncertainty, and an explained inference to a claim.
6. **Assumption validity:** assumptions and contexts are explicit, owned, justified, monitored, and within their validity conditions.
7. **Challenge validity:** counterevidence, defeaters, anomalies, alternative explanations, and dissent are sought and resolved or exposed to decision authority.
8. **Review validity:** competent, proportionately independent reviewers assess semantics and evidence—not merely notation—and findings close with evidence.
9. **Lifecycle validity:** baseline, change impact, operational feedback, supplier dependencies, restrictions, expiry, and re-acceptance preserve currency.
10. **Acceptance validity:** the authorized decision maker receives a faithful summary of claims, evidence, uncertainty, deficits, restrictions, and monitoring before deciding.

The case remains defeasible. New incidents, corrected data, changed configuration, failed controls, or better knowledge can undermine an earlier conclusion. That is a feature of honest assurance, not a weakness to hide.

## Alternatives and Trade-Offs

**Claim–argument–evidence prose versus graphical notation.** Prose can express nuance and warrants; diagrams expose topology and support navigation. Use both when complexity warrants, with one governed semantic model to prevent divergence.

**Integrated versus separate confidence case.** Integration keeps evidence-quality reasoning near claims; separation can make assurance-of-assurance systematic. Too much separation creates navigation overhead and regress. Apply proportional depth to consequential or uncertain links.

**Monolithic versus modular case.** A monolith avoids interface contracts but becomes unreviewable and change-sensitive. Modules improve ownership/reuse and parallel review but can hide interactions and circular dependencies. Modularize by stable responsibility and publish assumptions/guarantees.

**Hazard-based versus architecture-based decomposition.** Hazard structures align to risk decisions; architecture structures align to owners and evidence. Hybrid structures need explicit cross-cutting claims for interactions, common cause, human/organizational factors, and aggregate risk.

**Manual versus model-based management.** Manual documents are accessible but prone to broken links and stale copies. Model-based tooling supports queries, checks, reuse, and impact analysis but adds schema/tool/version risk. Preserve portable exports and human-readable conclusions.

**Independent evidence versus delivery speed.** Independence can reduce correlated bias but costs time and scarce expertise. Grade independence by consequence, novelty, uncertainty, and conflict of interest; record what independence does and does not cover.

**Reusable patterns versus bespoke reasoning.** Patterns teach valid questions and consistent structure, but copied nodes can conceal missing premises. Instantiate with explicit applicability and completeness rationale; never treat pattern conformance as safety evidence.

## Failure Modes and Misconceptions

- **“The PDF is the safety case.”** The governed argument/evidence set is the case; a PDF is one presentation baseline.
- **“More evidence means more confidence.”** Relevance, credibility, diversity, coverage, and applicability matter more than count.
- **“A green graph is complete.”** Structural checks cannot establish semantic truth, sufficiency, or absence of defeaters.
- **“Compliance proves safety.”** Compliance supports bounded claims; novel context and integrated hazards still need reasoning.
- **“A test passed, therefore the system is safe.”** A test supports a defined behavior/configuration under sampled conditions.
- **“All hazards are controlled, therefore hazard identification was complete.”** Control coverage and identification completeness are separate claims.
- **“Assumptions are harmless context.”** Assumptions are potential failure points and need ownership, validation, monitoring, and limits.
- **“Independent review makes the reviewer responsible.”** Review challenges the case; the dutyholder and authorized decision roles retain responsibility.
- **“Away claims remove integration responsibility.”** The integrator owns interface assumptions and emergent behavior.
- **“GSN/SACM syntax ensures a sound argument.”** Notation and interchange can be correct while reasoning is invalid.
- **“Confidence can be calculated by averaging node scores.”** Dependencies and ordinal judgments make naïve aggregation misleading.
- **“No counterevidence was found.”** Search method, sources, expertise, period, and reporting quality bound that statement.
- **“Operational success closes the case.”** It adds exposure-bounded evidence and may reveal new defeaters; the case remains living.
- **“Change only affects changed components.”** Interfaces, assumptions, controls, evidence, human tasks, and aggregate risk can propagate impact.
- **“Accepted means proven.”** Acceptance is an authorized bounded decision under uncertainty, not a theorem.

## Worked Examples

### Example 1

A team proposes the top claim “Drone X is safe.” Reviewers cannot determine configuration, mission, airspace, weather, payload, operator role, population exposure, criterion, or decision. The claim is rewritten: “Drone X configuration 3.4 is adequately safe for supervised daytime inspection within geofenced private sites, below 60 m, in weather envelope W, subject to restrictions R1–R3, for operational authorization O.” This does not make it true; it makes evidence applicability and counterexamples reviewable.

### Example 2

The top claim is decomposed into hardware, software, and operations branches. The strategy says only “argument by subsystem.” A reviewer raises a defeater: collision avoidance depends on sensor hardware, perception software, map data, communications, operator response, and site separation. No branch owns the interaction. The case adds a cross-cutting claim for end-to-end separation across nominal/degraded modes, with integrated evidence and an interface-assumption table. Organizational convenience no longer defines completeness.

### Example 3

A claim that emergency shutdown prevents overpressure cites a signed test report. Evidence review finds the test used configuration 2.8, one sensor, warm laboratory conditions, and a manual command; the release candidate is 3.1 with new sensor firmware and automatic initiation at low temperature. The report remains credible for what it observed but is not applicable or sufficient. It becomes supporting historical evidence while new integrated tests and analysis close the actual claim.

### Example 4

Three verification reports all conclude a model is correct. They were generated from the same requirements spreadsheet, simulation library, input dataset, and analyst. Counting them as independent triangulation overstates confidence. The case records shared provenance, then adds a requirements inspection by a different team, analytical boundary checks, and physical testing with separately acquired measurements. Diversity is justified by distinct failure-detection mechanisms, not organizational labels.

### Example 5

A safety control assumes one trained operator can acknowledge an alarm and isolate a leak within 40 seconds. The assumption is buried in test notes. The case promotes it to an owned assumption linked to staffing, competence, alarm workload, accessibility, and response evidence. A night-shift observation contradicts it when one operator manages two areas. The defeater stays open until design automation or staffing/response evidence changes the case; it is not deleted as “operator noncompliance.”

### Example 6

A supplier case claims a battery module prevents thermal propagation. Its interface guarantee covers 25°C, upright mounting, charge below 80%, and a specified vent path. The integrator mounts it horizontally, charges to 95%, and routes vents through a shared enclosure. An away-claim link without the contract would look satisfied. Explicit assumption/guarantee matching shows it is not applicable, triggering redesign, new evidence, or bounded restrictions.

### Example 7

A release pipeline updates an assurance model after every test. All nodes turn green because links resolve, yet a regression report shows an unexplained braking latency increase. The anomaly is negative evidence and a defeater to the timing claim. The case blocks decision readiness, records investigation and affected claims, and preserves the prior accepted baseline. Automation correctly maintains consistency only after the governance rule treats contrary evidence as first-class.

### Example 8

An infusion-pump case argues that all hazards are adequately addressed. A separate confidence branch asks whether hazard identification is complete enough: it cites multiple methods, representative clinicians, postmarket data, human-factors analysis, software/system analysis, and independent review, while stating gaps and update triggers. This confidence branch does not prove the hazard set complete. It justifies why the identification process and evidence are adequate for the defined regulatory decision.

### Example 9

A team assigns each evidence item a 0–1 confidence and averages to 0.93. One decisive containment analysis used an invalid material model, but many low-impact documents overwhelm it. The aggregate score hides logical structure. Review returns to claim-specific evidence fitness, sensitivity, dependencies, and defeaters. Quantification may help when semantics and combination rules are justified; an average is not a substitute for the argument.

### Example 10

An operational case was accepted for software 5.0 with two trained responders. Version 5.1 changes alarm priority and an approved temporary waiver reduces staffing. Impact traversal reaches human-response, hazard-control, emergency-operation, training, timing-test, monitoring, and acceptance nodes. Old component tests remain valid where unaffected, but integrated response evidence and the top decision do not. A limited authorization includes expiry and monitoring while revalidation proceeds.

## Cross-Program Connections

**Requirements engineering.** Claims depend on precise safety objectives and derived requirements. Bidirectional links reveal requirements without evidence and evidence without decision relevance.

**Architecture and interfaces.** Decomposition, away claims, assumptions/guarantees, fault containment, independence, and common cause follow architectural boundaries—but cross-cutting interaction claims remain essential.

**Reliability and quantitative analysis.** Reliability models, fault trees, uncertainty, sensitivity, and operational data can support claims. Model validity and applicability need their own assurance; numbers do not bypass inference.

**Software engineering.** Requirements, architecture, code analysis, testing, tool qualification, anomaly disposition, release, rollback, and observability contribute evidence. CI can maintain links and currency while accountable reviewers judge adequacy.

**API, platform, and data engineering.** Service dependencies, schema/version contracts, identity, deployment controls, telemetry, lineage, freshness, and shared infrastructure affect claim validity. Evidence pipelines need provenance and immutable baselines.

**Cybersecurity.** Security assurance cases share claim/argument/evidence structure. Safety and security cases should coordinate unsafe consequences, malicious paths, shared controls, and conflicting assumptions without merging unlike likelihood models.

**Human factors and operations.** Representative-use validation, staffing, competence, workload, maintenance, emergency response, procedures, and organizational governance often carry decisive claims that cannot be delegated to equipment design.

**Governance and regulation.** Acceptance authority, independent assessment, legal criteria, concessions, dissent, restrictions, monitoring, and re-acceptance turn an engineering argument into a controlled decision process.

## References

1. NASA, [NASA System Safety Handbook, Volume 1: System Safety Framework and Concepts for Implementation, NASA/SP-2010-580](https://ntrs.nasa.gov/api/citations/20120003291/downloads/20120003291.pdf), 2011.
2. NASA, [NASA System Safety Handbook, Volume 2: System Safety Concepts, Guidelines, and Implementation Examples, NASA/SP-2014-612](https://ntrs.nasa.gov/api/citations/20150015500/downloads/20150015500.pdf), 2015.
3. UK Ministry of Defence, [JSP 815: Defence Safety Management System Direction and Guidance](https://www.gov.uk/government/publications/defence-safety-management-system-jsp-815-volume-2), updated 2024.
4. UK Health and Safety Executive, [Offshore safety cases—regulations, assessment principles, and guidance index](https://www.hse.gov.uk/offshore/safetycases.htm), accessed 2026-08-31.
5. UK Health and Safety Executive, [A guide to the Offshore Installations (Safety Case) Regulations 2005, L30](https://www.hse.gov.uk/pubns/priced/l30.pdf), 2006.
6. UK Office for Nuclear Regulation, [Safety Assessment Principles for Nuclear Facilities, 2014 edition, January 2020 revision](https://www.onr.org.uk/publications/regulatory-guidance/regulatory-assessment-and-permissioning/safety-assessment-principles-saps), accessed 2026-08-31.
7. Object Management Group, [Structured Assurance Case Metamodel Specification, Version 2.3](https://www.omg.org/spec/SACM/About-SACM), 2023.
8. U.S. Food and Drug Administration, [Infusion Pumps Total Product Life Cycle: Guidance for Industry and FDA Staff](https://www.fda.gov/media/78369/download), 2014.
9. International Atomic Energy Agency, [GSR Part 4 (Rev. 1): Safety Assessment for Facilities and Activities—online standard](https://nucleus-apps.iaea.org/nss-oui/Content/Index?CollectionId=m_0d27280c-1967-4e9c-aa22-4394ea3acb5b&type=PublishedCollection), 2016.
10. U.S. National Institute of Standards and Technology, [Assurance case—CSRC glossary definition sourced to ISO/IEC 15026-1 and NIST SP 800-160](https://csrc.nist.gov/glossary/term/assurance_case), accessed 2026-08-31.

## Exercises

### Exercise 1

Formulate a top-level claim for authorizing an autonomous inspection robot inside an operating chemical plant. Define configuration, mission, environment, people, safety criterion, restrictions, time, and decision authority. Decompose the claim into four subclaims with strategies, contexts, assumptions, evidence classes, and at least two credible defeaters. Explain why the decomposition is sufficient enough for review without claiming completeness as fact.

### Exercise 2

Review this argument: “All safety requirements passed testing; therefore the system is adequately safe.” Identify missing premises and alternative explanations. Reconstruct it into a defensible structure that distinguishes requirement completeness, correct implementation, verification coverage, operational validation, hazard/control adequacy, evidence fitness, and residual-risk acceptance.

### Exercise 3

A supplier provides a safety case for a braking controller. The integrator changes power, network timing, wheel sensors, environmental range, update service, and maintenance organization. Define an away-claim contract and an impact-analysis procedure. State which supplier evidence might remain applicable, which conclusions require integration evidence, and how unresolved supplier limitations appear in the system case.

### Exercise 4

Design an adversarial review for a claim that an emergency shutdown is sufficiently independent of normal control. Include evidence provenance, common causes, model/data/tool diversity, configuration, human/maintenance dependencies, cybersecurity, negative evidence, uncertainty, and test coverage. Specify findings that would block readiness even if every graph node has a support link.

### Exercise 5

A living safety case has 1,400 claims and 6,000 evidence links. A release changes one shared library, two operating procedures, an alarm threshold, and minimum staffing under a temporary waiver. Propose an automated-plus-human workflow for impact analysis, evidence invalidation, review, monitoring, baseline preservation, conditional authorization, and re-acceptance. Define what automation may assert and what remains accountable judgment.

## Answers to the Exercises

### Answer 1

One bounded claim is: “Robot R configuration 2.3 is adequately safe for supervised visual/thermal inspection along approved routes in Plant Area A during normal production, within environmental envelope E and restrictions R1–R5, from authorization until the next major change or 12 months, according to site criterion P, for decision by the plant operating authority.” Restrictions might prohibit emergency-response routes, explosive atmospheres outside certification, unsupervised motion, or operation with degraded separation sensing.

Decompose by four strategies: hazards are comprehensively enough identified for this mission; preventive/mitigating controls are implemented and effective; human/organizational operation and emergency interaction are adequate; and residual/aggregate risk meets criterion P with continuing monitoring. Context includes plant configuration, routes, chemicals, traffic, workers, communications, and evidence cutoff. Assumptions include controlled access, valid plant maps, trained supervisor availability, and specified network latency. Evidence includes multi-method hazard analysis, route/interface surveys, control requirements and integrated tests, human-in-the-loop trials, cybersecurity analysis, emergency drills, maintenance/inspection plans, and independent review.

Defeaters include a release obscuring sensors or a shared map/network error defeating separation and supervision. Another is that the robot blocks evacuation or distracts operators during an unrelated plant emergency. The decomposition is reviewably adequate only if the strategy explains coverage across hazard/control, operational, and decision-continuity concerns and traces cross-branch interactions. It does not prove unknown hazards absent; the case records methods, limitations, monitoring, and reopen triggers.

### Answer 2

The original argument assumes the safety requirements are complete/correct; tests cover every relevant requirement and mode; oracles are valid; the tested item equals the released configuration; passing results imply integrated operational effectiveness; no untested hazards, human interactions, common causes, security paths, or organizational failures matter; and residual risk is acceptable. None follows from “all tests passed.” It also omits anomalies, uncertainty, and authority.

A defensible structure has separate claims: safety objectives and hazards were identified with adequate breadth; controls were selected and translated into complete, correct, traceable requirements; the released design implements them; verification covers requirements and adverse/degraded conditions with trustworthy methods; integrated validation demonstrates controls in intended use with representative users/environment; unresolved anomalies and contrary evidence are acceptably dispositioned; aggregate and residual risk meet explicit criteria; and operational/maintenance capability sustains controls. Each branch has evidence fitness and confidence review. The conclusion then supports a bounded recommendation to the acceptance authority; it does not convert test success into proof.

### Answer 3

The away-claim contract names controller hardware/software version, safety functions, timing and failure behavior, power quality, sensor semantics/ranges/diagnostics, network protocols/latency/loss, environmental limits, update/rollback rules, maintenance/calibration, cybersecurity assumptions, evidence access, change notification, unresolved anomalies, and supplier acceptance status. System claims state what is guaranteed and what the integrator must provide.

Impact analysis maps each change to assumptions and evidence. Algorithm/code unit evidence may remain relevant if binaries/toolchain and affected dependencies are unchanged; controller environmental or timing tests may remain partially useful as historical evidence. New power transients, sensor behavior, network timing, update service, and maintenance can invalidate independence, diagnostics, response-time, configuration, security, and human-restoration claims. Integrated closed-loop tests, fault injection, worst-case timing, power/environment qualification, update/rollback validation, and representative maintenance evidence are required.

Supplier gaps appear as explicit assumptions, open defeaters, evidence limitations, or unfulfilled away claims linked to system claims. The integrator either supplies compensating evidence/control, restricts operation, obtains supplier resolution, or presents the residual uncertainty to the proper authority. Delegation does not erase integration responsibility.

### Answer 4

The review first defines “independent” and the hazard/scenarios requiring it. It traces shared requirements, sensors, power, processors, software libraries, communications, clocks, actuation, location, environment, cooling, calibration, maintenance, test equipment, staffing, authorization, and security administration. It checks evidence producers, competence, conflicts, tools/models/data, configuration, dates, coverage, uncertainty, anomalies, exclusions, and whether supposedly diverse results share a source.

Adversarial tests include loss/corruption of shared inputs, common power/environmental stress, timing/resource exhaustion, maintenance misconfiguration, bypass, latent failures between proof tests, simultaneous demands, security compromise, false/spurious shutdown, degraded communications, and recovery. Negative field/test evidence is linked rather than summarized away. Sensitivity analysis challenges common-cause and diagnostic assumptions.

Blocking findings include wrong-configuration evidence; unverified shared dependency; invalid model or test oracle; uncovered demand mode; unresolved anomaly affecting response; independence claimed from labels alone; insufficient proof-test interval basis; cybersecurity path bypassing shutdown; maintenance procedure disabling both layers; or a material open defeater beyond the review/acceptance threshold. Complete graph connectivity cannot cure these semantic failures.

### Answer 5

Automation resolves the release delta to libraries, services, requirements, controls, claims, evidence, hazards, interfaces, procedures, staffing assumptions, modules, reviewers, and acceptances. It flags stale/wrong-baseline artifacts, open nodes, broken links, cycles, expired competence/calibration, changed away cases, and claims with invalidated support. It creates a candidate impact set and preserves the previously accepted immutable baseline and digest.

Responsible engineers review semantic reach: shared-library behavior, alarm response, procedure feasibility, staffing workload, common dependencies, aggregate risk, and new failure/cyber paths. Evidence owners rerun selected analysis/tests/validation; safety and domain reviewers assess argument sufficiency and defeaters. The temporary waiver records rationale, scope, compensating controls, monitoring, stop thresholds, owner, expiry, and removal plan. A decision package shows unaffected evidence, refreshed evidence, unresolved deficits, restrictions, and requested conditional or full authorization.

Automation may assert repository facts: identity, trace reachability, execution results, metadata completeness, signatures/digests, dates, configuration matches, and policy-defined gates. Humans remain accountable for hazard completeness, claim truth, inference validity, evidence credibility/relevance/sufficiency, uncertainty, control effectiveness, waiver prudence, and risk acceptance. Operational indicators feed back during the waiver; threshold breach, anomaly, configuration drift, new evidence, or expiry reopens the case and can terminate authorization.
