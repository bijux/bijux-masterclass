---
module_id: SARCH-020
program: Software Engineering: Software Architecture
level: 1
module_number: 20
title: Resolving Quality-Attribute Conflicts
status: complete
last_verified: 2026-09-06
---

# Resolving Quality-Attribute Conflicts

## One-Page Review

### Governing question

How can architects resolve competing quality-attribute demands without hiding constraints, inventing false precision, or allowing one stakeholder's gain to become another stakeholder's undisclosed harm?

### Essential definitions

- A **quality-attribute scenario** states a source, stimulus, environment, affected artifact, response, and response measure.
- A **conflict** exists when the same decision or limited resource improves one required response while worsening another under relevant conditions.
- A **tension** is a suspected interaction that still needs causal analysis and evidence; it is not automatically a conflict.
- A **hard constraint** is a condition a candidate must satisfy; it is not a low-weight preference.
- An **objective** is a quality outcome to improve or maintain within a declared scope.
- A **sensitivity point** is a property of one architectural decision on which a quality response depends strongly.
- A **trade-off point** is a property that affects two or more quality responses in competing ways.
- A candidate is **Pareto dominated** when another feasible candidate is no worse on every modeled objective and better on at least one.
- **Residual risk** is risk remaining after selected treatments, limitations, and uncertainty are considered.

### Central model, mechanism, or theorem

Let $D$ be candidate decisions, $H$ the hard constraints, and $z_i(d)$ the modeled loss for objective $i$, where smaller is better. The feasible set is

$$
F=\{d\in D:\forall h\in H,\ h(d)=true\}.
$$

For $a,b\in F$, $a$ dominates $b$ when $z_i(a)\le z_i(b)$ for every modeled objective and the inequality is strict for at least one. Eliminate dominated candidates, then choose among nondominated candidates through accountable judgment about scenarios, consequences, uncertainty, distribution of harm, cost, and option value. Pareto analysis narrows choice; it does not choose policy.

### Critical invariants

- compare concrete scenarios under the same declared conditions, not isolated quality labels;
- keep law, safety, rights, mission limits, and other non-compensable duties as constraints;
- trace each claimed interaction through a decision, mechanism, response, and evidence;
- normalize neither units nor scores without publishing meaning and assumptions;
- expose who receives benefits, costs, operational work, and residual risk;
- reject dominated candidates unless an omitted objective or incorrect model is demonstrated;
- preserve uncertainty, confidence, reversibility, and cost of delay;
- prefer experiments that discriminate between candidates rather than confirm a favorite;
- record the decision, rejected alternatives, evidence, owner, expiry, and reopening triggers;
- re-evaluate when workload, threat, dependency, regulation, population, cost, or observed behavior changes.

### Common failures

Common failures include treating every quality as maximizable; using a weighted score to cancel a safety or legal limit; comparing averages from different environments; claiming a conflict without a causal mechanism; choosing technology before scenarios; optimizing a component while degrading the task; omitting operational labor and failure coupling; double-counting correlated criteria; using precise but invented weights; suppressing minority harm in aggregate utility; presenting a Pareto frontier as a recommendation; and recording the winner without the rejected evidence or review trigger.

### Compact example

A cache reduces observed $p99$ latency from 900 ms to 300 ms but permits data up to 60 seconds stale. The requirement is $p99\le500$ ms and price age $\le5$ seconds. The cache setting is infeasible despite its latency gain. A five-second TTL plus event invalidation measures at 430 ms and four seconds stale, but introduces invalidation failure and operational cost. Keep the freshness limit as a constraint, compare feasible designs, test invalidation loss, and record residual risk.

### Connections

[SARCH-004](004-quality-attributes-as-architectural-drivers.md) supplies measurable scenarios; [SARCH-007](007-trade-offs-and-competing-objectives.md) supplies early decision framing; [SARCH-011](011-availability-and-recovery-tactics.md) through [SARCH-019](019-usability-and-accessibility-as-system-qualities.md) supply tactic consequences. [SARCH-021](../ROADMAP.md) begins architectural views, and [SARCH-061](../ROADMAP.md) later develops a full architecture evaluation method.

## Governing Question

