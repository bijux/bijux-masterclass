---
module_id: SARCH-082
program: Software Engineering: Software Architecture
level: 2
module_number: 82
title: Team Topologies and Architecture
status: complete
last_verified: 2026-09-06
---

# Team Topologies and Architecture

## One-Page Review

### Governing question

How can architects use team-topology and interaction-mode concepts to improve flow and constrain cognitive load while preserving domain integrity, platform accountability, specialist depth, and humane organizational evolution?

### Essential definitions

- a **stream-aligned team** owns outcomes for a durable flow of change rather than a temporary project or component queue;
- an **enabling team** helps another team acquire a missing capability and exits when that capability is demonstrated;
- a **complicated-subsystem team** owns a subsystem whose irreducible specialist demands would overload ordinary stream teams;
- a **platform grouping** provides compelling internal products that remove repeated complexity for stream-aligned teams and may contain several teams;
- **collaboration** is high-bandwidth joint discovery for a declared, bounded period;
- **X-as-a-Service** is consumption through a stable, supported interface with low routine coordination;
- **facilitation** is temporary teaching, mentoring, or obstacle removal that leaves capability with the receiving team;
- **team cognitive load** is the mental demand placed on a team by its bounded work, concepts, technologies, interactions, and operating context;
- a **fracture plane** is a candidate seam along which responsibilities might be separated;
- a **team API** states a team's purpose, owned outcomes, services, interaction modes, expectations, constraints, and contact paths;
- **fast flow** means timely, sustainable movement of valuable changes with quality and recovery—not maximum activity or release count.

### Central model, mechanism, or theorem

For team $t$ in context $q$ and time window $w$, model demand as a vector

$$
L_t=(L_d,L_m,L_p,L_o,L_i),
$$

covering domain, mechanism, policy, operational, and interaction demand. Let evidenced capacity be $K_t$ in the same dimensions. A viable topology requires no consequential dimension to remain persistently beyond capacity; one weighted scalar must not hide an unsafe overload. Respond by simplifying work, changing a technical boundary, providing a platform service, concentrating irreducible specialist work, enabling learning, or changing interaction mode. Team types are hypotheses about responsibility; interactions are dynamic mechanisms.

### Critical invariants

- a stream-aligned team owns an outcome, its change, and bounded operational consequences;
- team scope fits demonstrated cognitive and lifecycle capacity;
- platform value is measured in consumer outcomes and reduced burden, not centralized inventory;
- complicated-subsystem status reflects irreducible specialist depth, not merely neglected legacy complexity;
- enablement transfers capability and has an exit criterion;
- collaboration has a purpose, owner, budget, and end condition;
- service consumption has a real contract, support model, compatibility policy, and feedback loop;
- interaction modes may change as uncertainty and capability change;
- security, safety, data, legal, accessibility, and reliability authority remain explicit;
- topology changes preserve delivery, operation, recovery, people, and evidence during transition.

### Common failures

Common failures include relabeling component teams; declaring every shared team a platform; making enabling teams permanent executors; hiding a difficult monolith as a complicated subsystem; requiring collaboration forever; demanding X-as-a-Service while contracts are unstable; using topology diagrams as organization charts; treating cognitive load as a score for individuals; maximizing autonomy without system integrity; splitting into one team per service; creating one giant platform team; measuring ticket count as value; and reorganizing without migrating authority, knowledge, funding, on-call, and code.

### Compact example

A lending stream team owns applicant outcome but must understand Kubernetes policy, certificate rotation, model-serving internals, and a changing risk model. Classify the work rather than move boxes. A platform product supplies deployment, identity, policy evidence, and telemetry through self-service. A complicated-subsystem team owns the numerically specialized scoring engine and a versioned inference contract. An enabling team helps the stream team learn model monitoring for six weeks, then exits after independent operation. The stream and specialist teams collaborate only while discovering the contract, then shift to service consumption. Flow, incidents, cognitive-load interviews, exceptions, and customer and fairness guardrails determine whether the topology works.

### Connections

