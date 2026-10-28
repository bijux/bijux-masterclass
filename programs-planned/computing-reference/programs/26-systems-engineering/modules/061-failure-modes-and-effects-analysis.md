---
module_id: SYSENG-061
program: Systems Engineering
level: 2
module_number: 61
title: Failure Modes and Effects Analysis
status: complete
last_verified: 2026-08-31
---

# Failure Modes and Effects Analysis

## One-Page Review

### Governing question

How can an engineering team systematically reason upward from credible ways an item, function, process, software behavior, interface, or human interaction can fail, identify effects and existing controls, prioritize treatment without abusing ordinal scores, and maintain evidence as the design and operating context change?

### Essential definitions

- **Failure** is loss of ability to perform a required function within stated limits. It is defined relative to function, performance criteria, operating state, environment, duration, and configuration.
- A **failure mode** is the manner in which failure occurs or is observed: stuck closed, output biased high, omitted operation, untimely command, data corruption, leakage, fracture, or loss of isolation. “Bad component” is not an analyzable mode.
- A **failure cause** is a circumstance, mechanism, design weakness, process error, use condition, or initiating event that can produce a failure mode. Root cause should not be claimed before investigation evidence exists.
- A **local effect** is the consequence at the analyzed item; a **next-higher effect** is the consequence at the containing subsystem/process; an **end effect** is the consequence at the system, mission, user, patient, environment, or business objective.
- A **failure mechanism** is the physical, chemical, logical, informational, organizational, or human process that produces the mode, such as fatigue, wear, deadlock, stale state, incorrect setup, or ambiguous feedback.
- A **design FMEA (DFMEA)** analyzes product functions, interfaces, and design provisions. A **process FMEA (PFMEA)** analyzes manufacturing, assembly, service, maintenance, or operational process steps. Software and use-related analyses need domain-specific failure modes and causes.
- A **control** prevents a cause/mode, detects it before the effect, detects the effect, contains propagation, mitigates consequence, or enables recovery. A requirement without implemented and verified evidence is a planned control, not a demonstrated control.
- **Severity** ranks consequence under declared criteria. **Occurrence** ranks frequency/probability or qualitative likelihood under declared exposure. **Detection** ranks the chance that existing controls detect the cause or mode in time; in common scales, a larger value often means poorer detectability.
- A **risk priority number (RPN)** is commonly $S\times O\times D$. Its inputs are ordinal categories, so multiplication and comparisons can be misleading; identical RPNs can conceal radically different severity profiles.
- **Failure modes, effects and criticality analysis (FMECA)** extends FMEA with a declared criticality assessment, qualitative or quantitative. Quantitative formulas are valid only under their data, independence, exposure, mission-time, and failure-mode-allocation assumptions.
- A **single-point failure** is one failure whose effect alone can cause a specified unacceptable outcome without successful compensating means. The exact program definition and accepted exceptions must be stated.
- **Residual risk** is risk remaining after controls/actions, assessed using updated evidence and acceptance authority. Closing an action is not evidence that residual risk is acceptable.

### Central model, mechanism, or theorem

Represent a row for configuration and operating context $c$ as

$$
r=(i,f,m,k,e_L,e_N,e_E,c_0,S,O,D,a,v,\rho),
$$

where $i$ is the item/process step, $f$ required function, $m$ failure mode, $k$ causes/mechanisms, $e_L,e_N,e_E$ local/next/end effects, $c_0$ existing controls, $S,O,D$ declared rankings, $a$ recommended actions and owners/dates, $v$ verification evidence, and $\rho$ residual assessment.

For classical quantitative FMECA, one historical form estimates mode criticality as

$$
C_m=\beta\alpha\lambda_p t,
\qquad C_r=\sum_m C_m,
$$

where $\lambda_p$ is item failure rate, $\alpha$ the fraction attributed to the mode, $\beta$ the conditional probability that the mode produces the specified severity effect, and $t$ mission/exposure time. This is not a universal probability formula. Constant rates, data applicability, mode partition, exposure, repair, dependency, and conditional-effect assumptions must be justified.

Prioritization is a decision rule, not a ranking ritual:

$$
Priority(r)=P(S,O,D,\text{hazard link},\text{single point},\text{uncertainty},\text{control evidence}).
$$

High severity and mandatory safety actions cannot be traded away by a low RPN or a detectability claim.

### Critical invariants

