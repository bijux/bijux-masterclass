---
module_id: SARCH-009
program: Software Engineering: Software Architecture
level: 1
module_number: 9
title: Architecture Decision Records
status: complete
last_verified: 2026-09-05
---

# Architecture Decision Records

## One-Page Review

### Governing question

How can a team preserve consequential architecture decisions, their context, alternatives, evidence, ownership, and consequences so later change does not depend on memory or folklore?

### Essential definitions

- An **architecture decision record** (ADR) is a durable record of one architecturally significant decision and the context in which it was made.
- A **decision** commits to an alternative under stated authority; a proposal or discussion is not yet a decision.
- **context** describes the problem, forces, constraints, assumptions, evidence, and timing relevant at decision time.
- A **decision driver** is a goal, requirement, constraint, risk, or other force materially influencing the choice.
- A **consequence** is an expected beneficial, adverse, uncertain, or follow-on effect of the decision.
- **status** describes lifecycle state such as proposed, accepted, rejected, superseded, or deprecated under repository policy.
- **supersession** preserves an old record while a new record replaces some or all of its authority.
- **confirmation** states how the team will determine whether the realized system conforms to the decision.

### Central model, mechanism, or theorem

Treat ADRs as an append-preserving decision graph. Each record has a stable identity and links to drivers, considered alternatives, the selected outcome, consequences, owners, evidence, and review triggers. Accepted records are not silently rewritten when the decision changes; a new record supersedes them and explains the transition.

An ADR is complete for governance only when a reader can answer: what problem was decided, under whose authority, which options were credible, why this option was chosen, what it costs or risks, how conformance is checked, and when the decision must be revisited.

### Critical invariants

- one record captures one durable decision intent;
- the title names the decision outcome or problem, not a meeting or delivery sequence;
- context preserves drivers, constraints, assumptions, uncertainty, scope, and effective date;
- credible alternatives and the status quo are recorded proportionately;
- the selected outcome uses decisive language and names authority;
- positive, negative, uncertain, and follow-on consequences remain visible;
- confirmation is claim-specific and does not overstate automated checks;
- accepted history is preserved through supersession rather than destructive rewriting;
- links among requirements, risks, decisions, implementation, and evidence are bidirectional where useful;
- review triggers respond to invalidated assumptions, incidents, changed requirements, and observed consequences.

### Common failures

Common failures include recording only the chosen technology; writing ADRs after the fact to legitimize a choice; bundling many decisions; omitting rejected alternatives; using vague status; editing an accepted record until history disappears; treating “we decided” as authority; recording only positive consequences; making the ADR an implementation tutorial; declaring conformance from file existence; numbering by project phase; duplicating requirements; storing records where affected teams cannot find them; and never reviewing whether predictions held.

### Compact example

“Use PostgreSQL” is a weak ADR. A stronger record frames the need for one transactional authority for orders, identifies consistency, recovery, team skills, volume assumptions, and portability as drivers, compares PostgreSQL, another relational store, and the status quo, then chooses a bounded configuration. It records migration, operational ownership, licensing, scaling limits, and exit consequences, plus confirmation through schema ownership checks, recovery exercises, and workload evidence. If scale assumptions fail, a new ADR revisits the decision.

### Connections

[SARCH-001](001-architecture-as-significant-design-decisions.md) defines decision significance; [SARCH-005](005-constraints-assumptions-and-risks.md) supplies premises and risk; [SARCH-006](006-architecturally-significant-requirements.md) supplies drivers; [SARCH-007](007-trade-offs-and-competing-objectives.md) supplies comparison discipline; and [SARCH-008](008-architecture-versus-detailed-design.md) determines which choices merit architectural records. [SARCH-010](../ROADMAP.md) uses these practices to frame problems before technology selection.

## Governing Question

Months after an architecture choice, code reveals what was built but rarely why alternatives were rejected, which assumptions mattered, who accepted residual risk, or what would invalidate the choice. Meeting notes and chat preserve fragments without stable authority. How can a team create enough durable memory without turning decision work into bureaucracy?

An ADR answers by recording one consequential decision close to the system it governs. Its value is not the template itself. Its value is recoverable reasoning, explicit authority, traceable consequences, and a safe way to change the decision without erasing history.

## Why This Matters

Architecture decisions constrain later work. Without rationale, future teams either preserve obsolete mechanisms as folklore or repeat expensive analysis. They cannot distinguish deliberate trade-offs from accidents, and incidents cannot test whether predicted consequences were understood.