[SARCH-081](081-conway-s-law-and-team-structures.md) provides socio-technical dependency analysis. [SARCH-083](../ROADMAP.md) next examines governance models. [PLAT-009](../../29-platform-engineering/modules/009-platform-team-boundaries.md) owns detailed platform-team product boundaries; this chapter uses platforms only as one architectural topology.

## Governing Question

Team Topologies offers a compact language for four fundamental team types and three interaction modes in the book and maintained guidance [1], [2]. Its architectural value is not a prescribed organization chart. It helps architects ask who can own an end-to-end change, which complexity should be hidden behind a service, which expertise genuinely requires concentration, which capability should be learned, and how two teams should interact now.

A useful application treats topology as an evolving hypothesis. A team type describes the primary responsibility shape; an interaction mode describes a current relationship. Neither erases the actual dependency graph. The test is whether valuable changes flow sustainably, teams can comprehend and operate their responsibilities, and system-wide obligations remain controlled.

## Why This Matters

Architectures fail socially when responsibility is fragmented across queues. Organizations fail technically when boundaries ignore data authority, runtime coupling, or recovery. A topology vocabulary connects these views. It can expose that a “product team” still waits on six component owners, that a “platform” exports more complexity than it absorbs, or that an “enabling team” has become the permanent operator of everyone else's security work.

The second edition of *Team Topologies*, published September 2025, retains fast flow, cognitive load, four team types, and three interaction modes as its central toolkit [1]. The official maintained key-concepts material, checked 2026-09-06, presents the model as an adaptive pattern language [2]. These are practitioner constructs, not natural kinds or universal causal laws. Empirical delivery research and cognitive-load theory can inform evaluation, but they do not validate a topology merely because its labels match the book.

Architecture consequences are concrete. A stream boundary influences service and data boundaries. Platform interfaces change what application teams must know. A specialist subsystem creates contract and succession risk. Enablement changes knowledge distribution. Collaboration changes decision latency and attention. Every choice moves complexity; none deletes it.

## Prerequisites and Retrieval

Retrieve team, value stream, flow, outcome, domain, bounded context, cohesion, coupling, information hiding, contract, service, platform, product, cognitive load, working memory, expertise, autonomy, authority, accountability, interaction, collaboration, facilitation, handoff, queue, topology, deployment, operations, recovery, and fitness evidence.

SARCH-081 distinguishes technical, work, communication, authority, and outcome graphs. Use its dependency-capability model before choosing a team label. SARCH-072 through SARCH-080 supply evolutionary seams and transitions. This chapter does not replace product strategy, organization design, labor consultation, clinical or safety authority, personnel management, or the detailed platform product discipline owned by Platform Engineering.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish the four team types and three interaction modes precisely;
2. map a flow of change before selecting a topology;
3. assess team cognitive demand as a multidimensional, contextual construct;
4. test candidate fracture planes against architecture and operational evidence;
5. distinguish a platform product from a shared component or ticket queue;
6. distinguish irreducible specialist complexity from accidental complexity;
7. design time-bounded collaboration and facilitation with exit criteria;
8. define a team API and responsibility contract;
9. evolve interaction modes without losing authority or continuity; and
10. evaluate topology changes with flow, quality, human, and system outcomes.

## Core Exposition

**Map the flow first.** Name the external or internal stakeholder, triggering need, valuable outcome, major decisions, information and material transformations, operational consequences, and feedback. A stream is not a department name, channel, project, or arbitrary slice of a process. It should represent a durable flow for which one team can hold meaningful outcome accountability.

Trace a representative change from idea through operation and learning. Count queues, approvals, handoffs, synchronized releases, repositories, data authorities, incident responders, and exceptions. Observe actual work. If the supposed stream team cannot safely change and run the slice without recurring coordination, either the boundary, platform, contract, authority, or team capacity is incomplete.

**Use stream alignment as the default center of gravity.** A stream-aligned team should contain a useful mix of domain, product, engineering, quality, and operational capability appropriate to its consequences. “You build it, you run it” is incomplete unless the team also has authority, evidence, tooling, sustainable on-call, and help for exceptional conditions.

Do not map every user journey to a permanent team. Journeys overlap and change. Choose a stable flow of change with coherent decisions and feedback. A single team may own several deployables; one deployable may support several streams through a service contract. Team-service cardinality is not fixed.

