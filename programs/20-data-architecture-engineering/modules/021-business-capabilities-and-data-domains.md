---
module_id: DARCH-021
program: Data Architecture Engineering
level: 1
module_number: 21
title: Business Capabilities and Data Domains
status: complete
last_verified: 2026-09-03
---

# Business Capabilities and Data Domains

## One-Page Review

### Governing question

How can an organization use business capabilities, domain models, value and decision flows, ownership, and evidence to define durable data domains without merely copying its org chart, applications, databases, projects, or fashionable architecture labels?

### Essential definitions

- A **business capability** is an ability to produce a business outcome without specifying the particular process, organization, system, or technology that realizes it.
- A **business domain** is a coherent area of business knowledge, language, rules, decisions, and responsibility.
- A **bounded context** is an explicit boundary within which one domain model and its language apply consistently.
- A **data domain** is an accountable semantic and governance boundary for related data assertions, contracts, policies, and products; it may align with a bounded context but is not automatically identical to one.
- A **capability map** organizes abilities at useful levels of decomposition and relates them to outcomes, information, stakeholders, value, and implementation.
- A **domain map** records domains, bounded contexts, relationships, upstream/downstream responsibilities, translations, and shared concerns.
- A **data product** is a deliberately managed interface that provides data and metadata to named or anticipated consumers with ownership, quality, protection, support, and lifecycle commitments.
- A **system of entry** captures an assertion, a **system of reference** maintains an authoritative view for a declared scope, and a **system of insight** derives interpretations. These roles may differ by attribute, use, and time.
- **Domain ownership** is accountable authority and operational responsibility for specified data products and assertions, not unrestricted possession of every copy.
- **Federated governance** combines local domain decision rights with enforceable organization-wide obligations for interoperability, protection, risk, and evidence.

### Central model, mechanism, or theorem

Represent a candidate data domain as:

`D = (purpose, capabilities, outcomes, concepts, decisions, invariants, authorities, products, dependencies, protections, team, lifecycle)`

Assess a boundary with:

`Fit(D) = cohesion_inside - coupling_outside - ownership_ambiguity - governance_risk`

The expression is a decision frame, not a universal numerical formula. A durable data domain groups concepts and responsibilities that change together under one coherent language and accountable team, while exposing explicit contracts to other domains. Capability maps contribute stable “what,” but value flows, domain language, authority, change coupling, protection, and operability decide the actual boundary.

### Critical invariants

- Capabilities describe enduring abilities and outcomes, not departments, applications, processes, projects, or implementation stages.
- Domain boundaries follow coherent language, rules, decisions, change, and authority; organization structure is evidence but not proof.
- Every data concept and product has one accountable owning domain for a declared scope, while stewardship and contribution may be shared.
- Ownership is defined at a useful level: entity, attribute, relationship, event, policy, product, jurisdiction, and time—not by a vague enterprise label.
- Operational and analytical responsibilities are connected through domain semantics without requiring one physical platform or storage pattern.
- Cross-domain dependencies use versioned contracts, translations, provenance, quality objectives, protection rules, and escalation paths.
- Shared, aggregate, and consumer-aligned data products have explicit derivation authority and do not silently seize upstream ownership.
- Platform teams provide reusable capabilities; they do not become default owners of every domain's meaning or quality.
- Federated policies are computable where possible, locally actionable, centrally observable, and backed by accountable exceptions.
- Domain changes are evaluated against business outcomes, consumer impact, cognitive load, risk, and lifecycle evidence rather than diagram neatness.

### Common failures

Common failures are copying reporting lines into domain maps; naming every database a domain; treating capabilities as processes or software features; decomposing too finely to operate; creating a universal Customer domain with no scoped authority; assigning joint ownership to avoid decisions; centralizing all data quality in a platform team; decentralizing without interoperability rules; confusing physical locality with semantic ownership; creating data products with no consumers or service commitments; treating raw tables as products; allowing consumer aggregates to overwrite source meaning; measuring maturity by artifact counts; reorganizing teams without migration plans; and using “data mesh” to rename an unchanged centralized backlog.

### Compact example

An insurer has capabilities for Quote Risk, Underwrite Policy, Bill Account, Settle Claim, and Manage Party. The current application map puts party, policy, billing, and claim tables in one core system, while separate teams own channels. A domain analysis identifies Party, Policy, Billing, and Claims languages and invariants; defines scoped authority for legal identity, contact channels, policy terms, balances, and loss events; creates source-aligned products plus a governed Claims Performance aggregate; and assigns stable teams. Physical tables can remain temporarily co-located while contracts, ownership, lineage, protection, and migration follow the semantic boundaries.

### Connections

[DARCH-019](019-model-versioning.md) and [DARCH-020](020-reconciling-conflicting-models-across-systems.md) establish versioned contracts and cross-system mediation. This module begins the Domains, Ownership, and Data Products block before [DARCH-022](../ROADMAP.md) deepens boundary design, [DARCH-023](../ROADMAP.md) assigns accountability, and [DARCH-025](../ROADMAP.md) distinguishes source, aggregate, and consumer-aligned data.

