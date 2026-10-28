---
module_id: DARCH-007
program: Data Architecture Engineering
level: 1
module_number: 7
title: Architecture Drivers and Constraints
status: complete
last_verified: 2026-09-03
---

# Architecture Drivers and Constraints

## One-Page Review

### Governing question

How can data architects identify the small set of forces that should shape architecture, distinguish them from fixed constraints and uncertain assumptions, and turn them into testable scenarios and traceable trade-offs?

### Essential definitions

- An **architecture driver** is a stakeholder outcome, functional demand, quality requirement, risk, or change with enough consequence and design influence to shape architecture.
- A **constraint** is a condition the architecture must satisfy or operate within, regardless of whether it is desirable.
- An **assumption** is an unverified proposition temporarily treated as true for reasoning and therefore carrying an owner, confidence, consequence, and test.
- A **design decision** is a chosen response to drivers and constraints; it must not be mislabeled as an external constraint.
- A **quality-attribute scenario** makes a quality need concrete through source, stimulus, environment, artifact, response, and response measure.
- A **sensitivity point** is a property whose change materially affects a quality response; a **trade-off point** affects multiple qualities in competing ways.
- A **bound** is a measurable limit, range, or condition; a **preference** ranks feasible alternatives but does not make them mandatory.

### Central model, mechanism, or theorem

Model the decision context as:

`K = (D, C, A, U, E)`

where `D` is prioritized drivers, `C` is non-negotiable and negotiable constraints, `A` is testable assumptions, `U` is uncertainty, and `E` is evidence. Feasible options satisfy applicable hard constraints. Options are then evaluated against concrete scenarios, risks, costs, reversibility, and preferences. A candidate architecture is justified only through traceability from stakeholder concern to scenario, decision, predicted response, evidence, and review trigger.

### Critical invariants

- Every driver names stakeholder, outcome or obligation, scope, priority, time horizon, and acceptance evidence.
- Every constraint records source authority, exact bound, scope, effective period, and whether negotiation or exception is possible.
- Every assumption has an owner, confidence, consequence if false, validation plan, and expiry or review trigger.
- Chosen technologies and organizational habits are not called constraints unless an authorized source actually fixes them.
- Quality words become scenarios with measurable responses rather than unattached adjectives.
- Mandatory constraints are filtered before preferences are scored.
- Trade-offs retain dissent, distribution of benefits and harms, uncertainty, and change triggers.

### Common failures

Common failures are treating every requirement as a driver, using “scalable” or “secure” without scenarios, accepting budgets or deadlines with no source, calling a preferred cloud or database a constraint, hiding assumptions as facts, averaging away legal or safety limits, prioritizing only executive voices, optimizing nominal load while ignoring change and failure, and recording a decision without the driver it answers.

### Compact example

A team requests “real-time global customer analytics on the existing warehouse.” Investigation separates a driver—fraud reviewers need a risk view within 30 seconds for high-value transfers—from constraints—regional data-use restrictions and a six-month contract exit—from assumptions—peak event volume and identity-match accuracy—and from a chosen implementation—the warehouse. Several architectures can now be tested rather than treating the requested product as destiny.

### Connections

