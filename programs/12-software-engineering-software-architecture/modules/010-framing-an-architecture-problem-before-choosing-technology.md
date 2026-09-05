---
module_id: SARCH-010
program: Software Engineering: Software Architecture
level: 1
module_number: 10
title: Framing an Architecture Problem Before Choosing Technology
status: complete
last_verified: 2026-09-05
---

# Framing an Architecture Problem Before Choosing Technology

## One-Page Review

### Governing question

How can a team define the system, outcomes, stakeholders, drivers, constraints, uncertainty, and decision boundaries before products and fashionable styles narrow the solution space?

### Essential definitions

- A **problem frame** is a bounded, evidence-linked description of the situation architecture must address.
- The **system of interest** is the entity whose responsibilities and architecture are being decided.
- A **desired outcome** is an externally meaningful result, distinct from a requested feature or technology.
- A **driver** is a goal, requirement, constraint, risk, or quality scenario significant enough to shape architecture.
- A **solution hypothesis** is a candidate mechanism whose fitness remains to be tested.
- **premature solutioning** occurs when a mechanism is adopted before the relevant problem and evaluation conditions are understood.
- A **decision boundary** states what must be decided now, what can remain local, and what should be deferred pending evidence.
- A **framing assumption** is a falsifiable proposition that defines the problem while evidence remains incomplete.

### Central model, mechanism, or theorem

Create a frame

$$
F=(entity,purpose,scope,stakeholders,outcomes,scenarios,drivers,constraints,assumptions,risks,evidence,authority,horizon).
$$

Then state the decision question without embedding a product or style. Generate multiple coherent alternatives only after the frame is reviewable. Technology is admissible as a hard constraint only when an authoritative source, scope, rationale, effective period, and exception process exist; otherwise it is context or a hypothesis to evaluate.

### Critical invariants

- name one system of interest, purpose, lifecycle stage, and decision horizon;
- define in-scope outcomes, exclusions, actors, neighbors, and ownership gaps;
- trace drivers to legitimate sources and authorities;
- operationalize material qualities as contextual scenarios;
- separate constraints, assumptions, risks, issues, and preferences;
- state current evidence, uncertainty, and what would falsify the frame;
- include operation, failure, migration, security, data, cost, and retirement as applicable;
- express the decision as a question with more than one credible answer;
- defer reversible local choices and preserve option value;
- record the frame, decision, evidence, and reopening triggers.

### Common failures

Common failures include beginning with “which cloud”; treating a product name as scope; accepting stakeholder requests as normalized requirements; copying quality adjectives; hiding an inherited stack as a mandate; drawing components before context; optimizing one happy path; ignoring current-to-target transition; estimating cost without workload or horizon; holding vendor demos before evaluation criteria; demanding technology neutrality when a genuine constraint exists; and framing so broadly that one chapter or team cannot decide it.

### Compact example

“We need Kafka” embeds a mechanism. A useful frame asks: how should independent producers submit up to a declared burst of durable events so consumers can process, replay, evolve schemas, and recover within specified ordering, latency, privacy, and cost constraints? It records producer and consumer ownership, failure scenarios, staffing, current traffic, growth assumptions, migration, and evidence. A log broker, queue, database outbox, synchronous API, batch transfer, or hybrid can then be evaluated honestly.

### Connections

[SARCH-002](002-stakeholders-and-architectural-concerns.md) through [SARCH-009](009-architecture-decision-records.md) supply every part of the frame: stakeholders, context, quality drivers, constraints, assumptions, risks, ASRs, trade-offs, decision reach, and durable records. SARCH-011 onward applies the frame to concrete quality tactics and architectural structures.

## Governing Question

Teams are often asked to “design a microservices platform,” “move to cloud,” or “adopt event-driven architecture.” These phrases contain candidate solutions but omit the outcomes, boundaries, constraints, uncertainties, and evidence needed to decide whether the solution is appropriate.

The governing question is how to transform a solution-shaped request into a reviewable architecture problem without discarding legitimate intent or authoritative constraints. The result must be narrow enough to decide, broad enough to expose system consequences, and explicit about what remains unknown.

