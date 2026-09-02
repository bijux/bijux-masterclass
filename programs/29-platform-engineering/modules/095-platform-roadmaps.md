---
module_id: PLAT-095
program: Platform Engineering
level: 2
module_number: 95
title: Platform Roadmaps
status: complete
last_verified: 2026-09-02
---

# Platform Roadmaps

## One-Page Review

### Governing question

How should platform leaders turn strategy, user evidence, capability health, obligations, dependencies and finite capacity into a revisable sequence of outcomes without disguising uncertainty as committed features and dates?

### Essential definitions

- A **platform roadmap** is a versioned decision model that communicates intended outcomes, the problems and obligations behind them, their relative order, confidence, dependencies, evidence and conditions for change.
- An **outcome** is an observable change in user, service or organizational performance; an **output** is an artifact or capability delivered in pursuit of that change.
- A **roadmap item** is a bounded decision record containing an outcome or obligation, affected users, evidence, hypothesis, owner, horizon, confidence, dependencies, guardrails and next review.
- A **horizon** groups decisions by temporal distance and confidence, such as now, next and later; it is not a hidden release-date commitment.
- A **commitment** is work whose date or scope has been explicitly accepted by authorized owners under stated assumptions; an **intent** remains conditional.
- An **obligation** is work required to sustain safety, reliability, security, compliance, support, migration or retirement even when it does not create a visible feature.
- **capacity allocation** reserves scarce qualified effort among discovery, capability delivery, reliability, security, migration, support, toil reduction and interrupts.
- A **dependency** is a condition outside an item that must hold for its safe progress or outcome; sequencing merely because one item is nearby is not dependency evidence.
- A **decision trigger** is evidence or an event that causes an item to advance, stop, split, reorder or leave the roadmap.
- A **roadmap guardrail** is a limit that an intended outcome must not violate, such as error-budget, cost, accessibility, security or team-health bounds.

### Central model, mechanism, or theorem

For candidate item $i$, define expected outcome value $V_i$, confidence $q_i\in[0,1]$, time-criticality $T_i$, obligation weight $O_i$, risk reduction $R_i$, qualified capacity demand $C_i$, dependency readiness $D_i\in\{0,1\}$ and guardrail feasibility $G_i\in\{0,1\}$. A transparent comparison may use

$$
P_i=D_iG_i\frac{q_iV_i+T_i+O_i+R_i}{C_i},
$$

but no score owns the decision. Mandatory obligations, coupled dependencies, option value, distributional effects and capacity by skill must remain visible. A roadmap is valid only while its assumptions and evidence remain current; delivery of every named output cannot prove that its outcomes occurred.

### Critical invariants

- Every item traces to a user or service outcome, a mandatory obligation, or an explicit learning decision, with an owner and supporting evidence.
- Horizon, confidence, date semantics, assumptions and next review are visible; an intent is never silently presented as a commitment.
- Reliability, security, compliance, migration, retirement, support, accessibility and toil work compete in the same portfolio rather than disappearing beneath feature demand.
- Dependencies, qualified capacity, operational headroom and work-in-progress limits make the selected sequence feasible; personal overtime is not capacity.
- Outcome and guardrail evidence can stop or reorder work; sunk cost, executive sponsorship and output completion cannot exempt an item from review.
- Platform adoption remains voluntary wherever risk permits, alternatives and exit paths stay credible, and roadmap power cannot create an unaccountable internal monopoly.

### Common failures

Feature lists relabeled as strategy; quarterly dates treated as guarantees; commitments mixed with aspirations; executive requests bypassing discovery; adoption targets masking coercion; reliability and retirement work hidden; capacity planned at full utilization; dependencies represented as decorative arrows; ten top priorities; discovery used to validate a chosen solution; output counts substituted for outcomes; changing the roadmap considered failure; stale versions circulating; users invited only after sequencing; security used as an unchallengeable label; platform teams owning application outcomes they cannot control; and roadmaps that never stop low-value work.

### Compact example

A platform team’s objective is safer, faster production change. Research shows that deployment feedback, identity setup and restore evidence are the dominant journey constraints. The roadmap records three outcome hypotheses, a mandatory restore obligation, dependency order, 12 units of qualified capacity, a two-unit interrupt reserve and error-budget and support-load guardrails. Identity preview precedes deployment feedback because the latter consumes the former’s contract; restore evidence proceeds independently. A portal theme remains in later because its value evidence is weak. The published view distinguishes a committed regulatory date from conditional horizons. Monthly reviews compare journey time, change failure, restore proof, adoption by eligible cohort, support load and cost. When the identity preview fails an accessibility test, dependent rollout pauses; scope and dates change while the governing outcome remains stable.

