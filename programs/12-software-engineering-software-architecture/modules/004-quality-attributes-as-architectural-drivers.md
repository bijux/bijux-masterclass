---
module_id: SARCH-004
program: Software Engineering: Software Architecture
level: 1
module_number: 4
title: Quality Attributes as Architectural Drivers
status: complete
last_verified: 2026-09-05
---

# Quality Attributes as Architectural Drivers

## One-Page Review

### Governing question

How do stakeholders turn words such as fast, secure, reliable, usable, and maintainable into contextual, measurable demands that genuinely influence architecture?

### Essential definitions

- A **quality attribute** is a measurable or assessable property of a system, product, service, or its behavior that matters to stakeholders.
- A **quality-attribute concern** names a desired quality but may remain too vague for design or evaluation.
- A **quality-attribute scenario** states a source, stimulus, environment, affected artifact, response, and response measure.
- An **architectural driver** is a goal, function, quality, constraint, or risk significant enough to shape system-wide structure or difficult-to-reverse decisions.
- A **quality-attribute tactic** is a design decision intended to influence a quality response, such as detecting faults or bounding resource demand.
- A **quality-attribute utility tree** organizes important scenarios by quality and business value for elicitation and evaluation.
- A **stimulus** is an event arriving at or arising within the system; a **response** is the behavior required under a stated environment.
- A **response measure** is the observation and threshold used to decide whether that response satisfies the scenario.

### Central model, mechanism, or theorem

Represent a scenario as

$$
q=(source,stimulus,environment,artifact,response,measure).
$$

Trace $q$ to stakeholder goals, scope, decisions, tactics, implementation, and evidence. The attribute name classifies the concern; the scenario supplies the context and observable obligation. A scenario becomes an architectural driver when failing it has material consequence and satisfying it requires cross-cutting, early, expensive, or difficult-to-reverse decisions.

### Critical invariants

- derive qualities from stakeholder and mission goals rather than fashion;
- name system, boundary, lifecycle state, workload, and environment;
- define observable responses and units before selecting tactics;
- separate threshold, objective, budget, and aspiration;
- include normal, peak, degraded, attacked, recovery, change, and retirement conditions as relevant;
- avoid optimizing a local component while violating the end-to-end outcome;
- identify interactions among qualities, costs, functions, and constraints;
- trace each driver to decisions and claim-specific evidence;
- preserve uncertainty and do not present a catalogue or score as proof of completeness;
- revalidate drivers when context, workload, dependency, threat, organization, or consequence changes.

### Common failures

Common failures are listing “performance, security, scalability” without scenarios; using averages where tails matter; treating availability as uptime of one process; measuring test execution instead of change confidence; turning maintainability into code-style rules; selecting microservices or caching before defining the response; copying a quality model as a mandatory checklist; combining incompatible environments into one threshold; hiding cost and human workload; accepting a supplier metric as an end-to-end guarantee; and measuring what is easy rather than what stakeholders need.

### Compact example

“The service must be fast” is not a driver. A useful scenario is: during the weekday enrollment peak, an authenticated student submits a valid course selection to the registration capability; the system confirms or rejects it within two seconds at the 99th percentile for the declared workload, while preserving prerequisite and capacity rules. This formulation exposes scope, concurrency, consistency, dependencies, observation, and a trade-off surface. It still needs evidence about workload realism and consequence.

### Connections

[SARCH-002](002-stakeholders-and-architectural-concerns.md) supplies legitimate concerns, and [SARCH-003](003-functional-scope-and-system-context.md) fixes scope and crossings. [SARCH-005](../ROADMAP.md) records constraints, assumptions, and risks; [SARCH-006](../ROADMAP.md) identifies the resulting architecturally significant requirements. Modules SARCH-011 through SARCH-020 develop individual qualities and their interactions.

## Governing Question

Stakeholders ask for a system that is “available,” “secure,” “easy to change,” and “high performance.” Those labels sound decisive but do not yet tell an architect what event occurs, under which conditions, what part of the system responds, what outcome matters, or how evidence will distinguish success from failure.