## Why This Matters

Early framing determines which alternatives become visible. If the frame assumes services, containers, or one supplier, trade studies merely select details inside an unexamined commitment. Teams then rationalize sunk costs, overlook simpler options, and discover operational or data consequences after migration begins.

Framing also prevents endless analysis. By naming the decision horizon, evidence threshold, reversibility, and authority, the team can decide what must be known now and what can be learned through implementation. Good framing preserves options without demanding perfect foresight.

The frame becomes a shared contract among product, architecture, engineering, operations, security, data, finance, legal, suppliers, and affected users. It exposes differences in terminology and authority before they become incompatible systems.

## Prerequisites and Retrieval

Retrieve system of interest, stakeholder, concern, capability, context, interface, quality-attribute scenario, constraint, assumption, risk, issue, ASR, trade-off, alternative, architecture decision, evidence, verification, validation, authority, lifecycle, and option value.

From the preceding modules, retrieve known-inventory limits, responsibility boundaries, scenario anatomy, constraint pedigree, falsifiable assumptions, causal risk statements, significance profiles, dominance and sensitivity, architecture-versus-detail classification, and ADR lifecycle. This module integrates those concepts rather than replacing them.

## Learning Objectives

After completing this module, you should be able to:

1. transform a technology request into an outcome- and decision-centered problem;
2. name a precise entity, purpose, scope, lifecycle stage, and horizon;
3. assemble stakeholders, scenarios, drivers, constraints, assumptions, risks, and evidence;
4. distinguish genuine technology constraints from inherited context and preferences;
5. bound a problem so a responsible authority can decide it;
6. identify missing evidence and design early learning;
7. generate coherent alternatives without straw candidates;
8. include transition, operation, failure, data, security, and retirement;
9. define stop, defer, escalate, and reopen conditions;
10. preserve the problem frame and decision rationale durably.

## Core Exposition

**Recover intent from solution language.** When someone says “use microservices,” preserve the statement, source, and rationale. Ask what change or failure it addresses: independent releases, ownership, scale, fault isolation, technology diversity, acquisition, or organizational growth. Each answer implies different scenarios and may support different solutions.

Do not punish stakeholders for proposing technology. Their request contains experience and concern. Separate the raw request from normalized outcomes and candidate mechanisms so no information is erased and no mechanism gains unearned authority.

**Name the entity and purpose.** “Customer platform” might be a business domain, capability portfolio, product, service, data estate, or team. State the system of interest, users and affected parties, lifecycle stage, and externally observable purpose. Create related frames when several abstraction levels matter instead of mixing enterprise strategy and component design.

Define in-scope responsibilities, explicit exclusions, external neighbors, shared ownership, and unresolved boundaries. A useful frame explains who owns the end-to-end result and where authority changes. It does not require an internal component diagram yet.

**Describe outcomes and scenarios.** Start with what people or surrounding systems must accomplish and what loss must be prevented. Trace normal, peak, rejected, degraded, attacked, recovery, administrative, migration, audit, and retirement paths. State environment, workload, response, measure, and consequence.

Avoid quality adjectives without conditions. “Scalable and secure” is not enough to evaluate alternatives. State demand dimensions, data and threat boundaries, latency or throughput outcomes, authorization, failure, detection, recovery, and evidence. Use numbers only when their population, horizon, units, and uncertainty are defensible.

**Establish driver pedigree.** Link business and mission goals, stakeholder concerns, functional and quality requirements, constraints, assumptions, and risks. Identify the source and authority of each. Separate must satisfy from prefer, and separate current issues from uncertain events.

Create a small architecturally significant driver set while preserving the full authoritative requirement inventory. Explain why each driver changes broad or difficult-to-reverse decisions. Conflicting drivers are part of the frame, not defects to hide.

**Challenge constraints.** For every claimed mandate, ask who imposed it, what scope and time it covers, why it exists, how conformance is shown, and what exception or change process applies. “We run on AWS” is context. “The executed contract requires workload X to use AWS region Y through 2028” can be a constraint. The difference determines the feasible set.

