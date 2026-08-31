---
module_id: SYSENG-066
program: Systems Engineering
level: 2
module_number: 66
title: System Safety Hazards
status: complete
last_verified: 2026-08-31
---

# System Safety Hazards

## One-Page Review

### Governing question

What combinations of system condition, operating context, exposure, and causal mechanism can produce harm; how will the design eliminate or control them; and what verified evidence and authorized decision justify operating the exact configuration with its remaining risk?

### Essential definitions

- A **hazard** is a real or potential condition that can lead to a mishap. State the governing vocabulary because standards differ slightly; do not substitute a component failure, an injury, or a risk score for the hazardous condition.
- A **mishap** is an unplanned event or series of events resulting in death, injury, occupational illness, equipment/property damage, environmental harm, or other losses within the governing policy's scope.
- A **hazardous scenario** connects a hazard to initiating and contributing causes, exposure, system state, controls, and credible mishap consequences. The scenario is the unit of reasoning; a noun such as “battery” is not.
- **Severity** classifies the credible consequence magnitude. **Likelihood** classifies how often the mishap or hazardous scenario is expected under stated exposure and assumptions. **Risk** combines them according to an approved method.
- A **risk matrix** is a policy-defined ordinal lookup. Its cells are categories, not measurements on an interval scale; multiplying category numbers creates arithmetic that the scales do not justify.
- **Initial risk** is assessed before proposed controls are credited. **Current risk** reflects controls actually implemented and supported by evidence. **Residual risk** remains after all credited controls.
- A **safety control** eliminates a hazard or reduces its risk. A control is not creditable merely because it appears in a register: it needs an owner, requirement/design realization, configuration identity, independence assumptions, verification method, result, and continuing effectiveness.
- A **safety constraint** prohibits unsafe behavior or requires behavior needed to prevent or mitigate a mishap. It becomes enforceable through derived requirements allocated to responsible system elements and lifecycle activities.
- A **hazard log** is a configuration-controlled decision record linking hazard identity, scenarios, risk assessments, controls, requirements, evidence, actions, ownership, acceptance, and history.
- **Risk acceptance** is the documented decision by the authorized role to tolerate specified residual risk for a named configuration, scope, and period. The analyst estimates and communicates risk; the spreadsheet does not accept it.

### Central model, mechanism, or theorem

For hazard $h$ in configuration and context $c$, reason through an evidence chain

$$
h,c \rightarrow \{s_i\} \rightarrow \{C_j\} \rightarrow \{R_j\}
\rightarrow \{V_j\} \rightarrow r_{residual} \rightarrow A,
$$

where $s_i$ are credible scenarios, $C_j$ are controls, $R_j$ are allocated safety requirements, $V_j$ are verification results, $r_{residual}$ is the bounded residual-risk judgment, and $A$ is acceptance by the proper authority. Break any link and the closure claim fails.

Use a matrix only as its policy defines it:

$$
r=M(S,L),
$$

not $r=S\times L$. $S$ and $L$ are ordered categories; $M$ is a declared lookup. A movement from one cell to another is meaningful only when evidence supports the changed severity, likelihood, exposure, or scenario.

### Critical invariants

- Hazard analysis covers intended use, reasonably foreseeable misuse, degraded modes, maintenance, transport, storage, emergency response, modification, and disposal—not nominal operation alone.
- Hazard statements identify a hazardous condition and credible harm in a bounded context; they do not stop at “component fails.”
- Causes, hazard, hazardous event/state, exposure, and consequence remain distinct so controls attach to the mechanism they actually influence.
- Initial risk is preserved. Current and residual assessments identify which implemented, verified controls are credited and what uncertainty remains.
- Severity is reduced only when a control changes the credible consequence. Detection, warning, training, or lower exposure usually changes likelihood, not intrinsic consequence.
- Elimination and design changes receive priority over safety devices, warnings, procedures, training, and personal protective equipment. Lower-order controls need explicit justification and human/reliability assumptions.
- Every credited control traces through an unambiguous requirement to design or process realization and objective verification evidence in the applicable configuration.
- Independence, common-cause, bypass, maintenance, power, data, timing, environmental, and diagnostic dependencies of controls are analyzed.
- Open actions, assumptions, waivers, anomalies, control failures, transferred risk, introduced hazards, and aggregate risk remain visible.
- Residual-risk acceptance names the authority, configuration, operating envelope, duration, evidence baseline, restrictions, and reopen criteria.
- Changes and operational evidence trigger reassessment; a closed hazard is not permanently erased.
- No single FMEA, fault tree, HAZOP, STPA study, test, probability estimate, or incident-free period proves hazard completeness or safety.

### Common failures

Common failures include listing components instead of hazards; writing consequences without scenarios; using a matrix as multiplication; lowering severity because an alarm was added; scoring before defining exposure; treating “improbable” as impossible; selecting only nominal modes; blaming an operator without examining interface and workload; crediting a procedure that is unavailable under stress; claiming two controls are independent when they share power, sensors, software, environment, maintenance, or staff; closing an action because a document was issued rather than because the control was verified; omitting software timing and configuration; ignoring cybersecurity-induced unsafe states; transferring risk to maintainers or the public; accepting each hazard separately while aggregate risk remains unacceptable; and allowing configuration changes to invalidate old evidence silently.

### Compact example

A synthetic five-row hazard register uses an explicit severity/likelihood lookup. It contains unique IDs, complete required metadata, five verified controls, four controls at elimination/design/engineered levels, four initially high-or-serious scenarios, two residually serious scenarios, unchanged severity categories, five named acceptance authorities, and one open follow-up action. The executable fixture verifies those declared invariants. It does not show that a real system is safe, that the hazard set is complete, or that the categorical likelihood estimates are calibrated.

### Connections

SYSENG-061 through SYSENG-065 supply failure, causal, reliability, availability, and maintenance evidence; SYSENG-066 governs how that evidence supports harm-centered decisions. SYSENG-067 will structure safety claims and assurance evidence. Requirements, architecture, interfaces, human factors, software assurance, cybersecurity, configuration management, operations, and incident learning all create or consume hazard controls.

## Governing Question

