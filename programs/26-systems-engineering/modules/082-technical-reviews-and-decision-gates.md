---
module_id: SYSENG-082
program: Systems Engineering
level: 2
module_number: 82
title: Technical Reviews and Decision Gates
status: complete
last_verified: 2026-08-31
---

# Technical Reviews and Decision Gates

## One-Page Review

### Governing question

How can a technical review expose the maturity, evidence, uncertainty, dissent, and risk needed for an authorized decision to proceed, proceed with conditions, hold, redirect, repeat work, or terminate—without turning the event into a presentation ritual or a vote on confidence?

### Essential definitions

- A **technical review** is a planned, evidence-based assessment of a defined technical product, baseline, activity, readiness state, or lifecycle maturity against stated objectives and criteria.
- A **decision gate** is an authorized commitment point at which evidence and recommendations are used to choose a controlled course of action and allocate or withhold resources, authority, risk, or transition.
- **Entrance criteria** are conditions required to begin a review meaningfully; they prevent scarce review time from being spent on unavailable, unstable, or unreviewed material.
- **Success criteria** are accomplishments/evidence that must be satisfactorily demonstrated to meet review objectives and support further lifecycle progress. They are not merely agenda items.
- A **terms of reference/review charter** defines purpose, scope, authority, questions, criteria, membership, independence, products, schedule, access, interfaces, and reporting.
- A **peer review/inspection** examines a work product for defects and improvement, commonly within a lifecycle stage. It is not automatically a milestone or investment decision.
- A **readiness review** determines whether an activity such as test, deployment, production, operation, or disposal can begin safely and effectively with required people, products, facilities, procedures, instrumentation, support, and controls.
- An **independent review** provides objective expert assessment sufficiently separate from the responsible team, while the accountable decision authority retains the decision.
- A **finding** is an evidence-backed conclusion relevant to review objectives. A **recommendation** proposes action. An **action item/lien** records required work, owner, authority, due date, evidence, and closure rule.
- **Dissent** is a reasoned disagreement about evidence, interpretation, risk, recommendation, or decision. It must remain traceable and receive the escalation/decision process required by governance.

### Central model, mechanism, or theorem

Let decision $d$ at gate $g$ depend on criteria set $K$, evidence $E$, assumptions $A$, uncertainty $U$, risks $R$, open work $L$, and alternatives $X$ under authority $\alpha$:

$$
d_g=\alpha\big(K,E,A,U,R,L,X\big).
$$

A review produces an assessment and recommendation; it does not mathematically determine $d_g$. A defensible gate requires that every blocking criterion be satisfied or explicitly handled under authorized rules, conditions be enforceable, alternatives remain visible, and the decision record bound the commitment:

$$
\operatorname{proceed}\Rightarrow \neg\operatorname{unresolvedBlocker}
\land \operatorname{authorizedRisk}
\land \operatorname{credibleNextStagePlan}.
$$

### Critical invariants

- Define the decision, authority, scope, lifecycle context, alternatives, objectives, entrance/success criteria, evidence standard, and outcomes before assembling slides.
- Criteria trace to stakeholder outcomes, governing requirements, maturity needs, hazards/threats, risk classification, and the irreversible commitment being considered.
- Review material names exact baselines/configurations, source dates, analysis/model/tool/data versions, assumptions, uncertainty, anomalies, waivers, and unresolved work.
- The responsible team owns accurate evidence; reviewers challenge it; review leadership integrates findings; the decision authority decides and records rationale.
- Reviewer expertise covers relevant domains, interfaces, operations, human factors, production/supply, cost/schedule, safety/security, and retirement as applicable.
- Independence is proportionate to consequence and avoids conflicts, but independent reviewers still need context and evidence access.
- Pre-review preparation and issue discovery are encouraged; the event is not the first time reviewers see material.
- Green summaries cannot override adverse trends, missing data, critical exceptions, dissent, or an unsupported integrated baseline.
- Actions/conditions name owner, due date, closure evidence, authority, consequence of nonclosure, and impact on permitted work.
- A gate can legitimately hold, redirect, narrow scope, add conditions, or terminate; schedule pressure is not a success criterion.
- Review records preserve findings, recommendations, dissent, management response, decision, rationale, conditions, accepted risks, actions, and closure evidence.
- Passing one gate does not guarantee future success or authorize work outside the stated baseline, assumptions, scope, and conditions.

