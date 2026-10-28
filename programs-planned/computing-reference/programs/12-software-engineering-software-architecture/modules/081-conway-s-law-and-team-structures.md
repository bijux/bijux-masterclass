---
module_id: SARCH-081
program: Software Engineering: Software Architecture
level: 2
module_number: 81
title: Conway's Law and Team Structures
status: complete
last_verified: 2026-09-06
---

# Conway's Law and Team Structures

## One-Page Review

### Governing question

How should architects reason about the reciprocal relationship between technical dependencies and organizational communication without treating Conway's observation as fate or using a reorganization as a substitute for engineering?

### Essential definitions

- **Conway's observation** is the claim that organizations designing systems are constrained to produce designs whose communication structures are reflected in those systems;
- a **technical dependency** is a relationship in which changing, operating, or reasoning about one technical element requires knowledge or action concerning another;
- a **coordination need** is the work interaction required to resolve a technical or decision dependency;
- a **coordination capability** is a dependable channel, shared context, authority, cadence, or artifact that can satisfy such a need;
- **mirroring** is correspondence between organizational relationships and technical relationships, not literal identity between an organization chart and a component diagram;
- **socio-technical congruence** is alignment between coordination needs induced by work dependencies and the coordination relationships actually available;
- an **ownership boundary** assigns decision and operational accountability; it does not erase dependencies crossing that boundary;
- a **team API** is an explicit description of how another team obtains a service, decision, contribution, or collaboration from a team;
- the **inverse Conway maneuver** is the deliberate shaping of communication and team boundaries to encourage a desired architecture;
- a **coordination load** is the cognitive and interaction demand created by dependencies, changes, uncertainty, and exceptions.

### Central model, mechanism, or theorem

Let teams be vertices $V$. For each unordered pair $\{i,j\}$, let $d_{ij}\ge 0$ be the current coordination need induced by technical work and let $c_{ij}\in[0,1]$ be the demonstrated fraction of that need the organization can satisfy. Define residual coordination exposure

$$
U=\sum_{i<j} d_{ij}(1-c_{ij}).
$$

Reducing $U$ can mean decreasing technical coupling, improving coordination capability, relocating responsibility, or changing the delivery slice. The model is diagnostic, not a universal productivity law: weights, observations, time windows, and consequences must be declared. Perfect mirroring is neither always possible nor always desirable.

### Critical invariants

- model actual work and communication, not only reporting lines and intended components;
- treat organizational and technical structure as a feedback system that changes over time;
- assign one accountable decision owner without pretending that shared knowledge is unnecessary;
- put frequent, high-change dependencies within a team where feasible;
- give unavoidable cross-team dependencies explicit contracts, authority, compatibility rules, and interaction modes;
- distinguish coordination needed for discovery from stable coordination needed for operation;
- preserve security, safety, data, legal, and user obligations across every ownership change;
- measure flow, failures, and coordination friction before and after interventions;
- bound experiments and retain rollback or adaptation options;
- never infer individual performance or prescribe layoffs from repository-network data.

### Common failures

Common failures include reading an organization chart as the communication network; declaring Conway's observation a deterministic law; drawing service boundaries around departments; creating a team for every component; maximizing team independence while hiding end-to-end work; treating meetings as the only coordination mechanism; replacing conversation with brittle documentation; moving boxes without authority or skills; measuring commit counts as productivity; ignoring contractors, operations, security, and users; performing a large reorganization and platform rewrite together; and blaming teams for dependencies created by portfolio or architecture decisions.

### Compact example

Checkout changes repeatedly require synchronized edits by catalog, pricing, payment, and order teams. The visible symptom is slow cross-team delivery; the deeper dependency graph shows a volatile promotion rule split across four owners. One response is more meetings. A better diagnosis separates necessary dependencies from accidental ones: place promotion policy and its tests under one stream-aligned owner, publish a versioned decision contract to checkout, retain payment authorization with its specialist owner, and establish a short collaboration mode for the migration. Measure lead time, failed handoffs, incident recovery, and contract-change fan-out. The intervention changes both technical and organizational edges; a new chart alone would not.

### Connections

[SARCH-080](080-planning-architecture-evolution-across-multiple-releases.md) supplies safe multi-release change. [SARCH-082](../ROADMAP.md) next develops explicit team interaction patterns and cognitive-load boundaries. [SEPAT-081](../../11-software-engineering-patterns/ROADMAP.md), [SDRE-081](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md), and [PLAT-081](../../29-platform-engineering/ROADMAP.md) own complementary pattern, delivery, and platform practices.

## Governing Question

Software structure and organizational structure are not independent design variables. People discover requirements, make decisions, write and review code, operate services, respond to incidents, and negotiate change through communication relationships. A design requiring continual coordination between people who lack time, shared context, access, trust, or authority will accumulate delays and workaround interfaces. An organization that frequently coordinates across a technical boundary may gradually dissolve that boundary in practice even if diagrams retain it.