Can the program demonstrate, for each credible system safety hazard and the aggregate operating configuration, that it has identified relevant lifecycle scenarios, prioritized inherently safer design, implemented and verified traceable controls, disclosed uncertainty and dependencies, and obtained residual-risk acceptance from the authorized decision maker?

“The register has no red cells” is not an answer. The governing question concerns a configured socio-technical system: hardware, software, people, procedures, facilities, environment, suppliers, support, and organizational decisions. It also concerns evidence quality. A colored cell can summarize a judgment, but it cannot replace the causal model, control verification, or acceptance record behind that judgment.

## Why This Matters

Reliability asks whether intended functions persist; system safety asks how the system can cause harm, including while components operate as designed. A highly reliable actuator can move at the wrong time because its requirement, control logic, sensor interpretation, mode model, or human-machine interface is wrong. Conversely, a component failure can be benign because containment prevents exposure. Treating safety as an extension of component failure counting misses both cases.

MIL-STD-882E with Change 1 defines a lifecycle system-safety process for identifying hazards, assessing and reducing associated risk, verifying reductions, and accepting residual risk. The NASA System Safety Handbooks integrate hazard analysis with risk-informed decision making and safety assurance rather than treating a completed worksheet as proof. OSHA's process-safety rule likewise requires an analysis appropriate to process complexity, consideration of prior incidents, engineering and administrative controls, control failures, facility siting, and human factors, plus documented resolution and lifecycle revalidation.

The practical consequence is that system safety changes engineering decisions early. It can remove hazardous energy, constrain functions, separate incompatible materials, isolate propagation paths, change interfaces, add monitoring, alter maintenance access, or restrict operations. After architecture freezes, programs are more likely to depend on warnings and procedures whose effectiveness varies with workload, training, staffing, environmental stress, and organizational conditions.

Safety is never an unlimited claim. Relevant standards define scope and decision rights, and domains impose additional law, regulation, and certification criteria. A program must state what harms and populations are covered, which risk method governs, and which authority can accept which risk. This module teaches a portable reasoning discipline; it does not replace domain-specific compliance or authorization.

## Prerequisites and Retrieval

Before constructing or reviewing a hazard analysis, retrieve:

1. applicable statutes, regulations, contracts, standards, certification basis, organizational safety policy, risk matrix, acceptance thresholds, and named acceptance authorities;
2. mission/business objectives, concept of operations, intended use, foreseeable misuse, stakeholders, exposed populations, environments, sites, operating envelopes, and loss categories;
3. system boundary, architecture, interfaces, functional flows, physical energy/material inventories, modes, states, timing, autonomy, external services, and neighboring systems;
4. lifecycle scenarios for manufacture, integration, test, transport, storage, installation, startup, operation, degraded/emergency operation, maintenance, modification, recovery, decommissioning, and disposal;
5. requirements and constraints, design descriptions, control algorithms, data models, software versions, cybersecurity assumptions, human interfaces, procedures, staffing, training, and personal protective equipment;
6. historical incidents, near misses, anomalies, recalls, field reports, lessons learned, precursor data, maintenance findings, supplier notices, and evidence from analogous systems—with limits on analogy stated;
7. supporting analyses such as PHL/PHA, subsystem and system hazard analyses, operating/support hazard analysis, FMEA/FMECA, fault trees, event trees, HAZOP, functional hazard analysis, STPA, human-factors analysis, health-hazard analysis, PRA, and common-cause analysis;
8. control records: stable identifiers, owners, derived requirements, allocations, implementation artifacts, verification/validation plans and results, independence arguments, diagnostic coverage, inspection/maintenance intervals, and configuration effectivity;
9. open findings, assumptions, waivers/deviations, temporary controls, compensating measures, overdue actions, accepted risks, dissent, and decisions scheduled for review;
10. configuration baselines, change requests, hazard-log history, operational restrictions, release/readiness decisions, emergency plans, and criteria that reopen an assessment.

Perform a retrieval challenge before accepting completeness: choose one high-consequence mission thread and trace it through nominal, degraded, maintenance, emergency, and recovery states. Follow energy, commands, data, authority, people, and barriers across every interface. If the team cannot retrieve the current requirement, implementation, verification result, risk decision, and effectivity for a credited control, the control is not yet auditable.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish hazard, cause, hazardous state/event, exposure, mishap, consequence, severity, likelihood, and risk;
2. write bounded, actionable hazard statements and scenario chains;
3. select complementary hazard-identification and causal-analysis methods across the lifecycle;
4. construct and interpret an ordinal risk matrix without invented arithmetic precision;
5. prioritize hazard elimination and design controls over warnings and procedures;
6. derive traceable safety constraints and requirements from hazards;
7. evaluate control effectiveness, independence, common cause, bypass, maintenance, and verification evidence;
8. maintain a configuration-controlled hazard log with initial, current, and residual risk;
9. integrate software, human factors, cybersecurity, operations, change, and incident feedback into system safety;
10. formulate bounded residual-risk recommendations for decision by the proper authority.

## Core Exposition

**Establish governance before scoring.** Name the governing vocabulary, consequence scope, severity and likelihood definitions, matrix, decision thresholds, and acceptance authority. Mixing matrices or silently changing definitions makes comparisons invalid. Regulatory or contractual definitions prevail over a generic textbook formulation.

**Set the system and loss boundary.** Describe what is inside the system, what it exchanges with its environment, who can be harmed, and which lifecycle phases/configurations apply. Include operators, maintainers, contractors, public, environment, assets, and mission where policy covers them. Record external dependencies instead of pretending them away.

**Identify hazardous energy, material, information, and authority.** Traditional prompts include mechanical motion, pressure, electricity, heat, radiation, fire, explosives, chemicals, biological agents, gravity, and stored energy. Digital systems add unsafe commands, corrupted state, timing/order errors, stale or misleading data, loss of authority separation, and automation surprises. Information is safety-relevant when it controls exposure to physical or consequential harm.

**Model functions and constraints.** Ask what must never happen, what must happen, when, in which sequence, and under which modes. A control action may be unsafe when provided, not provided, provided too early/late/out of order, applied too long, or stopped too soon. This catches interaction hazards that a component-failure list misses.

