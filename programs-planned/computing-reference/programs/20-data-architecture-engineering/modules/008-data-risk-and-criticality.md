---
module_id: DARCH-008
program: Data Architecture Engineering
level: 1
module_number: 8
title: Data Risk and Criticality
status: complete
last_verified: 2026-09-03
---

# Data Risk and Criticality

## One-Page Review

### Governing question

How can an organization identify which data and dependencies are consequential, describe uncertain harm without false precision, and allocate controls, recovery, and decision authority in proportion to context?

### Essential definitions

- **Risk** is the effect of uncertainty on objectives; a data-risk statement connects a cause or condition, event, consequence, affected parties, context, and evidence.
- **Criticality** is the degree to which loss, delay, corruption, misuse, or unavailability of data or a data capability would impair a named decision, service, obligation, or population over time.
- **Sensitivity** concerns harm from unauthorized disclosure or use; it is not synonymous with criticality.
- **Impact** is the consequence if an event occurs; **likelihood** represents uncertainty about occurrence under a declared horizon and conditions.
- **Inherent risk** is assessed before the controls under consideration; **residual risk** remains after controls, assumptions, and dependencies are accounted for.
- A **critical dependency** is a source, service, person, policy, key, model, interface, or facility whose failure can prevent an important outcome.
- **Risk acceptance** is an authorized decision to retain a described residual exposure for a bounded period, not an absence of remediation.

### Central model, mechanism, or theorem

Model a risk scenario as:

`r = (objective, asset_or_flow, cause, event, consequence, affected, horizon, likelihood, impact, controls, uncertainty, owner)`

Criticality is scenario- and time-dependent, not an intrinsic scalar attached to a table. Prioritize by explicit consequence dimensions, dependency paths, time to harm, substitutability, recoverability, and uncertainty. Mandatory legal, safety, rights, and policy constraints remain noncompensable. Only the named authority can accept residual risk.

### Critical invariants

- Every risk names the objective, event, consequence, affected parties, time horizon, owner, evidence, and uncertainty.
- Confidentiality, integrity, availability, authenticity, provenance, privacy, safety, financial, operational, legal, and societal impacts remain distinguishable.
- Criticality follows dependencies and consumer decisions, including low-frequency and derived products.
- Unknown exposure, missing lineage, and untested recovery increase uncertainty; they do not justify a low rating.
- Control presence is separated from control operation, effectiveness, coverage, and residual outcome.
- Recovery priority is based on business or mission consequences and consistent recovery sets, not database size or executive visibility.
- Risk acceptance, exception, transfer, and treatment identify authority, expiry, evidence, and review triggers.

### Common failures

Common failures include equating sensitive with critical, ranking by data volume or query count, using red/amber/green without definitions, multiplying arbitrary ordinal scores, assigning low likelihood to unobserved events, assessing assets without consumers or dependencies, assuming backups prove recoverability, double-counting controls, ignoring correlated failures, transferring contracts but not consequences, and letting teams accept risks beyond their authority.

### Compact example

A 20-row exchange-rate table contains no personal data and receives few queries, yet a wrong rate can corrupt every daily settlement. A customer-behavior lake is highly sensitive but may tolerate a day of unavailability. Their confidentiality, integrity, availability, temporal, recovery, and decision consequences differ. One “tier 1” label cannot specify the controls each needs.

### Connections

[DARCH-007](007-architecture-drivers-and-constraints.md) supplies scenarios, constraints, assumptions, and evidence. [DARCH-009](../ROADMAP.md) presents risk through stakeholder-specific views. [Security Engineering](../../25-security-engineering/ROADMAP.md) develops threats and controls; [Systems Engineering](../../26-systems-engineering/ROADMAP.md) develops hazard, criticality, assurance, and lifecycle reasoning.

## Governing Question

Every dataset can be called valuable, and every failure can be called risky. Neither statement allocates architecture effort. Teams need to know what can go wrong, whose outcome changes, how quickly harm emerges, which dependencies concentrate exposure, what evidence supports the assessment, and who may decide what remains.

Data introduces distinctive risks. It is copied and combined, persists after applications change, carries meaning outside its source, and can influence decisions far from collection. Corruption can propagate silently. Disclosure can be irreversible. Deletion can destroy evidence or violate preservation. An analytical model can amplify biased observations. A tiny reference table can control an enormous financial flow.

