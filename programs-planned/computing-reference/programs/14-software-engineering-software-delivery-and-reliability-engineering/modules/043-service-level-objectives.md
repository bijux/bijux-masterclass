---
module_id: SDRE-043
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 43
title: Service-Level Objectives
status: complete
last_verified: 2026-09-06
---

# Service-Level Objectives

## One-Page Review

### Governing question

How can a team set a service-level objective that represents user need, is measurable and achievable under normal conditions, governs real decisions, and can evolve without rewriting history or pretending that perfection is free?

### Essential definitions

- a **service-level objective (SLO)** is a target value or range for a specified service-level indicator over a specified evaluation window;
- an **objective predicate** compares the measured SLI with a target, such as $S_W\ge\theta$;
- an **evaluation window** selects the observations whose aggregate is judged;
- a **rolling window** ends at the evaluation time and continuously advances;
- a **calendar-aligned window** has fixed civil-time boundaries such as a month or quarter;
- a **committed SLO** governs current operational decisions;
- an **aspirational SLO** is tracked as a desired future level without triggering the committed policy;
- an **internal objective** coordinates producers and consumers inside an organization;
- an **external expectation** is communicated to users but is not automatically a legal agreement;
- a **reliability frontier** is the feasible trade-off among reliability, latency, functionality, cost, and delivery speed;
- **attainability** means the target can normally be met with the declared design, capacity, dependencies, and operating practice;
- **coverage** means the chosen SLO set captures important user-visible failure modes;
- an **SLO specification** binds a versioned SLI, target, comparison operator, window, scope, owner, decision policy, evidence, and review process.

### Central model, mechanism, or theorem

For a versioned SLI $S$ evaluated over window $W$ and target $\theta$, a lower-bound SLO is met exactly when

$$
S_W\ge\theta.
$$

The expression is meaningful only if the SLI population, predicate, measurement point, exclusions, missing-data policy, and window are fixed. Target selection is a product-risk decision constrained by user harm and feasible operation—not a number inferred mechanically from current performance.

### Critical invariants

- bind every target to one versioned SLI and one window;
- start from a user journey and consequence, not a fashionable number of nines;
- distinguish committed, aspirational, internal, external, and contractual promises;
- require stakeholder ownership and a predeclared decision policy;
- avoid 100% unless the population and consequence genuinely justify it;
- test attainability under normal load, maintenance, release, and dependency behavior;
- use a small set with complementary coverage;
- preserve cohort harm instead of hiding it in a global aggregate;
- version material changes and keep historical evaluations reproducible;
- review false reassurance, false alarms, user evidence, and changed service context.

### Common failures

Failures include copying a vendor target, choosing the current average, demanding 100%, omitting the window, mixing incompatible SLI versions, treating a rolling and calendar result as equal, setting dozens of objectives, selecting internal resource metrics, accepting an unreachable target as permanent emergency, using a lax target that ignores user harm, hiding dependency assumptions, averaging cohorts, changing exclusions retroactively, confusing an SLO with an SLA, and tracking a number that never changes a decision.

### Compact example

A checkout team specifies: “For the versioned `checkout-correct-within-800ms` SLI, at least 99.5% of eligible client-observed logical operations in each rolling 28-day window must be good.” The team shows that the target captures support-ticket and abandonment spikes, can be met during normal releases and one dependency-zone loss, and has named owners and response policy. A tighter 99.9% target is tracked as aspirational while redesign proceeds. The specification does not promise legal remedy; that belongs to any separate agreement.

### Connections

[SDRE-042](042-service-level-indicators.md) supplies the measurement contract. [SDRE-044](../ROADMAP.md) next distinguishes negotiated service-level agreements; [SDRE-045](../ROADMAP.md) derives the tolerance implied by a committed objective.

## Governing Question

An SLI can measure a user journey precisely and still leave the team unable to decide whether service is good enough. An objective supplies the normative boundary. But a target is powerful: it can direct engineering time, constrain releases, shape user architecture, and create permanent emergency if set carelessly.

