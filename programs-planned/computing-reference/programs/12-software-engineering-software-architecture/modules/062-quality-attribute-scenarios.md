---
module_id: SARCH-062
program: Software Engineering: Software Architecture
level: 2
module_number: 62
title: Quality-Attribute Scenarios
status: complete
last_verified: 2026-09-06
---

# Quality-Attribute Scenarios

## One-Page Review

### Governing question

How can architects turn words such as fast, available, secure, modifiable, usable, and sustainable into bounded scenarios that expose decisions, support evidence, and resist ambiguity and metric gaming?

### Essential definitions

- A **quality attribute** is a measurable or assessable property expressing how well a system behaves or can be changed in a context; quality models organize such properties but do not set stakeholder priorities [1, 2].
- A **quality-attribute scenario** contains six parts: stimulus source, stimulus, environment, affected artifact, expected response, and response measure [1, 3].
- A **general scenario** is a reusable domain-independent pattern; a **concrete scenario** binds the pattern to named actors, system parts, conditions, and thresholds.
- A **stimulus** is an event or condition requiring a system response; its **source** identifies who or what produces it.
- The **environment** names operating state and relevant conditions when the stimulus arrives.
- The **artifact** is the part of the system, data, process, organization, or interface affected.
- The **response** states observable behavior; the **response measure** defines how success, failure, or uncertainty is judged.
- A **quality-attribute utility tree** groups and prioritizes scenarios; it does not make ordinal labels into cardinal utility.
- An **oracle** determines whether evidence satisfies the measure.
- A **guardrail** is a non-negotiable bound that constrains optimization of another measure.

### Central model, mechanism, or theorem

A scenario is the tuple

$$
Q=(src,stim,env,art,resp,meas).
$$

It is analysis-ready only if each component is specific enough to trace through architectural decisions and produce an observable verdict. A useful measure often combines a target with scope:

$$
M=(population,operation,workload,statistic,threshold,window,exclusions).
$$

“p99 latency below 300 ms” is incomplete without operation, admitted workload, measurement boundary, population, window, correctness guardrails, and treatment of timeouts. A scenario suite, not one metric, represents a quality across nominal, boundary, degraded, recovery, change, misuse, and adversarial conditions.

### Critical invariants

- each scenario names all six parts or explicitly records the unresolved part;
- source and affected artifact use durable identities rather than “user” and “system” when distinctions matter;
- environment includes load, data state, topology, lifecycle mode, dependency state, and threat conditions relevant to the claim;
- the response is externally or independently observable and distinct from the mechanism intended to produce it;
- measures specify units, population, statistic, threshold, time window, boundary, and exclusions;
- correctness, safety, security, privacy, accessibility, and fairness guardrails prevent a narrow metric from rewarding harm;
- missing, rejected, timed-out, cached, degraded, and unknown outcomes are classified rather than omitted;
- scenario priority reflects drivers, consequences, obligations, uncertainty, and stakeholder legitimacy—not vote count alone;
- evidence identifies architecture, version, configuration, workload, data, tool, and limitations;
- no passing scenario becomes a universal quality claim.

### Common failures

Common failures include treating an attribute label as a requirement; omitting environment; naming a technology as the response; measuring only averages; excluding errors from latency; using synthetic load unlike admitted demand; observing the component rather than the user outcome; confusing a target with an SLO or guarantee; optimizing availability with stale or incorrect responses; writing security scenarios without adversaries; measuring accessibility through page-load time; treating modifiability as lines changed; ignoring deployment, rollback, and data migration; averaging away minority harm; and keeping only scenarios that are easy to test.

### Compact example

Source: an authenticated tenant administrator. Stimulus: revoke one compromised analyst session. Environment: normal operation while the central identity service is unreachable and 20,000 sessions remain active. Artifact: authorization caches, gateways, and audit trail. Response: the named session loses read and export authority while unrelated valid sessions continue; the event remains attributable. Measure: revocation becomes effective at every enforcement point within 60 seconds, no post-deadline protected read succeeds, at least 99.9% of unrelated requests remain within their 500-ms target, and missing enforcement evidence fails the scenario. This exposes cache lifetime, invalidation, identity dependency, authorization locality, and audit decisions.

### Connections

[SARCH-061](061-architecture-tradeoff-analysis-method.md) uses scenarios within ATAM. [SARCH-063](../ROADMAP.md) next derives risk, sensitivity, and trade-off points from scenario-decision analysis. Testing Engineering owns detailed test design; Requirements Engineering owns broader requirement elicitation; this module owns architectural quality scenarios.

## Governing Question

Quality words compress incompatible meanings. “Available” can mean a process responds, a correct read succeeds, a payment reaches a terminal state, or a clinician retains safe access. “Modifiable” can mean changing code, deploying a compatible fleet, migrating data, retraining people, or obtaining regulatory approval.

