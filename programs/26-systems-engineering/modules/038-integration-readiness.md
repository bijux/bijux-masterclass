---
module_id: SYSENG-038
program: Systems Engineering
level: 1
module_number: 38
title: Integration Readiness
status: complete
last_verified: 2026-08-31
---

# Integration Readiness

## One-Page Review

### Governing question

What evidence justifies authorizing a specific integration step now, with these exact items, interfaces, people, procedures, environments, and residual risks, without confusing document completion or schedule pressure with technical readiness?

### Essential definitions

- **Integration readiness** is the evidence-supported condition that a declared integration step can begin and reach its intended end state safely, validly, and usefully under a controlled configuration and environment.
- A **readiness criterion** is a falsifiable, applicable condition that must be evaluated before authorization; it names required evidence, owner, due event, and consequence if unmet.
- An **entry criterion** must hold before the step starts. An **exit criterion** must hold before its result may progress to the next governed state.
- **Objective evidence** is inspectable information tied to an exact item, configuration, method, condition, result, date, provenance, and acceptance criterion.
- **Evidence validity** means the evidence actually bears on the criterion for the planned article, version, environment, and decision. **Evidence freshness** means relevant changes or time-dependent limits have not invalidated it.
- A **mandatory criterion** cannot be traded against other criteria through averaging. If unmet, the normal decision is hold unless an authorized deviation explicitly accepts the resulting risk.
- A **waiver or deviation** is a controlled authorization to depart from a requirement or baseline for stated scope and duration; it does not convert missing evidence into conformance.
- A **readiness gate** is a decision event at which accountable authorities review evidence, dissent, anomalies, residual risk, and constraints and issue a recorded outcome.
- A **conditional authorization** permits only bounded actions under explicit prerequisites, limits, monitors, stop conditions, owner, and expiration.
- A **readiness finding** is a criterion-level conclusion such as met, unmet, not applicable with rationale, indeterminate, or expired.
- A **hold point** is a required pause before a consequential action until named evidence and authority are present.
- **Readiness debt** is unresolved work or uncertainty deliberately carried into an authorized step; it has an owner, exposure, containment, closure event, and impact on evidence credit.

### Central model, mechanism, or theorem

For planned step (s), configuration (k), environment (h), decision time (t), and applicable criteria (C_s), partition criteria into mandatory (M_s) and discretionary/supplementary (D_s). Define (met(c,k,h,t)) only when the criterion is satisfied by valid, fresh evidence. Then ordinary authorization requires:

$$
Ready(s,k,h,t)=\bigwedge_{c\in M_s}met(c,k,h,t)
\land RiskAccepted(s,k,h,t)
\land AuthorityPresent(s,t).
$$

A descriptive completion fraction:

$$
F=\frac{|\{c\in C_s:met(c)\}|}{|C_s|}
$$

can help locate work but cannot establish readiness. (F=0.95) may still hide one catastrophic mandatory gap. A waiver changes the decision basis by accepting bounded nonconformance; it does not make (met(c)) true.

Evidence applicability can be represented as:

$$
Valid(e,c)\Rightarrow Article(e)=Article(c)\land Config(e)\sim Config(c)
\land Conditions(e)\supseteq Conditions(c)\land Method(e)\text{ is adequate},
$$

plus intact provenance and no invalidating change. Compatibility $(\sim)$ requires an explicit equivalence or impact argument, not name similarity.

### Critical invariants

- The integration step, starting and intended ending states, decision authority, configuration, environment, location, time, and evidence objective are explicit.
- Criteria are derived from the planned hazards, interfaces, dependencies, procedures, lifecycle, and evidence claims—not copied blindly from a generic checklist.
- Every applicable mandatory criterion is met by valid and fresh evidence or is visibly subject to a bounded authorized deviation; no average or color roll-up hides it.
- Every item is identified, accepted for the intended use, undamaged, correctly preserved, correctly configured, and accompanied by known limitations and anomaly status.
- Every interface to be mated or exercised has endpoint agreement, precheck evidence, correct applicability, and controlled change status.
- Procedures, drawings, models, software, data, test scripts, configurations, and criteria are mutually consistent and under appropriate control.
- Facilities, environments, tools, fixtures, simulators, instrumentation, storage, networks, and external systems are ready at the required fidelity and capacity.
- Personnel are trained, qualified, authorized, available, rested, briefed, and supported for their actual roles, including safety, quality, anomaly, and emergency response.
- Hazards, cybersecurity/privacy constraints, permits, protective measures, safe states, stop-work authority, abort thresholds, and emergency response are ready before exposure.
- Calibration, provenance, time synchronization, data acquisition, reduction, custody, backup, and reporting can support the intended evidence claim.
- Open anomalies, nonconformances, liens, waivers, deviations, risks, and prior actions have dispositions compatible with the planned step.
- Rollback, de-integration, recovery, spares, consumables, cleanup, and re-entry are credible for plausible failures.
- Dissent and uncertainty are recorded; the gate decision names rationale, conditions, residual risk owner, expiration, and evidence limitations.
- Any material change after the gate invalidates affected findings and triggers focused reassessment before execution.

### Common failures

Common failures include declaring “95% ready”; treating document existence as document adequacy; accepting self-reported green status without underlying evidence; checking part names but not serials/builds/options; relying on stale qualification or calibration; assuming supplier acceptance proves interface readiness; marking unknown as not applicable; closing findings by promising future work; allowing schedule leadership to waive technical facts informally; using waivers as conformance evidence; reviewing the test article but not tools, data, people, facilities, external services, or emergency response; counting trained people without checking the executing shift; approving a procedure never rehearsed; ignoring open anomalies and temporary modifications; failing to define abort/rollback; issuing a conditional go with no bounds or expiry; and letting a post-gate change retain readiness by inertia.

