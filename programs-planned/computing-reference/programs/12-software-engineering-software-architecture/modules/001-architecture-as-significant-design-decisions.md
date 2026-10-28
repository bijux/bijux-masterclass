---
module_id: SARCH-001
program: Software Engineering: Software Architecture
level: 1
module_number: 1
title: Architecture as Significant Design Decisions
status: complete
last_verified: 2026-08-29
---

# Architecture as Significant Design Decisions

## One-Page Review

### Governing question

Which design decisions are architecturally significant, and how can engineers connect those decisions to stakeholder concerns, system structures, evidence, trade-offs, and future change?

### Essential definitions

- **architecture** is the fundamental organization and properties of a system in its environment, embodied in elements, relationships, and principles governing design and evolution.
- An **architectural decision** chooses or constrains a system-wide structure, responsibility, interaction, technology-independent mechanism, deployment, data authority, or evolution rule.
- A decision is **significant** when changing it later has high cost, broad consequences, material quality/risk effects, difficult coordination, or irreversible commitments.
- A **driver** is a stakeholder concern, required capability, quality-attribute scenario, constraint, assumption, risk, business/mission goal, or lifecycle need that shapes architecture.
- A **quality attribute** is a measurable/testable property by which stakeholders judge a system, such as availability, performance, security, modifiability, interoperability, usability, accessibility, safety, or operability.
- A **view** expresses an architecture from a defined viewpoint to address particular stakeholder concerns; no single diagram is “the architecture.”
- An **architecture description** is a work product used to express architecture; the deployed system can differ from its description.
- A **trade-off** occurs when a decision improves one valued outcome or scenario while worsening another, increasing cost, or consuming optionality.
- **architectural risk** is uncertainty about whether decisions and structures will satisfy important concerns under relevant conditions.
- **technical debt** is not every compromise; it is a contingent future burden created by a decision, often accepted for a reason and requiring management.

### Central model, mechanism, or theorem

Represent a decision as

\[
d=(context,drivers,options,choice,rationale,consequences,evidence,triggers).
\]

Its significance is multi-dimensional rather than a single universal score:

\[
Sig(d)=f(impact,reach,risk,reversal\ cost,time\ horizon,coordination,uncertainty).
\]

Architecture work traces **goal/concern → scenario/constraint → decision → structure → evidence → consequence**. A decision is justified only relative to explicit drivers and competing options. A structural diagram without decisions and rationale is incomplete; a decision record without correspondence to the implemented and operated system is stale intent.

### Critical invariants

- Name the entity/system boundary, environment, stakeholders, concerns, lifecycle stage, and decision authority.
- Express qualities as scenarios with stimulus, context, affected artifact, response, and measurable response—not adjectives alone.
- Separate requirements/constraints from chosen mechanisms and vendor products.
- Compare plausible alternatives, including defer, simplify, buy, reuse, and retire; do not manufacture a foregone comparison.
- State assumptions and uncertainty; establish evidence proportional to consequence before commitment.
- Record consequences, rejected options, residual risks, ownership, status, and revisit/expiry triggers.
- Keep decision records, architecture views, code, configuration, deployment, data and operations mutually traceable.
- Preserve reversibility where uncertainty is high; spend irreversible commitment only where drivers justify it.
- Evaluate interactions among decisions and quality attributes, not decisions in isolation.
- Treat architecture as evolving; govern drift, exceptions, migrations and retirement explicitly.

### Common failures

Common failures include calling every design choice architecture; equating architecture with boxes-and-arrows; choosing products before drivers; writing “scalable” or “secure” without scenarios; treating mandated technology as proof of suitability; documenting only the selected option; using a numerical score as an automatic decision; confusing current structure with intended structure; ignoring data, deployment, build, operational, organizational and retirement views; centralizing all choices with an architect; allowing “team autonomy” to hide cross-system risks; recording decisions after the fact without evidence; and never revisiting assumptions after the environment changes.

### Compact example

“Use asynchronous messages” is not yet a justified architecture. Driver: order intake must accept a burst of 10,000 requests/minute for five minutes while fulfillment is degraded, without losing accepted orders, and recover backlog within 30 minutes. Options include synchronous throttling, durable queue, or admission plus batch. A durable queue improves decoupling and load leveling but introduces duplicate delivery, ordering, lag, broker operation and reconciliation. The decision must define ownership, idempotency, durability, observability, capacity evidence, failure policy and revisit trigger—not merely name a broker.

