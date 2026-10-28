---
module_id: SARCH-005
program: Software Engineering: Software Architecture
level: 1
module_number: 5
title: Constraints, Assumptions, and Risks
status: complete
last_verified: 2026-09-05
---

# Constraints, Assumptions, and Risks

## One-Page Review

### Governing question

Which conditions truly restrict architecture, which beliefs require validation, and which uncertain events threaten objectives—and how should each affect decisions without being confused with the others?

### Essential definitions

- A **constraint** is an externally imposed or deliberately governed restriction on acceptable solutions.
- An **assumption** is a proposition treated as true for a decision despite incomplete evidence.
- A **risk** is uncertainty that can affect objectives; an architectural risk links uncertain conditions to consequences and decisions.
- An **issue** is a relevant condition already known to exist, not a future uncertainty.
- A **dependency** is something an outcome relies on; it becomes a risk source when its future state or behavior is uncertain.
- **exposure** is a declared way to compare risk using likelihood and impact, not an objective property independent of the model.
- A **mitigation** changes likelihood or impact; a **contingency** prepares a response if the risk occurs.
- **residual risk** remains after treatment; **risk acceptance** is an authorized decision, not passive neglect.

### Central model, mechanism, or theorem

Maintain three linked registers. A constraint record states source, scope, authority, effective period, interpretation, evidence, and exception process. An assumption record states proposition, rationale, confidence, owner, validation method, deadline, impact if false, and trigger. A risk record states condition, uncertain event, consequence, affected objectives, likelihood and impact bases, owner, treatment, indicators, contingency, residual exposure, and acceptance authority.

Use trace links rather than collapsing the records: an assumption proven false may create an issue; a constraint can reduce options or mitigate risk; a dependency can motivate assumptions and risks.

### Critical invariants

- identify source and authority for every claimed constraint;
- make constraints testable and time- or scope-bounded;
- state assumptions as falsifiable propositions;
- assign assumption validation deadlines before dependent decisions become irreversible;
- write risks as cause/event/consequence chains tied to objectives;
- distinguish risk, issue, defect, hazard, dependency, and uncertainty;
- record likelihood and impact bases, not unexplained colors or numbers;
- assign treatment and acceptance to authorized owners;
- preserve residual risk, dissent, and evidence limits;
- reopen records when context, evidence, decisions, incidents, or lifecycle stage changes.

### Common failures

Common failures include treating preferences as constraints; citing “compliance” without a rule or interpretation; hiding a vendor choice as a mandate; writing assumptions as facts; validating assumptions after commitment; calling known defects risks; naming “lack of resources” without consequence; multiplying ordinal scores; using red/amber/green without definitions; assigning all risk to the architect; treating mitigation plans as completed controls; accepting risk without authority; and deleting closed records that explain later decisions.

### Compact example

A team says “data must stay in Sweden, so use Provider X.” The location rule may be a constraint, but the provider is only one candidate solution. Record the authoritative source, which data and copies it covers, lawful exceptions, effective dates, and evidence. Record assumptions that the provider’s regions, backups, support access, and subprocessors satisfy the interpretation. Record risks that configuration drift or supplier change creates prohibited transfer. This separation preserves alternatives and makes validation possible.

### Connections

[SARCH-003](003-functional-scope-and-system-context.md) identifies boundaries and dependencies; [SARCH-004](004-quality-attributes-as-architectural-drivers.md) identifies threatened objectives. [SARCH-006](../ROADMAP.md) selects architecturally significant requirements, and [SARCH-007](../ROADMAP.md) compares competing objectives. Later evaluation modules use these records to identify risk, sensitivity, and trade-off points.

## Governing Question

Architecture decisions are made with incomplete knowledge and limited freedom. Some conditions are genuinely mandatory, some are provisional beliefs, and some are uncertain threats or opportunities. If these are written as one undifferentiated list, teams freeze arbitrary choices, conceal uncertainty, and discover invalid premises only after reversal becomes costly.

The governing question is how to represent each condition honestly enough that it guides design, evidence, escalation, and revision. The purpose is not to eliminate uncertainty. It is to expose what decisions depend on, who can change or accept each condition, and what must happen before the next commitment.