The useful question is therefore not whether Conway's Law is “true.” It is which technical dependencies create coordination needs, which social mechanisms can satisfy them, which mismatches matter, and which intervention changes the whole system with acceptable risk. The answer may be a modularity change, a team-boundary change, a clearer contract, temporary collaboration, shared tooling, different sequencing, or no structural change at all.

## Why This Matters

Architecture advice often assumes that components can be assigned independently after their interfaces are drawn. Organization advice often assumes that changing reporting lines will produce autonomy. Both views omit feedback. Technical coupling drives interaction; repeated interaction builds shared language and authority; those social relationships shape the designs people can feasibly create. The result is path dependent.

Conway's 1968 paper reasoned from communication constraints in design organizations, not from microservices or a particular management fashion [1]. Later empirical work found both mirroring and important exceptions. MacCormack, Rusnak, and Baldwin observed different modularity in matched commercial and open-source products [6]. Colfer and Baldwin's review of 142 studies found prevalent mirroring in firms and industries but non-universal results, especially different evidence in open collaborative projects [7]. The responsible conclusion is a tendency with mechanisms and boundary conditions, not a theorem that every org chart becomes a runtime topology.

The stakes are operational. An ownership design affects deployment coupling, incident coordination, security review, data authority, on-call burden, and how quickly evidence reaches a decision maker. Poor alignment can make routine changes expensive and emergencies unsafe. Overcorrection also harms: forced isolation duplicates expertise, fragments user journeys, and turns every collaboration into contract negotiation.

## Prerequisites and Retrieval

Retrieve architecture, component, connector, interface, module, information hiding, cohesion, coupling, dependency, change propagation, bounded context, contract, ownership, accountability, authority, stakeholder, concern, value stream, cognitive load, flow, batch, queue, handoff, topology, graph, matrix, centrality, versioning, deployment, incident, recovery, and technical debt.

SARCH-011 through SARCH-020 establish decomposition and dependency reasoning. SARCH-031 through SARCH-040 compare architectural styles without mapping them mechanically to teams. SARCH-061 through SARCH-070 provide evidence and decision methods. SARCH-071 through SARCH-080 provide evolutionary mechanisms and safe sequencing. This module applies those tools to organizational communication. It does not replace organization design, labor relations, personnel management, psychology, security governance, or product strategy.

## Learning Objectives

After completing this module, you should be able to:

1. state Conway's original observation precisely and explain why common slogans overstate it;
2. distinguish reporting, communication, collaboration, authority, and technical dependency structures;
3. derive coordination needs from concrete work rather than component names;
4. construct and challenge a socio-technical dependency model;
5. identify consequential mismatches without treating correlation as causation;
6. compare technical, organizational, and coordination interventions;
7. apply an inverse Conway maneuver as a bounded hypothesis;
8. preserve end-to-end outcomes and cross-cutting obligations across team boundaries;
9. evaluate interventions with humane, privacy-aware evidence; and
10. adapt team and architecture structures incrementally as dependencies change.

## Core Exposition

**Begin with the original claim.** Conway wrote that organizations designing systems are constrained to produce designs that copy their communication structures [1]. “Communication structure” is richer than hierarchy. It includes who can obtain information from whom, how quickly, in which language and medium, with what shared context, and with whose decision authority. “Design” includes interfaces, decompositions, conventions, duplicated mechanisms, and omissions—not only deployable services.

The statement proposes a generative mechanism. A design task is partitioned among people. Their partial designs must be integrated through available communication paths. Where communication is easy, jointly shaped structure is feasible. Where it is costly or absent, teams favor interfaces they can specify across the divide, duplicate capability, make local assumptions, or avoid changes. The resulting artifact records these constraints. This does not imply conscious copying.

**Separate five structures.** A rigorous diagnosis overlays at least five graphs:

1. the technical dependency graph: elements that change, execute, fail, or recover together;
2. the work dependency graph: tasks requiring information, sequencing, or joint decisions;
3. the communication graph: observed information exchange and collaboration;
4. the authority graph: who may decide, fund, approve, deploy, and accept risk;
5. the outcome graph: users and value streams affected by combined behavior.

An organization chart approximates only part of the authority graph. A repository ownership file approximates only part of decision and review ownership. Chat traffic approximates communication but omits meetings, documents, pairing, tacit knowledge, and deliberate non-communication. Runtime calls omit schema, build, identity, operational, and semantic dependencies. No single data source is the organization.