### Connections

[SDDM-001](../../09-software-engineering-software-design-and-domain-modeling/modules/001-distinguishing-the-problem-domain-from-the-solution-domain.md) separates problem and solution models. [SEPAT-001](../../11-software-engineering-patterns/modules/001-recurring-problems-context-forces-and-consequences.md) frames recurring solutions through context, forces and consequences. [SEME-001](../../10-software-engineering-methods-and-evolution/modules/001-software-products-projects-services-and-platforms.md) supplies lifecycle ownership. The successor [SARCH-002](../ROADMAP.md) deepens stakeholders and concerns.

## Governing Question

How do engineers identify decisions whose consequences shape a software-intensive system beyond one local implementation, make those decisions with honest evidence, and keep the realized architecture aligned as the system evolves?

Architecture is neither a job title nor an early project phase. Every system has architecture because it has elements, relationships, environment and evolution constraints, whether deliberately chosen or accidentally accumulated. Architecture practice makes the consequential parts explicit enough to reason about, evaluate, communicate, implement and change.

## Why This Matters

Local code decisions can often be changed by one developer with narrow tests. Architectural decisions couple many changes: authority over customer data, isolation model, consistency boundary, deployment unit, interaction style, runtime platform, identity trust, recovery topology, extension mechanism, or compatibility policy. Mistakes surface late because happy-path function can work while latency, failure, safety, security, operability or change cost remains hidden.

Early decisions have leverage but early knowledge is weak. The architect’s task is therefore not maximal upfront certainty. It is to expose drivers and uncertainty, decide what must be fixed now, defer what can remain reversible, create evidence, and install feedback that reveals when assumptions fail.

Architecture also coordinates people. Team boundaries, ownership, funding, suppliers, review authority and operational response interact with technical boundaries. A technically elegant split with shared releases and unclear data ownership may not produce independent change. A simple monolith with disciplined modules and one team can be the better architecture for its context.

## Prerequisites and Retrieval

Retrieve these ideas before proceeding:

- system, environment, boundary, component, connector, interface, dependency, state and invariant;
- stakeholder, concern, requirement, constraint, assumption, risk and evidence;
- functional behavior versus quality attributes;
- latency percentiles, throughput, availability, recovery, confidentiality, integrity and compatibility;
- cohesion, coupling, information hiding and change propagation;
- deployment, data ownership, runtime failure, versioning and operations;
- opportunity cost, reversibility and total lifecycle cost.

You should be able to distinguish “customers submit orders” from “during a regional dependency outage, accepted orders are not lost and service recovers within a stated bound,” and explain why the latter is more likely to shape system structure.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish architecture, architecture descriptions, detailed design and implementation;
2. identify significant decisions using consequence, reach, risk, reversibility, coordination and uncertainty;
3. derive architectural drivers from goals, stakeholders, scenarios, constraints, assumptions and lifecycle needs;
4. trace one decision through structural consequences and evidence;
5. compare options without starting from a preferred technology;
6. expose trade-offs, residual risks and interactions among quality attributes;
7. document decision context, rationale, status, consequences and revisit triggers;
8. select views and evidence appropriate to stakeholder concerns;
9. diagnose drift between intended, described, implemented, deployed and operated architectures;
10. design a review path for unfamiliar high-consequence architecture without claiming automated approval.

## Core Exposition

### Architecture exists independently of its documentation

A system’s architecture is embodied in what it is and how it behaves: elements, relationships, externally relevant properties, deployment, data and principles of evolution. An architecture description is evidence—a set of views, models, decisions and correspondence claims used for a purpose. A diagram can be wrong while the system still runs; the absence of a diagram does not mean absence of architecture.

Distinguish at least four states:

- **intended architecture:** decisions and structures people mean to realize;
- **described architecture:** what records and models claim;
- **implemented architecture:** source, schemas, dependencies and configuration;
- **operational architecture:** deployed topology, runtime interactions, data movement and human procedures.