**Write analyzable hazard statements.** A useful form is: under context $c$, the system enters or maintains condition $h$, enabling consequence $m$ for exposed target $p$. Keep causal hypotheses separate. “Pump fails” is a failure mode; “vessel pressure exceeds containment capability during blocked outlet operation, enabling rupture and personnel exposure” is a hazard scenario.

**Build multiple scenarios per hazard.** One hazard may arise from distinct initiating causes, modes, environments, human interactions, software behaviors, or external events. Each path can require different controls. Conversely, one cause can contribute to several hazards. Use stable many-to-many traceability rather than duplicating prose until it diverges.

**Use complementary analysis methods.** A preliminary hazard list and PHA establish early breadth. Subsystem/system and operating/support analyses mature detail. FMEA starts from failure modes; fault trees reason backward from undesired events; event trees reason forward through barriers; HAZOP explores parameter deviations; STPA examines unsafe control and constraints. Choose methods by question, architecture maturity, and domain. Record blind spots.

**Include experience without overgeneralizing it.** Incidents and near misses reveal real mechanisms, organizational conditions, and barrier failures. Analogous-system data can prioritize inquiry, but different use, environment, scale, software, interfaces, or controls limit transfer. Absence of reported incidents may reflect low exposure or weak reporting rather than low risk.

**Describe exposure explicitly.** A hazardous condition may exist continuously while harm requires a person, asset, environment, or mission state to be exposed. Define occupancy, duration, demand rate, mission phases, maintenance presence, geography, and protective separation. Avoid double-counting exposure in both scenario frequency and consequence likelihood.

**Assess severity from credible consequence.** Select the worst credible—not physically imaginable without bound and not merely expected—consequence under the governing definition. State assumptions about propagation, occupancy, emergency response, and protective features. If uncertainty spans categories, show the range or conservatively select according to policy.

**Assess likelihood with a declared basis.** State whether the category refers to hazard occurrence, mishap occurrence, per-demand probability, per-hour rate, lifetime frequency, or qualitative expectation. Use field data, testing, models, expert elicitation, and analogous evidence with uncertainty. Do not map a component failure rate directly to mishap likelihood when exposure and barriers intervene.

**Treat matrix results as ordered decisions.** A matrix translates severity and likelihood categories into risk categories that trigger action and authority. It does not provide cardinal distance: two “medium” risks are not equal, and a move from high to serious is not a known percentage reduction. Preserve the underlying scenario and evidence.

**Assess initial risk before crediting proposals.** Initial risk shows the problem the design must address and prevents a proposed control from disappearing into the baseline. Current risk credits only implemented controls with adequate evidence. Target risk guides design. Residual risk is assessed after all credited controls and restrictions. Keep all states and dates.

**Apply control precedence.** MIL-STD-882E's order emphasizes eliminating hazards through design selection; reducing risk through design alteration; incorporating engineered features or devices; providing warning devices; then using procedures and training. Occupational hierarchies commonly separate elimination, substitution, engineering controls, administrative controls, and PPE. Apply the hierarchy mandated by the domain and explain why a lower-order control remains necessary.

**Design out the hazard when practicable.** Remove energy or material, substitute a less hazardous process, limit inventory, prevent incompatible states, separate people from exposure, simplify authority, or make unsafe commands structurally impossible. Elimination claims require boundary care: moving a hazardous process to a supplier transfers ownership and exposure; it may not eliminate system-level harm.

**Engineer prevention and mitigation.** Prevention stops the hazardous state or event; mitigation limits consequences after it begins. Guarding, containment, interlocks, relief, fault containment, independent shutdown, rate limiting, safe state, and physical separation can be effective. Analyze failure, bypass, inspection, test interval, diagnostic coverage, environmental qualification, and recovery.

**Avoid false independence.** Two barriers are not independent because they have different names. Trace shared power, sensors, processors, software requirements/code, networks, clocks, cooling, physical location, environment, maintenance, calibration, supplier, and decision makers. Common requirements errors can defeat diverse implementations.

**Use warnings and procedures honestly.** Warnings must be detectable, discriminable, timely, intelligible, prioritized, and actionable under realistic workload and impairment. Procedures require availability, time, access, training, staffing, authority, and opportunity. Model failure to execute and foreseeable workarounds; do not label the operator as the root cause.

**Derive enforceable requirements.** Translate controls into measurable “shall” statements with trigger, behavior, limit, timing, mode, interfaces, failure response, and verification. Allocate each requirement to responsible elements and link it back to hazards/scenarios. “The system shall be safe” and “provide an alarm” are not verifiable control requirements.

**Verify the control, then validate the scenario.** Inspection can confirm a guard; test can exercise an interlock; analysis can show containment margin; demonstration can assess a procedure. Verification proves specified implementation under stated conditions. Validation asks whether the integrated controls actually address the operational hazard with representative people, environment, timing, degraded states, and foreseeable misuse.

**Treat software as a system-safety contributor.** Software can create, control, detect, mitigate, or recover from hazardous conditions. Analyze incorrect value, timing, sequence, mode, authority, persistence, initialization, concurrency, stale data, overflow, resource exhaustion, configuration, update, rollback, and interface behavior. NASA-STD-8739.8B makes hazard-analysis traceability central to safety-critical software determination. Random hardware failure-rate mathematics is not a substitute for systematic software assurance.

**Integrate cybersecurity without collapsing disciplines.** Threat actors can exploit interfaces to create unsafe commands, disable controls, falsify displays, or delay response. Safety analysis supplies consequence and safe-state knowledge; security analysis supplies adversary capability and attack paths. Shared controls require coordinated assumptions, but malicious likelihood and random-failure likelihood should not be forced into one unsupported number.

**Analyze human and organizational context.** Examine interface design, workload, fatigue, staffing, handover, conflicting goals, supervision, training, maintainability, incentives, authority, communication, and emergency conditions. “Human error” is an observation requiring explanation. A robust system tolerates predictable slips and makes dangerous actions difficult, detectable, and recoverable.

