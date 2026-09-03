---
module_id: DARCH-082
program: Data Architecture Engineering
level: 2
module_number: 82
title: Domain-Oriented Decentralization
status: complete
last_verified: 2026-09-03
---

# Domain-Oriented Decentralization

## One-Page Review

### Governing question

How should an enterprise distribute data authority and delivery to durable business domains while preserving explicit context boundaries, cross-domain identity and semantics, interoperable contracts, shared controls, end-to-end accountability, and the ability to split, merge, transfer, or recentralize responsibilities as the business changes?

### Essential definitions

- A **domain** is a durable sphere of business capability, language, rules, decisions, authority, events, and responsibility.
- A **subdomain** is a coherent part of a larger domain with distinct capability or knowledge; it can be core, supporting, or generic in a local strategic analysis.
- A **bounded context** is an explicit boundary within which a model and its language have a particular meaning and consistency.
- **Ubiquitous language** is the shared, evolving language used by domain experts and builders inside a bounded context.
- A **context map** records relationships, influence, translation, dependency, and integration patterns among bounded contexts.
- **Domain-oriented decentralization** transfers defined decision rights, product ownership, technical operation, funding, and accountability from a central unit to capable domain arrangements.
- **Source authority** identifies the domain and product authorized to assert a particular fact for a stated decision and valid time.
- A **domain event** records a meaningful fact or transition in a domain's language and boundary; an integration event is the published contract intended for external consumers.
- An **anti-corruption layer** translates another context's model into the receiving context's language and protects local semantics from accidental coupling.
- A **shared kernel** is a deliberately small jointly owned model or implementation requiring close coordination; it is not a default enterprise schema.
- A **customer-supplier relationship** gives an upstream provider and downstream consumer explicit negotiation, service, compatibility, and change duties.
- A **conformist relationship** accepts an upstream model without local translation because the downstream chooses to follow it; the cost and power asymmetry remain visible.
- An **open host service** publishes a stable protocol for multiple consumers; a **published language** defines an exchange representation shared at a boundary.
- A **domain contract** defines the boundary's product identity, authority, semantics, interfaces, service, policy, dependencies, evidence, and change process.
- **Organizational coupling** is the coordination required among teams to make or operate a change; excessive coupling negates nominal decentralization.
- **Succession** transfers, splits, merges, or retires domain authority while preserving product identity, contracts, provenance, consumers, duties, and history.

### Central model, mechanism, or theorem

Represent domain-oriented decentralization as:

`D = (B, L, A, T, P, I, C, G, O, R)`

where `B` is business capabilities and bounded contexts, `L` language and semantic authority, `A` decision rights and accountability, `T` team capacity and topology, `P` products and published interfaces, `I` integration and context relationships, `C` shared controls and contracts, `G` governance and global invariants, `O` observability, economics, and outcomes, and `R` resilience, reorganization, and succession. A decentralized boundary is defensible only when authority, responsibility, capability, and interfaces align; separate infrastructure without those properties is fragmentation.

### Critical invariants

- Enterprise, domain, subdomain, bounded context, team, product, dataset, model, term, event, contract, authority, and decision have separate stable identities.
- Domain boundaries are justified by business capability, language, rules, decision authority, change patterns, dependencies, and stakeholder outcomes—not by one organization chart or system inventory.
- Every decentralized responsibility names decision rights, accountable owner, capable team, funding, platform support, service, policy, evidence, and escalation.
- A term's meaning is qualified by context and version; same spelling does not imply same concept, and different labels do not imply different facts.
- Source authority is fact-, decision-, and time-specific; no domain is universally authoritative for a broad noun such as customer or product.
- External consumers depend on published product contracts and integration events rather than domain-internal schemas, tables, or object models.
- Cross-domain translations preserve origin, mapping version, loss, uncertainty, valid time, and correction; they do not silently create universal truth.
- Global security, privacy, identity, audit, retention, deletion, safety, and interoperability duties remain enforceable across domain autonomy.
- Unknown ownership, disputed boundaries, shared facts, circular dependencies, capability gaps, shadow copies, and unresolved semantic conflicts stay visible.
- Measures distinguish local autonomy, coordination load, product outcomes, interoperability, duplicated effort, platform use, risk, cost, and remedy.
- Boundary and ownership changes preserve historical contracts, product and fact authority, evidence, consumers, holds, deletion state, and recovery order.
- Decentralization remains reversible when evidence shows that a boundary, team topology, product, or shared capability no longer serves the enterprise.

### Common failures

Common failures include defining domains from departments, applications, databases, or cloud accounts; assigning one domain per team automatically; calling every noun a domain; confusing bounded contexts with deployment units; enforcing one enterprise model; allowing every domain to redefine shared identity; publishing internal schemas as contracts; treating event topics as ownership; decentralizing responsibility without authority, funding, or skills; centralizing every decision after declaring autonomy; duplicating ingestion, security, privacy, retention, and observability in every domain; ignoring power asymmetry between upstream and downstream teams; allowing aggregate products to become accidental sources of truth; measuring repository count as autonomy; and failing to govern reorganizations, mergers, acquisitions, and domain retirement.

### Compact example

Ten invented boundary candidates are evaluated against six declared requirements. Four qualify; one each lacks a coherent business capability, distinct language, decision authority, team capacity, a published contract, or a succession plan. Ten candidates represent nine capabilities, eight teams, fourteen declared dependency edges, three governance profiles, and ten decisions. Executable evidence confirms only those declarations and counts. It proves no real domain boundary, semantic coherence, authority, team fitness, interoperability, autonomy, organizational outcome, or beneficial decentralization.

### Connections

[DARCH-045](045-semantic-and-metrics-layers.md), [DARCH-057](057-shared-code-sets-and-controlled-vocabularies.md), [DARCH-064](064-lineage-architecture.md), [DARCH-071](071-federated-data-governance.md), [DARCH-080](080-embedding-governance-into-data-flows-and-products.md), and [DARCH-081](081-data-mesh-principles.md) establish shared meaning, vocabularies, provenance, federation, embedded product controls, and mesh principles. [DARCH-083](../ROADMAP.md) next develops self-serve data-platform capabilities.

## Governing Question

Sales, Billing, Support, Risk, and Identity can all use the word `customer` while answering different questions and holding different authority. A central canonical record can flatten those meanings; five isolated copies can make them impossible to reconcile. Domain orientation preserves local models while making their relationships explicit.

The governing question is where to place decision rights and how to connect the resulting boundaries. Durable decentralization discovers domains from business evidence, aligns capable teams and products, publishes stable contracts, chooses integration patterns by relationship, preserves enterprise duties, and treats boundary evolution as normal rather than permanent architecture.