Criticality is therefore relational. Data is critical to a decision, service, obligation, or affected population under a scenario and time horizon. The same product can be critical for integrity during settlement, critical for confidentiality during investigation, and tolerant of delayed availability for historical research.

## Why This Matters

Uniform protection wastes resources and leaves real hazards hidden. If every asset receives the highest tier, teams cannot prioritize recovery and exceptions proliferate. If classification is based only on confidentiality, public but safety-critical or integrity-critical data is underprotected. If popularity drives priority, dormant legal records and annual regulatory products disappear from plans.

Risk analysis connects architecture to consequence. It informs isolation, redundancy, validation, access, minimization, provenance, quality, incident response, recovery objectives, supplier oversight, human review, and investment. It also shows when an apparently local product is a shared dependency with enterprise blast radius.

The analysis must remain honest about uncertainty. Threat frequencies may be sparse, impact estimates contested, lineage incomplete, and control effectiveness untested. Precision is useful when evidence supports it; otherwise ranges, scenarios, confidence, and sensitivity are more responsible than decimal scores.

Risk is not eliminated by documentation. The outcome is a decision: avoid the activity, reduce likelihood or impact, share or transfer defined obligations, prepare contingency, accept residual exposure, or stop. Each decision needs authority and monitoring.

## Prerequisites and Retrieval

You should understand objectives, stakeholders, data flows, classifications, quality, controls, incidents, dependencies, recovery, and decision authority. Recall the distinction among hard constraints, preferences, assumptions, and evidence.

Retrieve confidentiality, integrity, availability, authenticity, provenance, hazard, threat, vulnerability, likelihood, impact, exposure, inherent risk, residual risk, risk tolerance, risk appetite, RPO, RTO, maximum tolerable downtime, single point of failure, and correlated failure. Risk terminology varies by framework; define the local model.

## Learning Objectives

After completing this module, you should be able to:

- distinguish sensitivity, classification, value, quality, and criticality;
- write data-risk scenarios with causes, events, consequences, affected parties, horizons, and evidence;
- assess multiple impact dimensions without collapsing them prematurely;
- analyze dependency, concentration, propagation, and time-to-harm;
- express likelihood and uncertainty with appropriate evidence and ranges;
- distinguish inherent, current, residual, and target risk;
- connect treatments and controls to specific scenario causes or consequences;
- derive recovery priorities and objectives from consumer impact;
- identify the authority required to accept residual risk;
- maintain risk and criticality as data uses, threats, controls, and dependencies change.

## Core Exposition

Start with objectives and affected parties. Objectives may concern safe service, correct payment, privacy, lawful processing, scientific validity, public trust, revenue, operational continuity, contractual performance, or strategic learning. A risk has meaning only relative to what uncertainty can change.

A useful risk statement is: “Because of `cause or condition`, `event` may occur under `context`, leading to `consequence` for `affected parties` within `horizon`, supported by `evidence and uncertainty`.” Avoid noun-only risks such as “data quality” or “cybersecurity.” They do not reveal the scenario or treatment.

Distinguish a **threat source** from an event and vulnerability. A malicious actor, accident, component fault, process weakness, environmental event, or incentive can be a source or condition. Unauthorized export, incorrect join, delayed update, lost key, model misuse, or deletion failure is an event. Weak access, ambiguous identity, missing validation, or concentrated dependency can increase susceptibility.