Stakeholders often ask for stronger security, lower latency, higher availability, easier change, lower cost, richer telemetry, stricter privacy, and simpler use at once. These demands are not necessarily contradictory. Encryption can improve security with negligible user-visible latency; modularity can improve both change isolation and testability. A genuine conflict appears only when candidates, conditions, mechanisms, and response measures reveal incompatible outcomes or competition for a scarce resource.

The governing problem is therefore not “which quality wins?” It is how to build an honest decision boundary: which duties are mandatory, which outcomes are negotiable, what evidence distinguishes alternatives, who can accept residual risk, and what change should reopen the choice.

## Why This Matters

Quality conflicts shape boundaries that are difficult to reverse. Synchronous validation can strengthen immediate consistency while adding latency and dependency failure. Replication can improve continuity while expanding exposure, sovereignty obligations, and coordination. Fine-grained services can isolate some changes while increasing network failure, security surface, test scope, and operational workload.

Unstructured compromise usually rewards the loudest stakeholder or the easiest metric. A team may halve component latency while making recovery ambiguous, or maximize an aggregate score while violating an accessibility threshold for a smaller population. The arithmetic can look objective even when the model embeds unexamined power, false equivalence, and missing consequences.

Resolution is also temporal. A reversible decision with cheap measurement may justify an experiment. An irreversible data migration, physical safety boundary, or public protocol needs stronger pre-decision evidence. Architecture must preserve options when uncertainty is high and make residual risk visible rather than treating a meeting as permanent proof.

## Prerequisites and Retrieval

Retrieve stakeholder, concern, scenario, constraint, assumption, risk, invariant, tactic, decision, evidence, response measure, percentile, availability, latency, throughput, confidentiality, privacy, modifiability, testability, interoperability, observability, usability, accessibility, cost, uncertainty, reversibility, and residual risk.

From earlier modules, retrieve the six-part quality scenario, architectural significance, decision records, competing objectives, and the mechanisms and side effects of SARCH-011 through SARCH-019. You should be able to distinguish an observed response from a guarantee and a hard duty from a preference.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish a genuine quality conflict from a vague tension or false dichotomy;
2. translate interacting concerns into comparable scenarios and explicit constraints;
3. construct causal maps from decisions through mechanisms to quality responses;
4. identify sensitivity and trade-off points;
5. eliminate infeasible and Pareto-dominated candidates;
6. use weighted utility only with explicit value functions, units, and governance limits;
7. include distributional effects, operational work, uncertainty, reversibility, and option value;
8. design discriminating analyses, prototypes, experiments, and exercises;
9. negotiate and record an accountable decision with residual risk;
10. define evidence-based triggers for reopening the decision.

## Core Exposition

**Begin with scenarios, not attributes.** “Security versus usability” is too broad to analyze. Ask which user, threat, task, environment, response, and measure are involved. A second authentication factor may add twelve seconds to ordinary sign-in while reducing account takeover under a named threat model. Accessible recovery may improve both usability and security compared with knowledge questions. Scenario precision can dissolve a supposed conflict or locate it in one narrow condition.

ISO/IEC 25010:2023 provides a current reference model of nine product-quality characteristics and subordinate characteristics. It supports vocabulary and systematic challenge, but its catalogue does not establish project priorities or authorize one characteristic to cancel another [2]. Quality categories are prompts; stakeholder outcomes, duties, and system context govern the decision.

**Separate constraints from objectives.** A constraint defines admissibility. Examples include a statutory retention ceiling, a maximum safe actuation delay, a contractual recovery point, an accessibility requirement, or a physical resource limit. An objective distinguishes feasible candidates, such as lower median cost or shorter deployment lead time. Treating a constraint as a weighted criterion allows enough benefit elsewhere to “pay for” violation. That is a modeling error unless the responsible authority has explicitly made the boundary negotiable.

Some constraints are conditional. An emergency mode may permit a different response only under a declared trigger, authority, duration, audit obligation, and restoration rule. Model the condition; do not quietly soften the constraint for convenience.

**Trace causal mechanisms.** Draw a short chain for every claimed interaction:

decision $\rightarrow$ mechanism $\rightarrow$ response change $\rightarrow$ stakeholder consequence.