## Why This Matters

A false constraint can exclude a simpler architecture for years. An unstated assumption can make an apparently rational design fail when workload, staffing, supplier behavior, data authority, or regulation differs. A vague risk register can create ceremony without changing decisions. Conversely, explicit records make options visible, focus experiments, and preserve why a costly mechanism exists.

Constraints, assumptions, and risks interact with every architecture structure. Region restrictions affect deployment and data flows. Skill and staffing assumptions affect operability. Volume assumptions affect capacity and partitioning. Supplier continuity affects exit design. Recovery risks affect state, topology, and evidence. Their significance increases when decisions are expensive or irreversible.

These records also allocate authority. Legal interpretation belongs to qualified authorities, business-risk acceptance to delegated decision makers, safety acceptance to appropriate safety governance, and technical evidence to accountable engineering and assurance roles. An architect can analyze consequences but cannot silently acquire every authority.

## Prerequisites and Retrieval

Retrieve objective, stakeholder, concern, system boundary, environment, dependency, quality-attribute scenario, requirement, decision, evidence, uncertainty, probability, consequence, hazard, threat, vulnerability, control, owner, authority, lifecycle, and traceability.

From prior modules, retrieve the distinction between architecture and its description, known stakeholder inventories, typed context crossings, and contextual response measures. You should be able to explain why a current deployment is not automatically a constraint and why an external dependency is not automatically a risk statement.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish constraints, assumptions, risks, issues, hazards, and dependencies;
2. test whether a claimed constraint has source, authority, scope, and exception semantics;
3. write falsifiable assumption records with validation deadlines;
4. formulate cause-event-consequence risk statements;
5. select qualitative or quantitative comparison methods without false precision;
6. distinguish mitigation, contingency, transfer, avoidance, acceptance, and observation;
7. assign technical ownership and risk-acceptance authority correctly;
8. trace records to scenarios, decisions, evidence, and change triggers;
9. analyze correlated and systemic uncertainty;
10. maintain residual risk and reopen invalidated premises across the lifecycle.

## Core Exposition

**Classify before designing.** Ask of every “must”: who imposes it, through what authority, over which system and period, and what proves conformance? If no authoritative source exists, it may be a preference, goal, assumption, or inherited decision. That does not make it unimportant; it changes how it may be challenged.

Constraints include laws and regulations as interpreted for the system, contractual obligations, physical limits, interoperability commitments, budgets and deadlines authorized by governance, required interfaces, organizational policies, and accepted architecture principles. Each can have exceptions and expiry. “We already use Java” is current context. “The supported runtime is Java 21 until contract renewal because the operator certifies only that baseline” is a bounded constraint with a reason and review trigger.

**Separate policy from solution.** “Personal data must remain within named jurisdictions” may constrain placement and access. “Use one vendor’s regional database” is a solution unless explicitly mandated. Preserve the underlying constraint so alternative designs can be evaluated and a supplier change does not erase the obligation.

**Make assumptions falsifiable.** Useful assumptions assert something that evidence could contradict: peak accepted load will remain below 2,000 requests per second through 2028; all clients can validate a new signature algorithm before cutover; restoration staff can reach the recovery environment without the primary identity plane. Record why the belief is plausible and what decision depends on it.

Assign an owner, confidence basis, validation method, deadline, and invalidation trigger. Validate high-impact assumptions before architectural option loss grows. A cheap prototype, traffic analysis, contract review, fault exercise, or stakeholder study may retire uncertainty. “Users will like it” is too vague; define population, task, outcome, and observation.

**Write complete risk statements.** “Vendor risk” names a topic. A useful statement connects condition, uncertain event, and consequence: because all encryption keys and backups depend on one supplier account, loss or suspension of that account could make regulated records unrecoverable, causing service loss and retention violations. This formulation exposes what can be changed, observed, tested, and owned.

Risk is relative to objectives and perspective. Faster release can create opportunity and operational downside. A privacy authority, product owner, operator, and customer may evaluate the same uncertainty differently. Preserve distributions of consequence and non-compensable obligations rather than forcing consensus through a score.

