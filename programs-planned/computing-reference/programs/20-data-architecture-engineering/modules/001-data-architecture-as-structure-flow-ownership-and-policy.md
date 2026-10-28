---
module_id: DARCH-001
program: Data Architecture Engineering
level: 1
module_number: 1
title: Data Architecture as Structure, Flow, Ownership, and Policy
status: complete
last_verified: 2026-08-29
---

# Data Architecture as Structure, Flow, Ownership, and Policy

## One-Page Review

### Governing question

How can an organization make coherent, reviewable decisions about what its data means, where it moves, who may decide about it, and which constraints must hold across systems and time?

### Essential definitions

- **Data architecture** is the set of fundamental data-related structures, relationships, decision rules, responsibilities, and evolution choices for an enterprise or other bounded system of interest.
- A **structure view** describes concepts, domains, data products, logical relationships, representations, and stores.
- A **flow view** describes creation, acquisition, transformation, replication, access, feedback, preservation, and disposition paths.
- **Ownership** assigns decision rights and accountability for meaning, authoritative change, service, quality, access, and lifecycle outcomes.
- A **policy** is an authorized rule that constrains decisions or behavior; a control implements or monitors a policy at a named enforcement point.
- An **architecture view** addresses particular stakeholder concerns under a declared viewpoint; no single diagram answers every concern.
- A **transition architecture** is a coherent intermediate state connecting current and target states while preserving required operations and controls.

### Central model, mechanism, or theorem

Model a data architecture as four coupled projections over one bounded system:

`A = (S, F, O, P | context, decisions, evidence)`

where `S` is structure, `F` is flow, `O` is ownership, and `P` is policy. A proposed change is architecturally coherent only when every material data object and flow has an accountable decision boundary, applicable policy, implementation path, and evidence; the views agree on identity and scope; and a feasible transition preserves required outcomes.

### Critical invariants

- Every material data concept and product has an unambiguous semantic authority.
- Every cross-boundary flow names source, destination, purpose, contract, owner, and failure/correction path.
- Copies and derived products do not silently become competing systems of record.
- Policy follows data across representations and organizational boundaries where its authority applies.
- Architecture decisions trace to stakeholder concerns, quality attributes, constraints, and evidence.
- Current, target, and transition views use consistent identities and explicitly record unknowns.

### Common failures

Typical failures are equating architecture with a vendor diagram, modeling stores without meaning, mapping flows without purpose, assigning “the data team” as owner, publishing policy without enforcement, centralizing all semantics into one canonical model, declaring a target with no migration path, ignoring feedback and deletion flows, and measuring artifact production instead of architecture outcomes.

### Compact example

An `Order` exists in commerce, payment, fulfillment, and analytics. A storage diagram shows four databases but not which system may accept order intent, which owns settlement, how shipment projections lag, who approves semantic change, or where retention is enforced. Adding structure, flow, ownership, and policy views turns locations into an architecture argument.

### Connections

[DARCH-002](../ROADMAP.md) aligns architecture with business outcomes; [DARCH-003](../ROADMAP.md) maps the current landscape. Pipeline implementation belongs to [Data Engineering](../../19-data-engineering/ROADMAP.md), engine guarantees to [Database Engineering](../../18-database-engineering/ROADMAP.md), general architectural decision practice to [Software Engineering: Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md), and distributed execution to [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md).

## Governing Question

Organizations rarely suffer from a total absence of data systems. They suffer from systems whose meanings, dependencies, authorities, and constraints disagree. A customer identifier means one thing in sales and another in support. A reporting platform copies operational tables without accepting lifecycle obligations. A policy names sensitive data but no flow applies the classification. A modernization program selects a target platform before identifying which facts, decisions, and risks it must preserve.

Data architecture addresses this coordination problem. It is not the drawing of boxes and arrows, the purchase of a platform, or the construction of a universal model. It is the durable decision system that connects business meaning, information movement, organizational accountability, technical mechanisms, and policy outcomes across a defined scope.

[ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) distinguishes an architecture from an architecture description. The standard concerns how descriptions, viewpoints, model kinds, stakeholders, and concerns are expressed; a document conforming to a description standard does not guarantee that the underlying architecture is good. This distinction is foundational: artifacts are evidence and communication mechanisms, not the architecture itself.

## Why This Matters

Data decisions are unusually persistent. Application code can be replaced while identifiers, historical records, contracts, regulatory classifications, reports, and learned models continue to carry old assumptions. A local shortcut can become an enterprise dependency simply because copied data is easy to consume. Architecture makes those consequences visible before they become irreversible.

The cost of incoherence appears as reconciliation work, duplicate masters, broken reports, slow policy response, inaccessible evidence, brittle integrations, and migrations that never finish. These are not merely tooling defects. They often arise because meaning, movement, authority, and constraint were designed separately.

A coherent architecture creates options. It lets teams replace physical stores while preserving logical contracts, decentralize execution while retaining shared policy, introduce new consumers without surrendering source authority, and migrate incrementally with explicit compatibility and rollback. Architecture is valuable when it improves decisions and outcomes, not when it maximizes diagram count.

## Prerequisites and Retrieval

You should understand databases, files, APIs, events, data pipelines, basic security and privacy concepts, organizational roles, and software architecture. Recall the distinction between an abstract dataset and one physical representation, between accountability and task execution, and between a policy outcome and the mechanism selected to implement it. Familiarity with stakeholder, concern, invariant, dependency, and trade-off reasoning is assumed.

## Learning Objectives

After completing this module, you should be able to:

- define the bounded system of interest for a data-architecture decision;
- distinguish architecture, architecture description, platform design, and implementation;
- analyze data architecture through structure, flow, ownership, and policy views;
- connect views through stable identities and cross-view invariants;
- identify semantic authority separately from physical custody and platform operation;
- map a data flow with purpose, contract, control, and failure behavior;
- distinguish policy, standard, control, enforcement point, and evidence;
- explain current, target, and transition architectures;
- evaluate options against stakeholder concerns and quality attributes;
- design review evidence for high-consequence cross-organizational data change.

## Core Exposition

Begin by naming the **system of interest**: the enterprise, business capability, product ecosystem, public program, merger boundary, or other scope whose architecture is being considered. Its environment includes customers, partners, regulators, suppliers, external platforms, and adjacent systems. Without a scope, an “enterprise data model” can expand indefinitely and every exception becomes an argument about jurisdiction.

Stakeholders have concerns, not generic interest. Executives may care about strategic outcomes and risk. Domain owners care about meaning and authority. Product teams care about change autonomy and service expectations. Analysts care about discoverability and comparability. Security, privacy, legal, records, and audit functions care about authorized outcomes and evidence. Operators care about failure, recovery, cost, and observability. Architecture views should be selected to answer these concerns.

The **structure view** begins with concepts and relationships: customer, account, order, shipment, consent, device, reading, claim, or experiment. It separates conceptual meaning from logical schema and physical representation. It identifies domains, aggregate boundaries, business keys, temporal semantics, shared vocabularies, reference data, master data, datasets, data products, and their representations.

Structure is not a single hierarchy. A customer may have a legal-party identity, a marketing profile, a billing account, and a service user. Forcing these into one record can erase valid distinctions. Architecture should state where concepts deliberately align, translate, or remain different. Later modules develop conceptual, logical, canonical, temporal, and conflicting models.

W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) usefully distinguishes a conceptual dataset from a distribution—an accessible representation such as a file—and from a data service providing access or processing operations. This prevents a common error: treating a storage format or endpoint as the dataset's identity. DCAT supports interoperable catalog metadata; it does not assign enterprise ownership or verify semantic correctness.