These can diverge. Review correspondence with repository dependency analysis, deployment inventory, runtime traces, configuration, data lineage, incident evidence and interviews. No one artifact is authoritative for every concern.

### Find significance through consequences

Not every choice needs architecture governance. Naming a local variable rarely constrains other teams or system qualities. Choosing the system of record for identity, synchronous versus asynchronous integration, single- versus multi-tenant isolation, or a public compatibility policy can shape years of work.

Use several signals:

- **reach:** number and criticality of components, teams, users, data domains and suppliers affected;
- **quality impact:** influence on measurable availability, latency, security, safety, modifiability or other scenarios;
- **reversal cost:** migration, downtime, dual running, data conversion, retraining, contracts and opportunity cost;
- **commitment horizon:** how long consequences persist;
- **coordination:** number of independent authorities that must agree/change;
- **risk/uncertainty:** consequence severity, likelihood uncertainty and evidence gaps;
- **precedent:** whether the choice establishes a reusable rule or constraint;
- **optionality:** future choices enabled or foreclosed.

These are prompts, not a formula that declares architecture. A low-reach cryptographic random-number choice can be security critical; a broad formatting convention may be easy to reverse. Judgment remains tied to concrete concerns.

### Derive drivers before mechanisms

Start from business/mission goals and system context. Identify stakeholders—including operators, maintainers, security/safety reviewers, regulators, suppliers and people affected without direct use. Translate concerns into capabilities, quality scenarios, constraints, assumptions and risks.

A quality-attribute scenario names source of stimulus, stimulus, environment, affected artifact, response and response measure. For example: “During normal peak load, an authenticated customer submits a read request; the order service returns a correct response within 300 ms at the 99th percentile across a defined five-minute window, excluding no successful requests.” The exact threshold needs evidence and stakeholder agreement; the structure makes ambiguity visible.

Constraints narrow options: mandated protocol, existing contract, residency, hardware, deadline, skills, budget or certification. Challenge whether a claimed constraint is truly fixed, for how long, and by whom. An assumption is not a constraint; attach validation and expiry. A risk is uncertainty with consequence, not merely a negative statement.

### Decide at the appropriate abstraction level

An architectural decision should be specific enough to constrain meaningful design while avoiding needless implementation detail. “Use security” is empty. “All external requests terminate mutual authentication at an independently administered edge, with workload identity propagated as signed, short-lived claims and authorization owned by domain services” is structural. The brand of certificate manager may remain replaceable unless it changes lifecycle or trust properties.

Architecture is sometimes a **negative space**: forbid direct writes to another domain’s data; require backward-compatible events; isolate safety control from analytics; prevent a deployment tool from becoming business authority. Principles matter when they produce testable constraints and exception handling.

Decide late when alternatives remain cheap and uncertainty high. Decide early when downstream work needs stability or evidence takes time. Build an architectural runway only for known risks; speculative infrastructure consumes options rather than preserving them.

### Compare options and consequences

For each real option state:

1. how it satisfies each driver and scenario;
2. mechanisms and structures it requires;
3. failure modes and operational burden;
4. security, privacy, safety and compliance consequences;
5. delivery, migration, compatibility and retirement cost;
6. organizational ownership and skills;
7. evidence available and evidence still needed;
8. reversibility and future options;
9. residual risks and risk owner.

Avoid weighted scorecards that hide non-compensable constraints. A high average cannot offset violation of a safety requirement. Use matrices to expose reasoning, then deliberate thresholds, uncertainty and interactions. Document why credible options lost; straw alternatives weaken future review.

### Structures are the consequences of decisions

Architecture appears through multiple structures:

- **module/code:** decomposition, dependencies, ownership and build boundaries;
- **component-and-connector/runtime:** processes, services, queues, calls, protocols and failure propagation;
- **allocation/deployment:** mapping to hosts, zones, regions, devices and organizations;
- **data/information:** authority, schemas, flows, retention, consistency and lineage;
- **development/operations:** repositories, pipelines, observability, support and change authority.

One decision can change several structures. Database-per-service affects code dependencies, runtime transactions, deployment, ownership, analytics, recovery and migrations. One boxes-and-arrows view cannot communicate all of these with stable semantics.