**Use ratings as decision aids.** Qualitative likelihood and impact scales require definitions, time horizon, evidence, and calibration. Ordinal labels should not be multiplied as if the result were a physical quantity. Quantitative estimates can support sensitivity and expected-loss reasoning when data and models justify them, but rare events, adversaries, dependence, and changing systems create wide uncertainty.

For a simplified expected loss $E[L]=p\times I$, state probability horizon, impact units, distribution, and exclusions. Two risks with the same expectation can demand different treatment when one is frequent and recoverable while another is catastrophic. Legal, rights, safety, or mission limits may prohibit trading harm against cost by expectation alone.

**Choose treatment deliberately.** Avoid risk by removing the exposed objective or mechanism; reduce likelihood or impact through design and controls; transfer defined financial or operational consequences through contracts or insurance; accept residual risk under authority; or monitor when action is not yet justified. Transfer rarely removes accountability for the integrated system.

A mitigation must have owner, due condition, resources, verification, and effect on the risk model. “Use redundancy” is not complete: state which failures become tolerated, which correlated failures remain, and what evidence supports failover and recovery. A contingency differs: it specifies action after an indicator or event, such as switching suppliers, entering manual operation, or restoring from offline copies.

**Distinguish issue and risk.** If a certificate has expired, that is an issue with current impact. Future recurrence under uncertain renewal is a risk. If a hazard is a potential source of harm, risk analysis considers scenarios, likelihood or frequency where meaningful, severity, exposure, controls, and authority under the applicable domain process. Do not replace specialized safety, security, privacy, financial, or legal methods with a generic register.

**Model dependence and aggregation.** Risks are rarely independent. One identity outage may disable production access, monitoring, and recovery. One supplier can host nominally separate regions. One migration can invalidate load, data, and staffing assumptions together. Record common causes, coupling, cascades, and portfolio concentration. Adding individual red/amber/green entries does not expose systemic fragility.

**Trace decisions and residual risk.** Link every significant decision to the constraints it honors, assumptions it uses, risks it treats or introduces, evidence, and acceptance. Link each record back to affected goals and scenarios. Preserve rejected options and superseded assumptions so later reviewers understand why the architecture exists.

Closure requires evidence and authority. A mitigation marked complete may reduce but not eliminate risk. Record residual exposure, who accepted it, under what conditions, for what period, and which triggers reopen it. Incidents, near misses, workload change, supplier notices, new jurisdictions, staff turnover, and failed tests are evidence that premises need revision.

## Definitions and Notation

Let $O$ be the set of objectives and $D$ the set of architecture decisions. Define three record sets: constraints $C$, assumptions $A$, and risks $R$.

A constraint $c\in C$ has the form

$$
c=(statement,source,authority,scope,period,evidence,exception).
$$

An assumption $a\in A$ is

$$
a=(proposition,basis,confidence,owner,test,deadline,falseImpact,trigger).
$$

A risk $r\in R$ is

$$
r=(condition,event,consequence,objectives,horizon,estimate,treatment,owner,authority).
$$

Trace relations $uses\subseteq D\times A$, $honors\subseteq D\times C$, and $affects\subseteq R\times O$ expose decision premises. If an assumption used by a decision becomes false, the decision must be reviewed; this is a governance rule, not a logical proof that the decision is wrong.

When probability and impact are meaningfully quantified, simplified expected loss may be

$$
E[L]=\sum_i p_i I_i.
$$

This expression requires compatible impact units and an explicit probability model. It is unsafe to apply directly to ordinal “low/medium/high” categories, mutually dependent events, or non-compensable obligations. A range or distribution is often more honest than a point estimate.

## Mechanisms, Invariants, or Proof Structure

Use the following continuous mechanism.