NIST [SP 800-30 Rev. 1](https://csrc.nist.gov/pubs/sp/800/30/r1/final) provides a security-risk assessment process covering preparation, conduct, and maintenance, with threat, vulnerability, likelihood, impact, and uncertainty concepts. Its federal information-security context is useful but not a complete model for every business, privacy, safety, ethical, or data-quality risk.

Impact is multidimensional. **Confidentiality** loss exposes data or inferred information to unauthorized actors. **Integrity** loss changes facts, order, identity, calculation, or provenance. **Availability** loss prevents timely access or processing. **Authenticity** loss obscures who or what produced an assertion. **Privacy** harm can arise from authorized processing, surveillance, loss of autonomy, exclusion, or chilling effects—not only breach.

Other consequences include unsafe action, denied service, financial loss, regulatory breach, contract failure, reputational damage, environmental harm, scientific invalidity, discrimination, operational workload, strategic error, and loss of evidence. Record who bears each consequence. Benefit to one stakeholder does not offset an unacknowledged harm to another.

FIPS [199](https://csrc.nist.gov/pubs/fips/199/final) categorizes United States federal information and systems by potential impact from loss of confidentiality, integrity, and availability. Its low, moderate, and high structure is authoritative in its scope, not a universal enterprise taxonomy. A private organization can learn from the dimension separation without claiming FIPS compliance.

**Sensitivity** usually drives disclosure and use controls. **Criticality** concerns dependence of an outcome on trustworthy, timely capability. Public routing data may be availability- and integrity-critical. A confidential archive may be sensitivity-high but tolerate hours of outage. **Value** can include economic, public, evidentiary, or option value; it does not alone determine harm.

Classification labels should link to definitions, authority, effective time, policy, and handling rules. Avoid aggregating several dimensions into `critical` before their implications are derived. A compact tier may be useful for operations, but retain the underlying scenario profile.

Criticality analysis begins at the consumer decision. Ask what happens if the data is absent, late, incomplete, duplicated, wrong, unauthorized, unrecoverable, or used outside purpose. Identify time to material harm, detection, workaround, backlog growth, correction, and recovery. Consequence may rise nonlinearly over time.

A product can have different criticality windows. Intraday price data may become stale in seconds; the same historical data may support research months later. Payroll availability can tolerate some delay early in a cycle but become critical near disbursement. Record environment and calendar conditions.

Frequency is not criticality. A disaster-recovery manifest used only during catastrophe can be essential. A report queried millions of times may be a reconstructible convenience. Popularity, data size, and executive attention are weak proxies unless connected to consequences.

Analyze dependency graphs in both directions. Upstream, identify sources, identifiers, reference data, schemas, keys, policies, people, vendors, networks, and facilities required to produce the product. Downstream, identify services, reports, decisions, models, partners, and obligations that depend on it.

Criticality can propagate, but not mechanically. A critical consumer may use a replaceable optional field from a source. A low-volume reference table may be irreplaceable. Record dependency purpose, substitutability, failure behavior, freshness, and fallback before inheriting a tier.

Concentration creates systemic risk. Many products may depend on one identity service, schema registry, encryption key service, cloud region, specialist, or shared pipeline. Redundancy that shares credentials, control plane, network, operator, or corrupted source may fail together. Map common-cause and correlated failure domains.

Derived data creates propagation risk. A wrong source unit can contaminate aggregates, reports, models, and decisions. Lineage estimates reach, but actual consequence also depends on transformations, cached versions, detection, and use. Preserve release and source positions so affected outputs can be identified.

Feedback increases complexity. A risk score changes investigations, producing labels used to retrain the score. A forecast changes inventory, altering demand signals. Assess selection effects, self-confirming loops, delayed harms, and decision authority. Analytical accuracy alone does not characterize risk.

Likelihood is conditional on horizon, exposure, threat capability, vulnerabilities, controls, and environment. “Rare” over one day can be material over ten years or millions of operations. State the unit and basis. Separate frequency of initiating events from probability of consequence given the event.

Use quantitative probability when observations or defensible models support it. Use calibrated ranges, ordinal definitions, or structured scenarios when they do not. Never multiply labels such as `high = 3` and `medium = 2` and call the result a measured expected loss. Ordinal products do not preserve meaningful distance.

Absence of incidents is weak evidence when detection is poor, exposure new, or events rare. Near misses, control failures, attack intelligence, quality escapes, audits, user reports, simulations, and analogous systems can inform likelihood. Record source quality and uncertainty.

Impact estimates also need ranges and temporal structure. Direct remediation cost may be measurable; loss of trust, rights, or life may not be responsibly monetized. Preserve qualitative and distributional consequences. Some policy and ethical constraints should not be traded through expected monetary value.

Distinguish **inherent**, **current**, **residual**, and **target** risk. Inherent risk imagines specified controls absent; the counterfactual must be clear. Current risk reflects controls as actually operating. Residual risk estimates what remains after planned or existing treatment. Target risk expresses the authorized desired condition.

Do not subtract control ratings mechanically. A control changes a particular causal path, likelihood, detection, or impact. Encryption may reduce disclosure after storage theft but not authorized misuse, bad analytics, or key compromise. Backup may reduce data loss but not prove clean, timely consumer recovery.

For every control, record the risk scenarios addressed, owner, design, enforcement point, coverage, dependencies, operating evidence, effectiveness evidence, failure behavior, exceptions, and test frequency. A configuration flag is evidence of presence, not outcome.

Risk treatment options include **avoid** the use or dependency, **reduce** likelihood or impact, **share or transfer** specified obligations, **prepare** contingency, **accept** residual exposure, or **pursue** an opportunity with safeguards. Contracts and insurance can transfer costs or duties, but affected people and operations may still suffer.

Select treatments by causal effectiveness, policy, feasibility, lifecycle cost, new risks, reversibility, and evidence. Data minimization can reduce exposure and cost. Validation can reduce corruption. Isolation can reduce blast radius. Diverse recovery sources can reduce common-cause failure. Human review can reduce some automated harms while adding delay and inconsistency.

Risk acceptance belongs to an authority accountable for the affected objective and empowered by policy. A pipeline team cannot accept enterprise regulatory exposure merely because it operates the job. The record names scenario, residual estimate, uncertainty, controls, conditions, owner, approver, expiry, monitoring, and triggers.

Criticality drives, but does not uniquely determine, recovery. Conduct business or mission impact analysis to identify maximum tolerable disruption, recovery time, recovery point, minimum service, dependencies, capacity, order, and reopening authority. NIST [SP 800-34 Rev. 1](https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final) connects business impact analysis with contingency priorities in its federal information-system scope.

Recover a consistent **recovery set**: data, metadata, schemas, history, policies, identity, keys, code, configuration, checkpoints, lineage, controls, documentation, and skilled operation. A restored table without its semantics or authorization may be unusable or unsafe.

Recovery objectives must be consumer-facing. A database online in ten minutes does not prove a regulatory report, fraud decision, or clinical workflow is correct. Restore, replay, reconcile, validate, and obtain authority before reopening consequential use. Test capacity and degraded modes.

Privacy risk deserves independent treatment. NIST's [Privacy Framework](https://www.nist.gov/privacy-framework) is a voluntary tool for managing privacy risk through organizational outcomes and data-processing ecosystem understanding. Privacy impact can occur without confidentiality failure, so a CIA-only model is insufficient.

Security risk is also broader than asset labels. NIST [CSF 2.0](https://doi.org/10.6028/NIST.CSWP.29) organizes cybersecurity outcomes across Govern, Identify, Protect, Detect, Respond, and Recover. Architecture should map assets, flows, suppliers, roles, controls, response, and recovery without treating framework alignment as certification.

Third parties change control and evidence boundaries. Assess provider dependency, sub-processors, data location, access, change, incident notice, continuity, recovery, deletion, audit, concentration, financial health, and exit. A contractual promise requires verification and contingency.

Human dependencies matter. One analyst may know how to reconcile a critical close; one administrator may hold recovery knowledge; one steward may interpret identifiers. Document procedures, cross-train, rehearse, and protect staff workload. Do not reduce people to replaceable control components.

Risk registers should link to architecture identities, flows, decisions, controls, evidence, incidents, and review triggers. One row per broad asset is rarely enough. One scenario may cross many products; one product may participate in many scenarios. Preserve many-to-many relationships.

Prioritization should combine severity, urgency, exposure, control weakness, uncertainty, propagation, and decision reversibility. Keep noncompensable constraints visible. High uncertainty and high plausible impact often justify evidence gathering or precaution, not a low average.

Portfolio views reveal aggregation and concentration. Individually accepted exceptions may combine into an unacceptable shared dependency. Many small copies can create a large attack and deletion surface. Review cumulative exposure across domains and suppliers.

Risk measures include leading observations—control coverage, stale classifications, untested recoveries, unresolved critical lineage—and lagging outcomes such as incidents and losses. Pair them with denominators and counter-metrics. Fewer reported incidents can mean better controls or worse detection.

Review criticality when consumers, purposes, classifications, volumes, jurisdictions, threats, controls, dependencies, recovery evidence, business cycles, or tolerances change. Retirement itself creates risk: preserve required evidence, migrate consumers, revoke access, and verify deletion or archival treatment.

Communicate at the decision's altitude. Executives need consequences, concentrations, options, authority, and residual exposure. Engineers need scenarios, boundaries, controls, failure behavior, and tests. Consumers and affected stakeholders need fitness, limitations, incident communication, and recourse.

## Definitions and Notation

Let a risk scenario be:

`r = (o, a, c, e, k, p, h, l, i, z, u, w)`

where `o` is objective, `a` asset or flow, `c` cause or condition, `e` event, `k` consequence, `p` affected parties, `h` horizon, `l` likelihood characterization, `i` impact profile, `z` controls, `u` uncertainty, and `w` owner.

Let impact be a vector rather than a forced scalar:

`i = (confidentiality, integrity, availability, privacy, safety, financial, operational, legal, societal)`

Dimensions and scales must be tailored and defined. A decision may add environmental, scientific, accessibility, or other consequences. Aggregation is optional and must not erase noncompensable dimensions.

For product `x`, decision `d`, scenario `r`, and time `t`, write `Crit(x,d,r,t)` for its criticality profile. It depends on consequence, time to harm, substitutability, dependency, detection, correction, and recovery—not only inherent content.

Residual risk is conditional: `Residual(r | controls, evidence, assumptions, time)`. It is not simply inherent score minus control score. Record how each control changes a causal path and how effectiveness was established.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for data-risk and criticality assessment.

**1. Context gate.** Define objectives, system boundary, stakeholders, affected parties, horizon, risk criteria, authority, and decision to inform.

**2. Scenario gate.** State cause, event, consequence, affected parties, timing, and evidence. Split unrelated failure modes.

**3. Asset and flow gate.** Resolve products, representations, sources, consumers, purposes, classifications, and authoritative decisions.

**4. Impact gate.** Analyze confidentiality, integrity, availability, privacy, safety, financial, operational, legal, societal, and distributional consequences.

**5. Dependency gate.** Map upstream and downstream paths, common causes, concentration, substitutability, workarounds, propagation, and feedback.

**6. Likelihood gate.** Define horizon, exposure, conditions, observations, model, range or scale, confidence, and detection limitations.

**7. Control gate.** Map preventive, detective, corrective, and recovery controls to causal paths; verify coverage, operation, effectiveness, dependencies, and bypass.

**8. Criticality and recovery gate.** Determine time to harm, minimum service, maximum disruption, RPO/RTO, consistent recovery set, sequence, capacity, and reopening authority.

**9. Treatment gate.** Compare avoid, reduce, share, prepare, pursue, and accept choices under hard constraints, costs, new risks, and evidence.

**10. Decision and maintenance gate.** Record residual uncertainty, acceptance authority, expiry, monitoring, triggers, dissent, and portfolio aggregation.

The executable example reviews a small criticality register. It flags a high-impact product without an owner, a low rating based on missing lineage, an untested recovery claim, and a risk acceptance whose approver lacks authority.

<!-- bijux-verify: {"id":"criticality-register-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"records=4\nvalid=0\nfindings=customer_export:unknown-is-not-low,exchange_rates:missing-owner,payroll_snapshot:recovery-untested,risk_scores:unauthorized-acceptance\nready=false\n","stderr":""}} -->
```python
records = (
    {"id": "exchange_rates", "impact": "high", "owner": "", "lineage": "known", "recovery_tested": True, "acceptor": "risk-owner"},
    {"id": "customer_export", "impact": "low", "owner": "privacy", "lineage": "unknown", "recovery_tested": True, "acceptor": "risk-owner"},
    {"id": "payroll_snapshot", "impact": "high", "owner": "payroll", "lineage": "known", "recovery_tested": False, "acceptor": "risk-owner"},
    {"id": "risk_scores", "impact": "moderate", "owner": "risk", "lineage": "known", "recovery_tested": True, "acceptor": "pipeline-team"},
)

findings = []
valid = 0
for record in records:
    local = []
    if record["impact"] == "high" and not record["owner"]:
        local.append("missing-owner")
    if record["impact"] == "low" and record["lineage"] == "unknown":
        local.append("unknown-is-not-low")
    if record["impact"] == "high" and not record["recovery_tested"]:
        local.append("recovery-untested")
    if record["acceptor"] != "risk-owner":
        local.append("unauthorized-acceptance")
    if local:
        findings.extend(f"{record['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"records={len(records)}")
print(f"valid={valid}")
print(f"findings={','.join(sorted(findings))}")
print(f"ready={str(not findings).lower()}")
```

The checker validates only four declared registry rules. It does not prove impact ratings, lineage completeness, recovery quality, real authority, likelihood, control effectiveness, legal compliance, or ethical acceptability. Those require sourced scenarios, representative tests, appropriate experts, and accountable decisions.

## Alternatives and Trade-Offs

**Qualitative versus quantitative assessment.** Qualitative scales support sparse evidence and deliberation but can be inconsistent. Quantitative ranges support comparison and sensitivity but can manufacture precision. Match method to evidence and consequence.

**Asset-first versus scenario-first analysis.** Asset inventories improve coverage. Scenario-first analysis keeps consequence visible. Link many-to-many assets and scenarios rather than choosing one view.

**Maximum impact versus expected loss.** Maximum impact protects against catastrophic tails but can over-prioritize implausible conditions. Expected loss combines likelihood and impact but can hide rights and rare catastrophe. Preserve both where relevant.

**Uniform tiers versus multidimensional profiles.** Tiers simplify operations and control baselines. Profiles preserve confidentiality, integrity, availability, privacy, safety, and temporal differences. Derive tiers from retained profiles.

**Prevention versus resilience.** Prevention reduces event probability. Resilience limits consequence and duration. Neither substitutes universally for the other; defense depends on causal paths and common failures.

**Central versus domain assessment.** Central teams improve consistency and portfolio concentration analysis. Domains understand semantics and consequences. Shared criteria with domain evidence and independent challenge are stronger than either alone.

**Risk transfer versus retained capability.** Suppliers and insurance can shift duties or costs. The organization may retain service, rights, and reputational consequences. Maintain contingency and exit proportional to retained exposure.

**Transparency versus sensitive risk detail.** Broad visibility improves coordination and challenge. Detailed topology, vulnerabilities, personal information, and investigations require protection. Publish safe summaries while controlling evidence.

## Failure Modes and Misconceptions

1. **Sensitive means critical.** Disclosure sensitivity and outcome dependency are different dimensions.
2. **Large or popular means important.** Small, rare, and dormant data can be essential.
3. **A risk is a noun.** Useful risks connect cause, event, consequence, affected parties, horizon, and evidence.
4. **No incidents means low likelihood.** Detection, novelty, rarity, and exposure determine what absence shows.
5. **Ordinal multiplication is measurement.** Numeric labels do not create interval or ratio scales.
6. **Unknown means low.** Missing evidence increases uncertainty and may justify investigation or precaution.
7. **Control presence equals effectiveness.** Coverage, operation, bypass, dependency, and outcomes require evidence.
8. **Backups prove recovery.** Consumer-consistent restore, replay, reconciliation, capacity, and reopening must be exercised.
9. **Criticality automatically propagates.** Dependency purpose, fallback, substitutability, and timing determine propagation.
10. **Contracts transfer all risk.** Harms and operational consequences can remain with the organization and affected people.
11. **The operating team accepts the risk.** Acceptance authority follows accountable objectives and policy delegation.
12. **A risk register is static.** Uses, threats, controls, dependencies, evidence, and tolerances change.

## Worked Examples

### Example 1

**Question:** Is a public transit timetable low risk because it is public?

**Reasoning:** Confidentiality may be low, while integrity and availability can be critical to routing and accessibility.

**Conclusion:** Assess consequence dimensions separately.

### Example 2

**Question:** A table has only 20 rows and one daily read. Is it low criticality?

**Reasoning:** If it supplies exchange rates for settlement, one wrong value can propagate large loss.

**Conclusion:** Volume and frequency are weak proxies.

### Example 3

**Question:** No privacy incidents were detected last year.

**Reasoning:** Examine exposure, detection coverage, authorized harmful processing, near misses, and reporting incentives before updating likelihood.

**Conclusion:** Absence of evidence has conditions.

### Example 4

**Question:** A backup restored successfully. Is recovery proven?

**Reasoning:** Verify a consistent recovery set, source position, replay, reconciliation, capacity, consumer decisions, and reopening authority.

**Conclusion:** Byte restoration is only one recovery step.

### Example 5

**Question:** Encryption lowers a disclosure score by two points.

**Reasoning:** Identify which threat paths encryption changes and test keys, coverage, operation, and authorized misuse; do not subtract arbitrary labels.

**Conclusion:** Controls change causal paths, not generic scores.

### Example 6

**Question:** A vendor accepts liability for outage.

**Reasoning:** Financial terms do not restore service or prevent harm. Assess continuity, evidence, concentration, and exit.

**Conclusion:** Transfer does not erase retained consequences.

### Example 7

**Question:** A derived aggregate has no personal identifiers. Is privacy risk absent?

**Reasoning:** Consider small groups, linkage, inference, purpose, decisions, and affected populations.

**Conclusion:** Transformation changes but does not automatically remove risk.

### Example 8

**Question:** Two independent stores share one key service.

**Reasoning:** Their apparent redundancy has a common-cause dependency. Test key-service and credential failure.

**Conclusion:** Map failure domains, not component counts.

### Example 9

**Question:** Who may accept delayed payroll recovery?

**Reasoning:** The authority accountable for payroll outcomes and empowered by policy, informed by operations, finance, legal, and affected employees.

**Conclusion:** Operators provide evidence; accountable authority accepts exposure.

### Example 10

**Question:** When must criticality be reassessed?

**Reasoning:** On changed use, consumer, policy, threat, dependency, control, volume, timing, incident, recovery evidence, or tolerance.

**Conclusion:** Criticality is contextual and temporal.

## Cross-Program Connections

[Security Engineering](../../25-security-engineering/ROADMAP.md) develops threat modeling, vulnerabilities, security controls, assessment, incident response, and assurance. Data risk adds semantic corruption, provenance, quality, lifecycle, sharing, and decision feedback.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes hazard analysis, criticality, failure modes, safety, assurance cases, recovery, human factors, and lifecycle risk. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains partitions, common-mode failure, replication, consistency, and recovery assumptions.

[Data Engineering](../../19-data-engineering/ROADMAP.md) implements quality, lineage, SLO, observability, incident, disaster recovery, economics, and lifecycle controls. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) provides common controls and evidence but cannot accept product risk for domain owners.

## References

- ISO, [*ISO 31000:2018 — Risk Management Guidelines*](https://www.iso.org/standard/65694.html), 2018, confirmed current in 2023. International principles and guidelines for organizational risk management.
- NIST, [*SP 800-30 Rev. 1 — Guide for Conducting Risk Assessments*](https://csrc.nist.gov/pubs/sp/800/30/r1/final), 2012. Federal information-security guidance for preparing, conducting, and maintaining risk assessments.
- NIST, [*FIPS 199 — Standards for Security Categorization of Federal Information and Information Systems*](https://csrc.nist.gov/pubs/fips/199/final), 2004. United States federal standard for confidentiality, integrity, and availability impact categorization.
- NIST, [*Cybersecurity Framework (CSF) 2.0*](https://doi.org/10.6028/NIST.CSWP.29), NIST CSWP 29, 2024. Outcome-oriented cybersecurity risk-management framework across Govern, Identify, Protect, Detect, Respond, and Recover.
- NIST, [*Privacy Framework*](https://www.nist.gov/privacy-framework), checked 2026-09-03. Voluntary framework for identifying and managing privacy risk in data processing ecosystems.
- NIST, [*SP 800-34 Rev. 1 — Contingency Planning Guide for Federal Information Systems*](https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final), 2010. Federal guidance linking business impact analysis, recovery requirements, contingency strategies, testing, and maintenance.
- NIST, [*SP 800-39 — Managing Information Security Risk*](https://csrc.nist.gov/pubs/sp/800/39/final), 2011. Organization-, mission/business-process-, and information-system-level risk-management guidance.
- NIST, [*AI Risk Management Framework (AI RMF 1.0)*](https://doi.org/10.6028/NIST.AI.100-1), NIST AI 100-1, 2023. Voluntary framework for governing, mapping, measuring, and managing risks from AI systems, including data dependencies and affected parties.

## Exercises

### Exercise 1

Write distinct confidentiality, integrity, availability, privacy, and operational risk scenarios for a public transit location feed.

### Exercise 2

Assess the criticality of a low-volume exchange-rate product for settlement. Include time to harm, dependencies, fallback, detection, correction, and recovery.

### Exercise 3

Review a register that labels every customer dataset `high` and every public dataset `low`. Propose a multidimensional replacement and migration path.

### Exercise 4

Design a recovery-priority analysis for payroll, recommendation history, access-policy data, and a regulatory archive without ranking by storage size.

### Exercise 5

Write a residual-risk acceptance record for an expiring unencrypted legacy partner transfer. Include authority, controls, uncertainty, expiry, exit, and triggers.

## Answers to the Exercises

### Answer 1

Confidentiality: precise real-time vehicle traces intended for public use expose an operator-only emergency route before authorized publication, creating staff or public harm. Integrity: an attacker or faulty pipeline changes route positions, causing riders to travel to unsafe or inaccessible stops. Availability: the feed is absent during a disruption, preventing passengers and responders from adapting. Privacy: persistent vehicle and shift traces enable inference about drivers or small passenger groups even through authorized publication. Operational: routing systems consume delayed positions and dispatch unnecessary vehicles, worsening congestion. Each scenario needs population, environment, horizon, evidence, controls, uncertainty, owner, and affected stakeholder review.

### Answer 2

The product is integrity-critical if each daily settlement multiplies balances by its rates. Harm can occur at the next settlement; repeated wrong values propagate to ledgers, reports, customers, and corrections. Map the market-data source, approval, currency and effective-time semantics, transformation, keys, distribution, settlement consumers, and common infrastructure. Fallback might use the last approved rate only for named currencies and duration, manual approval, or paused settlement. Detect through source comparison, bounds, dual calculation, and control totals. Correct using versioned rates, affected-transaction identity, compensating entries, and consumer notice. Recover a clean approved snapshot, provenance, rules, access, and dependent positions, then reconcile before reopening.

### Answer 3

Retain the old labels temporarily as migration metadata, but create profiles for confidentiality, integrity, availability, privacy, safety, financial, legal, operational, and societal consequence plus time to harm, consumers, dependencies, substitutability, recovery, and uncertainty. Tie every rating to a scenario, definition, owner, evidence, and review date. Public safety and routing products may rise on integrity or availability; confidential historical data may remain high on disclosure while lower on immediate availability. Map old control baselines to dimensions, identify gaps, review highest plausible harm and unknowns first, and deprecate the legacy label only after controls and consumers use the new profile.

### Answer 4

Start with business or mission processes and time-dependent consequences. Payroll may have a cycle-sensitive deadline, employee harm, legal duties, identity, bank, and approval dependencies. Recommendation history may tolerate delay if serving has safe fallback, though privacy and rebuild cost remain. Access-policy data may require near-immediate integrity and availability because many services cannot authorize safely without it. A regulatory archive may tolerate online delay while requiring very strong preservation, authenticity, confidentiality, and retrieval within an official deadline. Define minimum services, MTD, RPO/RTO, recovery sets, dependencies, capacity, order, manual work, reconciliation, and reopening authority. Test combined failure and common control planes.

### Answer 5

Identify the exact partner, dataset, fields, purpose, route, frequency, jurisdiction, and legacy component. State disclosure and integrity scenarios, affected parties, horizon, current evidence, detection gaps, and residual uncertainty. The accountable data and risk authority—plus privacy, security, legal, or contract authority as applicable—approves; the integration team does not self-accept. Compensating controls may include minimization, strong file-level encryption where possible, private transport, allowlisted identities, short retention, reconciliation, monitoring, and rapid revocation. Set a near expiry, funded replacement owner, milestones, partner contract change, and verified deletion. Trigger immediate review on incident, route or recipient change, new data, failed control, missed milestone, or changed obligation. This answer is not legal or security approval.
