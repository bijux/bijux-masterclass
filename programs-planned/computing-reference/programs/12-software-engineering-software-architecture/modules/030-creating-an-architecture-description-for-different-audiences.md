---
module_id: SARCH-030
program: Software Engineering: Software Architecture
level: 1
module_number: 30
title: Creating an Architecture Description for Different Audiences
status: complete
last_verified: 2026-09-06
---

# Creating an Architecture Description for Different Audiences

## One-Page Review

### Governing question

How can one governed architecture description help different audiences make different decisions without fragmenting into contradictory stories, hiding material risk, or forcing everyone through the same detail?

### Essential definitions

- An **architecture description** is a governed work product used to express an architecture through stakeholders, concerns, viewpoints, views, models, correspondences, decisions, rationale, and evidence.
- An **audience** is a class of intended users sharing a decision context; it is not a stereotype about a job title.
- A **stakeholder** has an interest in the system, while a **reader** consumes an artifact and a **decision authority** may accept risk, fund work, operate a control, or approve a change.
- A **concern** is a matter important to one or more stakeholders, such as recoverability, cost, data authority, or regulatory evidence.
- A **viewpoint** specifies conventions for constructing and using a view; a **view** expresses the architecture from that viewpoint for particular concerns.
- A **projection** selects, orders, explains, and sometimes redacts governed claims for an audience while preserving their meaning.
- A **claim** is an explicit proposition about the architecture; **evidence** supports a claim within stated scope, time, and limitations.
- A **correspondence** relates elements or claims across models, views, decisions, implementation, and evidence.
- **Progressive disclosure** reveals detail in layers so readers can stop when their decision is supported and navigate deeper when necessary.
- **semantic consistency** means audience projections do not make incompatible claims about the same subject, scope, and time unless the conflict is explicit.

### Central model, mechanism, or theorem

Represent the governed description as

$$
AD=(S,C,V,M,K,D,E,G),
$$

where $S$ is stakeholders and audiences, $C$ concerns and decisions, $V$ viewpoints and views, $M$ models, $K$ correspondences, $D$ decisions and rationale, $E$ evidence, and $G$ governance metadata. An audience projection $P_a(AD)$ selects material for audience $a$ according to its authorized decisions, concerns, expertise, urgency, and disclosure constraints.

Projection is not reinvention. If two projections state claims $q_1$ and $q_2$ about the same subject, scope, lifecycle state, and effective time, they must agree or expose the unresolved conflict.

### Critical invariants

- define audiences by decisions, responsibilities, expertise, urgency, and disclosure need;
- maintain one governed claim set with stable identifiers and multiple navigable projections;
- state purpose, audience, concern, scope, lifecycle state, owner, version, and freshness;
- put the requested decision, alternatives, consequences, risks, uncertainty, and evidence first;
- preserve important caveats when simplifying; brevity must not reverse or overstate a claim;
- distinguish intended architecture, deployed configuration, observed behavior, and proposed change;
- expose correspondences between summaries, diagrams, decisions, controls, code, operations, and evidence;
- use progressive disclosure rather than either one giant document or disconnected audience decks;
- apply least disclosure and redaction without hiding control ownership, residual risk, or evidence provenance from authorized readers;
- make terminology, acronyms, notation, navigation, contrast, language, and format accessible;
- test comprehension with representative readers and record misunderstandings;
- govern ownership, review triggers, supersession, retention, and removal of stale exports.

### Common failures

Common failures include one deck for everyone; role stereotypes instead of decision analysis; executive summaries that omit uncertainty; developer diagrams with no operational state; runbooks disconnected from design decisions; security appendices no one can trace; unexplained acronyms; color-only meaning; public documents leaking sensitive topology; over-redaction that prevents oversight; conflicting copied diagrams; silent changes of scope or environment; dashboards presented as architecture; and measuring document visits instead of comprehension.

### Compact example

An executive asks whether to accept a regional-outage risk, an operator asks how traffic fails over, and a developer asks which state crosses regions. Use one stable decision and model set. The executive projection leads with options, business impact, residual risk, cost, owner, and evidence limits. The operational projection adds triggers, state, dependencies, signals, authority, and recovery. The developer projection adds interfaces, data ownership, replication semantics, and test obligations. Stable identifiers and correspondences keep all three statements consistent.

### Connections

[SARCH-002](002-stakeholders-and-architectural-concerns.md) identifies stakeholders and concerns; [SARCH-021](021-context-views.md) through [SARCH-029](029-c4-uml-and-informal-diagram-semantics.md) supply views and representation semantics. [SARCH-031](../ROADMAP.md) begins architectural styles. Software Engineering Methods, Systems Engineering, Security, Data Architecture, Delivery and Reliability, and Human-Computer Interaction deepen participation, assurance, operations, information, and accessibility.

## Governing Question