### Common failures

Common failures include reviewing because the calendar says so; vague “ready” criteria; tailoring after seeing gaps; thousands of slides without authoritative links; pre-briefs that suppress findings; reviewers selected for availability or agreement; management present in defect-focused peer inspections; no operations/production/safety/security voice; risk colors without trend or basis; averaging technical, cost, and schedule into one score; actions with no owner/evidence; conditional approval indistinguishable from full approval; dissent omitted from minutes; recommendation confused with decision; proceeding because stopping is expensive; rebaselining to hide variance; and declaring success when the next stage lacks credible people, facilities, supply, support, or retirement path.

### Compact example

A synthetic gate evaluates eight criteria. Six are satisfied, one is a permitted condition, and disposal authority is a blocking gap, so the review recommendation is hold. After authoritative disposal evidence is added, seven criteria are satisfied and one condition remains; the fixture reports only that “proceed with condition” may be recommended and still requires decision authority. It does not make a real lifecycle, safety, legal, or investment decision.

### Connections

Lifecycle planning, requirements, architecture, technical performance measures, earned value/schedule, risk, decision analysis, verification/validation, readiness, configuration/data management, peer inspection, independent assessment, governance, acceptance, certification, and lessons learned shape technical reviews and gates.

## Governing Question

Can the accountable authority make and defend the next commitment using current, configuration-bound, independently challenged evidence—and can successors reconstruct what was known, uncertain, disputed, accepted, conditioned, and excluded at the time?

Reviews are expensive interruptions only when treated as performances. Used well, they create a forcing function for integration: a requirements team cannot claim maturity while interfaces remain undefined; a design cannot be “complete” without manufacturing, operations, hazards, verification and retirement; a test cannot start without a stable article, procedure, facility, instrumentation, people, data and abort rules.

## Why This Matters

NASA Technical Assessment guidance places technical reviews within ongoing measurement and assessment: purpose, objectives, entrance/success criteria, team makeup, and action resolution are planned, while trends provide early warning. NASA's glossary distinguishes success criteria and Standing Review Boards; Product Verification describes tailored Test Readiness Reviews. Peer review guidance explicitly distinguishes inspections from milestone reviews, preventing defect finding from being confused with investment authority.

Independent review can improve challenge and accountability, but structure alone does not guarantee effectiveness. NASA's 2025 OIG report on Standing Review Board practices reinforces that independence, terms of reference, criteria, evidence access, governance, findings, and management response deserve continuing scrutiny. This module uses that public assessment as institutional evidence, not as proof about any local review.

Gate decisions occur under uncertainty. Waiting for certainty can destroy opportunity; proceeding without bounded evidence can lock in unsafe or unaffordable commitments. Good governance makes the trade explicit: which uncertainty remains, how it could affect outcomes, what work is permitted, which controls/conditions apply, who owns the risk, and what triggers reconsideration.

## Prerequisites and Retrieval

Before convening or passing a technical review/gate, retrieve:

1. governing lifecycle model, policy, contract/charter, review/gate name, exact decision question, decision and convening authorities, independence rules, prior decisions, and permitted outcomes;
2. terms of reference/review plan with purpose, scope, products/baselines, objectives, entrance/success criteria, tailoring rationale, evidence cutoff, agenda, membership, roles, access, conduct, outputs, schedule, and escalation;
3. stakeholder needs, intended use/ConOps, outcomes/MOEs, requirements, architecture/interfaces, design rationale, lifecycle/transition/retirement strategy, and configuration baseline;
4. technical maturity evidence across specialty domains, end/enabling products, technologies, manufacturing/supply, integration, verification/validation, operations/support, human systems, safety, security, data, facilities, and disposal;
5. technical performance measures and margins/trends, mass/power/capacity/reliability or domain budgets, model/measurement uncertainty, calibration, forecasts, thresholds, breaches, and corrective plans;
6. integrated cost/schedule/resource baseline, reserves/margins, assumptions, dependencies, critical path, staffing/skills, suppliers, facilities, uncertainty/confidence, and correlation with technical risk;
7. risk/opportunity/hazard/threat registers with causes, consequences, likelihood basis, controls, owners, trends, aggregate/common cause, residual risk, and acceptance authority;
8. verification/validation/acceptance matrices, evidence packages, anomalies/failures, waivers/deviations, open requirements/interfaces, change requests, technical debt, and lessons;
9. independent/team analyses, prior peer reviews, audits, test/readiness reviews, supplier reviews, assumptions, contradictory evidence, minority/dissenting positions, and information limitations;
10. next-stage plan: objectives, work breakdown, schedule, budget, people, facilities, supply, data, interfaces, configuration, reviews, decision points, risk retirement, and exit/success criteria;
11. candidate findings/recommendations/actions with evidence, significance, affected decision/criteria, owner, response, due date, closure evidence/authority, and consequences;
12. decision-record template with evidence baseline/date, criteria results, alternatives, assessment, recommendation, dissent, authority decision/rationale, accepted risk, conditions, permitted scope, actions, re-review/reopen triggers, and distribution/retention.

