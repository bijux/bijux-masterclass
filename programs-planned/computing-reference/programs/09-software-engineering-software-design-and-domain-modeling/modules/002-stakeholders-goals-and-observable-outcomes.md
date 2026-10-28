---
module_id: SDDM-002
program: Software Engineering: Software Design & Domain Modeling
level: 1
module_number: 2
title: Stakeholders, Goals, and Observable Outcomes
status: complete
last_verified: 2026-08-29
---

# Stakeholders, Goals, and Observable Outcomes

## One-Page Review

### Governing question

Whose interests, authority, exposure, and work define success, and how can broad goals be refined into observable outcomes without mistaking delivered features or convenient proxies for real-world improvement?

### Essential definitions

- A **stakeholder** is a person, group, organization, or other party that can affect, is affected by, or has a legitimate interest in the system or its outcomes.
- An **actor** interacts with the system; a **user** operates it; a **customer/acquirer** obtains it; a **sponsor** funds or authorizes it. Each can be a stakeholder, but the roles are not synonyms.
- A **goal** is a desired condition or direction in the problem domain.
- An **outcome** is a change or preserved condition experienced or observable in the domain.
- An **output** is an artifact or service produced; an **activity** is work performed. Neither alone proves an outcome.
- A **measure** maps observations to values under a defined procedure and unit.
- A **baseline** characterizes the condition before or without the intervention.
- A **target** is an accepted desired measure value within a time horizon and population.
- A **guardrail** is a constraint or measure that must not degrade while pursuing a target.
- A **proxy** is a measurable variable used in place of the underlying construct of interest.
- An **obstacle** is a condition that can prevent a goal from being satisfied.

### Central model, mechanism, or theorem

For stakeholder group $s$, goal $G_s$, outcome variable $Y_s$, population $P_s$, observation window $T$, and intervention specification $S$, define an outcome contract:

$$
O_s=(P_s,Y_s,baseline_s,target_s,T,guardrails_s,evidence_s).
$$

An observed target does not by itself prove that $S$ caused it. Adequacy still requires domain assumptions $W$, implementation conformance, and a causal/evidential argument:

$$
W\land S\models G_s,\qquad
observe(Y_s)\text{ supports but does not alone prove }cause(S,Y_s).
$$

### Critical invariants

- Identify directly affected, indirectly affected, operating, authorizing, accountable, and marginalized stakeholders.
- Separate stakeholder role, interest, authority, evidence, and conflict; influence is not legitimacy.
- Express goals in domain conditions before selecting solution outputs.
- Give every outcome a population, unit, baseline, target, window, data source, owner, and guardrails.
- Preserve distribution: an average improvement cannot conceal severe subgroup harm.
- Validate proxies against the construct and monitor gaming or drift.
- Trace goals to outcomes, requirements, mechanisms, and evidence in both directions.
- Revisit goals when assumptions, regulation, stakeholder composition, or observed effects change.

### Common failures

Common failures include equating sponsor preference with stakeholder need, interviewing only current users, treating “ship the dashboard” as an outcome, using system uptime as a proxy for successful work, choosing metrics only because data already exists, setting a target without a baseline or denominator, averaging away subgroup harm, rewarding a proxy until it is gamed, claiming causality from before/after correlation, and recording conflicts without an accountable decision.

### Compact example

A clinic asks for “an appointment reminder feature.” Output: reminders sent. Candidate outcome: fewer preventable missed appointments among patients who consent to reminders. A defensible contract defines eligible appointments, baseline missed-appointment rate, delivery/access subgroups, observation window, target, privacy and opt-out guardrails, and data-quality limitations. It does not call a queued message a kept appointment or assume reminders caused every change.

### Connections

