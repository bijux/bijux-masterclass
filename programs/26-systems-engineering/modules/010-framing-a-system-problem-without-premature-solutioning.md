---
module_id: SYSENG-010
program: Systems Engineering
level: 1
module_number: 10
title: Framing a System Problem Without Premature Solutioning
status: complete
last_verified: 2026-08-30
---

# Framing a System Problem Without Premature Solutioning

## One-Page Review

### Governing question

What situation, outcomes, mechanisms, stakeholders, constraints, uncertainties, and evidence should govern action before a preferred intervention is allowed to define the problem it is supposed to solve?

### Essential definitions

- A **problem situation** is a set of observed or anticipated conditions in which stakeholder outcomes differ materially from desired outcomes.
- An **opportunity** is a plausible change in capability or context that could create additional stakeholder value, not merely a proposed product feature.
- A **problem frame** is a provisional, purpose-specific account of the situation, affected stakeholders, boundaries, outcomes, evidence, mechanisms, constraints, uncertainties, and decision authority.
- A **symptom** is an observed effect; a **causal hypothesis** proposes a mechanism that may contribute to it and remains open to challenge.
- A **need** expresses an outcome or capability required to address the situation; it should not silently prescribe a realization.
- A **solution concept** is a candidate intervention or class of interventions considered after the frame establishes what successful change must accomplish.
- **Premature solutioning** occurs when an intervention is selected or embedded in the need before the problem, alternatives, tradeoffs, and consequences are adequately understood.
- **Solution neutrality** preserves multiple realizations at the problem/need level; it does not forbid technical constraints that genuinely come from authorized sources.
- A **boundary judgment** determines whose outcomes, which causes, and which lifecycle effects are included or excluded.
- A **measure of the problem** characterizes the present or counterfactual situation; a **measure of effectiveness** evaluates whether an intervention improves stakeholder outcomes.
- A **reframing trigger** is evidence that changes the relevant stakeholders, boundary, mechanism, objective, constraint, or decision.

### Central model, mechanism, or theorem

Represent a frame as:

\[
F=\langle situation,stakeholders,boundaries,outcomes,evidence,
mechanisms,measures,constraints,assumptions,uncertainties,authority,
options,learning,reframe\ triggers\rangle.
\]

Separate three claims:

\[
ObservedGap = DesiredOutcome-ObservedOutcome,
\]

\[
MechanismHypothesis: Conditions\rightarrow ObservedGap,
\]

\[
InterventionHypothesis: Action\rightarrow MechanismChange\rightarrow OutcomeChange.
\]

Evidence for the gap does not prove the mechanism; evidence for a mechanism does not prove a preferred intervention; intervention performance does not by itself establish legitimate stakeholder value. Maintain traceability and alternative explanations across all three.

### Critical invariants

- Problem statements distinguish observation, interpretation, causal hypothesis, value judgment, and proposed action.
- Every frame names affected non-users, disadvantaged groups, operators, maintainers, authorities, and lifecycle stakeholders where relevant.
- Boundaries expose exported cost, risk, workload, delay, environmental effect, and responsibility.
- Needs and objectives describe outcomes and capabilities unless an implementation is a verified external constraint.
- At least two materially different intervention classes remain visible before selection, including process, policy, information, organizational, demand, and no-build options where applicable.
- Root-cause language does not erase interacting causes, feedback, incentives, or uncertainty.
- Baselines, denominators, distributions, time horizons, and counterfactuals accompany performance claims.
- Measures resist proxy gaming and include distributional and unintended effects.
- Problem and solution understanding iterate, but new solution evidence must update the frame rather than rewrite it retrospectively.
- High-consequence frames require applicable domain, safety, security, legal, ethical, human-factors, and affected-stakeholder authority.

### Common failures

Failures include writing “we need an app” as the need; accepting the sponsor's favored cause as fact; solving a visible symptom while feedback recreates it; treating one stakeholder's inconvenience as the whole-system problem; choosing a boundary that exports harm; averaging away unequal outcomes; using “five whys” to assert one root cause; confusing absence of data with absence of impact; optimizing a proxy; demanding requirements before the problem frame is coherent; calling a mandate immutable without checking authority; running discovery only with current users; and refusing to reframe after experiments contradict the original theory.

### Compact example

“We need a mobile app so residents report water outages” embeds a channel. The problem might instead be delayed detection and inequitable response: some residents lack smartphones, outages may already be visible in pressure telemetry, call centers may not share records, field crews may lack prioritization, and utilities may have ambiguous response authority. A sound frame measures detection-to-restoration by population and outage type, maps mechanisms and handoffs, and compares telemetry, phone/SMS, community liaison, operational process, staffing, and app options. The app can remain a candidate without becoming the definition of success.

### Connections