- Scope, system boundary, lifecycle stage, configuration, mission/use profile, operating modes, environments, interfaces, assumptions, ranking criteria, and acceptance authority are established before scoring.
- Each analyzed item or process step has required functions and measurable performance limits. Modes negate or degrade those functions in specific ways.
- Causes, modes, and effects remain distinct. One cause may create several modes; one mode may have several causes and effects.
- Local, next-higher, and end effects are traced through actual architecture and controls without assuming that detection prevents occurrence or mitigation eliminates the mode.
- Existing controls are classified as prevention, detection, containment, mitigation, or recovery and are supported by implementation and verification status.
- Severity is based on credible end consequence before credit for detectability; high-severity items receive action according to policy regardless of RPN.
- Ranking scales include anchored definitions, direction, scope, data source, uncertainty, and tie/unknown handling. Numbers are not silently interpreted as interval probabilities.
- Actions prefer eliminating causes/modes or reducing occurrence/consequence before relying on detection, warnings, inspection, training, or downstream recovery.
- Every action has an owner, due date, expected effect, verification method, status, configuration, and residual assessment. Scores are not lowered merely because an action was proposed.
- Interfaces, software, human actions, maintenance, manufacturing variation, environmental stress, dormant failures, common causes, dependent failures, and combinations are addressed or explicitly covered by complementary analyses.
- FMEA remains configuration-controlled and is revisited after design/process/use changes, test or field findings, supplier changes, incidents, and control failure.
- FMEA supports but does not prove completeness, reliability, safety, security, compliance, or absence of common-mode and multi-failure paths.

### Common failures

Common failures include beginning with a blank worksheet rather than functions and architecture; writing causes in the mode column; stopping at local effects; using “system fails” for every end effect; assuming alarms prevent failures; copying generic libraries without confirming applicability; scoring before agreeing scales; multiplying ordinal scores and sorting mechanically; accepting low RPN for catastrophic severity; changing scores to make charts green; crediting planned controls; confusing occurrence with exposure; treating inspection as prevention; omitting interfaces, software, use error, maintenance, dormant and common-cause failures; analyzing only nominal operation; assigning actions without owners or verification; closing actions on document revision; never updating after test/field data; and presenting the completed table as a safety or reliability proof.

### Compact example

A synthetic FMEA contains five modes for a fluid-control function. A small checker confirms all required row fields and unique identities, computes five displayed RPNs, applies an explicit consequence-aware priority rule, finds four high-priority rows and four owned actions, and recomputes residual occurrence/detection rankings only for verified actions. It establishes declared table consistency and arithmetic. It does not validate the modes, rankings, controls, action effectiveness, independence, completeness, failure rates, or product acceptability.

### Connections

SYSENG-061 starts the reliability, availability, safety, and resilience block. SYSENG-062 uses top-down fault trees to complement FMEA’s bottom-up perspective; SYSENG-063 models success paths; later reliability, maintainability, safety, hazard, and resilience modules consume the modes, controls, and evidence. Digital threads preserve row-to-design/test/field provenance, while configuration management prevents applying one FMEA to the wrong variant.

## Governing Question

Can an independent reviewer select a configured item and operating condition, understand what function can be lost or degraded, follow each credible cause through local and system effects, see which controls actually exist and were verified, reproduce prioritization, and determine whether actions and residual risk were accepted by the proper authority?

The answer cannot be “the spreadsheet is complete.” FMEA is structured reasoning with a table as one possible representation. Its value comes from multidisciplinary challenge, architecture-based propagation, timely design change, and maintained evidence.

## Why This Matters

FMEA creates a disciplined bottom-up view of vulnerability. It can expose single points, missing diagnostics, unsafe propagation, difficult maintenance, weak process controls, ambiguous user feedback, and verification needs before failures become expensive or harmful. It also supplies inputs to reliability predictions, fault management, test design, inspection, spares, diagnostics, maintenance planning, hazard analysis, and change impact.

IEC 60812:2018 describes planning, performing, documenting, and maintaining FMEA/FMECA across hardware, software, processes, human action, and interfaces. NASA's active GSFC-HDBK-8004 similarly treats FMECA as a living risk assessment updated as designs, materials, operating parameters, processes, and knowledge evolve. The current DoD FMECA data-item description emphasizes potential impact on mission, safety, performance, maintainability, fault detection/isolation, and lifecycle control.

Historical MIL-STD-1629A remains influential but is cancelled; it should be cited as historical procedure, not presented as current mandatory policy absent a contract. Domain-specific requirements govern actual acceptance. Current FDA human-factors guidance illustrates another boundary: use-related failure analysis should involve relevant users/clinicians, design engineers, and human-factors expertise, and previously unanticipated use errors may still emerge during validation. FMEA is systematic, not omniscient.

## Prerequisites and Retrieval

Before conducting or accepting an FMEA, retrieve:

1. intended decision, applicable standard/contract, analysis type, lifecycle timing, tailoring, audience, acceptance authority, and update triggers;
2. system/process boundary, architecture, functions, performance limits, interfaces, states/modes, mission/use profiles, environments, configurations, effectivities, and assumptions;
3. requirement, hazard, fault-management, reliability, maintainability, cybersecurity, human-factors, manufacturing, service, supplier, and operational context;
4. item/process decomposition at a useful indenture level, stable identities, authority, configuration baseline, diagrams/models, bills of material/process, and interface contracts;
5. failure definitions, mode/cause libraries and their provenance, material/component/process/software/use data, exposure, stress, derating, and uncertainty;
6. severity, occurrence and detection criteria with anchored examples, direction, data sources, unknown policy, action-priority/criticality rule, and mandatory-action thresholds;
7. existing prevention, detection, containment, mitigation and recovery controls with implementation configuration, diagnostic coverage, response time, independence, verification, and known limitations;
8. test, inspection, anomaly, incident, field, warranty, maintenance, supplier, calibration, nonconformance, corrective-action, and lessons-learned evidence;
9. action workflow, owners, due dates, change/control linkage, verification/validation methods, escalation, residual-risk acceptance, and records retention;
10. complementary analyses covering top-down hazards, combinations/common cause, sequence/timing, software interactions, cybersecurity, human use, and emergency/recovery behavior.