Architecture descriptions serve action, not merely storage. A board member deciding investment, a developer changing an interface, an operator responding at 03:00, a security reviewer tracing a trust boundary, and a regulator examining evidence need different routes through the same architecture. Their vocabulary, time budget, authority, and acceptable disclosure differ.

The governing problem is therefore not how to create a separate truth for every role. It is how to preserve one governed body of claims while producing audience-appropriate projections that are understandable, sufficient for the decision, traceable to deeper material, and honest about uncertainty.

## Why This Matters

Bad audience design causes architectural failure even when the underlying model is sound. A terse leadership slide can turn a conditional recovery claim into a guarantee. A developer portal can describe an intended dependency after production has diverged. A security document can reveal exploitable topology to unauthorized readers. A runbook can be technically correct yet unusable under time pressure.

Conversely, adding everything to one document does not create transparency. It increases search cost, hides consequential facts among irrelevant detail, and encourages readers to construct their own inconsistent summaries. A durable description provides several deliberate entry points, shared identifiers, explicit scope, and a path from decision to evidence.

Audience adaptation is an architectural responsibility because communication changes what organizations build, approve, operate, and govern. The quality criterion is decision fitness with semantic integrity—not page count, graphical polish, or universal agreement.

## Prerequisites and Retrieval

Retrieve stakeholder, concern, decision authority, viewpoint, view, model kind, model, architecture decision record, quality-attribute scenario, correspondence, conformance, evidence, uncertainty, lifecycle state, environment, system boundary, trust boundary, failure domain, data authority, interface, deployment unit, observability, runbook, accessibility, confidentiality, and least privilege.

From SARCH-021–029, retrieve context, module, component-and-connector, runtime, deployment, information, development/build, and operational views, plus the distinction between model semantics and visual notation. From SARCH-002, retrieve the rule that job titles do not determine concerns: stakeholders must be discovered and their decision contexts validated.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish stakeholder, audience, reader, contributor, reviewer, and decision authority;
2. derive an audience profile from decisions, concerns, expertise, urgency, and disclosure constraints;
3. construct a governed architecture-description map rather than disconnected documents;
4. create executive, engineering, operational, security, data, assurance, and public projections;
5. preserve claim meaning, uncertainty, scope, and time across levels of detail;
6. use progressive disclosure, stable identifiers, glossaries, indexes, and correspondences;
7. quantify declared concern coverage without mistaking it for truth or comprehension;
8. design redaction and access control that preserve accountable oversight;
9. review accessibility, localization, freshness, and incident-time usability;
10. test whether representative audiences can make the intended decision correctly.

## Core Exposition

**Start with decisions, not document formats.** “Executives need slides” and “developers need diagrams” are stereotypes. Ask what decision must be made, who owns it, what consequences follow, what prior knowledge is reasonable, how much time is available, what uncertainty matters, and what information the reader may access.

An engineering manager approving a dependency may need cost and delivery impact; a chief executive accepting systemic risk may need the same evidence at a different aggregation level. An on-call developer during an incident is a different audience from the same developer planning a refactoring. Audience is contextual, not a permanent property of a person.

**Create an audience profile.** For each important decision, record the responsible authority, consulted stakeholders, decision horizon, urgency, required concepts, tolerable detail, preferred navigation, accessibility needs, language needs, confidentiality, expected evidence, and escalation route. Validate the profile with representative people instead of guessing.

Use names such as “incident commander deciding regional isolation” rather than “operations.” The first identifies action and context; the second contains many incompatible needs. Do not confuse influence with legitimacy: low-power users can have safety, accessibility, privacy, or labor concerns that the architecture must address.

**Build one description map.** ISO/IEC/IEEE 42010:2022 describes architecture descriptions in terms of stakeholders, concerns, viewpoints, views, model kinds, correspondences, and conventions [1]. Treat those relationships as a navigable graph. The description may span Markdown, model repositories, decision records, interface definitions, runbooks, control evidence, and generated views, but it needs declared authority and links.

Each durable claim receives a stable identifier when traceability matters. For example, `CLAIM-REC-014` may state that regional failover preserves acknowledged orders under assumptions A1–A4. Executive, operational, developer, and audit projections reference it rather than paraphrasing incompatible promises. Its evidence identifies test date, environment, result, and limits.

**Separate source from projection.** The governed model and claim set are sources. A projection chooses material for a decision and teaches enough vocabulary to use it. A projection can reorder, aggregate, translate, annotate, and redact. It must not silently change modality: “is intended to,” “was observed to,” “shall,” and “is guaranteed to” are different claims.

Do not assume one physical repository file is the only possible source of truth. Different model kinds may have different authoritative sources. Declare which artifact owns system identity, interface schemas, runtime placement, controls, or decisions, and govern correspondences among them. “Single source of truth” without bounded ownership usually hides conflicts rather than resolving them.