[DARCH-006](006-data-principles-and-decision-rules.md) turns recurring forces into governed defaults. [DARCH-008](../ROADMAP.md) deepens risk and criticality analysis. [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) develops scenario and trade-off methods, while [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies stakeholder, requirement, constraint, uncertainty, and lifecycle reasoning.

## Governing Question

Architecture is shaped by many requests, but only some are architecturally significant. A field name, one report, or a local code preference may be handled within existing structures. A new jurisdiction, tenfold data rate, irreversible retention duty, strict recovery target, or cross-domain identity decision can change fundamental boundaries and mechanisms.

The challenge is not collecting the longest requirement list. It is finding the consequential forces, establishing their authority and evidence, exposing conflicts and uncertainty, and turning vague quality language into scenarios against which alternatives can be evaluated. The process must also distinguish what the world imposes from what designers have chosen.

Drivers and constraints evolve. A regulation takes effect, an acquisition changes data ownership, volume evidence contradicts a forecast, a vendor reaches end of support, or a strategic outcome loses priority. Architecture must retain traceability and triggers so the design can be reconsidered without reconstructing its original reasoning.

## Why This Matters

Unclear drivers produce cargo-cult architecture. Teams adopt streaming because “real time” was mentioned, centralize data because “one truth” sounds desirable, or distribute authority because autonomy is fashionable. The resulting system may solve no important stakeholder problem while creating permanent cost and risk.

Unclear constraints produce false impossibility. “We must use the current warehouse” may mean a contract has two years remaining, a team lacks skills, an executive expressed a preference, or a policy actually mandates a controlled service. These conditions require different responses: comply, negotiate, train, migrate, document preference, or seek exception.

Hidden assumptions defer risk. Forecast volume, source quality, consumer adoption, legal interpretation, vendor portability, and recovery time are often treated as facts until late testing. Making assumptions first-class enables prototypes, measurements, legal review, contract tests, and reversible commitments.

Good driver analysis concentrates effort. High-priority scenarios determine which prototypes, capacity tests, failure exercises, privacy reviews, and migration rehearsals deserve investment. Traceability lets reviewers ask whether a design choice still earns its complexity.

## Prerequisites and Retrieval

You should understand stakeholders, concerns, requirements, quality attributes, risks, architecture decisions, data flows, contracts, and basic measurement. Recall that principles and policies carry different force and that consumer fitness is use-relative.

Retrieve source, stimulus, environment, artifact, response, response measure, baseline, threshold, uncertainty, risk, sensitivity, trade-off, constraint, assumption, option, and evidence. Familiarity with architecture decision records and scenario-based evaluation is useful.

## Learning Objectives

After completing this module, you should be able to:

- distinguish drivers, constraints, assumptions, preferences, and design decisions;
- identify architectural significance by consequence, reach, difficulty of change, and cross-boundary effect;
- trace each force to stakeholders, authority, scope, horizon, and evidence;
- write data-specific quality-attribute scenarios with measurable responses;
- classify constraints by source, hardness, negotiability, and effective period;
- maintain an assumption register with confidence, consequence, validation, and expiry;
- identify conflicts, sensitivity points, and trade-off points;
- compare feasible alternatives without compensating away mandatory limits;
- prioritize evidence and reversible experiments under uncertainty;
- define decision and architecture review triggers.

## Core Exposition

Begin with stakeholder outcomes and obligations. Drivers can arise from mission, customer service, public value, regulation, contract, security, privacy, safety, resilience, interoperability, cost, sustainability, time to market, merger, vendor exit, and technology end of support. A driver is important because of its consequence and design influence, not because a senior person used emphatic language.

Functional demands can drive architecture when their scale, distribution, authority, or lifecycle is consequential. “Produce a report” may be local. “Produce a legally attested consolidated report across 40 entities from a clean monthly cut, with corrections preserved for seven years” shapes semantics, provenance, close, identity, preservation, and governance.

Quality requirements often dominate structural choices. Relevant data qualities include semantic correctness, completeness, consistency, timeliness, provenance, traceability, confidentiality, integrity, availability, recoverability, interoperability, modifiability, portability, observability, usability, and cost efficiency. Names alone are not requirements.

ISO/IEC [25010:2023](https://www.iso.org/standard/78176.html) provides a product quality model of characteristics and subcharacteristics for specification and evaluation. It is a reference taxonomy, not a ready-made priority list or set of measures for a particular data product. Context and stakeholder consequences determine what matters.

A quality-attribute scenario makes a desired response testable. Specify:

- **source**: actor, system, event, or condition causing a stimulus;
- **stimulus**: the event, load, fault, request, or change;
- **environment**: normal, peak, degraded, attack, migration, recovery, or another state;
- **artifact**: the affected product, flow, store, contract, process, or organization;
- **response**: what the system and people do;
- **response measure**: observable bound and evidence.

“Data must be fresh” becomes: “When an accepted inventory adjustment occurs during peak sale traffic, the checkout availability projection for 99.9% of covered item-locations reflects the event within 20 seconds, identifies its source position, and fails closed for reservations after 60 seconds of staleness.” This still needs baseline, consequence, scope, and verification method.

Response measures require semantic care. Percentages need denominators; latency needs start and end events; availability needs eligible time and excluded periods; correctness needs an authority or reference; cost needs allocation; recovery needs a consumer boundary. An exact number without measurement semantics is fake precision.

The SEI [Quality Attribute Workshop](https://www.sei.cmu.edu/library/quality-attribute-workshops-qaws-third-edition/) engages diverse stakeholders early to identify and refine quality scenarios. The [ATAM collection](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) describes evaluating architectural approaches against quality goals to expose risks, sensitivity points, and trade-offs. These methods inform the chapter; claiming an official ATAM evaluation requires its actual process and qualified participants.

Stakeholder diversity matters. Producers see feasibility and source behavior. Consumers see decision fitness. Operators see failure and recovery. Security, privacy, legal, records, safety, accessibility, finance, and procurement see constraints and harms. People affected by the system may reveal burdens absent from sponsor priorities. Voting does not erase authority or rights.

A **constraint** restricts the solution space. External constraints include law, regulation, contract, standards, physical limits, sovereignty, external interfaces, and deadlines imposed by events. Internal constraints include approved policies, budget authorization, skills, operating model, existing commitments, and transition capacity. Some are hard; others can be negotiated, funded, changed, or excepted.

Record each constraint's source, owner, authority, exact statement, rationale, scope, effective and expiry dates, affected decisions, evidence, interpretation, negotiability, exception path, and review triggers. Paraphrase carefully and retain the source. Architects should not offer legal interpretation as legal authority.

A hard constraint is non-negotiable within the current decision authority. That does not mean universal or eternal. A regulator may change a rule; a board may change policy; a customer may renegotiate a contract. State who has authority to change it and the lead time.

Budget and schedule are usually bounded resources, but their exact status needs validation. Is the date tied to a statutory event, contract, seasonal launch, sunk promise, or preference? What happens if it moves? Which scope, risk, or quality can change? A triangle slogan is not stakeholder analysis.

Legacy systems can constrain transition without constraining the target forever. A source may expose only nightly files, a mainframe may remain for three years, or an identifier cannot change until partner contracts migrate. Model the transition condition, compatibility, and exit rather than embedding the legacy product into an enduring principle.

A **design decision** is not an external constraint merely because it was made earlier. “Use Kafka,” “centralize in the lake,” or “one cloud only” may be decisions supported by standards, investments, or skills. Trace them to their governing source. If the source is weak or expired, reopen the decision rather than laundering it as inevitability.

A **preference** helps compare feasible options. Familiar tools, reduced vendor count, reuse, lower operational surface, reversibility, or team autonomy may be legitimate preferences. They do not override hard policy. Record whose preference it is and how much cost or risk it may justify.

An **assumption** fills an evidence gap. Examples include peak throughput, event ordering, source completeness, user adoption, partner compatibility, legal interpretation pending review, model accuracy, network latency, cloud availability, and staffing. Every assumption should be falsifiable enough to test or explicitly acknowledged as judgment.

An assumption register includes identifier, statement, owner, source, confidence basis, scope, affected decisions, consequence if false, validation method, deadline, current evidence, status, and triggers. Prioritize assumptions with high consequence, low confidence, and irreversible dependent decisions.

Unknowns differ from assumptions. “We do not know the source's deletion behavior” is an unknown. “The source deletes within 24 hours” is an assumption only if the architecture temporarily relies on it. Do not convert ignorance to optimism merely to complete a template.

Dependencies connect assumptions. If adoption drives volume and volume drives partitioning, evidence about adoption changes the infrastructure decision. Build an assumption-to-decision graph so invalidation reveals blast radius. Avoid one giant risk score that hides causal structure.

Drivers conflict. Freshness may increase cost and partial-data risk. Centralization may improve comparability while reducing autonomy and increasing concentration. Detailed lineage may improve traceability while increasing sensitive metadata and expense. Retention may support audit while increasing privacy and breach exposure.

A **sensitivity point** is where a small change in a parameter or decision materially changes a response. Partition count may sharply affect throughput; replication lag may cross a fraud-decision bound; canonical-model scope may change coordination lead time. Sensitivities deserve measurement and monitoring.

A **trade-off point** affects several qualities. Replication may improve read availability and performance while increasing staleness, cost, and deletion complexity. Encryption can affect confidentiality, latency, key recovery, and operability. Trade-off analysis records direction, evidence, uncertainty, and stakeholders rather than declaring one quality “better.”

Prioritization should combine consequence, urgency, reach, architectural influence, difficulty of later change, uncertainty, and stakeholder authority. Keep mandatory obligations outside popularity voting. A low-frequency safety or statutory scenario can outrank a high-frequency convenience scenario.

Use a portfolio of scenarios. Include normal operations, peak load, failure, recovery, attack, correction, deletion, policy change, schema evolution, merger, vendor exit, staff turnover, and unexpected consumer growth. Nominal scenarios alone reward brittle designs.

Compare multiple options, including no change, process change, minimal data change, and larger architecture change. First remove options that violate hard constraints. Then assess scenario responses, risks, cost, time, reversibility, concentration, operational fit, transition, and exit.

Weighted scoring can organize preferences, but weights and ordinal ratings are uncertain. Show raw judgments and sensitivity. If a small weight change reverses the ranking, the decision is not robust. Do not combine incomparable harm into a comforting total.

Evidence should precede irreversible commitment. Measure current workload, sample data quality, prototype a critical transformation, test partner interfaces, benchmark under representative skew, rehearse recovery, perform threat or privacy analysis, and validate consumer use. Target the assumptions and sensitivity points most capable of changing the decision.

Prototypes have limits. A synthetic benchmark may omit skew, concurrency, governance, or operator behavior. A pilot may select cooperative users. A legal memo may depend on facts that change. State what evidence covers and retain residual uncertainty.

Architecture decisions should record drivers and constraints by stable identifier, alternatives, chosen response, predicted scenario outcomes, evidence, assumptions, risks, dissent, transition, and review triggers. A decision with no trace becomes folklore; a driver with no responding decision becomes unmet intent.

Review triggers include a breached response measure, invalidated assumption, new constraint, changed priority, repeated incident, material scale or distribution change, vendor or skill change, exception, merger, new consumer, or cheaper reversible option. Monitor the context, not only system health.

Constraints themselves can conflict. Residency law, global recovery, preservation, deletion, accessibility, and security may pull in different directions. Route interpretation to authorized experts and redesign scope or operating model. Architecture cannot solve authority conflict through technical cleverness alone.

Distributional effects belong in driver analysis. Faster decisions for average users may worsen outcomes for low-connectivity regions. Central quality thresholds may exclude small populations. Cost savings for producers may shift manual reconciliation to consumers. Record affected groups, counter-metrics, and dissent.

Economics should include total lifecycle cost and option value: acquisition, migration, integration, operation, data movement, controls, incident, recovery, change, decommission, and exit. A cheaper initial design may create expensive irreversibility. Avoid monetary precision where evidence is weak.

The output is a **driver package**, not a requirements dump: stakeholder map, prioritized driver statements, scenario set, constraint register, assumption register, conflicts, options, evidence plan, decisions, and review triggers. It should be compact enough to guide work and rich enough to audit.

## Definitions and Notation

Let `D` be drivers, `C_h` hard constraints, `C_n` negotiable constraints, `A` assumptions, `U` uncertainty records, and `E` evidence. For option `o`, feasibility at time `t` is:

`Feasible(o,t) = all(c(o,t) = satisfied for c in C_h)`

unless an applicable constraint explicitly permits a valid exception. Preferences compare only feasible options.

A quality scenario is `q = (source, stimulus, environment, artifact, response, measure)`. Let `R(o,q)` be the predicted or observed response of option `o` under scenario `q`, with evidence and uncertainty. Satisfaction requires comparing `R(o,q)` to a semantically defined bound, not merely attaching a green label.

An assumption `a` has `(statement, owner, confidence_basis, consequence, test, due, status)`. Define exposure qualitatively or quantitatively from consequence and uncertainty, but preserve both inputs. A risk number must not obscure why the assumption matters or which decision depends on it.

A decision trace is `stakeholder concern -> driver or constraint -> scenario -> option response -> decision -> evidence -> trigger`. Every arrow is a claim subject to review.

## Mechanisms, Invariants, or Proof Structure

Use nine gates to derive architectural drivers and constraints.

**1. Boundary gate.** Define system of interest, environment, lifecycle, organizations, jurisdictions, horizon, and decisions to inform.

**2. Stakeholder gate.** Identify authorities, operators, producers, consumers, affected people, and assurance roles; record their concerns and conflicts.

**3. Driver gate.** Derive functional, quality, risk, change, and outcome forces. Select the few with material consequence and design influence.

**4. Scenario gate.** Refine quality words into source, stimulus, environment, artifact, response, and measurable bound with baseline.

**5. Constraint gate.** Record exact source, authority, scope, time, hardness, negotiability, exception, and evidence. Separate prior decisions and preferences.

**6. Assumption gate.** Expose unknowns and assumptions, link them to decisions, rank consequence and uncertainty, and assign tests and deadlines.

**7. Option gate.** Generate real alternatives, filter hard constraints, evaluate scenarios, identify sensitivities and trade-offs, and retain dissent.

**8. Evidence gate.** Run measurements, prototypes, analyses, and rehearsals against decision-changing uncertainty. Record coverage and limitations.

**9. Decision gate.** Choose through named authority, preserve trace and transition, instrument response measures, and establish review triggers.

The executable example checks a compact context register. It flags a driver without measurable evidence, a supposed constraint with no authority, a hidden design decision mislabeled as a constraint, and an assumption with no test.

<!-- bijux-verify: {"id":"driver-context-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"items=5\nvalid=1\nfindings=cloud-choice:design-labeled-constraint,global-scale:missing-test,quality-need:missing-measure,warehouse-only:missing-authority\nready=false\n","stderr":""}} -->
```python
items = (
    {"id": "fraud-latency", "kind": "driver", "measure": "p99 <= 30s", "authority": "risk-owner", "test": "load-rehearsal"},
    {"id": "quality-need", "kind": "driver", "measure": "", "authority": "finance-owner", "test": "reconciliation"},
    {"id": "warehouse-only", "kind": "constraint", "measure": "", "authority": "", "test": "contract-review"},
    {"id": "cloud-choice", "kind": "constraint", "measure": "", "authority": "architecture-team", "test": "", "origin": "design"},
    {"id": "global-scale", "kind": "assumption", "measure": "50k events/s", "authority": "product-owner", "test": ""},
)

findings = []
valid = 0
for item in items:
    local = []
    if item["kind"] == "driver" and not item["measure"]:
        local.append("missing-measure")
    if item["kind"] == "constraint" and not item["authority"]:
        local.append("missing-authority")
    if item["kind"] == "constraint" and item.get("origin") == "design":
        local.append("design-labeled-constraint")
    if item["kind"] == "assumption" and not item["test"]:
        local.append("missing-test")
    if local:
        findings.extend(f"{item['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"items={len(items)}")
print(f"valid={valid}")
print(f"findings={','.join(sorted(findings))}")
print(f"ready={str(not findings).lower()}")
```

The fixture verifies only these registry predicates. It does not prove that a 30-second target is appropriate, that the named owner has authority, that a load rehearsal is representative, or that any option satisfies the driver. Substantive validation requires stakeholder, domain, policy, operational, and empirical evidence.

## Alternatives and Trade-Offs

**Interview versus observation.** Interviews expose intent and tacit concerns; runtime and workflow observation expose actual behavior. Use both and preserve disagreement.

**Taxonomy versus scenarios.** A quality taxonomy improves coverage and vocabulary. Scenarios create contextual measures. Taxonomies prompt; scenarios test.

**Executive prioritization versus broad stakeholder elicitation.** Executives own strategy and funding. Broader stakeholders reveal operations, harms, and hidden dependencies. Authority and participation must both be explicit.

**Hard bounds versus target ranges.** Hard bounds clarify acceptance where authority supports them. Ranges express uncertainty and trade space. False exactness is not rigor.

**Early commitment versus option preservation.** Commitment can accelerate coordination and learning. Reversible experiments protect against uncertain assumptions. Delay irreversible choices until evidence value falls below waiting cost.

**Quantitative scoring versus qualitative argument.** Scores aid comparison when measures are commensurable. Qualitative cases preserve context and noncompensable constraints. Use numbers as evidence, not authority.

**Central constraint register versus local context.** Central records improve consistency and discovery. Local ownership preserves interpretation. Federate sources with common identity, provenance, precedence, and escalation.

**Optimize dominant driver versus balance portfolio.** One driver can legitimately dominate a safety or legal case. Most designs serve several qualities. Document sacrificed outcomes and affected stakeholders rather than hiding them.

## Failure Modes and Misconceptions

1. **Every requirement is an architecture driver.** Only material, structurally influential forces deserve that status.
2. **A quality adjective is testable.** It needs scenario, response, measure, scope, and evidence.
3. **A constraint is permanent.** Authority, scope, effective interval, and change path bound it.
4. **An earlier decision is a constraint.** It remains a decision unless a valid authority now mandates it.
5. **An unknown can be omitted.** Hidden uncertainty becomes unmanaged risk.
6. **An assumption is a fact for planning.** It remains provisional and requires test and trigger.
7. **Stakeholder voting can override policy.** Participation prioritizes preferences, not non-waivable authority.
8. **One score resolves trade-offs.** Scores can hide hard constraints, uncertainty, and distributed harms.
9. **A prototype proves production fitness.** Coverage, scale, skew, failure, policy, and human behavior limit evidence.
10. **Nominal performance is enough.** Failure, recovery, change, correction, deletion, and exit also shape architecture.
11. **Architecture can resolve legal ambiguity.** Authorized interpretation is external evidence and may constrain options.
12. **A decision record is historical paperwork.** Its triggers and measures support active adaptation.

## Worked Examples

### Example 1

**Question:** Is “support analytics” an architecture driver?

**Reasoning:** Not yet. Name the consumer decision, consequence, population, history, freshness, quality, and acceptance evidence.

**Conclusion:** Functional nouns require outcome and scenario refinement.

### Example 2

**Question:** Is “use the existing cloud” a constraint?

**Reasoning:** Find its source: policy, contract, budget, skill, deadline, or preference. Record scope and change authority.

**Conclusion:** Do not launder a design preference into a constraint.

### Example 3

**Question:** How can “recoverable” become a scenario?

**Reasoning:** Name the failure, environment, affected product and consumers, restored boundary, RPO, RTO, reconciliation, and reopening authority.

**Conclusion:** Recovery quality is measured at the consumer boundary.

### Example 4

**Question:** Forecast volume has no evidence but drives irreversible partitioning.

**Reasoning:** Register the assumption, measure current behavior, model ranges, prototype skew, and favor reversible partition evolution.

**Conclusion:** High-consequence low-confidence assumptions deserve early evidence.

### Example 5

**Question:** A cheaper option violates a residency rule.

**Reasoning:** If the rule is an applicable hard constraint with no exception, remove the option before cost comparison.

**Conclusion:** Preferences do not compensate for mandatory constraints.

### Example 6

**Question:** Replication improves availability but complicates deletion.

**Reasoning:** This is a trade-off point. Quantify both scenarios, policy constraints, failure behavior, and affected stakeholders.

**Conclusion:** Record interacting qualities and evidence.

### Example 7

**Question:** An executive ranks dashboard speed first; operators rank correctness first.

**Reasoning:** Refine the decisions and consequences, establish authority, measure current state, and expose whether distinct products are needed.

**Conclusion:** Priority conflict is resolved through context, not volume of votes.

### Example 8

**Question:** A pilot succeeds with cooperative users.

**Reasoning:** Record selection, scale, workflow, data, and duration limits; test representative and adversarial conditions before expansion.

**Conclusion:** Evidence scope bounds the inference.

### Example 9

**Question:** When should a constraint trigger redesign?

**Reasoning:** When authority, scope, effective period, interpretation, or measured feasibility changes materially.

**Conclusion:** Monitor context as well as components.

### Example 10

**Question:** What makes a driver package complete enough?

**Reasoning:** Consequential stakeholders and scenarios are covered, hard constraints sourced, major assumptions testable, alternatives real, and decisions traceable with triggers.

**Conclusion:** Completeness is decision fitness, not item count.

## Cross-Program Connections

[Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) develops architecture drivers, quality attributes, scenarios, decisions, sensitivities, trade-offs, and evaluation methods. Data architecture adds persistent meaning, provenance, sharing, policy, history, and correction concerns.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes stakeholder needs, requirements, constraints, interfaces, verification, validation, configuration, uncertainty, and lifecycle reasoning. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies threat, risk, policy, control, and assurance drivers.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) turns common drivers into paved capabilities and constraints into guardrails. [Cloud and Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) supplies capacity, resilience, sovereignty, cost, and provider-exit mechanisms.

## References

- IEEE, [*IEEE/ISO/IEC 42010-2022 — Architecture Description*](https://standards.ieee.org/ieee/42010/6846/), 2022. Official standard record for systems of interest, stakeholders, concerns, viewpoints, views, and architecture-description correspondence.
- ISO/IEC, [*ISO/IEC 25010:2023 — Product Quality Model*](https://www.iso.org/standard/78176.html), 2023. Authoritative quality-characteristic reference model for ICT and software products.
- ISO/IEC, [*ISO/IEC 25030:2019 — Quality Requirements Framework*](https://www.iso.org/standard/72116.html), 2019. Authoritative framework for eliciting, defining, analyzing, maintaining, verifying, and validating quality requirements.
- Software Engineering Institute, [*Quality Attribute Workshops, Third Edition*](https://www.sei.cmu.edu/library/quality-attribute-workshops-qaws-third-edition/), CMU/SEI-2003-TR-016, 2003. Primary method for early stakeholder elicitation and refinement of quality-attribute scenarios.
- Software Engineering Institute, [*Architecture Tradeoff Analysis Method Collection*](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/), checked 2026-09-03. Official collection describing scenario-based evaluation, risks, sensitivity points, and trade-off points.
- The Open Group, [*The TOGAF Standard, 10th Edition*](https://www.opengroup.org/togaf), 2022, site checked 2026-09-03. Official enterprise-architecture standard family covering business drivers, requirements, constraints, governance, and transitions.
- NIST, [*Cybersecurity Framework (CSF) 2.0*](https://doi.org/10.6028/NIST.CSWP.29), NIST CSWP 29, 2024. Outcome-oriented governance and risk source for cybersecurity-related drivers and constraints.
- NIST, [*Privacy Framework*](https://www.nist.gov/privacy-framework), checked 2026-09-03. Official voluntary framework for privacy outcomes, organizational profiles, ecosystem roles, and risk management.

## Exercises

### Exercise 1

Turn “the data platform must scale globally” into three distinct quality scenarios and identify the assumptions hidden in the original statement.

### Exercise 2

Classify “use Vendor X,” “data remains in Region A,” “launch by the tax-year boundary,” “prefer managed services,” and “peak volume is 50,000 events per second” as constraint, decision, preference, or assumption, including evidence needed.

### Exercise 3

Build a constraint and assumption register for consolidating customer data after an acquisition. Include authority, time, uncertainty, consequence, test, and trigger.

### Exercise 4

Compare centralized replication, federated query, and governed domain products for a cross-region risk view. Filter hard constraints, then identify sensitivity and trade-off points.

### Exercise 5

Design an evidence plan for a proposed streaming architecture whose decision depends on freshness, event order, identity matching, consumer adoption, recovery time, and cost.

## Answers to the Exercises

### Answer 1

Availability scenario: when one region fails during peak processing, authorized consumers in unaffected regions continue reading the last confirmed projection within a declared latency, while writes follow a fenced failover rule and recovery meets named RPO/RTO. Performance scenario: when 50,000 events per second arrive with representative key skew, the product publishes 99.9% within a measured end-to-end delay without violating cost and error bounds. Change scenario: when a new jurisdiction is added, the team deploys its policy, identity, storage, and serving configuration within a target lead time without modifying unrelated domains. Hidden assumptions include region count, volume and skew, network, consistency, sovereignty, workload mix, consumer distribution, provider services, skills, budget, and acceptable degradation.

### Answer 2

“Use Vendor X” is a design decision unless an authorized contract or standard makes it a current constraint; retain the source and expiry. “Data remains in Region A” may be a hard legal, contractual, or policy constraint, but needs exact data, operations, jurisdiction, authority, and interpretation. The tax-year date is an external schedule constraint if tied to an authoritative event; identify consequence and negotiable scope. “Prefer managed services” is a preference or architecture principle with rationale and exception, not a hard constraint. Peak volume is an assumption until measurement or committed demand evidence supports it; record range, skew, growth, test, and consequence.

### Answer 3

Constraints may include merger contract, legal-entity control, purpose limitation, residency, records holds, partner interfaces, transaction continuity, and an authorized transition budget and date. Each record names source authority, exact scope, effective interval, hardness, interpretation owner, evidence, and change path. Assumptions may include identity overlap, source quality, consumer inventory, transfer throughput, consent compatibility, staff availability, and decommission cost. Each names confidence basis, decisions that depend on it, consequence if false, test and due date. Trigger review on legal interpretation, source profiling, duplicate-rate evidence, consumer discovery, incident, delayed contract, failed rehearsal, or changed acquisition scope.

### Answer 4

First filter options against applicable residency, purpose, confidentiality, availability, and contractual constraints. Central replication simplifies cross-region queries and consistent transformations but increases movement, concentration, deletion scope, and sovereignty exposure. Federated query reduces persistent copies but couples latency, availability, policy, and semantic resolution across sources. Governed domain products preserve authority and reusable contracts but require coordination, identity, and product operations. Sensitivities include cross-region latency, permitted fields, number of domains, identity-match accuracy, query concurrency, and change lead time. Trade-offs include freshness versus cost, availability versus consistency, central comparability versus autonomy, and traceability versus sensitive metadata.

### Answer 5

Measure source-to-consumer latency components under representative volume, skew, late events, and backpressure. Test ordering requirements by key and verify duplicate, gap, and replay behavior. Profile identity matching with adjudicated samples, uncertainty, subgroup analysis, and correction. Pilot the consumer workflow with representative users and preserve adoption and outcome limits. Rehearse checkpoint loss, source outage, clean restore, replay, reconciliation, and reopen authority against RPO/RTO. Model and measure compute, storage, transfer, egress, operations, control, incident, and backfill cost. Link every experiment to an assumption and decision threshold; record environments, versions, source positions, limitations, dissent, and review triggers.