The governing question is not “which percentage looks professional?” It is how to turn user consequences, evidence, technical feasibility, and organizational commitments into a target that participants understand and actually use. This requires more than a query and more than an availability percentage.

## Why This Matters

Google's SRE text defines an SLO as a target value or range measured by an SLI and warns that target choice has product and business consequences [1]. It recommends beginning with what users care about, avoiding unexamined adoption of current performance, and using objectives as inputs to a control loop [1]. The SRE Workbook makes adoption conditions explicit: stakeholders approve the SLO, responsible teams agree it is normally achievable, the organization commits to a decision policy, and a refinement process exists [2].

Window choice changes the operational meaning. The workbook contrasts rolling windows, which stay close to recent user experience, with calendar-aligned windows, which fit business planning but reset at boundaries [2]. It also treats an aspirational SLO as a separately labeled target that can guide improvement without keeping the team permanently under the current policy [2].

An SLO is not automatically an SLA. The first SRE book separates an objective from an agreement with consequences [1]; SDRE-044 develops that distinction. Current OpenSLO v1 models an SLO with an indicator, objective threshold, budgeting method, and rolling or calendar-aligned time window, while its repository labels v2 work as in progress [3]. That specification is useful for portability, but a schema cannot decide what users need or which consequences an organization will honor.

## Prerequisites and Retrieval

Retrieve service contract, stakeholder, user journey, SLI, target, threshold, inequality, evaluation window, rolling window, calendar window, cohort, coverage, reliability, latency, correctness, freshness, dependency, capacity, risk, trade-off, version, evidence, policy, and agreement.

From SDRE-041 retrieve property boundaries and feasible failure models. From SDRE-042 retrieve intended population, good-event predicate, measurement point, missingness, coverage, weighting, and proxy gaps. From SDRE-038 retrieve actionable response. Keep legal remedies for SDRE-044 and detailed error-budget calculations for SDRE-045.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish an SLO from an SLI, SLA, KPI, alert threshold, and capacity limit;
2. write a complete objective predicate over a versioned indicator and window;
3. derive candidate targets from user consequences and empirical evidence;
4. test target attainability under declared operating conditions;
5. choose between rolling and calendar-aligned evaluation windows;
6. design a small complementary objective set without double counting meaning;
7. separate committed, aspirational, internal, and external objectives;
8. analyze cohorts, dependencies, and conflicting stakeholder needs;
9. govern revisions without retroactively changing historical evaluations;
10. review whether an objective causes proportionate, useful decisions.

## Core Exposition

**Define the decision before the number.** Name what changes when the objective is met, threatened, or missed. Possibilities include pausing risky releases, prioritizing reliability work, engaging a dependency owner, adjusting capacity, or revisiting product expectations. Detailed budget policy arrives in SDRE-045, but an SLO with no decision consequence is merely a report.

Identify owners on both sides of the expectation. A service team controls mechanisms; a product owner represents user value; consumers understand dependency consequences; support, security, compliance, and finance may reveal distinct harms. Approval does not require universal preference, but it requires a recorded decision authority and dissent or uncertainty where material.

**Bind the objective to an SLI specification.** Write the indicator ID and version, population, measurement point, good predicate, exclusions, missing-data policy, and cohort scope. Then write operator, target, and evaluation window. “99.9% available” is incomplete. “At least 99.9% of eligible client-observed read operations return the authorized version within 400 ms in each rolling 28-day window” is testable, provided the linked SLI defines every term.

An SLO can also be an upper bound or range. Error rate may require $E_W\le0.1\%$; latency may use a threshold ratio; throughput quality may require $L\le S_W\le U$. The comparison direction and inclusivity at equality must be explicit.

**Start with user consequences.** Identify the point at which delay, failure, staleness, or incorrectness changes user behavior or causes harm. Evidence may include task abandonment, support cases, incident reports, customer interviews, workflow deadlines, dependency design requirements, safety analysis, and regulatory obligations. Correlation is not automatic causation, and absence of complaints is weak evidence when users silently leave.