Architecture must turn quality intent into scenarios precise enough to expose system-wide forces without pretending that every important concern is already measurable. The governing problem is to decide which qualities materially shape structure, to operationalize them honestly, and to connect decisions to evidence and consequences.

## Why This Matters

Functional requirements say what outcomes a system provides. Quality attributes often determine whether those outcomes remain valuable during load, fault, attack, change, recovery, and ordinary human use. Two systems can implement the same functions while differing radically in latency, availability, confidentiality, accessibility, change cost, operability, and environmental cost.

Quality decisions are architectural when they cross component and team boundaries or constrain difficult-to-reverse choices. A recovery objective can determine data replication and deployment topology. A confidentiality obligation can determine identity, key, data-flow, and audit boundaries. A modification scenario can determine module ownership and release coupling. Discovering such forces after construction creates expensive redesign or permanent risk.

Vagueness is dangerous in both directions. “Five nines” may drive costly redundancy even when users tolerate scheduled downtime, while “highly available” may conceal that accepted work can be lost. Scenario discipline gives stakeholders a shared object to challenge: the environment, response, threshold, observation method, and consequence can each be corrected before architecture hardens.

## Prerequisites and Retrieval

Retrieve stakeholder, concern, business or mission goal, system of interest, functional scope, context, interface, dependency, scenario, constraint, assumption, risk, invariant, decision, evidence, verification, validation, probability, percentile, rate, duration, and unit.

From prior modules, retrieve why architecture is a set of significant decisions, how stakeholder representation limits discovered concerns, and how end-to-end scenarios cross system boundaries. Be prepared to distinguish a quality category from a requirement, a component metric from a user outcome, and a measured observation from a universal guarantee.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish quality attributes, concerns, scenarios, requirements, tactics, and evidence;
2. derive quality intent from stakeholder and mission goals;
3. construct a six-part quality-attribute scenario;
4. define thresholds, objectives, budgets, and units without false precision;
5. decide whether a scenario is architecturally significant;
6. separate end-to-end outcomes from local component metrics;
7. expose environmental, workload, dependency, and lifecycle assumptions;
8. identify interactions and conflicts among qualities and functions;
9. select claim-appropriate evaluation evidence;
10. maintain drivers as context and operational evidence change.

## Core Exposition

**Start from value and consequence.** Ask what stakeholders are trying to accomplish, what can prevent it, who bears the loss, and which conditions make the loss material. “Availability” may mean a shopper can browse, a clinician can retrieve medication history, or an operator can stop dangerous machinery. The same label does not imply the same response, threshold, tactics, or authority.

**Use taxonomies as prompts.** ISO/IEC 25010:2023 defines a product quality model with nine characteristics and subordinate characteristics for specifying, measuring, and evaluating ICT-product quality. A reference model improves vocabulary and omission discovery, but it does not choose stakeholder priorities or replace system context. Domain qualities such as safety, explainability, auditability, sustainability, sovereignty, or fairness may require additional models and qualified authorities.

**Operationalize a concern as a scenario.** Identify the source of a stimulus, the stimulus itself, the relevant environment, the affected system or artifact, the required response, and a response measure. “Under ordinary weekday demand” differs from “during regional failover.” “Detect within 30 seconds” differs from “restore within 30 seconds.” “Ninety-nine percent of eligible screen-reader users complete the workflow in a study” is different evidence from conformance to an accessibility rule.

Use business language first. Protocols and products belong later unless they are genuine constraints. “When an authorized customer requests deletion, all governed copies enter an auditable deletion workflow within one day” expresses responsibility. “Send a Kafka event” selects a mechanism and leaves authority, copies, failure, and evidence unclear.

**Name the measure precisely.** State population, interval, unit, sampling, statistic, threshold, exclusions, and observation point. An average latency hides tail behavior. A monthly availability percentage can hide a complete outage during the only business-critical hour. An error rate without request eligibility, retries, or partial results is ambiguous. Every number carries assumptions and measurement error; precision in notation does not create confidence in the underlying estimate.