### Connections

Platform roadmaps consume discovery, funnel, migration, reliability, fleet, cost, security and support evidence from PLAT-081–094. They provide the decision history and capacity model needed for build-versus-buy, lifecycle governance, outcome measurement, strategy defense, autonomy and anti-monopoly review in PLAT-096–100.

## Governing Question

Which platform outcomes and obligations deserve scarce capacity now, which options should be explored next, which ideas should remain later or stop, and what evidence justifies changing that order?

A good answer cannot be a calendar of components. Platform work changes the constraints experienced by many teams, so a locally small item may have large systemic effects. Conversely, a highly visible portal feature may produce no improvement in a critical journey.

The roadmap must serve several audiences without creating several truths. Users need credible intent and contribution paths. Delivery teams need sequence, constraints and decision boundaries. Operators need reliability headroom. Security and compliance owners need explicit obligations. Finance and executives need investment logic and outcome evidence. One canonical model may generate audience-specific views, but the underlying state and semantics remain shared.

## Why This Matters

Platforms accumulate demand faster than capacity. Every application team can name a useful capability, and every shared component creates maintenance, support, migration and retirement obligations. Without portfolio discipline, the loudest request wins while invisible risk compounds.

Uncertainty increases with distance. Near-term work may have validated problems, staffed owners and resolved dependencies. Later work is often an option based on incomplete learning. Exact dates on both create false precision, encourage local plans to depend on speculation and make honest adaptation look like failure.

Roadmaps shape behavior. If they reward launches, teams optimize for shipping. If they expose journey outcomes and guardrails, teams can discover cheaper solutions, improve existing contracts or stop. If adoption is the sole outcome, platform teams may force migration and count captive users as product success.

Operational work must be made legible. Error budgets, vulnerabilities, unsupported versions, recovery gaps, toil and expiring contracts compete for the same specialists as new capabilities. Hiding them does not remove their cost; it transfers risk into incidents and interrupts.

A roadmap also allocates trust. Stakeholders tolerate change when they can see why an item existed, which evidence changed, who decided and what happens next. A polished static slide without provenance cannot provide that accountability.

## Prerequisites and Retrieval

Retrieve the platform strategy and non-goals; user segments, critical journeys and research; capability catalog and lifecycle state; adoption and retention cohorts; service SLOs, error budgets, incidents and recovery evidence; security threats, vulnerabilities and compliance dates; support demand and toil; migrations, deprecations and vendor end-of-life notices; cost and unit economics; architectural dependencies and interface owners; team skills, leave and on-call load; existing commitments, contracts and regulatory obligations; product-team roadmaps; accessibility and data-governance constraints; and prior roadmap decisions with forecasts and actual outcomes.

Distinguish strategy from roadmap; outcome from output; problem from requested solution; obligation from optional feature; evidence from opinion; discovery from delivery; dependency from preference; sequence from date; horizon from release train; confidence from probability theater; intent from commitment; target from forecast; eligible adoption from coerced usage; capacity from headcount; utilization from sustainable throughput; urgency from seniority; option from promise; guardrail from objective; change from failure; cancellation from waste; and one canonical roadmap from one universal presentation.

## Learning Objectives

After completing this module, you should be able to:

1. translate platform strategy, non-goals and user evidence into outcome-oriented roadmap items;
2. distinguish obligations, experiments, options, intentions, forecasts and authorized commitments;
3. model horizon, confidence, assumptions, dependencies and decision triggers without false date precision;
4. allocate qualified capacity across discovery, delivery, reliability, security, migration, support and interrupts;
5. sequence coupled platform capabilities while limiting work in progress and preserving operational headroom;
6. prioritize transparently without delegating judgment to a score or rewarding organizational influence;
7. publish useful stakeholder and user views from one canonical, versioned decision record;
8. connect outputs to outcome measures and guardrails that can stop or reorder investment;
9. govern adoption without coercion, lock-in or a platform monopoly; and
10. review, revise and retire roadmap items with an auditable explanation of changed evidence.

## Core Exposition

### Begin with strategy and non-goals

