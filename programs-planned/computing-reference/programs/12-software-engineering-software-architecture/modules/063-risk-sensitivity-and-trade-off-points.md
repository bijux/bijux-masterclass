---
module_id: SARCH-063
program: Software Engineering: Software Architecture
level: 2
module_number: 63
title: Risk, Sensitivity, and Trade-Off Points
status: complete
last_verified: 2026-09-06
---

# Risk, Sensitivity, and Trade-Off Points

## One-Page Review

### Governing question

Which architectural decisions make important outcomes fragile, where do small changes materially alter those outcomes, and which decisions improve one quality while worsening another?

### Essential definitions

- An **architectural risk** links a decision or omission, a scenario, uncertain conditions, and an unacceptable consequence; a vague topic such as “database risk” is not enough.
- A **nonrisk** is an analyzed decision judged adequate for named scenarios, assumptions, and evidence—not a permanent approval.
- A **sensitivity point** is a decision or parameter for which a small relevant change materially changes a quality response [1, 2].
- A **trade-off point** is a decision or parameter that materially affects two or more quality responses, often in competing directions [1].
- A **risk theme** groups findings that share a systemic cause, boundary, or governance weakness.
- **Uncertainty** describes incomplete knowledge; **variability** describes real differences across workload, users, environments, or time.
- A **threshold** is a boundary at which behavior or acceptability changes; a **cliff** is a sharp nonlinear deterioration near such a boundary.
- An **interaction** occurs when the joint effect of two decisions or conditions differs from the sum of their isolated effects.
- **Pareto dominance** means one alternative is no worse on every reviewed response and strictly better on at least one.
- **Residual risk** remains after treatment and requires explicit ownership and acceptance authority.

### Central model, mechanism, or theorem

For response $y=f(x_1,\ldots,x_n)$, a local finite-difference sensitivity for parameter $x_i$ is

$$
S_i\approx\frac{\Delta y}{\Delta x_i}.
$$

Its units and evaluation point matter. A normalized elasticity

$$
\epsilon_i\approx\frac{\Delta y/y}{\Delta x_i/x_i}
$$

supports limited relative comparison when $x_i$ and $y$ are nonzero, changes are sufficiently local, and the response is smooth. Neither expression discovers thresholds, interactions, or omitted variables by itself.

For two binary factors, an interaction contrast is

$$
I_{ab}=y_{11}-y_{10}-y_{01}+y_{00}.
$$

A nonzero value means the joint effect is not explained by adding isolated effects. Architectural analysis must therefore vary consequential combinations, not only one factor at a time.

### Critical invariants

- every risk names decision or omission, scenario, consequence, assumptions, evidence, and owner;
- likelihood, impact, exposure, and confidence retain units, time horizon, population, and source;
- ordinal labels are not multiplied, averaged, or interpreted as probabilities without a justified model;
- sensitivities name baseline, perturbation, response, units, range, and uncertainty;
- local gradients are not extrapolated across thresholds, discontinuities, mode changes, or large ranges;
- trade-offs compare a response vector and mandatory guardrails, not one opaque score;
- common causes and factor interactions are analyzed before independence is assumed;
- dominated alternatives are removed only within the declared dimensions and evidence;
- safety, security, privacy, accessibility, legal, and ethical constraints are not purchased away by aggregate benefit without competent authority;
- residual risk and dissent remain visible after a decision.

### Common failures

Common failures include listing components instead of risk statements; treating uncertainty as low probability; multiplying red/amber/green categories; assigning precise probabilities without data; confusing importance with sensitivity; using one-factor-at-a-time analysis on interacting decisions; extrapolating an average slope across a capacity cliff; declaring the cheapest option optimal; hiding guardrail violations in a weighted score; treating correlation as causation; ignoring common-mode dependencies; calling every multi-quality decision a tradeoff; removing minority harm through averaging; and closing risk when it is merely documented.

### Compact example

An authorization cache has a 30-second time-to-live. Increasing it to 60 seconds reduces identity-service calls from 1,000 to 650 per second under the measured workload, a local sensitivity of $(650-1000)/(60-30)=-11.67$ calls/s per added TTL second. But worst-case revocation exposure rises by 30 seconds. TTL is therefore a trade-off point between dependency load and revocation timeliness. The slope is local: cache-hit distribution, user sessions, active invalidation, and identity outage can create thresholds or different responses.

### Connections

[SARCH-061](061-architecture-tradeoff-analysis-method.md) defines ATAM findings, and [SARCH-062](062-quality-attribute-scenarios.md) supplies measurable scenarios. [SARCH-064](../ROADMAP.md) next turns selected architectural properties into fitness functions. This module owns decision fragility and multi-quality reasoning, not organizational risk management in general.