### Compact example

A networked controller is scheduled for actuator integration. The controller and actuator passed standalone acceptance, but the planned controller build uses a newer protocol profile, the actuator emulator did not model a stale-sequence fault, and the executing technician's hazardous-energy qualification expired. A dashboard reports 18 of 20 checks complete—90%. The gate holds: protocol compatibility needs direct evidence, the fault gap limits what prior tests establish, and qualified personnel are mandatory. Readiness is restored by testing the exact builds at the interface plane, dispositioning the fidelity gap, and assigning currently qualified staff—not by raising the percentage.

### Connections

SYSENG-037 determines which integration step is logically eligible and worth doing next; this module determines whether that exact step is executable now. SYSENG-039 supplies controlled baselines and configuration identity. SYSENG-040 organizes the wider integration strategy around interface risk. Product verification, validation, technical assessment, risk, suppliers, quality, safety, security, human integration, operations, and data management provide criteria and evidence.

## Governing Question

What must be demonstrably true before responsible authorities allow the next integration action, and what limits must accompany the decision when uncertainty or nonconformance is intentionally carried?

Readiness is not a property an item owns forever. It is a relationship among a particular step, starting state, participants, versions, interfaces, environment, procedure, personnel, evidence objective, hazards, time, and authority. The same product may be ready for a powered-off fit check, unready for energization, ready for a low-authority bench test, and unready for an operational external connection.

## Why This Matters

Integration creates new interactions and often increases energy, authority, scope, or irreversibility. A readiness gate prevents the calendar from becoming the only entry criterion. It gives engineers and operators a structured opportunity to expose missing products, incompatible interfaces, invalid evidence, unsafe states, unprepared facilities, untrained people, unresolved anomalies, and weak recovery before those gaps become damage or ambiguous results.

NASA's current Product Integration guidance calls for reviewing the integration plan and configuration documentation, inspecting received products, confirming their validation, and preparing integration-enabling products, facilities, equipment, simulators, recording devices, and workforce. NASA's Integration Plan outline asks for exact participants, support equipment, external systems, responsibilities, schedule, verification activity, and problem resolution at each step.

NASA Technical Assessment guidance frames reviews and technical measures as evidence for decisions and early corrective action. NASA Product Verification and Product Validation guidance distinguishes preparing the article, environment, procedures, instrumentation, personnel, criteria, and data from actually performing and analyzing the work. NASA Interface Management and Configuration Management guidance require compatible controlled interfaces and a true product representation through integration.

NASA's Goddard systems-review standard describes a System Integration Review as evaluating whether the overall system is ready to commence integration and test, including approved plans/procedures, components, personnel, facilities, ground-support equipment, data acquisition, and prior evidence. That institutional review is one application. The method in this module scales down to a single bench mating or software migration and up to multi-organization system assembly. Tailoring must preserve the decision's risk and evidence needs.

Readiness scales and percentages can support communication but are dangerous when treated as proof. GAO's technology-readiness guidance emphasizes credible, objective, reliable, useful assessment and evidence in the intended environment. Integration readiness is broader than technology maturity: mature items can be mutually incompatible, wrongly configured, unavailable, unsafe to connect, or unsupported by the actual workforce and facility.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. the exact planned integration step, dependency rationale, starting/ending states, sequence, location, schedule window, and decision/evidence objective;
2. item identities, serials/builds/versions/options, acceptance and verification evidence, preservation/handling history, limitations, and open anomalies;
3. interface identities, current contracts/ICDs, endpoint configurations, prechecks, changes, assumptions, guarantees, and discrepancies;
4. controlled procedures, drawings, models, software, scripts, data, criteria, expected results, hold/abort rules, and approval status;
5. facilities, fixtures, tools, instrumentation, simulators/emulators, networks, storage, external systems, environmental controls, and calibration;
6. named personnel, roles, qualifications, authorization, staffing, shift/handoff, safety/quality coverage, and emergency response;
7. hazards, threats, privacy constraints, permits, protective measures, safe states, operational limits, recovery, rollback, spares, and consumables;
8. evidence provenance, applicability, freshness, uncertainty, configuration control, risk acceptance, waiver/deviation, dissent, and change impact.

As a retrieval test, inspect “pump ready for software integration.” Ask which pump/firmware/controller builds, disposable fluid path, calibration, voltage, fixture, simulated patient, drug library, network, identity, time, test data, alarm route, procedure, nurse/engineer roles, safe fluid, cleanup, stop thresholds, and rollback apply. Ask what acceptance evidence excludes. The word `ready` without a step and context is not reviewable.

## Learning Objectives

After completing this module, you should be able to:

1. define readiness for a bounded integration step rather than as a permanent scalar property;
2. derive entry and exit criteria from dependencies, interfaces, hazards, evidence objectives, configurations, and lifecycle conditions;
3. distinguish criterion status, objective evidence, evidence validity/freshness, risk, waiver/deviation, and authorization;
4. construct readiness matrices that preserve mandatory gaps and do not misuse aggregate percentages;
5. assess products, interfaces, configurations, procedures, environments, enabling products, people, safety/security, data, and recovery together;
6. evaluate inherited, supplier, test-double, analytical, and prior-test evidence for exact applicability;
7. conduct a readiness gate with independent challenge, dissent, residual-risk acceptance, and precise decision recording;
8. specify conditional authorization, hold points, stop conditions, expiration, and evidence limits;
9. invalidate and reassess findings after relevant changes or expired evidence;
10. distinguish integration readiness from technology maturity, product acceptance, verification completion, test readiness, operational readiness, and validation.