State the platform’s intended contribution to organizational outcomes and the boundaries of that contribution. “Reduce the effort and risk of operating production services” guides choices; “build a developer portal” prematurely selects an output.

Define non-goals. A platform may standardize production evidence while declining to own application business logic. Boundaries keep the roadmap from becoming a collection of every engineering improvement.

Trace strategy through a small set of measurable outcome themes. Each theme should name affected users, present condition, desired change, guardrails and accountable sponsor.

### Discover problems before selecting solutions

Combine interviews, observation, journey telemetry, support evidence, incident analysis and service data. Requests are evidence of perceived need, not automatically the right solution.

Frame problems in user context: who is trying to achieve what, under which constraints, with what consequence? Quantify a baseline where possible and retain contradictory evidence.

Use discovery to test whether intervention is worthwhile and what class of response might work. A documentation change, policy clarification or removal of a broken capability may dominate a new service.

### Build a capability and obligation map

Map capabilities to critical journeys, owners, lifecycle, consumers, dependencies and operational health. This prevents a roadmap from treating every capability as greenfield delivery.

Add obligations: reliability deficits, restore tests, access reviews, vulnerabilities, audit evidence, data retention, vendor expiry, unsupported versions, migrations and retirement. Give each a consequence and latest responsible decision point.

Avoid a separate “technical roadmap” whose work becomes negotiable whenever feature pressure rises. Different views may exist, but obligations and product opportunities share one constrained portfolio.

### Write outcome-oriented items

Record an outcome or learning objective, not merely a noun. “Eligible teams can diagnose policy denials without intervention” is testable; “policy dashboard” is an output.

Include affected segments, problem evidence, baseline, hypothesis, possible interventions, owner, horizon, confidence, dependencies, capacity range, risks, guardrails, decision trigger and next review.

Keep solution flexibility proportional to uncertainty. Near execution, interfaces and acceptance evidence become specific. In later horizons, premature detail creates anchoring and accidental commitments.

### Separate item classes

Label mandatory obligations, outcome bets, discovery options, maintenance, migrations and retirement. They use different evidence and stopping rules.

A regulatory obligation may have a committed deadline but flexible implementation. An experiment may have fixed time and capacity but no promised rollout. A later option preserves learning without reserving delivery capacity.

Do not hide executive requests. Record sponsor, rationale and decision authority, then subject implementation to feasibility, guardrails and outcome evidence.

### Define date and confidence semantics

Use explicit fields such as committed date, target window, forecast range and review date. A quarter label alone is ambiguous.

Confidence should reflect problem evidence, solution evidence, dependency readiness, capacity and operational state. Avoid a single unexplained percentage that implies a precision the evidence cannot support.

Increase detail as decisions approach. Publish uncertainty in plain language, including assumptions that could move the forecast.

### Map real dependencies

Classify contract, data, identity, infrastructure, vendor, policy, staffing and learning dependencies. Name owner, required condition, evidence, lead time and fallback.

Distinguish hard dependencies from advantageous sequencing. Challenge circular plans and a foundational program that delays all user value.

Use thin vertical outcomes to break chains. A preview for one eligible cohort may test identity and feedback contracts before fleet-wide automation exists.

### Model qualified capacity

Capacity is not headcount multiplied by weeks. Subtract on-call, support, leave, coordination and interrupt reserves, then model scarce skills and authority.

Allocate explicit bands for discovery, outcome delivery, reliability/security obligations, migrations/retirement, toil reduction and interrupts. Bands are governance choices, not universal ratios.

Compare capacity ranges with historical throughput and interruption. If demand exceeds supply, change sequence, scope or promise; do not make overtime the hidden balancing variable.

### Limit work in progress

Too many concurrent platform initiatives multiply dependencies, cognitive load, half-supported interfaces and adoption campaigns. Set portfolio WIP limits by team and capability lifecycle.

Finish or stop learning loops before starting new bets. Protect small discovery probes, but do not let every probe turn into an unowned preview.

Count operationalization and adoption work as work in progress. Code completion does not free capacity while documentation, migration and support remain unfinished.

### Compare candidates transparently

Use common dimensions: outcome value, reach, confidence, time-criticality, risk reduction, obligation, effort, reversibility and strategic fit. Show evidence and disagreement.

Scores can expose assumptions and support sensitivity analysis. They cannot compare incomparable harms, determine ethics, satisfy mandatory obligations or manufacture evidence.