A quality-attribute scenario expands the word into a falsifiable situation. Its purpose is not grammatical completeness. It must expose which architectural decisions matter, which evidence could discriminate alternatives, and where stakeholder values or obligations conflict.

## Why This Matters

Functional requirements say what capability exists. Architecture is often determined by the difficult conditions under which that capability must remain useful, safe, secure, changeable, affordable, or operable. Vague qualities invite teams to optimize convenient proxies and discover the real contract during incidents or migrations.

Scenarios create traceability from concern to mechanism and evidence. They improve architecture evaluation, prototypes, capacity models, threat analysis, recovery exercises, fitness functions, and acceptance discussions. They also make uncertainty visible: if response or measure cannot be stated, the architecture decision is not ready for confident comparison.

## Prerequisites and Retrieval

Retrieve stakeholder, concern, quality attribute, driver, constraint, source, stimulus, environment, artifact, response, measure, population, unit, threshold, distribution, percentile, quantile, window, workload, state, oracle, guardrail, leading indicator, lagging indicator, proxy, confounder, baseline, scenario suite, traceability, evidence, and residual risk.

From SARCH-004 through SARCH-020 retrieve quality attributes and tactics. SARCH-021 through SARCH-030 supply architecture views. SARCH-051 through SARCH-060 supply advanced failure environments and evidence, while SARCH-061 supplies the ATAM context. Retrieve elementary probability summaries and dimensional consistency where quantitative measures are used.

## Learning Objectives

After completing this module, you should be able to:

1. construct complete six-part quality-attribute scenarios;
2. refine general scenarios into system-specific architectural probes;
3. define measures with units, populations, statistics, thresholds, windows, and exclusions;
4. distinguish stakeholder outcomes, system responses, mechanisms, and evidence;
5. write performance, availability, security, modifiability, usability, and operability scenarios;
6. include data, sustainability, privacy, accessibility, safety, and cost guardrails where relevant;
7. design nominal, boundary, degraded, recovery, evolution, and adversarial scenario suites;
8. detect proxy gaming, survivor bias, aggregation loss, and incompatible measurement boundaries;
9. trace scenarios to views, decisions, owners, tests, and evidence expiry;
10. review a scenario portfolio for coverage without claiming completeness.

## Core Exposition

**Begin with a consequential concern.** Ask who experiences value or harm, what event makes the quality visible, and which architectural decision is pending. “The service should be scalable” is not yet a scenario. “During a ticket release, admitted checkout requests rise from 2,000 to 8,000 per second within two minutes” supplies a concrete stimulus and environment.

Do not force every concern into a familiar label before understanding it. A public-warning delay may combine timeliness, accessibility, authority, and safety. Preserve the outcome, then use attribute tags for organization.

**Name the source precisely.** Sources can be end users, operators, attackers, developers, auditors, devices, dependencies, laws, markets, disasters, or time. Distinguish authenticated administrator from ordinary user, insider from external attacker, and primary provider from delayed callback.

Source characteristics affect architecture. Tenants may differ in size and jurisdiction; devices may be compromised; maintainers may lack production access; emergency responders may operate offline. “A user” erases these differences.

**Specify the stimulus.** A stimulus is what happens, not the desired result. It can be a request, load increase, component failure, credential revocation, data deletion, schema change, defect report, attack, legal request, energy constraint, or operator mistake.

Include magnitude, rate, sequence, duration, and identity when they matter. “Traffic increases” becomes “authenticated writes increase from 1,000 to 5,000 per second over 90 seconds while one shard holds 35% of keys.” Compound stimuli should be explicit rather than hidden in environment prose.

**Bound the environment.** State normal, peak, degraded, recovery, deployment, maintenance, disconnected, compromised, or disaster conditions. Add workload mix, data volume and skew, cache warmth, topology, dependency health, software/schema version, resource limits, time synchronization, and operator availability relevant to the claim.

An environment is not an excuse to assume away the risk. If the scenario says “under normal conditions,” define normal and add separate boundary cases. A response proven with warm cache and empty queue cannot silently transfer to cold recovery with backlog.

**Identify the artifact.** Name the affected decision surface: API boundary, authorization path, queue, partition map, deployment pipeline, schema, operator console, physical controller, data product, or organizational handoff. Often several artifacts form the end-to-end path.

Avoid “the system” when a more precise path would reveal ownership. Also avoid overfitting to one class or service name if the architectural decision spans a durable responsibility.

**State response before mechanism.** A response describes observable behavior: accept, reject, degrade, isolate, preserve, notify, recover, reconcile, adapt, or support a change. “Autoscale” and “use a cache” are mechanisms. The response might be “admitted correct reads remain within the bound”; several mechanisms could achieve it.

This distinction keeps alternatives open. It also reveals when a mechanism produces the wrong outcome: a queue may absorb load yet violate freshness, or failover may restore traffic yet permit stale writes.

