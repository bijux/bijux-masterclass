---
module_id: DARCH-060
program: Data Architecture Engineering
level: 2
module_number: 60
title: Designing an MDM Capability Without Centralizing Every Domain
status: complete
last_verified: 2026-09-03
---

# Designing an MDM Capability Without Centralizing Every Domain

## One-Page Review

### Governing question

How can an enterprise provide dependable identity, mastering, reference, hierarchy, governance, and distribution capabilities while preserving domain authority and avoiding a universal operational hub?

### Essential definitions

- A **master-data management capability** is an organizational and technical system for governing, identifying, reconciling, serving, changing, and retiring consequential shared entities and values.
- A **domain authority** owns defined business meanings and source decisions within a bounded domain.
- A **domain master-data product** is a governed interface through which a domain publishes identified, described, supported, and versioned master data for declared consumers.
- A **shared capability** is reusable infrastructure or workflow that domains consume without surrendering semantic or authoring authority.
- The **control plane** carries policy, metadata, ownership, contracts, configuration, assurance, and evidence; it does not necessarily carry master records.
- The **data plane** carries records, identifiers, events, queries, corrections, and projections used in operational or analytical flows.
- An **identity registry** binds source identifiers to enterprise or cross-domain identity assertions while preserving provenance and uncertainty.
- A **match service** produces candidate, score, rationale, and model or rule version; it does not independently decide business truth.
- A **survivorship policy** chooses or derives a value for a declared use from competing assertions using explicit authority, quality, time, and exception rules.
- A **minimal interoperability contract** defines only the stable identifiers, meanings, events, metadata, and obligations needed across a boundary.
- **Registry, consolidation, coexistence, centralized, and hybrid styles** are alternative allocations of storage, authoring, resolution, and distribution responsibility.
- **Federated MDM** centralizes selected cross-domain decisions and reusable mechanisms while leaving domain semantics and authoring with accountable domain owners unless a justified exception says otherwise.

### Central model, mechanism, or theorem

Represent an MDM capability as:

`M = (D, P, S, C, I, X, G, O, E, L)`

where `D` is domain authority, `P` domain data products, `S` shared services, `C` contracts, `I` identity and reference mechanisms, `X` change exchange, `G` governance, `O` operations, `E` evidence and economics, and `L` lifecycle closure. Fit requires every consequential decision to have an accountable owner; shared services to expose bounded contracts without acquiring undeclared authoring rights; each domain to choose a style appropriate to its entities, attributes, consequences, and constraints; and every active consumer to receive versioned, observable, recoverable, and closable service.

### Critical invariants

- Centralize a decision only when coordination, risk, consistency, or economy justifies central authority.
- Domain ownership does not mean domain isolation; shared contracts and enterprise invariants remain mandatory.
- A shared platform owns its service behavior, not the business meaning of every record it transports or matches.
- Enterprise identity is an assertion with provenance and lifecycle, not proof that all source records are identical.
- Match scores, golden records, and consolidated views preserve source assertions and decision rationale.
- No universal enterprise model is required; stable cross-domain contracts can coexist with richer domain models and consumer projections.
- Implementation style is chosen per domain, entity, attribute, relationship, and lifecycle state rather than once for the enterprise.
- Write authority, semantic authority, identity authority, service ownership, risk acceptance, and consumer fitness remain distinguishable.
- Changes are versioned, ordered where required, idempotent, observable, reconcilable, and reversible or compensable.
- Security, privacy, retention, legal, ethical, residency, and licensing constraints follow records, metadata, identifiers, events, caches, and derived products.
- Funding covers product operation, shared capabilities, consumer adoption, correction, migration, and retirement.
- Retirement closes authoring, publication, subscriptions, caches, credentials, contracts, evidence, recovery paths, and surviving obligations.

### Common failures

Common failures include buying a hub before defining decisions; declaring all domains mastered; making the integration team the data owner; forcing one canonical schema on incompatible concepts; assigning one style to every entity; treating a match score as truth; overwriting source assertions; letting shared services write domain data; publishing events without contracts or reconciliation; creating identifiers with no merge or split policy; centralizing stewardship queues; ignoring consumer transformations; measuring loaded records instead of outcomes; funding build but not operation; migrating by big bang; and decommissioning a hub while subscriptions, copies, or authority remain.

### Compact example

Customer, product, and supplier domains publish separate master-data products. Five shared capabilities provide identity, matching, vocabulary, propagation, and metadata services, but none may author domain master records. Each domain has an accountable authority and a supported implementation style. A small executable check reports three authorities, three products, five shared capabilities, zero shared authoring rights, zero unowned decisions, zero unsupported styles, and no universal-model requirement. It verifies only the declared configuration, not production authority, match quality, interoperability, security, adoption, or business value.

### Connections

[DARCH-051](051-master-data-and-golden-records.md) through [DARCH-059](059-governance-of-shared-data.md) supply the identity, quality, style, vocabulary, hierarchy, propagation, and governance mechanisms assembled here. [DARCH-061](../ROADMAP.md) begins metadata architecture. API, platform, distributed-systems, security, privacy, reliability, and organizational-design programs provide complementary delivery disciplines.

## Governing Question

Master data crosses organizational seams precisely because the enterprise needs customer, product, supplier, location, employee, account, asset, and reference concepts to remain intelligible across many decisions. That need does not imply that one team understands every domain, one application should author every value, or one physical database should become the center of all operations.

The governing question is how to select the few decisions that genuinely require enterprise coordination, preserve knowledgeable domain authority for the rest, supply reusable mechanisms at sustainable cost, and prove that cross-domain outcomes remain trustworthy over time.

## Why This Matters

Zhamak Dehghani's original [data mesh principles and logical architecture](https://martinfowler.com/articles/data-mesh-principles.html) joins domain-oriented ownership, data as a product, a self-service platform, and federated computational governance. MDM and data mesh address different problem statements, but the allocation principle is useful: scale depends on distributing contextual ownership while automating shared interoperability and policy.

IBM's [comparison of virtual, physical, and hybrid MDM capabilities](https://www.ibm.com/docs/en/imdm/11.6.0?topic=technologies-virtual-physical-hybrid-mdm) distinguishes distributed source authoring with central indexing, central physical mastering, and combinations of both. These are allocation choices, not maturity levels. A registry can be correct under source-authority or regulatory constraints; a central physical master can be correct when one transactional authority is legitimate.