Run portfolio scenarios rather than sorting one spreadsheet. Test what changes under capacity loss, an incident, a regulatory deadline, dependency delay or weak adoption evidence.

### Sequence for learning and value

Prefer sequences that retire the largest uncertainty or deliver a bounded user outcome early. Preserve option value when a large irreversible investment has weak evidence.

Coordinate migrations with support and consuming-team capacity. A technically feasible platform schedule can still be impossible for its users.

Place reliability prerequisites before scale when failure cost grows with adoption. Conversely, do not require hypothetical enterprise completeness before learning from a safe preview.

### Make commitments deliberately

Define who can accept date, scope, cost and risk commitments. Record assumptions, tolerance and consequences of change.

Commit to an outcome or obligation where possible, leaving implementation adaptable. When an external contract requires a deliverable, state that constraint honestly.

Do not let a roadmap presentation create commitments by implication. Meeting notes and change history should capture decisions explicitly.

### Publish one canonical state

Maintain a structured source containing identifiers, item class, outcome, evidence, horizon, status, owner, confidence, dependencies, dates, guardrails and review history.

Generate different views for users, teams, executives and risk owners. Redact genuine security-sensitive detail, but do not use sensitivity as a blanket excuse for opacity.

Mark freshness and maintainer. Archive prior versions so changed intent can be understood without allowing obsolete screenshots to masquerade as current state.

### Invite participation without transferring ownership

Provide contribution routes for problem evidence, corrections, proposals and dependency changes. Close the loop on decisions.

Engage product teams before prioritization, not only before rollout. Seek silent, blocked and non-adopting users, not just platform champions.

The platform product owner remains accountable for coherent decisions. Voting alone rewards group size and cannot resolve safety or cross-system trade-offs.

### Measure outcomes and guardrails

Pair each intended outcome with baseline, target direction, observation window, segmentation and data owner. Use leading and lagging evidence.

Measure eligible journey success, time, failure and recovery; adoption and retention by cohort; service reliability; support and toil; cost; accessibility; security; and consuming-team effects.

Guardrails reveal displacement. Faster deployment is not success if change failure, cognitive load, privilege or cost becomes unacceptable.

### Establish review and change control

Review operational signals continuously, near-horizon decisions frequently and strategy periodically. Cadence does not replace event-driven triggers.

At each review, record new evidence, assumption changes, dependency state, capacity, forecast, decision and owner. Recompute portfolio effects rather than moving one card in isolation.

Communicate what changed, why, who is affected and what users should do. Versioning makes adaptation credible rather than silent.

### Stop, split and reorder work

Define stopping rules before investment: invalidated problem, guardrail breach, cost beyond tolerance, inaccessible dependency, better alternative or insufficient adoption outcome.

Stopping prevents future waste even when past cost is unrecoverable. Preserve useful learning, contracts and retirement obligations; do not abandon consumers of a preview.

Split large items when learning and value can be independently demonstrated. Reorder when evidence changes, while protecting true commitments through explicit governance.

### Prevent coercion and monopoly

Define eligible adoption and permitted exceptions. Adoption should reflect improved user outcomes, not removal of every alternative before fitness is demonstrated.

Publish service levels, contribution governance, portability, data export, escape paths and appeal. Review whether platform authority can set policy, enforce migration and judge its own performance without independent challenge.

Count transferred cost and local work. A roadmap that centralizes visible capability while exporting integration toil has not necessarily improved the system.

### Link the roadmap to execution

Roadmap outcomes decompose into discovery and delivery backlogs; backlogs do not replace roadmap decisions. Teams retain freedom to learn and implement within guardrails.

Use readiness gates for entry into active delivery: owner, evidence, dependency plan, capacity, operational model, measurement and exit criteria.

Feed delivery discoveries back to forecasts and portfolio decisions. A roadmap that cannot change from execution evidence is theater.

## Definitions and Notation

Let $I$ be the set of candidate roadmap items and $S\subseteq I$ the selected portfolio. For item $i$, let $V_i$ be expected outcome value, $q_i\in[0,1]$ evidence confidence, $T_i$ time-criticality, $O_i$ obligation weight, $R_i$ risk reduction and $C_i>0$ qualified capacity demand.

Let $D_i$ indicate dependency readiness and $G_i$ guardrail feasibility. A diagnostic comparison score is

$$
P_i=D_iG_i\frac{q_iV_i+T_i+O_i+R_i}{C_i}.
$$

