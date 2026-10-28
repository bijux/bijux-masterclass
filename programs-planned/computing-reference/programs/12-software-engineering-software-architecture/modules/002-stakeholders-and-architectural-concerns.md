---
module_id: SARCH-002
program: Software Engineering: Software Architecture
level: 1
module_number: 2
title: Stakeholders and Architectural Concerns
status: complete
last_verified: 2026-08-29
---

# Stakeholders and Architectural Concerns

## One-Page Review

### Governing question

How can architects identify the people and institutions with legitimate interests in a system, turn their concerns into decision-ready evidence, and demonstrate that architecture descriptions address those concerns without mistaking a checklist for completeness?

### Essential definitions

- A **stakeholder** is an individual, team, organization, or class of them with an interest in the entity or system under consideration.
- A **concern** is an interest in that system relevant to one or more stakeholders. It may be functional, developmental, operational, technological, economic, legal, ecological, social, or organizational.
- A **stakeholder role** describes a relationship to the system—operator, acquirer, maintainer, regulator, or affected person—not merely a job title.
- An **architectural driver** is a sufficiently important concern, goal, constraint, assumption, or risk that materially shapes architecture.
- A **quality-attribute scenario** makes a quality concern evaluable by naming stimulus source, stimulus, environment, affected artifact, response, and response measure.
- An **architecture viewpoint** establishes conventions for constructing, interpreting, and using architecture views to frame specified concerns.
- An **architecture view** is the actual representation of a particular system made according to a viewpoint.
- **Representation** means that a legitimate stakeholder perspective can enter deliberation; it does not mean that every preference must win.
- **Traceability** is the maintained relation from stakeholder and concern through scenario, viewpoint/view or other evidence, decision, consequence, owner, and review trigger.
- A **concern conflict** exists when proposed responses cannot all be satisfied together, or when satisfying one materially changes cost, risk, or another valued outcome.

### Central model, mechanism, or theorem

Represent a concern record as

\[
c=(id,stakeholders,source,statement,rationale,scenario,priority,evidence,owner,status,triggers).
\]

The working trace is

\[
stakeholder \rightarrow concern \rightarrow scenario/constraint
\rightarrow viewpoint\ and\ view \rightarrow decision
\rightarrow evidence \rightarrow consequence.
\]

This is a governance mechanism, not a completeness theorem. If \(K\) is the set of known, in-scope concerns and \(A\subseteq K\) the concerns with an accountable response, then \(|A|/|K|\) measures declared-inventory coverage only. It says nothing about legitimate stakeholders or concerns that discovery missed.

### Critical invariants

- State the system/entity, boundary, environment, lifecycle stage, decision scope, and authority before eliciting concerns.
- Identify direct, indirect, future, operational, maintenance, assurance, acquisition, supplier, and adversely affected stakeholders.
- Preserve the source, rationale, dissent, uncertainty, and authority of a concern; do not silently translate it into a preferred solution.
- Separate concern from requirement, quality attribute, constraint, assumption, risk, decision, and implementation.
- Refine important concerns into scenarios or other falsifiable acceptance/evaluation evidence.
- Map each material concern to a response and owner; an explicit defer, reject, transfer, or accept-risk decision is a response only with rationale and authority.
- Use viewpoints because concerns differ; do not make one diagram answer every question or create one view per person automatically.
- Record conflicts and distributional consequences rather than averaging them away.
- Revalidate the stakeholder map and concern register when system, environment, regulation, organization, suppliers, incidents, or evidence changes.
- Never interpret inventory coverage, workshop votes, automated checks, or document conformance as proof that the architecture is correct, safe, equitable, or complete.

### Common failures

Common failures include equating stakeholders with end users; consulting only sponsors and developers; using job titles instead of system relationships; ignoring maintainers, operators, support, suppliers, regulators, data subjects, bystanders, and future owners; treating the loudest or highest-ranking person as the sole authority; recording solution requests as concerns; labeling “secure,” “fast,” or “easy” without conditions and measures; merging conflicting concerns until dissent disappears; counting rows as proof of completeness; prioritizing only by workshop votes; creating a view for every stakeholder; using a generic diagram for every concern; collecting concerns without decision owners; and never revisiting the map after architecture or context changes.

### Compact example

“Operations wants Kubernetes” is a proposed mechanism, not yet an architectural concern. Ask why. The underlying concerns may be: restore a failed workload within ten minutes at 03:00 with one on-call engineer; deploy without exposing credentials; and support the service with the skills and budget available. Those concerns admit several architectures. Record the operator source, refine scenarios and constraints, compare options, choose evidence, assign decision and risk owners, and preserve the rejected request and rationale.

### Connections

[SARCH-001](./001-architecture-as-significant-design-decisions.md) defines architectural significance and drivers. [SDDM-002](../../09-software-engineering-software-design-and-domain-modeling/modules/002-stakeholders-goals-and-observable-outcomes.md) develops stakeholder goals and outcome evidence. [SEME-002](../../10-software-engineering-methods-and-evolution/modules/002-lifecycle-activities-and-feedback-loops.md) keeps discovery and response alive across the lifecycle. [SARCH-003](../ROADMAP.md) uses the stakeholder map to establish functional scope and system context.