Distinguish a hard threshold from an objective or budget. A safety limit may be non-negotiable under named conditions. A service objective is a target used for operation and trade-off decisions. An error budget expresses tolerated unreliability over a window. An aspiration such as “instant” or “seamless” is useful discovery language but not yet an acceptance criterion.

**Test architectural significance.** A scenario is likely a driver when failure threatens a mission, legal duty, safety, trust, material revenue, or irreversible harm; when its solution affects several structures or teams; when late change is costly; when dependencies or uncertainty dominate; or when the architecture must reserve future options. Not every quality requirement is architectural. Changing one form label may matter greatly to users but not require system-wide design.

**Trace from scenario to tactics and evidence.** A driver motivates one or more decisions. Decisions realize tactics: redundancy, resource scheduling, authentication, isolation, indirection, partitioning, monitoring, rollback, or controlled variability. Tactics have preconditions and side effects. Redundancy can improve service continuity but add correlated failure, consistency, cost, and operational complexity. Caching can reduce latency but introduce staleness and invalidation behavior.

Traceability should be bidirectional. Given a driver, reviewers can find decisions, implementation responsibilities, and evidence. Given an expensive mechanism, reviewers can find which scenario justifies it. An untraced mechanism may be accidental complexity; an untraced driver may be an unaddressed risk.

**Evaluate the end-to-end system.** Component throughput does not prove user task completion. Database uptime does not prove a checkout flow is usable. Encryption in transit does not prove authorization or retention. The context from SARCH-003 defines the path whose weakest dependencies, human actions, queues, and policies shape the outcome. Decompose budgets only when composition assumptions are explicit.

**Expose interaction rather than optimize labels independently.** A stricter confidentiality control can add latency and recovery dependencies. Aggressive caching can improve latency and worsen freshness or privacy deletion. Fine-grained services can improve independent change for one team while reducing testability and availability end to end. Quality attributes are not scalar knobs with universally positive direction.

Use scenario pairs and boundary cases. Compare normal and peak, healthy and degraded, authorized and adversarial, hot and cold cache, ordinary deployment and rollback, single-region and failover, experienced and novice user, common and assistive interaction. Contrasts reveal assumptions and tactics more reliably than an isolated adjective.

**Treat evidence by claim type.** Static analysis can support structural rules. Tests can support observed behavior under specified inputs and environments. Load experiments support bounded throughput and latency observations. Fault-injection exercises support behavior under selected faults. Accessibility evaluation requires both applicable conformance checks and user-centered evidence. Threat analysis and penetration testing expose selected weaknesses but do not prove security. Production indicators support current operation under observed conditions, not every future workload.

Record toolchain, version, environment, input model, result, exclusions, date, and reviewer authority. Distinguish verified requirement conformance from validation that the requirement serves stakeholder needs. A beautifully measured wrong scenario is still wrong.

**Maintain a quality-driver register.** Give each scenario a stable identifier, source, owner, consequence, priority rationale, uncertainty, status, related context, decisions, evidence, and review triggers. Preserve rejected or superseded drivers with rationale. Reopen them after incidents, growth, supplier change, architecture change, new regulation, new user population, altered threat, or evidence that invalidates an assumption.

## Definitions and Notation

Represent a quality-attribute scenario as

$$
q=(src,stim,env,art,resp,meas),
$$

where $src$ produces stimulus $stim$ in environment $env$; artifact or system $art$ must produce response $resp$ assessed by $meas$. Let $Q_K$ be the set of known scenarios at review time. The subscript reminds us that stakeholder discovery and scenario elicitation are not provably complete.

For scenario $q$, define architectural significance as a structured judgment rather than a universal formula:

$$
sig(q)=(consequence,reach,irreversibility,uncertainty,optionCost).
$$