1. **Frame objectives and context:** name system, lifecycle, horizon, decision, stakeholders, and authorities.
2. **Elicit candidate conditions:** inspect goals, scenarios, interfaces, contracts, policies, incidents, dependencies, and evidence gaps.
3. **Classify:** separate constraints, assumptions, risks, current issues, decisions, and open questions.
4. **Normalize records:** make constraints sourced, assumptions falsifiable, and risks causal.
5. **Analyze significance:** consider consequence, likelihood basis, reach, coupling, irreversibility, and option loss.
6. **Plan validation and treatment:** assign owners, deadlines, resources, evidence, indicators, and contingencies.
7. **Decide under authority:** record interpretation, exceptions, residual risk, dissent, and acceptance conditions.
8. **Trace:** connect records to objectives, quality scenarios, options, decisions, implementation, tests, and operations.
9. **Monitor:** observe leading indicators, control performance, incidents, supplier and context change.
10. **Reopen or retire:** revise premises and decisions when evidence or authority changes; preserve history.

The governing invariants are explicit classification, authoritative constraint source, falsifiable assumption, causal risk statement, declared estimation basis, accountable treatment, authorized acceptance, visible residual risk, dependency awareness, and lifecycle traceability.

Register conformance proves only that required fields and relations are present. It cannot establish that every constraint was found, an assumption is true, probability is calibrated, treatment is effective, or residual risk is acceptable. Those claims require domain evidence and qualified judgment.

## Alternatives and Trade-Offs

**Separate registers** preserve semantics and tailored fields but can fragment related reasoning. **One integrated register** improves navigation but tempts teams to treat every row alike. Use distinct record types with explicit links in one governed information model.

**Qualitative scales** are accessible under sparse data and support discussion, but suffer inconsistent interpretation and invalid arithmetic. **Quantitative models** enable sensitivity and cost comparison but require data, distributions, dependencies, and uncertainty modeling. Match method to decision; do not add numbers for prestige.

**Early validation** reduces option loss but consumes time before a design may be selected. **Deferred validation** preserves speed but can harden a false premise. Prioritize assumptions by consequence if false, uncertainty, dependency reach, and time until the decision becomes costly to reverse.

**Risk avoidance** can remove exposure but also abandon value. **Mitigation** preserves value with control cost and residual failure. **Transfer** redistributes specified consequences while adding counterparty risk. **Acceptance** preserves resources but requires explicit authority and monitoring. The right treatment depends on objectives and non-compensable constraints.

## Failure Modes and Misconceptions

- **“The current system is a constraint.”** Existing state is context until an authority and bounded restriction are identified.
- **“The deadline cannot move.”** Record who set it, why, what scope it governs, and what trade or escalation process exists.
- **“Compliance requires vendor X.”** Separate the authoritative rule and interpretation from one proposed implementation.
- **“Assumptions are obvious.”** Unwritten premises cannot be validated, monitored, or connected to decisions.
- **“High confidence means validated.”** Confidence records belief and evidence quality; it is not truth.
- **“A dependency is a risk.”** State the uncertain event and consequence relative to objectives.
- **“A known outage is a risk.”** It is an issue; recurrence, duration, or recovery uncertainty may create risks.
- **“Likelihood times impact is objective.”** Estimates depend on horizon, model, evidence, scale, and perspective.
- **“Red means fix first.”** Non-compensable obligations, dependencies, timing, option loss, and authority matter beyond color.
- **“Mitigation closes risk.”** Verify effect and record residual exposure.
- **“Insurance transfers accountability.”** It may transfer defined financial loss, not user, legal, safety, or mission responsibility.
- **“The architect accepts risk.”** Acceptance belongs to explicitly delegated authorities for the affected objectives.
- **“No incidents means low risk.”** Detection, exposure, reporting, and changing threats determine what absence means.
- **“Closed records can be deleted.”** History supports future change, audits, incident analysis, and decision reversal.

## Worked Examples

### Example 1

**Question:** Is “must run on Kubernetes” a constraint?

**Reasoning:** Ask for source and authority. If an approved platform policy mandates Kubernetes for services in a defined environment, with a documented exception process and review date, it is a constraint for that scope. If the team merely operates Kubernetes today, it is context and perhaps a skill or migration assumption. Preserve the desired qualities—deployment control, recovery, isolation, or supportability—so alternatives remain assessable.

**Conclusion:** Technology becomes a constraint only through explicit authority and bounded applicability, not repetition.

### Example 2

**Question:** How should the assumption “traffic will double” be recorded?

