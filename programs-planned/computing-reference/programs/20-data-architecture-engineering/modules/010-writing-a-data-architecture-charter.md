---
module_id: DARCH-010
program: Data Architecture Engineering
level: 1
module_number: 10
title: Writing a Data Architecture Charter
status: complete
last_verified: 2026-09-03
---

# Writing a Data Architecture Charter

## One-Page Review

### Governing question

How can an organization write a data architecture charter that gives a bounded mandate, connects outcomes to architecture work, assigns legitimate decision rights and resources, and makes progress, exceptions, evidence, and reassessment auditable?

### Essential definitions

- A **data architecture charter** is an authorized operating agreement for a bounded architecture endeavor: why it exists, what it covers, which outcomes and decisions it serves, who may decide and contribute, what evidence and work products are required, and when the mandate changes or ends.
- A **mandate** is the legitimate source and extent of authority to perform work or make decisions; sponsorship, expertise, ownership, and approval are related but distinct roles.
- **Scope** defines included and excluded capabilities, data, decisions, organizations, jurisdictions, lifecycle intervals, and dependencies.
- An **outcome** is a valuable change in stakeholder or organizational condition; an **output** is a work product, system change, or activity that may contribute to an outcome.
- A **decision right** states who decides what, under which criteria and constraints, after which consultation, with which appeal or escalation path.
- A **success measure** has an operational definition, baseline, target or guardrail, horizon, source, segmentation, owner, uncertainty, and response.
- An **exception** is an authorized, bounded departure from an applicable rule with rationale, risk, compensating action, expiry, and closure evidence.
- A **review trigger** is an observable condition that requires the charter, architecture direction, decision, or evidence plan to be reconsidered.

### Central model, mechanism, or theorem

Model a charter as:

`X = (mandate, outcomes, boundary, stakeholders, authority, drivers, rules, work, evidence, governance, triggers)`

A charter is actionable only when authority covers its decisions, resources cover its obligations, outputs trace to outcome hypotheses and decision uses, mandatory constraints remain noncompensable, success measures are operational, and exceptions and changes have explicit paths. The charter authorizes bounded work and governance; it does not prove that the proposed architecture will achieve its outcomes.

### Critical invariants

- The mandate names its issuing authority, decision scope, effective period, resource commitment, superseded agreements, and termination or renewal path.
- Outcomes identify beneficiaries and affected parties, baseline, desired change, horizon, evidence, counter-metrics, and accountable owner.
- Scope names inclusions, exclusions, interfaces, external dependencies, current/transition/target applicability, and authority boundaries.
- Stakeholder participation is separated from approval, technical authority, semantic ownership, policy interpretation, implementation, operation, and risk acceptance.
- Every proposed output supports a named decision, obligation, outcome hypothesis, or evidence need.
- Principles, policies, constraints, preferences, assumptions, and architecture decisions remain distinct and trace to their sources.
- Metrics cannot be declared successful without denominators, measurement semantics, source quality, uncertainty, and distributional review.
- Every exception records authority, scope, consequence, controls, expiry, and closure evidence.
- Funding, staffing, access, tooling, and time are consistent with the charter's obligations or the gap is explicit.
- Material changes trigger reassessment and propagation; the charter is versioned, not silently rewritten.

### Common failures

Common failures are copying a project-charter template; describing technology before mandate and outcomes; using “single source of truth” as an unbounded goal; defining scope only by systems; naming a sponsor but no decision rights; treating an architecture council as owner of domain meaning; promising governance without staff or access; listing deliverables with no decisions; measuring catalog entries instead of improved decisions; hiding affected groups; converting legal interpretation into architectural fact; calling preferences constraints; averaging away mandatory limits; granting permanent exceptions; omitting transition and retirement; and allowing a steering meeting to change the charter without a controlled decision.

### Compact example

A retailer proposes a charter to “build an enterprise lake and govern all data.” It has no issuing authority, decision boundary, outcome baseline, product consumers, funding, or exception route. The rewritten charter is bounded to inventory availability for store and online fulfillment in two regions. It authorizes semantic and interface decisions for five named flows, preserves domain ownership, funds two engineers and steward capacity, requires current/target views and recovery evidence, sets freshness and correction guardrails, excludes customer identity, and expires after the rollout decision unless renewed. The charter now enables decisions without claiming enterprise-wide control.

### Connections

