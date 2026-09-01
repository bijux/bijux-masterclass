---
module_id: SYSENG-097
program: Systems Engineering
level: 2
module_number: 97
title: Organizations as Part of the System
status: complete
last_verified: 2026-09-01
---

# Organizations as Part of the System

## One-Page Review

### Governing question

How can engineers model and improve organizational goals, authority, resources, information, incentives, coordination, and learning as causal parts of a software-intensive system rather than treating them as external context or explaining failure with the word “culture”?

### Essential definitions

- An **organization** is a structured arrangement of participants, roles, authority, resources, routines, information flows, incentives, and boundaries formed to pursue goals.
- **Organizational control** is the process by which goals and constraints are communicated, action is authorized and resourced, performance is observed, and deviations are corrected or escalated.
- A **decision right** specifies who may decide, approve, veto, waive, accept risk, allocate resources, or change a rule for a defined scope.
- **Accountability** is an answerable obligation for an outcome or decision supported by commensurate authority, information, capability, and resources; it is not merely a name in a matrix.
- An **incentive** is a material or social consequence that changes the relative attractiveness of actions, including targets, budgets, promotions, penalties, reputation, and workload relief.
- **information attenuation** is the loss, delay, filtering, aggregation, or reframing of decision-relevant information as it crosses roles or boundaries.
- **goal conflict** occurs when participants must trade among objectives such as safety, service, legality, security, fairness, cost, and schedule without a feasible way to satisfy all of them.
- **organizational drift** is gradual movement of actual practice, margins, or norms away from intended constraints through repeated local adaptation and normalized success.
- **psychological safety** is a shared belief that interpersonal risk-taking such as asking, disagreeing, or reporting is acceptable; it does not remove performance standards or decision authority.
- A **learning loop** converts observations, anomalies, incidents, and successful adaptations into revised models, controls, resources, and verified action.

### Central model, mechanism, or theorem

For an organizational obligation $o$, define the support vector

$$
S(o)=\langle G,R,A,I,K,F,E\rangle,
$$

where $G$ is the governing goal or constraint, $R$ a responsible role, $A$ usable authority, $I$ timely information, $K$ capability and resources, $F$ feedback about effect, and $E$ enforcement or escalation. A necessary feasibility gate is

$$
feasible(o)\Rightarrow G\land R\land A\land I\land K\land F\land E.
$$

The conjunction is not sufficient. Each predicate may be falsely asserted, conflicting obligations may interact, informal work may differ, and outcomes remain uncertain. The model prevents a review from calling a control implemented when responsibility lacks the means to act or learn.

### Critical invariants

- Place boards, executives, regulators, customers, suppliers, managers, teams, operators, and support functions inside the causal boundary when their decisions affect outcomes.
- Connect every critical obligation to a legitimate goal, accountable role, usable authority, information, capability, resources, feedback, and escalation.
- Separate responsibility from authority and accountability from blame; assigning an owner does not create capacity or control.
- Model conflicting goals, incentives, budgets, schedules, staffing, contracts, metrics, and production pressure as system inputs.
- Trace information upward, downward, and laterally, including delay, aggregation, filtering, privacy, classification, and dissent.
- Design cross-boundary coordination, precedence, incident command, handoffs, veto, and dispute resolution before emergencies.
- Protect reporting and challenge while retaining competence, verification, and consequence-appropriate accountability.
- Study formal structures and informal networks, workarounds, expertise, shadow systems, and actual decision paths.
- Distinguish leading conditions from lagging outcomes; incident absence may reflect low exposure, hidden harm, adaptation, or luck.
- Investigate control interactions and organizational conditions rather than selecting one root cause or one negligent actor.
- Bind assurance to the actual organization, suppliers, contracts, staffing, leadership, configuration, jurisdiction, and period.
- Reassess after reorganizations, outsourcing, mergers, leadership changes, budget shifts, policy changes, incidents, or material technical evolution.

### Common failures

Common failures include drawing an organization chart as if it were a control model; assigning responsibility without authority or funding; using a RACI table as proof of coordination; setting local targets that undermine system constraints; suppressing bad news through punishment or impossible metrics; treating all violations alike; calling every problem cultural; assuming executive policy reaches field work unchanged; centralizing approval without response capacity; outsourcing execution while retaining invisible risk; investigating the last actor only; counting reports without closing learning loops; performing a reorganization as a technical control; and claiming maturity from documents, training completion, or an incident-free interval.