Retrieve [SDDM-001's problem/solution and world–machine distinction](001-distinguishing-the-problem-domain-from-the-solution-domain.md). [SDDM-003](../ROADMAP.md) develops the shared domain language needed to state goals consistently. Outcomes connect to [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md), [Data Engineering](../../19-data-engineering/ROADMAP.md), and [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

How can a team decide what “better” means when stakeholders disagree, important people never touch the software, desired conditions are only partly observable, and measurements can be distorted by the intervention itself?

Stakeholder discovery is not a meeting invitation list. Goal modeling is not copying requests into a backlog. Measurement is not selecting whatever appears on an existing dashboard. The engineering task is to make interests, authority, exposure, outcomes, assumptions, conflicts, and evidence explicit enough that a design can be challenged before outputs harden into false definitions of success.

## Why This Matters

Software redistributes capability, work, risk, information, and decision authority. A scheduling tool serves dispatchers but changes drivers' workloads. A fraud model helps investigators but can delay legitimate customers. A school portal serves teachers and parents while affecting children who cannot meaningfully consent. If the model includes only purchasers and screen users, it omits people who bear consequences.

Teams also optimize what they can see. Ticket closure time may fall because difficult tickets are split, deferred, or mislabeled. Click-through can rise while comprehension falls. Delivery frequency can increase while customer recovery time worsens. Measures influence behavior, so they must be treated as part of the designed socio-technical system.

Outcome clarity protects architecture and feedback. When “reduce time from accepted order to verified delivery” is stable, teams can compare routing, staffing, interface, and process alternatives. When “implement queue X” becomes the goal, design is frozen and external adequacy disappears from review.

## Prerequisites and Retrieval

You should understand the problem/solution distinction and adequacy argument from [SDDM-001](001-distinguishing-the-problem-domain-from-the-solution-domain.md), percentages, populations, averages, basic causal versus correlational reasoning, and ordinary software roles. Retrieve:

1. Requirements express needs and conditions, not merely stakeholder quotations.
2. A system can satisfy an internal specification while failing to improve the world.
3. Observability and controllability bound what software can know and cause.
4. A measure is an operational definition, not the underlying construct itself.
5. Evidence has a collection method, uncertainty, scope, and possible bias.

## Learning Objectives

After completing this module, you should be able to:

- distinguish stakeholder, actor, user, customer, sponsor, regulator, operator, subject, and affected non-user;
- build a stakeholder map based on interests, authority, exposure, and evidence needs;
- rewrite solution requests as problem-domain goals;
- refine goals through AND/OR relationships and identify obstacles;
- distinguish activities, outputs, product behavior, outcomes, and impacts;
- write an outcome contract with baseline, target, population, window, data source, and guardrails;
- identify proxy failure, denominator errors, gaming, survivorship bias, and distributional harm;
- choose evidence appropriate to causal and non-causal claims;
- reconcile conflicting goals through explicit authority and decision records;
- trace stakeholder goals to design and operational evidence.

## Core Exposition

### Discover stakeholders by relationship, not visibility

Begin at the problem boundary. Ask who supplies information, performs work, receives benefits, bears cost or risk, owns affected resources, authorizes decisions, enforces rules, operates and supports the intervention, audits it, can block it, and is represented only indirectly. Include future users and people excluded by current access patterns.

Record roles rather than compressing a person into one label. A nurse may be operator, domain expert, safety barrier, and affected employee. A patient may be subject of data and beneficiary without touching the application. A regulator has legitimate authority but does not define every usability goal. A sponsor can set budget scope but cannot waive law or manufacture evidence about lived work.

A useful stakeholder record contains:

- group and context boundary;
- roles and responsibilities;
- goals, concerns, rights, and unacceptable outcomes;
- degree and kind of impact, including reversibility;
- decision authority and its source;
- domain knowledge and evidence held;
- access, language, disability, safety, or representation needs;
- conflicts and dependencies with other groups;
- contact/representative and review cadence.

Power–interest grids help plan communication but are ethically incomplete: low-power/high-impact groups deserve stronger representation, not less attention. Add exposure and rights. For contested groups, document how representatives were selected and what evidence remains missing.

### Elicit goals rather than transcribe features

A stakeholder statement is an input claim. Ask what condition would be improved, for whom, under what circumstances, why it matters, how current work behaves, what must never happen, and what evidence would change the belief. “We need an export button” may conceal goals of regulatory submission, offline analysis, portability, or avoidance of vendor dependence. These support different designs and guardrails.

Goals range from strategic (“reduce preventable harm”) through operational (“clinicians see verified allergies before prescribing”) to system-facing requirements (“present current allergy status at medication ordering”). Preserve refinement links. A child goal contributes to its parent; it is not automatically sufficient.

AND-refinement means all subgoals are required. OR-refinement identifies alternatives, any acceptable combination of which can satisfy the parent under conditions. Operationalization connects a goal to assigned behavior or policy. Obstacles challenge refinements: unavailable data, conflicting incentives, access barriers, delays, malicious action, or physical limits.

Avoid circular goals. “Users adopt the portal” is not evidence the portal provides value when adoption is mandatory. “Improve engagement” is too ambiguous until the desired behavior and benefit are distinguished from interface activity.

### Separate activities, outputs, outcomes, and impacts

An **activity** is work: interview users, migrate records, train operators. An **output** is produced: a report, API, reminder, trained cohort. Product behavior is what the machine does at its boundary. An **outcome** is a near- or medium-term domain condition: fewer duplicate entries, quicker verified decisions, more successful task completion. **Impact** is a broader long-term effect: reduced harm, cost, or inequality.

The layers form a causal hypothesis:

$$
activities\rightarrow outputs\rightarrow use/behavior\rightarrow outcomes\rightarrow impacts.
$$

Every arrow needs evidence or an assumption. Shipping does not imply use; use does not imply correct use; correct use does not guarantee outcome; outcome correlation does not establish net impact. This model does not demean delivery metrics. It bounds what each metric proves.

### Write observable outcome contracts

A robust outcome statement names:

1. **population:** eligible people, cases, events, or systems;
2. **construct:** the domain condition of interest;
3. **operational measure:** numerator, denominator, unit, aggregation, and exclusions;
4. **baseline/comparator:** current, historical, control, benchmark, or threshold;
5. **target and direction:** magnitude and acceptable range;
6. **window:** observation and reporting periods, including seasonality;
7. **data source and quality:** provenance, missingness, latency, and collection effects;
8. **guardrails:** harms or qualities that must not worsen;
9. **owner and decision:** who acts when the measure changes;
10. **evidence strength:** descriptive, comparative, experimental, or causal claim.

“Cut processing time 20%” lacks event boundaries, population, baseline statistic, tail behavior, and quality guardrails. Prefer: “For complete standard applications received during the quarter, reduce median elapsed time from validated receipt to communicated decision from the trailing-six-month baseline of 10 days to at most 8 days, while 95th percentile stays below 20 days and verified decision-reversal and subgroup disparity rates do not increase.” It still needs operational definitions.

### Choose measures from questions

The Goal–Question–Metric pattern begins with a goal in context, derives questions whose answers determine satisfaction, then selects measures. This direction prevents dashboards from defining the mission. For a goal of reliable medication reconciliation, questions include completeness, timeliness, disagreement resolution, and affected workflows; each may need several measures.

Measures can be direct or proxy, leading or lagging, quantitative or qualitative. A leading indicator responds sooner but may be weakly connected to outcome. A lagging indicator is closer to impact but arrives late. Combine them into a causal/evidence portfolio rather than one composite score that hides trade-offs.

Every rate needs a denominator. “Errors fell from 40 to 20” is meaningless if processed cases changed from 100 to 10. Averages need distributions: median can improve while tail and subgroup outcomes worsen. Report uncertainty and sample size when inference is intended.

### Control proxy and gaming risk

A proxy is useful when the desired construct is latent, delayed, expensive, or partly unobservable. Validate its relationship under the actual context. Once rewards attach to it, participants adapt. The relationship can decay—an instance of the broader warning commonly associated with Goodhart's law.

Review how the measure can be improved without improving the goal: excluding cases, changing labels, discouraging demand, delaying admission to the denominator, shifting harm to another group, or optimizing short-term behavior. Add guardrails, audits, qualitative evidence, and periodic proxy revalidation. Do not punish operators for revealing bad outcomes.

### Address conflict and authority

Stakeholder goals conflict legitimately: customers want speed, compliance wants review, operators want manageable workload, finance wants cost control, affected communities want equitable access. Do not “average” incomparable rights and risks.

Classify constraints: law, contract, safety obligation, policy, budget, preference, or hypothesis. Identify the decision authority and escalation path. Record alternatives, evidence, rejected impacts, dissent, review date, and reversal conditions. A transparent decision can still be wrong, but hidden conflict cannot be governed.

Use non-negotiable guardrails for rights, safety, security, and legal constraints when appropriate. Optimize only within the admissible region. When no acceptable trade exists, change scope or decline the intervention.

### Treat observation as intervention

Instrumentation changes systems: additional data collection affects privacy, workload, latency, and behavior. Define lawful purpose, minimization, retention, access, deletion, and audit. Do not collect sensitive attributes casually; do not claim equity without the data or valid method needed to examine it. Sometimes privacy-preserving sampling or independent audit is preferable to continuous person-level tracking.

Missingness is rarely random. People without connectivity, rejected applicants, abandoned tasks, and non-users may disappear from telemetry precisely because the system failed them. Combine logs with observation, interviews, surveys, case review, and complaint analysis, recognizing each method's limits.

### Separate observation from causation

If outcome $Y$ improved after release $S$, other changes, selection, regression to the mean, seasonality, learning, or measurement drift may explain it. A causal claim asks what would have happened to the same population without $S$—a counterfactual that cannot be directly observed.

Randomized experiments can estimate effects when ethical, feasible, correctly powered, and analyzed. Quasi-experiments, phased rollout, matched comparisons, interrupted time series, and triangulation offer other evidence with assumptions. For safety or rights, withholding an established protection may be unacceptable. State the design and limitations rather than declaring “data-driven proof.”

### Maintain traceability and learning

Trace stakeholder evidence to goal, goal to outcome, outcome to requirement and design mechanism, mechanism to verification, and outcome to production observation. Reverse trace removes orphan features and metrics. Version every link; stakeholder composition and goals change.

Use review triggers: target reached, guardrail breached, proxy relationship weakened, law changed, affected group identified, data source drifted, or intervention retired. An outcome model is a learning instrument, not a permanent scorecard.

The following model evaluates one explicitly bounded rate target and two guardrails from aggregated observations. It demonstrates denominator and subgroup checks. It does not establish measurement validity, causality, representativeness, consent, or stakeholder legitimacy.

<!-- bijux-verify: {"id":"outcome-contract-evaluator","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"overall=0.850 target_pass=True\nnorth=0.900 south=0.800 gap=0.100 equity_pass=False\ncomplaints=4 complaint_pass=True\ncontract_pass=False\n","stderr":""}} -->
```python
groups = {
    "north": {"eligible": 100, "completed": 90},
    "south": {"eligible": 100, "completed": 80},
}
target_rate = 0.84
maximum_group_gap = 0.05
maximum_complaints = 5
complaints = 4

eligible = sum(group["eligible"] for group in groups.values())
completed = sum(group["completed"] for group in groups.values())
overall = completed / eligible
rates = {
    name: group["completed"] / group["eligible"]
    for name, group in groups.items()
}
gap = max(rates.values()) - min(rates.values())

target_pass = overall >= target_rate
equity_pass = gap <= maximum_group_gap
complaint_pass = complaints <= maximum_complaints
contract_pass = target_pass and equity_pass and complaint_pass

print(f"overall={overall:.3f} target_pass={target_pass}")
print(
    f"north={rates['north']:.3f} south={rates['south']:.3f} "
    f"gap={gap:.3f} equity_pass={equity_pass}"
)
print(f"complaints={complaints} complaint_pass={complaint_pass}")
print(f"contract_pass={contract_pass}")
```

## Definitions and Notation

Let $S=\{s_1,\ldots,s_n\}$ be stakeholder groups. For each $s$:

- $G_s$: desired domain condition;
- $A_s$: legitimate authority and its source;
- $X_s$: exposure to benefit, cost, or harm;
- $Y_s$: operational outcome variable;
- $P_s$: eligible population;
- $T_s$: observation window;
- $H_s$: guardrail predicates.

For binary outcome $y_i$ over eligible observations $P$, rate

$$
\hat p=\frac{\sum_{i\in P}y_i}{|P|},
$$

provided $P$ and exclusions are defined. For groups $g$, a simple disparity measure is $\Delta=\max_g\hat p_g-\min_g\hat p_g$. This difference is descriptive and does not by itself identify unfairness or cause.

A goal graph uses $G\leftarrow AND(G_1,\ldots,G_k)$ when every child is required and $G\leftarrow OR(G_1,\ldots,G_k)$ for accepted alternatives under stated conditions. An obstacle $O$ obstructs $G$ when $O$ can make the refinement insufficient.

## Mechanisms, Invariants, or Proof Structure

**Completeness mechanism.** Traverse every boundary phenomenon and ask who controls, observes, experiences, owns, regulates, supports, or can be harmed. Compare with stakeholder records; unexplained roles are discovery gaps.

**Goal-refinement invariant.** Child goals jointly or alternatively contribute to the parent under explicit assumptions. Feature delivery cannot substitute for the parent outcome without the causal link.

**Outcome-contract invariant.** A computed value is uninterpretable without population, unit, time, collection method, exclusions, and decision rule. Every target has at least one harm/quality guardrail.

**Distribution invariant.** Aggregate acceptance implies nothing about every subgroup. Review predeclared relevant distributions and intersectional limitations without manufacturing conclusions from inadequate samples.

**Causal-evidence invariant.** Descriptive observations support only descriptive claims unless a design and assumptions justify stronger inference.

**Traceability invariant.** Every design feature serves an accepted goal/outcome or a named constraint; every accepted outcome has mechanisms, verification, and operational evidence or is explicitly unmeasured with a mitigation.

## Alternatives and Trade-Offs

**Broad participation versus decision speed.** More perspectives reveal hidden impacts but consume time and can create performative consultation. Match depth to exposure and irreversibility; close the feedback loop by showing how input affected decisions.

**Quantitative versus qualitative evidence.** Quantitative measures compare scale and trends. Qualitative methods reveal meaning, mechanisms, and unseen outcomes. Strong discovery uses both rather than ranking one as inherently rigorous.

**Direct outcomes versus proxies.** Direct measures improve construct validity but may be delayed, invasive, or costly. Proxies provide timely feedback but require validation and gaming controls.

**One target versus outcome portfolio.** One metric focuses effort and is easy to govern; it invites tunnel vision. A small target/guardrail portfolio preserves trade-offs without creating an unactionable dashboard.

**Universal versus segmented outcomes.** Universal outcomes simplify communication. Segmentation reveals unequal effects but increases privacy, statistical, and governance burden. Collect only justified attributes with appropriate protections.

**Experiment versus observational rollout.** Randomization strengthens causal inference but may be unethical or operationally infeasible. Observational designs require stronger assumptions and humility. Safety constraints override experimental convenience.

## Failure Modes and Misconceptions

1. **Stakeholders are everyone.** Boundaries and relationships must be explicit or prioritization becomes meaningless.
2. **Users represent all affected people.** Non-users can bear data, labor, safety, environmental, or exclusion effects.
3. **Sponsors own truth.** They hold authority in a scope; domain facts require evidence.
4. **Goals are features written as verbs.** “Deploy portal” is an output unless the desired condition is portal existence itself.
5. **Observable means easy to log.** Valid outcomes may require research; easy telemetry can be a weak proxy.
6. **A target without a denominator is measurable.** Counts cannot establish rates or exposure.
7. **The average customer improved.** No such person may exist; distributions can move in opposite directions.
8. **Meeting the target proves causation.** It proves only the defined observation met its rule.
9. **More metrics prevent gaming.** They can create more games and obscure accountability.
10. **Stakeholder analysis finishes before design.** New mechanisms reveal stakeholders, impacts, and conflicts that must update the model.

## Worked Examples

### Example 1

**Question:** Who are stakeholders in warehouse route optimization besides the picker using the device?

**Reasoning:** Include pickers, supervisors, safety representatives, inventory owners, maintenance, fulfillment customers, accessibility representatives, labor authorities, and people working near changed vehicle routes. Record impact and authority separately.

**Conclusion:** Interface users are one subset of the socio-technical boundary.

### Example 2

**Question:** Rewrite “launch a customer analytics dashboard” as a goal.

**Reasoning:** Ask which decisions fail today. Suppose account managers cannot identify contracts at renewal risk early enough for a verified intervention. The goal is timely, justified recognition and response; dashboard, alerts, or workflow changes are alternatives.

**Conclusion:** Preserve the requested dashboard as a candidate output, not the definition of success.

### Example 3

**Question:** Is “10,000 reminders sent” an outcome?

**Reasoning:** It is an output count. Useful outcomes might be timely awareness, completed action, or reduced preventable misses among eligible recipients, constrained by consent, delivery, accessibility, and burden.

**Conclusion:** Outputs support but do not establish domain change.

### Example 4

**Question:** An overall completion rate rises from 80% to 85%, while group A rises to 92% and group B falls to 70%. Did the outcome contract pass?

**Reasoning:** The aggregate target might pass, but a predeclared non-degradation or disparity guardrail fails. Report denominators and uncertainty before interpreting the groups.

**Conclusion:** Distributional guardrails prevent averages from hiding harm.

### Example 5

**Question:** Ticket resolution time falls after agents begin closing tickets awaiting customer replies.

**Reasoning:** The proxy improved through classification rather than completed resolution. Track reopen rate, customer-confirmed resolution, age of pending work, complaints, and qualitative cases; revise incentives.

**Conclusion:** A gamed proxy must not define the goal.

### Example 6

**Question:** Refine “customers receive accurate decisions promptly.”

**Reasoning:** AND-refine into decision correctness under policy, communicated reason, bounded elapsed time, accessible delivery, and correction path. Obstacles include incomplete data, appeal backlog, delivery failure, and policy ambiguity.

**Conclusion:** Refinement exposes mechanisms and guardrails hidden by a soft goal.

### Example 7

**Question:** Revenue rose after a recommendation release. Can the team claim impact?

**Reasoning:** Seasonality, pricing, marketing, selection, and measurement changes are alternatives. Use rollout comparisons or another justified design, predeclare outcomes, inspect guardrails, and state remaining assumptions.

**Conclusion:** Temporal sequence plus correlation is not causal attribution.

### Example 8

**Question:** A regulator, sponsor, operator, and affected community disagree on identity verification.

**Reasoning:** Separate legal minimum, budget authority, operational burden, exclusion risk, fraud goal, and evidence. Generate alternatives within law and rights guardrails; record authority, dissent, review triggers, and exception/appeal paths.

**Conclusion:** Conflict requires governance, not majority averaging.

### Example 9

**Question:** A hospital triage system meets its wait-time target. Is it clinically successful?

**Reasoning:** Wait time may improve while acuity errors, subgroup harm, staff overload, or adverse outcomes worsen. The code example's kind of rate check cannot validate clinical constructs or causality. No external academic, clinical, regulatory, or practitioner review is claimed. Named qualified humans must review goals, clinical definitions, data, safety guardrails, causal evidence, workflow, hazards, and applicable assurance.

**Conclusion:** A passing metric contract is bounded evidence, not clinical approval.

### Example 10

**Question:** When should an outcome measure be retired?

**Reasoning:** Retire or redesign it when the goal changes, collection becomes disproportionate, the proxy loses validity, gaming dominates, the intervention ends, or no accountable decision depends on it. Preserve required audit history under retention policy.

**Conclusion:** Measurement has a lifecycle and should not become ambient surveillance.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) allocates outcome-supporting responsibilities across system boundaries.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) verifies mechanisms and designs evidence for observable claims.
- [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) connects release changes to operational measures and guardrails.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) owns measurement provenance, quality, lineage, and late data.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) identifies affected parties, abuse goals, rights, and non-negotiable constraints.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) integrates stakeholder needs, mission analysis, trade studies, and validation.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018, Requirements Engineering](https://www.iso.org/standard/72089.html), especially business/mission analysis and stakeholder needs and requirements definition. Consulted 2026-08-29.
2. ISO. [ISO/IEC 25010:2023, Product Quality Model](https://www.iso.org/standard/78176.html), edition 2, November 2023. Consulted 2026-08-29.
3. IEEE Computer Society. [Guide to the Software Engineering Body of Knowledge, requirements topics](https://www.computer.org/education/bodies-of-knowledge/software-engineering/topics), SWEBOK v4.0a. Consulted 2026-08-29.
4. van Lamsweerde, Axel. *Requirements Engineering: From System Goals to UML Models to Software Specifications*. Wiley, 2009.
5. Basili, Victor R. [Software Modeling and Measurement: The Goal/Question/Metric Paradigm](https://drum.lib.umd.edu/items/8119803a-362b-42ec-b6ce-2311713e7236). University of Maryland Technical Report CS-TR-2956, 1992.
6. Jackson, Michael. “The World and the Machine.” *ICSE-17*, 1995. [DOI: 10.1145/225014.225041](https://doi.org/10.1145/225014.225041).
7. Friedman, Batya, David G. Hendry, and Alan Borning. “A Survey of Value Sensitive Design Methods.” *Foundations and Trends in Human–Computer Interaction* 11(2), 2017. [DOI: 10.1561/1100000015](https://doi.org/10.1561/1100000015).

## Exercises

### Exercise 1

For a public-benefits application service, identify at least six stakeholder roles and distinguish authority from exposure.

### Exercise 2

Refine “make incident response better” into an AND/OR goal structure with at least two obstacles.

### Exercise 3

Diagnose this metric: “The chatbot resolved 80% of conversations.” State missing definitions, likely proxy failures, and guardrails.

### Exercise 4

Write an outcome contract for reducing failed package deliveries, including population, baseline, target, window, data, subgroup view, and guardrails. State what evidence would support causality.

### Exercise 5

Design stakeholder and outcome review for an automated railway maintenance-priority system. Separate automated checks from named human review and decision authority.

## Answers to the Exercises

### Answer 1

Roles include applicants/beneficiaries, case workers, eligibility-policy owners, appeals officers, identity/data providers, accessibility and language representatives, privacy/security officers, treasury, auditors, and people wrongly excluded before application. Statutory bodies own policy authority; budget sponsors authorize funding; case workers have operational expertise; applicants experience delays and denial; appeals bodies correct decisions. High exposure creates a representation obligation even without organizational power. A complete answer records rights, evidence, conflicts, representative selection, and people absent from current telemetry.

### Answer 2

Parent goal: incidents are contained and service restored with bounded harm. AND-children: timely validated detection; correct severity/context; authorized coordination; safe containment; verified restoration; stakeholder communication; evidence-preserving learning. OR-alternatives for coordination might be dedicated incident command or role-based rotation under equivalent capability conditions. Obstacles include alert floods that hide causal signals and containment actions that destroy forensic evidence or worsen availability. Outcomes require time boundaries and correctness/recurrence guardrails, not only shorter closure time.

### Answer 3

Define conversation eligibility, when a conversation starts/ends, what “resolved” means, who confirms it, transfers/reopens, repeat contacts, abandoned sessions, language/access groups, and denominator exclusions. The bot can improve the proxy by prematurely closing, discouraging users, misclassifying transfers, or preventing escalation. Guardrails include user-confirmed resolution, repeat-contact and escalation rates, complaint/severity review, accessibility, erroneous advice, time to human help, and subgroup outcomes. An 80% internal label rate is an output classification until validated against the desired construct.

### Answer 4

Example: for first-attempt residential deliveries in selected regions during the next full quarter, reduce verified failed-delivery rate from the prior comparable year's 8.0% to at most 6.5%. Numerator is packages not delivered on the first scheduled attempt; denominator is eligible attempts, with explicit exclusions for customer cancellation and force majeure. Use scan plus customer-confirmation provenance, report missing/late events, segment by region, dwelling/access needs, and carrier. Guardrails: loss/damage, unsafe driving, worker overtime, customer complaints, and redelivery emissions must not worsen beyond accepted bounds.

Causal support could come from randomized or phased assignment of a routing/notification intervention, with predeclared analysis and spillover checks. If infeasible, use a justified matched or interrupted time-series design, test seasonality and concurrent changes, and state residual uncertainty.

### Answer 5

Stakeholders include maintainers, train operators, infrastructure owner, passengers, nearby communities, safety authority, labor representatives, suppliers, incident investigators, and teams owning sensor/data feeds. Automation verifies schema and lineage, completeness/latency, deterministic prioritization, policy constraints, threshold boundaries, subgroup/region distributions, false-negative review samples, explanation trace, override/audit behavior, access controls, rollback, and target/guardrail calculations.

Automation cannot establish that priorities reflect degradation physics, maintenance capability, acceptable risk, worker safety, community impact, or regulatory duties. No external academic, railway, regulatory, or practitioner review is claimed. Named qualified humans must approve hazard definitions, stakeholder representation, model assumptions, data fitness, trade-offs, safety case, operational procedure, override authority, monitoring, and applicable railway assurance. Statutory safety authority and accountable infrastructure leadership retain their respective decisions; a sponsor or model score cannot replace them.