## Governing Question

Architecture evaluation becomes useful when it identifies where decisions matter. Some decisions barely move a response across the plausible range. Others create cliffs: one more shard, retry, region, privilege, schema version, or second of cache life changes cost, latency, correctness, or safety materially.

The goal is not to rank anxieties. It is to connect uncertain scenarios to decision variables and consequences, expose interactions and tradeoffs, and preserve the conditions under which a recommendation is rational.

## Why This Matters

Teams often spend precision on the wrong variables. They optimize average request time while an authority transition controls data integrity, or debate provider prices while a shared identity dependency defeats regional isolation. Sensitivity analysis focuses evidence where decisions can change outcomes.

Tradeoff analysis prevents local optimization. Caching, replication, isolation, batching, retention, automation, and centralization affect multiple qualities. A transparent response vector lets stakeholders see consequences and prevents arbitrary weights from laundering mandatory harm into an attractive total.

## Prerequisites and Retrieval

Retrieve architecture decision, scenario, response measure, risk, nonrisk, sensitivity point, trade-off point, uncertainty, variability, probability, frequency, consequence, exposure, threshold, derivative, finite difference, normalization, elasticity, interaction, confounder, correlation, common cause, Pareto dominance, utility, constraint, guardrail, option, mitigation, transfer, avoidance, acceptance, and residual risk.

From SARCH-004 through SARCH-020 retrieve quality attributes and tactics. SARCH-051 through SARCH-060 supply difficult distributed failure mechanisms. SARCH-061 supplies ATAM, while SARCH-062 supplies scenario and measurement discipline. Retrieve elementary algebra, proportions, dimensional analysis, and probability assumptions.

## Learning Objectives

After completing this module, you should be able to:

1. write decision-specific architectural risks and scoped nonrisks;
2. separate uncertainty, variability, likelihood, impact, confidence, and priority;
3. compute and interpret local finite-difference sensitivity with units;
4. normalize sensitivity when relative comparison is justified;
5. detect thresholds, cliffs, nonlinearity, and factor interactions;
6. distinguish sensitivity points from trade-off points;
7. compare alternatives using response vectors, guardrails, and Pareto dominance;
8. use risk matrices, expected loss, and weighted scores without false precision;
9. choose prototypes, experiments, models, and monitoring to reduce decision-relevant uncertainty;
10. document treatment, residual risk, dissent, evidence, and reevaluation triggers.

## Core Exposition

**Write a causal risk statement.** Use the form: because decision or omission $A$ operates under condition $B$, scenario $C$ may produce consequence $D$, and current evidence $E$ does not sufficiently bound it. Name affected stakeholders and time horizon.

“Database scalability is risky” identifies neither cause nor outcome. “Because all tenant writes share one unpartitioned index, the admitted holiday workload may exceed its measured service capacity, causing order acknowledgement beyond two seconds and an unbounded queue” is reviewable.

**Distinguish risk from issue and uncertainty.** An issue has already occurred or is known to violate a requirement. A risk concerns an uncertain future consequence. Uncertainty can concern model form, parameter value, implementation, workload, threat, human behavior, or evidence transfer.

Do not convert “unknown” into a low likelihood. Record epistemic uncertainty and commission the evidence that could change a decision. Real variability—such as tenant size or network delay—should be represented by distributions or scenarios rather than “resolved” by more measurement.

**Scope nonrisks.** A nonrisk records that a reviewed approach appears adequate for named scenarios and assumptions. It is valuable because it preserves reasoning and reduces repeated debate. It expires with material changes to architecture, workload, environment, threat, or evidence.

“Replication is a nonrisk” is too broad. “For loss of one storage node under the tested write workload, three replicas across independent power domains preserve acknowledged durability and recovery within 12 minutes” is scoped and still excludes common software corruption or region loss.

**Find decision variables.** Translate architecture descriptions into variables: replica count, quorum size, timeout, retry budget, queue capacity, cache TTL, shard count, batch size, isolation boundary, deployment cohort, retention, encryption mode, consistency level, staffing, and recovery capacity.

Some variables are categorical: active-passive versus active-active, centralized versus federated authority, mutable versus immutable deployment. Sensitivity analysis can compare categorical alternatives, but a derivative metaphor may be inappropriate.

**Measure local sensitivity.** Perturb one decision by a small meaningful amount near the current baseline and measure the response change. Always report units and direction. A value of $-11.67$ calls/s per TTL-second is meaningful only near the tested cache workload.

Normalize when units obstruct comparison. If a 10% increase in batch size produces a 4% reduction in CPU, local elasticity is about $-0.4$. This does not mean every 10% increase has the same effect or that CPU is the only relevant response.