**Treat cognitive load as a design constraint.** Sweller's cognitive-load theory distinguishes intrinsic complexity of material from extraneous demands imposed by presentation or process [3]. Applying this to teams is an analogy that requires care: a team is not one working memory, and expertise, coordination, tools, turnover, interruptions, and operating modes matter. Do not reduce people to “capacity units.”

Assess demand through interviews, observation, incidents, onboarding, decision delay, concepts owned, technologies changed, operational modes, policies interpreted, interactions sustained, and unplanned work. Separate:

- domain demand: business concepts, rules, stakeholders, and exceptions;
- mechanism demand: code, data, infrastructure, algorithms, and tooling;
- policy demand: safety, security, privacy, finance, legal, and governance interpretation;
- operational demand: telemetry, capacity, incidents, recovery, support, and lifecycle;
- interaction demand: consumers, providers, coordination, and contested decisions.

Persistent overload is a system finding, not an individual deficiency. Options include simplifying architecture, retiring variants, automating routine work, reducing interruptions, narrowing scope, improving tools, growing expertise, or changing topology.

**Use platform grouping to remove repeated extraneous complexity.** A platform supplies coherent internal products that let stream teams achieve recurring outcomes with lower effort and risk. It owns consumer research, interfaces, reliability, support, compatibility, security of its boundary, cost, change, and retirement. Provider teams may operate underlying components, but the platform remains accountable for the composed experience.

A portal, cluster team, cloud account group, shared library, or central approval queue is not automatically a platform. Ask whether consumers can perform a valuable task through a supported path without knowing provider topology, whether exceptions are bounded, whether feedback changes the product, and whether adoption improves consumer flow without degrading stability. PLAT-009 develops this boundary in depth.

**Reserve complicated-subsystem teams for irreducible depth.** Some responsibilities demand concentrated mathematics, algorithms, hardware, control theory, compilers, cryptography, or domain expertise that cannot be distributed economically across every stream. A specialist team can own the difficult subsystem and offer a clear interface.

The category is easy to abuse. A tangled legacy system is complicated but may not be intrinsically specialist. Calling it a complicated subsystem can institutionalize neglect. Require evidence of specialist depth, a cohesive boundary, explicit consumers, lifecycle ownership, succession, assurance, and a plan to simplify accidental complexity. The team must not become a generic expert queue.

**Use enabling teams to change capability.** Enablement is successful when the receiving team can perform the target practice independently in its context. The enabling team diagnoses obstacles, teaches, pairs, supplies examples, improves shared approaches, and feeds systemic obstacles to platforms or governance. It does not take over delivery indefinitely.

Define recipient, capability, baseline, approach, timebox, evidence, and exit. Attendance and documents are activity evidence. Independent implementation, diagnosis, operation, and teaching-back are stronger. If the receiving team should never own the work, choose a service relationship instead of disguising execution as enablement.

**Select interaction mode from uncertainty and capability.** Collaboration fits novel work where both teams must jointly discover a boundary, technology, or practice. It is high bandwidth and costly, so give it a question and end condition. X-as-a-Service fits repeatable consumption through a stable interface, supported behavior, compatibility policy, telemetry, and escalation. Facilitation fits capability transfer where one team helps another learn and then withdraws.

Modes can sequence. Two teams collaborate to discover an event contract, consume it as a service after conformance stabilizes, and use short facilitation when a new diagnostic capability is adopted. Record current and target modes. A long-lived “temporary” collaboration signals an unstable boundary or missing ownership.

**Define team APIs without dehumanizing interaction.** A team API can state purpose, owned outcomes, services, consumers, dependencies, decision rights, interaction modes, service expectations, support, contribution path, constraints, and roadmap. It reduces routing ambiguity. It cannot capture trust, negotiation, learning, or every exception. Keep a route for human collaboration and contested risk.

**Test fracture planes.** Candidate seams include business domains, regulatory boundaries, change cadence, risk, data authority, geography, technology, performance isolation, and independent lifecycle. A good fracture plane reduces consequential coordination while preserving cohesive decisions. A poor one creates distributed invariants, chatty calls, duplicated semantics, or coordinated releases.