Decision records also improve current reasoning. Writing the context, alternatives, and consequences exposes hidden assumptions and straw options before commitment. Review becomes about explicit claims rather than influence or memory. New maintainers can learn system boundaries and risks without reconstructing every conversation.

Poor ADR practice creates its own failure modes. Too many trivial records obscure significant ones; immutable wording can freeze errors; mutable history conceals accountability; unverified “consequences” become wishful thinking. The practice must therefore be selective, versioned, searchable, and connected to implementation evidence.

## Prerequisites and Retrieval

Retrieve architecture decision, ASR, stakeholder, authority, context, constraint, assumption, risk, alternative, trade-off, rationale, consequence, evidence, verification, validation, conformance, lifecycle, baseline, status, version, traceability, and reversibility.

From prior modules, retrieve consequence-based decision classification, hard constraints, uncertainty, sensitivity analysis, residual risk, end-to-end ownership, and the distinction between architecture and architecture description. Be ready to distinguish a decision record from the decision event and from a specification or runbook.

## Learning Objectives

After completing this module, you should be able to:

1. identify decisions worthy of an ADR;
2. write a precise problem and context without smuggling in a solution;
3. document credible alternatives and a decisive outcome;
4. record benefits, costs, risks, uncertainty, and follow-on work;
5. define status transitions and legitimate decision authority;
6. preserve history through supersession and deprecation;
7. connect ADRs to requirements, risks, implementation, and evidence;
8. design confirmation appropriate to a decision claim;
9. place and index ADRs for discoverability and ownership;
10. review decisions when premises or observed consequences change.

## Core Exposition

**Record decisions, not topics.** “Caching,” “database,” or “authentication” names an area. “Cache public product descriptions for at most five minutes at the regional edge” names a bounded outcome. A strong title remains understandable without the delivery narrative. Use one record per durable intent; split independent choices that can change separately.

Not every choice needs an ADR. Record decisions with broad reach, difficult reversal, material quality effects, cross-team contracts, persistent data, supplier commitment, high uncertainty, or significant risk. Local choices belong in code, tests, component documentation, or ordinary design notes unless their reach expands.

**Write context before outcome.** State the system and decision boundary, problem, stakeholders, drivers, constraints, assumptions, risks, evidence, and timing. Preserve uncertainty as it existed. Context should enable a future reviewer to understand why the decision was rational then, even if it later proves wrong.

Avoid advocacy in the problem statement. “We need Kafka to scale events” embeds solution and an unproven causal claim. Instead state event volume, ordering, delivery, latency, producer/consumer independence, recovery, skills, cost, and evolution requirements. Technology can then appear among alternatives.

**Compare credible alternatives.** Include the status quo when it is feasible; doing nothing has cost, risk, and option effects. Describe candidates at similar fidelity, including configuration, integration, operation, migration, and exit. Record why rejected options lost under the declared drivers rather than caricaturing them.

An ADR need not reproduce a full trade study. Link larger analyses and preserve decisive evidence, uncertainty, and selection rules. If only one option is legally or physically feasible, document the governing constraint and why alternatives are inadmissible.

**State the decision and authority.** Use direct wording: “We will…” or “The order service shall own…” State scope, effective date, owner, and any conditions. “The team agrees” is not enough when security, legal, safety, budget, or cross-organizational authority differs. Record who had authority and which approvals or dissent remain.

A proposed ADR supports discussion; an accepted ADR governs the stated scope. Rejected means the proposed outcome was not adopted. Deprecated can mean still present but discouraged or scheduled for removal. Superseded means another record replaces its authority. Define these statuses for the repository rather than assuming universal meanings.

**Record consequences honestly.** Include intended benefits, accepted costs, new risks, operational burden, migration, training, coupling, future options, security and privacy effects, and conditions under which consequences change. Consequences are predictions at decision time. Later observations should confirm, contradict, or refine them without rewriting what was believed.

Do not hide follow-on obligations in prose. Link implementation work, derived requirements, controls, migrations, runbooks, and evidence plans. An accepted ADR can be coherent before every task finishes, but status must not imply implementation completion.

**Confirm realization and outcome separately.** Confirmation can check static dependencies, schemas, configuration, deployment topology, contract tests, recovery exercises, performance experiments, or operational indicators. Choose evidence matching the decision. A linter can prove an encoded dependency predicate over scanned files; it cannot prove the architecture meets stakeholder goals.