## Governing Question

Organizations need boundaries that survive reorganizations, platform migrations, and individual applications. Business capabilities help because they describe what an enterprise must be able to do, relatively independently of how it does it. Domain analysis helps because it reveals distinct languages, rules, identities, and decisions. Data architecture must connect the two without assuming they are the same partition.

A capability may require data from several domains. One domain may support several capabilities. A bounded context can implement part of a capability, and a data product can serve several consumers without becoming a new enterprise domain. The architect's task is to establish accountable semantic boundaries and explicit relationships, then test whether teams can operate them safely.

## Why This Matters

Bad domain boundaries create chronic coordination. Changes require many teams, meaning drifts, quality issues have no owner, central platforms become ticket queues, and consumers copy data into undocumented marts. Boundaries that are too large overload teams and hide distinct languages. Boundaries that are too small multiply contracts and distributed failure.

The Object Management Group's [Business Architecture Core Metamodel 1.0](https://www.omg.org/spec/BACM/1.0/) defines capability as an ability to produce an outcome without specifying how, and relates capabilities to outcomes, business objects, information items, roles, value, and implementations. This supports the core separation between stable business ability and changing realization.

The OMG [Business Motivation Model 1.3](https://www.omg.org/spec/BMM/) separates ends, means, influencers, assessments, strategies, tactics, policies, and rules. Data domains should be traceable to outcomes and governing decisions, not derived from data inventories alone.

Eric Evans's [Domain-Driven Design Reference](https://www.domainlanguage.com/ddd/reference/) defines strategic patterns including bounded context, context map, shared kernel, customer/supplier, conformist, anticorruption layer, open host service, and published language. These patterns explain why a model needs a boundary and how independently governed models relate.

Zhamak Dehghani's [data mesh principles](https://martinfowler.com/articles/data-mesh-principles.html) connect domain-oriented ownership, data as a product, self-serve infrastructure, and federated computational governance. Adopting one slogan without the other three produces either centralized dependence, fragmented silos, unusable data, or uncontrolled risk.

## Prerequisites and Retrieval

You should understand business architecture, outcomes, value streams, processes, organizations, domain modeling, bounded contexts, canonical models, model reconciliation, data products, metadata, platforms, governance, quality, security, privacy, and team design.

Retrieve capability, outcome, business object, information item, resource, process, value stream, domain, subdomain, core, supporting, generic, bounded context, ubiquitous language, context map, cohesion, coupling, authority, ownership, stewardship, system of entry, system of reference, source-aligned, aggregate, consumer-aligned, data product, platform, federation, computational governance, cognitive load, topology, contract, service level, and lifecycle.

As a retrieval test, inspect a proposed “Customer domain.” Ask which capability and outcomes it supports; whether Customer means person, account, debtor, subscriber, patient, citizen, or role; which bounded contexts use which definitions; who is authoritative for each assertion and time; which products consumers need; what protection applies; and which team can operate the boundary. If those answers vary materially, the label is not yet a viable domain design.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish capabilities from processes, value streams, organizations, applications, projects, services, datasets, and domains;
2. construct capability and domain maps at levels that support decisions without false precision;
3. identify domains through language, invariants, decisions, authority, change patterns, value, and team operability;
4. classify core, supporting, generic, source-aligned, aggregate, and consumer-aligned responsibilities without turning labels into dogma;
5. relate capabilities, bounded contexts, data domains, operational services, analytical products, and physical platforms many-to-many;
6. define scoped ownership, stewardship, contribution, consumption, escalation, and governing-body accountabilities;
7. design data products with consumers, contracts, semantics, metadata, quality, protection, observability, support, and lifecycle;
8. balance domain autonomy with federated interoperability, security, privacy, quality, and portfolio governance;
9. evaluate boundaries using cohesion, coupling, cognitive load, change, risk, cost, and outcome evidence;
10. plan incremental transition from application- or platform-centered data ownership without losing service, provenance, or control.

## Core Exposition

**Start with outcomes and decisions.** Ask what outcomes the enterprise must produce, for whom, under which policies, and how success is measured. Then identify abilities required regardless of the current organization or technology. This avoids reproducing historical implementation accidents.

Capabilities are not verbs from a process diagram with “management” appended. Define an ability with purpose, outcome, business objects or information, stakeholders, policies, performance, and scope. “Settle Claim” is an ability; a particular five-step workflow, claims department, vendor package, and API are realizations.

**Separate capability from realization.** Processes describe behavior, value streams describe progression of value, organizations provide performers, systems automate work, and data supplies or records information. One capability can have several implementations across channels or regions. One process can use several capabilities.

This separation makes maps stable enough for planning. It also prevents application replacement from appearing to change the business's fundamental abilities. Record realization links so the map remains actionable rather than abstract decoration.

**Use a consistent capability decomposition.** Decompose by enduring business meaning, not arbitrary size. Parent and child capabilities should maintain a clear “ability to” relationship and collectively explain the parent without mixing process stages, organization names, or technologies.

Avoid more detail than the decision requires. A portfolio heat map may use two or three levels; ownership and contract design may need deeper analysis. Different views can select levels from one identified hierarchy. Do not pretend sibling capabilities are mutually exclusive when the business overlaps.

**Connect capabilities to information.** For each capability, identify information consumed, produced, changed, decided upon, and evidenced. Distinguish business objects from information items and representations. “Policy” may denote a contract, a set of terms, a document, a database row, or an organizational directive.

Record CRUD-style matrices only as a starting clue. “Reads Customer” does not reveal whether the capability needs legal identity, contact preference, credit role, or a current summary. Add concepts, predicates, grain, time, authority, protection, and consequence.

**Map value and decisions.** Capabilities contribute to outcomes through value streams, products, journeys, processes, and decisions. This context reveals data that must cross boundaries. A value-stream stage may need a stable contract even when its participating capabilities live in separate domains.

Decision models are especially useful. If Quote Risk and Underwrite Policy interpret risk differently, the domain design should expose that distinction rather than force one score. Trace input data, rules, authorities, outputs, and feedback.

**Discover domains through language.** Listen for terms whose definitions change across groups. Identify rules that must remain internally consistent, concepts that co-evolve, and experts who can resolve ambiguity. A bounded context names where one model and language apply.

Do not demand one ubiquitous enterprise language. Enterprise vocabulary can record correspondences and shared identifiers, while contexts retain specialized meanings. Published languages and anticorruption layers protect boundaries and make translation explicit.

**Distinguish domain, subdomain, and bounded context.** A domain is the broad area being addressed. Subdomains partition problem responsibility and may be core, supporting, or generic in a strategic analysis. A bounded context is a model boundary in the solution landscape. Their mapping can be one-to-one, but it need not be.

One subdomain may have multiple contexts because of lifecycle, regional, or legacy constraints. One context may provisionally cover several small supporting subdomains. Record the relationship and target rationale instead of enforcing a diagram rule.

**Define a data domain explicitly.** A data domain should state purpose, in-scope and out-of-scope concepts, assertions, events, authorities, consumers, products, dependencies, protection, team, and lifecycle. It is not merely a folder in a catalog or namespace in a warehouse.

Semantic ownership can remain with a domain while storage uses shared infrastructure. Conversely, data physically stored in a domain account may be owned semantically by an upstream provider. Label source, derived, cached, replicated, and locally asserted data.

**Use capabilities as one boundary signal.** A capability cluster can reveal data and decisions that belong together. But mapping one domain per capability often fragments shared invariants. Manage Policy, Price Policy, and Underwrite Policy may operate on one coherent Policy model or several contexts depending on language and change.

Score candidate boundaries against multiple signals: shared terminology, invariants, authority, change cadence, transactional consistency, data gravity, protection, outcome cohesion, team cognitive load, consumer contracts, and failure isolation. Treat the score as structured judgment, not objective arithmetic.

**Do not copy the org chart.** Current reporting lines reflect management history, geography, funding, and span of control. They can reveal expertise and accountability but change more often than many domain concepts. If every reorganization changes data identity, ownership becomes unstable.

Design durable semantic boundaries, then assign teams. Where organizational responsibility conflicts with the desired boundary, record transitional ownership and a migration. Never create “joint ownership” solely because managers cannot agree; name one accountable owner for each product or assertion scope and explicit contributors.

**Do not copy the application map.** A monolith may contain many domains; several applications may implement one domain. Vendor packages often blend generic functions and local distinctions. Databases reflect deployment and transaction choices, not necessarily knowledge boundaries.

Inventory applications, schemas, interfaces, and teams as evidence. Annotate which domain concepts they implement, where semantics leak, and what should be isolated. Physical separation can follow later when risk and value justify it.

**Classify strategic importance carefully.** Core subdomains create differentiation or mission advantage. Supporting subdomains enable the core but are not differentiators. Generic subdomains have broadly available solutions. The classification is contextual and changes over time.

It informs investment, expertise, sourcing, and tolerance for customization. It does not determine whether data needs ownership, quality, or protection. Payroll may be generic strategically yet highly sensitive and operationally critical.

**Scope authority below the domain label.** One Party domain cannot be universally authoritative for every party-related fact. Legal identity, contact preference, sanctions status, employment role, credit assessment, and marketing segment may have different authorities and effectivity.

Create an authority matrix by subject, predicate, context, jurisdiction, valid time, recorded time, and use. Distinguish system of entry, authoritative reference, derived insight, and consumer cache. Define correction and dispute workflows.

**Design context relationships.** A context map should name upstream/downstream influence, shared kernel, partnership, customer/supplier, conformist, anticorruption layer, open host service, published language, or deliberate separation as applicable. The relationship is governance as much as integration.

A shared kernel reduces translation but couples change and requires joint ownership of a small, explicit surface. Conformist adoption saves effort but accepts upstream meaning. An anticorruption layer protects a model at translation cost. Choose consciously and revisit with evidence.

**Connect operational and analytical data.** Operational services enforce current transactions and invariants. Analytical products retain histories, combine sources, and support exploratory or repeated decisions. The technologies and release cadences differ, but domain meaning should remain traceable.

Domain-oriented ownership can bring analytical responsibility closer to those who understand source semantics. It does not require the operational team alone to perform all engineering. Cross-functional teams or durable collaboration must cover product, domain, data engineering, reliability, security, privacy, and consumer support.

**Define data product boundaries.** A data product is not every table or file. Begin with consumer decisions and a cohesive semantic promise. Define address, interface, schema, grain, time, provenance, quality objectives, availability, freshness, retention, access, cost, support, versioning, and deprecation.

Products can expose events, tables, files, APIs, graphs, features, metrics, or query services. Their physical form can change if the contract and migration are governed. Avoid bundling unrelated data merely because one pipeline produces it.

**Keep datasets distinct from distributions and services.** W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) distinguishes conceptual datasets, distributions, data services, dataset series, and catalog records, and supports decentralized catalogs and version metadata. This helps a product catalog avoid treating one file location as the data product itself.