Teams may use ordinal scales to support comparison, but aggregation must not allow a low cost estimate to cancel a legal, safety, or rights constraint. The tuple preserves dimensions that a single score would hide.

For a latency objective, let $L_p(W,E)$ be the observed $p$th-percentile end-to-end latency under workload model $W$ and environment $E$. A requirement might state

$$
L_{0.99}(W_{peak},E_{healthy})\le 2\text{ s}.
$$

This predicate is meaningful only if request eligibility, sampling window, clock boundaries, retries, failures, and the models $W_{peak}$ and $E_{healthy}$ are defined. It does not imply behavior under failover or an unmodeled workload.

Let $T:Q_K\rightarrow 2^D$ map scenarios to architecture decisions and $X:D\rightarrow 2^E_v$ map decisions to evidence items. A known scenario has declared response coverage when it has an accountable disposition and relevant evidence plan. As before, coverage over $Q_K$ does not establish that $Q_K$ contains every legitimate concern.

## Mechanisms, Invariants, or Proof Structure

Use this mechanism for each candidate quality driver.

1. **Trace the source:** record stakeholder or mission goal, consequence, authority, and original language.
2. **Frame the context:** name system boundary, lifecycle state, users, dependencies, and operational environment.
3. **Construct the scenario:** fill source, stimulus, environment, artifact, response, and measure.
4. **Challenge the measure:** define population, unit, statistic, observation point, interval, exclusions, and uncertainty.
5. **Test significance:** examine consequence, cross-system reach, irreversibility, uncertainty, and option cost.
6. **Compare conditions:** add normal, boundary, degraded, recovery, adversarial, and change variants as applicable.
7. **Expose interactions:** identify affected functions, qualities, cost, human work, suppliers, and constraints.
8. **Select decisions and tactics:** state mechanisms, assumptions, alternatives, and expected quality response.
9. **Design evidence:** choose analysis, model, test, experiment, exercise, observation, or qualified review appropriate to the claim.
10. **Maintain correspondence:** link scenario, decision, implementation, evidence, residual risk, and reopening triggers.

The governing invariants are contextual measurement, end-to-end scope, explicit units, visible uncertainty, no silent trade-off, claim-specific evidence, decision traceability, accountable acceptance, and lifecycle review.

A scenario tuple is structurally complete if all six fields are meaningful. This is not a proof that the scenario is correct or important. Likewise, satisfying a measured predicate proves only the reported observation under its measurement model. The premise set must include workload, environment, population, instrumentation, statistical method, and exclusions before a result can support an architectural claim.

## Alternatives and Trade-Offs

**Quality taxonomies** provide shared vocabulary and systematic prompts but encourage checklist thinking. **Goal- and scenario-led elicitation** preserves context and consequence but can omit qualities stakeholders do not know to name. Use taxonomies to challenge scenario discovery, not to manufacture equal-priority requirements.

**Qualitative scenarios** work early when evidence is scarce and can reveal important mechanisms. They remain open to incompatible interpretations. **Quantified scenarios** support evaluation and budgets but can create false precision or optimize the wrong proxy. Quantify what decisions require, publish uncertainty, and retain the qualitative purpose.

**Utility trees and facilitated workshops** efficiently expose priorities and conflicts among represented participants. They inherit attendance, framing, facilitation, and power biases. Supplement them with interviews, observation, incident and complaint evidence, domain analysis, and representation of absent affected parties.

**Synthetic tests** are reproducible and safe but may use unrealistic workload, faults, data, or human behavior. **Production observation** is realistic for encountered conditions but exposes users to risk, suffers confounding, and cannot ethically explore every failure. Combine bounded preproduction evidence, guarded rollout, telemetry, and exercises appropriate to consequence.

**Local budgets** support team ownership and diagnosis. They can falsely assume independent or additive behavior. **End-to-end objectives** represent stakeholder outcomes but are harder to attribute and control. Keep the outcome primary and decompose only with explicit composition models and residual margin.

## Failure Modes and Misconceptions