**Derive coordination needs from change.** Static component coupling is insufficient. Two stable components with a mature contract may communicate at runtime but require little human coordination. Two repositories with no runtime edge may share a hidden release rule, data meaning, or security policy and therefore require intense coordination. Ask: for a proposed change, who needs whose knowledge, decision, artifact, or action before safe completion?

Record dependency kind, frequency, volatility, consequence, direction, and evidence. High-frequency, high-volatility, high-consequence dependencies deserve the strongest treatment. A yearly certificate rotation and a daily joint schema change are different even if both cross the same team boundary.

**Choose among four responses.** A mismatch between coordination need and capability can be addressed by:

- **reduce the dependency:** information hiding, stable contracts, local decision rules, duplicated read models, or a different decomposition;
- **increase coordination capability:** temporary collaboration, shared planning, pairing, liaison roles, communities, or common operational views;
- **move responsibility:** place coupled decisions and work within one accountable team or durable group;
- **change the delivery slice:** sequence work so fewer parties must coordinate simultaneously.

These responses have different costs. Reducing a dependency can add latency, duplication, or weaker consistency. Increasing coordination consumes attention. Moving responsibility can overload a team or separate specialists from peers. Resequencing can defer value. “Put everything in one team” drives external coordination toward zero but creates an unbounded cognitive and managerial system.

**Treat team boundaries as design decisions.** A durable team boundary should usually enclose a coherent stream of change and enough capability to deliver and operate it. It should not simply reproduce the current component inventory. Components can be merged, split, automated, retired, or offered as services; teams are social systems that need identity, learning, manageable load, and continuity.

Ownership has layers. A team may own a service's implementation and operation while a cross-domain body owns a shared semantic policy. A security team may own a control objective while product teams own compliant implementation. Name decision rights explicitly: propose, decide, implement, verify, operate, accept residual risk, and retire. A single “owner” label hides incompatible duties.

**Use interfaces for both software and work.** A technical API describes accepted requests, behavior, failure, compatibility, and change. A team interaction boundary needs analogous clarity: supported services, inputs, service expectations, decision authority, escalation, contribution rules, and unsupported requests. This is not a reason to turn all human interaction into tickets. Explicit interfaces handle repeatable work; collaborative interaction handles novel, uncertain, tightly coupled work.

Stable contracts can substitute for some continuous communication, as Herbsleb and Grinter observed, but modular design alone did not eliminate geographically distributed coordination problems [3]. Architecture, plans, processes, expertise location, and unexpected events interact. A contract that omits semantic meaning or recovery responsibility merely hides the need until integration or failure.

**Reason about socio-technical congruence.** Cataldo, Herbsleb, and Carley model coordination requirements induced by technical relationships and compare them with observed coordination [5]. Their empirical results associate congruence with shorter modification-request resolution in the studied setting, while also showing that logical dependencies can matter more than simple call or data edges. Use that research as a measurement lens, not a transferable constant.

The residual-exposure model in this chapter extends the lens for diagnosis. A dependency weight $d_{ij}$ can combine normalized frequency, volatility, and consequence only if the combination rule is documented. Capability $c_{ij}$ must reflect demonstrated coordination within a time window, not the existence of a channel. A shared chat room is not proof that the right people reach a decision before a release or incident deadline.

**Apply the inverse maneuver cautiously.** If organization shapes architecture, leaders may intentionally create communication paths and team responsibilities consistent with a desired architecture. This is often called the inverse Conway maneuver. The term describes an intervention hypothesis, not a mathematical inverse. Multiple organizational structures can support one architecture; legacy dependencies persist; incentives and skills may resist the new boundary; and organization changes have human consequences.

Make the desired technical outcome explicit, identify causal assumptions, choose the smallest reversible organizational and technical experiment, fund migration, and define evidence. For example, assign a stable cross-functional team to one end-to-end capability, give it deployment and operational authority, extract one seam, and observe change lead time and incident handling. Do not simultaneously reorganize every team and rewrite every subsystem: attribution and rollback disappear.

**Account for time.** Team and architecture graphs evolve at different speeds. A reporting change is immediate in a directory but slow in knowledge, trust, access, on-call competence, and code. A service split can be deployed before data authority or operational ownership is resolved. Measure states at explicit times. Lag can create a transient mismatch even when direction is sensible.

Transitions need dual coverage. The old owner must remain capable until the new owner has rehearsed delivery, operation, recovery, and retirement. Knowledge transfer is evidenced by independent action and reviewed outcomes, not attendance at handover meetings. Temporary collaboration needs an exit condition; otherwise a permanently coupled architecture is hidden behind a standing coordination group.

**Preserve cross-cutting integrity.** Security, privacy, reliability, accessibility, data semantics, finance, and regulatory obligations often cross stream boundaries. Centralizing every implementation creates bottlenecks; delegating every interpretation creates inconsistency. Separate policy authority, enabling capability, local implementation, and independent assurance. Provide defaults and automated evidence while retaining escalation for novel risk.