**Search for nonlinear behavior.** Plot or sample across the plausible range. Queues approach instability as arrival rate approaches service capacity; cache hit rate can saturate; sharding can add coordination; timeouts can trigger retry feedback; quorum changes are discrete.

A local slope away from a threshold can be small while the design is fragile at the boundary. Identify breakpoints, mode switches, hysteresis, and recovery paths. Test both directions when systems retain state.

**Analyze interactions.** One-factor-at-a-time analysis assumes other factors remain fixed and can miss combinations. A retry budget may be harmless at low concurrency and catastrophic with a slow dependency. Regional failover may work unless identity and DNS share the failed control plane.

Use factorial comparisons, scenario combinations, model checking, simulation, or dependency analysis appropriate to the claim. An interaction contrast quantifies non-additivity in a simple two-factor experiment; causal interpretation still depends on controlled conditions.

**Use global sensitivity when models justify it.** Local sensitivity studies a neighborhood. Global sensitivity varies inputs across declared distributions and can apportion output variance or rank influence [3]. It is useful for capacity, cost, reliability, and performance models with defensible inputs.

Global methods inherit model and distribution errors. A parameter with little variance contribution may still control a catastrophic threshold or mandatory constraint. Use consequence and guardrail analysis alongside variance-based rankings.

**Separate importance from sensitivity.** A response can be highly sensitive to an unimportant parameter, or an important outcome can be insensitive across the feasible design range. Importance comes from drivers and consequences; sensitivity comes from response change.

Prioritize evidence where importance, uncertainty, and decision sensitivity intersect. Avoid multiplying ordinal categories as though they formed a probability model.

**Identify trade-off points.** A sensitivity point becomes a trade-off point when it materially affects multiple quality responses. Cache TTL affects latency, dependency availability, revocation, and freshness. Cell size affects blast radius, utilization, cost, and operational complexity.

Not every multi-quality decision is a conflict. Replication may improve read latency and availability together within a range, though it can worsen cost and write coordination. Record direction, magnitude, range, and guardrails rather than asserting “everything is a tradeoff.”

**Represent a response vector.** For alternative $a$, record

$$
v(a)=(latency,cost,recovery,integrity,security,change,\ldots).
$$

Keep units and uncertainty. Mark mandatory gates before preferences. An option violating stale-write fencing is infeasible even if its weighted latency and cost score is attractive.

**Use Pareto reasoning.** Alternative $a$ dominates $b$ within reviewed dimensions if it is no worse on every response and better on at least one. Remove a dominated alternative only after verifying uncertainty and omitted dimensions cannot reverse the relation.

Nondominated alternatives form a frontier; stakeholder values are still needed to choose among them. Pareto status is not universal optimality.

**Treat weights carefully.** Weighted sums require direction normalization, scales, tradeoff rates, and stakeholder legitimacy. Changing normalization or weights can reverse the ranking. Run sensitivity on the decision model itself.

Do not allow a large benefit to compensate for a mandatory safety, privacy, legal, or accessibility violation. Encode noncompensatory constraints first. Use separate stakeholder views when one aggregate would erase distributional effects.

**Understand risk matrices.** Ordinal likelihood-impact matrices support conversation and routing. They can reverse rankings, imply unjustified arithmetic, collapse uncertainty, and hide time horizon and population. Define categories and never call cell position a probability.

Expected loss $E[L]=\sum p_iL_i$ can support repeated financial or operational decisions when probabilities, consequences, dependence, and horizon are credible. It is insufficient for poorly known catastrophic, adversarial, irreversible, or ethically constrained harm.

**Model uncertainty explicitly.** Use intervals, distributions, scenario bounds, and confidence grades. Separate aleatory variability from epistemic uncertainty when useful. Show how recommendations change at interval extremes.

If option A wins only under one optimistic estimate, the result is fragile. Value-of-information reasoning asks whether reducing uncertainty could change the decision and whether that evidence costs less than the expected decision improvement.

**Choose evidence by sensitivity.** Measure high-sensitivity parameters precisely enough for the decision. Prototype a novel mechanism, benchmark a capacity cliff, model a protocol, inject a failure, test a migration, or conduct representative human studies.

Low-sensitivity variables may tolerate conservative bounds. However, mandatory guardrails and catastrophic thresholds still require evidence even when average model outputs appear insensitive.

**Connect risks into themes.** Group risks only when they share cause or action: unbounded work amplification, implicit authority, global control coupling, incomplete lifecycle, missing observability, or unowned reconciliation. Preserve the individual scenario traces.

A theme may indicate a platform, organizational, or governance intervention. Do not use a broad label such as “technical debt” to avoid specific decisions and owners.