- **“Quality means no defects.”** Quality attributes describe distinct stakeholder-relevant properties; defect absence is neither fully observable nor sufficient.
- **“The taxonomy is the requirement set.”** A reference model supplies vocabulary, not priorities, thresholds, domain obligations, or completeness.
- **“Security is nonfunctional.”** Security responses can be observable system behavior and can determine functional authorization and recovery.
- **“Higher is always better.”** More isolation, durability, consistency, configurability, or availability can increase latency, cost, complexity, and operational risk.
- **“A percentile needs only a number.”** It needs population, workload, window, eligibility, observation point, and treatment of errors and retries.
- **“Average latency represents users.”** Averages can hide tails, cohorts, cold paths, and complete failure.
- **“Component SLA equals service quality.”** End-to-end outcomes include dependencies, clients, humans, data correctness, and recovery.
- **“A tactic guarantees an attribute.”** Tactics influence responses under assumptions and introduce other consequences.
- **“A test pass proves the quality.”** It supports a bounded claim for specified conditions and instrumentation.
- **“Every important requirement changes architecture.”** Architectural significance depends on reach, consequence, reversibility, uncertainty, and decision cost.
- **“One scenario per attribute is enough.”** Normal, peak, degraded, adversarial, recovery, and change conditions can require different responses.
- **“Scores make prioritization objective.”** Scales encode judgments and can conceal non-compensable duties or unevenly distributed harm.
- **“Maintainability is developer preference.”** Change lead time, affected scope, verification effort, deployability, and cognitive demand can affect mission capability.
- **“Quality work ends at design.”** Incidents, growth, new populations, threats, suppliers, and measurements invalidate assumptions.

## Worked Examples

### Example 1

**Question:** Convert “search must be fast” into an architectural driver.

**Reasoning:** Identify a shopper as source, submission of a syntactically valid query as stimulus, weekday peak as environment, the end-to-end search capability as artifact, useful ranked results or an explicit rejection as response, and a measure such as $L_{0.99}\le 800$ ms under a declared workload. Define eligible queries, dataset scale, cache state, dependency health, errors, and observation points. Then ask whether meeting the threshold affects indexing, caching, request budgets, data freshness, and deployment topology.

**Conclusion:** The six-part scenario turns an adjective into a contextual obligation and exposes architecture consequences.

### Example 2

**Question:** Does 99.9% monthly API availability satisfy a payroll requirement?

**Reasoning:** The percentage allows 43.2 minutes of unavailability in a 30-day month because $30\times24\times60\times0.001=43.2$, but timing matters more than the aggregate. Forty minutes during payroll cutoff can prevent salaries even if the monthly target passes. Specify the critical submission window, accepted-work durability, dependency scope, degraded manual path, recovery point, and confirmation behavior. Treat the monthly percentage as one measure, not the mission outcome.

**Conclusion:** Aggregate availability without business environment and consequence can be technically satisfied while the system fails its purpose.

### Example 3

**Question:** Which measure distinguishes latency improvement from hidden failure?

**Reasoning:** A service can drop slow requests and report lower latency for successes. Define the request population before filtering, publish success and rejection rates, include timeouts in outcome accounting, and measure end-to-end latency for eligible successful requests alongside the fraction receiving a correct terminal result. Compare cohort and tail distributions rather than one mean.

**Conclusion:** Measurement semantics must prevent the system from “improving” a quality by excluding harmed outcomes.

### Example 4

**Question:** Is “encrypt all data” a sufficient security driver?

**Reasoning:** Identify the asset, adversary or misuse, state, boundary, authorized response, and evidence. For a stolen backup scenario, the system should prevent recovery of customer records without separately controlled keys, detect unauthorized key use, and support revocation under specified recovery constraints. Encryption at rest is a tactic. It does not define authorization, key custody, metadata exposure, deletion, availability, or insider risk.

**Conclusion:** A security mechanism is not a scenario and cannot replace threat, context, response, and measure.

### Example 5

**Question:** A team wants independent weekly deployment. Is that modifiability or deployability?