## Governing Question

How should an architecture practice discover stakeholder interests, refine them into concerns that can guide decisions and views, resolve conflicts legitimately, and retain evidence as both the system and its environment evolve?

Architecture mediates among people who experience different consequences. A buyer sees acquisition and exit cost; a user sees capability and accessibility; an operator sees failure and recovery; a maintainer sees change propagation; a security or safety authority sees loss scenarios; a data subject sees surveillance and control; a supplier sees contracts and interfaces. None sees the whole system. Architecture becomes responsible when it makes these perspectives inspectable without pretending that elicitation eliminates judgment.

## Why This Matters

Many architecture failures begin as stakeholder-model failures. A service can satisfy the product sponsor while being impossible to operate. A migration can meet delivery dates while removing a legally required retention property. A scheduling system can optimize average throughput while imposing unacceptable delay on a protected or safety-critical class. The missing concern may never appear in a feature backlog because the affected stakeholder has no product account, no workshop invitation, or no power.

Conversely, treating every request as binding produces incoherence. Stakeholders speak from partial models, propose familiar technologies, and may have incompatible incentives. Architecture work must recover the interest beneath a request, determine relevant authority, expose conflicts, and create a justified response. “We listened” is not evidence that a concern was addressed; “the stakeholder approved” is not proof that the resulting system is technically adequate.

Concern work also determines what architecture documentation is for. A deployment view helps operators reason about failure containment but may not explain data authority. An information view can expose lineage and retention while saying little about build dependencies. Viewpoints select conventions for particular concerns. Without explicit concern-to-view relations, documentation tends toward either a single ambiguous diagram or an expensive collection that nobody can use.

## Prerequisites and Retrieval

Before this module, retrieve:

- system, entity of interest, boundary, environment, interface, dependency, state, lifecycle, and authority;
- stakeholder, goal, outcome, requirement, constraint, assumption, risk, quality attribute, and evidence;
- architectural decision, driver, significance, trade-off, view, viewpoint, and architecture description;
- functional behavior versus qualities such as availability, performance, security, privacy, safety, usability, accessibility, modifiability, interoperability, and operability;
- source, stimulus, environment, artifact, response, and response measure in a quality-attribute scenario;
- validation—evidence that the intended use and stakeholder need are served—versus verification against a specified claim.

You should be able to explain why “adopt product X” is a candidate decision, why “recover service within ten minutes during a zone failure” is an evaluable concern, and why passing the latter test would still not prove that all important stakeholders were found.

## Learning Objectives

After completing this module, you should be able to:

1. identify stakeholder classes from system relationships and consequences rather than an organization chart alone;
2. distinguish concerns from goals, requirements, qualities, constraints, assumptions, risks, decisions, and implementations;
3. construct a concern record with source, rationale, scenarios, evidence, ownership, status, and review triggers;
4. elicit silent, indirect, future, and adversely affected perspectives;
5. refine vague interests and solution requests into decision-ready architectural concerns;
6. map concerns to viewpoints, views, decisions, and evaluation evidence;
7. analyze conflicts, authority, priority, and distributional consequences without hiding dissent;
8. audit known concern coverage while stating the limits of coverage metrics;
9. evolve stakeholder and concern models when boundaries, evidence, and lifecycle conditions change;
10. define qualified human review for safety-, security-, privacy-, or rights-critical concerns without claiming external review.

## Core Exposition

### Begin with an entity, boundary, and purpose

“Who are the stakeholders?” has no stable answer until the entity of interest and decision scope are named. The stakeholders of a payment library differ from those of the retail platform that embeds it. A release decision, a data-retention decision, and an acquisition decision can involve overlapping but different authorities.

Record the entity, included capabilities, environment, lifecycle stage, decision horizon, jurisdictions, and interfaces. Treat the boundary as a hypothesis. Elicitation may reveal that a supposedly external identity provider controls recovery, that manual support is part of the operational system, or that exported data creates downstream obligations. Update the boundary and repeat discovery.

Purpose matters as well. An architecture description for procurement, threat analysis, maintenance, certification, onboarding, or modernization frames different concerns. The architecture is not changed merely by the audience, but the useful evidence and views are.

### Discover stakeholders through relationships and consequences

Start with relationships, not a list of executive names. Ask who:

- acquires, funds, owns, governs, or can terminate the system;
- uses capabilities directly or receives their outputs;
- is represented in, described by, or acted upon through system data;
- develops, integrates, tests, deploys, operates, supports, maintains, audits, or retires it;
- supplies infrastructure, data, models, components, services, or professional judgment;
- accepts operational, financial, legal, safety, security, privacy, or reputational risk;
- regulates, certifies, assures, investigates, or provides independent challenge;
- interoperates as an external producer or consumer;
- is displaced, excluded, monitored, delayed, endangered, or otherwise affected without choosing to use it;
- will inherit the system, data, contracts, or incidents later.