**Lead with the decision.** Every audience entry point should state: why the reader is here; the question or decision; the recommended or current position; alternatives; material consequences; risks and uncertainty; responsible owner; effective scope and time; and where to inspect detail and evidence.

The order matters. An executive should not have to decode twenty component boxes to learn that an option creates an unrehearsed recovery dependency. An engineer should not have to infer interface ownership from a funding summary. The projection foregrounds the material chain for its decision while preserving navigation to common facts.

**Use progressive disclosure.** A useful description often has four layers: an orientation page; concern-specific summaries; precise views and decisions; and evidence or implementation details. Each layer stands alone enough to answer its bounded questions and links to the next.

Progressive disclosure is not progressive distortion. A top-level statement should be a conservative abstraction of deeper material. If the evidence supports recovery in 20 minutes for one tested failure under four assumptions, the summary cannot say “zero downtime.” Preserve assumptions that would change the decision.

**Design executive and portfolio projections.** Leadership material frames outcomes, strategic constraints, alternatives, cost ranges, opportunity cost, quality consequences, risk owners, reversible versus irreversible choices, leading indicators, and decision deadlines. Use architecture vocabulary only where it distinguishes options.

Quantification needs provenance. A number such as “99.95% availability” must identify the service boundary, measurement window, exclusions, data source, and whether it is a target or observation. Traffic-light colors require labels, thresholds, trend, and uncertainty. A green status is not an architectural argument.

**Design developer and maintainer projections.** Developers need responsibility boundaries, stable terminology, module and runtime structures, interfaces and compatibility, state ownership, invariants, failure behavior, security obligations, local development paths, build/release relationships, decisions, and tests.

Start from the change a maintainer makes. Link a component identifier to its repository location, owners, interface contract, deployment unit, operational signals, and decisions. Avoid a portal that says only what the happy path does. Maintenance decisions depend on concurrency, retries, migration, rollback, deprecation, and failure boundaries.

**Design operational projections.** Operators need live and intended topology, dependencies, failure domains, states, health signals, symptoms, diagnostic paths, automation, safe actions, authorization, escalation, rollback or recovery, and known evidence limits. SARCH-028 explains the underlying operational view.

During an incident, time and cognition are constrained. Provide concise entry pages keyed by symptom and service, then link to detailed models and procedures. Mark dangerous actions, prerequisites, stop conditions, expected observations, and rollback. Distinguish a diagram of intended deployment from current inventory or observed traffic.

**Design security and privacy projections.** Security audiences need assets, actors, identities, trust boundaries, data classifications, flows, threat assumptions, attack surfaces, controls, control owners, residual risk, exceptions, and evidence. Privacy audiences also need purpose, lawful or authorized use, minimization, retention, subject rights, and data transfers where applicable.

Access differs by reader. A public overview may explain trust principles without exposing management endpoints. An internal reviewer may inspect boundaries and controls. A restricted assessor may need evidence and known vulnerabilities. Redaction is a governed transformation: identify what was withheld, by which policy, who can inspect it, and whether removal changes the apparent risk conclusion.

**Design data and analytics projections.** Data consumers and stewards need concepts, authoritative sources, lineage, transformations, freshness, quality rules, retention, access, privacy classification, reconciliation, and ownership. A product diagram that shows a database cylinder but omits system-of-record authority is insufficient.

Analytics readers may care about semantic definitions and delay more than transaction call paths. Operational readers may care about backlog, replay, duplicate handling, and correction. Use one data identity and lineage model to connect these projections; do not maintain separate names for the same measure without explicit mapping.

**Design assurance, procurement, and regulatory projections.** These audiences need obligations, claims, controls, evidence, supplier boundaries, exceptions, approvals, retention, provenance, and traceability. Organize by obligation and assurance question, not by the internal team chart.

A control matrix should point to architectural mechanisms and evidence, but a checked box is not proof that a control works. State evidence type, collection time, scope, reviewer, result, and limitation. For suppliers, distinguish contractual promise, design assumption, attestation, test result, and observed behavior.

**Design user, support, and public projections.** These readers may need system capabilities, data use, reliability expectations, degraded modes, accessibility behavior, support ownership, escalation, and planned change. Do not expose internal complexity merely to demonstrate sophistication.

Public transparency must remain truthful after simplification. Explain observable commitments and material limitations in plain language, offer alternate formats, and link to policy or assurance detail. Avoid terminology that requires an internal organization chart to decode.

**Design incident and emergency projections.** Incident audiences cross normal role boundaries. A commander needs authority, impact, options, dependencies, uncertainty, decision log, and communications. A responder needs diagnostic evidence and safe actions. Customer support needs externally observable effects and approved messages. Executives need consequences and escalation thresholds.

Prepare these routes before failure. Use stable service, dependency, control, and incident identifiers. Practice navigation in realistic drills. A description that works during a design review can fail under high urgency, partial tooling, low bandwidth, or an unavailable identity provider.

