---
module_id: DARCH-029
program: Data Architecture Engineering
level: 1
module_number: 29
title: Domain Metadata and Discoverability
status: complete
last_verified: 2026-09-03
---

# Domain Metadata and Discoverability

## One-Page Review

### Governing question

How can domains publish trustworthy, protected, interoperable metadata that helps authorized consumers discover, understand, evaluate, access, use, monitor, and retire data products without confusing catalog visibility with authority, quality, or permission?

### Essential definitions

- **Metadata** is data that describes, contextualizes, administers, connects, or evidences another resource, assertion, process, service, or decision.
- **Domain metadata** expresses domain-owned meaning, authority, rules, products, relationships, quality, service, protection, and lifecycle in its bounded context.
- **Discoverability** is the ability of an intended user or system to locate relevant resources and obtain enough context to judge next action.
- A **catalog** is a governed service that collects, indexes, relates, and presents descriptions of data products, datasets, services, distributions, terms, controls, and evidence.
- A **metadata record** is a versioned description of an identified resource, including provenance and lifecycle state.
- **Descriptive metadata** supports identification and discovery; **structural metadata** describes composition; **administrative metadata** supports management, protection, rights, and preservation.
- A **controlled vocabulary** is a governed set of identified concepts and labels with explicit relationships and lifecycle.
- **Provenance** describes entities, activities, agents, derivations, and responsibility relevant to origin and change.
- **Metadata quality** is fitness of metadata for declared discovery, evaluation, governance, operation, or assurance uses.
- **Authorized discoverability** reveals appropriate existence and context to eligible users while protecting sensitive content, relationships, vulnerabilities, and obligations.

### Central model, mechanism, or theorem

Represent a metadata record as:

`M = (identity, resource_type, domain, purpose, semantics, ownership, provenance, lineage, quality, service, protection, interfaces, relationships, lifecycle, evidence)`

Represent a discovery decision as `Find → Understand → Evaluate → Request → Use → Monitor → Exit`. Each stage needs different metadata and authorization. A useful record is identifiable, scoped, current, attributable, comprehensible, connected, actionable, protected, and versioned. Search ranking can suggest relevance, but only contracts, evidence, consumer context, and accountable review can establish fitness or permission.

### Critical invariants

- Every governed resource and metadata record has a stable identifier, type, domain, owner, steward, status, version, and effective time.
- Business definitions, physical schemas, product contracts, operational telemetry, provenance, lineage, and policy metadata remain linked but distinct.
- Metadata assertions identify source, method, authority, review state, confidence, and time; generated or inferred values never masquerade as approved facts.
- Discoverability does not grant access, purpose, licensing, legal authority, ethical acceptability, or fitness for a decision.
- Search, browse, graph navigation, and machine discovery preserve domain context and do not force ambiguous terms into false equivalence.
- Quality, service, incident, and limitation metadata are current enough to support evaluation and expose missing or uncertain evidence.
- Sensitive metadata and relationship graphs use classification, minimization, access, retention, audit, and safe public summaries.
- Catalog records link to authoritative sources rather than becoming uncontrolled copies of contracts, policies, and operational state.
- Metadata changes, mappings, merges, redirects, deprecations, and deletions preserve history and notify affected consumers.
- Discovery success is measured through findability, comprehension, qualified adoption, safe access, reduced duplication, issue outcomes, and retirement—not record count alone.

### Common failures

Common failures are bulk-registering every table without purpose; using names as identifiers; copying definitions from column names; treating a catalog as the source of truth for all metadata; leaving owner fields after reorganization; labeling machine inference as approved meaning; ranking popularity as quality; hiding limitations to improve adoption; exposing sensitive product existence or lineage; merging homonyms across domains; creating one enterprise taxonomy with no local context; requiring manual metadata already available from code; letting broken links and stale service data accumulate; measuring coverage by populated fields; and deleting retired records so historical decisions lose context.

### Compact example

An analyst searches “customer revenue” and finds 120 tables ranked by query count. The top result has no purpose, grain, authority, freshness, protection, or owner. The organization publishes product-level records with stable identifiers, scoped domain concepts, consumer purposes, semantic contracts, interfaces, quality and service evidence, lineage, access-request paths, limitations, versions, and lifecycle. Search combines text, controlled concepts, graph relationships, authorization, current evidence, and declared fitness signals. The analyst can compare two legitimate revenue meanings rather than being sent to the most popular table.

### Connections

[DARCH-015](015-shared-vocabulary-and-business-glossaries.md) introduces governed language. [DARCH-024](024-stewardship-roles.md) assigns metadata care, [DARCH-025](025-source-aligned-aggregate-and-consumer-aligned-data.md) defines product types, [DARCH-027](027-producer-and-consumer-contracts.md) defines exchange obligations, and [DARCH-028](028-cross-domain-dependencies.md) supplies relationships. This module makes those artifacts discoverable before [DARCH-030](../ROADMAP.md) evaluates domain cohesion.