A person can occupy several roles whose interests conflict. A hospital may be acquirer, operator, data controller, and employer; a clinician may be user and safety barrier. Keep roles distinct enough to reveal concerns. Avoid assuming one representative can speak authoritatively for every member of a broad class.

Use several discovery channels: context diagrams, lifecycle maps, value and harm chains, data-flow and supply-chain analysis, incident histories, support records, contracts, regulations, accessibility research, field observation, interviews, workshops, threat/hazard analysis, and predecessor-system evidence. Each channel has selection bias. Workshops privilege attendees and confident speakers; telemetry excludes non-use and hidden work; contracts expose formal authority but not all affected parties.

### Elicit interests before accepting solutions

A stakeholder statement can be a goal, observation, problem, fear, constraint, quality preference, solution request, or political position. Preserve the original statement, then inquire:

1. What outcome or loss is at issue?
2. Under what situation does it matter?
3. Which part of the system or environment is affected?
4. What response would be acceptable, and how could it be observed?
5. Who has authority to define or accept this condition?
6. What evidence supports it, and what uncertainty remains?
7. What happens if it is not addressed?
8. Does it conflict with another interest?

“Use a single database” might encode cost limits, transactional integrity, familiar operations, reporting needs, or an organizational desire for central control. Those lead to different decisions. Do not discard the proposed solution: retain it as source evidence and candidate option while extracting the concern.

### Distinguish nearby concepts

A concern is broader than a requirement. “The system must be supportable by a small on-call team” is a concern; a refined requirement could limit paging rate, diagnostic time, or manual recovery steps. A quality attribute supplies a vocabulary, not a complete scenario. “Availability” does not identify which capability, failure, environment, duration, or measure matters.

A constraint forbids or mandates part of the solution space because of authority or fact. Verify its source and duration. An assumption is believed for planning but needs validation and expiry. A risk is uncertainty plus consequence. A decision selects or constrains a response. An implementation realizes decisions. Keeping these separate allows a changing constraint or invalid assumption to trigger reconsideration without erasing the original concern.

Not every concern becomes an architectural driver. Significance depends on reach, quality impact, severity, reversal cost, coordination, precedent, uncertainty, and lifecycle consequences. Local presentation wording may remain detailed design; deletion rights across stores, backups, analytics, and suppliers can shape architecture.

### Make concerns decision-ready

A durable concern register is more than a sentence list. For each concern record:

- stable identifier and concise statement;
- affected stakeholder roles and named representatives where appropriate;
- source, authority, date, and original evidence;
- rationale, affected goals, potential benefit or loss;
- scope, system boundary, lifecycle conditions, and jurisdiction;
- scenario, constraint, acceptance threshold, or question to resolve;
- priority/criticality with method and dissent;
- related, duplicate, dependent, or conflicting concerns;
- chosen response, alternatives, decisions, and consequences;
- viewpoint, views/models, experiments, analyses, tests, or operational measures;
- accountable decision owner, evidence owner, and risk-acceptance authority;
- state, unresolved questions, residual risk, and review/expiry triggers.

Keep raw elicitation notes separate from normalized records so that translation remains auditable. Version material changes. A concern is not closed merely because a document links to it; closure requires an authorized disposition and evidence appropriate to the claim.

### Refine quality concerns with scenarios

For system qualities, a scenario counters adjective-driven design. Let

\[
q=(source,stimulus,environment,artifact,response,measure).
\]

“Fast” becomes: during the seasonal peak, an authenticated account holder requests the latest statement; the statement service returns a semantically correct response within 800 ms at the 99th percentile over a specified window, under a defined workload and data size. State exclusions openly.

Scenarios do not solve politics. Stakeholders may disagree about percentile, budget, affected population, degradation behavior, or whose delay counts. Preserve that disagreement. A threshold chosen by an architect without product, operations, and affected-user authority is not legitimized by precise notation.

Concerns that are legal, organizational, or ethical may need different evidence: policy interpretation, data-flow review, contractual analysis, accessibility evaluation, hazard argument, operating procedure, or governance decision. Do not force every interest into a latency-style measure.

### Use viewpoints to organize evidence

A viewpoint defines how to construct and interpret views for specified concerns: its stakeholders, concerns, model kinds, conventions, analysis methods, and correspondence rules. A view applies those conventions to the entity. “The security view” without scope or semantics is ambiguous; a threat-oriented viewpoint might require trust boundaries, assets, actors, flows, controls, assumptions, and analysis.

Map concerns to viewpoints many-to-many:

- one concern may require runtime, deployment, data, and operational views;
- one viewpoint may frame concerns shared by several stakeholder roles;
- one view can serve several concerns if its semantics and evidence are adequate.