A retry policy may improve success after transient failure. It can also multiply load, amplify a dependency outage, duplicate non-idempotent effects, and extend tail latency. Those outcomes follow from retry count, backoff, deadlines, idempotency, capacity, and correlation—not from the word “availability.” A causal account suggests measurements and countermeasures.

**Find sensitivity and trade-off points.** A cache time-to-live is sensitive for freshness. If increasing it reduces origin load and latency while increasing staleness, it is also a trade-off point. Replication factor may affect recovery, read capacity, write latency, storage cost, and exposure. Identify the parameter, its valid range, and the conditions in which the response changes. Avoid assuming a linear relation when queues, thresholds, quorum changes, or failure modes create discontinuities.

The Software Engineering Institute's ATAM material distinguishes risks, sensitivity points, and trade-off points while relating architectural approaches to quality scenarios and business drivers [3]. This chapter uses those foundational ideas; the complete facilitated evaluation method belongs to SARCH-061.

**Generate materially different candidates.** “Current design, but faster” is not an alternative. Change the mechanism: precompute rather than compute on demand; isolate rather than share; degrade a noncritical response rather than all responses; use asynchronous acknowledgment rather than synchronous completion; reduce data collection rather than protect an unnecessary copy; simplify a workflow rather than automate its complexity.

Include a no-change baseline and a stop or defer option. State what each candidate does during healthy, peak, degraded, recovery, adversarial, and change conditions. Include migration and rollback. A candidate that cannot be operated or exited is incompletely specified.

**Evaluate feasibility before preference.** Apply hard constraints first. Then compare objective vectors among feasible candidates. If candidate A is no worse than B on every modeled objective and better on one, B is dominated. Keeping B requires showing a missing objective, invalid observation, uncertainty interval, or distinct condition—not personal attachment.

Nondominated candidates form a Pareto set relative to the modeled objectives and evidence. Moving from one to another improves at least one outcome while worsening another. The set changes when objectives, constraints, conditions, or evidence change. It is not a timeless fact about the design space.

**Use scores carefully.** A weighted sum can make value judgments inspectable:

$$
U(d)=\sum_{i=1}^{m}w_i u_i(y_i(d)),\qquad w_i\ge0,\quad\sum_iw_i=1.
$$

But raw milliseconds, dollars, percentages, and incident consequences cannot be added. Each $u_i$ must define direction, scale, thresholds, and value meaning. Weights encode substitution: how much loss in one modeled objective is accepted for gain in another. Correlated criteria can double-count one concern. Small weight changes can reverse rankings. Multi-objective decision analysis structures judgment; it does not manufacture authority or facts [5].

Never place a non-compensable duty inside an ordinary weighted sum. Report the vector and constraints alongside any score so reviewers can see what aggregation hides.

**Include distribution and human work.** An aggregate outcome can conceal who bears harm. Report relevant populations, contexts, locations, and operational roles. A design that improves mean latency but creates inaccessible recovery is not uniformly better. A service split that shortens one team's change lead time while creating round-the-clock toil for another transfers rather than removes cost.

Security engineering likewise treats protection needs and trustworthy-system claims as lifecycle concerns rather than isolated features; NIST SP 800-160 Vol. 1 Rev. 1 remains the current final revision as checked on 2026-09-06 [6]. Security, safety, privacy, accessibility, and operational authority require the relevant accountable reviewers, not only a software scoring workshop.

**Model uncertainty explicitly.** Record intervals, distributions, confidence, missing cases, model error, and evidence age. If candidate A measures 480–560 ms and the threshold is 500 ms, do not report “500 ms” as decisive. Identify whether more evidence can narrow the uncertainty and whether harm is asymmetric. Use conservative bounds where consequence requires them.

Value information before expensive or irreversible commitments. A focused load test may distinguish queue designs; a threat analysis may expose a shared trust boundary; a usability evaluation may reveal that an alternative is not equivalent; a fault exercise may expose correlated recovery failure. Prefer an experiment whose possible results would change the decision.

**Consider reversibility and option value.** A feature flag, adapter, dual-read migration, bounded pilot, or replaceable provider can reduce cost of learning. These mechanisms add their own complexity and must have owners and removal criteria. Reversibility is not permission to expose users to unacceptable risk.