## Core Exposition

**Scope the decision first.** Record step ID, purpose, integration level, starting state, intended ending state, exact planned actions, configuration, environment, location, time window, evidence objective, consequences, and decision authority. Readiness for a dimensional inspection requires less than readiness for pressurization; neither implies readiness for human use.

**Derive criteria from the work.** Begin with the SYSENG-037 dependency and step records. For every item, interface, state change, energy/material/data/authority flow, hazard, observation, external participant, enabling product, and intended evidence claim, ask what must be true before start, at hold points, and before progression. Add applicable organizational/regulatory criteria. Generic checklists are prompts, not substitutes.

**Write falsifiable criteria.** Replace “procedure ready” with “Procedure INT-17 revision C is approved; dry-run findings A12 and A14 are closed; every command, observation, limit, hold point, abort, rollback, and data record maps to controller build 8.4 and actuator profile P3.” Define evidence and acceptance, not just an artifact title.

**Separate mandatory from supplementary.** Mandatory criteria protect validity, safety, configuration, interface compatibility, legal/regulatory obligations, or required authority. Supplementary evidence can strengthen confidence or manage efficiency. Do not use weighting to let several low-consequence greens offset one high-consequence red.

**Use explicit finding states.** Recommended states are `met`, `unmet`, `indeterminate`, `expired`, and `not applicable with approved rationale`. `In progress` describes work, not readiness. `Accepted risk` describes a decision about an unmet condition, not a met finding. Keep status, evidence, and authorization separate.

**Identify the integration items exactly.** Verify part/serial/lot, hardware modification, software/firmware build and hash, container/image, configuration settings, options, calibration, data/schema/model/library, certificates/keys/policies, procedures, fixtures, and doubles. Inspect custody, preservation, transport/environmental exposure, damage, contamination, licenses, and expiration.

**Review product evidence for intended use.** Acceptance or standalone verification may support readiness but inspect requirement set, article, version, environment, method, result, anomalies, deviations, and limitations. Qualification of one option or supplier lot does not transfer automatically. A product can conform to its specification yet be incompatible with a sibling's changed interface.

**Precheck interfaces.** For each planned mating/exercise, verify endpoint identities and versions; dimensions/keying/alignment; cleanliness; pinout/polarity/grounding/voltage; pressure/flow/material compatibility; protocols/schemas/units; timing/clock; identity/trust/authorization; command ownership; modes; failure/safe states; and approved change status. Use the actual observation plane. Visual similarity is not compatibility evidence.

**Establish configuration coherence.** The item list, drawings, ICDs, procedures, software, test scripts, expected values, test data, tooling, calibration, hazards, and rollback assets must describe one realizable state. A review packet assembled from individually current documents can still combine mutually incompatible revisions. Generate or audit a configuration applicability matrix.

**Assess procedures as executable controls.** Check step order, prerequisites, roles, inputs, equipment, settings, warnings, verification points, data capture, expected outcomes, decision points, hold/abort thresholds, stop-work authority, anomaly response, rollback/de-integration, cleanup, and re-entry. Rehearse novel, hazardous, time-critical, multi-team, or recovery procedures at suitable fidelity.

**Assess the environment and enabling products.** Confirm facility access and capacity; environmental controls; utilities; clean/secure zones; lifting/handling; fixtures; protective equipment; fire/emergency support; networks; accounts; storage; simulators/emulators; test equipment; monitoring; recording; data-reduction systems; calibration; maintenance; backup; spares; and consumables. Check simultaneous users and scheduled facility states, not catalog capability.

**Assess people and organization.** Name who will execute, witness, approve, monitor, analyze, maintain safety/quality/configuration, respond to anomalies, and authorize continuation. Verify training/qualification scope and expiry, recent practice, fatigue/workload, staffing, communication, shift handoff, language/accessibility, access permissions, and backup coverage. `The team is trained` is not evidence about the executing shift.

**Assess safety and environmental protection.** Confirm hazards/threats, controls, permits, protective systems, inhibited outputs, energy isolation, containment, exclusion, environmental monitoring, emergency stop, evacuation, medical/fire response, hazardous materials, waste, and safe hold states. Confirm controls work in intermediate integration configurations, which may differ from the final design.

**Assess cybersecurity and privacy.** Confirm trust roots, credentials, least privilege, network isolation, secure configuration, vulnerability disposition, logging, data minimization, synthetic/approved data, secrets handling, incident response, backup, key recovery, external connection authority, and cleanup. A test facility can introduce privileged backdoors or real sensitive data outside the operational controls.

**Assess measurement and evidence capability.** Trace every intended conclusion to instrumentation, sensors, logs, human observations, sampling, synchronization, ranges, uncertainty, calibration, data acquisition, reduction, quality checks, custody, retention, and analysis responsibility. If the system cannot observe the event at the required plane, the step may run but cannot support the claimed evidence.

**Review anomalies and prior findings.** List open discrepancies, nonconformances, waivers/deviations, liens, temporary repairs, patches, limitations, failed tests, previous-review actions, and accepted risks. For each, identify affected configurations, interfaces, hazards, procedure steps, evidence, downstream claims, owner, containment, closure, and authority. `Known` is not the same as compatible with the next step.

**Plan failure before start.** Identify credible procedural errors, item faults, interface mismatches, loss of utilities/network/time, tool failures, data corruption, threshold excursions, injury/environmental events, cyber incidents, and external-system loss. Define detection, safe state, hold/abort, evidence preservation, escalation, rollback/de-integration, spares/cleanup, investigation, regression, and re-entry.