[DARCH-001](001-data-architecture-as-structure-flow-ownership-and-policy.md) defines the discipline, [DARCH-002](002-business-strategy-and-data-outcomes.md) connects strategy to evidence, and [DARCH-003](003-current-state-data-landscape.md) supplies current-state facts. [DARCH-006](006-data-principles-and-decision-rules.md), [DARCH-007](007-architecture-drivers-and-constraints.md), [DARCH-008](008-data-risk-and-criticality.md), and [DARCH-009](009-architecture-views-and-stakeholders.md) provide rules, drivers, risks, and view obligations. This charter closes the introductory block and governs the modeling work that follows.

## Governing Question

A charter must answer a deceptively practical question: what legitimate agreement allows this architecture work to consume attention, constrain choices, request evidence, and make or recommend decisions? Without that agreement, architecture becomes either advisory theater or unaccountable power.

The charter is not the architecture. It is not a catalog, target diagram, roadmap, governance policy, funding request, or project plan, though it connects to each. It establishes the endeavor's mandate and rules of operation. The architecture team then produces decisions and evidence within that boundary.

The charter must also remain falsifiable. It should explain how leaders will know whether the work improves outcomes, which signals would invalidate its assumptions, what changes require renewed authority, and when the endeavor should stop. An immortal architecture program with expanding scope and activity-only metrics is not governed merely because it has a document.

## Why This Matters

Data architecture crosses organizational boundaries. A change to identifiers, retention, event contracts, mastering, placement, lineage, access, recovery, or decommissioning can affect revenue, public service, privacy, security, safety, audit, supplier commitments, and daily work. A technical team cannot legitimately settle all those consequences by itself.

Ambiguous authority creates two symmetrical failures. In one, architecture produces elegant recommendations that delivery teams may ignore because nobody authorized the decisions or resources. In the other, an architecture board assumes universal authority and overrides domain knowledge, product accountability, law, policy, or affected people without a legitimate mandate.