Technology neutrality is not an absolute virtue. Ignoring a true interoperability, certification, skills, licensing, physical, supplier, or policy constraint creates fictional alternatives. The goal is solution honesty, not vocabulary purity.

**Make uncertainty actionable.** Record assumptions as propositions with owners, evidence, confidence, deadlines, false impacts, and triggers. Record risks as condition-event-consequence chains with treatment and authority. Identify the next irreversible decision and validate high-impact assumptions before crossing it.

Use spikes, prototypes, load or fault experiments, contract and source review, traffic analysis, user research, operational observation, and supplier clarification to retire named uncertainties. An experiment should answer a framing question, not showcase a favored tool.

**Bound the decision.** State what must be selected now, what remains implementation detail, what can be deferred, and when. A frame for “service integration” may decide interaction semantics, responsibility, failure, and evolution without deciding a broker product. Deferral preserves option value only if interfaces and evidence obligations support later choice.

Avoid frames so broad that all architecture is one decision. Split independent choices by authority and change timeline, then record dependencies. Conversely, do not split away end-to-end outcomes until no owner remains.

**Generate coherent alternatives.** Include a real status quo, at least one materially different option when feasible, and hybrids or staged paths where they preserve learning. Describe responsibility, data, runtime, deployment, failure, operation, migration, skills, cost, and exit at comparable fidelity. Reject only against explicit constraints or evidence.

Do not select with slogans. “Managed service” varies by configuration and contract; “monolith” varies by modularity and deployment; “event-driven” varies by authority, delivery, ordering, and recovery. Alternatives must be concrete enough to evaluate the framed scenarios.

**Include transition and lifecycle.** Current and target designs do not compose automatically. Model dual running, routing, data migration, compatibility, rollback, staffing, supplier overlap, security access, monitoring, and retirement. A target that is excellent at steady state may be infeasible to reach safely.

Compare build, operate, change, incident, compliance, and exit costs across the decision horizon. Preserve long-lived data, contracts, skills, and evidence. Do not assume the team or supplier remains unchanged.

**Review and decide under authority.** Ask stakeholders to challenge boundaries, drivers, constraints, measures, assumptions, alternatives, and missing evidence. Operations, security, privacy, data, finance, accessibility, support, and suppliers should inspect their relevant consequences. Qualified domain authorities retain high-consequence decisions.

Record the final frame with the ADR or linked analysis. If evidence is insufficient, narrow the claim, choose a reversible step, or report the blocker. After implementation, compare observed consequences with predictions and reopen the frame when triggers fire.

## Definitions and Notation

Define the problem frame

$$
F=(E,P,B,S,O,Q,D,C,A,R,X,H),
$$

where $E$ is entity, $P$ purpose, $B$ boundary, $S$ stakeholders, $O$ outcomes, $Q$ scenarios, $D$ drivers, $C$ constraints, $A$ assumptions, $R$ risks, $X$ evidence, and $H$ decision horizon and authority context.

Let $Alt(F)$ be coherent alternatives generated for the frame and

$$
Feasible(F)=\{a\in Alt(F):a\text{ satisfies every applicable hard constraint in }C\}.
$$

Feasibility depends on interpretations and evidence. An empty feasible set can indicate contradictory constraints, incomplete alternatives, or a misframed boundary; it does not authorize silent constraint relaxation.

Let $Open(F)$ be unresolved facts whose plausible values can change feasibility, ranking, or risk acceptance. A frame is decision-ready under policy $p$ when every item in $Open(F)$ is resolved, explicitly tolerated under authority, or addressed by a reversible decision and learning plan. Decision-ready does not mean complete knowledge.

Trace relations connect $O\leftarrow S$, $Q\leftarrow O$, $D\leftarrow Q$, alternatives to $D$, and evidence to assumptions and predicted outcomes. Link direction should be semantically documented; mere graph connectivity is insufficient.

## Mechanisms, Invariants, or Proof Structure

Use this framing mechanism.