**Make the measure operational.** State measurement start and end, units, population, statistic, threshold, window, sampling, missing-data treatment, and exclusions. Define the clock and observer. Latency can be client-observed, gateway, service, or database time; these are not interchangeable.

Use distributions rather than only averages when tails matter. A percentile is a population statistic, not a maximum. State whether timeouts are included, assigned a bound, or separately limited. A p99 target allows 1% beyond the quantile; at one million requests that is 10,000 observations, subject to the exact quantile definition.

**Pair targets with correctness guardrails.** Fast errors do not satisfy useful latency. Cached responses do not satisfy availability if too stale for the decision. Lower storage cost does not satisfy efficiency if durability, deletion, or restore breaks.

A scenario can therefore contain multiple measures: latency, correct terminal-outcome rate, duplicate-effect count, stale-data age, resource ceiling, and recovery tail. Identify which are mandatory gates and which support comparison.

**Use measures appropriate to the attribute.** Performance scenarios measure response time, throughput, jitter, deadline misses, queue age, or resource use under workload. Availability scenarios measure useful correct service, impact duration, data loss, degraded scope, and reconciled recovery under faults.

Security scenarios name asset, actor or adversary, capability, access path, environment, prevention/detection/containment/recovery response, and evidence. “No breach” is not a practical oracle. Test authorization, confidentiality, integrity, audit, revocation, and recovery at explicit boundaries.

Modifiability scenarios name who changes what, when, under which compatibility and operating constraints. Measures may include affected responsibilities, independently deployable units, elapsed lead time, migration duration, coexistence window, rollback or forward-repair capability, and evidence—not lines of code alone.

Usability and accessibility scenarios name users, assistive technology, task, context, response, completion, errors, recovery, cognitive load, and relevant conformance criteria. WCAG 2.2 is an authoritative current web-accessibility recommendation, but conformance to selected criteria does not replace representative user evidence [4].

Operability scenarios name operator, signal, incident state, decision, control surface, response, time, and outcome. Observability is useful only if the signal supports the required inference and action. Test absent, delayed, contradictory, high-cardinality, and compromised telemetry.

**Cover change and lifecycle.** Quality appears during build, deploy, migration, operation, recovery, and retirement. Include schema evolution, mixed-version fleets, certificate rotation, tenant movement, provider exit, deletion, restore, and decommissioning.

A design may be modifiable in source code yet impossible to roll out safely across offline devices. A privacy deletion may work in the primary store yet resurrect from backup. Scenarios must cross lifecycle boundaries relevant to the driver.

**Construct a scenario family.** Begin with a general pattern, then create nominal, boundary, degraded, recovery, evolution, and adversarial variants. Change one dimension at a time for diagnosis, then combine high-risk factors to expose interactions.

For availability, variants might cover one process crash, zone loss, control-plane loss, identity outage, slow dependency, full queue, stale writer, restore, second fault during recovery, and compromised credentials. For modifiability, cover additive change, semantic change, data migration, rollback, parallel versions, emergency patch, and supplier replacement.

**Use generic scenarios carefully.** Catalogs improve recall and comparability. They can also create checkbox behavior. Refine generic “request arrives under peak load” into the actual operation, distribution, data, topology, and consequences.

When two systems use similar concrete scenarios, shared terminology helps platform decisions. Do not force identical thresholds where stakeholder outcomes differ.

**Elicit from diverse stakeholders.** Ask each group for a stimulus that could make the system valuable, costly, harmful, or hard to change. Operators see recovery and diagnosis; security teams see adversaries; finance sees cost volatility; users see task and access failure; developers see coupling; governance sees lifecycle and evidence.

Voting is an input, not legitimacy. Preserve severe minority, mandatory, privacy, security, safety, accessibility, and legal scenarios even when few participants represent them. Record dissent and participation gaps.

**Prioritize transparently.** Link scenarios to drivers and consequences. Consider importance, difficulty, uncertainty, irreversibility, affected population, obligations, novelty, incident history, and decision timing. High/Medium/Low categories are ordinal unless a separate elicitation establishes quantities.

Select a balanced portfolio rather than ten variants of peak latency. Record why scenarios are selected, deferred, delegated, or out of scope. Unselected does not mean low consequence.

**Trace to architecture.** For each scenario, trace stimulus through runtime, data, deployment, control, trust, and organizational views. Identify decisions, resources, dependencies, authority, queues, timing, and evidence. The trace exposes sensitivity and tradeoffs for SARCH-063.

If no decision changes the response, the scenario may be at the wrong abstraction or the architecture description may be incomplete. If every box is implicated, decompose the path while retaining the end-to-end oracle.

**Design the oracle.** Prefer an observer outside the affected boundary when possible. Use durable identities to connect attempts and effects. Combine telemetry with authoritative data, client observations, security evidence, physical sensors, or human-task outcomes appropriate to the claim.