Translate the consequence into candidate SLI thresholds and target percentages. A latency deadline of 800 ms may come from workflow tolerance; the target percentage says how broadly that experience must hold. Multiple latency grades can distinguish typical and tail experience, such as 95% under 300 ms and 99.5% under 800 ms, but each extra objective needs a distinct decision purpose.

**Assess feasibility without worshiping current performance.** Historical SLI distributions reveal failure modes, seasonality, traffic mix, maintenance, deployments, and dependency behavior. They do not dictate the objective. Setting the target just below the present value can institutionalize avoidable harm; setting it above feasible design creates chronic breach.

Model the service path. Identify component dependencies, shared failure domains, capacity limits, repair behavior, release risk, staffing, and maintenance. Estimate whether the target can normally be met, then validate with fault tests, load tests, recovery exercises, and observed operations. State uncertainty and confidence limits where statistical inference is used.

An objective may intentionally exceed current capability when labeled aspirational. Keep the current committed target and its policy active while tracking progress toward the desired future target. Do not describe an unreachable committed target as motivational: it removes the distinction between ordinary and exceptional conditions.

**Avoid automatic 100%.** Perfection allows no classified bad events in the evaluation population. Real systems have finite components, changes, dependencies, and measurement error. A 100% objective can prohibit learning and releases while still failing to guarantee correctness outside the SLI. If a safety- or integrity-critical obligation genuinely permits no bad events, define the hazard-specific contract, defense layers, and escalation; do not infer that one aggregate percentage proves safety.

**Choose the evaluation window deliberately.** A rolling window of duration $D$ evaluates observations in $(t-D,t]$ at time $t$. It changes continuously and does not forgive an outage at a month boundary. It also means one incident influences every overlapping evaluation until it ages out.

A calendar window has fixed boundaries in a declared timezone, such as a UTC month. It aligns with invoices, reports, or planning and creates boundary effects: identical incidents on the last and first day fall in different windows. Civil-time windows must specify timezone and daylight-saving behavior; fixed-duration UTC windows avoid some ambiguity.

Short windows react quickly but have fewer events and greater variance. Long windows stabilize rare-event estimates and support strategic investment but respond slowly. Use a primary window tied to decision cadence and supplementary short summaries for diagnosis. Do not silently apply a long-window target to a five-minute alert; alert design is a separate prediction and response problem.

**Keep the objective set small and complementary.** A serving system might need correct availability plus two latency grades. A data pipeline might need completeness, freshness, and correctness. A storage service might need read availability and acknowledged-state durability. Select objectives that cover distinct user harms; internal saturation, queue depth, and replica lag remain diagnostic indicators unless users value them directly.

Map known incidents and support cases to the proposed objectives. If serious incidents do not move any objective, coverage is weak. If minor internal changes breach several objectives without user impact, predicates or targets may be too sensitive. This comparison evaluates the objective system, not merely individual numbers.

**Protect cohorts.** A global event-weighted objective can pass while a small region or accessibility client fails completely. Define separate objectives for cohorts with distinct contracts or high consequences. Avoid an objective per customer unless the service model truly promises that granularity; otherwise use bounded tiers and diagnostic drill-down.

Do not average cohort percentages to create a global objective without declaring equal cohort weights. Keep global counts and cohort-specific evaluations. A composite score can hide which property failed and create trade-offs that users never accepted—for example, excellent latency cannot compensate for incorrect results.

**Model dependencies as assumptions, not excuses.** The user's experience includes dependency failures. A service cannot usually exclude all upstream or downstream faults and still claim an end-to-end objective. Internal objectives can allocate stricter expectations to dependencies, include safety margin, and make ownership explicit. If the service target is tighter than a critical dependency's real behavior, the design needs caching, redundancy, degradation, retries, or a changed promise.

**Separate audiences and commitment types.** A committed internal SLO coordinates action. An aspirational objective tracks desired improvement. An external published objective shapes user expectations. An SLA adds negotiated scope, remedies, and legal language. These can use the same SLI while having different targets or consequences, but the names and relationships must be explicit.