### Compact example

A synthetic ledger checks three organizational controls across owner, authority, resources, feedback, and escalation. Fourteen of fifteen fields are present, but supplier-revocation escalation is missing. The gate rejects organizational readiness even though 93% of cells pass. This demonstrates a noncompensable metadata check only; it does not prove that declared roles are legitimate, capable, trusted, or effective in practice.

### Connections

This module builds on stakeholder analysis, governance, function allocation, risk, safety, verification, operations, resilience, systems of systems, interoperability, emergent risk, and cognitive work. It prepares policy and ethics, adaptive systems, and whole-system review, while connecting organizational design to platform ownership, API governance, data stewardship, security response, and distributed-system operations.

## Governing Question

What organizational control structure makes desired system outcomes feasible and observable when decisions, resources, expertise, incentives, and authority are distributed across many roles and institutions?

An organization is not a box surrounding the technical system. It changes requirements, architecture, staffing, access, release cadence, maintenance, incident response, supplier behavior, evidence, and accepted risk. A technically available safety mechanism can be ineffective when nobody may activate it, budgets exclude its upkeep, telemetry is filtered, or a target rewards avoiding its use.

## Why This Matters

Software-intensive capabilities are produced and operated through organizations. Executives establish priorities and tolerances; finance and procurement shape resources and suppliers; product teams choose trade-offs; platform and security teams impose shared controls; operators adapt to demand; regulators and customers constrain acceptable behavior. Their combined decisions create the realized system.

Systems-theoretic safety models include organizational controllers, control actions, feedback, process models, and coordination because losses can arise without a failed component. NIST's Cybersecurity Framework 2.0 similarly elevates governance, roles, responsibilities, authority, resource allocation, policy, and supply-chain risk. These frameworks do not make an organization safe or secure by adoption. They provide questions and outcomes that must be implemented and evidenced in a particular context.

“Culture” can describe patterned ways an organization processes information, responds to dissent, balances goals, and learns. Used vaguely, it becomes a residual explanation that is difficult to test or improve. Replace slogans with observable mechanisms: which reports are rewarded, what reaches a decision maker, who can stop work, which budget funds recovery, how exceptions age, and whether lessons change verified practice.

## Prerequisites and Retrieval

Before assessing organizational control, retrieve:

1. stakeholder outcomes, mission, unacceptable losses, legal and ethical duties, protected constraints, risk appetite and tolerance, and acceptance authority;
2. the actual organizational boundary, including boards, executives, business units, engineering, operations, safety, security, legal, compliance, finance, human resources, procurement, suppliers, customers, regulators, and affected communities;
3. formal roles, decision rights, delegations, vetoes, waivers, risk acceptance, escalation, incident command, separation of duties, and succession arrangements;
4. budgets, staffing, expertise, tools, facilities, time, service capacity, on-call coverage, training, retention, and competing commitments;
5. strategies, policies, standards, procedures, contracts, service agreements, incentives, objectives, key results, scorecards, and performance reviews;
6. information channels: dashboards, reports, meetings, tickets, audits, complaints, near misses, forecasts, informal networks, classification, aggregation, delay, and evidence provenance;
7. formal architecture, team and supplier boundaries, ownership maps, dependencies, shared services, approval paths, interfaces, and responsibility gaps;
8. work as done: field observation, actual decisions, workarounds, shadow tools, escalation behavior, exception use, maintenance deferral, and successful adaptation;
9. incidents, weak signals, dissent, customer harm, audit findings, recovery exercises, corrective actions, closure evidence, recurrence, and suppressed or missing data;
10. change history: reorganizations, leadership turnover, acquisitions, outsourcing, policy changes, budget shifts, migrations, new threats, and operating-model changes;
11. environmental and institutional conditions: markets, jurisdictions, regulation, labor relations, public expectations, suppliers, infrastructure, and geopolitical constraints;
12. evidence limits: populations consulted, time period, locations, shifts, contractors, data exclusions, reporting bias, survey response, and applicability to current state.

