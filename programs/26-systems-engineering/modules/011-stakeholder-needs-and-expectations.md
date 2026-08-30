---
module_id: SYSENG-011
program: Systems Engineering
level: 1
module_number: 11
title: Stakeholder Needs and Expectations
status: complete
last_verified: 2026-08-30
---

# Stakeholder Needs and Expectations

## One-Page Review

### Governing question

How can a team discover, analyze, reconcile, validate, and preserve what diverse stakeholders need across the lifecycle without mistaking the loudest request, current workaround, or preferred design for the integrated basis of system validation?

### Essential definitions

- A **stakeholder** is a person, role, group, organization, or authority that has an interest, right, responsibility, influence, exposure, benefit, or potential harm related to the system or its lifecycle.
- A **customer/acquirer** obtains or funds the system; a **user** directly interacts with it; neither category includes every affected stakeholder.
- An **expectation** is a stakeholder's expressed or inferred need, desire, capability, concern, perceived constraint, or anticipated behavior before it is fully analyzed and integrated.
- A **stakeholder need** states an outcome, capability, quality, or condition needed in a defined context from a stakeholder perspective, without silently selecting realization.
- An **integrated set of needs** is the analyzed, consistent, feasible, traceable, lifecycle-aware basis agreed under named authority for requirements and system validation.
- **Elicitation** discovers information from people, observation, artifacts, operation, incidents, and context; it is not merely asking stakeholders to dictate requirements.
- **Need analysis** clarifies source, rationale, context, terminology, conflicts, assumptions, constraints, feasibility, measures, and lifecycle implications.
- **Need validation** checks with relevant stakeholders and evidence that the integrated needs accurately represent intended outcomes and context.
- A **derived need** follows from analysis of scenarios, risks, lifecycle concepts, law, ethics, interfaces, or enabling systems even when no stakeholder stated it verbatim.
- **Representation** is the justified way an individual or body speaks for a stakeholder class; attendance alone does not establish representativeness.
- **Priority** expresses relative decision importance under defined authority and method; it is not identical to urgency, influence, implementation order, or stakeholder power.

### Central model, mechanism, or theorem

Preserve three layers:

\[
RawInput \xrightarrow{analysis} CandidateNeed
\xrightarrow{integration/authority} BaselinedNeed
\xrightarrow{transformation} Requirements.
\]

Record a need as:

\[
n=\langle id,source,stakeholder,outcome,context,rationale,measure,
priority,assumptions,constraints,conflicts,trace,status,evidence\rangle.
\]

Trace transformation obligations:

\[
Need \Leftarrow Sources+Analysis,
\quad Requirements \Rightarrow NeedCoverage,
\quad ValidationEvidence \Rightarrow NeedSatisfaction.
\]

The arrows express required justification, not logical proof. A complete-looking register can still omit stakeholders, distort meaning, or validate against an unrepresentative context.

### Critical invariants

- Stakeholder discovery spans direct use, operation, support, acquisition, supply, governance, affected non-users, adversarial exposure, and retirement.
- Raw statements remain available after transformation so meaning and dissent are auditable.
- Each need states stakeholder outcome/capability, context, rationale, and source; solution language is justified only by a real constraint.
- One need does not conceal multiple independently tradeable outcomes.
- Silence, absence from telemetry, low institutional power, or inability to participate never proves absence of need.
- Conflicts are explicit, typed, and resolved or accepted by named authority; averaging does not erase rights or safety constraints.
- Prioritization considers consequence, value, obligation, urgency, dependency, uncertainty, and distribution—not influence alone.
- Derived needs trace to scenarios, hazards, lifecycle analysis, regulation, ethics, or system context.
- Requirements cover baselined needs bidirectionally, and validation returns to stakeholder outcomes.
- High-consequence needs require applicable independent domain and affected-stakeholder review.

### Common failures

Failures include equating sponsor with stakeholder population; interviewing only current users; asking people to write “shall” statements; copying feature requests as needs; treating workarounds as desired operation; omitting maintainers, trainers, responders, non-users, vulnerable groups, and retirement; converting low power into low priority; using votes to waive safety or rights; declaring consensus after suppressing dissent; mixing need, requirement, and design; leaving qualitative expectations unmeasurable forever; deriving needs without sources; tracing requirements only forward; and validating the built system against specifications rather than stakeholder outcomes.

### Compact example

A transit agency requests “a smartphone ticketing app.” Riders need reliable, understandable, affordable access to travel. Inspectors need quick, fair validation; finance needs accountable settlement; privacy and accessibility authorities constrain data and interaction; cash-dependent and unbanked riders must not lose access; operations and support need recovery during device, power, or network failure. The app is a candidate. The integrated needs describe access, validation, settlement, privacy, accessibility, degraded operation, support, and transition so multiple realizations can be compared and the eventual service validated.

### Connections

