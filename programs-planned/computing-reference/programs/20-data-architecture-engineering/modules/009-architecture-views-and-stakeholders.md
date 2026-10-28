---
module_id: DARCH-009
program: Data Architecture Engineering
level: 1
module_number: 9
title: Architecture Views and Stakeholders
status: complete
last_verified: 2026-09-03
---

# Architecture Views and Stakeholders

## One-Page Review

### Governing question

How can a data architect choose a small, sufficient set of views that lets specific stakeholders answer consequential questions, while preserving consistency, authority, uncertainty, and traceability across those views?

### Essential definitions

- A **stakeholder** is an individual, group, organization, or represented class with an interest in the entity and its outcomes; affected people can be stakeholders even when they neither fund nor operate it.
- A **concern** is an interest relevant to one or more stakeholders, such as meaning, ownership, privacy, availability, cost, change, or evidence.
- An **architecture viewpoint** defines conventions for constructing, interpreting, and using a family of views to frame particular concerns.
- An **architecture view** is a representation of architecture from a viewpoint for a declared entity, scope, purpose, stakeholders, concerns, and time.
- A **model kind** defines conventions for a model, including its element types, relationships, notation, constraints, and interpretation.
- A **correspondence** relates elements or claims across models or views; a **correspondence rule** states how those claims must agree.
- A **perspective** is a crosscutting analytic lens, such as privacy, resilience, or cost, applied across several views rather than confined to one diagram.
- A **view packet** combines a model with its purpose, audience, scope, legend, authoritative sources, assumptions, decisions, evidence, limitations, and maintenance metadata.

### Central model, mechanism, or theorem

Let stakeholders be `S`, concerns `C`, viewpoints `P`, views `V`, models `M`, and correspondence rules `R`. A usable description establishes traceable relations:

`S -> C -> P -> V -> M`

and validates `R` across the claims made by different models. View selection is sufficient for a decision `d` only when every material concern is addressed by an appropriate, current view or explicitly dispositioned by authorized rationale, every view has a real consumer and purpose, and cross-view contradictions are resolved or governed. More diagrams do not imply more coverage.

### Critical invariants

- Every view names its decision purpose, stakeholder audience, concerns, entity and boundary, lifecycle/configuration, viewpoint, owner, status, and evidence date.
- Stakeholders are represented by role and consequence, not only by organization chart or meeting attendance.
- Every material concern maps to one or more views or to an explicit authorized disposition; every view maps back to a real concern and use.
- Each model defines element and relation semantics, notation, units, cardinality, time, authority, and known omissions.
- Views share governed identity and vocabulary or declare mappings between different abstractions.
- Cross-view claims obey explicit correspondence rules for ownership, semantics, flow, state, deployment, controls, recovery, and lifecycle.
- A view distinguishes authoritative fact, architectural decision, prediction, assumption, proposal, and measured evidence.
- Access controls protect sensitive architecture information without hiding necessary consequences from legitimate stakeholders.
- Views evolve with decisions and evidence; stale views are marked, retired, or updated rather than silently trusted.

### Common failures

Common failures are drawing before identifying the decision; publishing one universal diagram; equating stakeholder with sponsor; omitting operators, maintainers, affected people, regulators, and external providers; calling a notation a viewpoint; listing concerns without mapping them to views; putting privacy or recovery in one isolated picture; using colors or arrows with no semantics; mixing conceptual and physical elements; duplicating identity across tools; allowing each view to be internally plausible while views contradict; hiding uncertainty; treating generated diagrams as authoritative; and keeping obsolete views discoverable without status.

### Compact example

A team proposes one “customer 360” diagram for executives, developers, privacy counsel, operations, and data stewards. It shows boxes and arrows but cannot answer who defines household, which purposes permit linkage, where consent applies, how corrections propagate, which stores serve operations, or how service is recovered. The architect replaces it with a small overview plus conceptual, lineage, authority, deployment, privacy, and recovery views. A correspondence matrix binds customer identity, purposes, flows, stores, owners, and recovery sets across them. Each audience now sees an appropriate abstraction without creating six unrelated architectures.

### Connections

[DARCH-003](003-current-state-data-landscape.md) supplies current-state evidence, [DARCH-007](007-architecture-drivers-and-constraints.md) supplies decision-driving concerns, and [DARCH-008](008-data-risk-and-criticality.md) identifies consequence and access needs. [DARCH-010](../ROADMAP.md) packages the results in a data architecture charter. Systems and software architecture provide broader viewpoint and architecture-description methods.

## Governing Question

