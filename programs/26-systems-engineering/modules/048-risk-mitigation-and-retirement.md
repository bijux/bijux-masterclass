---
module_id: SYSENG-048
program: Systems Engineering
level: 1
module_number: 48
title: Risk Mitigation and Retirement
status: complete
last_verified: 2026-08-31
---

# Risk Mitigation and Retirement

## One-Page Review

### Governing question

How can a systems team choose, implement, verify, and govern risk responses so that residual risk is understood and accepted by the right authority—and close a risk only when evidence satisfies predeclared retirement criteria?

### Essential definitions

- A **risk response** is an authorized action or decision intended to change a risk, improve knowledge, control exposure, or govern residual consequence.
- **Avoidance/elimination** changes objectives, architecture, scope, method, or exposure so the scenario source/path no longer applies; it may create new risks or lost benefits.
- **Mitigation/reduction** changes scenario likelihood, consequence, exposure, detectability, response time, or uncertainty through engineered or organizational controls.
- **Transfer/share** allocates specified financial, operational, or action responsibility to another party; system consequences and accountability do not disappear automatically.
- **Acceptance** is an authorized, documented decision to proceed with a stated residual risk after available net-beneficial actions and aggregate effects are considered.
- A **contingency** is a preplanned action taken if a trigger/event occurs or mitigation proves insufficient; it manages consequences or recovery rather than pretending the initiating risk vanished.
- A **leading indicator** provides evidence before or during causal progression; a **lagging indicator** records realized outcomes after they occur.
- A **trigger** is an observable, governed condition that initiates analysis, mitigation, contingency, escalation, stop-work, or reassessment.
- **Inherent/pre-response risk** describes the scenario before credited responses; **current risk** reflects controls/evidence now; **residual risk** remains after implemented and verified responses.
- **Secondary risk** is a new or changed risk caused by a response; **risk migration** shifts consequence across components, lifecycle stages, stakeholders, or domains.
- A **mitigation plan** maps causal mechanisms to actions, resources, schedule, owners, triggers, effectiveness measures, verification, residual analysis, contingency, and decision criteria.
- **Retirement/closure** is an authorized disposition supported by evidence that defined criteria hold—for example the condition/path no longer exists, scenario likelihood/consequence is below governed thresholds, or it has become an issue/successor record.
- A **closure package** preserves the original and final scenario, evidence, actions, results, residual/aggregate effects, approval, lessons, monitoring handoff, and reopening triggers.

### Central model, mechanism, or theorem

For risk scenario (s), control set (a), evidence (E), and baseline (B), compare conditional pre- and post-response profiles:

\[
R_0=(P(s\mid B,E),C(s\mid B,E),U_0),
\]

\[
R_a=(P(s\mid a,B,E'),C(s\mid a,B,E'),U_a).
\]

When probability and consequence are calibrated/cardinal on a common basis, a limited decision aid is

\[
NB(a)=E[C_0]-E[C_a]-Cost(a)-Secondary(a).
\]

Expected net benefit cannot by itself authorize safety, legal, ethical, security, or noncompensatory tradeoffs, and it must preserve dependence and uncertainty.

A retirement gate is a conjunction:

\[
Close(r)=K_{scenario}\land K_{implementation}\land K_{effectiveness}
\land K_{residual}\land K_{handoff}\land K_{authority}.
\]

Completing actions satisfies only part of this gate.

### Critical invariants

- Responses trace to the condition, event sequence, barriers, exposure, affected objectives, and consequence mechanisms of a current configured risk.
- Alternatives include avoidance, likelihood/consequence reduction, information, transfer/share, acceptance, monitoring, contingency, and combinations; the first proposed action is not assumed best.
- Every credited control has owner, resources, schedule/dependencies, entry/exit criteria, performance measure, evidence method, trigger, and configuration.
- Response effectiveness is forecast before approval and verified after implementation; activity completion is not risk reduction.
- Uncertainty, common cause, control reliability/degradation, human/organizational behavior, and model limitations accompany residual estimates.
- Secondary, transferred, migrated, aggregated, and portfolio risks are identified before response approval and tracked afterward.
- Mitigation, contingency, technical margin, management/schedule reserve, and acceptance are distinct and governed.
- Triggers are observable, timely relative to decision lead, assigned, tested, and linked to executable actions and authority.
- Acceptance identifies residual scenario, evidence, assumptions, validity period, aggregate effects, stakeholders/risk takers, concurrence, accountable authority, and conditions.
- Closure criteria are specific and measurable, preferably set before execution, and tied to objectives and evidence rather than matrix color alone.
- Retirement preserves history, accepted residuals, successor issue/risk links, monitoring ownership, lessons, approval, and reopening conditions.
- New evidence, change, control failure/drift, incident, near miss, trigger breach, or assumption invalidation reopens analysis without stigma.