**Preserve semantic consistency.** Let each claim have a key containing subject, predicate, scope, lifecycle state, and effective interval. Two projections conflict if their keys overlap and their propositions cannot both hold. Difference in detail is allowed; contradiction is not.

For example, “orders are stored in region A” and “orders may fail over to region B” are compatible if one describes authority and the other a bounded recovery state. “Region A is the sole copy” conflicts with “region B holds a synchronous copy” for the same time and scope. Resolve or label the conflict rather than selecting whichever document looks newer.

**Use correspondence and provenance.** A summary claim should trace to a decision, relevant models, implementation ownership, and evidence. A model element should trace across context, runtime, deployment, data, build, and operational views where relevant. Correspondence does not require every artifact to expose every link; indexes can carry them.

Record derivation. A cost range may be computed from capacity assumptions. An availability statement may derive from a service-level objective and measurement. A security conclusion may depend on a threat model and test. Readers must be able to distinguish source data, interpretation, and decision.

**Measure declared coverage carefully.** Let $A$ be the set of audiences and $C_a$ the material concerns for audience $a$. Let $R\subseteq A\times C$ contain addressed pairs. Then

$$
coverage(a)=\frac{|\{c\in C_a:(a,c)\in R\}|}{|C_a|},\qquad |C_a|>0.
$$

This exposes omissions in a declared concern set. It does not prove the concerns are correct, claims true, explanation understood, or evidence sufficient. Empty concern sets are a discovery failure, not 100% coverage.

**Treat uncertainty as content.** State unknowns, disputed facts, untested conditions, confidence, sensitivity, and expiration. Distinguish risk probability from impact and evidence strength. Use ranges and scenarios where single values imply false precision.

Audience adaptation must not remove uncertainty merely because it is difficult to explain. Translate uncertainty into decision consequences: “failover has not been rehearsed at peak load, so accepting this launch date retains a material recovery risk.”

**Apply least disclosure without creating false assurance.** Classify models and evidence by sensitivity. Generate public, partner, internal, and restricted projections from governed content where practical. Redact secrets, exploit-enabling detail, personal data, and contractual restrictions.

Still preserve accountable facts: that a control exists or is absent, which authority owns it, whether evidence was reviewed, and where authorized reviewers can inspect it. Test redacted outputs for inference attacks and for misleading gaps. Removing a server name is different from hiding an unmitigated trust crossing.

**Make the description accessible.** WCAG 2.2 is a W3C Recommendation dated 5 October 2023 and provides current web-content accessibility criteria [4]. Architecture material should not rely on color, hover, fine pointer control, visual position, or images without text alternatives. Use semantic headings, descriptive links, captions, text equivalents, readable contrast, keyboard navigation, and meaningful reading order.

ISO 24495-1:2023 frames plain-language principles and guidelines [5]. Plain language does not remove necessary technical precision; it selects familiar terms, defines unavoidable terms, organizes around reader goals, and makes relations explicit. Maintain a governed glossary, expand acronyms on first use, and avoid synonyms for stable architectural identities.

**Localize meaning, not just words.** Translation can break abbreviations, labels, sorting, date formats, legal terms, and diagram layout. Separate translatable prose from stable identifiers. Ask domain-aware reviewers to inspect translated claims and warnings. Record source language, translation version, and unresolved ambiguity.

**Test comprehension.** Give representative readers a bounded task: identify the decision owner, trace a dependency, explain the failure effect, locate evidence, or choose an escalation. Observe what they infer without coaching. Record completion, errors, dangerous misunderstandings, terminology failures, and missing routes.

Document analytics may show reach but not understanding. A high visit count can reflect confusion. Survey confidence can be high while answers are wrong. Pair behavioral tasks with discussion, accessibility checks, and semantic review.

**Govern change and freshness.** Every projection needs an owner, authoritative sources, version, last-reviewed date, applicability, review triggers, and supersession path. Trigger review when architecture decisions, interfaces, deployments, controls, owners, evidence, or regulations change—not merely on a calendar.

Generated exports must identify their source revision. Remove or prominently mark stale copies. Links should fail visibly when targets disappear. Preserve prior versions when audit or decision history requires them, but prevent historical material from masquerading as current operational guidance.

**Review the whole description.** Review each audience projection for decision fitness, terminology, accessibility, disclosure, and comprehension. Review the shared system for consistency, correspondence, coverage, authority, freshness, and evidence. A projection may pass local review yet contradict another; a consistent corpus may still be unusable by its audience.

## Definitions and Notation

Let $AD=(S,C,V,M,K,D,E,G)$ be an architecture description. $S$ contains stakeholder and audience profiles; $C$ contains concerns and decision questions; $V$ contains viewpoints and views; $M$ contains models; $K$ contains correspondences; $D$ contains decisions, status, and rationale; $E$ contains evidence with provenance and limits; and $G$ contains owners, access, versions, review triggers, and supersession.