Use staged commitment when uncertainty is reducible: choose a safe feasible candidate, instrument the disputed response, limit exposure, state stop conditions, and decide again at a named date. When uncertainty cannot be reduced locally, escalate to the authority that owns the consequence.

**Negotiate with decision rights.** Stakeholders contribute needs and evidence, but not every person has authority over every risk. Identify who owns product outcomes, security acceptance, privacy obligations, safety, accessibility, operations, budget, and affected communities. Record disagreements and absent representation. Facilitation is not consent, and consensus is not proof.

Error-budget policies illustrate a governed rule for one recurring conflict: when observed reliability is within the stated budget, change may proceed; when the budget is exhausted, policy redirects work toward reliability. The published Google SRE example explicitly frames this as balancing reliability with feature velocity, with declared exceptions and escalation [7]. It is an example policy, not a universal threshold.

**Record and re-open.** The decision record should contain scenario IDs, constraints, candidates, evidence, uncertainty, decision rights, selected option, rejected alternatives, consequences, residual risk, implementation responsibilities, expiry, and triggers. Triggers can include load growth, budget exhaustion, incident class, threat change, supplier degradation, user evidence, regulation, cost threshold, or loss of rollback.

A decision is resolved when responsibility and action are clear—not when uncertainty disappears. Monitor the responses that justified selection. If observations cross a trigger or an assumption fails, return to the candidate set rather than defend the historical choice.

## Definitions and Notation

Let $D$ be a finite candidate set and $H=\{h_1,\ldots,h_r\}$ be hard predicates. The feasible set is

$$
F=\{d\in D:\forall j\in\{1,\ldots,r\},\ h_j(d)=true\}.
$$

Let $z(d)=(z_1(d),\ldots,z_m(d))$ be modeled losses for a common scenario set, so smaller is better. For $a,b\in F$, define weak dominance

$$
a\preceq b\iff \forall i,\ z_i(a)\le z_i(b).
$$

Candidate $a$ strictly dominates $b$ when $a\preceq b$ and $z_k(a)<z_k(b)$ for at least one $k$. The modeled Pareto set is

$$
P=\{d\in F:\nexists a\in F\text{ such that }a\text{ strictly dominates }d\}.
$$

These relations are conditional on scenarios, measurements, direction, and uncertainty. Equality within measurement resolution should not be reported as superiority.

For an optional value model, $y_i(d)$ is a measured response, $u_i$ maps it to a declared value scale, and $w_i$ is an accountable trade weight:

$$
U(d)=\sum_{i=1}^{m}w_i u_i(y_i(d)),\qquad \sum_iw_i=1.
$$

Define local sensitivity of a score to weight $w_k$ between candidates $a$ and $b$ by

$$
\Delta_k(a,b)=u_k(y_k(a))-u_k(y_k(b)).
$$

A large $|\Delta_k|$ means ranking can be sensitive to that weight, but this derivative-like comparison does not validate the utility functions or compensate for missing objectives.

## Mechanisms, Invariants, or Proof Structure

Use this conflict-resolution mechanism.

1. **Frame:** identify decision scope, owners, deadline, reversibility, and authoritative constraints.
2. **Scenario:** write paired normal, boundary, degraded, recovery, adversarial, and change scenarios as applicable.
3. **Map:** trace each candidate decision through mechanisms to response measures and affected stakeholders.
4. **Generate:** include distinct mechanisms, baseline, defer option, migration, rollback, and operational ownership.
5. **Constrain:** reject candidates that violate a hard predicate under relevant conditions.
6. **Measure:** gather claim-appropriate analysis, model, test, prototype, exercise, observation, and qualified review.
7. **Compare:** retain raw vectors, uncertainty, distribution, operational work, and residual risk; eliminate demonstrated dominance.
8. **Challenge:** vary assumptions, weights, workloads, threats, failures, populations, prices, and evidence confidence.
9. **Decide:** use named authority to select, defer, experiment, or escalate; record dissent and affected parties.
10. **Govern:** implement controls, monitor responses, enforce stop conditions, and reopen on declared triggers.