**Maintain a live hazard log.** At minimum record ID, title, statement, boundary/configuration, lifecycle modes, exposed targets, causes, mishaps, assumptions, initial/current/residual risk, controls, precedence, requirements, evidence, dependencies, owners, actions, status, acceptance, effectivity, and history. Use controlled vocabularies where helpful without flattening scenario detail.

**Do not close by paperwork.** A hazard may be eliminated, controlled with accepted residual risk, transferred with explicit agreement, or remain open. Closure means the specified evidence and decision criteria are met, not that a meeting occurred. Preserve unresolved uncertainty and restrictions. Reopen when an assumption, configuration, control, exposure, incident, or governing threshold changes.

**Manage aggregate and transferred risk.** Individually acceptable hazards can combine through shared controls, simultaneous exposure, emergency interactions, workload, or common environment. A control for one hazard can create another: an automatic shutdown may remove propulsion in a dangerous location. Review system-level risk and receiving owners, not only rows independently.

**Connect change to reassessment.** Hardware substitutions, software releases, supplier/process changes, operating-envelope extensions, staffing reductions, maintenance revisions, cybersecurity patches, and temporary deviations can invalidate safety evidence. Change approval should identify affected hazards, controls, assumptions, verification, training, restrictions, and acceptance.

**Use operations as evidence, not absolution.** Monitor control demands, bypasses, alarms, near misses, anomalies, injuries, maintenance findings, leading indicators, and exposure. Investigate weak signals and feed findings into analysis. Incident-free operation increases exposure evidence only within the observed configuration and reporting quality; it does not prove unidentified hazards absent.

**Plan emergency response as mitigation.** Detection, evacuation, rescue, fire suppression, containment, medical response, communications, and continuity reduce consequences. Verify capacity, access, timing, environmental survivability, drills, and coordination. Emergency plans never excuse avoidable design hazards.

**Carry safety through retirement.** Decommissioning introduces unfamiliar configurations, degraded documentation, residual pressure/charge, hazardous materials, lifting/cutting, obsolete software, and changed staff. Preserve hazard knowledge and controls through disposal; retirement is an engineered lifecycle state.

The following fixture tests the internal consistency of declared synthetic hazard metadata. The matrix is an explicit lookup; no category multiplication occurs.