Missing data is an outcome. A metric pipeline failing during the incident cannot report zero errors. Define clock uncertainty, sampling loss, aggregation, and retention. Preserve raw evidence needed to validate derived statistics.

**Resist metric gaming.** Goodhart's law is often paraphrased as a warning that a measure used as a target can stop being a good measure. Campbell similarly warned that intensive use of quantitative indicators for decisions creates pressure that can corrupt both the indicator and the process it monitors [10]. The durable response is not to avoid measures; it is to connect them to outcomes, add guardrails, audit exclusions, rotate adversarial cases, and retain qualitative review.

Examples of gaming include dropping slow requests before measurement, excluding failed deployments from lead time, splitting incidents, serving stale cache as success, or reducing test coverage to shorten builds. Scenario suites make these boundary choices visible.

**Calibrate evidence strength.** A calculation supports a model under assumptions. A benchmark supports the recorded workload and environment. A fault exercise supports injected cases. A usability study supports its participants and tasks. A conformance check supports the cited criteria and version.

Record architecture revision, implementation, configuration, data, tool, workload, sample, observer, result, anomaly, and limitation. Define expiry when a decision, dependency, workload, threat, population, standard, or lifecycle state changes materially.

**Manage conflicts explicitly.** One scenario can improve while another worsens. Longer authorization caching improves latency and outage continuity but delays revocation. Synchronous replication may improve acknowledged durability while increasing latency and partition unavailability.

Do not average incomparable units into one quality score. Present a decision's response vector and guardrails. Accountable stakeholders decide which tradeoffs are permissible; architecture analysis makes consequences and uncertainty legible.

**Review the portfolio.** Check all six parts, measurement operability, driver trace, stakeholder representation, decision sensitivity, lifecycle, failures, adversaries, minority harm, and evidence plan. Search for duplicate scenarios with different wording and distinct scenarios accidentally merged.

No finite portfolio is complete. Report selected dimensions, omissions, unresolved measures, and future triggers. The value is disciplined coverage, not the fiction that every possible stimulus has been enumerated.

## Definitions and Notation

Let:

- $Q=(src,stim,env,art,resp,meas)$ be one quality-attribute scenario;
- $N$ be the number of eligible observations and $k$ the number violating a gate;
- $r=k/N$ be observed violation proportion for a named population and window;
- $L_q$ be latency quantile $q$ under a declared quantile convention;
- $T_b$ and $T_e$ be measurement-boundary start and end times;
- $W$ be the recorded workload, topology, data, version, and configuration;
- $G$ be mandatory guardrails and $O$ the oracle set;
- $S$ be a scenario suite and $C$ the set of reviewed coverage dimensions;
- **survivor bias** mean measuring only observations that reach a selected endpoint;
- **proxy** mean an indirect measure used in place of the stakeholder outcome;
- **measurement validity** mean whether the procedure supports the intended interpretation.

If $q=0.99$ and $N=1{,}000{,}000$, as many as $0.01N=10{,}000$ observations can lie beyond the p99 quantile boundary, depending on convention and ties. A p99 target therefore needs timeout, error, maximum-harm, and population guardrails where individual misses matter.

## Mechanisms, Invariants, or Proof Structure

### Scenario-construction procedure

1. Name stakeholder outcome, harm, pending decision, and accountable owner.
2. Identify a precise source and stimulus with magnitude, identity, timing, and sequence where relevant.
3. Bound environment by workload, state, topology, dependencies, lifecycle, threat, and people.
4. Name the affected architectural responsibility and end-to-end path.
5. State an observable response without prescribing the mechanism.
6. Define measures, boundaries, units, population, statistic, threshold, window, exclusions, and missing-data policy.
7. Add correctness, security, privacy, safety, accessibility, fairness, cost, and sustainability guardrails as applicable.
8. Create nominal, boundary, degraded, recovery, evolution, misuse, and adversarial variants.
9. Trace to drivers, decisions, views, owners, evidence, and expiry conditions.
10. Review prioritization, representation, gaming, uncertainty, and portfolio omissions.

### Proof obligations

- **Completeness of form:** Can a reviewer identify all six scenario components?
- **Causal relevance:** Does the stimulus exercise a decision that could alter the response?
- **Measurability:** Can an independent oracle obtain evidence for every gate?
- **Dimensional validity:** Do thresholds have defined units and compatible boundaries?
- **Population validity:** Are failures, timeouts, minority cohorts, and missing observations included correctly?
- **Transfer validity:** Are workload, topology, versions, data, participants, and exclusions close enough to the claimed context?
- **Anti-gaming:** Could the system improve the metric while harming the outcome?
- **Governance:** Does competent authority own mandatory consequences and residual uncertainty?

### Invariants