For audience $a$, define a context tuple

$$
a=(Q,U,X,T,L,F),
$$

where $Q$ is authorized decisions, $U$ concerns, $X$ expected expertise and vocabulary, $T$ time and urgency, $L$ disclosure limits, and $F$ format and accessibility needs. The projection function $P_a$ selects and presents material from $AD$ under that context.

A claim record is $q=(id,s,p,o,b,t,m,e)$: stable identity, subject, predicate, object, boundary or scope, effective time, modality, and evidence link. Modality distinguishes intended, required, proposed, observed, inferred, and guaranteed claims.

Let $material(a,q)$ mean claim $q$ could change an authorized decision or its risk assessment. Let $visible(a,q)$ mean the projection exposes $q$ or a faithful abstraction of it. Decision coverage requires $material(a,q)\Rightarrow visible(a,q)$ unless a documented disclosure rule redirects the authorized reader to a controlled source.

## Mechanisms, Invariants, or Proof Structure

**Projection-consistency invariant.** For projections $P_a$ and $P_b$, claims about the same subject, predicate, scope, lifecycle state, and overlapping time must be logically compatible or explicitly marked disputed. Different granularity is compatible when the coarser statement is entailed by the finer statement under declared assumptions.

**No-false-strengthening argument.** Suppose detailed claim $q$ says recovery succeeds within 20 minutes under assumptions $H$. A summary $q'$ saying recovery always succeeds within 20 minutes removes $H$ and has a strictly larger claimed domain. Evidence for $q$ therefore does not establish $q'$. Faithful summarization may retain $H$, narrow the scope, or weaken modality; it may not silently strengthen the claim.

**Materiality invariant.** If omitting a fact could reasonably change an authorized decision, residual-risk acceptance, safety action, or compliance conclusion, that fact or its controlled-access pointer is material. Short formats constrain presentation, not honesty.

**Traceability invariant.** A consequential summary claim has a stable identity and traces to its owner, decisions, relevant models, and evidence. A trace establishes provenance, not truth: the source may itself be wrong or stale.

**Freshness invariant.** Current guidance identifies applicability and source revision. When a review trigger fires, affected projections become suspect until reconciled. A recent timestamp without comparison to changed sources is weak evidence.

**Accessibility invariant.** Consequential meaning is recoverable without a single sensory channel, unexplained visual encoding, or undocumented acronym. Alternative formats preserve the claim and decision route, not merely decorative content.

**Disclosure invariant.** A projection exposes no information outside the audience's authorized disclosure boundary. Redaction must also preserve an honest account of control status and residual risk for the authorized decision.

**Declared-coverage calculation.** If an audience has eight material concerns and six are addressed, coverage is $6/8=75\%$. If one addressed item contains no evidence required by its decision contract, evidence-backed coverage is $5/8=62.5\%$. Neither value measures comprehension or correctness.

## Alternatives and Trade-Offs

**Single comprehensive document versus description map.** One document offers simple versioning and search but becomes dense, mixes access levels, and encourages irrelevant detail. A mapped corpus improves navigation and ownership but requires stable identifiers, indexes, link validation, and cross-artifact governance.

**Handwritten summaries versus generated projections.** Handwriting supports judgment, narrative, and nuanced risk. It also drifts. Generation improves repeatability and consistency for structured facts but can reproduce stale source data or produce unreadable output. Combine governed generation with human review and explicit non-generated interpretation.

**Role-based versus decision-based organization.** Role pages are easy to discover but roles vary between organizations and situations. Decision-based pages are more precise and durable but require careful indexing. Use decision routes with role and lifecycle entry points.

**Minimal disclosure versus broad transparency.** Minimal disclosure reduces security, privacy, and contractual exposure. Excessive restriction prevents challenge, creates duplicated unofficial diagrams, and weakens oversight. Classify at claim and evidence level, provide controlled review routes, and explain redactions.

**Formal notation versus plain explanation.** Formal models preserve precise semantics and support validation. They impose learning cost. Plain explanations reach more audiences but can hide ambiguity. Pair an accessible orientation with defined technical views and stable cross-references.

**Central ownership versus federated ownership.** A central architecture group can enforce consistency but becomes a bottleneck and loses local knowledge. Federated owners maintain domain accuracy but need shared identity, vocabulary, review, and escalation rules. Centralize governance conventions while assigning content ownership near the system.

**Calendar review versus event-driven review.** Calendar review catches quiet decay but may become ceremonial. Event triggers respond to actual change but miss unrecorded drift. Use both: change-triggered reconciliation plus risk-based periodic sampling.

## Failure Modes and Misconceptions