Distinguish conformance—was the decision realized?—from fitness—did it produce acceptable outcomes? A decision to isolate tenants may be reflected in deployment configuration yet fail under a shared identity or rate-limiting dependency. Link both structural checks and quality evidence where applicable.

**Preserve accepted history.** Correct typographical errors without changing meaning under repository policy, but do not silently replace context, outcome, or consequences. If a decision changes, create a new ADR that links to and supersedes the old one. State transition, migration, compatibility, rollback, and residual use.

Supersession may be partial. A new decision can replace storage technology while retaining the prior authority boundary. Make scope explicit instead of marking the entire old record obsolete. Avoid cycles: a record cannot ultimately supersede itself.

**Place records with ownership and reach.** Records should be version-controlled, reviewable, and discoverable to the people governed by them. Team-local ADRs can live near the component; organization-wide decisions may need a governed central catalogue plus links from affected repositories. Duplication creates drift, so maintain one authority and derived indexes.

Stable numeric identifiers help ordering and links but do not encode project phases. Titles should carry durable meaning. Generated indexes may show status, scope, owners, drivers, and supersession, while source records remain human-reviewable.

**Review as evidence changes.** Define triggers: requirement or constraint change, failed assumption, incident, scale threshold, supplier notice, new jurisdiction, security finding, poor developer or operator outcomes, or planned review date. Compare predicted and observed consequences. Reopen the decision when evidence invalidates its premise, not merely because a new tool is fashionable.

An ADR catalogue is not complete architecture documentation. Views, requirements, interface contracts, threat and hazard analyses, runbooks, and evidence have different purposes. Records link these artifacts and preserve why the architecture moved.

## Definitions and Notation

Let $R$ be the set of ADRs and $D$ the set of decisions. Each record $r\in R$ has stable identity $id(r)$ and describes at most one primary decision $dec(r)\in D$. Define

$$
r=(id,title,status,context,drivers,options,outcome,consequences,authority,confirmation,triggers).
$$

Let $supersedes\subseteq R\times R$. The directed supersession graph must be acyclic:

$$
\nexists r\in R: r\;supersedes^{+}\;r,
$$

where $supersedes^{+}$ is the transitive closure. An edge $(r_{new},r_{old})$ states that the newer record replaces the old record within an explicit scope.

Trace relations can include $motivatedBy\subseteq R\times Driver$, $realizedBy\subseteq R\times Artifact$, and $confirmedBy\subseteq R\times Evidence$. Presence of a link establishes reference structure only; reviewers must still assess semantic adequacy and evidence validity.

A catalogue coverage ratio may count accepted architectural decisions with records, but its denominator is generally unknown because unrecorded decisions are precisely what discovery seeks. Report known-inventory coverage, never “100% of architecture decisions” without a justified inventory.

## Mechanisms, Invariants, or Proof Structure

Use this ADR workflow.

1. **Detect significance:** identify a cross-boundary, durable, risky, uncertain, or expensive-to-reverse decision.
2. **Assign identity and owner:** create a stable record in the authoritative location.
3. **Frame context:** state problem, scope, drivers, constraints, assumptions, evidence, and decision deadline.
4. **Develop alternatives:** include credible status quo, candidate, hybrid, or staged options at comparable fidelity.
5. **Analyze:** expose trade-offs, uncertainty, sensitivity, migration, operation, exit, and residual risk.
6. **Decide under authority:** state outcome, scope, conditions, effective date, approvals, and dissent.
7. **Record consequences:** preserve expected benefits, costs, risks, follow-on obligations, and option effects.
8. **Confirm:** define structural conformance and outcome evidence with limitations.
9. **Maintain:** link implementation and observations; review triggers and status without erasing history.
10. **Supersede deliberately:** create a new record, link scopes, manage transition, and retain the old record.

The governing invariants are one decision intent, stable identity, honest contemporaneous context, credible alternatives, explicit authority, visible consequences, claim-specific confirmation, immutable semantic history, acyclic supersession, discoverable ownership, and lifecycle review.

Schema validation can prove required fields, valid status vocabulary, links, and absence of supersession cycles in the inspected catalogue. It cannot prove the decision was wise, alternatives complete, authority legitimate, consequences accurate, or realized system fit.

## Alternatives and Trade-Offs

**Minimal ADRs** with status, context, decision, and consequences are easy to maintain and encourage adoption. They can omit drivers, alternatives, authority, evidence, and review triggers. **Rich templates** improve rigor but invite boilerplate. Require fields proportional to decision consequence and link supporting analyses.

