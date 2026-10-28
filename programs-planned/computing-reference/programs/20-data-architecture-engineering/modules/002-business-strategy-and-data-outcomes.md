---
module_id: DARCH-002
program: Data Architecture Engineering
level: 1
module_number: 2
title: Business Strategy and Data Outcomes
status: complete
last_verified: 2026-08-29
---

# Business Strategy and Data Outcomes

## One-Page Review

### Governing question

How can data-architecture decisions be traced to worthwhile business or public outcomes without mistaking data volume, platform delivery, or proxy metrics for value?

### Essential definitions

- **Strategy** is a coherent set of choices about outcomes, scope, advantage or public value, constraints, and resource allocation.
- A **business outcome** is an observable change in organizational, customer, partner, or societal conditions.
- A **data outcome** is an observable improvement in the availability, meaning, trustworthiness, protection, or usability of data required for a business outcome.
- An **output** is a delivered artifact or activity; an **impact** is a longer-range consequence to which outcomes contribute.
- A **capability** is an enduring ability to produce an outcome, independent of one organizational chart or product.
- A **measure** operationalizes evidence; a **target** gives it a desired level and time boundary.
- A **leading indicator** precedes an outcome; a **lagging indicator** observes it afterward.
- A **guardrail** or **counter-metric** detects unacceptable harm or displacement while pursuing a target.

### Central model, mechanism, or theorem

Use an explicit outcome chain:

`strategic choice -> stakeholder decision/behavior -> information need -> data outcome -> architecture capability/change -> adoption -> business outcome -> impact`.

Every arrow is a hypothesis with an owner, assumptions, measure, baseline, target, time horizon, and falsification condition. Architecture is justified only when it improves the required decision or service under constraints; delivering a lake, catalog, model, or dashboard is evidence of output, not outcome.

### Critical invariants

- Every initiative traces to a named strategic choice and accountable outcome owner.
- The stakeholder decision or behavior to change is explicit.
- Data outcomes state fitness at the point of use, not generic “quality.”
- Measures include definitions, populations, windows, sources, and owners.
- Benefits, costs, risks, rights, and distributional effects are evaluated together.
- Adoption and workflow change sit between data availability and business outcome.
- Counter-metrics prevent local optimization from hiding harm or shifted work.
- Architecture evidence can falsify the outcome hypothesis and supports stopping or redirecting work.

### Common failures

Frequent failures are declaring “data-driven” as strategy, starting with a vendor, counting datasets or dashboards as value, choosing metrics without baselines, confusing correlation with attribution, optimizing a proxy until it harms the goal, ignoring nonusers and manual work, pricing all data as an asset, omitting privacy and security costs, and keeping initiatives alive because their platform output shipped.

### Compact example

A retailer wants fewer substitutions in online orders. The relevant decision is inventory promise at checkout. A data outcome is not “centralize inventory”; it is item-location availability with a defined freshness, correctness, and coverage at promise time. Candidate architecture changes include event publication and reconciliation. Measure substitution rate and promise latency, while guarding against overselling, store workload, customer exclusion, and infrastructure cost.

### Connections

[DARCH-001](001-data-architecture-as-structure-flow-ownership-and-policy.md) supplies structure, flow, ownership, and policy views. [DARCH-003](../ROADMAP.md) inventories the current landscape. Business alignment connects to [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md); pipeline delivery belongs to [Data Engineering](../../19-data-engineering/ROADMAP.md).

## Governing Question

Organizations often begin data programs with nouns: warehouse, lakehouse, catalog, master-data hub, mesh, semantic layer, or AI platform. These may be useful mechanisms, but none states which condition should improve or why data is the limiting factor. A strategy-led architecture begins with choices and outcomes, then derives information and capability needs.

The governing question is not “How can we align data with the business?” as if either were a single object. It is: which stakeholder decision, service, obligation, or behavior must change; what information would enable that change; which data properties are presently limiting; and what evidence would justify an architectural intervention?

[ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) requires architecture descriptions to address stakeholder concerns through declared viewpoints, but does not judge whether an architecture is good. The [TOGAF Standard, 10th Edition](https://www.opengroup.org/togaf) presents enterprise architecture as adaptable practice and retains the discipline of responding to goals, drivers, and stakeholder concerns. These sources support traceability; they do not supply an organization's strategy or authorize a project.

## Why This Matters

Data is valuable in use, not merely in possession. The same customer history may reduce support time, enable discriminatory pricing, expose private behavior, or remain unused. Its value depends on context, complementary capabilities, legal authority, trust, timing, and the decisions it changes. The OECD's 2022 [data-governance report](https://doi.org/10.1787/e3d783b0-en) emphasizes both benefits and risks and notes that ordinary metrics do not capture data's strategic or innovative value fully.

Architecture without outcome traceability accumulates durable cost. Platforms require operation, skills, migration, controls, and consumer change. Copies expand attack and deletion surfaces. Canonical models create coordination obligations. If a proposed capability cannot be linked to a decision bottleneck, it may industrialize movement without improving an outcome.

Outcome reasoning also prevents local metrics from dominating. A fraud model can reduce chargebacks by rejecting more legitimate customers. A hospital dashboard can reduce reported waiting time by changing when the clock starts. A catalog can increase registered datasets while discoverability worsens because descriptions are empty. Counter-metrics and qualitative review expose these substitutions.

Strategy is choice under constraints. “Make all data available to everyone” ignores privacy, security, contractual, intellectual-property, competition, and purpose limits. “Create one source of truth” ignores legitimate domain and temporal perspectives. A sound data strategy states what will be prioritized, what will not, and which principles control trade-offs.

Finally, evidence creates an exit. Before work begins, the initiative should state what observation would weaken its hypothesis. If better inventory data does not change promise decisions, the bottleneck may be workflow, incentives, or fulfillment capacity. Architecture teams should redirect resources rather than defend sunk platform cost.

## Prerequisites and Retrieval

You should understand stakeholders, capabilities, value streams, measures, baselines, risks, and architecture views. Recall from [DARCH-001](001-data-architecture-as-structure-flow-ownership-and-policy.md) that an architecture couples structure, flow, ownership, and policy, and that artifacts are descriptions rather than outcomes.

Basic statistical caution is required. A measured change can accompany an initiative without being caused by it. Seasonality, selection, concurrent changes, measurement drift, and regression to the mean can mislead. This chapter develops architecture traceability, not causal-inference methods; use appropriate experimental or quasi-experimental expertise where attribution matters.

## Learning Objectives

After completing this module, you should be able to:

- distinguish strategy, goal, outcome, output, capability, and impact;
- identify the stakeholder decision or behavior an initiative must change;
- derive information needs and data outcomes from that decision;
- write an outcome hypothesis with assumptions and falsification conditions;
- define measures with baselines, targets, windows, and accountable owners;
- pair target measures with guardrails and distributional analysis;
- separate data limitations from process, incentive, skill, and capacity limitations;
- compare architecture options by outcome contribution, cost, risk, and reversibility;
- design incremental evidence before committing to an enterprise-scale target;
- scope human review for high-consequence strategy and measurement choices.

## Core Exposition

**Strategy** is more than aspiration. It chooses a desired position or public result, identifies constraints and trade-offs, and allocates scarce attention and resources. “Use data and AI” is a theme. “Reduce preventable supply interruption by improving replenishment decisions in critical product lines while preserving supplier diversity and working-capital limits” begins to express a strategic choice.

A **goal** gives direction. An **objective** makes a goal more specific. An **outcome** is a changed condition, such as fewer avoidable stockouts or faster correct eligibility decisions. An **output** is something produced: a governed dataset, interface, migration, model, training session, or dashboard. Outputs can be necessary, but the causal gap between output and outcome must remain visible.

An **impact** is usually broader and later: improved health, resilience, trust, profitability, or environmental condition. A single initiative rarely controls impact. Claim contribution with assumptions rather than sole attribution unless research design supports the stronger claim.

A **capability** is an enduring ability, such as reconciling inventory across channels within a declared freshness window or tracing regulated data use to authority. A product implements or exposes capability; a team operates it; a process consumes it. Capability language helps architecture survive reorganizations and product replacement.

The trace begins with an outcome owner. This is the person or governing body authorized and accountable for the business result—not automatically the data or platform lead. Identify affected stakeholders, including those who do not operate the system: customers denied service, employees absorbing exceptions, partners bearing reporting cost, and communities exposed to externalities.

Next name the **decision or behavior**. Data creates no outcome until it changes selection, timing, allocation, coordination, automation, or understanding. “Improve customer data” becomes reviewable only when attached to a use such as resolving identity before fulfillment, routing support, or enforcing consent. Different decisions require different data and authority.

Derive the **information need** from the decision. State required entities, measures, classifications, history, comparison, uncertainty, and explanation. Then derive a **data outcome**: the information is available at the decision boundary with defined coverage, correctness, freshness, consistency, provenance, accessibility, protection, and usability.

Avoid maximizing every quality dimension. A monthly regulatory return and a millisecond authorization decision need different timeliness. A research cohort may accept delayed, carefully curated data; emergency routing may prioritize freshness while exposing uncertainty. Fitness is contextual and owned by producer and consumer authorities.

Build an **outcome hypothesis**:

“For stakeholder `S` making decision `D`, if capability `C` supplies information `I` with fitness `F` and the workflow adopts it under assumptions `A`, then outcome `O` should change by target `T` within horizon `H` without violating guardrails `G`.”

This form exposes the middle. If the capability ships but adoption is zero, the architecture output is real and the outcome pathway failed. If adoption is high but the outcome does not move, the information may not be decision-relevant or another constraint dominates.

Measures require semantic contracts. “Conversion,” “active customer,” “on time,” and “duplicate” need population, numerator, denominator, exclusions, event/time boundary, source, revision behavior, and owner. Baselines need representative windows and segmentation. Targets need time horizons and uncertainty, not ceremonial precision.

Leading indicators test early links: data coverage, decision latency, eligible-user adoption, or exception resolution. Lagging indicators observe outcomes: substitution, loss, readmission, or audit findings. Leading indicators are not guaranteed predictors; validate their relationship and retire them when they stop being informative.

Guardrails constrain optimization. A faster credit decision may be unacceptable if error disparity, complaint rate, privacy intrusion, or manual escalation rises. Measure distributions, not only averages: outcomes can improve overall while deteriorating for a protected, regional, low-volume, or accessibility-reliant group.

Costs include acquisition, licensing, integration, storage, computation, operations, migration, governance, security, training, workflow disruption, exit, and opportunity cost. Risks include breach, reidentification, unreliable automation, vendor dependence, semantic centralization, regulatory violation, and harmful feedback. Benefits and harms may accrue to different stakeholders.

Not every problem is a data problem. A team may already know which order is late but lack authority to expedite it. A clinician may have the result but lack time. A supplier may report accurately while capacity is constrained. Diagnose information, process, incentive, skill, authority, and resource gaps separately before selecting architecture.

Architecture options should be compared at the smallest level capable of testing the hypothesis. A governed view may establish whether shared semantics change decisions before a new platform is purchased. A bounded domain interface may test freshness before enterprise replication. Reversible experiments preserve options and reveal adoption work.

## Definitions and Notation

Let an outcome chain be `Q = (S,D,I,F,C,A,O,G,H)`:

- `S`: stakeholders and accountable outcome owner;
- `D`: decision, service, or behavior to change;
- `I`: required information;
- `F`: fitness properties at the point of use;
- `C`: architecture capability or change;
- `A`: assumptions, adoption, and complementary actions;
- `O`: observable outcome and target;
- `G`: guardrails, risks, rights, and cost constraints;
- `H`: evaluation horizon.

Let `b_m` be a measure's baseline and `y_m(t)` its observed value at time `t` under a versioned definition. A target such as `y_m(H) <= tau` is meaningful only with population, window, source, uncertainty, and counter-metrics. It is evidence about the operationalized measure, not automatically the whole outcome.

An outcome hypothesis is **falsifiable** when it names observations that would count against a causal link: capability unavailable, fitness missed, adoption absent, decisions unchanged, outcome unchanged after a justified horizon, or guardrails violated. A decision can still consider qualitative and ethical evidence; “measurable” does not mean “only what is easy to count.”

## Mechanisms, Invariants, or Proof Structure

An outcome-led architecture review can proceed through seven gates.

**1. Strategic authority.** Record the approved choice, scope, constraints, and accountable outcome owner. A presentation theme or executive slogan is not authority. Identify conflicts with other objectives and the forum that may resolve them.

**2. Decision diagnosis.** Observe the current workflow. Who decides, with what information, at what frequency and latency, under which policy, and with what fallback? Establish whether information is the binding constraint. Document manual work and the people who will bear changed responsibility.

**3. Outcome chain.** Instantiate `Q`. For every edge, record why the upstream change is expected to influence the downstream condition. Classify evidence as established research, organization-specific observation, expert judgment, or untested assumption.

**4. Measurement contract.** Define baseline, target, population, segmentation, horizon, sources, revision, uncertainty, and counter-metrics. Protect the measurement pipeline from the intervention when practical. A changed definition must not be presented as a changed outcome.

**5. Option comparison.** Compare no-change/process-only, minimal-data, and larger architecture options. Evaluate contribution, time to evidence, total lifecycle cost, risk, rights, interoperability, reversibility, concentration, and exit. Do not award value merely because an option is strategically fashionable.

**6. Bounded implementation and adoption.** Deliver the smallest safe capability that tests a material link. Instrument fitness and use, train stakeholders, update decision authority and exception paths, and preserve a control or comparison where responsible.

**7. Review and adaptation.** Evaluate the whole chain at declared checkpoints. Continue, expand, change, or stop. Archive the evidence and update architecture decisions; do not silently rewrite the original hypothesis after results arrive.

The executable example is a triage aid, not an investment algorithm. It rejects initiatives that lack an outcome owner, decision, measure, or guardrail, then applies a transparent score to the remaining candidates. Human authority still evaluates rights, strategy, dependencies, and evidence.

<!-- bijux-verify: {"id":"outcome-initiative-screen","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"eligible=(('inventory-promise', 9),)\nrejected=(('customer-lake', ('decision', 'guardrail')), ('risk-dashboard', ('measure',)))\n","stderr":""}} -->
```python
initiatives = (
    {
        "name": "inventory-promise",
        "owner": "commerce-director",
        "decision": "promise item-location availability at checkout",
        "measure": "substitution rate",
        "guardrail": "oversell rate",
        "outcome": 3,
        "evidence": 2,
        "reversibility": 2,
        "cost": 1,
        "risk": 0,
    },
    {
        "name": "customer-lake",
        "owner": "data-director",
        "decision": "",
        "measure": "datasets copied",
        "guardrail": "",
        "outcome": 2,
        "evidence": 0,
        "reversibility": 1,
        "cost": 3,
        "risk": 2,
    },
    {
        "name": "risk-dashboard",
        "owner": "risk-director",
        "decision": "prioritize control remediation",
        "measure": "",
        "guardrail": "unresolved critical findings",
        "outcome": 2,
        "evidence": 1,
        "reversibility": 2,
        "cost": 1,
        "risk": 1,
    },
)

required = ("owner", "decision", "measure", "guardrail")
eligible = []
rejected = []
for item in initiatives:
    missing = tuple(field for field in required if not item[field])
    if missing:
        rejected.append((item["name"], missing))
        continue
    score = (
        2 * item["outcome"]
        + item["evidence"]
        + item["reversibility"]
        - item["cost"]
        - item["risk"]
    )
    eligible.append((item["name"], score))

print(f"eligible={tuple(sorted(eligible))}")
print(f"rejected={tuple(sorted(rejected))}")
```

This run verifies the stated policy over three fixtures. It does not validate the ordinal ratings, compare unlike harms, establish causality, or authorize investment. Scores can conceal stakeholder conflict and false precision. Production governance should retain the underlying evidence, dissent, noncompensable constraints, and named decision authority.

## Alternatives and Trade-Offs

**Top-down versus use-case-led planning.** Top-down strategy controls fragmentation and portfolio conflict but can remain abstract. Use cases expose concrete value and adoption but can create local duplication. A portfolio can require strategic traceability while testing through bounded uses.

**Financial valuation versus multidimensional outcomes.** Money enables comparison where cash flows are defensible. Public value, rights, resilience, knowledge, option value, and avoided harm may resist a single price. Use a transparent multi-criteria argument rather than inventing currency precision.

**Central versus domain outcome ownership.** Central ownership can coordinate enterprise measures; domain owners understand decisions and consequences. Shared outcomes need an accountable forum and explicit decision rights, not collective ambiguity.

**Leading versus lagging measures.** Leading measures accelerate feedback but are proxies vulnerable to gaming. Lagging outcomes are closer to purpose but arrive late and mix many causes. Use both and validate their relationship.

**Standardization versus local fitness.** Shared semantics reduce reconciliation and enable enterprise questions. Uniform definitions can erase legitimate product, jurisdiction, or temporal distinctions. Standardize the intersection with demonstrated value and document translations elsewhere.

**Large target architecture versus incremental options.** A target can coordinate dependencies and prevent local dead ends. Incremental experiments reduce sunk cost and test assumptions. Preserve an architectural direction while making funding conditional on evidence.

## Failure Modes and Misconceptions

1. **“Data-driven” is a strategy.** It states neither choice, outcome, nor constraint.
2. **A platform is a business outcome.** It is an output or capability candidate until use changes a condition.
3. **More data has nonnegative value.** Collection can add cost, rights violations, attack surface, noise, and harmful power.
4. **One KPI represents the objective.** Proxies omit dimensions and invite gaming; guardrails and qualitative evidence remain necessary.
5. **A target without a baseline is ambitious.** It may be arbitrary or already achieved.
6. **Correlation after delivery proves value.** Concurrent changes, selection, seasonality, and definition drift can explain movement.
7. **Adoption proves benefit.** Mandatory use can be high while decisions worsen or manual shadow processes grow.
8. **The data team owns business outcomes.** It owns technical obligations; outcome authority belongs to the accountable domain or public body.
9. **Every strategy should become an enterprise model.** Some outcomes need process change, local data, or no new data capability.
10. **A positive aggregate justifies distributional harm.** Benefits, burdens, rights, and errors must be segmented and reviewed.

## Worked Examples

### Example 1

**Question:** Classify “deploy an enterprise catalog” and “reduce analyst time spent locating approved finance data.”

**Reasoning:** The catalog is an output/capability candidate. Reduced search time under defined approval and correctness constraints is a data outcome contributing to faster analysis.

**Conclusion:** Delivery nouns must be linked to changed conditions.

### Example 2

**Question:** A call center already sees churn risk but cannot offer retention terms. Is data the bottleneck?

**Reasoning:** No: authority or policy blocks action. Improving the score cannot change the decision until the offer capability and governance change.

**Conclusion:** Diagnose process and authority before adding data.

### Example 3

**Question:** Define “faster claims decisions.”

**Reasoning:** Name eligible claim population, receipt and decision events, working versus elapsed time, percentiles, exclusions, revision rules, and decision correctness. Segment by claim type and channel.

**Conclusion:** A measure becomes reviewable only through a semantic contract.

### Example 4

**Question:** Why pair fraud-loss reduction with approval and complaint measures?

**Reasoning:** Rejecting more transactions can reduce recorded fraud while harming legitimate customers. Approval, false-positive review, complaint, and group error rates expose displacement.

**Conclusion:** Guardrails protect the objective from proxy optimization.

### Example 5

**Question:** When does a shared customer model support strategy?

**Reasoning:** When named cross-domain decisions require aligned identity and the benefit exceeds coordination, privacy, migration, and exception costs. Similar words alone do not justify centralization.

**Conclusion:** Standardization is an outcome hypothesis, not an architectural default.

### Example 6

**Question:** How can an initiative test value before migrating the warehouse?

**Reasoning:** Publish a governed view for one decision, measure fitness, adoption, decision change, outcome, and guardrails, and compare with the existing path. Migration can follow if the limiting assumption survives.

**Conclusion:** A reversible slice can test the causal chain before major commitment.

### Example 7

**Question:** Dataset usage doubled. Did value double?

**Reasoning:** Usage can reflect duplication, mandatory migration, retries, or curiosity. Examine which decisions changed, user success, outcome measures, cost, and harmful use.

**Conclusion:** Consumption is a leading observation, not value itself.

### Example 8

**Question:** A metric improves immediately after its definition changes. What should be reported?

**Reasoning:** Restate the historical series under the new definition where possible or mark a break. Do not attribute the discontinuity to architecture.

**Conclusion:** Measurement-version integrity is part of outcome evidence.

### Example 9

**Question:** A health authority proposes linking datasets to reduce missed cancer follow-up. What evidence is required?

**Reasoning:** Define the clinical pathway, eligibility, missed-follow-up outcome, data completeness and linkage error, workflow adoption, intervention capacity, privacy/legal authority, equity, and patient harm. Named clinical, patient/public, privacy, security, data, and independent ethics/assurance reviewers must approve within the applicable regime. No external review is claimed here.

**Conclusion:** High-consequence outcomes require domain authority, rights review, and system evidence beyond technical linkage.

### Example 10

**Question:** When should a technically successful initiative stop?

**Reasoning:** Stop or redirect if users cannot act, the data fitness threshold remains infeasible, outcome change is absent after a justified horizon, costs dominate, or guardrails fail. Preserve evidence for later learning.

**Conclusion:** Shipping successfully is compatible with an invalid outcome hypothesis.

## Cross-Program Connections

[Software Engineering: Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) develops drivers, stakeholder concerns, quality attributes, and trade-off decisions. Data architecture specializes these for persistent meaning, sharing, rights, and lifecycle.

[Data Engineering](../../19-data-engineering/ROADMAP.md) implements reliable datasets and pipelines; its operational metrics become evidence only when connected to decision fitness. [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies integrity and workload guarantees beneath data outcomes.

[Security Engineering](../../25-security-engineering/ROADMAP.md) and governance authorities define noncompensable constraints and harm controls. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes stakeholder needs, verification, validation, and lifecycle reasoning for outcome chains spanning people and technology.

## References

- ISO/IEC/IEEE, [*ISO/IEC/IEEE 42010:2022 — Software, systems and enterprise — Architecture description*](https://www.iso.org/standard/74393.html), second edition, 2022. Authoritative requirements for stakeholder, concern, viewpoint, and architecture-description traceability.
- The Open Group, [*The TOGAF Standard, 10th Edition*](https://www.opengroup.org/togaf), 2022, site checked 2026-08-29. Current official enterprise-architecture standard family and adaptation guidance.
- OECD, [*Going Digital to Advance Data Governance for Growth and Well-being*](https://doi.org/10.1787/e3d783b0-en), OECD Digital Economy Papers 285, 2022. Current policy analysis of contextual data value, governance tensions, benefits, and risks.
- OECD, [*The Path to Becoming a Data-Driven Public Sector*](https://doi.org/10.1787/059814a7-en), OECD Digital Government Studies, 2019. Public-value and data-value-cycle treatment.
- Robert S. Kaplan and David P. Norton, [*The Balanced Scorecard—Measures that Drive Performance*](https://hbr.org/1992/01/the-balanced-scorecard-measures-that-drive-performance-2), *Harvard Business Review*, 1992. Primary formulation connecting multiple performance perspectives.
- John Doerr, [*Measure What Matters*](https://www.whatmatters.com/the-book), Portfolio, 2018. Practitioner treatment of objectives and measurable key results; useful for execution, not a substitute for strategy or causal evidence.
- Douglas W. Hubbard, [*How to Measure Anything*, third edition](https://www.wiley.com/en-us/How+to+Measure+Anything%3A+Finding+the+Value+of+Intangibles+in+Business%2C+3rd+Edition-p-9781118836446), Wiley, 2014. Decision-oriented measurement and uncertainty foundations.

## Exercises

### Exercise 1

Classify each as strategy, output, capability, data outcome, or business outcome: “reduce avoidable delivery failure,” “deploy a catalog,” “resolve shipment address before dispatch,” “address data is verified at dispatch,” and “prioritize reliable delivery over lowest carrier price.”

### Exercise 2

Write an outcome chain `Q` for reducing online-order substitutions. Include baseline, target, two assumptions, and three guardrails.

### Exercise 3

Diagnose an initiative whose proposal says “create a 360-degree customer lake, ingest 95% of sources, and deliver 50 dashboards.” Identify missing evidence and propose the smallest falsifiable intervention.

### Exercise 4

Compare centralized master data, a federated identity interface, and process-only change for a cross-channel customer-resolution outcome. Use contribution, time to evidence, cost, risk, rights, reversibility, and exit.

### Exercise 5

A public benefits agency wants to combine tax, housing, and health data to identify fraudulent claims faster. Specify the outcome hypothesis, counter-metrics, evidence, and named human-review roles required before architectural approval.

## Answers to the Exercises

### Answer 1

“Prioritize reliable delivery over lowest carrier price” is a strategic choice. “Deploy a catalog” is an output and possibly part of a capability. “Resolve shipment address before dispatch” describes a decision/process capability. “Address data is verified at dispatch” is a data outcome when verification fitness is defined. “Reduce avoidable delivery failure” is a business/customer outcome. The categories form a chain; relabeling the catalog as an outcome does not establish value.

### Answer 2

Strategy: improve fulfilled-order reliability without unacceptable oversell or cost. Decision: promise a substitute-sensitive item at checkout. Information: item-location sellable quantity and reservation state. Data outcome: at least 99% covered items, freshness below 30 seconds at decision time, reconciled daily. Capability: publish inventory changes and serve a governed promise view. Adoption: checkout uses the view with a safe fallback. Outcome: reduce substitutions from baseline 4.0% to at most 2.5% within two quarters. Assumptions include that stale inventory materially causes substitutions and stores execute reservations. Guardrails include oversell rate, checkout p99 latency, store reconciliation workload, customer-segment error, and lifecycle cost.

### Answer 3

The proposal contains architecture outputs and a source-coverage proxy but no strategic choice, decision, outcome owner, consumer, fitness threshold, baseline, outcome target, adoption path, risk, guardrail, or falsification condition. Start with one consequential decision—for example resolving a customer across support channels. Provide a governed identity view over the minimum sources for a bounded group, retain the existing workflow as comparison where responsible, and measure match precision/recall, resolution time, adoption, complaints, privacy incidents, manual effort, and cost. Expand only if the information changes decisions and improves the owned outcome.

### Answer 4

Central master data can provide one governed identity and strong reuse but has high migration, semantic-centralization, privacy, and exit cost; time to evidence is long. A federated interface preserves domain custody and can test matching sooner, but creates availability, latency, version, and cross-domain governance dependencies. Process-only change—shared lookup rules or human escalation—may solve low-volume cases cheaply and reversibly, yet may not scale or provide consistent evidence. Score no option automatically. Select the smallest approach satisfying resolution accuracy, latency, authority, rights, and scale, and record how consumers exit or migrate if assumptions fail.

### Answer 5

State the legitimate strategic objective and distinguish faster correct adjudication from maximizing fraud flags. Identify the authorized decision, populations, source meanings, time boundaries, linkage uncertainty, workflow, appeal, and human authority. Hypothesize that defined data fitness improves correct decision time within a horizon. Measure confirmed fraud precision/recall where labels are defensible, adjudication time, recovered loss, and data fitness; guard against false accusation, benefit delay or denial, disparate error, chilling effects, privacy intrusion, security exposure, appeal burden, staff work, and exclusion of people with sparse records. Require legal/statutory authority, data-protection impact assessment, security threat analysis, independent validation, pilot/control evidence where ethical, auditability, redress, rollback, and public transparency appropriate to the jurisdiction. Named reviewers include benefits-domain leaders, fraud investigators, data/linkage experts, privacy and security officers, legal counsel, equality/human-rights and ethics authorities, claimant/public representatives, and the independent oversight body. This model answer supplies no approval or external human review.
