---
module_id: DARCH-026
program: Data Architecture Engineering
level: 1
module_number: 26
title: Data Products and Service Expectations
status: complete
last_verified: 2026-09-03
---

# Data Products and Service Expectations

## One-Page Review

### Governing question

How can a data-product team translate consumer decisions and consequences into explicit, measurable, operable service expectations for meaning, quality, freshness, availability, change, support, protection, recovery, and lifecycle without promising more than its dependencies and evidence can sustain?

### Essential definitions

- A **data product** is a governed and supported data offering with defined users, purpose, semantics, interfaces, quality, service behavior, ownership, protection, evidence, change, and lifecycle.
- A **service expectation** is a declared consumer-facing statement about product behavior, measurement, response, and limitations.
- A **service-level indicator (SLI)** is a reproducible measure of a product behavior such as freshness, successful queryability, valid records, or correction latency.
- A **service-level objective (SLO)** is a target for an SLI over a declared population and time window, with explicit clock, exclusion, and evaluation rules.
- A **service-level agreement (SLA)** is a formal agreement whose missed commitments may trigger contractual, financial, regulatory, or other defined consequences.
- An **error budget** is the tolerated fraction or amount of nonconforming service implied by an SLO; it supports decisions but does not authorize unsafe or unlawful behavior.
- **Freshness** is the age of data relative to a defined business or publication event, not simply the most recent pipeline timestamp.
- **Availability** is the product's ability to serve a valid request through a declared interface under defined conditions.
- **Data-quality objective** is a measurable fitness requirement for a named characteristic, population, method, interval, and use.
- **Recovery expectation** defines restoration, replay, reconciliation, communication, and validation behavior after failure or corruption.

### Central model, mechanism, or theorem

Represent a product service contract as:

`C = (purpose, consumers, semantic_contract, interfaces, quality, SLOs, dependencies, ownership, operations, protection, evidence, change, lifecycle)`

Represent an SLO as:

`O = (behavior, indicator, population, window, target, clock, exclusions, measurement, breach, response, escalation)`

For a target success fraction `s` over `N` eligible events, the nominal tolerated nonconforming count is `(1 - s)N`; rounding policy must be declared. A credible objective is valuable to consumers, measurable from trustworthy evidence, affordable to operate, compatible with protection and dependency constraints, and connected to action. A target without semantics, telemetry, ownership, or response is decoration.

### Critical invariants

- Service expectations derive from declared consumer decisions, consequences, and time needs rather than copied industry percentages.
- Every SLI identifies event, population, unit, window, clock, exclusions, source, computation, aggregation, and uncertainty.
- Freshness, availability, completeness, validity, consistency, accuracy, timeliness, latency, durability, and support remain distinct.
- Product-level objectives account for dependency behavior, buffering, cached or degraded modes, repair, replay, and end-to-end validation.
- Missed objectives trigger proportionate communication, containment, correction, learning, and investment decisions; they are not merely dashboard colors.
- Error budgets never override safety, privacy, security, legal, records, ethical, contractual, or critical-decision obligations.
- Quality and reliability are measured at meaningful grains and consequence classes so large low-risk populations do not hide critical failures.
- Change expectations cover semantic and behavioral compatibility, notice, migration, version support, deprecation, and emergency handling.
- Objective evidence and incident records are protected, retained, reproducible, and reviewable; inaccessible telemetry does not prove success.
- Expectations are reviewed when consumers, dependencies, risk, cost, architecture, or product lifecycle change.

### Common failures

Common failures are promising “99.9% data quality” without a denominator; equating pipeline success with product correctness; measuring freshness from ingestion rather than business-effective events; reporting averages that hide critical partitions; excluding every inconvenient incident; counting stale cached output as current availability; offering an SLA before an internal SLO is operable; ignoring source and platform dependencies; setting objectives without consumer research; treating an error budget as permission to break controls; alerting on every row; owning dashboards but not response; declaring recovery when jobs restart before outputs reconcile; and leaving obsolete objectives active after product or consumer change.

### Compact example

A daily Risk Position product says it is “available 99.9%.” Consumers actually need a validated position by 06:00 local market time, with all material books represented and corrections announced before trading decisions. The team defines four objectives: eligible market-days published and queryable by 05:45; critical-book completeness at 100%; reconciliation variance within an approved threshold; and correction notices within fifteen minutes of confirmed material error. It documents calendars, holidays, late source behavior, measurement points, degraded states, dependencies, escalation, replay, protection, and review. Ordinary availability remains useful, but it no longer hides decision fitness.

### Connections

[DARCH-025](025-source-aligned-aggregate-and-consumer-aligned-data.md) distinguishes product alignments and semantic responsibilities. This module makes their service promises measurable before [DARCH-027](../ROADMAP.md) develops producer-consumer contracts, [DARCH-028](../ROADMAP.md) analyzes cross-domain dependencies, and [DARCH-030](../ROADMAP.md) addresses product portfolios and lifecycle.

## Governing Question

A product is not dependable merely because its pipeline ran. Consumers experience meaning, data values, interfaces, time, support, corrections, and change as one service. A technically available table can be unusable because it is stale, incomplete, semantically changed, inaccessible to the right users, or unsupported during a critical decision.