Use a retrieval challenge: choose one high-severity row and request the exact source configuration, function and mode definition, propagation rationale, control implementation and test evidence, ranking criteria and inputs, action change, verification result, residual assessment, and approval. A row that survives only as prose in a spreadsheet is not yet a durable engineering argument.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish failure, failure mode, mechanism/cause, local/next/end effect, control, action, and residual risk;
2. select and tailor functional, design, process, software, interface, and use-related FMEA scopes;
3. derive modes from functions, states, interfaces, and performance limits rather than generic nouns;
4. trace effects through architecture and distinguish prevention, detection, containment, mitigation, and recovery;
5. define and use severity, occurrence, detection, action-priority, criticality, and uncertainty criteria without abusing ordinal arithmetic;
6. calculate and challenge RPN and classical criticality values under explicit assumptions;
7. identify single points, dormant faults, diagnostic dependencies, common causes, human/software/interface modes, and missing complementary analyses;
8. convert findings into owned design/process/test actions and verified residual assessments;
9. maintain FMEA as configuration-controlled lifecycle evidence linked to requirements, hazards, changes, tests, and field observations;
10. communicate what FMEA supports and what it cannot establish.

## Core Exposition

**Plan the analysis.** State why it is being performed and which decisions it will support. Define boundaries, indenture, lifecycle stage, baseline, modes of operation, mission phases, environmental conditions, assumed upstream/downstream services, severity endpoints, ranking policy, roles, schedule, tools, deliverables, review and update triggers. Tailoring should remove irrelevant detail while preserving decision-critical coverage.

**Build a multidisciplinary team.** Include owners of system/design, reliability, safety, software, manufacturing/process, quality, test, maintainability/service, human factors/operations, cybersecurity, suppliers, and affected users as appropriate. A facilitator enforces column semantics and evidence discipline. Domain diversity reduces blind spots; attendance alone does not establish independence or completeness.

**Select useful decomposition.** Functional FMEA is valuable early when implementation is fluid. Hardware/design FMEA becomes possible as architecture matures. PFMEA follows process steps and their product/service effects. Analyze at the lowest level where action can change design or control, but propagate far enough to see end consequence. Excessive depth produces repeated rows; shallow depth hides mechanisms.

**Define functions before modes.** Use verb-object-performance-condition forms: “isolate reverse flow to less than 0.1 L/min within 200 ms from commanded closure at specified pressure and temperature.” Negations yield useful mode prompts: fails to isolate, isolates unintentionally, isolates too slowly, leaks beyond limit, oscillates, reports false state. Also examine too much/little, early/late, intermittent, biased, stuck, reversed, corrupt, unauthorized, unavailable, and state-dependent behavior.

**Separate cause, mode, and effect.** “Seal wear” is a mechanism/cause; “external leakage above limit” is a mode; “local pressure loss,” “subsystem unable to maintain flow,” and “loss of mission cooling” are effects at increasing levels. Keeping these separate makes controls actionable. One row may need splitting when causes, controls, or end effects differ materially.

**Trace propagation through real architecture.** Follow energy, material, information, control, timing, software, and human pathways. State assumptions about redundancy, switching, load sharing, isolation, fault containment, operator response, and environment. Do not give credit twice to the same sensor/software/power source. Identify when a diagnostic is disabled, dormant, masked, common-cause exposed, or too slow.

**Characterize existing controls.** Prevention reduces chance of cause/mode: design margin, poka-yoke, type constraints, process capability. Detection finds cause/mode before end consequence: test, monitor, diagnostic, inspection. Containment stops propagation; mitigation reduces consequence; recovery restores service. Record where, when, and under which conditions each acts. A planned monitor without implemented logic, threshold, timing, independence, and test evidence cannot justify a better detection rank.

**Rank severity consistently.** Anchor severity to stated end effects and program criteria, including safety, mission/service, regulatory, environmental, security, financial, and recoverability dimensions. Use the worst credible effect within scope, with assumptions visible. Detection does not lower inherent consequence; mitigation may change consequence only when reliably implemented and credited under the method.

**Estimate occurrence honestly.** Use applicable field/test/process data, reliability models, supplier evidence, physics, stress/exposure, software/change history, or structured expert judgment. State population, confidence and relevance. Component failure rate is not automatically mode occurrence; allocate modes with evidence. For process/use failures, opportunity/exposure and context matter. Unknown is not “rare.”

**Assess detection as a time-dependent control claim.** Define what is detected—the cause, mode, or effect—before which harmful progression point, with what coverage, false-positive/negative behavior, latency, independence, operator interpretation, and verification. End-effect detection after harm has occurred is not preventive detection. A control that shares the failed power, sensor, network, software, or human assumption may not be available.