1. **Preserve the request:** record original solution language, source, and rationale.
2. **Name entity and purpose:** define system, lifecycle, outcome, and decision horizon.
3. **Set context and boundary:** identify actors, neighbors, authorities, responsibilities, exclusions, and ownership gaps.
4. **Elicit scenarios:** cover normal, boundary, degraded, adversarial, recovery, transition, and retirement behavior.
5. **Establish drivers:** trace goals, ASRs, constraints, assumptions, risks, and issues to sources.
6. **Challenge premises:** test constraint authority and make uncertainty falsifiable.
7. **Bound the decision:** distinguish now, deferred, delegated, and escalated choices.
8. **Generate alternatives:** construct status quo, materially different, hybrid, and staged candidates at comparable fidelity.
9. **Plan evidence and review:** target uncertainties, stakeholders, qualities, lifecycle, and qualified authority.
10. **Decide and revisit:** record rationale, consequences, residual risk, implementation confirmation, and triggers.

The governing invariants are preserved source intent, explicit system and purpose, owned boundary, contextual scenarios, authoritative drivers, honest uncertainty, technology-neutral decision question except for proven constraints, coherent alternatives, lifecycle feasibility, legitimate authority, and durable reopening.

A structurally complete frame proves only that required fields exist. It cannot prove stakeholder discovery, requirement validity, constraint interpretation, alternative completeness, evidence accuracy, or architecture fitness.

## Alternatives and Trade-Offs

**Technology-neutral framing** broadens options and exposes intent but can ignore real standards, skills, contracts, or certifications. **Constraint-first framing** respects reality but can preserve accidental legacy choices. Test every constraint’s source, scope, and expiry.

**Broad discovery** reduces omission and reveals interactions but delays decision and increases coordination. **Narrow framing** accelerates learning but can externalize end-to-end consequences. Bound around one decision while retaining context links and explicit exclusions.

**Analysis before experimentation** avoids expensive irrelevant prototypes but relies on uncertain evidence. **Prototype-led discovery** reveals technical facts but anchors teams on the prototyped mechanism. State falsifiable questions and compare more than one credible mechanism where the decision warrants it.

**Early commitment** improves coordination and procurement but loses options. **Deferred commitment** preserves learning but can block dependent work or create accidental defaults. Use reversibility, option loss, evidence value, and cost of delay to decide timing.

## Failure Modes and Misconceptions

- **“The stakeholder asked for it, so it is a requirement.”** Preserve the request, then identify outcome, source, authority, and evidence.
- **“Technology-neutral means ignore constraints.”** Genuine standards, contracts, physical limits, and certifications belong in the frame.
- **“Current stack is mandatory.”** It is context until authority, scope, and exception rules prove constraint status.
- **“Draw components to understand the problem.”** Early sketches can explore hypotheses but must not silently define scope.
- **“Quality adjectives are drivers.”** They require scenarios, measures, environments, and consequences.
- **“More discovery always helps.”** Stop when the bounded decision has sufficient evidence under authorized risk tolerance.
- **“A prototype validates the architecture.”** It answers selected questions in a recorded environment.
- **“Vendor comparison is architecture analysis.”** Products are only part of coherent system and lifecycle alternatives.
- **“The target state is the plan.”** Transition, rollback, dual operation, and retirement require architecture.
- **“Cost is monthly infrastructure spend.”** Include people, delivery, incidents, migration, compliance, change, and exit.
- **“One frame covers the program.”** Independent decisions need bounded frames and linked records.
- **“Framing avoids decisions.”** It defines what must be decided, by whom, and with what evidence.
- **“Consensus grants authority.”** Legal, safety, security, financial, and mission acceptance may require named roles.
- **“Once decided, the frame is historical.”** Changed evidence or context must reopen it.

## Worked Examples

### Example 1

**Question:** Reframe “move the application to cloud.”

**Reasoning:** Identify desired outcomes: reduce recovery time, remove expiring hardware, support geographic demand, or change cost structure. Define workload, data residency, availability, skills, dependencies, contract horizon, migration deadline, current issues, and exit. Compare managed hosting, infrastructure cloud, software redesign, hybrid, and renewed on-premises service where feasible.