The design problem is to choose a small set of expectations that represent real consumer value and risk, make each measure reproducible, operate the response, and manage trade-offs. The objective is not perfect data or maximal availability. It is explicit, evidence-backed fitness and predictable behavior within lawful and affordable bounds.

## Why This Matters

Unstated expectations still exist. Analysts schedule reports based on observed delivery. Models assume update cadence. Operations teams build workarounds around a table's usual behavior. When the product changes, these implicit contracts fail without warning.

Formal expectations create a shared language for consumers, owners, stewards, engineers, platforms, security, privacy, risk, and leadership. They expose whether desired behavior is measurable, whether dependencies support it, whether staffing and recovery are sufficient, and whether cost matches consequence.

Google's [Site Reliability Engineering chapter on Service Level Objectives](https://sre.google/sre-book/service-level-objectives/) distinguishes indicators, objectives, and agreements and emphasizes choosing measures that matter to users. The [SRE Workbook chapter on Implementing SLOs](https://sre.google/workbook/implementing-slos/) develops practical measurement and error-budget mechanics. Data products require additional semantic and quality dimensions, but the operational discipline transfers well.

[ISO/IEC 25012:2008](https://www.iso.org/standard/35736.html) defines a general data-quality model, while [ISO/IEC 25024:2015](https://www.iso.org/standard/35749.html) addresses measurement of data quality. These sources help separate characteristics and measures from vague quality percentages.

W3C's [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/) supports publishing data-quality information, including measures, policies, annotations, and provenance. W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) supports descriptions of datasets, services, distributions, and catalog relationships. Machine-readable description improves discovery, though local evidence and operating processes establish actual fulfillment.

NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy secure-system engineering across the lifecycle. The NIST [Cybersecurity Framework 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20) connects governance, protection, detection, response, recovery, roles, and improvement. Service objectives must coexist with system trustworthiness and risk management rather than optimize availability in isolation.

## Prerequisites and Retrieval

You should understand data products, consumers, product contracts, quality dimensions, time semantics, lineage, dependencies, distributed systems, monitoring, incident response, recovery, risk, privacy, security, and lifecycle.

Retrieve SLI, SLO, SLA, error budget, success event, bad event, population, window, target, clock, freshness, latency, availability, completeness, validity, consistency, accuracy, durability, recovery point, recovery time, replay, reconciliation, correction, support, escalation, dependency, degraded mode, compatibility, and deprecation.

As a retrieval test, inspect “Customer data has a 99.9% SLO.” Ask 99.9% of which events or records; which customer product and interface; what success means; which population, time, geography, and consumer; how missing, late, duplicate, invalid, inaccessible, and stale behavior count; where evidence originates; what exclusions apply; and what action follows a breach. Without these coordinates, the number is not an objective.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish service expectations, SLIs, SLOs, SLAs, policies, guarantees, forecasts, and internal operating targets;
2. derive product behaviors and consequence tiers from consumer decisions, workflows, deadlines, and failure effects;
3. define reproducible freshness, availability, latency, completeness, validity, consistency, accuracy, durability, recovery, and support indicators;
4. select populations, windows, targets, clocks, exclusions, aggregation, rounding, evidence, breach, and response rules;
5. calculate nominal error budgets and burn rates while recognizing their assumptions and protection limits;
6. model dependency, end-to-end, cached, partial, degraded, replay, correction, and restatement behavior;
7. design observability, alerting, incident, communication, reconciliation, and review around product objectives;
8. govern semantic compatibility, notice, migration, version support, deprecation, and emergency changes;
9. balance consumer value, risk, reliability, quality, cost, capacity, complexity, and improvement investment;
10. audit whether expectations are meaningful, measurable, achieved, protected, and current through the product lifecycle.

## Core Exposition

**Begin with consumer decisions.** Identify who uses the product, for which decision or workflow, at what time, with what alternatives, and with what consequence when data is absent, late, wrong, incomplete, inaccessible, or changed. A monthly planning product and a fraud-intervention stream need different expectations.

Observe actual behavior as well as stated preference. Consumers may ask for real-time delivery while acting once a week, or tolerate delayed data but not silent corrections. Capture deadlines, critical partitions, degraded modes, recovery needs, and communication expectations.

**Define product behavior, not pipeline internals.** A successful orchestration job is evidence about one mechanism. Consumers care whether the contracted interface serves semantically correct and sufficiently current data. Measure at the consumption boundary when possible.

Internal indicators remain useful for diagnosis: source arrival, queue age, transformation success, validation, publication, indexing, and access enforcement. Connect them to a consumer-facing outcome instead of presenting them as substitutes.

**Distinguish expectation types.** An SLI is the measure. An SLO is the desired level. An SLA adds formal consequences and normally needs legal, commercial, risk, and operational review. A policy can impose an absolute constraint, and an internal target can be stricter than the published objective.

Use terminology consistently. Do not call every threshold an SLA. A product can begin with observed baselines and internal objectives, learn its behavior, and only then make durable external commitments.

**Define eligible events.** Event-based objectives count successful eligible events over all eligible events. An event may be an expected publication, query, partition, file, message, validation, correction, or consumer request. State how retries, duplicates, cancellations, maintenance, and partial outcomes count.

For `N` eligible events and target success fraction `s`, the nominal error budget is `(1-s)N`. If `N=10,000` and `s=0.999`, the budget is ten nonconforming events. Declare rounding; small populations make one event disproportionately important.

**Define time-based objectives.** Time-based objectives measure conforming intervals over eligible service time. Define interval size, sampling, maintenance, calendar, and how long failures span. One hourly sample can miss a forty-minute outage.

Event and time objectives answer different questions. A high-volume interface can fail many requests briefly, while a once-daily publication has only thirty monthly events. Use the denominator that matches consumer experience.

**Define freshness correctly.** Freshness can mean time since the newest business event represented, time since expected source close, time from event occurrence to queryability, or age of a successfully validated publication. Name the semantics.

`now - max(ingestion_time)` is misleading when source events arrive empty, future-dated, or missing. Compare expected source completeness, business-effective time, watermark, publication validation, and consumer deadline. Segment by critical source or partition.

**Separate latency from freshness.** Latency measures duration between declared events, such as source acceptance and product publication. Freshness describes the age or currency of available data relative to need. A stream can have low processing latency while missing an entire source partition and therefore be stale or incomplete.

Measure percentiles or distributions when tails matter. Averages hide periodic severe delay. Define whether clocks include upstream waiting and whether consumer-visible latency differs from internal processing time.

**Define availability at the interface.** Availability requires a valid request and success criteria. For SQL, success might mean authorized connection and correct query completion within latency bounds. For files, it may mean a complete, validated object at the declared path. For streams, it may include connection, delivery, order, and duplication semantics.

An interface returning stale cached data may be technically available but fail freshness. Report dimensions separately and define any degraded mode. Authorization correctly denying an ineligible request is not unavailability.

**Define completeness by population.** Completeness can concern required attributes, expected entities, source partitions, periods, event sequences, or relationships. The denominator must be known or estimated with stated uncertainty.

A product cannot infer missing rows solely from the rows it received. Use source control totals, expected manifests, sequence numbers, independent registers, reconciliation, or domain rules. Segment critical books, regions, or customer classes so large populations do not hide omissions.

**Define validity and consistency.** Validity tests conformance to format, type, value domain, range, pattern, relationship, or business rule. Consistency tests whether related assertions obey declared constraints across fields, records, products, or time.

Passing a schema does not prove business validity. A valid date can still precede the relevant event incorrectly. Record rule versions, populations, exceptions, severity, and evaluation time. Separate rejected records from silently coerced values.

**Treat accuracy carefully.** Accuracy compares a value to accepted evidence of the real-world or authoritative value. In many domains, ground truth is delayed, disputed, sampled, or costly. Avoid labeling agreement with another imperfect system as accuracy without stating the authority assumption.

Use audits, reconciliations, verified samples, external evidence, correction outcomes, or domain adjudication. Publish confidence and sampling error where relevant. Absence of reported defects is not an accuracy measure.

**Measure uniqueness and identity.** Uniqueness can apply to business keys, event identifiers, combinations at declared grain, or represented subjects. Duplicate physical rows are not the only identity failure; erroneous merges and splits matter.

Define legitimate repeats, versioned facts, retransmission, and correction. Identity-product objectives may need false-merge and false-split evidence, not merely key distinctness.

**Define durability and retention behavior.** Consumers may require that acknowledged publications remain retrievable, reproducible, or recoverable for a period. Durability differs from availability and from lawful retention.

State backup, replication, recovery, archive, deletion, legal hold, version, and reproducibility expectations. More retention is not automatically safer; privacy, security, records, licensing, and cost constrain it.

**Define correction expectations.** Track time from confirmed material defect to containment, consumer notice, corrected publication, downstream propagation, reconciliation, and closure. Different clocks reveal different capabilities.

Define what is corrected: current state, affected historical periods, derived products, models, reports, exports, and decisions. Preserve original-decision evidence where required. A restarted pipeline is not a verified correction.

**Define recovery objectives.** Recovery time objective can describe the targeted time to restore a service capability. Recovery point objective can describe tolerable data loss measured in time or another domain unit. Data products also need replay, deduplication, ordering, reconciliation, and consumer communication.

Test restoration from actual backups and logs. Validate semantic and quality state after recovery. A queryable but corrupted or incomplete product has not recovered.

**Define support expectations.** Publish support channel, hours, acknowledgement, severity, updates, escalation, owner, and out-of-hours arrangements. Support must match decision consequence and geography.

Separate incident support, usage questions, access requests, definition disputes, quality issues, and feature requests. Routing can differ, but consumers should not navigate the organization to report a material failure.

**Choose windows deliberately.** Rolling windows reflect recent experience but overlap and can obscure when a commitment resets. Calendar windows align with reporting periods but can encourage end-of-period gaming. Short windows detect bursts; long windows stabilize rare events.

Use more than one view when necessary: a 28-day objective plus critical-event absolute rules and short-window alerting. Document timezone, daylight-saving treatment, business calendars, holidays, and partial periods.

**Choose targets from consequence and capability.** Start with consumer need, risk tolerance, alternatives, dependency behavior, observed baseline, engineering cost, and recovery capacity. Do not add nines for prestige.

A stricter target increases investment and reduces change flexibility. If consumers need more than current architecture supports, disclose the gap, prioritize improvement, provide a safer degraded path, or change the product promise. Never silently lower measurement quality to meet the target.

**Use error budgets with care.** The allowed nonconforming fraction `1-s` can balance reliability work and product change. Burn rate is observed nonconforming fraction divided by the budget fraction. A burn rate of two consumes budget twice as fast as planned if sustained.

Error budgets work best for high-volume repeatable behavior with reliable indicators. They do not make ten critical privacy breaches acceptable because a count budget remains. Add absolute policies and consequence classes.

**Define exclusion policy before incidents.** Legitimate exclusions might include demonstrably invalid requests or consumer-cancelled operations. Maintenance, upstream failure, provider failure, and force majeure may still affect consumers and should remain visible even if formal treatment differs.

Require reason, evidence, authority, scope, time, consumer impact, and review. Track both gross and adjusted performance. If exclusions grow when targets are missed, the objective has lost integrity.

**Aggregate without hiding harm.** Overall success rates can conceal failure concentrated in one region, tenant, subject class, product partition, or accessibility path. Define critical slices and minimums.

Weighting by volume may underrepresent low-volume high-consequence events. Pair population metrics with worst-case, percentile, critical-cohort, and absolute-failure rules. Review whether classification itself creates blind spots.

**Model dependency contributions.** List source, product, platform, network, identity, catalog, policy, provider, and human dependencies. Record their contracts, observed behavior, failure modes, ownership, and escalation.

Product targets cannot be composed by multiplying availability percentages blindly. Dependencies may be parallel, optional, cached, correlated, sequential, or used only for some populations. Model actual critical paths and validate end-to-end behavior.

**Design degraded modes.** A product may serve last-known-good data, partial populations, delayed partitions, or reduced interfaces. Declare age, missing scope, limitations, and consumer choices. Never make degraded output appear current or complete.

Some decisions must stop rather than degrade. Define fail-open, fail-closed, manual fallback, and override authority based on consequence. Test the path and preserve evidence.

**Align source, aggregate, and consumer products.** Source-aligned products often emphasize source fidelity, event capture, completeness, corrections, and publication time. Aggregate products emphasize input coverage, reconciliation, grain, transformation, restatement, and dependency behavior. Consumer-aligned products emphasize decision deadlines, interpretation, usability, representativeness, and outcome feedback.

The same vocabulary can apply, but measures differ. Reusing a generic target across alignments can mask the behavior each product owns.

**Build trustworthy telemetry.** The measurement pipeline is itself a data product. Define sources, clocks, identities, late observations, missing telemetry, transformations, retention, access, and validation. Monitor the monitor.

Prefer independent or consumer-boundary evidence for critical objectives. If the same failed pipeline emits both data and success telemetry, absence of failure signals can look like success. Missing observations should be explicit, not automatically good.

**Separate objective and diagnostic indicators.** Objective indicators describe consumer-facing outcomes. Diagnostic indicators help locate causes: source delay, queue backlog, resource saturation, schema rejection, validation failure, or access-policy error.

Too many objectives dilute attention. Maintain a small product scorecard and richer diagnostic observability. Every alert needs an owner, playbook, urgency, and useful action.

**Alert on budget and consequence.** Multi-window burn-rate alerts can detect rapid and gradual consumption while limiting noise. Absolute critical failures may alert immediately regardless of budget.

Alert routing should reflect product ownership and dependency context. Avoid paging for conditions the responder cannot change. Escalate missing authority or chronic dependency failure as governance and investment issues.

**Operate incident response.** Define detection, declaration, severity, command, containment, evidence, communication, correction, recovery, validation, closure, and learning. Data incidents may remain latent longer than application outages and require downstream impact analysis.

Notify consumers with affected product, versions, periods, populations, symptoms, current guidance, workaround, next update, and correction status. Protect sensitive incident details and legal privilege as applicable.

**Verify recovery end to end.** Confirm source arrival, transformation, quality, publication, interface, access, lineage, critical consumer results, and correction propagation. Reconcile control totals and sample semantics.

Close only after residual risk, missing populations, stale copies, failed consumers, and recurrence work are recorded. Operational restoration and complete remediation may have different dates.

**Govern semantic change as service behavior.** Contracts should define compatibility for names, types, meaning, grain, units, codes, time, population, quality, ordering, and error semantics. Semantic stability is often more valuable than raw uptime.

Publish notices with impact, versions, dates, migration, tests, support, and rollback. Measure notice and migration objectives. Emergency changes need bounded authority and retrospective review.

**Offer version-support expectations.** State how many versions are supported, for how long, with which defect and security treatment. Indefinite compatibility accumulates cost; abrupt deprecation externalizes cost to consumers.

Track active consumers and unknown-use signals. A support window is credible only when product capacity and dependencies can operate it. Retirement requires evidence beyond low query counts.

**Connect objectives to release decisions.** When budget is exhausted or objectives repeatedly fail, policy may slow risky changes and prioritize reliability. The response should reflect cause and consequence rather than punish all delivery mechanically.

Some changes improve reliability and should continue. Some failures result from unrealistic objectives or changed consumer need. Review with evidence while preventing teams from redefining targets solely to erase failure.

**Price expectations.** Stronger freshness, recovery, support, history, validation, isolation, and availability require infrastructure and people. Make cost and capacity visible by product and objective.

Consumers can choose tiers when risks permit, but protection and baseline integrity are not optional premium features. Chargeback or showback must not encourage hidden copies that evade governance.

**Review agreements before contractualizing them.** An SLA needs precise terms, dependencies, measurement authority, exclusions, remedies, liability, jurisdiction, security, privacy, records, and termination. Internal SLO performance should demonstrate capability first.

Contract penalties can create perverse incentives to exclude failures or avoid ambitious commitments. Preserve consumer outcomes and transparent gross measures. Qualified legal and commercial review is required.

**Manage providers.** Cloud, SaaS, data vendors, and external producers may offer their own SLAs. Map them to the product's end-to-end objectives, including support hours, data correctness, update schedules, correction, audit, access, exit, and incident notification.

A provider credit does not restore a missed regulatory decision. Keep internal recovery, contingency, evidence, and accountable ownership. Monitor observed performance instead of assuming contractual conformance.

**Protect service evidence.** Telemetry and incident records can reveal customer activity, sensitive volumes, system architecture, vulnerabilities, personnel, or legal analysis. Apply minimization, access, retention, encryption, segregation, and audit.

At the same time, do not make evidence inaccessible to authorized reviewers and consumers. Publish appropriate aggregate status and limitations while protecting underlying details.

**Use scorecards as decision instruments.** A good scorecard shows objective definition, current and historical performance, gross and adjusted results, budget remaining, critical slices, incidents, corrections, dependencies, uncertainty, and actions.

Avoid red-amber-green without numbers and definitions. Pair measures with narratives for low-volume or complex quality characteristics. Show missing telemetry and stale objectives.

**Audit objective integrity.** Sample eligible and excluded events, recompute indicators, trace data sources, test clocks, confirm consumer relevance, review alerts and response, and compare product claims to behavior. Independent review is valuable for high-consequence products.

Watch Goodhart effects: teams may reduce denominators, relabel failures, delay incident confirmation, close corrections early, or optimize one measure at the expense of another. Use multiple evidence paths and governance challenge.

**Exercise failure scenarios.** Test late source, missing partition, invalid values, schema drift, access outage, catalog error, corrupt recovery, provider failure, notification failure, unknown consumer, and simultaneous dependency events.

Measure detection, decision, communication, containment, replay, validation, and closure. Exercises reveal whether the published expectation is operable, not merely calculable.

**Review objectives through lifecycle.** Early products may publish cautious objectives and measurement limitations. Mature critical products need stronger evidence, capacity, recovery, and assurance. Declining products can reduce support only through consumer-aware change.

Revisit objectives after new consumers, changed consequence, architecture migration, provider change, repeated incidents, cost shift, regulation, reorganization, or retirement. Preserve historical definitions so performance trends remain interpretable.

**Treat unknown quality as unknown.** Missing telemetry, uncertain populations, unverified source controls, and incomplete lineage should not be counted as success. Label uncertainty and create an improvement plan.

The final test is whether a consumer can understand what behavior to expect, determine whether it fits a decision, observe meaningful current evidence, receive useful response when it fails, and plan for change. If not, the product has a service slogan rather than a service contract.

## Definitions and Notation

For an SLI, define eligible events `E` and good events `G ⊆ E`. Event-based attainment is `A = |G| / |E|` when `|E| > 0`. Empty-population handling must be declared; it should not silently report perfect performance.

For target success fraction `s`, the nominal bad fraction is `b = 1 - s`. Over `N` eligible events, nominal bad-event allowance is `B = bN`, subject to declared rounding. Observed burn rate is `R = ((|E|-|G|)/|E|) / b` for `b > 0` and nonempty `E`.

Represent an objective as `O = (behavior, indicator, population, window, target, clock, exclusions, measurement, breach, response, escalation)`. Two objectives with the same percentage but different populations or clocks are not equivalent.

For dependency graph `D = (P,E_d)`, each dependency edge records producer version, consumer version, required behavior, fallback, evidence, change, correction, and escalation. End-to-end behavior depends on topology, correlation, buffering, routing, and degraded modes, not percentages alone.

Let `Fit(P,U,t)` mean product `P` satisfies declared use requirements `U` at time `t`, including semantic, quality, service, protection, and support constraints. SLO attainment is relevant evidence but is not sufficient by itself.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for each material product service expectation.

**1. Consumer gate.** Name consumers, decisions, timing, consequence, alternatives, critical cohorts, and excluded uses.

**2. Behavior gate.** Define semantic, interface, freshness, latency, availability, quality, correction, recovery, support, and change behaviors.

**3. Measurement gate.** Specify indicators, eligible populations, good criteria, clocks, windows, aggregation, rounding, uncertainty, and trustworthy evidence.

**4. Target gate.** Justify objectives from need, risk, baseline, dependencies, architecture, capacity, cost, and protection constraints.

**5. Dependency gate.** Model critical paths, correlated failures, buffering, fallbacks, degraded modes, provider terms, and end-to-end validation.

**6. Operation gate.** Implement ownership, diagnostics, alerts, runbooks, support, incident response, communication, correction, and reconciliation.

**7. Protection gate.** Enforce safety, privacy, security, purpose, records, licensing, evidence protection, segregation, and absolute constraints.

**8. Change gate.** Govern semantic compatibility, versions, notice, testing, migration, emergency change, deprecation, and retirement.

**9. Evidence gate.** Preserve raw and derived telemetry, definitions, exclusions, incidents, decisions, outcomes, limitations, reviews, and reproducibility.

**10. Lifecycle gate.** Exercise, audit, learn, fund, revise, transfer, reduce, retire, archive, and close expectations as context changes.

The executable example computes event-based attainment, nominal bad-event allowance, observed bad events, and burn rate for a fully declared illustrative objective.

<!-- bijux-verify: {"id":"service-objective-arithmetic","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"eligible=10000\ngood=9985\ntarget=0.999\nattainment=0.9985\nnominal_bad_allowance=10.0\nobserved_bad=15\nburn_rate=1.5\nobjective_met=false\n","stderr":""}} -->
```python
eligible = 10_000
good = 9_985
target = 0.999

attainment = good / eligible
nominal_bad_allowance = (1 - target) * eligible
observed_bad = eligible - good
burn_rate = (observed_bad / eligible) / (1 - target)

print(f"eligible={eligible}")
print(f"good={good}")
print(f"target={target}")
print(f"attainment={attainment:.4f}")
print(f"nominal_bad_allowance={nominal_bad_allowance:.1f}")
print(f"observed_bad={observed_bad}")
print(f"burn_rate={burn_rate:.1f}")
print(f"objective_met={str(attainment >= target).lower()}")
```

The arithmetic establishes results only for the declared illustrative counts. It does not prove that events are independent, the population is complete, the target is appropriate, telemetry is correct, exclusions are legitimate, failures have equal consequence, a budget authorizes any particular incident, or a production product is fit. Those require consumer research, domain and risk judgment, telemetry validation, protected evidence, operational exercises, sampled recomputation, and accountable approval.

## Alternatives and Trade-Offs

**Event-based versus time-based objectives.** Event measures align with requests or publications; time measures align with continuous service. Each can hide failure modes the other reveals. Choose from consumer experience and use both where justified.

**Rolling versus calendar windows.** Rolling windows show recent behavior continuously but overlap and complicate formal settlement. Calendar windows match business periods but can hide boundary effects. Publish exact rules and complementary views.

**Uniform versus segmented objectives.** One target is simple and comparable but hides critical cohorts. Segmentation represents consequence more accurately while increasing operational complexity. Require a small set of meaningful critical slices.

**Strict target versus graceful degradation.** Strict service can protect decisions but cost more and reduce flexibility. Degraded service preserves partial value but risks misuse. Declare visible limitations and stop unsafe decisions.

**Producer-boundary versus consumer-boundary measurement.** Producer measures are easier to operate and diagnose; consumer measures better represent experience. Combine end-to-end objectives with internal diagnostics.

**Availability versus correctness priority.** Serving output maximizes continuity; withholding suspected output prevents harmful decisions. Choose fail-open, fail-closed, or bounded stale behavior by consequence and communicate state.

**Internal SLO versus contractual SLA.** Internal objectives support learning and improvement; agreements create external consequences and stronger stability needs. Demonstrate measurement and operations before contractualizing.

**Higher reliability versus delivery speed and cost.** More redundancy, validation, support, and recovery reduce failure but require resources and can slow change. Use consumer value, risk, and error-budget evidence rather than prestige targets.

## Failure Modes and Misconceptions

1. **A percentage is an SLO.** Population, behavior, window, clock, evidence, breach, and response are also required.
2. **Pipeline success means product success.** Consumer-facing data can remain stale, incomplete, wrong, or inaccessible.
3. **Freshness is the latest ingestion timestamp.** Expected events, source completeness, validation, and business time matter.
4. **Availability includes any returned data.** Stale, partial, invalid, or unauthorized output may fail other contracted behavior.
5. **Completeness can be measured from received rows alone.** Missing populations need independent expectation or reconciliation.
6. **Agreement with a source proves accuracy.** Source authority and real-world evidence require examination.
7. **Averages represent every consumer.** Tail and cohort failures can be hidden by volume.
8. **Dependencies compose by multiplying percentages.** Topology, correlation, caching, and optional paths determine end-to-end behavior.
9. **Every failure can be excluded.** Exclusions need prior policy, evidence, authority, visibility, and review.
10. **An error budget permits harmful incidents.** Absolute legal, safety, privacy, security, and critical-decision constraints remain.
11. **More nines always improve a product.** Unneeded reliability consumes resources and reduces change flexibility.
12. **An SLA creates capability.** Measurement, staffing, architecture, support, and recovery must already make it credible.
13. **Recovery ends when the job restarts.** Outputs, history, consumers, lineage, access, and corrections need validation.
14. **No alerts means objectives are met.** Telemetry and alerting can fail together.
15. **Schema stability means service stability.** Meaning, population, grain, codes, quality, and support can change.
16. **Provider credits compensate consumer harm.** Internal continuity, correction, communication, and accountability remain.
17. **Old objectives remain valid until breached.** Consumer, risk, architecture, cost, and lifecycle change can make them obsolete.

## Worked Examples

### Example 1

A daily finance product measures job completion. Consumers need reconciled balances by 05:30. The product adds eligible business-day publication, critical-book completeness, reconciliation variance, queryability, and correction-notice objectives.

### Example 2

A stream reports five-second average latency while rare events take minutes. A percentile and maximum critical-event objective exposes tail delay, with event-time clocks and missing-sequence detection.

### Example 3

A file endpoint returns yesterday's copy during an outage. Availability remains green, but freshness fails. The interface labels last-known-good age and blocks a consumer workflow whose policy prohibits stale decisions.

### Example 4

A quality score averages 99.99 percent across customers while one regulated region is missing. Critical-region completeness is defined as an absolute objective, preventing global volume from hiding the failure.

### Example 5

A provider misses its upstream SLA, and the data-product team excludes the event. Governance restores it to gross consumer performance, applies contractual treatment separately, and funds an internal fallback because provider credit cannot restore the decision.

### Example 6

An objective permits ten bad events monthly, but one event exposed protected data. The error budget does not apply as authorization; privacy and security incident paths, absolute controls, notification analysis, and corrective action govern the event.

### Example 7

A restored warehouse answers queries after corruption. End-to-end validation detects missing partitions and inconsistent aggregates. Recovery stays open until replay, reconciliation, consumer validation, and correction communication finish.

### Example 8

A product changes a status code meaning without changing its type. Semantic compatibility fails. The owner publishes a new version, gives notice and mapping, monitors migration, and supports the old version for the declared window.

### Example 9

Telemetry shows no failed publications because the failed scheduler emits no events. An independent expected-publication calendar identifies missing observations and converts absence from assumed success to explicit failure.

### Example 10

A quarterly product loses its final consumer. The team confirms reports, archives, legal holds, and unknown-use signals, announces retirement, preserves historical contracts and evidence, revokes access, and closes objectives after migration.

## Cross-Program Connections

- **Site reliability engineering:** indicators, objectives, budgets, burn rates, alerting, incidents, recovery, and learning provide operational mechanisms.
- **Data engineering:** orchestration, watermarks, tests, reconciliation, lineage, replay, backfill, serving, and observability generate service behavior.
- **Product management:** users, decisions, value, tiers, support, roadmaps, adoption, cost, and retirement justify expectations.
- **Platform engineering:** common telemetry, catalogs, identity, policy, delivery, incident tooling, and self-service make objectives scalable.
- **Security and privacy:** absolute constraints, risk, access, purpose, incident response, evidence, and recovery bound reliability optimization.
- **Software engineering:** API compatibility, semantic versioning, dependency management, deployment, testing, and deprecation shape product change.
- **Statistics and measurement:** populations, samples, bias, aggregation, uncertainty, percentiles, denominators, and reproducibility determine indicator validity.
- **Systems engineering:** stakeholder needs, interfaces, requirements, verification, fault analysis, assurance, configuration, and lifecycle govern service claims.

## References

1. Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds., *Site Reliability Engineering: Service Level Objectives*, Google, 2016. <https://sre.google/sre-book/service-level-objectives/>
2. Murphy, N. R., Beyer, B., Jones, C., and Petoff, J., eds., *The Site Reliability Workbook: Implementing SLOs*, Google, 2018. <https://sre.google/workbook/implementing-slos/>
3. ISO/IEC, *25012:2008 Software engineering—Software product Quality Requirements and Evaluation (SQuaRE)—Data quality model*, 2008. <https://www.iso.org/standard/35736.html>
4. ISO/IEC, *25024:2015 Systems and software engineering—SQuaRE—Measurement of data quality*, 2015. <https://www.iso.org/standard/35749.html>
5. W3C, *Data on the Web Best Practices: Data Quality Vocabulary*, W3C Note, 2016. <https://www.w3.org/TR/vocab-dqv/>
6. W3C, *Data Catalog Vocabulary (DCAT)—Version 3*, W3C Recommendation, 2024. <https://www.w3.org/TR/vocab-dcat-3/>
7. NIST, *Systems Security Engineering: Considerations for a Multidisciplinary Approach in the Engineering of Trustworthy Secure Systems*, SP 800-160 Volume 1 Revision 1, 2022. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>
8. Pascoe, C., Quinn, S., and Scarfone, K., *The NIST Cybersecurity Framework (CSF) 2.0*, NIST CSWP 29, 2024. <https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20>

## Exercises

### Exercise 1

Design service expectations for a daily Cash Position product used before market open. Define consumers, decisions, indicators, populations, clocks, targets, exclusions, critical cohorts, dependencies, response, protection, and review.

### Exercise 2

Evaluate an existing “99.9% data quality” claim. Replace it with reproducible objectives for completeness, validity, freshness, consistency, correction, and consumer support, including exact evidence and limitations.

### Exercise 3

Calculate and interpret the nominal error budget and burn rate for 200,000 eligible events, a 99.95% objective, and 240 bad events. Explain why the calculation does not authorize every counted failure.

### Exercise 4

Design a recovery exercise for a product with one source, one aggregate, two interfaces, cached degraded service, and three critical consumers. Include corruption, telemetry failure, replay, reconciliation, communication, and closure.

### Exercise 5

Create an objective-governance policy covering definition, approval, baselining, measurement, exclusions, alerts, incident response, budget decisions, changes, providers, audit, lifecycle review, and retirement.

## Answers to the Exercises

### Answer 1

Name treasury operators and the funding decisions they make before each market opens. Eligible events are declared market-business days per legal entity. Define validated publication by 05:30 local market time, 100 percent representation of critical bank accounts, reconciled control totals within approved currency-specific thresholds, query success within latency bounds, and confirmed material-error notification within fifteen minutes. State daylight-saving, holiday, late-source, partial-day, and empty-population rules.

Evidence comes from an independent expected-publication calendar, source manifests, reconciliation controls, consumer-boundary queries, and incident records. Segment critical legal entities rather than averaging by volume. Dependencies include bank feeds, exchange rates, identity, platform, and support. Degraded output displays age and missing accounts; high-consequence funding can stop. Define owner, on-call, escalation, replay, historical restatement, privacy and security controls, gross and adjusted measures, monthly review, exercises, and change triggers.

### Answer 2

First reject the original number because its characteristic, population, method, window, and use are absent. Define completeness as received expected account-day records divided by an independently reconciled manifest, with absolute critical-account coverage. Define validity as records passing versioned domain rules, while reporting rejected and coerced records separately. Define freshness as elapsed time from expected source close to validated consumer queryability, not ingestion time.

Define consistency through cross-field, temporal, source-to-product, and aggregate reconciliation rules. Define correction clocks from confirmed material defect to containment, notice, corrected publication, downstream validation, and closure. Define support acknowledgement and update objectives by severity and hours. For every indicator record population, event, good criteria, source, calculation, window, target, clock, exclusions, uncertainty, owner, breach, and response. Publish missing telemetry and limitations; sampled accuracy requires separate authoritative evidence.

### Answer 3

The target is `s = 0.9995`, so nominal bad fraction is `0.0005`. For `N = 200,000`, nominal allowance is `(1 - 0.9995) × 200,000 = 100` bad events. Observed bad fraction is `240 / 200,000 = 0.0012`. Burn rate is `0.0012 / 0.0005 = 2.4`, so the population consumed budget at 2.4 times the planned rate and attainment was `199,760 / 200,000 = 99.88%`, below target.

Interpretation depends on eligibility, clocks, window, rounding, telemetry, and event consequence. The arithmetic treats counted events uniformly, but policy must not. A privacy breach, unsafe decision, regulatory miss, or critical-cohort omission can require immediate action regardless of remaining nominal budget. Exclusions require prior rules and evidence. The result guides reliability decisions; it is not permission for a particular failure.

### Answer 4

Inject a source delay followed by a corrupt late file while suppressing one ordinary telemetry signal. The independent expected-arrival control must detect absence. Trace source, aggregate, table, and API behavior. The cache serves last-known-good output with visible age; one critical consumer may continue under policy while another stops. Exercise declaration, owner and dependency routing, evidence protection, consumer messages, update cadence, and provider escalation.

Restore source evidence, quarantine corruption, replay idempotently, deduplicate, preserve ordering, recalculate the aggregate, and reconcile control totals and critical cohorts. Validate both interfaces, access, lineage, quality, and consumer results. Identify exports and decisions made during degradation. Correction communication distinguishes original and restated values. Closure records detection and recovery clocks, blind telemetry, residual risk, recurrence actions, accountable acceptance, and a retest. Restarting jobs alone does not pass.

### Answer 5

Require a product owner and named consumer evidence for every objective. Definitions include behavior, indicator, eligible and good events, population, critical slices, window, timezone, target, clock, exclusions, measurement source, rounding, uncertainty, breach, response, and escalation. Baseline observed behavior before durable commitment and approve targets using consequence, dependencies, architecture, capacity, cost, and protection review.

Operate trustworthy telemetry, missing-observation detection, diagnostics, consequence and burn-rate alerts, runbooks, support, incident response, correction, recovery, and communication. Predefine exclusion authority and show gross and adjusted results. Error-budget policy cannot override absolute controls. Version objective changes and prevent retroactive redefinition. Map provider terms without transferring internal accountability. Sample events and exclusions, recompute measures, exercise failure, and review Goodhart risks. Reassess after consumer, architecture, provider, risk, cost, or organizational change; retire objectives only with product-consumer and archival closure evidence.