**Select treatment.** Avoid the risk by removing the decision or exposure; reduce likelihood or consequence; transfer a bounded contractual or financial part; prepare contingency; or accept residual risk through competent authority. Security, safety, privacy, and legal responsibility may not be transferable merely by contract.

Each treatment has secondary risks. A circuit breaker reduces cascading load but can increase denied service; regional redundancy reduces some outages but adds control and consistency complexity. Analyze treatment as another architectural decision.

**Record the decision.** Include scenarios, alternatives, response vectors, assumptions, evidence, uncertainties, sensitivities, thresholds, interactions, guardrails, chosen treatment, residual risks, dissent, owner, and reevaluation triggers.

Monitor leading indicators near sensitivity points and lagging outcome measures. Reopen when workload, architecture, dependency, regulation, threat, incident evidence, or stakeholder values change materially.

**Preserve accountable boundaries.** Quantitative analysis informs judgment but does not authorize harm. Named safety, security, privacy, accessibility, financial, legal, and operational authorities decide within their mandates.

Report what was not modeled and who was not represented. Precision in a partial model must not erase the limits of the model or the legitimacy of affected people.

## Definitions and Notation

Let:

- $y=f(x_1,\ldots,x_n)$ be a quality response as a function of architectural variables;
- $S_i\approx\Delta y/\Delta x_i$ be local finite-difference sensitivity at a stated baseline;
- $\epsilon_i\approx(\Delta y/y)/(\Delta x_i/x_i)$ be local elasticity when denominators are nonzero;
- $I_{ab}=y_{11}-y_{10}-y_{01}+y_{00}$ be a two-factor interaction contrast;
- $v(a)$ be the response vector for alternative $a$;
- $G_j(a)$ be mandatory guardrail $j$, satisfied only when $G_j(a)=true$;
- $p_i$ and $L_i$ be justified probability and loss for outcome $i$ over one declared horizon;
- $E[L]=\sum_i p_iL_i$ be expected loss under the model;
- $U_e$ be epistemic uncertainty and $V_a$ aleatory variability;
- **robust decision** mean an alternative remaining acceptable across a reviewed uncertainty set;
- **fragile decision** mean a recommendation that changes under small plausible assumption changes.

Sensitivity has units unless normalized. A derivative or finite difference is descriptive of the modeled response near its baseline; it is not automatically causal, global, or transferable.

## Mechanisms, Invariants, or Proof Structure

### Analysis procedure

1. Select high-priority quality scenarios and mandatory constraints.
2. Trace each scenario to architectural decisions, variables, mechanisms, dependencies, and owners.
3. Write causal risks, scoped nonrisks, known issues, and unresolved uncertainties separately.
4. Establish baseline response vectors, units, bounds, evidence, and model validity.
5. Perturb variables locally, then sample plausible ranges for thresholds and nonlinearities.
6. Analyze common causes, factor interactions, degraded modes, and recovery sequences.
7. Identify sensitivity and trade-off points with direction, magnitude, range, and uncertainty.
8. Eliminate only defensibly dominated options; apply mandatory guardrails before preferences.
9. Test recommendation sensitivity to weights, normalization, probability, cost, and stakeholder assumptions.
10. Record treatment, residual risk, dissent, evidence gaps, monitoring, owner, and reevaluation triggers.

### Proof obligations

- **Trace:** Does each finding connect decision, scenario, response, consequence, and evidence?
- **Scale:** Are quantitative and ordinal inputs treated according to their measurement scale?
- **Locality:** Is a local sensitivity used only over a justified neighborhood?
- **Interaction:** Were plausible common causes and combinations evaluated?
- **Constraint:** Are mandatory bounds noncompensatory?
- **Robustness:** Does the recommendation persist across plausible uncertainty and normalization choices?
- **Distribution:** Are benefits and harms reported for consequential cohorts rather than only totals?
- **Authority:** Does the correct owner accept residual consequences?

### Invariants

- no unknown value becomes an invented probability;
- no ordinal matrix supports multiplication or expected-loss arithmetic;
- no sensitivity omits baseline, units, perturbation, range, or response;
- no local slope is extrapolated through a threshold without evidence;
- no weighted score compensates a mandatory guardrail violation;
- no Pareto claim omits reviewed dimensions and uncertainty;
- no treatment closes risk without evidence or accountable acceptance;
- no residual risk or dissent disappears from the decision record.

## Alternatives and Trade-Offs