Do not make a view per stakeholder automatically. Operators and security reviewers may use the same deployment model for different questions. Do not make one overloaded view either. A diagram that mixes runtime calls, code dependencies, deployment nodes, data authority, and organization ownership without notation is difficult to interpret and easy to contradict.

Correspondence matters. If a deployment view says services are isolated across zones but configuration deploys them together, the described and operational architectures diverge. Link concern evidence to build graphs, schemas, configuration, runtime traces, inventories, tests, analyses, and decision records where appropriate.

### Prioritize without manufacturing consensus

Priority is a governance decision made under finite resources. Consider severity, probability/uncertainty, legal or contractual force, mission value, affected population, irreversibility, time criticality, dependency, evidence cost, and stakeholder authority. Some constraints are non-compensable: a weighted score cannot trade a mandatory safety property for cosmetic benefit.

Voting can expose group preference but is sensitive to attendance, framing, coalitions, power, and the number of votes allocated. A quality-attribute workshop can generate, consolidate, prioritize, and refine scenarios; it is not proof that absent stakeholders consented or that low-voted risks are negligible. Record the method, participants, dissent, and follow-up for unrepresented groups.

When concerns conflict, identify the scenario pair and affected parties. Explore reframing, segmentation, graceful degradation, staged evidence, exception handling, or alternative boundaries. If a trade-off remains, name the decision authority and who bears each consequence. “Stakeholders agreed” should mean traceable agreement under a stated process, not the absence of recorded objection.

### Close the response loop

For every material concern, one of these dispositions should be visible:

- **addressed:** a decision and evidence meet the current acceptance claim;
- **partially addressed:** bounded evidence exists and residual work/risk is owned;
- **deferred:** a justified trigger/date and owner exist;
- **accepted risk:** authorized owner accepts stated residual consequence;
- **transferred/shared:** another party’s obligation and interface are explicit;
- **rejected/out of scope:** rationale, authority, boundary consequence, and escalation route are recorded;
- **open:** uncertainty or conflict remains and blocks the relevant claim.

These states are not interchangeable. Outsourcing transfers work, not necessarily accountability. Declaring a concern out of scope can move harm across the boundary; examine the surrounding system. Closing an issue tracker ticket does not close an operational concern if evidence has not been re-observed.

### Audit known coverage honestly

An automated register audit can detect empty sources, missing scenarios, absent view/evidence links, unknown owners, or invalid states. It cannot discover everyone who should have been consulted, decide whether a representative is legitimate, validate a scenario threshold, resolve conflicting rights, or judge architecture adequacy.

Use separate questions:

- **stakeholder discovery:** which relationship/consequence categories were examined and by what evidence?
- **representation:** who participated, who spoke for a class, who was absent, and how will gaps be addressed?
- **concern inventory:** which known concerns have valid source and scope?
- **response coverage:** which known material concerns have disposition, owner, view/decision relation, and evidence?
- **outcome validation:** do operational and stakeholder observations support the intended result?

A percentage may summarize response coverage within a declared inventory. Always publish numerator, denominator, filters, date, and limitations. Never call it “stakeholder completeness.”

### Maintain the model over the lifecycle

Stakeholders and concerns change as the system moves from proposal to acquisition, development, transition, operation, modernization, and retirement. A prototype’s primary stakeholders may be researchers and sponsors; a production system adds on-call teams, support, security response, compliance, suppliers, downstream consumers, data subjects, and future maintainers.

Review triggers include boundary changes, new integration or supplier, jurisdiction change, incident, threat or hazard discovery, workload shift, accessibility finding, organizational transfer, expiring assumption, architecture decision, material evidence failure, and retirement. Operational feedback may reveal a stakeholder class that design-time discovery missed. Preserve this as learning rather than rewriting history to appear complete.

## Definitions and Notation

Let \(E\) be the entity of interest in environment \(\mathcal{E}\). Let \(S_K\) be the set of known in-scope stakeholder roles at time \(t\), and \(K\) the set of known material concerns. The subscript is a reminder that discovery is incomplete in principle; the true set of all legitimate stakeholders is generally not observable.

Define relations:

\[
H\subseteq S_K\times K
\]

for stakeholder-holds-concern, \(F\subseteq K\times V_P\) for concern-framed-by-viewpoint, \(R\subseteq K\times D\) for concern-responded-by-decision, and \(E_v\subseteq K\times X\) for concern-evaluated-by-evidence. \(V_P,D,X\) denote viewpoints, decisions, and evidence items.

For known-inventory response coverage,

\[
Cov_K=\frac{|\{c\in K:\operatorname{validResponse}(c)\}|}{|K|}
\]

when \(|K|>0\). If \(K=\varnothing\), report “no inventory,” not 100%. A valid response is a policy predicate requiring appropriate disposition, owner, rationale, and evidence or trigger. \(Cov_K=1\) proves only that every registered item satisfies that predicate.

For a stakeholder category \(s\), a representation record can be

\[
rep(s)=(method,representative,authority,gaps,followup).
\]