AWS [data mesh guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-data-mesh/introduction.html) identifies domain ownership, data as a product, self-service platform, and federated governance, and warns that a central data team becomes a bottleneck as producers and consumers grow. Google Cloud's [data mesh architecture and functions](https://docs.cloud.google.com/architecture/data-mesh) similarly describes domain teams exposing products through defined interfaces while central services support policy, access, catalog, discovery, and platform functions. Vendor implementations are examples, not universal prescriptions.

The [CloudEvents 1.0.2 specification](https://github.com/cloudevents/spec/blob/ce@v1.0.2/cloudevents/spec.md) supplies a common event envelope that can improve interoperability without standardizing every domain payload. W3C [SKOS](https://www.w3.org/TR/skos-reference/) supports concept schemes, labels, semantic relations, and mappings; W3C [PROV-O](https://www.w3.org/TR/2013/REC-prov-o-20130430/) supports provenance about entities, activities, and agents; and the W3C [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/) supports explicit measurements and annotations. Each still requires a governed profile and local operational design.

The UK government's [Data Ownership Model](https://www.gov.uk/government/publications/data-ownership-in-government/data-ownership-model) frames ownership as lifecycle accountability and distinguishes owners, stewards, and custodians. NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy systems as a lifecycle engineering concern. Together these sources support an MDM capability that is organizational, semantic, technical, economic, and operational—not merely a repository.

## Prerequisites and Retrieval

You should understand domain boundaries, systems of record, master and reference data, identity resolution, matching, survivorship, quality, metadata, lineage, data products, contracts, APIs, events, distributed consistency, access control, privacy, security, reliability, governance, organizational design, economics, migration, and retirement.

Retrieve domain authority, semantic authority, source authority, write authority, identity authority, product owner, platform owner, consumer owner, risk owner, control plane, data plane, registry, consolidation, coexistence, centralized style, hybrid style, identity crosswalk, match candidate, survivorship, golden record, projection, concept scheme, hierarchy, provenance, quality evidence, contract, event, reconciliation, exception, service objective, criticality tier, migration, and closure.

As a retrieval test, inspect “the enterprise MDM hub owns customer.” Ask which customer concept, which attributes, which source transactions, which identifiers, which jurisdictions, which uses, which legal roles, which domain owner, which consumers, and which lifecycle decisions are meant. Then ask whether “owns” means semantic authority, write authority, hosting, service operation, risk acceptance, or accountability. The statement is not actionable until those distinctions are explicit.

## Learning Objectives

After completing this module, you should be able to:

1. frame MDM as a portfolio of governed capabilities rather than a mandatory central hub;
2. allocate semantic, source, identity, product, platform, consumer, control, and risk authority;
3. separate control-plane coordination from data-plane storage and movement;
4. choose registry, consolidation, coexistence, centralized, or hybrid styles per bounded need;
5. design domain master-data products and minimal interoperability contracts;
6. provide reusable identity, matching, vocabulary, hierarchy, metadata, quality, and propagation services without capturing domain authoring;
7. govern cross-domain changes, reconciliation, security, privacy, reliability, and recovery;
8. fund and measure domain products, shared capabilities, and consumer adoption as one operating system;
9. migrate incrementally from consequential decisions and thin vertical slices; and
10. retire obsolete authorities, products, services, contracts, and copies safely.

## Core Exposition

**Begin with consequential decisions.** Inventory business and mission decisions that fail when shared identities, classifications, hierarchies, or attributes disagree.

Examples include sanctions screening, patient safety, order fulfillment, supplier payment, product labeling, regulatory reporting, entitlement, asset maintenance, and emergency response. Rank consequence, dependency fan-out, change rate, sensitivity, and recoverability before selecting technology.

**Do not declare an enterprise-wide MDM scope by default.** Mastering is justified when coordinated identity or semantics materially improves a named outcome.

A local lookup used by one application may need ordinary application ownership. Conversely, one critical routing code used by two safety systems may deserve strict enterprise governance despite its small size.

**Define bounded domains.** A domain boundary groups business capabilities, vocabulary, rules, state transitions, expertise, and accountability.

Do not draw domains only from database ownership or the organization chart. Organizations change; semantic and operational responsibilities need durable descriptions and explicit succession.

**Separate domain authority from domain implementation.** A domain authority decides business meaning, authoritative sources, admissible states, correction rules, and acceptable representations.

It may delegate engineering and stewardship. Outsourcing storage, matching, or publication does not transfer that authority unless a formal governance decision says so.

**Inventory decision rights.** For each entity and attribute, name who may define, identify, create, amend, merge, split, classify, relate, approve, publish, consume, restrict, retain, and retire.

Also name who may challenge, arbitrate, accept risk, and verify evidence. “The MDM team” is not enough because those decisions require different expertise and legitimacy.

**Design a capability map before a product map.** Required capabilities usually include ownership, modeling, identity, matching, survivorship, stewardship, reference data, hierarchy, metadata, lineage, quality, contracts, access, change propagation, reconciliation, observation, support, recovery, and lifecycle closure.

Some belong within domains, some are shared, and some are enterprise governance functions. Map responsibility and contract for each instead of assuming one vendor suite should own all of them.

**Distinguish the control plane.** The MDM control plane records owners, policies, schemas, mappings, match configurations, survivorship rules, quality thresholds, contracts, subscriptions, access conditions, exceptions, evidence, and lifecycle state.

Central visibility can improve coordination without centralizing record authoring. The control plane itself needs availability, authorization, versioning, audit, and recovery guarantees.

**Distinguish the data plane.** The data plane handles identifiers, source assertions, resolved views, reference values, hierarchy edges, commands, events, queries, snapshots, corrections, and acknowledgments.

Data can remain in domain stores, move through a shared service, or be consolidated selectively. Control-plane policy must be enforced and evidenced in every relevant data-plane path.

**Create domain master-data products.** A domain product exposes bounded entities or values through supported interfaces and declares meaning, identifiers, schema, provenance, quality, freshness, availability, history, change policy, protection, support, and retirement.

It is more than a dataset. It includes accountable service, documentation, evidence, feedback, and consumer obligations.

**Publish authority, not merely availability.** A product contract states which attributes are authoritative for which purposes and time intervals.

A source can author postal address while a validation service supplies a normalized projection. Neither should silently replace the other, and consumers need to know which representation supports their decision.

**Use minimal interoperability contracts.** Standardize stable cross-domain needs such as identifiers, timestamps, provenance, event type, version, correction semantics, and a few shared concepts.

Keep rich domain details behind domain-owned schemas and publish purpose-specific projections. A universal schema accumulates optional fields, ambiguous compromises, central approval queues, and synchronized release risk.

**Treat mappings as governed assets.** When customer, party, account holder, patient, citizen, and employee overlap, record exact relationships rather than pretending the concepts are identical.

Mappings state source and target versions, direction, transformation, information loss, confidence, owner, validation evidence, effective time, and retirement. A mapping can be asymmetric or intentionally incomplete.

**Provide an identity registry where cross-domain identity matters.** The registry binds source identifiers and identity assertions to stable enterprise identifiers or equivalence groups.

It preserves provenance, rule or model version, evidence, confidence, status, and merge or split history. It does not erase source keys or force every source to use the enterprise identifier internally.

**Separate identification from authorization.** Knowing that two records likely concern the same person does not permit combining, exposing, or using their attributes.

Privacy, purpose, consent, confidentiality, competition, localization, and professional-secrecy rules can prohibit a technically possible join. Identity services enforce or expose relevant policy decisions rather than imply permission.

**Offer matching as a service with bounded authority.** A reusable service can normalize inputs, generate candidates, score comparisons, explain contributing features, and route ambiguous cases.

The domain defines acceptable evidence, thresholds, protected attributes, false-positive and false-negative consequences, review authority, and correction. The platform owns deterministic execution and service quality.

**Keep match assertions revisable.** Store the inputs, time, configuration, score, rationale, reviewer, and downstream activations associated with a resolution decision.

When a false merge is found, split the identity, repair affected products, notify consumers, reassess decisions, and retain correction evidence. An overwritten crosswalk makes safe repair impossible.

**Make survivorship attribute-specific.** One source rarely wins every attribute. A rule may select legal name from a regulated onboarding system, delivery address from recent successful fulfillment, and classification from a domain authority.

Define source precedence, validation, recency, completeness, confidence, exception, tie, manual review, temporal applicability, and provenance. Never reduce survivorship to “latest wins” without business justification.

**Choose registry style deliberately.** Registry keeps source systems authoritative and stores enough centrally to identify or assemble a view.

It minimizes disruption and supports constraints against central authoring, but availability can depend on sources, dynamic assembly may be slow, and correction remains distributed. Cache and projection behavior must be governed.

**Choose consolidation style deliberately.** Consolidation copies source data into a physical mastered view, usually for downstream use, while authoring remains in source systems.

It can simplify analytics and distribution but introduces lag, conflict resolution, duplicate storage, privacy scope, and feedback obligations. Consumers must not mistake the consolidated copy for transactional write authority.

**Choose coexistence deliberately.** Coexistence maintains a central mastered representation and synchronizes relevant changes with distributed authoring systems.

It supports gradual change but creates dual-write semantics, loop prevention, ordering, conflict, reconciliation, and recovery complexity. Attribute-level authority and propagation direction must be explicit.

**Choose centralized transactional mastering selectively.** Central authoring can be correct for enterprise-controlled identifiers, legal entities, shared product definitions, or reference values when one legitimate authority and service boundary exist.

It increases consistency but also concentrates availability, release, organizational, and migration risk. It should not absorb domain processes solely because the platform can store their fields.

**Use hybrid allocation.** An enterprise may use registry for customer identity, consolidation for supplier analytics, centralized authoring for country codes, and coexistence for product classification.

The choice can vary within a domain: identity attributes may be registered, regulated status centralized, and contact preferences remain in interaction domains. Record the rationale and reevaluate it as constraints change.

**Centralize enterprise identifiers carefully.** Define namespace, creation authority, uniqueness boundary, collision policy, immutability, aliasing, merge, split, redirect, reuse prohibition, exposure, and retirement.

An enterprise identifier should remain opaque unless encoded meaning is stable and governed. Consumers must handle redirects and splits rather than assuming identity history is monotonic.

**Share reference-data capabilities.** A reference service can manage concept schemes, code lists, mappings, versions, effective intervals, deprecations, translations, and distribution.

Concept authorities retain semantic decisions. Domains may maintain distinct schemes and publish mappings where interoperability is required instead of flattening all vocabularies into one list.

**Share hierarchy mechanisms without sharing every hierarchy.** A service can store versioned nodes, edges, relationship types, effective intervals, provenance, validation rules, and projections.

Domain authorities decide whether a hierarchy represents legal ownership, management, geography, product assortment, risk aggregation, or navigation. These relationships cannot be combined indiscriminately.

**Build metadata and lineage into publication.** Every product and shared capability registers owner, purpose, schema, identifiers, authority, provenance, quality evidence, protection, dependencies, contracts, operations, and lifecycle state.

Automate technical metadata collection where possible, but require accountable semantic review. A full catalog with incorrect authority is more dangerous than an incomplete catalog that exposes uncertainty.

**Express quality by use.** Measure completeness, validity, consistency, uniqueness, timeliness, accuracy proxies, and stability for declared populations, intervals, and consumer decisions.

Producers supply measurements and limitations; consumer owners decide fitness for their use. Shared platforms compute consistently but do not declare universal fitness.

**Design change contracts.** Every breaking or consequential change has identity, producer, version, effective time, compatibility class, affected fields, reason, impact, migration path, support window, and rollback or compensation plan.

Consumers register dependencies and acknowledge activation. Emergency changes follow bounded authority and retrospective review rather than bypassing evidence.

**Use interoperable event envelopes.** A common envelope can carry event identifier, source, type, subject, time, data-content type, schema reference, and extension attributes.

Domain payloads remain domain-owned. Define idempotency, ordering scope, duplicate handling, replay, tombstone, correction, authorization, and retention beyond the envelope standard.

**Separate notification from state transfer.** A small event can announce a version, while consumers retrieve an authorized snapshot or delta from the product.

This reduces sensitive payload spread and supports late subscribers, but it creates a dependency on retrieval availability and version retention. Select event-carried state only when its security and replay semantics are justified.

**Make reconciliation first-class.** Compare authoritative source counts, identifiers, versions, checksums, events, materialized views, acknowledgments, and consumer activations.

Define tolerance, detection interval, owner, remediation, replay, quarantine, and escalation. Delivery success does not prove application, and application does not prove correct interpretation.

**Prevent propagation loops.** Coexistence flows label origin, authority, mutation identifier, version, and hop or lineage context.

A receiving system distinguishes a domain-authored change from a reflected master update. Idempotency keys and provenance prevent the same correction from cycling indefinitely.

**Design for partition and recovery.** State which reads and writes remain safe when registry, matching, vocabulary, metadata, or event capabilities are unavailable.

Critical consumers may use bounded stale data with visible status; high-risk writes may fail closed. Recovery tests rebuild crosswalks, views, subscriptions, offsets, policy state, and evidence in a known order.

**Apply security and privacy by boundary.** Classify direct identifiers, quasi-identifiers, sensitive attributes, relationship edges, match features, lineage, and stewardship notes.

Use least privilege, purpose limitation, field and row controls, encryption, separation of duties, logging, retention, deletion, and monitored exports. An identity graph can be more sensitive than any one source.

**Limit shared service inputs.** A match service should receive only fields justified for the configured decision and should not retain raw inputs indefinitely by convenience.

Test discriminatory error across relevant populations where lawful and feasible. Document features that are prohibited, unavailable, or unreliable and provide correction and contestability paths.

**Keep consumer responsibility explicit.** Consumers register purpose, product and version, local mapping, transformations, caches, derived products, decision owner, protection, quality thresholds, incident contact, adoption window, retention, and exit plan.

The producer cannot guarantee fitness for an undisclosed use. A consumer that copies data becomes accountable for that copy and its derived decisions.

**Define service ownership.** Domain product owners manage roadmap, documentation, support, quality evidence, compatibility, incidents, and retirement for their product.

Shared capability owners manage availability, latency, capacity, isolation, security, configuration safety, observability, recovery, support, and cost. Neither role inherits the other's semantic decisions.

**Use criticality tiers.** Tier by harm, rights, legal obligation, operational dependency, financial exposure, fan-out, change rate, and recoverability.

Higher tiers can require independent change approval, stronger provenance, lower propagation lag, tighter recovery objectives, dual control, representative quality tests, and verified consumer activation. Avoid making all products carry maximum ceremony.

**Govern exceptions.** An exception names requirement, rationale, scope, affected decisions and people, risk owner, controls, evidence, start, expiry, remediation owner, and closure test.

An MDM office cannot accept operational, privacy, financial, or safety risk merely because it administers the workflow. Repeated renewal triggers architecture or funding review.

**Fund the capability portfolio.** Budget domain product ownership, shared services, stewardship, assurance, consumer migration, incident repair, recovery tests, and retirement.

Central funding can support enterprise invariants and public-good capabilities. Usage allocation can reveal demand, but pure chargeback can discourage metadata, correction, and low-volume critical consumers.

**Measure outcomes and flow.** Track duplicate-related decision harm, correction time, match precision and recall by relevant segment, unresolved ambiguity, propagation lag, reconciliation failure, contract adoption, consumer activation, service reliability, and retirement closure.

Also track lead time to onboard a domain or consumer, platform reuse, exception age, cost per supported product, and manual stewardship burden. Golden-record count and catalog coverage are activity or inventory measures, not value.

**Start with a thin vertical slice.** Choose one consequential decision, one bounded entity, a few attributes, two or three authorities, and named consumers.

Deliver identity, product contract, policy, propagation, reconciliation, quality evidence, support, and correction end to end. A broad ingestion program without consumer activation only creates a larger unresolved repository.

**Sequence by dependency and reversibility.** Establish ownership and contracts before moving write authority. Introduce read-only registry or consolidated views before coexistence where this reduces risk.

Use shadow matching, parallel outputs, sampled review, and bounded cohorts. Every migration gate states evidence, accountable approval, fallback, and consumer repair procedure.

**Preserve source and decision history during migration.** Record old and new identifiers, mappings, match decisions, value provenance, transformation, effective times, consumer versions, and exceptions.

Do not overwrite history to make the new system appear clean. Historical explainability is necessary for correction, audit, disputes, and rollback.

**Retire authority explicitly.** A source ceases authoring only after governance transfers its decisions, workflows, data, histories, controls, support, and legal duties.

Disable writes, rotate credentials, close outbound feeds, reconcile final state, notify consumers, retain or delete evidence properly, test restoration boundaries, and remove obsolete ownership entries.

**Retire shared capabilities safely.** Inventory domain products, configurations, subscriptions, client libraries, cached identifiers, dashboards, runbooks, backups, contracts, and funding dependencies.

Migrate or close every dependency, preserve required provenance and redirect behavior, and verify that disaster recovery cannot resurrect an unauthorized master. A powered-off server is not a completed retirement.

## Definitions and Notation

Let:

- `D` be the set of bounded domains;
- `A` be the set of consequential decision classes;
- `P` be the set of domain master-data products;
- `S` be the set of shared capabilities;
- `R` be the set of accountable roles;
- `C` be the set of versioned interoperability contracts;
- `Q` be the set of declared consumer uses;
- `V` be the set of versions and effective intervals;
- `E` be the set of evidence records; and
- `L` be the set of lifecycle obligations and dependencies.

Define accountable coverage:

`Owned(A) = forall a in A, exists! r in R : accountable(r, a) and authorized(r, a)`

The uniqueness symbol applies to accountability for a decision boundary, not to participation or execution. The same person may own several decisions, and several people may advise or execute one decision.

For a shared capability `s`, define authority safety:

`Bounded(s) = declared_contract(s) and service_owner(s) and not undeclared_domain_authoring(s)`

A shared capability can legitimately author enterprise identifiers or reference values if that write authority is explicitly declared and governed. The invariant prohibits accidental authority, not every central write.

For product `p` and consumer use `q`, define consumability:

`Consumable(p, q) = contract(p, q) and authorized(q) and quality_evidence(p, q) and compatible_version(p, q) and supported(p) and exit_defined(p, q)`

This predicate expresses required architecture evidence. It is not proof that a particular use is lawful, ethical, safe, or beneficial.

For change `x`, define convergent exchange:

`Convergent(x) = identified(x) and versioned(x) and provenance(x) and idempotent(x) and observable(x) and reconcilable(x) and repairable(x)`

Ordering is added when semantics require it. Some independent changes commute; others require entity, partition, or global ordering.

For an implementation-style choice `y`, define fitness:

`StyleFit(y) = authority_aligned(y) and consequence_proportionate(y) and constraints_satisfied(y) and operationally_supported(y) and reversible_or_compensable(y)`

No implication says registry is less mature than centralized or that physical storage is more governed than virtual assembly.

The overall assurance predicate is:

`FitMDM = Scoped and Owned(A) and all(Bounded(s) for s in S) and Products and Identity and Contracts and Quality and Propagation and Reconciliation and Protected and Operable and Funded and Adaptive and Closable`

Each term requires evidence for the declared scope. `FitMDM` is a review structure, not a mathematical proof of organizational success.

## Mechanisms, Invariants, or Proof Structure

**Scope gate.** Name decisions, entities, attributes, relationships, populations, authorities, consumers, consequences, jurisdictions, and lifecycle obligations. Reject “all enterprise data” as an unevaluated scope.

**Authority gate.** For every definition, identifier, source, match, survivor, code, hierarchy edge, correction, access, retention, and retirement decision, identify one accountable and authorized owner plus consultation, challenge, and escalation.

**Allocation gate.** Decide which mechanisms remain domain-local, which become shared services, and which decisions require enterprise authority. Record why coordination value exceeds concentration cost.

**Style gate.** Select registry, consolidation, coexistence, centralized, or hybrid arrangements per bounded entity or attribute. Validate source constraints, latency, write authority, conflict handling, repair, and exit.

**Product gate.** Require each domain product to declare semantics, authority, identifiers, schemas, interfaces, versions, quality, provenance, protection, service, support, cost, change, and retirement.

**Shared-service gate.** Require a clear contract, tenant isolation, configuration ownership, service objectives, evidence, recovery, portability, and prohibition on undeclared domain authoring.

**Identity gate.** Preserve source keys, match evidence, ambiguity, confidence, merge and split history, redirects, correction, and downstream activation. Do not let an identity assertion imply access permission.

**Semantic gate.** Govern vocabularies, hierarchies, mappings, translations, temporal validity, information loss, and concept authority. Avoid universal equivalence claims.

**Contract gate.** Version payload and behavior; define compatibility, consumer obligations, effective time, deprecation, support window, failure semantics, and exit. Test producer and consumer expectations independently.

**Propagation gate.** Specify origin, identity, version, ordering scope, idempotency, replay, duplicate handling, authorization, acknowledgment, correction, and tombstone behavior.

**Reconciliation gate.** Compare source authority, product state, shared views, event logs, acknowledgments, and active consumer versions. Route variance to an owner and retain repair evidence.

**Protection gate.** Apply purpose, minimization, access, encryption, separation, residency, retention, deletion, legal, ethical, and licensing controls to data and metadata across every copy and service.

**Operational gate.** Set availability, latency, freshness, capacity, support, observability, incident, continuity, recovery, and degradation expectations. Test failure of central capabilities before they become enterprise dependencies.

**Economic gate.** Fund product and platform ownership, consumer adoption, stewardship, assurance, repair, migration, and closure. Measure value and cost with declared denominators.

**Change gate.** Use thin slices, shadow evidence, cohorts, compatibility windows, consumer activation, rollback or compensation, and accountable promotion decisions.

**Lifecycle gate.** Close authority, writes, feeds, subscriptions, caches, access, contracts, evidence, recovery, funding, and surviving legal duties. Verify non-resurrection.

### Executable evidence: federated-mdm-capability-boundaries

The following Python program checks a deliberately small capability allocation. It demonstrates that three domain products have named authorities and supported styles, five shared capabilities have service owners but no permission to author domain masters, selected decision classes are owned, and no universal data model is required.

<!-- bijux-verify: {"id":"federated-mdm-capability-boundaries","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"domain_authorities=3\ndomain_products=3\nshared_capabilities=5\nshared_authoring_rights=0\nunowned_decisions=0\nunsupported_styles=0\nuniversal_model_required=false\n","stderr":""}} -->
```python
domains = {
    "customer": {"authority": "customer_domain", "style": "registry"},
    "product": {"authority": "product_domain", "style": "coexistence"},
    "supplier": {"authority": "supplier_domain", "style": "consolidation"},
}

products = {
    name: {"owner": item["authority"], "contract": f"{name}.master.v1"}
    for name, item in domains.items()
}

shared = {
    "identity_registry": {"owner": "identity_platform", "may_author_master": False},
    "matching_service": {"owner": "identity_platform", "may_author_master": False},
    "vocabulary_service": {"owner": "semantic_platform", "may_author_master": False},
    "propagation_service": {"owner": "integration_platform", "may_author_master": False},
    "metadata_service": {"owner": "metadata_platform", "may_author_master": False},
}

decisions = {
    "customer_identity_policy": "customer_domain",
    "product_classification": "product_domain",
    "supplier_survivorship": "supplier_domain",
    "cross_domain_identifier_namespace": "enterprise_data_owner",
    "shared_service_recovery": "platform_risk_owner",
}

supported_styles = {"registry", "consolidation", "coexistence", "centralized", "hybrid"}
shared_authoring_rights = sum(item["may_author_master"] for item in shared.values())
unowned_decisions = sum(not owner for owner in decisions.values())
unsupported_styles = sum(item["style"] not in supported_styles for item in domains.values())
universal_model_required = False

assert all(products[name]["owner"] == domains[name]["authority"] for name in domains)
assert all(item["owner"] for item in shared.values())

print(f"domain_authorities={len(domains)}")
print(f"domain_products={len(products)}")
print(f"shared_capabilities={len(shared)}")
print(f"shared_authoring_rights={shared_authoring_rights}")
print(f"unowned_decisions={unowned_decisions}")
print(f"unsupported_styles={unsupported_styles}")
print(f"universal_model_required={str(universal_model_required).lower()}")
```

The expected output reports `domain_authorities=3`, `domain_products=3`, `shared_capabilities=5`, `shared_authoring_rights=0`, `unowned_decisions=0`, `unsupported_styles=0`, and `universal_model_required=false` on separate lines.

The evidence is intentionally narrow. String-valued owners do not prove that real people have authority, competence, capacity, or budget. A supported style label does not prove the allocation is suitable. The program does not test schemas, semantic compatibility, match quality, survivorship, propagation, reconciliation, security, privacy, reliability, recovery, economics, consumer activation, or lifecycle closure. Production assurance requires representative records, stakeholder decisions, contract and failure tests, operational observations, correction exercises, legal and ethical analysis, and accountable approval.

## Alternatives and Trade-Offs

**Single central transactional hub.** This can provide one write path, strong normalization, consistent workflow, and simple downstream discovery. It also concentrates outage and change risk, demands enterprise-wide migration, and can detach semantics from domains. Use it for genuinely central authority, not as the default organizational answer.

**Virtual registry.** This preserves source authority and can integrate domains incrementally. It depends on trustworthy source access, match behavior, dynamic assembly, and distributed correction. It is suitable where central copying or authoring is constrained, but it is not operationally free.

**Consolidated master view.** This gives consumers a stable physical representation without moving transactional writes. It improves query and distribution performance while adding synchronization lag, storage, retention, reconciliation, and feedback complexity.

**Coexistence.** This supports staged modernization and centrally enriched values while sources continue some authoring. It demands exact attribute authority, loop prevention, conflict policy, versioning, and recovery across multiple writable representations.

**Domain-only autonomy.** This maximizes contextual speed and minimizes central dependency. Without common identity, contracts, policy, metadata, and arbitration, it externalizes integration cost to every consumer and permits incompatible high-risk decisions.

**Federated capability portfolio.** This combines domain products with shared identity, semantic, metadata, propagation, and governance mechanisms. It balances scale and consistency but requires mature ownership, product management, platform design, funding, and cross-domain conflict resolution.

**Universal canonical model.** One model can reduce transformation for stable shared concepts. Across diverse domains it often becomes ambiguous, sparse, slow to change, and politically governed. Prefer a small stable kernel plus explicit mappings and purpose-specific projections.

**Pairwise mappings.** These preserve local semantics and allow gradual adoption. Mapping count can grow rapidly and contradictions emerge. Govern high-value mappings centrally or generate them through a shared semantic service while leaving concept ownership explicit.

**Synchronous query.** It offers current assembled data and avoids broad replication. It couples availability and latency to sources and central resolution services. Use timeouts, degraded modes, caching policy, and explicit failure behavior.

**Event and snapshot distribution.** It decouples producers and supports many consumers. It adds duplicate, order, replay, lag, retention, schema evolution, and reconciliation concerns. Provide both current-state retrieval and replay evidence where consequences warrant them.

**Central funding.** It supports common goods and small critical consumers but can hide cost and weaken demand signals. Transparent service costs and portfolio review preserve accountability without penalizing every use.

**Chargeback.** It can expose consumption and fund capacity, but domains may avoid shared services, metadata, or correction to reduce local cost. Allocate enterprise invariants separately and price marginal demand carefully.

## Failure Modes and Misconceptions

1. **“MDM means one database.”** MDM is a governed capability system; storage is one allocation decision.
2. **“Federated means optional standards.”** Federation delegates within common invariants, contracts, and escalation.
3. **“The platform owns hosted data.”** Hosting creates custody and service duties, not automatic semantic authority.
4. **“A golden record is objective truth.”** It is a purpose-, time-, evidence-, and policy-bounded representation.
5. **“The highest match score wins.”** Thresholds require consequence analysis, calibration, review, and correction.
6. **“One source is best.”** Authority and fitness vary by attribute, purpose, population, and time.
7. **“Latest wins is neutral.”** Recency can select an unauthorized, invalid, or delayed assertion.
8. **“Enterprise ID proves equivalence.”** Identity bindings are governed assertions that can be revised or split.
9. **“Identity permits joining.”** Authorization, purpose, privacy, confidentiality, and ethics remain separate.
10. **“One canonical model removes mappings.”** It often hides mappings inside ambiguous optional fields and consumer logic.
11. **“Events guarantee convergence.”** Delivery needs application, ordering, idempotency, reconciliation, and repair evidence.
12. **“Coexistence is an easy transition.”** Multiple write paths are an enduring distributed-systems design unless explicitly retired.
13. **“A catalog supplies governance.”** Metadata supports decisions; it does not create authority or control effectiveness.
14. **“Domains can self-serve every concern.”** Shared platforms reduce duplicated engineering for common policy and reliability needs.
15. **“Central review improves all risk.”** Low-risk queues can delay correction and hide accountability; use consequence-based tiers.
16. **“Loading more records shows success.”** Outcomes, adoption, correction, convergence, reliability, and closure matter.
17. **“The project ends at go-live.”** Products and platforms require durable operation, funding, assurance, migration, and retirement.
18. **“Turning off the hub completes retirement.”** Authority, feeds, consumers, copies, contracts, evidence, and recovery must close.

## Worked Examples

### Example 1

A retailer needs a cross-channel customer view but each regional commerce system remains legally and operationally responsible for customer updates. It adopts a registry that preserves regional identifiers, stores match evidence and enterprise aliases, and offers an authorized read view. Regional owners handle corrections; the shared identity team operates matching and recovery. A false merge triggers a split, consumer notification, and repair of loyalty decisions rather than a silent row edit.

### Example 2

A manufacturer centralizes creation of global product identifiers and regulated classification because these are legitimate enterprise decisions. Engineering specifications remain authored in product-line domains, while market descriptions remain local. Product products publish a small identifier and classification contract plus richer projections. This is centralized for selected attributes and federated for the domain as a whole.

### Example 3

A hospital network cannot move all clinical source records into a central master. It uses a virtual patient registry with carefully selected match features and purpose-specific access. Possible matches go to authorized clinical identity stewards; clinical facts remain in source systems. The architecture separately evaluates whether a particular care team may retrieve facts after identity resolution.

### Example 4

A supplier capability consolidates legal name, tax status, payment eligibility, sanctions evidence, and bank-account assertions from procurement and finance sources. The consolidated view supports risk analysis but does not authorize payment-account changes. Finance retains write authority, and every mastered value links to source, validation, time, and survivorship rule.

### Example 5

A product organization uses coexistence while replacing legacy authoring systems. Events include origin and mutation identifiers, and the master publishes approved classifications back to sources. Legacy sources may still author descriptions but cannot overwrite centrally governed hazard codes. Reconciliation detects a missed event, replays it idempotently, and records consumer activation.

### Example 6

Geography, sales territories, legal ownership, and management reporting all use trees over similar organizational units. A shared hierarchy service supplies versioning, temporal edges, provenance, validation, and projection APIs. Separate domain authorities govern each relationship type. Consumers cannot substitute the sales hierarchy for legal control merely because both use the same nodes.

### Example 7

Customer, policyholder, beneficiary, claimant, and insured party are related but not equivalent. The insurance enterprise rejects a universal party schema and defines minimal identifier, role, provenance, and effective-time contracts. Governed mappings expose where transformations are partial or many-to-many. Underwriting and claims retain richer domain models.

### Example 8

A shared match service offers normalization and scored candidates to customer and supplier domains. Customer chooses a lower false-negative tolerance for service continuity; supplier payment chooses a lower false-positive tolerance because a false merge could redirect funds. The platform uses separate approved configurations, publishes calibration evidence, and has no authority to approve either business threshold.

### Example 9

An acquisition begins with read-only consolidated views for two high-value consumer decisions. Teams compare outputs in shadow mode, adjudicate disagreements, stabilize contracts, and onboard consumers by cohort. Only after evidence and accountable approval does one product attribute move to coexistence. The fallback retains old source reads and a repairable mapping history.

### Example 10

An obsolete enterprise customer hub is retired after domains publish replacement products. The program freezes new clients, inventories subscriptions and caches, migrates active consumers, reconciles final identifiers, preserves redirects and required provenance, closes credentials and outbound feeds, deletes unneeded copies, and tests that recovery cannot reactivate the hub. Ownership and funding records close only after the last obligation is accepted.

## Cross-Program Connections

- **Systems engineering:** boundary definition, stakeholder needs, trade studies, assurance cases, lifecycle thinking, and emergent-risk analysis frame a federated MDM capability as a system of organizational and technical systems.

- **API and service engineering:** resource contracts, compatibility, idempotency, error semantics, authorization, observability, deprecation, and consumer support make domain products and shared capabilities operated services rather than file drops.

- **Platform engineering:** self-service interfaces, paved roads, tenant isolation, policy automation, service ownership, reliability, capacity, support, and platform product economics reduce cognitive load without taking semantic control.

- **Data engineering:** capture, transformation, event and batch movement, data quality implementation, lineage, reconciliation, replay, and operational repair preserve the authority and evidence defined here.

- **Distributed systems engineering:** consistency, partitions, ordering, idempotency, replication, conflict, convergence, and recovery reveal coexistence and propagated mastering as distributed protocols even when marketed as data integration.

- **Software architecture and engineering patterns:** bounded contexts, anti-corruption layers, contracts, ownership boundaries, and evolutionary design help minimal interoperability contracts preserve local models.

- **Security, privacy, and reliability engineering:** threat analysis, purpose limitation, minimization, access, audit, incident response, service objectives, graceful degradation, continuity, and recovery constrain every capability boundary.

- **Organizational design:** decision rights, team boundaries, coordination mechanisms, incentives, funding, escalation, and succession determine whether owners have real authority and budget.

## References

1. Zhamak Dehghani, [“Data Mesh Principles and Logical Architecture”](https://martinfowler.com/articles/data-mesh-principles.html), 2020. Retrieved 2026-09-03.
2. IBM, [“Comparison of virtual, physical, and hybrid MDM capabilities”](https://www.ibm.com/docs/en/imdm/11.6.0?topic=technologies-virtual-physical-hybrid-mdm), updated 2024. Retrieved 2026-09-03.
3. Amazon Web Services, [“Strategies for building a data mesh-based enterprise solution on AWS”](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-data-mesh/introduction.html). Retrieved 2026-09-03.
4. Google Cloud, [“Architecture and functions in a data mesh”](https://docs.cloud.google.com/architecture/data-mesh), reviewed 2024. Retrieved 2026-09-03.
5. Cloud Native Computing Foundation, [“CloudEvents Specification, version 1.0.2”](https://github.com/cloudevents/spec/blob/ce@v1.0.2/cloudevents/spec.md), 2022. Retrieved 2026-09-03.
6. W3C, [“SKOS Simple Knowledge Organization System Reference”](https://www.w3.org/TR/skos-reference/), 2009. Retrieved 2026-09-03.
7. W3C, [“PROV-O: The PROV Ontology”](https://www.w3.org/TR/2013/REC-prov-o-20130430/), 2013. Retrieved 2026-09-03.
8. UK Government, [“Data Ownership Model”](https://www.gov.uk/government/publications/data-ownership-in-government/data-ownership-model), updated 2024. Retrieved 2026-09-03.
9. W3C, [“Data on the Web Best Practices: Data Quality Vocabulary”](https://www.w3.org/TR/vocab-dqv/), 2016. Retrieved 2026-09-03.
10. NIST, [“Systems Security Engineering: Considerations for a Multidisciplinary Approach in the Engineering of Trustworthy Secure Systems,” SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final), 2022. Retrieved 2026-09-03.

## Exercises

### Exercise 1

A bank has customer, commercial-client, merchant, employee, and counterparty domains. Design the authority map, shared capabilities, domain products, and minimal interoperability contracts needed for sanctions screening and customer service without one universal party model.

### Exercise 2

A manufacturer proposes a central product hub for identifiers, engineering attributes, marketing copy, regulatory classifications, pricing, inventory, and maintenance data. Select an implementation style per bounded attribute group and justify each allocation, including change and correction behavior.

### Exercise 3

A coexistence deployment sometimes produces divergent addresses after network partitions and occasionally loops reflected updates between systems. Define an event, idempotency, ordering, authority, reconciliation, and recovery design that produces explainable convergence.

### Exercise 4

An executive dashboard reports 40 million golden records, 98 percent match confidence, 95 percent catalog coverage, and 99.9 percent hub uptime. Critique these measures and design an outcome, adoption, quality, convergence, correction, reliability, and economic scorecard.

### Exercise 5

An enterprise will replace a central customer hub with regional domain products and shared identity, matching, vocabulary, metadata, and propagation capabilities. Design an incremental migration and retirement plan with evidence gates, consumer activation, rollback or compensation, and non-resurrection tests.

## Answers to the Exercises

### Answer 1

Define the concepts separately: a retail customer, commercial organization, merchant accepting payment, workforce member, and financial counterparty can refer to overlapping real-world parties while carrying different relationships, state, authority, legal duties, and permitted uses. Assign a semantic and source owner for each domain; an enterprise identity owner for cross-domain identifier policy and merge or split rules; sanctions and financial-crime owners for screening policy and risk acceptance; domain product owners; platform service owners; consumer owners; and privacy, security, legal, records, ethics, and assurance participation according to consequence. Do not let the shared identity team decide whether an employee is a customer or whether a counterparty may transact.

Publish one versioned product per domain with its local identifier, enterprise identity assertion where authorized, role, effective interval, source provenance, quality evidence, change contract, protection, support, and correction path. Shared capabilities include identity registry, configurable matching, sanctions reference data, vocabulary and mapping, metadata and lineage, authorized query, propagation, reconciliation, audit evidence, and stewardship routing. Minimal contracts cover opaque identifiers, domain and role, identity-assertion provenance and confidence, event identity and version, correction and tombstone semantics, screening-list version, decision timestamp, and consumer acknowledgment. Customer service receives a purpose-specific projection; sanctions screening receives only justified identity features and relationship context. Mappings are explicit and incomplete where concepts differ. Measure false merges and misses, screening decision repair, service outcomes, access and purpose compliance, propagation lag, consumer activation, and correction closure.

### Answer 2

Centralize global product identifier creation because the enterprise requires a stable non-reused namespace and one legitimate issuance policy. Keep engineering attributes in product-line domains because their meaning, lifecycle, units, variants, and change authority belong with engineering capability; publish interoperable projections and consolidate selected values for enterprise discovery. Use coexistence for regulatory classifications if domain experts propose and maintain evidence while an enterprise authority approves high-consequence classifications and distributes the approved view. Keep marketing copy domain- or market-authored with localized vocabulary and product links. Keep pricing in market or commercial domains because price depends on jurisdiction, channel, contract, customer, currency, and effective time. Keep inventory in operational location or fulfillment domains because it is volatile transactional state rather than stable product master data. Keep maintenance definitions with asset or service engineering and map them to product identifiers.

For each group define source and write authority, identifiers, contract, version, effective time, provenance, quality, event and snapshot behavior, consumer use, reconciliation, correction, service objectives, protection, and retirement. A regulated-classification correction can require approval, urgent propagation, consumer acknowledgment, affected-product quarantine, and decision remediation. A marketing correction can use a lower-risk workflow. The design is therefore hybrid at the enterprise level without treating hybrid as one product configuration.

### Answer 3

Give every change an immutable mutation identifier, entity identifier, attribute scope, origin system, authoring authority, source version, event time, effective time, schema version, causal predecessor or entity sequence where required, and provenance. Consumers persist processed mutation identifiers for idempotency. Reflected master updates carry the original mutation identifier plus a distribution identifier and may not be re-emitted as new domain-authored changes. Attribute policy states which source can author which interval and how simultaneous admissible changes are resolved; “last arrival wins” is rejected because network delay does not establish authority.

Maintain authoritative per-entity versions and a durable change log. Reconciliation compares source versions, master state, event offsets, subscriber acknowledgments, hashes or selected values, and active consumer versions. A gap triggers replay from a known checkpoint; a conflict is quarantined for deterministic policy or steward review; a false application produces a compensating correction with preserved history. During partition, permit bounded local writes only for locally authoritative attributes, mark assembled reads stale, and fail closed for high-risk central decisions. Recovery restores policy and identity state before replay, proves idempotent convergence in a shadow projection, obtains accountable promotion, and then repairs downstream decisions. Test duplicate, missing, delayed, reordered, unauthorized, poison, split-brain, and replayed messages.

### Answer 4

The measures lack denominators, populations, uses, time windows, thresholds, error consequences, consumer state, and cost. Record count can reward duplicates or unnecessary scope. Average confidence is not precision, recall, or calibration and may hide harmful segment errors. Catalog coverage does not show semantic correctness, authority, use, or current contracts. Hub uptime excludes dependency failure, latency, stale data, write unavailability, recovery, and consumer activation.

Build an outcome layer: duplicate-related payment loss, screening or safety errors, order failures, service resolution, prevented harm, and decision correction. Add adoption: eligible products and consumers, contract binding, current-version activation, discovery-to-use time, and obsolete path retirement. Add quality: purpose-specific rules by population, match precision and recall from representative adjudicated samples, calibration, ambiguity, provenance, freshness, and mapping loss. Add convergence and correction: propagation lag percentiles, reconciliation variance, replay success, false merge and split rates, time to detect and repair, affected decisions corrected, and recurrence. Add reliability: end-to-end successful and fresh responses, degraded-mode use, incident duration, recovery objective tests, and dependency budgets. Add economics: product and platform cost, marginal capacity, stewardship effort, onboarding lead time, reuse, avoided pairwise integration, and closure liability. State confidence and limitations and assign an owner for corrective action.

### Answer 5

Start by inventorying the hub's semantic and write authorities, schemas, rules, identifiers, source links, consumers, exports, caches, integrations, quality controls, incidents, service objectives, access, retention, backups, staff knowledge, contracts, and funding. Define regional domain boundaries and succession of each decision right. Establish enterprise identifier, cross-domain policy, common event envelope, minimal contracts, platform boundaries, consumer obligations, and non-negotiable protection and evidence before moving data or writes.

Choose one consequential consumer journey and a bounded cohort. Publish regional products while the hub remains authoritative, run identity and match output in shadow mode, compare representative results, resolve ambiguity, test false merge repair, verify security and recovery, and bind the consumer to versioned interfaces. Promote read traffic gradually with a fallback to the hub and explicit decision owner. Move write authority only for attributes whose workflows, propagation, reconciliation, correction, support, and risk approval are complete. Repeat by reversible cohorts; keep crosswalks and source provenance through every cutover. Track active consumers rather than interface calls alone.

For retirement, freeze new hub consumers and schema expansion, announce deadlines, migrate or close every subscription and batch export, reconcile final state, preserve identifier redirects and legally required evidence, disable old write paths, rotate credentials, stop feeds, delete unauthorized copies, close exceptions and support, transfer remaining duties, and update catalogs and ownership. Test that disaster recovery, backups, automation, and old credentials cannot restore active authority or publication. Accountable domain, platform, consumer, security, privacy, records, operational-risk, and service owners accept closure; unresolved obligations keep the retirement open.