Construct an **obligation-to-control trace**. Select one protected outcome, derive an organizational obligation, identify its governing authority, responsible actors, decisions, information, resources, incentives, feedback, enforcement, and escalation. Walk the trace in normal and degraded conditions, then follow one adverse signal upward and one policy decision downward to find attenuation and delay.

## Learning Objectives

After completing this module, you should be able to:

1. model organizations as causal control structures within a system boundary;
2. distinguish responsibility, authority, accountability, ownership, and blame;
3. analyze goals, incentives, resources, metrics, and conflicting pressures;
4. trace information attenuation and process-model mismatch across levels;
5. design coordination, escalation, veto, waiver, and risk-acceptance paths;
6. reason about culture through observable information and learning mechanisms;
7. include suppliers, regulators, customers, and affected communities in organizational analysis;
8. investigate incidents without root-cause oversimplification or consequence-free ambiguity;
9. design leading indicators and closed learning loops with owners and evidence;
10. bound organizational assurance by actual configuration, period, and institutional context.

## Core Exposition

**Define organizational outcomes and constraints.** Start with stakeholder value and unacceptable loss. Translate them into obligations such as preserving a safety margin, protecting personal data, restoring an essential service, or obtaining independent approval. Avoid goals such as “be world class” that cannot guide a decision. State precedence when schedule, service, cost, safety, security, fairness, and legality conflict.

**Draw control, not hierarchy alone.** An organization chart shows reporting relations but rarely shows decisions, feedback, resources, or cross-functional coordination. Model controllers, controlled processes, control actions, feedback, process models, delays, and lateral relationships. Include committees only when their decisions and authority are concrete. A box named “governance” is not a control action.

**Make decision rights explicit.** For each consequential decision, state who proposes, evaluates, approves, vetoes, executes, verifies, accepts residual risk, and changes the rule. Define scope and degraded modes. Two simultaneous approvers can create ambiguity; one central approver can create delay and common cause. Delegation requires thresholds, competence, records, and revocation.

**Give accountability the means to work.** A named owner needs authority, information, capability, capacity, and resources. Otherwise the assignment transfers blame without transferring control. Test whether the owner can obtain evidence, stop or change work, fund remediation, coordinate dependencies, and escalate unresolved conflict. Separate outcome accountability from the many contributions required to achieve it.

**Analyze goal conflict.** Organizations pursue multiple legitimate goals. A support team may be measured on ticket closure while users need durable repair; a product team may be measured on release frequency while shared recovery capacity erodes. Identify hard constraints, negotiated objectives, and discretionary preferences. Observe what happens when all cannot be met, because the actual priority often appears only under pressure.

**Treat metrics as interventions.** Measurement directs attention and can change behavior. A target may improve visibility, invite gaming, shift work out of scope, suppress reports, or optimize a proxy. Define the causal rationale, denominator, population, time window, uncertainty, owner, decision, and counter-metrics. Never allow a composite score to compensate for a prohibited outcome.

**Model resource control.** Policies without staffing, budget, time, skills, tooling, and maintenance are weak controls. Trace who allocates each resource and on what cadence. Annual planning may be too slow for a new threat; emergency funds may lack procurement authority. Include opportunity cost and the workload imposed by reporting, approval, and compliance mechanisms.

**Trace information attenuation.** Frontline detail is summarized as it moves upward; policy loses context as it moves downward. Aggregation is necessary, but can hide tails, dissent, uncertainty, or affected populations. Design escalation triggers, direct evidence access, anomaly preservation, and feedback to reporters. Ask what leaders believe about field conditions and what evidence could falsify that model.

**Engineer lateral coordination.** Many outcomes cross teams that share no manager. Define interface obligations, common artifacts, service expectations, decision precedence, synchronized changes, and dispute resolution. Coordination costs capacity and must be funded. A meeting is not closure unless decisions, owners, evidence, and follow-up are captured.

**Include informal organization.** Trusted experts, chat channels, spreadsheets, personal scripts, and unofficial brokers often keep work functioning. They can supply missing context and also create fragility, access risk, or hidden single points of failure. Map them without automatically banning them. Preserve useful knowledge through supported tools, redundancy, documentation, and succession.