**Reasoning:** The motivating scenario may be: one product team changes a pricing rule during ordinary operation, validates affected behavior, and deploys without coordinating releases of unrelated capabilities within one working day. This crosses modifiability, testability, deployability, and organizational ownership. Measure elapsed time, affected modules and teams, regression scope, rollback, and failure rate. A service split is one possible tactic, not the requirement.

**Conclusion:** Real change scenarios span named qualities and are better drivers than categorical labels.

### Example 6

**Question:** Does adding three replicas improve availability?

**Reasoning:** Replicas can tolerate independent instance failure, but shared region, credentials, deployment, configuration, dependency, or corrupt data can fail all copies. Replication may also delay consistency or make recovery harder. Define fault assumptions, detection, failover time, state recovery, capacity during failure, and correlated-failure evidence. Compare the required response with the replica topology.

**Conclusion:** Redundancy is a tactic whose value depends on failure model and operational evidence, not replica count alone.

### Example 7

**Question:** How can caching create a quality conflict?

**Reasoning:** A cache may reduce search latency and backend load. It can also serve stale eligibility, retain deleted personal data, complicate authorization changes, and create cold-start spikes. Specify freshness bounds, invalidation authority, sensitive-data rules, miss behavior, and failure mode. Evaluate the latency scenario together with correctness, privacy, availability, and operability scenarios.

**Conclusion:** Tactics influence several qualities; an isolated performance win is not an architecture verdict.

### Example 8

**Question:** A supplier reports 99.99% availability. What can the architecture claim?

**Reasoning:** Inspect the supplier’s service definition, regions, exclusions, measurement window, client obligations, maintenance, rate limits, data correctness, and remedies. Map every other dependency and the integration’s retry, timeout, fallback, and recovery behavior. Locally observed end-to-end evidence may support a bounded service claim. The supplier figure alone cannot be copied into a user guarantee.

**Conclusion:** External evidence must be scoped and composed with the complete context.

### Example 9

**Question:** How should accessibility become an architectural driver rather than a late UI check?

**Reasoning:** Define affected users and assistive interactions, critical tasks, device and network environments, completion behavior, error recovery, time constraints, and evaluation methods. Architectural implications may include semantic information models, consistent navigation, notification channels, session timing, document generation, identity flows, and third-party component choice. Combine applicable rule-based checks with expert and user-centered validation; neither alone proves universal usability.

**Conclusion:** Accessibility scenarios can shape cross-system choices and must be traced from affected people to evidence.

### Example 10

**Question:** How should quality drivers be handled for a remote infusion-monitoring system?

**Reasoning:** Separate monitoring from clinical decision authority. Construct scenarios for delayed or missing readings, incorrect identity, alarm delivery, network partition, sensor replacement, override, audit, recovery, and retirement. Define units, populations, timing, false-positive and false-negative consequences, degraded operation, and responsible humans. Automated checks and simulations support only specified models. No external clinical, safety, regulatory, cybersecurity, human-factors, or practitioner review is claimed; named qualified authorities must validate hazards, clinical workflow, thresholds, evidence, independence, residual risk, and release authority.

**Conclusion:** High-consequence quality drivers require precise scenarios, explicit authority, diverse evidence, and qualified human judgment.

## Cross-Program Connections

- [Software Engineering Methods & Evolution](../../10-software-engineering-methods-and-evolution/ROADMAP.md) develops requirements practices, stakeholder validation, lifecycle feedback, and change governance.
- [Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) locates invariants and change boundaries affected by quality scenarios.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) designs verification and validation evidence without equating tests with universal correctness.
- [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) operationalizes service objectives, error budgets, recovery, deployment, and production feedback.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) derives threat, trust, authorization, and assurance scenarios.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects qualities to mission, lifecycle, human, physical, and assurance concerns.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies models for partial failure, consistency, replication, and end-to-end behavior.

## References