Retrieve system boundaries, effectiveness, stakeholder value, emergence, feedback, openness, uncertainty, assumptions, dependencies, and operational scenarios from Modules 001–009. Continue to stakeholder needs and expectations, operational concepts, requirements, architecture alternatives, decision analysis, risk, validation, and socio-technical governance.

## Governing Question

Teams rarely begin with no proposed solution. A customer requests a dashboard, a regulator cites a control, an executive announces artificial intelligence, or an engineer recognizes a familiar architecture. Candidate ideas are useful probes. The danger begins when the favorite idea determines which evidence is collected, which stakeholders count, how success is measured, and what alternatives are allowed.

The governing question is therefore disciplined and political as well as technical: what must be true about the situation before action is justified, whose outcomes define improvement, and which choices remain genuinely open? A good frame neither freezes analysis forever nor pretends to be neutral. It records evidence, values, boundary judgments, uncertainty, authority, and the conditions under which it must change.

## Why This Matters

The cost of solving the wrong problem can exceed the cost of poor implementation. A faster claims system can increase unjust denials. More road capacity can induce demand and restore congestion. An alerting tool can add signals while staffing and authority remain broken. A predictive model can automate a biased decision instead of improving the underlying outcome.

NASA's systems engineering guidance distinguishes needs, goals, objectives, requirements, and designs and states that a need should relate to the problem rather than be the solution. SEBoK's problem/opportunity guidance emphasizes affected parties, environment, viewpoints, problem context, power, and iteration between problem exploration and solution synthesis. ISO/IEC/IEEE 15288:2023 places business or mission analysis and stakeholder needs within a lifecycle framework.

Avoiding premature solutioning does not mean delaying every decision until certainty. Framing must be sufficient for the consequence and reversibility of the next commitment. Teams can use small prototypes, simulations, policy trials, and observational studies to learn. The discipline is to label them as candidate interventions, retain competing explanations, protect affected stakeholders, and feed evidence back into the frame.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. boundaries are chosen for a concern and can hide exported consequences;
2. stakeholders include affected non-users and governing/support roles;
3. measures of effectiveness connect mission outcomes to stakeholder value;
4. feedback, delays, and adaptation can recreate a symptom after local improvement;
5. uncertainty includes data gaps, model form, futures, ambiguity, and value conflict;
6. assumptions and constraints require source, scope, evidence, and authority;
7. operational scenarios reveal end-to-end interactions and lifecycle obligations.

As a retrieval test, examine “the queue is too long.” Ask which queue, for whom, compared with what baseline or need, at which times, with what outcome consequence, and across which boundary. A short visible queue may hide abandonment, deflection to another channel, staff overload, or inequitable prioritization. The observed length is a symptom; the frame must connect it to valued outcomes and plausible mechanisms.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish situation, symptom, gap, causal hypothesis, need, objective, requirement, and solution concept;
2. write evidence-backed problem/opportunity frames without silently selecting implementation;
3. expose stakeholder, power, boundary, lifecycle, and distributional judgments;
4. develop and test multiple causal hypotheses, including feedback and common causes;
5. separate problem measures, effectiveness measures, constraints, and proxies;
6. identify solution-laden language and determine whether it represents bias or a real constraint;
7. create materially different intervention classes and a defensible no-build comparator;
8. design learning actions that can reframe the problem safely;
9. define frame adequacy and reframing triggers for the next decision;
10. state evidence limits and escalate consequential judgments to appropriate authorities.

## Core Exposition

**Begin with the situation, not the artifact.** Describe what is happening, where, when, to whom, and with what consequence. Separate observed facts from reports and interpretations. “Thirty percent of rural emergency calls lack usable location within two minutes” is more informative than “dispatch needs a location dashboard.” Include denominators, distributions, observation method, and uncertainty.

**Frame opportunities as outcomes.** An opportunity is not “adopt digital twins.” It might be “reduce discovery time for cross-discipline integration conflicts before physical assembly.” The technology may be promising, but other interventions—shared interface models, earlier integration, process changes, simulation, supplier collaboration—must remain comparable.

**Distinguish symptom and mechanism.** A backlog is observable. Causes may include arrival bursts, low capacity, rework, batching, priority rules, missing information, incentives, policy, or feedback from delay. Treat causal diagrams, interviews, logs, experiments, and domain theory as evidence with limits. Do not promote correlation or stakeholder belief to established cause without warrant.

**Avoid the single root-cause trap.** Some defects have a direct correctable cause. Socio-technical outcomes often arise from necessary and contributory conditions, common causes, feedback, and historical choices. “Five whys” can reveal hypotheses but its stopping point depends on question, boundary, and authority. Maintain a causal network and distinguish control leverage from moral blame.

**Make value judgments explicit.** Calling a state problematic requires a desired comparison. Who prefers the change, who may lose, and who decides? State outcome, affected population, threshold or direction, horizon, and rationale. Preserve non-compensable safety, rights, accessibility, or legal constraints instead of averaging them into total benefit.