- **Qualitative risk statement versus quantitative model:** statements expose causal structure early; models sharpen comparison when inputs and consequences are defensible.
- **Local versus global sensitivity:** local methods diagnose neighborhoods; global methods explore ranges and distributions at greater model and computation cost.
- **One-factor-at-a-time versus factorial analysis:** isolated changes aid attribution; factorial designs reveal interactions.
- **Risk matrix versus expected loss:** matrices organize ordinal judgment; expected loss preserves numeric probability and consequence but demands stronger evidence.
- **Weighted score versus response vector:** scores simplify selection; vectors preserve units, distribution, guardrails, and disagreement.
- **Point estimate versus interval:** points communicate easily; intervals reveal fragility and uncertainty.
- **Expected value versus worst credible case:** expected values suit repeatable decisions; consequence bounds matter for catastrophic or irreversible outcomes.
- **Optimization versus satisficing:** optimization seeks best modeled value; satisficing meets guardrails and may be more robust under deep uncertainty.
- **Mitigation versus option preservation:** immediate mitigation reduces known exposure; reversible designs preserve choices as evidence improves.
- **Central control versus local autonomy:** centralization simplifies global policy; local authority improves latency and partition operation but complicates revocation and reconciliation.
- **Efficiency versus isolation:** shared capacity improves utilization; cells and bulkheads bound blast radius at duplication and operating cost.
- **Transparency versus confidentiality:** broad findings aid accountability; sensitive threat, supplier, personal, or commercial evidence requires governed access.

## Failure Modes and Misconceptions

1. **“Risk is a component list.”** Risk needs a causal decision-scenario-consequence statement.
2. **“Unknown means unlikely.”** Missing knowledge is uncertainty, not probability evidence.
3. **“Red times red equals nine.”** Ordinal categories do not justify arithmetic.
4. **“Expected loss decides every risk.”** Catastrophic, adversarial, irreversible, and mandatory harms may not fit the model.
5. **“Sensitivity means importance.”** Response change and stakeholder value are different.
6. **“One-at-a-time changes find the important variables.”** Interactions and common causes can dominate.
7. **“A small local slope means robust architecture.”** A nearby threshold may create a cliff.
8. **“Normalization removes judgment.”** Baselines and scales encode choices and can reverse rankings.
9. **“Correlation identifies the architectural cause.”** Confounding and shared dependencies may explain it.
10. **“Every decision is a tradeoff.”** Some options improve several responses together within a range.
11. **“A Pareto-front option is optimal.”** Values are still needed among nondominated alternatives.
12. **“One score is objective.”** Weights, units, compensation, and population choices remain normative.
13. **“Mitigation has only benefits.”** Every tactic introduces mechanisms, cost, and secondary risks.
14. **“Transferred risk is gone.”** Operational, legal, ethical, and reputational consequences may remain.
15. **“Accepted risk needs no monitoring.”** Assumptions and exposure change.
16. **“A nonrisk is permanent.”** It expires with scenario, design, or evidence changes.
17. **“Documenting risk closes it.”** Closure needs treatment evidence or competent acceptance.
18. **“Quantification authorizes harm.”** Models inform but do not replace accountable authority.

## Worked Examples

### Example 1

**Rewrite a vague risk.**

**Situation.** A register says “message broker—high risk.”

**Reasoning.** The reviewed decision uses one broker cluster for orders and analytics with shared storage and no tenant admission. During an analytics replay, storage may saturate, causing order commands to exceed their 30-second validity and leave customer payments unresolved. Existing evidence covers normal load only. The causal risk names decision, condition, consequence, missing evidence, and owners.

**Conclusion.** A specific risk can be analyzed and treated; a colored component label cannot.

### Example 2

**Compute local TTL sensitivity.**

**Situation.** Authorization-cache TTL rises from 30 to 60 seconds; identity calls fall from 1,000 to 650 per second.

**Reasoning.** $S=(650-1000)/(60-30)=-350/30=-11.67$ calls/s per TTL-second. Relative input change is 100%; relative output change is -35%, so elasticity over this large interval is approximately -0.35, though calling it local is weak. Revocation exposure rises by up to 30 seconds, making TTL a trade-off point.

**Conclusion.** Units, baseline, interval size, and the second quality are essential to interpretation.

### Example 3

**Expose a capacity cliff.**

**Situation.** Queue arrival rises from 700 to 800 requests/s while service remains 1,000/s; average wait changes little. A forecast extrapolates safely to 1,100/s.

**Reasoning.** Net spare capacity falls from 300 to 200/s, but at 1,100/s arrival exceeds service by 100/s and backlog grows without bound under the constant-rate model. The response crosses a stability threshold at 1,000/s; a slope below 800/s cannot justify extrapolation. Retries and variability may move practical failure earlier.

**Conclusion.** Threshold analysis overturns a comforting local trend.

### Example 4

**Calculate an interaction.**

**Situation.** Recovery time is 10 minutes at baseline, 14 with a slow database alone, 13 with identity outage alone, and 30 with both.