Retrieve stakeholders/value, uncertainty, assumptions, context/scenarios, and problem framing from Modules 003 and 007–010. Continue to operational concepts, functional and performance requirements, constraints, testability, decomposition, allocation, traceability, and change management. Later human factors, safety, security, validation, lifecycle, and systems-of-systems modules deepen stakeholder evidence and governance.

## Governing Question

Stakeholders rarely deliver a coherent specification. They describe pain, desired outcomes, current tools, policy, fears, exceptions, and imagined features using different language and power. Some cannot participate directly. Others experience only one lifecycle stage. A systems engineer must preserve their knowledge without treating every statement as equally authoritative, feasible, complete, or solution-neutral.

The governing question concerns transformation with accountability. How does a team move from partial and conflicting evidence to an integrated need set while preserving source meaning, affected populations, uncertainty, and dissent? The answer shapes the entire lifecycle because requirements and architecture are verified, but the realized capability is ultimately validated against stakeholder needs in operational context.

## Why This Matters

Building the specified thing is not enough when the specification omitted the right people or mistranslated their outcomes. A service can pass every requirement yet exclude users with limited connectivity. A device can serve clinicians while creating unmanageable sterilization work. A platform can improve developer speed while transferring incident burden to operations. These are needs-definition failures before they become design failures.

ISO/IEC/IEEE 15288:2023 describes stakeholder needs as needs, wants, desires, expectations, and perceived constraints in operational context and treats transformed stakeholder requirements as a reference for validation. ISO/IEC/IEEE 29148:2018 provides lifecycle requirements-engineering processes and information items. NASA separates stakeholder expectations, needs/goals/objectives, requirements, and designs, emphasizing stakeholder identification, ConOps/scenarios, traceability, and continuing involvement.

SEBoK's current Stakeholder Needs Definition guidance emphasizes that elicitation alone is insufficient: risk, drivers, constraints, lifecycle concepts, feasibility, consistency, and integration produce a need set. This module follows that broader view. A meeting transcript is evidence; it is not yet the governed basis for system definition.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. stakeholders include affected non-users, support roles, authorities, and lifecycle participants;
2. value depends on stakeholder, context, measure, distribution, and time;
3. a problem frame separates outcomes, evidence, mechanisms, and interventions;
4. context and scenarios reveal interactions, modes, failures, and handoffs;
5. assumptions and perceived constraints require source and validation;
6. solution-neutral needs preserve alternatives unless realization is genuinely constrained;
7. validation asks whether the integrated system achieves intended use and outcomes.

As a retrieval test, consider “users need one-click approval.” Identify the stakeholder class and operational objective. A requester may want speed, an approver may need evidence and deliberation, security may need authorization, audit may need rationale, and affected parties may need recourse. One-click is an interface proposal. The need set must express timely action, informed authority, auditability, risk limits, accessibility, and exceptions before interaction design.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish stakeholders, customers, users, expectations, needs, objectives, requirements, and designs;
2. discover stakeholder classes across operation, support, governance, impact, and lifecycle;
3. select elicitation methods appropriate to access, power, uncertainty, and context;
4. transform raw inputs into well-formed, solution-neutral candidate needs with source trace;
5. derive needs from scenarios, risks, constraints, ethics, and lifecycle concepts;
6. analyze ambiguity, duplication, feasibility, assumptions, and conflicts;
7. prioritize without equating power, urgency, value, safety, and implementation order;
8. validate and baseline an integrated need set while preserving dissent;
9. trace needs bidirectionally to requirements and operational validation;
10. state evidence limits and escalate consequential judgments to appropriate authorities.

## Core Exposition

**Discover stakeholder classes systematically.** Start from mission, context, scenarios, lifecycle, hazards, interfaces, supply, and governance. Ask who benefits, uses, operates, decides, pays, owns, supplies, maintains, trains, audits, regulates, responds, is exposed, can block, bears failure, and inherits retirement. Use roles before names, then map actual representatives and authority.

**Distinguish interest from representation.** A manager can represent contractual acquisition but not every user workflow. A clinician cannot automatically represent patients, pharmacy, or maintenance. Community organizations may reach people absent from product telemetry but do not erase internal diversity. Record stakeholder class, selected representative, basis, limitations, conflicts of interest, and missing voices.

**Plan elicitation as evidence collection.** Interviews reveal meaning and exceptions; observation reveals actual work and workarounds; workshops reveal interfaces and conflict; surveys estimate distributions if sampling is sound; scenarios reveal temporal needs; artifact/incident review reveals constraints and failure; prototypes reveal response to candidates; operational data reveals observed behavior but omits invisible populations. Triangulate methods.

**Prepare ethical and accessible engagement.** Explain purpose, use, consent, confidentiality, retention, and limits. Provide language, format, timing, assistive, and compensation support where appropriate. Avoid placing participants at employment, legal, social, or safety risk. Some contexts require formal ethics, privacy, labor, community, or regulatory oversight.