**Include power and voice.** Sponsors, users, operators, maintainers, suppliers, regulators, communities, and people excluded by current service have different evidence and influence. Participation does not automatically resolve conflict. Record whose frame was heard, whose evidence is missing, how dissent is preserved, and which authority can decide without pretending authority creates legitimacy.

**Challenge the boundary.** Expand around exported workload, risk, delay, cost, waste, privacy harm, emissions, and lifecycle responsibility. A hospital can reduce emergency wait time by diverting cases elsewhere while worsening population outcomes. A platform can improve internal reliability by transferring integration toil to every team. Model adjacent systems and affected stakeholders before accepting local metrics.

**Define baseline and counterfactual.** Current performance, trend, seasonal pattern, cohort differences, and existing workarounds establish the baseline. The relevant counterfactual may be no action, continuation, policy change already underway, or an alternate intervention. Before-after improvement is weak evidence when demand, population, incentives, or environment changed.

**Separate measures.** Problem measures characterize the gap. Measures of effectiveness test stakeholder outcome. Measures of performance characterize the intervention. Leading indicators expose mechanisms and conditions. Guardrail measures detect harm. For a call-routing intervention, model accuracy is performance; time to appropriate care is effectiveness; missed vulnerable callers is a guardrail.

**Protect against proxy gaming.** When a measure becomes a target, actors and systems adapt. Track distributions, denominators, unobserved populations, balancing measures, and qualitative evidence. Shortening average case time can increase abandonment and complex-case harm. Specify what evidence would show the metric no longer represents the intended outcome.

**Write a provisional frame.** Use:

\[
f=(id,situation,evidence,stakeholders,affected\ nonusers,boundary,
observed\ outcomes,desired\ outcomes,mechanisms,constraints,assumptions,
uncertainties,measures,authority,learning,triggers).
\]

Mark confidence and disagreement. A frame is a versioned decision artifact, not a timeless truth. It should explain why the next analysis or commitment is warranted and what would reopen it.

**Translate to solution-neutral needs.** “Provide a centralized dashboard” prescribes form. “Enable authorized incident coordinators to establish shared, current incident state within two minutes under network degradation” expresses capability and context. If centralization is legally mandated or required by a verified interface, record the source as a constraint rather than smuggling it into the need.

**Generate intervention classes.** Explore prevention, demand shaping, policy/rule, process, staffing/skills, information, interface, organizational authority, automation, physical design, market/incentive, resilience, and recovery. Include improvements to the current system, substitution, removal, and no-build/monitoring. Alternatives should differ in mechanism, not color or vendor.

**Use ideas to test the frame.** Sketching a candidate can reveal missing needs, constraints, and stakeholders. Keep a trace from feature to hypothesized mechanism and outcome. If a prototype succeeds, ask whether the frame changes; if it fails, distinguish bad implementation from wrong mechanism or outcome assumption. Do not rewrite the original problem to match the built artifact.

**Define frame adequacy by decision.** A frame is adequate for a reversible discovery experiment sooner than for an irreversible procurement or public-safety deployment. Criteria include stakeholder/boundary coverage, evidence strength, alternative mechanisms, solution-neutral outcomes, constraints/authority, uncertainty, measures, options, learning plan, and consequence. Adequate does not mean complete.

The executable checker below examines three declared frame records. It flags missing evidence, absent affected non-users, and explicit solution-lock phrases. It cannot infer whether the prose is truthful, whether a technology term is actually mandated, whether stakeholders are legitimate, or whether the frame is adequate beyond those fields.