The governing invariants are scenario comparability, constraint preservation, causal traceability, visible units and uncertainty, distributional accountability, evidence proportional to consequence, explicit decision rights, reversible learning where safe, residual-risk ownership, and lifecycle reopening.

Pareto elimination has a modest logical guarantee: relative to the included objectives and exact observations, selecting a strictly dominated candidate cannot improve any modeled objective. It does not prove that a nondominated candidate is acceptable, because constraints may be incomplete, evidence uncertain, objectives omitted, and authority unresolved.

## Alternatives and Trade-Offs

**Constraint-first Pareto analysis** keeps non-compensable boundaries visible and avoids arbitrary aggregation. It may leave several incomparable candidates. **Weighted utility** can expose preferences and support sensitivity analysis, but its scales and weights demand legitimate ownership and can hide distribution and thresholds.

**Analytical models** are cheap, explainable, and useful before implementation. Their queue, failure, workload, and independence assumptions may be wrong. **Prototypes and experiments** observe behavior in a bounded environment but can omit rare failures, real users, attackers, and long-term operation. Use each to challenge the other.

**Central architecture decisions** can resolve cross-system constraints consistently. They risk distant context and queues. **Team-local decisions** exploit domain knowledge and speed but can externalize dependency, security, data, and operational costs. Assign decision scope to the smallest authority that owns all material consequences.

**Permanent optimization** reduces ongoing mechanism complexity when the future is known. **Reversible staged commitment** buys information but carries dual-running, compatibility, monitoring, and cleanup cost. Treat optionality as an investment with an expiry, not free flexibility.

**Consensus** can improve commitment and uncover knowledge. It can suppress dissent or exclude affected people. **Explicit decision authority** prevents deadlock but can ignore expertise. Use inclusive evidence gathering, then make authority and dissent transparent.

## Failure Modes and Misconceptions

- **“Every quality conflicts with every other.”** Many tactics are complementary; demonstrate the causal interaction.
- **“The attributes are too subjective to measure.”** Scenarios can define bounded responses even when value judgments remain.
- **“The highest weighted score is objectively best.”** Value functions, weights, omissions, and authority shape the result.
- **“A safety or legal requirement can receive a very high weight.”** A mandatory boundary belongs in feasibility constraints.
- **“The Pareto frontier selects the architecture.”** It only removes modeled dominance and preserves incomparable options.
- **“More candidates always improve the decision.”** Redundant variants add noise; seek materially different mechanisms.
- **“Average response is enough.”** Tails, failures, subgroups, and critical windows can carry the consequence.
- **“Component optimization composes.”** Queues, retries, dependencies, consistency, and user workflow can reverse local gains.
- **“Operational effort is implementation detail.”** On-call load, cognitive demand, recovery, and coordination are quality consequences.
- **“Security always defeats usability.”** Better identity and recovery design can improve both; inspect the specific threat and task.
- **“An experiment makes the decision empirical.”** It supports only the tested environment, population, workload, and claim.
- **“Consensus transfers accountability.”** Named authorities still own duties and residual risk.
- **“Reversible means safe.”** Exposure can cause irreversible user, financial, privacy, or safety harm.
- **“A decision record closes the issue.”** Evidence and assumptions can expire; reopening is part of governance.

## Worked Examples

### Example 1

**Question:** A product-price cache offers candidates A: 900 ms and 0 seconds staleness, B: 430 ms and 4 seconds staleness, and C: 300 ms and 60 seconds staleness. Requirements are latency at most 500 ms and staleness at most 5 seconds. Which candidate is feasible?

**Reasoning:** A violates latency. C violates freshness. B satisfies both predicates. Before selecting B, test invalidation loss, cold-cache behavior, origin overload, clock meaning, and whether the observations cover peak and recovery scenarios. B's feasibility is conditional, not a universal guarantee.

**Conclusion:** Apply constraints before admiring an isolated improvement.

### Example 2

**Question:** Encryption adds 0.4 ms to a 120 ms request. Must security and performance be treated as a material conflict?

**Reasoning:** The measured increase is $0.4/120\approx0.00333=0.33\%$. Compare it with latency variance, percentile budget, CPU saturation, key-service failure, and the protection scenario. If the end-to-end objective still passes with margin, the interaction exists but is not a decision-driving conflict. Removing protection would create a false dichotomy.