## Governing Question

Finding a table name is not the same as discovering usable data. A consumer must know what the resource claims, who governs it, which decisions it supports, how it behaves, what evidence exists, what restrictions apply, how to request access, and how it changes. A catalog that answers only “where?” accelerates misuse.

The architectural task is to assemble metadata from domain knowledge, delivery artifacts, runtime observation, controls, and stewardship while preserving authority and protection. Good discoverability reduces search cost and ambiguity without turning rankings or generated descriptions into governance decisions.

## Why This Matters

Organizations often have both scarcity and excess: consumers cannot find trustworthy products, while platforms inventory millions of tables, fields, files, jobs, and dashboards. Increasing record count can worsen the problem when stale and low-value objects overwhelm useful product descriptions.

Metadata is also operational. Incident responders need affected products and owners. Change teams need consumers and versions. Privacy teams need purpose and flow. Records teams need retention and holds. Product owners need adoption and support evidence. Discoverability should serve these decisions through linked views.

W3C [Data Catalog Vocabulary Version 3](https://www.w3.org/TR/vocab-dcat-3/) provides terms for catalogs, resources, datasets, data services, distributions, relationships, and versioning. It supports interoperable descriptions while allowing profiles for local requirements.

W3C [PROV-O](https://www.w3.org/TR/prov-o/) represents entities, activities, agents, and derivation. W3C [SKOS Reference](https://www.w3.org/TR/skos-reference/) provides a model for concept schemes, labels, semantic relationships, mappings, and notes. Together they support provenance and controlled domain language without requiring every concept to be globally identical.

The [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) provide a widely used vocabulary for resource description. [Schema.org Dataset](https://schema.org/Dataset) supplies web-oriented dataset properties. These vocabularies aid exchange and indexing, but a profile must state local cardinality, authority, validation, and interpretation.

[ISO/IEC 11179-3:2023](https://www.iso.org/standard/78915.html) specifies registry metamodel and basic attributes for metadata registries. The W3C [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/) supports quality measures, annotations, policies, and provenance. The [FAIR Guiding Principles](https://doi.org/10.1038/sdata.2016.18) articulate findability, accessibility, interoperability, and reusability for scientific data stewardship. FAIR does not mean unrestricted public access; authentication and authorization can remain necessary.

## Prerequisites and Retrieval

You should understand domains, products, identifiers, business glossaries, schemas, lineage, provenance, quality, service objectives, contracts, search, access, privacy, security, records, and lifecycle.

Retrieve metadata, catalog, registry, glossary, taxonomy, thesaurus, ontology, concept scheme, identifier, label, synonym, homonym, schema, profile, provenance, lineage, quality, service, classification, rights, license, access request, indexing, ranking, faceting, graph search, federation, harvesting, and deprecation.

As a retrieval test, inspect a result named `customer_revenue_gold`. Ask which product it describes; which customer and revenue concepts apply; what one record represents; who owns and stewards it; which source and derivation created it; which quality and service evidence is current; which uses and users are permitted; what interface and version apply; and whether it is active. A search hit without these answers is only a locator.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish descriptive, structural, administrative, semantic, operational, protection, provenance, quality, and lifecycle metadata;
2. define stable resource and record identities, types, versions, effective intervals, sources, authorities, and states;
3. design product-level metadata profiles with required, recommended, conditional, and extensible elements;
4. connect domain concepts, schemas, contracts, interfaces, owners, lineage, quality, service, policies, incidents, and consumers;
5. govern controlled vocabularies, synonyms, homonyms, mappings, multilingual labels, deprecation, and cross-domain context;
6. combine text search, facets, graph relationships, behavioral signals, and authorization without treating ranking as truth;
7. automate extraction and enrichment while preserving provenance, confidence, review, override, and correction;
8. protect sensitive metadata and expose safe summaries, request paths, rights, licenses, purpose, and access states;
9. measure metadata quality and discovery outcomes through decision-centered evidence rather than field-population vanity metrics;
10. federate, synchronize, audit, transfer, archive, and retire metadata across domain and platform lifecycles.

## Core Exposition

**Begin with discovery tasks.** Identify users and questions: find a product for a decision, understand a term, compare alternatives, request access, diagnose failure, assess change impact, trace provenance, respond to a right, or retire a dependency. Each task needs different metadata.

Do not begin with every field a tool can collect. Start with decisions and minimum evidence, then automate and enrich. A smaller current product catalog can be more useful than a complete inventory of undocumented objects.

**Choose the governed resource level.** Catalog domains, data products, datasets, services, distributions, schemas, terms, rules, controls, reports, models, and pipelines as distinct resource types. Link them rather than flattening them into one “asset” type.

Physical tables remain useful implementation metadata, but consumers usually need a product contract and purpose first. Millions of partitions should not each compete with governed products in search results.

**Assign stable identifiers.** Names change, collide, translate, and move. Give resources and metadata records durable identifiers independent of display label, physical location, or incumbent owner.

State namespace, issuer, uniqueness, persistence, merge, split, redirect, and retirement policy. Preserve aliases and old identifiers so links and historical evidence remain resolvable.

**Separate resource and record.** A data product is not its catalog record. The record describes the product and has its own version, provenance, review, and access. This separation enables multiple authorized views without duplicating the resource identity.

Record metadata about metadata: source, extraction method, agent, time, confidence, authority, review state, and supersession. Consumers can then distinguish owner-approved definition from inferred description.

**Define a metadata profile.** A profile specializes general vocabularies for local use. Identify required, recommended, optional, conditional, repeatable, controlled, derived, and protected properties. Define cardinality, value type, vocabulary, validation, and authority.

Avoid requiring fields no one uses. Conditional rules can demand stronger evidence for critical, sensitive, shared, or externally published products. Extensions need stable namespaces and documentation.

**Describe identity and purpose.** Core descriptive metadata includes identifier, title, alternative title, resource type, domain, summary, purpose, intended users, decisions, keywords, language, geography, temporal coverage, and status.

Purpose should be specific enough to assess relevance and protection. “Reporting” or “analytics” is rarely sufficient. Include excluded uses and known limitations near the summary rather than hiding them in a policy attachment.

**Describe semantics.** Link concepts, definitions, business keys, grain, time semantics, units, codes, null meanings, derivations, examples, and interpretations. A column name can be evidence but is not a definition.

Show context. `Customer` may legitimately differ in Commerce, Billing, Support, and legal processing. Map related concepts without forcing exact equivalence. Identify which concept each product contract uses.

**Govern labels and synonyms.** Controlled vocabularies assign concept identifiers, preferred and alternative labels, definitions, notes, broader and narrower relationships, and mappings. Search can use synonyms while results preserve the governing concept.

Handle homonyms explicitly. `Account` can mean financial account, user credential, client organization, or chart-of-accounts entry. Ranking should not silently merge them.

**Support multilingual metadata.** Attach language tags to labels, definitions, examples, and notes. Translate meaning through qualified review rather than copying tokens mechanically.

One concept can have several labels, but translations may not be exact. Record scope and differences. Search should use locale and still permit cross-language discovery where authorized.

**Describe ownership and stewardship.** Link durable accountable roles, stewards, custodians, producers, support contacts, control roles, and current incumbents with effective intervals. State decision scope and escalation.

An owner field without authority or current person is weak metadata. Synchronize role sources and detect vacancies, stale incumbents, or conflicting assignments. Do not expose personal details beyond operational need.

**Describe provenance.** Record sources, authoritative assertions, transformations, agents, activities, parameters, versions, execution, and evidence. Separate observed, adopted, reconciled, calculated, inferred, and presented values.

PROV-O provides an interoperable model, but local profiles determine granularity. Preserve enough provenance for fitness, correction, reproduction, incident response, and audit without exposing sensitive implementation or data.

**Describe lineage.** Link upstream and downstream products, schemas, transformations, reports, models, and interfaces. Label design-declared, runtime-observed, manual, inferred, and verified edges.

Technical lineage is not semantic authority. Show product contracts and assertion relationships. Record coverage and confidence, especially for dynamic queries, spreadsheets, manual files, and third parties.

**Describe quality.** Publish characteristics, metrics, populations, methods, windows, thresholds, results, exceptions, incidents, limitations, and provenance. A naked score cannot support evaluation.

Distinguish objective definition from observed result. Keep history so consumers can assess trends and reproduce decisions. Protect quality evidence that reveals sensitive populations or vulnerabilities.

**Describe service behavior.** Publish interfaces, freshness, latency, availability, publication schedule, correction, recovery, support, status, incidents, and maintenance. Link precise indicator definitions and current evidence.

Avoid copying operational status manually into descriptions. Integrate authoritative telemetry while preserving measurement time, source, and missing evidence. A stale green badge is harmful.

**Describe protection and rights.** Include classification, permitted purpose, eligibility, access method, license, rights, retention, jurisdiction, sharing, provider, audit, and incident contacts at an appropriate disclosure level.

Catalog visibility does not grant use. Make the access-request path and decision criteria discoverable to eligible users. A result can reveal safe summary metadata while withholding sensitive fields, lineage, locations, or existence.

**Describe interfaces and distributions.** A product may offer table, view, file, stream, API, semantic model, or query service distributions. Record protocol, schema, version, format, endpoint, authentication, examples, limits, service, and deprecation.

Keep interface details synchronized with delivery specifications. Broken links destroy trust. Expose sandbox or synthetic samples where appropriate without leaking production content.

**Describe relationships.** Useful relationships include version of, replaces, conforms to, derived from, distributed as, serves, consumes, governed by, described by, related concept, equivalent under condition, and incompatible with.

Name relation direction and semantics. A generic “related to” edge helps navigation little and can mislead automated reasoning. Version relationships should preserve history and redirects.

**Describe lifecycle.** Use controlled states such as proposed, active, deprecated, retired, archived, suspended, or withdrawn with entry criteria and effective dates. State support and access behavior in each state.

Retired records remain discoverable enough to explain history, redirect consumers, and support corrections. Search should prefer active products while allowing explicit historical queries.

**Establish metadata authority.** Different properties have different authoritative sources: owners from organizational assignments, schemas from repositories, interfaces from specifications, telemetry from observability, classifications from approved workflows, and definitions from domain stewardship.

Do not make the catalog an uncontrolled master copy. Resolve values from authoritative systems or publish signed/versioned records. Conflicts should be visible and routed, not silently overwritten by last write.

**Automate collection.** Extract schemas, descriptions, lineage, tags, owners, tests, usage, and service evidence from code and platforms. Automation reduces duplicate entry and improves currency.

Extraction also propagates bad names and stale comments. Label source and method, validate identifiers, map to product context, and provide steward review. Generated content starts as proposed unless policy states otherwise.

**Use inference carefully.** Classifiers can suggest sensitivity, concepts, owners, descriptions, relationships, and quality rules. Record model, version, inputs, time, confidence, limitations, and review state.

Do not expose inferred sensitive facts broadly. False negatives can weaken protection; false positives can block use. Apply human and control review proportional to consequence, and preserve corrections for future evaluation.

**Design ingestion and synchronization.** Define authoritative source, polling or event mechanism, transformation, identity resolution, conflict policy, latency, retry, deletion, and replay for each metadata feed.

Metadata pipelines need observability and recovery. A failed owner synchronization or classification feed can create access and incident risk even while data pipelines continue.

**Validate structure and semantics.** Structural rules check identifiers, types, required fields, cardinality, formats, vocabularies, links, and state transitions. Semantic review checks definitions, authority, grain, time, purpose, limitations, and mappings.

Validation errors should route to capable owners with severity and service expectations. Blocking publication can be appropriate for critical omissions; warnings may suit exploratory resources. Never equate validator success with fitness.

**Design search from intent.** Support text, facets, controlled concepts, domain, product type, geography, time, quality, service, interface, status, and authorized purpose. Query understanding can expand synonyms without erasing context.

Different tasks need different rankings. A beginner may value certified and well-documented products; an incident responder needs dependency and owner evidence; a migration team needs deprecated versions and consumers.

**Rank transparently.** Signals can include semantic match, exact concept, purpose match, authoritative status, currentness, evidence, quality, service, adoption, consumer feedback, and lifecycle. Popularity is useful but can reinforce legacy and bias.

Expose why a result ranked and allow filters. Do not claim an opaque relevance score proves quality or approval. Protect behavioral signals and avoid leaking restricted resource popularity.

**Support graph discovery.** Users often navigate from domain to product, concept, schema, owner, upstream source, downstream report, quality issue, or replacement. Typed relationships can answer richer questions than keyword search.

Control traversal. A public product may depend on sensitive sources whose identities should not be revealed. Provide summarized or redacted edges and audit privileged graph access.

**Support machine discovery.** Publish documented APIs, schemas, profiles, identifiers, content negotiation, pagination, versioning, change feeds, and authentication. Machine clients need deterministic semantics and error behavior.

Use established vocabularies where they fit and local extensions where necessary. Validate profiles and provide examples. Interoperability is demonstrated through exchange tests, not vocabulary names alone.

**Federate catalogs.** Domains can own metadata close to products while a shared platform indexes common profiles and relationships. Federation preserves context and distributes work, provided identifiers, minimum fields, vocabularies, synchronization, and conflict rules align.

Central teams should supply platform, standards, training, and assurance rather than rewrite every domain definition. Domains should not publish incompatible identifiers or hidden local states that prevent enterprise discovery.

**Handle duplicates and variants.** Similar records may be replicas, aliases, versions, distributions, regional variants, competing products, or accidental duplication. Do not merge solely by title or schema similarity.

Use stable identity, provenance, owner decision, and contract comparison. Preserve legitimate variants and explain differences. Redirect aliases and retire accidental copies after consumer review.

**Collect consumer feedback.** Let users report unclear definitions, broken links, access friction, quality limitations, missing products, and successful decisions. Link feedback to resource and version.

Feedback is evidence, not authority. Route it through stewardship and product workflows. Protect reporter identity and sensitive details. Close the loop with visible outcomes.

**Design access discovery.** Show eligibility, purpose requirements, approvers, expected response, prerequisites, costs, and support. Integrate requests with identity and policy systems while maintaining separation between discovery and authorization.

Measure denial reasons and abandoned requests to improve products and policies. Do not weaken necessary controls merely to raise adoption. Provide accessible alternatives where possible.

**Protect metadata.** Names, schemas, row counts, owners, lineage, query patterns, classifications, vulnerabilities, incident histories, and provider relationships can be sensitive. Classify metadata independently of underlying data.

Apply minimization, access, encryption, audit, retention, redaction, aggregation, and safe summaries. Protect metadata pipelines and catalogs as critical services. Plan incident response and recovery.

**Measure metadata quality.** Useful dimensions include completeness for a profile, validity, consistency, accuracy against authority, currency, provenance, link integrity, uniqueness, comprehensibility, and actionability.

Every measure needs population and method. Field completion can be gamed with meaningless prose. Sample records and ask whether real users can make correct decisions. Segment critical products.

**Measure discovery outcomes.** Track search success, time to qualified product, reformulation, zero results, abandoned sessions, access completion, qualified adoption, duplicate creation avoided, support questions, misuse, change reach, incident routing, and retirement migration.

Behavioral measures can be privacy-sensitive and ambiguous. Combine them with research, feedback, and outcome evidence. High search volume may mean interest or poor navigation.

**Curate high-value surfaces.** Landing pages, domain maps, product collections, common tasks, semantic guides, and recommended paths help users who do not know exact terminology. Curation should disclose criteria and owner.

Avoid permanent hand-maintained portals disconnected from authoritative records. Compose curated experiences from versioned metadata and verify links.

**Operate metadata incidents.** Broken ownership, wrong classification, misleading definition, stale service status, leaked sensitive lineage, or incorrect access guidance can cause harm. Define detection, severity, containment, correction, notification, evidence, and review.

Metadata corrections may require downstream communication just like data corrections. Preserve old versions when decisions relied on them. A fixed catalog page does not repair prior misuse automatically.

**Govern change.** Classify metadata changes by semantic, administrative, operational, protection, interface, and lifecycle impact. Notify consumers when the change affects interpretation, access, service, or migration.

Version material assertions and preserve effective time. Typographical corrections can follow lighter policy. Emergency redaction needs bounded authority and retrospective reconciliation.

**Audit provenance and freshness.** Sample high-criticality records, trace each field to authority, recompute generated values, test links, compare catalog and product contracts, verify owners, and review access.

Independent assurance can challenge popularity bias, hidden products, missing limitations, and overbroad visibility. Distinguish self-attestation, automation, runtime observation, consumer evidence, and external review.

**Manage reorganization.** Transfer domain records, owner and steward assignments, products, vocabulary schemes, issues, exceptions, access paths, and support. Preserve identifiers when resources remain the same.

Do not mass-edit labels while leaving decision authority unclear. New roles explicitly accept work and capacity. Monitor stale contacts and orphan records during transition.

**Retire metadata deliberately.** Retirement keeps identifiers, final definitions, versions, provenance, replacement links, support dates, retention, and historical obligations while removing active routing and unauthorized access.

Delete metadata only when law, policy, protection, and evidence needs support deletion. Tombstones or redirects can prevent identifiers from being reused incorrectly.

**Treat discoverability as a product.** The catalog and metadata platform have users, owners, service expectations, quality, protection, support, change, and lifecycle. Domains provide governed content; platform teams provide scalable mechanisms.

The final test is whether an authorized consumer can find an appropriate product, understand its meaning and limitations, assess current evidence, obtain access through a clear path, use it under contract, respond to change or failure, and exit cleanly. Search alone is not discovery.

## Definitions and Notation

Let resource `r` have metadata record `M(r) = (id,type,domain,purpose,semantics,ownership,provenance,lineage,quality,service,protection,interfaces,relationships,lifecycle,evidence)`.

For property `p`, represent an assertion as `A = (subject,predicate,value,source,method,authority,confidence,review_state,effective_time,recorded_time)`. The value alone cannot establish its trust or currency.

Let discovery stages be `D = (find, understand, evaluate, request, use, monitor, exit)`. Define `Supports(M,d,u,t)` when record `M` provides authorized and sufficiently current evidence for user context `u`, stage `d`, and time `t`.

Let a local profile `P` define property obligations `(cardinality,value_type,vocabulary,condition,authority,protection,validation)`. Structural conformance to `P` is necessary for interoperable processing but not sufficient for semantic correctness or fitness.

Metadata coverage compares required resources `R*` and properties under `P` with current records, then reports missing, invalid, inconsistent, stale, unauthoritative, unreviewed, inaccessible, or orphaned evidence.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for every material domain metadata record.

**1. Identity gate.** Assign stable resource and record identifiers, type, domain, version, state, aliases, redirects, and effective intervals.

**2. Purpose gate.** Describe intended users, decisions, populations, scope, value, excluded uses, and limitations.

**3. Semantic gate.** Link concepts, definitions, keys, grain, time, units, codes, nulls, derivations, examples, mappings, and authority.

**4. Responsibility gate.** Link owners, stewards, producers, custodians, support, control roles, incumbents, deputies, and escalation.

**5. Evidence gate.** Preserve source, method, provenance, lineage, confidence, review, quality, service, incidents, and currentness.

**6. Access gate.** Publish interfaces, distributions, eligibility, purpose, rights, license, request path, costs, prerequisites, and support.

**7. Protection gate.** Apply classification, minimization, privacy, security, records, jurisdiction, redaction, audit, retention, and incident handling.

**8. Discovery gate.** Support text, facets, controlled concepts, graph navigation, machine APIs, ranking explanations, and accessible experiences.

**9. Change gate.** Govern validation, synchronization, conflicts, versions, notice, corrections, mappings, deprecation, replacement, and emergency action.

**10. Lifecycle gate.** Measure outcomes, audit, transfer, federate, archive, retire, revoke, preserve history, and close obligations.

The executable example checks four narrow metadata-record failures: missing owner, missing purpose, missing provenance, and missing classification.

<!-- bijux-verify: {"id":"domain-metadata-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"records=4\nvalid=0\nfindings=claims-lineage:missing-classification,customer-product:missing-purpose,orders-schema:missing-owner,revenue-metric:missing-provenance\nready=false\n","stderr":""}} -->
```python
records = (
    {"id": "orders-schema", "owner": False, "purpose": True, "provenance": True, "classification": True},
    {"id": "customer-product", "owner": True, "purpose": False, "provenance": True, "classification": True},
    {"id": "revenue-metric", "owner": True, "purpose": True, "provenance": False, "classification": True},
    {"id": "claims-lineage", "owner": True, "purpose": True, "provenance": True, "classification": False},
)

findings = []
valid = 0
for record in records:
    local = []
    if not record["owner"]:
        local.append("missing-owner")
    if not record["purpose"]:
        local.append("missing-purpose")
    if not record["provenance"]:
        local.append("missing-provenance")
    if not record["classification"]:
        local.append("missing-classification")
    if local:
        findings.extend(f"{record['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"records={len(records)}")
print(f"valid={valid}")
print("findings=" + ",".join(sorted(findings)))
print(f"ready={str(valid == len(records)).lower()}")
```

The checker validates four declared record predicates only. It does not prove owner authority, semantic correctness, provenance completeness, suitable classification, current quality or service, lawful access, search relevance, interoperability, consumer fitness, catalog security, or production readiness. Those require authoritative-source reconciliation, profile and link validation, domain review, protected access tests, consumer research, sampled decisions, operational evidence, and accountable approval.

## Alternatives and Trade-Offs

**Product-first versus asset-complete cataloging.** Product-first scope improves consumer signal and stewardship; complete technical inventory supports operations and risk. Keep both layers linked and rank governed products for general discovery.

**Centralized versus federated metadata.** Central authoring improves uniformity but loses context and becomes a bottleneck. Federation preserves domain ownership but needs identifiers, profiles, synchronization, and assurance.

**Manual versus automated metadata.** Manual curation captures meaning but scales poorly. Automation improves coverage and currency but propagates weak source descriptions and uncertain inference. Combine provenance-labeled automation with review.

**Open versus restricted discovery.** Broad visibility promotes reuse and reduces duplication; metadata can reveal sensitive assets and relationships. Publish safe summaries and authorized detail with explicit access.

**One taxonomy versus mapped vocabularies.** One taxonomy simplifies search but can erase bounded context. Domain schemes with mappings preserve meaning but increase governance. Use stable concepts and explicit mapping relations.

**Popularity versus authority in ranking.** Popularity reflects observed adoption but entrenches legacy and may leak behavior. Authority and evidence improve trust but can undervalue emerging products. Blend transparent signals and filters.

**Current-only versus historical metadata.** Current views reduce clutter; history supports reproducibility, incidents, corrections, and audit. Prefer current results by default while preserving versioned historical access.

**Rich lineage versus minimized exposure.** Detailed graphs aid impact and diagnosis but reveal sensitive sources, controls, and vulnerabilities. Offer role-based, redacted, and aggregated views.

## Failure Modes and Misconceptions

1. **A searchable table is discoverable data.** Consumers also need purpose, semantics, evidence, access, and lifecycle.
2. **The catalog is authoritative for every field.** Authority usually remains distributed across governed sources.
3. **A name is a stable identifier.** Names collide and change; identifiers need persistence and redirect rules.
4. **Column comments are business definitions.** They may be generated, stale, local, or implementation-specific.
5. **More metadata fields mean better metadata.** Unused, copied, and stale fields increase noise.
6. **A validator proves correctness.** It can prove only configured structural and selected semantic rules.
7. **Generated descriptions are approved meaning.** They require provenance, confidence, review, and correction.
8. **Popularity proves quality or fitness.** Legacy, habit, and visibility also drive use.
9. **One enterprise term removes ambiguity.** Context-specific meanings can remain legitimate and should be mapped.
10. **Discoverability grants access.** Permission, purpose, rights, and fitness remain separate decisions.
11. **Metadata is not sensitive.** Names, schemas, lineage, counts, owners, incidents, and vulnerabilities can expose risk.
12. **Runtime lineage is complete.** Dynamic, manual, external, encrypted, and unobserved paths create gaps.
13. **A green quality badge is current.** Measurement source, time, population, and missing evidence matter.
14. **Federation means every domain chooses any format.** Shared identifiers, profiles, and exchange rules remain necessary.
15. **No search results means no product exists.** indexing, authorization, vocabulary, and stale feeds can fail.
16. **Reorganization only changes owner names.** Authority, stewardship, support, access, and open work must transfer.
17. **Retirement should erase catalog records.** Historical decisions, corrections, contracts, and redirects may depend on them.

## Worked Examples

### Example 1

Search for “customer” returns technical replicas. A product-first index promotes governed Customer Profile offerings and lets users drill into schemas, distributions, lineage, quality, service, and regional variants.

### Example 2

Commerce and Billing use different `Customer` concepts. SKOS-style concept identifiers and scoped mappings expose overlap and difference without declaring false exact equivalence.

### Example 3

A classifier marks a product public with low confidence. Policy keeps the value proposed and restricted until a steward and security role review it; inference provenance remains attached.

### Example 4

An owner sync fails after reorganization. Metadata observability detects stale assignments, routes critical products to temporary accountability, and verifies successor acceptance before clearing findings.

### Example 5

A quality badge says 99.9 percent but lacks date and population. The record links objective, computation, eligible records, result window, exceptions, provenance, and current incident state.

### Example 6

Lineage reveals a sensitive fraud source behind a public aggregate. General users see bounded provenance and owner contact; authorized investigators can traverse protected detailed edges with audit.

### Example 7

An analyst searches a local-language synonym. Language-tagged labels find the concept, while the result preserves the reviewed domain definition and warns that the translation is narrower.

### Example 8

Two datasets share a title and schema but differ by jurisdiction and retention. Identity and provenance prevent an unsafe merge; search explains the variant and its permitted users.

### Example 9

A deprecated product remains popular. Ranking displays replacement and end date, registered consumers receive migration notices, and observed use drives support rather than silently hiding the result.

### Example 10

A retired revenue product supported old board decisions. Its active endpoints and credentials are removed, while final definitions, contracts, lineage, versions, quality evidence, and replacement links remain protected and discoverable.

## Cross-Program Connections

- **Information retrieval:** indexing, tokenization, ranking, facets, query understanding, relevance evaluation, and feedback shape discovery.
- **Knowledge representation:** identifiers, vocabularies, taxonomies, ontologies, mappings, provenance, and graph relationships express meaning.
- **Data engineering:** schema extraction, lineage, quality, orchestration, telemetry, synchronization, and serving populate metadata.
- **Platform engineering:** catalogs, search, identity, policy, workflow, APIs, observability, and self-service deliver discoverability at scale.
- **Security and privacy:** classification, minimization, purpose, access, redaction, audit, retention, and incidents govern metadata itself.
- **Product management:** user journeys, value, adoption, support, feedback, metrics, change, and retirement frame the catalog as a product.
- **API and service engineering:** machine discovery, interface descriptions, authentication, versioning, errors, and service expectations support exchange.
- **Systems engineering:** viewpoints, traceability, configuration, verification, assurance, stakeholder concerns, and lifecycle connect metadata views.

## References

1. W3C, *Data Catalog Vocabulary (DCAT)—Version 3*, W3C Recommendation, 2024. <https://www.w3.org/TR/vocab-dcat-3/>
2. W3C, *PROV-O: The PROV Ontology*, W3C Recommendation, 2013. <https://www.w3.org/TR/prov-o/>
3. W3C, *SKOS Simple Knowledge Organization System Reference*, W3C Recommendation, 2009. <https://www.w3.org/TR/skos-reference/>
4. Dublin Core Metadata Initiative, *DCMI Metadata Terms*, 2020. <https://www.dublincore.org/specifications/dublin-core/dcmi-terms/>
5. Schema.org, *Dataset*, continuously maintained vocabulary. <https://schema.org/Dataset>
6. ISO/IEC, *11179-3:2023 Metadata registries (MDR)—Part 3: Metamodel for registry common facilities*, 2023. <https://www.iso.org/standard/78915.html>
7. W3C, *Data on the Web Best Practices: Data Quality Vocabulary*, W3C Note, 2016. <https://www.w3.org/TR/vocab-dqv/>
8. Wilkinson, M. D. et al., *The FAIR Guiding Principles for scientific data management and stewardship*, Scientific Data 3, 2016. <https://doi.org/10.1038/sdata.2016.18>

## Exercises

### Exercise 1

Design a metadata profile for domain data products. Define required, conditional, derived, protected, and extensible properties with authorities, validation, and lifecycle.

### Exercise 2

Design search and graph discovery for a user seeking customer revenue data. Include intent, concepts, facets, ranking, explanations, authorization, comparison, access, and feedback.

### Exercise 3

Create a federated metadata operating model for eight domains and one shared platform. Include identifiers, profiles, vocabularies, ingestion, conflicts, stewardship, assurance, and service.

### Exercise 4

Plan automation for schema, lineage, owner, classification, quality, service, and usage metadata. State provenance, confidence, review, failure, protection, and correction behavior.

### Exercise 5

Build a metadata and discoverability scorecard that avoids record-count and field-completion vanity metrics. Include quality, search, evaluation, access, adoption, safety, change, incident, and retirement outcomes.

## Answers to the Exercises

### Answer 1

Require stable product and record identifiers, resource type, domain, title, summary, purpose, intended users, decisions, status, version, owner, steward, semantic contract, interfaces, support, classification, access path, provenance, and last verification. Conditionally require stronger quality, service, retention, jurisdiction, license, provider, incident, recovery, and assurance metadata for critical, sensitive, external, shared, or regulated products. Derive technical schema, runtime lineage, telemetry, and usage from authoritative systems with source and time.

Protect sensitive endpoints, owners, lineage, volumes, controls, incidents, and classifications through role-based views and safe summaries. Permit namespaced domain extensions with definitions and validation. For each property define cardinality, type, vocabulary, source authority, update mechanism, review, confidence, effective interval, and deletion. Validate links and state transitions. Preserve versions, aliases, redirects, replacements, and historical evidence. Structural conformance is necessary but domain and consumer review establish usefulness.

### Answer 2

Interpret “customer revenue” against authorized controlled concepts and domain contexts. Offer facets for Commerce, Billing, Finance, customer concept, revenue measure, jurisdiction, period, product alignment, status, quality, freshness, interface, and permitted purpose. Rank exact scoped concept and decision-purpose matches, authoritative active products, current evidence, documentation, and qualified adoption while treating popularity as one transparent signal. Explain each rank and preserve two legitimate revenue meanings.

Results show purpose, grain, time, sources, derivation, owner, quality and service evidence, limitations, protection summary, interfaces, version, and replacement. Graph navigation connects concepts, source products, aggregates, reports, and consumers under authorization. Comparison highlights semantic and policy differences. Access discovery shows eligibility, approvers, expected response, and support without granting permission. Capture reformulation, zero results, successful evaluation, access completion, feedback, and downstream outcomes under privacy controls.

### Answer 3

The shared platform owns catalog, search, graph, APIs, identity integration, policy enforcement, ingestion framework, telemetry, support, and common profile validation. Domains own product identity requests, definitions, purpose, authority, owners, stewards, mappings, quality interpretation, limitations, and lifecycle. An enterprise body governs minimum identifiers, core property semantics, controlled state, exchange, protection, and cross-domain conflict.

Domain repositories and systems publish versioned records; the platform harvests them with provenance and reconciles runtime evidence. Stable namespaces prevent collision. Shared vocabularies cover common concepts while domain schemes and explicit mappings preserve context. Conflict rules prefer declared property authorities and expose unresolved differences. Service objectives cover ingest delay, search, links, access routing, and recovery. Communities build competence. Metrics and samples evaluate currentness, comprehension, qualified use, security, and closure. Exceptions expire, and transfers require successor acceptance.

### Answer 4

Extract schemas and interface specifications from governed repositories, runtime lineage from supported collectors, owner assignments from role systems, classifications from approved workflows, quality from measurement products, service from telemetry, and usage from authorized aggregate logs. Every assertion records resource, property, value, source, method, agent or model, version, observation and effective time, confidence, review state, and override.

Deterministic extraction can publish automatically after validation for bounded properties. Inferred concepts, descriptions, sensitive classifications, and ownership start proposed and require consequence-based review. Missing feeds become explicit stale or unknown states rather than preserving green values. Protect samples, usage, lineage, vulnerabilities, and identities; minimize retention and audit access. Route conflicts and failures to stewards with service expectations. Preserve human corrections, compare them with inference, test false positives and negatives, and allow rollback and replay after source or model change.

### Answer 5

Metadata quality measures required-property coverage by consequence, validity, authority reconciliation, currency, provenance, link integrity, uniqueness, comprehensibility, actionability, stale owners, broken interfaces, and protected-view correctness. Sample prose and mappings so meaningless filled fields do not pass. Discovery measures time to qualified product, search success, reformulation, zero results, comparison, graph completion, accessibility, and user comprehension.

Outcome measures include access-request completion and denial reasons, qualified adoption, duplicate products avoided, reduced support questions, correct owner routing, consumer feedback closure, change-notice reach, migration, incident response, misuse, sensitive-metadata exposure, and retired-product closure. Segment critical and restricted products. Track missing telemetry and uncertainty. Combine privacy-protected behavioral measures with research, sampled decisions, exercises, and independent review. Never reward raw record count, search clicks, popularity, or field completion without evidence of correct and safe action.