<!-- bijux-verify: {"id":"system-safety-hazard-register-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"hazards=5\nunique_ids=1\ncomplete_rows=5\nverified_controls=5\ndesign_priority_controls=4\ninitial_high_or_serious=4\nresidual_high_or_serious=2\nseverity_unchanged=1\nacceptance_authorities=5\nopen_actions=1\nstatus=declared_hazard_register_consistent\nevidence=synthetic_metadata_only\n","stderr":""}} -->
```python
matrix = {
    4: {5: "high", 4: "high", 3: "high", 2: "serious", 1: "serious"},
    3: {5: "high", 4: "high", 3: "serious", 2: "medium", 1: "medium"},
    2: {5: "serious", 4: "serious", 3: "medium", 2: "medium", 1: "low"},
    1: {5: "medium", 4: "medium", 3: "low", 2: "low", 1: "low"},
}
hazards = [
    {"id": "HZ-001", "initial_severity": 4, "residual_severity": 4,
     "initial_likelihood": 3, "residual_likelihood": 1,
     "control": "limit cell propagation by thermal isolation", "precedence": 2,
     "verified": True, "authority": "program executive", "open_actions": 0},
    {"id": "HZ-002", "initial_severity": 3, "residual_severity": 3,
     "initial_likelihood": 4, "residual_likelihood": 2,
     "control": "inhibit actuator motion through independent interlock", "precedence": 3,
     "verified": True, "authority": "chief engineer", "open_actions": 0},
    {"id": "HZ-003", "initial_severity": 4, "residual_severity": 4,
     "initial_likelihood": 2, "residual_likelihood": 1,
     "control": "provide verifiable stored-energy isolation", "precedence": 2,
     "verified": True, "authority": "program executive", "open_actions": 1},
    {"id": "HZ-004", "initial_severity": 3, "residual_severity": 3,
     "initial_likelihood": 3, "residual_likelihood": 1,
     "control": "reduce toxic inventory and contain release", "precedence": 2,
     "verified": True, "authority": "site director", "open_actions": 0},
    {"id": "HZ-005", "initial_severity": 2, "residual_severity": 2,
     "initial_likelihood": 3, "residual_likelihood": 1,
     "control": "prioritize and cross-check hazardous-state alarms", "precedence": 4,
     "verified": True, "authority": "operations director", "open_actions": 0},
]
required = {"id", "initial_severity", "residual_severity",
            "initial_likelihood", "residual_likelihood",
            "control", "precedence", "verified", "authority", "open_actions"}
initial = [matrix[row["initial_severity"]][row["initial_likelihood"]] for row in hazards]
residual = [matrix[row["residual_severity"]][row["residual_likelihood"]] for row in hazards]
print(f"hazards={len(hazards)}")
print(f"unique_ids={int(len({row['id'] for row in hazards}) == len(hazards))}")
print(f"complete_rows={sum(required <= row.keys() for row in hazards)}")
print(f"verified_controls={sum(row['verified'] for row in hazards)}")
print(f"design_priority_controls={sum(row['precedence'] <= 3 for row in hazards)}")
print(f"initial_high_or_serious={sum(value in {'high', 'serious'} for value in initial)}")
print(f"residual_high_or_serious={sum(value in {'high', 'serious'} for value in residual)}")
print(f"severity_unchanged={int(all(row['initial_severity'] == row['residual_severity'] for row in hazards))}")
print(f"acceptance_authorities={sum(bool(row['authority']) for row in hazards)}")
print(f"open_actions={sum(row['open_actions'] for row in hazards)}")
print("status=declared_hazard_register_consistent")
print("evidence=synthetic_metadata_only")
```

The `severity_unchanged` assertion is intentionally narrow: the fixture stores one severity field rather than inventing a lower residual consequence. Real controls sometimes reduce consequence, but that conclusion requires a changed physical/functional consequence model. The fixture does not validate the selected categories, control adequacy, independence, completeness, or acceptance decisions.

## Definitions and Notation

Let $H$ be the identified hazard set for a declared system boundary, configuration, lifecycle scope, and date. Completeness is never established merely by enumerating $H$; instead record the methods, participants, inputs, assumptions, and coverage arguments that generated it.

For hazard $h\in H$, let scenarios $s\in S_h$ describe initiating conditions $I_s$, contributing conditions $K_s$, exposure $E_s$, hazardous state/event $Q_s$, controls $C_s$, and mishap consequence $D_s$:

$$
s=(I_s,K_s,E_s,Q_s,C_s,D_s).
$$

This tuple is a reasoning aid, not a claim that events are independent or linearly ordered. Feedback, concurrency, organizational decisions, and control actions can form loops.

Let severity $S_s\in\{1,\ldots,m\}$ and likelihood $L_s\in\{1,\ldots,n\}$ be ordered categories whose textual definitions come from governing policy. A risk category is

$$
R_s=M(S_s,L_s),
$$

where $M$ is the approved matrix. Because the inputs are ordinal, $S_sL_s$, category averages, and arithmetic reductions have no general semantic validity.

For control $c$, define traceability relation

$$
c\leftrightarrow requirement\leftrightarrow allocation\leftrightarrow implementation
\leftrightarrow verification\ result\leftrightarrow configuration.
$$

Let $A(r,cfg,t)$ denote acceptance of specified residual risk $r$ for configuration `cfg` and operating period/scope $t$ by an authorized role. Acceptance is invalid outside those bounds.

## Mechanisms, Invariants, or Proof Structure

A defensible hazard closure is an assurance argument with at least these links:

1. **Scope validity:** governing harm categories, exposed stakeholders, system boundary, configurations, lifecycle states, environments, and decision authorities are explicit.
2. **Identification validity:** complementary top-down, bottom-up, functional, operational, human, software, interface, and experience-based methods cover the intended scope; limitations are recorded.
3. **Scenario validity:** causes, contributing conditions, exposure, hazardous state/event, mishap, and consequence are causally coherent and do not collapse into a label.
4. **Risk validity:** severity and likelihood use the approved definitions, evidence basis, uncertainty, time/exposure unit, and matrix; initial risk is preserved.
5. **Control validity:** controls address identifiable scenario links, follow the required precedence, include dependencies and failure modes, and avoid unexamined transferred or introduced risk.
6. **Requirements validity:** each credited control is allocated as precise, verifiable constraints/requirements with owner and effectivity.
7. **Evidence validity:** implementation and verification/validation results match the configuration, environment, interfaces, people, timing, and failure/degraded conditions being credited.
8. **Decision validity:** current/residual risk, aggregate effects, open uncertainty, restrictions, actions, dissent, and review triggers are visible to the correct acceptance authority.
9. **Lifecycle validity:** configuration change, operational evidence, control degradation, incidents, and disposal feed back into the living analysis.

The structure is defeasible: new evidence can invalidate a premise. “Closed” therefore means the current, bounded decision criteria are satisfied—not that the hazard can never recur or the analysis can never change.

## Alternatives and Trade-Offs

**Broad early analysis versus detailed late analysis.** Early PHL/PHA work can influence architecture but operates with uncertainty. Later analyses have detail but less design freedom. Use progressive refinement with stable traceability, not a choice between the two.

**Qualitative matrix versus quantitative risk model.** A matrix is accessible and ties categories to governance, but compresses uncertainty and creates boundary effects. Quantitative models support sensitivity and aggregation when data/models are credible, yet can manufacture precision. Use the simplest method adequate for the decision and disclose limitations.

**Prevention versus mitigation.** Prevention reduces hazardous-event occurrence; mitigation limits harm. Prevention often avoids exposure entirely, while mitigation can address unavoidable hazards. Defense in depth may use both, but layers need independence analysis and upkeep.

**Passive versus active controls.** Passive containment and separation can work without detection or command but may add mass, space, or cost. Active interlocks and shutdowns adapt to conditions but add sensors, logic, power, timing, diagnostics, and spurious-actuation hazards.

**Automation versus human authority.** Automation can react rapidly and consistently, but may act on incorrect mode/data or surprise operators. Human confirmation adds judgment but also delay and workload. Allocate authority by timing, observability, reversibility, failure consequence, and fallback—not ideology.

**Operational restriction versus redesign.** Restriction can safely bound a temporary configuration or rare mission, but burdens compliance and can erode. Redesign may be expensive or introduce hazards. State duration, monitoring, owner, removal criteria, and accepted risk for temporary restrictions.

**Centralized versus federated hazard ownership.** A central safety team provides consistent governance; subsystem owners hold detailed knowledge and implementation authority. Use centralized methods/independent challenge with accountable distributed ownership, avoiding a register no engineer owns.

## Failure Modes and Misconceptions

- **“Hazard equals failed part.”** A failure is one cause; hazards can emerge from correct components and interactions. Write the hazardous condition and consequence path.
- **“Severity times likelihood equals risk.”** Ordinal labels do not support multiplication. Apply the approved lookup and retain the evidence behind each axis.
- **“An alarm reduces severity.”** An alarm usually changes response probability. Severity changes only if credible consequence magnitude changes.
- **“Improbable means impossible.”** Rare categories still represent risk, often with high uncertainty. Preserve consequence controls and monitoring.
- **“The operator caused it.”** Examine interface, workload, cues, procedure, training, staffing, authority, and organizational context before attributing cause.
- **“Two barriers mean independence.”** Shared sensors, power, code, location, environment, maintenance, or requirements can defeat both.
- **“A passed component test verifies the safety control.”** Integrated timing, modes, interfaces, environmental limits, and adverse conditions can invalidate component evidence.
- **“Software has no random failure rate, so it is not a hazard cause.”** Systematic requirements, design, code, data, timing, and configuration faults can create unsafe behavior.
- **“Security owns malicious events.”** Cyber causes remain security work, but safety must analyze resulting hazardous states and coordinate controls.
- **“The procedure is the control.”** Only if people can obtain, understand, and execute it correctly in representative conditions, and evidence supports that credit.
- **“No incidents proves low risk.”** Exposure may be small, reporting incomplete, or controls lucky. State the statistical and observational limits.
- **“Accepted means safe forever.”** Acceptance is bounded by configuration, authority, evidence, restrictions, and time; triggers can reopen it.
- **“Closing every row closes system risk.”** Aggregate, coupled, common-cause, and introduced risks require system-level review.
- **“Emergency response replaces prevention.”** Response mitigates consequences and can fail; design precedence still applies.
- **“Disposal is outside engineering.”** Retirement changes barriers and exposes different people. Include it in lifecycle scope.

## Worked Examples

### Example 1

An analyst writes “brake controller fails” and assigns catastrophic severity. This is not yet a hazard: it gives no mode, context, exposure, or harm path. Rewrite it as: “During downhill autonomous travel with a pedestrian in the stopping corridor, commanded braking torque is absent or delayed, allowing loss of separation and fatal collision.” Candidate causes include power loss, stale speed data, wrong mode, saturated actuator, timing defect, or maintenance misconfiguration. Controls can now target speed/route separation, independent stopping, command monitoring, safe-state behavior, and verification under downhill load. The conclusion remains bounded: the rewrite improves analyzability but does not establish completeness or risk.

### Example 2

A maintenance team must open a hydraulic accumulator circuit. “Use lockout procedure and face shield” relies heavily on administrative action and PPE. The analysis identifies stored pressure remaining after pump shutdown. Higher-priority controls add a lockable isolation point, automatic bleed to a monitored safe pressure, a mechanical indicator independent of the controller, and a connector that cannot be opened above a pressure threshold. The procedure still defines verification and authorization. Severity remains potentially fatal if isolation fails; likelihood can be reassessed only after representative verification and inspection/maintenance assumptions are established.

### Example 3

A battery enclosure can propagate one cell's thermal runaway to adjacent cells and occupied space. Initial risk is high under the program matrix. The team first reduces inventory and changes spacing/material selection, then adds propagation barriers, directed venting, detection, and operational charge limits. A smoke alarm alone would not prevent propagation. Tests must represent aged cells, worst credible state of charge, manufacturing variation, enclosure pressure, vent blockage, temperature, and configuration. Passing one demonstration supports only the tested envelope; uncertainty and field monitoring remain.

### Example 4

An infusion controller computes the correct dose but applies a stale patient-weight value after a network reconnect. Every processor functions as designed, so a hardware FMEA may miss the hazard. A control-oriented analysis finds an unsafe action: infusion begins when data provenance and freshness are invalid. Requirements inhibit delivery, display the conflicting values, require deliberate reconciliation, log authority, and prevent silent fallback. Verification covers reconnect timing, duplicated messages, clock skew, rollback, partial persistence, and alarm workload. Software assurance is traceable to the system hazard rather than treated as generic code quality.

### Example 5

Two scenarios receive severity categories 4 and 2 and likelihood categories 1 and 2. Multiplication gives both “4,” inviting the claim that they are equivalent. The approved lookup instead classifies them serious and medium because policy treats catastrophic-improbable risk differently from marginal-remote risk. Even that categorization does not mean all serious risks are equal. Reviewers retain the consequences, exposure, evidence uncertainty, controls, and acceptance authority. The example demonstrates why numeric-looking category labels are not cardinal measurements.

### Example 6

During an emergency, one console presents twelve simultaneous alarms. A procedure directs the operator to isolate a toxic release within thirty seconds. Testing the procedure after classroom rehearsal in a quiet room is weak evidence. The hazard review examines alarm prioritization, masking, diagnosis cues, workload, staffing, protective equipment, communication, and time available. Design changes suppress consequential alarms, highlight source confidence, automate a reversible isolation, and preserve manual override. Representative simulations include noise, competing failures, fatigue-relevant schedules, and ambiguous sensors. “Operator error” is replaced by testable system conditions.

### Example 7

A primary valve and an emergency shutdown valve appear to provide two barriers. Dependency analysis shows both receive position from one sensor, power from one bus, and maintenance from the same procedure; a miscalibrated sensor can keep both open while indicating closed. The team adds diverse pressure evidence, separates power, changes proof testing, and prevents common calibration data from silently propagating. A fault tree helps expose common cause, but evidence must also address systematic specification and maintenance errors that simple independence probabilities omit.

### Example 8

A remote service interface can command a crane into maintenance mode, disabling collision avoidance. Safety analysis identifies unintended motion near maintainers; threat analysis identifies credential theft and replay paths. Joint controls require authenticated, fresh, authorized commands; local physical consent; restricted motion/energy in maintenance mode; visible state; audit; and fail-safe communication loss. Safety does not assign an unsupported random probability to the attacker, and security does not stop at confidentiality. Both disciplines verify the shared system behavior and manage possible control conflicts.

### Example 9

A supplier substitutes a pressure transducer with the same range and connector. Procurement calls it replacement in kind, but the new device has slower response, a different diagnostic mode, and shared firmware with the shutdown channel. Change review traces affected hazard controls, timing requirements, common-cause assumptions, software configuration, calibration procedure, spares, and verification. Acceptance of the old configuration does not transfer automatically. Release is withheld until updated evidence is reviewed or a bounded temporary restriction is accepted by the authorized role.

### Example 10

A retired test facility has been unpowered for months. A disposal plan assumes it is inert, but capacitors retain charge, gas cylinders remain connected, software-controlled locks no longer boot, labels have faded, and the experienced team has left. The retirement hazard analysis inventories stored energy/material, verifies isolation with independent instruments, establishes access control and lifting/cutting constraints, and archives disposition records. The result illustrates lifecycle continuity: normal-operation controls and expertise may disappear exactly when dismantling creates new exposure.

## Cross-Program Connections

**Reliability and availability.** FMEA, FTA, common-cause analysis, failure data, diagnostic coverage, and repair models inform scenarios and control effectiveness. Reliability of a safety device matters, but safety also covers systematic interactions and correct-but-unsafe behavior.

**Requirements and architecture.** Hazards generate safety constraints, allocations, separation, fault containment, modes, degraded behavior, and verification needs. Architectural trade studies must expose risk transferred across boundaries.

**Software and API engineering.** Contracts, authorization, idempotency, ordering, timeouts, retries, schema evolution, observability, rollout, and rollback can be safety controls or hazard causes. Safety-critical interfaces require semantic and temporal guarantees, not only syntactic compatibility.

**Data engineering.** Provenance, freshness, quality, access, retention, lineage, model/data drift, and replay affect control decisions and evidence. Dashboards summarize hazards but cannot become the sole decision record without configuration and auditability.

**Platform engineering.** Deployment guardrails, isolation, policy enforcement, secrets, identity, fleet configuration, feature flags, rollback, and incident telemetry influence physical and operational safety. Shared platforms can create common-cause exposure across products.

**Human factors and operations.** Work-as-done, staffing, workload, fatigue, alarm design, maintainability, training, emergency response, and organizational incentives determine whether controls are usable and resilient.

**Cybersecurity.** Threats can drive hazardous states; safety consequences can prioritize defenses. Keep adversarial and accidental causal models distinct while coordinating shared requirements and assurance.

**Safety cases and governance.** The next module structures claims, evidence, context, assumptions, and rebuttals. A hazard log supplies governed evidence, but neither the log nor the case replaces authorized risk decisions.

## References

1. U.S. Department of Defense, [MIL-STD-882E, System Safety, Revision E with Change 1—official ASSIST document record](https://quicksearch.dla.mil/qsDocDetails.aspx?ident_number=36027), 2023.
2. NASA, [NASA System Safety Handbook, Volume 1: System Safety Framework and Concepts for Implementation, NASA/SP-2010-580](https://ntrs.nasa.gov/api/citations/20120003291/downloads/20120003291.pdf), 2011.
3. NASA, [NASA System Safety Handbook, Volume 2: System Safety Concepts, Guidelines, and Implementation Examples, NASA/SP-2014-612](https://ntrs.nasa.gov/api/citations/20150015500/downloads/20150015500.pdf), 2015.
4. NASA Office of Safety and Mission Assurance, [System Safety discipline policy and guidance index](https://sma.nasa.gov/sma-disciplines/system-safety), accessed 2026-08-31.
5. NASA Technical Standards System, [NASA-STD-8739.8B Software Assurance and Software Safety Standard—active standard record](https://standards.nasa.gov/standard/NASA/NASA-STD-87398), 2022.
6. NASA, [NASA-STD-8739.8B Software Assurance and Software Safety Standard](https://standards.nasa.gov/sites/default/files/standards/NASA/B/0/NASA-STD-87398RevB.pdf), 2022.
7. U.S. Occupational Safety and Health Administration, [29 CFR 1910.119: Process Safety Management of Highly Hazardous Chemicals](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119), current electronic regulation accessed 2026-08-31.
8. U.S. Occupational Safety and Health Administration, [Appendix C to 29 CFR 1910.119: Compliance Guidelines and Recommendations for Process Safety Management](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.119AppC), accessed 2026-08-31.
9. National Institute for Occupational Safety and Health, [Hierarchy of Controls](https://www.cdc.gov/niosh/hierarchy-of-controls/about/index.html), 2024.
10. Federal Aviation Administration, [Safety Management System Policy and Requirements reference library](https://www.faa.gov/about/initiatives/sms/reference_library/policy_and_requirements), accessed 2026-08-31.

## Exercises

### Exercise 1

An autonomous warehouse robot moves 900 kg pallets among workers, visitors, charging stations, fire exits, and manually operated forklifts. Produce three hazard statements covering nominal operation, degraded sensing, and maintenance. For one hazard, construct two distinct scenarios, assign illustrative initial risk using a declared 4-by-5 matrix, propose controls in precedence order, derive two verifiable requirements, and specify evidence and residual-risk authority. State all assumptions and evidence limits.

### Exercise 2

A review board receives a register with columns `hazard`, `severity`, `likelihood`, `S×L`, and `color`. The author averaged scores across 28 rows, lowered severity after adding training, and closed all green rows. Diagnose the conceptual and governance defects. Propose a minimally sufficient replacement record and explain what conclusions a matrix can and cannot support.

### Exercise 3

A high-pressure cleaning skid has a pump, accumulator, hoses, software pressure control, relief valve, emergency stop, maintenance isolation, and operator procedure. Develop a harm-centered scenario for hose rupture and another for stored energy during maintenance. Allocate prevention and mitigation controls, identify at least three common-cause/dependency questions, and design a verification strategy that distinguishes component verification from integrated validation.

### Exercise 4

A remotely updated clinical device receives commands through an API, estimates state from patient data, and asks a nurse to confirm exceptional actions. Analyze one scenario in which software timing, cyber compromise, and human workload interact to create harm. Keep safety and security likelihood reasoning distinct. Derive constraints covering command freshness, authorization, mode, display, fallback, and recovery, then identify representative adversarial and operational tests.

### Exercise 5

A program has individually accepted residual risks for ten hazards. A new software release changes alarm priorities, maintenance mode, and failover timing while an operational waiver permits reduced staffing for six months. Explain how to evaluate change impact, aggregate risk, transferred risk, evidence validity, temporary restrictions, acceptance authority, and reopen criteria. Provide a decision-ready outline rather than a simple approve/reject answer.

## Answers to the Exercises

### Answer 1

Assume speeds up to 2 m/s, mapped mixed-use aisles, a four-level severity scale, five-level likelihood scale, and the illustrative lookup used in the chapter fixture; no field-rate data are available. Three hazards are: (1) during pallet transport near a person, the robot maintains motion without adequate separation, enabling crushing or fatal impact; (2) with degraded localization or obstacle sensing, the robot enters a forklift lane or blocks an emergency exit, enabling collision or delayed evacuation; (3) during service with stored electrical/mechanical energy, motion or discharge occurs while a maintainer is within the mechanism, enabling severe injury.

For hazard 1, scenario A is occluded pedestrian entry during nominal autonomous travel; scenario B is stale localization after network recovery while the controller believes the aisle is clear. Assign severity 4 and illustrative likelihood 3, producing `high` by lookup—not multiplication. Controls in order: physically separate pedestrian and robot routes where practicable; reduce speed/energy in shared zones; add diverse protective sensing and a safety-rated stop; provide clear state warnings; then use access/training procedures.

Requirements include: “The robot shall prevent commanded traction above 0.3 m/s whenever either independent shared-zone occupancy channel reports occupied or invalid, within 100 ms of the report,” and “Loss, conflict, or staleness beyond 150 ms of localization used for motion authority shall transition the robot to a monitored stop before the declared protective separation is consumed.” Verify timing, stopping distance, sensor independence, invalid/stale/conflicting data, occlusion, maximum load, surface, battery state, and mixed forklift traffic; validate with representative users without placing them at risk. The safety manager owns analysis, systems/hardware/software owners implement controls, and the named program executive accepts any high-consequence residual risk according to program policy. Evidence remains synthetic until site-specific exposure, test, independence, and human-factors results exist.

### Answer 2

The table confuses a hazard label with a scenario, treats ordinal categories as numbers, invents meaning through multiplication and averaging, changes severity without changing consequence, and equates a green decision category with closure. It omits boundary/configuration, exposed target, causes, mishap, category definitions, evidence, uncertainty, controls, requirements, verification, dependencies, ownership, actions, residual-risk decision, and history. Averaging can allow many low labels to conceal one catastrophic scenario and has no defined unit.

A minimally sufficient record includes stable ID; bounded hazard statement and scenarios; lifecycle mode/configuration/exposure; causes and consequences; initial severity, likelihood, risk, definitions, evidence, and uncertainty; each proposed/implemented control with precedence, owner, requirement/allocation, dependencies, verification result, and effectivity; current/residual assessment; open actions; introduced/transferred/aggregate links; status/history; and acceptance authority/date/scope/restrictions/reopen criteria. A matrix can consistently map declared ordered judgments to governance categories and decision levels. It cannot prove completeness, calculate expected loss, establish equal distance between categories, average risks, or prove the system safe.

### Answer 3

Operation scenario: while cleaning at pressure, hose degradation, incompatible chemical/material, connection error, overpressure, or external damage causes rupture; a worker in the jet/release zone is struck, injected, burned, or exposed. Maintenance scenario: after pump shutdown, the accumulator or trapped hose volume remains pressurized; opening a fitting releases energy toward the maintainer.

Prevention includes limiting pump pressure/energy, compatible rated hose and keyed fittings, safe routing/guarding, accumulator isolation and monitored bleed, and control logic that inhibits pressurization outside a valid configuration. Mitigation includes containment/shielding, relief to a safe location, emergency stop, detection, exclusion zones, PPE, and response. Dependency questions: Do pressure control and relief depend on the same sensor or blocked discharge path? Do emergency stop and isolation share power, software, or a valve? Can one maintenance/calibration error disable multiple controls? Also ask whether chemical attack is common to hose and seals and whether frozen/blocked venting defeats containment.

Component verification checks hose proof pressure/material compatibility, relief set point/capacity, valve leakage, sensor accuracy, stop response, and accumulator discharge. Integrated validation uses worst credible fluid, temperature, aging, maximum inventory, blocked outlet, sensor faults, power loss, software timing, incorrect mode, representative PPE/access, and controlled rupture/flow surrogates. It measures safe pressure before disassembly and verifies that procedures cannot outrun physical discharge. Tests support the sampled configurations; they do not establish every degradation or misuse path.

### Answer 4

Scenario: an attacker replays an authenticated but old dose-change message during a network interruption; the device reconnects in the wrong mode, displays a low-salience confirmation among multiple alarms, and an overloaded nurse confirms it believing it is current. The stale command plus mode ambiguity causes excessive delivery and patient harm. Safety assesses credible harm, system states, exposure, and control performance; security assesses adversary access, replay capability, credential compromise, and attack paths. Do not assign the attacker a random hardware rate.

Constraints require unique command identity, authenticated authority and anti-replay freshness; explicit patient/device/session binding; rejection of commands outside the current mode and physiological bounds; display of source, age, old/new value, consequence cue, and conflicts; a safe hold with local essential function when authority/data are invalid; rate/energy limits independent of the remote service; logged two-person or higher-authority confirmation for exceptional irreversible actions where operationally feasible; and recoverable rollback with state reconciliation.

Tests include expired, duplicated, reordered, delayed, conflicting, partially authenticated, wrong-patient, wrong-mode, privilege-escalated, and rollback commands; clock skew and restart; loss of network/identity service; saturated alarm/display workload; ambiguous state; nurse handover; and recovery after partial execution. Red-team evidence covers feasible attack paths; human-in-the-loop simulations cover interpretation and workload; integrated safety tests cover bounded delivery. No one test set proves absence of unknown attacks or interaction hazards.

### Answer 5

Start with a change-impact map from release/waiver to alarms, maintenance mode, failover timing, staffing assumptions, shared controls, derived requirements, verification artifacts, procedures, training, and every linked hazard. Reconstruct scenarios in which alarm reprioritization delays detection, maintenance mode disables protections, failover changes command/state ordering, or reduced staffing increases exposure and response time. Identify coupled hazards that demand the same people, display, network, sensor, or fallback simultaneously. Review whether risk moved to operators, maintainers, another service, or the public.

For each credited control, decide whether old evidence remains applicable to the exact software, configuration, environment, and staffing. Re-run timing, mode-transition, alarm-workload, failure/recovery, cybersecurity, and representative operational validation where assumptions changed. Preserve prior initial/current/residual assessments and record the proposed new state with uncertainty. Treat the waiver as a temporary control package with scope, compensating measures, monitoring, stop criteria, owner, expiry, and removal plan—not as silent normalization.

The decision package should contain: change/configuration identity; affected hazards and newly identified scenarios; control/evidence impact; individual and aggregate residual-risk ranges; common-cause and transferred-risk review; unresolved actions and dissent; proposed restrictions/monitoring; acceptance thresholds and the specific authorized roles; release, hold, or limited-operation alternatives; and automatic reopen triggers such as alarm misses, failover anomalies, staffing below minimum, control demand, near miss, configuration drift, or waiver expiry. The analyst recommends; the authorized decision maker accepts or rejects the bounded risk.