The score does not authorize a decision. Mandatory set $M\subseteq I$, hard-dependency relation $E\subseteq I\times I$, skill demand $c_{i,k}$ and available capacity $B_k$ produce constraints

$$
M\subseteq S,\qquad (j,i)\in E\land i\in S\Rightarrow j\in S,\qquad \sum_{i\in S}c_{i,k}\le B_k.
$$

For outcome $o$, record baseline $b_o$, intended direction or target $t_o$, observation window $W_o$ and guardrail vector $g_o$. Let roadmap version $R^v$ contain evidence snapshot $E^v$, decisions $A^v$, assumptions $H^v$ and timestamp $\tau_v$. A decision is auditable when the transition $R^v\rightarrow R^{v+1}$ identifies which evidence or assumption changed and who accepted the consequence.

## Mechanisms, Invariants, or Proof Structure

### Twelve-step roadmap mechanism

1. Reaffirm platform strategy, non-goals, authority and consuming-user boundaries.
2. Retrieve journey, product, operational, security, cost, lifecycle and support evidence.
3. Map current capabilities, obligations, dependencies, owners and lifecycle risks.
4. Frame outcome, obligation and learning items without prematurely fixing solutions.
5. Record evidence, hypothesis, guardrails, item class, confidence and decision triggers.
6. Estimate qualified capacity and reserve support, incident and recovery headroom.
7. Build feasible portfolio scenarios under dependency, WIP and mandatory constraints.
8. Decide sequence, horizon, date semantics and explicit commitments with accountable owners.
9. Publish audience-appropriate views from one versioned canonical state.
10. Execute bounded discovery and delivery while measuring outcomes and guardrails.
11. Review evidence and trigger continuation, split, stop, reorder, migration or retirement.
12. Record the decision transition and feed learning into strategy, capability and capacity models.

### Traceability invariant

Every item connects to an evidenced user/service outcome, mandatory obligation or explicit learning objective, with an owner, baseline or consequence, and next decision point.

### Semantic invariant

Intent, target, forecast, commitment, horizon and confidence remain distinguishable in storage and presentation; audience-specific views cannot change their meaning.

### Feasibility invariant

Selected work respects hard dependencies, mandatory obligations, skill-specific capacity, operational headroom and WIP limits without relying on hidden overtime.

### Adaptation invariant

New outcome or guardrail evidence can advance, split, stop or reorder work through named authority; output completion and sunk cost confer no immunity.

### Lifecycle invariant

Discovery, delivery, operation, support, migration and retirement costs are represented, and a new capability cannot silently externalize unowned lifecycle work.

### Autonomy invariant

Adoption, exception, portability and appeal remain observable; platform roadmap authority cannot coerce use, eliminate credible exits or judge monopoly harms without challenge.

### Proof sketch: completed outputs cannot prove roadmap success

Construct two roadmap portfolios that each complete ten promised outputs on their published dates. In Portfolio A, eligible users complete critical journeys faster with lower failure and no guardrail breach. In Portfolio B, the outputs are unused, duplicate existing paths and increase support and migration toil. Their output completion counts and schedule conformance are equal while outcomes differ. Therefore completion and schedule alone are insufficient evidence of roadmap success; outcome, guardrail, adoption and transferred-cost evidence are necessary.

### Executable portfolio gate

This synthetic audit checks mandatory coverage, hard dependencies, skill-neutral capacity and distinct outcome groups. It demonstrates deterministic portfolio arithmetic, not a universal prioritization formula.