- no adjective substitutes for a six-part scenario;
- no response is specified only as a favored mechanism;
- no percentile omits its population, errors, timeouts, window, or boundary;
- no availability measure rewards stale, incorrect, unauthorized, or duplicate outcomes;
- no aggregate erases a consequential cohort without separate review;
- no priority vote overrides mandatory or severe-harm guardrails;
- no evidence transfers beyond its recorded configuration and expiry conditions;
- no scenario suite claims exhaustive quality coverage.

## Alternatives and Trade-Offs

- **Quality model versus stakeholder elicitation:** models improve vocabulary and recall; elicitation discovers contextual value and harm. Use both without treating taxonomy as priority.
- **General versus concrete scenario:** general scenarios aid reuse; concrete scenarios expose system decisions and measurable evidence.
- **Single measure versus response vector:** one measure communicates simply; multiple gates preserve correctness and competing qualities.
- **Average versus percentile:** averages summarize total tendency; percentiles reveal distribution tails but still hide maxima, cohorts, and timeouts.
- **Synthetic versus production workload:** synthetic load is controlled; production evidence is realistic but variable, risky, and historically bounded.
- **Component versus end-to-end measure:** component metrics diagnose mechanisms; end-to-end metrics represent stakeholder outcomes but complicate attribution.
- **Strict threshold versus distribution:** thresholds support decisions; distributions reveal sensitivity and cliffs. Preserve both when useful.
- **Broad suite versus deep evidence:** breadth covers more conditions; depth strengthens fewer claims. Prioritize and preserve gaps.
- **Stable scenarios versus evolving scenarios:** stable identities support longitudinal comparison; drivers, threats, standards, and architecture changes require revision and versioning.
- **Shared platform target versus product-specific target:** common targets improve governance; product contexts may require different populations, harm bounds, and workloads.
- **Leading versus lagging indicators:** leading signals enable intervention; lagging outcomes validate consequence. A strong suite connects them.
- **Quantitative versus qualitative measure:** quantities enable reproducibility; human, ethical, and contextual outcomes may require structured qualitative evidence and competent review.

## Failure Modes and Misconceptions

1. **“Performance means fast.”** Operation, workload, population, statistic, boundary, and correctness are missing.
2. **“Availability is uptime.”** Useful correct service and business completion can fail while processes run.
3. **“Security has no measurable scenarios.”** Prevention, authorization, detection, containment, recovery, and audit can have bounded evidence.
4. **“A technology name is a response.”** It prescribes a mechanism and hides alternatives.
5. **“The environment is normal production.”** Normal must be defined and boundary states added.
6. **“p99 covers everyone.”** It permits a tail and may omit timeouts or cohorts.
7. **“Errors should be excluded from latency.”** Exclusion can reward fast failure unless a separate gate constrains it.
8. **“One scenario represents an attribute.”** Qualities vary across nominal, failure, recovery, change, and adversarial conditions.
9. **“More scenarios mean better coverage.”** Near-duplicates can crowd out consequential dimensions.
10. **“Votes determine legitimacy.”** Obligations and severe minority harm are not popularity contests.
11. **“Lines changed measure modifiability.”** Coordination, migration, deployment, rollback, learning, and validation may dominate.
12. **“WCAG conformance proves usability.”** It covers named criteria, not every user, task, device, or context.
13. **“A dashboard is an oracle.”** It may share the fault boundary, aggregate loss, or encode the wrong outcome.
14. **“Missing telemetry is zero impact.”** Absence must be classified and independently checked.
15. **“A target is a guarantee.”** Evidence, scope, and authority determine the claim.
16. **“One number combines tradeoffs.”** Incomparable qualities and values should not be hidden by arbitrary weights.
17. **“Passing evidence never expires.”** Architecture, workload, population, threat, and standards change.
18. **“A scenario portfolio is complete.”** Finite selection always leaves reported uncertainty.

## Worked Examples

### Example 1

**Refine a performance adjective.**

**Situation.** A team requires “fast product search.”

**Reasoning.** Source: authenticated shopper. Stimulus: query with three filters. Environment: 8,000 searches/s, catalog 50 million items, one search replica unavailable, cache mix recorded. Artifact: search API and index path. Response: return a correct, permission-filtered first page or explicit overload response. Measures: client-observed p95 below 400 ms and p99 below 900 ms over five minutes; errors below 0.2%; timeouts count as 2 seconds; freshness under 60 seconds; no hidden product leaks.

**Conclusion.** The scenario exposes indexing, caching, admission, replica, filtering, and measurement decisions that “fast” hides.

### Example 2

**Catch survivor bias in latency.**

**Situation.** A dashboard reports p99=250 ms after dropping all requests that exceed a one-second gateway timeout.

**Reasoning.** The percentile population includes only survivors, so the slowest and failed observations disappear. The corrected scenario measures client intents, assigns timed-out intents a declared censored or failing outcome, and separately gates success rate and terminal business state. It also reports conditional latency for successful requests as diagnostic evidence, not the service claim.

