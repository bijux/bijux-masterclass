---
module_id: DARCH-061
program: Data Architecture Engineering
level: 2
module_number: 61
title: Metadata Architecture
status: complete
last_verified: 2026-09-03
---

# Metadata Architecture

## One-Page Review

### Governing question

How should an enterprise structure, identify, govern, exchange, operate, and retire metadata so that people and machines can discover, understand, trust, control, and use data across heterogeneous domains and systems?

### Essential definitions

- **Metadata** is structured information that describes, explains, locates, constrains, relates, operates, or preserves a resource and its use.
- A **metadata subject** is the resource, concept, event, process, policy, person, organization, service, or decision being described.
- A **metadata assertion** is a claim by an identified agent or process about a subject, predicate, value, scope, time, and provenance.
- A **metadata schema** defines allowed structures, fields, relationships, datatypes, cardinalities, and constraints for a class of records.
- A **metadata vocabulary** defines stable terms and their intended meanings; a schema determines how terms are composed and constrained.
- An **application profile** selects and constrains terms from one or more vocabularies for a bounded community and purpose.
- A **metadata registry** governs definitions, identifiers, versions, statuses, authorities, and representations of metadata elements or models.
- A **catalog** publishes searchable descriptions and access paths for assets and services; it is a view over metadata, not the entire architecture.
- **Provenance metadata** describes entities, activities, agents, derivations, attributions, generation, use, and time relevant to origin and change.
- **Lineage** is a purpose-bounded representation of dependencies and transformations across resources and processes.
- **Operational metadata** records runs, states, performance, incidents, freshness, capacity, and other execution evidence.
- **Behavioral metadata** records observed discovery, access, query, transformation, adoption, and use under explicit privacy and retention controls.
- A **metadata control plane** coordinates identity, ownership, schemas, policy, contracts, evidence, lifecycle, and discovery without necessarily moving the described data.
- A **metadata graph** represents identified subjects and typed relationships while preserving provenance, version, scope, and access boundaries.

### Central model, mechanism, or theorem

Represent metadata architecture as:

`M = (S, I, A, V, P, R, E, Q, C, O, L)`

where `S` is subject scope, `I` identifiers, `A` assertions and authorities, `V` vocabularies and schemas, `P` profiles and projections, `R` relationships, `E` exchange and retrieval, `Q` quality and validation, `C` controls and governance, `O` operations and observability, and `L` lifecycle closure. The architecture is fit only when consequential subjects have stable identity and accountable ownership; assertions retain provenance, time, scope, and confidence; contracts support interoperable exchange without forcing one universal model; consumers can distinguish current, historical, inferred, and disputed claims; and metadata remains secured, observable, correctable, recoverable, and closable.

### Critical invariants

- Metadata has its own semantics, quality, provenance, security, reliability, and lifecycle; it is not automatically trustworthy because it describes other data.
- Every metadata assertion identifies its subject, meaning, authority, source, effective time, observation time, and status when those dimensions affect interpretation.
- Stable identifiers outlive display names, locations, technologies, organizations, and mutable labels.
- Description of a resource is distinct from the resource, its representation, its schema, its distribution, and the service that exposes it.
- Business, semantic, structural, operational, provenance, quality, governance, security, and behavioral metadata remain distinguishable but linkable.
- Domain authorities own contextual meaning; shared platforms own reusable metadata services and declared exchange behavior.
- One enterprise metamodel is not required; a small interoperability kernel, profiles, mappings, and purpose-specific projections can connect heterogeneous models.
- A catalog result is a projection with freshness and authorization limits, not proof of existence, correctness, permission, or fitness.
- Lineage edges state type, direction, granularity, scope, provenance, version, and time; visual adjacency alone is not causation.
- Inference, observation, manual assertion, imported claim, and authoritative decision are explicitly labeled.
- Metadata access can reveal sensitive schemas, identities, relationships, behavior, vulnerabilities, or business plans and is governed accordingly.
- Retirement preserves required identifiers and provenance while closing active publication, access, collection, dependencies, and recovery paths.

### Common failures

Common failures are equating metadata architecture with buying a catalog; using mutable names as identity; treating all metadata as “data about data”; forcing one schema on every domain; copying assertions without provenance; allowing crawlers to become semantic authorities; overwriting conflicting claims; confusing dataset, file, table, view, service, and product; drawing lineage with no transformation semantics; measuring populated fields instead of consumer outcomes; indexing sensitive metadata globally; retaining behavioral metadata indefinitely; publishing stale ownership; assuming technical schemas explain business meaning; breaking clients with metamodel changes; and deleting records so historical evidence becomes unintelligible.

### Compact example

Three assets—orders, customers, and customer-order facts—receive stable identifiers, accountable owners, current metadata versions, and three typed lineage edges. A small executable check verifies that all referenced endpoints exist and that no asset is orphaned from ownership. It reports three assets, complete owner and identifier coverage, three lineage edges, zero invalid edges, three current versions, and zero orphan assets. It does not prove semantic correctness, authentic ownership, complete lineage, authorized access, freshness, or consumer value.

### Connections

[DARCH-023](023-data-ownership-and-accountability.md), [DARCH-026](026-data-products-and-service-expectations.md), [DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-050](050-mapping-data-workloads-to-platforms-and-serving-systems.md), and [DARCH-060](060-designing-an-mdm-capability-without-centralizing-every-domain.md) establish ownership, product, contract, serving-system, and federated-capability boundaries. [DARCH-062](../ROADMAP.md) next examines metadata harvesting and synchronization.

## Governing Question

Metadata determines whether a person or machine can find an asset, distinguish it from another, interpret fields, learn who is accountable, assess provenance and quality, request access, understand transformations, observe operation, react to change, and know when use must end. When those functions are fragmented, an enterprise has descriptions but not a metadata architecture.

The governing question is which subjects, assertions, models, authorities, services, interfaces, controls, and lifecycle mechanisms create dependable meaning across domains without turning one catalog, graph, or team into an accidental universal source of truth.

## Why This Matters