An architecture description exists to support decisions and coordinated action. Which data is authoritative? What may be combined? Where does a definition apply? How does a correction travel? Who can approve a policy? What fails together? Can the business recover a decision path? A useful view makes a bounded class of such questions answerable for named people.

No single representation answers every concern. A conceptual model can clarify meaning while concealing runtime copies. A lineage graph can show movement while omitting decision authority. A deployment view can locate stores while saying little about legal purpose. An ownership matrix can name accountable roles while failing to show propagation. The task is therefore to select complementary views and preserve their correspondences, not to create one enormous drawing.

Stakeholder plurality makes the work harder. Producers, consumers, operators, security and privacy specialists, legal and records authorities, finance, vendors, regulators, auditors, and affected people have different questions, vocabularies, access rights, and power. Architecture must preserve these differences without fragmenting into inconsistent stories or pretending that consultation creates consensus.

## Why This Matters

Architecture that cannot be interpreted cannot guide implementation, governance, assurance, procurement, migration, or operations. A technically accurate diagram can still be useless if its intended reader cannot locate the decision, understand the notation, or distinguish current state from target state.

The opposite failure is documentation excess. Teams maintain hundreds of diagrams because a framework lists artifact types, even though nobody uses them. Stale copies then compete with code, catalogs, policies, and contracts. Documentation cost grows while confidence falls. View selection must be demand-driven and governed by value, risk, and change rate.