Perform a **decision-backward audit**: start with what changes if the authority says proceed, hold, redirect, or terminate. For every irreversible resource/risk/configuration transition, identify the evidence and success criterion that justify it. Material without a decision connection may be reference, not gate evidence.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish peer reviews, audits, readiness reviews, lifecycle reviews, independent assessments, and decision gates;
2. write a decision-centered review charter and non-circular entrance/success criteria;
3. tailor criteria and independence proportionately before outcome evidence is known;
4. assemble configuration-bound integrated technical, programmatic, operational, and lifecycle evidence;
5. select reviewer expertise and roles while managing conflicts and psychological safety;
6. conduct pre-review, review, caucus/deliberation, reporting, response, decision, and follow-up without suppressing dissent;
7. separate observations, findings, risks, recommendations, actions, conditions, and authority decisions;
8. assess technical margin/trend, cost/schedule/resource credibility, aggregate risk, and next-stage feasibility together without collapsing them into one score;
9. issue bounded proceed/conditional/hold/redirect/terminate decisions with enforceable conditions;
10. audit action closure, decision compliance, re-review triggers, and review-process effectiveness.

## Core Exposition

**Name the decision before the review.** “Conduct PDR” is an event, not a decision. State whether authority will establish a baseline, commit implementation resources, authorize test, enter production, deploy, extend operation, accept, or dispose. Define what proceeding permits and what remains prohibited.

**Choose the right review form.** Peer inspections find defects in a work product. Audits check compliance/process/records. Readiness reviews assess ability to conduct an activity. Lifecycle reviews assess integrated maturity. Independent assessments provide objective advice. Gates allocate authority/resources/risk. Combine evidence where efficient but preserve purposes and roles.

**Write criteria as evidence propositions.** “Requirements complete” is vague. Better criteria specify baselined stakeholder expectations, validated ConOps, atomic/traceable/verifiable requirements, resolved critical interfaces, bounded open items, approved changes, and evidence that omissions/conflicts were audited. Criteria should expose immaturity, not describe desired slide sections.

**Tailor prospectively.** Remove/add criteria based on lifecycle, product, delivery model, risk, regulation, quantity, reversibility, novelty and consequence before results are known. Record rationale and authority. Tailoring rigor is not lowering a bar to match the calendar.

**Establish entrance readiness.** Confirm stable/cutoff baselines, distributed material, evidence links/access, completed lower-level reviews, current metrics/risks, identified gaps, correct reviewers, time to prepare, and no blocking administrative/evidence issue. A review can be rescheduled or narrowed when entrance fails.

**Build an integrated evidence package.** Use concise narratives and dashboards with drill-down to requirements/models/analyses/raw results/configuration. Connect technical maturity to cost, schedule, supply, operations, safety/security and retirement. Declare data dates, uncertainty, assumptions, exclusions and changes since cutoff.

**Select reviewers for the system.** Cover mission/domain, architecture/interfaces, specialty engineering, verification, human/operations/support, manufacturing/supply, safety/security, cost/schedule/risk, data/configuration, and retirement. Include receiver/downstream perspectives. Document conflicts and independence; provide onboarding without coaching conclusions.