**Reasoning.** $I=30-14-13+10=13$ minutes. Adding isolated increases predicts 17 minutes, but the joint case takes 30 because recovery workers cannot obtain credentials while replay holds database capacity. The contrast establishes non-additivity in the recorded experiment, not universal causation.

**Conclusion.** The 13-minute interaction directs analysis to the shared recovery path.

### Example 5

**Remove a dominated alternative carefully.**

**Situation.** For the same workload, option A has latency 300 ms, monthly cost 80 units, and recovery 20 minutes; B has 250 ms, cost 75, and recovery 15 minutes.

**Reasoning.** B dominates A on the three reviewed responses. Before removing A, reviewers check uncertainty, integrity, security, portability, staffing, and migration. B requires a proprietary service unavailable in one jurisdiction, adding a mandatory residency violation for that population.

**Conclusion.** Dominance is relative to included dimensions and constraints; an omitted guardrail can reverse feasibility.

### Example 6

**Challenge an ordinal risk matrix.**

**Situation.** Two risks are rated likelihood Medium and impact High, then assigned $2\times3=6$.

**Reasoning.** The categories order judgments but do not establish equal intervals, multiplication, probability, or consequence units. One risk is a frequent 10-minute delay; the other is poorly known irreversible data disclosure. The team preserves descriptions, horizons, confidence, affected populations, and mandatory privacy treatment rather than treating equal cells as equivalent.

**Conclusion.** A matrix can route discussion but cannot manufacture quantitative comparability.

### Example 7

**Test a weighted decision for fragility.**

**Situation.** Centralized and cell-based designs score 72 and 70 after normalized cost, latency, recovery, and operability weights.

**Reasoning.** Moving the recovery weight from 0.20 to 0.25 reverses the ranking; changing cost normalization also reverses it. The two-point difference is smaller than input uncertainty. Both pass security guardrails, so the decision is preference-sensitive rather than technically settled. A targeted cell-operations prototype may reduce uncertainty.

**Conclusion.** Weight sensitivity should be reported instead of presenting 72 as objective superiority.

### Example 8

**Distinguish variability from uncertainty.**

**Situation.** Tenant write rates vary 100-fold, while the compression ratio of a new format is known only from a small sample.

**Reasoning.** Tenant variation is real population variability and requires skewed workload scenarios, isolation, and distribution reporting. Compression knowledge is epistemic uncertainty reducible through representative measurement. Replacing tenant rates with their mean hides large tenants; collecting more compression samples does not remove tenant variability.

**Conclusion.** The two forms require different architecture and evidence responses.

### Example 9

**Analyze mitigation as a new tradeoff.**

**Situation.** A circuit breaker is added to contain a slow dependency.

**Reasoning.** It bounds thread and connection consumption, improving containment and recovery. Its threshold and open duration can reject requests the dependency might have served, synchronize retry probes, and expose stale fallback. The team varies latency, error mix, concurrency, threshold, and half-open policy; guardrails cover incorrect fallback and priority users.

**Conclusion.** A mitigation changes the response surface and creates new sensitivity points.

### Example 10

**Route safety acceptance correctly.**

**Situation.** An automated rail-door controller reduces dwell time but occasionally loses obstruction-sensor evidence during network partition.

**Reasoning.** Dwell time, throughput, availability, and maintenance are response dimensions, while safe door/traction interlock is a noncompensatory guardrail. No weighted passenger-time benefit can offset an unbounded interlock claim. Architecture analysis identifies local authority, independent sensing, fail-safe state, diagnostic evidence, and partition scenarios; competent rail safety authorities own residual acceptance.

**Conclusion.** Tradeoff analysis informs design without converting safety authority into arithmetic.

## Cross-Program Connections

- **Software Design and Decision-Making:** owns general uncertainty, alternatives, utility, reversibility, options, and decision records.
- **Algorithm Engineering:** supplies optimization, sensitivity, approximation, distributions, and computational tradeoffs.
- **Software Testing and Quality Engineering:** owns experimental design, factor interaction, measurement validity, confidence, and evidence.
- **Systems Engineering:** owns risk management, hazard analysis, FMEA, fault trees, lifecycle assurance, and accountable acceptance.
- **Security Engineering:** owns threat likelihood limits, adversarial behavior, security risk, control evidence, and residual security authority.
- **Software Delivery and Reliability Engineering:** supplies incident, SLO, change, recovery, and operational evidence for sensitivities.
- **Data Architecture Engineering:** owns data authority, lifecycle, governance, privacy, residency, and cross-system consequences.
- **Platform Engineering:** owns shared controls whose sensitivity and blast radius affect multiple product architectures.
- **Economics and finance:** supply cost, benefit, expected-value, option, budget, and portfolio models under their assumptions.
- **Requirements Engineering:** owns stakeholder values, constraints, traceability, conflict, and requirement-change legitimacy.