**Reasoning:** Replace it with a falsifiable proposition: peak eligible demand will remain at or below 4,000 requests per second through December 2028 under defined campaign and regional scope. Record forecast basis, confidence interval, owner, quarterly validation, capacity decision using it, consequence if exceeded, and trigger at observed 70% headroom. Include burst shape and data growth if they drive different bottlenecks.

**Conclusion:** A bounded assumption can guide capacity while creating an explicit validation obligation.

### Example 3

**Question:** Rewrite “database risk” as a useful statement.

**Reasoning:** Because primary and backup credentials depend on the same identity tenant, tenant suspension or corruption could make both copies inaccessible, causing loss of order processing and failure to meet recovery objectives. Assign an owner, horizon, evidence for likelihood, impact range, indicators, mitigation such as separately controlled recovery access, a recovery exercise, contingency, and residual-risk authority.

**Conclusion:** Cause-event-consequence structure exposes correlated recovery risk and actionable evidence.

### Example 4

**Question:** A defect currently loses one event per million. Is it a risk?

**Reasoning:** The observed defect is an issue. Uncertainty about future recurrence, detection, affected event classes, data loss, and repair time creates risks. Track the defect and remediation separately while the risk record addresses recurrence conditions and consequences. Do not downgrade the current issue by placing it in a future-risk queue.

**Conclusion:** Issues require present action; related uncertainty can be managed as linked risk.

### Example 5

**Question:** Can low, medium, and high likelihood and impact be multiplied?

**Reasoning:** These are ordinal categories unless calibrated numeric intervals are defined. Assigning 1, 2, and 3 then multiplying assumes equal spacing and valid arithmetic not supplied by the scale. Use a defined matrix for prioritization, preserve rationales and uncertainty, and inspect catastrophic or non-compensable consequences separately.

**Conclusion:** Qualitative ratings support structured judgment but do not become measurements through arithmetic.

### Example 6

**Question:** Does a multi-region deployment mitigate cloud outage risk?

**Reasoning:** It may reduce exposure to an independent regional infrastructure failure. It does not address global identity, control plane, DNS, account suspension, shared deployment errors, corrupt replicated data, or staff access. State the failure model, independence assumptions, routing and data behavior, recovery measures, tests, cost, and residual common causes.

**Conclusion:** A mitigation is credible only relative to named events, assumptions, and evidence.

### Example 7

**Question:** What is wrong with accepting “supplier continuity risk” indefinitely?

**Reasoning:** Acceptance needs an authorized owner, rationale, affected objectives, residual exposure, duration, indicators, and reopening triggers. Supplier financial deterioration, acquisition, product retirement, terms change, or missed service obligations should trigger review. Exit documentation and data portability may reduce impact even when switching is not immediately justified.

**Conclusion:** Risk acceptance is a governed, conditional decision rather than absence of action.

### Example 8

**Question:** A new privacy interpretation changes which support staff may access data. What must reopen?

**Reasoning:** Reassess the constraint source, scope, effective date, and exceptions. Invalidate assumptions about operational access, inspect identity and audit decisions that use them, identify current unauthorized paths as issues, and update risks for delayed support or circumvention. Validate controls and revised support scenarios before claiming conformance.

**Conclusion:** A changed constraint propagates through assumptions, decisions, evidence, and residual risks.

### Example 9

**Question:** Why can ten individually low risks form a high architectural concern?

**Reasoning:** They may share one cause. Separate services can all depend on one identity provider, schema registry, deployment pipeline, or specialist. Independent scoring misses concentration and cascade. Model common dependencies, simultaneous failure, recovery contention, and combined objectives, then consider isolation, fallback, staffing, or explicit acceptance.

**Conclusion:** Portfolio analysis must expose correlation and systemic reach rather than summing isolated labels.

### Example 10

**Question:** How should a rail-signaling assumption be governed?

**Reasoning:** State the exact operational and physical proposition, evidence basis, validity range, owner, validation and monitoring, dependent hazard controls, deadline, and consequence if false. Do not let a generic software risk matrix replace applicable rail safety processes. No external railway, safety, regulatory, human-factors, security, or practitioner review is claimed; named qualified authorities must validate assumptions, hazards, independence, evidence, residual risk, and acceptance.