**Design supplier control realistically.** Outsourcing execution does not outsource stakeholder impact or retained obligations. Specify outcomes, interfaces, evidence, audit and incident rights, vulnerabilities, sub-suppliers, data use, change notification, recovery, exit, and continuity. Verify operational coordination, not just contract language. Concentrated vendors and shared cloud or identity roots create common-cause risk.

**Model regulators and customers as participants.** External authorities set constraints, request evidence, approve, inspect, or sanction. Customers supply requirements, operational feedback, and sometimes unsafe incentives. Affected people may lack purchasing power or formal representation. Include how concerns enter decisions, how conflicts are adjudicated, and how redress works.

**Protect reporting and challenge.** Psychological safety supports questions, disagreement, and reporting but is not permission to ignore competence or standards. Separate honest error, system-induced adaptation, reckless conduct, and malicious action using a fair, reviewable process. Protect reporters from retaliation, limit confidentiality promises honestly, and ensure reports lead to visible action or explanation.

**Investigate mechanisms, not one root.** Reconstruct decisions using information available at the time. Trace goals, constraints, process models, control actions, feedback, delays, coordination, resources, and prior successful adaptations. The last person touching the system is rarely the sole causal mechanism. Nor should “the system” erase individual agency. Match accountability and improvement to evidence and authority.

**Close learning loops.** Collection is not learning. An incident, near miss, audit, or suggestion must be triaged, analyzed, decided, funded, implemented, verified, communicated, and monitored for recurrence or side effects. Record rejected actions and rationale. Age open findings by consequence, and escalate when owners lack resources or cross-boundary authority.

**Learn from normal success.** Study how teams maintain constraints despite variation. Successful work may reveal hidden expertise, informal coordination, and consumed margin. Preserve beneficial adaptations while repairing conditions that make heroics necessary. Absence of loss cannot distinguish robust control from low exposure, hidden harm, or luck.

**Use organizational leading indicators.** Examples include rising exception age, shrinking recovery-test participation, unfilled critical roles, delayed risk acceptance, repeated ownership disputes, suppressed incident severity, unreviewed supplier changes, or widening differences between field and executive models. Each indicator needs mechanism, population, threshold, owner, action, uncertainty, and anti-gaming analysis.

**Design change as a control problem.** Reorganizations alter authority, networks, workload, expertise, funding, and interfaces even when technical architecture is unchanged. Map obligations before and after; preserve incident command, ownership, access, and institutional memory; test new escalation paths; and monitor transition workload. A new chart does not itself correct a causal mechanism.

**Bind evidence to organizational configuration.** Surveys, audits, certifications, exercises, and incident records cover specific participants, suppliers, leaders, sites, periods, and reporting conditions. A merger, outsourcing decision, new incentive plan, or leadership change can invalidate conclusions. Record the envelope and renewal triggers.

The following fixture checks declared organizational-control metadata. It cannot establish real authority or effectiveness.