### Quality attributes interact through tactics

Architectural mechanisms or tactics influence qualities. Replication can improve availability/read capacity while increasing consistency, cost and operational complexity. Caching lowers latency/load while creating staleness and invalidation risk. Encryption improves confidentiality while adding key management, latency and recovery obligations. Asynchronous messaging decouples time and absorbs bursts while introducing duplicates, lag and harder tracing.

Ask for causal chain: driver requires response; tactic changes system behavior; structure realizes tactic; measure evaluates response. “Microservices improve scalability” skips workload, partitionability, bottleneck, deployment, data and operational evidence. A modular monolith may scale adequately with less distributed failure.

Quality goals can be compatible in one scenario and conflicting in another. Security and usability, consistency and availability, latency and durability, modifiability and performance all need scenario-specific analysis rather than slogans.

### Evidence reduces uncertainty, not responsibility

Choose evidence proportional to stakes and timing:

- prototype/spike to test uncertain integration or performance mechanism;
- analytical models for capacity, reliability, queues, cost or failure propagation;
- threat/hazard analysis for adversarial or safety consequences;
- load, fault, recovery and compatibility experiments;
- architecture evaluation workshops and scenario walkthroughs;
- dependency, schema and deployment conformance checks;
- observability and incident/postmortem evidence from operation;
- formal model/proof for sharply defined critical properties;
- supplier documentation, contracts, attestations and exit tests.

A benchmark is evidence only for its hardware, workload, data, versions and configuration. A prototype can show feasibility, not production fitness. A proof can establish a modeled property, not that the model captures stakeholder intent. Record evidence scope, date, owner and invalidation trigger.

### Record decisions as living governance

A useful decision record contains title, status, context, drivers, considered options, decision, rationale, consequences, evidence, owners and revisit triggers. Status might be proposed, accepted, superseded, deprecated or rejected. Immutability of historical records preserves rationale; superseding records explain change.

Decision records complement views. The record explains why; views show structures; tests/fitness functions check selected constraints; operational evidence shows realized consequences. Link them through stable identifiers where practical. Do not turn a lightweight record into an approval document for every code choice.

Revisit on triggers: assumption invalidated, threshold breached, scale or threat changes, supplier/version lifecycle, new regulation, repeated exceptions, incident pattern, or cheaper migration window. Calendar review alone can become theater; event-driven review focuses attention.

### Architecture is socio-technical and evolutionary

Technical boundaries require ownership and coordination. If two “independent” services share a database, release train and on-call team, they may not deliver independent change. Conversely, organizational separation cannot erase runtime/data coupling. Architecture decision authority should sit near knowledge and consequences, with federated guardrails for cross-boundary risks.

Architecture evolves through normal changes. Drift is divergence from intended constraints; erosion is accumulated degradation of qualities or coherence. Some drift is evidence that the intended architecture is wrong. Classify it: defect to repair, accepted exception with expiry, or signal to update the decision. Enforcing obsolete diagrams is not governance.

Migration is part of a decision, not an afterthought. Include coexistence, data reconciliation, routing, observability, rollback, consumer change, decommissioning and proof of retirement. A target architecture without a credible transition can be infeasible.

### A small executable reach analysis

The following toy graph computes transitive structural reach for two proposed changes. Reach is one significance signal, never an automatic architecture decision.