NISO's [Understanding Metadata](https://www.niso.org/publications/understanding-metadata) describes structured information that supports description, explanation, location, retrieval, use, and management, and distinguishes descriptive, structural, and administrative functions. Enterprise architecture extends these ideas to data products, services, models, policies, pipelines, controls, and operational decisions.

NIST publishes [metadata and vocabulary standards for NIST data](https://data.nist.gov/od/dm/) using JSON-LD, JSON Schema, core and extension models, and mappings to public-data schemas. The example shows that one architecture can maintain an internal extensible model and produce governed external representations rather than require one serialization for every participant.

The Dublin Core Metadata Initiative's [metadata terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) define globally identified properties, classes, datatypes, and vocabulary schemes intended for combination in application profiles. W3C [RDF 1.1 Concepts and Abstract Syntax](https://www.w3.org/TR/2014/REC-rdf11-concepts-20140225/) supplies a graph model of subject-predicate-object statements, IRIs, literals, blank nodes, graphs, and datasets. Neither requires an enterprise to store all metadata in an RDF database.

W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) provides a vocabulary for describing datasets, data services, catalogs, distributions, versions, and related resources so metadata can be aggregated across catalogs. W3C [PROV-O](https://www.w3.org/TR/2013/REC-prov-o-20130430/) represents entities, activities, agents, and qualified provenance relations. W3C's [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/) supports quality dimensions, metrics, measurements, annotations, policies, and feedback.

W3C [SHACL](https://www.w3.org/TR/shacl/) defines shapes and validation reports for checking RDF graphs against declared conditions. [OpenLineage's object model](https://openlineage.io/docs/spec/object-model/) describes jobs, runs, datasets, events, and extensible facets for operational lineage. These technologies cover different concerns and can coexist through profiles and mappings.

The original [FAIR Guiding Principles](https://www.nature.com/articles/sdata201618) emphasize persistent identifiers, rich searchable metadata, standardized retrieval, shared knowledge-representation languages, qualified references, licenses, provenance, and domain standards. FAIR concerns do not prove quality, permission, privacy, or fitness, but they reveal why metadata must survive beyond one tool and remain usable by machines as well as people.

## Prerequisites and Retrieval

You should understand data architecture, data modeling, schemas, domains, identifiers, APIs, events, catalogs, search, graphs, semantics, provenance, lineage, quality, governance, access control, privacy, security, reliability, distributed systems, temporal data, versioning, organizational ownership, product management, and lifecycle engineering.

Retrieve resource, subject, representation, distribution, service, product, assertion, predicate, value, identifier, namespace, vocabulary, schema, metamodel, profile, mapping, crosswalk, registry, catalog, index, graph, provenance, lineage, quality measure, policy, owner, steward, crawler, emitter, inference, observation, snapshot, event, freshness, confidence, version, effective time, transaction time, correction, tombstone, retention, preservation, and closure.

As a retrieval test, inspect “customer_table is certified.” Ask which stable asset is meant, whether the object is a logical dataset, physical table, view, contract, or product, who made the certification, under which policy and use, what evidence and quality interval support it, when it became effective, whether it remains current, which representation carries the assertion, and who may see it. A badge without this context is decoration.

## Learning Objectives

After completing this module, you should be able to:

1. frame metadata as a governed architectural system rather than a catalog feature;
2. classify business, semantic, structural, operational, provenance, quality, governance, security, and behavioral metadata;
3. define stable subject identity, assertion provenance, authority, scope, time, status, and confidence;
4. design registries, repositories, graphs, indexes, catalogs, and embedded metadata as complementary components;
5. create an interoperability kernel, application profiles, mappings, and projections across heterogeneous domain models;
6. distinguish source metadata, observations, inferences, imports, approvals, conflicts, and corrections;
7. govern schemas, vocabularies, lineage, quality, access, versioning, and lifecycle together;
8. design metadata APIs, events, snapshots, validation, reconciliation, observability, and recovery;
9. evaluate metadata through consumer decisions, freshness, coverage, correctness, adoption, and operating cost; and
10. migrate and retire metadata services without losing required identity or historical interpretation.

## Core Exposition

**Begin with decisions and users.** Identify who needs metadata to discover, interpret, integrate, govern, operate, audit, secure, repair, or retire a resource.

Consumers include analysts, engineers, application owners, data scientists, stewards, security teams, privacy specialists, records managers, auditors, regulators, automated policy agents, orchestration systems, and incident responders. Each needs a different projection and assurance level.

**Define the subject universe.** Decide whether the architecture describes domains, concepts, terms, entities, attributes, datasets, tables, columns, files, streams, topics, APIs, events, models, dashboards, reports, policies, controls, jobs, runs, people, organizations, decisions, or incidents.

Do not model every possible subject at once. Start with consequential journeys and add subject types when they support a named outcome.

**Separate subject from metadata record.** A dataset can have several records in domain catalogs, registries, access systems, and lineage stores.

The records are representations of assertions about the dataset. Their identifiers, ownership, freshness, and authority must not be confused with the dataset's identity or state.

**Separate logical and physical resources.** A logical customer product can be represented by a table, API, event stream, snapshot, and historical archive.

Model each representation and its relationship to the logical product. Otherwise availability, schema, retention, quality, and access statements attach to the wrong object.

**Define stable identifiers.** Assign identifiers that remain stable across renames, moves, platform migrations, reorganizations, replicas, and changing display labels.

Document namespace owner, uniqueness boundary, issuance, opacity, resolution, aliases, redirects, merge, split, reuse prohibition, persistence, exposure, and retirement. A warehouse path is usually a locator, not a durable identity.

**Use typed relationships.** “Related to” cannot support precise navigation, impact analysis, or assurance.

Define relations such as represents, distribution-of, derived-from, generated-by, used-by, conforms-to, governed-by, owned-by, supersedes, replaces, cites, maps-to, exposes, depends-on, and invalidates. State direction and inverse behavior.

**Treat assertions as first-class.** Record subject, predicate, object or value, source, responsible agent, collection mechanism, scope, event time, effective time, record time, confidence, status, and supersession.

This makes conflicts and correction visible. A flattened current-value row can remain a serving projection, but it should not destroy evidence needed to explain the value.

**Distinguish authority from origin.** The system that emits a schema observation is the source of that observation, while a domain owner may hold semantic authority and a platform owner may approve technical registration.

Store each role. “Source system” does not answer who can define the field or accept risk from a breaking change.

**Distinguish observed, declared, inferred, and approved metadata.** A crawler may observe a column named `cust_id`; a domain contract may declare it a customer identifier; a classifier may infer that it is sensitive; a privacy owner may approve a classification.

These assertions can coexist. Label their basis and do not silently promote inference to authoritative policy.

**Classify business metadata.** Business metadata covers purpose, owner, steward, definition, business rule, criticality, use, outcome, audience, service expectation, issue channel, and lifecycle disposition.

It connects technical resources to accountable decisions. Free-text definitions alone are insufficient when identifiers, authorities, and effective times matter.

**Classify semantic metadata.** Semantic metadata covers concepts, terms, meanings, synonyms, exclusions, relationships, code schemes, mappings, units, classifications, and ontologies.

It explains what representations mean and where concepts differ. Semantic authority resides with the accountable domain or concept owner, not automatically with a catalog administrator.

**Classify structural metadata.** Structural metadata covers schemas, fields, datatypes, keys, constraints, partitions, formats, encodings, layouts, interfaces, and composition.

It can often be observed automatically, but observed structure may not equal the supported contract. Retain both and surface divergence.

**Classify administrative and governance metadata.** This includes ownership, stewardship, policy, classification, access conditions, license, retention, legal basis, certification, exception, control, review, and approval.

These assertions require authority and evidence. A populated owner field is not proof that the person accepted the role or still has mandate.

**Classify provenance and lineage metadata.** Provenance describes origins, activities, agents, generation, use, derivation, attribution, delegation, and time.

Lineage selects dependency and transformation paths for questions such as impact, reproducibility, audit, correction, or incident containment. It is a projection of provenance and execution evidence, not a universal graph.

**Classify operational metadata.** Record run identity, job and code version, inputs, outputs, parameters, start and end, state, error, retries, freshness, volume, latency, capacity, service objective, deployment, incident, and recovery evidence.

Operational metadata changes quickly and often needs streaming ingestion, bounded retention, aggregation, and observability distinct from curated definitions.

**Classify quality metadata.** Identify dimension, metric, method, population, sample, interval, threshold, result, uncertainty, exception, responsible owner, consumer use, and corrective action.

A green score with no metric version, population, time, or decision cannot support fitness. Quality metadata itself must be reproducible and protected from selective reporting.

**Classify behavioral metadata carefully.** Search, access, query, join, transformation, dashboard use, export, and feedback can improve discovery and reveal dependencies.

They can also expose personal behavior, sensitive investigations, commercial strategy, or security posture. Collect only justified events, minimize identifiers, restrict purpose, aggregate appropriately, set retention, and provide oversight.

**Define a metadata control plane.** The control plane coordinates identifiers, owners, models, profiles, policies, contracts, access, subscriptions, validation, change, evidence, and lifecycle.

It can integrate many repositories and indexes. Central coordination does not require every metadata assertion to reside in one database.

**Choose authoritative systems by assertion type.** A schema registry can own supported interface schemas, identity management can own workforce principal status, a domain registry can own terms, and an orchestrator can own run observations.

Publish an authority matrix at subject-predicate granularity where collisions matter. Avoid declaring one catalog authoritative for facts it merely imports.

**Use a federated architecture.** Domains publish contextual metadata products and shared services provide identity, exchange, validation, graph, search, policy, and observability capabilities.

Enterprise governance defines interoperability and control invariants. Federation fails if domains lack ownership, capacity, or incentives, or if shared services hide arbitrary central semantics.

**Define the interoperability kernel.** Include stable subject identifier, subject type, assertion identifier, predicate identifier, value representation, source, authority, version, effective and observation times, status, provenance, protection, and extension mechanism.

Keep the kernel small and stable. Domain-specific models remain richer and expose projections into the kernel for cross-domain functions.

**Use vocabularies and namespaces.** Globally or organizationally stable term identifiers prevent identical labels from implying identical meaning.

Define namespace governance, term status, definition, domain and range where applicable, examples, mappings, effective time, deprecation, and replacement. Labels can vary by language and audience without changing identity.

**Use schemas for structure.** Schemas define record and message shape, datatype, requiredness, cardinality, constraints, composition, and extensibility.

Schema conformance does not prove semantic truth. A syntactically valid owner identifier can still refer to the wrong or inactive person.

**Use application profiles for bounded use.** A profile selects terms from multiple vocabularies, constrains cardinality and representation, adds obligations, and declares validation and extension policy for a community.

Profiles allow interoperability without forcing every publisher to adopt every term. Version the profile and identify compatible predecessors and successors.

**Use mappings as governed assets.** A mapping states source and target term or shape, versions, relation strength, direction, transformation, loss, condition, owner, evidence, effective time, and lifecycle status.

Exact equivalence is rare. Broader, narrower, close, derivable, and incompatible relations should remain distinct.

**Support multiple representations.** The same assertions may be served as JSON, JSON-LD, RDF, CSV, relational views, search documents, or generated documentation.

Define one semantic contract and representation-specific profiles. Test round trips only where they are expected to preserve meaning; document information loss elsewhere.

**Distinguish registry, repository, graph, index, and catalog.** A registry governs definitions and status; a repository persists records; a graph supports relationships; an index accelerates retrieval; a catalog presents discovery and workflow.

One product may implement several roles, but the responsibilities remain separable for replacement, scaling, and assurance.

**Keep metadata near the source when useful.** Embedded schemas, code annotations, manifests, configuration, and deployment descriptors can remain versioned with the resource.

Publish them into shared services for discovery and cross-domain use. Avoid a central copy that loses source linkage, and avoid source-only metadata that no consumer can find.

**Define collection contracts.** Producers declare emitted assertions, identity, schema, version, cadence, ordering, completeness, deletion, correction, replay, protection, and service expectations.

Collectors declare validation, authentication, deduplication, isolation, acknowledgment, quarantine, retention, and error feedback. DARCH-062 develops harvesting and synchronization in depth.

**Design APIs around subject and assertion identity.** Support lookup by stable identifier, typed search, relationship traversal, version and time selection, provenance retrieval, change feed, feedback, and correction status.

Use authorization at subject, predicate, relationship, representation, and purpose boundaries where required. Search result counts and existence can themselves be sensitive.

**Design events for change, not replacement of state retrieval.** Events carry assertion or subject identity, source, type, version, effective time, changed predicates, provenance pointer, and compatibility class.

Consumers still need an authorized current-state or versioned retrieval path. Define duplicate, order, replay, gap, correction, tombstone, and subscription semantics.

**Version independently where change differs.** Vocabulary, schema, profile, mapping, assertion, resource, distribution, service, and API versions need not advance together.

Record dependency constraints and effective intervals. One global metadata version creates unnecessary coordinated releases and hides which contract changed.

**Model bitemporal metadata where needed.** Effective time states when an assertion applies to its subject; record time states when the metadata system learned or changed the assertion.

This supports questions such as “who was the owner on the incident date?” and “what did the catalog report when the decision was made?” Do not overwrite retroactive corrections.

**Represent conflict explicitly.** Two domains can publish different classifications or definitions due to scope, jurisdiction, observation time, or genuine disagreement.

Store both assertions, authority boundaries, evidence, and status. A purpose-specific projection may choose one, but the decision rule and discarded alternatives remain inspectable.

**Represent absence carefully.** Missing owner can mean not collected, not applicable, unknown, withheld, deleted, pending approval, or collection failure.

Use explicit states where consequence warrants them. A blank string should not collapse these meanings.

**Validate at boundaries.** Check identifier syntax, resolvability, subject type, term identity, datatype, cardinality, required provenance, owner status, temporal consistency, relationship endpoints, policy references, and profile conformance.

Separate violation, warning, information, and unavailable validation. Never silently drop rejected metadata; quarantine with bounded retention and owner-visible feedback.

**Validate semantics through accountable review.** Automated constraints cannot establish that a business definition is meaningful, a mapping is legitimate, or a quality measure fits a consumer decision.

Combine machine checks with domain review, consumer feedback, sampled evidence, and independent assurance for high-consequence claims.

**Measure metadata quality contextually.** Dimensions can include completeness, validity, consistency, accuracy evidence, uniqueness, freshness, provenance, accessibility, interpretability, and stability.

Measure by subject type, predicate, authority, domain, consumer journey, and time. Weighting everything into one enterprise score obscures harmful gaps.

**Design lineage granularity by question.** Dataset-level lineage supports broad impact; field-level lineage supports sensitive-field tracing; record-level provenance can support disputes but can be expensive and invasive.

Code and parameter capture may be necessary for reproducibility. Choose granularity by consequence, cost, data volume, retention, and privacy.

**Qualify lineage edges.** State operation, inputs, outputs, run, code version, parameters, time, environment, confidence, collection mechanism, and completeness boundary.

A manually declared dependency and an observed successful run are different evidence. A graph should let consumers distinguish them.

**Avoid false causality.** Query access, temporal order, and shared names do not prove derivation.

Use terms such as read-by, referenced-by, joined-with, copied-from, transformed-from, and statistically-associated-with accurately. Inferred lineage must expose method and confidence.

**Connect policy to enforcement.** Metadata can declare classification, permitted use, retention, residency, license, and access conditions.

Controls must bind those assertions to authorization, masking, movement, deletion, monitoring, and evidence. Policy metadata alone does not protect data.

**Protect the metadata system.** Threats include ownership takeover, classification downgrading, lineage erasure, schema poisoning, search enumeration, behavioral surveillance, secret leakage, denial of discovery, and dependency-graph reconnaissance.

Use strong identities, least privilege, separation of duties, signing or integrity evidence where warranted, audit, anomaly detection, backups, and tested recovery.

**Define visibility tiers.** Public metadata can support broad discovery; internal metadata may reveal business design; restricted metadata can expose personal, security, contractual, or regulatory information.

Serve safe projections instead of either publishing everything or hiding the whole asset. Existence, owner contact, schema field names, sample values, lineage edges, and usage counts can have different tiers.

**Design for availability and degradation.** Decide whether production writes, pipeline execution, access decisions, and incident response depend synchronously on metadata services.

Cache signed or versioned policy bundles where safe, define bounded stale behavior, and fail closed for selected high-risk operations. A catalog outage should not necessarily stop every data flow.

**Observe the architecture itself.** Track ingestion lag, rejected assertions, unresolved identities, stale owners, broken links, failed validations, event gaps, index delay, graph errors, search latency, access denials, correction time, recovery tests, and consumer version adoption.

Trace a user-visible result back to source assertions and projection logic. Otherwise the metadata plane cannot explain its own behavior.

**Reconcile stores and projections.** Compare authoritative source versions, registry definitions, repository records, graph edges, search documents, catalog pages, caches, and consumer acknowledgments.

Define tolerances, owners, repair, replay, and escalation. A successful crawl does not prove that the current index or catalog view is correct.

**Provide correction workflows.** Feedback names subject, assertion, observed problem, evidence, reporter, affected use, urgency, responsible owner, decision, correction, propagation, and closure.

Protect reporters and sensitive evidence. Measure recurrence and downstream repair, not only ticket closure.

**Treat certification as a governed assertion.** Define certifying authority, policy, scope, evidence, level, consumer uses, effective and expiry times, monitoring, revocation, and appeal.

Certification does not eliminate consumer fitness assessment. A resource can be certified for one purpose and unsafe for another.

**Fund metadata as a product and platform.** Domains fund contextual definition and product obligations; shared funding supports identifiers, exchange, graph, search, policy, validation, and common reliability.

Budget consumer integration, stewardship, correction, model evolution, recovery, and retirement. A one-time catalog implementation cannot sustain living metadata.

**Measure consumer outcomes.** Track discovery-to-understanding time, successful access request, integration lead time, prevented misuse, impact-analysis completeness, incident containment, reproducibility, correction time, contract adoption, and retired dependency closure.

Also track operational cost, platform reuse, manual curation, stale assertions, search abandonment, feedback quality, and false inference. Field population is only a coverage measure.

**Evolve through compatibility contracts.** Classify changes to terms, schema, profile, mappings, APIs, events, search behavior, and authorization.

Offer versioned representations, deprecation windows, migration guidance, test fixtures, consumer registration, activation evidence, and rollback or compensation. Never reinterpret an existing identifier incompatibly.

**Migrate incrementally.** Inventory current systems, owners, identifiers, models, assertions, interfaces, consumers, controls, evidence, and retention before choosing a target.

Create stable crosswalks, dual-publish bounded subjects, compare projections, migrate consumers by cohort, preserve history, and close old writers only after reconciliation and acceptance.

**Retire without erasing meaning.** Preserve persistent identifiers, required definitions, versions, provenance, mappings, and tombstones so historical records remain interpretable.

Close active collection, publication, subscriptions, access, credentials, indexes, caches, behavioral tracking, contracts, exceptions, support, and recovery. Metadata can outlive data, but only under explicit preservation and protection decisions.

## Definitions and Notation

Let:

- `S` be the set of identified metadata subjects;
- `A` be the set of metadata assertions;
- `P` be the set of predicate or term identifiers;
- `R` be the set of typed relationships;
- `U` be the set of accountable authorities and service owners;
- `V` be the set of vocabularies, schemas, profiles, and mappings;
- `C` be the set of consumers and declared uses;
- `T` be the set of effective and record-time intervals;
- `E` be the set of evidence, provenance, and validation results; and
- `L` be the set of active and historical lifecycle obligations.

Define an assertion:

`a = (id, subject, predicate, value, source, authority, scope, effective_time, record_time, status, confidence, provenance)`

Not every predicate needs every optional dimension, but the profile must require dimensions whose absence could alter interpretation or consequence.

Define referential integrity:

`ValidEdges(R, S) = forall r in R : source(r) in S and target(r) in S and type(r) is declared`

This proves only that relationship endpoints and types are registered, not that the relationship is true, complete, authorized, or current.

Define authoritative coverage for required predicates `P_req(s)`:

`Covered(s) = forall p in P_req(s), exists a in A : a.subject = s and a.predicate = p and Active(a) and Authorized(a.authority, s, p)`

Several assertions can remain active for different scopes or jurisdictions. Coverage must not flatten legitimate plurality.

Define a metadata projection for consumer `c`:

`Projection(c) = select(authorized(c), compatible(c), purpose(c), time(c), profile(c), assertions(S))`

Search, catalog, API, and graph views are projections. Their omission of an assertion is not proof that the assertion or subject does not exist.

Define freshness for assertion `a` relative to a declared interval `delta`:

`Fresh(a, now, delta) = now - observed_at(a) <= delta and source_version(a) = reconciled_version(a)`

Freshness says nothing about semantic accuracy or fitness. A freshly copied error remains an error.

The assurance predicate is:

`FitMetadata = Scoped and Identified and Owned and Modeled and Profiled and Provenanced and Validated and Interoperable and Discoverable and Protected and Observable and Correctable and Recoverable and Evolvable and Closable`

Each term requires evidence for named subjects, assertions, consumers, purposes, and times. The predicate is a review structure, not a proof of universal truth.

## Mechanisms, Invariants, or Proof Structure

**Outcome gate.** Name consumer decisions, operational journeys, obligations, harms, and evidence needs before selecting catalog or graph technology.

**Subject gate.** Distinguish logical resource, representation, distribution, service, schema, process, run, policy, person, and decision identities.

**Identifier gate.** Verify namespace authority, uniqueness, opacity, resolution, aliases, redirects, non-reuse, persistence, and retirement.

**Assertion gate.** Require subject, predicate, value, source, authority, scope, time, status, confidence where applicable, and provenance.

**Model gate.** Govern vocabularies, schemas, profiles, mappings, constraints, versions, extension, and deprecation without assuming one universal metamodel.

**Authority gate.** Allocate semantic, structural, operational, provenance, quality, policy, security, and service ownership at meaningful granularity.

**Exchange gate.** Define APIs, events, snapshots, representations, compatibility, authorization, retry, replay, correction, tombstone, and feedback contracts.

**Graph gate.** Validate endpoint identity, relation type, direction, granularity, temporal scope, provenance, confidence, and access boundaries.

**Quality gate.** Measure metadata completeness, validity, consistency, freshness, provenance, accessibility, interpretability, and stability for named uses.

**Protection gate.** Apply classification, purpose, minimization, access, integrity, confidentiality, retention, deletion, audit, and incident controls to metadata itself.

**Projection gate.** Make selection, inference, ranking, aggregation, staleness, authorization, and limitations visible in catalog, search, API, and graph results.

**Operations gate.** Set service objectives, capacity, observability, degradation, continuity, recovery, reconciliation, support, and correction ownership.

**Evolution gate.** Version terms, schemas, profiles, mappings, assertions, interfaces, and projections independently with compatibility and consumer activation evidence.

**Economic gate.** Fund domain publication, shared services, consumer adoption, stewardship, assurance, correction, migration, preservation, and retirement.

**Lifecycle gate.** Preserve required identity and meaning while closing active collection, publication, access, dependencies, behavioral tracking, and recovery paths.

### Executable evidence: metadata-architecture-minimum-contract

This Python example checks a tiny inventory with stable identifiers, owners, current versions, and typed lineage whose endpoints all exist.

<!-- bijux-verify: {"id":"metadata-architecture-minimum-contract","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"assets=3\nowner_coverage=3\nstable_ids=3\nlineage_edges=3\ninvalid_edges=0\ncurrent_versions=3\norphan_assets=0\n","stderr":""}} -->
```python
assets = {
    "urn:bijux:data:orders": {"owner": "order_domain", "version": "7", "current": True},
    "urn:bijux:data:customers": {"owner": "customer_domain", "version": "4", "current": True},
    "urn:bijux:data:customer-orders": {"owner": "analytics_domain", "version": "12", "current": True},
}

lineage = [
    ("urn:bijux:data:orders", "derived_into", "urn:bijux:data:customer-orders"),
    ("urn:bijux:data:customers", "derived_into", "urn:bijux:data:customer-orders"),
    ("urn:bijux:data:customer-orders", "depends_on", "urn:bijux:data:orders"),
]

declared_relations = {"derived_into", "depends_on"}
invalid_edges = [
    edge
    for edge in lineage
    if edge[0] not in assets or edge[2] not in assets or edge[1] not in declared_relations
]
owner_coverage = sum(bool(asset["owner"]) for asset in assets.values())
stable_ids = sum(identifier.startswith("urn:bijux:data:") for identifier in assets)
current_versions = sum(asset["current"] and bool(asset["version"]) for asset in assets.values())
orphan_assets = sum(not asset["owner"] for asset in assets.values())

print(f"assets={len(assets)}")
print(f"owner_coverage={owner_coverage}")
print(f"stable_ids={stable_ids}")
print(f"lineage_edges={len(lineage)}")
print(f"invalid_edges={len(invalid_edges)}")
print(f"current_versions={current_versions}")
print(f"orphan_assets={orphan_assets}")
```

The expected output reports `assets=3`, `owner_coverage=3`, `stable_ids=3`, `lineage_edges=3`, `invalid_edges=0`, `current_versions=3`, and `orphan_assets=0` on separate lines.

The evidence is deliberately narrow. Prefix matching does not prove persistent or globally unique identity. Nonempty owner strings do not prove acceptance, authority, competence, or current employment. Endpoint existence does not prove a lineage relation is complete, causal, current, authorized, or observed. Version strings do not prove compatibility. Production assurance requires source reconciliation, semantic review, representative validation, access and threat testing, failure and recovery exercises, consumer evidence, correction traces, and accountable approval.

## Alternatives and Trade-Offs

**Central repository.** One store simplifies search, joins, policy, and backup but concentrates scale, availability, authorization, model-change, and migration risk. It becomes harmful when it silently owns imported meaning.

**Federated repositories.** Domain stores preserve context, autonomy, and local availability. Cross-domain discovery and assurance require shared identity, exchange, profiles, reconciliation, and dependable domain operation.

**Knowledge graph.** A graph represents typed relationships and flexible extension well. It does not automatically provide correct semantics, provenance, authorization, temporal behavior, or acceptable query cost.

**Relational registry.** Tables and constraints support governance, transactions, and familiar operation. Deep or evolving relationships can require more joins and schema changes; graph projections can complement the registry.

**Search index.** Search supports discovery, relevance, faceting, and broad text retrieval. An index is a delayed derived projection and should not become the authority for corrections or exact current state.

**Embedded metadata.** Metadata versioned beside code or data can remain close to the source and review workflow. It is hard to search and govern across repositories without publication and stable identity.

**Push events.** Events reduce discovery lag and support change-driven consumers. They introduce duplicate, order, gap, replay, authorization, and retention concerns and need snapshot reconciliation.

**Pull harvesting.** Pull can isolate producers and simplify recovery from missed changes. It adds detection lag, load, cursor, deletion, and overlap problems; DARCH-062 compares synchronization mechanisms.

**One enterprise metamodel.** A shared model can reduce mapping for stable common concepts. Broad scope creates coordination bottlenecks and lowest-common-denominator semantics; use profiles and extensions.

**Independent domain models.** Local models maximize fit and speed. Without mappings and an interoperability kernel, consumers bear repeated integration cost and cannot perform dependable enterprise impact analysis.

**Automated inference.** Classifiers and parsers scale metadata generation and reveal hidden assets. They produce uncertain claims and bias; preserve confidence, method, evidence, review, and correction.

**Manual curation.** Human expertise handles meaning and nuance. It is slow, inconsistent, and difficult to keep fresh; focus review on consequential semantics while automating observable facts.

## Failure Modes and Misconceptions

1. **“A catalog is the architecture.”** A catalog is one discovery and workflow projection over a larger system.
2. **“Metadata is merely data about data.”** It also describes services, processes, policies, people, decisions, operations, and preservation.
3. **“The table name is its identifier.”** Names and locations change and can be reused.
4. **“The crawler is authoritative.”** A crawler observes; authority depends on the assertion type and governance.
5. **“Schema equals semantics.”** Structure constrains representation but does not establish business meaning or legitimate use.
6. **“One model enables interoperability.”** Interoperability also needs profiles, mappings, versions, contracts, and compatible behavior.
7. **“A graph makes relationships true.”** Edges require provenance, type, scope, time, validation, and authority.
8. **“Lineage proves causation.”** Access, adjacency, and temporal order can be observational rather than causal.
9. **“More fields mean richer metadata.”** Unused, stale, contradictory, or unauthoritative fields increase confusion.
10. **“Search results are complete.”** Authorization, indexing lag, ranking, model scope, and failures shape the projection.
11. **“Certification is permanent.”** It is scoped, evidenced, monitored, expiring, and revocable.
12. **“Metadata can be public because data is protected.”** Metadata can reveal identities, vulnerabilities, relationships, and strategy.
13. **“Usage telemetry is harmless.”** Behavioral metadata can reveal people, investigations, intentions, and confidential work.
14. **“Fresh means correct.”** A current assertion can be false, semantically wrong, or unfit for a use.
15. **“Validation proves quality.”** Constraint conformance covers declared rules, not truth, completeness, or benefit.
16. **“Centralization removes conflicts.”** It can overwrite rather than resolve legitimate scoped disagreement.
17. **“Metadata migration is simple copying.”** Identity, authority, history, mappings, clients, and controls must migrate.
18. **“Deleting a catalog completes retirement.”** Active sources, subscriptions, indexes, caches, access, evidence, and recovery remain.

## Worked Examples

### Example 1

A retailer gives a logical orders product one stable identifier and links its table, stream, API, daily snapshot, and archive as distinct distributions. Availability attaches to services, file format to distributions, and semantic ownership to the product. Search users see one product rather than five apparent datasets, while engineers can inspect representation-specific contracts.

### Example 2

A crawler observes a `national_id` column and a classifier marks it likely sensitive at confidence 0.91. The domain owner confirms a more restrictive classification under a named policy. The architecture retains observation, inference, and approval as separate assertions, prevents low-confidence automation from downgrading policy, and records propagation to access controls.

### Example 3

Two domains use “active customer” differently: commerce means an order in 12 months; support means an open entitlement. Each term has its own identifier and authority. A reporting profile maps both to a broader engagement concept with explicit conditions and loss, rather than redefining either domain term.

### Example 4

A research catalog publishes DCAT-compatible dataset and distribution metadata while retaining a richer domain profile for instruments, samples, and calibration. Stable identifiers and mappings allow external aggregation. Restricted location and subject metadata remain in an authorized projection, demonstrating that interoperability does not require universal visibility.

### Example 5

An analytics pipeline emits run, job, input, output, code-version, and state events. Dataset-level lineage supports impact analysis, while selected high-risk transformations capture field derivations and parameters. Failed runs remain operational evidence but do not assert that their proposed outputs became current products.

### Example 6

An owner changes departments after an incident. Bitemporal assertions show that the person was accountable on the incident date, that the registry learned of a retroactive correction later, and that a successor now owns the asset. An overwritten current owner field could answer none of these audit questions reliably.

### Example 7

A metadata search index remains available while the authoritative registry is unreachable. The interface marks results stale, suppresses high-risk certification status beyond its cache interval, and blocks ownership changes. Discovery degrades gracefully without letting a derived index accept authoritative writes.

### Example 8

A lineage graph infers dependencies from SQL parsing and query logs. It labels parser-derived and observed-read edges separately, records confidence and observation interval, and asks owners to approve critical transformations. The system avoids claiming complete causality when dynamic SQL and external processes are outside collection scope.

### Example 9

A bank gives schema names internal visibility but restricts sample values, sensitive classifications, behavioral queries, and incident-linked lineage. Different projections support general discovery, engineering integration, and authorized investigations. The architecture logs enumeration attempts without exposing restricted subject existence.

### Example 10

A legacy catalog is replaced by a federated registry and search platform. Stable identifiers and historical versions move first; sources dual-publish and projections are reconciled; consumers migrate by cohort; old write paths close; caches and subscriptions expire; required tombstones persist; and recovery tests prove the legacy service cannot resume publication.

## Cross-Program Connections

- **Data engineering:** schemas, run events, manifests, quality results, lineage capture, reconciliation, backfills, and retention produce and consume operational metadata.
- **API and service engineering:** resource identity, representations, typed links, conditional changes, compatibility, authorization, pagination, events, errors, and deprecation shape metadata contracts.
- **Platform engineering:** self-service publication, registries, search, graphs, policy, tenancy, observability, recovery, support, and cost management provide reusable capabilities.
- **Database engineering:** catalogs, constraints, transactions, temporal tables, logs, indexes, query plans, and recovery records supply technical and operational evidence.
- **Distributed systems engineering:** identity, partial failure, replication, ordering, idempotency, convergence, partitions, and clocks govern synchronization and projection behavior.
- **Security and privacy engineering:** classification, purpose, minimization, authorization, integrity, confidentiality, audit, threat analysis, and retention constrain metadata itself.
- **Software architecture:** bounded contexts, contracts, dependency direction, representations, anti-corruption layers, and evolutionary compatibility shape federated models.
- **Knowledge representation:** identifiers, vocabularies, ontologies, graphs, inference, shapes, mappings, and provenance support semantic interoperability.
- **Reliability engineering:** objectives, dependency failure, stale modes, event gaps, reconciliation, continuity, recovery, and incident evidence define service trust.
- **Organizational design:** semantic authority, domain ownership, platform ownership, stewardship, incentives, funding, escalation, and succession determine whether metadata stays current.

## References

1. NISO, [“Understanding Metadata”](https://www.niso.org/publications/understanding-metadata), 2004. Retrieved 2026-09-03.
2. NIST, [“Metadata and Vocabulary Standards for NIST Data”](https://data.nist.gov/od/dm/). Retrieved 2026-09-03.
3. Dublin Core Metadata Initiative, [“DCMI Metadata Terms”](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/), 2020. Retrieved 2026-09-03.
4. W3C, [“RDF 1.1 Concepts and Abstract Syntax”](https://www.w3.org/TR/2014/REC-rdf11-concepts-20140225/), 2014. Retrieved 2026-09-03.
5. W3C, [“Data Catalog Vocabulary (DCAT) — Version 3”](https://www.w3.org/TR/vocab-dcat-3/), 2024. Retrieved 2026-09-03.
6. W3C, [“PROV-O: The PROV Ontology”](https://www.w3.org/TR/2013/REC-prov-o-20130430/), 2013. Retrieved 2026-09-03.
7. W3C, [“Data on the Web Best Practices: Data Quality Vocabulary”](https://www.w3.org/TR/vocab-dqv/), 2016. Retrieved 2026-09-03.
8. W3C, [“Shapes Constraint Language (SHACL)”](https://www.w3.org/TR/shacl/), 2017. Retrieved 2026-09-03.
9. OpenLineage, [“Object Model”](https://openlineage.io/docs/spec/object-model/). Retrieved 2026-09-03.
10. Mark D. Wilkinson et al., [“The FAIR Guiding Principles for scientific data management and stewardship”](https://www.nature.com/articles/sdata201618), *Scientific Data* 3, 2016. Retrieved 2026-09-03.

## Exercises

### Exercise 1

Design a metadata subject and identity model for a data product exposed through a table, API, event stream, daily files, and archived versions. Show which assertions attach to the logical product, distributions, services, schemas, and runs.

### Exercise 2

Customer and risk domains publish conflicting sensitivity, ownership, and retention assertions for the same physical table. Design an assertion, authority, scope, temporal, conflict, projection, and escalation model that does not overwrite legitimate context.

### Exercise 3

Create a federated metadata architecture for ten domains using different schemas and tools. Specify the interoperability kernel, profiles, mappings, registries, graph, index, APIs, events, authorization, validation, reconciliation, and service ownership.

### Exercise 4

A catalog claims 97 percent metadata completeness and 20,000 monthly users. Design a scorecard that evaluates discovery, understanding, integration, governance, lineage, correction, security, reliability, consumer adoption, and cost without collapsing them into one score.

### Exercise 5

Plan migration from a central catalog with path-based identifiers and overwritten current values to a federated, versioned metadata architecture. Include identity crosswalks, history, source cutover, consumer migration, correction, preservation, and retirement evidence.

## Answers to the Exercises

### Answer 1

Give the logical product a stable opaque identifier and attach purpose, semantic owner, steward, business definition, governed entities, quality commitments, consumer uses, support, classification, change policy, and lifecycle. Give every table, API representation, event stream, file series, and archive a distinct distribution or service identifier linked by `distribution-of` or `exposes`. Attach locator, format, schema binding, availability, freshness, access method, retention, and service owner at the representation boundary where each differs. Do not put API latency on the logical product or use a table path as the product identity.

Identify schema versions separately and link each distribution or event type to the supported profile and compatibility policy. Runs receive immutable identifiers with job and code version, input and output identifiers, parameters, times, states, and provenance; a failed run does not make its proposed output current. Version assertions bitemporally where later correction matters. Catalog and API views select authorized current assertions but allow historical retrieval. Validate identifiers, relationship endpoints, required ownership, schema compatibility, temporal coherence, and provenance. Reconcile source contracts, registry records, graph edges, search projections, and active consumer versions.

### Answer 2

Represent each claim as an assertion with its own identifier, stable table subject, predicate, value, source, accountable authority, jurisdiction or use scope, effective interval, record time, policy and evidence, status, and confidence if inferred. The customer domain can own business semantics; security or privacy authority can own enterprise minimum classification; records or legal owners can set retention under applicable obligations; platform custody does not acquire those decision rights. A physical table can inherit several requirements, and the effective control uses the applicable precedence and most protective compatible requirement rather than a catalog administrator's last write.

Retain conflicts in the authoritative assertion store and open an issue with affected consumer, control, and risk owners. Projections explain which assertion was selected, the policy rule, unresolved dissent, freshness, and limitations. Different jurisdictions may legitimately see different effective assertions. Changes propagate to access, masking, retention, monitoring, and consumer contracts and are reconciled. Escalate contradictory mandates to the authorized legal or operational risk owner; never let the metadata platform accept risk. Preserve superseded assertions and decisions for audit while restricting sensitive evidence.

### Answer 3

Let each domain own semantic definitions, domain profiles, product descriptions, supported schemas, quality evidence, correction, and publication service. Shared teams own subject and term namespaces, exchange contracts, validation services, graph and search projections, authorization integration, observability, reconciliation, recovery, and support. Enterprise governance owns minimum protection, provenance, ownership, compatibility, lifecycle, and evidence invariants plus cross-domain arbitration. Publish an authority matrix by subject and predicate.

The kernel contains subject and assertion identifiers, subject type, term identifier, value representation, source, authority, scope, effective and record times, version, status, provenance, protection, and extensions. Domains map their schemas into versioned application profiles rather than adopting one universal model. Registries govern terms, profiles, identifiers, and statuses; repositories keep assertions and history; a graph serves typed relationships; an index serves authorized discovery; catalogs present workflows. APIs support identity, version, time, provenance, feedback, and correction; events carry changes and tombstones; snapshots recover gaps. Validation checks syntax and profiles, while accountable review checks meaning. Reconciliation compares domain versions through projections and consumer acknowledgments. Service objectives cover lag, search, graph, recovery, correction, and bounded stale modes.

### Answer 4

First expose the completeness denominator: required predicates by subject type, criticality, domain, use, time, and profile. Separate populated, valid, authoritative, current, provenanced, and consumer-accepted coverage. User count needs unique human and machine consumers, eligible population, meaningful actions, purpose, repeat use, failures, and privacy-safe aggregation; traffic alone can reflect bots or frustrated search.

Measure discovery success, search abandonment, time to identify the right product, and unauthorized existence leakage. Measure understanding through definition and contract comprehension, mapping ambiguity, support questions, and integration rework. Measure lineage by declared scope, observed and approved edges, broken endpoints, impact-analysis recall samples, and correction. Measure governance through active accepted owners, policy-to-control bindings, certification expiry, issue closure, and recurrence. Measure freshness, event gaps, index lag, API reliability, stale-mode use, recovery tests, access violations, and incident containment. Measure contract adoption, current consumer activation, correction propagation, retired dependencies, platform reuse, manual curation, domain effort, infrastructure cost, and cost per successful journey. Keep dimensions separate, state confidence and limitations, and assign corrective owners.

### Answer 5

Inventory subjects, path identifiers, aliases, models, current values, historical exports, sources, owners, consumers, APIs, searches, lineage, policies, access, event feeds, caches, contracts, retention, backups, and recovery automation. Define durable identifiers and create versioned crosswalks from every old path, including collisions, renames, splits, merges, replicas, and reused names. Classify which old values are authoritative assertions, observations, inferences, or unknown-origin claims. Recover source and effective times where evidence permits and label uncertainty rather than invent history.

Establish the interoperability kernel, domain profiles, authority matrix, assertion history, protection policy, APIs, events, snapshots, validation, and reconciliation. Migrate one bounded subject class and consumer journey at a time. Dual-publish from authoritative sources, compare current and historical projections, sample semantic accuracy, test sensitive access and correction, migrate consumers by cohort, and retain rollback or compensation. Freeze new legacy integrations early. Close legacy writes only after domain acceptance and consumer activation are evidenced. Preserve identifiers, definitions, versions, mappings, tombstones, provenance, and required audit history. Disable crawlers, feeds, subscriptions, credentials, indexes, caches, behavioral tracking, support, and funding; delete unnecessary copies; update ownership; and test that backups and automation cannot resurrect active publication. Retirement remains open while any consumer or obligation depends on the old service.