ISO/IEC/IEEE [42010:2022](https://www.iso.org/standard/74393.html) distinguishes an entity's architecture from its architecture description and structures descriptions around stakeholders, concerns, viewpoints, and models. A charter sits around that description: it identifies the entity, purposes, stakeholders, decisions, and governance that make the description useful. The standard does not prescribe a charter format or organization-specific decision authority.

The Open Group's TOGAF Standard includes preliminary, vision, governance, content, and change-management concerns within a broader enterprise architecture method. The [Architecture Development Method](https://pubs.opengroup.org/togaf-standard/adm/) can inform scope, capability, stakeholders, work, and governance. It should be tailored rather than converted into a mandatory artifact list.

A strong charter reduces waste. It tells contributors which decisions matter, tells stakeholders how to participate and challenge, tells delivery teams what architecture constraints are authoritative, tells reviewers which evidence is sufficient, and tells sponsors what resources and trade-offs they have actually approved.

## Prerequisites and Retrieval

You should understand business and public outcomes, system and organizational boundaries, current-state discovery, data roles, principles and policies, drivers and constraints, uncertainty, risk, stakeholders and concerns, architecture views, decision records, roadmaps, governance, and measurement.

Retrieve mandate, sponsor, accountable owner, decision authority, technical authority, semantic owner, policy authority, risk acceptor, stakeholder, beneficiary, affected party, scope, exclusion, dependency, output, outcome, baseline, target, guardrail, counter-metric, assumption, exception, evidence, review trigger, renewal, and termination.

As a retrieval test, read a charter that promises “a trusted data platform.” Ask who issued it, which decisions are authorized, which products and regions are included, whose trust and for what use, which baseline and evidence apply, which rules cannot be traded away, what resources are committed, how domains retain authority, how exceptions expire, and when the mandate is reviewed. Missing answers are governance risks, not editorial gaps.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish a data architecture charter from an architecture description, roadmap, policy, program plan, and project charter;
2. establish a legitimate mandate, decision boundary, effective period, funding commitment, and renewal or termination path;
3. express outcomes as testable changes for named beneficiaries and affected parties;
4. define scope across decisions, capabilities, data, organizations, jurisdictions, lifecycle states, and interfaces;
5. assign sponsor, owner, decision, technical, semantic, policy, evidence, implementation, operations, and risk roles;
6. connect drivers, constraints, principles, assumptions, risks, views, work products, and decisions without conflation;
7. define measures, guardrails, evidence thresholds, and learning actions with honest uncertainty;
8. create governance, escalation, dissent, exception, and change-control paths;
9. align work, staffing, access, funding, dependencies, and milestones to decision need;
10. review, approve, maintain, renew, supersede, and close a charter through explicit evidence.

## Core Exposition

**State document identity and authority first.** Record charter identifier, title, entity or endeavor, status, version, issuing body, accountable sponsor, charter owner, effective date, review date, expiry, approvals, superseded charters, and controlled location. A signature proves authorization by named parties; it does not prove that claims are correct or that missing stakeholders agree.

**Write a bounded mandate.** Explain why the architecture endeavor exists and what it is authorized to do. Separate decision rights from recommendation, facilitation, standards stewardship, assurance, funding, and delivery. For each authority, name the subject, boundary, criteria, required consultation, escalation, appeal, and delegation limits.

“The data architecture team governs data” is unusable. A bounded mandate might authorize the team to approve cross-domain semantic identifiers and interoperability contracts for a named portfolio, recommend placement options to product owners, verify required architecture evidence at investment gates, and escalate unresolved policy conflicts to a named authority. It does not seize ownership of source facts or accept operational risk.

**Identify the source of mandate.** Authority may derive from board or executive delegation, legislation, regulation, policy, contract, investment governance, product accountability, or a joint agreement among autonomous parties. Preserve the source and its limits. A workshop vote cannot expand authority, and urgency does not turn expertise into approval power.

**Frame the problem without preselecting the solution.** Describe observed conditions, affected outcomes, causal hypotheses, evidence, uncertainty, and urgency. “Duplicate customer identifiers create correction delays and inconsistent eligibility decisions” frames a problem. “We need one enterprise database” embeds a design before alternatives and constraints are examined.

**Define outcomes and beneficiaries.** Each outcome record should include outcome statement, beneficiaries, affected groups, current baseline, desired direction or threshold, horizon, causal hypothesis, leading and lagging indicators, counter-metrics, evidence source, uncertainty, owner, and review trigger. Include harms that must not increase while optimizing the primary outcome.

Outputs are necessary but insufficient. A glossary, canonical model, platform, policy, lineage graph, migration plan, or council is not an outcome. State what decision or behavior it enables and how that contribution will be tested. Stop or change outputs that do not improve the intended outcome.

**Declare scope in several dimensions.** Cover business capabilities and decisions; data subjects, products, flows, and representations; organizational domains and partners; applications, platforms, and interfaces; jurisdictions and populations; environments and regions; current, transition, target, and retirement intervals; and architecture decisions or work products. Name exclusions and adjacency explicitly.

Scope boundaries are interfaces, not walls. For each excluded dependency, identify owner, contract, assumption, risk, and escalation. Excluding customer identity from an inventory charter does not remove the identity dependency. It means the dependency must be governed at the boundary rather than redesigned under this mandate.

**Separate current, transition, and target applicability.** A principle or contract may govern the target while a time-bounded exception permits current operation. A legacy source may remain authoritative during coexistence. State effective conditions and exit evidence so teams do not apply target rules prematurely or turn transition choices into permanent architecture.

**Build the stakeholder and authority model.** Include beneficiaries, affected parties, sponsors, portfolio and product owners, source producers, consumers, domain data owners and stewards, architects, engineers, operators, maintainers, security, privacy, legal, records, safety, accessibility, finance, procurement, suppliers, auditors, regulators, support, and reviewers as applicable.

For each role, record interest and concern, contribution, decision or approval right, evidence responsibility, communication need, availability, conflict, and representation basis. Use a decision-right matrix more precise than one generic RACI. Consultation does not imply concurrence; concurrence does not imply authority; authority does not establish technical truth.

**Record principles, policies, constraints, and preferences correctly.** Principles guide recurring choices. Policies impose authorized rules. Constraints restrict the feasible space. Preferences rank acceptable options. Assumptions temporarily bridge evidence gaps. Architecture decisions choose among alternatives. Give each a stable identifier and source; do not launder a favored technology into the charter as an external constraint.

Mandatory legal, rights, safety, contractual, and policy conditions are feasibility gates. They are not points that benefits elsewhere can offset. Architects should record the authorized interpretation and review path rather than present their own legal judgment as law.

**Summarize current-state evidence.** Include the relevant landscape, capabilities, products, flows, semantic conflicts, systems of record and engagement, contracts, quality, controls, recovery, cost, organizational capacity, decisions, debt, and uncertainty. Link governed evidence rather than pasting a static inventory into the charter. State confidence and discovery gaps.

**Express architecture direction without pretending the design is settled.** Direction can describe desired capabilities, boundaries, qualities, principles, transition posture, and option constraints. Preserve alternatives where evidence is incomplete. A charter may require domain-owned products with governed contracts without choosing a specific broker, database, catalog, or organizational topology.

**Define required views and decision records.** Select views from stakeholder concerns and uses: context, conceptual, logical, flow/lineage, authority, interface, deployment, quality, protection, operations/recovery, transition, and cost. For each, name decision, audience, owner, source, evidence threshold, access, update trigger, and correspondence obligations. Require architecture decision records for material choices and supersession.

**Specify work as decision-enabling increments.** A work item should state question, output, decision or evidence use, owner, contributors, dependencies, entry evidence, acceptance condition, due or latest-useful date, resource need, risk, and downstream effect. Organize sequencing by learning, risk, dependency, reversibility, and decision dates rather than by document completion alone.

Create a roadmap that joins current constraints, transition states, target capability, migration, coexistence, training, operational readiness, recovery, decommissioning, and benefit evidence. Milestones should represent decisions or demonstrated capability, not percentages of diagrams drawn.

**Make resources explicit.** Record funding source and bound, staff roles and capacity, domain participation, specialist review, data and environment access, tooling, procurement, supplier effort, training, change support, and operational ownership. If required resources are uncommitted, classify them as dependencies and restrict the promise accordingly.

Under-resourced governance shifts work invisibly to stewards, engineers, analysts, and operators. Estimate recurring decision and evidence workload, not only initial authoring. A charter that mandates manual classification for thousands of products without funded capacity is an unfunded policy claim.

**Define success measures with operational semantics.** Measures might concern decision latency, correction propagation, semantic defect escape, interoperability lead time, data fitness, recovery achievement, policy exceptions, consumer task success, incident consequence, retirement, cost, or stakeholder outcome. For each, state numerator, denominator, start/end events, exclusions, segments, distribution, source, cadence, owner, baseline, target or guardrail, confidence, and response.

Activity metrics such as meetings, catalog coverage, models published, standards written, or training attendance can measure delivery. They do not establish outcome. Pair them with adoption, decision, quality, risk, operational, and distributional evidence. Beware Goodhart effects: teams may maximize registered assets while leaving consequential flows unknown.

**State an evidence and learning plan.** Map important claims and assumptions to current evidence, confidence, consequence if false, validation method, owner, deadline, decision affected, and response. Use interviews, record review, profiling, lineage discovery, representative workloads, prototypes, contract tests, recovery exercises, privacy/security/safety analysis, cost models, usability tests, and operational telemetry as appropriate.

SEI's [Quality Attribute Workshop collection](https://www.sei.cmu.edu/library/quality-attribute-workshop-collection/) describes stakeholder-centered scenario generation and refinement before an architecture exists. Such scenarios can sharpen charter drivers and evidence needs. A workshop result is input; it does not confer legal authority, guarantee representative participation, or approve architecture.

**Govern decisions and dissent.** Define meeting and asynchronous mechanisms, quorum if relevant, required roles, evidence package, decision record, time bounds, nonconcurrence, escalation, appeal, emergency decisions, and communication. Avoid consensus theater. Some decisions legitimately require one accountable authority after consultation; the record should preserve material dissent and consequence.

**Design an exception path.** Identify the rule, requester, rationale, scope, affected parties, consequence, risk owner and acceptor, alternatives considered, compensating controls, evidence, approval authority, effective and expiry dates, monitoring, renewal conditions, and closure proof. No team approves its own exception unless the mandate explicitly and legitimately grants that power.

**Control change.** Define which changes the charter owner may make editorially and which require renewed approval: scope expansion, new jurisdiction, changed outcome, material funding reduction, decision-right change, relaxed constraint, new affected population, major supplier, or extended expiry. Preserve version history and propagate decisions to roadmaps, views, contracts, policies, delivery plans, and evidence.

**Set review and termination criteria.** Review on calendar and event triggers: strategy change, new regulation or policy, acquisition, incident, missed outcome, invalidated assumption, repeated exception, cost threshold, major architecture decision, lifecycle transition, or loss of resources. Renew only with evidence. Close when outcomes are embedded in enduring ownership, the mandate expires, the problem no longer warrants work, or the endeavor is superseded.

Termination includes disposition of open decisions, artifacts, access, contracts, risks, exceptions, metrics, staffing, and records. “Program complete” does not mean responsibilities disappear. Transfer them to named operational and governance owners with acceptance evidence.

NIST's [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) emphasizes governance, organizational context, roles, policy, oversight, and risk strategy alongside identify, protect, detect, respond, and recover outcomes. The [Privacy Framework](https://www.nist.gov/privacy-framework) similarly provides voluntary risk-management structure. They can inform charter concerns and evidence, but neither substitutes for applicable law, local policy, specialist interpretation, or a complete data architecture charter.

**Write for use.** Place the bounded mandate, decisions, scope, outcomes, roles, hard constraints, resources, and next review in a concise front section. Link detailed registers and evidence. Use stable identifiers, real line breaks, accessible tables, defined terms, clear status, and navigable references. Test whether a contributor can determine what to do and whether a stakeholder can challenge an unsupported claim.

## Definitions and Notation

Let a charter be:

`X = (M, O, B, S, A, D, R, W, E, G, T)`

where `M` is mandate, `O` outcomes, `B` boundary and scope, `S` stakeholders, `A` authority and roles, `D` drivers/constraints/assumptions/risks, `R` principles and applicable rules, `W` work and architecture outputs, `E` evidence and measures, `G` decision/exception/change governance, and `T` review, renewal, closure, and transition triggers.

For output `w`, define `supports(w,o,d,e)` to mean that `w` supports outcome hypothesis `o`, decision `d`, or evidence obligation `e`. Output closure requires every funded output to have at least one typed support relation. This prevents deliverable lists from becoming self-justifying.

For decision `d`, let `authorized(a,d,b,t)` state that authority `a` may decide `d` inside boundary `b` at time `t`. A recorded approval is valid only when the approver's delegated authority covers that exact decision and conditions. Signature count cannot repair an authority mismatch.

For measure `q`, an operational definition is `q = (population, event, value, unit, aggregation, window, exclusions, segments, source, baseline, target_or_guardrail, uncertainty, owner, response)`. A number missing these semantics is not reproducible evidence.

## Mechanisms, Invariants, or Proof Structure

Use ten gates to write and approve a data architecture charter.

**1. Mandate gate.** Establish issuing authority, problem, decision boundary, effective period, resources, supersession, renewal, and termination.

**2. Outcome gate.** Name beneficiaries, affected parties, baseline, desired change, causal hypothesis, horizon, indicators, counter-metrics, and owner.

**3. Scope gate.** Bound capabilities, decisions, data, products, flows, organizations, jurisdictions, lifecycle states, interfaces, dependencies, inclusions, and exclusions.

**4. Stakeholder and authority gate.** Separate participation, expertise, ownership, recommendation, concurrence, approval, implementation, operations, evidence, and risk acceptance.

**5. Driver and rule gate.** Trace drivers, constraints, assumptions, risks, principles, policies, preferences, and existing decisions to sources and applicability.

**6. Direction and work gate.** Connect architecture direction, views, decisions, outputs, roadmap, migration, and retirement to outcome and evidence uses.

**7. Resource gate.** Reconcile funding, capacity, specialist participation, access, tooling, suppliers, training, and recurring governance with obligations.

**8. Evidence gate.** Operationalize measures, validate assumptions, state confidence, preserve counter-metrics, and define learning responses.

**9. Governance gate.** Define decision, dissent, escalation, appeal, exception, emergency, change, communication, and propagation mechanisms.

**10. Lifecycle gate.** Set approval criteria, review triggers, versioning, renewal, supersession, closure, and responsibility transfer.

The executable example checks a small charter register. It detects an outcome without a baseline, an output without a decision or evidence use, a decision with no authorized approver, and an exception whose expiry is absent.

<!-- bijux-verify: {"id":"charter-register-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"records=4\nvalid=0\nfindings=customer-correction:missing-baseline,domain-model:missing-use,identity-policy:missing-authority,legacy-export:missing-expiry\nready=false\n","stderr":""}} -->
```python
records = (
    {"id": "customer-correction", "kind": "outcome", "baseline": None, "use": "reduce correction delay", "authority": "portfolio", "expiry": "n/a"},
    {"id": "domain-model", "kind": "output", "baseline": "n/a", "use": "", "authority": "architecture", "expiry": "n/a"},
    {"id": "identity-policy", "kind": "decision", "baseline": "n/a", "use": "authorize identifier rules", "authority": "", "expiry": "n/a"},
    {"id": "legacy-export", "kind": "exception", "baseline": "n/a", "use": "bounded coexistence", "authority": "risk-owner", "expiry": ""},
)

findings = []
valid = 0
for record in records:
    local = []
    if record["kind"] == "outcome" and record["baseline"] is None:
        local.append("missing-baseline")
    if record["kind"] == "output" and not record["use"]:
        local.append("missing-use")
    if record["kind"] == "decision" and not record["authority"]:
        local.append("missing-authority")
    if record["kind"] == "exception" and not record["expiry"]:
        local.append("missing-expiry")
    if local:
        findings.extend(f"{record['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"records={len(records)}")
print(f"valid={valid}")
print(f"findings={','.join(sorted(findings))}")
print(f"ready={str(not findings).lower()}")
```

The checker validates only four declared field rules. It does not establish legitimate authority, representative outcomes, sufficient resources, correct baselines, lawful policy, effective controls, architecture quality, or stakeholder agreement. Those require source records, accountable review, domain interpretation, and empirical evidence.

## Alternatives and Trade-Offs

**Enterprise charter versus bounded domain charter.** Enterprise scope can coordinate systemic concerns but becomes vague and centralized. Domain scope improves accountability but can miss cross-domain effects. Use nested charters with explicit interfaces and precedence where authority supports them.

**Outcome-led versus deliverable-led planning.** Outcomes preserve purpose and learning but are harder to attribute. Deliverables are controllable but invite output theater. Tie every output to a decision, hypothesis, evidence need, and stop condition.

**Detailed charter versus concise charter with registers.** Detail improves auditability but makes the primary agreement hard to read. Concision improves use but can hide ambiguity. Keep the controlling decisions concise and link versioned supporting registers.

**Permanent council versus time-bounded mandate.** Permanence supports continuity but encourages jurisdiction growth. A bounded mandate sharpens accountability but may fragment enduring work. Assign stable operational ownership while periodically renewing architecture authority from evidence.

**Central decision rights versus federated rights.** Centralization can resolve shared standards and concentration risk. Federation preserves semantic and product accountability. Allocate rights by decision type, consequence, and legitimate authority rather than one ideological model.

**Fixed roadmap versus adaptive evidence plan.** Fixed sequencing aids commitment and procurement. Adaptive sequencing responds to learning. Protect hard obligations and decision dates while allowing evidence to change reversible work.

**Ambitious target versus funded minimum.** Ambition can mobilize change but creates unfunded promises. A smaller funded scope may deliver evidence and capability. State option paths and conditions for expansion rather than pretending resources exist.

## Failure Modes and Misconceptions

1. **The charter is a project kickoff.** It governs continuing authority, decisions, evidence, exceptions, change, and closure.
2. **The sponsor owns every decision.** Funding authority does not imply semantic, legal, technical, or risk authority.
3. **Scope is a system list.** Decisions, data, organizations, jurisdictions, lifecycle states, interfaces, and exclusions also matter.
4. **A target technology is the outcome.** Products and diagrams are outputs; stakeholder condition is the outcome.
5. **A slogan is measurable.** “Trusted,” “democratized,” and “real time” require users, scenarios, measures, and evidence.
6. **Architecture owns the data.** Ownership follows accountable domain and policy authority, not documentation authorship.
7. **A steering vote resolves constraints.** Mandatory obligations require the proper interpretation, waiver, or redesign authority.
8. **Catalog percentage proves benefit.** Activity and declaration measures do not establish fitness, use, or reduced harm.
9. **Unfunded participation is committed.** Named people, capacity, access, and budgets must be authorized.
10. **An exception is permanent compatibility.** Exceptions need consequence, controls, expiry, renewal, and closure.
11. **Approval proves feasibility.** It establishes a decision by authorized parties, not factual truth or outcome achievement.
12. **The charter never ends.** Renewal and closure keep mandate proportional to current evidence and need.

## Worked Examples

### Example 1

A bank charter says the central architecture board owns all customer data. Domain executives own source-accountability decisions, privacy counsel owns policy interpretation, and operational risk accepts exposure. The charter is revised to give the board authority over cross-domain identity contracts and evidence gates while preserving those authorities. Coordination no longer depends on a false ownership claim.

### Example 2

A public agency's goal is “100% catalog coverage.” Teams register empty records to meet it. The revised outcome is faster, more accurate eligibility correction for named programs, with catalog completeness as one leading indicator and correction time, error recurrence, appeal burden, and subgroup outcomes as evidence and counter-metrics.

### Example 3

A healthcare charter includes every platform but excludes clinical users because the work is “technical.” Recovery and identity decisions then optimize infrastructure uptime while delaying patient care. The stakeholder model adds clinical safety authority, clinicians, registration staff, accessibility, and patient representation; outcome and recovery gates become noncompensable.

### Example 4

A retailer mandates streaming for all inventory data. Current-state evidence shows one daily supplier file, one high-rate store event, and several correction workflows. The charter replaces the technology mandate with freshness, correction, provenance, cost, and recovery scenarios. Teams may now choose batch, events, queries, or hybrids by evidence.

### Example 5

A two-year program funds model creation but no steward or operations capacity. The resource gate estimates recurring review, exception, quality, incident, and migration work. Scope is reduced to three decision paths, domain capacity is funded, and expansion becomes conditional on measured workload and benefit.

### Example 6

A merger charter says “standardize both companies within six months.” Jurisdictions, contracts, retention holds, customer identity, and exit costs are unknown. The charter authorizes discovery and reversible interface decisions first, sets legal and risk gates, and defers irreversible mastering until evidence closes critical assumptions.

### Example 7

An exception allows an unencrypted legacy export “until replacement.” There is no owner or date. The corrected record names affected data and parties, approval authority, transfer controls, monitoring, a 90-day expiry, migration owner, funded work, renewal evidence, and automatic escalation. Silence no longer renews risk.

### Example 8

An architecture council approves a canonical model by majority vote despite domain nonconcurrence about meaning. The decision matrix shows the council may require interoperability but the domain owns semantic definitions. A mediated contract maps domain concepts to shared exchange semantics and preserves disagreement, tests, and change rules.

### Example 9

A charter reports success because all ten diagrams were delivered. Consumer task testing shows teams still cannot find authority or assess schema impact. The outputs are reconnected to decision uses, view navigation and correspondences are repaired, and success depends on bounded task performance and defect evidence rather than publication.

### Example 10

An initiative meets its correction-time outcome and embeds contract, ownership, quality, recovery, and change responsibilities in product operations. The closure review transfers open risks and metrics, retires temporary forums and access, preserves approved decision baselines, and ends the charter. Governance continues through named enduring owners rather than an immortal program.

## Cross-Program Connections

- **Systems engineering:** charters connect mission, stakeholders, boundaries, requirements, risks, evidence, lifecycle decisions, and accountable authorities.
- **Product management:** outcomes, hypotheses, roadmaps, discovery, counter-metrics, and stop conditions keep architecture connected to value.
- **Project and program management:** funding, capacity, dependencies, milestones, procurement, communication, and closure make the mandate executable.
- **Software architecture:** drivers, quality scenarios, views, decisions, trade-offs, and evaluations become controlled charter obligations.
- **Data engineering:** profiling, lineage, contracts, pipelines, observability, recovery, and migrations supply evidence and implementation paths.
- **Platform engineering:** paved roads, policy, tenancy, control planes, service levels, and product operating models need bounded authority and adoption evidence.
- **Security, privacy, safety, and compliance:** specialist authority, hard constraints, risk acceptance, evidence, exceptions, and affected parties must be explicit.
- **Organizational design:** decision rights, incentives, ownership, staffing, escalation, and federated boundaries determine whether architecture can operate.

## References

1. ISO/IEC/IEEE, *42010:2022 Software, systems and enterprise—Architecture description*, 2022. <https://www.iso.org/standard/74393.html>
2. ISO/IEC/IEEE, *15288:2023 Systems and software engineering—System life cycle processes*, 2023. <https://www.iso.org/standard/81702.html>
3. The Open Group, *TOGAF Standard, 10th Edition: Architecture Development Method*, current web edition. <https://pubs.opengroup.org/togaf-standard/adm/>
4. The Open Group, *TOGAF Standard, 10th Edition: Architecture Content*, current web edition. <https://pubs.opengroup.org/togaf-standard/architecture-content/>
5. Software Engineering Institute, *Quality Attribute Workshop Collection*, 2016. <https://www.sei.cmu.edu/library/quality-attribute-workshop-collection/>
6. Software Engineering Institute, *Views and Beyond Collection*, 2009–2018. <https://www.sei.cmu.edu/library/views-and-beyond-collection/>
7. National Institute of Standards and Technology, *Cybersecurity Framework 2.0*, 2024. <https://www.nist.gov/cyberframework>
8. National Institute of Standards and Technology, *Privacy Framework*, current web edition. <https://www.nist.gov/privacy-framework>

## Exercises

### Exercise 1

Rewrite this mandate: “The data office owns all enterprise data and will create a single source of truth.” Define legitimate authorities, bounded decisions, scope, interfaces, outcomes, evidence, resources, and expiry without preselecting one implementation.

### Exercise 2

Create a charter outcome record for reducing inventory-related canceled orders. Include beneficiaries and affected parties, baseline, target or direction, causal hypothesis, leading and lagging indicators, counter-metrics, segments, evidence, uncertainty, owner, and review trigger.

### Exercise 3

Design a decision-right matrix for shared customer identity. Cover domain meaning, exchange contract, privacy-purpose interpretation, technical design, funding, implementation, operations, evidence, exception, risk acceptance, appeal, and emergency action.

### Exercise 4

A roadmap contains 24 outputs: 15 trace to decisions and outcomes, 3 trace only to evidence obligations, 4 have no typed use, and 2 violate a hard policy constraint. Compute declared support coverage under stated rules, then explain why the ratio cannot authorize the roadmap.

### Exercise 5

Review a charter whose scope doubles, funding falls 30%, a new jurisdiction is added, the main assumption is invalidated, and three exceptions have expired. Specify required decisions, evidence, containment, propagation, renewal conditions, and possible closure.

## Answers to the Exercises

### Answer 1

Replace universal ownership with a mandate issued by named portfolio authorities. Authorize the data office to facilitate shared semantic and interoperability decisions, maintain cross-domain views and evidence, verify applicable architecture gates, and escalate unresolved conflicts for a named portfolio and period. Domain owners retain source-fact accountability; policy and legal authorities interpret obligations; product owners fund and deliver; operations own service; risk owners accept residual exposure.

Bound the first scope to named customer and order decision paths, regions, interfaces, current/transition/target intervals, and explicitly governed external identity dependencies. Seek reduced correction delay and inconsistent decisions, not one store. Require alternative analysis, semantic/lineage/authority/recovery views, representative evidence, committed steward and engineering capacity, decision records, exception expiry, and review after six months or material triggers. Renew only if evidence supports wider authority.

### Answer 2

Outcome: reduce inventory-related cancellation after accepted orders for store and online fulfillment while avoiding increased oversell, customer inequity, manual workload, and supplier penalties. Beneficiaries include customers and fulfillment teams; affected parties include store staff, suppliers, support, and low-connectivity customers. Define baseline cancellation rate with eligible-order denominator, reason-code quality, channel/region/item segments, and confidence interval.

Set a locally authorized target and horizon only after baseline review. The hypothesis is that governed availability semantics, faster accepted-event propagation, correction workflows, and observable staleness reduce false availability. Leading indicators include contract adoption, freshness distribution, correction completion, and unknown inventory; lagging indicators include attributable cancellations and support burden. Counter-metrics include oversell, latency, staff workload, exclusion by channel, cost, and incidents. Product operations owns outcome evidence; architecture owns contribution evidence. Trigger review on denominator changes, channel disparity, weak reason codes, cost breach, or no outcome movement despite adoption.

### Answer 3

Domain authorities own definitions and source facts. A portfolio authority approves the cross-domain exchange obligation after domain consultation. Authorized privacy/legal roles interpret permitted purpose and jurisdiction. Technical authority selects a conforming design with architecture review. Portfolio and product authorities commit funding; delivery owners implement; service owners operate and recover; independent evidence owners produce tests and measures.

The applicable policy authority approves policy exceptions, while the accountable risk owner accepts only residual risks within delegated tolerance. Appeals go to the authority above the disputed decision, not automatically to architecture. Emergency operations may temporarily contain or disable flows under predefined bounds, notification, evidence preservation, expiry, and retrospective review. Record conflicts, recusals, conditions, and decision identifiers rather than compressing these roles into “accountable.”

### Answer 4

If an output is declared supported when it traces either to a decision/outcome or an evidence obligation, then `(15+3)/24 = 75%` declared support coverage. Four outputs are unsupported. Two more have links but are infeasible because they violate a hard constraint; therefore only 16 outputs might remain feasible if the violating outputs were within the supported group, but the exact overlap must be established before computing a feasible-support ratio.

The 75% does not establish semantic adequacy, benefit, evidence quality, resource feasibility, stakeholder authority, dependency closure, or legal/policy acceptability. Hard-constraint violations cannot be averaged away. Remove or redesign them, justify or stop unsupported outputs, inspect every typed trace, reconcile resources and risks, and obtain decisions from the correct authorities.

### Answer 5

Freeze new irreversible commitments and identify which decisions rely on the invalid assumption or expired exceptions. Reassess affected people, jurisdictions, policy interpretations, risks, suppliers, capacity, outcome baselines, architecture views, contracts, roadmap, operations, and recovery. Obtain authoritative interpretation for the new jurisdiction; expired exceptions require closure, containment, or new explicitly authorized time-bounded decisions rather than silent extension.

Reconcile the doubled scope against 30% lower funding by reducing scope, changing outcomes or timing, funding capacity, or closing the endeavor; do not retain all promises. Record change impact and propagate approved results through charter version, decisions, plans, interfaces, policies, controls, staffing, evidence, and communications. Renewal requires a legitimate expanded mandate, feasible funded work, resolved hard constraints, refreshed evidence and assumptions, authorized risks/exceptions, and credible measures. If those conditions cannot be met or the outcome hypothesis no longer holds, terminate or supersede the charter and transfer remaining obligations explicitly.