This records how a perspective enters the process. It does not assign equal decision authority or assert consent.

## Mechanisms, Invariants, or Proof Structure

Use the following repeatable mechanism.

1. **Frame:** declare entity, boundary, environment, purpose, lifecycle stage, and decision authority.
2. **Discover:** traverse acquisition, use, data, delivery, operation, assurance, supply, impact, and retirement relationships.
3. **Represent:** record participation, authority, limitations, absent groups, and follow-up channels.
4. **Elicit:** preserve original statements and evidence before normalization.
5. **Refine:** distinguish goal, concern, scenario, constraint, assumption, risk, request, and decision.
6. **Relate:** link concern to stakeholders, conflicts, viewpoints/views, decisions, evidence, owners, and triggers.
7. **Deliberate:** evaluate significance, non-compensable constraints, uncertainty, distributional consequences, and dissent.
8. **Respond:** choose an explicit disposition under the correct authority.
9. **Verify and validate:** check the specified response and observe whether stakeholder outcomes are served.
10. **Revisit:** react to triggers and maintain correspondence with the realized system.

The governing invariants are source preservation, no silent concern loss, explicit authority, claim-specific evidence, visible conflict, accountable disposition, and honest coverage scope.

The following executable example audits declared fields for three concern records. It is deterministic evidence for the register predicate only. It cannot establish stakeholder completeness, legitimate representation, threshold validity, decision quality, safety, compliance, or architecture fitness.