1. **“There is one universal audience.”** Readers make different decisions under different constraints.
2. **“A job title defines information need.”** Context, authority, urgency, expertise, and disclosure matter more.
3. **“An executive summary may omit caveats.”** Omitted material assumptions can turn evidence into a false guarantee.
4. **“More detail is more transparent.”** Unstructured volume can conceal material facts and increase misinterpretation.
5. **“Separate decks can be independently correct.”** Copied claims drift unless they share identity and correspondence.
6. **“A diagram speaks for itself.”** Scope, notation, lifecycle state, and relationship semantics must be declared.
7. **“Current dashboards are the architecture.”** Telemetry is bounded evidence about observed behavior, not the entire intended system.
8. **“Redaction only removes secrets.”** It can also remove context and create misleading assurance.
9. **“Restricted means ungoverned.”** Sensitive artifacts still need owners, freshness, review, and authorized oversight.
10. **“Plain language means imprecision.”** It removes avoidable complexity while preserving necessary distinctions.
11. **“Translation is word replacement.”** Domain meaning, warnings, layout, law, and identifiers require review.
12. **“Accessible means a text transcript exists.”** Navigation, structure, contrast, input, reading order, and equivalent meaning matter.
13. **“A visited document was understood.”** Reach, confidence, comprehension, and correct action are distinct measures.
14. **“A recent review date proves freshness.”** Review must reconcile the artifact with changed authoritative sources.
15. **“Traceability proves truth.”** It proves lineage; claims and evidence still require technical review.

## Worked Examples

### Example 1

**Situation.** A payments service has an executive investment decision, a developer migration decision, and an operator failover decision.

**Reasoning.** Create audience contexts keyed to each decision. All reference `PAY-BOUNDARY-01` and recovery claim `CLAIM-REC-014`. The executive route shows options, customer impact, cost, residual risk, and evidence limitations. The developer route shows data authority, interface compatibility, migration states, and tests. The operator route shows dependencies, signals, failover authority, actions, stop conditions, and rollback. Each identifies the same effective architecture revision.

**Conclusion.** Different routes can preserve one claim set while exposing decision-specific depth.

### Example 2

**Situation.** A leadership summary says, “The platform survives a regional outage,” while the test covered stateless traffic only.

**Reasoning.** The summary strengthened a bounded observation into a system-wide guarantee. Rewrite it: “In test `DR-2026-08`, stateless requests failed over within 12 minutes; stateful orders and peak load were outside scope.” State the decision consequence and link to assumptions, state replication, and unresolved risks.

**Conclusion.** Audience simplification may reduce detail but cannot enlarge evidence scope.

### Example 3

**Situation.** A developer view calls `Ledger` synchronously, while an operational view shows an event queue between the services.

**Reasoning.** Compare subject, lifecycle state, environment, and effective time. If the developer view is proposed and the operational view is deployed, label both and show the migration decision. If both claim current production, they conflict. Inspect interface definitions, deployment configuration, traces, and owners; correct the stale projection and record supersession.

**Conclusion.** Apparent cross-audience disagreement must be resolved by scope, time, and evidence—not presentation preference.

### Example 4

**Situation.** A public security overview removes hostnames but leaves a management endpoint, privileged workflow, and internal IP ranges visible.

**Reasoning.** Redaction must operate on sensitivity and inference, not string patterns. Classify elements and relationships, remove exploit-enabling topology, generalize control mechanisms, and test the output as an adversarial reader. Retain honest statements about authentication, administrative separation, residual risk, and the route for authorized assurance review.

**Conclusion.** Safe publication requires semantic redaction and an assurance-preserving projection.

### Example 5

**Situation.** An assessor asks how a retention obligation is implemented across six services.

**Reasoning.** Begin with the obligation and its interpretation. Trace it to data categories, authoritative stores, replicas, queues, backups, deletion mechanisms, owners, exceptions, and evidence. Distinguish design intent, configuration, executed test, and sampled production observation. Provide restricted evidence links rather than copying sensitive output into the overview.

**Conclusion.** Assurance audiences need claim-to-mechanism-to-evidence traceability, not a collection of team diagrams.

### Example 6

**Situation.** During an outage, responders spend twelve minutes locating the owner and cannot tell whether a failover command is reversible.

**Reasoning.** Create an incident entry page keyed by service and symptom. Put current authority, impact, dependencies, dangerous actions, prerequisites, expected observations, stop conditions, rollback, communications, and escalation first. Link to the deeper topology and decision. Drill with a read-only copy and record navigation and interpretation failures.

**Conclusion.** Incident architecture communication is a predesigned decision interface, not a normal document read faster.

### Example 7

**Situation.** An audience profile declares eight material concerns. Six appear in the projection, but one has no required evidence.

**Reasoning.** Declared concern coverage is $6/8=75\%$. Evidence-backed coverage is $5/8=62.5\%$. The missing concerns and evidence are explicit review findings. The denominator still depends on correct stakeholder discovery, and neither rate establishes comprehension, truth, or sufficient evidence quality.