Evaluate a candidate with change history, runtime and data dependencies, incident paths, deployment coupling, authority, cognitive demand, and future evolution. Perform a thin vertical extraction or responsibility experiment before reorganizing broadly. Architecture diagrams alone cannot demonstrate independence.

**Preserve system-wide obligations.** Stream alignment does not make reliability, security, privacy, accessibility, data semantics, finance, or safety purely local. Assign objective authority, reusable enabling mechanisms, local implementation, and assurance. Platforms can automate controls; enabling teams can transfer capability; specialist teams can own hard mechanisms. Residual risk still needs legitimate acceptance.

**Evolve topology as architecture evolves.** Team structures should be stable enough for trust and learning but adaptable when flow, domains, technology, or obligations change. Avoid constant reshuffling. Use evidence checkpoints, bounded pilots, continuity plans, and consultation. Transfer code, data, access, on-call, budgets, knowledge, supplier relationships, and decision rights together.

**Measure outcomes without surveillance.** Use change lead time, blocked time, handoff delay, deployment independence, failure and recovery, platform task success, support burden, exception demand, cognitive-load interviews, sustainable on-call, learning, and user outcomes. The SPACE framework warns against reducing developer productivity to one dimension or metric [8]. Never rank individuals from commits, messages, tickets, or telemetry.

## Definitions and Notation

Let $T$ be a set of teams and $Q$ a set of operational contexts such as routine delivery, incident response, migration, and audit. For team $t$, context $q$, and time window $w$, define demand vector

$$
L_{t,q,w}=(L_d,L_m,L_p,L_o,L_i),
$$

with domain, mechanism, policy, operational, and interaction components. Define corresponding evidenced capacity $K_{t,q,w}$. Components may be ordinal or independently measured; addition is invalid unless scales and aggregation have been justified.

Let an interaction be $I=(a,b,m,p,e,x)$: provider or helper $a$, consumer or recipient $b$, mode $m$, purpose $p$, evidence $e$, and exit or review condition $x$. Mode $m$ is one of collaboration, X-as-a-Service, or facilitation. The tuple makes the relationship reviewable without claiming it captures social reality.

A **platform** is a product boundary serving internal consumers; a **platform grouping** may contain stream-aligned, platform, enabling, or specialist teams. A **service relationship** is defined by behavior and responsibility, not necessarily a remote API. **Autonomy** is bounded authority and capability to act; it is not isolation or freedom from system constraints.

## Mechanisms, Invariants, or Proof Structure

### Vector capacity invariant

For every team and consequential context, each material demand dimension must be within evidenced capacity or have a funded mitigation and deadline. A low average cannot compensate for an unsafe policy or recovery overload.

### Interaction lifecycle invariant

Every cross-team interaction names its current mode, purpose, decision rights, evidence, and review or exit condition. Service mode additionally requires supported behavior and escalation; facilitation requires recipient capability evidence; collaboration requires a bounded discovery outcome.

### Complexity-transfer invariant

When work moves behind a platform or specialist boundary, responsibility for that complexity and its lifecycle moves explicitly. Hidden provider toil, consumer lock-in, security risk, or incident duty is not complexity reduction.

### Heuristic mode classifier

The following executable rule makes a proposed decision reviewable. It is intentionally a heuristic, not part of the Team Topologies source model and not an organization-design algorithm.