### Common failures

Common failures include naming “monitor” as mitigation without decision logic; assigning a task list unrelated to causal mechanisms; claiming risk reduction when funding is approved; taking credit for an unimplemented or unverified control; using a passed nominal test despite adverse anomalies; reducing likelihood while increasing consequence; shifting burden to operators or vulnerable stakeholders; assuming insurance/contract transfer removes mission risk; counting the same control in baseline and mitigation; hiding contingency as mitigation; spending reserve without updating confidence; setting triggers after the threshold is already unrecoverable; declaring acceptance because the score is green; using unauthorized owners to accept safety/security risk; closing when actions finish; closing realized risks without issue links; deleting closed rows; and never reassessing controls after system or environment change.

### Compact example

A calibrated teaching scenario has pre-response probability 0.30 and consequence 20 cost units, expected 6.00. A mitigation costing 2 reduces the modeled residual to probability 0.10 and consequence 8, expected 0.80; nominal net expected reduction is 3.20. This arithmetic supports comparison but cannot prove the control, capture tail/non-cost consequences, or authorize acceptance. Retirement still requires implementation evidence, effectiveness verification, residual threshold/acceptance, contingency evidence, monitoring handoff, no unresolved anomaly, and approval.

### Connections

SYSENG-047 creates causal risk records. This module turns them into response, evidence, acceptance, and retirement decisions. SYSENG-049 preserves decision rationale and SYSENG-050 applies it to architecture choice. Requirements, architecture, interfaces, integration, readiness, verification/validation, configuration, cost/schedule forecasts, human factors, safety, security, operations, and stakeholder values shape both response effectiveness and residual risk.

## Governing Question

What action changes which causal part of the risk, how will the team know the change occurred, what new risks does the action create, what remains afterward, and who is accountable for deciding that the remaining exposure is acceptable or closable?

Risk management is not task management with colors. Installing a control changes the system configuration; testing it produces evidence; analyzing that evidence changes the risk model; authority then decides whether to continue, modify, accept, elevate, invoke contingency, or close. Conflating these steps rewards activity rather than outcome.

## Why This Matters

Mitigation consumes scarce cost, schedule, margin, attention, and opportunity. It can reduce one risk while increasing complexity, common cause, operator workload, supply dependence, environmental burden, or later lifecycle cost. Poor closure hides residual exposure and destroys learning. Good response planning makes tradeoffs explicit, produces discriminating evidence early enough to act, and protects fallback options.

NASA's current objectives-driven Risk Management Handbook integrates risk-informed direction setting with continuous identify–analyze–plan–track–control work. NPR 8000.4C distinguishes mitigate, accept, close, elevate, and other dispositions; requires mitigation effectiveness parameters, acceptance rationale/conditions/criteria, closure rationale/approval, aggregate risk consideration, and appropriate risk authority. It also recognizes that milestone decisions can implicitly accept risk.

NASA Technical Risk Management calls for monitoring response implementation, implementing mitigation and contingency on thresholds, continuing until residual risk/consequence is acceptable, communicating results, and capturing rationale and lessons. These principles generalize: a response deserves credit only to the extent that evidence shows it changes the scenario for the configured system and intended operating context.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. current risk statement/narrative, objective/requirement, configuration, causal/event model, likelihood/consequence/uncertainty, timeframe, dependencies, evidence, owner, and authority;
2. risk posture, tolerance, acceptance/elevation criteria, safety/security/legal/ethical rules, affected stakeholders/risk takers, dissent and concurrence process;
3. architecture/interfaces, lifecycle, operational scenarios, humans/organizations, suppliers, hazards/threats, controls/barriers, margins, issues/anomalies, and existing mitigations;
4. response candidates, models/prototypes/tests, effectiveness/reliability/degradation evidence, cost-loaded schedule, resources/facilities, procurement, change and configuration control;
5. triggers/indicators, telemetry/inspection/audits, contingency/recovery/rollback, stop criteria, reserves, fallback, and exercise results;
6. closure thresholds, verification/validation evidence, residual/aggregate analysis, acceptance records, monitoring handoff, lessons, retention, and reopening rules;
7. decision analysis, sensitivity/uncertainty, value of information, causal inference, verification, human factors, and benefit/cost concepts.

As a retrieval test, challenge “risk retired—mitigation complete.” Ask which scenario component changed; configured control; acceptance criteria; test/operational evidence; uncertainty/anomalies; current/residual/aggregate risk; secondary risks; contingency; monitoring owner; closure authority/rationale; and reopening trigger. If the only evidence is a checked task, retirement is unsupported.

## Learning Objectives

After completing this module, you should be able to:

1. formulate response objectives from a causal risk model and governed tolerance;
2. compare avoidance, reduction, information, transfer/share, acceptance, monitoring, contingency, and fallback alternatives;
3. design mitigation work with resources, schedule logic, triggers, effectiveness measures, verification, and change control;
4. distinguish activity, control implementation, control effectiveness, risk reduction, residual acceptance, and closure;
5. identify control failure/degradation, uncertainty, common cause, secondary risk, and risk migration;
6. design leading/lagging indicators and timely, tested triggers;
7. assess residual and aggregate risk without invalid ordinal arithmetic or double counting;
8. create traceable acceptance packages with correct authority, concurrence, stakeholder/risk-taker conditions, and validity limits;
9. establish and audit measurable retirement criteria, closure evidence, monitoring handoff, history, and reopening;
10. communicate response tradeoffs, dissent, residual ignorance, and learning proportionately.

## Core Exposition

**Revalidate the risk before planning.** Confirm objectives, baseline/configuration, condition, event sequence, asset, consequence, evidence, uncertainty, timing, dependencies, current controls, and authority. A response to an obsolete or vague record wastes resources and can create false confidence. Split or merge scenarios when mechanisms/owners differ or double counting exists.

**Define the response objective.** State the target change in likelihood, consequence, exposure, uncertainty, decision time, or recoverability; target date; evidence standard; residual tolerance; and decision enabled. “Reduce risk” is not measurable. A target matrix cell can route work but needs underlying physical/operational criteria.

**Generate response alternatives broadly.** Consider removing the condition; changing requirements/architecture/scope; reducing exposure/frequency/duration; preventing initiation; interrupting propagation; detecting earlier; limiting consequence; adding diversity/redundancy/isolation; improving procedures/training/staffing; qualifying suppliers; acquiring evidence; monitoring; transferring/sharing specified responsibilities; reserving resources; contingency/recovery; staged/reversible deployment; accepting; or stopping. Include do-nothing/current plan as comparison.

**Map actions to causal mechanisms.** A control should identify which condition, branch probability, exposure, barrier, consequence pathway, detection time, or recovery mechanism it changes. Map multiple controls into a bow-tie/event/fault/causal model. Do not multiply generic “risk reduction percentages” without dependence and common-cause analysis.

**Compare alternatives across outcomes.** Evaluate technical effectiveness, safety/security, affected stakeholders, cost/schedule, integration, readiness, control reliability, implementation risk, lifecycle operations/maintenance, environment, legal/regulatory constraints, reversibility, uncertainty, information value, and opportunity cost. Noncompensatory requirements and acceptance authority remain visible.

**Separate mitigation from information.** A prototype/test/analysis may reduce epistemic uncertainty without changing physical risk. That can be valuable if it changes a decision before commitment. A redesigned barrier may change physical likelihood/consequence while leaving uncertainty large. State which effect is expected and how both will be assessed.

**Build the plan as controlled work.** For each action record ID, causal purpose, owner and technical authority, WBS/schedule activity, resources/budget/facility/supplier, dependencies, configuration, entrance criteria, procedure, output/evidence, acceptance/effectiveness criteria, due/decision date, indicators/triggers, contingency, secondary-risk review, and reporting. Protect analysis/rework time after tests.

**Model response timing.** A mitigation that completes after the risk decision or possible event is ineffective for that exposure. Compare action lead time, information arrival, decision deadline, scenario onset (“sunrise”), consequence horizon, fallback expiry, and recovery duration. Place triggers early enough for action plus margin.

**Define effectiveness measures before implementation.** Measures can include physical margins, failure/detection probabilities, test outcomes, defect/escape rates, supplier process capability, schedule float/confidence, response time, operator workload/error, control coverage, recovery time/objective, environmental release, or affected-group outcomes. Define population, uncertainty, thresholds, and evidence.

**Verify implementation separately.** Inspection/configuration records show the control exists as designed. Verification demonstrates specified control behavior. Validation/operational evidence supports intended risk reduction in context. A firewall installed, valve added, staff trained, or test written is implementation—not necessarily effective control under representative conditions.

**Challenge control reliability and common cause.** Controls fail, drift, are bypassed, become obsolete, share power/software/operators/suppliers, or create mode confusion. Model diagnostic coverage, proof-test intervals, maintenance, latent failures, cyber compromise, human response, and dependencies. Redundant identical controls can share the initiating failure.

**Identify secondary and migrated risks.** A schedule acceleration can increase rework/fatigue; redundancy can add interfaces/common-mode software; stronger security can delay emergency access; supplier diversification can vary quality; environmental mitigation can shift waste communities; automation can change human workload and skill. Add linked records before taking net credit.