**Evaluate evidence validity.** For evidence item (e), ask whether its article/configuration matches; conditions cover the planned use; method measures the relevant property; criteria were predeclared and applied; instrumentation was adequate; result passed without hidden exceptions; anomalies are understood; provenance is intact; and no later change invalidates it. An assertion, screenshot, meeting memory, or green cell without its evidence chain is weak.

**Evaluate freshness and volatility.** Calibration, training, credentials, permits, environmental surveys, vulnerability assessments, supplier status, data, risk, facility bookings, and software dependencies can expire. Other evidence is invalidated by change rather than time. Set `valid through` or change triggers based on the claim, not one universal age.

**Use inheritance carefully.** Prior tests, heritage, qualification, supplier certificates, analytical models, and test-double results may reduce new work. Create an applicability argument covering similarity/difference in article, configuration, interface, environment, load, mode, lifecycle, method, and evidence quality. Carry excluded behaviors and required regression explicitly.

**Quantify only what has a sound scale.** Counts of met criteria, open findings by severity, evidence age, procedure-rehearsal completion, or residual-risk exposure can help manage work. A weighted readiness score is an index, not a probability of success. Do not multiply arbitrary ordinal likelihood and consequence labels as if the result had physical units.

**Prepare the gate packet for challenge.** Include scope/configuration; planned step and dependency; criteria matrix; evidence links; interface/configuration status; procedure and rehearsal; facility/tool/data/people readiness; hazards/security/privacy; anomalies/waivers/risks; rollback; decisions requested; dissent; and changes since packet cutoff. Make evidence available early enough for review.

**Use appropriate independence.** The people closest to work understand details; independent reviewers can detect confirmation, ownership, and schedule bias. Select independence proportional to consequence and novelty. Reviewers need domain competence, access to underlying evidence, conflict disclosure, and authority to record dissent—not ceremonial attendance.

**Conduct the gate as a decision, not presentation theater.** Verify scope and configuration, review mandatory gaps first, sample evidence to source, challenge assumptions and equivalence claims, walk high-risk procedures and failure paths, hear dissent, and make disposition visible. Do not spend the meeting reading slides that conceal absent records.

**Issue precise outcomes.** Useful outcomes include:

- `authorized`: all mandatory criteria met and residual risk accepted within authority;
- `authorized with constraints`: bounded action is permitted under enumerated prerequisites, limits, monitors, hold points, stop conditions, owner, and expiration;
- `hold`: missing/invalid evidence or unaccepted risk prevents the action until named conditions are satisfied;
- `cancel/replan`: the step or configuration is no longer appropriate.

Avoid vague `conditional go` language. State exactly what may happen before each condition closes. If the condition must close before any action, the decision is hold.

**Govern waivers and deviations.** Name the unmet requirement/criterion, affected item/configuration/step, reason, evidence, consequence, risk, compensating controls, monitoring, duration, downstream limitations, approval authority, and closure. A waiver may authorize integration but does not grant verification credit for the waived property.

**Record readiness debt.** For every carried gap, record owner, containment, exposure window, triggers, effect on evidence and future states, closure event, and contingency. Track cumulative interactions: several individually tolerated gaps can share a common cause or eliminate recovery margin.

**Reconfirm at execution.** At start, verify the authorized step, configuration, items, people, environment, procedure revision, tools/calibration, anomaly status, permits, time window, and conditions. A gate held days earlier does not override changed facts. Use pre-job brief and signed/recorded entry confirmation appropriate to the domain.

**Invalidate findings after change.** Changes to item, software/data, interface, procedure, facility, tooling, staff, qualification, hazard, external service, anomaly, waiver, schedule window, or intended evidence can invalidate only some or all criteria. Perform focused impact analysis, but do not retain a green finding without a rationale.

**State evidence limits.** A passed readiness gate supports authorization under its scope; it does not predict success with certainty or prove verification, validation, operational readiness, production readiness, regulatory acceptance, or lifecycle fitness. A hold is not project failure; it is the mechanism preventing unsupported exposure.

The following checker evaluates a small set of declared readiness records at a fixed decision date. It does not prove the criteria are complete, correctly classified, or substantively adequate.