**Conclusion:** Cloud is an alternative family; the problem is the set of outcomes and constraints motivating change.

### Example 2

**Question:** Reframe “split the monolith into microservices.”

**Reasoning:** Ask which changes are slow, where ownership conflicts, what scale differs, and which failures need isolation. Measure coupling, deployment coordination, data authority, incidents, and team capability. Compare modularization, build improvements, selected extraction, and broader service decomposition, including migration and operations.

**Conclusion:** Service count is not the outcome; change and responsibility scenarios define the problem.

### Example 3

**Question:** When is “use protocol X” a legitimate starting constraint?

**Reasoning:** If an authoritative external interoperability standard or executed partner contract requires protocol X for a defined interface and period, record it as a constraint with version, interpretation, conformance, and exception process. Internal implementation and unrelated interfaces remain open.

**Conclusion:** Proven constraint scope narrows alternatives legitimately without turning one protocol into the entire architecture.

### Example 4

**Question:** How should a team frame “we need real-time analytics”?

**Reasoning:** Define who acts on which result, source-to-decision latency, event time, freshness, completeness, correction, volume, cost, and consequence of delay. “Real time” may mean 100 ms fraud blocking, five-minute operations response, or hourly planning. Alternatives differ after the threshold and authority are known.

**Conclusion:** Operational outcome and time semantics replace an ambiguous solution-driving phrase.

### Example 5

**Question:** A vendor demo processes one million events per second. What does it prove?

**Reasoning:** It proves reported behavior only for the vendor’s workload, configuration, hardware, data, and measurement. Compare with the framed event size, partition keys, ordering, durability, consumers, failures, privacy, cost, operations, and recovery. Reproduce a representative experiment if the uncertainty affects the decision.

**Conclusion:** Benchmark evidence is admissible only after mapping it to the problem frame.

### Example 6

**Question:** How can framing expose an infeasible requirement set?

**Reasoning:** Suppose a mobile workflow must remain fully functional during indefinite disconnection, use no local persistent data, and receive central authorization for every action. The conditions conflict. Record authorities and scenarios, explore bounded offline duration or limited actions, and escalate rather than choosing a technology that cannot make all premises true.

**Conclusion:** An empty feasible set is a finding, not permission to hide a requirement.

### Example 7

**Question:** What should be decided now for an event integration?

**Reasoning:** Decide event ownership, identity, semantics, ordering needs, delivery outcomes, privacy, schema evolution, failure, replay, and operational responsibility if these cross teams. Defer broker product, client library, and internal serialization when genuine constraints and evidence do not require them yet.

**Conclusion:** Decision boundaries preserve architectural coherence and local option value.

### Example 8

**Question:** Why include retirement in a new supplier decision?

**Reasoning:** Data export, semantic portability, credential revocation, callbacks, contracts, audit history, replacement overlap, and staff knowledge determine exit feasibility. A low entry price can create high irreversible cost. Make exit a scenario and include evidence before commitment.

**Conclusion:** Lifecycle framing prevents procurement from becoming hidden architecture lock-in.

### Example 9

**Question:** What if user research contradicts a latency assumption after design starts?

**Reasoning:** Update evidence, reopen affected quality scenarios, budgets, alternatives, and ADRs, and distinguish implementation conformance from problem validity. If users need a different feedback pattern rather than lower latency, a workflow change may outperform infrastructure investment.

**Conclusion:** Frames evolve from evidence; sunk design effort does not validate the premise.

### Example 10

**Question:** How should “use AI for emergency dispatch” be reframed?

**Reasoning:** Define advisory versus decision authority, incidents, data, populations, latency, uncertainty, failure, bias, explanation, override, security, monitoring, and fallback. Compare non-ML rules, workflow improvement, advisory models, and any automation boundary. No external emergency-services, safety, statistical, equity, regulatory, human-factors, cybersecurity, or practitioner review is claimed; named qualified authorities must validate the problem, evidence, harms, and residual risk.