**Observe without surveilling.** Useful system measures include change lead time, blocked time, handoff count, cross-boundary change fan-out, review delay, incident coordination time, ownership ambiguity, contract breakage, and repeated exception paths. Combine repository, deployment, incident, and qualitative evidence. Never treat message volume, hours online, commits, or individual centrality as productivity. Such measures are incomplete, gameable, context-dependent, and capable of harming people.

Aggregate where possible, minimize data, state purpose and retention, involve affected workers, control access, and forbid employment decisions unsupported by valid evidence. A socio-technical intervention must be reviewed as a change to working conditions, not merely a graph optimization.

**Review architecture and organization together.** At each checkpoint, ask whether dependency edges changed, whether coordination capability works under routine and exceptional load, whether authority matches accountability, whether cognitive load is bounded, and whether users receive improved outcomes. A lower cross-team edge count is not success if reliability worsens or policy variants proliferate.

## Definitions and Notation

Let $V=\{1,\ldots,n\}$ be teams or durable work groups in a declared scope and time window. Let $T=(V,E_T)$ be a weighted coordination-need graph. For $i<j$, $d_{ij}\ge 0$ measures the need for coordination between teams $i$ and $j$. Let $C=(V,E_C)$ describe available coordination capability, with $c_{ij}\in[0,1]$ representing the evidenced fraction of the declared need that can be satisfied within its required time and quality.

Define residual exposure:

$$
U(T,C)=\sum_{i<j}d_{ij}(1-c_{ij}).
$$

If a dependency is absent, $d_{ij}=0$. If capability is fully demonstrated for the bounded need, $c_{ij}=1$. Neither value is permanent. The model does not require organizational and technical graphs to be isomorphic; it asks whether coordination capacity covers consequential need.

For a change $x$, let $F(x)$ be the set of teams whose coordinated action is required. Its organizational fan-out is $|F(x)|$. Let $H(x)$ be the number of handoffs on the critical work path. Fan-out and handoffs are diagnostic observations, not universal complexity measures: parallel expert collaboration can outperform a forced single owner.

A **logical dependency** exists when artifacts change together for a shared reason even without a declared static or runtime edge. A **communication path** is a repeatable means of exchanging and interpreting information. **Authority** is legitimate decision power; **accountability** is answerability for outcomes. **Collaboration** means jointly discovering or executing work. **Coordination** also includes stable mechanisms—contracts, plans, automation, standards, or shared artifacts—that align separate action.

## Mechanisms, Invariants, or Proof Structure

### Dependency-capability invariant

For every material technical or work dependency, either the responsible work lies within one accountable boundary or an adequate cross-boundary coordination mechanism is named, exercised, and observed. A documented interface with no versioning or incident path does not satisfy the invariant.

### Authority-accountability invariant

Every material decision has an accountable owner with sufficient authority, information, and capacity. Shared consultation is compatible with one decision owner. Conversely, naming one owner does not remove affected stakeholders or assurance duties.

### Transition-continuity invariant

During a boundary change, at least one explicitly named party can deliver, operate, recover, and safely stop the affected capability. Transfer is complete only when the new owner demonstrates these actions and obsolete access and obligations are retired.

### Proposition: four ways to lower modeled residual exposure

For one pair with contribution $u_{ij}=d_{ij}(1-c_{ij})$, exposure decreases if an intervention validly lowers $d_{ij}$, raises $c_{ij}$, removes the pair by placing the coordinated responsibility inside one modeled vertex, or changes the work slice so the dependency is absent in the evaluated window.

**Proof.** Because $d_{ij}\ge0$ and $0\le c_{ij}\le1$, lowering $d_{ij}$ with fixed $c_{ij}$ cannot increase the product, and raising $c_{ij}$ with fixed $d_{ij}$ cannot increase it. Internalizing the relationship removes its cross-vertex term but may create new internal load or external edges; therefore only this model contribution is proven lower. Removing the dependency from the scoped work makes its weight zero for that window. No step proves better organizational performance because measurement error, new edges, internal load, and outcome effects remain.

### Executable finite model

The following bounded model compares raising coordination capability with relocating one coupled responsibility. It illustrates arithmetic only; it does not prescribe a team design.