**Capture raw input faithfully.** Preserve exact wording where useful, source, role, context, date, method, facilitator interpretation, and confidence. Separate quotation, observation, inference, and candidate need. Do not “clean up” disagreement before analysis. Protect sensitive identity while retaining enough provenance for review.

**Analyze current work without canonizing it.** Workarounds reveal unmet needs, resilience, local expertise, and hidden workload. They can also be unsafe adaptations to a poor system. Ask what outcome the workaround protects, why it exists, who pays its cost, and whether the future system should support, replace, or make it unnecessary.

**Write candidate needs.** Prefer a stakeholder/outcome statement with operational context and rationale: “During regional network loss, field responders need access to the current authorized evacuation area so they can direct residents safely.” Do not write a system `shall`; formal system responsibility comes later. Split independent outcomes that may differ in priority, solution, or validation.

**Avoid invented precision.** Early expectations may be qualitative. Record the qualitative concern and create a measurement-learning item rather than selecting a number without evidence. Later objectives and requirements need justified measures, thresholds, conditions, and uncertainty. A provisional target remains a TBR with owner and consequence.

**Analyze quality.** Check uniqueness, source, stakeholder, rationale, outcome/capability, context/mode, solution neutrality, necessity, feasibility, consistency, assumptions, constraints, measure direction, priority basis, and validation concept. “Easy to use” needs stakeholder tasks, environments, accessibility, workload, error/recovery, and evidence—one generic usability score will not suffice.

**Derive needs responsibly.** Stakeholders may not request cybersecurity, safe disposal, calibration, maintainability, audit, resilience, or emergency behavior. Derive these from hazards, law, ethics, context, enabling systems, lifecycle concepts, operational scenarios, and organizational obligations. Label them derived, cite source/rationale, and validate implications with affected stakeholders and authorities.

**Integrate duplicates without losing nuance.** Two statements may share an outcome but differ by population, mode, threshold, rationale, or authority. Merge only when semantics and downstream validation remain intact. Maintain source links so contributors can see how their input was represented.

**Model conflicts.** Conflicts include incompatible outcomes, resource competition, timing, privacy versus observability, autonomy versus control, safety versus throughput, global consistency versus local adaptation, and unequal distribution. State alternatives, affected groups, non-compensable constraints, evidence, uncertainty, and decision authority. Some conflicts remain deliberately unresolved until trade study or policy decision.

**Prioritize transparently.** Record method and authority. Consider mission contribution, consequence of absence, legal/ethical obligation, safety/security, affected population/distribution, urgency, dependency, feasibility, uncertainty, option loss, and cost of delay. MoSCoW or numeric ranks can communicate but cannot justify themselves. A “must” needs rationale and authority.

**Preserve power distinctions.** High influence does not prove high stakeholder value, and low influence does not justify exclusion. Apply rights, safety, legal, and ethical constraints before compensatory prioritization. Document dissent, imposed decisions, and mitigation. Consensus is evidence of agreement among participants, not universal legitimacy.

**Validate candidate needs.** Use playback, scenario walkthrough, prototypes, models, cross-stakeholder review, and operational evidence. Ask whether the need accurately captures outcome, context, exceptions, rationale, and affected groups; whether it is feasible enough for the next step; and whether any design assumption slipped in. Record acceptance, qualification, objection, and missing evidence.

**Build the integrated set.** Reconcile terminology, scope, lifecycle, conflicts, constraints, and measures. Check coverage across stakeholder classes, scenarios, modes, environments, functions, quality concerns, hazards, support, transition, and retirement. Baseline under named authority only when adequate for the next commitment. Adequate never means every future need is known.

**Trace transformations.** Keep raw sources to candidate needs, integrated needs to requirements, requirements/design to validation methods, and operational evidence back to needs. A requirement can cover multiple needs and a need can require multiple requirements. Coverage needs rationale, not merely a link. Orphan requirements may be unnecessary; uncovered needs may invalidate completeness.

**Use executable checks as bounded aids.** The example below checks five declared records for source, context, solution phrases, conflict state, and learning evidence. It cannot judge whether stakeholder classes are complete, representatives legitimate, needs semantically correct, conflicts acceptable, or validation sufficient.