**Conclusion:** High-consequence technology requests require outcome, authority, population, and failure framing before model selection.

## Cross-Program Connections

- [Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) supplies domain language, responsibility, invariants, and local solution exploration.
- [Software Engineering Methods & Evolution](../../10-software-engineering-methods-and-evolution/ROADMAP.md) provides discovery, iteration, hypothesis testing, and change governance.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) turns framing uncertainty into claim-specific experiments and validation.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) exposes data authority, lifecycle, lineage, residency, and migration constraints.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) develops assets, threats, trust, controls, and risk authority before product choice.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies problem definition, operational concepts, alternatives, trade studies, lifecycle, and technical authority.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) distinguishes internal platform outcomes from fashionable tool adoption.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 42010:2022, Software, systems and enterprise—Architecture description](https://www.iso.org/standard/74393.html), edition 2, November 2022. Current architecture-description concepts for entities, environments, stakeholders, concerns, viewpoints, decisions, rationale, and correspondence; consulted 2026-09-05.
2. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018, Systems and software engineering—Life cycle processes—Requirements engineering](https://www.iso.org/standard/72089.html), edition 2, November 2018. Requirements elicitation, analysis, characteristics, traceability, and lifecycle information; consulted 2026-09-05.
3. Paul Clements and Len Bass. [Relating Business Goals to Architecturally Significant Requirements for Software Systems](https://www.sei.cmu.edu/library/relating-business-goals-to-architecturally-significant-requirements-for-software-systems/), CMU/SEI-2010-TN-018, 2010. Business-goal pedigree and derivation of quality-attribute requirements.
4. Software Engineering Institute. [Quality Attribute Workshop Collection](https://www.sei.cmu.edu/library/quality-attribute-workshop-collection/), Carnegie Mellon University, 2016. Stakeholder-based discovery, prioritization, and refinement of architecture-critical scenarios; consulted 2026-09-05.
5. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*, fourth edition, Addison-Wesley, 2021. Business goals, drivers, quality scenarios, tactics, trade-offs, and evaluation.
6. Humberto Cervantes and Rick Kazman. *Designing Software Architectures: A Practical Approach*, Addison-Wesley, 2016. Iterative architecture design from drivers through structures, decisions, and analysis.
7. Michael Jackson. *Problem Frames: Analysing and Structuring Software Development Problems*, Addison-Wesley, 2001. Separation of problem-world phenomena, requirements, machine behavior, and solution structure.
8. Donald Gause and Gerald Weinberg. *Exploring Requirements: Quality Before Design*, Dorset House, 1989. Problem discovery, ambiguity, stakeholders, context, and alternatives before design commitment.

## Exercises

### Exercise 1

Reframe “replace the database with NoSQL” for a customer-account capability. Include outcome, context, drivers, constraints, assumptions, risks, evidence, and decision boundary.

### Exercise 2

Construct a decision-ready frame for processing image uploads during burst demand. Separate decisions needed now from reversible implementation detail.

### Exercise 3

Diagnose a proposal that begins with a vendor reference architecture, lists “fast, secure, scalable,” copies the current organization chart as boundaries, and compares only that vendor’s service tiers.

### Exercise 4

Compare early commitment and deferred commitment for a message broker. Define option value, cost of delay, learning experiments, and triggers.

### Exercise 5

Frame an unfamiliar remote floodgate-control architecture problem. Separate automated analysis, physical and operational evidence, qualified authority, and blockers.

## Answers to the Exercises

### Answer 1

Preserve the original request and rationale. Define the account system, authoritative customer facts, users and consumers, transaction and consistency requirements, workload and growth, latency, availability, recovery, privacy, residency, audit, schema change, operations, migration, and exit. Candidate drivers may be write contention, change coupling, regional availability, or cost; each needs evidence. Constraints include authoritative contracts and policies, not current product preference. Assumptions cover access patterns, scale, staff skills, and tolerance for staleness. Risks include migration loss, weakened invariants, supplier lock-in, and operational gaps.

The decision question can be: which data model, authority boundary, and storage topology best satisfy the declared scenarios over the horizon? Compare improving the relational design, partitioning, a document or key-value store, specialized read models, and hybrids. Decide authority, consistency, migration, and external semantics now if cross-boundary; defer internal indexes and client libraries where replaceable. “NoSQL” remains a solution family until this analysis selects a concrete option.

### Answer 2

Entity: authenticated image-ingestion capability. Outcomes: accept an eligible upload durably, reject invalid or unauthorized input clearly, produce derived representations, and expose status. Frame normal and burst arrival rates, size distributions, formats, malicious content, duplicate/retry behavior, privacy, retention, scan latency, processing deadline, downstream failure, cost, recovery, and user experience. Record traffic evidence and uncertainty.

Decide now: upload identity, acceptance boundary, authoritative state machine, size and security constraints, durable handoff, asynchronous versus synchronous responsibility, status semantics, retention, failure/retry, observability, and resource isolation. Candidate architectures include direct synchronous processing, durable object acceptance plus queued work, admission-controlled batch, and hybrid previews. Defer worker language, internal queue library, image algorithm, and most deployment detail if contracts and budgets preserve choice. Prototype representative parsing, malicious input, storage, burst, and failure questions before irreversible procurement or schema commitment.

### Answer 3

The vendor architecture anchors the solution and may omit system purpose, boundaries, alternatives, transition, ownership, and exit. Quality adjectives lack scenarios and measures. Organization charts describe communication structures, not necessarily capability, data, trust, runtime, or failure boundaries. Comparing service tiers cannot reveal whether another architecture or the status quo better solves the problem.

Recover stakeholder outcomes and consequences; define entity and context; discover ASRs; classify constraints, assumptions, risks, and issues; quantify only with scoped evidence; map multiple boundary lenses; and construct coherent status quo, vendor, alternative supplier, self-managed, hybrid, or nontechnical options where feasible. Include migration, operation, security, data, cost, skills, and retirement. Reuse the reference architecture later as evidence for one candidate, not as the frame.

### Answer 4

Early commitment can secure procurement, skills, interfaces, and delivery coordination, and can be necessary when broker semantics shape many producers and consumers. It loses leverage and options while workloads, ordering, recovery, and team capability remain uncertain. Deferred commitment preserves competition and allows learning, but dependent teams may invent incompatible defaults or delay delivery.

Decide stable event semantics, identity, ownership, failure, schema evolution, and evidence obligations first. Use small reproducible experiments for throughput shape, tail latency, partition behavior, replay, schema tooling, operations, and cost with at least credible alternatives. Encapsulate vendor-specific APIs where justified. Commit when the expected value of additional information is below delay and coordination cost or when a deadline is authoritative. Reopen on workload thresholds, unsupported semantics, operational evidence, supplier change, cost divergence, or contract expiry.

### Answer 5

Frame the physical water system, gate authority, upstream and downstream populations, operators, sensors, weather inputs, communications, power, mechanical limits, environmental and safety constraints, manual control, security, maintenance, fail-safe states, emergency operations, recovery, audit, and retirement. Scenarios include rising water, conflicting sensors, lost communications, power failure, jammed gate, malicious command, operator override, inaccessible site, and evacuation coordination. Separate advisory software, automated control, and legal operating authority.

Automated analysis can check model units, command/state invariants, timing budgets in specified models, configuration bounds, trace links, identity, and reproducibility. Physical models, calibrated sensors, hardware-in-the-loop tests, fault injection, site exercises, manual-operation drills, and observed operations provide bounded evidence. They cannot establish environmental model validity, hazard completeness, community impact, or acceptable residual risk alone. No external hydrology, civil engineering, environmental, safety, regulatory, human-factors, cybersecurity, or practitioner review is claimed. Named qualified authorities must own constraints, hazards, operating limits, validation, release, and risk acceptance. Unclear command authority, invalid physical assumptions, failed safe state, untested manual operation, or unresolved high-severity harm blocks the corresponding decision and readiness claim.