<!-- bijux-verify: {"id":"concern-register-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"C-01 addressed: ready\nC-02 open: attention[missing_evidence]\nC-03 deferred: attention[missing_trigger]\nsummary ready=1 attention=2\n","stderr":""}} -->
```python
records = [
    {
        "id": "C-01",
        "status": "addressed",
        "stakeholders": ["operator"],
        "source": "on-call interview",
        "scenario": "restore within 10 minutes after a zone failure",
        "view": "deployment-and-recovery",
        "owner": "service-owner",
        "evidence": "recovery exercise R-17",
        "trigger": "topology changes",
    },
    {
        "id": "C-02",
        "status": "open",
        "stakeholders": ["data-subject"],
        "source": "privacy review",
        "scenario": "delete linked records after an authorized request",
        "view": "information-lifecycle",
        "owner": "data-owner",
        "evidence": "",
        "trigger": "retention policy changes",
    },
    {
        "id": "C-03",
        "status": "deferred",
        "stakeholders": ["maintainer"],
        "source": "dependency analysis",
        "scenario": "upgrade the runtime without changing domain modules",
        "view": "module",
        "owner": "architecture-owner",
        "evidence": "baseline dependency graph",
        "trigger": "",
    },
]

ready = 0
for record in records:
    missing = []
    for field in ("stakeholders", "source", "scenario", "view", "owner"):
        if not record[field]:
            missing.append(f"missing_{field}")
    if record["status"] == "addressed" and not record["evidence"]:
        missing.append("missing_evidence")
    if record["status"] == "open" and not record["evidence"]:
        missing.append("missing_evidence")
    if record["status"] == "deferred" and not record["trigger"]:
        missing.append("missing_trigger")
    result = "ready" if not missing else f"attention[{','.join(missing)}]"
    ready += not missing
    print(f"{record['id']} {record['status']}: {result}")

print(f"summary ready={ready} attention={len(records) - ready}")
```

The audit intentionally treats an open item without evidence as requiring attention, even though open can be a legitimate state. In a production schema, rules should depend on concern class, disposition, evidence plan, and governance policy rather than a universal field checklist.

## Alternatives and Trade-Offs

**Individual interviews** reveal sensitive concerns and reduce group dominance but are slower and make conflicts harder to resolve collectively. **Facilitated workshops** expose assumptions and conflicts efficiently but inherit attendance and power bias. Combine them, and provide asynchronous or protected channels when participation risk differs.

**Role catalogues and checklists** offer repeatability and help novices remember operations, maintenance, assurance, and affected parties. They can create false closure and may not match a novel domain. Use them as prompts after boundary/consequence analysis, never as proof.

**Personas** make user contexts concrete but can become invented stereotypes. Ground them in research, state sampling limits, and do not use one persona to represent operators, data subjects, regulators, or other distinct roles.

**Backlog-only management** integrates concerns with delivery, ownership, and workflow. It often loses source, rationale, viewpoint relations, dissent, lifecycle scope, and rejected/deferred history. Link work items to a durable concern register rather than forcing one artifact to serve both governance and execution.

**Central architecture boards** can coordinate cross-system constraints and independent challenge but create delay, detached decisions, and power concentration. **Federated ownership** improves context and speed but can miss shared risks. Allocate authority by decision reach and consequence, with explicit escalation and exception paths.

**Quantitative prioritization** supports consistency and sensitivity analysis. Scores can conceal uncertain estimates, non-compensable obligations, and who bears harm. Publish inputs and uncertainty; use numbers to inform deliberation, not automate legitimacy.

**Comprehensive documentation** improves assurance and succession but can be expensive and stale. **Minimum documentation** reduces overhead but can omit rationale needed by future maintainers and reviewers. Documentation depth should follow consequence, lifespan, coordination, regulation, and reversibility; automate correspondence checks where their limitations are clear.

## Failure Modes and Misconceptions

- **“The customer is the stakeholder.”** Acquirers are one class; users, operators, maintainers, data subjects, affected non-users, suppliers, and assurance authorities can hold different interests.
- **“A stakeholder is anyone who asks.”** Interest must relate to the framed entity, but lack of access or voice does not remove legitimate affected parties.
- **“Every concern is a requirement.”** Concerns can motivate requirements, questions, risks, decisions, or evidence without being specified obligations.
- **“Every request must be implemented.”** Preserve the request, uncover its concern, analyze authority and alternatives, then record disposition.
- **“Quality attributes are concern statements.”** A category such as security or usability lacks actor, situation, response, measure, and priority.
- **“A workshop finds the stakeholders.”** It finds contributions from those invited and able to participate under its conditions.
- **“Voting creates objective priority.”** Votes reveal a framed group preference; they do not settle law, safety, rights, severity, or absent-party interests.
- **“Consensus means no conflict.”** It may mean power suppressed dissent or wording became vague. Record incompatible scenarios and residual disagreement.
- **“One viewpoint per stakeholder.”** Viewpoints frame recurring concern sets and can serve multiple roles; one role can need several viewpoints.
- **“A view addresses a concern because a link exists.”** Inspect semantics, correspondence, evidence, and stakeholder usability.
- **“100% coverage proves completeness.”** It covers only the registered denominator under a declared predicate.
- **“The architect owns acceptance.”** Concern, decision, evidence, and risk-acceptance authorities can differ; critical domains require qualified independent roles.
- **“Supplier assurance transfers accountability.”** Contracts and attestations are scoped evidence; integrators retain obligations for their system context.
- **“Stakeholder work ends after requirements.”** Incidents, operations, organizational changes, new jurisdictions, and retirement reveal new roles and concerns.

## Worked Examples

### Example 1

**Question:** Is “the product owner” a sufficient stakeholder model for a hosted invoicing service?

**Reasoning:** The product owner can prioritize product value but may not represent accountants, invoice recipients, support, operators, tax/legal authorities, accessibility needs, data subjects, payment providers, or maintainers. Map relationships across use, data, operation, assurance, supply, and retirement, then document representation and authority.

**Conclusion:** A named sponsor is an input, not a complete stakeholder model.

### Example 2

**Question:** An operator requests Kubernetes. What should enter the concern register?

**Reasoning:** Preserve the request and ask what loss it prevents. Suppose the operator needs automated restart, bounded recovery, safe secrets, observable health, and feasible on-call workload. Express those as scenarios and constraints. Kubernetes remains one option whose complexity, skills, failure modes, and exit cost need evidence.

**Conclusion:** Normalize the underlying interests without erasing the proposed solution.

### Example 3

**Question:** Does \(Cov_K=12/12=1\) show that every stakeholder concern is addressed?

**Reasoning:** It shows that all twelve known registered concerns satisfy the response predicate. If data subjects were never identified, their deletion and transparency concerns are outside \(K\). If a weak predicate accepts any hyperlink, the numerator is also misleading.

**Conclusion:** Publish denominator and predicate; known-inventory coverage is not discovery completeness.

### Example 4

**Question:** Should an operator and a security reviewer receive separate deployment views?

**Reasoning:** Both may need nodes, zones, identities, network paths, and failure boundaries. One semantically defined deployment view can support recovery and trust-boundary analyses, perhaps with distinct overlays. Separate views are justified when information density, confidentiality, or model conventions conflict—not merely because audiences differ.

**Conclusion:** Organize views by concerns and usable semantics, not headcount.

### Example 5

**Question:** A workshop votes performance first and accessibility last. Can architecture defer accessibility automatically?

**Reasoning:** Voting reflects participants and framing. Accessibility may be a legal obligation, an inclusion condition, or a capability prerequisite for an absent group. Determine authority, affected population, non-compensable constraints, severity, and representation gap before priority.

**Conclusion:** Workshop votes inform deliberation but cannot override legitimate obligations.

### Example 6

**Question:** A supplier claims 99.99% availability. Is the availability concern addressed?

**Reasoning:** The claim may exclude client configuration, regions, dependencies, planned maintenance, data correctness, and recovery of the integrated capability. Obtain definitions and evidence, model end-to-end dependencies, specify the stakeholder scenario, and assign residual-risk ownership.

**Conclusion:** Supplier evidence must be scoped to the integrated system concern.

### Example 7

**Question:** A concern is marked “out of scope” because data export happens after the API boundary. Is that sufficient?

**Reasoning:** A technical boundary does not erase downstream harm, interoperability, confidentiality, retention, or contractual obligations. Identify the surrounding system, receiving stakeholder, interface contract, and accountable authority. The response may be transferred, but correspondence and evidence remain necessary.

**Conclusion:** Scope decisions must expose displaced consequences and interfaces.

### Example 8

**Question:** An addressed recovery concern fails during an incident. What changes?

**Reasoning:** Preserve the prior evidence and decision. Record incident conditions, determine whether assumptions, topology, workload, procedures, or measures changed, reopen affected concerns, update stakeholders and boundary if necessary, and supersede evidence or decisions with traceable records.

**Conclusion:** Concern status is evidence-relative and must respond to lifecycle triggers.

### Example 9

**Question:** Can a concern audit approve architecture for an autonomous railway braking function?

**Reasoning:** The audit can find missing fields and trace links. It cannot validate hazard completeness, operational railway scenarios, human factors, control safety, cybersecurity, regulatory obligations, acceptable residual risk, or independence. No external academic, railway, regulatory, safety, or practitioner review is claimed. Named qualified railway-domain, safety, software, operations, human-factors, cybersecurity, assurance, and regulatory authorities must review stakeholder representation, hazards, scenarios, decisions, evidence, independence, residual risks, and change control.

**Conclusion:** Automation supports record integrity; qualified humans retain high-consequence judgment and authority.

### Example 10

**Question:** Who are the stakeholders when a service is retired?

**Reasoning:** Include current and dormant users, downstream consumers, record owners, data subjects, support, operations, legal/compliance, finance, suppliers, security, and future auditors. Concerns include export, compatibility, retention/deletion, access revocation, evidence preservation, cost termination, dependency discovery, and post-shutdown monitoring.

**Conclusion:** Retirement changes the stakeholder map; it does not eliminate it.

## Cross-Program Connections

- [Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) connects stakeholder goals to domain models and observable outcomes.
- [Software Engineering Methods & Evolution](../../10-software-engineering-methods-and-evolution/ROADMAP.md) supplies lifecycle feedback and change governance.
- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) relates stakeholder forces and consequences to recurring solutions.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) designs claim-specific verification and validation evidence.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) identifies assets, threat actors, trust boundaries, and risk authorities.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) treats stakeholder needs, lifecycle processes, system context, and assurance across wider system boundaries.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 42010:2022, Software, systems and enterprise—Architecture description](https://www.iso.org/standard/74393.html), edition 2, November 2022. Current standard for architecture-description structure, stakeholders, concerns, viewpoints, views, frameworks, languages, and model kinds; consulted 2026-08-29.
2. ISO/IEC. [ISO/IEC 25010:2023, SQuaRE—Product quality model](https://www.iso.org/standard/78176.html), edition 2, November 2023. Current product-quality reference model and lifecycle stakeholder use; consulted 2026-08-29.
3. Software Engineering Institute. [Quality Attribute Workshop Collection](https://www.sei.cmu.edu/library/quality-attribute-workshop-collection/), Carnegie Mellon University, 2016. Official method material for stakeholder-generated, prioritized, refined quality scenarios; consulted 2026-08-29.
4. Mario R. Barbacci et al. [Quality Attribute Workshops (QAWs), Third Edition](https://www.sei.cmu.edu/library/quality-attribute-workshops-qaws-third-edition/), CMU/SEI-2003-TR-016, 2003. Workshop process, participants, scenario generation, prioritization, and refinement.
5. Paul Clements et al. *Documenting Software Architectures: Views and Beyond*, second edition, Addison-Wesley, 2010. Stakeholder/viewpoint-driven architecture documentation, view packets, and correspondence.
6. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*, fourth edition, Addison-Wesley, 2021. Stakeholders, business goals, quality-attribute scenarios, architecture drivers, and evaluation.
7. Rick Kazman, Mark Klein, and Paul Clements. [ATAM: Method for Architecture Evaluation](https://sei.cmu.edu/library/atam-method-for-architecture-evaluation/), CMU/SEI-2000-TR-004, 2000. Stakeholder scenarios, risks, sensitivity points, and trade-off analysis.
8. Helen Sharp, Anthony Finkelstein, and Galal Galal. “Stakeholder Identification in the Requirements Engineering Process.” *Proceedings of the 10th International Workshop on Database and Expert Systems Applications*, IEEE, 1999. Role-based and interaction-oriented stakeholder identification.

## Exercises

### Exercise 1

For a university course-registration system, distinguish six stakeholder roles and state one architectural concern for each without proposing technology.

### Exercise 2

Turn “support wants a single admin database” into source-preserving concern records and trace one concern through scenario, viewpoint, decision, and evidence.

### Exercise 3

Diagnose a concern register with 40 rows, 100% “addressed” status, no stakeholder-source field, one generic architecture diagram, and no review triggers.

### Exercise 4

Design a stakeholder discovery and concern-prioritization process for replacing a regional public-transport ticketing platform. Address absent parties, power, conflict, and changing lifecycle roles.

### Exercise 5

Define architecture-concern assurance for an unfamiliar intensive-care medication-dosing platform. Separate automated coverage checks from named human review and decision authority.

## Answers to the Exercises

### Answer 1

Student/user: complete enrollment during peak demand with a confirmed, correct result. Registrar/record owner: preserve prerequisite, capacity, degree, and audit rules across changes. Instructor: receive an authoritative roster while approved late changes remain traceable. Accessibility stakeholder: complete every registration flow using applicable assistive interaction under the same deadlines. Operator: recover the registration capability within an agreed bound without losing accepted changes. Privacy/security authority or data subject: restrict sensitive academic records, expose legitimate access, and apply retention/deletion rules.

These are roles defined by relationships. Add acquirer, finance, support, identity provider, auditors, downstream learning systems, and future maintainers as scope requires. None of the concern statements mandates a database, cloud, queue, or vendor.

### Answer 2

Preserve: “support wants a single admin database,” source/date/representative, and the stated rationale. Elicitation may reveal distinct concerns: (C1) support must locate a customer’s relevant operational state within two minutes during an authorized case; (C2) access must be least-privilege and audited; (C3) inconsistent replicas must not cause an incorrect corrective action; (C4) the on-call team cannot operate multiple bespoke query tools.

For C1, specify the support actor, case type, normal/degraded environment, permitted customer scope, response, two-minute measure, and privacy exclusions. An information viewpoint frames data authority/lineage; an operational viewpoint frames the support workflow. Compare a consolidated read model, federated authorized queries, and a single system of record. Suppose the decision selects a derived support view with short-lived authorization, provenance, bounded staleness, and links to source systems. Evidence includes workflow usability tests, authorization tests, staleness/reconciliation tests, audit review, and timed incident exercises. This addresses the concern without silently treating “single admin database” as a requirement.

### Answer 3

The denominator has no trustworthy stakeholder relation, so it cannot demonstrate representation. “Addressed” lacks a predicate, source, authority, scenario, owner, disposition rationale, or evidence. One generic diagram is unlikely to express code, runtime, data, deployment, operational, security, and lifecycle semantics; links alone would not prove adequacy. Missing triggers make closure stale after incidents, decisions, suppliers, and boundary changes.

Reframe the entity and purpose; reconstruct stakeholder discovery from lifecycle, context, data, supply, impact, incident, contract, and assurance evidence; preserve raw sources; define concern classes and valid dispositions; refine material qualities into scenarios; map concerns to defined viewpoints/views, decisions, evidence, and owners; expose conflicts and gaps; add review triggers. Recompute coverage only over the declared, dated inventory and publish limitations.

### Answer 4

Frame the transport ecosystem: riders, non-rider affected parties, operators, drivers/inspectors, support, accessibility groups, municipalities, acquirer/funder, finance, privacy/data authorities, security and fraud teams, payment and identity suppliers, maintainers, downstream mobility services, legal/regulatory authorities, and future retirement owners. Discover through field observation, accessible research sessions, complaint/incident data, data and payment flows, frontline interviews, supplier/contracts, assurance analysis, and separate facilitated workshops. Fund participation and provide language, accessibility, asynchronous, and protected channels.

Preserve scenario sources and sampling limits. Do not let an executive vote override accessibility, privacy, safety, or statutory obligations. Prioritize mission value, severity, affected population, uncertainty, irreversibility, dependency, authority, and non-compensable constraints; record dissent and who bears cost. Map concerns to context, information, runtime, deployment, operational, security, migration, and retirement viewpoints. Publish open and rejected concerns with owners and appeal/escalation routes. Re-run discovery at procurement, pilot, migration, operation, incident, supplier change, and legacy shutdown because roles and consequences change.

### Answer 5

Automated controls can validate schema fields; stable stakeholder/concern identifiers; bidirectional trace links among hazards, scenarios, requirements, decisions, models, tests, configuration, releases, and incidents; missing owners/approvals; version/digest integrity; model/test execution; dose-limit invariants in a defined model; access controls; evidence freshness; and change-trigger coverage. Tool output establishes only the specified model and record predicates.

No external academic, clinical, regulatory, safety, or practitioner review is claimed. Named qualified clinicians, pharmacists, nursing/workflow experts, patients or legitimate patient representatives, clinical-safety engineers, software and data engineers, human-factors/accessibility experts, cybersecurity/privacy experts, operations/support, independent assurance, quality management, and applicable regulatory authorities must review representation, intended use, clinical workflow, dosing semantics, units, contraindications, data/model provenance, hazards, fail-safe behavior, alarms, overrides, degraded modes, validation populations, evidence independence, residual risk, rollout, monitoring, rollback, and change control. Product or architecture owners decide ordinary design within delegated authority; clinical-risk acceptance, release authorization, and emergency restriction belong to explicitly named qualified authorities. Missing critical evidence or unresolved high-severity concern blocks the corresponding completion or deployment claim.