<!-- bijux-verify: {"id":"coordination-exposure-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"baseline=9.2\ncollaboration=5.6\nrelocation=4.4\n","stderr":""}} -->
```python
needs = {
    ("catalog", "checkout"): 6.0,
    ("checkout", "payments"): 4.0,
    ("checkout", "risk"): 2.0,
}

baseline_capability = {
    ("catalog", "checkout"): 0.2,
    ("checkout", "payments"): 0.4,
    ("checkout", "risk"): 0.0,
}

def exposure(capability, omitted=frozenset()):
    return sum(
        need * (1 - capability[pair])
        for pair, need in needs.items()
        if pair not in omitted
    )

collaboration = dict(baseline_capability)
collaboration[("catalog", "checkout")] = 0.8

print(f"baseline={exposure(baseline_capability):.1f}")
print(f"collaboration={exposure(collaboration):.1f}")
print(f"relocation={exposure(baseline_capability, {('catalog', 'checkout')}):.1f}")
```

The baseline is $6(0.8)+4(0.6)+2(1)=9.2$. Raising catalog–checkout capability from $0.2$ to $0.8$ lowers its contribution by $6(0.6)=3.6$, producing $5.6$. Modeling that responsibility within one boundary removes the $4.8$ cross-boundary contribution and leaves $4.4$. The apparent advantage of relocation excludes its migration cost, internal cognitive load, and any new dependencies.

### Evidence ladder

An organization chart or component diagram proposes structure. Repository and work-system traces observe selected relationships. Interviews and work observation add meaning. A bounded intervention with before/after measures supports a causal hypothesis more strongly. Replication across changes and operating modes strengthens confidence. None alone proves that organization caused architecture, that the intervention generalizes, or that an individual performed well or poorly.

## Alternatives and Trade-Offs

**Align teams to value streams.** This can reduce handoffs for frequent end-to-end changes and create outcome accountability. It may duplicate specialist capability and struggle where one regulated or scarce function serves many streams.

**Align teams to technical subsystems.** This concentrates expertise and can protect demanding internals. It can make customer outcomes cross many queues and encourage local component optimization.

**Internalize versus contract.** Internalizing a volatile dependency permits rich communication and joint change. A stable contract enables independent work and replacement. Premature contracts freeze misunderstanding; permanent collaboration around a supposedly stable API signals a false boundary.

**Centralize versus federate cross-cutting decisions.** Central authority can ensure consistency and manage rare expertise. Federation improves local context and speed. A layered model—central objective and evidence rule, shared enabling capability, local implementation—often avoids both unchecked divergence and approval queues.

**Reorganize versus refactor.** Moving teams can improve authority and communication before code moves, but inherited coupling remains. Refactoring first can reveal a seam, but teams may lack authority to sustain it. A coordinated sequence with explicit transition ownership is safer than assuming either order is universally correct.

**Stable teams versus project teams.** Stable teams accumulate domain and operational knowledge. Temporary project teams can concentrate on a bounded change. Repeated disbanding destroys ownership; permanent teams around temporary components fossilize transition architecture.

**Rich communication versus asynchronous artifacts.** Direct collaboration resolves ambiguity and builds shared models. Versioned decisions, contracts, and runbooks preserve context across time zones and turnover. Novel work needs conversation; repeatable work benefits from reliable artifacts. Either extreme fails.

**Mirroring versus deliberate non-mirroring.** Mirroring can economize coordination. Non-mirroring may be valuable when independent modular architecture is a strategic objective, when a platform serves many groups, or when an open community coordinates through public artifacts. Colfer and Baldwin document exceptions and partial mirroring; the design choice needs evidence, not dogma [7].

## Failure Modes and Misconceptions

1. **“The org chart is the architecture.”** It omits informal communication, work, authority, and technical edges.
2. **“Conway's Law predicts one inevitable design.”** It describes constraint and tendency, not a unique topology.
3. **“One team equals one microservice.”** Team and deployment boundaries solve different problems and change at different rates.
4. **“More communication is always better.”** Unfocused coordination consumes attention and can obscure authority.
5. **“Documentation eliminates communication.”** Artifacts reduce repeated clarification only when semantics, ownership, and change processes are sound.
6. **“A shared channel proves coordination.”** Availability is not timely comprehension or decision capability.
7. **“Low cross-team coupling means good architecture.”** It may reflect duplicated rules, fragmented journeys, or unobserved dependencies.
8. **“Reorganization removes code coupling.”** Legacy data, releases, contracts, and operations persist after reporting changes.
9. **“A service boundary grants autonomy.”** Shared databases, synchronized releases, central approvals, or weak observability can negate it.
10. **“The inverse Conway maneuver is literally inverse.”** There is no one-to-one invertible mapping.
11. **“Repository edges reveal all dependencies.”** Semantics, incidents, deployment, policy, and tacit knowledge are missing.
12. **“Commit or message counts measure productivity.”** They are incomplete, gameable activity signals and unsafe individual metrics.
13. **“Every shared concern needs a central team.”** Centralization can create queues; policy, enablement, implementation, and assurance can be separated.
14. **“Every specialist belongs in every product team.”** Scarce expertise may require enabling or service relationships and deliberate knowledge diffusion.
15. **“Ownership means isolation.”** Accountable teams still collaborate and honor system-wide constraints.
16. **“A handover meeting transfers ownership.”** New owners must demonstrate delivery, operation, recovery, and decision competence.
17. **“Mirroring research supplies a universal coefficient.”** Results depend on constructs, samples, contexts, and time windows.
18. **“Organization design is purely technical.”** It affects careers, workload, identity, power, privacy, and working conditions.

## Worked Examples

### Example 1

**Situation.** A diagram shows four services owned by four teams, and leaders conclude the architecture mirrors the organization.

**Reasoning.** Inspect change and operation rather than labels. All four services deploy from one pipeline, share one schema, require one release manager, and page one operations group. The technical and work graphs are tightly connected despite separate boxes. Meanwhile, engineers across the four teams pair daily, so the communication graph does not match the hierarchy either. The slogan fits neither observed graph.

**Conclusion.** Mirroring must be evaluated against explicit technical, work, communication, and authority relationships, not visual box counts.

### Example 2

**Situation.** Catalog–checkout need is $6$, checkout–payments need is $4$, and checkout–risk need is $2$. Capabilities are $0.2$, $0.4$, and $0$ respectively.

**Reasoning.** Residual exposure is $6(1-0.2)+4(1-0.4)+2(1-0)=4.8+2.4+2=9.2$. Improving the first capability to $0.8$ produces $6(0.2)+2.4+2=5.6$. The difference is $3.6$. This ranks one modeled opportunity but says nothing about cost or outcome.

**Conclusion.** Weighted mismatch makes assumptions inspectable; it does not turn organization design into a context-free optimization.

### Example 3

**Situation.** Two teams own services with no runtime calls, so an architect declares them independent.

**Reasoning.** Six recent changes touched both repositories because both encode the same eligibility rule. Neither static imports nor traces reveal this logical dependency. A shared policy decision and conformance examples are needed, or one owner should hold the rule and expose a stable decision contract. Duplicating the rule to avoid communication would increase semantic drift.

**Conclusion.** Co-change and shared reasons can create stronger coordination needs than runtime edges.

### Example 4

**Situation.** A payments team and checkout team must collaborate daily while a new authorization protocol is discovered.

**Reasoning.** Freezing an API immediately would encode unresolved fraud, timeout, and recovery assumptions. Establish temporary close collaboration with one decision log, joint executable examples, and a weekly boundary review. When semantics and failure behavior stabilize, publish a versioned contract, independent conformance tests, escalation path, and exit criteria for the collaboration.

**Conclusion.** Interaction mode should evolve from discovery-rich collaboration toward a service boundary only when uncertainty falls.

### Example 5

**Situation.** Leadership wants an inverse Conway maneuver to create independent order and fulfillment capabilities.

**Reasoning.** Current code shares one database and transaction. Create two durable teams with joint responsibility for a bounded seam, not instant isolated ownership. Release 1 maps behavior and adds observability. Release 2 introduces a fulfillment request contract while the old owner remains on call. Release 3 transfers one region under rehearsed rollback. Only after the new team independently deploys and recovers does old access retire. Compare lead time, cross-team blocking, correctness, and recovery with baseline.

**Conclusion.** A safe inverse maneuver couples organization change to technical migration and evidence rather than a one-day chart change.

### Example 6

**Situation.** A central security team approves every routine dependency update, producing a two-week queue.

**Reasoning.** Preserve central ownership of control objectives, threat intelligence, exception criteria, and assurance. Move ordinary implementation decisions to product teams through curated versions, automated policy checks, provenance evidence, and local remediation guidance. Reserve synchronous central review for novel risk and exceptions. Monitor bypasses, vulnerable exposure time, false positives, and incidents.

**Conclusion.** Separating policy, enablement, implementation, and assurance can reduce coordination load without abandoning security governance.

### Example 7

**Situation.** Repository analysis identifies one engineer as the highest-centrality node, and a manager proposes evaluating them as a bottleneck.

**Reasoning.** The data omits design conversations, mentoring, generated changes, pair work, access constraints, and why reviews were requested. Centrality could mean expertise, imposed approval policy, understaffing, or accidental ownership. Use aggregate system diagnosis, obtain context from affected people, minimize and protect data, and change the system—such as distributing knowledge or removing needless approval—without converting the signal into an individual productivity score.

**Conclusion.** Socio-technical telemetry supports humane system inquiry, not surveillance or causal claims about a person.

### Example 8

**Situation.** A platform team offers a deployment service to twenty product teams, so strict mirroring would appear to demand twenty platform copies.

**Reasoning.** The dependency can be managed through a stable self-service interface, compatibility policy, paved path, support boundary, and product feedback loop. Rare joint discovery uses temporary collaboration; routine consumption does not require reporting-line mirroring. If every adoption needs bespoke platform work, the interface or platform product boundary is not yet effective.

**Conclusion.** A service relationship can deliberately avoid structural mirroring when the interface and operating model actually absorb coordination.

### Example 9

**Situation.** After teams are reorganized around customer journeys, lead time improves but incidents take longer to resolve.

**Reasoning.** The intervention internalized feature decisions but fragmented runtime expertise and shared dependency response. Add federated incident roles, common telemetry, rehearsed cross-team response, and explicit platform escalation. Preserve journey ownership while repairing exceptional-mode coordination. Evaluate both normal delivery and degraded operation; optimizing one mode was insufficient.

**Conclusion.** Organizational congruence is mode-dependent, and end-to-end architecture review must include incidents and recovery.

### Example 10

**Situation.** A hospital wants teams aligned to patient journeys, but medication safety, privacy, device integration, clinical operations, and procurement cross those journeys.

**Reasoning.** Define accountable journey teams without claiming sole clinical authority. Retain hospital-governed safety and privacy objectives, shared medication and identity semantics, specialist enabling relationships, independent assurance, and escalation. Pilot one low-risk workflow with clinicians and affected staff; record workload, safety events, handoffs, recovery, access, and patient impact. Do not infer clinical validity from software flow or reorganize regulated responsibilities through architecture alone.

**Conclusion.** In safety-critical socio-technical systems, team alignment must preserve professional, legal, operational, and patient authority beyond software boundaries.

## Cross-Program Connections

- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) owns reusable design-pattern forces; organization is context, not another software pattern catalog.
- [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns delivery flow, production operations, incident practice, and reliability evidence affected by team boundaries.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns data-domain authority and governance; a team restructure does not transfer data meaning automatically.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) owns broader socio-technical boundaries, lifecycle authority, human factors, and validation in operational context.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns protocol contracts and service interaction mechanics that can reduce repeated cross-team coordination.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns platform-as-product and consuming-team relationships; a platform boundary is judged by user outcomes, not centralization alone.