**Conclusion.** Coverage metrics help locate omissions only when their bounded meaning is preserved.

### Example 8

**Situation.** A diagram uses red, amber, and green service boxes; the PDF is printed in grayscale and translated labels overflow.

**Reasoning.** Add text status, icons or patterns with defined meaning, sufficient contrast, semantic table equivalents, and a reading order. Separate stable service identifiers from translated names. Expand acronyms, allow label wrapping, and review the target-language rendering with domain-aware users. Do not rely on color or box position for status.

**Conclusion.** Accessible localization requires equivalent semantics and tested rendering, not literal translation.

### Example 9

**Situation.** A wiki, a slide deck, and a generated service catalogue show three owners for the same component.

**Reasoning.** Declare one bounded authoritative ownership source and a stable component identifier. Generate or link projections from it. Mark source revision and generation time, validate links, and retire stale exports. If operational escalation differs from code ownership, model two typed responsibilities instead of forcing one owner field.

**Conclusion.** Apparent duplication may conceal distinct responsibilities, but untyped copied ownership inevitably drifts.

### Example 10

**Situation.** A municipal flood-warning architecture must serve residents, dispatchers, sensor engineers, emergency managers, accessibility reviewers, and public auditors during degraded connectivity.

**Reasoning.** Create a plain-language public route for capability, data use, alert channels, limitations, and support; an accessible dispatcher route for authority, confidence, acknowledgment, and fallback; engineering views for sensor provenance, communication, state, and failure; management views for impact, options, and exercises; and assurance views for accessibility, privacy, retention, and evidence. Use printable and low-bandwidth formats, stable identifiers, controlled detail, and multilingual comprehension drills.

**Conclusion.** High-consequence descriptions require reconciled audience projections tested under realistic access, language, and urgency constraints.

## Cross-Program Connections

- **Software Engineering Methods:** participation, review, responsibility, and decision records shape audience discovery and governance.
- **Systems Engineering:** stakeholder needs, viewpoints, assurance cases, physical systems, hazards, and lifecycle baselines broaden description scope.
- **Software Delivery and Reliability Engineering:** runbooks, incident roles, service levels, telemetry, recovery, and operational evidence feed urgent projections.
- **Security Engineering:** classification, least privilege, threat models, control evidence, and inference risk govern disclosure.
- **Data Architecture:** semantics, authority, lineage, quality, retention, and stewardship shape data-audience routes.
- **Human-Computer Interaction:** information architecture, cognitive load, accessibility, localization, and comprehension testing shape usable descriptions.
- **API and Service Engineering:** interface contracts, compatibility, service ownership, and failure semantics connect developer and consumer views.
- **Platform Engineering:** portals and catalogues can generate projections, but their source coverage and freshness must remain explicit.
- **Testing and Quality Engineering:** task-based usability tests, link checks, conformance checks, and evidence review support bounded validation.

## References

1. ISO/IEC/IEEE, *ISO/IEC/IEEE 42010:2022 Software, systems and enterprise — Architecture description*, 2nd ed., November 2022. Official catalogue; current edition checked 2026-09-06. https://www.iso.org/standard/74393.html
2. Paul Clements et al., *Documenting Software Architectures: Views and Beyond*, 2nd ed., Addison-Wesley, 2010.
3. Nick Rozanski and Eoin Woods, *Software Systems Architecture: Working With Stakeholders Using Viewpoints and Perspectives*, 2nd ed., Addison-Wesley, 2011.
4. W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*, W3C Recommendation, 5 October 2023. Retrieved 2026-09-06. https://www.w3.org/TR/WCAG22/
5. ISO, *ISO 24495-1:2023 Plain language — Part 1: Governing principles and guidelines*, June 2023. Official catalogue checked 2026-09-06. https://www.iso.org/standard/78907.html
6. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
7. Simon Brown, “Diagrams,” *C4 model*. Retrieved 2026-09-06. https://c4model.com/diagrams
8. Diomidis Spinellis, “Architectural Knowledge: Existence, Location, and Presentation,” in *Software Architecture Knowledge Management*, Springer, 2009.

## Exercises

### Exercise 1

Precisely distinguish stakeholder, audience, reader, contributor, reviewer, decision authority, concern, viewpoint, view, projection, claim, evidence, and correspondence.

### Exercise 2

An operational audience has ten material concerns. Eight are represented; two represented concerns lack current evidence. Compute declared and evidence-backed coverage. Explain four things these percentages do not prove.

### Exercise 3

Diagnose a description in which an executive slide promises “zero downtime,” a developer page specifies asynchronous replication, an operator runbook warns of ten minutes of data loss, and each artifact has a different owner and no effective date. Define a repair sequence.

### Exercise 4