**Records beside code** improve synchronization, review, and component ownership but can hide cross-repository impact. **Central catalogues** improve enterprise discovery but drift from implementation and centralize control. Use one authoritative record at the decision’s ownership boundary and generated or linked indexes elsewhere.

**Immutable accepted records** preserve historical truth but retain errors and stale links. **Editable records** stay current but can erase rationale. Allow nonsemantic corrections transparently; use annotations or superseding records for meaningful change.

**Numeric identifiers** provide stable short references and chronological hints but can create collision or sequencing rituals. **Descriptive identifiers** improve meaning but are harder to rename when outcomes change. Stable ID plus durable descriptive title balances both.

## Failure Modes and Misconceptions

- **“ADR means any design note.”** Select architecturally significant, durable decisions.
- **“The template creates rigor.”** Evidence, alternatives, authority, and honest consequences create rigor.
- **“Accepted means implemented.”** Decision status and realization status are different.
- **“Code is the decision record.”** Code rarely preserves alternatives, context, authority, or rejected reasoning.
- **“The newest technology requires a new ADR.”** Reopen only when drivers, evidence, or consequences justify change.
- **“One ADR can cover the whole architecture.”** Independent decisions need independent lifecycle and supersession.
- **“Rejected alternatives should disappear.”** They prevent repeated analysis and expose the comparison’s limits.
- **“Consequences are benefits.”** Costs, risks, uncertainty, operational work, and lost options must remain visible.
- **“Do not edit ever.”** Transparent typo or link repair is different from silently changing semantic history.
- **“Superseded means deleted.”** Historical context remains necessary for migration, audit, and surviving scope.
- **“A linter confirms architecture.”** It confirms only encoded predicates over inspected artifacts.
- **“All ADRs belong centrally.”** Authority and affected reach determine placement; indexes can federate discovery.
- **“Numbering shows delivery phase.”** Stable identifiers should not encode temporary project narratives.
- **“An ADR grants authority.”** The record documents authority; it does not create it.

## Worked Examples

### Example 1

**Question:** Should “choose a logging library” receive an ADR?

**Reasoning:** If one component can replace it while preserving security, telemetry, performance, licensing, and operations obligations, it is local. If a shared format, correlation identity, retention, sensitive-data policy, or organization-wide platform contract depends on it, the broader decision merits an ADR; library choice may remain an implementation detail.

**Conclusion:** Record the significant cross-boundary decision, not every mechanism used to realize it.

### Example 2

**Question:** Rewrite “ADR-12: Use Kafka.”

**Reasoning:** Frame producer independence, event volume, ordering, delivery, replay, recovery, latency, data sensitivity, skills, cost, and schema evolution. Compare synchronous calls, a durable log, a queue, and status quo at equivalent detail. Choose a bounded event backbone only if those drivers support it, then record operations, partitioning, migration, and exit consequences.

**Conclusion:** A technology name becomes defensible only after the problem and alternatives are explicit.

### Example 3

**Question:** An accepted ADR’s workload assumption proves false. Should the old text be corrected?

**Reasoning:** Preserve the original assumption and decision context. Add evidence showing invalidation, create a new ADR that re-evaluates alternatives, and supersede the relevant scope. Link migration and residual uses. Rewriting the old record would make the historic decision appear irrational or differently informed.

**Conclusion:** Supersession preserves learning and accountability better than semantic editing.

### Example 4

**Question:** Can one ADR select database, cloud, service boundaries, and deployment pipeline?

**Reasoning:** These choices have different drivers, owners, evidence, and change timelines. Bundling makes partial supersession ambiguous and encourages shallow alternatives. Split records, then link dependencies—for example, data authority constrains database placement, while deployment automation realizes recovery and change objectives.

**Conclusion:** One durable decision intent per record supports independent review and evolution.

### Example 5

**Question:** How should an ADR confirm a no-cross-layer-dependency decision?

**Reasoning:** Define allowed module graph, exceptions, scanned artifacts, generated code, runtime reflection limits, and ownership. A dependency checker can report conformance for the inspected graph and version. Integration tests and reviews address behavioral or dynamic coupling. The ADR should not claim architectural fitness from a green graph alone.

**Conclusion:** Confirmation matches the decision predicate and publishes evidence limits.

### Example 6

**Question:** Is a rejected ADR a failure?