Catalog metadata should include owner, contact, domain, purpose, themes, descriptions, versions, distributions, access services, rights, quality, lineage, and lifecycle. Discovery is necessary but not sufficient: a catalog entry without an operating team and usable contract is inventory, not a product.

**Assign product accountability.** One accountable team owns product outcomes, contract decisions, quality, protection, support, change, and retirement. Contributors can supply source data, platform capabilities, stewardship, and policy review. Consumers share responsibility for correct use and timely migration.

Define escalation and decision rights. Product ownership without budget, skills, access, or authority is a label. Conversely, ownership does not grant permission to override legal, security, privacy, records, or enterprise interoperability obligations.

**Use federated governance.** Organization-wide policies should cover identifiers, contract metadata, interoperability, security, privacy, residency, retention, quality evidence, lineage, accessibility, incident response, and lifecycle. Domains make local decisions within those constraints and participate in shared evolution.

Computable controls can validate required metadata, schema compatibility, lineage, classification, access, encryption, retention, and service objectives. Human governance remains necessary for semantics, authority, purpose, exceptions, and consequence. Automation enforces declared rules; it does not invent legitimate policy.

ISO/IEC [38505-1:2026](https://www.iso.org/standard/87195.html) frames governance of data as governing current and future use, protection, and management decisions. Domain autonomy operates under governing-body accountability rather than outside it.

**Separate platform and domain responsibilities.** The platform offers paved paths for storage, compute, contracts, cataloging, identity, policy, quality, lineage, observability, deployment, and recovery. It owns the usability and reliability of those capabilities. Domains own their meanings, products, and local operational decisions.

If every new product requires platform tickets, autonomy is fictional. If every domain builds encryption, catalog, and orchestration independently, duplication and risk grow. Product-manage the platform with domain teams as customers and measure time-to-safe-product, not resource counts.

**Use provenance to preserve accountability.** W3C [PROV-O](https://www.w3.org/TR/prov-o/) models entities, activities, agents, usage, generation, derivation, and attribution. These distinctions can link data products to sources, transformations, teams, and releases without claiming the catalog itself proves factual authority.

Lineage should answer which domain assertions and transformations produced an output, under what versions and policies. Cross-domain aggregates must retain upstream provenance and local derivation authority. Do not let the aggregate owner silently become the source owner.

**Design aggregate and consumer-aligned domains carefully.** Some products combine several domains for a coherent analytical purpose, such as Customer Lifetime Value or Network Risk. Assign ownership to the team accountable for the derived concept and consumer outcome, while preserving upstream contracts and authority.

Avoid “shared” as a dumping ground. A shared domain needs a coherent language, stable consumers, decision rights, and durable team. If it merely hosts fields nobody else wanted, revisit the model.

**Evaluate cohesion.** A cohesive domain contains concepts and rules that need coordinated change and expert interpretation. Indicators include shared invariants, common lifecycle, one decision authority, high internal interaction, and a clear product portfolio.

Low cohesion appears as unrelated datasets, many optional concepts, multiple incompatible languages, and ownership escalation for ordinary changes. Split by durable meaning, not file size. Preserve contracts between the resulting domains.

**Evaluate coupling.** Count dependency directions, change coordination, synchronous availability, semantic translations, shared transactions, shared schemas, and policy coupling. Some coupling reflects real business invariants and should not be hidden.

Reduce accidental coupling through stable contracts, events, caching, identifiers, anticorruption layers, and asynchronous workflows. Do not trade visible coordination for duplicated inconsistent truth without reconciliation.

**Evaluate team cognitive load.** A team must understand domain rules, consumers, technology, operations, quality, and protection well enough to own outcomes. An enormous domain exceeds that capacity; microscopic domains overwhelm teams with coordination and platform overhead.

Use incident history, change lead time, unanswered questions, ownership handoffs, on-call burden, and product support as evidence. Team boundaries and domain boundaries should co-evolve rather than one being treated as permanently correct.

**Evaluate risk and protection.** A boundary may need to isolate payment, health, identity, safety, export-controlled, or regulated data. Purpose and residency can require separate products even within a coherent business model. Conversely, splitting can create uncontrolled copies and inconsistent deletion.

Threat-model cross-domain joins, catalog metadata, lineage, development access, support tools, and aggregate inference. Define classification inheritance, least privilege, segregation, consent, retention, legal hold, deletion, audit, and incident ownership.

**Measure outcomes, not domain counts.** Useful measures include consumer time to discover and use, change lead time, contract breakage, data-quality objective attainment, unresolved ownership, incident recovery, support responsiveness, policy conformance, cost-to-serve, and consumer satisfaction.

Avoid quotas such as datasets per domain, products per team, or number of catalog entries. They reward fragmentation and relabeling. Measure whether business decisions and changes become safer, faster, and more understandable.

**Plan transitions incrementally.** Select a business outcome with painful coupling and willing owners. Baseline flows, models, consumers, incidents, quality, protection, cost, and lead time. Define candidate domains and contracts, then establish ownership and products alongside existing systems.

Use adapters, change data capture, events, views, or replicated products while physical systems remain. Reconcile outputs, migrate consumers in cohorts, monitor, and preserve rollback. Avoid a multi-year replatforming prerequisite; semantic and accountability improvements can begin before storage moves.

**Govern domain lifecycle.** Domains emerge, split, merge, transfer, and retire as the business changes. Version maps and contracts. Define how identifiers, products, histories, obligations, consumers, and teams move. A reorganization should not silently rewrite historical ownership or provenance.

Retirement requires consumer migration, archive interpretation, retention/deletion, support closure, incident transfer, and catalog state. A successor domain must explicitly accept obligations rather than inheriting them through a renamed folder.

**Treat uncertainty as evidence.** Early maps contain contested boundaries and unknown consumers. Record hypotheses, alternatives, experiments, decisions, owners, and revisit dates. Use event storming, domain narratives, capability workshops, dependency analysis, and product discovery as inputs—not ceremonies that automatically yield truth.

A good domain map is an evolving governance instrument. It enables teams to explain who can decide, what a product promises, how domains interact, and where risk remains. Its value is operational clarity, not colorful boxes.

## Definitions and Notation

Let `C = (ability, outcome, objects, information, stakeholders, measures, policies)` denote a capability independent of a particular realization. Let `I = (processes, people, systems, locations, vendors, controls)` denote one implementation. Several `I` can realize one `C`, and one `I` may support several capabilities.

Let a data domain candidate be `D = (L, R, A, P, T)`, where `L` is its language and model, `R` its invariants and decisions, `A` scoped authority, `P` product portfolio and dependencies, and `T` accountable team. A viable boundary needs internal coherence across these coordinates; shared vocabulary alone is insufficient.

Represent a capability-domain relation as a many-to-many edge `supports(D,C,scope,time,evidence)`. It does not assert identity between a capability and domain. A capability map and domain map can therefore evolve independently while their links remain versioned.

For candidate boundary `D`, use the qualitative decision frame:

`Fit(D) = cohesion(D) - external_coupling(D) - ownership_ambiguity(D) - governance_risk(D)`

Each term is an evidence bundle, not a universal scalar. Teams may use ordinal scores with definitions, but must preserve observations and tradeoffs rather than presenting arithmetic as proof.

A data-product contract is `P = (purpose, consumers, semantics, interface, SLOs, quality, provenance, protection, owner, version, lifecycle)`. Technical accessibility without the other coordinates is a distribution, table, or service—not yet a complete product commitment.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for each domain proposal.

**1. Outcome gate.** Identify stakeholders, outcomes, value, decisions, measures, obligations, and business motivation before drawing technology boundaries.

**2. Capability gate.** Define enduring abilities and decomposition separately from processes, organizations, applications, projects, and implementations.

**3. Language gate.** Discover concepts, definitions, examples, invariants, events, decisions, and conflicting meanings; propose bounded contexts and translations.

**4. Boundary gate.** Evaluate cohesion, coupling, authority, change, consistency, protection, value, and cognitive load across capability, domain, and system evidence.

**5. Authority gate.** Assign scoped accountable ownership for assertions, relationships, events, products, policies, corrections, disputes, and lifecycle.

**6. Product gate.** Define consumers, purpose, semantics, interfaces, quality objectives, SLOs, provenance, protection, support, versioning, cost, and retirement.

**7. Relationship gate.** Map upstream/downstream responsibilities, contracts, published languages, translations, shared kernels, aggregates, dependencies, and escalation.

**8. Governance gate.** Apply federated interoperability, security, privacy, quality, lineage, accessibility, financial, legal, and records controls with governed exceptions.

**9. Operability gate.** Verify team capacity, platform usability, deployment, monitoring, support, incident response, recovery, consumer migration, and sustainable cost.

**10. Evolution gate.** Test change scenarios, version maps, measure outcomes, revisit hypotheses, and govern domain split, merge, transfer, and retirement.

The executable example checks four narrow domain-proposal failures: a capability tied to one application, missing semantic scope, shared accountability, and a product without a consumer commitment.

<!-- bijux-verify: {"id":"data-domain-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidates=4\nvalid=0\nfindings=billing:application-defined-capability,customer:missing-semantic-scope,party:ambiguous-accountability,risk-score:missing-consumer-contract\nready=false\n","stderr":""}} -->
```python
candidates = (
    {"id": "billing", "capability_application_bound": True, "semantic_scope": "billing", "accountable_owners": 1, "is_product": False, "consumer_contract": True},
    {"id": "customer", "capability_application_bound": False, "semantic_scope": "", "accountable_owners": 1, "is_product": False, "consumer_contract": True},
    {"id": "party", "capability_application_bound": False, "semantic_scope": "party identity", "accountable_owners": 2, "is_product": False, "consumer_contract": True},
    {"id": "risk-score", "capability_application_bound": False, "semantic_scope": "underwriting risk", "accountable_owners": 1, "is_product": True, "consumer_contract": False},
)

findings = []
valid = 0
for candidate in candidates:
    local = []
    if candidate["capability_application_bound"]:
        local.append("application-defined-capability")
    if not candidate["semantic_scope"]:
        local.append("missing-semantic-scope")
    if candidate["accountable_owners"] != 1:
        local.append("ambiguous-accountability")
    if candidate["is_product"] and not candidate["consumer_contract"]:
        local.append("missing-consumer-contract")
    if local:
        findings.extend(f"{candidate['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"candidates={len(candidates)}")
print(f"valid={valid}")
print("findings=" + ",".join(sorted(findings)))
print(f"ready={str(valid == len(candidates)).lower()}")
```

The checker validates four declared proposal predicates only. It does not prove capability correctness, domain cohesion, complete ownership, product value, authority, team capacity, federated governance, protection, consumer satisfaction, migration safety, or business outcomes. Those require facilitated domain work, exact contracts, organizational evidence, representative consumers, operational measures, risk review, and accountable decisions.

## Alternatives and Trade-Offs

**Capability-first versus domain-first discovery.** Capability maps provide stable enterprise coverage; domain modeling provides semantic depth. Either alone can mislead. Iterate between outcomes, capabilities, language, systems, teams, and data flows.

**Large versus small domains.** Large domains reduce interfaces but increase cognitive load and internal inconsistency. Small domains improve focus but multiply contracts and distributed coordination. Choose the smallest boundary a durable team can own without splitting essential invariants.

**Centralized versus domain-oriented data ownership.** Central teams provide consistency and scarce expertise but become distant bottlenecks. Domain teams understand meaning and change but can fragment standards. Combine accountable domain products, self-service platforms, and federated controls.

**Operational-team versus dedicated data-product ownership.** Operational teams are close to source semantics but may lack analytical skills and capacity. Dedicated teams focus on consumers but can drift from the domain. Use durable cross-functional ownership and explicit source authority.

**Shared kernel versus translation.** A shared kernel reduces duplicate concepts but couples change and governance. Translation preserves autonomy but costs engineering and can lose meaning. Keep shared kernels small and versioned; translate where contexts legitimately differ.

**Physical co-location versus isolation.** Shared infrastructure can reduce cost and improve controls. Isolation can improve blast radius, residency, performance, and autonomy. Semantic ownership and product contracts should not depend on physical topology.

**One enterprise catalog versus federated catalogs.** One catalog improves discovery and policy visibility but can centralize curation. Federated publication respects ownership but requires common metadata and search. Use shared protocols with domain-maintained records.

**Permanent map versus evolving hypothesis.** A frozen map provides organizational stability but becomes false. Constant redrawing creates churn. Version maps, use change evidence, and revise through explicit lifecycle decisions.

## Failure Modes and Misconceptions

1. **Capabilities are processes.** A capability is an ability and outcome; processes are realizations.
2. **Capabilities are application features.** Applications implement capabilities and can be replaced.
3. **One capability requires one domain.** Their relation is many-to-many and depends on semantics.
4. **Domains are departments.** Organization structure is evidence, not the definition.
5. **Domains are databases.** Storage topology does not establish language or authority.
6. **A bounded context is a deployment unit.** It is a model boundary; deployment may align but need not.
7. **One enterprise language removes integration cost.** It often hides legitimate contextual differences.
8. **Every table is a data product.** Products require consumers, contracts, ownership, quality, protection, and support.
9. **A central platform owns data meaning.** It owns enabling capabilities unless explicitly assigned domain authority.
10. **Domain autonomy means no standards.** Autonomy requires federated interoperability and protection obligations.
11. **Joint ownership is collaborative.** Without one accountable decision owner, it often creates paralysis.
12. **Physical copies transfer ownership.** Replicas and derivatives retain source provenance and scoped authority.
13. **Core domains deserve governance; generic ones do not.** Strategic differentiation differs from criticality and sensitivity.
14. **A golden record belongs in a universal shared domain.** Authority is predicate-, purpose-, and time-specific.
15. **More domains mean greater maturity.** Excess fragmentation increases coordination and operating cost.
16. **A reorganization completes the architecture.** Contracts, products, systems, evidence, and consumers need migration.
17. **A catalog makes data discoverable and usable.** Metadata without operational ownership and a reliable interface is only inventory.

## Worked Examples

### Example 1

A bank's capability map lists Manage Party, Open Account, Assess Credit, and Detect Fraud. Domain analysis keeps Party identity distinct from Account contracts, Credit assessments, and Fraud hypotheses. Each assertion receives scoped authority and products rather than a universal customer table.

### Example 2

A department called Digital owns three unrelated applications and proposes a Digital domain. Language and change analysis reveals Acquisition, Identity, and Content contexts. The team structure changes gradually while contracts and ownership move to the three durable domains.

### Example 3

An ERP database contains billing, inventory, supplier, and payroll tables. The architecture documents four domains even though physical separation is initially too risky. Views, access controls, change ownership, and product contracts establish boundaries before later extraction.

### Example 4

A product catalog file is published nightly with no named consumers, freshness objective, support, or owner. Product discovery identifies pricing and recommendation uses, then splits stable reference and rapidly changing availability products with distinct contracts.

### Example 5

A central data team repairs source quality after ingestion. Recurring invalid shipping addresses persist because the fulfillment domain never sees failures. Quality ownership moves upstream with feedback and prevention, while the platform supplies validation and observability capabilities.

### Example 6

Two domains share a small Currency kernel of identifiers and decimal rules but interpret Price differently. The shared kernel is jointly governed; Price remains translated through published contracts. The design shares genuine invariants without forcing one pricing model.

### Example 7

A Claims Performance aggregate combines Policy, Claims, Party, and Finance products. Its owner is accountable for the derived metric and consumers, while upstream domains retain authority for their assertions. Lineage, versions, restatement, and reconciliation are part of the aggregate contract.

### Example 8

A healthcare domain seems cohesive but mixes treatment data and marketing outreach. Purpose and consent analysis requires separate protected products and access paths even where patient identity is shared. Platform policy enforces the boundary consistently.

### Example 9

A domain team owns fifteen products across five technologies and cannot sustain on-call or answer consumer questions. Cognitive-load evidence supports splitting into Transaction and Decision Support contexts with an explicit event contract and separate teams.

### Example 10

A merger creates overlapping Supplier domains. Instead of selecting one model by executive preference, teams compare capabilities, definitions, authorities, contracts, consumers, protections, and change patterns; publish translations; migrate cohorts; and retain historical provenance through the eventual boundary decision.

## Cross-Program Connections

- **Business analysis and architecture:** outcomes, capabilities, value streams, motivation, decisions, stakeholders, and operating models frame domains.
- **Software architecture:** bounded contexts, services, modularity, coupling, published languages, and team boundaries implement domain relationships.
- **Data engineering:** source and aggregate products, pipelines, lineage, quality, CDC, backfill, and serving interfaces operationalize ownership.
- **Platform engineering:** self-service storage, compute, contracts, catalogs, policy, observability, deployment, and recovery enable autonomy.
- **API and service engineering:** stable interfaces, compatibility, authentication, quotas, errors, and deprecation expose products to consumers.
- **Security and privacy:** classification, purpose, consent, residency, access, retention, deletion, and incident response constrain boundaries.
- **Product management:** consumer discovery, value, roadmaps, service commitments, satisfaction, cost, and lifecycle make data usable.
- **Systems engineering:** capability decomposition, interfaces, configuration, traceability, assurance, lifecycle, and organizational constraints inform evaluation.

## References

1. Object Management Group, *Business Architecture Core Metamodel*, Version 1.0, 2024. <https://www.omg.org/spec/BACM/1.0/>
2. Object Management Group, *Business Motivation Model*, Version 1.3, 2015. <https://www.omg.org/spec/BMM/>
3. Evans, E., *Domain-Driven Design Reference*, 2015. <https://www.domainlanguage.com/ddd/reference/>
4. Dehghani, Z., “Data Mesh Principles and Logical Architecture,” 2020. <https://martinfowler.com/articles/data-mesh-principles.html>
5. W3C, *Data Catalog Vocabulary (DCAT)—Version 3*, W3C Recommendation, 2024. <https://www.w3.org/TR/vocab-dcat-3/>
6. W3C, *PROV-O: The PROV Ontology*, W3C Recommendation, 2013. <https://www.w3.org/TR/prov-o/>
7. ISO/IEC, *11179-3:2023 Information technology—Metadata registries—Part 3: Metamodel for registry common facilities*, 2023. <https://www.iso.org/standard/78915.html>
8. ISO/IEC, *38505-1:2026 Information technology—Governance of data—Part 1: Application of ISO/IEC 38500 to the governance of data*, 2026. <https://www.iso.org/standard/87195.html>

## Exercises

### Exercise 1

Create a capability-to-domain analysis for an online retailer covering assortment, pricing, inventory, order, fulfillment, payment, party, and recommendation. Explain boundaries, many-to-many links, authorities, and products.

### Exercise 2

Evaluate a proposed enterprise Customer domain. Identify contextual meanings, bounded contexts, assertion-level authorities, shared identifiers, translations, protection, and cases where the proposal should split.

### Exercise 3

Specify a data product for released podcast listening events. Include consumers, semantics, grain, time, versions, quality, provenance, protection, SLOs, support, cost, and lifecycle.

### Exercise 4

Design federated governance responsibilities among a data-domain team, a self-service platform team, security/privacy functions, and a governing body. Cover policy, enforcement, evidence, incidents, and exceptions.

### Exercise 5

Plan an incremental transition from a central warehouse team to domain-oriented ownership without a wholesale replatform. Include baseline, pilot, contracts, team design, quality, migration, measures, rollback, and lifecycle.

## Answers to the Exercises

### Answer 1

Define capabilities independently of current systems: Manage Assortment, Set Price, Promise Availability, Capture Order, Fulfill Order, Settle Payment, Manage Party, and Generate Recommendation. Candidate domains include Catalog, Pricing, Inventory, Ordering, Fulfillment, Payments, Party, and Recommendations. Links are many-to-many: Capture Order consumes Price and Availability while Ordering owns order intent and lifecycle; Fulfillment consumes order commitments and owns shipment events.

Authority is scoped: Catalog owns product description, Pricing price decisions, Inventory stock observations and allocations, Ordering order state, Payments settlement, Party identity assertions, and Recommendations derived ranks. Products expose published schemas, versions, time, provenance, quality, protection, and support. A shared product identifier kernel can coordinate references, but offer, stocked item, and recommendation candidate remain contextual concepts. Aggregate commercial-performance products retain upstream authority and own only their derivations.

### Answer 2

Inventory meanings such as natural person, organization, prospect, buyer account, debtor, subscriber, patient, beneficiary, contact, and household. Identify which bounded contexts use each and which invariants differ. Create stable Party and Account identifiers only where identity semantics are justified; represent roles and relationships rather than renaming all records Customer.

Assign legal identity, contact preference, account status, credit assessment, marketing segment, and service entitlement to different authorities by purpose, jurisdiction, and time. Version translations and preserve unresolved matches. Protection can require separate views because consent and purpose differ. Split the proposal when languages, invariants, decision authorities, protections, change cadences, or team cognitive load are materially distinct. Retain an enterprise vocabulary and context map instead of forcing a single model.

### Answer 3

Name consumers such as royalty calculation, creator analytics, recommendations, and reliability analysis. Define grain as one accepted listening event per playback identity, with listener pseudonym, podcast and episode identities, occurrence and recorded times, duration semantics, geography precision, device class, schema and consent context. State deduplication, corrections, bot filtering, late-event windows, and exclusions.

Provide addressable event and batch interfaces, immutable versions, samples, lineage, retention, access, minimization, deletion behavior, and incident contact. Quality objectives cover valid identities, duplicate rate, lateness, completeness evidence, and reconciliation to operational counters. SLOs cover freshness, availability, recovery, and support. Record cost allocation, consumer limits, change notice, compatibility, deprecation, and retirement. The domain owns semantic and product outcomes; the platform owns the reusable serving controls.

### Answer 4

The domain team owns definitions, contracts, product quality, consumer support, local access intent, changes, corrections, incidents, and retirement. The platform team owns usable paved paths for identity, storage, compute, catalog, policy enforcement, lineage, observability, deployment, and recovery. Security and privacy functions define and review classification, purpose, access, residency, retention, deletion, threat, and incident obligations with domains.

The governing body evaluates, directs, and monitors effective, efficient, acceptable use and protection of data, setting risk appetite and accountability. Shared policies become machine-checkable controls where possible; evidence and exceptions remain visible. Domains propose exceptions with scope, risk, compensating controls, owner, expiry, and review. Incidents have one operational commander and explicit domain, platform, security/privacy, legal, consumer, and executive escalation responsibilities.

### Answer 5

Baseline consumer lead time, ownership gaps, quality incidents, change dependencies, warehouse products, source models, protection, costs, and platform constraints. Select one valuable, bounded pilot with motivated domain experts and consumers. Assign a cross-functional accountable team, publish a source-aligned product contract, and use current warehouse infrastructure through a self-service path rather than waiting for new storage.

Move quality feedback and semantic decisions toward the domain while the central team becomes an enabling platform and coaching function. Migrate consumers in cohorts, maintain old interfaces during a support window, reconcile results, and preserve rollback. Measure discovery-to-use time, change lead time, objective attainment, incidents, policy conformance, consumer satisfaction, and cost. Expand by business outcome, not quotas. Version ownership and contracts, fund on-call and lifecycle work, and retire old products only after consumer, archive, protection, and recovery evidence passes.