Design audience projections for a medical appointment platform serving patients, clinicians, developers, operators, privacy officers, security reviewers, executives, suppliers, and regulators. Address decision routes, shared claims, access, accessibility, freshness, and evidence.

### Exercise 5

Transfer the method to an international tsunami-warning network operating with sensors, national agencies, telecommunications providers, multilingual public channels, inaccessible regions, intermittent links, and life-safety urgency. Specify the description map and its validation.

## Answers to the Exercises

### Answer 1

A **stakeholder** has an interest in the system. An **audience** groups intended users by a particular decision context. A **reader** consumes an artifact; a **contributor** changes it; a **reviewer** assesses it; and a **decision authority** can approve a choice, accept risk, operate a control, or authorize action. One person may occupy several roles at different times.

A **concern** is a matter important to stakeholders. A **viewpoint** defines conventions for addressing selected concerns; a **view** applies a viewpoint to express an architecture. A **projection** selects and presents governed content for an audience without changing its meaning. A **claim** is an explicit proposition; **evidence** supports it within scope and limitations. A **correspondence** relates claims or elements across views, decisions, implementation, and evidence.

### Answer 2

Declared coverage is $8/10=80\%$. Evidence-backed coverage is $(8-2)/10=6/10=60\%$. The two missing concerns and two unsupported represented concerns require different remediation.

The values do not prove that the declared concern set is complete, that represented claims are true, that evidence is strong enough, or that the audience understands and can act correctly. They also do not establish accessibility, semantic consistency with other projections, or current applicability. The denominator and evidence contract require independent review.

### Answer 3

First freeze the claims as suspect rather than choosing the newest-looking artifact. Identify system boundary, environments, lifecycle states, effective intervals, and decision authorities. Give the service and recovery claim stable identifiers. Retrieve architecture decisions, replication configuration, recovery objectives, tests, incidents, and owners.

Next reconcile meaning. Asynchronous replication cannot generally establish zero loss; the operator's ten-minute statement may be an objective, bound, estimate, or observed case. Write a bounded claim stating recovery and data-loss behavior under explicit assumptions, evidence, and uncertainty. Record unresolved discrepancies as risk.

Assign bounded authoritative ownership for decision, configuration, operational guidance, and evidence. Create executive, developer, and operational projections referencing the same claim. Add effective dates, source revisions, review triggers, and supersession notices. Finally test each audience's intended decision and audit cross-projection consistency. Do not restore “zero downtime” unless evidence establishes precisely defined zero downtime for the declared boundary and conditions.

### Answer 4

Create a description map organized around decisions. Patients need capability, data use, accessibility, outage behavior, support, and consent routes. Clinicians need workflow, safety-relevant state, source authority, degraded operation, and escalation. Developers need boundaries, interfaces, state, privacy constraints, failures, deployment mapping, and tests. Operators need topology, signals, dependencies, safe actions, authority, and recovery. Executives need outcomes, options, cost, risk, evidence, and owners.

Privacy and security projections show classified data, purpose, retention, identities, trust boundaries, threats, controls, residual risk, exceptions, and evidence. Supplier routes show interfaces, obligations, service assumptions, notification, and audit access. Regulatory routes organize claims and evidence by obligation and preserve provenance.

Use stable identifiers for patient identity, appointment, clinical system, notification, suppliers, controls, and claims. Apply tiered access and semantic redaction. Provide semantic HTML, text alternatives, keyboard navigation, defined terminology, suitable contrast, and tested language variants. Every route states scope, lifecycle state, source revision, owner, effective date, evidence limits, and review triggers. Validate with representative task-based comprehension, cross-view consistency, source comparison, accessibility checks, security review, and incident drills.

### Answer 5

Build a public orientation route explaining alert levels, channels, geographic applicability, uncertainty, accessibility, privacy, and actions in plain language. Provide multilingual, low-bandwidth, printable, audio-compatible, and offline-capable formats. A dispatcher route shows observation time, confidence, authority, acknowledgment, escalation, fallback, and message status. Agency leaders receive impact, options, jurisdiction, residual risk, exercises, and communication authority.

Engineering views model sensor identity and provenance, detection, validation, network paths, clocks, message semantics, state authority, telecommunications dependencies, regional failure, retries, duplicate handling, and manual fallback. Operational views link symptoms to current topology, signals, safe actions, degraded modes, and restoration. Assurance views trace life-safety, accessibility, security, privacy, retention, supplier, and jurisdictional obligations to mechanisms and evidence.

Use stable identifiers across languages and projections. Classify sensitive infrastructure and produce access-controlled detail without hiding residual risk from authorized oversight. Govern translation source, effective intervals, owners, and supersession. Validate with semantic consistency checks, link and offline tests, failure exercises, multilingual comprehension tasks, disability-inclusive testing, adversarial redaction review, telecom-loss drills, timing measurements, and evidence review. Report bounded results and unresolved conditions; never infer universal reach from one successful exercise.