<!-- bijux-verify: {"id":"interaction-mode-heuristic","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"contract discovery: collaboration\nroutine deployment: x-as-a-service\nmonitoring adoption: facilitation\nunstable service: collaboration\n","stderr":""}} -->
```python
def mode(*, uncertainty, contract_stability, recipient_capability, transfer_goal):
    if transfer_goal and recipient_capability < 0.8:
        return "facilitation"
    if uncertainty > 0.4 or contract_stability < 0.7:
        return "collaboration"
    return "x-as-a-service"

cases = {
    "contract discovery": dict(uncertainty=0.9, contract_stability=0.1,
                               recipient_capability=0.8, transfer_goal=False),
    "routine deployment": dict(uncertainty=0.1, contract_stability=0.95,
                                recipient_capability=0.9, transfer_goal=False),
    "monitoring adoption": dict(uncertainty=0.2, contract_stability=0.9,
                                recipient_capability=0.3, transfer_goal=True),
    "unstable service": dict(uncertainty=0.3, contract_stability=0.5,
                             recipient_capability=0.9, transfer_goal=False),
}
for name, evidence in cases.items():
    print(f"{name}: {mode(**evidence)}")
```

Thresholds are hypothetical. A real decision must include consequences, capacity, authority, worker input, and evidence quality. The rule correctly refuses service mode for an unstable contract and facilitation when the goal is not capability transfer.

### Non-compensation proposition

Suppose acceptability requires $L_j\le K_j$ for every consequential dimension $j$. Then a weighted average score below a threshold is insufficient to prove acceptability.

**Proof by counterexample.** Let two dimensions have equal weight, $L=(0,10)$ and $K=(6,6)$. Average demand is $5$, below average capacity $6$, yet the second dimension exceeds capacity by $4$. Therefore scalar average acceptance does not imply componentwise acceptance. This is why severe on-call or policy overload cannot be hidden by easy domain work.

## Alternatives and Trade-Offs

**One broad stream versus several narrow streams.** Broad scope preserves outcomes and reduces interfaces but raises cognitive and operational demand. Narrow scope improves focus but multiplies contracts, distributed decisions, and end-to-end coordination.

**Platform versus local ownership.** A platform removes repeated complexity and standardizes evidence; it can create lock-in, systemic failure, queueing, and distance from domain needs. Local ownership preserves context and options but duplicates work and policy interpretation.

**Specialist team versus embedded specialists.** Concentration sustains deep expertise and assurance. Embedding shortens feedback and spreads context. Use a cohesive subsystem for durable specialist ownership and facilitation or collaboration for knowledge exchange.

**Service versus collaboration.** Service mode enables independent flow when semantics are stable. Collaboration enables discovery but consumes attention. Forcing service too early freezes ambiguity; leaving collaboration permanent hides coupling.

**Facilitation versus training content.** Direct help adapts to context and reveals systemic obstacles. Reusable material scales. Combine them, but judge capability by independent performance, not course completion.

**Stable topology versus frequent adaptation.** Stability supports trust, mastery, and ownership. Adaptation follows changed domains and architecture. Prefer small evidence-driven changes with explicit review over fashionable periodic reshuffling.

## Failure Modes and Misconceptions

1. **“Four types describe every job title.”** They describe primary team responsibility patterns, not personnel taxonomy.
2. **“A component team becomes stream-aligned when renamed.”** Outcome authority and end-to-end capability must change.
3. **“Every internal provider is a platform.”** A platform is a coherent product that improves consumer outcomes.
4. **“Platform means one giant team.”** A platform grouping may require several bounded teams.
5. **“Legacy complexity is a complicated subsystem.”** Accidental complexity should be simplified, not canonized.
6. **“Enabling teams deliver for other teams.”** Persistent execution is a provider or shadow-owner relationship.
7. **“Collaboration is culturally superior.”** It is valuable, costly, and should be purposeful and bounded.
8. **“X-as-a-Service means no people talk.”** Feedback, support, incidents, and evolution still require human paths.
9. **“Facilitation is a help desk.”** Its outcome is transferred capability, not closed tickets.
10. **“Cognitive load is one objective number.”** It is multidimensional, contextual, and partly qualitative.
11. **“An average load proves safety.”** One critical dimension can exceed capacity.
12. **“Autonomy means no standards.”** Teams need bounded authority within system obligations.
13. **“One service requires one team.”** Team-to-service cardinality depends on cohesion, demand, and lifecycle.
14. **“A team API replaces relationships.”** It clarifies routine boundaries but cannot encode trust or novel negotiation.
15. **“Fast flow means more deployments.”** Value, quality, recovery, sustainability, and learning matter.
16. **“Topology diagrams prove causality.”** They are hypotheses requiring observation and intervention evidence.
17. **“Metrics should rank teams.”** Context differs and competitive scoring encourages gaming and harm.
18. **“Reorganization is complete when reporting lines change.”** Authority, code, access, knowledge, on-call, and funding must move safely.

## Worked Examples

### Example 1

**Situation.** A “checkout stream team” owns UI work but waits on catalog, pricing, payment, database, and release teams for every feature.

**Reasoning.** Map the change flow and decision rights. The name supplies neither end-to-end capability nor authority. Internalize cohesive checkout and promotion decisions, consume payment through a stable service, use a platform for deployment, and preserve catalog semantics with a contract. Measure blocked time and coordinated releases.

**Conclusion.** Stream alignment is evidenced by ownership and flow, not a team label.

### Example 2

**Situation.** A team has demand $L=(3,4,9,8,3)$ and capacity $K=(6,6,6,6,6)$.

**Reasoning.** Average demand is $5.4$, below average capacity $6$, but policy and operations exceed capacity. Assigning more domain features would hide risk. Provide policy enablement and automated controls, narrow on-call scope, simplify failure modes, or move a cohesive operational mechanism behind a supported platform.

**Conclusion.** Multidimensional review prevents easy work from compensating for unsafe overload.

### Example 3

**Situation.** Five teams open infrastructure tickets; leaders rename the ticket team “platform engineering.”

**Reasoning.** Consumers still translate provider choices, wait in a queue, and diagnose composition failures. Define consumer journeys, self-service contracts, responsibility, telemetry, compatibility, support, and feedback. Start with one recurring deployment outcome and measure task success, lead time, incidents, exceptions, and operator load.

**Conclusion.** A shared queue is not a platform product until it absorbs coherent complexity and improves consumer outcomes.

### Example 4

**Situation.** An actuarial pricing engine uses specialist mathematics and regulatory evidence that eight product teams cannot each sustain.

**Reasoning.** Create a complicated-subsystem team with cohesive model, verification, versioning, deployment, monitoring, and succession responsibility. Expose versioned decisions and explanations; product teams retain product suitability and customer outcomes. Use collaboration for new semantics and service mode for stable scoring.

**Conclusion.** Concentrated irreducible expertise can reduce distributed load without transferring product accountability.

### Example 5

**Situation.** A cloud enablement team has configured production accounts for other teams for eighteen months.

**Reasoning.** There is no recipient capability transfer or exit, so the relationship is not facilitation. Either productize account provisioning behind a platform service, with the provider owning it, or timebox genuine enablement with independent provisioning, diagnosis, and recovery evidence. Stop calling permanent execution mentoring.

**Conclusion.** Interaction classification exposes shadow ownership and missing product boundaries.

### Example 6

**Situation.** Identity and claims teams collaborate continuously because every schema change requires negotiation.

**Reasoning.** Investigate whether identity facts, authorization decisions, and presentation claims are improperly mixed. During discovery retain collaboration. Separate authority, define versioned semantic contracts and conformance examples, then test service consumption. If joint decisions remain inherently frequent, reconsider the boundary rather than impose a fictional API.

**Conclusion.** Persistent collaboration is evidence about architecture, not automatically a teamwork success.

### Example 7

**Situation.** A monolith is proposed for twelve teams along directory boundaries.

**Reasoning.** Directories may not be fracture planes. Analyze domain rules, data authority, co-change, runtime calls, transactions, incidents, deployments, and future cadence. Pilot one vertical seam with observable behavior and independent release. Reject a split that converts local calls into chatty remote calls while retaining one database and coordinated release.

**Conclusion.** Team topology should follow tested architectural seams, not source-tree geometry.

### Example 8

**Situation.** Security requires all teams to learn every cloud control, causing overload and drift.

**Reasoning.** Central security owns objectives and exceptions; a platform supplies secure defaults and evidence; an enabling team helps teams learn threat modeling for their domain; stream teams own local intent and response. Independent assurance samples consequential controls. Track exposure, false positives, bypasses, recovery, and flow.

**Conclusion.** Several topology roles can distribute one cross-cutting obligation without centralizing every action.

### Example 9

**Situation.** A topology change lowers lead time but doubles night-time pages for one stream team.

**Reasoning.** Fast flow is not achieved sustainably. The operational dimension exceeds capacity. Analyze shared failure modes, platform gaps, service objectives, staffing, automation, and recovery. Reduce failure complexity or redistribute a cohesive platform responsibility; do not praise the delivery metric while exporting harm to on-call workers.

**Conclusion.** Flow evidence requires human and operational countermetrics.

### Example 10

**Situation.** A medical-device company wants stream teams for clinical capabilities while firmware, safety engineering, cybersecurity, manufacturing, and post-market surveillance span products.

**Reasoning.** Align software change where coherent, but retain legally and professionally valid authorities. Use specialist teams for irreducible firmware or safety mechanisms, platforms for validated delivery evidence where appropriate, and time-bounded enablement for secure development. Define interactions, traceability, configuration, incident, recall, and transfer duties. Pilot under quality-system and worker consultation; topology labels cannot authorize clinical use.

**Conclusion.** Regulated topology design must preserve lifecycle assurance and legitimate authority beyond delivery flow.

## Cross-Program Connections

- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) supplies technical design patterns whose ownership and cognitive consequences topology must consider.
- [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns delivery flow, on-call, incidents, and recovery evidence used to assess topology.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns data domains, semantic authority, mesh, and governance; stream labels do not create valid data domains.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) owns broader lifecycle, safety, human, supplier, and federated-system boundaries.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns durable service contracts that enable low-coordination consumption.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns platform product discovery, interfaces, operation, and consumer experience in depth.