**Pre-review for discovery, not sanitization.** Give reviewers adequate preparation time, questions channels and direct evidence access. Resolve factual misunderstandings and obvious defects before the event while retaining issue history. Do not pressure reviewers to withdraw concerns because the team plans a later fix.

**Run the event around criteria and decisions.** Present changes, evidence, margins/trends, exceptions, assumptions, anomalies, risks, alternatives, and next-stage plan. Use questions to test causal reasoning and adequacy. Park deep defect resolution for technical working sessions when it obscures the gate decision, but capture it.

**Control late evidence and cognitive load.** Material introduced after the cutoff is identified, impact-screened, and either reviewed with adequate preparation or deferred; surprise evidence cannot silently redefine the baseline. Size agendas and sessions so reviewers can reason, inspect sources, and deliberate before fatigue or time pressure converts unresolved uncertainty into passive agreement.

**Keep epistemic categories distinct.** Observation: “thermal margin fell 30%.” Finding: “the current model and test correlation do not support the required hot-case margin.” Risk: possible performance loss. Recommendation: obtain correlated evidence/redesign. Action: named owner/date/deliverable. Decision: authority holds or conditions work. Conflation weakens accountability.

**Assess trends and margins, not colors.** A parameter inside threshold but converging rapidly toward it may be less healthy than a known breach with credible recovery. Show measurement/model basis, uncertainty, forecast, reserves, correlated budgets and decision thresholds. Do not average red safety with green documentation.

**Integrate technical and programmatic feasibility.** A technically mature design with no credible supplier, facility, staffing, schedule or operations plan is not ready. A budget-compliant plan with weak requirements/architecture is also not ready. Preserve dimensions and causal dependencies rather than one composite score.

**Deliberate independently and record dissent.** Reviewers distinguish factual corrections, requests for information, findings and recommendations. Support evidence links and significance. Record minority views and the team's response. Consensus can be useful but must not become a veto on documented concern.

**Separate recommendation from authority.** A board may recommend proceed, proceed with conditions, hold, redirect or terminate. The decision authority can differ, but must record rationale, accepted risks and response to material findings/dissent. Silence or applause is not approval.

**Make conditions executable.** Define permitted work and limits, owners, resources, due dates, evidence, reviewer/closure authority, dependencies and consequence of nonclosure. Conditions that must be met before irreversible work are true gates, not post-meeting action lists.

**Follow through and reopen when needed.** Track actions, verify corrections, update baselines/risks/plans, distribute decision records, and audit compliance. Material new evidence, assumption invalidation, trend breach, missed condition, configuration change or recurrence can trigger focused re-review. Do not wait for the next ceremonial milestone.

**Measure review effectiveness.** Examine issue discovery timing, decision reversals, recurrence, action quality/latency, downstream escapes, reviewer preparation/diversity, evidence access, dissent handling and value versus burden. Counting slides, attendees, actions or on-time gates can reward the wrong behavior.

The following fixture demonstrates only declared criterion-state gates.