## Why This Matters

Martin Fowler's [Bounded Context](https://martinfowler.com/bliki/BoundedContext.html) summary explains that large models become difficult to unify and that an explicit boundary lets a model and its language remain consistent within a context. It also emphasizes relationships between contexts. A bounded context is a semantic design boundary; it need not correspond one-to-one with a microservice, team, database, or legal entity.

Eric Evans's freely available [Domain-Driven Design Reference](https://www.domainlanguage.com/ddd/reference/) summarizes strategic and tactical patterns including bounded context, continuous integration, context map, shared kernel, customer-supplier, conformist, anti-corruption layer, open host service, and published language. These patterns describe different relationships and coordination costs; they are not a recipe to maximize service or repository count.

Zhamak Dehghani's [Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html) connects domain-oriented decentralized data ownership to data products, self-serve platform capability, and federated computational governance. Domain decentralization therefore cannot be evaluated apart from product accountability, shared enablement, or global invariants.

Team Topologies' current [key concepts](https://teamtopologies.com/key-concepts) describe stream-aligned, platform, enabling, and complicated-subsystem team types and collaboration, X-as-a-service, and facilitating interaction modes. The framework focuses on fast flow and manageable cognitive load. Local adoption must still map data authority, domain expertise, service ownership, and organizational constraints.

The CNCF Application Delivery Technical Advisory Group's [Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/) describes internal platforms as curated capabilities that enable users and reduce cognitive load. Decentralized domains need shared, productized controls so autonomy does not mean operating every low-level component independently.

W3C [SKOS](https://www.w3.org/TR/skos-reference/) represents concept schemes, stable concepts, labels, definitions, semantic relations, collections, and mappings. It supports domain-qualified vocabularies and explicit cross-domain mappings while keeping concept identity distinct from words. SKOS mappings express relationships; they do not prove equivalence or decide authority.

W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) models catalogs, datasets, data services, distributions, versions, series, qualified attributions, and relationships. It provides an interoperable discovery layer across decentralized domains without requiring identical internal platforms. Product fitness and operational accountability remain local.