<!-- bijux-verify: {"id":"roadmap-portfolio-gate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"selected=3\ncapacity=10/12\nmandatory=2/2\ndependency_violations=0\noutcome_groups=3\nheadroom=2\ngate=pass\n"}} -->
```python
items = {
    "identity-preview": {
        "capacity": 3, "dependencies": [], "mandatory": True, "outcome": "access"
    },
    "deployment-feedback": {
        "capacity": 4, "dependencies": ["identity-preview"],
        "mandatory": False, "outcome": "diagnosis"
    },
    "restore-evidence": {
        "capacity": 3, "dependencies": [], "mandatory": True, "outcome": "recovery"
    },
    "portal-theme": {
        "capacity": 2, "dependencies": [], "mandatory": False, "outcome": "appearance"
    },
}
selected = {"identity-preview", "deployment-feedback", "restore-evidence"}
limit = 12
used = sum(items[name]["capacity"] for name in selected)
mandatory = {name for name, item in items.items() if item["mandatory"]}
violations = sum(
    dependency not in selected
    for name in selected
    for dependency in items[name]["dependencies"]
)
outcomes = {items[name]["outcome"] for name in selected}
gate = mandatory <= selected and not violations and used <= limit

print(f"selected={len(selected)}")
print(f"capacity={used}/{limit}")
print(f"mandatory={len(mandatory & selected)}/{len(mandatory)}")
print(f"dependency_violations={violations}")
print(f"outcome_groups={len(outcomes)}")
print(f"headroom={limit - used}")
print(f"gate={'pass' if gate else 'fail'}")
```

### Verification strategy

Sample items back to research, incidents, obligations and strategy; reconcile roadmap owners with catalog and operational ownership; test date semantics with each audience; recompute capacity by skill and interrupt reserve; traverse every hard dependency; compare published views to canonical state; reproduce prioritization sensitivity; inspect stopped and rejected items; trace outputs to segmented outcomes and guardrails; survey silent and non-adopting users; audit exceptions, portability and appeal; and compare past forecasts, changes and actual results without turning forecast error into punishment.

## Alternatives and Trade-Offs

1. Outcome roadmaps preserve solution flexibility but demand stronger measurement and stakeholder fluency.
2. Feature roadmaps are concrete but anchor teams to outputs before value is established.
3. Now-next-later horizons express uncertainty but can conceal capacity unless semantics are explicit.
4. Calendar roadmaps coordinate external events but invite false precision for uncertain work.
5. Public roadmaps support trust and coordination but require security-aware redaction and disciplined freshness.
6. Restricted roadmaps protect sensitive detail but can hide duplication, monopoly power and changed intent.
7. Central prioritization improves portfolio coherence but can suppress local knowledge and autonomy.
8. Federated proposals broaden evidence but require common item contracts and decision authority.
9. Quantitative scoring exposes assumptions but can launder weak evidence and incomparable values.
10. Deliberative judgment handles context but may reward influence unless evidence and dissent are recorded.
11. Fixed capacity bands protect obligations but can become rigid when risk changes.
12. Fully dynamic allocation adapts quickly but may starve long-running reliability and retirement work.
13. Large foundational programs promise consistency but delay learning and concentrate dependency risk.
14. Thin vertical slices produce early evidence but may duplicate temporary integration work.
15. Firm commitments aid dependent planning but transfer uncertainty and raise change cost.
16. Conditional intent preserves options but supplies less certainty to consuming teams.
17. Standardization reduces variation and support cost but may erase legitimate domain constraints.
18. Credible alternatives preserve autonomy but require portability investment and tolerate some duplication.

## Failure Modes and Misconceptions

1. “A roadmap is a feature list with dates” discards outcomes and uncertainty.
2. “Strategy and roadmap are interchangeable” confuses direction with sequencing decisions.
3. “The backlog is the roadmap” replaces portfolio intent with implementation tasks.
4. “Every request belongs on the roadmap” treats demand as validated value.
5. “Executive sponsorship is evidence” confuses authority with user or service proof.
6. “Discovery confirms the proposed solution” removes the learning decision.
7. “Later means committed later” mistakes an option for a promise.
8. “A quarter label has obvious meaning” hides forecast, target and commitment semantics.
9. “Confidence can be one precise percentage” disguises several uncertain dimensions.
10. “Roadmap change shows poor planning” punishes adaptation to evidence.
11. “Never changing proves execution” may prove only that learning is ignored.
12. “All dependencies are technical” misses policy, staffing, vendor and user capacity.
13. “Dependency arrows make a plan feasible” omits owner, state, lead time and fallback.
14. “Headcount is capacity” ignores skills, operations, leave and interrupts.
15. “Full utilization is efficient” removes learning and incident headroom.
16. “Ten top priorities create focus” makes priority meaningless.
17. “Starting proves commitment” allows WIP to grow without completion.
18. “Code complete means capacity is free” ignores rollout, support and retirement.
19. “Reliability work belongs off-roadmap” makes necessary cost invisible.
20. “Security always outranks everything” prevents consequence and alternative analysis.
21. “A score decides objectively” embeds subjective weights behind arithmetic.
22. “The highest-value item goes first” can violate obligations and dependencies.
23. “Output delivery proves outcome” ignores use, effect and displaced cost.
24. “Adoption proves product fit” may count forced or ineligible consumers.
25. “One view fits every audience” either overwhelms users or strips decision evidence.
26. “Multiple decks can be reconciled later” permits incompatible truths.
27. “Public means publishing sensitive architecture” ignores layered views and redaction.
28. “Stopping wastes prior investment” applies sunk cost to future decisions.
29. “Platform ownership includes application outcomes” assigns accountability without control.
30. “Mandatory use makes the platform successful” confuses monopoly reach with value.

## Worked Examples

### Example 1

A portal redesign request becomes a discovery item after research shows users cannot find ownership data. Search and catalog fixes improve journey completion without replacing the portal.

### Example 2

A vulnerability deadline is recorded as a mandatory obligation with a committed date and flexible implementation. A less urgent feature moves rather than hiding the security work in team capacity.

### Example 3

Deployment feedback depends on a stable identity contract. The roadmap makes identity preview a hard dependency, assigns its owner and retains a manual fallback for the first cohort.

### Example 4

A “Q4” label is interpreted three ways. The team replaces it with target window, forecast range, confidence factors and monthly review date.

### Example 5

Five initiatives fit nominal headcount but require the same identity specialist. Skill-specific capacity exposes the infeasible sequence and two items remain next.

### Example 6

Error-budget exhaustion triggers the published guardrail. Scale rollout pauses while recovery automation proceeds, even though adoption is an executive objective.

### Example 7

Eligible adoption rises after alternatives are disabled, while support load and journey time worsen. The roadmap rejects adoption alone and restores an exception path pending product repair.

### Example 8

A six-month project loses problem evidence after a policy change. Leaders stop delivery, preserve reusable contracts and schedule safe preview retirement instead of invoking sunk cost.

### Example 9

An executive view and user view disagree because one deck is stale. Both are regenerated from the canonical version, which records changed capacity and affected commitments.

### Example 10

A regulated consumer cannot meet the standard migration window. An independently reviewed exception preserves control outcomes and adds evidence for a broader portability improvement.

## Cross-Program Connections

- Product Management contributes strategy, discovery, outcome roadmaps and stopping decisions.
- Systems Engineering contributes boundary, dependency, lifecycle and emergent-risk analysis.
- Site Reliability Engineering contributes error budgets, toil, launch readiness and operational headroom.
- Operations Research contributes constrained portfolio selection, sensitivity and capacity models.
- Software Engineering contributes architecture dependencies, incremental delivery and maintainability evidence.
- Security Engineering contributes threat consequence, control obligations and independent assurance.
- Data Engineering contributes metric provenance, cohort quality, lineage and delayed outcome evidence.
- Organizational Design contributes ownership, decision authority, cognitive load and team interaction.
- Finance contributes investment constraints, option value, unit economics and sunk-cost discipline.
- Technology Governance contributes transparency, exception, appeal, monopoly and accountability controls.

## References

1. CNCF TAG App Delivery. [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/). Retrieved 2026-09-02.
2. CNCF TAG App Delivery. [Platform Engineering Maturity Model](https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/). Retrieved 2026-09-02.
3. CNCF TAG App Delivery. [Product Thinking for Platforms](https://tag-app-delivery.cncf.io/blog/product-thinking-for-platforms/). Retrieved 2026-09-02.
4. DORA. [Platform Engineering](https://dora.dev/capabilities/platform-engineering/). Retrieved 2026-09-02.
5. DORA. [2024 DORA Accelerate State of DevOps Report](https://dora.dev/research/2024/dora-report/). Retrieved 2026-09-02.
6. GOV.UK Service Manual. [Developing a Roadmap](https://www.gov.uk/service-manual/agile-delivery/developing-a-roadmap). Retrieved 2026-09-02.
7. GOV.UK Service Manual. [How the Discovery Phase Works](https://www.gov.uk/service-manual/agile-delivery/how-the-discovery-phase-works). Retrieved 2026-09-02.
8. GOV.UK Service Manual. [How the Alpha Phase Works](https://www.gov.uk/service-manual/agile-delivery/how-the-alpha-phase-works). Retrieved 2026-09-02.
9. GOV.UK Service Manual. [How the Beta Phase Works](https://www.gov.uk/service-manual/agile-delivery/how-the-beta-phase-works). Retrieved 2026-09-02.
10. GOV.UK Service Manual. [How to Set Performance Metrics for Your Service](https://www.gov.uk/service-manual/measuring-success/how-to-set-performance-metrics-for-your-service). Retrieved 2026-09-02.
11. GOV.UK Service Manual. [Plan User Research for Your Service](https://www.gov.uk/service-manual/user-research/plan-user-research-for-your-service). Retrieved 2026-09-02.
12. Google SRE. [Error Budget Policy](https://sre.google/workbook/error-budget-policy/). Retrieved 2026-09-02.
13. Google SRE. [Reliable Product Launches at Scale](https://sre.google/sre-book/reliable-product-launches/). Retrieved 2026-09-02.
14. Google SRE. [Eliminating Toil](https://sre.google/workbook/eliminating-toil/). Retrieved 2026-09-02.
15. Google SRE. [Service Best Practices](https://sre.google/sre-book/service-best-practices/). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Turn the requested output “build a deployment dashboard by Q4” into a roadmap item that preserves learning and makes date semantics explicit.

### Exercise 2

A portfolio selects items A, B and C with capacity demands 3, 5 and 4. Capacity is 10; C depends on A and is mandatory. Diagnose feasibility and propose two legitimate responses.

### Exercise 3

A platform’s adoption rises from 40% to 85% after leadership prohibits alternatives. Define evidence needed to determine whether this is a successful roadmap outcome.

### Exercise 4

Design a roadmap review after error-budget exhaustion, a vendor delay and new research that invalidates a high-profile feature hypothesis.

### Exercise 5

Create publication semantics for a canonical roadmap used by engineers, consuming teams, executives and security reviewers without producing conflicting truths.

## Answers to the Exercises

### Answer 1

Frame the problem and outcome: eligible teams currently take too long to diagnose deployment failure; the intended change is a lower median and tail diagnosis time without higher support load or inappropriate data exposure. Record research and baseline, affected cohorts, a hypothesis that better feedback may help, and alternative interventions such as inline diagnostics, search or a dashboard.

Use “target Q4” only if it is an aspiration, “forecast Q4 with medium confidence” if evidence supports a range, or “committed by 15 December” only when authorized owners accept scope/date/cost under named assumptions. Add identity and telemetry dependencies, accessibility/security guardrails, capacity range, a preview decision trigger and monthly review. Do not commit to a dashboard before the solution test.

### Answer 2

The selected demand is $3+5+4=12$, which exceeds capacity 10. The dependency constraint is satisfied only if both A and C remain selected; mandatory C cannot be dropped without changing the governing obligation. Therefore the portfolio is infeasible even before skill, support and interrupt dimensions are checked.

One response is to defer B, leaving A and C at capacity 7 with headroom. Another is to reduce independently valuable scope in A or B while preserving C’s dependency condition, after validating that the smaller slice is operationally complete. Leaders may also fund qualified capacity, but cannot relabel overtime or unfilled roles as available supply.

### Answer 3

Define eligible cohorts and compare journey success, time, failure, retention, incidents, support, local integration work, cost, accessibility, security and satisfaction before and after the prohibition. Look for abandoned work, shadow platforms, exception denial, migration harm and whether consumers can export data or exit safely.

Use research with adopters, reluctant users and rejected exceptions. Separate value-driven adoption from compliance-driven presence. Success requires improved user and service outcomes within guardrails, not merely captive reach; the result may justify repairing the platform, narrowing mandatory scope or restoring alternatives.

### Answer 4

Trigger an event-driven review rather than waiting for the calendar. Freeze scale work that would worsen the exhausted error budget, prioritize recovery according to policy and recompute qualified capacity. Update the vendor dependency with owner, delay range, fallback and affected forecasts.

Record the invalidating research and stop or return the feature to discovery despite its sponsor. Rebuild portfolio scenarios including mandatory obligations, consuming-team effects and WIP. Authorized owners decide changed commitments; the canonical transition records evidence, assumptions, decision and consequence. Publish what changed, why, affected users, safe actions and next review.

### Answer 5

Store one canonical item record with stable identifier, class, outcome, evidence, owner, status, horizon, date type, confidence factors, dependencies, capacity, guardrails, sensitivity, decision history and freshness. Generate an engineering view with dependencies and readiness, a consumer view with outcomes and migration implications, an executive view with investment and guardrails, and a security view with obligations and restricted evidence links.

All views retain identical status, horizon, date semantics and version. Redaction removes sensitive detail without changing the decision. Each view links to its maintainer, update time, contribution route and change history; automated comparison can detect stale or contradictory representations.