<!-- bijux-verify: {"id":"technical-decision-gate-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"criteria=8\nsatisfied=6\nconditions=1\nblocking_gaps=1\nblockers=disposal_authority\ninitial_recommendation=hold\nafter_evidence_satisfied=7\nafter_evidence_conditions=1\nafter_evidence_blocking_gaps=0\nafter_evidence_recommendation=proceed_with_condition_requires_authority\nstatus=declared_gate_fixture_consistent\nevidence=synthetic_criterion_states_only\n","stderr":""}} -->
```python
criteria = {
    "stakeholder_outcomes": "satisfied",
    "requirements_baseline": "satisfied",
    "architecture_interfaces": "satisfied",
    "verification_strategy": "satisfied",
    "safety_security": "satisfied",
    "cost_schedule_resources": "satisfied",
    "supplier_condition": "condition",
    "disposal_authority": "blocking_gap",
}

def recommendation(records):
    blockers = [name for name, state in records.items() if state == "blocking_gap"]
    conditions = [name for name, state in records.items() if state == "condition"]
    if blockers:
        return "hold", blockers
    if conditions:
        return "proceed_with_condition_requires_authority", []
    return "proceed_requires_authority", []

initial, blockers = recommendation(criteria)
print(f"criteria={len(criteria)}")
print(f"satisfied={sum(state == 'satisfied' for state in criteria.values())}")
print(f"conditions={sum(state == 'condition' for state in criteria.values())}")
print(f"blocking_gaps={sum(state == 'blocking_gap' for state in criteria.values())}")
print("blockers=" + ",".join(blockers))
print("initial_recommendation=" + initial)

criteria["disposal_authority"] = "satisfied"
after, _ = recommendation(criteria)
print(f"after_evidence_satisfied={sum(state == 'satisfied' for state in criteria.values())}")
print(f"after_evidence_conditions={sum(state == 'condition' for state in criteria.values())}")
print(f"after_evidence_blocking_gaps={sum(state == 'blocking_gap' for state in criteria.values())}")
print("after_evidence_recommendation=" + after)
print("status=declared_gate_fixture_consistent")
print("evidence=synthetic_criterion_states_only")
```

The fixture cannot define adequate criteria, validate evidence, classify risk, assess independence, authorize a condition, or make a real decision. It only prevents a declared blocker from producing a proceed recommendation under its toy rules.

## Definitions and Notation

Let review $Q=(g,o,K,B,T,P)$ identify gate/decision $g$, objectives $o$, criteria $K$, evidence baseline $B$, terms/roles $T$, and review products $P$. Evidence quality includes relevance, provenance, configuration currency, completeness, uncertainty and independent challenge.

Let criterion state be $s_i\in\{\text{satisfied},\text{condition},\text{blocking gap},\text{not applicable approved},\text{not assessed}\}$. “Not assessed” cannot become satisfied. Condition $l=(owner,due,evidence,authority,restriction,consequence)$ is enforceable only when all elements are defined.

Decision record $D=(d,\alpha,B,R,A,L,X,\Delta)$ contains outcome, authority, evidence baseline, accepted risks, assumptions, conditions/actions, alternatives and dissent. It bounds permission $\Delta$ for next-stage work.

## Mechanisms, Invariants, or Proof Structure

A defensible review/gate argument follows this chain:

1. define decision, authority, alternatives, scope, permitted outcomes and irreversible commitments;
2. charter the review with prospective objectives, criteria, tailoring, evidence baseline, team/independence and products;
3. establish entrance readiness and distribute integrated configuration-bound evidence early;
4. review criteria, trends/margins, assumptions, uncertainty, anomalies, risks, feasibility and next-stage plan with relevant expertise;
5. preserve questions, findings, recommendations, contradictions, dissent and responsible-team responses;
6. integrate without collapsing technical/programmatic dimensions or averaging blockers;
7. issue recommendation separately from authority decision and record rationale/accepted risk;
8. make conditions/actions enforceable, control permitted work, verify closure and update baselines;
9. monitor triggers, re-review material change and audit review effectiveness.

The invariants are decision-centered purpose, prospective criteria, authoritative evidence, correct expertise, proportionate independence, trend/uncertainty visibility, dissent preservation, recommendation/decision separation, enforceable conditions, bounded permission, follow-through and reopenability.

## Alternatives and Trade-Offs

**Formal event versus continuous review.** Formal gates focus authority and records; continuous reviews find issues earlier. Use continuous evidence/peer challenge feeding deliberate commitment points.

**Independent board versus embedded peers.** Independence improves objective challenge; embedded peers know context. Combine independent assessment with direct technical access and responsible-team dialogue.

**One-step versus staged review.** One event is efficient; staged technical then integrated/programmatic assessment allows evidence maturation but risks inconsistent baselines. Freeze/trace changes between steps.

**Checklist criteria versus principle-based judgment.** Checklists expose omissions; principles handle novel systems. Use required evidence propositions plus documented expert judgment.

**Consensus versus recorded minority.** Consensus simplifies recommendations; minority views preserve uncertainty and weak signals. Never force unanimity by deleting dissent.

**Proceed with conditions versus hold.** Conditions sustain momentum where risk is bounded and work reversible; hold protects against irreversible commitment or missing authority/evidence. Define permitted scope and nonclosure consequences.

**Broad review versus focused special review.** Broad views expose interactions; focused reviews go deep. Trigger focused reviews without losing integrated system context.

**Reusable standard criteria versus tailored criteria.** Standards improve comparability; tailoring reflects product/lifecycle/risk. Preserve core governance and record every change.

## Failure Modes and Misconceptions

**“The review passed.”** The authority made a bounded decision; review findings and conditions can remain.

**“All entrance criteria met means ready to proceed.”** Entrance only means ready to review.

**“Green status means low risk.”** Basis, trend, uncertainty, correlation and exceptions determine meaning.

**“Independent means uninformed.”** Reviewers need context and direct evidence while retaining judgment separation.

**“More slides mean more rigor.”** Rigor is traceable evidence, reasoning, uncertainty and challenge.

**“No reviewer objected.”** Silence can reflect time, hierarchy, access or suppressed dissent.

**“Actions can close after proceeding.”** Only if authority defines condition eligibility, permitted work and consequences.

**“Cost already spent justifies continuation.”** Sunk cost does not establish prospective value or acceptable risk.

**“Rebaseline makes the project healthy.”** It changes the comparison baseline; causal variance and risk remain.

**“A gate guarantees the next stage.”** New evidence, invalid assumptions and change can reopen the decision.

## Worked Examples

### Example 1

A requirements review shows 98% approved requirements, but the missing 2% controls emergency shutdown and external authority. Count-based green status hides criticality. The gate holds baseline approval until authority, interface and verifiability are resolved or explicitly scoped out.

### Example 2

A design review receives polished thermal margins based on an uncorrelated model. Reviewers trace inputs, uncertainty and test correlation, finding hot-case margin unsupported. The finding is about evidence adequacy, not presentation quality; authority conditions fabrication that would not prejudice redesign.

### Example 3

A test readiness review finds the article/procedure ready but an instrument calibration expired and abort authority is unclear. Both are entrance/safety blockers. Schedule availability does not authorize the run; readiness is re-reviewed after evidence and roles are corrected.

### Example 4

A production readiness review sees a verified design but 45% pilot yield, unstable supplier process and missing trained inspectors. Product verification does not prove repeatable production. The decision redirects process/design maturity before rate commitment.

### Example 5

A deployment gate has one open documentation action and one unresolved data-loss failure. A single “yellow” category is misleading. Documentation may be conditional; data integrity is blocking unless bounded and authorized. Conditions are criterion-specific, not color-specific.

### Example 6

An independent reviewer dissents from the board's proceed recommendation because correlated schedule and technology risk exhaust margin. The minority evidence and management response enter the decision record. The authority may still proceed, but accepts the risk transparently and sets triggers.

### Example 7

A peer inspection finds defects in a security design. Management converts the meeting into a go/no-go decision, discouraging defect reports. Restoring separation lets trained peers record defects; a later security/readiness authority assesses corrected evidence and residual risk.

### Example 8

A service extension review emphasizes uptime while vendor support ends, key staff leave and disposal migration needs six months. Prospective mission value is assessed with supply/security/knowledge/retirement margin. “Still running” does not establish responsible extension.

### Example 9

A condition says “close interface issues before launch.” It lacks IDs, owners, evidence, authority and work restriction. The corrected condition lists affected interfaces, approved ICDs/tests, due date, closure board, prohibited integration and automatic gate reconvening.

### Example 10

A project passes a gate, then a supplier change invalidates qualification evidence. Configuration impact triggers a focused review rather than waiting for the next lifecycle event. Previous approval remains historical evidence, not permission for the changed baseline.

## Cross-Program Connections

- **Platform engineering:** architecture, security, production/deployment, operational readiness, migration and deprecation gates need adopter/operator evidence and reversible conditions.
- **API/service engineering:** contract readiness, load/failure testing, version coexistence, data migration, client support and SLO evidence feed deployment decisions.
- **Data engineering:** lineage/quality, model assumptions, population coverage, privacy, migration/reconciliation and reproducibility must be reviewable, not dashboard claims.
- **Object-oriented/functional programming:** code/design peer review finds defects; release/system gates additionally require integration, operations, security and lifecycle evidence.
- **Risk/decision analysis:** alternatives, uncertainty, value, sensitivity, correlated risks and information value structure recommendations while authority retains judgment.
- **Safety/security:** independent authority, noncompensatory criteria, dissent, waivers, residual risk and stop-work rules constrain gate outcomes.
- **Configuration/data management:** cutoff baselines, evidence provenance, changes between review steps, records, actions and decision history preserve auditability.
- **Organizational behavior:** hierarchy, incentives, psychological safety, groupthink, normalization and sunk-cost pressure affect what evidence reaches authority.

## References

1. NASA, [Technical Assessment, Systems Engineering Handbook section 6.7](https://www.nasa.gov/reference/6-7-technical-assessment/), accessed 2026-08-31.
2. NASA, [Decision Analysis, Systems Engineering Handbook section 6.8](https://www.nasa.gov/reference/6-8-decision-analysis/), accessed 2026-08-31.
3. NASA, [Technical Risk Management, Systems Engineering Handbook section 6.4](https://www.nasa.gov/reference/6-4-technical-risk-management/), accessed 2026-08-31.
4. NASA, [Technical Planning, Systems Engineering Handbook section 6.1](https://www.nasa.gov/reference/6-1-technical-planning/), accessed 2026-08-31.
5. NASA, [NASA Program/Project Life Cycle](https://www.nasa.gov/reference/3-0-nasa-program-project-life-cycle/), accessed 2026-08-31.
6. NASA, [Systems Engineering Handbook Glossary](https://www.nasa.gov/reference/appendix-b-glossary/), accessed 2026-08-31.
7. NASA, [Product Verification, including Test Readiness Reviews](https://www.nasa.gov/reference/5-3-product-verification/), accessed 2026-08-31.
8. NASA, [Guidance on Technical Peer Reviews and Inspections, Appendix N](https://www.nasa.gov/reference/appendix-n-guidance-on-technical-peer-reviews-inspections/), accessed 2026-08-31.
9. NASA, [Program Planning and Control Guidance Documents, including Standing Review Board Handbook](https://www.nasa.gov/ocfo/ppc-corner/ppc-guidance-documents/), updated 2026.
10. NASA Office of Inspector General, [NASA's Standing Review Board Practices, IG-25-009](https://oig.nasa.gov/wp-content/uploads/2025/07/final-report-ig-25-009-nasas-standing-review-board-practices.pdf), 2025.

## Exercises

### Exercise 1

Draft a charter and success criteria for a production readiness review of a safety-critical hardware/software product with two suppliers and a new factory.

### Exercise 2

A gate has 12 criteria: 8 satisfied, 2 conditions, 1 blocking gap and 1 not assessed. A dashboard assigns satisfied=1, condition=0.5, other=0 and reports 75%. Evaluate the arithmetic and decision meaning.

### Exercise 3

Design a test readiness review after one prior test failed from both setup and product anomalies. Define entrance evidence, roles, criteria and allowed outcomes.

### Exercise 4

An independent board recommends proceed, but one reviewer dissents about a correlated cost/schedule/technical risk. Define the decision and record process.

### Exercise 5

Convert “proceed with conditions” for a service migration into enforceable conditions and monitoring/re-review rules.

## Answers to the Exercises

### Answer 1

Decision: authorize controlled production ramp—not unrestricted rate production—for named design/process/factory/supplier baselines. Authority, conveners and review board are named. Scope includes product, production/test/inspection systems, supply, software build/release, workforce, quality, facilities, logistics, operations/support and safety/security. Material is configuration-frozen at a stated cutoff; later changes are identified.

Entrance criteria include approved design/requirements/interfaces, completed qualification and critical anomalies, pilot/first articles on intended processes, current yield/process/measurement data, supplier/factory audits, controlled work instructions/tooling/software, trained staff, calibrated inspection/test, nonconformance/CAPA, capacity/rate plan, supply/obsolescence, traceability, acceptance, safety/security, spares/support, and distributed evidence. Reviewers cover design, manufacturing/process, supplier quality, software/configuration, verification, safety/security, operations/support and cost/schedule.

Success criteria establish producible design; stable/capable critical processes with justified evidence; qualified suppliers and alternatives/controls; reproducible signed builds/configuration; trained workforce; ready tools/facilities/inspection; acceptable pilot yield/defect/rework and ramp model; closed critical anomalies; accepted residual risks; product/unit/lot acceptance and traceability; credible rate/cost/schedule; operational/support readiness; controlled change and rollback. Outcomes: authorize bounded ramp with limits, condition reversible work, hold, redirect design/process/supplier work, or terminate. Conditions identify units/rate, owners, evidence, closure authority and stop triggers.

### Answer 2

The score is $(8\times1+2\times0.5)/12=9/12=75\%$, so the arithmetic follows the dashboard rule. The decision meaning is invalid or at least insufficient. A blocking criterion and one not-assessed criterion cannot be averaged away by eight passes. Conditions also differ in eligibility, impact and enforceability; assigning each 0.5 has no evidence basis.

Report the state vector: 8 satisfied, 2 conditional candidates, 1 blocking gap, 1 not assessed, plus criticality, evidence and trend. Determine whether not-assessed is itself blocking and whether conditions are permitted with owners/restrictions/closure. Under the chapter's necessary rule, proceed is not supportable while a blocker exists. The authority can narrow the decision scope, obtain evidence, hold, redirect, or explicitly act under governing exception/risk rules; a percentage does not grant permission.

### Answer 3

Entrance evidence preserves the original failed run, exact article/build/configuration, procedure, environment, instruments/calibration, raw data/logs, chronology, setup deviation, product anomaly, causal/impact analysis, corrections, independent checks and regression plan. The revised procedure/configuration is controlled and dry-run; article state/pedigree and damage assessment are known. Facility, instrumentation, data, support equipment, operators, observers and abort/emergency roles are ready.

Separate setup correction from product correction; both require evidence. Criteria cover requirement/objective/oracle, article/configuration, procedure approvals, hazards/controls, environment, instrumentation range/accuracy/calibration, data capture/time, staffing/training, communications, abort limits/authority, anomaly/reporting, contingency/recovery, and post-test disposition. Include relevant independent safety/quality/test authority and product/domain experts; author/runner cannot self-authorize critical exceptions.

Outcomes are ready for exact scoped test, ready with pre-run conditions that do not permit test until closed, hold, or redesign/replan. A later pass preserves the failure and verifies predicted mechanisms plus risk-based regression. If evidence remains ambiguous, reduce scope or increase instrumentation rather than declaring the prior failure purely setup-related.

### Answer 4

Record the majority recommendation and the dissent separately, with evidence, assumptions, risk mechanism, correlations, consequences, likelihood/uncertainty and proposed discriminating information/controls. Give the responsible team a factual response and correction opportunity without requiring withdrawal. The chair verifies the dissent is accurately stated and routes it under the applicable escalation process.

The decision authority reviews the same baseline, alternatives and terms of reference; assesses whether cost, schedule and technical risks share causes or consume the same reserves; examines sensitivity and next-stage reversibility. Possible decisions include proceed with explicit accepted risk/triggers/reserves, narrow/resequence scope, obtain additional evidence, hold/redirect, or terminate. If proceeding against dissent, record rationale, risk owner, controls, margins, monitoring thresholds, conditions, permitted commitment and automatic re-review triggers. Disagreement is not erased after decision; new evidence can reopen it.

### Answer 5

Define each condition against a criterion. Example: before more than 5% traffic, complete reconciliation dry run R-17 with zero unexplained records and approval by data authority; before irreversible schema writes, demonstrate backup/restore and rollback within named RTO/RPO; before 50%, close severity-one security finding with independent retest; before old-system shutdown, show 100% approved clients migrated or formally excepted. Name exact old/new builds, schemas, regions, clients, data windows and evidence repositories.

Each condition has owner, resources, due date, verifier/closure authority, dependency, accepted residual risk, and consequence. Permit only reversible canary/cohort work within declared limits. Monitor data loss/duplication/reconciliation, errors/latency/capacity, identity/authorization, client versions, support incidents, rollback health and stakeholder outcomes with thresholds and abort authority. Preserve old service/data path until rollback expires under approval.

Missed condition, threshold breach, unclassified anomaly, configuration change, rollback failure or new critical evidence automatically pauses expansion and triggers focused re-review. The final decision record distinguishes review recommendation from migration authority, lists open conditions and accepted risk, and requires post-migration validation plus retirement verification before declaring transition complete.