<!-- bijux-verify: {"id":"integration-readiness-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"criteria_total=8\nmandatory_total=7\nmet_mandatory=4\nunmet_mandatory=interfaces,procedure,people\nexpired_evidence=people\nmissing_evidence=procedure\nwaivers_open=interfaces\ndecision=hold\nevidence=declared_records_only\n","stderr":""}} -->
```python
decision_date = "2026-08-31"
criteria = [
    {"id": "items", "mandatory": True, "status": "met", "evidence": ["receipt-17"], "valid_until": None, "waiver": False},
    {"id": "interfaces", "mandatory": True, "status": "waived", "evidence": ["DEV-09"], "valid_until": None, "waiver": True},
    {"id": "configuration", "mandatory": True, "status": "met", "evidence": ["baseline-K4"], "valid_until": None, "waiver": False},
    {"id": "environment", "mandatory": True, "status": "met", "evidence": ["facility-check-8"], "valid_until": "2026-09-05", "waiver": False},
    {"id": "procedure", "mandatory": True, "status": "met", "evidence": [], "valid_until": None, "waiver": False},
    {"id": "people", "mandatory": True, "status": "met", "evidence": ["qualification-Q7"], "valid_until": "2026-08-01", "waiver": False},
    {"id": "safety", "mandatory": True, "status": "met", "evidence": ["hazard-closeout-3"], "valid_until": None, "waiver": False},
    {"id": "rollback", "mandatory": False, "status": "planned", "evidence": ["rollback-draft"], "valid_until": None, "waiver": False},
]

def expired(item):
    return item["valid_until"] is not None and item["valid_until"] < decision_date

def valid_met(item):
    return item["status"] == "met" and bool(item["evidence"]) and not expired(item)

mandatory = [item for item in criteria if item["mandatory"]]
unmet = [item["id"] for item in mandatory if not valid_met(item)]
print(f"criteria_total={len(criteria)}")
print(f"mandatory_total={len(mandatory)}")
print(f"met_mandatory={sum(valid_met(item) for item in mandatory)}")
print("unmet_mandatory=" + ",".join(unmet))
print("expired_evidence=" + ",".join(item["id"] for item in criteria if expired(item)))
print("missing_evidence=" + ",".join(item["id"] for item in criteria if not item["evidence"]))
print("waivers_open=" + ",".join(item["id"] for item in criteria if item["waiver"]))
print("decision=" + ("authorized" if not unmet else "hold"))
print("evidence=declared_records_only")
```

The open waiver remains an unmet mandatory criterion; the empty procedure evidence and expired qualification invalidate two more. Even after those records are repaired, substantive review must determine whether their evidence is correct and sufficient.

## Definitions and Notation

Let planned steps be (S), configurations (K), environments (H), criteria (C), evidence objects (E), findings (F), risks (R), authorities (A), and decision time (t).

Applicability relation:

$$
Applicable\subseteq C\times S\times K\times H.
$$

Evidence-support relation:

$$
Supports\subseteq E\times C,
$$

with support accepted only when provenance, configuration, condition, method, result, freshness, and change impact are adequate.

For applicable mandatory set:

$$
M(s,k,h)=\{c\in C:Applicable(c,s,k,h)\land mandatory(c)\}.
$$

Ordinary readiness at time (t):

$$
Ready(s,k,h,t)\iff
\left(\forall c\in M(s,k,h):finding(c,t)=met\right)
\land acceptedRisk(s,k,h,t)\land authorized(a,s,t).
$$

If a deviation permits action despite criterion (c) being unmet, preserve:

$$
finding(c,t)=unmet,
$$

and record separate authorization (deviation(c,scope,limits,expiry,authority)). This prevents decision metadata from corrupting evidence truth.

A readiness record should include criterion ID/text/category, source/rationale, applicability, mandatory flag, owner, evidence requirement, linked evidence, finding, reviewer/date, valid-through/change triggers, anomaly/risk/waiver links, action, due event, and decision impact.

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—step-specific criterion derivation.** Traverse the integration step, predecessor conditions, interfaces, states, hazards, evidence objectives, enabling products, people, external systems, and recovery. Convert each necessary truth into a criterion with observable evidence.

**Mechanism 2—configuration and evidence indexing.** Build the exact item/configuration list and link every criterion to controlled records. Check cross-document applicability rather than only current revision labels.

**Mechanism 3—criterion-level assessment.** A responsible assessor reviews evidence to source and assigns met, unmet, indeterminate, expired, or justified not-applicable. Findings state uncertainty and limitations. Owners cannot self-close high-consequence disputes without required authority.

**Mechanism 4—cross-domain challenge.** Review fan-in across product, interfaces, procedures, facilities, people, hazards/security/privacy, measurement/data, logistics, anomaly, and recovery. Search for correlated gaps and unsafe intermediate states.

**Mechanism 5—gate decision.** The authority distinguishes evidence truth from risk acceptance, hears dissent, confirms scope, and records authorized/limited/hold/replan with conditions and expiration.

**Mechanism 6—execution confirmation and change invalidation.** Reconfirm volatile facts immediately before work. After changes, trace affected criteria and evidence, repeat only what is necessary, and record why unaffected findings remain valid.

The reasoning obligation is:

1. show the criterion set is credible for the scoped step;
2. show each mandatory criterion's finding follows from applicable valid evidence;
3. show residual risks and deviations are understood and within authority;
4. show conditions/monitoring/abort/recovery bound the authorized exposure;
5. show the execution configuration still matches the decision.

This is an assurance argument, not a proof that integration will succeed.

## Alternatives and Trade-Offs

**Single formal system gate** can align organizations and independent review but may be too coarse for volatile daily work. **Step-level micro-gates** keep evidence current but require disciplined tooling and delegated authority. Use a hierarchy of gates with clear inheritance and invalidation.

**Checklist-based assessment** is repeatable and helps novices. **Argument-based assessment** handles context and evidence relevance. Combine controlled checklist prompts with explicit rationale; neither exhaustive boxes nor eloquent narrative should hide missing proof.

**Binary criteria** preserve decisive boundaries. **Maturity scales** show progress before the boundary. Keep the authorization predicate binary at the scoped decision while using maturity indicators diagnostically.

**Independent review** reduces ownership and schedule bias. **Embedded review** has faster, deeper context. Scale independence to consequence, novelty, external obligation, and uncertainty while preserving dissent channels.

**Full evidence review** offers confidence but can be slow. **Risk-based sampling** is efficient when evidence systems and processes are trustworthy. Never sample away the exact high-consequence interface or configuration at issue.

**Hold until conformance** minimizes carried debt. **Bounded deviation** may enable learning or schedule protection. Deviation is rational only with authority, containment, observability, recovery, expiration, and no prohibited exposure.

**Dashboard automation** improves freshness, traceability, and anomaly detection. **Manual judgment** evaluates semantic adequacy and unusual risk. Automate retrieval and consistency checks; retain accountable technical judgment.

## Failure Modes and Misconceptions

**“Readiness is 92%.”** The percentage describes record completion at best. It cannot show which mandatory condition is missing or the consequence.

**“All documents are approved.”** The documents may refer to inconsistent configurations, omit the planned state, or be technically inadequate.

**“The supplier signed acceptance.”** Supplier evidence may not cover shipping damage, exact options, sibling compatibility, new environment, local procedures, or current anomalies.

**“Green means evidence exists.”** Status color without source evidence, reviewer, date, configuration, and limitation is an assertion.

**“Unknown is N/A.”** Not applicable requires rationale and approval. Unknown/indeterminate remains a gap.

**“The waiver closes the criterion.”** It authorizes bounded nonconformance; the finding stays unmet and downstream credit is limited.

**“The review board owns the risk.”** Risk authority must be explicit and may remain with program, safety, security, operations, regulatory, or other accountable leadership.

**“Training was completed last year.”** Scope, expiry, executing personnel, recent practice, shift, workload, and changed procedure matter.

**“The test equipment powers on.”** Range, accuracy, uncertainty, calibration, configuration, software, probes, synchronization, data path, and capacity determine evidence fitness.

**“We can roll back.”** Verify backups, compatible versions/schemas, physical access, consumables, safe de-energization, data reconciliation, credentials, and practiced procedure.

**“Nothing changed since the gate.”** Verify through configuration and operational records. Informal patches, environment changes, expired credentials, staffing changes, and external updates are changes.

**“A hold is failure.”** A justified hold is successful risk control. Proceeding without evidence merely transfers the problem into a higher-consequence state.

## Worked Examples

### Example 1

**Ninety percent ready is a hold.** Twenty criteria include eighteen met, one mandatory interface-polarity precheck missing, and one mandatory emergency-stop rehearsal failed. The completion fraction is:

$$
F=18/20=0.90.
$$

Both missing criteria can cause harm and invalidate results; the step holds. Correct wiring/precheck evidence and successful rehearsal restore the relevant findings. Adding two low-consequence checklist items and marking them green would raise the fraction but change nothing technically.

### Example 2

**Accepted supplier item, wrong configuration.** A navigation unit passed factory acceptance, but the delivered option lacks the time-input module named by the current ICD and runs firmware 4.1 while the integration procedure expects 4.3 message behavior.

Receipt status is accepted; readiness is unmet. The team verifies identity/options, checks approved compatibility, obtains or installs the correct controlled configuration, repeats affected acceptance/interface tests, updates procedure applicability, and records supplier change evidence. Factory pass does not cross the configuration gap.

### Example 3

**Precheck prevents damage.** Two connectors mate mechanically. The controlled interface drawing assigns 28 V power to pin 4; one as-built harness inspection finds pin 4 tied to signal ground. Continuity evidence blocks mating/energization.

The harness is quarantined, discrepancy traced to drawing/build/configuration, affected siblings inspected, repair authorized, and polarity/insulation/continuity repeated. A visual “connector compatible” green would have been dangerously shallow.

### Example 4

**Procedure rehearsal finds an authority gap.** A dry run of a pressure-system activation reaches an alarm. The procedure says `operator stops`, but the operator cannot see the pressure trace; the test conductor can see it but lacks command authority; safety expects an automatic trip that is inhibited in this integration state.

The procedure and temporary architecture are corrected: observation, callout, authority transfer, trip state, thresholds, and abort are explicit. Roles rehearse again. Paper approval alone would not reveal the coupled human/interface hazard.

### Example 5

**Expired calibration invalidates an evidence objective.** A thermal chamber is operational, but the reference sensor calibration expired five days earlier. The step could physically run, yet its intended qualification evidence requires traceable temperature uncertainty.

The gate holds formal evidence acquisition. Options are recalibration, a qualified replacement sensor, or reclassifying a bounded run as diagnostic only under authority. Running now and relabeling later would corrupt evidence provenance.

### Example 6

**Test-double evidence has a boundary.** An actuator emulator supports command, timing, and selected fault tests. Its readiness evidence covers protocol profile P3 and 10–200 ms latency, but not backlash, saturation, thermal trip, current transient, or mechanical limits.

The controller/emulator increment is ready for the declared software-interface objective. It is not ready to claim real actuator performance or safe motion. The gate records excluded behaviors and mandatory repeat tests when production hardware arrives.

### Example 7

**The qualified team is not the executing team.** Day-shift technicians completed clean handling and hazardous-energy rehearsal. A schedule change moves work to night shift, where one assigned technician lacks the new fixture qualification and the safety observer is unavailable.

Previous personnel readiness becomes inapplicable to execution. Reassign qualified staff, train/assess the night shift, or reschedule. A department-level training percentage cannot authorize named roles.

### Example 8

**Bounded deviation, not green status.** A redundant telemetry channel is unavailable. The planned low-energy fit and protocol step can proceed on the primary channel with independent local recording, strict duration, no operational evidence claim, stop on any primary degradation, and a deadline to restore redundancy before environmental testing.

The telemetry-redundancy criterion remains unmet. Authorized deviation DEV-22 defines scope, controls, risk owner, expiry, affected evidence, and closure. A later step cannot inherit readiness from this authorization.

### Example 9

**Software deployment readiness includes data rollback.** A service build is tested, but the database migration is destructive and backups have not been restore-tested. Application rollback alone would leave the old build unable to read new data.

The release holds. The team makes the schema backward compatible or establishes a validated backup/restore and reconciliation path, exercises mixed versions, defines canary authority and stop thresholds, confirms monitoring/on-call roles, and records exact builds/schemas/flags. Passing unit and integration tests did not establish operational integration readiness.

### Example 10

**Post-gate change invalidates selected findings.** After authorization, a facility network security update rotates certificates, changes firewall policy, and restarts the time service. Hardware identity, mounting, and mechanical procedure findings remain valid; identity, network, time, logging, external-interface, and end-to-end procedure findings require reassessment.

Focused impact analysis avoids a ritual full review while preventing green-status inertia. The execution brief uses the revised configuration and decision record.

## Cross-Program Connections

**Platform engineering.** Deployment readiness covers artifact provenance, infrastructure, identity, policy, observability, capacity, change windows, on-call staffing, canary limits, rollback, and external dependencies.

**API and service engineering.** Contract compatibility, version/schema, credentials, quotas, test environments, consumer evidence, failure behavior, and provider change status determine service-integration readiness.

**Data engineering.** Dataset/schema identity, lineage, quality, replay, backfill, reconciliation, retention, privacy, capacity, backup/restore, and rollback are readiness criteria, not post-deployment chores.

**Object-oriented programming.** Passing unit tests and build success are evidence inputs; runtime wiring, versions, resources, data, permissions, and operational contexts determine integration readiness.

**Functional programming.** Pure-core tests can strongly support transformation correctness, while effects, state, concurrency, external systems, data provenance, and operations still require contextual readiness evidence.

**Quality and configuration management.** Nonconformance, inspection, calibration, audit, baseline identity, status accounting, and change control maintain evidence truth.

**Safety, security, and human integration.** Hazards, threats, roles, workload, authority, training, protective controls, emergency response, and dissent create mandatory criteria.

## References

1. NASA, *Systems Engineering Handbook, Section 5.2: Product Integration*, current web edition. <https://www.nasa.gov/reference/5-2-product-integration/>
2. NASA, *Systems Engineering Handbook, Appendix H: Integration Plan Outline*, current web edition. <https://www.nasa.gov/reference/appendix-h-integration-plan-outline/>
3. NASA, *Systems Engineering Handbook, Section 6.7: Technical Assessment*, current web edition. <https://www.nasa.gov/reference/6-7-technical-assessment/>
4. NASA, *Systems Engineering Handbook, Section 5.3: Product Verification*, current web edition. <https://www.nasa.gov/reference/5-3-product-verification/>
5. NASA, *Systems Engineering Handbook, Section 5.4: Product Validation*, current web edition. <https://www.nasa.gov/reference/5-4-product-validation/>
6. NASA, *Systems Engineering Handbook, Section 6.3: Interface Management*, current web edition. <https://www.nasa.gov/reference/6-3-interface-management/>
7. NASA, *Systems Engineering Handbook, Section 6.5: Configuration Management*, current web edition. <https://www.nasa.gov/reference/6-5-configuration-management/>
8. NASA Goddard Space Flight Center, *GSFC-STD-1001A, Rules for the Design, Development, Verification, and Operation of Flight Systems*, System Integration Review criteria. <https://standards.nasa.gov/sites/default/files/standards/GSFC/A/0/gsfc-std-1001A_extension.pdf>
9. U.S. Government Accountability Office, *Technology Readiness Assessment Guide*, GAO-20-48G, 2020. <https://www.gao.gov/products/gao-20-48g>
10. ISO/IEC/IEEE, *15288:2023 Systems and software engineering—System life cycle processes*, 2023. <https://www.iso.org/standard/81702.html>

## Exercises

### Exercise 1

A gate has 12 applicable criteria: eight mandatory and four supplementary. Six mandatory and all four supplementary are met; one mandatory interface criterion has an approved deviation; one mandatory safety-observer criterion is expired. Compute the descriptive completion fraction if `met` alone counts. State the finding and decision treatment for the deviation and expired evidence.

### Exercise 2

Classify the validity of: (a) a calibration valid through 2026-09-30 for a 2026-09-20 test, with no instrument change; (b) a training certificate valid through 2026-10-01 when the executing procedure changed its emergency response materially on 2026-09-15; (c) a supplier qualification for firmware 3.2 when build 3.4 changes timing but not message schema. What additional evidence or action is needed?

### Exercise 3

A team proposes a conditional authorization despite an unavailable secondary monitor. The planned step lasts two hours, primary-monitor failure likelihood is estimated as 0.02 for the step from relevant data, and consequence if undetected is rated catastrophic. Explain why multiplying labels or relying on expected consequence alone is insufficient. Design a defensible conditional authorization or conclude hold.

### Exercise 4

Critique this statement: “The integration package is 95% complete, all leads report green, and the review board approved proceeding provided the remaining actions close as soon as possible.” Rewrite it as a decision record that could be audited.

### Exercise 5

Develop a readiness assessment for integrating a hospital medication pump with patient identity, clinical orders, drug library, network/time/identity services, alarm workflow, electronic record, nurses, pharmacy, and biomedical maintenance. Include evidence validity, configuration, people, environment, safe states, privacy/security, anomalies, rollback, decision authority, and evidence limits.

## Answers to the Exercises

### Answer 1

Met criteria are six mandatory plus four supplementary, so:

$$
F=10/12=0.8333\ldots\approx83.3\%.
$$

The interface criterion remains `unmet`; its deviation is a separate authorization record defining scope, controls, risk, owner, expiry, and downstream evidence limitations. The safety-observer criterion is `expired`, also not met. Ordinary authorization fails because not every mandatory criterion is met. The gate either holds until both are met or an authority competent for both consequences issues bounded deviations where permitted. If an observer is required by law, safety rule, or risk control and cannot be waived, the only valid decision is hold. The fraction has no authority.

### Answer 2

(a) The calibration is temporally fresh and, absent change, may support readiness. Still verify instrument identity/configuration, range, uncertainty, method, environment, traceability, and required accuracy. A date alone is not full validity.

(b) The certificate's calendar date has not expired, but a material procedure change is an invalidation trigger. Assess the delta; brief, train, rehearse, and requalify to the extent required before treating the executing person as ready. Preserve prior competence only for unchanged work.

(c) Schema similarity does not establish timing compatibility. Review the 3.4 change, exact interface contract, scheduling/load/environment, failure behavior, and downstream assumptions. Obtain supplier evidence and run targeted timing/compatibility/regression tests on the exact build. Qualification for 3.2 can support unchanged properties with a documented equivalence argument; it cannot cover changed timing by assertion.

### Answer 3

The 0.02 estimate is conditional on data scope, configuration, duration, environment, independence, and failure definition. `Catastrophic` is an ordinal consequence category, not a numeric unit; multiplying it by 0.02 does not determine acceptability. Expected value can hide a low-likelihood intolerable event, common cause, uncertainty, inability to detect failure, regulatory constraints, and absent recovery.

A defensible conditional authorization exists only if governing safety/risk policy permits single-monitor operation and competent authority accepts it. Controls might include an independent local recording/limit channel, pre- and continuous primary health checks, reduced energy/authority and duration, staffed direct observation, automatic safe state on monitor loss, conservative abort thresholds, no evidence credit requiring redundancy, no hazardous exposure that depends on the missing monitor, stop on any degradation, exact configuration, and expiry at step end. Demonstrate those controls before start. If catastrophic harm can occur after one undetected primary failure or redundancy is a mandatory hazard control, hold until the secondary monitor is restored.

### Answer 4

Defects are: scope/configuration absent; `95%` hides criterion consequence; `complete` may mean documents rather than valid evidence; self-reported green lacks source; remaining actions are unnamed; `provided` does not say what may start; no authority, risk, limits, monitor, abort, owner, deadline, or expiry exists.

An auditable record would say: “Gate IRG-24 assessed integration step INT-08 for items/builds listed in baseline K17 at Facility F2 on 2026-08-31. Of 20 applicable mandatory criteria, 18 are met by evidence links in matrix RM-24. Interface precheck IC-7 and emergency-response rehearsal ER-3 are unmet; no deviation has been approved. Decision: hold all mating and energization. Owners A and B will supply approved as-built continuity results and a passed rehearsal by 2026-09-02. The integration authority will reassess those criteria and any intervening changes. Existing findings expire on change to K17, procedure P9, assigned staff, facility state, or listed interfaces. Dissent D-4 is attached.”

If limited preparatory work is safe, enumerate it separately and prohibit consequential actions.

### Answer 5

Scope one step—for example, a synthetic-patient end-to-end integration in a controlled clinical test environment with no patient connection or production order authority. Establish exact pump serial/hardware, embedded build/hash, drug-library version/signature, disposable set, calibration, patient/order/record schemas, network/time/identity configurations, certificates/policies, alarm routing, procedures, fixtures, safe fluids, and synthetic datasets.

Mandatory criteria include:

- pump receipt, fluid/power/battery integrity, calibration, actuator/sensor limits, watchdog, inhibited/safe state, cleaning/biocompatibility boundaries, and open anomalies;
- correct patient/order/drug/dose/rate semantics and units, provenance, version compatibility, authorization, freshness, conflict behavior, and trace through every interface;
- network loss/latency, independent time uncertainty, identity/certificate validity, least privilege, audit, privacy-approved synthetic data, logging, incident response, and external-service change state;
- approved/rehearsed setup, programming, independent check, start, alarm, occlusion/air/free-flow, battery loss, disconnection, restart, recovery, update, cleaning, maintenance, rollback, and cleanup procedures;
- representative nurse, pharmacy, biomedical, IT/security, safety, and test roles with current training, authorization, staffing, communication, workload, shift/handoff, stop-work, and emergency response;
- facility, test pump/fixtures, safe fluids, network sandbox, order/record doubles, alarm simulator, time/identity services, instrumentation/calibration, synchronized acquisition, data custody, backup, spares, and consumables;
- known anomalies, waivers, prior failures, test-double fidelity exclusions, residual hazards, regulatory/institutional requirements, and independent clinical/safety/security review appropriate to the intended decision;
- safe patient-disconnected state, no unintended order/record side effects, immediate inhibit/stop, data rollback/reconciliation, credential cleanup, pump restoration, anomaly preservation, and controlled re-entry.

Evidence must identify article/build, condition, method, result, criteria, date, reviewer, provenance, limitations, and invalidation triggers. Supplier certificates and prior test results receive credit only through applicability arguments. The gate authority must include the technical, clinical, safety, privacy/security, and institutional authority required for the exposure; no engineer can waive a prohibited patient-safety or privacy condition alone.

Possible decision: authorize only the synthetic, patient-disconnected increment under enumerated versions, trained participants, safe fluid, isolated interfaces, monitoring, and stop thresholds; prohibit clinical deployment and formal claims outside the tested configuration. Hold on any patient/order/drug semantic ambiguity, missing safe-state control, unqualified staff, uncontrolled real data, incompatible version, expired calibration, or unaccepted critical anomaly. Passing this gate and run supports only readiness/evidence for the scoped test—not clinical validation, production reliability, cybersecurity across all threats, regulatory approval, or safe use on patients.