**Reasoning:** No. A proposed decision can expose a constraint, reveal better alternatives, or prove infeasible. Preserve the rejected status, reasoning, evidence, and any replacement link. It becomes failure only if status is ambiguous or the rejected outcome is implemented without authority.

**Conclusion:** Rejected records are durable decision evidence, not clutter to delete.

### Example 7

**Question:** Where should a cross-repository identity decision live?

**Reasoning:** Place authority where the shared identity contract and governance are owned, not arbitrarily in one consumer. Give it a stable URL or identifier, version it, and generate indexes or local pointers in affected repositories. Consumer-specific authorization decisions can remain local ADRs linked to the shared record.

**Conclusion:** One authority plus federated discovery avoids both hiding and duplication.

### Example 8

**Question:** A record predicts lower operator load, but incidents show the opposite. What changes?

**Reasoning:** Attach or link the observation, inspect whether implementation conformed, and compare actual context with assumptions. If the decision mechanism causes the burden, reopen or supersede it; if realization drifted, repair conformance. Preserve the mistaken consequence prediction so the organization can learn.

**Conclusion:** ADRs connect predicted and observed consequences rather than protecting prior decisions.

### Example 9

**Question:** Should a security exception be recorded only in an ADR?

**Reasoning:** The ADR can explain architecture context and compensating controls, but exception authority, expiry, risk acceptance, evidence, and monitoring belong in the governed security or risk system. Link the authoritative exception; do not duplicate it or imply that an architecture record grants approval.

**Conclusion:** ADRs integrate authorities and evidence without replacing specialized governance.

### Example 10

**Question:** What must an ADR contain for a safety-critical train-control fallback?

**Reasoning:** Preserve hazard and requirement sources, operational context, human and automated authority, alternatives, independence, timing, degraded behavior, evidence, transition, and residual risk. No external railway, safety, regulatory, human-factors, cybersecurity, or practitioner review is claimed. Named qualified authorities must own applicable decisions, validation, release, and acceptance.

**Conclusion:** High-consequence ADRs document but do not replace domain assurance and legitimate authority.

## Cross-Program Connections

- [Software Engineering Methods & Evolution](../../10-software-engineering-methods-and-evolution/ROADMAP.md) connects ADRs to iterative discovery, change control, and technical debt.
- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) uses explicit context, forces, and consequences rather than pattern-name justification.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies confirmation evidence matched to decision claims.
- [Software Delivery & Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) links decisions to deployment, recovery, incidents, and observed consequences.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies authoritative threat, control, exception, and risk records.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) situates decisions within requirements, baselines, verification, validation, and lifecycle authority.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) requires discoverable shared decisions plus explicit consumer freedoms and escape paths.

## References