**Credit controls once.** Define whether baseline likelihood/consequence already includes current controls. Distinguish inherent, current, planned, and residual profiles. Avoid counting a barrier in both base model and mitigation reduction or in several dependent risk rows. Maintain configuration/evidence identity across the risk model and integrated cost/schedule/performance forecast.

**Design leading and lagging indicators.** Leading indicators track conditions/barriers: technical margin trend, overdue inspection, supplier yield, unresolved interface defects, forecast threshold, staffing/fatigue, certificate expiry. Lagging indicators track failures/incidents. Indicators need definition, source, quality, cadence, threshold/hysteresis, owner, access, action, and false-positive/negative consequences.

**Engineer triggers and response playbooks.** State observable condition, confirmation, authority, notification, immediate action, resource/fallback, stop/rollback, escalation, record, and recovery. Exercise contingencies in representative simulations/drills/tests; validate timing, access, human coordination, data and alternatives. A trigger without an executable action is an alarm, not control.

**Use contingency appropriately.** Contingency manages an occurred event or imminent threshold; it may limit consequence or recover objectives. It does not reduce pre-event likelihood unless its existence changes behavior/exposure. Define when mitigation transitions to contingency and link realized issues. Reserve enables action but does not itself mitigate.

**Update residual risk from evidence.** Reestimate scenario branches, consequence, uncertainty, timeframe, dependencies and aggregate effects using the implemented configuration and verified results. Compare planned versus observed effectiveness and investigate discrepancy. Do not tune scales merely to reach a closure cell.

**Assess aggregate and portfolio effects.** Check shared resources, common controls, correlated scenarios, transferred provider risks, accepted residuals, reserves, and simultaneous stresses. Several individually acceptable risks may be unacceptable together. Conversely, duplicate risk rows should not inflate exposure. Elevate to authority capable of portfolio choice.

**Make acceptance explicit.** Package current/residual scenario, objectives, evidence/uncertainty, controls, alternatives and net-beneficial mitigation, aggregate effects, consequences/distribution, validity period/configuration, contingency, monitoring, affected stakeholders/risk takers, concurrence/dissent, criteria, and authority. “Below threshold” establishes who may decide, not automatic acceptance.

**Recognize implicit acceptance.** Architecture freeze, launch/release, delivery, waiver, reduced testing, reserve allocation, or schedule commitment can accept risks. Trace these decisions to the risk posture and record rationale/accountability. Provider acceptance does not bind an acquirer automatically; delivery transfers outstanding management responsibility only through governed acceptance.

**Predeclare retirement criteria.** Criteria may require removal of initiating condition/path; verified likelihood/consequence below threshold; completed observation window; requirements/margins met; anomalies/issues resolved; residual/aggregate risk accepted; successor risks/issues linked; contingency tested; monitoring transferred; documents/configuration updated; lessons captured; and approval. Tailor to scenario and law/policy.

**Distinguish closure reasons.** Close because condition no longer exists; scenario is impossible under current baseline; likelihood/consequence is below closure criteria with evidence; event occurred and is now an issue with successor risks; risk merged/split/transferred/elevated with linked active records; or lifecycle ended with disposition. The code/reason determines interpretation and reopening.

**Assemble the closure package.** Preserve original/latest statements, configuration, history, analyses, actions, implementation and effectiveness evidence, anomalies, residual/aggregate profile, acceptance, open secondary risks/issues, contingency/monitoring handoff, lessons, closure rationale/code, approvals, and reopening triggers. Closed does not mean secret or deleted.

**Audit retirement independently.** Check criteria were not weakened after results, evidence covers representative conditions and duration, failures/anomalies are resolved, owners/authority concur, dependent risks are updated, residual risk is not hidden, and monitoring has resources. Sample closed risks after time to assess recurrence/calibration.

**Reopen without blame.** Reopen or create linked risk when condition/evidence/configuration/objective/environment changes, controls degrade, trigger breaches, near miss/incident occurs, residual exceeds criteria, or new causal understanding emerges. Reopening is a healthy control-loop result, not failure of reporting.

**Measure burn-down honestly.** Track verified change in likelihood/consequence/uncertainty, margin, trigger health, control reliability, action effectiveness, residual exposure, and forecast impact. Do not use actions closed, dollars spent, or risk rows removed as proxies. Show planned versus actual trajectory and reasons.

The following checker demonstrates expected-value comparison and a separate conjunctive retirement review. Its numbers are declared teaching inputs, not an accepted real risk model.