<!-- bijux-verify: {"id":"problem-frame-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"frames_total=3\ncomplete_declared_frames=1\nmissing_evidence=F-access\nmissing_affected_nonusers=F-congestion\nsolution_lock_signals=F-access:mobile app\nframes_with_learning_questions=3\nframe_records_ready=false\nevidence=declared_fields_and_lexical_signals_only\n","stderr":""}} -->
```python
frames = [
    {
        "id": "F-water",
        "need": "reduce detection-to-restoration time for affected residents",
        "evidence": ["outage-timestamps", "resident-interviews"],
        "affected_nonusers": ["residents-without-digital-access"],
        "learning": ["test handoff-delay hypothesis"],
    },
    {
        "id": "F-access",
        "need": "build a mobile app for service access",
        "evidence": [],
        "affected_nonusers": ["people-without-smartphones"],
        "learning": ["compare assisted and remote channels"],
    },
    {
        "id": "F-congestion",
        "need": "reduce unreliable door-to-door travel time",
        "evidence": ["travel-time-distribution"],
        "affected_nonusers": [],
        "learning": ["measure induced-demand response"],
    },
]
solution_phrases = ("mobile app", "dashboard", "blockchain", "chatbot")

missing_evidence = sorted(frame["id"] for frame in frames if not frame["evidence"])
missing_nonusers = sorted(frame["id"] for frame in frames if not frame["affected_nonusers"])
solution_signals = sorted(
    f"{frame['id']}:{phrase}"
    for frame in frames
    for phrase in solution_phrases
    if phrase in frame["need"].lower()
)
complete = [
    frame
    for frame in frames
    if frame["evidence"]
    and frame["affected_nonusers"]
    and not any(phrase in frame["need"].lower() for phrase in solution_phrases)
]

print(f"frames_total={len(frames)}")
print(f"complete_declared_frames={len(complete)}")
print(f"missing_evidence={','.join(missing_evidence) or 'none'}")
print(f"missing_affected_nonusers={','.join(missing_nonusers) or 'none'}")
print(f"solution_lock_signals={','.join(solution_signals) or 'none'}")
print(f"frames_with_learning_questions={sum(bool(frame['learning']) for frame in frames)}")
ready = len(complete) == len(frames)
print(f"frame_records_ready={str(ready).lower()}")
print("evidence=declared_fields_and_lexical_signals_only")
```

**Design learning and reframing.** Prioritize uncertainty that could change the boundary, mechanism, outcome, or choice. Use interviews, observation, data audit, process tracing, simulation, experiments, prototypes, and historical comparison with appropriate consent and safeguards. Predefine what result supports, weakens, or changes each hypothesis.

**Preserve decision history.** Version frames and link evidence, stakeholder contributions, rejected interpretations, candidate concepts, and decisions. When the frame changes, record why and reassess requirements, architecture, risks, and validation. A clean narrative that hides uncertainty and dissent is weaker than an honest evolution record.

## Definitions and Notation

Let stakeholder or affected group (g\in G), outcome measure (y_g(t)), desired condition (y_g^*(t)), and problem gap:

\[
\Delta_g(t)=y_g^*(t)-y_g(t).
\]

Direction and acceptability depend on the measure; not all stakeholder values are scalar or compensable. Define baseline (B), candidate action (a), and counterfactual outcome (Y(0)). The intervention effect of interest is conceptually:

\[
Effect(a)=Y(a)-Y(0),
\]

but (Y(0)) is generally unobserved and requires a causal design or bounded assumptions. Before-after difference alone is not the effect.

Let mechanism hypothesis (h_k) have supporting/challenging evidence (E_k), uncertainty (U_k), and predicted observations under action (a). Maintain alternatives (H=\{h_1,\ldots,h_n\}) until evidence or decision scope justifies narrowing.

A solution-neutral need (N) specifies outcome/capability (O), context (C), affected group (G), measure/threshold (M), and constraints (K), without specifying realization (R) unless (R\in K) is supported by authorized evidence:

\[
N=\langle O,C,G,M,K\rangle,\quad R\notin N\setminus K.
\]

## Mechanisms, Invariants, or Proof Structure

Use this problem-framing procedure:

1. **State the observed situation.** Separate measurements, reports, interpretations, unknowns, and source limitations.
2. **Identify stakeholders and power.** Include beneficiaries, harmed/excluded groups, operators, maintainers, suppliers, authorities, and lifecycle parties.
3. **Choose and challenge boundaries.** Trace exported cost, delay, risk, workload, environmental effect, and responsibility.
4. **Define outcome gaps.** State baseline, desired condition, population, distribution, horizon, counterfactual, and value rationale.
5. **Develop causal hypotheses.** Map interacting mechanisms, feedback, delays, incentives, common causes, and alternatives.
6. **Separate constraints from choices.** Verify source, authority, scope, waiver, and evidence for claimed mandates.
7. **Design measures.** Distinguish problem, effectiveness, performance, leading, and guardrail measures; anticipate gaming.
8. **Generate intervention classes.** Preserve materially different mechanisms and a credible no-build/current-system comparator.
9. **Plan learning.** Target decision-relevant uncertainty with ethical, bounded, interpretable evidence.
10. **Set adequacy and reframing gates.** Record authority, residual disagreement, next commitment, and triggers for reopening.

Five invariants guide review.

**Separation invariant.** Observation, causal interpretation, desired value, and proposed intervention remain individually traceable.

**Plurality invariant.** Multiple stakeholder frames, mechanisms, and intervention classes remain visible until narrowing is justified.

**Boundary invariant.** Improvement cannot be claimed by silently exporting material harm or obligation.

**Neutrality invariant.** Needs express outcomes/capabilities unless implementation is an evidenced authorized constraint.

**Learning invariant.** New evidence can revise the frame, and records preserve what changed rather than manufacturing hindsight.

## Alternatives and Trade-Offs

**Broad versus actionable frame.** A wide frame exposes causes and consequences but can exceed decision authority. A narrow frame enables action but may optimize locally. Maintain the wider situation and explicitly select the next tractable intervention boundary.

**Root-cause depth versus timely control.** Investigation can reveal durable leverage. Immediate containment may be essential before causal certainty. Separate containment, recovery, and long-term mechanism change.

**Solution neutrality versus genuine mandates.** Neutrality preserves options. Physical, legal, contractual, interoperability, or emergency constraints can narrow them. Verify mandates and distinguish required outcome/interface from inherited implementation detail.

**Quantitative evidence versus lived experience.** Measurements support scale and comparison; qualitative evidence reveals mechanisms, meaning, exclusion, and unobserved work. Triangulate rather than ranking one automatically above the other.

**Consensus versus preserved disagreement.** Agreement speeds commitment. Forced consensus hides value conflict and uncertainty. Record alternative frames, decision rules, dissent, and consequences.

**Discovery versus delivery.** More framing can reduce expensive error but delay benefit. Scale evidence to consequence, uncertainty, reversibility, and option loss; use bounded learning actions.

**Optimization versus robustness.** Optimization serves a chosen model and metric. Robust interventions perform acceptably across frames and futures but may sacrifice peak gains. Compare distributions and guardrails.

**Build versus change the surrounding system.** A product can be visible and fundable. Process, policy, staffing, incentives, standards, or removal may address the mechanism more directly. Compare lifecycle burden and stakeholder effects.

## Failure Modes and Misconceptions

1. **The request defines the problem.** A request supplies evidence and authority, not automatic causal adequacy.
2. **Solution words are always forbidden.** A mandated interface can be a real constraint; prove source and scope.
3. **A symptom is a cause.** Backlog, error, delay, and cost require mechanism hypotheses.
4. **There is one root cause.** Interacting socio-technical systems often have multiple necessary and contributory causes.
5. **More stakeholder interviews create legitimacy.** Sampling, power, exclusion, synthesis, and decision authority still matter.
6. **The average defines improvement.** Distributional harm and non-compensable constraints can be hidden.
7. **A metric is the outcome.** Proxies drift and invite gaming.
8. **No data means no problem.** Measurement systems can systematically omit affected groups or informal work.
9. **Prototyping validates the frame.** It provides conditional evidence about a candidate and tested context.
10. **Problem framing ends before design.** Solution exploration and operation can reveal reasons to reframe.
11. **Reframing means failure.** Evidence-driven reframing is disciplined learning; silent retrospective rewriting is failure.
12. **Neutrality removes values.** Boundary, outcomes, measures, and authority always embody judgments that must be explicit.

## Worked Examples

### Example 1

**Question:** How should “build a water-outage app” be reframed?

**Assumptions:** The sponsor observes delayed resident reports and restoration but does not yet know whether reporting is the limiting mechanism.

**Reasoning:** Measure detection, confirmation, dispatch, repair, and restoration time by location, outage type, and population. Include residents without smartphones, call center, telemetry, field crews, utility authority, public health, and community organizations. Hypotheses include poor sensing, fragmented intake, ambiguous priority, staffing, parts, or authority. Compare telemetry, phone/SMS, shared case state, community liaison, process, and app interventions. Guardrails include accessibility, privacy, false reports, and unequal restoration.

**Evidence limit:** Existing digital analytics omit disconnected residents and cannot establish the causal bottleneck. Field/process observation and affected-community input are needed.

**Conclusion:** Frame the outcome as equitable detection-to-restoration, preserving the app as one candidate mechanism.

### Example 2

**Question:** Is road congestion solved by adding lanes?

**Assumptions:** Peak travel time is unreliable; population, land use, mode choice, price, and routing adapt to capacity.

**Reasoning:** Define whose accessibility and travel reliability matter, including transit users, pedestrians, residents, freight, emergency services, and displaced communities. Model bottlenecks, demand timing, incidents, land use, parking, pricing, transit alternatives, induced demand, emissions, safety, and feedback. Lane expansion may improve an initial constraint while attracting demand and shifting congestion. Compare demand management, transit, incident response, flexible work, land-use, pricing, and targeted capacity.

**Evidence limit:** Short post-opening travel improvement does not establish durable system effect. Counterfactual, multi-year, distributional, safety, and environmental evidence is needed.

**Conclusion:** The problem is reliable, equitable access under adaptive demand, not insufficient asphalt by definition.

### Example 3

**Question:** Why might replacing an incident pager fail to improve response?

**Assumptions:** Teams report missed pages and slow recovery, and a new alert product is proposed.

**Reasoning:** Trace detection, classification, routing, acknowledgement, escalation, shared state, decision rights, remediation, handoff, and learning. Slow response may arise from noisy monitors, unclear ownership, excessive workload, access failure, missing runbooks, dependency uncertainty, or authority—not pager transport. Measure time to correct recognition and effective action, false/duplicate load, after-hours burden, and recovery quality. Candidate classes include monitoring, ownership, staffing, training, access, process, and tooling.

**Evidence limit:** Pager delivery logs show transmission, not comprehension, authority, or effective mitigation. Observed incident work and controlled exercises are required.

**Conclusion:** Alert delivery is one link in a socio-technical response mechanism and should not define the need.

### Example 4

**Question:** Can shorter average hospital wait time be a harmful frame?

**Assumptions:** Leadership targets average arrival-to-disposition time; patient severity, language, disability, complexity, and access vary.

**Reasoning:** Average reduction can be achieved by deflecting difficult cases, premature discharge, or prioritizing easy throughput. Frame timely appropriate care, safety, experience, equity, staff workload, downstream readmission, and population access. Analyze distributions and cohorts, triage policy, diagnostics, beds, discharge coordination, staffing, arrival patterns, and external care capacity. Preserve safety and rights as guardrails. Engage patients, clinicians, support staff, and downstream providers.

**Evidence limit:** Administrative timestamps and one metric cannot establish clinical appropriateness or equity. Clinical, human-factors, operational, legal, and patient review are required.

**Conclusion:** Optimize stakeholder health outcomes and safe flow, not an average proxy isolated from consequence.

### Example 5

**Question:** When is a specified technology legitimately part of the frame?

**Assumptions:** A system must interoperate with an installed rail signaling interface governed by a binding standard, but the sponsor also prefers a vendor product.

**Reasoning:** Verify the standard, version/profile, applicability, authority, interface semantics, and waiver path. Treat conformance as a constraint if justified. The particular vendor remains a design choice unless procurement or compatibility authority proves otherwise. Express the need as safe interoperable control across the mandated interface, not “buy vendor X.” Explore conforming realizations, adapters, transition, assurance, lifecycle support, and exit.

**Evidence limit:** A citation or sponsor assertion does not establish technical/legal applicability. Qualified engineering, procurement, safety, and regulatory interpretation is required.

**Conclusion:** Solution neutrality respects genuine constraints while refusing to convert preference into inevitability.

### Example 6

**Question:** What is wrong with “operator error is the root cause”?

**Assumptions:** An operator issued an incorrect command before an outage; interface, training, workload, alarms, procedure, and organizational incentives also influenced action.

**Reasoning:** Distinguish proximate action from conditions making it possible and likely. Reconstruct information available, mode, interface mapping, confirmation, time pressure, fatigue, staffing, alarm load, training, procedure, authority, and recovery. Ask counterfactuals: would another qualified operator likely do the same? Could one action create catastrophic effect? Compare interface constraints, automation, training, workload, review, and safe recovery. Avoid blame-driven boundary closure.

**Evidence limit:** Logs show events but not perception, cognition, or organizational context. Independent human-factors and just-culture investigation may be needed.

**Conclusion:** Causal framing should reveal system conditions and control leverage, not stop at the last human action.

### Example 7

**Question:** How should an energy-flexibility opportunity be framed?

**Assumptions:** A campus can shift some loads, generation and prices vary, and occupants value comfort and continuity.

**Reasoning:** State opportunity as reducing peak cost/emissions and increasing resilience without violating comfort, safety, research, accessibility, or operational constraints. Map load types, thermal/storage state, occupancy, forecasts, tariffs, grid signals, generators, maintenance, and authority. Compare scheduling, controls, storage, envelope improvements, local generation, pricing, and behavior support. Measure lifecycle cost, emissions with marginal factors, comfort distributions, interruption, and rebound.

**Evidence limit:** Simulation depends on weather, occupancy, tariff, control, and equipment assumptions. Pilot evidence may not transfer seasons or buildings.

**Conclusion:** Outcome framing keeps technology choices open and makes opportunity tradeoffs visible.

### Example 8

**Question:** How should “use AI for case triage” be reframed?

**Assumptions:** Case assignment is slow and inconsistent; historical labels reflect prior policy, workload, and possible inequity.

**Reasoning:** Define needed outcome: timely, accurate, explainable, equitable routing with safe escalation and manageable work. Investigate intake quality, category ambiguity, policy, expertise distribution, queue incentives, handoff, feedback, and appeal. Compare clearer rules, training, forms, staffing, workflow, decision support, statistical models, and automation. Model how predictions change labels and future data. Set subgroup, override, false-negative, workload, privacy, and recourse guardrails.

**Evidence limit:** Offline accuracy does not establish causal benefit, fairness, workflow fit, or legitimacy. Representative prospective and human-system evaluation is required.

**Conclusion:** Frame the decision outcome and mechanism before selecting artificial intelligence as the intervention.

### Example 9

**Question:** What if stakeholders disagree whether the situation is a problem?

**Assumptions:** A river-control project reduces downstream flood probability but affects upstream land, ecosystems, cultural sites, and livelihoods.

**Reasoning:** Preserve distinct frames, evidence, rights, power, uncertainty, and distribution across time and geography. Do not average all outcomes into one undisputed score. Define legal and safety constraints, non-compensable values, decision authority, consent/consultation duties, and alternatives such as restoration, zoning, warning, relocation support, or distributed retention. Use scenarios and deliberation to expose consequence and uncertainty.

**Evidence limit:** Technical modeling cannot determine legitimate cultural value, acceptable displacement, or distributive justice. Independent ecological, legal, community, and governance processes are required.

**Conclusion:** Disagreement can be substantive value conflict requiring explicit governance, not noise to eliminate from the frame.

### Example 10

**Question:** How should a safety-critical medication problem be framed without prescribing automation?

**Assumptions:** Harmful administration errors occur across ordering, verification, preparation, dispensing, bedside identification, delivery, monitoring, and response.

**Reasoning:** Characterize event and near-miss pathways by medication, patient, setting, workload, handoff, interface, equipment, policy, and recovery. Include patients, clinicians, pharmacy, support, devices, records, suppliers, governance, and regulators. Hypotheses include ambiguous orders, look-alike packaging, interruptions, identity, timing, training, alerts, staffing, and reconciliation. Compare process, packaging, staffing, standardization, decision support, device, and monitoring interventions with workload and new-failure guardrails.

**Evidence limit:** Incident reports undercount harm and contain hindsight bias. No local analysis establishes clinical efficacy, regulatory sufficiency, or acceptable residual risk; no external review is claimed.

**Conclusion:** High-consequence framing must preserve the medication-use system, multiple mechanisms, patient outcomes, and independent authority before automation selection.

## Cross-Program Connections

- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) separates domain problems, policies, invariants, and candidate software responsibilities.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) evaluates alternative structures against stakeholder concerns and quality-attribute scenarios.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) governs evidence provenance, population coverage, quality, lineage, and measurement bias.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) reframes requested controls through assets, adversaries, trust, harm, and assurance.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) distinguishes service outcomes from endpoint or protocol choices.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) frames developer and organizational outcomes before selecting platform products or automation.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 15288:2023 — System life cycle processes](https://www.iso.org/standard/81702.html), second edition, May 2023. Consulted 2026-08-30.
2. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html), second edition, November 2018. Consulted 2026-08-30.
3. NASA. [*NASA Systems Engineering Handbook*, Rev. 2](https://www.nasa.gov/reference/systems-engineering-handbook/), NASA/SP-2016-6105 Rev2, 2016. Consulted 2026-08-30.
4. NASA. [Stakeholder Expectations Definition](https://www.nasa.gov/reference/4-1-stakeholder-expectations-definition/), *NASA Systems Engineering Handbook*. Consulted 2026-08-30.
5. SEBoK Editorial Board. [Identifying and Understanding Problems and Opportunities](https://sebokwiki.org/wiki/Identifying_and_Understanding_Problems_and_Opportunities), *Guide to the Systems Engineering Body of Knowledge*, version 2.14. Consulted 2026-08-30.
6. SEBoK Editorial Board. [Business or Mission Analysis](https://sebokwiki.org/wiki/Business_or_Mission_Analysis), *Guide to the Systems Engineering Body of Knowledge*, version 2.14. Consulted 2026-08-30.
7. Horst W. J. Rittel and Melvin M. Webber. “Dilemmas in a General Theory of Planning.” *Policy Sciences* 4, 155–169, 1973.
8. Peter Checkland. *Systems Thinking, Systems Practice*. John Wiley & Sons, 1999.

## Exercises

### Exercise 1

Reframe “build a dashboard for delayed freight” into an evidence-backed problem/opportunity frame. Include stakeholders, non-users, boundary, baseline, outcomes, causal hypotheses, constraints, measures, intervention classes, learning, and reframing triggers.

### Exercise 2

Diagnose these statements: “We need blockchain for trust,” “customers abandon because the form is long,” “the budget requires cloud,” “operators cause 70% of incidents,” and “average response time improved 20%.” Separate observation, hypothesis, value, constraint, uncertainty, and solution claim.

### Exercise 3

Create a causal hypothesis set for recurring deployment failure. Include at least two feedback loops, a common cause, alternative explanations, evidence that would discriminate them, containment, and longer-term intervention classes.

### Exercise 4

Design a measurement system for equitable access to a public digital service. Distinguish problem, effectiveness, performance, leading, distributional, and guardrail measures; address people absent from digital logs and metric gaming.

### Exercise 5

Frame an opportunity/problem for automated clinical appointment prioritization. Include competing stakeholder values, historical-data limitations, workflow feedback, alternative non-automation interventions, safe learning, constraints, and required external authority.

## Answers to the Exercises

### Answer 1

Situation: freight deliveries miss committed windows with a stated distribution by route, commodity, carrier, customer type, and disruption condition. Stakeholders include shippers, carriers, dispatchers, drivers, ports/terminals, customers, communities affected by staging/traffic, regulators, maintainers, and workers outside the proposed dashboard. Boundary includes booking, handoffs, customs, loading, routing, capacity, traffic/weather, communication, unloading, records, and recovery—not only internal tracking.

Hypotheses include inaccurate readiness data, batching, capacity mismatch, priority/incentives, handoff ambiguity, route disruption, missing exception authority, or measurement timestamp error. Define on-time and predictability outcomes, distributional/service consequences, safety/emissions/workload guardrails, baseline/counterfactual, and legal/contractual constraints. Compare process/authority, scheduling, data standards, alerts, staffing, contracts, physical capacity, and dashboard options. Learn through timestamp audit, observation, process trace, controlled handoff changes, and stakeholder interviews. Reframe on evidence that another stage dominates, excluded parties bear harm, demand changes, or the dashboard does not change decisions.

### Answer 2

“We need blockchain for trust” embeds a solution and leaves trust actors, threat, evidence, authority, and outcome undefined. “Customers abandon because the form is long” combines an observation—if abandonment is measured—with one causal hypothesis; content difficulty, eligibility, accessibility, identity, fear, time, device, and support are alternatives. “The budget requires cloud” is likely a preference or cost hypothesis unless an authorized budget plus evidence makes non-cloud options infeasible; cloud is not itself a budget constraint. “Operators cause 70% of incidents” needs incident denominator, causal classification method, system conditions, and uncertainty and risks blame-based boundary closure. “Average response improved 20%” lacks baseline period, population, distribution, counterfactual, outcome, tails, and guardrails.

Rewrite each as separately traceable observed evidence, interpretation/hypothesis, desired outcome/value, claimed constraint with source/authority, uncertainties, and candidate interventions. Then state what evidence could falsify or reframe each claim.

### Answer 3

Candidate mechanisms include configuration inconsistency, insufficient preproduction representativeness, dependency change, rushed review, access/tool failure, and ambiguous ownership. A schedule-pressure loop can reduce testing, increase failures/rework, and create more pressure. A noisy-failure loop can produce alerts/workarounds, lower attention and configuration discipline, and increase later failure. A common source/build/deployment service can affect test and production simultaneously. Apparent deployment faults may instead be latent application defects or observability misclassification.

Discriminating evidence includes artifact/configuration provenance, environment diff, dependency/version timeline, fault reproduction, change/review/test history, access and tool telemetry, causal incident reconstruction, and controlled rehearsal. Contain with rollback, freeze, isolation, safe deployment rate, and staffing. Longer-term classes include environment parity, configuration policy, dependency contracts, staged exposure, architecture decoupling, review/workload, testing, observability, and recovery design. Do not equate correlation with cause or containment with durable correction.

### Answer 4

Problem measures include eligible population unable to start/complete service, time and failure reasons by channel and group, unmet outcome, abandonment, assistance demand, and appeal. Effectiveness measures include timely successful receipt of the intended public outcome and equitable distribution. Performance measures include availability, latency, accessibility conformance, form error, and support capacity. Leading measures include identity/document failure, queue growth, page/channel drop-off, and translation or assistive-technology defects. Guardrails cover wrongful denial, privacy, burden, staff workload, fraud-response harm, and loss of alternate channels.

Digital logs omit people without connectivity/device/identity, those deterred before entry, assisted/offline users, and inaccessible experiences. Use population denominators, surveys/community research, service/appeal records, call/in-person observation, accessibility testing, and linked outcomes with privacy safeguards. Anticipate gaming through deflection, reclassification, easy-case priority, or narrowed denominators. Publish definitions, distributions, missingness, qualitative evidence, and independent review rather than one target average.

### Answer 5

Frame the outcome as timely, clinically appropriate, equitable appointment allocation with understandable decisions, safe escalation, patient recourse, and manageable clinical work. Stakeholders include patients across conditions/languages/disabilities/access, caregivers, schedulers, clinicians, service lines, emergency care, privacy/IT, payers where relevant, regulators, and people excluded by current access. Historical labels reflect prior capacity, policy, clinician judgment, access, inequity, and the scheduling system itself; prediction can change future demand and labels.

Hypotheses include incomplete intake, inconsistent criteria, capacity, referral quality, communication, no-shows, scheduling rules, specialty handoffs, and inequitable access. Compare policy clarification, intake redesign, staffing/capacity, navigation, reminders, reserved capacity, human decision support, and automation. Use retrospective audit only as preliminary evidence, then simulation/shadow evaluation and bounded prospective study with subgroup/clinical guardrails, human override, monitoring, stop/rollback, and recourse. Automation cannot establish clinical benefit, fairness, consent, privacy legality, regulatory sufficiency, or acceptable risk. Named clinical, patient/community, human-factors/accessibility, privacy/security, operational, ethics, legal/regulatory, and safety authorities must review applicable claims. No external clinical, regulatory, academic, or practitioner review is claimed.