1. Michael Nygard. [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions), Cognitect, 15 November 2011. Original lightweight ADR formulation using title, status, context, decision, and consequences; consulted 2026-09-05.
2. MADR project. [ADR Template](https://adr.github.io/madr/decisions/adr-template.html), MADR 4 series. Current structured template covering context, drivers, options, outcome, consequences, confirmation, and review considerations; consulted 2026-09-05.
3. MADR project. [About MADR](https://adr.github.io/madr/), current project documentation. Versioned Markdown ADR practice and template history; consulted 2026-09-05.
4. ISO/IEC/IEEE. [ISO/IEC/IEEE 42010:2022, Software, systems and enterprise—Architecture description](https://www.iso.org/standard/74393.html), edition 2, November 2022. Current architecture-description concepts including decisions, rationale, concerns, views, and correspondence; consulted 2026-09-05.
5. Olaf Zimmermann. “Architectural Decision Identification in Architectural Patterns.” *Proceedings of WICSA/ECSA*, IEEE, 2011. Decision identification, alternatives, outcomes, and architectural knowledge.
6. Jeff Tyree and Art Akerman. “Architecture Decisions: Demystifying Architecture.” *IEEE Software* 22(2), 2005. Architecture-decision content, rationale, constraints, and traceability.
7. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*, fourth edition, Addison-Wesley, 2021. Architecture drivers, decisions, quality consequences, analysis, and evolution.
8. Paul Clements et al. *Documenting Software Architectures: Views and Beyond*, second edition, Addison-Wesley, 2010. Architecture rationale, views, interfaces, context, variability, and documentation practice.

## Exercises

### Exercise 1

Decide which of these deserve ADRs for a payment service and justify why: variable naming convention, payment idempotency identity, test assertion library, database authority, and log color scheme.

### Exercise 2

Write the essential content for an ADR choosing asynchronous invoice generation. Include problem, drivers, credible alternatives, decision, authority, consequences, confirmation, and triggers.

### Exercise 3

Diagnose an ADR catalogue where accepted records are edited in place, half the records say “use technology X,” implementation status is mixed with decision status, and superseded files are deleted.

### Exercise 4

Design a supersession chain for moving from a shared customer database to service-owned data. Address partial scope, transition, rollback, residual consumers, and confirmation.

### Exercise 5

Define ADR governance for an unfamiliar clinical alarm platform. Separate automated record checks, technical evidence, domain validation, authority, and blockers.

## Answers to the Exercises

### Answer 1

Payment idempotency identity merits an ADR because it governs duplicate and unknown outcomes across clients, processors, persistence, and reconciliation. Database authority merits an ADR because it establishes transactional and data ownership, recovery, migration, and cross-team boundaries. Variable names, assertion library, and log colors are normally local unless they implement a regulated interface, organization-wide platform contract, accessibility obligation, or other material cross-boundary decision.

The answer must analyze reach and reversibility rather than infer significance from technology size. Local choices still need proportionate tests and ownership; they simply do not need architecture-decision governance.

### Answer 2

Problem: invoices require expensive rendering and external tax/reference lookups; synchronous generation violates request latency and couples availability. Drivers include correct immutable invoice identity, two-minute completion objective, burst workload, authorization, retry, customer visibility, retention, and operator recovery. Compare synchronous generation, asynchronous durable work, scheduled batch, and a hybrid preview/final process at equivalent detail.

Decision: the authorized service owner accepts durable asynchronous generation with stable job identity, explicit queued/running/succeeded/failed states, immutable input snapshot, bounded retries, cancellation policy, notification, and reconciliation. Consequences include lower request coupling and burst absorption, but added storage, queue operation, provisional state, schema versioning, delayed authorization concerns, and support complexity. Confirmation includes state-machine/invariant tests, contract and authorization tests, load and failure exercises, reconciliation, recovery, and end-to-end observation. Triggers include volume threshold, completion-objective failure, supplier change, material support burden, or altered invoice authority.

### Answer 3

In-place semantic edits destroy contemporaneous context and make later decisions appear differently informed. Technology-only records omit problem, drivers, alternatives, authority, consequences, and evidence. Decision status describes governance, while implementation progress belongs in linked work or explicit realization fields. Deletion breaks migration, audit, rationale, and surviving-scope history.

Define stable IDs and statuses; preserve accepted records; create new records for changed outcomes; establish acyclic, scope-specific supersession links; restore deleted history from version control if safely possible; split bundled records; and enrich future records proportionately. Add authoritative placement, generated indexes, trace links, confirmation, review triggers, and periodic observation of consequences. Do not rewrite old records merely to make the catalogue look complete.

### Answer 4

ADR A records the original shared authority and remains historical. ADR B supersedes A for new customer-profile writes in services X and Y, defines field authority, event/API semantics, dual-read behavior, reconciliation, security, migration, and rollback. A remains effective for legacy reporting and any unmigrated fields. ADR C later supersedes the residual scope after consumers, data, credentials, backups, and recovery paths retire.

Each edge names scope and effective condition. Confirmation covers writer discovery, schema permissions, traffic and consumer inventory, consistency/reconciliation, migration counts and checksums, rollback exercises, access revocation, and absence of legacy reads over a declared interval. Do not mark A wholly superseded until every governed responsibility has moved or been retired.

### Answer 5

Require stable IDs, one decision intent, source and authority, clinical and operational context, alarm hazards, assumptions, alternatives, human authority, timing, prioritization, degraded behavior, consequences, evidence, residual risk, and review triggers. Automated checks can validate schema, status vocabulary, trace links, digests, required approvals, supersession acyclicity, and evidence freshness. Technical evidence can include timing analysis, interface and state-machine tests, load/fault exercises, cybersecurity assessment, device integration, recovery, and production monitoring under approved conditions.

These checks do not establish clinical alarm validity, human comprehension, hazard completeness, regulatory compliance, or acceptable risk. No external clinical, medical-device, safety, regulatory, human-factors, cybersecurity, or practitioner review is claimed. Named qualified authorities must own alarm requirements, hazard controls, independent assurance, clinical validation, release, and residual-risk acceptance. Missing clinical authority, ambiguous alarm priority, violated timing, unsafe degraded operation, stale evidence, or unresolved high-severity hazard blocks the corresponding decision or readiness claim.