## References

1. Paul Clements, Rick Kazman, and Mark Klein, *Evaluating Software Architectures: Methods and Case Studies*, Addison-Wesley, 2002.
2. Rick Kazman, Mark Klein, and Paul Clements, *ATAM: Method for Architecture Evaluation*, CMU/SEI-2000-TR-004, August 2000. <https://doi.org/10.21236/ADA382629>
3. Andrea Saltelli, Marco Ratto, Terry Andres, Francesca Campolongo, Jessica Cariboni, Debora Gatelli, Michaela Saisana, and Stefano Tarantola, *Global Sensitivity Analysis: The Primer*, Wiley, 2008. <https://doi.org/10.1002/9780470725184>
4. Andrea Saltelli, Stefano Tarantola, Francesca Campolongo, and Marco Ratto, *Sensitivity Analysis in Practice: A Guide to Assessing Scientific Models*, Wiley, 2004. <https://doi.org/10.1002/0470870958>
5. Robert L. Nord, Mario R. Barbacci, Paul Clements, Rick Kazman, and Mark Klein, *Integrating the Architecture Tradeoff Analysis Method (ATAM) with the Cost Benefit Analysis Method (CBAM)*, CMU/SEI-2003-TN-038, December 2003. <https://doi.org/10.21236/ADA421615>
6. ISO, *Risk Management — Guidelines*, ISO 31000:2018, February 2018. <https://www.iso.org/iso-31000-risk-management.html>
7. National Institute of Standards and Technology, *Guide for Conducting Risk Assessments*, NIST SP 800-30 Revision 1, September 2012. <https://doi.org/10.6028/NIST.SP.800-30r1>
8. Ralph L. Keeney and Howard Raiffa, *Decisions with Multiple Objectives: Preferences and Value Tradeoffs*, Cambridge University Press, 1993.
9. Douglas W. Hubbard, *The Failure of Risk Management: Why It's Broken and How to Fix It*, 2nd ed., Wiley, 2020.
10. ISO/IEC/IEEE, *Systems and Software Engineering — Architecture Description*, ISO/IEC/IEEE 42010:2022, November 2022. <https://standards.ieee.org/ieee/42010/6846/>

## Exercises

### Exercise 1

Define architectural risk, issue, uncertainty, variability, nonrisk, sensitivity point, trade-off point, threshold, cliff, interaction, local sensitivity, elasticity, Pareto dominance, guardrail, robust decision, fragile decision, treatment, and residual risk.

### Exercise 2

A batch size rises from 100 to 125 records. CPU time per record falls from 8 to 7 milliseconds, while p99 end-to-end latency rises from 400 to 550 milliseconds. Compute local sensitivities and approximate elasticities for both responses. State why the batch size is a trade-off point and why extrapolation is unsafe.

### Exercise 3

Diagnose a risk process that labels unknown likelihood Low, multiplies red/amber/green numbers, tests variables one at a time, extrapolates average slopes across peak load, averages every quality into one score, and marks transferred risks closed. Replace it with an evidence-bounded method.

### Exercise 4

Compare risk matrices, expected loss, response vectors, Pareto analysis, local sensitivity, global sensitivity, scenario bounds, and value-of-information reasoning for a multi-region payment architecture. State prerequisites and failure modes for each.

### Exercise 5

Analyze risk, sensitivity, and trade-off points for an international wildfire-detection and evacuation platform with satellites, cameras, field sensors, intermittent networks, local authorities, public alerts, accessibility, privacy, false alarms, missed detections, limited crews, changing weather, and safety-critical time. Include scenarios, variables, thresholds, interactions, response vectors, guardrails, uncertainty, treatments, residual authority, evidence, and reevaluation.

## Answers to the Exercises

### Answer 1

An **architectural risk** links a decision or omission and uncertain scenario to consequence. An **issue** is a known present violation. **Uncertainty** is incomplete knowledge; **variability** is real difference. A **nonrisk** is a scoped adequate finding. A **sensitivity point** materially affects one response; a **trade-off point** affects several, often oppositely. A **threshold** changes behavior or acceptability; a **cliff** is sharp deterioration. An **interaction** is a joint effect not explained additively. **Local sensitivity** is response change per nearby input change; **elasticity** is relative response change per relative input change. **Pareto dominance** means no worse on all reviewed dimensions and better on one. A **guardrail** is mandatory. A **robust decision** survives plausible uncertainty; a **fragile decision** reverses under small plausible change. **Treatment** avoids, reduces, contingently prepares for, transfers a bounded part of, or accepts risk. **Residual risk** remains afterward under named authority.