**Conclusion:** Magnitude, condition, and consequence determine whether a tension is material.

### Example 3

**Question:** Three immediate retries appear to increase availability. What competing response must be analyzed?

**Reasoning:** With 1,000 original calls, three retries permit up to 4,000 attempts. During correlated dependency failure, that fourfold demand can deepen overload, extend queues, and reduce overall success. Bound attempts with deadlines, exponential backoff and jitter, capacity-aware retry budgets, circuit breaking, and idempotent operation identity. Test correlated failure rather than only independent transient errors.

**Conclusion:** A local recovery tactic can reduce system availability through load amplification.

### Example 4

**Question:** Batch sizes 10, 100, and 1,000 yield throughput 80, 500, and 700 items/s, with worst wait before dispatch of 0.1, 1, and 10 seconds. How should the choice be framed?

**Reasoning:** Larger batches improve throughput with diminishing gain while increasing wait and failure replay scope. If throughput must be at least 450 items/s and wait at most 2 seconds, size 100 is feasible; size 10 misses throughput and size 1,000 misses wait. Also evaluate memory, partial failure, duplicate handling, and traffic variability.

**Conclusion:** A quality conflict becomes tractable when response thresholds expose a feasible region.

### Example 5

**Question:** Global replication improves regional continuity but places personal data in a prohibited jurisdiction. Can availability compensate through a score?

**Reasoning:** No. Data-location authority is a hard predicate for the relevant records. Reject the candidate, then consider permitted regional cells, encrypted minimal replicas, stateless failover, redacted recovery data, or an explicitly degraded mode. Qualified privacy and legal authorities must determine the actual boundary.

**Conclusion:** Non-compensable obligations shape the candidate set before optimization.

### Example 6

**Question:** Engineers want full request bodies in traces to improve diagnosis. What resolution avoids “observability versus privacy” as a slogan?

**Reasoning:** Identify diagnostic questions and fields actually needed. Prefer stable operation IDs, structured error categories, allowlisted attributes, redaction before export, protected access, short retention, and auditable break-glass detail. Evaluate diagnostic success and incident time against collection purpose, exposure, access, deletion, cardinality, and loss behavior.

**Conclusion:** Redesigning the evidence mechanism can improve useful observability without collecting unnecessary content.

### Example 7

**Question:** A banking session expires after five minutes for security, but a customer using assistive technology needs fifteen minutes to review a transfer. What should the architecture do?

**Reasoning:** Separate unattended authorization validity from recoverable draft state and final side effect. Warn accessibly, allow governed extension, preserve a protected unsigned draft, reauthenticate before commitment, show authoritative state, and retain stable submission identity. Evaluate shared-device exposure, stolen sessions, duplicate transfer, privacy, focus, and accessible recovery.

**Conclusion:** Decomposing session, draft, and commitment states can preserve both protection and accessible control.

### Example 8

**Question:** Two candidates have normalized values: A has performance 0.9 and modifiability 0.4; B has 0.7 and 0.8. Which wins a weighted score?

**Reasoning:** With weights $(0.6,0.4)$, $U(A)=0.6(0.9)+0.4(0.4)=0.70$ and $U(B)=0.6(0.7)+0.4(0.8)=0.74$, so B ranks higher. With weights $(0.8,0.2)$, A scores $0.80$ and B scores $0.72$, reversing the result. The scales and weights require justification; neither candidate dominates the other.

**Conclusion:** Sensitivity analysis exposes that a score expresses policy rather than discovering a fact.

### Example 9

**Question:** For losses (latency ms, monthly cost units, recovery minutes), A=(400,80,20), B=(450,90,30), and C=(350,120,15). Which candidate is dominated?

**Reasoning:** A is better than B on all three losses, so A strictly dominates B. C improves latency and recovery over A but costs more; A and C are incomparable. Uncertainty or an omitted objective could change the model, but without such evidence B should be removed.

**Conclusion:** Dominance eliminates avoidable loss while preserving genuine trade-offs.

### Example 10

**Question:** How should conflicts be resolved for a regional medical-dispatch platform balancing response time, confidentiality, continuity, accessibility, and operator workload?