<!-- bijux-verify: {"id":"risk-response-retirement-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"baseline_probability=0.300\nbaseline_consequence=20.0\nbaseline_expected=6.00\nresidual_probability=0.100\nresidual_consequence=8.0\nresidual_expected=0.80\nmitigation_cost=2.00\nnet_expected_reduction=3.20\nclosure_criteria_met=6\nclosure_criteria_required=6\ncontingency_tested=1\ndecision=eligible_for_retirement_review\nevidence=declared_scenario_only\n","stderr":""}} -->
```python
baseline = {"probability": 0.30, "consequence": 20.0}
residual = {"probability": 0.10, "consequence": 8.0}
mitigation_cost = 2.0
criteria = {
    "implementation_verified": True,
    "effectiveness_verified": True,
    "residual_within_threshold": True,
    "no_unresolved_anomaly": True,
    "monitoring_handoff": True,
    "authority_review_ready": True,
}
contingency_tested = True
baseline_expected = baseline["probability"] * baseline["consequence"]
residual_expected = residual["probability"] * residual["consequence"]
net = baseline_expected - residual_expected - mitigation_cost

print(f"baseline_probability={baseline['probability']:.3f}")
print(f"baseline_consequence={baseline['consequence']:.1f}")
print(f"baseline_expected={baseline_expected:.2f}")
print(f"residual_probability={residual['probability']:.3f}")
print(f"residual_consequence={residual['consequence']:.1f}")
print(f"residual_expected={residual_expected:.2f}")
print(f"mitigation_cost={mitigation_cost:.2f}")
print(f"net_expected_reduction={net:.2f}")
print(f"closure_criteria_met={sum(criteria.values())}")
print(f"closure_criteria_required={len(criteria)}")
print(f"contingency_tested={int(contingency_tested)}")
eligible = all(criteria.values()) and contingency_tested
print("decision=" + ("eligible_for_retirement_review" if eligible else "continue_management"))
print("evidence=declared_scenario_only")
```

“Eligible for retirement review” is deliberately not automatic closure. Appropriate authority must examine assumptions, non-cost consequences, aggregate risk, dissent, policy and evidence.

## Definitions and Notation

Let scenario (S), response alternative (a\in A), baseline/configuration (B), objectives (O), evidence before/after (E,E'), likelihood (P), consequence vector (C), uncertainty (U), secondary-risk set (Q_a), cost/schedule/resource impact (K_a), and authority (D).

Risk state transition:

\[
R_0=(S,P_0,C_0,U_0,B,E)\xrightarrow{implement(a),verify(E')}
R_a=(S',P_a,C_a,U_a,B',E').
\]

The arrow requires evidence and can change the scenario/configuration, not merely its score.

For scalar cardinal consequences under justified probability:

\[
\Delta E=\sum_sP_0(s)C_0(s)-\sum_sP_a(s)C_a(s).
\]

Decision comparison includes implementation cost and secondary/portfolio consequences, with noncompensatory constraints separate.

Trigger (g_j) at time (t):

\[
g_j(X_t,E_t)\ge h_j\Rightarrow action_j,
\]

with observable (X_t), threshold/hysteresis (h_j), data quality, owner, decision lead and tested action.

Retirement record:

\[
Retire(r)=(criteria,evidence,residual,aggregate,acceptance,handoff,history,reopen).
\]

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—causal response framing.** Revalidate risk and define measurable target change, time, evidence, residual tolerance and authority.

**Mechanism 2—alternative and plan design.** Compare avoidance/reduction/information/transfer/acceptance/contingency/fallback; map selected actions to mechanisms, work, resources and triggers.

**Mechanism 3—implementation and effectiveness evidence.** Control configuration, verify installation/behavior, validate representative risk reduction and update uncertainty.

**Mechanism 4—residual and aggregate governance.** Identify secondary/migrated/common-cause risks, update joint profile, exercise contingency and obtain authorized acceptance/elevation.

**Mechanism 5—retirement and learning.** Apply predeclared conjunctive criteria, preserve closure package/handoff/history, independently audit and reopen on evidence/change.

No response proves zero risk. Evidence can support bounded reduction or closure under current conditions; resilience and monitoring address residual and omitted mechanisms.

## Alternatives and Trade-Offs

**Avoidance** can remove a scenario but sacrifice capability/value or move risk. **Mitigation** preserves objectives but costs resources and may fail/degrade.

**Prevention** reduces initiation likelihood. **Consequence limitation/recovery** accepts initiation possibility but changes outcomes. Defense in depth may combine both with independence review.

**Information actions** improve decisions without necessarily changing physical exposure. **Direct controls** change exposure but may be poorly targeted under uncertainty.

**Transfer/share** can allocate financial/action responsibility. **Local retention** preserves control. Neither automatically changes mission/system consequence.

**Early robust action** protects schedule and adverse outcomes but can overinvest. **Adaptive/staged action** learns before commitment but needs observability, reversibility and decision lead.

**Acceptance** avoids disproportionate mitigation. **Further reduction** may be mandatory or net-beneficial. Authority and affected-risk-taker conditions constrain tradeoffs.

## Failure Modes and Misconceptions

**“Mitigation complete means risk reduced.”** Completion proves activity; effectiveness evidence supports changed risk.

**“Monitoring is mitigation.”** Observation changes outcomes only when linked to timely, effective action.

**“Redundancy always reduces risk.”** Shared design, power, software, maintenance or environment can create common failure and complexity.

**“Transfer removes the risk.”** Contracts/insurance shift specified burden; objectives can still fail.

**“Contingency lowers likelihood.”** Usually it changes consequence/recovery after trigger; state causal credit precisely.

**“Below acceptance threshold means accepted.”** The threshold identifies authority/routing; a decision and rationale remain required.

**“A green residual score permits closure.”** Criteria, evidence, aggregate effects, handoff and approval are needed.

**“Closing deletes the record.”** History, residual acceptance, lessons and reopen triggers must remain.

**“Reopening proves the prior team failed.”** Conditions and evidence evolve; reopening is expected feedback.

**“Burn-down is the number of closed actions.”** Risk outcome evidence, not administrative throughput, measures reduction.

## Worked Examples

### Example 1

**Task versus effectiveness.** A redundant sensor is installed. Implementation passes inspection, but common software filtering rejects both sensors identically under icing. Risk credit waits for representative integrated evidence and common-cause analysis.

### Example 2

**Information action.** A prototype does not reduce battery thermal propagation but narrows uncertainty and shows architecture A cannot meet the safety constraint. Its value is an early decision to change architecture, not a fictitious likelihood decrease.

### Example 3

**Timeliness.** Alternate supplier qualification completes two months after the last date to preserve launch. It cannot mitigate that launch exposure unless schedule/architecture changes. Preserve it for later units while selecting a timely response now.

### Example 4

**Secondary risk.** Tight security lockout reduces unauthorized access but can delay emergency operator intervention. Analyze threat reduction, emergency consequence, human workflow, override controls, audit and authority together.

### Example 5

**Transfer.** A fixed-price supplier absorbs redesign cost, but late delivery still affects integration and mission. Track contractual cost allocation and technical/schedule consequence separately; acquirer acceptance remains.

### Example 6

**Trigger design.** Schedule float below 20 days triggers alternate test-facility reservation requiring 15-day lead plus 3-day decision. A 10-day trigger would be too late. Verify data cadence, authority, funds and facility availability.

### Example 7

**Contingency exercise.** Disaster recovery documentation exists, but an exercise finds credentials unavailable during network isolation. The contingency is not credited until access, timing, data integrity and roles pass representative evidence.

### Example 8

**Implicit acceptance.** A release board waives two boundary tests to meet date. It records the resulting safety/security/operational scenarios, evidence limits, affected authority, contingency/monitoring and rationale; “schedule decision” does not hide risk acceptance.

### Example 9

**Closure after occurrence.** Supplier insolvency occurs. Close the original occurrence risk with reason “realized/converted,” link the procurement issue, alternate-source schedule/cost risks and lessons. Do not mark it mitigated.

### Example 10

**Reopening.** A closed corrosion risk relied on indoor use; deployment changes to coastal outdoor sites. Reopen/clone for the new configuration, preserve old closure validity, and reassess material/coating/inspection evidence.

## Cross-Program Connections

**Platform engineering.** Responses include isolation, quotas, redundancy/diversity, staged rollout, rollback, SLO triggers, capacity reserve, provider alternatives and incident exercises; each can create operational complexity.

**API and service engineering.** Versioning, idempotency, timeouts/circuit breakers, authentication, compatibility tests, canaries and rollback change coupled client/dependency risks and need representative evidence.

**Data engineering.** Replay, lineage, validation, dual writes, backups, privacy controls, schema gates and reconciliation require tested recovery, correctness and secondary cost/latency analysis.

**Object-oriented programming.** Encapsulation/refactoring, dependency pinning, tests, feature flags and rollback can reduce change risk but add abstraction, compatibility and operational burden.

**Functional programming.** Types/effect boundaries, immutability, property tests and staged migration can constrain failure paths but do not remove runtime, integration, team or operations risk without evidence.

## References

1. NASA, *Risk Management Handbook Version 2.0, Part 1*, NASA/SP-20240014019, 2024. <https://ntrs.nasa.gov/citations/20240014019>
2. NASA, *Risk Management Handbook Version 2.0, Part 2*, NASA/SP-20240014326, 2024. <https://ntrs.nasa.gov/citations/20240014326>
3. NASA, *NPR 8000.4C Appendix A: Risk Dispositions, Acceptance, and Criteria*. <https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_8000_004C_&page_name=AppendixA>
4. NASA, *NPR 8000.4C Chapter 3: Risk Decisions, Mitigation, Closure, and Acceptance*. <https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_8000_004C_&page_name=Chapter3>
5. NASA, *NPR 8000.4C Chapter 2: Roles, Concurrence, and Risk Takers*. <https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_8000_004C_&page_name=Chapter2>
6. NASA, *Systems Engineering Handbook, Section 6.4: Technical Risk Management*, current web edition. <https://www.nasa.gov/reference/6-4-technical-risk-management/>
7. NASA Safety and Mission Assurance, *Risk Management*, current policy/guidance index. <https://sma.nasa.gov/sma-disciplines/risk-management>
8. NASA Goddard, *Guideline for Performing Risk Assessments*, GSFC-HDBK-8005 Rev. A, active 2024. <https://standards.nasa.gov/node/1951>
9. NASA, *NPR 8000.4C Chapter 1: Objectives-Driven Risk Management Requirements*. <https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_8000_004C_&page_name=Chapter1>
10. NASA Software Engineering Handbook, *SWE-086 Continuous Risk Management*. <https://swehb.nasa.gov/spaces/SWEHBVB/pages/32604571/SWE-086+-+Continuous+Risk+Management>

## Exercises

### Exercise 1

A scenario has calibrated probability 0.25 and consequence 40 cost units. Response A costs 3 and changes probability to 0.10 and consequence to 25. Response B costs 5 and changes probability to 0.05 and consequence to 20. Compute simple expected profiles and nominal net expected reductions. State why this does not choose the response.

### Exercise 2

Design a mitigation/contingency plan for a single-source component whose qualification and delivery threaten an integration date. Cover causal action, schedule lead, supplier evidence, alternate source, design accommodation, triggers, reserves, secondary risks, effectiveness and closure.

### Exercise 3

Critique a risk closed because “training delivered, likelihood now green.” Specify the evidence and governance needed for mitigation credit, residual acceptance and retirement when the scenario concerns operator response during a rare emergency.

### Exercise 4

Audit a portfolio where each project accepts several residual risks below local thresholds, but all depend on the same cloud provider, identity service, staffing pool and recovery site. Design aggregate analysis and elevation.

### Exercise 5

Design mitigation and retirement governance for wildfire smoke risk in public schools, including air quality sensing/forecasting, HVAC/filtration, building variation, outdoor activity, transport, power loss, staff/families, disability/health needs, procurement/maintenance, contingency, equity, evidence, authority and reopening.

## Answers to the Exercises

### Answer 1

Baseline expected consequence is

\[
0.25(40)=10.
\]

Response A residual expected consequence is (0.10(25)=2.5). Nominal net expected reduction after action cost is

\[
10-2.5-3=4.5.
\]

Response B residual expected consequence is (0.05(20)=1.0), with nominal net expected reduction

\[
10-1-5=4.0.
\]

On this narrow scalar expected-cost model A is larger by 0.5, but it does not select A. Review probability/consequence uncertainty and dependence, tails, technical/safety/security/human/environmental outcomes, implementation time, control reliability, secondary risks, reversibility, affected stakeholders, constraints, information value, aggregate exposure and authority. If consequence units are not cardinal/commensurate or probabilities are not calibrated, the arithmetic is not valid. A response may be mandatory even with negative scalar net benefit.

### Answer 2

Revalidate condition: sole source, unfinished process/product qualification, lead-time distribution, component function/interfaces, integration entry, current inventory, supplier evidence and consequences. Response branches include supplier process support and witnessed qualification; early long-lead order; alternate-source screening/qualification; interface/architecture accommodation for both; buffer inventory; resequenced integration using simulator/emulator; requirement/descope; and protected fallback decision.

Build schedule logic from evidence dates, anomaly analysis/retest, manufacturing lots, transport/acceptance, alternate-source lead, redesign/interface freeze and integration. Set triggers before fallback expiry—for example qualification yield/critical test by a review date or predicted delivery consuming declared float. Name decision authority, funds/reserve, supplier/acquirer owners and notification. Contingency covers late/nonconforming units: simulator use, resequence, alternate install, rollback/repair and commitment escalation.

Verify not just purchase orders but qualification criteria, process capability/yield, configured-unit acceptance, interface/performance/environment tests, delivery evidence and integrated behavior. Analyze secondary risks: alternate quality/configuration, dual-interface complexity, rushed verification, inventory obsolescence, supplier data rights and common upstream subtiers. Update cost/schedule/performance confidence and aggregate supplier risks.

Closure requires current condition/path eliminated or residual below governed threshold with representative evidence, no unresolved anomalies, integration evidence, accepted remaining supplier/dual-design risks, contingency tested, monitoring/supplier surveillance handed off, history/lessons and authority approval. A delivery alone does not close lifecycle obsolescence or quality risk; link successor records.

### Answer 3

Training delivery proves attendance/content distribution at most. It does not show retention, recognition, decision, communication, physical access, team coordination or correct action during rare stressed conditions. Check role/task analysis, representative emergency scenarios, accessibility/language, fatigue/workload, turnover, procedures/tools, alarm quality, authority, timing, common failures, and consequence.

Predefine observable performance: correct detection/decision/action, response time, errors/omissions, coordination, workload, recovery and subgroup/shift/site results with uncertainty. Use simulations/drills and, where safe/ethical, operational evidence; independent observers; configured procedures/tools; surprise/retention repeats; anomaly analysis; and corrective retraining/redesign. Training may reveal that alarm/interface/staffing/authority—not knowledge—is the causal bottleneck.

Mitigation credit follows verified representative performance and updated likelihood/consequence/uncertainty, including control degradation and turnover. Residual acceptance identifies rare-event evidence limits, affected risk takers, contingency, monitoring/drill cadence, aggregate staffing risks, concurrence and authorized rationale. Retirement requires predeclared criteria, no unresolved adverse trials, monitoring handoff, successor risks/issues, retained records, approval and reopen triggers for staff/procedure/system/environment/incident changes. A green ordinal cell cannot replace this evidence.

### Answer 4

Local threshold compliance does not establish aggregate acceptability. Build a dependency graph linking every project scenario to cloud region/control plane, identity, staffing skills/on-call rotations, network/power and recovery site. Reconcile baselines, horizons, probabilities, consequence units and current controls; remove duplicate rows; identify simultaneous demand, common cyber/configuration faults, provider outage, regional hazard and recovery-contention scenarios.

Use joint/conditional models where evidence supports them and stress/bounding scenarios otherwise. Evaluate correlated service loss, queue/recovery sequencing, staff overload, site capacity, data consistency, security and contractual limits across mission/safety/cost/schedule/stakeholder objectives. Test whether credited redundancy shares provider, identity, people, tooling or facility. Exercise multi-project recovery rather than isolated plans.

Aggregate current and residual profiles, reserves/capacity, decision lead, priority conflicts and accepted-risk conditions. Elevate to portfolio/acquirer authority able to allocate diversity, capacity, identity isolation, cross-training, alternative recovery, provider negotiation and project priority. Preserve project owners/actions and linked parent risks. Revisit every local acceptance and milestone decision with aggregate evidence, formal dissent/concurrence and appropriate security/safety authority; do not average or sum ordinal scores.

### Answer 5

Define objectives by building/population/time: keep indoor particulate exposure within public-health requirements, protect students/staff—especially respiratory/cardiovascular/disability needs—maintain learning/access and safe transport, communicate accurately, and avoid unequal closures/burdens. Map smoke scenarios, outdoor air, building leakage/HVAC, filter capacity/fit, sensor/forecast error, occupancy/activity, power, maintenance/procurement, staffing, transport and compound heat/fire/outage.

Responses include source/forecast/sensor validation; building-specific HVAC assessment, sealing and MERV/portable filtration compatible with airflow; clean-air rooms; preventive filter inventory/change/inspection; outdoor activity thresholds; schedule/remote/relocation alternatives; transport protocols; health plans/medication access; multilingual accessible communication; worker protection; power/backup; and coordination with public health. Do not assume one filter or threshold fits every building or person.

Measure indoor/outdoor PM by calibrated/located sensors, airflow/pressure, filter status, exposure duration, attendance/access, symptoms/health-service demand, response timing and affected-group outcomes with privacy. Verify installation and representative smoke-load effectiveness, HVAC safety, noise/accessibility, maintenance and human procedures. Analyze secondary risks: reduced ventilation/CO2/heat, electrical/fire/trip hazards, noise, inequitable remote-learning access, family work burden, supply waste and staff workload.

Triggers combine forecast, outdoor/indoor readings, equipment/power state and health guidance with confirmation, hysteresis, authority and early lead. Contingencies cover HVAC/filtration/power/sensor failure, extreme smoke, evacuation/closure/relocation, transport and medically vulnerable support; exercise them. Maintain reserves and alternate suppliers without calling them mitigation until actionable.

Acceptance/closure authority includes school/public-health/facilities/emergency governance and applicable regulators, with affected staff/family/student and disability/community input; individual schools cannot accept public-health exposure outside authority. Retirement after a season or action requires building-specific evidence, resolved anomalies, residual/aggregate exposure assessment, accepted conditions, maintained equipment/monitoring handoff, contingency readiness, lessons and records. Reopen for smoke/health thresholds, building/HVAC/occupancy, sensor, filter/supplier, power, regulation, inequitable outcome, near miss or incident change. Seasonal end closes an exposure window but not the recurring source risk; retain a monitored recurring record.