### Answer 2

The batch change is $\Delta x=25$ records. CPU response change is $-1$ ms/record, so local sensitivity is $-1/25=-0.04$ milliseconds per record of added batch size. Relative batch change is $25/100=0.25$; relative CPU change is $-1/8=-0.125$, giving approximate elasticity $-0.125/0.25=-0.5$.

Latency changes by 150 ms, so sensitivity is $150/25=6$ ms of p99 latency per added record. Relative latency change is $150/400=0.375$, giving elasticity $0.375/0.25=1.5$. Larger batches improve CPU efficiency while worsening tail latency, so batch size is a trade-off point. The 25% perturbation is not especially local; queueing, memory, packet, timeout, and service limits may create nonlinear thresholds. Test the plausible range and workloads rather than extrapolating either slope.

### Answer 3

Record unknown likelihood as epistemic uncertainty with confidence and needed evidence; do not turn it into Low. Use ordinal categories only for routing, with defined descriptions, horizons, populations, and consequences. Numeric expected loss requires defensible probabilities, consequence units, dependence, and time horizon. Trace risks causally from decision through scenario to outcome.

Identify architectural variables and mandatory guardrails, establish baseline response vectors with units and uncertainty, test local perturbations and the plausible range, and include factorial or scenario combinations for common causes and interactions. Search explicitly for capacity, timing, authority, and mode thresholds. Preserve each response rather than collapsing latency, integrity, safety, privacy, accessibility, and cost into a compensatory score. If weights support preference, test rankings against weight and normalization changes. A transferred contractual or financial portion does not remove operational, legal, ethical, security, or reputational residuals; keep owners, monitoring, acceptance, and reopen triggers.

### Answer 4

Risk matrices need defined ordinal categories and support triage, not probability arithmetic. Expected loss suits repeated comparable outcomes only with numeric probabilities, losses, horizon, and dependence; it is weak for adversarial, catastrophic, irreversible, or mandatory harm. Response vectors preserve units, uncertainty, distribution, and guardrails. Pareto analysis removes dominated options within included dimensions but cannot choose among nondominated ones or repair omitted constraints.

Local sensitivity needs a baseline and meaningful perturbation and exposes nearby decision leverage, not distant cliffs. Global sensitivity needs a credible model and input distributions and can rank variance influence, but low variance contribution does not dismiss catastrophic thresholds. Scenario bounds support deep uncertainty without invented distributions but may be conservative and dependent on scenario selection. Value-of-information reasoning prioritizes evidence when uncertainty could change the decision; it needs costs, possible decision changes, and credible value consequences. For payments, apply these to quorum, replication, timeout, retry, cache, region, provider, identity, capacity, integrity, reconciliation, and cost while preserving duplicate-capture, stale-authority, privacy, and legal guardrails.

### Answer 5

Scenarios cover detection under smoke/cloud, false alarm near dense populations, missed remote ignition, network partition, sensor compromise, regional control loss, rapidly changing wind, multilingual and accessible alerting, route closure, crew saturation, power loss, stale map, and recovery. Variables include sensor density, sampling rate, confidence threshold, fusion window, model version, cache age, link redundancy, local authority duration, alert threshold, region/cell size, route refresh, crew reserve, and human review.

Measure detection delay and miss/false-alarm distributions by terrain and population; alert delivery and comprehension by language, disability, device, and connectivity; route freshness; unauthorized alert count; privacy exposure; crew travel and capacity; power, bandwidth, cost, and reconciliation. Safety, authenticated authority, accessibility, privacy law, environmental constraints, and no stale evacuation command are noncompensatory guardrails.

Search thresholds where sensor load saturates links, confidence delays alerts past evacuation time, false alarms exhaust trust or crews, and local authority expires. Combine smoke with satellite gap, network loss with fast wind, regional outage with credential revocation, and false sensor injection with public panic. Use response vectors and remove options only when dominance survives uncertainty and omitted-dimension review. Treat model accuracy, weather, population movement, device reach, human response, and provider independence as separate uncertainty or variability.

Treat risks through diverse sensing, bounded local authority, independent alert channels, accessible templates, priority admission, authenticated epochs, privacy minimization, human escalation, staged model updates, reserve crews, and physical drills. Every treatment creates cost and new failure paths. Evidence combines historical replay, calibrated sensor tests, simulation, adversarial tests, network and power fault injection, representative accessibility and evacuation studies, and authorized field drills. Local emergency, fire, public-safety, accessibility, privacy, environmental, security, and governmental authorities own residual acceptance. Reevaluate after fire regime, climate, population, sensor/model, network, law, staffing, incident, or exercise changes.