The **flow view** traces data through time. Flows include collection, command handling, event publication, extraction, replication, transformation, aggregation, feature generation, serving, export, feedback, archive, correction, and deletion. An arrow must mean more than “data moves.” It should name producer and consumer, data identity, direction, trigger, timing, interface, purpose, transformation, delivery/failure semantics, controls, and owner.

Physical movement is not required. A federated query, secure view, or in-place computation creates access and dependency flows without copying the full dataset. Conversely, a storage replication mechanism can create a physical copy that is not a new semantic product. Architecture distinguishes information value flow, control flow, and physical transfer.

The [NIST Big Data Reference Architecture](https://doi.org/10.6028/NIST.SP.1500-6r2) identifies Data Provider, Data Consumer, Application Provider, Framework Provider, and System Orchestrator roles, surrounded by management and security/privacy fabrics. Its data arrows can represent transfer by value or access by reference. The model is vendor-neutral and informative; an organization must specialize roles, authority, contracts, and evidence for its context.

Flow analysis exposes blast radius and cycles. A supposedly downstream risk score may feed pricing decisions that alter future training data. A spreadsheet export may become a partner's source. A reverse-ETL job may write analytical segments into operational systems. Feedback edges require explicit causality, delay, monitoring, and authority; hiding them behind a generic “analytics” box makes risk invisible.

The **ownership view** assigns decision rights. Ownership is not possession, server administration, or personal authorship. A semantic owner decides what a fact means and which source is authoritative. A product owner accepts service and lifecycle accountability. A steward may coordinate definitions and quality. A custodian or platform team operates storage and controls. A policy authority establishes constraints. These roles can coincide, but the decisions must remain distinguishable.

Ownership must be granular enough to decide conflicts. “Finance owns customer data” is ambiguous if commerce accepts customer identity, finance owns billing accounts, privacy approves purposes, and a platform team operates the warehouse. State who may create or correct each fact, approve semantic changes, accept quality risk, grant access, authorize exceptions, fund service, and retire the product.

Parnas's [information-hiding criterion](https://doi.org/10.1145/361598.361623) argues that decomposition should hide changeable design decisions rather than merely follow processing steps. Applied to data, a domain boundary should encapsulate authoritative rules and expose stable contracts, not let consumers join private tables. Conway's 1968 [*How Do Committees Invent?*](https://www.bitsavers.org/magazines/Datamation/196804.pdf) explains why communication structures shape system designs. Ownership that contradicts organizational authority will be expensive to sustain.

The **policy view** maps authorized rules to scope, decision, enforcement, exception, and evidence. Policies may concern classification, permitted use, access, segregation, quality, interoperability, residency, retention, preservation, deletion, ethics, or risk. A policy statement such as “protect confidential data” is not implementable until classification, actors, actions, contexts, resources, decisions, and enforcement responsibilities are defined.

Distinguish five layers. A **principle** guides recurring choices, such as “authoritative facts have one accountable write boundary.” A **policy** expresses an authorized required outcome. A **standard** narrows acceptable implementation or representation. A **control** prevents, detects, or corrects deviation. An **evidence record** supports whether the control operated and the outcome held. A green control result does not prove the policy was complete or ethically sufficient.

Policy must travel across structure and flow. Classification attached only to a source table is lost when fields are exported, aggregated, embedded, or used to train a model. The architecture needs propagation and re-evaluation rules: a derived product may inherit the strongest applicable restriction, reduce sensitivity through an approved transformation, or gain new risk through combination. Those are domain and policy decisions, not automatic label arithmetic.

The four views constrain one another. Structure without flow produces a static glossary. Flow without structure moves ambiguously defined bytes. Ownership without policy grants authority without boundaries. Policy without ownership and enforcement becomes ceremonial. A coherent architecture uses stable identifiers to connect concepts, products, flows, owners, policies, decisions, and evidence.

Architecture descriptions should make inconsistency testable. If the structure view lists a `CustomerProfile` product, the flow view should locate its production and consumers, the ownership view should name decision authorities, and the policy view should state applicable controls. Unknown information should be recorded as an explicit gap with owner and resolution path rather than invented to complete a diagram.

Architecture decisions respond to drivers and constraints. Drivers include new capabilities, merger integration, unreliable reporting, artificial-intelligence use, policy obligations, cost, resilience, and time to market. Constraints include legacy contracts, skills, budgets, sovereignty, latency, vendor commitments, and transition windows. Quality attributes—interoperability, modifiability, traceability, confidentiality, availability, consistency, recoverability, and cost efficiency—make trade-offs evaluable.

The current state is what evidence shows, including unofficial copies and exceptions. The target state expresses desired structures, flows, responsibilities, policies, and measurable outcomes. The **transition architecture** defines intermediate states, dual-running rules, data synchronization, compatibility, reconciliation, cutover, rollback, and decommission. A target with no feasible transition is aspiration, not an executable architecture.

Architecture is governed through decisions, not static approval. Record context, decision, alternatives, consequences, owner, review triggers, and evidence. Use standards and reference patterns for recurring problems while permitting explicit exceptions with authority, expiry, compensating controls, and removal plans. Reassess when business meaning, law, threat, scale, technology, or organizational authority changes.

Fitness functions can test selected properties: every production data product has an owner; every cross-domain flow has a contract; sensitive outputs have an access policy; no deprecated interface has active undeclared consumers; every target component has a transition predecessor. Automated checks improve consistency, but they cannot decide whether a domain boundary, purpose, or policy is substantively right.

## Definitions and Notation

Let the system of interest be `X` in environment `E`, with stakeholder set `H` and concern set `C`. Define the architecture projection `A_X = (S, F, O, P)`, where:

- `S = (N_S, R_S)` is a graph of semantic/physical data nodes and structural relationships;
- `F` is a set of directed flow records `(source, target, data, purpose, contract, timing)`;
- `O : Decisions -> AccountableRoles` assigns each material decision to an accountable role;
- `P : Context -> RequiredOutcomes` maps applicable context to policies and enforcement obligations.

For each flow `f`, define `owner(f)`, `purpose(f)`, `contract(f)`, and `controls(f)`. A minimal consistency predicate is:

`Coherent(f) = Known(source) and Known(target) and owner(f) != empty and purpose(f) != empty and contract(f) != empty and ApplicablePolicy(f) is addressed`.

This predicate is necessary, not sufficient. A populated field can still be wrong. Human and empirical review must test semantics, authority, feasibility, and outcomes.

A **viewpoint** specifies the conventions for constructing and interpreting a view for named concerns. A **view** is the resulting representation for this architecture. A **model** is a purposeful abstraction. A **reference architecture** supplies reusable concepts and relations; a **target architecture** commits a bounded organization to intended decisions. A **roadmap** orders outcome-bearing transitions; it is not a list of product purchases.

## Mechanisms, Invariants, or Proof Structure

An architecture argument should connect claim, context, design, transition, and evidence. First state the outcome and stakeholders. Then show how the four views jointly realize it. Identify assumptions and failure modes. Compare alternatives against named quality attributes. Finally, define implementation responsibilities, transition checkpoints, evidence, and review triggers.

The executable checker below illustrates cross-view consistency for a tiny architecture inventory. It verifies that assets have owners and policy identifiers, flows have purposes and contracts, and a flow does not target a less restrictive classification without an explicitly modeled approved treatment. One deliberately defective marketing export demonstrates the findings. String labels and rank ordering are pedagogical conventions, not a real classification policy.

<!-- bijux-verify: {"id":"architecture-cross-view-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"valid_flows=2\nviolations=5\nfindings=marketing_export.owner,marketing_export.policy,orders->marketing_export.classification,orders->marketing_export.contract,orders->marketing_export.purpose\n","stderr":""}} -->
```python
RANK = {"public": 0, "internal": 1, "confidential": 2, "restricted": 3}

assets = [
    {"name": "orders", "owner": "commerce", "class": "confidential", "policy": "orders-7y"},
    {"name": "shipment_projection", "owner": "logistics", "class": "confidential", "policy": "shipment-2y"},
    {"name": "revenue_metrics", "owner": "finance", "class": "restricted", "policy": "finance-7y"},
    {"name": "marketing_export", "owner": "", "class": "internal", "policy": ""},
]

flows = [
    {"source": "orders", "target": "shipment_projection", "purpose": "fulfillment", "contract": "order-v3"},
    {"source": "orders", "target": "revenue_metrics", "purpose": "reporting", "contract": "order-v3"},
    {"source": "orders", "target": "marketing_export", "purpose": "", "contract": ""},
]

index = {asset["name"]: asset for asset in assets}
findings = []
for asset in assets:
    if not asset["owner"]:
        findings.append(f"{asset['name']}.owner")
    if not asset["policy"]:
        findings.append(f"{asset['name']}.policy")

valid_flows = 0
for flow in flows:
    label = f"{flow['source']}->{flow['target']}"
    source = index[flow["source"]]
    target = index[flow["target"]]
    before = len(findings)
    if not flow["purpose"]:
        findings.append(f"{label}.purpose")
    if not flow["contract"]:
        findings.append(f"{label}.contract")
    if RANK[target["class"]] < RANK[source["class"]]:
        findings.append(f"{label}.classification")
    if len(findings) == before:
        valid_flows += 1

print(f"valid_flows={valid_flows}")
print(f"violations={len(findings)}")
print(f"findings={','.join(sorted(findings))}")
```

The result establishes only that a small inventory satisfies declared syntactic rules except where shown. It does not prove that owners have authority, policies are lawful or ethical, classifications are accurate, contracts preserve meaning, or actual runtime flows match the inventory.

## Alternatives and Trade-Offs

**Centralized versus federated authority.** Central authority can standardize terminology and controls but may lack domain knowledge and become a bottleneck. Federation keeps meaning near accountable domains but needs shared interoperability and escalation mechanisms. The right split varies by decision: identity, classification, platform controls, and local product semantics need not share one authority.

**Canonical enterprise model versus bounded translation.** A canonical model reduces pairwise transformations for stable shared concepts. Universal models often accumulate compromises and slow change. Bounded models with explicit translation preserve domain autonomy but require mapping ownership and compatibility evidence.

**Movement versus access by reference.** Copying improves local performance and resilience but multiplies lifecycle, quality, and security obligations. Federation or in-place computation reduces copies but creates runtime dependency, authorization, latency, and availability concerns. Architecture should choose from workload and policy, not from slogans.

**Global platform versus plural platforms.** One platform can simplify operation and governance. Diverse workloads, sovereignty, acquisitions, and specialized capabilities may justify several. Platform count is not the objective; coherent contracts, portability, evidence, and lifecycle cost are.

**Preventive versus detective controls.** Prevention blocks disallowed behavior but can impede legitimate exceptional work. Detection and correction preserve flexibility but permit exposure before response. High-consequence flows often need layered controls with explicit residual risk.

**Detailed versus minimal architecture descriptions.** Detail supports implementation and audit, but stale diagrams create false confidence. Maintain only views tied to decisions and automate synchronization where possible. Mark as-of dates, authority, uncertainty, and review triggers.

## Failure Modes and Misconceptions

1. **Architecture is a platform diagram.** Products and stores omit meaning, ownership, policy, and transition.
2. **One enterprise model eliminates ambiguity.** It can instead hide valid contextual differences behind overloaded fields.
3. **The source system owns every downstream product.** Derivations create new semantic and service responsibilities.
4. **Custody equals ownership.** Operating storage does not grant authority to redefine business facts or policy.
5. **An arrow documents a flow.** Without purpose, contract, time, failure, and controls, it is decoration.
6. **Policy documents enforce themselves.** Enforcement points, exception paths, operators, and evidence are required.
7. **A catalog is the architecture.** It supports discovery but does not decide boundaries, authority, or transition.
8. **The target state justifies a big-bang migration.** Intermediate consistency, rollback, and coexistence may be the dominant risks.
9. **Every copy is a system of record.** Copies may be projections with explicit freshness and reconciliation obligations.
10. **Automated conformance proves good architecture.** It proves only encoded predicates over observed inputs.

## Worked Examples

### Example 1

**Question:** Is a diagram showing a warehouse, lake, catalog, and dashboards a data architecture?

**Reasoning:** It is one technology/topology view. It omits conceptual structure, authoritative sources, data contracts, owners, policy propagation, quality attributes, current evidence, and transitions. It may contribute to an architecture description but cannot stand alone.

**Conclusion:** Technology topology is necessary for some concerns and insufficient for the architecture.

### Example 2

**Question:** Who owns an `email_address` field stored in a shared platform?

**Reasoning:** The platform team owns custody and service. A customer-identity domain may own the asserted contact fact; a verification service owns verification status; privacy authority decides permitted purposes; consumer domains own their derived use. One column has several distinct decisions.

**Conclusion:** Assign ownership by decision, not by storage location.

### Example 3

**Question:** What must an arrow from payroll to analytics declare?

**Reasoning:** Name the dataset/version boundary, purpose, legal/organizational authority, source and destination owners, interface, schedule or trigger, transformation, latency/completeness, classification, access, retention, failure/reconciliation, and evidence. Otherwise reviewers cannot judge consequence.

**Conclusion:** A flow is a governed relationship, not merely connectivity.

### Example 4

**Question:** Can a warehouse copy be authoritative for revenue reporting?

**Reasoning:** Yes, for a specifically defined reported-revenue measure if finance owns its rules, source reconciliation, close process, corrections, and service. It need not become authoritative for payment settlement or order acceptance.

**Conclusion:** Authority is scoped to a fact, purpose, and time boundary.

### Example 5

**Question:** A policy requires restricted data to remain in approved regions. What architecture evidence is needed?

**Reasoning:** Map classification and residency scope to flows, stores, backups, support access, processing services, logs, and derived outputs. Name enforcement points and exceptions. Test configured and observed locations and retain decision evidence. A cloud-region label alone misses operators and copies.

**Conclusion:** Policy outcomes require cross-view scope, controls, and evidence.

### Example 6

**Question:** Should every domain use one customer identifier?

**Reasoning:** A stable enterprise party identifier may improve reconciliation. Domains may still need account, user, household, device, or subject identifiers with different lifecycle and policy. Force-fitting them into one key produces incorrect joins.

**Conclusion:** Shared identity requires explicit semantic equivalence, not naming uniformity.

### Example 7

**Question:** How does a feedback flow change a recommendation architecture?

**Reasoning:** Recommendations influence clicks, which enter future training data. The flow is causal, delayed, selective, and potentially self-reinforcing. Architecture must show experiment assignment, event provenance, policy, monitoring, and authority to intervene.

**Conclusion:** Feedback edges carry different risks from one-way analytical delivery.

### Example 8

**Question:** A target architecture replaces twelve databases with one platform. Is simplification proven?

**Reasoning:** Count reduction may centralize failure, authority conflicts, migration coupling, and incompatible workloads. Compare operational cost, boundaries, recovery, policy, change autonomy, performance, and transition complexity—not logos or instance count.

**Conclusion:** Architectural simplicity is reduced decision and coordination complexity, not necessarily fewer products.

### Example 9

**Question:** A national blood-allocation service proposes a shared patient and inventory hub. Is cross-view consistency enough for approval?

**Reasoning:** No. Clinical meaning, allocation policy, identity errors, timeliness, downtime, regional authority, privacy, cybersecurity, audit, recovery, human factors, and migration require named clinical, blood-service, safety, legal/privacy, security, operational, records, accessibility, and independent assurance review. No external review is claimed here.

**Conclusion:** High-stakes architecture needs domain authorization and system evidence beyond structural coherence.

### Example 10

**Question:** What makes a transition architecture credible?

**Reasoning:** Each intermediate state has owners, write authority, synchronization direction, compatibility, reconciliation, policy coverage, observable entry/exit criteria, rollback, and decommission evidence. “Migrate data, then switch” supplies none of these.

**Conclusion:** Transition states are production architectures, not project annotations.

## Cross-Program Connections

Data engineering realizes pipelines and data products inside the architecture; data architecture decides enterprise boundaries, ownership, integration styles, policy propagation, and evolution. Database engineering supplies storage, query, transaction, and recovery mechanisms. Large-scale data systems supply distributed execution mechanisms. None of these mechanism choices independently determine enterprise authority or meaning.

Software architecture contributes stakeholder concerns, quality attributes, views, trade-offs, and decision records. Systems engineering contributes system boundaries, environments, interfaces, verification, and lifecycle thinking. Security and privacy turn policy into cross-cutting constraints and controls. API and service engineering make selected data flows explicit contracts.

Organizational design is part of feasibility. An architecture assigning rapid domain-local decisions to a quarterly central committee contradicts itself. Conversely, federation without common standards, platform capabilities, escalation, and evidence can produce disconnected local optimizations. Technical and social structures must be designed together.

## References

- ISO/IEC/IEEE, [*42010:2022 — Software, systems and enterprise—Architecture description*](https://www.iso.org/standard/74393.html), second edition, 2022. Current international requirements for architecture descriptions, viewpoints, and model kinds.
- The Open Group, [*TOGAF Standard, 10th Edition*](https://www.opengroup.org/togaf), checked 2026-08-29. Current official enterprise-architecture framework and guidance source.
- DAMA International, [*DAMA-DMBOK 2.0 Revised*](https://dama.org/dama-dmbok-revision/), 2024 maintenance release, checked 2026-08-29. Professional data-management knowledge-area and terminology reference.
- Wo L. Chang, David Boyd, and Orit Levin, [*NIST Big Data Interoperability Framework: Volume 6, Reference Architecture*](https://doi.org/10.6028/NIST.SP.1500-6r2), NIST SP 1500-6r2, 2019. Vendor-neutral provider, consumer, framework, management, security/privacy, and flow roles.
- W3C, [*Data Catalog Vocabulary (DCAT), Version 3*](https://www.w3.org/TR/vocab-dcat-3/), Recommendation, 22 August 2024. Current standard distinction among datasets, distributions, data services, series, and catalogs.
- NIST, [*Privacy Framework 1.0*](https://doi.org/10.6028/NIST.CSWP.01162020), 2020. Official privacy-risk and data-processing-ecosystem framework; policy authority remains context-specific.
- David L. Parnas, [*On the Criteria To Be Used in Decomposing Systems into Modules*](https://doi.org/10.1145/361598.361623), Communications of the ACM 15(12), 1972. Primary information-hiding and decomposition argument.
- Melvin E. Conway, [*How Do Committees Invent?*](https://www.bitsavers.org/magazines/Datamation/196804.pdf), Datamation 14(4), 1968. Primary argument relating communication structures and system designs.
- Len Bass, Paul Clements, and Rick Kazman, [*Software Architecture in Practice*, fourth edition](https://www.pearson.com/en-us/subject-catalog/p/software-architecture-in-practice/P200000003421), Addison-Wesley, 2021. Durable stakeholder, quality-attribute, architecture, and evaluation foundations.
- Eric Evans, [*Domain-Driven Design*](https://www.informit.com/store/domain-driven-design-tackling-complexity-in-the-heart-9780321125217), Addison-Wesley, 2003. Durable domain, bounded-context, model, and responsibility foundations.

## Exercises

### Exercise 1

For an online marketplace, give one example each of a structure element, flow, ownership decision, and policy obligation. Explain how the four connect.

### Exercise 2

Given a flow from `clinical_events` to `research_extract`, formulate the minimal `Coherent(f)` checks and identify at least four substantive questions the predicate cannot answer.

### Exercise 3

A catalog lists three customer datasets, each called authoritative. Diagnose the architecture defect and design evidence to determine legitimate authority without simply selecting the newest platform.

### Exercise 4

Compare a central canonical customer model with bounded domain models plus translations. Recommend an approach for a multinational retailer and state decision criteria, exceptions, and transition needs.

### Exercise 5

A regional emergency-communications network is merging dispatch, hospital-capacity, road-closure, and public-alert data. Design the architecture review package and named human-review roles required before a staged cutover. Include offline operation, conflicting authority, sensitive data, and rollback.

## Answers to the Exercises

### Answer 1

A structure element is the `Listing` concept and its versioned product; a flow carries accepted listing changes from marketplace operations to search indexing; the marketplace domain owns validity and correction of listing facts while search owns its projection service; policy requires prohibited-content classification and region-specific visibility to propagate to the index. Connect them through stable listing/product identities, a versioned event contract, source and target owners, policy attributes and enforcement at publication/search serving, plus reconciliation and evidence. The platform team may operate transport without becoming semantic owner.

### Answer 2

Check that source and target identities exist, the flow has an accountable owner, purpose and contract, and applicable classification/access/lifecycle policy has an enforcement path. Also check timing, failure and correction fields if the local viewpoint requires them. These populated fields cannot determine whether patient consent or other authority permits the research purpose, whether de-identification is adequate, whether the clinical semantics are correct, whether the owner actually has decision authority, whether the extract can be re-identified through combination, or whether runtime behavior matches the inventory. Those require clinical, privacy/legal, security, research-ethics, technical, and empirical review as applicable.

### Answer 3

The defect is unscoped authority: “customer” may denote legal party, account, user, contact, household, support profile, or analytical identity. Inventory each product's grain, identifiers, creation/correction rights, temporal boundary, source evidence, consumers, owner, and promised facts. Trace actual write and reconciliation flows, interview accountable domain authorities, sample conflicting cases, and record which product is authoritative for each named fact and time. Establish translations rather than declaring one universal winner. Platform recency is irrelevant unless the platform also has legitimate semantic authority and evidence.

### Answer 4

Use bounded domain models for commerce, loyalty, billing, support, and regional legal-party contexts, with a small governed shared identity/reference layer where equivalence is defensible. This preserves local language and change autonomy while enabling selected enterprise questions. Choose shared concepts by stability, cross-domain value, policy need, identity quality, and cost of translation. Permit explicit regional exceptions when law, language, product model, or sovereignty differs; record owner, scope, mapping, and review trigger. Transition through source inventory, identity-quality analysis, mapping contracts, shadow reconciliation, consumer migration, rollback, and retirement of redundant masters—not a big-bang canonical rewrite.

### Answer 5

The package should contain system/environment scope; stakeholder/concern register; conceptual vocabulary and authority map; source, projection and offline-copy inventory; end-to-end normal, degraded, correction, feedback, retention and deletion flows; decision-rights matrix; classification/access/purpose policy; interface, timing, availability and staleness contracts; threat/privacy/safety analyses; current-target-transition views; reconciliation, dual-run, cutover, rollback and decommission plan; drills and acceptance evidence; unresolved gaps and exception records. Named reviewers should include dispatch commanders, emergency clinicians/hospital operations, road/transport authorities, public-alert and accessibility specialists, public-safety/human-factors assurance, privacy/legal and records authorities, cybersecurity, network/platform/data engineers, field responders, partner/jurisdiction representatives, continuity/recovery operators, community communication authorities, and an independent assurance authority required by the jurisdictions. Offline replicas need authority, freshness, conflict, reconnection, encryption and disposition rules. No chapter or automated check can authorize this cutover; external domain approval and realistic staged exercises are mandatory.