<!-- bijux-verify: {"id":"sarch-001-decision-reach","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"identity-boundary direct=2 transitive=6 nodes=analytics,audit,checkout,customer-data,gateway,identity\nlog-format direct=1 transitive=1 nodes=log-shipper\n","stderr":""}} -->
```python
dependencies = {
    "gateway": {"identity", "checkout"},
    "identity": {"audit", "customer-data"},
    "checkout": {"customer-data"},
    "customer-data": {"analytics"},
    "audit": set(),
    "analytics": set(),
    "log-shipper": set(),
}

decisions = {
    "identity-boundary": {"gateway", "identity"},
    "log-format": {"log-shipper"},
}

def reachable(starts):
    seen = set()
    pending = list(starts)
    while pending:
        node = pending.pop()
        if node in seen:
            continue
        seen.add(node)
        pending.extend(dependencies[node] - seen)
    return seen

for name, direct in decisions.items():
    affected = reachable(direct)
    print(
        f"{name} direct={len(direct)} transitive={len(affected)} "
        f"nodes={','.join(sorted(affected))}"
    )
```

The run proves reachability only in this declared finite graph. Edge direction, missing runtime/data/team dependencies, node criticality, quality effects, reversal cost, threat/safety consequences and organizational authority are not validated. A one-node decision can still be significant.

## Definitions and Notation

Let entity of interest be (E) in environment (Env), stakeholders (S), concerns (C), drivers (G), decisions (D), structures (R), evidence (V), and observed operation (O). Architecture description (AD) expresses selected concerns through views/models; it is not identical to architecture (A(E)).

Decision (d=(c,g,o,x,r,k,v,t)) contains context (c), drivers (g), options (o), choice (x), rationale (r), consequences (k), evidence (v), and revisit triggers (t). `direct(d)` names immediately affected elements; (reach(d)) is transitive closure over a declared relation. A correspondence claim links description elements to other descriptions or realized elements. Residual risk remains after treatment and requires an owner.

Use MUST only for verified non-negotiable constraints, SHOULD for defaults with accountable exceptions, and MAY for permitted variation when those terms are explicitly governed; capitalization alone does not create authority.

## Mechanisms, Invariants, or Proof Structure

1. Name entity, environment, lifecycle stage, stakeholders, concerns and authority.
2. Derive capabilities, quality scenarios, constraints, assumptions and risks from goals.
3. Identify decisions with high reach, quality/risk consequence, reversal cost, coordination or uncertainty.
4. Preserve options until evidence or downstream dependency justifies commitment.
5. Compare credible alternatives against scenarios, thresholds, costs, failures and lifecycle consequences.
6. Select a decision and state causal rationale, not merely preference or popularity.
7. Realize it in explicit module, runtime, data, deployment and organizational structures.
8. Define verifiable constraints, tests, experiments, models and operational measures.
9. Record consequences, residual risks, owner, status, expiry and revisit triggers.
10. Validate correspondence among decisions, views, code, configuration, deployment and operation.
11. Govern exceptions and drift as evidence; repair or supersede deliberately.
12. Plan migration and retirement, then confirm obsolete structures and obligations are removed.

Review claims in three layers: **structural conformance** (does realization satisfy declared constraints?), **quality evidence** (do scenarios meet measures under stated conditions?), and **fitness of intent** (do drivers reflect stakeholder/mission reality?). Automation can strongly support the first, partially support the second, and cannot independently authorize the third.

## Alternatives and Trade-Offs

**Big design upfront** can expose integration and safety risks before irreversible work; it can overcommit under uncertainty. **Emergent architecture** learns from delivery; without intentional boundaries it can accumulate expensive coupling.

**Central architecture board** offers cross-system coherence and scarce expertise; it can become a context-poor queue. **Federated authority** places decisions near evidence; it needs shared invariants, escalation and transparent cross-boundary review.

**Standardization** reduces variation, integration and support cost; it can freeze obsolete choices or erase valid context. **Local autonomy** improves fit and ownership; it can multiply incompatibility and operational burden.

**Single integrated system** minimizes distributed failure/coordination and can preserve transactions; it can increase deployment/change coupling. **Distributed services** isolate some scaling/failure/ownership concerns; they introduce network, data consistency and operations complexity.

**Build** maximizes fit/control at lifecycle cost; **buy** accelerates capability while adding supplier, integration, data and exit constraints; **reuse/platform** amortizes common mechanisms while imposing shared evolution.

**Quantitative scoring** makes assumptions comparable; false precision and compensating averages can hide mandatory constraints. **Qualitative deliberation** captures nuance but can conceal bias. Combine transparent evidence, thresholds, uncertainty ranges and accountable judgment.

## Failure Modes and Misconceptions

- **“Architecture is the diagram.”** Diagram is one description under a viewpoint.
- **“Architecture is the technology stack.”** Products realize decisions; names do not explain drivers or consequences.
- **“Only architects make architecture.”** Teams make consequential decisions; authority must match scope and risk.
- **“Every decision is architectural.”** Governance cost should target significance.
- **“Significance equals broad reach.”** Narrow safety/security decisions can dominate consequence.
- **“Quality attributes are adjectives.”** They need contextual, measurable scenarios.
- **“Constraints cannot be questioned.”** Identify source, authority, duration and escape.
- **“A pattern proves suitability.”** Context and forces determine consequences.
- **“Microservices are more scalable.”** Workload, partition, state and operation decide.
- **“The highest score wins.”** Thresholds, uncertainty and non-compensable risks matter.
- **“A prototype proves production readiness.”** It establishes scoped feasibility.
- **“An ADR is governance.”** Records require realization, evidence and revisit.
- **“Architecture must never drift.”** Drift can reveal obsolete intent.
- **“Migration is implementation detail.”** Coexistence and data/consumer transition often dominate risk.
- **“Formal proof makes the architecture safe.”** Model validity and real-world authorization remain.

## Worked Examples

### Example 1

**Situation.** Team debates whether a variable should be `userId` or `customerId`.

**Reasoning.** Locally this may be naming, but if the term defines identity across public contracts, data ownership and compliance, it becomes significant. Ask reach, semantic authority and migration cost rather than label by artifact size.

**Conclusion.** Significance comes from consequences, not code granularity.

### Example 2

**Situation.** Requirement says “the checkout must be highly available.”

**Reasoning.** Identify stimulus/environment/measure: loss of one zone during peak traffic; accepted purchases remain durable; 99.9% requests complete within a defined latency; recovery within five minutes. Only then compare redundancy, failover, queueing and degraded modes.

**Conclusion.** Concrete scenarios transform slogans into drivers.

### Example 3

**Situation.** Organization mandates a cloud database, so team records “use vendor X.”

**Reasoning.** Capture constraint authority/duration plus decisions still open: data model, tenancy, consistency, encryption, residency, backup/recovery, capacity, access, portability and exit. Verify whether mandate covers service or specific configuration.

**Conclusion.** A constraint narrows architecture; it does not complete it.

### Example 4

**Situation.** Architects propose ten services for a five-person team expecting one deployment per month.

**Reasoning.** Independent service boundaries create network, contract, observability, data and on-call work without clear change/scale isolation. A modular monolith preserves boundaries with lower operational cost and an extraction trigger if evidence changes.

**Conclusion.** Architecture optimizes contextual qualities, not fashion.

### Example 5

**Situation.** Cache cuts median latency from 180 ms to 40 ms.

**Reasoning.** Review tail latency, hit distribution, staleness tolerance, invalidation, authorization leakage, memory/cost, cold start and failure fallback. If inventory must be exact at purchase, cached browse and authoritative checkout may use different policies.

**Conclusion.** A tactic’s benefit and liabilities depend on scenario boundaries.

### Example 6

**Situation.** Two services own and directly update the same customer table.

**Reasoning.** Deployment labels suggest independence, but schema changes, invariants, access and incidents are coupled. Choose one authority with contracts, intentionally shared ownership/governance, or reunify boundary. Adding APIs without changing authority may only hide coupling.

**Conclusion.** Data and organizational structures can contradict component diagrams.

### Example 7

**Situation.** ADR says events are at-least-once, but consumers apply charges twice.

**Reasoning.** Decision consequence required idempotent consumer/transactional deduplication and stable event identity; record alone did not realize it. Add contract tests, failure replay and operational duplicate metrics, then repair affected data.

**Conclusion.** Architecture evidence must trace from rationale to behavior.

### Example 8

**Situation.** Benchmark proves chosen store handles 50,000 operations/second.

**Reasoning.** Inspect workload mix, key distribution, payload, consistency, indexes, hardware, concurrency, duration, failures and tail latency. Production may be write-skewed and multi-region. Reproduce representative conditions and model growth.

**Conclusion.** Benchmarks reduce only the uncertainty they actually sample.

### Example 9

**Situation.** Runtime traces show a forbidden dependency introduced to meet an incident deadline.

**Reasoning.** Classify: urgent exception with owner/expiry/removal evidence, or proof original boundary cannot support recovery. Either restore conformance or supersede decision. Silently editing diagram hides operational truth.

**Conclusion.** Drift is evidence requiring a governed response.

### Example 10

**Situation.** Architecture controls infusion-pump dosing and remote updates.

**Reasoning.** Separate safety control from noncritical telemetry, define hazard/fault states, timing, units, sensor validity, authenticated update/rollback, offline/manual mode, audit and recovery. Use hazard analysis, formal/finite models where suitable, fault injection, hardware tests, threat analysis and traceability. Each technique has a scope.

**Conclusion.** Named clinicians and biomedical/safety engineers, human-factors/accessibility specialists, cybersecurity/privacy experts, software/hardware/operations engineers, quality/regulatory representatives and independent assessors must review requirements, hazards, evidence, residual risk and release. Automated conformance cannot authorize clinical use.

## Cross-Program Connections

- **Design and Domain Modeling:** domain boundaries and invariants inform architectural authority and integration.
- **Methods and Evolution:** lifecycle, evidence, ownership, project transitions and retirement shape decisions.
- **Patterns:** patterns supply reusable option knowledge, never context-free answers.
- **Testing and Quality:** verifies architectural scenarios and guards against regression.
- **Delivery and Reliability:** deployment, observability, recovery and incident evidence reveal operational architecture.
- **Distributed Systems:** partial failure, time, replication and consistency constrain structures.
- **Security Engineering:** trust boundaries and threats make narrow decisions highly significant.
- **Systems Engineering:** environment, stakeholders, hazards and lifecycle extend beyond software.
- **Platform Engineering:** shared capabilities encode architectural defaults and cross-team constraints.
- **Cloud Engineering:** provider services create topology, responsibility, portability and cost decisions.

## References

- ISO/IEC/IEEE, [ISO/IEC/IEEE 42010:2022 — Architecture description](https://www.iso.org/standard/74393.html), November 2022, retrieved 2026-08-29. Current standard distinguishing architecture from architecture descriptions and defining stakeholders, concerns, viewpoints and views.
- Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, fourth edition, Addison-Wesley, 2021. Quality attributes, tactics, business drivers, evaluation and architecture lifecycle.
- Dewayne E. Perry and Alexander L. Wolf, “Foundations for the Study of Software Architecture,” *ACM SIGSOFT Software Engineering Notes*, 1992. Foundational elements/form/ rationale model.
- David Garlan and Mary Shaw, *An Introduction to Software Architecture*, Carnegie Mellon University, 1993. Foundational architectural styles and system-level reasoning.
- David L. Parnas, “On the Criteria To Be Used in Decomposing Systems into Modules,” *Communications of the ACM*, 1972. Information hiding and change-oriented decomposition.
- Philippe Kruchten, “The 4+1 View Model of Architecture,” *IEEE Software*, 1995. Multiple-view architecture communication by stakeholder concern.
- Jeff Tyree and Art Akerman, “Architecture Decisions: Demystifying Architecture,” *IEEE Software*, 2005. Structured architectural decision rationale and consequences.
- Rick Kazman, Mark Klein, and Paul Clements, [ATAM: Method for Architecture Evaluation](https://sei.cmu.edu/library/atam-method-for-architecture-evaluation/), CMU/SEI-2000-TR-004, retrieved 2026-08-29. Scenario- and trade-off-oriented evaluation foundations.
- Paul Clements et al., *Documenting Software Architectures: Views and Beyond*, second edition, Addison-Wesley, 2010. Viewpoints, views, interfaces, behavior and rationale documentation.
- Neal Ford, Rebecca Parsons, Patrick Kua, and Pramod Sadalage, *Building Evolutionary Architectures*, second edition, O’Reilly, 2022. Evolution, incremental change and fitness-function framing.

## Exercises

### Exercise 1

Classify five decisions—local variable name, public identifier semantics, logging library patch, data authority, and region topology—by significance signals. Explain exceptions to the apparent ranking.

### Exercise 2

Turn “the upload system must be fast and reliable” into two quality-attribute scenarios, then identify conflicting tactics and evidence.

### Exercise 3

An ADR selects event-driven microservices “for scalability.” Diagnose the record and produce a repaired decision outline.

### Exercise 4

Compare modular monolith, distributed services and managed platform implementation for a new regulated case-management system with uncertain growth.

### Exercise 5

Design architecture decision and assurance evidence for an autonomous railway-platform-door coordination system. Include migration and named human review.

## Answers to the Exercises

### Answer 1

Local variable usually has narrow reach/reversal and is detailed design; it becomes significant if it encodes a regulated/domain meaning propagated by generation. A logging-library patch is usually local maintenance, but a security vulnerability, global telemetry contract or runtime incompatibility can make it architectural. Public identifier semantics affect contracts, data, privacy, compatibility and migration: significant. Data authority affects invariants, integration, security, recovery and ownership: significant. Region topology affects latency, residency, availability, cost, operations and failure: significant. Rank is not enough: assess scenario consequences, criticality, evidence and reversibility. A single safety check can outweigh a broad easy-to-reverse convention.

### Answer 2

Performance: under normal peak load, an authenticated user uploads a 100 MiB supported file over a stated network profile; service accepts durable ownership within 2 seconds at p99 and reports progress without blocking other tenants. Reliability: during loss of one processing worker after durable acceptance, no accepted upload is lost or exposed to another tenant, processing resumes automatically, and final status appears within 10 minutes. Values need stakeholder validation. Direct streaming may reduce latency but couples client to processor failure; durable object storage plus queue improves recovery/load leveling but adds write/queue latency and duplicate handling. Evidence: representative network/load tests, tail distributions, durability guarantees, worker-kill/failover and replay tests, tenant isolation/security checks, capacity model and operational recovery exercise. Averages or one successful upload cannot support either claim.

### Answer 3

Record lacks context, workload, quality scenarios, data/consistency needs, constraints, alternatives, consequences and evidence. Repair: identify independent change/scale/failure boundaries, team/operational capacity and target scenarios. Compare modular monolith, coarser services and events versus requests/batch for each interaction. If choosing events, define producers/consumers, schemas/compatibility, delivery/order semantics, identity/idempotency, durability, backpressure, lag, reconciliation, observability, privacy and ownership. Record why expected benefits exceed network/data/on-call/migration costs, prototype/load/failure evidence, residual risks and triggers such as sustained scaling or coordination thresholds. Do not make “event-driven” a system-wide default when only burst absorption needs it.

### Answer 4

First define case authority, audit/privacy/residency, accessibility, availability/recovery, change and integration scenarios. Modular monolith offers transactions, simpler operation and reversible module boundaries; enforce information hiding, schema ownership and dependency rules so uncertain growth can be observed. Distributed services may isolate regulated domains or independently scaled integrations, but add identity, network failure, consistency, audit correlation and operational burden. Managed platform can reduce commodity operation but adds supplier, configuration, residency, extensibility, auditability, pricing and exit constraints. Under uncertain growth, prefer the simplest option meeting mandatory risks and preserve extraction/portability seams; run targeted supplier and load/recovery experiments. Choose per scenario, staff and lifecycle economics, not presumed future scale. Record migration triggers and reassess with actual workload/change evidence.

### Answer 5

Define entity/environment: train, platform, doors, signaling, sensors, communications, operators and passengers. Drivers include doors cannot open unless train stopped/aligned/authorized; movement cannot be authorized unless doors confirmed safe; obstruction/fault yields defined safe response; commands are authenticated/fresh; degraded manual operation remains controlled; timing and accessibility are specified. Decisions cover safety-control boundary, authoritative state, redundant sensing/voting, communication protocol/time model, fail-safe states, independence from passenger-information analytics, local versus central control, update/rollback, logging and human override.

Evidence traces hazards to decisions, structures and tests: state-machine/formal invariant review, timing/capacity analysis, threat model, sensor disagreement/partition/stale-command/power/restart fault injection, hardware-in-loop, accessibility/human-factors trials, independent implementation/conformance checks and operational drills. Migration uses one platform at a time, shadow observation without control authority, configuration identity, rollback, reconciliation and explicit old-controller decommissioning. Named railway signaling and rolling-stock engineers, drivers/station operations and maintainers, safety assessors, human-factors/accessibility and passenger representatives, cybersecurity/privacy specialists, software/hardware/communications engineers, quality/configuration managers and regulators review hazards, assumptions, evidence, residual risk and authority. Automated evidence cannot approve passenger operation.