<!-- bijux-verify: {"id":"organizational-control-ledger","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"controls=3\nrequired_fields=5\nchecks=15\npassed_checks=14\nfailed_checks=1\nblocked=supplier_revocation:escalation\nreadiness_gate=reject_incomplete_control_support\nevidence=declared_metadata_only\n","stderr":""}} -->
```python
controls = {
    "change_containment": {
        "owner": True, "authority": True, "resources": True,
        "feedback": True, "escalation": True,
    },
    "supplier_revocation": {
        "owner": True, "authority": True, "resources": True,
        "feedback": True, "escalation": False,
    },
    "incident_learning": {
        "owner": True, "authority": True, "resources": True,
        "feedback": True, "escalation": True,
    },
}
fields = ("owner", "authority", "resources", "feedback", "escalation")
blocked = [
    f"{name}:{field}"
    for name, support in controls.items()
    for field in fields
    if not support[field]
]
checks = len(controls) * len(fields)
print(f"controls={len(controls)}")
print(f"required_fields={len(fields)}")
print(f"checks={checks}")
print(f"passed_checks={checks - len(blocked)}")
print(f"failed_checks={len(blocked)}")
print(f"blocked={','.join(blocked)}")
print("readiness_gate=reject_incomplete_control_support")
print("evidence=declared_metadata_only")
```

## Definitions and Notation

Let organizational participants and roles be $P$, goals and constraints $G$, decisions and control actions $U$, observations and feedback $Y$, resources $K$, authority relation $A$, coordination relation $C$, and environment $E$. These elements are time- and configuration-dependent.

For obligation $o$, $S(o)=\langle G,R,A,I,K,F,E\rangle$ records declared support. “True” must mean more than a document exists: authority must be recognized in the relevant mode, information timely enough, resources usable, feedback linked to effect, and escalation able to resolve the blocked condition.

Define an evidence envelope

$$
\Omega_O=\langle entities,roles,suppliers,jurisdictions,sites,period,scenarios,data,assumptions\rangle.
$$

An organizational claim outside $\Omega_O$ needs an applicability argument or new evidence. Culture, maturity, and readiness scores are indicators within this envelope, not transitive properties of every unit or future configuration.

## Mechanisms, Invariants, or Proof Structure

1. **Frame outcomes and constraints.** Identify stakeholders, mission, losses, duties, precedence, tolerance, and acceptance authority.
2. **Map the actual organization.** Include formal and informal roles, external authorities, suppliers, customers, and affected communities.
3. **Trace obligations.** Connect goals to responsibility, authority, information, capability, resources, feedback, enforcement, and escalation.
4. **Analyze pressures.** Examine metrics, incentives, budgets, schedules, staffing, contracts, and conflicting goals under stress.
5. **Trace information.** Follow signals and decisions across levels and boundaries; identify delay, filtering, aggregation, and model mismatch.
6. **Analyze coordination.** Check lateral interfaces, precedence, incident command, handoffs, veto, waiver, and dispute resolution.
7. **Study work as done.** Observe adaptations, informal networks, shadow tools, reporting, and actual decisions.
8. **Design controls and resources.** Correct authority, capacity, feedback, enforcement, and cross-boundary support rather than issuing unsupported policy.
9. **Verify and learn.** Exercise paths, inspect outcomes, protect reporting, close corrective loops, and monitor leading conditions.
10. **Govern evolution.** Reassess organization, suppliers, incentives, leadership, policy, and evidence after material change.

Core invariants are: no accountability without commensurate control; no policy without communication, resources, feedback, and enforcement; no critical signal depends on one filtered path; no local metric overrides a protected system constraint; no supplier boundary erases retained obligation; no investigation ends with a person or culture label; no finding closes without verified effect; and no organizational evidence escapes its configuration and period.

There is no theorem that an organizational arrangement will produce every desired behavior. Interests conflict, institutions evolve, informal networks matter, and evidence is incomplete. The durable engineering contribution is explicit causal structure, feasible controls, protected learning, and change-aware assurance.

## Alternatives and Trade-Offs

**Centralization versus delegation.** Centralization can align policy and scarce expertise but adds latency, bottlenecks, and concentrated failure. Delegation improves local response but needs constraints, competence, feedback, and escalation. Choose decision by decision, including degraded modes.

**Functional teams versus outcome-aligned teams.** Functional grouping concentrates expertise and standards; outcome alignment reduces handoffs and clarifies service ownership. Either can create silos. Preserve professional learning while making cross-boundary outcome accountability and interfaces explicit.

**Standardization versus discretion.** Standards improve consistency and interoperability. Discretion handles local context and novelty. Define nonnegotiable constraints, authorized tailoring, evidence, and review rather than choosing unrestricted uniformity or improvisation.

**Transparency versus confidentiality.** Broad information access supports coordination and challenge but can expose personal, security, legal, or market-sensitive data. Apply purpose, minimum necessary access, protected reporting, aggregation limits, and independent oversight without using confidentiality to suppress risk evidence.

**Blameless learning versus individual accountability.** Fear suppresses reporting and distorts hindsight; consequence-free ambiguity can erode trust and standards. Use a fair process that distinguishes system-induced adaptation, honest error, capability gaps, reckless action, and malice while examining organizational causes in every case.

**Efficiency versus organizational resilience.** Lean staffing and consolidated services reduce cost but remove surge capacity, succession, independent checking, and recovery practice. Protect margin according to variability and consequence, and measure the workload created by coordination and control.

## Failure Modes and Misconceptions

- **“The organization is outside the system.”** Organizational decisions create technical state, operating conditions, and accepted risk.
- **“The chart shows control.”** Reporting lines omit actions, feedback, resources, lateral coordination, and informal influence.
- **“One owner means accountability.”** Ownership without authority, information, capability, and capacity is ceremonial.
- **“RACI closes the interface.”** A letter does not define semantics, timing, conflict resolution, evidence, or degraded operation.
- **“Policy changes behavior.”** Policy needs communication, feasibility, resources, reinforcement, observation, and correction.
- **“Culture is the root cause.”** The label must be decomposed into observable information, incentive, authority, and learning mechanisms.
- **“Bad news should go through management.”** One filtered route can suppress urgent dissent and distort process models.
- **“Metrics are neutral.”** Targets redirect attention and can cause gaming, exclusion, and proxy optimization.
- **“Outsourcing transfers risk.”** Contracts redistribute tasks and liability but may leave stakeholder and regulatory obligations intact.
- **“No incidents proves maturity.”** Exposure, reporting, hidden harm, adaptation, and luck affect the record.
- **“More reporting means more learning.”** Untriaged or unresourced reports increase workload and cynicism.
- **“Blameless means unaccountable.”** Fair causal analysis can coexist with clear standards and evidence-based consequences.
- **“A reorganization fixes coordination.”** It also changes authority, networks, workload, and memory and may reproduce the mechanism.
- **“Certification covers every unit.”** Scope, period, sample, exclusions, and actual implementation bound assurance.
- **“Leadership commitment is measurable by statements.”** Resource choices, decision behavior, response to dissent, and verified outcomes provide stronger evidence.

## Worked Examples

### Example 1

**Situation:** A service owner is accountable for availability but cannot fund capacity or block risky launches. **Reasoning:** Responsibility, authority, and resources are split with no escalation deadline. Transfer decision rights or define a binding cross-owner gate and funded escalation. **Conclusion:** Naming an owner does not create feasible control.

### Example 2

**Situation:** Teams are rewarded for deployment frequency while platform recovery tests consume delivery time. **Reasoning:** Local optimization predictably defers resilience work. Add protected recovery constraints, capacity, and leadership review rather than asking teams to care more. **Conclusion:** Incentive architecture is system architecture.

### Example 3

**Situation:** Incident severity is reduced before executive reporting because high severity triggers scrutiny. **Reasoning:** The metric and social consequence attenuate risk information. Preserve original classification, allow independent challenge, and audit outcome-based reclassification. **Conclusion:** A green dashboard can reflect filtering rather than control.

### Example 4

**Situation:** A central security board approves all emergency firewall changes but meets weekly. **Reasoning:** Central expertise conflicts with response time. Define pre-authorized bounded actions, on-call authority, logging, expiry, and retrospective review. **Conclusion:** Centralization without mode-aware capacity can create hazard.

### Example 5

**Situation:** A supplier operates identity infrastructure but the customer contract omits incident access and exit testing. **Reasoning:** Service execution moved; retained continuity and accountability did not. Add notification, evidence, sub-supplier, revocation, recovery, and transition obligations and exercise them. **Conclusion:** Procurement choices become control-path dependencies.

### Example 6

**Situation:** Operators rely on an unofficial spreadsheet to coordinate maintenance. **Reasoning:** The sheet supplies sequencing and ownership absent from the official tool, but lacks access control and version history. Incorporate the useful representation into supported workflow before retiring it. **Conclusion:** Shadow systems are evidence about unmet organizational work.

### Example 7

**Situation:** An investigation concludes that an engineer bypassed review. **Reasoning:** The review queue exceeded the outage deadline, the emergency path required an unavailable director, and prior bypasses restored service without consequence. Correct queue capacity, emergency authority, feedback, and incentives while evaluating the action fairly. **Conclusion:** The last action is not the whole causal system.

### Example 8

**Situation:** A hospital encourages safety reports but leaves hundreds open without feedback. **Reasoning:** Reporting grows while learning capacity does not; staff stop investing effort. Triage by consequence, fund analysis, publish decisions, verify action, and explain accepted residual risk. **Conclusion:** Collection without closure can weaken reporting culture.

### Example 9

**Situation:** A merger combines two on-call teams with different incident authority. **Reasoning:** The new chart removes duplicate managers but creates unclear veto, tooling access, escalation, and handoff. Map obligations and exercise a cross-environment failure before cutover. **Conclusion:** Organizational transition needs integration and verification.

### Example 10

**Situation:** An annual survey reports high psychological safety. **Reasoning:** Contractors, night shifts, and a recently acquired site have low response; incident records show delayed escalation. Segment evidence, investigate reporting conditions, and combine methods. **Conclusion:** An aggregate survey is bounded evidence, not an organization-wide property.

## Cross-Program Connections

- **Platform Engineering:** team boundaries, product ownership, paved-path governance, support, funding, and incident command determine platform effectiveness.
- **API and Service Engineering:** standards, compatibility, deprecation, ownership, consumer representation, and exception processes are organizational controls.
- **Data Engineering:** stewardship, quality ownership, lineage, access, correction, retention, and data-product contracts depend on authority and resources.
- **Security Engineering:** risk governance, separation of duties, reporting, incident response, supplier control, and exception management cross the enterprise.
- **Distributed Systems:** technical decentralization interacts with distributed authority, local goals, partial knowledge, and coordination delay.
- **Software Architecture:** communication and ownership boundaries influence interface structure, coupling, change, and operability.
- **Human Factors:** workload, expertise, hierarchy, common ground, and psychological safety mediate organizational control.
- **Machine Learning:** model governance, data responsibility, monitoring, appeal, rollback, and harm response need cross-functional decision rights.
- **Economics:** budgets, opportunity cost, principal-agent relationships, externalities, and incentives explain control feasibility and drift.
- **Law and Ethics:** duties, accountability, worker rights, community impact, evidence preservation, and redress constrain organizational action.

## References

1. Nancy G. Leveson and John P. Thomas, [STPA Handbook](https://psas.scripts.mit.edu/home/get_file.php?name=STPA_handbook.pdf), MIT Partnership for Systems Approaches to Safety and Security, 2018.
2. Nancy G. Leveson, [CAST Handbook](https://psas.scripts.mit.edu/home/get_file.php?name=CAST_handbook.pdf), MIT Partnership for Systems Approaches to Safety and Security, 2019.
3. U.S. Nuclear Regulatory Commission, [Safety Culture Policy Statement](https://www.nrc.gov/reading-rm/doc-collections/nuregs/brochures/br0500/index), NUREG/BR-0500 Revision 4, 2018.
4. National Institute of Standards and Technology, [The NIST Cybersecurity Framework 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20), NIST CSWP 29, 2024.
5. Ron Westrum, [A Typology of Organisational Cultures](https://doi.org/10.1136/qshc.2003.009522), Quality and Safety in Health Care, 2004.
6. Amy C. Edmondson, [Psychological Safety and Learning Behavior in Work Teams](https://doi.org/10.2307/2666999), Administrative Science Quarterly, 1999.
7. James Reason, [Managing the Risks of Organizational Accidents](https://www.routledge.com/Managing-the-Risks-of-Organizational-Accidents/Reason/p/book/9781840141054), Routledge, 1997.
8. NASA Office of Safety and Mission Assurance, [System Safety](https://sma.nasa.gov/sma-disciplines/system-safety), accessed 2026-09-01.

## Exercises

### Exercise 1

Distinguish responsibility, authority, accountability, ownership, and blame for a production-data retention control.

### Exercise 2

A control ledger has four obligations and six required support fields per obligation. Twenty-two fields pass. Compute the pass rate, then explain why a missing noncompensable field blocks readiness.

### Exercise 3

Construct an obligation-to-control trace for emergency revocation of a compromised software supplier credential.

### Exercise 4

Design an incident-learning loop that protects reporting while maintaining evidence-based accountability and verified corrective action.

### Exercise 5

Evaluate a proposal to reorganize component teams into service-aligned teams for a regulated payment platform.

## Answers to the Exercises

### Answer 1

Responsibility assigns work: a data-platform team may implement retention jobs, legal may interpret duties, product teams may classify records, and operations may monitor execution. Authority grants decisions: a data owner may approve retention classes, privacy may veto unlawful storage, and an incident commander may pause deletion during a legal hold. Ownership identifies the role expected to maintain a defined artifact or outcome over time.

Accountability makes a role answerable for a result or decision, but only credibly when it has information, authority, capability, resources, feedback, and escalation. An executive data steward might be accountable for the enterprise outcome while many roles contribute. Blame is an adverse judgment about fault; it should not substitute for causal analysis or be assigned automatically to the accountable role.

Trace data categories, jurisdictions, purposes, holds, deletion propagation, backups, suppliers, evidence, exceptions, and redress. Verify the actual control and reconcile failures. A responsibility matrix is useful retrieval evidence, but it does not prove authority, capacity, correct classification, or deletion outcome.

### Answer 2

There are $4\times6=24$ required checks. With 22 passing, the arithmetic pass rate is

$$
\frac{22}{24}\times100\%\approx91.7\%.
$$

The percentage is descriptive and cannot compensate for a missing hard condition. If emergency recovery lacks authority or a safety decision lacks feedback, the relevant obligation is infeasible even if every other cell passes. Report the two failed fields by obligation and mechanism, not only the aggregate.

Validate that each “pass” is true in actual modes: a named role may be vacant, authority may be disputed, resources unavailable during a surge, feedback delayed, or escalation unable to resolve conflict. Analyze interactions and competing obligations. The ledger is a completeness screen, not proof of organizational effectiveness.

### Answer 3

The protected outcomes are preventing unauthorized supplier access, containing compromise, preserving essential service, retaining evidence, and meeting notification duties. The obligation is to revoke affected credentials and trust paths within a consequence-based deadline while controlling unsafe disruption. Define who declares compromise, who scopes credentials, who authorizes revocation, who executes across identity and deployment systems, who verifies propagation, and who accepts degraded service.

Inputs include supplier identity inventory, sub-suppliers, credential lineage, active sessions, artifacts, environments, service dependencies, legal constraints, and current incident evidence. Resources include on-call identity, platform, security, legal, procurement, and service owners with tested tooling. Feedback must confirm revocation, residual sessions, blocked workloads, customer impact, and recovery. Escalation resolves unavailable approvers, disputed scope, and supplier noncooperation.

Exercise partial identity outage, incomplete inventory, compromised communication, off-hours staffing, shared credentials, and a critical service that cannot immediately rotate. Use pre-authorized bounded containment, independent channels, audit evidence, expiry, reconciliation, and restoration criteria. The contract should provide notification, investigation access, and exit support, but operational drills must show that the retained organization can act.

### Answer 4

Provide accessible channels for incidents, near misses, weak signals, successful adaptations, and dissent, with stated confidentiality limits and anti-retaliation control. Preserve original accounts and technical evidence. Triage by potential consequence and recurrence, not only realized damage. Give reporters acknowledgement, status, and a way to challenge closure.

Analysis reconstructs goals, information, authority, resources, actions, feedback, coordination, incentives, and changes using the perspective available at the time. A fair-accountability process separately evaluates capability, honest error, system-induced adaptation, reckless disregard, and malicious action with consistent criteria and appeal. Protecting learning does not require hiding evidence or abandoning standards.

For each action, record causal mechanism, owner, authority, funding, deadline, affected configurations, verification method, side effects, and residual risk. Implement and verify outcome, not document completion. Monitor recurrence and leading conditions; communicate decisions and rejected proposals. Escalate aging high-consequence findings. Periodically test whether the loop itself has reporting gaps, bottlenecks, or incentives to reduce severity.

### Answer 5

Service-aligned teams can reduce handoffs, align development and operation, and clarify end-to-end ownership. They may duplicate specialist work, fragment standards, overload small teams, and weaken independent control. In a regulated payment platform, preserve nondelegable compliance, risk acceptance, segregation, audit, data, security, and resilience obligations while moving routine decisions closer to service context.

Map current and target decision rights, interfaces, shared platforms, specialist communities, staffing, on-call, supplier ownership, evidence, escalation, and incident command. Identify services that cross team boundaries and common controls that require central authority or independent verification. Fund migration, training, access changes, runbook and dashboard ownership, and temporary coordination load.

Before cutover, exercise fraud, privacy, settlement, identity, dependency, and recovery scenarios across the target structure. Track ownership gaps, decision latency, support demand, conflicting priorities, control exceptions, operator workload, and outcome tails. Roll out reversibly where possible. The proposal succeeds only if the new organization makes obligations more feasible and evidenced; changing team labels or repository ownership is not sufficient.