**Reasoning:** Define emergency and routine scenarios, safety and privacy constraints, dispatch deadlines, degraded communication, accessible operator and public paths, location authority, clinical data minimization, regional failure, manual control, and recovery. Compare cellular, radio, offline, and assisted mechanisms; simulate load and selected faults; conduct human-factors exercises; record uncertainty and stop conditions. No external medical, emergency-services, accessibility, privacy, telecommunications, safety, security, human-factors, or practitioner review is claimed. Named qualified authorities and affected operators and communities must validate constraints, exercises, release, and residual risk.

**Conclusion:** High-consequence resolution requires constraint-first, multidisciplinary evidence and explicit authority.

## Cross-Program Connections

- [Software Engineering: Methods & Evolution](../../10-software-engineering-methods-and-evolution/ROADMAP.md) owns stakeholder discovery, iterative planning, negotiation, and lifecycle change.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns discriminating test design, measurement validity, uncertainty, and evaluation evidence.
- [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns SLOs, error budgets, deployment controls, production feedback, and incident learning.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns threat analysis, protection needs, security controls, and security-risk evidence.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) owns requirements conflict, system trades, lifecycle assurance, physical constraints, and qualified authority.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns consumer-facing protocol decisions whose latency, compatibility, retry, error, and security effects enter architectural trade-offs.

## References

1. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*, 4th edition. Addison-Wesley, 2021. Quality attributes, tactics, scenarios, trade-offs, and architecture evaluation.
2. ISO/IEC. [ISO/IEC 25010:2023, Systems and software engineering—Systems and software Quality Requirements and Evaluation (SQuaRE)—Product quality model](https://www.iso.org/standard/78176.html), edition 2, November 2023. Current product-quality reference model; consulted 2026-09-06.
3. Rick Kazman, Mark H. Klein, Mario R. Barbacci, Thomas A. Longstaff, Howard F. Lipson, and Jeromy Carriere. [The Architecture Tradeoff Analysis Method](https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/), CMU/SEI-98-TR-008, July 1998. Quality scenarios, risks, sensitivity points, trade-off points, and iterative evaluation; consulted 2026-09-06.
4. Paul Clements, Rick Kazman, and Mark Klein. *Evaluating Software Architectures: Methods and Case Studies*. Addison-Wesley, 2002. Architecture evaluation, stakeholder participation, scenarios, and evidence.
5. Ralph L. Keeney and Howard Raiffa. *Decisions with Multiple Objectives: Preferences and Value Tradeoffs*. Cambridge University Press, 1993. Multi-objective value models, preference structure, and sensitivity.
6. Ron Ross, Mark Winstead, and Michael McEvilley. [NIST SP 800-160 Volume 1 Revision 1, Engineering Trustworthy Secure Systems](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final), November 2022. Protection needs, trustworthy-system engineering, assurance, and lifecycle trades; consulted 2026-09-06.
7. Steven Thurgood. [Example Error Budget Policy](https://sre.google/workbook/error-budget-policy/), *The Site Reliability Workbook*, 2018. An explicit policy for balancing service reliability and change velocity; consulted 2026-09-06.

## Exercises

### Exercise 1

Distinguish a tension, conflict, constraint, sensitivity point, and trade-off point using one content-delivery cache decision.

### Exercise 2

Candidates have losses A=(8,5,9), B=(8,7,10), C=(10,4,6), and D=(7,8,8), where dimensions are latency, cost, and recovery loss and smaller is better. Identify dominated candidates and the modeled Pareto set.

### Exercise 3

Diagnose a proposal that selects global synchronous replication because it has the highest weighted score, while omitting jurisdiction, correlated failure, tail latency, operator workload, migration, rollback, evidence intervals, and decision authority.

### Exercise 4

Design a conflict-resolution process for choosing between a modular monolith and independently deployed services. Address scenarios, constraints, candidates, evidence, team structure, operational cost, reversibility, and reopening.

### Exercise 5

Resolve quality conflicts for an unfamiliar floodgate-control system. Separate safety constraints, performance, availability, security, operability, accessibility, cost, evidence, qualified authority, and readiness blockers.

## Answers to the Exercises

### Answer 1

A possible **tension** is that a longer cache TTL may improve latency but harm freshness; it remains suspected until workload and invalidation mechanisms are analyzed. A **conflict** exists for a declared scenario if measured candidates cannot meet both the latency and freshness responses. A **constraint** might require emergency notices to be no more than five seconds old. TTL is a **sensitivity point** when freshness changes strongly with it. It is a **trade-off point** when changing it improves hit latency or origin capacity while worsening freshness or deletion propagation.

The classifications depend on context. Event invalidation might dissolve the TTL conflict but create new availability and operational interactions. Record cache population, workload, failure, invalidation loss, observation points, user consequences, and evidence uncertainty.

### Answer 2

A=(8,5,9) strictly dominates B=(8,7,10): A is equal or lower on every loss and lower on cost and recovery loss. No candidate dominates A because C improves cost and recovery but worsens latency, while D improves latency but worsens cost. C and D do not dominate each other. Therefore the modeled Pareto set is $\{A,C,D\}$ and B should be eliminated.

This conclusion assumes exact comparable observations and complete objectives. With uncertainty intervals, different scenarios, a missing objective, or a hard constraint, the result may change. Pareto membership does not establish acceptability or select among A, C, and D.

### Answer 3

The weighted score improperly begins before feasibility and hides its value scales, weights, and distributions. Data-location or other jurisdictional duties may reject global replication regardless of score. Synchronous coordination can add tail latency and fail under partition; replicas can share software, identity, network, or operational failure. Operator workload, incident coordination, exposure, migration, rollback, and exit cost are material responses.

Reframe normal, peak, partition, region-loss, recovery, attack, data-subject, and change scenarios. Establish authoritative constraints, generate permitted topology candidates, measure with intervals, test correlated faults and recovery, analyze threats and data flows, estimate lifecycle work, and identify decision rights. Keep raw objective vectors and residual risks. Select, stage, or escalate only after qualified legal, privacy, security, reliability, product, and operational review appropriate to the actual system.

### Answer 4

Define change scenarios, team ownership, workload, latency, availability, consistency, security, test, deployment, incident, and cost outcomes. Hard constraints may include data integrity, access control, recovery, regulatory boundary, and support capacity. Candidates should include a well-modularized monolith, a few independently deployed boundaries, and finer services only where distinct ownership and release needs justify them.

Measure dependency and change coupling, build and test time, deployment coordination, call and queue behavior, failure amplification, recovery, observability, security surface, and on-call load. Include current team skills and organizational communication without assuming the architecture must mirror today's chart. A modular monolith is often more reversible initially; extraction seams, versioned contracts, and data ownership can preserve options. Record why a boundary is selected, how migration and rollback work, what evidence is missing, and triggers such as sustained independent release demand, scaling isolation, incidents, or coordination cost. Evaluate observed outcomes after adoption rather than declaring either style universally superior.

### Answer 5

Treat safe water-level bounds, fail-safe physical behavior, authorized actuation, local manual control, and protection against hazardous commands as constraints owned by qualified safety and control authorities. Define response deadlines, sensor validity, power and network loss, stuck mechanisms, conflicting commands, cyberattack, maintenance, flood conditions, evacuation, accessible alarms, operator workload, and recovery. Compare local autonomous control, supervised remote control, redundant sensing, diverse communications, mechanical protection, and degraded modes.

Use hazard analysis, control models, timing analysis, threat analysis, independent protection review, hardware-in-the-loop tests, selected fault injection, manual drills, accessibility evaluation, recovery exercises, and configuration audits. Preserve provenance, command authority, clock validity, interlocks, safe state, bounded automation, offline procedures, and tamper-evident records. Cost may distinguish candidates only inside the safe feasible set.

No external hydrology, civil-engineering, control-systems, emergency-management, accessibility, environmental, safety, regulatory, security, human-factors, or practitioner review is claimed. Named qualified authorities and affected operators and communities must approve assumptions, hazards, constraints, tests, operating procedures, release, and residual risk. Unknown safe bounds, unverified interlocks, inaccessible alarms, ambiguous command authority, failed manual control, unresolved correlated failure, or absent emergency procedures blocks readiness.