**Conclusion.** A precise population and timeout rule prevent apparent latency improvement through failure.

### Example 3

**Make availability useful.**

**Situation.** An order service returns HTTP 200 from stale cache while the checkout writer is unavailable.

**Reasoning.** A process-response metric counts success, but shoppers cannot create orders and shown inventory is 40 minutes stale. The scenario separates browse and checkout operations, labels cache age, requires a correct terminal order state for admitted checkout, and permits read-only degraded browsing only within a five-minute freshness bound. Unknown payment outcomes remain failures until reconciled.

**Conclusion.** Availability is scoped useful service, not any response from a live process.

### Example 4

**Write a security-revocation scenario.**

**Situation.** An analyst credential is compromised while the identity provider is unreachable.

**Reasoning.** Source: authenticated security responder. Stimulus: revoke the named session and export capability. Environment: identity outage, 20,000 sessions, normal analytical traffic. Artifact: gateways, authorization caches, data service, audit. Response: deny the compromised identity, retain unrelated valid service, and record attributable enforcement. Measures: all enforcement points effective within 60 seconds, zero protected reads afterward, unrelated request success above 99.9%, and missing audit evidence fails.

**Conclusion.** The scenario exposes cache invalidation, local authorization, identity dependency, and audit without prescribing one product.

### Example 5

**Measure modifiability across rollout.**

**Situation.** A tax rule changes for one jurisdiction while mobile clients may remain old for 90 days.

**Reasoning.** Source: authorized policy owner. Stimulus: add the dated rule. Environment: three API versions, mixed client fleet, month-end load, rollback required. Artifact: policy model, calculation service, data schema, APIs, audit, deployment. Response: old and new clients receive correct dated calculations, rules remain attributable, and rollback or forward repair preserves issued records. Measures cover affected responsibilities, lead time, compatibility window, migration duration, defect gates, and zero unexplained historical rewrite.

**Conclusion.** Lines changed would miss compatibility, data, deployment, audit, and repair—the architectural cost of change.

### Example 6

**Use an accessibility guardrail.**

**Situation.** A redesigned incident console reduces median task time but removes keyboard access to the emergency action.

**Reasoning.** The scenario names operators using keyboard-only and screen-reader interaction under alert load. Response measures include successful identification and execution, error and recovery, time distribution, focus order, accessible name/state, and applicable WCAG 2.2 criteria. Median improvement for mouse users cannot pass if the mandatory action is unavailable to the named cohort.

**Conclusion.** Aggregate usability optimization needs accessibility and severe-task guardrails.

### Example 7

**Interpret a p99 bound.**

**Situation.** A service processes one million eligible operations and claims that p99 below 300 ms means nearly all users meet 300 ms.

**Reasoning.** One percent of one million is 10,000 observations. Depending on quantile convention and ties, the p99 boundary says nothing about how far beyond 300 ms those observations lie. The scenario adds timeout and error gates, p99.9 or maximum-harm bounds where justified, cohort breakdown, and raw tail distribution.

**Conclusion.** A percentile is useful only with a defined population and tail guardrails.

### Example 8

**Create a recovery family.**

**Situation.** A regional service has one scenario for process restart.

**Reasoning.** The team derives variants for application-zone loss, database quorum loss, global identity outage, control-plane loss, stale writer on return, cold bootstrap without artifact registry, full replay queue, second fault during recovery, and compromised credentials. Every variant shares durable outcome identities and measures impact, authority, useful service, data integrity, backlog, and reconciliation.

**Conclusion.** A scenario family reveals architectural dimensions that repeated process kills cannot cover.

### Example 9

**Reject an energy-only optimization.**

**Situation.** A batch platform proposes shutting workers down aggressively to minimize kilowatt-hours.

**Reasoning.** Source: scheduler under low-carbon operating policy. Stimulus: carbon-intensity rise and workload arrival. Environment: deadline-bound regulatory jobs and interruptible analytics. Artifact: admission, placement, checkpointing, and workers. Response minimizes measured energy and shifts flexible work while mandatory jobs meet deadlines, data locality and privacy, checkpoint durability, and restart limits. Measures include energy at a declared boundary, completion, retry work, hardware state, and excluded embodied impacts.

**Conclusion.** Sustainability measures need workload, boundary, and correctness guardrails to avoid shifting harm.

### Example 10

**Trace one scenario across views.**

**Situation.** A hospital must restore medication history during regional isolation.

**Reasoning.** Runtime trace follows clinician request, local identity, cache, record authority, synchronization, and audit. Data view distinguishes verified history, pending updates, provenance, and privacy deletion. Deployment view exposes regional and hospital dependencies. Trust view covers emergency authority. Operational view covers stale-data display, reconciliation, and manual escalation. Measures address access time, maximum age, missing records, unauthorized exposure, clinician acknowledgement, and post-recovery conflicts.