## References

1. Melvin E. Conway, [“How Do Committees Invent?”](https://melconway.com/Home/pdf/committees.pdf), *Datamation* 14(4), 1968. Original statement and communication-constraint argument; author-hosted copy checked 2026-09-06.
2. David L. Parnas, [“On the Criteria To Be Used in Decomposing Systems into Modules”](https://doi.org/10.1145/361598.361623), *Communications of the ACM* 15(12), 1972. Primary source on information-hiding decomposition and responsibility-bearing modules.
3. James D. Herbsleb and Rebecca E. Grinter, [“Architectures, Coordination, and Distance: Conway's Law and Beyond”](https://herbsleb.org/web-pubs/pdfs/herbsleb-architectures-1999.pdf), *IEEE Software* 16(5), 1999. Empirical account of distributed coordination and the limits of architecture alone.
4. James D. Herbsleb and Rebecca E. Grinter, [“Splitting the Organization and Integrating the Code: Conway's Law Revisited”](https://doi.org/10.1145/302405.302455), *ICSE '99*, 1999. Primary case study of cross-site integration and coordination.
5. Marcelo Cataldo, James D. Herbsleb, and Kathleen M. Carley, [“Socio-Technical Congruence: A Framework for Assessing the Impact of Technical and Work Dependencies on Software Development Productivity”](https://herbsleb.org/web-pubs/pdfs/cataldo-socio-2008.pdf), *ESEM '08*, 2008. Primary framework and empirical study of coordination requirements and observed coordination.
6. Alan MacCormack, John Rusnak, and Carliss Y. Baldwin, [“Exploring the Duality between Product and Organizational Architectures: A Test of the Mirroring Hypothesis”](https://doi.org/10.1016/j.respol.2012.04.011), *Research Policy* 41(8), 2012. Matched-product empirical study of organizational form and software modularity.
7. Lyra J. Colfer and Carliss Y. Baldwin, [“The Mirroring Hypothesis: Theory, Evidence, and Exceptions”](https://doi.org/10.1093/icc/dtw027), *Industrial and Corporate Change* 25(5), 2016. Review of 142 empirical studies and explicit treatment of exceptions and partial mirroring.
8. Nachiappan Nagappan, Brendan Murphy, and Victor Basili, [“The Influence of Organizational Structure on Software Quality: An Empirical Case Study”](https://doi.org/10.1145/1368088.1368160), *ICSE '08*, 2008. Primary study relating organizational measures to post-release failure proneness in one setting.
9. Ruth E. Kraut and Lynn A. Streeter, [“Coordination in Software Development”](https://doi.org/10.1145/203330.203345), *Communications of the ACM* 38(3), 1995. Empirical study of coordination mechanisms across project scale and uncertainty.
10. Karl E. Weick, *Sensemaking in Organizations*, Sage, 1995. Foundational treatment of organizational sensemaking used to distinguish channels from shared interpretation.
11. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021. Architecture structures, quality attributes, stakeholders, and organizational context.
12. ISO/IEC/IEEE, [ISO/IEC/IEEE 42010:2022 — Software, Systems and Enterprise — Architecture Description](https://www.iso.org/standard/74393.html), 2nd ed., published November 2022. Official current record checked 2026-09-06; organizational and social influences are among architecture concerns, while the standard does not prescribe an organization design method.

## Exercises

### Exercise 1

Distinguish a technical dependency, work dependency, communication path, authority relationship, and reporting relationship using one two-team example.

### Exercise 2

Three team pairs have coordination needs $8$, $5$, and $3$, with demonstrated capabilities $0.75$, $0.2$, and $1.0$. Compute residual exposure $U$. If the second capability rises to $0.8$, compute the new value and the reduction. State what the calculation does not prove.

### Exercise 3

A customer-notification change requires synchronized edits in order, preference, template, and delivery services owned by four teams. Releases frequently block at integration, yet runtime traces show only order calling delivery. Diagnose missing dependency evidence and propose a bounded intervention with measures.

### Exercise 4

Compare reorganizing teams before refactoring with refactoring before reorganizing for a shared-database monolith. Recommend a sequence under high operational risk and explain transition ownership.

### Exercise 5

A national emergency-alert capability spans government agencies, telecom operators, device vendors, accessibility experts, local responders, and platform teams. Apply the chapter's method without assuming one enterprise can reorganize all parties. Specify boundaries, coordination mechanisms, evidence, and ethical limits.

## Answers to the Exercises

### Answer 1

Suppose checkout needs a fraud decision. The runtime call from checkout to risk is a **technical dependency**. Updating the decision schema and rollout sequence creates a **work dependency** between the teams. A joint version review and incident channel are **communication paths**. The risk owner may have **authority** to approve decision semantics while checkout owns presentation and fallback. Each team's manager defines a **reporting relationship**, which need not connect the two engineers. A complete answer keeps these structures distinct and notes that one observed relationship is only partial evidence of the others.

### Answer 2

Initially,

$$
U=8(1-0.75)+5(1-0.2)+3(1-1)=2+4+0=6.
$$

After the second capability rises to $0.8$,

$$
U'=2+5(0.2)+0=3,
$$

so modeled residual exposure falls by $3$. This proves only the arithmetic under the chosen needs, capability scores, pairs, and time window. It does not prove causal productivity improvement, measurement validity, cost-effectiveness, good working conditions, architecture quality, or transfer to another organization.

### Answer 3

The runtime graph misses logical and lifecycle dependencies: shared event meaning, preference and consent semantics, template variables, localization, delivery guarantees, retry and deduplication, release compatibility, monitoring, and recovery. Examine co-change history, blocked work, schema and event contracts, incidents, deployment coupling, decision records, and interviews. A bounded intervention could give one cross-functional group temporary ownership of a single notification journey, define one versioned message contract and conformance suite, and assign explicit semantic authorities. Measure blocked time, handoffs, change fan-out, contract failures, lead time, delivery correctness, and incident recovery before and after. The group exits when routine changes proceed through the tested contract; persistent collaboration is evidence that the boundary remains unstable.

### Answer 4

Reorganizing first can align authority and build shared context, but code, database, on-call, and deployment coupling remain. Refactoring first can expose a seam, but existing component teams may lack end-to-end authority and may recreate the old boundary. Under high operational risk, form a bounded transition group drawn from current owners, map dependencies and authority, add observability and recovery tests, and extract one reversible seam. Assign a durable receiving team, but keep the current owner jointly accountable until that team independently deploys, operates, restores, and rolls back the slice. Then retire obsolete access and duplicated duties. This sequence changes social and technical edges incrementally and preserves continuity.

### Answer 5

Treat the alert network as a federated socio-technical system rather than one reorganizable firm. Model message, identity, localization, accessibility, delivery, acknowledgment, security, and operational dependencies across legally independent authorities. Name decision rights for alert initiation, geographic scope, content, translation, transport, device behavior, local response, incident command, and public correction. Use statutory or contractual interfaces, common profiles, versioned conformance suites, joint exercises, liaison paths, interoperable telemetry, and emergency escalation while allowing each constituent to retain internal organization. Evidence must cover representative devices and networks, congestion, partial failure, multilingual and accessible delivery, false and missed alerts, recovery, auditability, and exercises with responders and affected communities. Minimize personnel and citizen data; do not use communication telemetry for worker scoring; preserve accessibility, civil-rights, labor, privacy, security, and public-accountability review. Software delivery evidence alone cannot authorize an alert or establish public safety.