The following controlled evaluator demonstrates rolling-window comparison and equality semantics. It assumes complete daily good and valid counts; it is not an alert, budget policy, or statistical forecast.

<!-- bijux-verify: {"id":"evaluate-rolling-slo","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"window=7d good=6970 valid=7000 sli=99.5714%\ntarget=99.5000% met=True margin=5 events\nnext-day sli=99.4286% met=False\n","stderr":""}} -->
```python
days = [
    (995, 1000), (998, 1000), (997, 1000), (996, 1000),
    (994, 1000), (992, 1000), (998, 1000),
]
target = 0.995
good = sum(g for g, _ in days)
valid = sum(v for _, v in days)
sli = good / valid
required_good = target * valid
print(f"window=7d good={good} valid={valid} sli={sli:.4%}")
print(f"target={target:.4%} met={sli >= target} margin={good-required_good:.0f} events")

next_window = days[1:] + [(985, 1000)]
next_sli = sum(g for g, _ in next_window) / sum(v for _, v in next_window)
print(f"next-day sli={next_sli:.4%} met={next_sli >= target}")
```

**Specify change governance.** Version target, SLI reference, scope, and window. Record rationale, evidence, owners, effective date, review date, decision policy, and migration. Evaluate old and proposed definitions in parallel over historical and live data. Explain how known incidents, false positives, and false negatives change.

Never retroactively edit the definition used for a past evaluation. If a measurement defect is corrected, preserve the original report, publish the corrected result with provenance, and state the impact. If user needs or service architecture change, create a new version with a prospective effective date.

**Review continuously but not opportunistically.** Review after material product changes, user research, incidents that escape coverage, persistent false alarms, dependency changes, and planned intervals. Tightening can be justified when users need more and the design can deliver it. Relaxing can be justified when the former target produces cost or operational behavior disproportionate to user value. Neither direction is inherently virtuous.

A complete review asks: does the SLI still represent the journey, does the target distinguish meaningful harm, is the objective normally attainable, do cohorts remain protected, are dependencies feasible, and did the policy lead to proportionate action? Record uncertainty and the next evidence needed.

## Definitions and Notation

Let $S^{(v)}_W$ be version $v$ of an SLI evaluated over window $W$. A lower-bound SLO with target $\theta\in[0,1]$ is the predicate

$$
M(W)=\mathbf{1}\{S^{(v)}_W\ge\theta\}.
$$

For good and valid event counts $g_W$ and $n_W>0$, $S_W=g_W/n_W$. The minimum good count satisfying the target is

$$
g_{\min}=\lceil\theta n_W\rceil.
$$

The event margin is $m=g_W-g_{\min}$. A nonnegative margin means the objective is currently met for that completed window; it does not forecast the remainder of an open calendar window.

For rolling duration $D>0$ evaluated at time $t$, $W_R(t)=(t-D,t]$. For calendar index $k$, $W_C(k)=[b_k,b_{k+1})$ with declared boundaries and timezone. These window families answer different operational questions.

For objectives $j=1,\ldots,r$, a strict conjunction is met only when $\bigwedge_j M_j(W)=1$. A weighted composite $\sum_jw_jS_j$ is meaningful only when scales, direction, weights, and substitutability are justified; otherwise it can conceal unacceptable failure.

## Mechanisms, Invariants, or Proof Structure

**Binding argument.** A target without an SLI version cannot be reproduced because changes to population or goodness can change $S_W$ while service behavior remains constant. Therefore target, SLI version, and effective interval form one governed object.

**Minimum-count derivation.** The inequality $g_W/n_W\ge\theta$ with $n_W>0$ implies $g_W\ge\theta n_W$. Since $g_W$ is integral, the least satisfying count is $\lceil\theta n_W\rceil$. This exposes small-population granularity hidden by rounded percentages.

**Rolling-overlap argument.** An event at time $x$ belongs to every rolling window ending at $t$ where $x\le t<x+D$. One incident can therefore affect evaluations for nearly $D$ after it occurs. Repeated overlapping misses are not independent incidents.

**Calendar-boundary counterexample.** Put one outage immediately before a calendar boundary and an identical outage immediately after. They enter separate calendar windows but may enter the same rolling window. Thus calendar and rolling compliance cannot be substituted without changing meaning.

**Conjunction argument.** If correctness and latency represent non-substitutable user requirements, a weighted average permits excess correctness to compensate for unacceptable latency or vice versa. Conjunction preserves both constraints; a composite requires an explicit substitutability claim.

**Feasibility argument.** If a mandatory serial dependency has worse end-to-end success under the same population than the proposed service objective and no mechanism masks its failures, the service target is unattainable. A tighter internal dependency objective alone does not create feasibility; architecture or contract must change.

## Alternatives and Trade-Offs

**Rolling versus calendar windows.** Rolling windows reflect recent experience continuously and complicate period closure. Calendar windows align with contracts and planning but reset sharply. Select from decision purpose and publish boundaries.

**Strict versus loose initial targets.** Strict targets can protect users and force investment but create permanent breach if infeasible. Loose targets permit learning but may normalize avoidable harm. Use evidence, explicit uncertainty, and scheduled refinement.

**Committed versus aspirational objectives.** Committed objectives activate policy and must be attainable. Aspirational objectives make desired progress visible without treating every interval as emergency. Never mix their dashboards or consequences.

**Internal versus external objectives.** Internal targets can be tighter to provide safety margin and earlier response. External targets provide stable expectations. Excessive hidden divergence can confuse priorities; document their relationship.

**One combined versus several complementary objectives.** A combined good-event predicate represents complete success. Separate objectives localize availability, latency, correctness, or freshness. Use the smallest set that covers distinct harms and keeps decisions understandable.

**Global versus cohort objectives.** Global ratios describe total events and are stable for large populations. Cohort objectives protect concentrated harm but add governance and sparse-data challenges. Choose bounded cohorts from distinct contracts or consequences.

**Observed versus modeled feasibility.** Historical behavior includes real complexity but may omit rare failures and future growth. Models explore counterfactuals but depend on assumptions. Use both and test high-risk assumptions.

**Fixed versus adaptive targets.** Fixed targets are predictable and auditable. Adaptive targets can follow context but risk moving goalposts and strategic manipulation. If adaptation is essential, predefine its inputs, bounds, authority, and version behavior.

## Failure Modes and Misconceptions

1. **“An SLO is a metric.”** The metric feeds an SLI; the SLO is a target predicate over the indicator and window.
2. **“An SLO is an SLA.”** An agreement adds negotiated scope and consequences; an objective alone does not.
3. **“More nines mean maturity.”** Appropriate reliability depends on user consequence, feasibility, and cost.
4. **“Current performance is the correct target.”** It is evidence, not the value judgment.
5. **“Aspirational and committed mean the same thing.”** Only the committed target should activate the current policy.
6. **“100% guarantees no failure.”** It covers only the measured population and creates zero tolerance for classified bad events.
7. **“The window is presentation detail.”** Rolling, calendar, short, and long windows change classification and decisions.
8. **“A calendar reset repairs user experience.”** Users do not forget an outage because the month changed.
9. **“Every SLI needs an objective.”** Diagnostic metrics and exploratory indicators may not warrant policy targets.
10. **“Every user needs a unique SLO.”** Unbounded objectives become ungovernable; use distinct contracts and bounded cohorts.
11. **“A global pass protects every cohort.”** High-volume healthy traffic can mask complete failure elsewhere.
12. **“Dependencies are excluded from our SLO.”** End-to-end users still experience them unless the contract explicitly says otherwise.
13. **“A tighter dependency target guarantees our target.”** Shared failures, composition, and missing mitigation can defeat it.
14. **“A composite score is neutral.”** Weights encode substitutability and stakeholder values.
15. **“An objective should trigger a page directly.”** Window compliance and urgent alerting have different time and action semantics.
16. **“A missed SLO proves negligence.”** It is evidence for the declared policy, not an automatic causal or legal judgment.
17. **“Targets only move upward.”** Evidence can justify tightening, relaxing, splitting, or retiring an objective.
18. **“Editing the query fixes history.”** Definition changes require versioning and prospective governance.

## Worked Examples

### Example 1

**Situation.** A team proposes “API availability: 99.9%.”

**Reasoning.** The statement lacks an indicator version, event unit, eligibility, goodness, measurement point, window, and scope. Rewrite it: at least 99.9% of eligible client-observed logical read operations return the authorized version within 400 ms in each rolling 28-day window, using SLI `read-success-v3`.

**Conclusion.** A percentage becomes an objective only when bound to a reproducible measurement contract and window.

### Example 2

**Situation.** An SLO target is 99.5% over 7,000 valid operations; 6,970 are good.

**Reasoning.** The minimum satisfying good count is $\lceil0.995\times7{,}000\rceil=6{,}965$. The observed SLI is $6{,}970/7{,}000=99.5714\%$, so the objective is met with a five-event margin. This is classification of the completed population, not a prediction.

**Conclusion.** Integer counts reveal the exact boundary hidden by rounded percentage display.

### Example 3

**Situation.** A new service has achieved 99.97% for two quiet weeks, and leaders propose 99.95% as its permanent objective.

**Reasoning.** The sample lacks peak load, maintenance, dependency loss, release churn, and seasonal traffic. User research suggests 99.5% would meet current workflow needs. Adopt a provisional committed target with review date, load and fault evidence, and a separately tracked higher aspiration rather than treating two weeks as destiny.

**Conclusion.** Historical performance informs but does not mechanically choose the target.

### Example 4

**Situation.** A 60-minute outage begins at 23:30 UTC on January 31.

**Reasoning.** Monthly calendar evaluation splits 30 minutes into January and 30 into February. A rolling 28-day evaluation at February 1 includes the entire outage. Both computations can be correct, yet their decisions differ. The specification must name the window and timezone.

**Conclusion.** Window boundaries are part of objective semantics, not dashboard formatting.

### Example 5

**Situation.** Global success is 99.95%, but an accessibility client cohort records 700 good of 1,000 eligible operations.

**Reasoning.** If this cohort has a distinct supported contract and substantial harm, the global pass is insufficient. Define a bounded cohort objective or a combined predicate covering required accessibility behavior. Preserve counts because sparse cohorts produce coarse percentages.

**Conclusion.** Objective coverage must protect important cohorts rather than rely only on aggregate volume.

### Example 6

**Situation.** A team wants one score: 50% availability ratio plus 50% latency ratio. Availability is 90% and latency is 100%, giving 95%.

**Reasoning.** If users require both successful and timely results, perfect latency among available operations cannot compensate for 10% failure. Use a combined correct-and-timely SLI or conjunctive objectives. A weighted composite is defensible only if stakeholders accept the substitution.

**Conclusion.** Arithmetic weights silently encode product values and can hide non-substitutable harm.

### Example 7

**Situation.** A service promises 99.99% success but its mandatory unmasked dependency delivers 99.9% under the same demand.

**Reasoning.** Every dependency failure becomes service failure, so the service cannot normally exceed that path without mitigation. A stricter request to the dependency is not a mechanism. Add redundancy, caching, degradation, or change the service promise and validate the new failure assumptions.

**Conclusion.** Dependency feasibility must be established architecturally, not wished into an objective.

### Example 8

**Situation.** A product needs 99.9% today but only achieves 99.0%; closing the gap requires a six-month redesign.

**Reasoning.** Keep an achievable committed objective that drives current decisions, label 99.9% aspirational, define milestones and user-risk mitigations, and review whether the current commitment remains ethically and commercially acceptable. Calling 99.9% committed would make ordinary operation a constant violation.

**Conclusion.** Aspirational objectives preserve direction without destroying the meaning of current policy.

### Example 9

**Situation.** An incident caused many tickets but the SLO stayed green; another green-user day caused a miss due to telemetry classification.

**Reasoning.** The first is a coverage false negative: improve the SLI boundary, add a missing user harm, or tighten the target. The second is a false positive: repair measurement or relax a target unsupported by harm. Replay known incidents under candidate definitions and record precision-versus-recall trade-offs.

**Conclusion.** User and incident evidence should test whether the objective separates meaningful conditions.

### Example 10

**Situation.** A team changes eligibility during a bad month and recomputes the month as compliant.

**Reasoning.** The change may be technically justified but retroactive substitution destroys auditability. Preserve the original SLO result, publish a corrected analysis with defect provenance, version the SLI/SLO prospectively, and run old and new definitions in parallel.

**Conclusion.** Honest evolution adds versions; it does not erase the decision context of historical results.

## Cross-Program Connections

1. [SARCH-001](../../12-software-engineering-software-architecture/ROADMAP.md) connects dependency paths and failure containment to objective feasibility.
2. [API-001](../../28-api-and-service-engineering/ROADMAP.md) connects user-visible operations and protocol contracts to objective scope.
3. [PLAT-001](../../29-platform-engineering/ROADMAP.md) connects reusable objective schemas and governance to platform capabilities.
4. [STQE-001](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) connects fault, load, and regression tests to attainability evidence.
5. [SYSENG-001](../../26-systems-engineering/ROADMAP.md) connects stakeholder value, trade studies, and lifecycle review to objective choice.
6. [SEME-001](../../10-software-engineering-methods-and-evolution/ROADMAP.md) connects opportunity cost and prioritization to reliability investment.
7. [SEC-001](../../25-security-engineering/ROADMAP.md) connects abuse, integrity, and security consequences to bounded objectives.
8. [DE-001](../../19-data-engineering/ROADMAP.md) connects freshness, completeness, and correctness objectives to data pipelines.
9. [DBE-001](../../18-database-engineering/ROADMAP.md) connects dependency guarantees and durability targets to data services.
10. [SDDM-001](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) connects product discovery and feedback to evolving user expectations.

## References

1. Jones, C., Wilkes, J., Murphy, N. R., and Smith, C. “Service Level Objectives.” *Site Reliability Engineering*. O'Reilly/Google, 2016. <https://sre.google/sre-book/service-level-objectives/>. Retrieved 2026-09-06.
2. Thurgood, S., and Ferguson, D., with Hidalgo, A., and Beyer, B. “Implementing SLOs.” *The Site Reliability Workbook*. O'Reilly/Google, 2018. <https://sre.google/workbook/implementing-slos/>. Retrieved 2026-09-06.
3. OpenSLO Authors. “OpenSLO Specification.” Version 1 repository; version 2 identified as work in progress. <https://github.com/OpenSLO/OpenSLO>. Retrieved 2026-09-06.
4. McCormack, B., and Bonnell, W. “SLO Engineering Case Studies.” *The Site Reliability Workbook*. O'Reilly/Google, 2018. <https://sre.google/workbook/slo-engineering-case-studies/>. Retrieved 2026-09-06.
5. Alvidrez, M. “Embracing Risk.” *Site Reliability Engineering*. O'Reilly/Google, 2016. <https://sre.google/sre-book/embracing-risk/>. Retrieved 2026-09-06.
6. Google. “Product-Focused Reliability for SRE.” Google SRE resources. <https://sre.google/resources/practices-and-processes/product-focused-reliability-for-sre/>. Retrieved 2026-09-06.

## Exercises

### Exercise 1

Define SLO, target, objective predicate, rolling window, calendar window, committed objective, aspirational objective, attainability, coverage, and reliability frontier. Distinguish SLO, SLI, SLA, KPI, and alert threshold.

### Exercise 2

For 19,931 good of 20,000 valid operations and a target of 99.6%, compute the SLI, minimum good count, event margin, and met status. Then recompute after 20 additional bad operations enter the same window.

### Exercise 3

Design a committed and aspirational SLO pair for a video-upload workflow. Bind them to indicator versions, targets, windows, cohorts, decision purposes, feasibility evidence, and review dates.

### Exercise 4

A dependency has 99.8% observed success, while your service seeks 99.95% correct completion. Compare accepting the mismatch, negotiating an internal objective, adding a cache, adding redundant providers, and degrading functionality. State the assumptions that decide among them.

### Exercise 5

Transfer the objective model to a hospital medication-order system. Propose a small objective set, distinguish aggregate reliability from safety obligations, specify governance and evidence, and avoid claiming certification or clinical adequacy.

## Answers to the Exercises

### Answer 1

An SLO is a target range or value for a versioned SLI over a window. The target is the comparison boundary; the objective predicate decides met or missed. A rolling window advances with evaluation time; a calendar window uses fixed civil boundaries. A committed objective activates current policy; an aspirational objective tracks desired future performance. Attainability means normal design and operation can meet the target. Coverage is how well the objective set captures important user harm. The reliability frontier is the feasible trade-off among reliability and other constraints. The SLI defines measurement, the SLO defines desired level, the SLA adds negotiated consequences, a KPI may measure broader business performance, and an alert threshold triggers an urgent response rather than classifying long-window compliance.

### Answer 2

The SLI is $19{,}931/20{,}000=99.655\%$. The minimum satisfying count is $\lceil0.996\times20{,}000\rceil=19{,}920$, so the margin is 11 good events and the objective is met. After 20 bad operations, good remains 19,931 and valid becomes 20,020. The SLI is $19{,}931/20{,}020=99.5554\%$. The minimum is $\lceil0.996\times20{,}020\rceil=\lceil19{,}939.92\rceil=19{,}940$, the margin is $-9$, and the objective is missed. Rounding the displayed SLI must not replace integer-boundary evaluation.

### Answer 3

Committed: for `upload-complete-v2`, at least 99.0% of eligible client-started logical uploads of supported size must become correctly playable within ten minutes in each rolling 28-day window; evaluate global and bounded mobile/region cohorts. This drives current release and defect priority and is supported by peak-load, retry, storage-loss, transcode-failure, and recovery evidence. Aspirational: track 99.8% against the same SLI and window while a resumable-upload and multi-region transcode redesign proceeds; it informs investment but does not activate the current policy. Name product and service owners, source coverage, effective date, six-month review, and conditions for promotion. Acceptable variants may use multiple size tiers if each represents a distinct contract and remains bounded.

### Answer 4

Accepting the mismatch makes 99.95% unattainable if every dependency failure is exposed. A negotiated tighter internal objective helps only if the dependency can achieve it and composition leaves margin. A cache can mask read failures if data may be stale and cache hit rate is sufficient. Redundant providers can improve success only with independent failures, compatible semantics, bounded failover, and adequate capacity; common networks or data sources defeat the model. Degradation can satisfy a narrower correct contract if users accept reduced functionality. Choose using operation semantics, consistency, staleness, failure correlation, cost, latency, security, and tested recovery. Otherwise lower or redefine the service objective honestly.

### Answer 5

Possible objectives are: eligible medication orders are recorded with correct patient, medication, dose, prescriber, and timestamp before the clinical deadline; authorized retrieval returns the current order correctly within a workflow deadline; urgent order changes reach required clinical roles before escalation deadlines. Use separate predicates where timeliness cannot compensate for correctness, plus bounded cohorts for wards, downtime modes, and accessibility needs. Aggregate percentages do not make a hazardous wrong order acceptable and do not prove safety. Governance requires clinical product authority, engineering, safety, security, privacy, operations, audit provenance, prospective versioning, incident review, hazard analysis, independent correctness oracles, fault and downtime exercises, and explicit manual fallback. Targets and responses require qualified local judgment. This educational design is not clinical validation, regulatory compliance, certification, or evidence that the system is safe for use.