1. ISO/IEC. [ISO/IEC 25010:2023, Systems and software engineering—Systems and software Quality Requirements and Evaluation (SQuaRE)—Product quality model](https://www.iso.org/standard/78176.html), edition 2, November 2023. Current product-quality reference model with nine characteristics and lifecycle uses; consulted 2026-09-05.
2. Software Engineering Institute. [Quality Attribute Workshop Collection](https://www.sei.cmu.edu/library/quality-attribute-workshop-collection/), Carnegie Mellon University, 2016. Official collection describing quality attributes derived from mission/business goals and stakeholder scenario generation, prioritization, and refinement; consulted 2026-09-05.
3. Mario R. Barbacci et al. [Quality Attribute Workshops (QAWs), Third Edition](https://www.sei.cmu.edu/library/quality-attribute-workshops-qaws-third-edition/), CMU/SEI-2003-TR-016, 2003. Quality-attribute scenario elicitation and refinement method.
4. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*, fourth edition, Addison-Wesley, 2021. Quality-attribute scenarios, tactics, architecture drivers, business goals, and evaluation.
5. Paul Clements et al. *Documenting Software Architectures: Views and Beyond*, second edition, Addison-Wesley, 2010. Documentation of quality properties, views, interfaces, rationale, and evidence.
6. Rick Kazman, Mark Klein, and Paul Clements. [ATAM: Method for Architecture Evaluation](https://www.sei.cmu.edu/library/atam-method-for-architecture-evaluation/), CMU/SEI-2000-TR-004, 2000. Scenarios, utility trees, risks, sensitivity points, and trade-offs.
7. ISO/IEC/IEEE. [ISO/IEC/IEEE 42010:2022, Software, systems and enterprise—Architecture description](https://www.iso.org/standard/74393.html), edition 2, November 2022. Architecture-description concepts connecting stakeholders, concerns, viewpoints, views, and model kinds; consulted 2026-09-05.
8. John D. Musa. *Software Reliability Engineering: More Reliable Software Faster and Cheaper*, second edition, AuthorHouse, 2004. Operational profiles, measurement context, reliability objectives, and test allocation.
9. Nicole Forsgren, Jez Humble, and Gene Kim. *Accelerate: The Science of Lean Software and DevOps*, IT Revolution, 2018. Empirical treatment of delivery performance, stability, and organizational capabilities, with claims bounded to the reported research.
10. World Wide Web Consortium. [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/), W3C Recommendation, 5 October 2023. Current normative web-accessibility success criteria and conformance requirements; consulted 2026-09-05.

## Exercises

### Exercise 1

Explain why “scalable, secure, and maintainable” is not yet an architecture-driver set. For each term, state the missing scenario information.

### Exercise 2

Construct and analyze a quality-attribute scenario for a ticket-sale peak. Define population, workload, percentile, correctness, failure treatment, observation point, and architectural significance.

### Exercise 3

Diagnose a dashboard that reports 120 ms average latency, 99.99% database uptime, 100% automated-test pass rate, and zero known security incidents as proof that the architecture meets all quality requirements.

### Exercise 4

Compare synchronous validation with deferred asynchronous validation for a bulk data-import capability. Analyze performance, availability, correctness, operability, security, user experience, and change implications.

### Exercise 5

Define a quality-driver and evidence process for an unfamiliar regional wildfire-alert platform. Separate automated evidence, operational exercises, stakeholder validation, qualified authority, and conditions that block readiness claims.

## Answers to the Exercises

### Answer 1

The labels provide categories but no source, stimulus, environment, artifact, response, or measure. For scalability, specify what demand changes—concurrent sessions, events per second, stored objects, tenants, or geography—over what interval, and the required response and resource or cost bound. For security, identify asset, threat or misuse, trust context, permitted behavior, detection/prevention/recovery response, and assurance evidence. For maintainability, name a representative change, team and skill assumptions, affected scope, required analysis/test/deploy response, elapsed-time or coordination measure, and acceptable risk.

An acceptable answer can choose different concrete scenarios, but each must connect a stakeholder purpose to observable behavior and define enough context to evaluate architecture. Merely attaching numbers to the adjectives is insufficient if the population, environment, and consequence remain unknown.

### Answer 2

One scenario is: during the announced opening minute for a stadium event, registered buyers submit eligible seat requests to the end-to-end sale capability; under a workload model of 80,000 arrivals in five minutes with a declared burst distribution, the system returns confirmed reservation, sold-out rejection, or an explicit bounded pending state for 99% of accepted requests within two seconds and never confirms the same seat twice.

Define whether queue-wait time is included, how bots and invalid requests are classified, how retries correlate, where clocks start and stop, how abandoned clients count, and how payment uncertainty affects terminal state. Observe at the user edge and authoritative reservation ledger, publishing latency distribution, admission/rejection, correctness, and unknown outcomes. The scenario is architectural because it affects admission control, reservation authority, concurrency, idempotency, capacity, dependency budgets, degradation, and recovery. A different threshold may be valid, but it needs stakeholder consequence and workload evidence rather than arbitrary precision.

### Answer 3

Average latency can hide tails, failed requests, regions, cohorts, cold paths, and critical periods. Database uptime is one dependency measure, not end-to-end availability, accepted-work durability, or correctness. Automated-test passes support only the exercised code and environment; they do not establish scenario validity, production topology, usability, recovery, or absence of untested defects. No known incidents can mean effective prevention or weak detection, reporting, and exposure.

Reconstruct a dated quality-driver register from stakeholder goals and context. For each scenario, define population, environment, response, measure, authority, and consequence. Add end-to-end latency and outcome distributions, business-window availability, dependency and recovery evidence, change scenarios, accessibility validation, threat analysis, control verification, incident detection, fault exercises, and production observation as applicable. State uncertainty and evidence limits. The original dashboard can contribute evidence but cannot prove “all quality requirements.”

### Answer 4

Synchronous validation gives an immediate accept/reject result and can simplify user understanding, but couples import latency and availability to every validator and may hold scarce resources. Deferred validation can absorb bursts, isolate workers, retry transient faults, and expose progress, but introduces queued state, versioned validation rules, cancellation, duplicate work, expiry, notification, authorization after delay, and reconciliation. It may disappoint users if “uploaded” is mistaken for “accepted.”

Define correctness authority and immutable import identity in both designs. Compare admission latency, total completion time, queue capacity, dependency failure, partial results, resource isolation, sensitive-data retention, operator visibility, replay safety, rule rollout, rollback, and user recovery. A hybrid can synchronously validate syntax and authorization, then asynchronously perform expensive semantic validation. That is acceptable only if states and guarantees are explicit. Selection depends on quality scenarios and consequences, not a universal preference for asynchronous architecture.

### Answer 5

Frame the system boundary and distinguish sensor/forecast ingestion, recommendation, legal alert authorization, channel delivery, public receipt, and emergency response. Construct scenarios for rapidly changing fire boundaries, sensor loss, conflicting models, telecom partition, overload, stale maps, false positives, missed alerts, multilingual and accessible communication, malicious messages, operator override, evacuation, recovery, audit, and retirement. Define geography, population, time bounds, uncertainty, false-positive/negative consequences, degraded behavior, and accountable authorities.

Automated evidence can check schema and unit invariants, provenance, signatures, access, duplicate suppression, model execution for specified cases, trace links, configuration, and evidence freshness. Load and fault experiments support bounded technical claims; field and tabletop exercises support selected operational paths. They do not establish fire-model validity, community comprehension, lawful issuance, accessibility for every resident, or acceptable residual risk. No external wildfire, emergency-management, safety, accessibility, regulatory, cybersecurity, or practitioner review is claimed. Named qualified authorities must validate domain models, thresholds, human decision allocation, communication, exercises, independent assurance, release, and residual risk. Missing provenance, unclear alert authority, untested degraded channels, inaccessible critical flows, or unresolved high-severity hazards block the corresponding readiness claim.