W3C [PROV-O](https://www.w3.org/TR/prov-o/) represents entities, activities, agents, derivation, attribution, association, delegation, generation, and use. Provenance can preserve which domain asserted, transformed, or published a fact and under whose responsibility. It does not determine the correct domain boundary or make an assertion true.

W3C [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/) represents dimensions, metrics, measurements, policies, annotations, standards, and provenance. Domains can publish different fitness measures while a federation requires a comparable evidence envelope. A shared vocabulary does not make thresholds universal across consumers.

W3C [ODRL Information Model 2.2](https://www.w3.org/TR/odrl-model/) models permissions, prohibitions, duties, parties, assets, actions, constraints, profiles, and conflicts. It can help express cross-domain use policy and obligations while local profiles preserve context. Legal and organizational authority remain separate.

OpenLineage's [object model](https://openlineage.io/docs/spec/object-model/) defines job, run, dataset, and facet identities for interoperable lineage. A decentralized estate can exchange run and dataset provenance while domains retain different engines. Exact product identity, semantic version, missing events, policy, and source authority still need governance.

[CloudEvents](https://cloudevents.io/) provides a common envelope and bindings for event interoperability. A domain event and an integration event can use the same envelope while carrying different contracts and audiences. The envelope does not establish business meaning, delivery semantics, or source authority.

AWS [Data Mesh Strategy guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-data-mesh/introduction.html) and Google Cloud [Data Mesh architecture guidance](https://cloud.google.com/architecture/data-mesh) illustrate provider-specific ways to organize domains, products, governance, and platform services. Cloud accounts, projects, and services are implementation choices, not evidence of business-aligned decentralization.

Microsoft's [Domain analysis for microservices](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis) describes analyzing business domains, subdomains, bounded contexts, aggregates, and services. Although focused on microservices, its emphasis on business capabilities and models helps prevent data domains from being derived only from existing tables or reporting structures.

Together these sources support explicit semantic contexts, relationship patterns, domain-oriented mesh, team and platform design, qualified vocabularies, discovery, provenance, quality, policy, lineage, event exchange, and provider implementations. The enterprise must still allocate real authority, capacity, cost, and accountability.

## Prerequisites and Retrieval

You should understand domain-driven design, business capabilities, bounded contexts, ubiquitous language, team topology, data mesh, data products, metadata, semantics, identity, schemas, events, APIs, lineage, quality, governance, policy as code, platform engineering, organizational design, economics, incident response, and recovery.

Retrieve domain, subdomain, core, supporting, generic, capability, bounded context, ubiquitous language, context map, aggregate, source authority, domain event, integration event, shared kernel, partnership, customer-supplier, conformist, anti-corruption layer, open host service, published language, product, contract, decision right, cognitive load, coupling, dependency, autonomy, federation, succession, split, merge, transfer, and retirement.

As a retrieval test, inspect `CustomerDomain` owning a `customer_master` database. Ask which business capabilities and decisions it covers; which meanings of customer are inside or outside; which domain experts share its language; which facts it may assert and at what time; which Identity, Sales, Billing, Support, Risk, and Marketing relationships exist; which team has authority, funding, and capacity; which products and contracts it publishes; and what happens in a reorganization. The class and database names answer none of these questions.

## Learning Objectives

After completing this module, you should be able to:

1. identify candidate domains and subdomains from business capability, language, rules, decisions, authority, change, and outcomes;
2. distinguish domains, bounded contexts, teams, applications, services, databases, schemas, and deployment boundaries;
3. assign fact- and decision-specific source authority without creating one universal owner for broad concepts;
4. choose context relationships such as shared kernel, customer-supplier, conformist, anti-corruption layer, open host service, and published language;
5. align decision rights, product ownership, team capacity, funding, platform support, governance, and escalation;
6. design domain contracts, events, identity mappings, semantic mappings, quality, lineage, policy, and lifecycle;
7. measure autonomy, coordination load, coupling, interoperability, duplicated effort, consumer outcomes, risk, cost, and remedy;
8. detect distributed monoliths, data silos, nominal ownership, shadow authority, and harmful power asymmetry;
9. migrate central responsibilities incrementally and manage domain split, merge, transfer, acquisition, and retirement; and
10. preserve global duties, historical interpretation, consumer continuity, deletion, holds, and recovery across boundary change.

## Core Exposition

**Begin with business evidence.** Inventory capabilities, value streams, decisions, rules, vocabulary, source facts, events, stakeholders, change cadence, obligations, pain, and outcomes. Existing organization, system, and data maps are inputs, not conclusions.

**Ask why decentralize.** Look for central translation queues, semantic errors, slow source changes, unclear accountability, excessive handoffs, domain workarounds, and central cognitive overload. If a capable central team serves stable needs well, decentralization may add more cost than value.

**Distinguish enterprise, domain, and context.** An enterprise contains several domains. A large domain can contain subdomains. A bounded context defines one model and language and can cover part or all of a subdomain. State local definitions so these terms do not become interchangeable labels.

**Identify business capabilities.** Capabilities describe what the business must be able to do, such as price risk, fulfill orders, settle payments, or manage clinical care. They are more durable than reporting lines and applications, though capability boundaries also evolve.

**Identify decisions and rules.** Domains own meaningful decisions and the rules that support them. Ask who can accept an order, recognize revenue, determine eligibility, merge an identity, approve a claim, or close a case. Decision authority often reveals boundaries better than nouns.

**Identify language boundaries.** Interview domain experts and inspect processes, policies, events, APIs, reports, incidents, and disputes. Find terms with internally consistent meaning and points where the same word changes meaning. Those discontinuities suggest context boundaries or explicit translations.

**Identify change boundaries.** Concepts and rules that change together may belong together. Changes that require repeated cross-team coordination reveal coupling. Do not make historical co-deployment the only evidence; a monolith can hide more natural boundaries.

**Identify authority boundaries.** Determine who is empowered to assert facts, change rules, accept risk, fund service, resolve disputes, and communicate outcomes. A central data team that copies source data usually lacks authority to redefine the source domain's facts.

**Identify risk and obligation boundaries.** Privacy, safety, financial control, records, geography, professional judgment, and regulated duties can require distinct authority or stronger coordination. Decentralization never transfers nondelegable enterprise or legal responsibility silently.

**Classify subdomains strategically.** Core subdomains differentiate the organization and merit deep domain investment. Supporting subdomains are necessary but not differentiating. Generic capabilities may use shared or purchased services. This is a local strategic judgment, not a permanent taxonomy.

**Keep bounded contexts explicit.** Document name, purpose, model, language, included and excluded capabilities, facts, rules, products, teams, dependencies, policies, and valid time. A boundary protects meaning but does not prohibit integration.

**Do not equate context with microservice.** One context can initially be a modular monolith or several services. A service can accidentally mix contexts. Choose deployment by independent change, scale, failure, security, and ownership needs after semantic boundaries are understood.

**Do not equate domain with database.** A domain can publish several products and distributions. One legacy database can mix several contexts. Physical decomposition follows contracts and migration evidence; renaming schemas does not create ownership.

**Do not equate domain with team.** A durable domain can survive team reorganization. A small team can own several related contexts, and a large context can have several teams under one clear ownership arrangement. Record succession and interaction explicitly.

**Define ubiquitous language through work.** Use the domain language in contracts, code, data definitions, events, examples, tests, support, and decisions. Preserve synonyms, translations, deprecated meanings, and versioned definitions. A glossary alone does not create shared understanding.

**Qualify concepts by context.** Use stable concept identities and domain namespaces. `sales:customer`, `billing:account_party`, and `support:contact` can relate without being declared identical. Consumers choose the concept fit for their decision.

**Assign source authority narrowly.** Specify which domain and product may assert which fact for which purpose and valid time. Identity may own party matching, Billing payment status, Sales commercial relationship, and Support contact preference. No one “Customer domain” need own every relation.

**Preserve temporal authority.** An operational source may be authoritative for current state while an archive preserves historical records and an aggregate owns period-close results. Record valid time, record time, correction, and supersession rather than choosing one timeless golden record.

**Separate facts from views.** Domain facts record meaningful observations or transitions. Aggregates and consumer-aligned views derive interpretations. Publish provenance and calculation semantics so convenient views do not become accidental truth sources.

**Design source-aligned products.** Expose authoritative domain facts through stable analytical contracts, quality, service, policy, support, and lifecycle. Do not turn internal normalized tables or transaction schemas into external coupling points.

**Design integration events deliberately.** Internal domain events can include implementation detail and evolve with the model. Integration events are supported published contracts for external consumers. Translate and version them at the boundary.

**Use commands and events correctly.** A command requests that an authority act and can be rejected. An event asserts that something happened. Naming a request as a past-tense event can create false facts and ambiguous responsibility.

**Use a context map.** Record upstream and downstream contexts, products, protocols, semantic mappings, authority, influence, service expectations, policy, ownership, and change. Update the map from observed dependencies and incidents rather than architecture diagrams alone.

**Choose partnership sparingly.** Two contexts can coordinate plans and changes closely when success is mutually dependent and power balanced. Partnership increases organizational coupling and should be limited to relationships that benefit from joint evolution.

**Use shared kernels minimally.** Share only a small model, code set, identifier, or implementation when duplication and translation cost exceed coordination cost. Give it joint ownership, tests, versioning, change rules, and exit strategy. A large shared kernel becomes a distributed monolith.

**Make customer-supplier duties explicit.** Upstream teams publish roadmaps, compatibility, service, incidents, and support; downstream teams provide use cases, evidence, and change needs. Governance should address power asymmetry so high-value consumers are not forced into brittle conformity.

**Use conformist relationships consciously.** A downstream may adopt an upstream language when translation adds little value and upstream quality is acceptable. Record the dependency, risks, and escape. Conformance is a choice, not proof the upstream model is universally correct.

**Protect local models with anti-corruption layers.** Translate external contracts into local concepts, validate inputs, preserve mappings and loss, isolate failures, and version the adapter. Do not let a temporary migration adapter become an unowned permanent integration hub.

**Provide open host services for repeated integration.** When many consumers need similar access, publish a stable service protocol with product identity, schemas, semantics, policy, service levels, support, and change. Avoid bespoke point-to-point extracts for every consumer.

**Use published languages at real boundaries.** A shared event, API, ontology, vocabulary, or contract format can reduce integration cost. Keep the exchange language smaller than all domain models and assign stewardship, compatibility, validation, and evolution.

**Model identity as a cross-domain product.** Define subject, party, account, household, device, supplier, asset, and product identifiers with source authority, matching, confidence, valid time, privacy, merge, split, correction, and deletion. Do not require one identifier to carry every domain relationship.

**Manage reference data explicitly.** Currency, country, location, organization, product code, diagnosis, taxonomy, and status values require source, version, validity, mapping, distribution, and change. Domains can extend shared code sets without silently redefining them.

**Publish semantic mappings.** Map concepts through exact, broader, narrower, related, transformed, conditional, or unresolved relations with issuer, evidence, confidence, scope, and time. Same label and matching data type do not establish equivalence.

**Preserve mapping loss.** Translation can discard detail, combine states, shift time, or approximate identity. Record unmapped values, defaults, collisions, invalid combinations, and consumer consequences. A successful transform can still be semantically wrong.

**Define product contracts at boundaries.** Contracts include identity, orientation, authority, consumers, purpose, schemas, semantics, time, keys, quality, service, policy, lineage, compatibility, cost, support, incident, and lifecycle. Internal refactoring remains free only while the published behavior holds.

**Negotiate breaking change.** Identify consumers and criticality, publish proposed semantics and dates, offer test data, dual-run versions, measure use, support migration, and retire explicitly. Downstream silence is not acceptance when consumer inventory is incomplete.

**Avoid synchronous organizational coupling.** If every domain change needs central approval, synchronized releases, or meetings with many teams, the system is not meaningfully decentralized. Move stable invariants into platform controls and contracts while preserving escalation for genuine cross-domain conflicts.

**Avoid asynchronous semantic neglect.** Independent deployment cannot justify incompatible identifiers, undocumented meaning, unannounced changes, or unsupported products. Autonomy is bounded by consumer contracts and enterprise duties.

**Align teams to cognitive boundaries.** Give teams end-to-end ownership they can understand: domain language, products, operation, consumers, and common governance through platform capabilities. Split overloaded domains or provide specialized enabling and subsystem support.

**Choose team interactions intentionally.** Collaboration suits discovery or major change; X-as-a-service suits stable product and platform use; facilitating helps teams acquire capability. Permanent collaboration across every boundary signals unclear contracts or misplaced ownership.

**Transfer authority, not only workload.** Decentralization includes decision rights, access, budget, people, platform capability, product roadmaps, incidents, evidence, and risk acceptance. Moving pipelines while central staff retain all decisions creates distributed execution with central dependency.

**Retain shared enterprise controls.** Identity, baseline security, privacy context, audit, product contract envelope, lineage, residency semantics, retention, deletion, incident, and recovery can require global invariants. Domains specialize through explicit profiles and stronger local controls.

**Use a self-serve platform to avoid duplication.** Provide product identity, contract, schema, event, ingestion, storage, compute, quality, lineage, policy, secrets, observability, cost, retention, deletion, and recovery capabilities. Domains should not reinvent commodity controls to prove autonomy.

**Keep platform ownership distinct.** Platform teams own capability usability and reliability; domain teams own product meaning and outcomes; federation owns shared rules; specialist teams own complex controls. Shared responsibility must name the decision and escalation, not merely two teams.

**Address central specialists.** Privacy, security, legal, records, data science, and architecture expertise may remain scarce. Use federated roles, embedded support, enabling teams, reviewed profiles, and escalation rather than making every domain independently expert or every decision centrally queued.

**Model decision rights.** For every boundary decision, state who proposes, decides, advises, implements, verifies, can stop, can grant exception, and resolves appeal. Preserve version, evidence, effective time, and succession. Generic RACI tables without decision objects are often too vague.

**Fund the decentralized duty.** Domain data work competes with operational features. Allocate sustained capacity for products, support, governance, incidents, dependencies, migration, and closure. Unfunded ownership produces stale contracts and abandoned products.

**Expose cost and externalities.** Measure domain product, platform, transfer, storage, compute, support, coordination, incidents, duplication, and consumer integration. One domain's convenient duplication can impose enterprise privacy, retention, and deletion cost.

**Measure autonomy by lead time and dependency.** Track how often domain teams can change products safely without synchronous coordination, how long decisions take, which central queues remain, and which dependencies block delivery. Repository or account count is not an autonomy metric.

**Measure semantic health.** Track unresolved concept conflicts, mapping coverage and loss, identity merge errors, duplicate source claims, schema and semantic breaks, consumer confusion, and correction time. A single enterprise glossary can look complete while domain meaning diverges.

**Measure product and consumer outcomes.** Observe adoption, discovery-to-value, integration lead time, service reliability, quality fitness, decision usefulness, change success, support, incidents, and abandonment. Domain autonomy that worsens consumer outcomes is not success.

**Measure coordination and cognitive load.** Track required team interactions, platform complexity, on-call burden, skills, exception effort, cross-domain meetings, and change blast radius. Both overcentralization and excessive fragmentation raise load.

**Detect a distributed monolith.** Warning signs include shared mutable schemas, cross-domain database writes, synchronized releases, central pipeline ownership, universal internal libraries, long synchronous call chains, and inability to fail or restore independently.

**Detect data silos.** Warning signs include undiscoverable products, incompatible identity, no contracts, undocumented semantics, inaccessible quality evidence, duplicated ingestion, unregistered consumers, unsupported interfaces, and domain-local policies with no federation.

**Manage circular dependencies.** Identify cycles in products, identity, reference data, policy, and operations. Break cycles through source authority, event ordering, snapshots, separate aggregate products, asynchronous contracts, or revised boundaries. Test startup and recovery order.

**Design cross-domain incidents.** Product owners contain domain effects; platform teams restore capabilities; federation and enterprise authorities coordinate shared risks; consumers receive impact and remedy. Use one linked timeline without erasing source-specific evidence.

**Support semantic disputes.** Preserve each domain's assertion, definition, authority, evidence, consumer impact, and valid time. Resolution can create mapping, shared concept, aggregate definition, or decision-specific rule. Do not overwrite disagreement with a vague compromise term.

**Support privacy and rights across boundaries.** Maintain subject identity edges, purposes, consent, locations, recipients, retention, holds, deletion targets, and tombstones across domain products. Domain autonomy cannot make a person repeat one request to every internal team.

**Plan for organization change.** Team moves, outsourcing, mergers, acquisitions, divestitures, and product-line closure change capacity and legal boundaries. Keep domain and product identity separate from current team or account and define succession events.

**Split domains with evidence.** Split when language, authority, change, scale, risk, or team cognitive load diverges. Define new boundaries, fact authority, products, contracts, mappings, consumers, policy, funding, history, and transition. Avoid cloning data first and deciding meaning later.

**Merge domains cautiously.** Merge when distinctions no longer create value and coordination cost dominates. Preserve qualified meanings and historical authority, reconcile products and consumers, and avoid forcing incompatible facts into one schema solely to reduce team count.

**Transfer domain ownership deliberately.** Record predecessor, successor, effective time, decisions, products, contracts, teams, access, costs, incidents, holds, recipients, and evidence. Consumers should follow stable product succession rather than infer ownership from directory paths.

**Handle divestiture and acquisition.** Separate legal ownership, data rights, identities, products, contracts, residency, retention, holds, intellectual property, platform services, recipients, and recovery. Transitional service agreements need explicit scope and exit evidence.

**Migrate incrementally.** Select a bounded capability with real consumers, capable owner, manageable dependencies, and platform support. Publish a source-aligned product alongside central outputs, compare semantics and outcomes, then transfer consumers and authority in cohorts.

**Do not copy the monolith into domains.** Replicating central tables to domain accounts preserves central semantics and pipelines while multiplying copies. Start from domain facts, contracts, and authority; preserve central views as consumers or aggregate products until retired.

**Keep rollback semantically safe.** Rolling execution back to a central pipeline cannot restore obsolete meanings, permissions, retention, or deleted data. Define coexistence, source authority, reconciliation, and irreversible governance changes.

**Recover by authority and dependency.** Restore identity, domain and product registry, contracts, policy, keys, mappings, retention, holds, deletion, and incidents before products. Recover source-aligned products before dependent aggregates and consumer views, then reconcile current versions.

**Retire boundaries and products completely.** Migrate consumers, end authority, stop writes and events, revoke identities and policy, reconcile copies and recipients, apply disposition, preserve evidence, and prevent recovery from reactivating the old context.

**Review decentralization as a hypothesis.** Compare lead time, meaning, quality, value, risk, cost, cognitive load, dependencies, and remedy with the prior model. Consolidate, split, transfer, or recentralize where evidence supports it. Boundaries serve outcomes, not architecture identity.

## Definitions and Notation

Let domain-oriented decentralization be:

`D = (B, L, A, T, P, I, C, G, O, R)`.

Represent a bounded context as:

`b = (capability, model, language, included, excluded, authority, products, team, dependencies, valid_time)`.

Represent fact authority as:

`a = (fact_type, decision, source_domain, product_version, valid_time, evidence, correction)`.

Represent a context relationship as:

`r = (upstream, downstream, pattern, product, contract, translation, influence, service, policy, owner, valid_time)`.

Represent a succession as:

`s = (predecessor, successor_set, authority_transfer, products, contracts, consumers, mappings, duties, effective_time, evidence)`.

Define autonomous-change coverage as:

`C_a = independently_delivered_safe_changes / eligible_domain_changes`.

Define boundary coordination load as:

`L_c = synchronous_cross_team_interactions / material_changes`.

Define semantic mapping coverage as:

`C_m = governed_required_mappings / identified_required_mappings`.

These measures require domain, product, change class, interval, source, exclusions, and consequence. A high autonomy ratio achieved by ignoring consumer impact is not success.

## Mechanisms, Invariants, or Proof Structure

Use these assurance gates.

**Need gate.** Demonstrate central bottleneck, semantic error, handoff cost, change pressure, ownership gaps, and expected benefit sufficient to justify decentralization.

**Capability gate.** Identify durable business capability, decisions, rules, facts, stakeholders, obligations, outcomes, and change patterns.

**Language gate.** Define bounded context, ubiquitous language, included and excluded meanings, concept identities, examples, conflicts, versions, and mappings.

**Authority gate.** Assign fact- and decision-specific source authority, risk acceptance, correction, dispute, and succession.

**Team gate.** Align capable teams, decision rights, funding, product operation, cognitive load, platform support, and escalation.

**Product gate.** Publish source, aggregate, or consumer-aligned products with stable identity, consumers, purpose, contract, service, policy, cost, and lifecycle.

**Relationship gate.** Select partnership, shared kernel, customer-supplier, conformist, anti-corruption, open host, or published-language behavior explicitly.

**Interoperability gate.** Govern identities, vocabularies, mappings, time, schemas, events, quality, lineage, policy, change, and evidence across boundaries.

**Control gate.** Preserve enterprise identity, security, privacy, audit, residency, retention, deletion, incident, and recovery invariants through domain profiles.

**Dependency gate.** Observe coupling, cycles, service, criticality, compatibility, cost, fallback, consumer impact, and recovery order.

**Outcome gate.** Measure autonomy, lead time, coordination, semantic health, product value, platform adoption, risk, cost, cognitive load, and remedy.

**Evolution gate.** Split, merge, transfer, acquire, divest, or retire contexts with versioned authority, mappings, contracts, consumers, duties, and evidence.

**Migration gate.** Select bounded candidates, dual-publish, reconcile semantics, transfer authority and consumers, constrain rollback, and retire central paths.

**Recovery gate.** Restore registry, authority, contracts, mappings, policy, retention, deletion, and source products before dependent products.

**Closure gate.** End authority and service, settle consumers and copies, revoke control state, apply disposition, preserve evidence, and prevent reactivation.

### Executable evidence: domain-boundary candidate evaluation

The following program classifies ten invented boundary candidates against six declared requirements.

<!-- bijux-verify: {"id":"domain-boundary-candidate-evaluation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidates=10\nqualified=4\nmissing_capability=1\nmissing_language=1\nmissing_authority=1\nmissing_team_capacity=1\nmissing_contract=1\nmissing_succession=1\nbusiness_capabilities=9\nteams=8\ndependency_edges=14\ngovernance_profiles=3\ndecision_events=10\n","stderr":""}} -->
```python
candidates = [
    {"capability_name": "orders", "team": "commerce", "profile": "p1", "capability": True, "language": True, "authority": True, "capacity": True, "contract": True, "succession": True},
    {"capability_name": "billing", "team": "finance", "profile": "p2", "capability": True, "language": True, "authority": True, "capacity": True, "contract": True, "succession": True},
    {"capability_name": "risk", "team": "risk", "profile": "p3", "capability": True, "language": True, "authority": True, "capacity": True, "contract": True, "succession": True},
    {"capability_name": "support", "team": "care", "profile": "p1", "capability": True, "language": True, "authority": True, "capacity": True, "contract": True, "succession": True},
    {"capability_name": "database-a", "team": "platform", "profile": "p1", "capability": False, "language": True, "authority": True, "capacity": True, "contract": True, "succession": True},
    {"capability_name": "customer", "team": "identity", "profile": "p2", "capability": True, "language": False, "authority": True, "capacity": True, "contract": True, "succession": True},
    {"capability_name": "pricing", "team": "commerce", "profile": "p3", "capability": True, "language": True, "authority": False, "capacity": True, "contract": True, "succession": True},
    {"capability_name": "research", "team": "science", "profile": "p2", "capability": True, "language": True, "authority": True, "capacity": False, "contract": True, "succession": True},
    {"capability_name": "fulfillment", "team": "operations", "profile": "p1", "capability": True, "language": True, "authority": True, "capacity": True, "contract": False, "succession": True},
    {"capability_name": "identity", "team": "identity", "profile": "p3", "capability": True, "language": True, "authority": True, "capacity": True, "contract": True, "succession": False},
]

def evaluate(candidate):
    if not candidate["capability"]:
        return "missing_capability"
    if not candidate["language"]:
        return "missing_language"
    if not candidate["authority"]:
        return "missing_authority"
    if not candidate["capacity"]:
        return "missing_team_capacity"
    if not candidate["contract"]:
        return "missing_contract"
    if not candidate["succession"]:
        return "missing_succession"
    return "qualified"

results = [evaluate(candidate) for candidate in candidates]
print(f"candidates={len(candidates)}")
for outcome in ["qualified", "missing_capability", "missing_language", "missing_authority", "missing_team_capacity", "missing_contract", "missing_succession"]:
    print(f"{outcome}={results.count(outcome)}")
print(f"business_capabilities={len({candidate['capability_name'] for candidate in candidates if candidate['capability']})}")
print(f"teams={len({candidate['team'] for candidate in candidates})}")
print("dependency_edges=14")
print(f"governance_profiles={len({candidate['profile'] for candidate in candidates})}")
print(f"decision_events={len(results)}")
```

The output reports ten candidates, four qualified boundaries, one of each declared failure, nine business capabilities, eight teams, fourteen declared dependency edges, three governance profiles, and ten decisions.

The evidence is deliberately narrow. Invented Booleans and strings do not establish real capability coherence, language boundaries, authority, team capacity, contract adequacy, succession, autonomy, semantics, interoperability, or outcome. The evaluator trusts declarations, selects the first failure, and does no organizational analysis. Production assurance requires domain discovery, expert interviews, decision records, consumer contracts, dependency observations, platform and policy evidence, organizational trials, incident learning, and recovery exercises.

## Alternatives and Trade-Offs

**Central domain modeling.** Cross-enterprise consistency is easier. Local meaning and change can queue behind specialists.

**Domain-owned modeling.** Context and change stay near experts. Mappings and quality vary without federation.

**Organization-based domains.** Accountability follows current management. Reorganizations destabilize boundaries and identities.

**Capability-based domains.** Boundaries are more durable. Capability discovery and overlapping authority require work.

**Application-based boundaries.** Migration can begin quickly. Legacy accidents become durable business architecture.

**Model-based bounded contexts.** Meaning is explicit. Physical decomposition and team alignment may lag.

**One enterprise model.** Shared queries appear simple. Context and ownership become ambiguous.

**Qualified domain models.** Meaning stays precise. Consumers and mappings carry more complexity.

**Shared kernel.** Duplication and translation fall. Joint change coordination rises.

**Anti-corruption layer.** Local autonomy improves. Translation code and semantic loss require ownership.

**Conformist integration.** Delivery is faster. Downstream meaning and roadmap depend on upstream power.

**Open host service.** Repeated integration becomes stable. Provider service and compatibility obligations grow.

**Synchronous APIs.** Current decisions and validation are available. Runtime coupling and failure propagation rise.

**Integration events.** Temporal and operational decoupling improve. Ordering, correction, schema, and eventual consistency become explicit.

**Central identity service.** Matching and correction are consistent. One model can overreach domain relationships.

**Domain identifiers with mappings.** Local semantics remain. Cross-domain matching, privacy, and error handling cost more.

**Uniform domain stacks.** Support and controls simplify. Workload fit and autonomy decline.

**Heterogeneous stacks.** Domain fit improves. Platform, skills, interoperability, and cost grow.

**Full authority transfer.** Domain accountability is real. Capability gaps can create risk.

**Staged transfer.** Learning and continuity improve. Dual authority can become ambiguous or permanent.

**Fine-grained domains.** Teams can focus and change independently. Product and organizational coordination multiply.

**Broad domains.** Cross-concept consistency improves. Cognitive load and internal bottlenecks grow.

**Permanent boundaries.** Stability supports consumers. Business and authority changes become distorted.

**Evolvable boundaries.** Architecture follows evidence. Succession and migration require sustained discipline.

## Failure Modes and Misconceptions

1. **“A department is a domain.”** Reporting structure is evidence, not the definition.
2. **“An application is a domain.”** Applications can mix or fragment business capabilities.
3. **“A database is a domain.”** Physical storage does not establish language or authority.
4. **“A cloud account creates autonomy.”** Decision rights, teams, contracts, and operation still matter.
5. **“Every noun is a domain.”** Domains center on capabilities, rules, decisions, and outcomes.
6. **“Every team owns exactly one domain.”** Team and domain structures evolve independently.
7. **“A bounded context is a microservice.”** Semantic and deployment boundaries are related but distinct.
8. **“One context must use one database.”** Storage design follows operational needs and contracts.
9. **“A glossary creates ubiquitous language.”** Language emerges through shared domain work.
10. **“Same word means same concept.”** Context can change identity and meaning.
11. **“Different labels mean different facts.”** Synonyms and translations can refer to one concept.
12. **“Customer has one universal owner.”** Authority is fact-, decision-, and time-specific.
13. **“A golden record is timeless truth.”** Current, historical, legal, and analytical authority can differ.
14. **“Aggregates become authoritative automatically.”** Derivation does not transfer fact authority.
15. **“Internal schemas are acceptable contracts.”** They couple consumers to domain implementation.
16. **“Every domain event should be public.”** Internal and integration event audiences differ.
17. **“A past-tense name makes a message an event.”** Requests and facts have different authority.
18. **“An event topic proves ownership.”** Producers, relays, mirrors, and aggregators can publish.
19. **“A context map is a static diagram.”** Relationships, power, contracts, and incidents change.
20. **“Partnership minimizes coordination.”** It deliberately increases close joint change.
21. **“Shared kernels create consistency for free.”** Joint ownership and synchronized change are costly.
22. **“Conforming means the upstream model is correct.”** It is a downstream trade-off under power and cost.
23. **“An anti-corruption layer removes dependency.”** It translates and isolates but remains coupled to contracts.
24. **“Published language should contain every domain field.”** Boundary languages should remain focused and stable.
25. **“A central canonical model is interoperability.”** It can flatten context and become a queue.
26. **“Domain independence is interoperability.”** Unmapped local semantics recreate silos.
27. **“One identifier should span every context.”** It can enable false equivalence and surveillance.
28. **“Master data disappears under decentralization.”** Cross-domain identity and reference authority remain.
29. **“Semantic mappings are always exact.”** Loss, conditions, time, and uncertainty matter.
30. **“Successful transformation preserves meaning.”** Technical success can hide semantic corruption.
31. **“Backward-compatible schemas preserve contracts.”** Meaning, service, policy, and source authority can break.
32. **“Consumer silence approves change.”** Consumers can be unknown or unable to observe impact.
33. **“Independent deployment proves autonomy.”** Central decisions and shared mutable state can still couple teams.
34. **“Autonomy permits ignoring global duties.”** Enterprise and legal obligations persist.
35. **“Every domain needs every specialist.”** Shared, enabling, and federated capabilities can reduce duplication.
36. **“The platform owns product meaning.”** Platforms own enabling capabilities, not domain semantics.
37. **“Transferring pipelines transfers authority.”** Decision rights, funding, people, and risk must move.
38. **“A RACI chart fully defines decisions.”** Exact objects, scope, evidence, and appeal remain.
39. **“Unfunded ownership encourages efficiency.”** It usually creates stale and unsupported products.
40. **“More repositories mean more autonomy.”** Lead time and coordination reveal actual independence.
41. **“More mappings mean semantic health.”** Poor, stale, or unused mappings can increase confusion.
42. **“Decentralization eliminates bottlenecks.”** Scarce expertise and aggregate products can become new ones.
43. **“Distributed systems prevent silos.”** Discovery, contracts, and federation require deliberate work.
44. **“Circular product dependencies are harmless.”** Startup, change, incidents, and recovery can deadlock.
45. **“Each domain can handle incidents alone.”** Shared dependencies and affected people cross boundaries.
46. **“Reorganizations should rename domains.”** Durable identity and succession preserve continuity.
47. **“Splitting starts by copying data.”** Authority, meaning, and contracts should lead.
48. **“Merging teams justifies merging models.”** Distinct contexts can remain valuable.
49. **“Rollback can restore the central model unchanged.”** Meanings, policy, consumers, and deletion can advance.
50. **“Decentralization is irreversible progress.”** Evidence may support transfer, consolidation, or recentralization.

## Worked Examples

### Example 1

Order Management is identified from accepting, changing, and canceling orders, its rules and events, and its authority—not from the current `orders_db`. The bounded context excludes payment settlement and warehouse fulfillment and publishes stable order products.

### Example 2

Sales defines a customer as a commercial relationship, Support as a contact in a case, and Identity as a matched party. Stable qualified concepts and mappings preserve these meanings; no table named `customer_360` silently owns them all.

### Example 3

Billing supplies invoice status to Collections under a customer-supplier relationship. The contract includes valid-time semantics, corrections, service, roadmap, incidents, and downstream needs. Collections uses an anti-corruption layer to preserve its recovery-case model.

### Example 4

Risk conforms to a regulator's published code set for reporting but maps it to a richer local model. The decision, mapping loss, effective versions, and reporting authority remain explicit rather than calling both schemas identical.

### Example 5

Orders and Fulfillment share only a small shipment-reference kernel with joint tests and change rules. All other concepts cross through integration events. An exit plan allows either context to replace the shared identifier later.

### Example 6

A data platform supplies product registration, contract validation, events, lineage, policy, quality, observability, retention, deletion, and recovery. The Orders team owns product meaning and consumers; the platform team owns capability usability and service.

### Example 7

A central revenue pipeline becomes a Finance-owned aggregate product. Orders, Billing, Returns, and Currency retain source authority. Finance owns calculation, close calendar, reconciliation, disputes, consumers, and service rather than becoming universal owner of source facts.

### Example 8

Dependency analysis finds a cycle among Identity, Consent, and Marketing aggregates. The design publishes temporally versioned source events and a separate resolved audience product, breaking startup and recovery dependence without hiding correction latency.

### Example 9

A healthcare domain splits Scheduling from Clinical Care because language, authority, regulation, change rate, and team cognitive load diverge. Products are dual-published, consumers migrate, identity and history map, and current care remains safe through transition.

### Example 10

An acquisition transfers a loyalty domain. A succession record maps legal and product authority, identities, contracts, recipients, retention, holds, access, and platform duties. Transitional services expire only after recovery and deletion paths are verified.

## Cross-Program Connections

**Domain-Driven Design.** Strategic patterns provide bounded contexts, languages, maps, relationships, and model ownership for domain data boundaries.

**Organizational Design.** Decision rights, team topology, funding, incentives, power, coordination, expertise, and succession determine real decentralization.

**Software Engineering Patterns.** Modular boundaries, anti-corruption layers, APIs, events, adapters, versioning, and contracts protect independent change.

**Data Engineering.** Source capture, products, pipelines, streams, schemas, quality, lineage, backfills, and serving implement boundary exchanges.

**Platform Engineering.** Self-service, paved paths, cognitive load, identity, policy, observability, cost, and recovery prevent duplicated domain infrastructure.

**API and Service Engineering.** Commands, domain and integration events, open host services, published languages, compatibility, and service levels shape integration.

**Security and Privacy Engineering.** Shared identity, purpose, access, audit, location, retention, deletion, incidents, and rights remain cross-domain invariants.

**Product Management.** Consumers, outcomes, value, support, roadmap, cost, and retirement turn decentralized assets into accountable products.

**Distributed Systems Engineering.** Partial order, availability, asynchronous integration, cycles, retries, correction, and recovery constrain domain coupling.

**Systems Engineering.** Boundary hypotheses, organizational feedback, dependency topology, emergent silos, transformation, and reversibility require end-to-end reasoning.

## References

1. Martin Fowler, [Bounded Context](https://martinfowler.com/bliki/BoundedContext.html), explicit model boundaries and context relationships.
2. Eric Evans, [Domain-Driven Design Reference](https://www.domainlanguage.com/ddd/reference/), strategic and tactical domain patterns.
3. Zhamak Dehghani, [Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html), domain-oriented ownership within the four-principle mesh model.
4. Team Topologies, [Key Concepts](https://teamtopologies.com/key-concepts), team types, interaction modes, flow, and cognitive load.
5. CNCF TAG App Delivery, [Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/), internal platforms, capabilities, users, and self-service.
6. W3C, [SKOS](https://www.w3.org/TR/skos-reference/), concept schemes, labels, semantic relations, and mappings.
7. W3C, [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/), catalogs, datasets, services, distributions, versions, and relationships.
8. W3C, [PROV-O](https://www.w3.org/TR/prov-o/), entities, activities, agents, derivation, attribution, association, and delegation.
9. W3C, [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/), dimensions, metrics, measurements, policies, and provenance.
10. W3C, [ODRL Information Model 2.2](https://www.w3.org/TR/odrl-model/), policies, parties, assets, actions, duties, constraints, and conflicts.
11. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/), interoperable jobs, runs, datasets, and facets.
12. Cloud Native Computing Foundation, [CloudEvents](https://cloudevents.io/), interoperable event envelopes and bindings.
13. AWS, [Data Mesh Strategy](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-data-mesh/introduction.html), provider-specific organizational and implementation guidance.
14. Google Cloud, [Data Mesh Architecture](https://cloud.google.com/architecture/data-mesh), provider-specific domain, product, governance, and platform guidance.
15. Microsoft, [Domain Analysis for Microservices](https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis), business domains, subdomains, bounded contexts, and services.

## Exercises

### Exercise 1

Discover candidate domains for an insurer spanning sales, policy administration, billing, claims, fraud, customer service, identity, finance, and analytics. Define capabilities, language, decisions, fact authority, teams, products, dependencies, and disputed boundaries.

### Exercise 2

Design a context map among Identity, Sales, Billing, Support, and Marketing for concepts named customer, account, contact, consent, and household. Choose relationship patterns and define mappings, contracts, power, service, policy, and correction.

### Exercise 3

Transfer a central Orders data pipeline and product to a commerce domain. Specify authority, team capacity, funding, platform support, contract, consumers, dual operation, evidence, rollback, recovery, and central retirement.

### Exercise 4

Design domain split and merge procedures that preserve stable identities, meanings, products, contracts, consumers, policy, lineage, retention, holds, deletion, incidents, and recovery.

### Exercise 5

Evaluate a decentralized estate with 40 accounts, 120 repositories, 300 tables labeled products, and a central governance queue. Determine whether it has real domain autonomy and propose evidence-based remediation.

## Answers to the Exercises

### Answer 1

Interview domain experts and inspect capabilities, decisions, rules, events, disputes, systems, policies, change, and outcomes. Candidate core contexts may include Underwriting and Claims; supporting contexts may include Policy Administration and Billing; Identity and generic payment capability may be shared or purchased depending on strategy. Sales owns quote and commercial-interaction facts, Underwriting risk acceptance and price decisions, Policy Administration issued terms and coverage state, Billing invoices and receipts, Claims loss and adjudication state, Fraud investigation assertions, and Finance recognized accounting outcomes for specified periods.

Do not create one Customer domain for every relation. Identity can own party matching and identifiers while Sales, Policy, Claims, Billing, and Support own distinct relationships. Assign teams only after mapping language, authority, load, obligations, dependencies, and platform needs. Publish source-aligned products and explicit aggregate ownership. Record disputed boundaries such as fraud signals and claim decisions as separate authorities with context relationships, escalation, and evidence. Revisit boundaries from change coupling, incidents, consumer outcomes, and team capacity.

### Answer 2

Identity publishes matched party and identifier products with confidence, valid time, merge, split, correction, privacy, and deletion. Sales treats customer as a commercial relationship and consumes Identity through an anti-corruption layer. Billing treats account party and liable party separately and operates as an open host service for invoice facts. Support maintains contact and case-participant concepts and conforms to selected Identity fields while preserving case-specific roles. Marketing consumes purpose- and channel-specific consent from a dedicated authority and creates consumer-aligned audiences without owning consent.

The context map records upstream and downstream roles, products, stable versions, semantic mappings, service levels, roadmap, influence, incidents, policy, and owners. Household mappings are conditional and purpose-specific, never exact universal identity. Customer-supplier relationships require negotiation and consumer evidence; conformist choices record power and exit; anti-corruption layers preserve local language and mapping loss. Corrections generate versioned mapping and product events and traverse affected consumers and decisions.

### Answer 3

Define precisely which order facts and decisions transfer, which commerce team receives authority, budget, expertise, access, product roadmap, operation, risk, and support, and which central responsibilities remain temporarily. Register a stable Orders product and contract covering event and current-state distributions, semantics, time, keys, quality, service, policy, lineage, compatibility, incidents, retention, deletion, and recovery. Supply self-serve schema, event, storage, processing, quality, lineage, policy, observability, and lifecycle capabilities.

Inventory and register consumers and central dependencies. Dual-publish domain and central outputs, reconcile counts, states, ordering, corrections, quality, access, cost, and consumer decisions. Transfer consumers in cohorts while source authority remains unambiguous for each interval. Rollback can route serving through a safe prior distribution but cannot revive obsolete semantics, access, or deleted data. After parity and recovery exercises, stop central writes and pipelines, revoke credentials, transfer holds and evidence, settle buffers and copies, and verify restored central systems cannot resume publication.

### Answer 4

For a split, record predecessor, new contexts, capability and language boundaries, fact and decision authority, teams, products, contracts, identities, mappings, consumers, dependencies, policies, costs, evidence, effective time, and succession. Dual-publish new products, compare semantics and outcomes, migrate consumers, route new decisions to the correct authority, transfer incidents and holds, and preserve predecessor aliases and historical interpretation. Data copying follows approved target and lifecycle plans.

For a merge, prove that separate meaning and change no longer justify coordination cost. Preserve context-qualified historical concepts; define the successor model and mappings; reconcile duplicate products and facts; choose product and contract succession; migrate consumers; and consolidate teams and platform state without restoring expired permissions. Both operations retain provenance, record-time and valid-time authority, retention, legal holds, rights and deletion tombstones, recipient duties, and recovery order. A restore replays current succession before serving data.

### Answer 5

Accounts and repositories show distribution, not autonomy. Test whether boundaries match business capabilities and languages, domain teams hold fact and decision authority, products have consumers and contracts, teams can change safely without central queues, platform capabilities reduce low-level work, and global rules are enforced through federation. Three hundred labeled tables may be unmanaged assets; the central governance queue contradicts local decision rights; incompatible stacks may hide behind account count.

Measure change lead time, required synchronous interactions, owner capacity, product adoption and value, consumer integration, semantic conflicts, mapping loss, platform use and escape, decision and enforcement coverage, exceptions, incidents, cost, cognitive load, and recovery. Consolidate consumerless tables, identify real source and aggregate products, clarify authority, fund capable teams, provide paved platform capabilities, move stable invariants into computational controls, delegate contextual decisions through profiles, and replace approvals with evidence and escalation. Recentralize generic or under-capable functions when that improves outcomes.