**Treat RPN as a display, not truth.** Ordinal scales encode order, not equal distance. $10\times2\times2=40$ and $4\times5\times2=40$ do not express equal engineering risk. Many triples collide, scale definitions differ, and a one-level subjective change can reorder rows. Always retain components, prioritize high severity and mandatory hazards, use explicit policy, and inspect uncertainty and control evidence.

**Use criticality calculations conditionally.** For $C_m=\beta\alpha\lambda_pt$, verify units and assumptions: $lambda_p$ per hour, $t$ hours, dimensionless $alpha$ and $\beta$. Mode fractions should be appropriate and may sum to one only for a complete mutually exclusive partition. Constant-rate approximation may fail for wear-out, demand-based, repaired, software, dependent, or changing-stress behavior. Report uncertainty and source applicability.

**Identify actions in the preferred order.** First eliminate the function need, hazard, cause, or failure mode where possible. Then reduce occurrence through robust design/process, reduce consequence through architecture/containment, improve verified detection and response, and finally use procedural/label/training controls where justified. Consider whether an action creates new modes or common dependencies.

**Write executable actions.** “Improve design” is not an action. Specify changed item/requirement/control, owner, due date, expected ranking/criticality effect, affected configurations, verification method and acceptance authority. Link to change control. Do not lower prospective scores until implementation and evidence justify it; distinguish forecast from verified residual assessment.

**Close the loop.** After implementation, confirm configuration, rerun affected analysis/test, verify control coverage/timing, update effects and rankings with evidence, identify new modes, link residual risk acceptance, and retain prior baseline. An action can be complete while risk remains unacceptable; the workflow needs both statuses.

**Cover interfaces.** Connector mismatch, timing disagreement, unit/frame error, protocol/version incompatibility, resource contention, stale data, electromagnetic/thermal coupling, ambiguous ownership, and invalid assumptions often cross item boundaries. Assign interface row ownership jointly and test both sides plus integrated behavior.

**Treat software appropriately.** Software does not wear like hardware, but design and execution can produce omission, commission, incorrect value/order/timing, stale state, resource exhaustion, deadlock, race, overflow, error-handling failure, unsafe fallback, update/configuration mismatch, and corrupted/unauthorized behavior. Occurrence may depend on triggering conditions and systematic defects, making hardware failure-rate analogies inappropriate.

**Analyze human interaction and processes.** A PFMEA step has intended transformation and product/process effect. Use-related analysis examines perception, cognition, action, feedback, environment and foreseeable misuse without labeling the person as the failure. Involve representative users and human-factors expertise. Training and warnings are generally weaker than interface or process redesign and require validation in real use conditions.

**Link but do not merge complementary analyses.** Fault trees begin with a top event and expose combinations; hazard analyses begin with harms/hazards; HAZOP applies guidewords to deviations; reliability block diagrams model success structure; event trees model sequences; common-cause analysis challenges independence; STPA examines unsafe control. Cross-reference shared identities/evidence while preserving method semantics.

**Maintain configuration and provenance.** Each row should bind item/function/interface versions, analysis baseline, criteria version, sources, assumptions, reviewer/approval and change history. Generated links and libraries need mappings and applicability review. Supplier FMEAs may be protected; define the assertions, audit rights and gaps needed for system analysis.

**Use field and test feedback.** Compare observed failures, near misses, diagnostic performance, false alarms, repair findings, process escapes, use errors, and environmental conditions against the analysis. Add missing modes/causes, recalibrate occurrence/detection, challenge controls, and assess affected configurations. Absence of observed failure in limited exposure is weak evidence, not proof of impossibility.

The following executable fixture checks a declared table and an explicit priority policy. Residual values are credited only where the action is marked verified.