## References

1. Matthew Skelton and Manuel Pais, [*Team Topologies: Organizing Business and Technology for Fast Flow of Value*](https://itrevolution.com/product/team-topologies/), 2nd ed., IT Revolution, published September 23, 2025. Publisher record checked 2026-09-06.
2. Team Topologies, [“Key Concepts and Practices”](https://teamtopologies.com/key-concepts), continuously maintained official guidance, retrieved 2026-09-06. Current descriptions of four types, three modes, cognitive load, and adaptive topology.
3. John Sweller, [“Cognitive Load During Problem Solving: Effects on Learning”](https://doi.org/10.1207/s15516709cog1202_4), *Cognitive Science* 12(2), 1988. Foundational cognitive-load theory; team-level use in this chapter is explicitly an analogy rather than direct experimental transfer.
4. Melvin E. Conway, [“How Do Committees Invent?”](https://melconway.com/Home/pdf/committees.pdf), *Datamation* 14(4), 1968. Primary communication-structure argument.
5. David L. Parnas, [“On the Criteria To Be Used in Decomposing Systems into Modules”](https://doi.org/10.1145/361598.361623), *Communications of the ACM* 15(12), 1972. Information hiding and responsibility-oriented decomposition.
6. Nicole Forsgren, Jez Humble, and Gene Kim, *Accelerate*, IT Revolution, 2018. Empirical and methodological treatment of software-delivery performance and organizational capabilities.
7. Manuel Pais and Matthew Skelton, [“Team Interaction Modeling with Team Topologies”](https://teamtopologies.com/key-concepts-content/team-interaction-modeling-with-team-topologies), official maintained guidance, retrieved 2026-09-06. Evolutionary interaction and cognitive-load modeling.
8. Nicole Forsgren et al., [“The SPACE of Developer Productivity”](https://queue.acm.org/detail.cfm?id=3454124), *ACM Queue* 19(1), 2021. Multidimensional productivity framework and cautions against single metrics.
9. Abi Noda et al., [“DevEx: What Actually Drives Productivity”](https://queue.acm.org/detail.cfm?id=3595878), *ACM Queue* 21(2), 2023. Feedback loops, cognitive load, and flow state as experience dimensions.
10. CNCF Platforms Working Group, [*Platforms White Paper*](https://tag-app-delivery.cncf.io/whitepapers/platforms/), 2023. Community guidance on platform capabilities, interfaces, consumers, and product thinking.
11. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021. Quality attributes, structures, interfaces, and organizational context.
12. ISO/IEC/IEEE, [ISO/IEC/IEEE 42010:2022 — Software, Systems and Enterprise — Architecture Description](https://www.iso.org/standard/74393.html), 2nd ed., published November 2022. Official current record checked 2026-09-06; used for architecture, stakeholder, concern, and viewpoint discipline, not as a team-topology prescription.

## Exercises

### Exercise 1

Define each of the four team types and three interaction modes in one sentence, including the defining outcome or exit condition.

### Exercise 2

A team has $L=(7,3,2,9,5)$ and $K=(6,6,6,6,6)$. Identify breaches. Explain why averaging is unsafe and propose two different mitigations.

### Exercise 3

An “enabling” database team performs every schema migration for six product teams. Diagnose the interaction, choose a target topology, and specify evidence and exit criteria.

### Exercise 4

Compare a platform team and a complicated-subsystem team for shared machine-learning capability. Give conditions favoring each and explain product-team accountability.

### Exercise 5

A regional rail operator, ticketing vendor, infrastructure agency, accessibility office, cybersecurity center, and several passenger-product teams must modernize disruption communications. Design a federated topology and interaction evolution without assuming common management authority.

## Answers to the Exercises

### Answer 1

A **stream-aligned team** owns outcomes and lifecycle for a durable flow of change. An **enabling team** transfers a declared capability and exits when the recipient demonstrates it. A **complicated-subsystem team** owns a cohesive subsystem requiring irreducible specialist depth. A **platform grouping** owns compelling internal products that reduce consumer burden and improve flow. **Collaboration** jointly discovers something uncertain for a bounded period. **X-as-a-Service** provides repeatable behavior through a stable supported interface. **Facilitation** mentors or removes obstacles until the recipient can act independently. Labels without these outcomes or exit conditions are incomplete.

### Answer 2

Domain demand $7>6$ and operational demand $9>6$ breach capacity; mechanism, policy, and interaction demand do not. Average demand is $26/5=5.2<6$, but the average hides both breaches, so it cannot establish viability. One mitigation is to narrow the stream boundary or simplify/retire domain variants. Another is to move cohesive repeated operational complexity behind a supported platform service, improve automation, and rebalance sustainable on-call. Growing expertise or staffing may help, but simply adding people can add coordination load. Reassess every dimension and user/worker outcomes after intervention.

### Answer 3

The current relationship is permanent execution, not enablement. Determine whether migrations can become a safe self-service platform capability or whether product teams should own them after real facilitation. A platform target fits when the database team can own versioned migration workflows, policy checks, observability, rollback support, and consumer experience. A facilitation target fits when schema semantics and application rollout must remain with product teams: timebox pairing, conformance examples, rehearsals, and teaching-back. Evidence includes independent safe migration and recovery, fewer queues, correct data semantics, bounded incidents, and recipient diagnosis. Exit when the declared target capability is repeatedly demonstrated; otherwise rename and fund the provider relationship honestly.

### Answer 4

A platform fits reusable model packaging, deployment, feature storage, identity, policy evidence, telemetry, and lifecycle journeys whose complexity can be offered through stable consumer-oriented interfaces. A complicated-subsystem team fits a cohesive inference, optimization, or model mechanism requiring scarce mathematics and specialized assurance. The same organization may use both: a specialist team supplies versioned model behavior through the platform. Product teams retain problem definition, data fitness, user outcome, fairness and safety context, appropriate use, fallback, and monitoring of product consequences. Neither provider may silently accept domain or regulated risk outside its authority.

### Answer 5

Treat the parties as a federation. Passenger-product teams may be stream-aligned to disruption-information outcomes within their channels. A vendor or operator platform supplies versioned event distribution, identity, status, observability, and conformance. A specialist accessibility capability and cybersecurity center provide standards, assurance, and time-bounded facilitation without becoming feature queues. Agencies retain source authority for infrastructure and service facts; the operator retains operational communication authority; each legal entity retains its mandated duties. Collaborate initially to discover shared semantics, failure modes, offline behavior, correction, and escalation. Move stable distribution to service mode and use facilitation for adoption. Evidence includes multilingual and accessible delivery, latency, provenance, correction, partial-network failure, incidents, exercises, passenger research, support burden, and independent recovery. Contracts, joint forums, escalation, and public accountability substitute for a common reporting line; no software topology displaces transport safety, accessibility, labor, privacy, procurement, or statutory authority.