**Conclusion:** High-consequence assumptions require domain-specific assurance and explicit authority beyond an architecture register.

## Cross-Program Connections

- [Software Engineering Methods & Evolution](../../10-software-engineering-methods-and-evolution/ROADMAP.md) connects assumptions and risks to iterative discovery, change, and governance.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) designs evidence to test assumptions, controls, and failure hypotheses.
- [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) operates indicators, mitigations, contingencies, and recovery evidence.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies threat, vulnerability, control, and security-risk methods.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) governs assumptions, hazards, lifecycle evidence, and technical risk across the wider system.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) exposes partial failure, correlated dependency, timing, and consistency uncertainty.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) turns governed constraints and recurring risks into paved capabilities without hiding exceptions.

## References

1. ISO. [ISO 31000:2018, Risk management—Guidelines](https://www.iso.org/standard/65694.html), edition 2, February 2018; reviewed and confirmed current in 2023. Principles and guidelines for creating and protecting value through integrated, structured, inclusive, dynamic risk management; consulted 2026-09-05.
2. ISO/IEC. [IEC 31010:2019, Risk management—Risk assessment techniques](https://www.iso.org/standard/72140.html), edition 2, June 2019. Selection and application of risk-assessment techniques; consulted 2026-09-05.
3. Joint Task Force Transformation Initiative. [NIST SP 800-30 Rev. 1, Guide for Conducting Risk Assessments](https://csrc.nist.gov/pubs/sp/800/30/r1/final), September 2012. Threat, vulnerability, likelihood, impact, uncertainty, and risk-assessment guidance; consulted 2026-09-05.
4. Christopher J. Alberts et al. [Continuous Risk Management Guidebook](https://www.sei.cmu.edu/library/continuous-risk-management-guidebook/), Software Engineering Institute, 1996. Continuous identification, analysis, planning, tracking, control, and communication of software-project risk.
5. ISO/IEC/IEEE. [ISO/IEC/IEEE 42010:2022, Software, systems and enterprise—Architecture description](https://www.iso.org/standard/74393.html), edition 2, November 2022. Architecture concerns, decisions, correspondence, rationale, and environment; consulted 2026-09-05.
6. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*, fourth edition, Addison-Wesley, 2021. Architecture drivers, constraints, quality scenarios, tactics, risk, and evaluation.
7. Rick Kazman, Mark Klein, and Paul Clements. [ATAM: Method for Architecture Evaluation](https://www.sei.cmu.edu/library/atam-method-for-architecture-evaluation/), CMU/SEI-2000-TR-004, 2000. Architecture risks, non-risks, sensitivity points, trade-off points, and scenario-based evaluation.
8. NASA. [NASA Systems Engineering Handbook, Revision 2](https://www.nasa.gov/reference/systems-engineering-handbook/), NASA/SP-2016-6105 Rev2, 2016. Technical risk, decision analysis, requirements, interfaces, verification, validation, and lifecycle reviews; consulted 2026-09-05.

## Exercises

### Exercise 1

Classify and rewrite these statements for a public library platform: “must use cloud,” “membership records stay in the country,” “traffic is low,” “the identity provider might fail,” and “the export job is currently broken.”

### Exercise 2

Create an assumption record for a mobile application that expects offline periods shorter than four hours. Include falsifiability, evidence, deadline, dependent decision, false impact, and triggers.

### Exercise 3

Diagnose a risk register that contains only red/amber/green topics, multiplies 1–3 likelihood and impact scores, marks mitigations complete when tickets close, and names the architect as acceptance owner.

### Exercise 4

Compare avoiding, reducing, transferring, accepting, and monitoring the risk that a critical proprietary document format becomes unsupported. Include option value and residual risk.

### Exercise 5

Design constraint, assumption, and risk governance for an unfamiliar remote water-treatment control system. Separate automated checks, engineering evidence, qualified human authority, and blockers to readiness claims.

## Answers to the Exercises

### Answer 1

“Must use cloud” is an unproven constraint claim; find the authority, scope, and exception process, or reclassify it as a goal, preference, or option. “Membership records stay in the country” is a candidate constraint requiring authoritative source, covered records and copies, access interpretation, effective period, and evidence. “Traffic is low” becomes a falsifiable assumption with workload definition, horizon, forecast basis, validation, owner, and impact if false.

“The identity provider might fail” names a dependency and event but needs conditions, consequence, objectives, horizon, likelihood basis, treatment, contingency, and authority to become a risk. “The export job is currently broken” is an issue; uncertainty about recurrence or missed records can be linked risks. Full credit requires preserving relationships without forcing all five statements into one record type.

### Answer 2

Proposition: for the declared field population and operating season, 99% of disconnected intervals during essential workflows end within four hours through December 2027. Basis: twelve months of connectivity telemetry stratified by region and journey type, with stated gaps. Owner: product reliability lead. Validation: monthly distribution and cohort review plus field sampling before architecture freeze. Deadline: before choosing the local retention and conflict strategy.

The dependent decision sizes offline storage, credential lifetime, synchronization, conflict resolution, and user status. If false, users may lose work, credentials may expire, data may diverge, and devices may exceed storage. Triggers include a new region, disaster season, network-provider change, 95th-percentile duration above three hours, field complaints, or telemetry coverage below its threshold. Confidence must reflect sampling bias; the assumption does not guarantee any individual connection.

### Answer 3

Topics lack cause-event-consequence statements, objectives, horizons, owners, evidence, treatments, indicators, contingencies, and residual exposure. Undefined ordinal labels cannot support meaningful comparison, and multiplying 1–3 codes assumes invalid equal intervals. Ticket closure shows work status, not that a control changed likelihood or impact. The architect may own technical analysis but usually lacks business, legal, safety, or mission risk-acceptance authority.

Define calibrated qualitative scales or justified quantitative models; preserve rationale and uncertainty; model dependencies and catastrophic/non-compensable cases separately. Give mitigations expected effect, evidence, and operating owner. Record residual risk and assign acceptance to delegated authorities with expiry and triggers. Keep issues distinct, link risks to decisions and objectives, and audit closure against evidence rather than workflow state.

### Answer 4

Avoidance stops accepting the format, removing new exposure but possibly abandoning customers and historical value. Reduction can implement a validated open canonical representation, dual-read migration, converters, conformance corpora, and archival documentation; transformation error and future maintenance remain. Transfer can contract vendor support or escrow, but counterparty, scope, and enforcement risks remain. Acceptance retains the format for a bounded period under authorized residual-risk ownership. Monitoring tracks vendor notices, ecosystem use, parser vulnerabilities, and conversion fidelity until a trigger justifies action.

Preserve option value by exporting semantics and test cases early, isolating the parser, retaining provenance, and testing reversible migration. Compare data criticality, horizon, legal retention, transformation loss, supplier concentration, cost, and time to exit. A combined treatment is likely: reduce and monitor now, maintain contingency, and accept bounded residual risk. None eliminates accountability for readable, correct records.

### Answer 5

Record physical, chemical, environmental, regulatory, cybersecurity, operator, and lifecycle constraints with authoritative sources, plant scope, effective conditions, evidence, and exceptions. Assumptions must state sensor ranges, process dynamics, staffing, communications, power, maintenance, and environmental conditions with validation and invalidation triggers. Risks must connect conditions and uncertain events to water quality, equipment, personnel, environment, and service consequences, including common-cause and cascade behavior.

Automated checks can validate units, schemas, configuration bounds, access, trace links, model execution for specified cases, evidence age, and alarm routing. Engineering evidence includes calibrated sensors, independent protection, simulations, hazard analysis, fault and recovery tests, manual-mode exercises, and field observation within approved conditions. These do not establish hazard completeness or acceptable risk. No external water-treatment, process-safety, environmental, regulatory, cybersecurity, human-factors, or practitioner review is claimed. Named qualified authorities must own process models, hazard controls, independent assurance, operating limits, release, and residual-risk acceptance. Unverified critical assumptions, ambiguous control authority, failed protective action, missing degraded procedures, or unresolved high-severity hazards block the corresponding readiness claim.