**Conclusion.** An end-to-end scenario coordinates multiple architecture views while keeping distinct oracles and owners.

## Cross-Program Connections

- **Software Testing and Quality Engineering:** owns test oracles, coverage, workload design, measurement error, reproducibility, and evidence strength.
- **Software Delivery and Reliability Engineering:** owns SLIs, SLOs, incidents, recovery exercises, deployment performance, and production observation.
- **Requirements Engineering:** owns broader stakeholder elicitation, requirement quality, conflict, traceability, validation, and change.
- **Security Engineering:** owns adversary models, assets, authorization, detection, containment, recovery, assurance, and security testing.
- **Systems Engineering:** owns physical hazards, stakeholder needs, verification, validation, lifecycle assurance, and acceptance authority.
- **Data Architecture Engineering:** owns data quality, authority, lifecycle, residency, deletion, lineage, and governance scenarios.
- **API and Service Engineering:** owns client-visible latency, error, deadline, idempotency, pending state, and compatibility contracts.
- **Platform Engineering:** supplies measurable deployment, isolation, capacity, policy, telemetry, and recovery capabilities.
- **Algorithm Engineering:** supplies distribution, quantile, approximation, optimization, and adversarial-analysis foundations.
- **Software Design and Decision-Making:** owns alternatives, uncertainty, values, reversibility, and decision records informed by scenario evidence.

## References

1. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
2. ISO/IEC, *Systems and Software Engineering — Systems and Software Quality Models*, ISO/IEC 25010:2023, November 2023. <https://www.iso.org/standard/78176.html>
3. Mario Barbacci, Mark Klein, Thomas Longstaff, and Charles Weinstock, *Quality Attributes*, CMU/SEI-95-TR-021, 1995. <https://doi.org/10.21236/ADA307888>
4. W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*, W3C Recommendation, 12 December 2024; retrieved 2026-09-06. <https://www.w3.org/TR/WCAG22/>
5. Robert Barbacci et al., *Quality Attribute Workshops (QAWs), Third Edition*, CMU/SEI-2003-TR-016, August 2003. <https://doi.org/10.21236/ADA418428>
6. Paul Clements, Rick Kazman, and Mark Klein, *Evaluating Software Architectures: Methods and Case Studies*, Addison-Wesley, 2002.
7. ISO/IEC/IEEE, *Systems and Software Engineering — Architecture Description*, ISO/IEC/IEEE 42010:2022, November 2022. <https://standards.ieee.org/ieee/42010/6846/>
8. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.
9. Raj Jain, *The Art of Computer Systems Performance Analysis*, Wiley, 1991.
10. Donald T. Campbell, “Assessing the Impact of Planned Social Change,” *Evaluation and Program Planning* 2(1), 1979. <https://doi.org/10.1016/0149-7189(79)90048-X>

## Exercises

### Exercise 1

Define quality attribute, quality model, quality-attribute scenario, general scenario, concrete scenario, source, stimulus, environment, artifact, response, response measure, oracle, guardrail, proxy, survivor bias, measurement validity, and evidence expiry.

### Exercise 2

Rewrite “the API must be fast and reliable” as two complete six-part scenarios for normal peak traffic and dependency degradation. Include client-visible boundaries, distributions, errors, timeouts, correctness, workload, and recovery measures.

### Exercise 3

Diagnose a dashboard that reports server-side average latency only for successful requests, uptime from process heartbeats, modifiability by lines changed, security by blocked-login count, and usability by all-user median. Design valid scenario families and oracles.

### Exercise 4

Compare averages, percentiles, maximum or deadline-miss bounds, error rates, qualitative task evidence, conformance criteria, and scenario-based judgments. Allocate them to performance, availability, security, modifiability, accessibility, and operability without combining them into one score.

### Exercise 5

Design a quality-attribute scenario portfolio for an international disaster-relief logistics platform with donors, warehouses, intermittent field teams, customs, vulnerable recipients, multiple languages, payments, perishable supplies, personal data, fraud, and rapidly changing routes. Cover all six parts, quality families, lifecycle, adversaries, minority harm, measurement, guardrails, evidence, prioritization, and omissions.

## Answers to the Exercises

### Answer 1

A **quality attribute** expresses how well a system behaves or changes in context; a **quality model** organizes such properties. A **quality-attribute scenario** contains source, stimulus, environment, artifact, response, and response measure. A **general scenario** is reusable across systems; a **concrete scenario** binds actors, conditions, paths, and thresholds. The **source** causes a **stimulus** in an **environment**; the **artifact** is affected; the **response** is observable behavior; the **response measure** decides its bounds. An **oracle** judges evidence. A **guardrail** constrains harmful optimization. A **proxy** indirectly represents an outcome. **Survivor bias** measures only cases reaching a selected endpoint. **Measurement validity** concerns whether evidence supports its interpretation. **Evidence expiry** names material changes that invalidate unreviewed transfer.