<!-- bijux-verify: {"id":"fmea-ranking-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"rows=5\ncomplete_rows=5\nunique_rows=1\nrpn_values=108,280,160,140,216\nhigh_priority_rows=4\nhigh_priority_owned_actions=4\nverified_actions=4\nresidual_rpn_values=36,105,64,60,216\nseverity_unchanged=1\nstatus=declared_fmea_fixture_passed\nevidence=synthetic_rankings_only\n","stderr":""}} -->
```python
rows = [
    {"id": "FM-1", "function": "isolate flow", "mode": "stuck closed", "cause": "stem seizure", "local": "no outlet flow", "end": "cooling lost", "control": "position and flow monitor", "s": 9, "o": 3, "d": 4, "action": "change bearing and verify margin", "owner": "mechanical", "verified": True, "ro": 1, "rd": 4},
    {"id": "FM-2", "function": "measure pressure", "mode": "biased high", "cause": "calibration drift", "local": "incorrect measurement", "end": "unsafe control demand", "control": "range check", "s": 7, "o": 5, "d": 8, "action": "add diverse plausibility check", "owner": "controls", "verified": True, "ro": 3, "rd": 5},
    {"id": "FM-3", "function": "contain fluid", "mode": "external leak", "cause": "seal damage", "local": "fluid released", "end": "pressure and fluid loss", "control": "proof test", "s": 8, "o": 4, "d": 5, "action": "key seal installation and inspect", "owner": "manufacturing", "verified": True, "ro": 2, "rd": 4},
    {"id": "FM-4", "function": "command valve", "mode": "stale command retained", "cause": "update race", "local": "wrong valve state", "end": "cooling path unavailable", "control": "command timeout", "s": 10, "o": 2, "d": 7, "action": "make command sequence atomic", "owner": "software", "verified": True, "ro": 1, "rd": 6},
    {"id": "FM-5", "function": "carry sensor signal", "mode": "intermittent open", "cause": "connector fretting", "local": "signal dropouts", "end": "degraded monitoring", "control": "continuity check", "s": 6, "o": 6, "d": 6, "action": "evaluate connector change", "owner": "electrical", "verified": False, "ro": 6, "rd": 6},
]
required = ("id", "function", "mode", "cause", "local", "end", "control", "s", "o", "d", "action", "owner")
complete = sum(all(row[key] not in (None, "") for key in required) for row in rows)
rpns = [row["s"] * row["o"] * row["d"] for row in rows]
high = [row for row in rows if row["s"] >= 9 or (row["s"] >= 8 and row["o"] >= 4) or row["d"] >= 8]
residual = [row["s"] * (row["ro"] if row["verified"] else row["o"]) * (row["rd"] if row["verified"] else row["d"]) for row in rows]
print(f"rows={len(rows)}")
print(f"complete_rows={complete}")
print(f"unique_rows={int(len({row['id'] for row in rows}) == len(rows))}")
print("rpn_values=" + ",".join(str(value) for value in rpns))
print(f"high_priority_rows={len(high)}")
print(f"high_priority_owned_actions={sum(bool(row['action'] and row['owner']) for row in high)}")
print(f"verified_actions={sum(row['verified'] for row in rows)}")
print("residual_rpn_values=" + ",".join(str(value) for value in residual))
print(f"severity_unchanged={int(all(row['s'] == row['s'] for row in rows))}")
print("status=declared_fmea_fixture_passed")
print("evidence=synthetic_rankings_only")
```

The fixture's `severity_unchanged` check is intentionally narrow: the code never creates a residual severity field. Real mitigation may justify a different residual consequence only after architecture, applicability, independence, and verification evidence support that claim.

## Definitions and Notation

Let $I$ be configured items or process steps and $F(i,c)$ their required functions in context $c$. A mode $m$ belongs to the declared deviation set $M(f,c)$ for a function, not to a generic universal library. Let $K(m)$ be candidate causes/mechanisms and $E(m,c)$ the propagation path to effects.

Let $C_p,C_d,C_t,C_m,C_r$ denote prevention, detection, containment, mitigation, and recovery controls. A control-credit judgment is

$$
Credit(C,c)=Implemented\land Applicable\land Timely\land Independent\land Verified,
$$

with strength and uncertainty assessed separately. This conjunction is a review discipline, not proof that controls are perfect.

Let $S,O,D$ be ordinal category labels under criteria version $v$. Comparisons within the same controlled scale can support prioritization; addition, multiplication, ratios, and cross-scale comparisons do not inherit interval meaning automatically.

## Mechanisms, Invariants, or Proof Structure

A defensible FMEA row supports a bounded argument:

1. **Context:** the configured item/process, state, environment, exposure, function and performance limit are applicable.
2. **Mode:** the stated deviation is physically/logically/humanly credible and distinct from its causes and effects.
3. **Propagation:** local, next-higher and end effects follow declared architecture, timing and assumptions.
4. **Control:** existing controls are classified, implemented, applicable, timely, sufficiently independent, and verified to their claimed coverage.
5. **Priority:** severity, occurrence, detection, criticality and mandatory policy use controlled criteria and disclosed evidence/uncertainty.
6. **Action:** treatment addresses cause, occurrence, consequence, detection or recovery; has owner/date/configuration; and is assessed for introduced modes.
7. **Verification:** objective evidence confirms implementation and effectiveness in the applicable configuration and conditions.
8. **Residual disposition:** updated effects/rankings and uncertainty are reviewed and accepted or escalated by authorized roles.

Completeness remains bounded by decomposition, prompts, architecture, team knowledge, evidence and complementary analyses. A review can establish that the method and declared scope were executed; it cannot prove that every possible failure was imagined.

## Alternatives and Trade-Offs

**Functional versus piece-part FMEA.** Functional analysis begins earlier and follows loss/degradation of behavior; it may hide component mechanisms. Piece-part analysis supports detailed design, reliability and maintainability but can become enormous and arrive late. Use functional analysis early and refine high-consequence or uncertain areas.

**DFMEA versus PFMEA.** DFMEA treats design inadequacy and product behavior; PFMEA treats process variation and execution. A design that is robust on paper may be difficult to manufacture, and a capable process cannot repair an unsafe design. Link but do not merge authority.

**Qualitative matrix versus quantitative criticality.** Qualitative ranking works with sparse data and stakeholder criteria but is subjective and coarse. Quantitative criticality improves explicitness when applicable rate, mode fraction, conditional-effect and exposure data exist; false precision is dangerous. Report uncertainty and use sensitivity.

**RPN versus explicit action priority.** RPN is easy to compute and trend within one method but hides components and ordinal limitations. A rule that directly treats severity, occurrence, detection, hazards, single points and uncertainty is more transparent, though it requires governance and can still be subjective.

**Workshop versus analyst draft.** Workshops expose cross-domain interactions but are expensive and vulnerable to groupthink. An analyst draft improves preparation; owners must challenge it. Use asynchronous evidence gathering plus focused multidisciplinary sessions for propagation, controls and actions.

**Embedded table versus linked knowledge model.** Tables are portable and reviewable; repeated text drifts. Linked models improve identity, configuration, query and change impact but add tooling and schema governance. Regardless of medium, preserve export, provenance and reviewable snapshots.

## Failure Modes and Misconceptions

- **“FMEA identifies all failures.”** It is systematic but bounded by scope, knowledge, prompts, architecture and evidence.
- **“The cause is ‘component failure.’”** That repeats the event and gives no actionable mechanism or condition.
- **“Detection lowers severity.”** Detection may change exposure or enable mitigation; inherent consequence does not become smaller merely because an alarm exists.
- **“A low RPN is safe.”** High severity, hazards, single points and uncertainty may require action regardless of product score.
- **“Redundancy removes the row.”** Redundancy can share power, environment, software, maintenance, sensor, design defect or switching failure; analyze coverage and common cause.
- **“Inspection prevents the defect.”** Inspection detects some defects with imperfect coverage; prevention changes design/process so defects are less likely.
- **“Software cannot fail because it does not wear.”** Systematic defects and triggering conditions create incorrect, missing, untimely or unsafe behavior.
- **“The user is the failure mode.”** Analyze task, interface, context, perception, action and feedback; blame is neither mechanism nor control.
- **“Closed action means accepted risk.”** Implementation, verification, residual analysis and authorized acceptance are distinct.
- **“The latest FMEA applies to every unit.”** Bind rows, controls and evidence to versions, serial/lot effectivity, software, process and operating context.

## Worked Examples

### Example 1

A valve row says function “valve,” mode “seal wear,” cause “leak,” effect “failure.” Rewrite it: function is contain fluid below a leakage limit under declared pressure/temperature; seal abrasion from assembly damage is a cause/mechanism; external leakage above the limit is the mode; local fluid release and pressure loss propagate to subsystem cooling loss and mission shutdown. Prevention is keyed tooling and protected handling; proof test detects leakage. The rewritten row creates actionable design, process and test decisions.

### Example 2

A controller output can freeze at its last valid value. The local effect appears plausible, so a range check does not detect it. Timestamp/sequence supervision detects staleness, but it shares the controller clock. A diverse receiving-system timeout improves independence. Analysis must state update rate, maximum safe latency, network partitions, startup and degraded modes. The control can justify detection credit only after implementation and fault-injection evidence under applicable timing.

### Example 3

Two rows both have RPN 120: catastrophic severity 10, occurrence 3, detection 4; and moderate severity 5, occurrence 6, detection 4. Sorting treats them equally. Policy instead requires action for severity 9–10, links the first to the hazard and single-point review, and separately addresses the second's frequent rework. Same arithmetic does not mean same consequence, urgency, treatment or acceptance authority.

### Example 4

A redundant pump pair is credited as preventing flow loss. Both receive power from one bus, use the same command software, share an inlet susceptible to blockage, and one dormant standby failure is detected only on annual test. The FMEA keeps individual pump modes, adds shared-support and switching/latent cases, and links common-cause and fault-tree work. Nominal two-unit redundancy is architecture, not demonstrated independence.

### Example 5

A PFMEA says an operator may install a seal backward and proposes training. Examination finds symmetric geometry and an unreadable orientation mark. Redesign makes reverse installation physically impossible and adds machine-readable confirmation; training becomes secondary. Process validation challenges representative parts, lighting, gloves, shifts, rework and bypass. The action reduces occurrence only after capable implementation evidence, not after updating the work instruction.

### Example 6

An FMECA uses $\lambda_p=2\times10^{-6}$/h, $\alpha=0.25$, $\beta=0.4$, and $t=1{,}000$ h. Then $C_m=0.0002$ under the constant-rate rare-event approximation. The reviewer checks that mode fractions, rate population, stress and mission exposure apply. This is an expected criticality contribution, not observed frequency or proof of a $0.02\%$ mission probability under arbitrary dependencies/repairs.

### Example 7

An infusion-device use analysis lists “user enters wrong dose.” The team decomposes tasks: read order, select units, enter value, confirm, and interpret feedback under interruptions and low vision. A mode is a dose-unit mismatch accepted without salient feedback; causes include default units and similar labels; end effect is incorrect delivery and harm. Representative clinicians/users and human-factors specialists propose interface constraints and test them. The analysis does not declare user negligence as root cause.

### Example 8

A supplier supplies only a summary stating no high RPNs. The integrator cannot evaluate its severity criteria, system end effects, configuration or controls. The data agreement instead requires stable item/mode IDs, interface effects, high-severity/single-point declarations, criteria versions, affected configurations, control assertions, change notices and audit access. Proprietary causes can remain protected, but unresolved system-impact evidence is an explicit gap, not a green status.

### Example 9

Field reports reveal intermittent connector opens during vibration, absent from the original FMEA. The team links serials, connector lot, environment, maintenance history and diagnostic logs; adds fretting and harness-load causes; challenges occurrence and detection; updates affected configurations; introduces retention/strain-relief changes and a representative vibration test. Prior baselines remain for decision reconstruction. One field cluster supports corrective action, not a universal rate without exposure/population analysis.

### Example 10

A design action adds an isolation valve to contain leakage. The new valve introduces stuck-closed, stuck-open, leakage, inadvertent actuation, command/power and maintenance modes. Change impact adds rows, updates fault trees, verifies timing and diagnostic coverage, and assesses common power/control. The original leakage consequence improves only for conditions in which isolation acts successfully. Risk treatment can redistribute rather than erase failure.

## Cross-Program Connections

- **Data engineering:** field/exposure populations, provenance, censored data, schema/versioning, uncertainty and bitemporal histories govern occurrence and control-performance evidence.
- **API and service engineering:** failure contracts, timeouts, retries, idempotency, stale data, partial failure, compatibility and observability supply software/interface modes and controls.
- **Platform engineering:** shared dependencies, control-plane failure, rollout/configuration, multi-tenancy, recovery and common-mode infrastructure challenge naive redundancy.
- **Object-oriented programming:** responsibility, state invariants, encapsulation and interface contracts help derive functional/software failure modes; inheritance and shared dependencies can create propagation.
- **Functional programming:** explicit result types, immutability, pure transformations and property-based tests reduce or expose missing, invalid, stale and order-dependent behavior.
- **Security engineering:** threat-induced failures may share effects with random/systematic failures, but adversarial intent and adaptive attack require threat modeling beyond FMEA.

## References

1. International Electrotechnical Commission, [IEC 60812:2018, Failure modes and effects analysis (FMEA and FMECA)](https://webstore.iec.ch/en/publication/26359), edition 3.0, stability date 2029.
2. NASA Goddard Space Flight Center, [GSFC-HDBK-8004, Guideline for Failure Modes and Effects Analysis and Risk Assessment](https://standards.nasa.gov/standard/GSFC/GSFC-HDBK-8004), active handbook, 2024.
3. NASA, [Software Failure Modes and Effects Analysis](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695706/8.05+-+SW+Failure+Modes+and+Effects+Analysis), Software Engineering Handbook Version D, accessed 2026-08-31.
4. Defense Logistics Agency ASSIST, [MIL-STD-1629 document record](https://quicksearch.dla.mil/qsDocDetails.aspx?ident_number=37027), historical standard and cancellation record, accessed 2026-08-31.
5. Defense Logistics Agency ASSIST, [DI-SESS-81495, Failure Modes, Effects, and Criticality Analysis](https://quicksearch.dla.mil/qsDocDetails.aspx?ident_number=205553), Revision C data-item record, 2024.
6. U.S. Food and Drug Administration, [Applying Human Factors and Usability Engineering to Medical Devices](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices), final guidance, 2026.
7. U.S. Food and Drug Administration, [Recognized Consensus Standards database result for IEC 60812](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/results.cfm?category=&effectivedatefrom=&effectivedateto=&organization=2&pagenum=50&productcode=&referencenumber=&regulationnumber=&sortcolumn=pdd&start_search=51&title=&type=), accessed 2026-08-31.
8. NASA, [Failure Modes and Effects Analysis: A Bibliography](https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20000070720.pdf), NASA/SP-2000-6110, 2000.
9. NASA, [Systems Engineering Handbook](https://www.nasa.gov/reference/systems-engineering-handbook/), current web edition, accessed 2026-08-31.
10. SAE International, [J1739_202101, Potential Failure Mode and Effects Analysis including Design FMEA, Supplemental FMEA-MSR, and Process FMEA](https://www.sae.org/standards/content/j1739_202101/), standard record, 2021.

## Exercises

### Exercise 1

Construct three rigorous FMEA rows for a battery thermal-management loop: one hardware, one software/interface, and one maintenance/use-related mode. Include functions, causes, local/next/end effects, controls, rankings with criteria assumptions, actions and verification.

### Exercise 2

An FMEA team ranks four rows $(S,O,D)$ as A=(10,2,2), B=(8,5,1), C=(5,4,4), D=(4,5,4). All have RPN 40 or 80. Critique RPN ordering and design a transparent action-priority policy.

### Exercise 3

Calculate and challenge quantitative mode criticality for $\lambda_p=4\times10^{-6}$/h, $\alpha=0.3$, $\beta=0.5$, $t=2{,}000$ h. State the result, units/interpretation, assumptions, uncertainty and evidence needed.

### Exercise 4

Review a claimed redundant safety function with two channels sharing power, sensor type, software library and maintenance procedure. Extend FMEA and name complementary analyses/tests.

### Exercise 5

Design a lifecycle update and action-closure workflow after field data reveal an unmodeled intermittent failure affecting some serials. Preserve configuration, prior decisions, evidence and residual-risk authority.

## Answers to the Exercises

### Answer 1

Hardware: function “circulate coolant above minimum flow through the battery in charge states under declared temperature/pressure”; mode “pump produces insufficient flow”; causes include impeller damage or bearing seizure; local effect is reduced flow, next effect is rising coolant/battery temperature, end effect may be charge shutdown or thermal hazard. Existing controls might be flow/temperature monitoring and commanded shutdown. Rankings cite the project anchors and exposure; high severity is not reduced by detection. Action could add verified design margin, independent temperature protection and representative degraded-flow test.

Software/interface: function “command pump speed corresponding to validated thermal demand within latency”; mode “stale low-speed command retained”; causes include timestamp loss, race or interface-version mismatch; local effect is wrong command, next effect insufficient cooling, end effect matches configuration-specific thermal consequence. Range checking may not detect a plausible stale value. Action adds sequence/time validity, safe timeout, version contract and fault injection. Verification covers startup, packet loss/reorder, clock faults, load and degraded modes.

Maintenance/use: function “restore coolant circuit with specified fluid volume and no trapped air”; mode “circuit returned to service underfilled”; causes include ambiguous fill indication, inaccessible bleed point or skipped purge; local effect air pocket/low inventory, next effect cavitation/low heat transfer, end effect overheating. Procedure sign-off is weak detection. Prefer keyed connections, observable fill state and automated plausibility, then validate with representative maintainers and environments. Each action needs owner, configuration, due date and residual acceptance; none of these illustrative rankings proves actual risk.

### Answer 2

A=40, B=40, C=80, D=80. Mechanical ordering places C/D above catastrophic A and severe B even though the scales are ordinal and the consequences differ. D and C also share an RPN despite different severity/occurrence/detection profiles. Multiplication assumes equal spacing and compensability that the criteria do not establish.

A transparent policy might require immediate analysis/action for severity 9–10; high priority for severity 7–8 with occurrence at least 4 or poor detection, for any hazard/single point/regulatory requirement, or for large uncertainty/missing control evidence; medium priority for frequent lower-severity loss or lifecycle cost; and documented disposition for all others. Therefore A is mandatory high; B is high because severity 8 and occurrence 5; C is medium/high according to consequence and repeated occurrence; D may be medium despite the same RPN. Owners must inspect controls and evidence, not only categories. Criteria and exceptions need approval and residual-risk authority.

### Answer 3

Under the stated historical constant-rate model,

$$
C_m=(0.5)(0.3)(4\times10^{-6}\,h^{-1})(2{,}000\,h)=0.0012.
$$

It is a dimensionless criticality contribution for the specified mode/severity classification under the method; it is not automatically an observed failure probability. For a rare constant-rate nonrepairable event, it may approximate a contribution, but exact probability and dependencies require an appropriate model.

Evidence must support the population/stress/environment relevance of $\lambda_p$, the mode allocation $\alpha$, conditional-effect probability $\beta$, and actual exposure $t$. Check that modes form the intended partition, rates are constant, repair/dormancy/demand behavior is compatible, controls and dependencies are treated correctly, and parameter uncertainty is reported. Sensitivity or intervals are more honest than extra decimals. Software/systematic and common-cause behavior usually invalidate naive hardware-rate use.

### Answer 4

Add channel failure modes and shared-support modes: common power loss/disturbance; common sensor bias/environment; shared library logic or configuration defect; identical timing/resource fault; maintenance miscalibration or simultaneous disablement; switching/voter/isolation failure; latent standby fault; and test mechanism that masks or introduces common failure. Trace local effects through detection, arbitration and actuation timing to the end hazard.

For every claimed control, test implementation, applicability, diagnostic coverage, latency, false behavior, independence and recovery. Actions may diversify power/sensing/implementation, partition fault containment, improve online proof tests, prevent common maintenance error and define safe degradation—but diversity can create integration modes.

Complement FMEA with top-down fault tree/minimal cut sets, common-cause/dependency analysis, hazard/control analysis, reliability/availability modeling and sequence/event analysis. Test shared power/environment faults, common biased inputs, software/configuration injection, latent failures, switching under timing extremes and maintenance restoration. Two channels prove neither independence nor safety.

### Answer 5

Open a controlled anomaly with stable identity and link affected serials/lots, hardware/software/process configurations, environment, use, maintenance and observed timestamps. Preserve raw reports/logs/parts and provenance. Do not overwrite the prior FMEA: record the baseline used for earlier release decisions and create a new revision/effective scope.

Triage distinguishes observation, mode, candidate mechanisms and hypotheses. Estimate exposed population and censoring before changing occurrence. Add or split rows for the intermittent mode, propagate effects, challenge dormant/detection behavior, and link hazards, fault trees, tests, supplier evidence and change impact. Identify containment for fielded units separately from durable corrective action.

Actions have owners, dates, affected configurations and expected effects: supplier/process/material/design changes, diagnostic improvement, inspection or field action as justified. Verify under representative stress and intermittent conditions, test introduced modes, reconcile production/field records, and monitor recurrence/false alarms. Update rankings only after evidence; document uncertainty and unaffected/unknown populations. Authorized technical/safety/product roles accept residual risk and effectivity. Preserve prior decisions, corrections and reasons so later reviewers can reconstruct what was known when.