<!-- bijux-verify: {"id":"stakeholder-need-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"needs_total=5\nwell_formed_declared=1\nmissing_source=N-maintenance\nmissing_context=N-reporting\nsolution_signals=N-reporting:mobile app\nunresolved_conflicts=N-safety,N-speed\nneeds_with_validation_questions=5\nneed_set_ready=false\nevidence=declared_fields_and_lexical_signals_only\n","stderr":""}} -->
```python
needs = [
    {
        "id": "N-access",
        "source": ["rider-research", "accessibility-review"],
        "statement": "riders need equitable access to valid travel",
        "context": ["normal", "network-loss"],
        "conflicts": [],
        "validation": ["representative journey study"],
    },
    {
        "id": "N-reporting",
        "source": ["resident-workshop"],
        "statement": "residents need a mobile app for outage reporting",
        "context": [],
        "conflicts": [],
        "validation": ["compare reporting channels"],
    },
    {
        "id": "N-maintenance",
        "source": [],
        "statement": "maintainers need safe diagnostic access",
        "context": ["maintenance"],
        "conflicts": [],
        "validation": ["maintenance simulation"],
    },
    {
        "id": "N-speed",
        "source": ["operations"],
        "statement": "operators need rapid throughput",
        "context": ["peak"],
        "conflicts": ["unresolved:N-safety"],
        "validation": ["peak scenario"],
    },
    {
        "id": "N-safety",
        "source": ["hazard-analysis"],
        "statement": "affected people need exposure below the authorized limit",
        "context": ["all-modes"],
        "conflicts": ["unresolved:N-speed"],
        "validation": ["safety validation concept"],
    },
]
solution_phrases = ("mobile app", "dashboard", "chatbot", "blockchain")

missing_source = sorted(need["id"] for need in needs if not need["source"])
missing_context = sorted(need["id"] for need in needs if not need["context"])
solution_signals = sorted(
    f"{need['id']}:{phrase}"
    for need in needs
    for phrase in solution_phrases
    if phrase in need["statement"].lower()
)
unresolved = sorted(
    need["id"]
    for need in needs
    if any(conflict.startswith("unresolved:") for conflict in need["conflicts"])
)
well_formed = [
    need
    for need in needs
    if need["source"]
    and need["context"]
    and not any(phrase in need["statement"].lower() for phrase in solution_phrases)
    and need["id"] not in unresolved
]

print(f"needs_total={len(needs)}")
print(f"well_formed_declared={len(well_formed)}")
print(f"missing_source={','.join(missing_source) or 'none'}")
print(f"missing_context={','.join(missing_context) or 'none'}")
print(f"solution_signals={','.join(solution_signals) or 'none'}")
print(f"unresolved_conflicts={','.join(unresolved) or 'none'}")
print(f"needs_with_validation_questions={sum(bool(need['validation']) for need in needs)}")
ready = len(well_formed) == len(needs)
print(f"need_set_ready={str(ready).lower()}")
print("evidence=declared_fields_and_lexical_signals_only")
```

**Manage change and learning.** Needs change when context, stakeholders, policy, hazards, technology possibility, or observed outcomes change. Version rather than overwrite; analyze downstream impact; revalidate with relevant stakeholders; and distinguish newly discovered need from scope change. Operational feedback closes the loop.

**Escalate consequential judgment.** Engineering can structure evidence and alternatives. It cannot unilaterally determine acceptable clinical harm, legal compliance, community legitimacy, labor rights, accessibility, public safety, or ethical tradeoffs. Named authorities and affected stakeholders must participate according to consequence.

## Definitions and Notation

Let stakeholder classes be (G=\{g_1,\ldots,g_m\}), lifecycle contexts (C), raw inputs (I), integrated needs (N), requirements (R), and validation evidence (V).

Define source trace (T_{IN}\subseteq I\times N), coverage trace (T_{NR}\subseteq N\times R), and validation trace (T_{NV}\subseteq N\times V). For baselined need (n):

\[
SourceCovered(n)\iff \exists i:(i,n)\in T_{IN},
\]

\[
RequirementCovered(n)\iff \exists r:(n,r)\in T_{NR},
\]

\[
ValidationPlanned(n)\iff \exists v:(n,v)\in T_{NV}.
\]

Existence of a link does not prove semantic adequacy. Coverage reviews must inspect rationale, context, measures, and transformation loss.

For stakeholder group (g), outcome (y_g), context (c), and desired condition (A_g(c)), a need can be modeled as a predicate:

\[
NeedSatisfied(n,g,c)\iff y_g(c)\in A_g(c).
\]

Some admissible sets are qualitative or partially ordered; forcing a scalar score may erase non-compensable values.

## Mechanisms, Invariants, or Proof Structure

Use this stakeholder-needs procedure:

1. **Frame mission and scope.** Connect problem/opportunity, context, outcomes, lifecycle, constraints, and decision.
2. **Discover stakeholder classes.** Use context, scenarios, hazards, supply, support, governance, impact, and retirement.
3. **Plan representative elicitation.** Select methods, access, ethics, sampling, accommodations, and provenance.
4. **Capture raw evidence.** Separate words, observations, interpretations, inferred needs, and uncertainty.
5. **Form candidate needs.** State one outcome/capability with stakeholder, context, rationale, source, and validation idea.
6. **Analyze and derive.** Check quality, feasibility, assumptions, constraints, lifecycle, hazards, and omitted obligations.
7. **Resolve or preserve conflicts.** Record alternatives, distribution, non-compensable limits, dissent, and authority.
8. **Prioritize transparently.** Use explicit criteria, evidence, consequence, obligation, and decision rights.
9. **Validate and baseline.** Play back across stakeholder classes and scenarios; record qualifications and gaps.
10. **Trace and evolve.** Link sources, requirements, validation, and operational evidence; govern change.

Five invariants guide review.

**Provenance invariant.** Every integrated need retains sources, analysis rationale, and transformation history.

**Representation invariant.** Every claimed stakeholder voice records basis, limitations, missing populations, and conflicts of interest.

**Neutrality invariant.** Need statements preserve realization options unless an evidenced authorized constraint applies.

**Conflict invariant.** Incompatibility and dissent remain visible until explicitly resolved or accepted by authority.

**Validation invariant.** System acceptance returns to stakeholder outcomes in representative lifecycle context, not only requirement conformance.

## Alternatives and Trade-Offs

**Broad discovery versus focused decision.** Broad discovery reduces omission but consumes time and can create unbounded scope. Maintain a stakeholder universe, then justify relevant engagement for each decision and consequence.

**Direct participation versus representation.** Direct voices reduce interpretation loss but may be impractical or unsafe. Representatives enable access but can distort diversity. Combine methods and record limitations.

**Qualitative richness versus quantitative comparability.** Narrative captures context and meaning; measures support thresholds and tradeoffs. Preserve both and avoid invented early precision.

**Consensus versus governed disagreement.** Consensus improves coordination. Forced agreement hides conflict and power. Record dissent and use legitimate decision authority with safeguards.

**Stable baseline versus evolving need set.** Baselines control downstream work. Context and learning continue. Version changes with impact analysis rather than freezing or silently editing.

**Need integration versus source fidelity.** Consolidation makes engineering tractable. Over-merging removes population and context differences. Retain trace and split independently tradeable outcomes.

**Stakeholder priority versus system obligation.** Stated preference matters, but law, ethics, safety, and externality can create needs not prioritized by powerful users. Preserve authority and non-compensable constraints.

**Elicitation depth versus participant burden.** More engagement can improve evidence but impose time, privacy, fatigue, or risk. Target decision-relevant uncertainty and compensate/protect participation appropriately.

## Failure Modes and Misconceptions

1. **The customer is the stakeholder set.** Acquisition authority does not cover every use, impact, or lifecycle role.
2. **Stakeholders know their requirements.** They know outcomes and work; engineers must analyze and transform without usurping value authority.
3. **A feature request is a need.** Recover the desired outcome and context.
4. **Current users represent future and excluded users.** Selection effects can erase the population most affected.
5. **Observation is objective.** Observer, access, context, and interpretation shape evidence.
6. **Consensus proves correctness.** Participants can share blind spots or unequal power.
7. **Priority equals stakeholder influence.** Rights, safety, ethics, consequence, and distribution constrain prioritization.
8. **Derived means optional.** Derived lifecycle, hazard, or legal needs can be mandatory when adequately sourced.
9. **Qualitative means unverifiable.** It needs operational meaning and an appropriate validation concept, not arbitrary numbers.
10. **A trace link proves coverage.** Transformation semantics and validation rationale require review.
11. **Baselined needs never change.** Operational evidence and context change demand governed evolution.
12. **Passing requirements proves need satisfaction.** Verification and stakeholder validation answer different questions.

## Worked Examples

### Example 1

**Question:** How should a transit app request become an integrated need set?

**Assumptions:** The agency wants digital ticketing; riders vary in device, payment, language, disability, connectivity, and trust.

**Reasoning:** Elicit riders, inspectors, drivers, support, finance, privacy/accessibility, operations, and excluded cash/unbanked populations. Separate access, purchase, validation, fare policy, settlement, privacy, accessibility, degraded operation, fraud, support, and transition outcomes. Observe existing cash/card work and failure. Compare app, card, account, kiosk, assisted, and mixed realization later. Trace every consolidated need to source populations and scenarios.

**Evidence limit:** Current-app surveys exclude non-users and failed adopters. Representative journey studies and authority review are needed.

**Conclusion:** Digital ticketing is a solution space; equitable valid travel across contexts is the stakeholder outcome basis.

### Example 2

**Question:** How should sponsor and community expectations be handled when they conflict?

**Assumptions:** A logistics sponsor values nighttime throughput; nearby residents report sleep, safety, and pollution impacts.

**Reasoning:** Preserve throughput, worker, resident, road-user, environmental, and regulatory needs separately. Measure time/location distributions, exposure, incidents, jobs, and alternatives. Do not weight sponsor influence as stakeholder value. Identify legal/noise/safety constraints and decision authority. Compare schedule, routing, quieter equipment, barriers, staging, demand, monitoring, and compensation without presuming all harms are compensable. Record dissent and imposed decisions.

**Evidence limit:** A public meeting attendance list is not representative; operational and environmental studies plus accessible community engagement are needed.

**Conclusion:** Integration exposes conflict and authority; it does not manufacture consensus or erase affected non-users.

### Example 3

**Question:** How does “clinicians expect fewer clicks” become a valid need?

**Assumptions:** Click count is a reported burden in medication ordering; error prevention, evidence, and exceptions also matter.

**Reasoning:** Observe complete tasks across roles, cases, interruptions, and recovery. Determine whether burden comes from redundant data, navigation, latency, unclear policy, alerts, or necessary safety decisions. State needs for timely, cognitively manageable, clinically appropriate ordering with required evidence and safe exception handling. Use task time, error/rework, workload, comprehension, and patient outcomes rather than click count alone. Compare process, policy, data, interface, and staffing changes.

**Evidence limit:** Self-report and click telemetry cannot establish clinical safety or causal mechanism. Human-factors and clinical evaluation are required.

**Conclusion:** Preserve the burden signal while translating the proposed proxy into outcome and context.

### Example 4

**Question:** Why are maintainer needs often discovered late?

**Assumptions:** Acquisition interviews users and operators but treats service access, calibration, spares, tools, and records as supplier details.

**Reasoning:** Add maintainer, trainer, depot, logistics, configuration, cybersecurity, safety, supplier, and disposal roles during context/scenario analysis. Walk fault isolation, safe shutdown, access, diagnosis, replacement, calibration, update, rollback, proof of readiness, and return to service. Derive needs for observability, modularity, access, records, tools, skill, time, and supply continuity. Validate physical/cognitive work using representative configurations.

**Evidence limit:** Design drawings and predicted repair time omit access, tool, fatigue, environment, and supply conditions. Maintenance demonstrations are needed.

**Conclusion:** Lifecycle stakeholder discovery prevents operational capability from depending on invisible support work.

### Example 5

**Question:** How should throughput and safety needs conflict?

**Assumptions:** Operations requests a faster automated line; hazard analysis identifies exposure increasing with speed and reduced separation.

**Reasoning:** State productive throughput and exposure/safe-state needs separately with modes, populations, distributions, and constraints. Determine authorized safety limits before compensatory trade. Explore guarding, separation, sensing, fail-safe control, batch/routing, staffing, and lower-speed alternatives. Record evidence, uncertainty, residual risk authority, and conflict resolution. “High priority” throughput cannot waive a non-compensable limit.

**Evidence limit:** Simulation and component certification do not establish integrated human-system safety. Independent hazard and operational validation are required.

**Conclusion:** Conflict handling applies authority and constraints before optimization; it does not average injury against output.

### Example 6

**Question:** Are supplier and acquirer needs legitimate stakeholder needs?

**Assumptions:** A platform depends on suppliers and must be affordable/supportable, but vendor convenience can conflict with users and lifecycle outcomes.

**Reasoning:** Acquirer needs include mission value, cost, evidence, governance, and exit. Supplier needs may concern stable interfaces, supportability, change notice, and viable delivery. These affect feasibility but do not automatically outrank user safety, privacy, or accessibility. Separate contractual requirements, business preferences, and system needs. Trace accepted supplier constraints and expose lock-in, data custody, support horizon, and substitution.

**Evidence limit:** Commercial agreement shows authority between parties, not satisfaction of all affected stakeholder outcomes.

**Conclusion:** Acquisition and supply are lifecycle perspectives to integrate transparently, not hidden reasons to distort the need set.

### Example 7

**Question:** How can telemetry hide stakeholder needs?

**Assumptions:** A public portal team studies only successful sessions and concludes users need faster page rendering.

**Reasoning:** Missing groups include people without connectivity/device/identity, those deterred before arrival, assistive-technology failures, abandoned sessions before logging, offline/assisted users, and people denied eligibility. Use population denominators, support/appeal records, accessibility tests, community research, observation, and alternate-channel data. Faster rendering can help but may not change access, comprehension, eligibility, or outcome.

**Evidence limit:** Instrumentation observes the system's selected population. Linking broader evidence requires privacy, sampling, and interpretation safeguards.

**Conclusion:** Absence from logs is a stakeholder-discovery signal, not evidence of absent need.

### Example 8

**Question:** How should multilingual expectations be elicited and transformed?

**Assumptions:** Translation occurs after English needs and interface design are fixed; terminology and workflow differ across communities.

**Reasoning:** Engage participants and domain-qualified interpreters early; distinguish language, literacy, cultural meaning, legal terminology, accessibility, and channel. Preserve source-language evidence and translation decisions. Validate scenarios, concepts, error/recovery, urgency, and comprehension—not only literal strings. Derive needs for language selection, consistency, update, interpreter handoff, records, and fallback. Avoid treating one bilingual employee as universal representative.

**Evidence limit:** Back-translation detects some divergence but does not establish operational comprehension or cultural validity. Representative testing is needed.

**Conclusion:** Language is part of stakeholder context and system behavior, not a cosmetic downstream requirement.

### Example 9

**Question:** Can numeric prioritization resolve conflicting needs?

**Assumptions:** A workshop assigns 1–5 scores for value, urgency, and effort, then totals them.

**Reasoning:** Scores may be ordinal, differently interpreted, correlated, and dominated by participants with power. Separate legal/safety/rights constraints; document scoring definitions, evidence, stakeholder/population, uncertainty, and authority; examine sensitivity and distribution; retain conflicts and veto conditions. Use scores to structure conversation, not transform legitimacy into arithmetic. Record why final priority differs from a total.

**Evidence limit:** Reproducible calculation does not validate weights, scales, representation, or compensability.

**Conclusion:** Prioritization is a governed decision supported by evidence, not an automatic property of a spreadsheet.

### Example 10

**Question:** How should needs be validated for an AI-assisted clinical triage capability?

**Assumptions:** Sponsors seek speed; clinicians seek decision support; patients need appropriate care, explanation, privacy, equity, and recourse; historical data reflect prior policy and access.

**Reasoning:** Elicit patients/non-users, caregivers, clinicians, schedulers, emergency care, privacy/security, quality, operations, ethics, and regulators. State needs for timely appropriate routing, safe escalation, comprehensible support, override/recourse, calibrated uncertainty, subgroup outcomes, workload, monitoring, and fallback without prescribing AI. Validate through scenarios, workflow studies, representative populations, and independent domain review. Compare non-automation options.

**Evidence limit:** Interviews and retrospective accuracy cannot establish clinical benefit, fairness, consent, legal sufficiency, or acceptable risk. No external review is claimed.

**Conclusion:** High-consequence need validation requires affected-party and independent authority before requirements or automation claims harden.

## Cross-Program Connections

- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) preserves stakeholder language, policies, roles, and domain invariants without copying solution requests.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) maps stakeholder concerns and scenarios to quality attributes and design decisions.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) governs stakeholder evidence provenance, missing populations, lineage, and measurement quality.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) derives protection needs for users, owners, operators, affected parties, and contested environments.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) translates consumer/provider journeys and constraints into service contracts.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) elicits needs across platform consumers, operators, governance, security, and organizational leadership.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 15288:2023 — System life cycle processes](https://www.iso.org/standard/81702.html), second edition, May 2023. Consulted 2026-08-30.
2. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html), second edition, November 2018. Consulted 2026-08-30.
3. NASA. [*NASA Systems Engineering Handbook*, Rev. 2](https://www.nasa.gov/reference/systems-engineering-handbook/), NASA/SP-2016-6105 Rev2, 2016. Consulted 2026-08-30.
4. NASA. [Stakeholder Expectations Definition](https://www.nasa.gov/reference/4-1-stakeholder-expectations-definition/), *NASA Systems Engineering Handbook*. Consulted 2026-08-30.
5. SEBoK Editorial Board. [Stakeholder Needs Definition](https://sebokwiki.org/wiki/Stakeholder_Needs_Definition), *Guide to the Systems Engineering Body of Knowledge*, version 2.14. Consulted 2026-08-30.
6. SEBoK Editorial Board. [Stakeholder Needs and Requirements](https://sebokwiki.org/wiki/Stakeholder_Needs_and_Requirements_%28glossary%29), *Guide to the Systems Engineering Body of Knowledge*, version 2.14 glossary. Consulted 2026-08-30.
7. INCOSE. [*Guide to Needs and Requirements*](https://portal.incose.org/ItemDetail?Category=EBOOKS&WebsiteKey=d4c31fa4-467a-4959-b48b-cae3ea93e516&iProductCode=GUIDENEEDSREQ), 2022. Consulted 2026-08-30.
8. ISO. [ISO 9241-210:2019 — Human-centred design for interactive systems](https://www.iso.org/standard/77520.html), second edition, 2019. Consulted 2026-08-30.

## Exercises

### Exercise 1

Develop a stakeholder discovery and elicitation plan for a regional emergency-alert capability. Include affected non-users, representation, methods, ethics/access, lifecycle, evidence, and decision authority.

### Exercise 2

Transform these raw statements into candidate needs while preserving sources and uncertainties: “make it one click,” “we cannot lose audit data,” “customers want 24/7,” “maintenance is somebody else's problem,” and “use our current identity vendor.”

### Exercise 3

Analyze and govern a conflict among privacy, fraud detection, customer recourse, support observability, and regulatory retention for a payment service. Separate constraints, needs, measures, authority, and unresolved uncertainty.

### Exercise 4

Design bidirectional traceability from five stakeholder needs through requirements and validation evidence. Include many-to-many coverage, transformation rationale, orphan detection, change impact, and semantic review beyond links.

### Exercise 5

Create and review an integrated need set for a remotely monitored home medical device. Cover patient/caregiver, clinician, emergency, maintenance, supplier, privacy/security, accessibility, network/power, calibration, update, support, and retirement.

## Answers to the Exercises

### Answer 1

Stakeholders include message recipients across language, disability, literacy, device/connectivity, custody/institution, and geography; people without enrollment; originators and authorizing officials; emergency services; local agencies; broadcasters/carriers/platforms; schools/hospitals/employers; support; cybersecurity/privacy; maintainers/trainers; regulators; community organizations; and people harmed by false, late, inaccessible, or privacy-invasive alerts. Map roles, interests, exposure, authority, representation basis, and missing voices.

Use incident/artifact review, accessible multilingual interviews/focus groups, community partnership, operator observation, scenario workshops, survey with population sampling, prototype comprehension studies, and end-to-end exercises. Address consent, confidentiality, participant risk, compensation, accessibility, translation, data retention, and emergency ethics. Cover commissioning, routine warning, ambiguity, overload, network/power failure, cancellation/correction, support, maintenance/update, incident review, and retirement. Preserve raw evidence and dissent. Named emergency, public safety, accessibility, community, privacy/security, operational, technical, and regulatory authorities govern applicable decisions.

### Answer 2

“One click” becomes timely, cognitively manageable completion of a named task in stated contexts, retaining authorization, error prevention, accessibility, and recovery; click count remains source evidence or a candidate performance proxy. “Cannot lose audit data” separates accountable reconstruction/retention needs from durability, legal, privacy, and recovery constraints with data classes and horizons. “24/7” becomes outcome and interruption/recovery needs by service, population, mode, consequence, and time zone rather than literal perfection.

“Maintenance is somebody else's problem” is a scope assertion to challenge: derive safe diagnosability, access, repair, calibration, configuration, supply, records, and return-to-service needs from lifecycle scenarios and assign roles. “Use current identity vendor” is a design preference unless an evidenced contract/interface makes it a scoped constraint; recover identity, authorization, availability, privacy, assurance, degraded-mode, migration, and exit needs. Each candidate retains speaker/source, context, rationale, assumptions, uncertainty, conflicts, and validation question.

### Answer 3

Stakeholder needs include legitimate fraud prevention, minimal/authorized data use, explainable decisions, timely challenge and correction, support diagnosis, evidentiary integrity, and service continuity. Constraints include applicable privacy, payment, consumer-protection, record-retention, security, and contractual obligations interpreted by competent authority. Do not label all desired telemetry or retention mandatory.

Map data purpose, provenance, access, decision use, false positives/negatives, affected populations, appeal, support views, retention/deletion/holds, audit, breach consequence, and supplier flows. Measures cover fraud loss/detection uncertainty, wrongful block and subgroup distribution, resolution time/outcome, data exposure, access misuse, support efficacy, and record completeness. Explore minimization, tiered access, purpose separation, derived signals, retention classes, case-based elevation, independent audit, and recourse. Preserve conflicts and non-compensable legal/rights constraints; legal/privacy, security, risk, operations, support, customer/affected-party, and governance authorities decide residual tradeoffs.

### Answer 4

Give every need, source, requirement, and validation item stable identity and version. Store source-to-need rationale, need-to-requirement coverage rationale, requirement allocation/verification, and need-to-validation outcome evidence. A need can map to several functional, performance, interface, constraint, and support requirements; one requirement can support multiple needs. State partial versus full coverage, contexts, assumptions, and measures.

Audit needs without requirements or validation, requirements without authorized need/constraint source, and validation evidence without a need/outcome. Review semantics: a link from “equitable access during network loss” to “API timeout 30 seconds” is not obviously adequate. On change, traverse affected requirements, architecture, hazards, tests, operations, and stakeholders; preserve baselines and revalidate. Link counts support navigation but cannot prove transformation fidelity or operational satisfaction.

### Answer 5

Patient/caregiver needs cover safe intended outcome, comprehensible/accessibile operation, consent/privacy, status, alarm interpretation, burden, travel/use conditions, supplies, help, recourse, and local safe behavior. Clinicians need trustworthy context/trends, uncertainty, workflow fit, escalation, records, and responsibility. Emergency roles need location/contact, priority, handoff, and device-independent action. Maintenance needs diagnosability, safe access, calibration, parts/tools, configuration, update/rollback, cleanliness, evidence, and return-to-service. Suppliers/operators need supportable interfaces, monitoring, incident/change communication, and lifecycle feasibility without displacing patient outcomes.

Derived needs address network/power loss, time/identity, cybersecurity/privacy, data quality/provenance, alarm delivery, interoperability, manufacturing variation, calibration drift, accessibility/language, training, backup/recovery, updates, decommissioning, data/key deletion, and disposal. Validate across representative homes, populations, clinical workflows, degraded/emergency/maintenance states, and lifecycle conditions. Automation or local review cannot establish clinical benefit, informed consent, legal/regulatory sufficiency, accessibility, equity, or acceptable residual risk. Named patient/caregiver, clinical, human-factors/accessibility, safety, privacy/security, software/data, maintenance, operational, quality, ethics, legal/regulatory, emergency, and supplier authorities must review applicable needs. No external clinical, regulatory, academic, or practitioner review is claimed.