### Answer 2

Performance scenario: source, authenticated mobile customer; stimulus, submits an order query; environment, 6,000 requests/s with declared mix, 30 million orders, warm/cold-cache proportions, all dependencies healthy; artifact, client-to-order read path; response, returns a permission-correct page or explicit admission rejection; measures, client-observed p95 under 400 ms and p99 under 900 ms over five minutes, timeout counted at two seconds, correct-success rate at least 99.8%, stale age under 30 seconds, and cohort results reported.

Degradation scenario: source, database dependency; stimulus, latency rises to two seconds for 15 minutes; environment, same admitted load with one application zone absent and queues initially empty; artifact, gateway, service pools, cache, database path, and status API; response, bounded admission and explicitly age-labeled read fallback preserve unrelated operations, unknown outcomes remain queryable, and recovery drains without retry storm; measures, at least 98% of admitted safe reads under one second, zero unauthorized or falsely current results, pool and queue bounds, overload response under 200 ms, normal contract restored within ten minutes of dependency recovery, and all unknown writes reconciled within 30 minutes.

### Answer 3

The latency population has survivor bias, wrong boundary, and no distribution; use client intents, errors and timeouts, workload, cohorts, p50/p95/p99 and deadline misses plus correctness. Heartbeats measure process liveness, not useful availability; add operation-level correct outcomes, freshness, degraded scope, impact time, data loss, and reconciliation. Lines changed omit coordination, compatibility, migration, deployment, validation, learning, and rollback; create representative change scenarios across those artifacts.

Blocked logins measure one control activity, not security outcomes; add scenarios for unauthorized access, revocation, data export, malicious input, detection, containment, recovery, audit, and evidence gaps under adversary capabilities. An all-user median can erase accessibility and severe-task failure; name user cohorts, assistive technology, tasks, context, success, errors, recovery, time distributions, and applicable conformance checks. Use independent oracles and report missing data, architecture/version, sample, exclusions, and limitations.

### Answer 4

Averages help capacity and total-work reasoning but hide tails. Percentiles describe a population distribution boundary but require quantile convention, cohort, errors, and timeout rules. Maximum or deadline-miss counts suit hard or consequential timing when measurement resolution and observation coverage are credible. Error rates need semantic outcome classes, not status codes alone. Performance and availability usually combine distributions, deadline misses, correct-success rates, resource bounds, and recovery outcomes.

Security uses scenario judgments plus counts or times for authorization, revocation, detection, containment, recovery, and audit under a threat model; zero observed attacks is not proof. Modifiability uses representative changes, affected responsibilities, lead and migration time, compatibility, rollout, repair, and evidence quality. Accessibility combines applicable conformance criteria with representative user/task evidence, errors, completion, recovery, and distributions. Operability combines signal validity, diagnosis and action tasks, control outcomes, time, access, and recovery. Preserve a response vector and mandatory gates; arbitrary normalization into one score destroys units, assumptions, and stakeholder consequences.

### Answer 5

Drivers include timely equitable delivery, safety of perishable goods, offline field continuity, customs compliance, donor accountability, recipient privacy and accessibility, fraud containment, payment integrity, route adaptability, multilingual operation, cost, and recovery. Sources include recipient, field worker, warehouse sensor, donor, customs officer, payment provider, attacker, weather event, border closure, and policy owner. Stimuli cover demand surge, route loss, cold-chain excursion, duplicate identity, credential revocation, payment ambiguity, data correction/deletion, translation change, warehouse outage, schema rollout, and compromised device.

Each scenario names normal, peak, disconnected, degraded, recovery, migration, or compromised environment; affected mobile, inventory, routing, identity, payment, customs, notification, data, and audit artifacts; observable accept/reject/allocate/reroute/isolate/reconcile behavior; and measures with start/end, units, population, distribution, threshold, window, missing-data rule, and evidence. Guardrails prevent fast allocation from double-spending inventory, cheap routing from violating safety, availability from exposing recipient data, fraud controls from excluding legitimate recipients, and aggregate success from hiding language, disability, island, or low-connectivity cohorts.

The portfolio includes nominal donation-to-delivery, peak surge, offline allocated inventory rights, cold-chain alarm, customs delay, duplicate and fraudulent claims, payment timeout, revoked field device, regional warehouse loss, route replanning, multilingual and accessible recipient task, mixed-version rollout, privacy deletion and backup restore, and full reconciliation. Trace each to drivers, architecture views, decisions, owners, tests, field evidence, and expiry. Prioritize by consequence, urgency, obligation, uncertainty, irreversibility, affected cohort, and pending decisions—not votes alone. Report omitted disasters, countries, populations, suppliers, attacks, physical tests, and regulatory interpretations; route safety, humanitarian legitimacy, accessibility, privacy, customs, financial, and security acceptance to competent authorities.