ISO/IEC/IEEE [42010:2022](https://www.iso.org/standard/74393.html) distinguishes an entity's architecture from an architecture description and specifies concepts for stakeholders, concerns, viewpoints, views, model kinds, and correspondences. It does not prescribe one architecting method, notation, tool, or document format. The SEI [Views and Beyond collection](https://www.sei.cmu.edu/library/views-and-beyond-collection/) similarly organizes documentation around relevant views plus information that applies across them. These sources support disciplined description; they do not determine which views a particular data decision requires.

Data architecture especially needs cross-view reasoning. The same business concept may appear as a term, logical entity, event schema, table, API field, object-store path, policy object, quality rule, lineage node, recovery set, and financial asset. Without stable identity and explicit mappings, a change can be “complete” in one view while remaining absent or contradictory elsewhere.

## Prerequisites and Retrieval

You should understand system boundaries, stakeholders, concerns, drivers, constraints, data products, domains, conceptual and logical models, interfaces, lineage, ownership, risk, quality, security, privacy, resilience, and architecture decisions.

Retrieve the difference between architecture and its description; stakeholder and role; concern and requirement; viewpoint, view, model, and model kind; abstraction and projection; current, transition, and target state; authoritative source and derived representation; correspondence and trace; evidence and assumption; audience, purpose, and access classification.

As a retrieval test, inspect a box-and-arrow diagram. Ask who uses it, for which decision, under which viewpoint conventions, what every box and arrow means, which boundary and date apply, where its facts originate, which concerns it addresses, what it intentionally omits, and how its claims correspond to other models. If those answers are absent, it is an illustration, not yet a governed architecture view.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish stakeholders, concerns, viewpoints, views, models, model kinds, and perspectives;
2. identify stakeholders by lifecycle role, authority, expertise, dependence, exposure, and affected outcome;
3. elicit decision-relevant concerns without flattening conflict or inventing consensus;
4. select a minimum sufficient view set from explicit use cases and risk;
5. design data-specific conceptual, flow, authority, deployment, quality, protection, operational, and evolution views;
6. specify a reusable viewpoint with conventions, model kinds, correspondence rules, and evaluation criteria;
7. produce self-describing view packets appropriate to audience and access level;
8. establish identity, vocabulary, trace, and cross-view consistency;
9. review view coverage, usability, currency, contradictions, and information hazards;
10. govern view ownership, generation, change impact, retirement, and evidence limitations.

## Core Exposition

**Begin with decisions and uses.** List the decisions the description must support: approve a target boundary, assign authority, compare placement, review privacy, design an interface, plan migration, investigate an incident, rehearse recovery, estimate cost, or onboard a team. For each use, name the actor, question, consequence of error, needed resolution, evidence threshold, deadline, and access constraints. A view without a use is a maintenance liability.

**Map stakeholders by relationship to consequences.** Include sponsors and decision authorities, but also producers, consumers, data owners, stewards, architects, engineers, operators, maintainers, incident responders, security and privacy specialists, legal and records authorities, finance and procurement, risk owners, suppliers, auditors, regulators, researchers, support staff, downstream partners, and people affected by data-driven decisions. Decompose broad labels such as “users” when subgroups face different benefits or harms.

Stakeholder identification is not attendance counting. One person may represent several roles; one role may require several perspectives. Representation may be delegated, but the record should state the basis, conflicts, missing voices, and limits. An executive can authorize funding without being competent to establish semantics, legal interpretation, safety, or lived impact.

**Elicit concerns as answerable questions.** “Security,” “governance,” and “performance” are topic labels. Convert them into questions: Who may read linked identity and behavior? Which policy and purpose authorize the join? How quickly must revocation propagate? What evidence detects unauthorized access? Which dependency can defeat both replicas? Questions reveal which model kinds and evidence are needed.

Record each concern with identifier, statement, originating and affected stakeholders, decision/use, priority or obligation, lifecycle phase, scenarios, evidence need, confidentiality, owner, status, and disposition. Preserve conflicting concerns. A producer's desire for schema autonomy and a consumer's need for comparability are both architecture inputs; neither becomes invalid because the other exists.

**Understand viewpoint versus view.** A viewpoint is reusable specification: concerns framed; stakeholder types; purposes; model kinds; element and relation vocabulary; construction and interpretation conventions; consistency and correspondence rules; analysis methods; examples; and limitations. A view applies those conventions to a specific entity and configuration. A lineage viewpoint might define dataset, transformation, transfer, policy, and evidence relationships; the quarterly-risk lineage view instantiates them for one governed scope.

**Do not confuse notation with meaning.** UML, ArchiMate, entity-relationship notation, SQL DDL, graph languages, tables, prose, and dashboards can express models. The notation alone does not determine which concerns are framed or what a relation means. A plain table with explicit semantics can be a stronger view than a beautiful diagram whose arrows ambiguously mean “calls,” “contains,” “owns,” or “depends on.”

**Select a minimum sufficient view set.** Start from the stakeholder-concern-use matrix. Group concerns that share compatible abstractions and interpretation needs. Separate views when one representation would mix incompatible semantics, reveal restricted facts unnecessarily, or become unreadable. Add a view only when it discharges an uncovered obligation or materially improves a high-consequence decision.

A practical data architecture description may choose among these families:

- **context and landscape views** show the entity boundary, external actors, ecosystems, major capabilities, products, and exchanges;
- **conceptual and semantic views** show business concepts, definitions, identity, relationships, rules, and semantic ownership;
- **logical information views** show normalized structures, keys, cardinalities, constraints, histories, and representation-independent schemas;
- **flow and lineage views** show sources, transformations, decisions, transfers, sinks, timing, provenance, and quality propagation;
- **authority and governance views** show decision rights, ownership, stewardship, policy sources, exception paths, and accountability;
- **interface and contract views** show APIs, events, files, schemas, compatibility, service levels, error behavior, and consumer obligations;
- **physical and deployment views** show stores, compute, networks, regions, copies, keys, trust zones, providers, and shared dependencies;
- **quality and observability views** show quality dimensions, rules, measurement points, thresholds, owners, evidence, alerts, and remediation;
- **security, privacy, safety, and records views** show threats or harms, purposes, classifications, controls, retention, deletion, legal holds, and residual risk;
- **operational and recovery views** show service paths, dependencies, failure modes, minimum service, recovery sets, sequence, reconciliation, and reopening authority;
- **transition and evolution views** show current, intermediate, and target states, coexistence, migration, compatibility, cutover, rollback, decommission, and decision triggers;
- **cost and portfolio views** show demand, capacity, allocation, unit economics, concentration, commitments, option value, and retirement exposure.

These are candidates, not a mandatory artifact list. One model can participate in several views when the semantics and access policy fit. One concern often requires several views: privacy may need semantic purpose, lineage, identity, access, deployment, retention, operations, and evidence. Treating a crosscutting quality as a single specialist diagram hides composition.

**Create a view packet.** Include stable identifier and title; decision purpose; stakeholders and concerns; entity, boundary, abstraction level, lifecycle state, configuration and effective date; viewpoint and model kinds; notation and legend; elements and relations; source and authority of claims; assumptions and uncertainties; decisions and rationale; correspondences; analyses and evidence; open issues; access classification; owner, reviewers, status, version, and next-review trigger.

Every visual should be accompanied by enough text to interpret it. Explain primary presentation, element catalog, relation catalog, context diagram, variability, rationale, known limitations, and navigation to related views. Provide machine-readable source when practical. An exported image should not be the only maintainable artifact.

**Govern identity and vocabulary.** Give architecture subjects stable identifiers independent of display names and tool-local keys. Maintain definitions, aliases, namespaces, versions, units, enumerations, classification markings, and equivalence mappings. Do not force entities at different abstraction levels into one identity: conceptual `Customer`, mastered party record, CRM row, API resource, and analytics dimension correspond but are not necessarily identical.

**Declare authority by claim.** A catalog may authoritatively register ownership, a schema repository may govern interface structure, policy may govern permitted purpose, infrastructure-as-code may govern deployed topology, and runtime telemetry may evidence actual behavior. No single tool is automatically the source of truth for every claim. Record authority, derivation, synchronization, and conflict resolution for each claim class.

**Define correspondences.** Useful rules include: every critical conceptual fact has an accountable semantic owner; every logical element maps to conceptual meaning or justified technical state; every cross-boundary flow has an interface contract and authority; every physical store realizes declared logical data; every sensitive flow maps to applicable purpose and controls; every recovery-critical consumer maps to a consistent recovery set; every target element maps to a migration action; and every deployed dependency appears in operational and risk views.

Correspondence does not require identical shape. A many-to-many mapping can be correct when abstractions differ. Record relation type, direction, cardinality, transformation, conditions, version, confidence, evidence, owner, and validation rule. “Related to” is too weak for assurance.

**Check contradictions semantically.** Two views may use different aggregation without conflict. Contradiction arises when applicable claims cannot both hold: two roles have final authority for the same decision; a logical schema requires a field that an interface forbids; a privacy view says a flow is prohibited while lineage says it operates; a recovery view requires a store omitted from the recovery set; or a target view removes a source that a transition view still needs after cutover.

Classify findings as vocabulary mismatch, identity mismatch, applicability difference, abstraction difference, stale version, missing correspondence, genuine contradiction, or unverified assumption. Resolve from authoritative sources and accountable decisions. Do not edit whichever picture is easiest merely to make lines match.

**Use perspectives across views.** Apply privacy, security, resilience, accessibility, cost, performance, operability, sustainability, and changeability questions across the selected set. NIST [SP 800-160 Vol. 1 Rev. 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) places trustworthy security engineering in the system lifecycle; it supports integrating protection concerns into architecture rather than treating security as a late overlay. Its scope does not establish a complete data architecture method or local compliance.

**Tailor depth to risk and reversibility.** A low-consequence reversible experiment may need an overview, decision record, interface contract, and rollback view. A regulated, safety-relevant, identity-linking platform may require detailed semantic, purpose, lineage, trust, deployment, human, recovery, and evidence views plus independent challenge. Tailoring should state what is omitted and why.

**Design for audience without distorting truth.** Executives may need consequences, options, dependencies, and decisions; engineers need precise interfaces and allocations; operators need states, failure and recovery; specialists need control and evidence paths; affected communities need understandable uses and recourse. Generate audience-specific projections from governed claims where possible. Simplification may omit detail but must not reverse meaning or hide material risk.

**Protect architecture information proportionately.** Detailed data locations, trust boundaries, vulnerabilities, keys, personal-data flows, supplier weaknesses, and incident paths can be sensitive. Classify at element or view level, minimize disclosure, redact safely, and preserve controlled trace. Restricted access does not justify excluding accountable reviewers or affected consequences; create safe projections and governed review channels.

**Validate usability.** Ask representative stakeholders to perform real tasks: find the owner, trace a correction, identify purpose, determine blast radius, plan a schema change, locate a recovery dependency, or explain a decision. Measure task success, time, interpretation errors, unresolved questions, and stale navigation. A view can be semantically correct yet unusable.

The SEI [Views and Beyond](https://www.sei.cmu.edu/library/documenting-software-architectures-views-and-beyond-second-edition/) material emphasizes relevant views and cross-view information so stakeholders can build, analyze, maintain, and learn from a system. Its [structured review approach](https://insights.sei.cmu.edu/library/a-structured-approach-for-reviewing-architecture-documentation/) centers review on documentation stakeholders. Apply those ideas to the data lifecycle while retaining domain-specific semantics, authority, regulation, and empirical evidence.

**Keep views current.** Define source ownership, generation rules, review cadence, decision triggers, dependency-based impact analysis, replacement and retirement. Triggers include schema or policy changes, new consumers, changed purpose, deployment movement, incidents, recovery exercises, regulation, acquisition, supplier exit, lifecycle transition, and invalidated assumptions.

Generated views reduce drift only when generation inputs are authoritative and complete for the claim. Code can reveal deployed tables or network edges but may omit business meaning, approved purpose, manual processes, shadow exports, contractual duties, or actual consumer decisions. Label observed, declared, inferred, and proposed facts separately.

## Definitions and Notation

Let `S`, `C`, `P`, `V`, and `M` denote stakeholders, concerns, viewpoints, views, and architecture models. Define relations:

- `interest(s,c)`: stakeholder `s` has concern `c`;
- `frames(p,c)`: viewpoint `p` provides conventions for concern `c`;
- `conforms(v,p)`: view `v` follows viewpoint `p`;
- `contains(v,m)`: view `v` uses model `m`;
- `addresses(v,c)`: view `v` supplies appropriate information for concern `c`;
- `serves(v,s,d)`: view `v` supports stakeholder `s` in decision or use `d`;
- `corresponds(x,y,k)`: claims or elements `x` and `y` are related by typed rule `k`.

For decision `d`, let `C_d` be its material concerns. Bounded concern coverage is:

`Coverage(d) = addressed_or_authorized(C_d) / |C_d|`

The ratio is a navigation aid, not an adequacy proof. A single uncovered legal, safety, rights, or recovery concern may block a decision while many cosmetic concerns do not. Each discharge still requires semantic review, evidence, and authority.

Let `R` be cross-view correspondence rules. Internal agreement for baseline `b` is `all(r(b) holds for r in R_applicable)`. That claim is limited to encoded rules, loaded versions, declared mappings, and modeled conditions. It cannot establish that stakeholder discovery, concerns, sources, abstractions, or real-world behavior are complete.

## Mechanisms, Invariants, or Proof Structure

Use nine gates to construct and assure a stakeholder-centered view set.

**1. Decision gate.** Define entity, boundary, lifecycle/configuration, decisions, consequences, evidence threshold, deadline, and access conditions.

**2. Stakeholder gate.** Map authority, expertise, dependence, operation, maintenance, exposure, affected outcomes, representation, conflicts, and missing voices.

**3. Concern gate.** Convert topics into answerable questions with origin, scope, priority or obligation, scenario, owner, evidence need, and disposition.

**4. Viewpoint gate.** Select or define conventions, model kinds, semantics, correspondence rules, analyses, and limitations appropriate to concerns.

**5. Selection gate.** Choose the minimum sufficient view set, documenting coverage, overlap, deliberate omissions, sensitivity, and access segmentation.

**6. Construction gate.** Build self-describing view packets with governed identity, vocabulary, sources, authority, assumptions, rationale, evidence, and status.

**7. Correspondence gate.** Trace meaning, ownership, flow, contract, deployment, control, recovery, transition, and evidence across abstractions and versions.

**8. Challenge gate.** Test representative stakeholder tasks, negative space, adversarial scenarios, contradictions, stale evidence, confidentiality, and usability.

**9. Lifecycle gate.** Approve bounded use, assign maintenance, monitor triggers, propagate changes, supersede or retire views, and preserve decisions.

The executable example checks a compact concern-to-view register. It flags a stale deployment view, an unused monitoring view, and stakeholder roles whose concerns are nominally addressed but not represented in the addressing views.

<!-- bijux-verify: {"id":"view-register-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"concerns=4\nviews=5\nfindings=c_privacy:missing-stakeholder:affected_person,c_recovery:missing-stakeholder:risk_owner,deployment:stale-evidence,monitoring:orphan-view\nready=false\n","stderr":""}} -->
```python
concerns = {
    "c_semantics": {"stakeholders": {"consumer", "data_steward"}},
    "c_recovery": {"stakeholders": {"operations", "risk_owner"}},
    "c_privacy": {"stakeholders": {"privacy", "affected_person"}},
    "c_cost": {"stakeholders": {"finance", "platform"}},
}

views = {
    "conceptual": {"concerns": {"c_semantics"}, "stakeholders": {"consumer", "data_steward"}, "current": True},
    "lineage": {"concerns": {"c_semantics", "c_privacy"}, "stakeholders": {"consumer", "privacy"}, "current": True},
    "recovery": {"concerns": {"c_recovery"}, "stakeholders": {"operations"}, "current": True},
    "deployment": {"concerns": {"c_cost"}, "stakeholders": {"finance", "platform"}, "current": False},
    "monitoring": {"concerns": set(), "stakeholders": {"operations"}, "current": True},
}

findings = []
for view_id, view in views.items():
    if not view["concerns"]:
        findings.append(f"{view_id}:orphan-view")
    if not view["current"]:
        findings.append(f"{view_id}:stale-evidence")

for concern_id, concern in concerns.items():
    addressing = [view for view in views.values() if concern_id in view["concerns"]]
    represented = set().union(*(view["stakeholders"] for view in addressing)) if addressing else set()
    for stakeholder in concern["stakeholders"] - represented:
        findings.append(f"{concern_id}:missing-stakeholder:{stakeholder}")

print(f"concerns={len(concerns)}")
print(f"views={len(views)}")
print(f"findings={','.join(sorted(findings))}")
print(f"ready={str(not findings).lower()}")
```

The checker evaluates only declared register coverage, currency, and role representation. It does not prove that stakeholders are legitimate representatives, concerns are complete, views are semantically adequate, evidence is true, correspondences hold, access is lawful, or an architecture is fit for production. Those claims require accountable participation, source review, semantic inspection, and empirical validation.

## Alternatives and Trade-Offs

**One overview versus many specialized views.** An overview improves orientation but loses analytic precision. Specialized views support consequential tasks but raise navigation and consistency cost. Use a small overview as a map into governed detail.

**Standard viewpoints versus tailored viewpoints.** Standards improve shared interpretation and reuse. Tailoring fits domain questions and local evidence. Adapt explicitly and retain provenance rather than copying a framework artifact list blindly.

**Central model versus federated sources.** A central repository improves identity and automated correspondences but can erase specialist semantics or become a bottleneck. Federation preserves domain authority but needs contracts, mappings, and configuration control.

**Handcrafted versus generated views.** Handcrafted views communicate intent and rationale well but drift. Generated views reflect source data repeatably but inherit source omissions. Combine governed machine-derived facts with reviewed narrative and decisions.

**Stable snapshots versus live views.** Snapshots support audit and approved baselines. Live views support operations and change. Bind live evidence to time and configuration, and preserve signed snapshots for decisions.

**Broad access versus restriction.** Broad access improves discovery and challenge. Restriction protects sensitive topology, personal data, vulnerabilities, and negotiations. Use least disclosure, safe projections, and controlled trace rather than total secrecy.

**Current and target combined versus separated.** Overlay can expose migration directly but becomes ambiguous. Separation improves clarity but may hide coexistence. Maintain explicit current, transition, and target semantics plus mappings.

## Failure Modes and Misconceptions

1. **The stakeholder is the sponsor.** Sponsors are one class; operators, consumers, affected people, authorities, and dependencies also matter.
2. **A notation is a viewpoint.** Symbols do not define concerns, interpretation, analysis, or correspondence.
3. **One picture is the architecture.** Architecture exceeds any projection, and different concerns require different abstractions.
4. **More views mean completeness.** Coverage depends on concerns, semantics, evidence, and use, not artifact count.
5. **Every framework artifact is mandatory.** Tailor from decision need and consequence, documenting omissions.
6. **Privacy belongs in the privacy view.** Crosscutting qualities must compose through semantics, flows, interfaces, deployment, operation, and lifecycle.
7. **Same name means same entity.** Identity and abstraction must be governed explicitly.
8. **Different shapes contradict.** Projections can aggregate differently; apply typed correspondence rules.
9. **The catalog is authoritative for everything.** Authority is claim-specific and may be distributed.
10. **Generated means current and correct.** Generation proves repeatability from inputs, not source completeness or meaning.
11. **Approval means shared understanding.** Test interpretation and stakeholder tasks; preserve dissent and limitations.
12. **Published views remain usable.** Status, version, effective date, triggers, supersession, and retirement are required.

## Worked Examples

### Example 1

An executive overview says customer data is centralized. A conceptual view distinguishes person, household, account, and prospect; lineage shows five mastered and seven copied representations; an authority view shows two domains own different facts. The overview is corrected to say shared identity services coordinate several authoritative domains. Simplification no longer reverses the architecture.

### Example 2

A privacy team requests “the data-flow diagram.” The decision concerns purpose limitation, cross-border transfer, retention, correction, and processor access. One lineage view cannot answer all five. The architect combines semantic-purpose, lineage, deployment, access-control, and lifecycle views with typed correspondences and a safe external projection.

### Example 3

Two diagrams contain `Order`. One denotes a commercial agreement; the other an immutable submission event. A naive merge creates cardinality contradictions. Stable identifiers and an explicit `evidences` relation preserve distinct concepts while showing how events contribute to agreement state.

### Example 4

An operations view marks two stores as redundant. A deployment view shows both depend on one identity service and region. A recovery view restores data but not the shared policy version. Cross-view review removes the unsupported independence claim and creates common-cause and reconciliation actions.

### Example 5

A board asks for a single scorecard. It hides that finance accepts a two-day reporting delay while patient operations cannot accept a ten-minute identity outage. The architect provides a one-page decision view with noncompensable constraints and links to stakeholder-specific impact and recovery views. Concision is retained without averaging away consequence.

### Example 6

Infrastructure discovery generates a current deployment view nightly. It sees managed databases and buckets but misses spreadsheets emailed to a supplier. A stakeholder walkthrough and egress evidence reveal the flow. The generated view remains valuable but is labeled observed infrastructure, not complete data movement.

### Example 7

A logical model shows deletion after 30 days; a records view requires preservation for an active hold; a pipeline view hard-deletes staging after seven days. Applicability analysis finds the hold should override both schedules. The team adds policy precedence, hold propagation, evidence, and a correspondence test.

### Example 8

Developers ignore a 200-node diagram. In task testing, they cannot find schema ownership or compatibility rules. A navigable landscape, domain-level interface views, and a searchable element catalog reduce median task time in a local usability test. The result supports those tested tasks only, not universal usability.

### Example 9

A supplier receives the internal security view to plan integration, exposing unrelated sensitive topology. The team defines an external interface viewpoint containing contract, trust boundary, allowed flows, evidence duties, and escalation without unrelated internals. Access reduction preserves the supplier's legitimate concerns.

### Example 10

A migration decision uses current, transition, and target views. The target removes a source system, but correspondence analysis shows the transition still reads it for late corrections after the planned shutdown. The schedule adds a correction handoff, archive interface, rollback bound, and retirement evidence before approval.

## Cross-Program Connections

- **Systems engineering:** stakeholder needs, operational concepts, logical and physical architecture, interfaces, and lifecycle assurance require coordinated viewpoints.
- **Software architecture:** module, component-and-connector, allocation, behavior, and interface views provide reusable documentation patterns.
- **Data engineering:** schemas, lineage, orchestration, quality, event time, and deployment evidence populate and challenge declared views.
- **API and service engineering:** contract, dependency, sequence, state, compatibility, and SLO views expose service interactions and consumer obligations.
- **Platform engineering:** tenant, cell, control-plane, data-plane, policy, fleet, deployment, and recovery views reveal shared dependencies and authority.
- **Security and privacy:** threats, trust boundaries, purposes, identities, controls, retention, evidence, and affected parties cut across every relevant view.
- **Product and organizational design:** decision rights, incentives, funding, team boundaries, and customer outcomes shape which views are actionable.
- **Verification and operations:** tests, telemetry, incidents, exercises, configurations, and change records determine whether view claims remain supported.

## References

1. ISO/IEC/IEEE, *42010:2022 Software, systems and enterprise—Architecture description*, 2022. <https://www.iso.org/standard/74393.html>
2. Software Engineering Institute, *Views and Beyond Collection*, 2009–2018. <https://www.sei.cmu.edu/library/views-and-beyond-collection/>
3. Clements, P. et al., *Documenting Software Architectures: Views and Beyond, Second Edition*, 2010. <https://www.sei.cmu.edu/library/documenting-software-architectures-views-and-beyond-second-edition/>
4. Nord, R., Clements, P., Emery, D., and Hilliard, R., *A Structured Approach for Reviewing Architecture Documentation*, CMU/SEI-2009-TN-030, 2009. <https://insights.sei.cmu.edu/library/a-structured-approach-for-reviewing-architecture-documentation/>
5. Clements, P., *Comparing the SEI's Views and Beyond Approach for Documenting Software Architectures with ANSI-IEEE 1471-2000*, CMU/SEI-2005-TN-017, 2005. <https://www.sei.cmu.edu/library/comparing-the-seis-views-and-beyond-approach-for-documenting-software-architectures-with-ansi-ieee-1471-2000/>
6. National Institute of Standards and Technology, *SP 800-160 Vol. 1 Rev. 1: Engineering Trustworthy Secure Systems*, 2022. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>
7. The Open Group, *TOGAF Standard, 10th Edition: Architecture Content*, 2022. <https://pubs.opengroup.org/togaf-standard/architecture-content/>
8. arc42, *Quality Model and Architecture Documentation Template*, current web edition. <https://docs.arc42.org/>

## Exercises

### Exercise 1

Build a stakeholder-concern-use matrix for a regional patient-identity platform. Include authority, expertise, operators, producers, consumers, affected people, privacy/security, clinical safety, records, regulators, suppliers, and missing representation. Propose a minimum sufficient view set.

### Exercise 2

Define a lineage viewpoint: framed concerns, stakeholder types, model kinds, elements, relations, notation, required metadata, correspondence rules, analyses, evidence, access constraints, and limitations. Then distinguish the viewpoint from one concrete view.

### Exercise 3

Review three claims: the conceptual model gives `Customer` one identifier; an event contract permits two identifiers during migration; the warehouse dimension creates a surrogate key. Decide whether they contradict and specify the correspondences needed.

### Exercise 4

A decision has 20 material concerns: 15 adequately addressed, 2 authorized and time-bounded dispositions, 2 nominally mapped to stale views, and 1 unaddressed legal concern. Compute declared and adequate coverage under stated rules, then decide what the ratios cannot establish.

### Exercise 5

Design a view review and maintenance process for a multi-region data platform. Include stakeholder task tests, semantic and correspondence checks, access segmentation, current/transition/target control, source authority, generated views, change triggers, supersession, and bounded approval.

## Answers to the Exercises

### Answer 1

Map funding and portfolio authority; clinical, registration, laboratory, billing, analytics, and public-health consumers; source-system and interface producers; identity stewards; platform and on-call operations; security, privacy, records, legal, safety, accessibility, finance, procurement, suppliers, auditors, regulators, and patients or legitimate representatives. Record decision authority separately from semantic, legal, clinical, and lived expertise; expose conflicts and unrepresented populations.

A minimum set might include a public-safe context view; identity and matching conceptual view; authority/policy view; source-to-decision lineage view; interface/compatibility view; trust and deployment view; privacy-purpose/retention view; quality and observability view; failure/recovery view; and current-transition-target migration view. Each must name the decisions it supports. Combine or omit only when concern coverage, access, readability, and correspondence remain adequate.

### Answer 2

The viewpoint frames provenance, propagation, permitted movement, impact, correction, quality, and audit concerns for consumers, stewards, engineers, privacy/security specialists, operators, auditors, and risk owners. Model kinds include directed transformation/transfer graphs, element catalogs, timing overlays, purpose/control overlays, and evidence tables. Elements include data product, representation, event, transformation, transfer, decision, actor, policy, control, and evidence; relations distinguish reads, writes, derives, transfers, decides, authorizes, and evidences.

Require stable identity, semantics, owner, purpose, location, time/version, confidence, classification, source evidence, and access marking. Correspond lineage to conceptual meaning, contracts, deployment, controls, quality, retention, and recovery. Analyze reachability, impact, cycles, prohibited paths, stale edges, and missing sources/sinks. State that discovery cannot prove semantic correctness or complete shadow flows. The viewpoint is this reusable specification; a concrete view applies it to, for example, the 2026-09 billing-correction decision path and named configuration.

### Answer 3

The claims need not contradict because they occupy different abstractions and lifecycle conditions. The conceptual identifier may express stable business identity; the event may carry old and new natural identifiers during coexistence; the warehouse surrogate may provide local row identity. They contradict only if “one identifier” was intended as a physical prohibition across all representations or if mappings cannot preserve required identity.

Define typed correspondences from both event identifiers to the conceptual identity with applicability and conflict rules, from the accepted event identity to the warehouse dimension, and from the surrogate key back to the governed business identity and history. Record migration interval, authoritative resolution, ambiguity handling, cardinality, version, evidence, and retirement trigger.

### Answer 4

If declared coverage counts adequate, authorized dispositions, and stale nominal mappings, then `(15+2+2)/20 = 95%`. If adequate coverage counts only semantically adequate current views, it is `15/20 = 75%`; dispositions should be reported separately rather than silently called adequate. Another transparent dashboard reports 75% adequate, 10% disposed temporarily, 10% stale, and 5% absent.

No ratio establishes concern consequence, correctness, representative participation, evidence quality, cross-view consistency, usability, or readiness. The unaddressed legal concern can block the decision regardless of percentage. The authority must resolve it, refresh stale views, evaluate dispositions and expiry, and state a bounded conclusion.

### Answer 5

Bind each review to entity, purpose, baseline, region/tenant classes, lifecycle states, stakeholders, concerns, viewpoints, evidence date, and access rules. Have representative users perform tasks such as locating owner, tracing change, testing purpose, finding blast radius, planning recovery, and challenging a decision. Review legends, identity, vocabulary, source authority, assumptions, claim labels, model semantics, negative space, and correspondence across conceptual, lineage, contract, deployment, policy, quality, recovery, and transition views.

Generate observed topology and schemas from governed sources, but label coverage and combine them with reviewed meaning, authority, manual work, and decisions. Separate current, transition, and target applicability. Trigger impact analysis for schema/policy/deployment/purpose/consumer changes, incidents, exercises, suppliers, regulation, lifecycle milestones, and invalidated assumptions. Update dependents or record a bounded exception; mark superseded views prominently and retain decision baselines. Approval states only which stakeholder tasks and decisions the controlled view set adequately supports, not that the architecture or documentation is universally complete.
